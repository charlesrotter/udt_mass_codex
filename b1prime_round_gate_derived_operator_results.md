> **SUPERSEDED / CONDITIONS-CHANGED (2026-07-06 supersession sweep) — NOT a native-micro UDT result; mine for history.**
> Rode the PRE-NATIVE scalar-tensor (f=e^{2φ}, X=−2e5) operator, superseded 2026-07-01 by the native constrained-two-player operator
> (EH-empty, φ-blind matter, geometric 𝒦). Already premise-tagged in NEGATIVES_REGISTRY object-identity (2026-06-21) + 2026-07-04 re-grade.
> Gate-A native-carrier survivor legs re-graded clean; box-control targets CONDITIONS-CHANGED; object imported-S³.

# B1' — Round-Limit Gate on the Derived Operator (RADIAL reconstruction + blind verification)

**Mode:** OBSERVE / INFRASTRUCTURE, METRIC-LED, DATA-BLIND. No mass/ratio/spectrum/catalog
value loaded or targeted. **Driver:** Claude Opus 4.8 (1M), agent for udt_mass_codex.
**Date:** 2026-06-21. **Status: BANKED — blind-verifier SUPPORTED-WITH-REVISIONS** (revisions
folded in below; verifier agent id in §7).

**What this is (scope — read first, do NOT overclaim):** this is the **round-limit GATE** for the
B1' off-round build. It RECONSTRUCTS the derived two-player operator into a well-posed **RADIAL**
(1-D, four-field A,B,phi,Theta) solver, with **phi added as an independent player** (not slaved),
and proves the reconstruction recovers the trusted ROUND results we already banked. **It is NOT the
3-D off-round residual** — that genuine build (phi wired into the full3d a,b,c,d off-round machinery,
where the phi-angular obstruction lives) is the NEXT push, gated. The small-warp continuity here is a
LINEARIZED l=2 proxy, not a 3-D solve. This doc banks the gate; it does not enter the off-round sector.

**Why this push happened (Charles, 2026-06-21):** Phase-B "clean the gate first." A first reconstruction
pass had a smuggled value (a kap8=0.05 factor) and two soft spots; Charles directed cleaning the round
gate to a trustworthy state BEFORE the 3-D build. The cleanup turned up a genuine correction to a banked
result (the scalar hair). All of it is blind-verified here.

**Scripts (new, /tmp, nothing committed):** `b1prime_round.py` (spectral radial solver, symbolic-
continuum EL — authoritative), `b1prime_gateA2_fix.py` / `b1prime_gateB_fix.py` (kap8-fixed gate
drivers), `t2_authoritative.py` (box cell-scan), plus the verifier's independent `/tmp/verif_*.py`.
The derived-operator radial scripts the doc-of-record `static_soliton_rerun_derived_operator_results.md`
referenced (`soliton_*.py`) were never committed; reconstructed here from that doc.

---

## 0. THE OPERATOR (verbatim — derived upstream, USED not re-derived)

```
S = INT sqrt(-g) [ e^{2phi} R  +  X e^{2phi} g^{ab} d_a phi d_b phi  +  e^{2phi} L_m ] dV,   f = e^{2phi}
E_munu = f G_munu + (g_munu box - nabla_mu nabla_nu) f - X f (d_mu phi d_nu phi - 1/2 g_munu (dphi)^2) - f T^m_munu
```
phi an INDEPENDENT field (two-player; B=1/A FREE, not slaved). L_m = native S^2 L2+L4, charge-1
hedgehog Theta(core)=pi, Theta(seal)=0. Production X=-2e5 (healthy ghost-free + Cassini-safe window),
xi=kap=2e-2. Derivation: `native_dilation_weight_derivation_results.md`. Round target object:
`static_soliton_rerun_derived_operator_results.md`. Round box-control spectrum target:
`STEP2_timelive_matter_results.md`.

---

## 1. THE SMUGGLED VALUE — FOUND AND FIXED (load-bearing)

