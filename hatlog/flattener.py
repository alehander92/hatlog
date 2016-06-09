import ast
import re
from collections import defaultdict
from hatlog.env import Env

def flatten(root):
    if len(root.body) != 1 or not isinstance(root.body[0], ast.FunctionDef):
        raise ValueError("hatlog supports expects a function")
    x = Flattener()
    x.flatten(root.body[0])
    return [x.nodes, root.body[0].name]

NOT_SUPPORTED = defaultdict(set,
    FunctionDef={'keywords', 'starargs', 'kwargs'},
    BinOp={'op'},
    UnaryOp={'op'},
    AugAssign={'op'},
    Call={'keywords', 'starargs', 'kwargs'},
    For={'orelse'},
    Attribute={'ctx'})

class Flattener:
    def __init__(self):
        self.env = {}
        self.nodes = []
        self.type_index = -1
        self.env = Env()
        self.args = []
        self.return_type = None
        self.function = ''

    def flatten(self, node):
        if isinstance(node, list):
            f = [self.flatten(e) for e in node]
            return f
        elif node is None:
            return 'v'
        else:
            sub = getattr(
                self,
                'flatten_%s' % type(node).__name__.lower(),
                self.default)
            return sub(node)

    def default(self, node):
        f = [self.flatten(getattr(node, f)) for f in node._fields if f not in NOT_SUPPORTED[type(node).__name__]]
        node_type = self.new_type()
        self.nodes.append(('z_%s' % self.to_snake_case(type(node).__name__), f, node_type))
        return node_type

    def flatten_call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.function:
            return self.flatten_rec(node)
        elif isinstance(node.func, ast.Attribute):
            return self.flatten_method_call(node)
        else:
            function = self.flatten(node.func)
            args = [self.flatten(e) for e in node.args]
            return_type = self.new_type()

            if isinstance(node.func, ast.Name) and node.func.id not in self.env.values: # named
                self.nodes.append(('z_call', [node.func.id, args], return_type))
            else:
                self.nodes.append(('z_fcall', [function, args], return_type))

            return return_type

    def flatten_subscript(self, node):
        value = self.flatten(node.value)
        node_type = self.new_type()
        if isinstance(node.slice, ast.Index):
            index = self.flatten(node.slice.value)
            self.nodes.append(('z_index', [value, index], node_type))
        else:
            lower = self.flatten(node.slice.lower) if node.slice.lower else None
            upper = self.flatten(node.slice.upper) if node.slice.upper else None
            if lower and upper is None:
                upper = lower
            elif lower is None and upper:
                lower = upper
            else:
                raise ValueError('hatlog expects only slice like [:x], [x:] or [x:y]')
            self.nodes.append(('z_slice', [value, lower, upper], node_type))
        return node_type

    def flatten_num(self, node):
        if isinstance(node.n, int):
            return 'int'
        else:
            return 'float'

    def flatten_rec(self, node):
        '''
        we know that functions return the same value
        prolog terms cant be rec so we =
        '''
        if len(node.args) != len(self.args):
            raise ValueError("%s expected %d args" % (len(self.args)))
        for a, (_, b) in zip(node.args, self.args):
            c = self.flatten(a)
            self.nodes.append(('=', [c], b))
        return self.return_type

    def flatten_str(self, node):
        return 'str'

    def flatten_compare(self, node):
        if len(node.comparators) != 1:
            raise ValueError("hatlog supports only 1 comparator")
        if isinstance(node.ops[0], ast.Eq):
            op = 'z_eq'
        else:
            op = 'z_cmp'
        a = self.flatten(node.left)
        b = self.flatten(node.comparators[0])
        node_type = self.new_type()
        self.nodes.append((op, [a, b], node_type))
        return node_type

    def flatten_list(self, node):
        if len(node.elts) == 0:
            sub_types = [self.new_type()]
        else:
            sub_types = [self.flatten(a) for a in node.elts]
        node_type = self.new_type()
        self.nodes.append(('z_list', sub_types, node_type))
        return node_type

    def flatten_method_call(self, node):
        '''
        A call with an
        attribute as func
        '''
        receiver = self.flatten(node.func.value)
        args = list(map(self.flatten, node.args))
        node_type = self.new_type()
        self.nodes.append(('z_method_call', [receiver, node.func.attr, args], node_type))
        return node_type


    def flatten_dict(self, node):
        if len(node.keys) == 0:
            sub_types = [self.new_type(), self.new_type()]
        else:
            sub_types = zip([self.flatten(a) for a in node.keys], [self.flatten(b) for b in node.values])
        node_type = self.new_type()
        self.nodes.append(('z_dict', sub_types, node_type))
        return node_type

    def flatten_assign(self, node):
        if len(node.targets) != 1:
            raise ValueError("assignment normal")
        node.targets = node.targets[0]
        return self.default(node)

    def flatten_name(self, node):
        if node.id == 'True' or node.id == 'False':
            return 'bool'
        elif node.id == 'None':
            return 'void'
        else:
            name_type = self.env[node.id]
            if not name_type:
                name_type = self.new_type()
                self.env[node.id] = name_type
            return name_type

    def flatten_functiondef(self, node):
        self.args = [(arg.arg, self.new_type()) for arg in node.args.args]
        self.return_type = 'X'
        self.function = node.name
        self.env[node.name] = node.name
        self.env = Env(dict(self.args), self.env)
        [self.flatten(child) for child in node.body]
        self.env = self.env.parent
        self.nodes.append(('z_function', [a[1] for a in self.args], self.return_type))
        return self.env[node.name]

    def flatten_expr(self, node):
        return self.flatten(node.value)

    def flatten_return(self, node):
        v = self.flatten(node.value)
        self.nodes.append(('=', [v], self.return_type))
        return v

    def new_type(self):
        self.type_index += 1
        return 'Z%d' % self.type_index

    def to_snake_case(self, label):
        return re.sub(r'([a-z])([A-Z])', r'\1_\2', label).lower()

# BinOp(2, BinOp(b, a))

# bin_op(X1, X2, X3)
# bin_op(int, X3, X4)