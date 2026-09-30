"""Independent direct-review anchors, exact stdlib rational arithmetic."""
import json
import platform
from fractions import Fraction as F

checks={}
rejections={}
def check(name,truth):
    checks[name]=bool(truth)
    assert truth,name
def reject(name,false_claim):
    rejections[name]=not bool(false_claim)
    assert not false_claim,name
def add(p,q):
    n=max(len(p),len(q))
    return [(p[i] if i<len(p) else F(0))+(q[i] if i<len(q) else F(0)) for i in range(n)]
def scale(p,a):
    return [a*x for x in p]
def mul(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return out
def integral(p):
    return sum(F(2)*x/F(i+1) for i,x in enumerate(p) if i%2==0)
def shift(p,n):
    return [F(0)]*n+p
def norm(v):
    return -v[0]**2+v[1]**2
def form(m,v,w):
    return sum(v[i]*m[i][j]*w[j] for i in range(2) for j in range(2))

# Original supplied beam sums, separate from parent matrix helpers.
beams=[(F(4),(F(1),F(1))),(F(1),(F(1),F(-1)))]
j=[sum(w*k[i] for w,k in beams) for i in range(2)]
m=[[sum(w*((-1 if i==0 else 1)*k[i])*((-1 if q==0 else 1)*k[q]) for w,k in beams) for q in range(2)] for i in range(2)]
uj=[x/F(4) for x in j]
nj=[F(3,4),F(5,4)]
wm=[F(3),F(1)] # u_M=wm/sqrt(8); avoid radical library by squared norms.
check('original_first_moment',j==[5,3] and norm(j)==-16)
check('current_frame_unit',uj==[F(5,4),F(3,4)] and norm(uj)==-1)
check('original_covariant_second_moment',m==[[5,-3],[-3,5]])
check('second_frame_unscaled_norm',norm(wm)==-8)
check('second_frame_unscaled_eigenvector',[-sum(m[0][q]*wm[q] for q in range(2)),sum(m[1][q]*wm[q] for q in range(2))]==[-4*x for x in wm])
check('second_frame_rest_value',form(m,wm,wm)/8==4)
check('current_frame_flux_nonzero',form(m,uj,nj)==3)
check('distinct_covariant_velocities',uj[1]/uj[0]==F(3,5) and wm[1]/wm[0]==F(1,3))
reject('covariance_alone_identifies_clock_frame',uj[1]/uj[0]==wm[1]/wm[0])

p=[F(3,8),F(0),F(-30,8),F(0),F(35,8)]
check('P4_lower_bound_square_identity',add(p,[F(3,7)])==scale(mul([F(-3,7),0,1],[F(-3,7),0,1]),F(35,8)))
check('P4_upper_bound_factor_identity',add([F(1)],scale(p,F(-1)))==scale(mul([1,0,-1],[1,0,7]),F(5,8)))
for n in (0,1,2):
    check('P4_low_moment_'+str(n),integral(shift(p,n))==0)
check('P4_azimuthal_transverse_moment',integral(mul(p,[F(1,2),0,F(-1,2)]))==0)
check('P4_fourth_moment',integral(shift(p,4))==F(16,315))
check('P4_square_integral',integral(mul(p,p))==F(2,9))
reject('isotropic_low_moments_force_isotropic_distribution',integral(shift(p,4))==0)
print(json.dumps({'status':'PASS','python':platform.python_version(),'arithmetic':'stdlib Fraction exact',
 'checks':checks,'false_claim_rejections':rejections,'outputs':{'v_J':'3/5','v_M':'1/3','current_frame_second_moment_flux':'3','P4_fourth_moment':'16/315','P4_square_integral':'2/9'},
 'scope':'Direct-review independent finite anchors, not blind producer review or a physical adoption.'},indent=2))
