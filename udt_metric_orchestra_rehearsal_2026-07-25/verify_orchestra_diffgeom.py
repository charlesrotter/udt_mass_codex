#!/usr/bin/env python3
"""Independent SymPy diffgeom controls for selected orchestra Ricci edges."""

import csv
from fractions import Fraction
from pathlib import Path

from sympy import Matrix, Rational, diag, exp, simplify, symbols
from sympy.diffgeom import Manifold, Patch, CoordSystem, TensorProduct, metric_to_Ricci_components

NAMES = ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")
m = Manifold("Mreview", 4)
p = Patch("Preview", m)
cs = CoordSystem("Creview", p, symbols("u0 u1 u2 u3", real=True))
u0, u1, u2, u3 = cs.coord_functions()
forms = cs.base_oneforms()


def ricci_fields(fields):
    phi, sigma, alpha, k, s10, s11, s20, s21 = fields
    r = exp(sigma/2-alpha)
    q = exp(sigma/2+alpha)
    E = Matrix([
        [exp(-phi), 0, 0, 0],
        [0, exp(phi), 0, 0],
        [r*(s10+k*s20), r*(s11+k*s21), r, k*r],
        [q*s20, q*s21, 0, q],
    ])
    g = E.T * diag(-1,1,1,1) * E
    tensor = 0
    for i in range(4):
        for j in range(4):
            tensor += g[i,j] * TensorProduct(forms[i], forms[j])
    raw = metric_to_Ricci_components(tensor)
    return Matrix(4,4,lambda i,j: simplify(raw[i,j].subs({u0:0,u1:0,u2:0,u3:0})))


def ricci(rate):
    return ricci_fields([rate[i] * u0 + rate[8+i] * u1 for i in range(8)])


def unit(index):
    out=[0]*16
    out[index]=1
    return out


def plus(i,j):
    out=[0]*16
    out[i]=out[j]=1
    return out


def hessian(i,j):
    if i == j:
        return 2*ricci(unit(i))
    return ricci(plus(i,j))-ricci(unit(i))-ricci(unit(j))


controls = {
    "phi0_alpha0": ((0,2), diag(0, 0, -2, 2)),
    "phi0_k0": ((0,3), Matrix([[0,0,0,0],[0,0,0,0],[0,0,0,1],[0,0,1,0]])),
    "phi0_S11_0_absent": ((0,5), Matrix.zeros(4)),
    "sigma0_S11_0": ((1,5), Matrix([[0,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,0]])),
    "alpha0_S11_0": ((2,5), Matrix([[0,0,0,0],[0,0,-1,0],[0,-1,0,0],[0,0,0,0]])),
    "k0_S21_0": ((3,7), Matrix([[0,0,0,0],[0,0,Rational(1,2),0],[0,Rational(1,2),0,0],[0,0,0,0]])),
    "S11_0_S10_1": ((5,12), diag(1, -1, 1, 0)),
    "S11_0_S21_0": ((5,7), Matrix([[0,0,0,0],[0,0,0,0],[0,0,0,Rational(-1,2)],[0,0,Rational(-1,2),0]])),
}
for name,((i,j),expected) in controls.items():
    observed = hessian(i,j)
    assert observed == expected, (name, observed, expected)
    print(name)
    print(observed)
print("all_8_load_bearing_rate_controls PASS")


def second(field_index, kind):
    fields = [0]*8
    fields[field_index] = {"d00":u0**2/2, "d01":u0*u1, "d11":u1**2/2}[kind]
    return ricci_fields(fields)


root=Path(__file__).resolve().parent
table=root/"RICCI_SECOND_JET_RESPONSE.tsv"
with table.open(newline="", encoding="utf-8") as handle:
    rows=list(csv.DictReader(handle,delimiter="\t"))
component_names=["R00","R01","R02","R03","R11","R12","R13","R22","R23","R33"]
component_indices=[(0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]
mismatches=[]
for row in rows:
    observed=second(NAMES.index(row["instrument"]),row["second_jet"])
    for name,(i,j) in zip(component_names,component_indices):
        f=Fraction(row[name]); expected=Rational(f.numerator,f.denominator)
        if simplify(observed[i,j]-expected)!=0:
            mismatches.append((row["instrument"],row["second_jet"],name,observed[i,j],expected))
print("all_240_second_jet_entries", "PASS" if not mismatches else mismatches)
assert not mismatches
