"""Distinct QC1 probe: arbitrary rational Laurent profiles, not a Green solver.

Recompute residual and anchor-matched comparison directly from each profile.
Exact Fraction bounds are supplemented by 60-digit Decimal nonlinear readouts.
No author code or output is read. Finite probes do not certify sup hypotheses.
"""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
import json
import platform
import random

rng=random.Random(260)
l,u=F(1,2),F(2)
m=F(1,2)
grid=[F(i,8) for i in range(4,17)]
counts={'exact_profile':0,'decimal_readout':0,'positivity':0,'mutation_rejections':0}

def evaluate(poly,x,derivative=0):
    answer=F(0)
    for k,v in poly.items():
        coeff=v
        for j in range(derivative):
            coeff*=k-j
        answer+=coeff*x**(k-derivative)
    return answer
def majorant(poly):
    return sum(abs(v)*max(l**k,u**k) for k,v in poly.items())
def U(x): return (x*x+2/x)/3
def V(x): return (x*x-1/x)/3
def U1(x): return (2*x-2/x**2)/3
def V1(x): return (2*x+1/x**2)/3
def U2(x): return (2+4/x**3)/3
def V2(x): return (2-2/x**3)/3
def dec(f): return D(f.numerator)/D(f.denominator)

worst_profile_ratio=F(0)
with localcontext() as ctx:
    ctx.prec=60
    for case in range(36):
        # Fixed reference-sized coefficients plus free signed perturbations.
        # Baseline positive lower bound is1; absolute perturbation majorant is
        # verified, not inferred from sample values.
        perturb={k:F(rng.randrange(-9,10),100000) for k in range(-3,5)}
        profile=dict(perturb)
        for k,v in {0:F(1),2:F(1,10),-1:F(1,10)}.items():
            profile[k]=profile.get(k,F(0))+v
        assert majorant(perturb)<F(1,4)
        delta0=F(rng.randrange(-9,10),100000)
        delta1=F(rng.randrange(-9,10),100000)
        d0=evaluate(profile,F(1))-delta0
        d1=evaluate(profile,F(1),1)-delta1
        A=(d0-1+d1)/3
        B=(2*(d0-1)-d1)/3
        reference={0:F(1),2:A,-1:B}
        assert A>=0 and B>=0  # Hence reference>=1 on the entire positive axis.
        counts['positivity']+=2
        residual={k:v*(k*(k-1)/2-1) for k,v in profile.items()}
        # Integer division above is deliberately replaced by exact arithmetic.
        residual={k:v*(F(k*(k-1),2)-1) for k,v in profile.items()}
        residual[0]=residual.get(0,F(0))+1
        epsilon=majorant(residual)
        eta0,eta1=abs(delta0),abs(delta1)
        D0=eta0*max(U(l),U(u))+eta1*max(abs(V(l)),abs(V(u)))+epsilon*(max(U(l),U(u))-1)
        D1=(eta0+epsilon)*max(abs(U1(l)),abs(U1(u)))+eta1*max(V1(l),V1(u))
        D2=(eta0+epsilon)*U2(l)+eta1*max(abs(V2(l)),abs(V2(u)))
        for x in grid:
            b=[eta0*U(x)+eta1*abs(V(x))+epsilon*(U(x)-1),
               (eta0+epsilon)*abs(U1(x))+eta1*V1(x),
               (eta0+epsilon)*U2(x)+eta1*abs(V2(x))]
            for j,limit in enumerate(b):
                actual=abs(evaluate(profile,x,j)-evaluate(reference,x,j))
                assert actual<=limit<=[D0,D1,D2][j], (case,x,j,actual,limit)
                counts['exact_profile']+=1
                if limit:
                    worst_profile_ratio=max(worst_profile_ratio,actual/limit)
            q,p=dec(evaluate(profile,x)),dec(evaluate(reference,x))
            qp,pp=dec(evaluate(profile,x,1)),dec(evaluate(reference,x,1))
            mm=dec(m)
            hdiff=abs(qp/(2*q)-pp/(2*p))
            hbound=dec(b[1])/(2*mm)+abs(pp)*dec(b[0])/(2*mm**2)
            jdiff=abs(qp/(2*q.sqrt())-pp/(2*p.sqrt()))
            jbound=dec(b[1])/(2*mm.sqrt())+abs(pp)*dec(b[0])/(4*mm*mm.sqrt())
            assert hdiff<=hbound and jdiff<=jbound
            counts['decimal_readout']+=2
            for z in (l,F(1),u):
                qz,pz=dec(evaluate(profile,z)),dec(evaluate(reference,z))
                b0z=eta0*U(z)+eta1*abs(V(z))+epsilon*(U(z)-1)
                actual=abs(((q/qz)/(p/pz)).ln())/2
                bound=dec(b[0]+b0z)/(2*mm)
                assert actual<=bound+D('1e-56')  # Decimal-rounding allowance only.
                counts['decimal_readout']+=1

# Actual false-pass catches: each corrupted claim must throw AssertionError.
# Three failures correspond to omitting each independent error/control input.
def reject(label,callback):
    try:
        callback()
    except AssertionError:
        counts['mutation_rejections']+=1
        return
    raise AssertionError('corruption unexpectedly accepted: '+label)
def gate(a,b): assert a<=b
reject('omit value data',lambda:gate(U(F(2)),F(0)))
reject('omit slope data',lambda:gate(abs(V(F(2))),F(0)))
reject('omit residual input',lambda:gate(U(F(2))-1,F(0)))
reject('negative left kernel mass',lambda:gate(abs(U1(F(1,2))),U1(F(1,2))))

print(json.dumps({'status':'PASS','python':platform.python_version(),
 'method':'exact rational direct Laurent profile/residual/data evaluation; Decimal nonlinear readouts',
 'profiles':36,'points_per_profile':len(grid),'radius_domain':['1/2','2'],
 'certified_common_positive_lower_bound':'1/2','decimal_precision':60,
 'decimal_log_rounding_allowance':'1e-56','counts':counts,
 'maximum_exact_profile_bound_ratio':str(worst_profile_ratio),
 'author_code_or_output_imported':False,'candidate_exposed_before_this_script':True},indent=2))
