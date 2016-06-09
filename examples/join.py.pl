:- initialization main.

:- use_module(pythonTypeSystem).
:- use_module(prettyTypes).

f(join, [Z0, Z1], X) :-
    z_assign(Z2, str, Z3),
    z_unary_op(int, Z6),
    z_slice(Z0, Z6, Z6, Z5),
    z_bin_op(Z4, Z1, Z7),
    z_aug_assign(Z2, Z7, Z8),
    z_for(Z4, Z5, [Z8], Z9),
    z_unary_op(int, Z11),
    z_index(Z0, Z11, Z10),
    z_aug_assign(Z2, Z10, Z12),
    =(Z2, X).

main :-
    open('examples/join.py.txt', write, Stream),
    (
        f(join, Z0, Z1),
        unvar(Z0, Z1, Z2, Z3, Z4), % replace free vars with names
        pretty_args(Z2, Y),
        pretty_type(Z3, Z),
        pretty_generic(Z4, X),
        format(Stream, '~a::', [X]),
        write(Stream, Y),
        write(Stream, ' -> '),
        write(Stream, Z),
        write(Stream, '\n'),

        true
    ),

    close(Stream),
    halt.
main :-
    halt(1).
