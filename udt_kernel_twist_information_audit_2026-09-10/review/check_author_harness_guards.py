#!/usr/bin/env python3
import ast
import json
from pathlib import Path
import sympy as s
p=Path(__file__).resolve().parents[1]
tree=ast.parse((p/'check_candidate.py').read_text())
names={'load_defs','simple','values','same','rejected'}
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
ns={'ast':ast,'s':s,'checks':[]}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'<author guard definitions>','exec'),ns)
results=[]
for name, call in [
 ('wrong scalar rejected by equality guard',lambda:ns['same']('wrong',s.Integer(1),s.Integer(0))),
 ('wrong matrix rejected by equality guard',lambda:ns['same']('wrong',s.eye(2),s.zeros(2))),
 ('vacuous negative control rejected',lambda:ns['rejected']('vacuous',s.Integer(0),s.Integer(0))),
 ('missing AST function rejected',lambda:ns['load_defs'](p.parent/'udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/derive_complete_coframe_extension.py',{'pullback','nonexistent_function'},{}))
]:
 try:
  call()
 except AssertionError as exc:
  results.append({'guard':name,'rejected':True,'exception':str(exc)})
 else:
  raise AssertionError('guard false pass: '+name)
print(json.dumps({'status':'PASS','guard_rejections':results},indent=2))
