"""Replay the preserved initial Fraction type failure without changing it."""
from pathlib import Path
import ast
p=Path(__file__).resolve().parent/'recompute_cubic_initial.py'
tree=ast.parse(p.read_text())
stop=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assert) and getattr(n,'lineno',0)>30)
ns={'__file__':str(p)}
exec(compile(ast.Module(tree.body[:stop],type_ignores=[]),str(p),'exec'),ns)
for key in ['a','eta','arrival','logp','logq']:
    print(key,[(i,str(ns[key][i]),type(ns[key][i]).__name__) for i in [1,3,5]])
