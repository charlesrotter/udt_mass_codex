# W8 — The Catalog Solve: Results (CONTINUUM; the lead withdrawn)

Date: 2026-06-13. Driver: Claude (Opus 4.8). Frame: CATALOG_FRAME.md.
Declaration: W8 section of w_stiffness_push_declaration.md. Phase A
(assemble) = w8_catalog_problem.md + w8a_formula_confirm.py (15/15).
Phase B (GPU solve) = w8b_backgrounds.py / w8b_scan.py / w8b_qstar.py /
w8b_analyze.py (arm agent abb0c98eb4d04e7ac). Independent main-loop
blind verifier = agent a9b8c55e1c7b4509c (w8b_verifier*.py; own
trust-window coupled re-pose + genuine-fold-BC re-derivation; data-blind
discipline confirmed held). All kappa != 0 / time-dependent physics
HYPOTHESIS-GRADE.

## VERDICT: CONTINUUM (pre-registered outcome ii) — the naive catalog
## form does not discretize at this order; the one discretizing lead
## was a boundary-condition artifact.

The catalog frame's first concrete test — "impose all cell-defining
conditions at once and see if the stable set is discrete" — returns a
CONTINUUM. Stable self-consistent cells fill open 2D (gamma, mult)
patches in both D_cell forks; the Misner-Sharp weld charge
p_F = gamma/2 is forced by the weld data (re-derived exactly,
verifier-confirmed), and the seal charge varies continuously in
(gamma, mult), so the catalog's mass RATIOS are just the chosen
gamma-grid ratios — NOT a metric-selected discrete set. gamma is a free
continuous input; nothing in the solve quantizes it. The wall numbers
are therefore not predicted (a clean DATA-BLIND miss; reproducing them
would require tuning gamma — that is not a prediction).

## The q*/mirror-fold "discretizer" lead: WITHDRAWN as a BC artifact

The arm's one lead — that the q*/mirror-fold closure strongly narrows
the stable band toward discreteness — does NOT survive. The genuine
same-minus fold boundary condition was ALREADY derived in this repo
(w7_a_mirror_bc.py, 7/7): the involution sigma:(a,b)->(-a,-b) imposes a
PARITY DICHOTOMY at the D=0 crease (sigma-even -> Neumann, sigma-odd ->
Dirichlet; crease normal rho = b - f q a), and W7 already established
(B-4) that the crease BC ALONE does not quantize — the OUTER finite-cell
wall does (box-control, registry #1). w8b_qstar.py instead imposed an
arbitrary underived Robin (h=1) at the f->0 SEAL (wrong condition, wrong
location). The verifier showed the genuine Neumann fold BC reproduces
the arm's "narrowing" exactly, while the Dirichlet tower (mislabeled
"q=0 control") is the equally-legitimate WIDE band — so the q*-coupling
introduces NO new discrete selection. Registry #30's f-row w_thth door
gains NO support from W8-B. The mirror fold, correctly posed, labels
parity; it does not discretize.

## Attack A (frozen-f) — the continuum is not a frozen-f collapse
## artifact, but the arm skipped its own self-consistency test

The scan is structurally frozen-f (no f back-reaction; the claimed
w8b_selfconsistent.py DOES NOT EXIST — defect). The verifier ran the
named trust-window COUPLED re-pose on the base cell: at kappa = -1 and
+kappa_c the stable RING branch SURVIVES f back-reaction (f_min stays
1.0, same frequency) — so the continuum verdict is not overturned by a
frozen-f collapse. At kappa = -2 the coupled march is not executable
even on the trust window (unsealing, CFL-exceeded), so deep-kappa
points still carry "f-backreaction excluded." Scoped: single cell,
single cadence; SURVIVES is not yet theorem-grade.

## Defects (verifier-found; carried into the banked record)
1. w8b_selfconsistent.py absent — the scan's self-consistency handler
   does not exist; 100% frozen-f, contradicting the spec (w8 sec v.1).
2. Analyzer over-counted negative-kappa-stable cells: n_neg_stable
   omitted the G1 energy-validity gate; 59 rows fail it (edrift ~1.6e-4
   >> 1e-6). Strict valid count 88-of-107 cells — STILL a continuum,
   but the "58 negative-stable" figure is inflated; recount with the
   gate before any further use.
3. robin1 mis-identified as the fold BC (contradicts the repo's own
   verified W7 derivation).

## Standing: the frame is not refuted, the W8-B FORM is exhausted

Whole-cell discreteness could still live in a correctly-posed
fold/outer-wall quotient or the breather sector, but the
"scan-the-limited-parameters-for-isolated-stable-points" form is done:
dynamics/stability does not discretize the cells at this order (they
form a continuum in the shaping parameter), and the mirror fold only
labels parity. The discreteness gap stands.

## Registry: see NEGATIVES_REGISTRY.md #31.