A first reconstruction inserted **kap8 = 0.05** in front of the matter stress
(`E = fG + (g box - nabla nabla)f - Xf(...) - kap8 f T`). That factor is **NOT in the derived action**:
matter enters as `e^{2phi} L_m` at coefficient 1, with source strength carried by xi=kap. The 0.05
suppressed the source ~20x and was the cause of the first pass's quantitative mismatches (hair and
B=1/A break ~15-20x below the banked doc).

**kap8 = 1 is DERIVED, not chosen** (verifier C1, independent sympy from the SINGLE action): the reduced
Euler-Lagrange of B from `S = INT sqrt-g[fR + Xf(dphi)^2 + f L_m]` gives a matter term equal to
**exactly -1 x** the Hilbert stress of `e^{2phi}L_m` (ratio = -1, symbolic). The action is linear in the
matter coefficient with exactly one matter term `f L_m`; any kap8 != 1 is a different action. The 0.05
was a genuine bug; the fix is forced by the action.

This is the method's "chose-or-derived" tripwire working at the cheap stage: a fixed value that felt
like a convention turned out to change the system, and the correct value is derived, not picked.

---

## 2. GATE A (omega->0 / static round) — PASS

With warps off and phi=phi(r), the reconstruction recovers the round static object:

- **G1 hairless** (phi frozen): recovers B=1/A exact up to the matter-body break only; the t/r collapse
  `E^t_t - E^r_r -> 0` at phi=const under B=1/A (symbolic).
- **G2 vacuum** (L_m=0): the phi EOM reduces to `phi'' + 2phi'/r (+phi'^2) = 0`, a 1/r tail.
- **Localized charge-1**: Theta pi->0; sin^2 peak at r ~ 0.85-1.07 (Nr 16->24) -> L = sqrt(kap/xi) = 1.
  Converges to |F|^2 ~ 1e-13.
- **B=1/A break** (verifier C5, CONFIRMED with a magnitude revision): `rho + p_r = (Theta')^2/B (xi +
  2 kap sin^2 Theta / r^2) > 0` in the winding body (symbolic, exact; e^{2phi} weight ~1) => T^t_t !=
  T^r_r => B != 1/A, **forced and matter-kinetic / OPERATOR-INDEPENDENT** (= the old radial_Bfree break;
  phi is ~2e-7, six orders below, negligible). Magnitude: **grid-noisy band ~0.04-0.10** (saw 0.044 at
  Nr=64; non-monotone in Nr, not sharply grid-converged), central value ~0.07, core-peaked. The
  mechanism / sign / peak-location / operator-independence are robust; the precise magnitude is not
  yet grid-converged (REVISION: stated band widened from 0.06-0.10 to 0.04-0.10).

---

## 3. THE HAIR CORRECTION — NO RESOLVABLE SCALAR HAIR (corrects the banked doc)

`static_soliton_rerun_derived_operator_results.md` banked a "**tiny 1/r scalar hair** q ~ 1/|X|,
q.|X| ~ 0.5" (flagged by that doc itself as SOFT — coarse outer grid). Two reconstructions disagreed
on the magnitude by ~10-50x (doc 0.5 vs first-pass 0.045). The diagnostic (and the blind verifier, C3)
**dissolved both numbers:**

- A 1/r body-fit "q" **does NOT converge** under grid refinement: the doc's number DIVERGES
  (0.5 -> 1.3 over N=20->80); the reconstruction's FLIPS SIGN (q.|X|: -0.060, +0.045, +0.010, +0.015
  over Nr 16->40). Neither is a stable quantity.
- `|phi|max` itself -> 0 with resolution (2.4e-6 -> 2.5e-7); the apparent "q ~ 1/|X| scaling" was
  tracking the CORE AMPLITUDE |phi|max, **not an asymptotic charge**.
- The conserved scalar current (independently derived: `J ∝ r^2 sqrt(A/B) e^{2phi} phi'`, confirming
  the e^{2phi} g^{rr} weight) has a **far-sphere flux ~= 0** on BOTH solvers; the interior current
  noise floor shrinks with refinement (~1e-6 at Nr=40; the conservatively-stated ~1e-3 was a
  seal-boundary-derivative artifact, REVISION: bound tightened to ~1e-6 interior).

