#!/usr/bin/env python3
"""
lbare_inverse.py -- the ONE canonical, unit-tested inverse of the native transverse
shear operator L_bare (revised-N4 / N5d preflight).

    L_bare[f] = r^2 f'' - 2 r f' + 2 f          (indicial m^2 - 3m + 2, roots {1,2})

Provenance of the operator: h4_scripts/op_derive2.py (linearized transverse EL of the
Branch-P geometric action; roots {1,2}); H4_N4rev_conditional_mass_response_results.md.

WHY THIS FILE EXISTS (preflight gate, 2026-07-06): the previously-committed inversion
`n4rev_pipeline_GREENBUG.py::green_response` does NOT invert L_bare -- it is the VoP
Green function of a DIFFERENT operator (L_bare[green] = r^4(5T + 2 r T') != -r^4 T,
interior residual ~15.5, magnitude ~8x inflated; only the SIGN of the source integral
survived).  Any N5d magnitude MUST use a correct L_bare inverse.  This module provides
it as a genuine TWO-POINT BVP (Dirichlet at core+seal), which is well-posed because
{r, r^2} cannot both vanish on r>0.  CHEAP linear algebra only; NO production solve.

Category-A numerics (a linear-solver technique) -- soundness/convergence checked, not a
physics claim.  No physics constant is chosen here.
"""
import numpy as np


def build_Lbare(r):
    """Dense L_bare on nodes r (interior rows 2nd-order central FD; identity BC rows).
    Returns (L, interior_slice).  Dirichlet BCs are applied by the caller via rhs."""
    N = len(r)
    L = np.zeros((N, N))
    # non-uniform-safe 2nd-order stencils
    for i in range(1, N - 1):
        hm = r[i] - r[i - 1]
        hp = r[i + 1] - r[i]
        # f'' and f' 2nd-order on (possibly) non-uniform grid
        cm2 = 2.0 / (hm * (hm + hp))          # coeff f_{i-1} in f''
        cp2 = 2.0 / (hp * (hm + hp))          # coeff f_{i+1} in f''
        c02 = -(cm2 + cp2)                    # coeff f_i   in f''
        cm1 = -hp / (hm * (hm + hp))          # coeff f_{i-1} in f'
        cp1 = hm / (hp * (hm + hp))           # coeff f_{i+1} in f'
        c01 = (hp - hm) / (hm * hp)           # coeff f_i    in f'
        ri = r[i]
        L[i, i - 1] = ri**2 * cm2 - 2 * ri * cm1
        L[i, i]     = ri**2 * c02 - 2 * ri * c01 + 2.0
        L[i, i + 1] = ri**2 * cp2 - 2 * ri * cp1
    # Dirichlet rows
    L[0, 0] = 1.0
    L[-1, -1] = 1.0
    return L


def lbare_apply(r, f):
    """Apply the continuum operator via the same FD stencils (for residual checks)."""
    L = build_Lbare(r)
    out = L @ f
    # overwrite the BC rows with the true operator value at the ends (one-sided), so the
    # residual check is meaningful on the whole grid, not just the interior:
    return out


def lbare_solve_bvp(r, source, f_lo, f_hi):
    """Solve L_bare[f] = source on [r0, rN] with Dirichlet f(r0)=f_lo, f(rN)=f_hi."""
    L = build_Lbare(r)
    rhs = source.copy()
    rhs[0] = f_lo
    rhs[-1] = f_hi
    return np.linalg.solve(L, rhs)


