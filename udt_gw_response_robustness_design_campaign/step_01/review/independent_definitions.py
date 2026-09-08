"""Independent RD1 definition checks; no producer code/data imported."""
from fractions import Fraction as Q
import cmath
import hashlib
import json
import math
import platform
import sys

def mv(a, x):
    return [sum((v*w for v, w in zip(row, x)), Q(0)) for row in a]

def norm(x):
    return math.sqrt(float(sum(abs(v)**2 for v in x)))

def inner(x, y):
    return sum(complex(a).conjugate()*complex(b) for a,b in zip(x,y))

def caught_bad_zero(value):
    try:
        assert abs(value) < 1e-12, "deliberately invalid zero assertion"
    except AssertionError:
        return True
    raise AssertionError("defect not caught")

F = [[Q(1),Q(0)], [Q(0),Q(1)], [Q(1),Q(1)]]
b = [Q(-1),Q(-1),Q(1)]
epsilon = Q(1,100)
E = [[Q(0),Q(0)],[Q(0),Q(0)],[epsilon,Q(0)]]
out = {"python":platform.python_version(), "method":"stdlib Fraction plus scalar float/complex; finite anchors, not continuum certification"}
assert mv(list(map(list,zip(*F))), b) == [0,0]

# Exact leakage counterexample with nonzero arbitrarily small operator error.
leakage=[]
for a in [Q(1),Q(100),Q(1000000)]:
    h=[a,Q(0)]
    y=[u+v for u,v in zip(mv(F,h),mv(E,h))]
    residual=sum(v*w for v,w in zip(b,y))
    assert residual == epsilon*a
    leakage.append({"wave_amplitude":str(a), "unnormalized_null":str(residual), "unit_null":float(residual)/math.sqrt(3)})
out["amplitude_scaling"]=leakage
assert caught_bad_zero(float(leakage[-1]["unnormalized_null"]))
# A common two-polarization response is still in the nominal column space.
K=[[Q(3,2),Q(1,3)], [Q(-2,7),Q(4,5)]]
for h in ([Q(2),Q(-3)], [Q(0),Q(8)], [Q(-5,3),Q(2,9)]):
    assert sum(v*w for v,w in zip(b,mv(F,mv(K,h))))==0
out["image_preserving_common_response"]="exact zero for three finite witnesses; algebra bFK=(bF)K owns all h"

# Stable recovery: F^T F=[[2,1],[1,2]] has gamma=1.
e=[Q(1,100),Q(-2,100),Q(1,100)]
eta=norm(e)
eta_N=abs(float(sum(v*w for v,w in zip(b,e))))/math.sqrt(3)
beta=float(epsilon)/math.sqrt(3)
min_amp_margin=math.inf
max_ratio=0.
count=0
for x in range(-4,5):
    for z in range(-4,5):
        h=[Q(x,3),Q(z,5)]
        if h==[0,0]:
            continue
        y=[v+w+n for v,w,n in zip(mv(F,h),mv(E,h),e)]
        H=(norm(y)+eta)/(1-float(epsilon))
        r=abs(float(sum(v*w for v,w in zip(b,y))))/math.sqrt(3)
        assert H+1e-14>=norm(h)
        assert r<=beta*H+eta_N+1e-14
        assert r<=beta*norm(h)+eta_N+1e-14
        min_amp_margin=min(min_amp_margin,H-norm(h))
        max_ratio=max(max_ratio,r/(beta*H+eta_N))
        count+=1
out["stable_recovery"]={"gamma":1,"epsilon":float(epsilon),"beta":beta,"eta":eta,"eta_null":eta_N,"cases":count,"smallest_amplitude_slack":min_amp_margin,"largest_leakage_bound_ratio":max_ratio}

# Finite kernel ignored by a 3-by2 calibration submatrix.
kernel=[]
for a in [Q(1),Q(1000000)]:
    h=[Q(0),Q(0),a]
    enlarged=[[Q(1),Q(0),Q(0)],[Q(0),Q(1),Q(0)],[Q(1),Q(1),Q(0)]]
    defect=[[Q(0),Q(0),Q(0)],[Q(0),Q(0),Q(0)],[Q(0),Q(0),epsilon]]
    y=[u+v for u,v in zip(mv(enlarged,h),mv(defect,h))]
    kernel.append({"hidden_wave_norm":float(a),"data_norm":norm(y),"null":float(sum(v*w for v,w in zip(b,y)))})
assert caught_bad_zero(kernel[-1]["null"])
out["hidden_domain_kernel"]=kernel

# Common time filter fails to commute with time-varying response/null.
hp=[Q(1),Q(0)]
hc=[Q(0),Q(0)]
a=[Q(1),Q(2)]
channels=[hp,hc,[a[j]*hp[j]+hc[j] for j in range(2)]]
point_null=[-a[j]*channels[0][j]-channels[1][j]+channels[2][j] for j in range(2)]
filtered=[[sum(ch,Q(0))/2]*2 for ch in channels]
wrong=[-a[j]*filtered[0][j]-filtered[1][j]+filtered[2][j] for j in range(2)]
assert point_null==[0,0]
assert wrong==[Q(0),Q(-1,2)]
assert caught_bad_zero(float(wrong[1]))
out["common_filter_commutator"]={"correct":list(map(str,point_null)),"wrong":list(map(str,wrong))}

