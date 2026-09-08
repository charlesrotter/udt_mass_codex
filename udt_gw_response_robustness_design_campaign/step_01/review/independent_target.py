"""RD1 target checks via scalar quadrature/elimination and exact rational geometry."""
import hashlib
import json
import math
import pathlib
import platform
from fractions import Fraction as Q

ROOT=pathlib.Path(__file__).resolve().parents[3]
P=pathlib.Path(__file__).resolve().parents[1]
expected={"CANDIDATE.md":"46e8002a6a0138eaf993476fdc1dd9bbf2a724413bd9558efead2e1229779803","checks.py":"0be202298d3d5c523f53443786e3776b66196f4f9e461fd61d4ef1c767aeb152","checks_run.stdout":"1c15a27b5d32888360746953a4782f88c7cf5ebd8ed8c0212bcb0c78c919915e"}
for name,sha in expected.items():
    assert hashlib.sha256((P/name).read_bytes()).hexdigest()==sha
author=json.loads((P/"checks_run.stdout").read_text())
cofile=ROOT/"udt_complementary_wave_observable_campaign_2026-09-07/step_02/design_run.stdout"
assert hashlib.sha256(cofile.read_bytes()).hexdigest()=="b89c8e432788842cdbddc1270c3135043e60f12c557cb24725d2162560fdfac2"
co=json.loads(cofile.read_text())
F=co["F_HLV_plus_cross"]
a,b=F[0]; c,d=F[1]
det=a*d-b*c
inv=[[d/det,-b/det],[-c/det,a/det]]
ga=sum(row[0]**2 for row in inv)
gb=sum(row[0]*row[1] for row in inv)
gc=sum(row[1]**2 for row in inv)
bn=math.sqrt((ga+gc+math.hypot(ga-gc,2*gb))/2)
S=[sum(F[2][i]*inv[i][j] for i in range(2)) for j in range(2)]
sn=math.sqrt(sum(v*v for v in S))
assert abs(bn/author["B_norm"]-1)<1e-13
assert max(abs(u-v) for u,v in zip(S,author["S"]))<1e-13
tau=[Q(str(x)) for x in co["arrival_minus_geocenter_seconds"]]
seps=[(tau[i]-tau[j])*4096 for i in range(3) for j in range(i)]
assert all(x.denominator!=1 for x in seps)
assert list(map(str,seps))==author["asynchronous_nominal_fractional_sample_differences"]
assert all(row[0]!=0 for row in F)
xL=math.pi*500*4000/299792458
xV=math.pi*500*3000/299792458
eL=xL+4*xL*xL/3
eV=xV+4*xV*xV/3
kappa=bn*math.sqrt(2)*eL
rho=eV+sn*math.sqrt(2)*eL
assert abs(kappa/author["arm"]["arm_only_kappa"]-1)<1e-13
assert abs(rho/author["arm"]["arm_only_rho"]-1)<1e-13

def dot(u,v):
    return sum(x*y for x,y in zip(u,v))
def mv(A,x):
    return [dot(row,x) for row in A]
def solve(A,b):
    rows=[list(row)+[rhs] for row,rhs in zip(A,b)]
    n=len(b)
    for j in range(n):
        k=max(range(j,n),key=lambda k:abs(rows[k][j]))
        rows[j],rows[k]=rows[k],rows[j]
        pivot=rows[j][j]
        assert abs(pivot)>1e-14
        for k in range(j,n+1):
            rows[j][k]/=pivot
        for i in range(n):
            if i!=j:
                factor=rows[i][j]
                for k in range(j,n+1):
                    rows[i][k]-=factor*rows[j][k]
    return [row[-1] for row in rows]
def integrate(fn,lo,hi,n):
    dx=(hi-lo)/n
    v=fn(lo)+fn(hi)
    for i in range(1,n):
        v+=(4 if i%2 else 2)*fn(lo+i*dx)
    return v*dx/3
def K(s,n):
    return 2*integrate(lambda f:math.cos(2*math.pi*f*s),1.,4.,n)
