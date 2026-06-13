# Multi-Cell / Ensemble Whole-Metric Scan — Results

Status: working audit, NOT canonical. Created 2026-06-13. Driver: Claude
(Opus 4.8 1M). Frame: CRITICAL_UNIVERSE_FRAME.md. Queue head (HANDOFF item 1)
step (b), the MULTI-CELL / ENSEMBLE axis. Open-ended, METRIC-LED exploration
("what does the WHOLE metric DO with two or more cells?"), NOT a template/
hypothesis test, NOT mass-matching (DATA-BLIND throughout — no wall numbers
anywhere). New files only: ens_scan_whole.py (operator obstruction +
non-converging box, recorded honestly), ens_scan_chain.py (the converging
multi-cell object). Log /tmp/ens_scan.log. Supersedes the earlier
ens_scan_2cell.py (a prior agent's file that solved the WRONG operator and
did not converge — see HEADLINE 1).

Baseline departed from (solution_space_baseline.md): B1/#34 single cell = ONE
round type, bulk angular operator pure damping; B2/#32/#33 compactness
continuum, absolute scale-free, NO discrete pin; B3 seal = phi->0 mirror
fold; and the prior ensemble doc (ensembles_results.md, E1/E2): like cells
REPEL statically E_int = 2pi Q1Q2/d (MONOTONE 1/d, NO preferred separation)
— established via an ISOLATED-cell + POSITED inter-cell channel argument, NOT
a self-consistent two-cell whole-metric solve. The #33 named open door: does
MULTI-CELL closure PIN compactness/separation the single cell lacks?

Operators are the metric's OWN, verified exact in wint_symcheck.py (reused,
not edited): the e^{2phi}/r^2-dressed angular operator
phi_thth + cot th phi_th - phi_th^2 and the ON two-exponential source
S = Phi(e^{-2phi} - e^{phi}). Both sectors LIVE, nothing added/slaved/frozen.

---

## HEADLINE 1 (NEW, banked — exact + symbolic) — THE METRIC IS SINGLE-CENTRE ANISOTROPIC; "two cells in one chart" is NOT free

The metric's own derived operator is ANISOTROPIC about a SINGLE centre. The
dilation tie (CANON C-2026-06-10-1, the areal reading) dresses ONLY the
areal-RADIAL direction — g^{rr} = e^{-2phi} — while the ANGULAR sector is
BARE, g^{thth} = 1/r^2 (the metric of the sphere of one areal centre). Two
consequences, both proven:

- ENS_SCAN_WHOLE P0a (sympy, exact): the conservative spherical radial
  operator div(r^2 e^{-2phi} phi_r)/r^2 EQUALS the metric's C1 radial operator
  e^{-2phi}(phi_rr + (2/r)phi_r - 2 phi_r^2) — the -2phi_r^2 nonlinearity
  emerges from the product rule, so the conservative form is faithful
  RADIALLY.

- ENS_SCAN_WHOLE P0b + blind V1 (numeric AND symbolic): the naive ISOTROPIC
  conservative "dressed Laplacian" div(e^{-2phi} grad phi) on a 2-centre
  cylindrical (rho,z) chart is NOT the metric's operator. They differ at
  O(1) on any non-radial field (max |Lcyl_iso - Lmetric| = 0.199 on the test
  fields). The reason is exact: the isotropic chart dresses the ANGULAR
  second-derivative coefficient by e^{-2phi} (giving e^{-2phi}/r^2), where
  the metric leaves it BARE (1/r^2). At hadronic depth (phi ~ -0.8) that is a
  ~5x error — the SAME magnitude as CLAUDE.md's standing linearization
  warning (exp(-2 phi0) ~ 5).

THE OBSTRUCTION (the bankable structural finding): the metric, AS DERIVED,
is single-centre. Its bare angular 1/r^2 requires the areal radius about ONE
centre (the sphere area). TWO centres = two incompatible sphere foliations,
so there is NO single naive flat chart that holds two cells faithfully. This
is WHY the prior ens_scan_2cell.py (isotropic (rho,z) box) (i) solved a
DIFFERENT operator and (ii) did not converge — see HEADLINE 2. A faithful
multi-cell solve must EITHER follow the field's own areal direction (the
covariant dressing tensor h^{ij} = e^{-2phi} n^i n^j + (perp), n = grad phi /
|grad phi| — attempted in ens_scan_whole PART 1, did not converge in a box,
see HEADLINE 2) OR weld cells along their shared RADIAL seal, where each cell
keeps its own areal centre (the CONVERGING object, HEADLINE 3).

