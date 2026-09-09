"""Algebra only: does not numerically/axiomatically certify the gluing theorem."""
import itertools
import json
import platform
import sympy as s

u,a,chi=s.symbols('u a chi', real=True)
c=(1-u*u)/(1+u*u)
sn=2*u/(1+u*u)
k=s.Matrix([a*(-1+2*c),a*(-1-c+s.sqrt(3)*sn),a*(-1-c-s.sqrt(3)*sn)])
k0=s.Matrix([a,-2*a,-2*a])
tau=s.simplify(sum(k))
assert tau == -3*a
assert s.simplify(k.dot(k)-9*a*a)==0
delta=k-k0
kbar=k0+chi*delta
Hbar=s.factor(sum(kbar)**2-kbar.dot(kbar))
assert s.simplify(Hbar-chi*(1-chi)*delta.dot(delta))==0
assert Hbar.subs({a:1,u:s.Rational(1,100),chi:s.Rational(1,2)})>0
# Actual flat momentum for a radial variable cutoff: diagonal K, fixed trace.
x,y,z=s.symbols('x y z', real=True)
rad=x*x+y*y+z*z
f=s.Function('f')
Kbar=s.diag(*(k0+f(rad)*delta))
coords=(x,y,z)
M=s.Matrix([sum(s.diff(Kbar[j,i],coords[j]) for j in range(3))-s.diff(s.trace(Kbar),coords[i]) for i in range(3)])
assert all(s.simplify(M[i]-delta[i]*s.diff(f(rad),coords[i]))==0 for i in range(3))

# Derive representation by actual pullback of vector fields, not a typed table.
fields=[s.Matrix([1,0,0]),s.Matrix([0,1,0]),s.Matrix([0,0,1]),s.Matrix([0,-z,y])]
chars=[]
for signs in itertools.product((-1,1),repeat=3):
    S=s.diag(*signs)
    row=[]
    for Y in fields:
        pulled=S*Y.subs(dict(zip(coords,[signs[i]*coords[i] for i in range(3)])), simultaneous=True)
        character=next(sign for sign in (-1,1) if pulled==sign*Y)
        row.append(character)
    assert row==[signs[0],signs[1],signs[2],signs[1]*signs[2]]
    chars.append(row)
avg=[s.Rational(sum(row[j] for row in chars),8) for j in range(4)]
assert avg==[0,0,0,0]
central=s.diag(-1,-1,-1,1)
assert ((s.eye(4)+central)/2).rank()==1  # rejected central-parity-only shortcut

E=s.Matrix([s.factor(tau*ki-ki*ki) for ki in k])
assert s.simplify(sum(E))==0
for i,j,l in ((0,1,2),(0,2,1),(1,2,0)):
    assert s.simplify(E[i]-E[j]-(k[i]-k[j])*k[l])==0
disc=s.factor(s.prod((E[i]-E[j])**2 for i in range(3) for j in range(i+1,3)))
assert disc.subs(u,0)==0
assert disc.subs({u:s.Rational(1,100),a:1})>0
assert E.subs(u,0)==s.Matrix([-4*a*a,2*a*a,2*a*a])
# Uniform small interval: |u|<.1 gives c>99/101 and |sn|<.2;
# these explicit bounds separate k1>0,k2<0,k3<0,k1-k2,k1-k3;
# k2-k3=2sqrt(3)a sn is nonzero for u!=0 and a>0.
assert -1+2*s.Rational(99,101)>0
assert -1-s.Rational(99,101)+s.sqrt(3)/5<0
assert 3*s.Rational(99,101)-s.sqrt(3)/5>0

# Recompute electric curvature from a general power-law 4-metric at T0.
T,T0=s.symbols('T T0',positive=True)
p=s.symbols('p1 p2 p3',real=True)
for pi,ki in zip(p,k):
    b=(T/T0)**(2*pi)
    # R^0_{i0i}= derivative Gamma^0_ii - Gamma^0_ii Gamma^i_0i.
    R0i0i=-(s.diff(s.diff(b,T)/2,T)-(s.diff(b,T)/2)*(s.diff(b,T)/(2*b)))
    electric=s.simplify((R0i0i/b).subs(T,T0))
    assert s.simplify(electric-pi*(1-pi)/T0**2)==0
    assert s.simplify(electric.subs(pi,-T0*ki).subs(T0,1/(3*a))-(tau*ki-ki*ki))==0
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,'status':'PASS',
 'kind':'symbolic algebra and meaningful shortcut controls, not PDE proof',
 'cutoff_H':str(Hbar),'full_group_characters':chars,'invariant_kernel_dimension':0,
 'central_parity_surviving_dimension':1,'Weyl_discriminant':str(disc),
 'small_interval':'0<abs(u)<1/10, a>0; additional theorem smallness required',
 'omissions':['no gluing PDE numerical solve','no computed existence radius',
 'no independent author context','no long-time evolution','no full365 pass']},indent=2))
