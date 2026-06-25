# Independent Blind Verifier — Did vacuum UDT depart from GR? (gravity-sector re-derivation)

**Verifier:** Claude Opus 4.8 (1M), blind adversarial pass, **2026-06-18**.
**Method:** independent sympy re-derivation from scratch (CPU). I did NOT read the
constructor's scripts (`gravity_sector_*.py`) or its results doc
(`udt_gravity_sector_rederivation_results.md`) until AFTER completing my own
derivation of the four load-bearing claims. I read only the disputed original
(`udt_field_equations_derivation_results.md`). Nothing committed was changed; no
git commit. Default stance: skepticism — this CONFIRMS the owner's prior, so I
attacked the three flagged joints hardest.

My independent scripts (in /tmp, not committed): verif_st.py, verif_schw.py,
verif_slaved.py, verif_dof.py, verif_solve.py, verif_check.py.

---

## Summary table

| Claim under test | Verdict | My independent number |
|---|---|---|
| (i) terms dropped; honest vacuum eqn = `fG + (g□-∇∇)f = 0` | **CONFIRMED** | E_μν nonzero; matches §2 |
| (ii) Schwarzschild fails honest vacuum | **CONFIRMED** | residual `EQ_tt/f = 14 r_s²/(r³(r-r_s))` |
| (iii) conformal kinetic term physical (coeff 96 ⇒ not GR) | **CONFIRMED-with-caveat** | (3/2)(F'/F)² = (3/2)(−8)² = **96** |
| (iv) phi-slaved robustness (slaving does NOT kill survival) | **CONFIRMED** | honest minisuperspace EL_N(schw) = `−7c0³ r_s²(r−r_s)²/(8πG r⁴) ≠ 0` |

**OVERALL: YES — vacuum UDT departs from GR**, conditional on the premises below
(notably granting the EH R-term and the `c⁴/16πG` coupling). The departure is
PHYSICAL/invariant, not a chart artifact.

---

## Joint 1 (THE LINCHPIN) — phi slaved vs independent: does the slaving kill E?

This was the joint the task flagged as "most likely wrong." I tested it two
fully-independent ways and they AGREE.

- **Independent-field reading** (vary `S=∫√-g f(φ)R` treating f as a separate
  field): I computed the full Einstein tensor and the `E_μν=(g□-∇∇)f` term with
  `f=c0⁴e^{−8φ}/16πG`. E is manifestly nonzero (e.g. `E^r_r/f = 8e^{−2φ}(rφ'−2)φ'/r`).

- **HONEST SLAVED reading** (the adversarial test): I built the reduced
  (minisuperspace) action with TWO free radial functions `N(r)=−g_tt`, `L(r)=g_rr`,
  and substituted `f = N⁴/(c0⁴·16πG)` — i.e. f is a function of the METRIC
  COMPONENT g_tt, NOT an independent field — then varied the reduced action
  directly via the full Euler–Lagrange operator (including the 2nd-derivative term,
  since R carries N''). This automatically respects the slaving and retains the
  Hamiltonian/constraint equation. Result at Schwarzschild:

  ```
  EL_N(schw) = −7 c0³ r_s² (r − r_s)² |sinθ| / (8πG r⁴)   ≠ 0
  EL_L(schw) ≠ 0   (same (r−r_s)/r⁶ structure)
  EL_N(flat) = EL_L(flat) = 0
  ```

- **Cross-check the two readings agree:** EL_N (slaved) / [f G + E]^t_t
  (covariant, f-independent) = `−r³/(c0(r−r_s))`, a smooth nonvanishing Jacobian
  (the `δ/δN` ↔ lower-index chain-rule + √-g factor). Both vanish at the SAME
  locus (only r→∞), i.e. both say Schwarzschild fails everywhere.

**VERDICT (iv): CONFIRMED.** The slaving does NOT cancel the surviving terms. The
δf/δg_tt contributions the task worried about do not produce a cancellation; the
honest metric-only variation reproduces the same Schwarzschild failure. The
constructor's "robust to slaved-vs-independent" claim is TRUE on my independent
computation. This is the joint I expected to break the claim, and it held.

---

## Joint 2 — conformal-equivalence escape: physical or pure-gauge?

- **Coefficient 96 reproduced independently:** with Ω²=F(φ)=e^{−8φ}, the
  Einstein-frame kinetic coefficient (3/2)(F'/F)² = (3/2)(−8)² = **96**, nonzero.
  So the c⁴-on-R factor is NOT pure relabeling — it is Brans–Dicke-type.

- **The genuine subtlety the task raised (is the kinetic term carried by a real
  DOF?):** here φ is slaved to the metric, so there is no SEPARATE scalar DOF to
  "carry kinetic energy." BUT that does not make the departure unphysical. The
  invariant test is whether a curvature-/equation-level difference survives that
  no coordinate or units choice can remove. It does: Schwarzschild is Ricci-flat,
  so f·G=0 there, and the entire residual `14 r_s²/(r³(r−r_s))` IS the surviving
  E term — a nonzero value of a tensor equation on a fixed geometry. No chart
  change can turn a nonzero `f G^μ_ν + E^μ_ν` into zero (it is a tensor eq). The
  original doc's "absorbable" argument was correct for c IN g_tt alone (a genuine
  reparametrization of the lapse) but does NOT extend to c⁴ MULTIPLYING R — the
  constructor correctly identifies this as the exact site of the error. I confirm
  the distinction: lapse-c folds into φ (chart); coupling-c⁴ does not (dynamics).

  **VERDICT (iii): CONFIRMED, with caveat.** The departure is physical/invariant
  (a nonzero tensor field equation on Schwarzschild). I note honestly that "96"
  is presented as an Einstein-frame *kinetic* coefficient; with φ slaved it is
  better read as the curvature-level non-cancellation (the 96 and the
  Schwarzschild residual are two faces of the same surviving E). Either framing
  yields "not GR." This is why I grade CONFIRMED-with-caveat rather than a flat
  CONFIRMED of the literal "dynamical scalar" wording.

---

## Joint 3 — the over-constraint smell: flat-only, artifact or real?

I went past the constructor here to settle whether "flat-only" is an artifact of
imposing B=1/A. I did NOT impose B=1/A. With N, L independent:

- `EL_L = 0` is ALGEBRAIC in L (the Hamiltonian/constraint):
  `L = 2r²(N'/N)² + 9r(N'/N) + 1`.
- Substituting into `EL_N = 0` gives a single 2nd-order ODE for φ (writing
  N=c0²e^{−2φ}); its nontrivial factor is `−8r²φ'³ + 18rφ'² − rφ'' − 2φ' = 0`.
- This ODE DOES admit nontrivial φ'≠0 solutions (I integrated it numerically). So
  "no solution" is too strong. BUT — the constraint then forces
  `L = 2r²(N'/N)² + 9r(N'/N) + 1`, which along every nontrivial solution I tried
  goes **NEGATIVE** (e.g. L = −1.59 at r=3). A negative g_rr is a signature flip,
  not a physical Lorentzian metric. At φ'=0 (flat) the constraint gives L=+1.

**VERDICT (joint 3): CONFIRMED in substance, sharpened in wording.** Within the
static-SSS-diagonal slice the honest vacuum equations admit **only flat space as
a regular Lorentzian solution** — the nontrivial branches exist mathematically
but require g_rr<0 (unphysical). This is NOT an artifact of pre-imposing B=1/A: I
kept N and L fully independent and the over-constraint reappeared as the
constraint driving g_rr negative. The DOF count is honest (2 functions, 2
equations, one algebraic = a constraint), and the system is over-stiff for
massive Lorentzian vacua. Physically: the modification makes vacuum STIFFER, not
richer — consistent with (but not proof of) the critical-energy / boundary-tension
reading the constructor offered. The macro-story tension the task flagged is REAL
and should be logged: if honest static-SSS UDT vacuum has no massive exterior,
the galactic/lensing successes must come from (a) matter present (T≠0), (b) the
non-static or non-diagonal sectors, or (c) the global/finite-boundary sector — NOT
from a static isolated vacuum profile. This does not refute the departure claim;
it raises a downstream physical question for the program.

---

## Principle-7 note (flagged, not resolved)

Granting the Einstein–Hilbert R-term at all is itself a possible Principle-7
smuggle (defaulting to GR's action FORM). The constructor flags this as A1
(unresolved) and I concur it is unresolved. The verdict is correctly scoped as
"**even granting GR's R-term**, carrying the c⁴ coefficient honestly makes vacuum
≠ GR." A fully native gravity action could differ further; the specific numbers
(−8, 96, 10/9, 8φ'²−φ'') are tied to the c⁴ power, but ANY non-constant
coefficient on R leaves nonzero ∇∇f, so "vacuum ≠ GR" is robust to the exact
power.

---

## Discrepancies with the constructor (after reading its doc/scripts)

None material. Every computational number I produced independently matches:
- Einstein tensor (G^t_t=G^r_r, G^θ_θ) — identical.
- E_μν nonzero, E^r_r/f = 8e^{−2φ}(rφ'−2)φ'/r — identical.
- Schwarzschild residuals: EQ_tt/f=14r_s²/(r³(r−r_s)), EQ_rr/f=2r_s(4r−3r_s)/(r³(r−r_s)),
  EQ_θθ/f=4r_s(5r_s−r)/(r³(r−r_s)) — identical.
- Slaved EL_N(schw) = −7c0³r_s²(r−r_s)²/(8πG r⁴) — identical.
- Conformal coeff 96 — identical.
- Flat solves; Schwarzschild fails — identical.

The only refinements I add (not corrections): (a) the constructor's §5 "only
φ'≡0 satisfies both" is more precisely "only flat is a regular LORENTZIAN
solution; nontrivial branches exist but force g_rr<0"; (b) the "96 = dynamical
scalar kinetic term" wording is slightly loose given φ is slaved (no separate
DOF) — the invariant content is the non-cancelling tensor residual, which is what
actually proves not-GR.

---

## OVERALL VERDICT

> **YES — vacuum UDT genuinely (physically, invariantly) departs from GR**, given
> the premises (EH R-term granted [A1, unresolved Principle-7 question]; the
> c⁴/16πG coupling granted [A2]; static-SSS-diagonal slice). The
> `(g_μν□−∇_μ∇_ν)f(φ)` terms survive at T=0, are nonzero, cannot be removed by
> chart/units, and make Schwarzschild fail the honest vacuum equation. The
> original doc's "vacuum = Schwarzschild/Birkhoff exactly" arises from writing
> `G^μ_ν=(8πG/c⁴)T^μ_ν` — dividing by the position-VARYING c⁴ as if constant —
> which silently drops the ∇∇f terms. The constructor's central claim is CONFIRMED
> on a fully independent re-derivation, including the hardest joint (φ-slaved),
> which I expected to break it and did not.
>
> DEPENDS-ON (the honest unfixed choices, none of which rescue GR): the EH R-term
> as the native gravity action (Principle-7 open); the exact c⁴ power (only the
> numbers move, not the verdict); and the downstream physical question that the
> honest static-SSS vacuum is over-stiff (flat-only for Lorentzian metrics), which
> the program must reconcile with its macro/galactic successes (matter-present /
> non-static / global-boundary sectors, out of this slice's scope).

CANONIZATION = Charles's call.

---

## CORRECTION (2026-06-18, Charles-approved, driver-appended)

This pass correctly verified the MATH of the constructor's re-derivation, but
both docs analyze an ASSUMED `c^4·R` (`f(phi)R`) action that UDT does NOT use
(validated corpus `udt_validated_results.md` line 3064: UDT = Einstein-Hilbert +
MINIMALLY-coupled scalar, "no `f(phi)R`"). That action is independently
solar-system-falsified (PPN γ=9; see `gravity_sector_local_reduction_results.md`).
So "vacuum UDT departs from GR" is a true statement about a FALSIFIED non-UDT
action, not about UDT. Dead-end logged. Live program: derive UDT's φ-law
NATIVELY from the dilation-carrying metric (action downstream, no assumed action,
no Λ). NOT canon.