# Frequency-domain crop/window mixing: no input retained-band amplitude bound.
# DFT conventions: x_n=sum H_k exp(2pi i kn/N)/sqrt(N).
n=8
H=[0j]*n
H[3]=8.
x=[sum(H[k]*cmath.exp(2j*math.pi*k*j/n) for k in range(n))/math.sqrt(n) for j in range(n)]
w=[1.,0.,0.,0.,0.,0.,0.,0.]
W=[sum(w[j]*x[j]*cmath.exp(-2j*math.pi*k*j/n) for j in range(n))/math.sqrt(n) for k in range(n)]
assert H[1]==0 and abs(W[1]-1)<1e-14
assert caught_bad_zero(abs(W[1]))
out["window_frequency_mixing"]={"input_kept_bin_norm":abs(H[1]),"outside_bin_amplitude":abs(H[3]),"output_kept_bin_amplitude":abs(W[1])}

# Conditioning failure: rank2 for each s>0 does not give a common lower bound.
degenerate=[]
for s in [Q(1,10),Q(1,1000),Q(1,1000000)]:
    h=[Q(0),1/s]
    nominal=[[Q(1),Q(0)],[Q(0),s],[Q(0),Q(0)]]
    error=[[Q(0),Q(0)],[Q(0),Q(0)],[Q(0),s/2]]
    y=[u+v for u,v in zip(mv(nominal,h),mv(error,h))]
    assert y==[0,1,Q(1,2)]
    degenerate.append({"s":str(s),"h_norm":norm(h),"y_norm":norm(y),"epsilon_over_gamma":.5})
out["rank_without_uniform_recovery"]=degenerate

# Even two input function spaces can cover three output spaces through shifts.
# Three Fourier modes per input, two per output: a permutation is onto.
input6=[Q(2),Q(3),Q(5),Q(7),Q(11),Q(13)]
output3x2=[input6[0:2],input6[2:4],input6[4:6]]
assert sum(output3x2,[])==input6
out["domain_dimension_separator"]="Two functions with3 modes each can map bijectively to three channels with2 retained modes each; codimension0, no nonzero output null."

# Same scalar marginals, opposite cross-correlations, different null variance.
b2=[1.,-1.]
Cplus=[[1.,1.],[1.,1.]]
Cminus=[[1.,-1.],[-1.,1.]]
def variance(row,c):
    return sum(complex(row[i])*complex(c[i][j])*complex(row[j]).conjugate() for i in range(len(row)) for j in range(len(row)))
vplus=variance(b2,Cplus).real
vminus=variance(b2,Cminus).real
assert vplus==0 and vminus==4
out["equal_marginal_covariances"]={"same_diagonal":[1,1],"contrast_variances":[vplus,vminus],"matrices_positive_semidefinite":"outer products [1,1] and [1,-1]"}
# Exact disjoint marginal-failure atoms: marginals coverage2/3, joint0.
atoms=[(1,0,0),(0,1,0),(0,0,1)]
marginal=[sum(Q(1,3) for row in atoms if row[j]==0) for j in range(3)]
joint=sum((Q(1,3) for row in atoms if not any(row)),Q(0))
assert marginal==[Q(2,3)]*3 and joint==0
out["pointwise_not_joint"]={"marginal_coverage":list(map(str,marginal)),"simultaneous":str(joint)}

# Inverse calibration direction and safe bound.
ratio=complex(1.02,.03)
release=1/ratio
assert abs(release*ratio-1)<1e-14
rho=abs(ratio-1)
assert rho<1 and abs(release-1)<=rho/(1-rho)
out["calibration_inverse"]={"true_over_model":[ratio.real,ratio.imag],"release_over_true":[release.real,release.imag],"actual_defect":abs(release-1),"bound":rho/(1-rho)}

# Constant delay frequency multiplier bound; numerical anchors only.
rows=[]
for bandwidth in [1.,30.,500.]:
    for dt in [0.,1e-6,1e-3,.1]:
        largest=0.
        for i in range(201):
            f=bandwidth*(i-100)/100
            err=abs(cmath.exp(2j*math.pi*f*dt)-1)
            upper=min(2.,2*math.pi*bandwidth*abs(dt))
            assert err<=upper+2e-14
            largest=max(largest,err)
        rows.append({"B":bandwidth,"delay":dt,"sampled_max":largest,"uniform_bound":min(2.,2*math.pi*bandwidth*abs(dt))})
out["constant_delay"]=rows
out["passed"]=True
print(json.dumps(out,sort_keys=True,indent=2))

