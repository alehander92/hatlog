:- module(pythonTypeSystem, [z_list/2,
    is_number/1, z_assign/3, z_call/3, z_method_call/4, z_bin_op/3,
    z_cmp/3, z_eq/3,
    z_fcall/3, z_unary_op/2, z_aug_assign/3, z_slice/4, z_index/3,
    z_if/4, z_for/4, m/4, sequence/1, f/3]).

z_list([], _).
z_list([H], [list, H]).
z_list_([H, H | T], [list, H]) :- z_list(T, [list, H]). % hom list

z_dict([], _).
z_dict([Y, Z], [dict, Y, Z]) :- hashable(Y).
z_dict([Y, Z, Y, Z | T], [dict, Y, Z]) :- hashable(Y), z_dict(T, [dict, Y, Z]). % hom dict

comparable(int).
comparable(float).

is_number(int).
is_number(float).

sequence([list, _]).
sequence([dict, _, _]).

hashable(int).
hashable(float).
hashable(string).
hashable(bool).


element_of(A, [list, A]).
element_of(A, [dict, A, _]).

z_assign(A, A, void).
z_aug_assign(A, A, void).
z_call(Function, Args, Result)  :- f(Function, Args, Result).
z_method_call(Receiver, Message, Args, Result) :- m(Receiver, Message, Args, Result).
z_fcall([function, Args, Res], Args, Res).

z_bin_op(int, int, int).
z_bin_op(str, str, str).
z_bin_op(A, B, float) :- is_number(A), is_number(B).
% union([union | T], T).
z_cmp(A, A, bool)     :- comparable(A).
z_eq(A, A, bool).

z_if(bool, _, _, _). % test if_true if_false result
z_for(Element, Sequence, _, void) :- sequence(Sequence), element_of(Element, Sequence).

z_unary_op(int, int).
z_unary_op(float, float).

z_index([list, X], int, X).
z_index([dict, X, Y], X, Y).
z_index(str, int, str).

z_slice([list, X], int, int, [list, X]).
z_slice(str, int, int, str).


m([list, A], append, [A], void).
m([list, A], pop, [], A).
m([list, A], extend, [[list, A]], void).
m([list, A], index, [A], int).
m([list, A], index, [A, int], int).
m([list, A], index, [A, int, int], int).


m([dict, A, B], get, [A, B], B).
m([dict, A, _], keys, [list, A]).
m([dict, _, A], values, [list, A]).
m(string, join, [[list, string]], string).
m(string, split, [string], [list, string]).

f(len, [[list, _]], int).
f(sorted, [[list, A]], [list, A]).

