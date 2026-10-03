"""Independent numerical incidence and exact conformal-metric checks."""
import json,hashlib,sys,platform,time
from pathlib import Path
import mpmath as mp
import sympy as sp
B=Path(__file__).resolve().parent
def echo():
    records=[];gates={}
    for digits in [60,100]:
        with mp.workdps(digits):
            for speed in ['0','0.6','-0.6','0.8']:
                v=mp.mpf(speed);gamma=1/mp.sqrt(1-v*v)
                for denom in [10,20,40,80,160]:
                    L=mp.mpf(1)/denom
                    def F(e,r):return mp.cosh(e)*mp.cosh(r)*mp.cos(L)-mp.sinh(e)*mp.sinh(r)-mp.cosh(v*(r-e))
                    def arrive(e):
                        lo=e+gamma*L/2;hi=e+2*gamma*L
                        assert F(e,lo)<0<F(e,hi)
                        r=mp.findroot(lambda r:F(e,r),(lo,hi),solver='anderson',tol=mp.mpf(10)**(-digits+10),maxsteps=200)
                        assert r>e and abs(F(e,r))<mp.mpf(10)**(-digits+8)
                        return r
                    def period(e,r):
                        fe=mp.sinh(e)*mp.cosh(r)*mp.cos(L)-mp.cosh(e)*mp.sinh(r)+v*mp.sinh(v*(r-e))
                        fr=mp.cosh(e)*mp.sinh(r)*mp.cos(L)-mp.sinh(e)*mp.cosh(r)-v*mp.sinh(v*(r-e))
                        return -fe/fr
                    b=arrive(mp.mpf(0));a=arrive(b);p=period(mp.mpf(0),b);q=period(b,a)
                    assert 0<p<mp.sqrt(2) and q>0
                    D=mp.log(q)-mp.log(p/(2-p*p));pred=-v*v/(3*(1-v*v)**3)
                    row=dict(digits=digits,speed=speed,L_denominator=denom,
                        **{name:mp.nstr(value,digits) for name,value in dict(first_arrival=b,return_arrival=a,p=p,q=q,D=D,scaled_D=D/L**6,predicted_coefficient=pred,null_residual=max(abs(F(0,b)),abs(F(b,a)))).items()})
                    if v==0:
                        row['flat_boost_control_pass']=bool(abs(p-1/mp.cos(L))<mp.mpf('1e-45') and abs(D)<mp.mpf('1e-45'))
                    else:
                        row['relative_coefficient_error']=mp.nstr(abs(D/L**6/pred-1),digits)
                        row['negative_residual']=bool(D<0)
                    records.append(row)
    with mp.workdps(110):
        pairs={(r['speed'],r['L_denominator']):r for r in records if r['digits']==60}
        cross=max(abs(mp.mpf(r['D'])-mp.mpf(pairs[r['speed'],r['L_denominator']]['D'])) for r in records if r['digits']==100)
        gates['unboosted_control']=all(r.get('flat_boost_control_pass',True) for r in records)
        gates['negative_boosted']=all(r.get('negative_residual',True) for r in records)
        gates['finest_coefficient']=all(mp.mpf(r['relative_coefficient_error'])<mp.mpf('.01') for r in records if r['speed']!='0' and r['L_denominator']==160)
        gates['precision_agreement']=bool(cross<mp.mpf('1e-40'))
    return dict(gates=gates,records=records,max_cross_precision_D=str(cross))
