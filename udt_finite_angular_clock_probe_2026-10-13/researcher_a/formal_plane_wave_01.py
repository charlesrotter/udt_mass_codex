"""Actual PSW clocks in a supplied symmetric plane wave; exact formal author check.

Coordinates a=sqrt(2)u,b=sqrt(2)v give
g=-da db+dx^2+dy^2+(x^2-y^2)da^2/2. Central U=(1,1,0,0).
Direction n=(n_x,n_y,Z), X=n_x^2 and n_y^2=1-X-Z^2.
"""
import hashlib
import json
from pathlib import Path
import platform
import time
import sympy as s

L, xi, eta, X, Z = s.symbols('L xi eta X Z')
weights = [X,1-X-Z**2]
H = [s.Rational(1,2),s.Rational(-1,2)]


def trunc(expr, degree=6):
    return s.Poly(s.expand(expr),L).slice(0,degree+1).as_expr()


def S(h,arg):
    return arg+h*arg**3/6+h**2*arg**5/120


def C(h,arg):
    return 1+h*arg**2/2+h**2*arg**4/24


def sphere(expr):
    result=0
    for (i,j),coef in s.Poly(s.expand(expr),X,Z).terms():
        if j % 2:
            continue
        result+=coef*s.factorial2(2*i-1)*s.factorial2(j-1)/s.factorial2(2*i+j+1)
    return s.factor(result)


def assertzero(expr,label):
    assert s.expand(expr)==0,(label,s.factor(expr))


def main():
    started=time.monotonic()
    # These are the exact geodesic/transport formulas truncated consistently.
    # B proper time is L*eta. A proper time is L*xi.
    xb=[];vb=[];prep_x=[];prep_Ux=[]
    for h in H:
        xb.append(s.expand((S(h,L*(Z+eta))-S(h,L*eta))/Z))
        vb.append(s.expand((C(h,L*(Z+eta))-C(h,L*eta))/Z))
        prep_x.append(s.expand(S(h,Z*L)/Z))
        prep_Ux.append(s.expand((C(h,Z*L)-1)/Z))
    b0=-Z*L+sum(weights[i]*(s.Rational(2,3)*H[i]*Z*L**3+s.Rational(2,15)*H[i]**2*Z**3*L**5) for i in range(2))
    bB=trunc(b0+L*eta+sum(weights[i]*(xb[i]*vb[i]-prep_x[i]*prep_Ux[i]) for i in range(2)),5)
    aB=L*(Z+eta)
    # Timelike geodesic normalization along the complete freely released B.
    norm=trunc(-s.diff(bB,eta)/L+sum(weights[i]*(vb[i]**2+H[i]*xb[i]**2) for i in range(2))+1,4)
    assertzero(norm,'B_unit_timelike')
    for i,h in enumerate(H):
        assertzero(trunc(s.diff(xb[i],eta,2)/L**2-h*xb[i],3),'B_original_x_geodesic')
    # Original spacelike preparation norm and parallel transport x equations.
    for i,h in enumerate(H):
        assertzero(trunc(s.diff(prep_Ux[i],L)-h*Z*prep_x[i],3),'prep_Ux_parallel')
    prep_norm=trunc(-Z*s.diff(b0,L)+sum(weights[i]*(C(H[i],Z*L)**2+H[i]*Z**2*prep_x[i]**2) for i in range(2))-1,4)
    assertzero(prep_norm,'prep_unit_spacelike')
    # Null incidence derived from integral of original null equation:
    # (aB-aA)(bB-bA)=sum [d*C_h(d)/S_h(d)] xB_i^2.
    d=aB-L*xi
    F=trunc(d*(bB-L*xi)-sum(weights[i]*(1+H[i]*d**2/3-H[i]**2*d**4/45)*xb[i]**2 for i in range(2)),6)/L**2
    F=s.expand(F)
    assertzero(F.coeff(L,0)-((eta-xi)**2-1),'flat_incidence')
    result={'metric':'-da db+dx^2+dy^2+(x^2-y^2)da^2/2',
            'central_U':'partial_a+partial_b','angular_variables':'X=n_x^2,Z=n_z; n_y^2=1-X-Z^2',
            'python':platform.python_version(),'sympy':s.__version__,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'incidence_scaled':str(s.factor(F))}
    for branch in ['forward','reverse']:
        source,target=(xi,eta) if branch=='forward' else (eta,xi)
        c2,c4=s.symbols('c2 c4')
        root=1+c2*L**2+c4*L**4
        residual=trunc(F.subs(source,0).subs(target,root),4)
        solution=s.solve([residual.coeff(L,2),residual.coeff(L,4)],(c2,c4),dict=True)[0]
        root=s.expand(root.subs(solution))
        assertzero(trunc(F.subs(source,0).subs(target,root),4),branch+'_incidence')
        numerator=trunc(-s.diff(F,source).subs(source,0).subs(target,root),4)
        denominator=trunc(s.diff(F,target).subs(source,0).subs(target,root),4)
        # Both factors have the same nonzero constant 2 on future branches.
        assert numerator.coeff(L,0)==denominator.coeff(L,0)==2
        n2,n4=numerator.coeff(L,2)/2,numerator.coeff(L,4)/2
        d2,d4=denominator.coeff(L,2)/2,denominator.coeff(L,4)/2
        logp=s.expand((n2-d2)*L**2+(n4-d4-(n2**2-d2**2)/2)*L**4)
        output={'arrival_proper_over_L':str(s.factor(root)),
                'log_L2':str(s.factor(logp.coeff(L,2))),
                'log_L4':str(s.factor(logp.coeff(L,4))),
                'mean_L2':str(sphere(logp.coeff(L,2))),
                'mean_L4':str(sphere(logp.coeff(L,4)))}
        result[branch]=output
        print(branch,json.dumps(output),flush=True)
    result['duration_seconds']=time.monotonic()-started
    target=Path(__file__).with_name('formal_plane_wave_01_result.json')
    with target.open('x') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    main()
