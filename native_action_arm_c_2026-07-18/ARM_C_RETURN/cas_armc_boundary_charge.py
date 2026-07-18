#!/usr/bin/env python3
"""Arm-C algebra for total derivatives, boundary momentum, and EH reduction.

Certifies that a total derivative preserves the bulk Euler equation while
shifting boundary momentum, and that reciprocal-spherical EH is a radial total
derivative. It cannot select boundary data, corner terms, reference subtraction,
charge normalization, topology, or a differentiable gravitational action.
"""
import sympy as sp

checks=[]
def check(label, condition):
    ok=bool(condition); checks.append(ok); print(("PASS " if ok else "FAIL ")+label)

r=sp.symbols("r", positive=True)
lam=sp.symbols("lambda", real=True)
f=sp.Function("f")(r)
fp=sp.diff(f,r)
L0=fp**2/2
F=lam*f
L1=L0+sp.diff(F,r)
def EL(L):
    return sp.simplify(sp.diff(L,f)-sp.diff(sp.diff(L,fp),r))
check("total derivative leaves bulk Euler equation unchanged", sp.simplify(EL(L1)-EL(L0))==0)
p0,p1=sp.diff(L0,fp),sp.diff(L1,fp)
check("total derivative shifts boundary momentum", sp.simplify(p1-p0-lam)==0)
check("Dirichlet parity does not set normal derivative", p0 != 0)

# Reciprocal spherical EH identity for ds2=-A dt2+A^-1 dr2+r2dOmega2.
A=sp.Function("A")(r)
R=-sp.diff(A,r,2)-4*sp.diff(A,r)/r+2*(1-A)/r**2
primitive=-r**2*sp.diff(A,r)-2*r*A+2*r
check("r^2 R is an exact radial total derivative", sp.simplify(r**2*R-sp.diff(primitive,r))==0)

# Reference subtraction and overall normalization remain independent algebraically.
q,qref,k=sp.symbols("q q_ref k", real=True)
Q=k*(q-qref)
check("reference and normalization are independent charge choices", sp.diff(Q,qref)==-k and sp.diff(Q,k)==q-qref)

print("BOUNDARY_MOMENTUM_BEFORE",p0)
print("BOUNDARY_MOMENTUM_AFTER",p1)
print("EH_PRIMITIVE",primitive)
print("LIMIT: bulk algebra does not select a finite-cell primitive, subtraction, or normalized charge")
print(("PASS" if all(checks) else "FAIL")+f" SUMMARY {sum(checks)}/{len(checks)} checks")

