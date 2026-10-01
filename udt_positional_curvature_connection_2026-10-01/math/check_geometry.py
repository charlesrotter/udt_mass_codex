#!/usr/bin/env python3
"""Independent source-first PCC1 control; exact direct-connection calculation.

FREE: all supplied metric parameters and their comparison matching.
No field equation, source, response identification or selected physical scale.
Run only through the work-order capture wrapper after the parent grants CPU.
"""
import hashlib
import itertools
import json
import platform
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent
checks = []


def eq(label, lhs, rhs=0):
    residual = s.simplify(lhs-rhs)
    checks.append({"label": label, "residual": str(residual), "pass": residual == 0})
    if residual != 0:
        raise AssertionError((label, residual))


def direct(diag, coords):
    """Return all lower R(a,b,c,d)=g(R(d_a,d_b)d_c,d_d) components."""
    n = len(coords)
    gam = {}
    for a,b,c in itertools.product(range(n), repeat=3):
        gam[a,b,c] = s.simplify((
            (s.diff(diag[a], coords[b]) if a == c else 0)
            +(s.diff(diag[a], coords[c]) if a == b else 0)
            -(s.diff(diag[b], coords[a]) if b == c else 0)
        )/(2*diag[a]))
    curv = {}
    for a,b,c,d in itertools.product(range(n), repeat=4):
        value = s.diff(gam[d,b,c],coords[a])-s.diff(gam[d,a,c],coords[b])
        value += sum(gam[d,a,h]*gam[h,b,c]-gam[d,b,h]*gam[h,a,c]
                     for h in range(n))
        curv[a,b,c,d] = s.simplify(diag[d]*value)
    section = {(a,b):s.simplify(curv[a,b,b,a]/(diag[a]*diag[b]))
               for a in range(n) for b in range(a+1,n)}
    ric = [[s.simplify(sum(curv[h,b,c,h]/diag[h] for h in range(n)))
            for c in range(n)] for b in range(n)]
    scalar = s.simplify(sum(ric[a][a]/diag[a] for a in range(n)))
    return curv, section, ric, scalar


def mixed_check(tag, curv):
    selected = [(idx,value) for idx,value in curv.items()
                if not (idx[0] == idx[3] and idx[1] == idx[2])
                and not (idx[0] == idx[2] and idx[1] == idx[3])]
    for idx,value in selected:
        eq(f"{tag} mixed {idx}",value)
    return len(selected)


def specialize(expression, function, actual):
    return s.simplify(expression.subs(function, actual).doit())


def sectional_tensor(section):
    eta = [-1,1,1,1]
    ans = {}
    for a,b,c,d in itertools.product(range(4),repeat=4):
        value = 0
        if a != b:
            kval = section[tuple(sorted((a,b)))]
            if a == d and b == c:
                value = eta[a]*eta[b]*kval
            elif a == c and b == d:
                value = -eta[a]*eta[b]*kval
        ans[a,b,c,d] = s.sympify(value)
    return ans


t,r,theta,phi = s.symbols("t r theta phi", real=True)
m,k,c = s.symbols("m k c", real=True)
f = s.Function("f")(r)
curv,section,ric,scalar = direct([-f,1/f,r*r,r*r*s.sin(theta)**2],
                                [t,r,theta,phi])
static_mixed = mixed_check("static",curv)
fk = 1-2*m/r-k*r*r
f0 = 1-2*m/r
physical = {ij:specialize(v,f,fk) for ij,v in section.items()}
reference = {ij:specialize(v,f,f0) for ij,v in section.items()}
expected = {(0,1):2*m/r**3+k,(0,2):-m/r**3+k,(0,3):-m/r**3+k,
            (1,2):-m/r**3+k,(1,3):-m/r**3+k,(2,3):2*m/r**3+k}
for ij,value in physical.items():
    eq(f"static sectional {ij}",value,expected[ij])
    eq(f"static contrast {ij}",value-reference[ij],k)
