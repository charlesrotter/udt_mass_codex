#!/usr/bin/env python3
"""Arm-C independent three-part mass/virial accounting.

Certifies the conditional stress/source identity and bookkeeping implications.
It cannot prove EH, minimal coupling, a finite-cell mass generator, a local
surface theorem, the reported numerical gaps, exact criticality, or a
controlled asymptotic/domain limit.
"""
import sympy as sp

checks=[]
def check(label, condition):
    ok=bool(condition); checks.append(ok); print(("PASS " if ok else "FAIL ")+label)

E2,E4,B,W=sp.symbols("E2 E4 B_boundary W_res", real=True)
M0=2*E4
Ecar=E2+E4
defect=sp.expand(M0-(Ecar+B+W))
check("finite-cell virial implies M0=Ecarrier+B+W", sp.simplify(defect.subs(E4,E2+B+W))==0)
check("exact criticality W=0 still leaves boundary term", sp.simplify((M0-Ecar).subs({E4:E2+B,W:0})-B)==0)
check("separate B=W=0 closure gives M0=Ecarrier", sp.simplify((M0-Ecar).subs(E4,E2+B+W).subs({B:0,W:0}))==0)

# Exact source identity for the chosen minimal 4D L2+L4 completion.
rho2,rho4=sp.symbols("rho2 rho4", real=True)
S2,S4=-rho2,rho4
check("minimal carrier gives rho+S=2rho4", sp.simplify((rho2+rho4)+(S2+S4)-2*rho4)==0)

# A nonzero reported relative virial gap algebraically forbids E2=E4.
gap=sp.Rational(-27,1000)
check("nonzero -2.7 percent gap forbids finite-box E2=E4", gap != 0)

print("FINITE_CELL_DEFECT",defect)
print("REPORTED_GAP_RATIONAL",gap)
print("LIMIT: identities are conditional bookkeeping; surface theorem, numerics, and limits remain open")
print(("PASS" if all(checks) else "FAIL")+f" SUMMARY {sum(checks)}/{len(checks)} checks")

