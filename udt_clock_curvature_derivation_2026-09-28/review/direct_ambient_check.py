#!/usr/bin/env python3
"""Independent direct-stage geometry check; no author code imported/read."""
import json
import platform
import sympy as s

t,x,y,z=s.symbols('t x y z', real=True)
coords=(t,x,y,z)
rho=1+t+x*y+z*z
p=(t+2*x+3*y+5*z)/20
g=rho**2*s.diag(-1,1,1,1)
inv=g.inv()
U=s.Matrix([(1+p*p)/(1-p*p),2*p/(1-p*p),0,0])/rho
null=s.Matrix([1,0,1,0])/rho
cancel=s.cancel
Gamma=[[[cancel(sum(inv[a,e]*(s.diff(g[e,b],coords[c])+s.diff(g[e,c],coords[b])
    -s.diff(g[b,c],coords[e])) for e in range(4))/2) for c in range(4)] for b in range(4)] for a in range(4)]
def R(a,b,c,d):
    return s.diff(Gamma[a][d][b],coords[c])-s.diff(Gamma[a][c][b],coords[d])+sum(
        Gamma[a][c][q]*Gamma[q][d][b]-Gamma[a][d][q]*Gamma[q][c][b] for q in range(4))
M=s.Matrix(4,4,lambda a,b:cancel(s.diff(U[a],coords[b])+sum(Gamma[a][b][q]*U[q] for q in range(4))))
A=(M*U).applyfunc(cancel)
gradA=s.Matrix(4,4,lambda a,b:s.diff(A[a],coords[b])+sum(Gamma[a][b][q]*A[q] for q in range(4)))
convM=s.Matrix(4,4,lambda a,b:sum(U[c]*(s.diff(M[a,b],coords[c])
    +sum(Gamma[a][c][q]*M[q,b]-Gamma[q][c][b]*M[a,q] for q in range(4))) for c in range(4)))
tide=s.Matrix(4,4,lambda a,b:cancel(sum(R(a,c,b,d)*U[c]*U[d] for c in range(4) for d in range(4))))
ricci_identity=(convM+M*M-gradA+tide).applyfunc(cancel)
assert ricci_identity==s.zeros(4),ricci_identity
assert cancel((U.T*g*U)[0]+1)==0
assert cancel((null.T*g*null)[0])==0

# Directional derivative of measured frequency along a geodesic jet,
# including the independently supplied coordinate geodesic acceleration.
Uflat=g*U
gradUflat=s.Matrix(4,4,lambda a,b:s.diff(Uflat[b],coords[a])-sum(Gamma[q][a][b]*Uflat[q] for q in range(4)))
kdot=s.Matrix([-sum(Gamma[a][b][c]*null[b]*null[c] for b in range(4) for c in range(4)) for a in range(4)])
direct_domega=-sum(s.diff(Uflat[b],coords[c])*null[c]*null[b] for b in range(4) for c in range(4))-(Uflat.T*kdot)[0]
transport=-sum(null[a]*null[b]*gradUflat[a,b] for a in range(4) for b in range(4))
assert cancel(direct_domega-transport)==0

point={t:s.Rational(1,3),x:s.Rational(1,5),y:s.Rational(-1,7),z:s.Rational(1,11)}
point_tide=tide.subs(point).applyfunc(cancel)
point_M2=(M*M).subs(point).applyfunc(cancel)
wrong_sign=(convM+M*M-gradA-tide).subs(point).applyfunc(cancel)
missing_quadratic=(convM-gradA+tide).subs(point).applyfunc(cancel)
assert any(v!=0 for v in point_tide), 'Sign control must have nonzero tide'
assert any(v!=0 for v in point_M2), 'Quadratic control must be active'
assert any(v!=0 for v in wrong_sign), 'Wrong sign falsely passed'
assert any(v!=0 for v in missing_quadratic), 'Missing M^2 falsely passed'

# Independent direct immersion computation in flat four-space.
tt,ss=s.symbols('tt ss',real=True)
X=s.Matrix([s.sinh(tt),s.cosh(tt)*s.cos(ss),s.cosh(tt)*s.sin(ss),0])
eta=s.diag(-1,1,1,1)
paircoords=(tt,ss)
dX=[X.diff(v) for v in paircoords]
dot=lambda V,W:s.trigsimp(s.expand_trig((V.T*eta*W)[0]))
induced=s.Matrix(2,2,lambda i,j:s.simplify(dot(dX[i],dX[j])))
assert induced==s.diag(-1,s.cosh(tt)**2),induced
norm=s.simplify(dot(X,X))
assert norm==1
II=s.Matrix(2,2,lambda i,j:s.simplify(dot(X,X.diff(paircoords[i]).diff(paircoords[j]))))
# II's coefficients on the unit normal, then convert to the orthonormal frame.
II00=II[0,0]
II11=s.simplify(II[1,1]/s.cosh(tt)**2)
II01=s.simplify(II[0,1]/s.cosh(tt))
assert (II00,II11,II01)==(1,-1,0)
assert II00+2*II01+II11==0 and II00-2*II01+II11==0
gauss_correction=II00*II11-II01**2
assert gauss_correction==-1

print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
    'construction':'conformal flat ambient metric rho^2 eta with spacetime-dependent rationally normalized boosted observer',
    'rho':str(rho),'boost_parameter':str(p),'method':'direct coordinate Christoffel/Riemann and tensor covariant differentiation',
    'arithmetic':'exact symbolic identities, independent author-code-free implementation',
    'ricci_identity_components':16,'all_ricci_residuals':'0 identically',
    'observer_unit_norm':True,'null_initial_direction':True,'frequency_transport_residual':'0 identically',
    'actual_rejections':{'wrong_curvature_sign':True,'missing_M_squared':True},
    'rejection_point':{str(k):str(v) for k,v in point.items()},
    'immersion_metric':str(induced),'II_frame':[str(II00),str(II11),str(II01)],
    'both_null_II_vanish':True,'nonzero_gauss_correction':str(gauss_correction)},indent=2))