**Converged, trustworthy statement:** the round charge-1 soliton on the derived operator carries
**NO resolvable 1/r scalar monopole hair** (conserved scalar charge ~= 0; cannot formally exclude a
hair below the interior noise floor ~1e-6). The honest static object is **GR + a global monopole, no
scalar hair** — even MORE GR-like than the doc's "tiny hair" headline. This **reinforces** the standing
conclusion that the derived operator's teeth are in the DYNAMICS, not the static profile (the static
new-operator effect is smaller than recorded). Do NOT bank either prior q magnitude (0.5 or 0.045).

---

## 4. GATE B (round box-control spectrum) — PASS

The round small-amplitude standing-wave spectrum (self-adjoint Sturm-Liouville from the quadratic
action, Dirichlet both ends), independently rebuilt by the verifier (C2), reproduces the
`STEP2`/`P5e_proper` box-control verdict:

- **Positive tower omega^2 ~ 1/R^2** (cell wall, no intrinsic level): omega^2_low falls
  1.75 -> 0.014 over R=4->48; omega^2 * R^2 plateaus ~20-32 (no positive floor through R=48). The
  zero-intercept fit gives c0 ~ 0.01 (small, consistent with box-control; the airtight c0->0 needs
  R=64 at higher Nr, which the doc reached — THROUGHPUT-limited here, not a physics gap).
- **Exactly ONE negative mode, node-free** = the Derrick/breathing direction, with omega^2_neg -> 0
  as R grows (authoritative step2 solver: R=4:-0.287, 8:-0.252, 16:-0.129, 32:-0.0008; verifier's
  independent build: same COUNT and same R->0 trend). The first pass's "n_neg=0" was a flawed
  full-energy-Hessian V, NOT physics; the action's genuine second variation gives n_neg=1.

**METHODOLOGICAL NOTE (verifier, for the record):** the documented SL potential V **drops a `u·u_r`
cross term** of the genuine second variation. The verifier confirmed this does NOT change the
negative-mode COUNT or the box-control TREND (n_neg=1 and omega^2~1/R^2 both ways), so the central
result is safe — but the documented omega^2_neg MAGNITUDE is not the action-exact value (with the cross
term it is ~10x larger at small R). **Flag for any future QUANTITATIVE use of omega^2_neg.**

**Small-warp continuity (LINEARIZED l=2 proxy — not a 3-D solve):** a tiny l=2 centrifugal warp shifts
the low modes smoothly/monotonically with no discontinuity and no spurious negative. A faithful linear
witness that the angular sector connects continuously to the round one; the full nonlinear 3-D off-round
solve is the (gated) next push.

---

## 5. OPERATOR-ACTION CONSISTENCY — PASS

The phi EOM used IS the action's own equation: `delta S/delta phi = (positive volume weight) x EL_phi`
(verifier C4, independent sympy). The matter piece /sqrt-g equals `2 e^{2phi} L_m` exactly; the vacuum
piece is the operator's vacuum phi-equation up to the strictly-positive measure. Any autograd-of-
discrete-action divergence seen during the build was the spectral `a''` edge term in `e^{2phi}R` (a
discretization artifact that converges with Nr), not a missing physical term.

---

## 6. PREMISE LEDGER (chose / derived)

| # | Premise / value / choice | Status |
|---|---|---|
| Operator E_munu, f=e^{2phi}, a(phi)=e^{phi}; matter weight e^{2phi} | DERIVED upstream (native_dilation_weight); USED |
| **kap8 = 1** (matter coefficient) | **DERIVED** (matter term = -1 x Hilbert stress of e^{2phi}L_m, symbolic) — corrects the first pass's chosen 0.05 |
| X = -2e5 | CHOSE (one healthy ghost-free + Cassini-safe value; X-scanned to expose the 1/|X| amplitude law; not data-fit) |
| xi = kap = 2e-2 | CHOSE (the converged regime, inherited from static_soliton) |
| Charge-1 hedgehog Theta(0)=pi, Theta(seal)=0 | CHOSE (native degree-1; NO m>=2 ladder) |
| Areal static chart, B=1/A FREE | CHOSE chart (CANON C-2026-06-18-1 slice); B=1/A explicitly freed |
| Symbolic continuum EL (vs autograd-of-discrete-action) | CHOSE (proven = delta S/delta field; cleaner than the spectral-a''-noisy discrete-action autograd) |
| SL spectrum recipe (mass metric, Dirichlet ends) | CHOSE (STEP2 recipe); documented V drops a u.u_r cross term (count/trend robust; magnitude not exact) |
| Conserved scalar current J ∝ r^2 sqrt(A/B) e^{2phi} phi' | DERIVED (verifier-confirmed weight); flux ~= 0 |