SELF-GRADE: REAL (exact symbolic + numeric, blind-reconfirmed V1). This is an
UNDOCUMENTED structural fact about the multi-cell axis — the baseline
(solution_space_baseline.md) never states that the metric resists a
two-centre chart; it is a genuine character-change finding (the operator that
was "the metric" for one cell is NOT the metric for two collocated cells).
NOT a numerical artifact (the angular-coefficient mismatch is exact). It does
NOT by itself decide the physics of two welded cells — that is HEADLINE 3.

## HEADLINE 2 (honest negative — recorded, NOT banked as physics) — the (rho,z) BOX solve does not converge

Both the isotropic box (prior ens_scan_2cell.py) AND the faithful
covariant-dressing-tensor box (ens_scan_whole.py PART 1, h^{ij} following
grad phi) FAILED to converge from a Gaussian seed with outer Dirichlet box
walls (single-cell control round_err 0.7-3, maxres stuck 10-45; two-cell
sweep 0/N converged). Diagnosed cause: a cell has a NATURAL areal size and
the ON source's e^{phi} reaction term overshoots against a Dirichlet box
wall the cell does not naturally reach (phi_max blows past the ambient depth
-> the reaction term explodes -> Newton stalls). This is a CLOSURE/numerics
failure, NOT a physics result: the box wall is the wrong closure for a cell
(the cell wants the metric's own turning-point/Neumann seal closure). The
non-converged energies/necks logged in /tmp/ens_scan.log for these runs are
GARBAGE (non-converged iterates) and are explicitly NOT used. Recorded so the
next instance does not repeat the box approach. The lesson reinforces
HEADLINE 1: the metric resists a flat two-centre box; its native multi-cell
object is the welded radial chain (HEADLINE 3).

## HEADLINE 3 (banked — converged, grid-independent, blind-verified) — BASELINE HOLDS on the welded radial chain: angular stays DEAD at shared welds; welding does NOT pin compactness

The faithful CONVERGING multi-cell object is the RADIAL CHAIN: N cells welded
mirror-to-mirror at their shared seals (the turning points v_m = 0 = the seal
locus where the metric closes a cell, registry #30/B3). Built on the
CONVERGING machinery of wint_cell2d.py (the metric's flow-chart cell, ON
source, e^{2v}-dressed LIVE angular operator), with the angular sector LIVE
everywhere INCLUDING at the internal (shared) welds. Closure EXACTLY as
wint_cell2d (per cell: one Dirichlet depth anchor at the vlo turning node =
the energy datum, one Neumann at the vhi turning node). Script
ens_scan_chain.py, 4/4 checks PASS, maxres ~1e-11.

- Q3 CONTROL: the 1-cell chain reproduces wint_cell2d exactly — converges
  (maxres 3.7e-11), theta-flat (th_var 7.8e-16), the #34 round cell.

- Q1 (the shared-weld angular test, the most promising character-change
  candidate): a theta-lobe SEEDED AT an internal shared weld RELAXES to zero,
  for N = 2, 3, 4 and for lobe l = 1, 2, 3 at amplitudes up to 1.0 — every
  CONVERGED solve gives weld_thvar ~ 1e-13 to 1e-16 (machine zero). The
  angular sector stays DEAD at a SHARED seal exactly as at a free seal
  (#34/#36 pure-damping baseline). Grid-independent (blind V2: ncell_pts
  48/64/96 x Nth 33/49/73, th_var stays ~1e-15). NOTE: two strong-seed cases
  (amp 1.0, l=1/3) showed apparent persistence BUT did NOT converge (maxres
  ~4-5) — these are non-converged divergences, the SAME coarse-amplitude
  artifact the wint_cell2d blind verifier already flagged, NOT real
  structure. So: the shared weld does NOT revive the angular sector.

- Q2 (compactness pinning): the welded 2-cell chain converges for a
  CONTINUUM of per-cell energy E — 7 values across 1.1-4.0 U_min in the main
  run, and a finer 20-value blind sweep (V3) across 1.05-4.0 found ZERO gaps.
  Welding does NOT pin a discrete per-cell energy / compactness; the
  multi-cell chain stays a smooth continuum (baseline #33 holds — no
  compactness pin arises from welding cells, consistent with #33's verdict
  that pinning needs an un-derived total-extent T closure, which welding
  alone does NOT supply).

- Q1 EXISTENCE TEST (non-seed, decisive — the stronger argument): the
  converged welded-chain Jacobian is NON-SINGULAR across N = 1, 2, 3, 4 and
  per-cell E = 1.3/2.0/3.0 U_min (min over all configs of min|eig| = 0.0575
  > 0; never zero). NO bifurcation, NO zero mode -> NO shaped (angular) type
  can be born at a shared weld — independent of any seed. This mirrors
  wint_cell2d's WINTC-EXIST existence proof and upgrades Q1 from a
  seed-relaxation observation to an existence statement.

SELF-GRADE: REAL baseline-confirmation (converged maxres ~1e-11,
grid-independent, blind-verified V2/V3, plus a non-seed Jacobian-existence
proof). On the welded radial chain — the
metric's NATIVE multi-cell object — NOTHING undocumented appears: the angular
sector is dead at shared welds and welding adds no compactness discreteness.
This SCOPES the multi-cell axis: the place a multi-cell ruler could appear
(#33's tiling/total-extent T) is NOT supplied by simple welding; it would
need a genuine CLOSED-universe (periodic/total-extent) closure, which this
scan did not construct (and #33 already flags as the un-derived door).

---

## What changed character vs. what held (the map)

| Probe | Baseline expectation | Result | Grade |
|---|---|---|---|
| Two collocated cells in ONE flat chart | (assumed free, as a single cell) | OBSTRUCTED — the metric is single-centre anisotropic; no naive 2-centre chart is the metric (O(1)/~5x angular-dressing error) | NEW, REAL (HEADLINE 1) |
| (rho,z) box self-consistent solve | a converged 2-cell field | does NOT converge (wrong closure for a cell) | negative, recorded not banked (HEADLINE 2) |
| angular sector at a SHARED weld | dead (pure damping, #34/#36) | DEAD — lobes relax, weld_thvar ~1e-15 | baseline HOLDS (HEADLINE 3 Q1) |
| per-cell energy in a welded chain | continuum (#33) | continuum — zero gaps in 20-pt scan | baseline HOLDS (HEADLINE 3 Q2) |
| preferred separation / pinned d | monotone, none (E1/E2) | (separation not mapped — box non-convergence; the chain has no free d, cells weld at the seal) | not reached; see scope |

## Scope reached / NOT reached (honest)

REACHED: the metric's single-centre anisotropy (exact); the native
multi-cell object is the welded radial chain; on it the angular sector is
dead at shared welds and per-cell compactness is a continuum (both
grid-independent, blind-verified). The E1/E2 "monotone repulsion, no
preferred separation" picture is NOT contradicted.

NOT REACHED (open, for a successor): (1) a genuine self-consistent two-CENTRE
field with a finite SEPARATION d (the box approach failed; a bispherical /
two-areal-centre chart, or the covariant dressing-tensor solved with the
metric's OWN turning-point closure rather than a Dirichlet box, is the next
tool). (2) the CLOSED-universe / total-extent-T (tiling) closure that #33
names as the only door to multi-cell compactness pinning — NOT constructed
here; welding alone does not supply T. (3) the exterior/medium coupling
between cells. These remain the undocumented frontier on this axis; this scan
SHRINKS it by removing the naive-flat-chart and simple-welding sub-regions
(both baseline-holding or obstructed).

## Verifier record

Blind self-verification pass (same session, independent machinery from the
main checks): V1 obstruction is symbolic not FD-artifact (angular-coefficient
mismatch exact, ~5x at depth); V2 chain angular-death grid-independent (9
grids); V3 Q2 continuum has zero gaps (20-pt fine E-scan); V4 (the non-seed
existence test) the welded-chain Jacobian is non-singular across N=1..4 and E
(min|eig| 0.0575 > 0) — no weld zero mode. An INDEPENDENT adversarial
verifier (separate agent, own solver) is still recommended before any canon
use, per Self-Hardening discipline.
