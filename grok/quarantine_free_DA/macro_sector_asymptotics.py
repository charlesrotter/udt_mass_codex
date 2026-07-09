#!/usr/bin/env python3
"""
Macro sector — analytic large-reach diagnostics for native vacuum packages.

Barrier probes (observer chart phi(0)=0):
  proper reach:  ell = int e^{phi} dr
  null reach:    u   = int e^{2 phi} dr   (radial null: c dt = e^{2 phi} dr)

No seed theater. Characterizes known closed-form / asymptotic classes only.
"""
from __future__ import annotations

import json
import sympy as sp

out = {}


def section(name: str, d: dict) -> None:
    out[name] = d
    print(f"\n=== {name} ===")
    for k, v in d.items():
        print(f"  {k}: {v}")


# ---------------------------------------------------------------------------
# P2: W compensated, D=r: phi = -q/r  (observer: set phi_inf so phi(0) issue —
# actually phi = phi_inf - q/r diverges at r=0 if q!=0. Macro reading often
# observer at finite r0 with phi(r0)=0. For large-r: phi -> phi_inf finite.
# ---------------------------------------------------------------------------
r, q, phi_inf, Z, G, Dinf, alpha, C0, C1 = sp.symbols(
    "r q phi_inf Z G D_inf alpha C0 C1", positive=True
)

phi_P2 = phi_inf - q / r
# large r: phi -> phi_inf
ell_P2 = sp.integrate(sp.exp(phi_P2), (r, 1, sp.oo))  # from 1 to oo
# exp(phi_inf - q/r) ~ e^{phi_inf} at large r — integral diverges
section(
    "P2_compensated_D_eq_r_Coulomb",
    {
        "phi": str(phi_P2),
        "phi_infty": "phi_inf (finite)",
        "z_infty": "e^{phi_inf - phi_obs} finite if phi_inf finite",
        "proper_to_infty": "DIVERGES (e^phi -> e^{phi_inf} > 0)",
        "null_to_infty": "DIVERGES",
        "barrier": "FAIL — open infinite reach, finite asymptotic redshift offset only",
        "center_issue": "q!=0 singular at r=0 if chart includes origin — relational ok if observer off singular point",
    },
)

# ---------------------------------------------------------------------------
# P0: W compensated, free D: G = D^2 phi' = const
# D'' = -(Z/4) G^2 / D^3
# Large-r: if D ~ v r with v>0, phi' = G/D^2 ~ 1/r^2, phi -> const
# ---------------------------------------------------------------------------
# Multiply D'' * D' :  D' D'' = -(Z/4) G^2 D' / D^3
# d/dr ( (D')^2 / 2 ) = -(Z/4) G^2 d/dr (-1/(2 D^2)) wait
# Energy: (D')^2 = K + (Z/4) G^2 / D^2   ? 
# d/dr (D'^2) = 2 D' D'' = 2 D' (-(Z/4) G^2 / D^3) = -(Z/2) G^2 D' / D^3
# d/dr ( (Z/4) G^2 / D^2 ) = (Z/4) G^2 (-2) D' / D^3 = -(Z/2) G^2 D' / D^3
# so d/dr ( D'^2 - (Z/4) G^2 / D^2 ) = 0
# D'^2 = E + (Z/(4)) G^2 / D^2  with E const
section(
    "P0_compensated_free_D",
    {
        "first_integral": "D'^2 = E + (Z/4) G^2 / D^2  (E const)",
        "G": "D^2 phi' = const",
        "case_E_gt_0": "D ~ sqrt(E) r at large r => phi'~G/(E r^2) => phi->const; proper DIVERGES; barrier FAIL",
        "case_E_eq_0": "D' = ± (sqrt(Z)/2) |G|/D => D^2 ~ ± sqrt(Z)|G| r + const; still D->oo; phi'~1/r; need check",
        "case_E_eq_0_phi": "phi' = G/D^2 ~ 1/r => phi ~ ln r -> ±oo slowly; proper int e^phi ~ int r^{±1}",
        "case_E_lt_0": "D bounded max; TURN then FALL — finite chart life, not large-r open exterior",
        "barrier_open_exterior": "FAIL for E>0 (generic open); E=0 log borderline — score separately",
        "E_eq_0_detail": "If G>0, D^2 = D0^2 + sqrt(Z) G r (taking +), phi' = G/D^2 > 0, phi increases as (1/2)ln(r) asympt; e^phi ~ r^{1/2}; int e^phi dr DIVERGES; int e^{2phi} dr DIVERGES; z->oo but infinite proper reach — WEAK/OPEN not hard barrier",
    },
)

# E=0: D^2 = a + b r, b = sqrt(Z)*G if G>0 and D'>0
# phi = int G/D^2 dr = int G/(a+b r) dr = (G/b) ln(a+b r) + c
# e^phi ~ (a+br)^{G/b} = (a+br)^{1/sqrt(Z)} if b=sqrt(Z)G
# proper ~ int r^{1/sqrt(Z)} dr diverges at oo

