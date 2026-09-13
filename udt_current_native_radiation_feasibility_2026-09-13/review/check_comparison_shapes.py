"""Pre-execution frozen finite diagnostic: inspect actual equality input lengths.

The initial equal helper used zip without a length guard. This wrapper retains
the source unchanged, instruments that one definition in memory, replays its
current checks, and deliberately sends one unequal-shape comparison. Same-code
regression integrity only; no extra independent mathematical evidence. Stop
after this bounded capture (180s/2048MiB, one process/thread).
"""
from pathlib import Path
import hashlib,json,sys,datetime

source=Path(__file__).resolve().parent/'independent_exact.py'
raw=source.read_text()
old='def equal(name,a,b):zero(name,[x-y for x,y in zip(flat(a),flat(b))])'
new='''shape_comparisons=[]
def equal(name,a,b):
    aa,bb=flat(a),flat(b)
    shape_comparisons.append({'name':name,'left':len(aa),'right':len(bb)})
    assert len(aa)==len(bb), 'unequal comparison shapes'
    zero(name,[x-y for x,y in zip(aa,bb)])'''
assert raw.count(old)==1
adapted=raw.replace(old,new)
outpath=Path(sys.argv[1]);bodypath=outpath.with_name('SHAPE_REPLAY_BODY.json')
args=sys.argv[:];sys.argv=[str(source),str(bodypath)]
ns={'__name__':'__main__','__file__':str(source)}
try:
    exec(compile(adapted,str(source),'exec'),ns)
except SystemExit as e:
    assert e.code==0
finally:sys.argv=args
baseline=ns['shape_comparisons'][:]
caught=False
try:ns['equal']('deliberate_unequal_shapes',[0,0],[0])
except AssertionError:caught=True
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'instrumented replay of same reviewer code, no independent mathematical count','source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'adapted_sha256':hashlib.sha256(adapted.encode()).hexdigest(),'actual_comparison_shapes':baseline,'all_actual_shapes_equal':all(x['left']==x['right'] for x in baseline),'unequal_shape_mutation_caught':caught,'baseline_result_path':str(bodypath),'note':'Initial84 did not contain this length guard; current actual shapes checked here without rewriting initial evidence.'}
with outpath.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(json.dumps({'actual_comparisons':len(baseline),'all_actual_shapes_equal':r['all_actual_shapes_equal'],'unequal_shape_mutation_caught':caught}))
sys.exit(0 if r['all_actual_shapes_equal'] and caught else 1)
