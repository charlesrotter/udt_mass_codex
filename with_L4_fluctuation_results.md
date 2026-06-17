# WITH-L4 (stabilized) matter fluctuation operator — OBSERVE Results (F1–F5)

Date: 2026-06-17. Driver: Claude (Opus 4.8, 1M ctx). Mode: OBSERVE (pre-registered,
safeguarded). Branch: session-2026-06-17 (local). NOT canon. NEW file (append-never-edit).

Contract (frozen): `with_L4_fluctuation_PREREG.md` — obeyed exactly, no retuning.
Prior context: `matter_sector_potential_results.md` (the L2-only run + its verifier
a29669db: L2-only box-controlled for positive modes, tachyon = dropped-L4 Derrick
artifact, WITH-L4 case UNTESTED), `check1_wall3_keystone_results.md`,
`lepton_soliton_spectrum_results.md` (#44 breathing tower), `native_stabilizer_results.md`
(native L4 = |omega_H1 current|^2_g), `angular_lagrangian_results.md` (L2 + Jacobi sign).

Scripts (committed this push):
- `VERIF_with_L4_fluctuation_F1.py` — symbolic second variation of L2+L4 (S1).
- `VERIF_with_L4_fluctuation_F2345.py` — REAL L2+L4 hedgehog (S2) + WITH-L4 eigenproblem
  + S4 box-control trap-test (l=0,1,2) + L2-only control.
- `VERIF_with_L4_fluctuation_F3reconcile.py` — l=0 box-vs-#44 reconciliation (two weights).
- `VERIF_with_L4_fluctuation_F45bc.py` — S3 seal-BC sensitivity, S5 Goldstone, deep-phi trap.

Blind adversarial verifier: PENDING (verifier-before-record; attack-here block at end).
NOT committed by this agent.

GOAL FRAME (per contract): emergent quantization — does the WITH-L4 (stabilized) matter
guiding-wave operator give INTRINSIC discrete modes (a native quantum face)? Report what
the math gives, desired or not. NOT a mass hunt; honest scope vs #44 (F5).

---

## HEADLINE VERDICT: NEGATIVE (clean, premise-scoped)

**Including L4 CURES the L2-only tachyon but adds NO intrinsic discrete gap.** With the
native L4 stabilizer in BOTH the background and the fluctuation operator (the exact second
variation, 4th-order, S1–S3 satisfied):

- The L2-only l=0 **Derrick tachyon is GONE**: lowest l=0 omega^2 goes from -4.99 (L2-only)
  to **+0.099 (WITH L4)** — positive, stable. This confirms the prior verifier: the tachyon
  was a dropped-stabilizer (Derrick) artifact, not real structure.
- BUT the S4 box-control trap-test (R = {8, 25, 80, 250} L, factor ~31) shows **every mode
  in every sector (l=0, 1, 2) is BOX-CONTROLLED**: omega^2 ~ 1/R^2, omega^2 → 0 as R → ∞,
  with omega^2·R^2 → a clean constant per sector (l=0: 9.90; l=1: 20.23; l=2: 33.28).
- The phi-angular coupling (the attractive Jacobi V + the U(1) connection + the L4 k^4
  stiffness) produces **NO distinct intrinsic discrete structure** beyond a box-set ladder.
- The radial l=0 tower's SHAPE (ratios) matches #44 and is R-independent (intrinsic shape),
  but its ABSOLUTE lowest frequency is box-controlled (no intrinsic gap) — a sharper-than-#44
  statement, robust to the seal BC (clamp vs natural identical to 3 digits, S3).

So: L4 is the genuine stabilizer (removes the tachyon, gives a positive, sized-soliton
breathing tower), but it does NOT manufacture native spectral discreteness. The matter
guiding wave's only intrinsic discreteness remains TOPOLOGICAL (winding), not spectral —
the same Friedrichs/box-control wall (conjecture A) the metric sector and the L2-only matter
sector hit, now reached a THIRD time WITH the stabilizer included. **Confidence 0.78.**

This CONDITIONS-CHANGE-clears the L2-only run's "WITH-L4 UNTESTED" caveat: the WITH-L4 case
is now tested and is box-controlled (negative), not the missed intrinsic mode the verifier
flagged as the live possibility.

---

## F1 — EXACT L2+L4 SECOND-VARIATION OPERATOR (S1): SUCCEEDS

Derived FROM SCRATCH (`VERIF_with_L4_fluctuation_F1.py`), no keystone import.

**L2 piece (Jacobi / harmonic-map second variation).** For a tangent fluctuation
eta = u e1 + v e2 on the target S^2, the exact O(eta^2) variation of L2 = -(xi/2) g^{mn} dn·dn
is the Jacobi (geodesic-deviation) operator
```
  J eta = - D^m D_m eta  -  K [ |grad n0|^2 eta  -  <eta, grad n0> grad n0 ],   K = Gauss(S^2) = +1,
```
with D_m = d_m + (U(1) tangent-bundle connection w_m) the connection-covariant derivative.
The curvature term enters with a **MINUS (attractive/tachyonic)** sign. **CONFIRMED exactly
by sympy** on a concrete geodesic variation: d^2/ds^2 [(1/2)|d_t n|^2]|_{s=0} = -1 = -K|grad n0|^2
with K=+1 (matches matter_sector_potential E1, two methods). The reduced background potential
(the corpus sphere-reduced invariant, matter_sector_potential:51):
```
  V_curv(r) = - ( e^{-2phi} Theta'^2 + 2 sin^2Theta / r^2 )   (ATTRACTIVE).
```

**L4 piece (the NEW content — the stabilizer, INCLUDED).** L4 = -(kappa/4) g^{mp}g^{nq} S_mn·S_pq,
S_mn = d_m n × d_n n = the native |omega_H1 winding current|^2_g (native_stabilizer:46-69).
Its second variation about the winding hedgehog is a **fourth-order, positive-definite k^4
stiffness**: schematically delta^2 L4 ~ kappa·d_r^2( c4(r) d_r^2 eta ) + (background-weighted
d_r^2 terms), with c4(r) = (2 sin^4Theta + 2 sin^2Theta) ≥ 0 (the Theta'^2-coefficient of the
corpus reduced E4_r, lepton_soliton_spectrum:39). The leading symbol +kappa·c4·k^4 > 0:
**L4 adds positive stiffness and CANNOT create a new tachyon** — it is the stabilizer the
L2-only run dropped.

**Full operator (self-adjoint generalized eigenproblem H u = omega^2 W u, channel l):**
```
  H u = -(1/(e^{phi} r^2)) d_r( e^{-phi} r^2 d_r u )                  [L2 radial kinetic]
        + [ l(l+1)/r^2 + V_curv(r) ] u                                [centrifugal + Jacobi V]
        + kappa (1/(e^{phi} r^2)) d_r^2( c4(r) d_r^2 u )              [L4 k^4 stiffness, +]
  W = e^{2phi}      (g^{tt} weight = the matter guiding-wave / KG charge weight, keystone Q3).
```
VERDICT F1: SUCCEEDS. Exact second variation, L4 included, 4th-order, V + connection + k^4
stiffness all present and derived.

## F2 — REAL L2+L4 STABILIZED HEDGEHOG (S2): SUCCEEDS

Solved the REAL profile from its actual EOM (full Euler–Lagrange of E2_r+E4_r, sympy-derived
Theta'' = num/den; NOT an ansatz; scipy solve_bvp, xi=kappa=1).
- Flat (phi=0): monotone pi→0, max rms residual 1.0e-8, half-twist radius **0.693 L**
  (corpus 0.648 L — agrees within solver/grid tolerance), **E0 = 45.599** (corpus 45.6069).
- Deep-phi (p=1 log cell): twist pushed OUTWARD to 2.13 L, residual 1e-8 (matches
  native_stabilizer:126 "deep-phi pushes twist outward"). Two real backgrounds in hand.
VERDICT F2: SUCCEEDS. Real stabilized hedgehog, matches corpus E0~45.6.

## F3 — RADIAL l=0 EIGENPROBLEM WITH L4 + #44 COMPARISON (S6): box-controlled SHAPE-tower

WITH L4, flat, l=0 lowest eigenvalues (R=8): **omega^2 = [0.099, 0.583, 1.53, 2.97, 4.90, ...]**
— all POSITIVE (stable; L4 cured the Derrick tachyon), O(1)-spaced. The #44 breathing tower
is [0.198, 0.554, 1.039, 1.688, ...]: **same KIND** (positive, O(1), overtone-like). The
factor-~2 absolute difference is the known breathing-weight normalization convention (the #44
verifier already recorded a ~4.2× weight normalization that cancels in ratios).

**TRAP-TEST + #44 reconciliation (the load-bearing reading, `F3reconcile.py`):**

| weight | R | om0^2 | om0^2·R^2 | R1=om1/om0 | R2=om2/om0 |
|---|---|---|---|---|---|
| W=e^{2phi} (matter-wave/KG) | 8→250 | 9.9e-2→1.6e-4 | 6.3→**9.90** (→const) | 2.43→**2.00** | 3.93→**3.00** |
| W=e^{3phi}r^2 (#44 breathing) | 8→250 | 5.7e-3→8.0e-9 | 0.37→0.0005 (→0, falls faster) | 2.28→**2.12** | 3.59→**3.25** |

The reconciliation: under BOTH weights the **absolute lowest omega^2 → 0 as R grows**
(box-controlled, NO intrinsic gap), while the **RATIOS are R-independent** (the tower SHAPE
is intrinsic). #44's "intrinsic" claim was about the ratios/spacing (shape) and was correct
in that sense; this run sharpens it: the tower's absolute frequency scale is set by the box,
not by an intrinsic gap. Under the KG weight the box modes form a clean integer harmonic
ladder (1:2:3), the signature of a box. VERDICT F3: the radial tower is the #44 tower
(consistent), but it is box-controlled in absolute terms — no intrinsic radial gap.

## F4 — ANGULAR (l≥1) WITH V + CONNECTION + L4 STIFFNESS (THE NEW QUESTION): NEGATIVE

S4 box-control trap-test, flat phi=0, WITH L4, clamped 4th-order BCs:

| l | R=8 | R=25 | R=80 | R=250 | omega^2·R^2 | verdict |
|---|---|---|---|---|---|---|
| 0 | 9.902e-2 | 1.259e-2 | 1.497e-3 | 1.584e-4 | 6.3→**9.90** (const) | **BOX-CONTROLLED** |
| 1 | 2.901e-1 | 3.224e-2 | 3.161e-3 | 3.237e-4 | 18.6→**20.23** (const) | **BOX-CONTROLLED** |
| 2 | 5.145e-1 | 5.325e-2 | 5.201e-3 | 5.325e-4 | 32.9→**33.28** (const) | **BOX-CONTROLLED** |

Every angular sector: omega^2 ~ 1/R^2, omega^2·R^2 → a clean per-l box constant, omega^2 → 0
as R → ∞. **The phi-angular coupling (attractive Jacobi V + U(1) connection + L4 stiffness)
adds NO distinct intrinsic discrete structure beyond a box-set centrifugal ladder.** L4
stiffened the operator (the l=1 mode is positive, not the L2-only box at the same constant
20.2 — same value, confirming the centrifugal box dominates the large-R scaling and L4 does
not change it), but did not trap a mode.

**S3 seal-BC sensitivity (load-bearing 4th-order BC):** clamp (u'=0) vs natural (u''=0) seal,
l=1: omega^2·R^2 → 20.23 vs 20.19 — **identical to 3 digits**. The box-control verdict is
ROBUST to the 4th-order seal BC. (Core BC = regular Dirichlet + clamp, the physical regular
branch; the same rung conjecture A turned on.)

**S5 Goldstone separation:** the l=1 sector contains the translational zero mode
(eta_i ~ d_i n0), a flat-space symmetry. On the finite Dirichlet cell it is the LOWEST box
mode, lifted by the walls as ~1/R^2 (omega^2·R^2 → 20.2 const) — i.e. the would-be Goldstone
is exactly the box continuum's lowest rung, NOT an intrinsic bound mode. No candidate "bound
mode" survived as a genuine intrinsic state; none was a true omega^2=0 zero mode at finite R
either (they are box-lifted). Iso-rotation (chi) is the cyclic rotor band E_n = E0 + J^2/2Λ3
(monodromy_depth) — a rigid-rotor tower, separate from these fluctuation modes and not a
spatial bound mode.

**Deep-phi (p=1) angular trap-test:** conditioning-LIMITED, not cleanly readable. The e^{2phi}
weight spans (R/rc)^{2p} ~ 10^{4–5} across the large cells — the SAME float64 conditioning
failure #44 documented for p≥2 (spurious sign flips). The flat-background trap-test
(well-conditioned) is the reliable diagnostic and is unambiguously box-controlled in every
sector; the deep-phi numbers (erratic w^2·R^2 at R=250) are reported as conditioning-limited,
NOT over-read. A high-precision (mpmath) deep-phi rerun is flagged for the verifier; the flat
verdict is not expected to change (deep-phi only reweights, it did not manufacture a hierarchy
in #44 either). VERDICT F4: NEGATIVE — no distinct intrinsic angular structure.

## F5 — EMERGENT-QUANTIZATION READING + HONEST SCOPE: no native spectral quantum face

Are the WITH-L4 fluctuation modes "discrete observables" of the matter guiding wave? **No —
not as intrinsic spectral structure.** Every mode is box-controlled (its frequency vanishes
as the cell grows), so the "discreteness" is the discreteness of a wave in a box (the cell
walls/seal), not a native gap of the operator. The only R-independent content is the tower's
SHAPE (the box's own integer-ladder ratios) — that is the geometry of a finite cavity, not an
emergent quantum observable the metric manufactured.

HONEST SCOPE vs #44: this is fully consistent with #44 (O(1) breathing tower, NOT the lepton
hierarchy) and sharpens it — #44's tower is the box's modes; its intrinsic content is the
ratio-shape, not an absolute frequency gap. No inflation: the matter guiding wave does NOT
carry native discrete spectral observables. The native discreteness in the corpus remains
TOPOLOGICAL (winding charge, the omega_H1 quantization, the one-soliton-per-cell fact from
#44), consistent with the keystone's pilot-wave picture (the wave is a curved-KG mode in the
dilation medium; its quantization, where it exists, is topological/boundary, not spectral-trap).

---

## PREMISE LEDGER (chose / derived)

1. L2+L4 second-variation operator = matter guiding-wave operator — **DERIVED** (F1, exact
   sympy + the Jacobi/harmonic-map identity; L4 4th-order stiffness positive-definite).
2. Curvature term SIGN = attractive (K=+1, S^2 Gauss) — **DERIVED** (F1 sympy, d^2/ds^2 = -1).
3. Stabilized hedgehog Theta(r) = solution of the L2+L4 reduced EOM — **DERIVED** (F2, two
   backgrounds, residual 1e-8, E0=45.60 matches corpus).
4. Reduced invariant |grad n0|^2 = e^{-2phi}Theta'^2 + 2 sin^2Theta/r^2 — **DERIVED-as-reduced**
   (corpus sphere-reduced energy; the S^2-texture vs S^3-Skyrme factor-2 issue, #51, affects the
   well coefficient, NOT the box-control verdict — which holds for any positive multiple).
5. **4th-order BCs (S3, LOAD-BEARING):** core = Dirichlet u=0 + clamp u'=0 (regular branch,
   DERIVED-grade); seal = Dirichlet u=0 + clamp u'=0 (CHOSEN, finite-cell) — **sensitivity
   TESTED**: clamp vs natural seal identical to 3 digits (box-control robust). VARIED R in trap-test.
6. Breathing/matter-wave weight W = e^{2phi} (KG charge weight, keystone Q3) for the trap-test;
   #44 breathing weight e^{3phi}r^2 cross-checked (F3reconcile) — both give box-control. **CHOSE**
   the weight; both readings agree on the verdict.
7. L4 k^4 stiffness coefficient c4(r) from the corpus reduced E4_r — **DERIVED** (the Theta'^2
   coeff 2 sin^4+2 sin^2 ≥ 0). The leading symbol positivity is what cures the tachyon.
8. Angular l = {0,1,2} scanned — **CHOSEN per mode** (low sector); all give the same KIND of
   verdict (box-controlled).
9. Goldstone identification (translation in l=1; the box-lifted lowest mode) — **DERIVED** (S5).
10. NO approximation/linearization as a stated result: the operator is the exact second
    variation; backgrounds are exact EOM solutions (S1–S3 satisfied).

## CONFIDENCE: 0.78

High on the structural verdict: WITH L4 the tachyon is gone (l=0 +0.099, the stabilizer works
self-consistently with the sized soliton), and EVERY mode in EVERY sector is box-controlled
(omega^2·R^2 → clean per-l constants 9.90/20.23/33.28 over a 31× cell; clamp vs natural seal
identical; two weights agree; L2-only control reproduces the prior box 20.2 and tachyon -4.99).
Held below 0.85 by: (i) the deep-phi angular trap is conditioning-limited (float64; flagged for
mpmath verifier — but flat is clean and deep-phi did not manufacture structure in #44); (ii) the
S^2/S^3 well-coefficient issue #51 (affects depth, not the box verdict); (iii) FD discretization
of a 1/r^2-singular 4th-order operator (convergence not mpmath-anchored, but consistent across
N and BC variants). None of these can convert a uniformly 1/R^2 box spectrum into an intrinsic gap.

## SINGLE MOST LOAD-BEARING PREMISE (flagged for the blind verifier)

**The 4th-order BCs (premise 5) + the intrinsic-vs-box diagnosis in the angular sector (F4),
plus the Goldstone separation (S5).** The whole verdict hinges on: (a) the box-control diagnosis
(omega^2 ~ 1/R^2 in every sector) being a genuine large-R wall fact, not a BC/discretization
artifact — tested via clamp-vs-natural seal (identical) and the R-scan, but the verifier should
re-derive the operator and re-run the trap-test independently, and check whether ANY physical
non-Dirichlet core/seal BC, or a higher angular l, or the S^3-Skyrme well coefficient, traps an
R-independent mode; (b) confirming no candidate "bound mode" is a mislabeled box-lifted Goldstone;
(c) the deep-phi conditioning (mpmath rerun) — does deep-phi keep box-control or (unexpectedly)
manufacture an intrinsic gap?

---

## NEGATIVES_REGISTRY ENTRY (proposed, premise-scoped)

NEGATIVE: "The WITH-L4 (Skyrme-stabilized) matter fluctuation operator gives the matter guiding
wave INTRINSIC discrete bound modes (a native spectral quantum face), including in the phi-angular
sectors." REFUTED (this run). PREMISE SET: exact L2+L4 second variation (L4 INCLUDED, 4th-order);
real charge-1 stabilized hedgehog (flat, residual 1e-8, E0=45.60); regular-core + finite-cell
4th-order BCs (clamp/natural seal both tested); matter-wave weight e^{2phi} (and #44 breathing
e^{3phi}r^2 cross-checked); angular l=0,1,2; FD eigensolve. RESULT: tachyon cured (L4 works), but
every mode box-controlled (omega^2 ~ 1/R^2; omega^2·R^2 → 9.90/20.23/33.28). CLOSES the L2-only
run's "WITH-L4 UNTESTED" CONDITIONS-CHANGE flag. CONDITIONS-CHANGE triggers: a physical
non-Dirichlet seal/core BC that traps; a native repulsive angular barrier uncovered elsewhere;
mpmath deep-phi showing an intrinsic gap; or the S^3-Skyrme texture (#51) changing the verdict.

## ATTACK-HERE (for the blind verifier)

1. Re-derive the L2 Jacobi operator + its attractive sign AND the L4 4th-order quadratic operator
   (positive k^4 symbol) independently. Confirm L4 is INCLUDED and cures the l=0 tachyon
   (+0.099 vs L2-only -4.99).
2. Re-run the S4 box-control trap-test (vary R, ≥4 values, factor >10) for l=0,1,2 WITH L4;
   confirm omega^2·R^2 → const (box) in every sector and that NO mode is R-independent.
3. Probe the load-bearing BC (premise 5): try a physical Robin/seal BC and a higher l; does
   anything trap intrinsically? Confirm clamp vs natural seal agree (box robust).
4. S5: confirm the lowest l=1 mode is the box-lifted translational Goldstone, not a bound mode.
5. Deep-phi: rerun the angular trap with mpmath (the float64 deep-phi here is conditioning-limited);
   does deep-phi keep box-control or manufacture a gap?
6. Frame/smuggling: did the matter-wave weight choice (e^{2phi} vs e^{3phi}r^2) change the verdict?
   (It did not — both box.) Did a second scale sneak in? (Only the box R; kappa/xi cancels in ratios.)

---

## BLIND ADVERSARIAL VERIFIER BLOCK

**Date:** 2026-06-17. **Verifier agent:** blind-adversarial-verifier-2 (Opus 4.8, 1M ctx).
**Compute:** sympy 1.14.0, numpy 2.2.6, scipy 1.15.3, mpmath 1.3.0 (CPU). Independent
re-derivation of the Jacobi sign + independent FD reassembly of the L2+L4 operator + a
high-precision (mpmath 50–70 dps, log-grid) deep-phi trap-test (the make-or-break). Scripts
re-implemented from the documented forms, NOT imported from the run's scripts.
**Stance:** NEGATIVE under test; attacked BOTH ways. Most effort on (B), deep-phi, as instructed.

### (A) OPERATOR + TACHYON-CURE — **SURVIVES**

Independent re-derivation reproduces the run EXACTLY.
- Jacobi sign: a DIFFERENT geodesic family on S^2 (meridian background, azimuthal tilt) gives
  d^2/ds^2[(1/2)|d_t n|^2]|_0 = **-1 = -K|grad n0|^2, K=+1 (ATTRACTIVE)**. F1 sign CONFIRMED.
- Stabilized hedgehog (independent EOM solve, residual 1e-8): half-twist r=0.6933 L,
  **E0 = 45.599** vs corpus 45.6069. F2 CONFIRMED.
- L4 stiffness coefficient c4 = 2 sin^4Θ + 2 sin^2Θ ≥ 0 (manifestly positive). CONFIRMED.
- **Tachyon cure (l=0, R=8): L2-only lowest ω² = -4.991 → WITH-L4 +0.09902.** Reproduced to
  4 digits. The L2-only tachyon IS a dropped-stabilizer (Derrick) artifact in the FLAT/shallow
  regime; L4 cures it there. Vindicates the matter_sector verifier (a29669db) Task A. SURVIVES.

### (B) DEEP-PHI ATTACK — **FAILS (the headline does NOT generalize to deep-phi)**

This is the make-or-break, and the run's "ALL sectors box-controlled, V adds NO intrinsic
structure" headline does NOT survive into the deep-phi (p=1) regime it admitted it could not test.
- **float64 is confirmed garbage in deep-phi** (independent reproduction): w^2*R^2 swings
  +109, -39, -1.3e6 (l=0) — the run's "conditioning-limited" admission is real, NOT over-cautious.
- **mpmath (log-grid, change of variables x=ln r) BEATS the e^{phi}-span conditioning.** dps=30
  is still junk (gives -189, -267 at R=25); **dps=50 converges cleanly** and dps=70 confirms:
  l=0, R=25: N=60→-0.5466, N=90→-0.5495, N=120→-0.5522 (dps50) = -0.55221899 (dps70, N=120).
  Converged in BOTH N and precision to ~1%.
- **The deep-phi lowest mode is INTRINSIC, not box-controlled** (l=0, WITH L4, dps=50):
  R=15 → ω² = -0.5633; R=25 → -0.5495; R=40 → -0.5328. **ω² is R-INDEPENDENT in absolute
  value** (drifts ~5% over R=15→40), while ω²·R² GROWS (-127, -343, -852) — i.e. ω² does NOT
  vanish as 1/R². A box mode would have ω²·R² → const. This one does not. **It is an intrinsic,
  depth-controlled mode.** l=1 deep-phi behaves the same: ω² = -0.182/-0.265/-0.305 across
  R=15/25/40 (R-independent in magnitude, ω²·R² growing).
- **L4 does NOT cure the deep-phi tachyon.** L2-only deep-phi l=0 (R=25) = -4.636; WITH-L4 =
  -0.549. L4 lifts it ~8x but NOT to positive. So in the depth-amplified regime (e^{-2phi} ~ 1e6
  per E5), the attractive Jacobi well DOMINATES the positive k^4 stiffness and produces an
  intrinsic UNSTABLE (ω²<0) mode — exactly the "hidden intrinsic mode" the matter_sector
  verifier (a29669db, Task C) flagged as the live possibility WITH L4. The run's flat test is
  structurally blind to it; its claim that the flat result "is not expected to change" in
  deep-phi (F4) is WRONG — deep-phi has qualitatively different (intrinsic, non-box) content.
- **CAUSAL attribution (clean):** toggling the well in deep-phi (l=0, R=25, dps50): well ON →
  ω² = -0.549; well OFF (V_curv→0) → ω² = +0.175. Turning the attractive Jacobi well OFF removes
  the negative intrinsic mode. AND with the well off, deep-phi reverts to clean box-control
  (ω²·R² = 107/109/112 across R=15/25/40, constant). This proves (i) the mpmath/log-grid assembly
  is sound — it reproduces box-control when the well is absent — and (ii) the intrinsic negative
  mode IS the depth-amplified attractive well, not a stencil/conditioning artifact.
- HONEST caveat on what this is: the intrinsic mode is TACHYONIC, so it is NOT a STABLE discrete
  "quantum face" — it does not hand the run a POSITIVE. But it DOES refute the run's specific
  claim that "every mode in every sector is box-controlled" and "phi-angular V adds no intrinsic
  structure." Deep-phi hosts intrinsic structure (it just signals instability, not binding). The
  negative as stated is therefore SHALLOW-SCOPED, not clean.

### (C) BOX-CONTROL (shallow/flat) — **SURVIVES**

Independent FD reassembly reproduces the flat trap-test EXACTLY (factor-31 R-scan):
- l=0: ω²·R² = 6.34 → 7.87 → 9.58 → **9.919** (→ 9.90); ratio R1 → 2.000.
- l=1: ω²·R² = 18.57 → 20.15 → 20.23 → **20.231** (→ 20.23).
- l=2: ω²·R² = 32.93 → 33.28 → 33.28 → **33.284** (→ 33.28).
In the FLAT/shallow background every sector is genuinely box-controlled (ω²→0 as 1/R², clean
per-l constant, integer-like ladder). The shallow box-control reproduces conjecture A. CONFIRMED.

### (D) GOLDSTONE / BC — **SURVIVES**

- Clamp vs natural seal (l=1): ω²·R² → 20.231 vs 20.191 — identical to 3 digits. Box-control
  robust to the load-bearing 4th-order seal BC. CONFIRMED.
- **Goldstone (decisive test):** scaling the well V down by 100x (Vmult 1.0→0.01) leaves the l=1
  ω²·R² at 20.23 → 20.23 (UNCHANGED). The lowest l=1 mode is set by the CENTRIFUGAL BOX, not by
  the well — it is the box-lifted translational Goldstone, NOT a bound state. CONFIRMED.
- Robin seal (β = ±2): still box-controlled (ω²·R² → ~20.2, ω²→0). No physical seal BC traps an
  R-independent mode in the SHALLOW background. CONFIRMED (shallow only — the trapping happens in
  the DEEP background via the well, not via a BC).

### (E) PREMISE AUDIT — corrected honest verdict

The cleanest honest statement is **NOT** the run's "no intrinsic spectral discreteness (clean,
premise-scoped)." It is: **"BOX-CONTROLLED in the FLAT/shallow background (all sectors, robustly
reproduced); the L2-only flat tachyon is a Derrick artifact that L4 cures THERE; but DEEP-PHI
(p=1) HOSTS AN INTRINSIC (R-independent, depth-controlled) mode that L4 does NOT cure
(ω² ≈ -0.55 at l=0, -0.3 at l=1) — so the deep-phi regime is NOT box-controlled, and the
negative is SHALLOW-SCOPED, not clean."** The conjecture-A box-control wall is genuinely hit a
third time only in the SHALLOW regime; in the deep regime the operator escapes box-control into
intrinsic (unstable) structure. The run's F4 prediction "deep-phi only reweights, did not
manufacture structure" is the smuggled assumption that fails: depth-amplification of the
attractive well DOES manufacture an intrinsic mode, precisely as the prior verifier warned.

### VERDICTS / CONFIDENCE

| Task | Verdict |
|------|---------|
| (A) operator + tachyon cure | **SURVIVES** — re-derived exactly; L4 cures the FLAT tachyon (+0.099) |
| (B) deep-phi | **FAILS** — mpmath(50–70 dps) shows an INTRINSIC (R-indep) mode, ω²≈-0.55 (l=0)/-0.3 (l=1), NOT box; L4 does not cure it |
| (C) box-control (shallow) | **SURVIVES** — flat trap-test reproduced exactly (9.90/20.23/33.28) |
| (D) Goldstone / BC | **SURVIVES** — Vmult test confirms box-lifted Goldstone; clamp/natural/Robin all box (shallow) |
| (E) premise audit | corrected: SHALLOW-SCOPED, not clean |

**Overall confidence that the NEGATIVE is correct AS STATED ("clean, premise-scoped"): 0.30.**
**Confidence that the negative is correct AT SHALLOW SCOPE only (flat box-controlled; deep-phi
hosts an intrinsic, depth-controlled, UNSTABLE mode — NOT a clean no-intrinsic-structure result):
0.85.** The half of the headline that is solid: flat/shallow box-control (A,C,D, reproduced
exactly). The half that fails: "ALL angular sectors box-controlled / phi-angular V adds NO
intrinsic structure / flat verdict not expected to change in deep-phi" (B).

**Single biggest weakness:** the deep-phi conditioning the run ADMITTED but then dismissed
("flat verdict not expected to change"). It does change. The depth-amplified attractive Jacobi
well (e^{-2phi} ~ 1e6 at p=1) produces an intrinsic R-independent mode that L4 stiffness does not
overcome — the exact hidden-positive the matter_sector verifier pre-flagged. Using the flat test
as "the reliable diagnostic" for a DEPTH-amplified potential is the methodological error
(it tested the regime where the effect is absent).

**Does the verdict change? YES — re-grade to SHALLOW-SCOPED.** Recommended: (1) downgrade the
headline from "NEGATIVE (clean, premise-scoped)" to "shallow box-controlled; deep-phi hosts an
intrinsic (depth-controlled, currently UNSTABLE) mode — NOT clean"; (2) the NEGATIVES_REGISTRY
entry must NOT claim deep-phi box-control — it must record the mpmath finding of an intrinsic
deep-phi mode as a CONDITIONS-CHANGE / open lead; (3) the L2-only run's "WITH-L4 UNTESTED"
caveat is only PARTIALLY closed: WITH-L4 is now tested and is box-controlled SHALLOW, but
deep-phi WITH-L4 hosts an intrinsic mode — the live question (does the depth-amplified well bind
an intrinsic mode?) is answered YES (intrinsic), with stability the open sub-question. The
S^2-vs-S^3 well-coefficient issue (#51) directly governs the depth/sign of this mode and must be
resolved before reading the intrinsic mode's stability as physical: the mode is intrinsic
robustly; whether it is a stable bound state or an instability depends on the true well
coefficient and is NOT settled here.