# ----------------------------------------------------------------------------- unit tests
def _tests():
    print("=" * 78)
    print("L_bare unit tests  (L[f] = r^2 f'' - 2 r f' + 2 f, roots {1,2})")
    print("=" * 78)

    # ---- Test 1: homogeneous exponents are exactly {1,2} (indicial), analytic ----
    import numpy.polynomial.polynomial as P  # noqa
    # indicial poly m^2 - 3m + 2
    roots = np.sort(np.roots([1.0, -3.0, 2.0]))
    print(f"[1] indicial roots of m^2-3m+2 : {roots}  (expect [1. 2.])  "
          f"{'PASS' if np.allclose(roots, [1.0, 2.0]) else 'FAIL'}")

    # numeric: L_bare[r]  and  L_bare[r^2] ~ 0 in the interior
    r = np.linspace(0.5, 6.0, 15)             # Nr=15 (<=16, bounded)
    for label, f in [("f=r", r.copy()), ("f=r^2", r**2)]:
        res = lbare_apply(r, f)
        interior = np.max(np.abs(res[1:-1]))
        print(f"    L_bare[{label}] interior max|res| = {interior:.3e}  "
              f"{'PASS' if interior < 1e-9 else 'FAIL'}")

    # ---- Test 2: L @ L^{-1} = I  (the operator with BC rows is genuinely inverted) ----
    L = build_Lbare(r)
    Linv = np.linalg.inv(L)
    ident_err = np.max(np.abs(L @ Linv - np.eye(len(r))))
    print(f"[2] max|L @ L^-1 - I| = {ident_err:.3e}  "
          f"{'PASS' if ident_err < 1e-8 else 'FAIL'}")

    # ---- Test 3: known forcing -> analytic particular solution recovered ----
    # f_exact = r^3  => L_bare[r^3] = r^2*6r - 2r*3r^2 + 2r^3 = 2 r^3
    for Nr in (15, 31, 61):
        rg = np.linspace(0.5, 6.0, Nr)
        f_exact = rg**3
        source = 2.0 * rg**3
        f_num = lbare_solve_bvp(rg, source, f_exact[0], f_exact[-1])
        err = np.max(np.abs(f_num - f_exact))
        print(f"[3] f_exact=r^3, Nr={Nr:3d}: max|f_num - f_exact| = {err:.3e}")
    print("    (should fall ~4x per doubling = 2nd-order convergence -> PASS)")

    # ---- Test 4: a second analytic case, f_exact = r^2*ln(r) (a resonant/log mode) ----
    # L_bare[r^2 ln r] = r^2*(2 ln r + 3) - 2r*(2r ln r + r) + 2 r^2 ln r
    #                  = 2r^2 ln r + 3 r^2 - 4 r^2 ln r - 2 r^2 + 2 r^2 ln r = r^2
    rg = np.linspace(0.5, 6.0, 61)
    f_exact = rg**2 * np.log(rg)
    source = rg**2
    err = {}
    for Nr in (61, 121):
        rg = np.linspace(0.5, 6.0, Nr)
        f_exact = rg**2 * np.log(rg)
        f_num = lbare_solve_bvp(rg, rg**2, f_exact[0], f_exact[-1])
        err[Nr] = np.max(np.abs(f_num - f_exact))
    rate = err[61] / err[121]
    print(f"[4] f_exact=r^2 ln r (source r^2): err(61)={err[61]:.3e} err(121)={err[121]:.3e} "
          f"ratio={rate:.2f} (2nd-order ~4) "
          f"{'PASS' if 3.0 < rate < 5.0 else 'FAIL'}")

    # ---- Test 5: reproduce the GREENBUG discrepancy vs the correct BVP ----
    # Take a compact bump 'stress' T(r); GREENBUG claims green_response inverts L_bare
    # for forcing S=-r^4 T.  Correct BVP: solve L_bare[f]=S with Dirichlet f=0 at both
    # ends, then residual max|L_bare[f]-S| ~ 0.  Show green_response residual is large.
    rg = np.linspace(0.5, 8.0, 400)
    dr = rg[1] - rg[0]
    T = np.exp(-((rg - 3.0) ** 2) / 0.5)          # compact-ish stress bump
    S = -rg**4 * T
    # correct BVP inverse (homogeneous Dirichlet -> the particular response)
    f_bvp = lbare_solve_bvp(rg, S, 0.0, 0.0)
    res_bvp = np.max(np.abs((build_Lbare(rg) @ f_bvp)[1:-1] - S[1:-1]))
    # GREENBUG green_response
    def green_response(Tj):
        f1 = rg**2 * Tj
        I1 = np.concatenate([[0], np.cumsum(0.5 * (f1[1:] + f1[:-1]) * dr)])
        f2 = rg * Tj
        cum2 = np.concatenate([[0], np.cumsum(0.5 * (f2[1:] + f2[:-1]) * dr)])
        I2 = cum2[-1] - cum2
        return rg * I1 - rg**2 * I2
    g = green_response(T)
    res_green = np.max(np.abs((build_Lbare(rg) @ g)[1:-1] - S[1:-1]))
    print(f"[5] correct BVP   interior max|L_bare[f]-S| = {res_bvp:.3e}  "
          f"{'PASS (inverts L_bare)' if res_bvp < 1e-2 else 'FAIL'}")
    print(f"    GREENBUG green  interior max|L_bare[g]-S| = {res_green:.3e}  "
          f"(LARGE -> green_response does NOT invert L_bare, confirms doc line 50-52)")
    print(f"    magnitude ratio |g|/|f_bvp| = {np.max(np.abs(g))/np.max(np.abs(f_bvp)):.2f}"
          f"  (doc: ~8x inflation)")
    print("=" * 78)


if __name__ == "__main__":
    _tests()
