#!/usr/bin/env python3
"""Verify the exact radial p=4 flux and its small-amplitude expansion in the reciprocal spherical representative."""
import sympy as sp

r = sp.symbols("r", positive=True)
eps, a = sp.symbols("eps a", real=True)
f = sp.Function("f")(r)
phi = eps*f
phip = sp.diff(phi, r)
# N sqrt(h)=r^2 sin(theta); X=h^rr phi'^2=e^-2phi phi'^2;
# X h^rr phi'=e^-4phi phi'^3.
flux_no_angle = sp.simplify(a*r**2*sp.exp(-4*phi)*phip**3)
print("Exact angle-stripped boundary flux =")
sp.pprint(flux_no_angle)
series_flux = sp.series(flux_no_angle, eps, 0, 5)
print("Expansion through O(eps^4) =")
sp.pprint(series_flux)
leading = a*r**2*eps**3*sp.diff(f, r)**3
print("Exact minus leading, series through O(eps^5) =")
sp.pprint(sp.series(sp.simplify(flux_no_angle-leading), eps, 0, 6))