times=[0.,.08,.21,.39]
v=[.2,-.1,.7,-.3]
gram=[[K(s-t,2048) for t in times] for s in times]
gram_coarse=[[K(s-t,1024) for t in times] for s in times]
coef=solve(gram,v)
norm2=dot(v,coef)
norm2coarse=dot(v,solve(gram_coarse,v))
assert abs(norm2/author["interpolation"]["norm_squared"]-1)<1e-10
res=math.sqrt(sum((a-b)**2 for a,b in zip(mv(gram,coef),v)))/math.sqrt(dot(v,v))
assert res<1e-12
train=gram[:3]
train=[row[:3] for row in train]
y=v[:3]
cross=[gram[i][3] for i in range(3)]
s=solve(train,y)
h0sq=dot(y,s)
prediction=dot(cross,s)
psq=gram[3][3]-dot(cross,solve(train,cross))
radius=math.sqrt(.4*psq)
hmaxsq=h0sq+.4
endpoint=[]
for sign in [-1,1]:
    vec=y+[prediction+sign*radius]
    val=dot(vec,solve(gram,vec))
    assert abs(val/hmaxsq-1)<1e-12
    endpoint.append(val)
for key,value in [("h0_norm_squared",h0sq),("prediction",prediction),("p_norm_squared",psq),("sharp_radius",radius)]:
    assert abs(value-author["holdout"][key])<1e-10
# A strictly wider holdout interval fails the same norm budget.
outside=y+[prediction+1.001*radius]
outside_norm2=dot(outside,solve(gram,outside))
assert outside_norm2>hmaxsq
# Source-defined kernel L2 norm by independent spectrum integration.
def spectral_energy(f):
    real=sum(q*math.cos(2*math.pi*f*t) for q,t in zip(coef,times))
    imag=-sum(q*math.sin(2*math.pi*f*t) for q,t in zip(coef,times))
    return real*real+imag*imag
spectral=2*integrate(spectral_energy,1,4,4096)
assert abs(spectral/norm2-1)<1e-11

# Exact abstract sharpness anchor independent of trigonometric/kernel numerics.
T=[[Q(1),Q(1),Q(0)],[Q(0),Q(1),Q(1)]]
k=[Q(1),Q(-1),Q(2)]
h0=[Q(0),Q(1),Q(1)]
z=[Q(1),Q(-1),Q(1)]
assert mv(T,h0)==[1,2] and mv(T,z)==[0,0]
assert dot(h0,z)==0 and dot(h0,h0)==2 and dot(z,z)==3
exact=[]
for sign in [-1,1]:
    h=[a+sign*b for a,b in zip(h0,z)]
    assert mv(T,h)==[1,2] and dot(h,h)==5
    exact.append(str(dot(k,h)))
assert exact==["-3","5"]
# p=0 holdout is directly predictable, despite nonzero null kernel.
k0=[Q(1),Q(2),Q(1)]
assert dot(k0,z)==0
assert all(dot(k0,[a+q*b for a,b in zip(h0,z)])==3 for q in [Q(-10),Q(0),Q(9)])
out={"passed":True,"python":platform.python_version(),"method":"stdlib scalar Simpson integrals, pivoted elimination, closed2x2 Gram eigenvalue; Fraction sharpness; no NumPy or producer import","pins":expected,"CO2_pin":"b89c8e432788842cdbddc1270c3135043e60f12c557cb24725d2162560fdfac2","B_norm":bn,"S":S,"S_norm":sn,"threshold":1/bn,"nominal_delay_fractional_samples":list(map(str,seps)),"arm_only":{"kappa":kappa,"rho":rho},"kernel":{"norm2_n1024":norm2coarse,"norm2_n2048":norm2,"quadrature_spectral_norm2":spectral,"interpolation_relative_residual":res},"holdout":{"h0_norm2":h0sq,"p_norm2":psq,"prediction":prediction,"radius":radius,"H_max_squared":hmaxsq,"endpoint_norms":endpoint,"outside_1p001_radius_norm2":outside_norm2},"exact_abstract":{"training":[1,2],"H_max_squared":5,"sharp_endpoints":exact,"zero_p_prediction":"3","kernel_dimension":1},"finite_scope":"independent anchors; analytic proof owns all distinct times/targets and sharp intervals"}
print(json.dumps(out,sort_keys=True,indent=2))

