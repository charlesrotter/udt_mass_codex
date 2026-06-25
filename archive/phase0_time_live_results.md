# Phase-0 Results — Time-Live Bare-Metric Solve (Birkhoff bank + non-round escape + feasibility)

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M). MODE = BUILD (first step).
DATA-BLIND (no mass/ratio/wall numbers; sizes in units of R only). Category-A
(derive/confirm; nothing imported; GR methods borrowed for tractability only).
Frame: time_live_bare_solve_DESIGN.md (DECISIONS-LOCKED + RED-TEAM-REVISIONS #1,4)
+ CANON C-2026-06-18-1 (held metric structure: exponential dilation + B=1/A along
grad phi) + C-2026-06-10-2 (finite cell + seal).

Scripts (all NEW, prefix phase0_; nothing committed changed):
- phase0_birkhoff.py            -> (A) Birkhoff bank
- phase0_nonround_escape.py     -> (B) non-round escape (B1 rotation, B2 quadrupole)
- phase0_rotation_sharpen.py    -> (B1) sharpened: does rotation force d_t w=0?
- phase0_kernel_feasibility.py  -> (C) kernel time-axis feasibility

This is a CONFIRM/feasibility step. NO physics frequency is claimed; NO solve of
the full Phase-1 system was run. The box-control gate (DESIGN 5.1) is NOT exercised
here (it lives at Phase 2/3, non-round).

---

## (A) BIRKHOFF BANKED — round + diagonal + vacuum is STATIC BY THEOREM

### Setup
Held UDT round/diagonal metric with TIME-DEPENDENT dilation (vacuum, T_munu=0):

    ds^2 = -e^{-2 phi(t,r)} c^2 dt^2 + e^{+2 phi(t,r)} dr^2 + r^2 dOmega^2.

Einstein tensor computed exactly (sympy 1.13.1, full Christoffel -> Ricci ->
G_munu, no closed form assumed).

### Result (exact, sympy)
The off-diagonal (momentum-constraint) component, LOWERED:

    G_{t r}  =  2 * d_t(phi) / r            <-- exactly the red-team value

    G_{t r} / d_t(phi) = 2/r   (proportional to d_t phi, as predicted)

Mixed form for completeness: G^t_r = -2 e^{2phi} d_t(phi) / (c^2 r) (same
vanishing condition; the lowered form is the one matching "2 d_t phi / r").

VACUUM => G_{t r} = 0 => for r>0, **d_t phi = 0** => the metric is STATIC.

### Cross-check (independent, second route)
Started from generic diagonal g_tt = -A(t,r), g_rr = B(t,r) (no tie). The standard
derivation gives the momentum constraint

    G_{t r}(generic) = d_t(B) / (r B).

Imposing the UDT/Schwarzschild tie A*B = c^2 (i.e. B = c^2/A) turns this into
G_{t r} = -d_t(A)/(r A); substituting the held form A = e^{-2phi}c^2, B = e^{2phi}
reproduces **G_{t r} = 2 d_t phi / r** identically. GATE (i) PASS (two ways).

### UDT tie == Schwarzschild AB=1 (exact)
    g_tt * g_rr = (-e^{-2phi}c^2)(e^{+2phi}) = -c^2     (exact; verified == -c^2)

In A,B language the tie is A*B = c^2, which with c=1 is precisely Schwarzschild's
A*B = 1. The reciprocal lock removes EXACTLY the one radial DOF that Schwarzschild's
AB=1 removes. There is **no extra degree of freedom** in the UDT diagonal class to
dodge Birkhoff. GATE (ii) PASS (exact).

### BIRKHOFF STATEMENT (banked)
> A round (spherically symmetric), diagonal, matter-empty UDT cell holding the
> C-2026-06-18-1 structure (exponential dilation + B=1/A) is STATIC BY THEOREM.
> The vacuum momentum constraint G_{t r} = 2 d_t phi / r forces d_t phi = 0
> pointwise; the result is INDEPENDENT of the cell size and of the seal (it is a
> local constraint, not a boundary effect). UDT's B=1/A tie is identical to
> Schwarzschild's AB=1, so no extra DOF rescues time-dependence. C-2026-06-13-1
> ("the diagonal sector propagates in T") does NOT apply here — that hyperbolicity
> carried the L2+L4 MATTER source; with the matter slot empty it is gone.

### RE-GRADE (recorded)
Any past round+static UDT solve was static **by theorem, not by physics choice**.
"Round" and "static" are the SAME constraint in vacuum: choosing spherical symmetry
in the empty diagonal class already forces the metric to freeze. A static round
result therefore carries no information about whether time-life is possible — that
question lives entirely in the non-round class (B).

---

## (B) THE NON-ROUND ESCAPE — where a vacuum geon can live

Each minimal non-round extension was tested at LEADING (linear) ORDER off a round
background (tagged LEADING-ORDER; this is the existence question, per DESIGN, not
the full solve). The test: does the extension RELAX the Birkhoff obstruction so
genuine d_t != 0 is consistent with vacuum?

### (B1) ROTATION / frame-dragging — off-diagonal axial shift g_{t psi} = eps*w(t,r,theta)
O(eps) vacuum equations (sympy):

    G_{t r}     = 0,   G_{t theta} = 0,   G_{r theta} = 0     (no freezing constraint!)
    G_{t psi}   = (1/2r^2)[ -r^2 w_rr - w_thth + w_th/tan(th) ] = 0   (PURE SPATIAL, no d_t)
    G_{r psi}   = (1/c^2 r)[ w_t - (r/2) w_rt ] = 0
    G_{theta psi} = (1/c^2)[ w_t/tan(th) - (1/2) w_t,theta ] = 0

The two equations carrying d_t (G_rpsi, G_thetapsi) FACTOR (separable w = Tf(t)Wf(r,th)):

    G_{r psi}     = Tf'(t) * [ Wf - (r/2) Wf_r ] / (c^2 r) = 0
    G_{theta psi} = Tf'(t) * [ Wf/tan(th) - (1/2) Wf_theta ] / c^2 = 0

i.e. the structure is **Tf'(t) * L_spatial[Wf] = 0**. This is satisfied by a
TIME-DEPENDENT Tf(t) (Tf' != 0) provided Wf solves the spatial conditions
L_spatial[Wf]=0. d_t w != 0 is therefore CONSISTENT with vacuum — NOT forced to
zero. Contrast (A): G_{t r} = 2 d_t phi/r had NO spatial operator to absorb the
time-dependence, so it forced d_t phi = 0 pointwise. **The off-diagonal shift
supplies the spatial operator that absorbs the time-derivative -> Birkhoff
obstruction RELAXED.** (This is the standard stationary frame-dragging structure:
the shift equations are first-order in time, not a wave; rotation escapes by being
a stationary off-diagonal sector that the round momentum constraint cannot freeze.)

### (B2) QUADRUPOLE l=2 — diagonal warp h(t,r)*P_2(cos theta) on the angular block
Added g_thth -> r^2(1 + eps h P2), g_psps -> r^2 sin^2(th)(1 - eps h P2),
P2 = (3cos^2 th - 1)/2. O(eps) vacuum equations (sympy):

    G_{t r} = 0     (the freezing momentum constraint is gone at this order)

    G_{theta theta}/eps  carries  BOTH  d_r^2 h  AND  **d_t^2 h**  (a WAVE operator):
       ~ r[ -3c^2 r cos^2(th) h_rr + c^2 r h_rr - 6c^2 cos^2(th) h_r + 2c^2 h_r
            + 3 r cos^2(th) h_tt - r h_tt ] / (4c^2)

The presence of d_t^2 h means h(t,r) obeys a **vacuum WAVE equation**: a
gravitational-wave-type degree of freedom. d_t h != 0 is allowed; round/static is
NOT forced. **Birkhoff obstruction RELAXED.**

### WHICH MINIMAL DOF FIRST ESCAPES -> the Phase-1 class
Both escape, by DIFFERENT mechanisms:
- B1 (rotation) escapes as a STATIONARY off-diagonal sector (first-order in t,
  frame-dragging): time-dependence consistent because the shift's own spatial
  operator absorbs it.
- B2 (l>=2 quadrupole) escapes as a genuine PROPAGATING wave DOF (second-order in
  t, d_t^2 h present): a vacuum gravitational-wave mode.

**RECOMMENDED Phase-1 search class: the l>=2 (quadrupole) diagonal deformation
(B2).** Reasons: (i) it carries a genuine d_t^2 (wave) operator, so it is the DOF
that can host a true self-gravitating standing wave / breather (the designed-for
geon), whereas B1's frame-dragging is first-order and is the natural SPINNING
companion, not the primary breather; (ii) it stays within the diagonal class, so it
reuses the existing diagonal-block machinery (einstein_3d_eval) most directly;
(iii) it is exactly the angular-block content the carrier audit flagged as the
native-structure suspect. B1 (rotation / g_{t psi}) is the recommended Phase-2/3
companion (the spinning mode). NB: the round diagonal sector is now demoted to a
static/gauge SANITY CHECK only (per RED-TEAM-REVISION #1); it cannot host a rhythm.

---

## (C) FEASIBILITY — the committed Einstein kernel accepts a live time axis

Inspected whole_metric_3d_core.py and exercised it numerically (phase0_kernel_feasibility.py).

1. **t-slot present (drop-in).** The derivative array is dg[..., k, mu, nu] with k
   running over ALL FOUR coords (T,R,TH,PS); the docstring and code confirm k=0 is
   the t-slot, "d_t g = 0 (stationary) -> dg[...,0,:,:]=0" only because every
   current caller zeroes it. dGamma[..., k, a, b, c] likewise carries a k=t slot.
   Supplying dg[T] != 0 is a literal drop-in: the kernel returned FINITE G with
   nonzero time-row derivatives populated (max|G| finite, isfinite all True).

2. **Static limit recovered.** Schwarzschild fed through the kernel on a full
   spatial grid (d_r AND d_theta Christoffel derivatives via d_dx) returns
   max|G_munu| ~ 5e-4 on a coarse 9x9 grid (FD truncation; falls with resolution).
   GATE: a single-axis test left max|G|~0.14 purely because the d_theta Christoffel
   slot was unfilled — NOT a kernel error; with both spatial slots supplied (as the
   real solver does) G -> 0. The kernel is correct.

3. **omega -> 0 continuity (GATE iv).** With a harmonic live time-row amplitude
   g ~ g0 + A cos(omega t) (so d_t g = -A omega sin(omega t), algebraic in omega),
   the live Einstein tensor returns CONTINUOUSLY to the static G as omega -> 0:

       omega = 1.00 : max|G_live - G_static| = 4.2e-2
       omega = 0.10 :                          4.5e-4
       omega = 0.01 :                          4.5e-6
       omega = 0.00 :                          0.0 (exact)

   Clean O(omega^2) approach; static is the continuous omega->0 limit. GATE (iv) PASS.

4. **The d_t plan confirmed.** d_dx differentiates SPATIAL axes only (ax = axis-3
   indexes the last 3 dims, r/theta/psi); it CANNOT produce a time derivative.
   Therefore the t-slots dg[T], dGamma[T] and all d_t^2 content must be supplied by
   the HARMONIC-BALANCE projection: for g = sum_k [a_k cos(k omega t) + b_k sin(k omega t)],
   each d_t brings an algebraic factor (k omega) on the harmonic amplitudes. Spatial
   derivatives via d_dx; time derivatives algebraic-in-omega from the projection.
   This matches the red-team note exactly. FEASIBILITY: CONFIRMED. (We did NOT build
   the Phase-1 solver — only confirmed the time axis wires in and the static limit
   recovers.)

---

## VALIDATION GATES (pass/fail)

- (i) round-vacuum G_tr = 2 d_t phi/r reproduced two ways .................. PASS
      (direct held metric AND generic-A,B-with-tie cross-check, both exact)
- (ii) UDT tie == Schwarzschild AB=1 (exact) ............................... PASS
      (g_tt g_rr = -c^2 exactly; = AB=1 at c=1; no extra DOF)
- (iii) non-round escape shown >= leading order, specific DOF named ........ PASS
      (B1 rotation g_{t psi}: time-dep consistent, obstruction relaxed;
       B2 l=2 quadrupole h(t,r)P2: vacuum WAVE eqn, d_t^2 h present;
       Phase-1 class = l>=2 quadrupole, rotation = Phase-2/3 companion)
- (iv) omega -> 0 -> static recovered ...................................... PASS
      (continuous O(omega^2); exact at omega=0; Schwarzschild static recovered)
- (v) category-A only, data-blind confirmed ............................... PASS
      (sympy/torch only; no mass/ratio/wall number used; sizes never appear;
       no mechanism imported; GR methods used only for tractability)

---

## PREMISE LEDGER (chose / derived / leading-order)

| Item | tag | note |
|---|---|---|
| Exponential dilation g_tt = -e^{-2phi}c^2 | DERIVED (C-2026-06-18-1, R1) | held structure |
| B = 1/A tie (g_tt g_rr = -c^2) along grad phi | DERIVED (C-2026-06-18-1, R3+P8) | held; P8 caveat noted |
| Vacuum T_munu = 0 (matter slot empty) | CHOSE | the bare-first decision (DESIGN, locked) |
| Round + diagonal class (for A) | CHOSE | exactly the class Birkhoff tests; shown to FORCE static |
| Areal radius (rho = r chart) | CHOSE | a chart (DESIGN 4); chart-independence not tested here |
| B1 axial shift g_{t psi} = eps w (flat round bg) | CHOSE + LEADING-ORDER | existence test; O(eps) only |
| B2 l=2 warp h(t,r)P2 (flat round bg) | CHOSE + LEADING-ORDER | existence test; O(eps) only |
| Separable w = Tf(t)Wf(r,th) (B1 sharpen) | CHOSE | a sufficiency demonstration, not the general solution |
| Harmonic-balance / algebraic-in-omega d_t plan | DERIVED-from-kernel | d_dx is spatial-only -> forced |
| omega as free eigenvalue, static = omega->0 | CHOSE (DESIGN pose (a)) | confirmed continuously contained |

REGIME STAMPS: (A) = exact, all-orders, round+diagonal+vacuum, any r>0, any cell
size, any seal (local result). (B1)+(B2) = LEADING (linear) order off a round
background, single-mode, existence-only (NOT a converged solution, NOT a frequency).
(C) = numeric feasibility on the committed kernel, coarse grid, single point /
small harmonic amplitude; no physics claim.

---

## ATTACK HERE (for a blind verifier)

- **G_tr sign/factor**: recompute G_{t r} for the held metric independently (e.g.
  Mathematica/xAct or a second sympy convention). Confirm the LOWERED component is
  +2 d_t phi/r (the mixed G^t_r differs by g^{tt}; do not conflate them). Confirm
  the generic-(A,B)-with-tie route lands on the SAME expression — if the two routes
  disagree, the bank is wrong.
- **Birkhoff scope honesty**: is the claim genuinely INDEPENDENT of the seal? G_tr=0
  is a pointwise constraint, so yes — but verify no boundary term or regularity
  condition was quietly used. Confirm d_t phi=0 follows for ALL r>0 (the 1/r is
  harmless away from the core; check the r->0 endpoint separately is not needed for
  the freezing conclusion).
- **B1 is it really an escape, or a hidden constraint forcing static?** The factored
  form Tf'(t)*L_spatial[Wf]=0 admits Tf'!=0 ONLY if L_spatial[Wf]=0 has a nontrivial
  solution. ATTACK: does the FULL set {G_tpsi=0 (elliptic on Wf), G_rpsi=0,
  G_thetapsi=0} over-determine Wf so the ONLY solution is Wf=0 (=> trivial, no
  escape)? The separable demonstration shows consistency, not existence of a
  nontrivial mode — confirm a nonzero Wf survives all three spatial conditions
  jointly (this is the genuine open point in B1; B2's wave operator is the cleaner
  escape and is why l>=2 is the recommended Phase-1 class).
- **B2 wave operator reality**: confirm the d_t^2 h coefficient does not vanish
  identically after the full l=2 angular projection (it is theta-weighted here:
  (3cos^2 th - 1) structure). A proper Regge-Wheeler/Zerilli reduction should leave
  a clean radial wave equation; verify the d_t^2 term survives projection onto P2
  and is not a coordinate artifact removable by gauge.
- **Leading-order honesty**: B1/B2 are O(eps) existence checks off a ROUND
  background, NOT solutions. Confirm the report does not overclaim a frequency or a
  converged mode. The box-control gate (DESIGN 5.1) is correctly NOT run here.
- **Kernel feasibility not overclaimed**: the omega->0 test used a TOY harmonic
  amplitude and a coarse grid; confirm it demonstrates only (a) the t-slot accepts
  nonzero d_t g, (b) finite G, (c) continuous static limit — and NOT that Phase-1
  converges. Verify the Schwarzschild residual is FD truncation (falls with grid
  refinement / both spatial slots filled), not a kernel bug.
- **Scale smuggle**: confirm no dimensionful quantity beyond c (set to 1 / carried
  symbolically) entered; sizes appear only as the symbol r; no xi/kappa, no hidden
  length. (Data-blind confirmed.)

## STATUS
Phase-0 COMPLETE. Birkhoff banked (round+diagonal+vacuum static by theorem,
re-grade recorded). Non-round escape shown at leading order: rotation (B1,
stationary off-diagonal) and l>=2 quadrupole (B2, vacuum wave) both relax the
obstruction; **Phase-1 search class = l>=2 quadrupole diagonal deformation**, with
rotation as the Phase-2/3 spinning companion. Kernel feasibility CONFIRMED (live
t-slot drop-in; omega->0 returns static; d_t via harmonic-balance algebraic-in-omega).
Nothing committed changed. Awaiting blind verifier + Charles before Phase-1 build.

---

## BLIND VERIFIER VERDICT — 2026-06-18 (verifier agent abef35d7bb1a9a3a8): STANDS

Independent sympy re-derivation (did not trust author scripts). Both load-bearing calls confirmed.
- (A) BIRKHOFF CONFIRMED: independent Christoffel->Ricci->Einstein gives G_{tr}=2 d_t phi/r (lowered)
  exactly; g_tt g_rr=-c^2 = Schwarzschild AB=1 exactly; vacuum => d_t phi=0 for all r>0 (pointwise
  local constraint, no boundary/regularity term). No round non-static vacuum loophole found.
- (A2) No contradiction with C-2026-06-13-1: the diagonal Ricci DOES carry phi_tt/phi_t^2; in VACUUM
  the momentum constraint G_tr=0 zeros d_t phi FIRST, foreclosing the wave terms (CONSTRAINT-KILLED,
  not term-absent -- a precision note); with matter G_tr=kT_tr!=0 permits d_t phi!=0 and genuine
  propagation. Distinction real.
- (B2-1) l=2 WAVE IS PHYSICAL, NOT GAUGE (the decisive Phase-1 check): G_thth carries d_t^2 h with
  coefficient r^2 P2/2; explicit gauge test shows a pure-gauge diagonal l=2 warp has d_t^2(h_thth)==0,
  so the author's d_t^2 content is gauge-invariant/radiative (consistent with l>=2 = nonzero Zerilli;
  l=0,1 don't radiate). => Phase-1 (l>=2 quadrupole standing wave) CAN host a geon.
- (B1) ROTATION: verifier found the joint profile Wf=r^2 sin^2 theta DOES exist (linearized-Kerr
  frame-drag) and satisfies the elliptic constraint too -- claim was UNDERSTATED, reported
  conservatively. Open point: whether that r^2-growing profile is a bounded breather vs a rotation
  gauge mode. Honest.
- (C) feasibility CONFIRMED (kernel time slot real; d_t via harmonic-balance algebraic-in-omega;
  omega->0->static at O(omega^2)). (T) targeting clean: data-blind, category-A, no smuggle; B1 came
  out stronger and was still reported conservatively (anti-verdict-hunting).

NET BANKED: (1) ROUND + matter-empty UDT cell is STATIC BY THEOREM (Birkhoff) -- "round" and "static"
are the SAME constraint; past round/static solves were static by theorem, not physics choice. (2) The
NON-ROUND class hosts time-life: l=2 quadrupole carries a PHYSICAL gravitational-wave DOF (the Phase-1
standing-wave/geon search class); rotation (g_tpsi) is a second route (Phase-2/3), bounded-vs-gauge open.
(3) The committed Einstein kernel can carry a live time axis (harmonic-balance). Phase-1 is sound to build.
