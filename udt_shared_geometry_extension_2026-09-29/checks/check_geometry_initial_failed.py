"""Exact controls for SGE1. Supplied metrics; no native solution/physics claim."""
import json
from pathlib import Path
import sympy as s

checks = []


def zero(name, value):
    residual = s.simplify(value)
    assert residual == 0, (name, residual)
    checks.append({'name': name, 'residual': str(residual)})


# Differentiate a shifted metric and unit observer through their actual 2-jets.
# Ricci is computed from connection derivatives, not defined by Raychaudhuri.
t,x,y,z = coords = s.symbols('t x y z', real=True)
at = dict.fromkeys(coords, 0)
N=s.exp(t/7+x/5); A=s.exp(t/3); C=s.exp(-t/4); D=s.exp(2*t/5)
B=t/6+y/8
co=s.Matrix([[N,N*B,0,0],[0,A,0,0],[0,0,C,0],[0,0,0,D]])
eta=s.diag(-1,1,1,1); g=co.T*eta*co; U=s.Matrix([1/N,0,0,0])
zero('unit observer as a field',(U.T*g*U)[0]+1)
g0=g.subs(at); inv=g0.inv(); u=U.subs(at)
dg=[g.diff(c).subs(at) for c in coords]
ddg=[[g.diff(c).diff(d).subs(at) for d in coords] for c in coords]
di=[-inv*dg[c]*inv for c in range(4)]
du=[U.diff(c).subs(at) for c in coords]
ddu=[[U.diff(c).diff(d).subs(at) for d in coords] for c in coords]
G=[[[sum(inv[a,d]*(dg[b][d,c]+dg[c][d,b]-dg[d][b,c])/2
             for d in range(4)) for c in range(4)] for b in range(4)] for a in range(4)]
dG=[[[[sum((di[e][a,d]*(dg[b][d,c]+dg[c][d,b]-dg[d][b,c])
             +inv[a,d]*(ddg[e][b][d,c]+ddg[e][c][d,b]-ddg[e][d][b,c]))/2
             for d in range(4)) for c in range(4)] for b in range(4)] for a in range(4)] for e in range(4)]
Ric=s.Matrix(4,4,lambda b,d:sum(dG[a][a][d][b]-dG[d][a][a][b]
              +sum(G[a][a][e]*G[e][d][b]-G[a][d][e]*G[e][a][b] for e in range(4))
              for a in range(4)))
M=s.Matrix(4,4,lambda a,b:du[b][a]+sum(G[a][b][c]*u[c] for c in range(4)))
dM=[s.Matrix(4,4,lambda a,b:ddu[e][b][a]+sum(dG[e][a][b][c]*u[c]+G[a][b][c]*du[e][c] for c in range(4))) for e in range(4)]
theta=s.trace(M); H=theta/3; acc=M*u
dacc=[dM[e]*u+M*du[e] for e in range(4)]
diva=sum(dacc[a][a]+sum(G[a][a][b]*acc[b] for b in range(4)) for a in range(4))
Utheta=sum(u[a]*s.trace(dM[a]) for a in range(4))
# At the evaluation event g=eta and U=e0. Spatial derivative decomposes directly.
spatial=M[1:4,1:4]
sig=(spatial+spatial.T)/2-H*s.eye(3); vort=(spatial-spatial.T)/2
sig2=sum(v*v for v in sig); vort2=sum(v*v for v in vort)
zero('direct Ricci vs complete kinematic identity',Utheta+3*H**2+sig2-vort2+(u.T*Ric*u)[0]-diva)
directions=[s.Matrix(v) for v in [(1,0,0),(-1,0,0),(0,1,0),(0,0,1),
    (s.Rational(3,5),s.Rational(4,5),0),(0,s.Rational(5,13),s.Rational(12,13))]]
for i,n in enumerate(directions):
    k=s.Matrix([1,*n]); cov=g0*M
    original=(k.T*cov*k)[0]
    expected=H+(n.T*sig*n)[0]+(n.T*acc[1:4,0])[0]
    zero('null contraction direction '+str(i),original-expected)
assert sig2!=0 and vort2!=0 and acc!=s.zeros(4,1)
checks.append({'name':'mixed control activates shear twist and acceleration','values':[str(sig2),str(vort2),str(acc)]})

# Auxiliary clock field on exactly the same flat ray, not a native model.
lam=s.symbols('lam',real=True); rapid=lam*(1-lam)
ut=s.Matrix([s.cosh(rapid),s.sinh(rapid),0,0]); k=s.Matrix([1,1,0,0])
frequency=s.expand_trig(-(k.T*eta*ut)[0])
zero('boosted ray frequency',frequency-s.exp(-rapid))
raw=-s.diff(s.exp(-rapid),lam)/s.exp(-rapid)
zero('auxiliary density exact derivative',raw-s.diff(rapid,lam))
zero('auxiliary endpoint cancellation',s.integrate(raw,(lam,0,1)))
assert raw.subs(lam,s.Rational(1,4))!=0
checks.append({'name':'nonzero interior density with unchanged endpoints','value':str(raw.subs(lam,s.Rational(1,4)))})

# Shifted stationary 1+1 comparison embedded in4D. L=1/2, shift coefficient1/4.
# Radial null roots are dt/dx=+/-1/(1+x)-x/4 on a regular coordinate-time patch.
L=s.Rational(1,2); shift=x/4; lapse=1+x
out=s.integrate(1/lapse-shift,(x,0,L)); back=s.integrate(1/lapse+shift,(x,0,L))
nb=1+L; source,relay=s.symbols('source relay',real=True)
fab=nb*(source+out); fba=relay/nb+back; F=fba.subs(relay,fab)
zero('shifted null outgoing root',-lapse**2*((1/lapse-shift)+shift)**2+1)
zero('shifted null return root',-lapse**2*((-1/lapse-shift)+shift)**2+1)
p=s.diff(fab,source); q=s.diff(fba,relay)
zero('stationary immediate return derivative',s.diff(F,source)-1)
zero('stationary outgoing times return product',p*q-1)
assert p>1 and q<1 and s.simplify(F-source)==2*s.log(s.Rational(3,2))
checks.append({'name':'stationary shifted red/blue legs','p':str(p),'q':str(q),'delay':str(s.simplify(F-source))})

# Sensitivity controls reject common wrong rules instead of merely passing zeros.
wrong={'omit_twist':vort2,'wrong_Ricci_sign':2*(u.T*Ric*u)[0],
       'omit_acceleration_divergence':diva,'both_stationary_slopes_same':p*p-1,
       'auxiliary_generator_invariant':raw.subs(lam,s.Rational(1,4))}
for name,residual in wrong.items():
    assert s.simplify(residual)!=0,(name,'vacuous control')
    checks.append({'name':'reject '+name,'nonzero_residual':str(s.simplify(residual))})

result={'status':'PASS','checks':checks,'count':len(checks),'direct_Ric_UU':str((u.T*Ric*u)[0]),
        'scope':'Exact supplied controls. Analytic arguments own quantifiers; no native geometry or empirical claim.'}
outpath=Path(__file__).with_name('geometry_result.json')
assert not outpath.exists(),'preserve prior evidence'
outpath.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
