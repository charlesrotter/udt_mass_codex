"""Execute the actual worker retry-loop AST with CPU injected trial outcomes.

This tests the changed control block directly, not a separate reimplementation,
and does not claim a GPU/CUDA execution or full-process failure simulation.
"""
import ast,copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;SOURCE=HERE.parents[1]/'production_worker.py'
tree=ast.parse(SOURCE.read_text())
main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
loops=[n for n in ast.walk(main) if isinstance(n,ast.While) and isinstance(n.test,ast.Constant) and n.test.value is True]
assert len(loops)==1
loop=copy.deepcopy(loops[0])
body=ast.parse('def actual_loop(jump):\n retries=0\n pass\n return dict(jump=jump,retries=retries,state=(newg,newv,stage_omega))\n').body[0]
body.body[1]=loop;module=ast.fix_missing_locations(ast.Module(body=[body],type_ignores=[]))
namespace=dict(torch=None,engine=None,g=None,v=None,spec=dict(dt_min=.001,cfl=.25))
exec(compile(module,str(SOURCE),'exec'),namespace)
records=[]
for name,initial_jump,outcomes in [('unexpected',4,['INJECTED_IMPLEMENTATION_ERROR']),
    ('stage_retry',4,['STAGE_CFL',None]),('floor',1,['STAGE_CFL'])]:
    calls=[];emits=[];saves=[]
    def trial(*args):
        calls.append(args[-2]);item=outcomes[len(calls)-1]
        if item:raise RuntimeError(item)
        return 1,2,3
    namespace.update(checked_rk4=trial,emit=lambda *a,**k:emits.append((a,k)),
                     checked_save=lambda *a:saves.append(a))
    try:result=namespace['actual_loop'](initial_jump);error=None
    except RuntimeError as exc:result=None;error=str(exc)
    if name=='unexpected':assert error=='INJECTED_IMPLEMENTATION_ERROR' and len(calls)==1 and not emits and not saves
    elif name=='stage_retry':assert result['jump']==2 and result['retries']==1 and len(calls)==2 and not saves
    else:assert result==75 and saves==[(True,'TIMESTEP_FLOOR')] and len(calls)==1
    records.append(dict(case=name,dt_calls=calls,emits=emits,saves=saves,result=result,error=error))
print(json.dumps(dict(status='RETRY_CLASSIFICATION_PASS',records=records,
    worker_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    tested_ast_sha256=hashlib.sha256(ast.dump(loop).encode()).hexdigest(),
    scope='Actual retry-loop AST with injected CPU outcomes; no GPU error was manufactured.'),indent=2,sort_keys=True))
