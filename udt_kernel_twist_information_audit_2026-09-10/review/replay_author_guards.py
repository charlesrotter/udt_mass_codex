#!/usr/bin/env python3
"""Replay author's actual wrong-formula cases through its equality guard, in memory."""
import ast
from pathlib import Path

path=Path(__file__).resolve().parents[1]/'check_candidate.py'
tree=ast.parse(path.read_text())
replacement=ast.parse('''
def rejected(name, wrong, right):
    try:
        same(name, wrong, right)
    except AssertionError as exc:
        checks.append({'name':name,'type':'author equality guard actually rejected injected wrong formula',
                       'passed':True,'actual_exception':str(exc)})
    else:
        raise AssertionError(('wrong formula survived actual equality guard',name))
''').body[0]
tree.body=[replacement if isinstance(n,ast.FunctionDef) and n.name=='rejected' else n for n in tree.body]
exec(compile(ast.fix_missing_locations(tree),str(path),'exec'),{'__file__':str(path),'__name__':'__main__'})
