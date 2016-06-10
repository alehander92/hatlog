# hatlog

a proof of concept of a type inference tool for Python written in Prolog. Idea described in [blog](http://code.alehander42.me/prolog_type_systems)

# how?

currently it works for simple one-function python files

```bash
bin/hatlog examples/map.py
# A,B::Callable[[A],B] -> List[A] -> List[B]
```

* hatlog flattens the python ast and annotates the types:  constants for literals and variables otherwise
* it generates a prolog program with the flattened ast: each node is represented as a prolog rule applied on its element types
* the program imports the specified type system, infers the types of the function based on it and saves it
* hatlog prints it

the type system is described as a simple file with prolog rules:

they describe the type rules for python nodes, e.g.

```prolog
z_cmp(A, A, bool)     :- comparable(A).

z_index([list, X], int, X).
z_index([dict, X, Y], X, Y).
z_index(str, int, str).

```

and some builtin methods, e.g.

```prolog
m([list, A], index, [A], int).
```

You can easily define your custom type systems just by tweaking those definitions.


# Author

[Alexander Ivanov](http://code.alehander42.me), 2016
