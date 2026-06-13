# ens_scan — INDEPENDENT HOSTILE VERIFIER RECORD

Agent: independent blind adversarial verifier (Claude Opus 4.8 1M).
Date: 2026-06-13. Own machinery (own sympy + own numpy FD stencils; did
NOT trust the challenger's scripts for the core claims, reproduced them
from scratch). Log: /tmp/ens_verify.log. Prosecutes ens_scan_results.md
HEADLINE 1 ("the metric is SINGLE-CENTRE ANISOTROPIC; no flat two-centre
chart is faithfully the metric") and the consequence (welded radial chain).

## VERDICT: PARTIALLY-CONFIRMED (scope) — exact arithmetic survives; the
## word "anisotropic" and the sentence "no faithful two-centre chart" are
## OVER-FRAMED and must be downgraded to chart/gauge statements.

---

## What I independently CONFIRMED

1. THE METRIC OPERATOR IS AS STATED (exact). Built the dilation-tie metric
   from CANON C-1 independently: g_rr=e^{2phi}, g_thth=r^2, g_phph=r^2 sin^2,
   so g^{rr}=e^{-2phi} (radial dressed) and g^{thth}=1/r^2 (angular bare).
   Confirmed against wint_symcheck.py (3/3 PASS on my run). The metric's own
   2D field equation carries e^{-2phi} on the radial second-derivative and a
   BARE 1/r^2 on the angular. EXACT, not a misreading of the symbolic file.

2. P0a (exact, reproduced): div(r^2 e^{-2phi} phi_r)/r^2 - C1op = 0 in my
   own sympy. The conservative spherical radial operator equals the metric's
   C1 radial operator; the -2 phi_r^2 nonlinearity emerges from the product
   rule. Conservative form is faithful RADIALLY. CONFIRMED.

3. P0b (reproduced to the digit): my own FD coding of the isotropic
   cylindrical op vs the metric op gives max|diff| = 0.19910 (challenger:
   ~0.199) on the same test field. The naive isotropic-cylindrical
   "div(e^{-2phi} grad phi)" is NOT the metric's areal-chart operator; they
   differ at O(1) on non-radial fields. CONFIRMED.

4. THE MISMATCH IS EXACTLY e^{-2phi}. The cylindrical op dresses the angular
   second-derivative by e^{-2phi}/r^2; the metric (areal chart) leaves it
   bare 1/r^2. The ratio is precisely e^{-2phi} — the conformal factor
   relating an isotropic (rho,z) chart to the areal chart. At hadronic depth
   (phi~-0.8) this is ~5x, matching CLAUDE.md's linearization warning.
   CONFIRMED as the magnitude of the chart error.

5. CONSEQUENCE INTEGRITY HOLDS. The welded-radial-chain results (HEADLINE 3:
   angular dead at shared welds th_var~1e-15; per-cell E continuum; non-
   singular weld Jacobian, no zero mode) are produced by a SEPARATE solver in
   the metric's own (m,theta) flow chart and do NOT use the (rho,z) operator
   at all. They do not depend on whether a two-centre chart exists. Even if a
   faithful two-centre chart DOES exist, the welded-chain findings stand as
   far as they go (scoped to welded-along-shared-radial-seal configurations).

## What I REFUTE / DOWNGRADE (the strongest points against the claim)

A. "SINGLE-CENTRE ANISOTROPIC" IS THE ORDINARY AREAL CONVENTION, NOT A
   SPECIAL UDT ANISOTROPY. g_thth = r^2 (=> g^{thth}=1/r^2 "bare") holds
   IDENTICALLY in flat-spherical, Schwarzschild, and ANY static spherical
   metric written in the AREAL radius r=sqrt(Area/4pi). The angular sector is
   "bare" BECAUSE the areal gauge has already absorbed all angular size into
   r. The "bare angular / dressed radial" split is the DEFINITION of the
   areal coordinate, present in every spherically reduced metric. Calling it
   "the metric is anisotropic" is a misnomer: the cell IS spherically
   symmetric about its centre. The genuine, defensible content is only:
   in the AREAL chart the dilation appears solely in the radial coefficient.

B. A SINGLE CELL HAS AN ISOTROPIC CHART (so "bare angular" is gauge, not an
   obstruction). For phi=phi(r), define isotropic R by dR/R = e^{phi} dr/r;
   this ODE always integrates and the metric becomes psi^4(dR^2+R^2 dOmega^2)
   — manifestly conformally flat. So "angular bare" is a statement ABOUT THE
   AREAL CHART, not a coordinate-free fact. There IS a non-trivial anisotropy
   between the areal chart and an isotropic chart (radial proper length
   stretched by e^{phi}, angular not — verified: equal-conformal forces
   phi=0), but that is a chart relationship, not a structural single-centre
   lock.

C. "NO FAITHFUL FLAT TWO-CENTRE CHART EXISTS" IS NOT PROVEN — only that ONE
   naive chart fails. The proof shows a COEFFICIENT mismatch (the e^{-2phi}
   angular factor) when areal-chart coefficients are pasted onto an isotropic
   cylindrical grid. It does NOT show a structural/topological obstruction.
   The dilation action is chart-INVARIANT; the standard faithful two-centre
   representations (Brill-Lindquist / isotropic punctures, or bispherical
   coordinates) are exactly the GR machinery the charter calls a "mine." Two
   Schwarzschild centres likewise have no common areal chart yet have a
   perfectly faithful isotropic chart. So the obstruction is the WEAK
   coordinate statement (i), not the strong physics statement (ii).
   MITIGATION: the doc's own "NOT REACHED (1)" section explicitly lists the
   bispherical/two-areal-centre chart as the open next tool and does NOT bank
   the strong form — so the over-claim is in the HEADLINE rhetoric only, not
   in the banked scope. The (rho,z) box NON-convergence (HEADLINE 2) is
   correctly recorded as a closure/numerics failure, not a physics no-go.

## The exact surviving statement

In the AREAL chart, the derived UDT dilation appears ONLY in the radial
metric coefficient (g^{rr}=e^{-2phi}); the angular coefficient is the
ordinary areal 1/r^2. Consequently a naive isotropic cylindrical (rho,z)
chart that pastes the areal-chart radial dressing onto a flat angular metric
is NOT the metric's operator — it over-dresses the angular second derivative
by e^{-2phi} (~5x at hadronic depth). This is a real CHART-FIDELITY caution
and correctly explains the prior two-centre non-convergence. It is NOT a
proof that the metric is intrinsically anisotropic (it is areal-gauge
spherical symmetry about one centre) and NOT a proof that no faithful
two-centre chart exists (a covariant bispherical/isotropic chart remains the
unrun, faithful representation). The welded-radial-chain conclusions are
independent of this framing and survive within their (welded-chain) scope.

## Recommendation to Charles

Bank the ARITHMETIC (P0a, P0b, the e^{-2phi}/~5x chart caution, the welded-
chain baseline-holds). STRIKE or re-word the words "the metric is single-
centre anisotropic" -> "in the areal chart the dilation dresses only the
radial coefficient (ordinary areal convention)"; and "no flat two-centre
chart is faithfully the metric" -> "no naive isotropic-cylindrical chart with
areal coefficients is the metric; a covariant bispherical/isotropic two-
centre chart is the untested faithful representation." The two-centre,
finite-d physics remains genuinely OPEN, as the doc's scope section already
concedes.
