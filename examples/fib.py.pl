:- initialization main.

:- use_module(pythonTypeSystem).
:- use_module(prettyTypes).

f(fib, [Z0], X) :-
    z_cmp(Z0, int, Z1),
    =(int, X),
    z_bin_op(Z0, int, Z2),
    =(Z2, Z0),
    z_bin_op(Z0, int, Z3),
    =(Z3, Z0),
    z_bin_op(X, X, Z4),
    =(Z4, X),
    z_if(Z1, [int], [Z4], Z5).

main :-
    open('examples/fib.py.txt', write, Stream),
    (
        f(fib, Z0, Z1),
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