def completion():
    eta,x,y,z=sp.symbols('eta x y z',real=True);coords=[eta,x,y,z]
    O=sp.Function('O')(eta);g=sp.diag(-1,1,1,1)/O**2;inv=g.inv();n=4
    G=[[[sp.simplify(sum(inv[a,d]*(sp.diff(g[d,c],coords[b])+sp.diff(g[d,b],coords[c])-sp.diff(g[b,c],coords[d])) for d in range(n))/2) for c in range(n)] for b in range(n)] for a in range(n)]
    Ric=sp.Matrix(n,n,lambda a,b:sp.simplify(sum(sp.diff(G[c][a][b],coords[c])-sp.diff(G[c][a][c],coords[b])+sum(G[c][c][d]*G[d][a][b]-G[c][b][d]*G[d][a][c] for d in range(n)) for c in range(n))))
    R=sp.simplify(sum(inv[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
    k=sp.Matrix([O**2,O**2,0,0]);U=sp.Matrix([O,0,0,0]);checks={}
    def zero(name,val):checks[name]=bool(sp.simplify(val)==0)
    zero('original_scalar',R-(12*sp.diff(O,eta)**2-6*O*sp.diff(O,eta,2)))
    zero('clock_unit',(U.T*g*U)[0]+1);zero('ray_null',(k.T*g*k)[0]);zero('frequency',-(U.T*g*k)[0]-O)
    for label,V in [('affine_null',k),('proper_clock',U)]:
        for a in range(n):zero(label+str(a),sum(V[b]*sp.diff(V[a],coords[b]) for b in range(n))+sum(G[a][b][c]*V[b]*V[c] for b in range(n) for c in range(n)))
    h=sp.symbols('h',positive=True);controls=[]
    for beta in [1,2]:
        val=(1-h*eta)**beta;rr=sp.simplify(R.subs(O,val).doit());HH=-sp.diff(val,eta)
        tau=-sp.log(1-h*eta)/h if beta==1 else ((1-h*eta)**-1-1)/h
        zero('proper_time_beta'+str(beta),sp.diff(tau,eta)-1/val)
        zero('R_beta'+str(beta),rr-6*beta*(beta+1)*h*h*(1-h*eta)**(2*beta-2))
        controls.append(dict(beta=beta,Omega=str(val),p=str(1/val),H=str(HH),R=str(rr),proper_time=str(tau),boundary_derivative=str(sp.diff(val,eta).subs(eta,1/h)),R_limit=str(sp.limit(rr,eta,1/h,dir='-'))))
    bump=sp.exp(16-1/((eta-sp.Rational(1,4))*(sp.Rational(3,4)-eta)))
    eps=sp.Rational(1,100);val=(1-eta)*(1+eps*bump);rr=sp.simplify((12*sp.diff(val,eta)**2-6*val*sp.diff(val,eta,2)).subs(eta,sp.Rational(1,2)))
    checks['interior_curvature_changed']=bool(rr!=12)
    return dict(gates=checks,scalar=str(R),Ricci=[[str(Ric[i,j]) for j in range(n)] for i in range(n)],controls=controls,
        bump=dict(epsilon=str(eps),interior_expression=str(bump),support='(1/4,3/4), zero outside; smooth flat endpoint joins proved analytically',R_midpoint=str(rr),baseline_R='12'),
        limits='Exact symbolic controls support the independent analytic simple-zero/Taylor argument. No finite check proves completion or native admission.')
def main():
    start=time.monotonic();freeze=json.loads((B/'CHECK_FREEZE.json').read_text())
    for f,h in freeze['files'].items():assert hashlib.sha256((B/f).read_bytes()).hexdigest()==h,f
    e=echo();c=completion();gates={**{'echo_'+k:v for k,v in e['gates'].items()},**{'completion_'+k:v for k,v in c['gates'].items()}}
    out=dict(status='PASS' if all(gates.values()) else 'FAIL_REQUIRES_REVIEW',gates=gates,echo=e,completion=c,
        duration_seconds=time.monotonic()-start,python=sys.version,sympy=sp.__version__,mpmath=mp.__version__,platform=platform.platform())
    with (B/'PARENT_CHECK_RESULT.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps(dict(status=out['status'],gates=gates,echo_cases=len(e['records']),duration_seconds=out['duration_seconds'],R_bump_midpoint=c['bump']['R_midpoint'])))
if __name__=='__main__':main()
