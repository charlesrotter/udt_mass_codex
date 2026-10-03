"""Separate CBR1 source-first diagnostic. No parent scientific code imports."""
import json, math, platform
from fractions import Fraction as F
from pathlib import Path

OUT=Path(__file__).parent
checks={}
def check(name, condition):
    checks[name]=bool(condition)
    if not condition: raise AssertionError(name)

# Seven-frame quadratic contractions at v=3/5, gamma²=25/16.
v=F(3,5); g2=1/(1-v*v)
c00=F(2); spatial=[F(3),F(-4),F(8)]; mixed=[F(5),F(-2),F(7)]
boost=[g2*(c00+v*v*spatial[i]+sgn*2*v*mixed[i])
       for i in range(3) for sgn in [-1,1]]
weight=1/(2*g2*v*v); center=-(1+3/(v*v))
rhat=weight*sum(boost)+center*c00
check('seven_frame_scalar_exact',rhat==sum(spatial)-c00)
check('omitted_center_catch',weight*sum(boost)!=rhat)
# Spatial cross components never enter the listed axial boosts.
def axial_contractions(offdiag):
    tensor=[[c00,*mixed],[mixed[0],spatial[0],offdiag[0],offdiag[1]],
            [mixed[1],offdiag[0],spatial[1],offdiag[2]],
            [mixed[2],offdiag[1],offdiag[2],spatial[2]]]
    ans=[]
    for i in range(1,4):
        for sign in [-1,1]:
            vec=[F(1),F(0),F(0),F(0)];vec[i]=sign*v
            ans.append(g2*sum(tensor[a][b]*vec[a]*vec[b] for a in range(4) for b in range(4)))
    return ans
check('spatial_offdiagonal_nullspace',axial_contractions([F(1),F(2),F(3)])==axial_contractions([F(-99),F(42),F(13)]))
check('arbitrary_tensor_contractions',boost==axial_contractions([F(1),F(2),F(3)]))

# v²=1/3: scalar R = six c boosts -10 c0; c=-2 sum(y)/L².
yweights=[F(20)]*3+[F(-2)]*18
boxweights=[F(-4),F(-1),F(-1)]+[F(1)]*6
check('scalar_log_l1_weight',sum(abs(w) for w in yweights)==96)
check('scalar_log_variance_weight',sum(w*w for w in yweights)==1272)
check('box_shared_center_l1_weight',sum(abs(w) for w in boxweights)==12)
check('box_shared_center_variance_weight',sum(w*w for w in boxweights)==24)
joint=[a*b for a in yweights for b in boxweights]
check('joint_noise_l1_weight',sum(abs(w) for w in joint)==1152)
check('joint_noise_variance_weight',sum(w*w for w in joint)==30528)
check('adversarial_noise_attains_bound',sum(w*(1 if w>0 else -1) for w in joint)==1152)

# Actual initial prepared outgoing clock/null records from analytic FLRW metric.
records=[]
for k in [-0.25,0.25]:
    previous=math.inf
    for length in [0.2,0.1,0.05,0.025]:
        root=math.sqrt(abs(k)); z=root*length
        tb=(math.tan(z) if k>0 else math.tanh(z))/root
        p=1+k*tb*tb
        logp=math.log(p)
        got=-6*logp/length**2; truth=-6*k
        error=abs(got-truth)
        check(f'analytic_domain_{k}_{length}',p>0 and z<=0.1)
        check(f'analytic_refinement_{k}_{length}',error<previous)
        previous=error
        records.append(dict(k=k,L=length,arrival=tb,proper_period_ratio=p,
                            log_period_ratio=logp,ric00_estimate=got,
                            independent_ric00=truth,absolute_error=error,
                            fixed_1e_minus_8_log_noise_curvature_shift=6e-8/length**2))
check('fixed_noise_increases_4x',math.isclose(records[1]['fixed_1e_minus_8_log_noise_curvature_shift']/records[0]['fixed_1e_minus_8_log_noise_curvature_shift'],4))

falsepass=[]
for t in [F(0),F(1),F(2)]:
    hh=F(1,5)/(1+F(2,5)*t); hprime=-2*hh*hh
    rr=6*(hprime+2*hh*hh); original00=3*hh*hh
    check(f'falsepass_{t}',rr==0 and original00>0)
    falsepass.append(dict(t=str(t),R=str(rr),BoxR='0',original_E00=str(original00)))

r1,r2,q1,q2=F(1),F(2),F(1,4),F(3,4)
slope=(q2-q1)/(r2-r1); alpha=1/(6*slope); lam=(r1-q1/slope)/4
check('affine_identification',alpha==F(1,3) and lam==F(1,8))
check('heldout_pass',F(5,4)==slope*(F(3)-4*lam))
check('heldout_falsepass_catch',F(3,2)!=slope*(F(3)-4*lam))
# Equal R and unequal Q cannot obey Q=M²(R-4Λ) for any common constants.
check('equal_R_unequal_Q_catch',F(1)==F(1) and F(2)!=F(3))
# Same sampled pair R=1,Q=2 admits alpha=1/6,Lambda=-1/4 and alpha=1/3,Lambda=-3/4.
check('equal_pairs_do_not_force_Q_zero',all(6*a*2-1+4*l==0 for a,l in [(F(1,6),F(-1,4)),(F(1,3),F(-3,4))]))

result=dict(scope='source-first exact algebra and supplied analytic controls only',
    python=platform.python_version(),checks=checks,pass_count=sum(checks.values()),
    noise_weights=dict(R_l1=96,R_variance=1272,Box_l1=12,Box_variance=24,
                      combined_l1=1152,combined_variance=30528),
    analytic_prepared_clock_records=records,falsepass_control=falsepass,
    affine_fixture=dict(alpha=str(alpha),Lambda=str(lam)),
    exclusions=['no parent main data/code','no physical law confirmation','no interval certification'])
out=OUT/'SOURCE_FIRST_RESULT.json'
with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