---

## 7. VERIFICATION (2026-06-21) — blind adversarial pass, agent a6b142162a3211abd

Independent re-derivation FROM SCRATCH (own sympy / own discretization; /tmp used only to reproduce
specific numbers) of all five load-bearing claims. **OVERALL: SUPPORTED-WITH-REVISIONS.**
- **C1 kap8=1 derived** — CONFIRMED (matter term = -1 x Hilbert stress, exact).
- **C2 box-control** — CONFIRMED (one node-free negative mode + 1/R^2 tower, no floor through R=48);
  caught the dropped u.u_r cross term (count/trend unaffected; omega^2_neg magnitude ~10x at small R).
- **C3 no resolvable hair** — CONFIRMED (independent conserved current; flux ~=0; body-fit q
  non-convergent / sign-flipping; tightened noise floor to ~1e-6 interior).
- **C4 operator-action consistency** — CONFIRMED.
- **C5 B=1/A break matter-kinetic** — CONFIRMED with magnitude caveat (band ~0.04-0.10, not sharply
  grid-converged; mechanism/sign/operator-independence robust).

REVISIONS folded into this record: (1) B=1/A break band widened to ~0.04-0.10, flagged not-grid-
converged; (2) hair noise floor tightened to ~1e-6 interior (~1e-3 was a seal artifact); (3) the SL
V's dropped u.u_r cross term noted for future quantitative omega^2_neg use.

---

## 8. HONEST STATUS — settled vs deferred

**SETTLED (banked, verified):**
1. The derived two-player operator is reconstructed into a well-posed radial solver with phi an
   INDEPENDENT player; kap8=1 is DERIVED (the smuggled 0.05 removed).
2. Gate A PASS: localized charge-1 soliton, B=1/A break matter-kinetic / operator-independent (~0.07
   central, band 0.04-0.10).
3. Gate B PASS: the round box-control verdict reproduces — positive 1/R^2 tower (no floor through R=48)
   + exactly one node-free negative Derrick mode (omega^2_neg -> 0 with R).
4. The operator IS the action's own equation (delta S/delta phi check).
5. **HAIR CORRECTION:** no resolvable scalar hair (conserved charge ~= 0); both prior q magnitudes are
   fit artifacts. Static object = GR + global monopole, no hair (more GR-like than banked).

**DEFERRED / THROUGHPUT-LIMITED (NOT done here):**
- The genuine **3-D off-round residual** (phi wired into the full3d a,b,c,d machinery) is NOT built —
  that is the next push (where the phi-angular obstruction is actually tested). Small-warp here was a
  linearized l=2 proxy only.
- Box-control intercept c0 -> 0: reached R=48 (c0~0.01); the airtight R=64/higher-Nr version is the doc's
  and a B6 numerics task.
- Hair: ~0 to ~1e-6 interior resolution; a hair below that is not formally excluded.

---

## 9. ATTACK HERE (for any future re-grade)

1. **The conserved scalar current weight** `e^{2phi} g^{rr}`: re-derive the Noether/Gauss-law current
   independently; confirm flux ~= 0 is interior-converged, not a noise floor masking a small hair.
   Push small |X| (large |phi|) + a Robin/asymptotic outer BC to chase a sub-1e-6 hair.
2. **The SL cross term** `u.u_r`: confirm including it leaves n_neg=1 and the box-control trend, and
   recompute omega^2_neg with it for any quantitative use.
3. **B=1/A band**: tighten with a graded/finer core mesh; confirm the 0.04-0.10 spread is Chebyshev-
   node-vs-steep-core noise, not a real spread.
4. **The deferred 3-D off-round residual is where the physics is** — this gate validates the operator
   in the round limit only; the off-round l>=2 angular obstruction is UNTESTED on the derived operator.
