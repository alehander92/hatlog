:- module(prettyTypes, [pretty_type/2, pretty_args/2, unvar/5, join/3, pretty_generic/2]).

:- use_module(library(assoc)).
:- use_module(library(pairs)).

join(A, S, R) :- join_(A, S, '', R).
join_([], _, S, S).
join_([A], _, B, C) :- concat(B, A, C).
join_([A | B], S, Input, Result) :- concat(Input, A, C), concat(C, S, Z), join_(B, S, Z, Result).
pretty_args(A, Z) :- pretty_args_(A, Y),
    join(Y, ' -> ', Z).

pretty_args_([], []).
pretty_args_([A | T], [X | Y]) :-
    pretty_type(A, X),
    pretty_args_(T, Y).

pretty_inner(A, Z) :-
    pretty_args_(A, Y),
    join(Y, ',', Z).

pretty_type(Type, Z) :-
    var(Type),
    format(atom(Z), '~p', [Type]);
    pretty_z(Type, Z).

pretty_z([list | Z], X) :-
    pretty_inner(Z, Args),
    format(atom(X), 'List[~p]', [Args]).

pretty_z([dict | Z], X) :-
    pretty_inner(Z, Args),
    format(atom(X), 'Dict[~p]', [Args]).

pretty_z([function, Argz, Ret], X) :-
    pretty_inner(Argz, Args),
    pretty_type(Ret, Return),
    format(atom(X), 'Callable[[~p],~p]', [Args, Return]).

pretty_z(void, 'None').

pretty_z(Type, Z) :- 
    atom(Type),
    format(atom(Z), "~a", [Type]).



unvar(Args, Return, UArgs, UReturn, GenericId) :-
    assoc:list_to_assoc([], Vars1),
    replace_vars(Args, UArgs, Vars1, Vars2, 1, L),
    replace_vars(Return, UReturn, Vars2, _, L, GenericId).

replace_vars(Val, UVal, Vars, NewVars, L, Z) :-
    var(Val),
    replace_var(Val, UVal, Vars, NewVars, L, Z);
    
    replace_vars_(Val, UVal, Vars, NewVars, L, Z).

replace_var(Value, UValue, Vars, NewVars, L, Z) :-
    format(atom(A0), '~p', Value),
    writeln(A0),
    assoc:get_assoc(A0, Vars, A1),
    =(Vars, NewVars), % var exists
    =(UValue, A1),
    =(Z, L);

    format(atom(A0), '~p', Value),
    Z is L + 1, M is L - 1,
    write(M),write(L),writeln(''),
    sub_atom('ABCDEF', M, 1, _, UValue),
    assoc:put_assoc(A0, Vars, UValue, NewVars).

replace_vars_([], [], Vars, Vars, L, L).
replace_vars_([A | B], [UA | UB], Vars, NewVars, L, Z) :-
    replace_vars(A, UA, Vars, Vars1, L, L1),
    replace_vars_(B, UB, Vars1, NewVars, L1, Z).

replace_vars_(Value, Value, Vars, Vars, L, L).

pretty_generic(GenericId, Generics) :-
    Index is GenericId - 1,
    sub_atom('ABCDEF', 0, Index, _, Sub),
    atom_chars(Sub, Vars),
    join(Vars, ',', Generics).

%% prettyTypes:unvar([A0], [e], A1, A2).