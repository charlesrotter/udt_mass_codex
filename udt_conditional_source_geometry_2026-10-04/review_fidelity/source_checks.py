#!/usr/bin/env python3
"""Independent exact source-first checks; no parent candidate imports."""
import json
import os
import platform
import resource
from pathlib import Path

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
assert os.environ.get("OPENBLAS_NUM_THREADS") == "1"
assert os.environ.get("OMP_NUM_THREADS") == "1"
import sympy as S

out = Path(__file__).resolve().parent
checks = []
def zero(name, expr):
    value = S.simplify(S.trigsimp(expr))
    if value != 0:
        raise AssertionError((name, str(value)))
    checks.append(name)

t,r,theta,phi=S.symbols("t r theta phi", real=True)
m,Lam=S.symbols("m Lambda", real=True)
x=[t,r,theta,phi]
f=1-2*m/r-Lam*r*r/3
g=S.diag(-f,1/f,r*r,r*r*S.sin(theta)**2)
inv=g.inv()
Gamma=[[[S.simplify(sum(inv[i,d]*(S.diff(g[d,k],x[j])+S.diff(g[d,j],x[k])-S.diff(g[j,k],x[d])) for d in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
for i in range(4):
    for j in range(4):
        ric=sum(S.diff(Gamma[k][i][j],x[k])-S.diff(Gamma[k][i][k],x[j])+sum(Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k] for l in range(4)) for k in range(4))
        zero(f"full_coordinate_Ricci_{i}{j}",ric-Lam*g[i,j])

Om=S.sqrt(m/r**3-Lam/3)
Ut=1/S.sqrt(1-3*m/r)
u=S.Matrix([Ut,0,0,Om*Ut])
geq=g.subs(theta,S.pi/2)
zero("circular_unit_norm",(u.T*geq*u)[0]+1)
for i in range(4):
    zero(f"circular_original_geodesic_{i}",sum(Gamma[i][j][k].subs(theta,S.pi/2)*u[j]*u[k] for j in range(4) for k in range(4)))

F,e,v,b,R,E,q=S.symbols("F e v b R E q",positive=True)
gr=S.diag(-F,1/F,R*R,R*R)
ur=S.Matrix([e/F,v,0,0])
er=S.Matrix([v/F,e,0,0])
ep=S.Matrix([0,0,0,1/R])
kk=S.Matrix([E/F,E*q,0,E*b/R**2])
def reduce(expr):
    expr=S.factor(expr)
    expr=S.together(expr).subs(e**2,F+v**2).subs(q**2,1-F*b*b/R**2)
    return S.factor(expr)
zero("receiver_unit_norm",reduce((ur.T*gr*ur)[0]+1))
zero("receiver_radial_axis_norm",reduce((er.T*gr*er)[0]-1))
zero("receiver_tetrad_orthogonality",(ur.T*gr*er)[0])
zero("receiver_phi_axis_norm",(ep.T*gr*ep)[0]-1)
zero("original_null_norm",reduce((kk.T*gr*kk)[0]))
w=-(ur.T*gr*kk)[0]
nr=-(er.T*gr*kk)[0]/w
np=-(ep.T*gr*kk)[0]/w
zero("sky_tetrad_radial_formula",nr-(v-e*q)/(e-v*q))
zero("sky_tetrad_phi_formula",np+F*b/(R*(e-v*q)))
zero("sky_unit_identity",reduce(nr**2+np**2-1))

# Differentiate actual two-point null incidence before setting the base ray b=0.
bb=S.symbols("bb",real=True)
Tintegrand=1/(f*S.sqrt(1-f*bb**2/r**2))
Phiintegrand=bb/(r**2*S.sqrt(1-f*bb**2/r**2))
zero("radial_base_T_b",S.diff(Tintegrand,bb).subs(bb,0))
zero("radial_base_Phi_b",S.diff(Phiintegrand,bb).subs(bb,0)-1/r**2)
ss=S.symbols("s",positive=True)
ee=(ss+F/ss)/2
vv=(ss-F/ss)/2
zero("redshift_inverse_timelike",ee**2-vv**2-F)
zero("redshift_inverse_same_Z",ee+vv-ss)
zero("arrival_vs_contraction",F/(ee-vv)-(ee+vv))

records=[]
for lam in [-S.Rational(1,100000),S.Integer(0),S.Rational(1,100000)]:
    a0=S.Integer(10); R0=S.Integer(30); m0=S.Integer(1)
    fA=f.subs({r:a0,m:m0,Lam:lam})
    fR=f.subs({r:R0,m:m0,Lam:lam})
    ut=Ut.subs({r:a0,m:m0})
    omega2=m0/a0**3-lam/3
    # Analytic interval bound: f>=1-2/a-|Lambda| R²/3 >0 for a<=r<=R.
    assert 1-2/a0-abs(lam)*R0**2/3>0 and omega2>0 and 1-3*m0/a0>0
    for z in [S.Rational(3,4),S.Rational(4,3)]:
        s0=z/ut; e0=(s0+fR/s0)/2; v0=(s0-fR/s0)/2
        assert e0>0
        zero(f"radial_case_norm_{lam}_{z}",e0**2-v0**2-fR)
        zero(f"radial_case_shift_{lam}_{z}",ut*(e0+v0)-z)
        records.append({"kind":"radial_shift","Lambda":str(lam),"target_Z":str(z),"f_R":str(fR),"e":str(e0),"v":str(v0)})
    for b0 in [-S.Integer(2),S.Integer(2)]:
        v0=S.Rational(1,5); e0=S.sqrt(fR+v0*v0)
        q0=S.sqrt(1-fR*b0*b0/R0**2)
        assert 1-fR*b0*b0/R0**2>0 and e0-v0*q0>0
        values={F:fR,R:R0,e:e0,v:v0,b:b0,E:1,q:q0}
        zero(f"nonradial_sky_norm_{lam}_{b0}",(nr**2+np**2-1).subs(values))
        records.append({"kind":"nonradial_endpoint","Lambda":str(lam),"b":str(b0),"v":str(v0)})
assert len(records)==12
result={"status":"PASS","evidence":"exact symbolic and rational arithmetic; not empirical or global certification","checks":checks,"finite_case_count":len(records),"cases":records,"versions":{"python":platform.python_version(),"sympy":S.__version__},"resources":{"RLIMIT_AS_bytes":resource.getrlimit(resource.RLIMIT_AS),"OPENBLAS_NUM_THREADS":os.environ["OPENBLAS_NUM_THREADS"],"OMP_NUM_THREADS":os.environ["OMP_NUM_THREADS"],"maxrss_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(out/"SOURCE_CHECK_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"status":"PASS","exact_checks":len(checks),"finite_cases":len(records),"versions":result["versions"]},indent=2))
