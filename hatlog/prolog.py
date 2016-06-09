def generate_prolog(x, name, file):

    header = '''\
:- initialization main.

:- use_module(pythonTypeSystem).
:- use_module(prettyTypes).
'''
    fun = generate_fun(x, name)

    m = '''main :-
    open('%s.txt', write, Stream),
    (
        f(%s, Z0, Z1),
        unvar(Z0, Z1, Z2, Z3, Z4), %% replace free vars with names
        pretty_args(Z2, Y),
        pretty_type(Z3, Z),
        pretty_generic(Z4, X),
        format(Stream, '~a::', [X]),
        write(Stream, Y),
        write(Stream, ' -> '),
        write(Stream, Z),
        write(Stream, '\\n'),

        true
    ),

    close(Stream),
    halt.
main :-
    halt(1).
''' %(file, name)
    program = '%s\n%s\n%s' % (header, fun, m)
    with open('%s.pl' % file, 'w') as f:
        f.write(program)
    return '%s.pl' % file

def generate_fun(x, name):
    head = 'f(%s, [%s], %s) :-' % (name, ', '.join(x[-1][1]), x[-1][-1])
    # print(x[:-1])
    block = ',\n    '.join(['%s(%s)' % (a, ', '.join(map(generate_arg, args + [b]))) for a, args, b in x[:-1]])
    return '%s\n    %s.\n' % (head, block)

def generate_arg(a):
    if isinstance(a, str):
        return a
    else:
        return '[%s]' % ', '.join(map(generate_arg, a))

