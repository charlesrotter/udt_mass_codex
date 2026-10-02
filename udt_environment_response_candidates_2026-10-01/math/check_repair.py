"""Exposed review of bounded ERC1 checker repair; no production mutation."""
import ast,hashlib,json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent.parent
def functions(path):
    tree=ast.parse(path.read_text())
    return {node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
old=functions(ROOT/'check_candidates_initial.py')
new=functions(ROOT/'check_candidates.py')
assert old.keys()==new.keys()
changed=[k for k in old if ast.dump(old[k],include_attributes=False)!=ast.dump(new[k],include_attributes=False)]
assert changed==['symbolic'],changed
def fixture(function):
    zero=next(n for n in function.body if isinstance(n,ast.FunctionDef) and n.name=='zero')
    loops=[n for n in function.body if isinstance(n,ast.For) and 'offdiagonal_' in ast.unparse(n)]
    assert len(loops)==1
    code=compile(ast.fix_missing_locations(ast.Module(body=[zero,loops[0]],type_ignores=[])),'fixture','exec')
    ric=sp.zeros(4);Q=sp.zeros(4);ric[0,1]=1;Q[0,1]=-1
    env={'sp':sp,'checks':{},'ric':ric,'Q':Q}
    try:
        exec(code,env)
        return {'passes':True,'checks':env['checks']}
    except AssertionError as err:
        return {'passes':False,'error':str(err),'checks':env['checks']}
before=fixture(old['symbolic']);after=fixture(new['symbolic'])
assert before['passes'] and not after['passes']
sym=json.loads((ROOT/'parent_symbolic_repaired/symbolic.json').read_text())
assert sym['status']=='PASS' and sym['exact_zero_checks']==39
assert all(v=='0' for v in sym['checks'].values())
repair=json.loads((ROOT/'REPAIR_CHECKPOINT.json').read_text())
for name,wanted in repair['hashes'].items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==wanted,name
result={'pass':True,'changed_functions':changed,'actual_old_loop_fixture':before,
 'actual_repaired_loop_fixture':after,'repaired_symbolic_count':39,
 'repair_binding_count':len(repair['hashes']),
 'scope':'AST and actual extracted assertion loop/capture correspondence; parent symbolic output is regression, not independent scientific proof',
 'chronology':'Repair checkpoint is post-execution correspondence only. Reviewer received repair notice after its execution; no independent pre-execution observation is claimed.'}
(ROOT/'math/repair_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