eq("static scalar",specialize(scalar,f,fk),12*k)
for i,di in enumerate([-fk,1/fk,r*r,r*r*s.sin(theta)**2]):
    eq(f"static Ricci diagonal {i}",specialize(ric[i][i],f,fk),3*k*di)
    for j in range(4):
        if j != i:
            eq(f"static Ricci offdiagonal {i},{j}",specialize(ric[i][j],f,fk))
static_delta = sectional_tensor({ij:physical[ij]-reference[ij] for ij in physical})
unit_form = sectional_tensor({ij:1 for ij in physical})
for idx,value in static_delta.items():
    eq(f"static full tensor contrast {idx}",value,k*unit_form[idx])

x,y,z = s.symbols("x y z",real=True)
a = s.Function("a")(t)
fc,fs,fr,fscl = direct([-1,a*a,a*a,a*a],[t,x,y,z])
flrw_mixed = mixed_check("isotropic-time",fc)
a0 = s.exp(t*t/2)
a1 = s.exp(t*t/2+c*t)
fp = {ij:specialize(v,a,a1) for ij,v in fs.items()}
fref = {ij:specialize(v,a,a0) for ij,v in fs.items()}
for ij in fp:
    eq(f"variable contrast {ij}",fp[ij]-fref[ij],2*c*t+c*c)
eq("variable contrast derivative",s.diff(fp[0,1]-fref[0,1],t),2*c)
fd = sectional_tensor({ij:fp[ij]-fref[ij] for ij in fp})
for idx,value in fd.items():
    eq(f"variable full tensor contrast {idx}",value,(2*c*t+c*c)*unit_form[idx])

# Algebraic curvature of -dt^2 plus constant-curvature spatial 3-metric.
# A rational boost probes a direction invisible to the unboosted electric form.
prod = sectional_tensor({ij:(0 if 0 in ij else c) for ij in physical})
u = [s.Rational(5,4),s.Rational(3,4),0,0]
nlong = [s.Rational(3,4),s.Rational(5,4),0,0]
ntrans = [0,0,1,0]


def contract(tensor,n,u):
    return s.simplify(sum(value*n[i]*u[j]*u[l]*n[h]
                         for (i,j,l,h),value in tensor.items()))


eq("one-frame longitudinal",contract(prod,nlong,u),0)
eq("one-frame boosted transverse",contract(prod,ntrans,u),9*c/16)
for i in (1,2,3):
    n = [int(j == i) for j in range(4)]
    eq(f"unboosted product electric {i}",contract(prod,n,[1,0,0,0]))

at = {m:1,r:4,k:s.Rational(1,100)}
tides = [-physical[0,i].subs(at) for i in (1,2,3)]
for i,want in enumerate([-s.Rational(33,800),s.Rational(9,1600),s.Rational(9,1600)]):
    eq(f"regular sample tide {i}",tides[i],want)
eq("sample physical lapse",fk.subs(at),s.Rational(17,50))
eq("sample reference lapse",f0.subs(at),s.Rational(1,2))

output = {
    "status":"PASS",
    "kind":"exact symbolic controls, not all-frame proof or physical adoption",
    "python":platform.python_version(),"sympy":s.__version__,
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "convention":"R(X,Y)Z=[nabla_X,nabla_Y]Z-nabla_[X,Y]Z; (-+++)",
    "static_sectionals":{str(ij):str(v) for ij,v in physical.items()},
    "static_reference_sectionals":{str(ij):str(v) for ij,v in reference.items()},
    "static_scalar":str(specialize(scalar,f,fk)),
    "static_sample_tides":list(map(str,tides)),
    "static_mixed_components_checked":static_mixed,
    "time_family_sectionals":{str(ij):str(v) for ij,v in fp.items()},
    "time_reference_sectionals":{str(ij):str(v) for ij,v in fref.items()},
    "time_contrast":"2*c*t+c**2","time_mixed_components_checked":flrw_mixed,
    "one_frame_boosted_transverse":str(contract(prod,ntrans,u)),
    "checks":checks,"check_count":len(checks),
}
(ROOT/"geometry_output.json").write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps({"status":output["status"],"check_count":len(checks),
                  "script_sha256":output["script_sha256"]}))