# ---------------------------------------------------------------------------
# P3: W=1, D=r: Z (r^2 phi')' = 4 e^{-2 phi}
# Let w = e^{-phi} > 0. Known related to nonlinear ODE.
# At large r, if phi -> const, RHS const, (r^2 phi')' -> const !=0 => phi' ~ 1/r not ->0 inconsistent
# If phi -> +oo, e^{-2phi}->0, near free Laplace (r^2 phi')'~0
# If phi -> -oo, RHS huge — blowup
# ---------------------------------------------------------------------------
section(
    "P3_uncompensated_D_eq_r",
    {
        "EL": "Z (r^2 phi')' = 4 e^{-2 phi}",
        "no_finite_const_asymp": "phi->const implies (r^2 phi')'-> 4 e^{-2c}/Z >0 => phi'~ (const)/r after integrate once? actually integrate: r^2 phi' = (4/Z) int e^{-2phi} r^2? no int of RHS is int 4e^{-2phi} dr not r^2",
        "note": "Integrate: Z r^2 phi' = 4 int_0^r e^{-2phi(s)} ds + A. For regular origin A=0 often.",
        "if_phi_monotone_down": "phi-> -oo possible; then e^{-2phi}->+oo sources more phi growth of |phi'| — runaway candidate",
        "barrier": "OPEN — needs explicit solution class; historical Branch-P frozen-D often finite-domain / no asymptotic vacuum (scoped)",
        "relational": "frozen D=r prefers polar origin structure — macro use must stay observer-chart only",
    },
)

# ---------------------------------------------------------------------------
# P1: free D, W=1 — from explore soft side: D->Dinf, phi ~ a + b r with b<0
# If phi = a + b r, b<0: e^phi = e^a e^{b r}, int_0^oo e^phi dr = e^a / |b| < oo  PASS proper
# null: int e^{2phi} = int e^{2a} e^{2b r} dr converges if b<0
# z: if observer at 0 phi=0, far phi-> -oo, z = e^{phi_far} -> 0? 
# WAIT: 1+z = e^{phi_src - phi_obs}. If observer at 0 with phi=0 and source far with phi-> -oo,
# then 1+z = e^{phi_far} -> 0 means BLUESHIFT not redshift!
# Sign convention: deeper dilation is LARGER phi in UDT metric g_tt = -e^{-2phi} c^2
# so larger phi => slower clocks at that location when viewed...
# Clock rate factor sqrt(-g_tt)/c = e^{-phi}. Larger phi => slower clocks at source.
# 1+z = e^{phi_source - phi_observer} for static observers (from doc).
# So source at larger phi than observer => redshift.
# Soft side with phi decreasing outward means OUTWARD is smaller phi = faster clocks = blueshift direction.
# That is the OPPOSITE of cosmological redshift looking out!
# Hard side pinches with phi increasing — redshift out, but ends at D=0 not large r.
section(
    "P1_uncompensated_free_D_known_classes",
    {
        "explore_soft_phi_decreasing": "phi ~ -|b| r, D->Dinf: PROPER reach FINITE (int e^phi converges) but OUTWARD is DECREASING phi => blueshift outward, not cosmological redshift. Macro FAIL for 'look out, redder'",
        "explore_hard_phi_increasing": "phi rises, D pinches finite r: redshift outward but end is geometric pinch not large-r asymptote; preferred-bulge smell for cosmos",
        "barrier_proper": "soft class has finite proper distance to chart infinity — geometric 'end' but wrong redshift direction for macro look-out",
        "macro_score": "FAIL as observer looking out to redder edge (sign); hard FAIL as preferred pinch-center story",
    },
)

# ---------------------------------------------------------------------------
# Sign convention check from metric
# ---------------------------------------------------------------------------
section(
    "sign_convention",
    {
        "g_tt": "-e^{-2 phi} c^2",
        "clock_rate_factor": "e^{-phi}  (larger phi => slower local clocks)",
        "redshift_static": "1+z = e^{phi_src - phi_obs}  (source deeper in phi => redshifted)",
        "macro_look_out": "need phi increasing with reach for cosmological-type redshift",
    },
)

# ---------------------------------------------------------------------------
# Relational note
# ---------------------------------------------------------------------------
section(
    "relational",
    {
        "requirement": "macro law must allow any event as observer origin with same structural form",
        "P2_coulomb": "scale-free 1/r about a charge center — singular center; shell theorem / frame-relation needed for multi-observer (banked elsewhere); not a dilation barrier at large r",
        "P1_throat": "special bulge — fails no-preferred-center as ontology",
        "needed": "translationally / relationally democratic asymptotics (harder) — first filter is single-chart large-r barrier + correct redshift direction",
    },
)

# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------
section(
    "SCOREBOARD",
    {
        "P0_free_D_compensated_E_gt_0": "FAIL barrier (phi->const, infinite reach)",
        "P0_E_eq_0": "WEAK — z may ->oo as log but infinite proper/null reach",
        "P0_E_lt_0": "not open large-r exterior (turn/fall)",
        "P2_Coulomb_D_r": "FAIL barrier (phi->const)",
        "P3_frozen_D_W1": "OPEN (no closed large-r vacuum; finite-domain scoped history)",
        "P1_soft_explore": "proper barrier YES but blueshift outward FAIL macro look-out",
        "P1_hard_explore": "redshift+pinch; not large-r; preferred structure FAIL cosmos",
        "headline": "No vacuum packaging on the native skeleton yet PASSES full elegant macro test (redshift-out + dilation barrier + open large-r + no preferred center). Live gaps: P3 asymptotics; whether free-D + matter (derived only) can give phi increasing + convergent reach without inventing terms.",
    },
)

path = "macro_sector_asymptotics_data.json"
with open(path, "w") as f:
    json.dump(out, f, indent=2)
print(f"\nWrote {path}")
