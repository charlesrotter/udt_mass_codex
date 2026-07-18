#!/usr/bin/env python3
"""Verify controlled Taylor expansions of the reciprocal metric factors and their remainders' first omitted order."""
import sympy as sp

eps, f = sp.symbols("eps f", real=True)
minus = sp.exp(-2*eps*f)
plus = sp.exp(2*eps*f)
print("e^(-2 eps f) through eps^2 =", sp.series(minus, eps, 0, 3))
print("e^(+2 eps f) through eps^2 =", sp.series(plus, eps, 0, 3))
prod_truncated = sp.expand((1-2*eps*f+2*eps**2*f**2)*(1+2*eps*f+2*eps**2*f**2))
print("Product of O(eps^2) truncations through eps^4 =", prod_truncated)
print("Product through retained O(eps^2) =", sp.series(prod_truncated, eps, 0, 3))
