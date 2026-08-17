#!/usr/bin/env python3
"""Exact production algebra and immersion countermodel for G144."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.cancel(x) == 0 for x in matrix)


def main() -> None:
    checks: list[str] = []
    eta2 = sp.diag(-1, 1)

    def upper(a, u, d):
        return sp.Matrix([[a, u], [0, d]])

    # A genuine B+(2) overlap: F_beta o psi = F_alpha, J=dpsi.
    T, L, a, d = sp.symbols("T L a d", positive=True)
    r, u = sp.symbols("r u", real=True)
    Rbeta = upper(T, r, L)
    Jba = upper(a, u, d)
    Hbeta = Rbeta.T * eta2 * Rbeta
    Halpha = Jba.T * Hbeta * Jba
    Ralpha = Rbeta * Jba
    require(zero(Halpha - Ralpha.T * eta2 * Ralpha),
            "pullback_metric_factor_transforms_by_overlap_Jacobian", checks)
    Cba = Rbeta * Jba * Ralpha.inv()
    require(zero(Cba - sp.eye(2)), "Bplus_same_event_overlap_total_is_identity", checks)
    require(zero(Cba.T * eta2 * Cba - eta2),
            "overlap_total_is_Lorentz_isometric", checks)

    # Triple-overlap differential cocycle.
    b, e = sp.symbols("b e", positive=True)
    v = sp.symbols("v", real=True)
    Jcb = upper(b, v, e)
    Jca = Jcb * Jba
    require(zero(Jcb * Jba - Jca), "overlap_differentials_compose", checks)
    Rgamma = upper(sp.symbols("Tg", positive=True), sp.symbols("rg", real=True),
                   sp.symbols("Lg", positive=True))
    Ralpha_from_gamma = Rgamma * Jca
    Rbeta_from_gamma = Rgamma * Jcb
    Ccb = Rgamma * Jcb * Rbeta_from_gamma.inv()
    Cba_chain = Rbeta_from_gamma * Jba * Ralpha_from_gamma.inv()
    Cca = Rgamma * Jca * Ralpha_from_gamma.inv()
    require(zero(Ccb * Cba_chain - Cca), "overlap_total_transitions_compose", checks)

    # Exact positive-triangular intersection with O(1,1).
    x, y = sp.symbols("x y", positive=True)
    n = sp.symbols("n", real=True)
    C = upper(x, n, y)
    defect = sp.expand(C.T * eta2 * C - eta2)
    require(defect[0, 0] == 1 - x**2 and defect[0, 1] == -n*x,
            "Bplus_Lorentz_defect_first_equations_exact", checks)
    require(defect[1, 1] == -n**2 + y**2 - 1,
            "Bplus_Lorentz_defect_last_equation_exact", checks)
    require(zero(defect.subs({x: 1, n: 0, y: 1})),
            "positive_solution_identity_satisfies_Lorentz", checks)
    # With x,y positive, defect00=0 gives x=1; defect01=0 then n=0; defect11=0 gives y=1.

    # Same observer boundaries, different regular timelike interiors.
    t, s = sp.symbols("t s", real=True)
    eps = sp.symbols("eps", positive=True)
    eta4 = sp.diag(-1, 1, 1, 1)
    F0 = sp.Matrix([t, s, 0, 0])
    Fb = sp.Matrix([t, s, eps * s * (1 - s), 0])
    DF0 = F0.jacobian([t, s])
    DFb = Fb.jacobian([t, s])
    h0 = sp.simplify(DF0.T * eta4 * DF0)
    hb = sp.simplify(DFb.T * eta4 * DFb)
    require(h0 == sp.diag(-1, 1), "flat_strip_pair_metric_exact", checks)
    require(hb[0, 0] == -1 and hb[0, 1] == 0,
            "bulged_strip_clock_and_shift_exact", checks)
    require(sp.expand(hb[1, 1] - (1 + eps**2 * (1 - 2*s)**2)) == 0,
            "bulged_strip_ruler_metric_exact", checks)
    require(sp.expand(hb.det() + 1 + eps**2 * (1 - 2*s)**2) == 0,
            "bulged_strip_regular_timelike_determinant", checks)
    require(zero((Fb - F0).subs(s, 0)) and zero((Fb - F0).subs(s, 1)),
            "two_strips_share_both_observer_boundaries", checks)
    require(sp.factor((Fb - F0)[2]) == -eps*s*(s - 1),
            "interior_separation_factor_exact", checks)
    require((Fb - F0)[2].subs(s, sp.Rational(1, 2)) == eps / 4,
            "interior_images_distinct_witness", checks)
    require(sp.solve(sp.Eq((Fb - F0)[2], 0), s) == [0, 1],
            "image_intersection_only_on_boundaries_in_strip_coordinate", checks)

    hashes = {}
    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative, _role = line.split("\t")
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"source_hash_{Path(relative).parent.name}", checks)
        hashes[relative] = actual

    result = {
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "checks": checks,
        "landing": {
            "genuine_overlap": "branch-resolved embedded open overlap owns psi=F_beta^-1 o F_alpha and J=dpsi",
            "same_event_total": "C_beta_alpha=R_beta J_beta_alpha R_alpha^-1 is Lorentz isometric; in positive triangular gauge it is I",
            "endpoint_only": "same observer boundaries do not imply open image overlap or differential carry",
            "open": "nonoverlap gluing branch population physical query family history and Xmax",
        },
        "endpoint_countermodel": {
            "F0": "(t,s,0,0)",
            "Fbulge": "(t,s,eps*s*(1-s),0)",
            "h0": str(h0),
            "hbulge": str(hb),
            "intersection_s": ["0", "1"],
        },
        "source_hashes": hashes,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
