#!/usr/bin/env python3
"""Exact algebra for the actual Gaussian-solution record interface; not a PDE solver."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as S

checks = []
controls = []

def zero(name, value):
    entries = list(value) if isinstance(value, S.MatrixBase) else [value]
    residual = [S.trigsimp(S.simplify(x)) for x in entries]
    assert all(x == 0 for x in residual), (name, residual)
    checks.append(name)

def reject(name, value):
    value = S.trigsimp(S.simplify(value))
    assert value != 0, (name, value)
    controls.append({'name': name, 'nonzero_exact_witness': str(value)})

X, A, B, theta, c = S.symbols('X A B theta c', real=True)
s = -S.Rational(2,3) + c
p, r = A*S.cos(X), B*S.cos(X+theta)
k = (p*p+r*r-s*s)/(2*s)
K = S.Matrix([[k,0,0],[0,s-p,-r],[0,-r,s+p]])
I = S.eye(3)
directions = [S.Matrix(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]]
def evaluate(matrix):
    return [(v.T*matrix*v)[0] for v in directions]
def recover(q):
    return S.Matrix([[q[0],(q[3]-q[0]-q[1])/2,(q[4]-q[0]-q[2])/2],
                     [(q[3]-q[0]-q[1])/2,q[1],(q[5]-q[1]-q[2])/2],
                     [(q[4]-q[0]-q[2])/2,(q[5]-q[1]-q[2])/2,q[2]]])

# A common actual metric development supplies these values and derivatives at T0.
# Existence and consistency on a neighborhood belong to the written CK argument.
q0 = evaluate(I)
qdot = evaluate(-2*K)
qdotX = [S.diff(v,X) for v in qdot]
zero('six original density-squared values reconstruct gamma0',recover(q0)-I)
Krec = -recover(qdot)/2
KXrec = -recover(qdotX)/2
zero('six common time derivatives reconstruct full K',Krec-K)
zero('common spatial derivatives reconstruct full K_X',KXrec-K.diff(X))
zero('Hamiltonian original residual',S.trace(K)**2-S.trace(K*K))
zero('three momentum original residuals',S.Matrix([S.diff(K[0,j],X)-(S.diff(S.trace(K),X) if j==0 else 0) for j in range(3)]))

# Positive supplied gamma guarantees all q>0. No claim that six positive q alone
# guarantee SPD. Compute normalized germs from the pulled-back metric and column map.
q = S.symbols('q', positive=True)
h = S.diag(-1,q)
L = S.diag(1,1/S.sqrt(q))
zero('raw Gaussian pair determinant',h.det()+q)
zero('normalized Gram computed by ruler-column rescaling',L.T*h*L-S.diag(-1,1))
zero('normalized determinant', (L.T*h*L).det()+1)
zero('all initial pair values are Euclidean across family',S.Matrix(q0)-S.Matrix([1,1,1,2,2,2]))

# Spatial orientation XYZ+, K=-gamma_dot/2. Bcurl is explicitly defined here;
# its Weyl/Hodge sign is independently fixed by the construction/review calculation.
def curl(tensorX):
    return S.Matrix(3,3,lambda i,j: sum(S.LeviCivita(i,0,l)*tensorX[l,j] for l in range(3)))
E = S.trace(Krec)*Krec-Krec*Krec
Bcurl = curl(KXrec)
Jcurl = S.trigsimp(S.trace(E*Bcurl))
D = S.trigsimp(p*S.diff(r,X)-r*S.diff(p,X))
zero('relative-phase determinant', D+A*B*S.sin(theta))
zero('curl contraction reconstructed entirely from retained density jets',Jcurl+2*k*D)
zero('curl tensor symmetric', Bcurl-Bcurl.T)
zero('curl tensor traceless',S.trace(Bcurl))
zero('electric tensor traceless under Hamiltonian',S.trace(E))
for label, sub in [('zero A',{A:0}),('zero B',{B:0}),('aligned phase',{theta:0}),('opposite aligned phase',{theta:S.pi})]:
    zero(label+' joint contraction',Jcurl.subs(sub))
zero('opposite quadrature reverses sign at unchanged k',Jcurl.subs(theta,-S.pi/2)+Jcurl.subs(theta,S.pi/2))

# Exact tangent-preserving homogeneous family c=epsilon^2 d, representative of
# an arbitrary analytic O(epsilon^2) c for the leading coefficient argument.
eps,a,b,d = S.symbols('epsilon a b d',real=True)
radial = Jcurl.subs({A:eps*a,B:eps*b,c:eps**2*d})
leading = S.simplify(S.diff(radial,eps,2).subs(eps,0)/2)
zero('same-tangent leading coefficient independent of homogeneous tail',leading-S.Rational(2,3)*a*b*S.sin(theta))
sample={A:S.Rational(1,8),B:S.Rational(1,10),theta:-S.pi/2,X:0,c:0}
reject('joint quadrature diagnostic nonzero',Jcurl.subs(sample))
reject('changing completion changes exact contraction',Jcurl.subs(sample)-Jcurl.subs({**sample,c:S.Rational(1,12)}))

# Meaningful erroneous completions/readouts fail specific claims.
badK=K.copy(); badK[0,0]=-s/2
reject('dropping quadratic axial completion violates Hamiltonian',(S.trace(badK)**2-S.trace(badK*badK)).subs(sample))
axis_only=S.diag(*[K[i,i] for i in range(3)])
reject('axis-only record reconstruction loses transverse offdiagonal', (axis_only-K)[1,2].subs({**sample,X:S.pi/2}))
reject('normalized records cannot replace retained density derivatives',Krec[1,2].subs({**sample,X:S.pi/2}))

# G405's actual clock-coordinate control. s_tape=e^t sigma; inverse Jacobian
# from (t,s_tape) to (t,sigma) gives this metric, unlike pointwise Gram rescaling.
t,z = S.symbols('t z',real=True)
Jac=S.Matrix([[1,0],[-z*S.exp(-t),S.exp(-t)]])
tape=Jac.T*S.diag(-1,S.exp(2*t))*Jac
zero('actual tape-coordinate pullback',tape-S.Matrix([[-1+z*z,-z],[-z,1]]))
zero('actual tape determinant',tape.det()+1)
reject('fixed-tape clock differs from original clock',(-tape[0,0]-1).subs(z,S.Rational(1,2)))
original=S.Matrix([1,z])
zero('original clock retained with transformed tangent',(original.T*tape*original)[0]+1)

result={
 'status':'PASS','kind':'exact symbolic identities and explicit invalid-control witnesses; no PDE integration',
 'python':platform.python_version(),'sympy':S.__version__,
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'checks':checks,'checks_count':len(checks),'rejected_controls':controls,
 'formulas':{'D':str(D),'Jcurl':str(Jcurl),'radial_order2':str(leading)},
 'scope':'Actual local Ric=0 developments are justified analytically in the candidate; record algebra does not itself prove existence.',
 'sign_caution':'Bcurl=epsilon_i^{kl} partial_k K_lj. Weyl Hodge convention is separately checked; no silent sign identification.'
}
print(json.dumps(result,indent=2,sort_keys=True))
