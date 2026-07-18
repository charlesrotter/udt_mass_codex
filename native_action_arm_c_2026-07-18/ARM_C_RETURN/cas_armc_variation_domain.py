#!/usr/bin/env python3
"""Arm-C finite-dimensional model of vary/restrict/multiplier alternatives.

The calculation certifies the chain-rule loss of the normal Euler equation
under a hard reciprocal constraint. It is an algebraic analogue, not a proof
of any continuum action, constraint qualification, gauge fixing, or boundary
legality.
"""
import sympy as sp

checks=[]
def check(label, condition):
    ok=bool(condition); checks.append(ok); print(("PASS " if ok else "FAIL ")+label)

x,y,a,b,c,lam = sp.symbols("x y a b c lambda", real=True)
L = a*x**2/2 + b*y**2/2 + c*x*y
Ex, Ey = sp.diff(L,x), sp.diff(L,y)

# Reciprocal hard constraint C=x+y=0, hence y=-x and tangent (dx,dy)=(1,-1).
Lr = sp.expand(L.subs(y,-x))
Er = sp.diff(Lr,x)
check("restrict-then-vary gives tangent projection Ex-Ey", sp.simplify(Er-(Ex-Ey).subs(y,-x))==0)
normal = sp.simplify((Ex+Ey).subs(y,-x))
check("a separate normal equation remains", normal != 0)

# Multiplier imposes C=0 but gives only equality Ex=Ey after lambda elimination.
ELx = Ex+lam
ELy = Ey+lam
check("multiplier elimination gives Ex-Ey=0", sp.simplify(ELx-ELy-(Ex-Ey))==0)

# Concrete witness: L=x+y vanishes after restriction, yet both full Euler
# components are nonzero. Tangent variation and multiplier stationarity allow it.
Lw=x+y
Ewx,Ewy=sp.diff(Lw,x),sp.diff(Lw,y)
check("tangent-stationary witness is not full-stationary", sp.diff(Lw.subs(y,-x),x)==0 and (Ewx!=0 or Ewy!=0))
check("multiplier can solve witness equations", sp.solve([Ewx+lam,Ewy+lam],[lam], dict=True)==[{lam:-1}])

# Least-squares normal equations are another theory: stationary points of E^2
# need not be zeros without rank assumptions.
z=sp.symbols("z", real=True)
E=sp.Matrix([z**2+1])
normal_eq=sp.diff((E.dot(E))/2,z)
check("normal equation can vanish while original equation does not", normal_eq.subs(z,0)==0 and E[0].subs(z,0)!=0)

print("FULL_EULER", Ex, Ey)
print("TANGENT_EULER", Er)
print("NORMAL_EULER_ON_CONSTRAINT", normal)
print("LIMIT: finite chain-rule model only; continuum/gauge/boundary equivalence is not certified")
print(("PASS" if all(checks) else "FAIL")+f" SUMMARY {sum(checks)}/{len(checks)} checks")

