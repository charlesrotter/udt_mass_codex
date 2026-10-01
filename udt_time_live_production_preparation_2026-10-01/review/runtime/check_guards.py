"""Actual worker CLI catches, with fixture-only np.load redirection and no Torch.

The initial files stay inside reviewer ownership. The only interception redirects
the one declared producer initial path to the chosen reviewer fixture; the actual
worker schema, state validation and CLI exception handling execute unchanged.
"""
import argparse,copy,hashlib,json,os,subprocess,sys
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];ROOT=BASE.parent
SOURCE=BASE/'production_worker.py'
INITIAL='udt_time_live_production_preparation_2026-10-01/initial/reviewer_fixture.npz'

LAUNCHER='''import os,runpy,sys,numpy as np
from pathlib import Path
def forbid_directory_creation(*a,**kw):raise RuntimeError('UNEXPECTED_RUN_CREATION')
Path.mkdir=forbid_directory_creation
original=np.load
def fixture_load(path,*a,**kw):
    if str(path).endswith('/initial/reviewer_fixture.npz'):path=os.environ['REVIEW_INITIAL_FIXTURE']
    return original(path,*a,**kw)
np.load=fixture_load
class NoTorch:
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0]=='torch':raise RuntimeError('UNEXPECTED_TORCH_IMPORT')
sys.meta_path.insert(0,NoTorch())
sys.argv=sys.argv[1:]
runpy.run_path(sys.argv[0],run_name='__main__')
'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('destination')
    args=parser.parse_args();dest=HERE/args.destination;dest.mkdir(exist_ok=False)
    base=dict(n=8,initial=INITIAL,period=2*np.pi,dt_min=.001,end_tick=100,
        max_step_ticks=4,cfl=.1,check_ticks=4,checkpoint_ticks=20,
        windows=[dict(center=50,stride=2,count=5)],wall_seconds=10,
        gpu_bytes=1024**3,output_bytes=1024**2,constraint_limit=2e-5)
    g=np.broadcast_to(np.diag([-1.,1.,1.,1.]),(8,8,8,4,4)).copy();v=np.zeros_like(g)
    fixtures={}
    for name in ['valid','asymmetric_g','asymmetric_v','nonfinite','wrong_dtype','wrong_shape','wrong_period']:
        a,b=g.copy(),v.copy();period=2*np.pi
        if name=='asymmetric_g':a[...,0,1]=.001
        if name=='asymmetric_v':b[...,0,1]=.001
        if name=='nonfinite':a[0,0,0,0,0]=np.nan
        if name=='wrong_dtype':a=a.astype(np.float32)
        if name=='wrong_shape':a=a[:-1];b=b[:-1]
        if name=='wrong_period':period+=.1
        path=dest/(name+'.npz');np.savez_compressed(path,g=a,v=b,period=np.array(period));fixtures[name]=path
    # Valid source-level control proves fixture schema and schedule are accepted.
    module=type(np)('reviewed_worker');module.__file__=str(SOURCE)
    exec(compile(SOURCE.read_text(),str(SOURCE),'exec'),module.__dict__)
    from unittest.mock import patch
    old=np.load
    with patch.object(module.np,'load',side_effect=lambda *a,**kw:old(fixtures['valid'],**kw)):
        saves,checks,_=module.validate(base)
    assert {0,46,48,50,52,54,100}<=set(saves) and set(saves)<=set(checks)
    cases=[]
    def add(name,key,value):
        spec=copy.deepcopy(base);spec[key]=value;cases.append((name,spec,'valid',[],None))
    for key,value in [('n',True),('n',7),('n',65),('dt_min',float('nan')),('dt_min',0),
        ('cfl',float('inf')),('cfl',0),('period',float('nan')),('constraint_limit',float('nan')),
        ('constraint_limit',2.1e-5),('constraint_limit',0),('wall_seconds',float('nan')),
        ('wall_seconds',0),('wall_seconds',181),('gpu_bytes',0),('gpu_bytes',True),
        ('output_bytes',0),('output_bytes',1.5),('max_step_ticks',3),('check_ticks',0),
        ('checkpoint_ticks',101),('end_tick',0),('windows',None)]:
        add(f'bad_{key}_{len(cases)}',key,value)
    for name,window in [('count4',dict(center=50,stride=2,count=4)),('count6',dict(center=50,stride=2,count=6)),
        ('negative',dict(center=0,stride=2,count=5)),('beyond',dict(center=100,stride=2,count=5)),
        ('stride0',dict(center=50,stride=0,count=5)),('floatcenter',dict(center=50.5,stride=2,count=5))]:
        add(name,'windows',[window])
    for name in fixtures:
        if name!='valid':cases.append((name,copy.deepcopy(base),name,[],None))
    spec=copy.deepcopy(base);spec['extra']=1;cases.append(('extra_schema',spec,'valid',[],None))
    for name,path in [('absolute','/tmp/fixture.npz'),('escape','../fixture.npz'),('outside','other/initial/fixture.npz')]:
        add('path_'+name,'initial',path)
    cases.append(('negative_pause',copy.deepcopy(base),'valid',['--pause-after','-1'],None))
    cases.append(('missing_cublas',copy.deepcopy(base),'valid',[],''))
    cases.append(('run_path',copy.deepcopy(base),'valid',[],None))
    records=[]
    for name,spec,fixture,extra,cublas in cases:
        sp=dest/(name+'.spec.json');sp.write_text(json.dumps(spec,indent=2)+'\n')
        run=BASE/'runs'/('reviewer_guard_'+name) if name!='run_path' else dest/(name+'_run')
        command=[sys.executable,'-c',LAUNCHER,str(SOURCE),str(sp),str(run),*extra]
        env=dict(os.environ,CUDA_VISIBLE_DEVICES='',CUBLAS_WORKSPACE_CONFIG=':4096:8' if cublas is None else cublas,
            REVIEW_INITIAL_FIXTURE=str(fixtures[fixture]))
        result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,timeout=10)
        (dest/(name+'.stdout')).write_bytes(result.stdout);(dest/(name+'.stderr')).write_bytes(result.stderr)
        actual=json.loads(result.stderr)
        assert result.returncode==2 and 'UNEXPECTED_' not in actual['reason'],(name,actual)
        assert actual['type']=='ValueError',(name,actual)
        if name!='run_path':assert actual['reason']!='RUN_PATH_SCOPE',(name,actual)
        assert not run.exists(),name
        records.append(dict(case=name,returncode=result.returncode,reason=actual['reason'],run_created=False))
    print(json.dumps(dict(status='TPP1_WORKER_GUARDS_PASS',cases=records,
        worker_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        valid_control_schedule=dict(saves=saves,checks=checks),
        scope='Actual pre-Torch CLI rejects; fixture-only np.load redirection, blocked Torch import. Not GPU runtime coverage.'),indent=2,sort_keys=True))

if __name__=='__main__':main()
