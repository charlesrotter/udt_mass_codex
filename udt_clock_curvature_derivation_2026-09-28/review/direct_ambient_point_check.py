#!/usr/bin/env python3
"""Bounded exact-jet replacement for retained memory-limited symbolic run."""
import json
import platform
import sympy as s

t,x,y,z=s.symbols('t x y z',real=True)
coords=(t,x,y,z)
rho=1+t+x*y+z*z
p=(t+2*x+3*y+5*z)/20
g=rho**2*s.diag(-1,1,1,1)
inv=g.inv()
U=s.Matrix([(1+p*p)/(1-p*p),2*p/(1-p*p),0,0])/rho
null=s.Matrix([1,0,1,0])/rho
Gamma=[[[sum(inv[a,e]*(s.diff(g[e,b],coords[c])+s.diff(g[e,c],coords[b])
    -s.diff(g[b,c],coords[e])) for e in range(4))/2 for c in range(4)] for b in range(4)] for a in range(4)]
points=[(s.Rational(1,3),s.Rational(1,5),s.Rational(-1,7),s.Rational(1,11)),
    (s.Rational(-1,4),s.Rational(1,7),s.Rational(1,3),s.Rational(-1,9)),
    (s.Rational(1,2),s.Rational(-1,6),s.Rational(1,8),s.Rational(1,5))]
results=[]
for values in points:
    pt=dict(zip(coords,values))
    ev=lambda f:s.cancel(f.subs(pt))
    V=U.applyfunc(ev); k=null.applyfunc(ev); gp=g.applyfunc(ev)
    du=s.Matrix(4,4,lambda a,b:ev(s.diff(U[a],coords[b])))
    ddu=[[[ev(s.diff(U[a],coords[b],coords[c])) for c in range(4)] for b in range(4)] for a in range(4)]
    G=[[[ev(Gamma[a][b][c]) for c in range(4)] for b in range(4)] for a in range(4)]
    dG=[[[[ev(s.diff(Gamma[a][b][c],coords[d])) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    def R(a,b,c,d):
        return dG[a][d][b][c]-dG[a][c][b][d]+sum(G[a][c][q]*G[q][d][b]-G[a][d][q]*G[q][c][b] for q in range(4))
    M=s.Matrix(4,4,lambda a,b:du[a,b]+sum(G[a][b][q]*V[q] for q in range(4)))
    dM=[[[ddu[a][b][c]+sum(dG[a][b][q][c]*V[q]+G[a][b][q]*du[q,c] for q in range(4)) for c in range(4)] for b in range(4)] for a in range(4)]
    A=M*V
    gradA=s.Matrix(4,4,lambda a,b:sum(dM[a][c][b]*V[c]+M[a,c]*du[c,b] for c in range(4))+sum(G[a][b][q]*A[q] for q in range(4)))
    convM=s.Matrix(4,4,lambda a,b:sum(V[c]*(dM[a][b][c]+sum(G[a][c][q]*M[q,b]-G[q][c][b]*M[a,q] for q in range(4))) for c in range(4)))
    tide=s.Matrix(4,4,lambda a,b:sum(R(a,c,b,d)*V[c]*V[d] for c in range(4) for d in range(4)))
    residual=(convM+M*M-gradA+tide).applyfunc(s.cancel)
    assert residual==s.zeros(4),residual
    assert (V.T*gp*V)[0]==-1
    assert (k.T*gp*k)[0]==0
    assert -(V.T*gp*k)[0]>0
    # Frequency differentiation along the independently supplied geodesic jet.
    Uflat=g*U; covector=Uflat.applyfunc(ev)
    dcov=s.Matrix(4,4,lambda a,b:ev(s.diff(Uflat[b],coords[a])))
    gradcov=s.Matrix(4,4,lambda a,b:dcov[a,b]-sum(G[q][a][b]*covector[q] for q in range(4)))
    kdot=s.Matrix([-sum(G[a][b][c]*k[b]*k[c] for b in range(4) for c in range(4)) for a in range(4)])
    d_omega=-sum(dcov[c,b]*k[c]*k[b] for b in range(4) for c in range(4))-(covector.T*kdot)[0]
    transport=-sum(k[a]*k[b]*gradcov[a,b] for a in range(4) for b in range(4))
    assert s.cancel(d_omega-transport)==0
    wrong_sign=(convM+M*M-gradA-tide).applyfunc(s.cancel)
    missing_quadratic=(convM-gradA+tide).applyfunc(s.cancel)
    assert any(v!=0 for v in wrong_sign)
    assert any(v!=0 for v in missing_quadratic)
    results.append({'point':list(map(str,values)),'zero_ricci_components':16,'frequency_transport':True,
        'wrong_sign_rejected':True,'missing_quadratic_rejected':True,
        'nonzero_tide_components':sum(v!=0 for v in tide)})

tt,ss=s.symbols('tt ss',real=True)
X=s.Matrix([s.sinh(tt),s.cosh(tt)*s.cos(ss),s.cosh(tt)*s.sin(ss),0])
eta=s.diag(-1,1,1,1)
paircoords=(tt,ss)
dot=lambda V,W:s.simplify(s.trigsimp((V.T*eta*W)[0]))
induced=s.Matrix(2,2,lambda i,j:dot(X.diff(paircoords[i]),X.diff(paircoords[j])))
assert induced==s.diag(-1,s.cosh(tt)**2)
assert dot(X,X)==1
II=s.Matrix(2,2,lambda i,j:dot(X,X.diff(paircoords[i]).diff(paircoords[j])))
II00=II[0,0];II11=s.simplify(II[1,1]/s.cosh(tt)**2);II01=s.simplify(II[0,1]/s.cosh(tt))
assert (II00,II11,II01)==(1,-1,0)
assert II00+2*II01+II11==0 and II00-2*II01+II11==0
assert II00*II11-II01**2==-1
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,'rho':str(rho),'boost_parameter':str(p),
    'arithmetic':'exact rational metric/observer jets; exact symbolic immersion',
    'general_proof':'reviewed analytically by Ricci commutation, not supplied by finite point checks',
    'points':results,'immersion_metric':str(induced),'II_frame':[str(II00),str(II11),str(II01)],
    'both_null_II_vanish':True,'nonzero_gauss_correction':'-1','author_code_exposure':False},indent=2))
