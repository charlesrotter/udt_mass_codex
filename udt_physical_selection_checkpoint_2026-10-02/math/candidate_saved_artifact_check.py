"""Exposed saved-clock-artifact check using the reviewer's sealed arithmetic.

Parent code/helpers are not imported. Metric a(t) is reconstructed from saved
clock jets via t(L)=integral p(L)dL, then tested with original tensor components.
"""
from fractions import Fraction as Q
from pathlib import Path
import contextlib, hashlib, io, json, math, runpy, platform

base=Path('udt_physical_selection_checkpoint_2026-10-02')
own=base/'math/source_first_fraction.py'
saved=base/'EXACT_RESULT.json'
with contextlib.redirect_stdout(io.StringIO()):
    lib=runpy.run_path(str(own))
original=lib['original_components']
state=original.__globals__
N=state['N']; const=state['const'];add=state['add'];mul=state['mul']
scale=state['scale'];integrate=state['integrate'];compose=state['compose']
def exp_series(a):
    value=const(1);power=const(1)
    for n in range(1,N+1):
        power=mul(power,a);value=add(value,scale(power,Q(1,math.factorial(n))))
    return value
def revert_unit(a):
    result=const(0)
    for n in range(1,N+1):
        target=Q(1) if n==1 else Q(0)
        result[n]=target-compose(a,result)[n]
    return result

results=[]
for row in json.loads(saved.read_text())['saved_clock_jets']:
    state['alpha']=Q(row['alpha']);state['beta']=Q(row['beta'])
    logp=const(0)
    for n in [3,4,5]:logp[n]=Q(row[f'b{n}'])
    p=exp_series(logp)
    proper_t=integrate(p)
    inverse=revert_unit(proper_t)
    metric_a=compose(p,inverse)
    C,D,R=original(metric_a)
    assert all(x==0 for x in C[:3]), C[:3]
    assert all(x==0 for x in D[:2]), D[:2]
    assert R[0]==0 and R[1]==Q(row['P0'])
    b3,b4,b5=(logp[n] for n in [3,4,5])
    got_alpha=-b3/(120*(b5-Q(12,5)*b4*b4/b3))
    got_beta=-got_alpha*b4/(27*b3*b3)
    assert got_alpha==Q(row['alpha']) and got_beta==Q(row['beta'])
    results.append({'name':row['name'],'metric_a_through5':[str(x) for x in metric_a[:6]],
        'original00_coefficients_0_2':[str(x) for x in C[:3]],
        'original_spatial_coefficients_0_1':[str(x) for x in D[:2]],
        'geometric_Rdot0':str(R[1]),'alpha':str(got_alpha),'beta':str(got_beta),
        'quadratic_relation_defect':str(b5+b3/(120*got_alpha))})

# Independent polarization of the original tensor polynomial: no handwritten
# cross-term formula from the parent is used in this evaluation.
state['alpha']=Q(1);state['beta']=Q(1)
def Dlinear(c3,c4,c5):
    a=const(1);a[3]=Q(c3);a[4]=Q(c4);a[5]=Q(c5)
    return original(a)[1][1]
cross=Dlinear(1,1,0)-Dlinear(1,0,0)-Dlinear(0,1,0)+Dlinear(0,0,0)
c5coef=Dlinear(0,0,1)-Dlinear(0,0,0)
c3coef=Dlinear(1,0,0)-Dlinear(0,0,0)
assert (cross,c5coef,c3coef)==(Q(-93312),Q(-1440),Q(-12))
assert cross/2==Q(-46656)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
print(json.dumps({'status':'PASS','python':platform.python_version(),
    'saved_artifact_sha256':sha(saved),'own_sealed_helper_sha256':sha(own),
    'parent_helpers_imported':False,'results':results,
    'independent_original_D_linear_coefficients':{
        'beta_c3_c4':str(cross),'alpha_c5':str(c5coef),'c3':str(c3coef)},
    'scope':'Supported finite coefficients from saved clock jets; no later coefficients certified'},indent=2))
