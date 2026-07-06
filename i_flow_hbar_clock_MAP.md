# i-flow / ℏ clock MAP — is there a native action-per-phase-cycle, or only structural i?

**Mode:** DERIVE-OR-REFUTE MAP (armchair + CAS; sympy-exact; NO numerical PDE solve, NO data, NO
particle labels). **Status: BANKED — BLIND-VERIFIED (verifier a847ba3e0429d6c4a, 2026-07-05: OUTCOME 7
HOLDS; all 7 attacks PASS, no Outcome 6 found). The flip point — the G^t_r momentum-constraint channel
(linear in ω) — was independently order-counted and confirmed a FIRST-CLASS CONSTRAINT whose
back-substitution gives an O(ω²) renormalization of I, NOT a symplectic ∫dt A·∂_t n (no O(1) T-odd
background to source a Berry/Landau term). Structural i re-confirmed CAS-exact; the anti-"area form ⟹ ℏ"
discipline verified correct. Verifier ADDED an independent nail: the 3+1D θ-term ∫F∧F ≡ 0 (F=n*ω, ω∧ω=0
on the 2D target, H⁴(S²)=0) ⇒ NO continuous ℤ θ-angle exists at all. Two wording/citation fixes folded
in: (1) the π₄↔π₅ slip corrected; (2) "seal FORBIDS" softened to "θ̇ is t→−t-odd; the seal's
projecting-out is the OPEN NODE-1 question" — the verdict rests on lines 1+2 (independent, decisive).**
**NOT canon.** **Driver:** claude-opus-4-8[1m]. **Date:** 2026-07-05.
**CAS:** `/tmp/.../iflow_cas.py` (reproduced inline below; sympy-exact, bounded, no solve).

**THE QUESTION.** The native S² carrier already carries STRUCTURAL i (the target's complex/Kähler
structure — established, F6 N-2). Is there ALSO a native ℏ — a native action-per-phase-cycle
coefficient — or only structural i without a dimensionful action quantum? Structural i being native
does NOT by itself give ℏ; the load-bearing discipline here is to aim HARDEST against the tempting
shortcut **"the S² area form, therefore ℏ."** That inference is INVALID unless the NATIVE time-live
action supplies a dimensionful action-per-phase-cycle coefficient. This MAP tests whether it does.

**HEADLINE (Task 5, the crux): the native time-live action is SECOND-ORDER (a rigid-rotor moment of
inertia), with NO native first-order Berry/Wess-Zumino/symplectic term.** Structural i is native;
**ℏ is NOT derived** (Outcome 7). The "area form ⟹ ℏ" shortcut is REFUTED: the area form is a
STATIC symplectic/Kähler 2-form on the target and its helicity is a dimensionless topological
INTEGER (Q_H ∈ ℤ) — it supplies i and a charge, not an action quantum. To read a ℏ off it you need
a first-order-in-time term whose coefficient is a dimensionful, anchored action; the native action
does not contain one, and the seal t→−t involution actively disfavors a non-topological one.

---

## THE HYPOTHESIS, WHOLE (stated before slicing)

- **Structural i is native** (to re-confirm): on T_nS², J_n(v)=n×v with J_n²=−1, and the area form
  ω_n(u,v)=n·(u×v) is the symplectic/Kähler 2-form, metric-compatible. This is a property of the
  TARGET geometry — it exists on any config, static or live. (F6 N-2/N-3; largely established.)
- **ℏ is the OPEN question.** ℏ would be an action-per-phase-cycle: a dimensionful coefficient of a
  FIRST-ORDER-in-time (symplectic) term, ∮ p dq = (action), that survives as the phase winds once.
  The hypothesis to TEST (not assume): does UDT's native time-live sigma-model supply such a term,
  and if so is its coefficient dimensionful AND anchored?

Kept DISTINCT throughout: **structural i (ESTABLISHED)** vs **ℏ (the OPEN question).** The whole
danger is laundering the first into the second.

---

## PREMISE LEDGER (chose / derived / import)

| # | premise | tag | note |
|---|---|---|---|
| carrier = unit 3-vector n_a, |n|=1, target S² | THEORY (C-2026-06-14-1) | blind-verified anchor |
| native action E=∫[(ξ/2)|∂n|² + (κ/4)F_ij²] (FS L2+L4) | DERIVED | unique diffeo-scalar ≤4-deriv, target-isometry-inv (`angular_lagrangian_results.md`, `node_H3:48`); ξ,κ CHOSE normalizations (category-A) |
| metric ds²=−e^{−2φ}c²dt²+e^{2φ}dr²+ρ²dΩ² | DERIVED | `relativistic_metric_rederivation_results.md` (g_tt g_rr=−c²) |
| time-live kinetic weight = g^{tt}=−e^{2φ}/c² (SECOND-order) | DERIVED (this MAP, CAS) | forced by covariance on the native metric |
| seal involution: TIME-ON sector governed by t→−t | THEORY (CANON C-2026-07-04-1) | temporal mirror; governs the phase/rotating fields |
| structural i = J_n / area form ω_H1 | DERIVED-candidate (F6 N-2) | re-confirmed CAS-exact here (Task 1) |
| Q_H=∫A∧dA ∈ π₃(S²)=ℤ | DERIVED (H2, blind-verified) | dimensionless topological integer, metric-free |
| ℏ / quantization-as-a-rule | IMPORT (postulate A) | the object under test — do NOT import to "derive" it |
| geometric quantization / Schrödinger form / canonical commutators | NOT USED (forbidden) | would smuggle the answer |
| measured value of ℏ | NOT USED (forbidden) | data-blind |

---

## TASK 1 — STRUCTURAL i (re-confirm; CAS-exact) — ESTABLISHED

On the tangent plane T_nS² (n·v=0, |n|=1), define J_n(v)=n×v. CAS (sympy, exact):

```
J_n^2(v) - [ n(n·v) - v|n|^2 ] = [0,0,0]          (identity, all n,v)
  on the tangent plane (n·v=0, |n|=1):  J_n^2(v) = -v          => J_n^2 = -1
  at n=e3:  J(e1)=e2 (rotation by +pi/2),  J(e2)=-e1,  J^2(e1)=-e1
area/symplectic 2-form  omega_n(u,v) = n·(u x v)
compatibility:  omega_n(u, J_n u) = (n·n)|u|^2 - (n·u)^2  --> |u|^2  on |n|=1, n·u=0
  explicit unit n(theta,phi), u = a e_theta + b e_phi:  omega(u,J_n u) - |u|^2 = 0  (exact)
```

**VERDICT: CONFIRMED.** J_n²=−1 (a rotation by π/2 in the tangent plane), ω_n is the compatible
symplectic/Kähler form (ω(u,J u)=|u|²>0), so (S², ω, J, g) is Kähler and i=J is native. This is a
property of the TARGET, independent of any dynamics. **Structural i is native.** (Does NOT yet give ℏ.)

---

## TASK 2 — THE NATIVE PHASE CONNECTION FROM THE HOPFION — ESTABLISHED (H2)

The winding 2-form ω_S² = sin θ dθ∧dφ is closed (a top 2-form on S²; dω=0) with ∫_{S²}ω=4π (deg-1
generator; CAS confirms 4π). Pulled back by the field n: R³→S², **F := n*ω_S²** is the closed field
2-form (H2: dF=0, {dn_a} rank-2 on |n|=1). On a localized defect F is EXACT on the base, so it has a
GLOBAL potential **A** with **dA=F** — this A is the U(1) connection on the Hopf bundle (the pullback
of the S² monopole potential; NO Dirac string because deg→0 at infinity ⇒ F exact ⇒ A global native).

The self-linking is the **Whitehead integral Q_H = ∫A∧dA ∈ π₃(S²)=ℤ** — a homotopy invariant read off
n, metric-free (A∧dA is a 3-form, needs only orientation; the warp e^{2φ} never enters), integer,
DIMENSIONLESS. **This is a THEOREM of algebraic topology (Category-A), NOT a Chern-Simons/gauge
import** (L2+L4 contains no A, no −¼F² kinetic, no gauge coupling — H2, blind-verified).

**VERDICT: CONFIRMED (H2).** A is native; F=dA=n*ω_S²; Q_H is the Whitehead integer. **Note for the
ℏ question:** Q_H is a dimensionless INTEGER. It is the STATIC helicity of the SPATIAL field — a
count, not an action. (This is exactly where the shortcut fails; see CF-6.)

---

## TASK 3 — WHAT THE i-FLOW IS (pick with evidence)

The candidates: (a) Hopf-fiber phase; (b) target U(1) rotation about n_∞; (c) hopfion collective
orientation zero-mode; (d) pure gauge/coordinate convention.

**Evidence (no_selector_audit, blind-verified ac28a9c57dcfd18be; CAS T1):** by Hopf **equivariance**,
a SPATIAL rotation about the torus axis IS a TARGET rotation about n_∞ (w→e^{iα}w, exact) — so (b)
and (c) are the SAME object (the diagonal SO(2)). On the isotropic round cell the torus axis is a
**FREE ZERO-MODE** (Goldstone of spontaneously broken spatial SO(3)→SO(2), energy-degenerate; CAS
T1b: energy depends on space only through rotation-scalars). And n_∞ per se is a **gauge choice**
(Target 3: the charge readouts are n_∞-independent).

**VERDICT: the i-flow = a GENUINE COLLECTIVE COORDINATE (b=c), the free orientation zero-mode — NOT
pure gauge (d).** It carries genuine (zero-cost) dynamics: it is a real modulus of the solution
space, a rigid-rotor angle. But it is a RIGID CYCLIC coordinate (an angle θ∈[0,2π) with no
potential), and its ABSOLUTE value is a gauge/convention while its MOTION θ(t) is physical. This is
the object to promote to time-dependence in Task 4. (CF-2 checked below: not pure gauge — there IS a
DOF — but the DOF is a flat rotor, which is why the ℏ question turns on Task 5, not Task 3.)

---

## TASK 4 — THE TIME-LIVE ACTION FOR THIS COORDINATE (derived from the native metric)

Promote the orientation to θ(t) and read the kinetic term off the native relativistic sigma-model
L = −(ξ/2) g^{μν}(∂_μ n_a)(∂_ν n_a) on the native metric. CAS (exact):

```
g_tt = -e^{-2phi} c^2      =>   g^{tt} = 1/g_tt = -e^{2phi}/c^2
time density:  L_t = -(xi/2) g^{tt} (d_t n)^2 = +(xi/2)(e^{2phi}/c^2) thetadot^2 |d_theta n|^2
```

Integrating over the cell, **L_t = ½ I θ̇²** with the moment of inertia
**I = ∫ (ξ e^{2φ}/c²) |∂_θ n|² √(g_space) d³x** (positive, dimensionful). The Faddeev term (κ/4)F²
adds a further **second-order** contribution of the same rotor form (H3; the Skyrme term is
(n×∂n)² — quadratic in ∂, hence quadratic in θ̇). 

**VERDICT: the native time-live action for the phase/orientation coordinate is a RIGID-ROTOR,
SECOND-ORDER-in-θ̇ kinetic term ½Iθ̇² — a moment of inertia, NOT an action-per-cycle.** The native
metric time-weight e^{−2φ}/e^{+2φ} multiplies this SECOND-order (T-EVEN) term; it supplies a rotor
inertia I, not a symplectic coefficient. (I is also FREE/data-blind: I∝ξ with ξ a free normalization
— see CF-4.)

---

## TASK 5 ★ — FIRST-ORDER vs SECOND-ORDER (THE DECISIVE TASK, load-bearing)

Does the native action contain a FIRST-ORDER-in-time symplectic / Wess-Zumino / Berry term
(∝∫dt A·∂_t n, or ∝Q_H·θ̇, linear in θ̇ — which would supply a symplectic structure and a natural
action quantum), or ONLY the second-order ½Iθ̇² rotor of Task 4?

**Three independent lines all say: ONLY SECOND-ORDER. No native first-order term.**

**(1) The native action has no such term (DERIVED, corpus-established).** L2+L4 is built from
(∂n)² and F² — both quadratic in derivatives, hence quadratic (never linear) in θ̇. There is no
∫dt A·∂_t n term in the action; there is no −¼F² gauge kinetic and no A in L2+L4 (H2). The corpus
computed this directly: **NEGATIVE #49** (`monodromy_depth_results.md`, blind-verified) — "the
internal-longitude twist enters ONLY as (Ψ′)² (zero source, no linear/bare term)"; and **there is no
native WZW/Hopf (π₃) term in L2+L4.**

**(2) The rotor Berry connection is FLAT = 0 (DERIVED, corpus-established).** **NEGATIVE #53**
(`crux2_coinflip_results.md`, blind-verified STANDS) — the rigid-rotor Gaussian fluctuation-vacuum
Berry connection (½)Im Tr[S⁻¹dS] = 0 because L2+L4 is REAL and P/T-even ⇒ real symmetric fluctuation
operator ⇒ **flat connection ⇒ 2π holonomy = +1 ⇒ no linear-in-velocity/WZW term ⇒ ν=0 DERIVED.**
The su(3) rep-theory route agrees: carrier ℓ=1 (integer spin) ⇒ U(2π)=1 exactly; all generators
traceless ⇒ no central extension ⇒ non-projective ⇒ no anomaly/WZW at the functional level either.

**(3) The seal t→−t DISFAVORS a bare first-order term (this MAP + CAS; seal-projection is NODE-1 OPEN,
verifier-corrected).** A first-order term L₁ = A_a(n)∂_t n_a ~ b·θ̇ is LINEAR in θ̇, hence **ODD under
t→−t** (θ̇→−θ̇). The TIME-ON sector is governed by the temporal mirror t→−t (CANON C-2026-07-04-1),
which by canon is the pure t→−t mirror, **explicitly NOT P×T** (CANON.md:371-378) — so the T-even
escape route (a P×T-even first-order term) is unavailable. **CAVEAT (verifier a847..):** whether the
seal actually PROJECTS OUT / pins / permits the ω of a spinning phase is flagged OPEN as canon NODE-1
(CANON.md:391-393); so this line is a DISFAVORING, not a settled forbidding. **The verdict does not rest
on it** — lines (1) and (2) independently and decisively kill the first-order term. And the topological
escape is independently closed: the only continuous 3+1D θ-term candidate ∫F∧F **vanishes IDENTICALLY**
(F=n*ω_S² and ω∧ω=0 on the 2-dimensional target, H⁴(S²)=0 — verifier-added nail), so there is NO
ℤ-valued time-Wess-Zumino theta-angle of that form to carry an anchored first-order coefficient; the
only topological class is the DISCRETE π₅(S²)=ℤ₂ statistics sign (#53), not a continuous ℤ. The static
helicity Q_H∈ℤ (Task 2) is a SPATIAL 3-form invariant, not a term in the time-action. (By contrast the
SECOND-order ½Iθ̇² term is T-EVEN and survives regardless — consistent with it being the only native
time term.)

**★ VERDICT (Task 5): ONLY SECOND-ORDER.** The native time-live action for the phase/orientation
coordinate is the rigid-rotor ½Iθ̇² — a moment of inertia. There is NO native first-order
symplectic/Berry/Wess-Zumino term: it is absent from the action (line 1), the rotor Berry connection
computes to exactly zero (line 2), and the seal t→−t forbids a non-topological one while no ℤ-valued
topological θ-angle exists to supply an anchored one (line 3). **This is the load-bearing result of
the MAP.**

---

## TASK 6 — (conditional on a first-order term) — DOES NOT APPLY

No native first-order term exists (Task 5), so there is no first-order coefficient to derive or to
test for an anchor. **Outcome 6 (a candidate ℏ_UDT) DOES NOT OBTAIN.** For the record, even the
SECOND-order coefficient I is dimensionful but **FREE/UNANCHORED** (I∝ξ, ξ a free data-blind
normalization; e^{2φ} background) — a moment of inertia sets an ENERGY scale (once combined with an
externally-supplied ℏ, via ℏ²/2I), never an action-per-cycle by itself.

---

## TASK 7 — (only second-order flow) — THE HONEST VERDICT — Outcome 7

**OUTCOME 7: structural i is native, but ℏ is NOT yet derived.** The native time-live action gives a
rigid-rotor moment of inertia ½Iθ̇² — an energy scale, NOT an action-per-phase-cycle quantum. The
rotor is a compact cyclic coordinate (θ∈[0,2π)); its classical action ∮p dθ = I θ̇·2π is a CONTINUOUS
function of θ̇, taking any value — it is NOT quantized natively. To turn this into a discrete
spectrum (spin ~ ℏ²n²/2I, or Bohr–Sommerfeld ∮p dθ = 2πℏn) requires an **EXTERNAL ℏ** to set the
action unit — which is exactly the postulate (postulate A / P-1) we must NOT import. The native
structure supplies the phase space (the compact rotor, structural i, the symplectic FORM ω on the
target) but NOT the symplectic SCALE (the dimensionful ℏ that says how much area = one state).

This is fully consistent with the banked F6 ledger: **i = area form is a DERIVE-candidate (N-2,
native); ℏ / quantization-as-a-rule is P-1 (POSTULATED, the minimal import);** "the i-FLOW / dynamics
e^{iS/ℏ} is the separate parked clock/ℏ gap" (F6 N-2, verbatim). This MAP CONFIRMS that parking with
a derivation: the gap is real and structural — the native action is second-order, so there is no
native action quantum, and the shortcut that would close the gap ("area form ⟹ ℏ") is invalid.

---

## CLEAN-FAILURE LEDGER (pre-registered, frozen; each fired / did-not-fire with evidence)

| CF | statement | fired? | evidence |
|----|-----------|--------|----------|
| **CF-1** | structural i requires an imported complex Hilbert space | **DID NOT FIRE** | i=J_n native on the target; J²=−1, ω Kähler-compatible, CAS-exact (Task 1). No Hilbert space posited. |
| **CF-2** | the phase flow is only a gauge/coordinate convention (no dynamics) | **DID NOT FIRE (strictly)** | The i-flow is a genuine collective-coordinate DOF (free orientation zero-mode = target U(1) via equivariance; no_selector T1/T1b), not pure gauge. BUT it is a FLAT RIGID ROTOR — n_∞'s absolute value IS a gauge choice; only its motion is physical. Weak-fire flavor: the dynamics is trivial (flat). |
| **CF-3** | no native first-order phase-action term exists (only second-order) | **★ FIRES** | Task 5, three lines: absent from L2+L4 (#49); rotor Berry connection =0 (#53); seal t→−t forbids a bare one, no ℤ theta-angle (π₄=ℤ₂ sign). THE load-bearing failure. |
| **CF-4** | the coefficient of any phase-action term is FREE/unanchored | **FIRES** | No first-order coefficient exists to anchor; the second-order I∝ξ is dimensionful but FREE/data-blind (Task 6). |
| **CF-5** | deriving ℏ requires measured input / an external ℏ | **FIRES** | Quantizing the rotor (spin ℏ²n²/2I or ∮p dθ=2πℏn) needs an EXTERNAL ℏ = postulate A / P-1; not native (Task 7). |
| **CF-6** | the Hopf helicity gives only an INTEGER (Q_H), not a dimensionful action quantum | **FIRES** | Q_H=∫A∧dA ∈ π₃(S²)=ℤ is dimensionless, topological, metric-free (Task 2); it is the STATIC spatial helicity, not a term in the time-action. It supplies i + a charge count, never an action-per-cycle. |

**Net:** CF-3, CF-4, CF-5, CF-6 all fire (the ℏ-not-derived cluster); CF-1 and CF-2 do not (structural
i and the collective-coordinate DOF are both genuine/native). This is the clean Outcome-7 signature:
**native phase space, native i, native charge integer — but NO native symplectic SCALE (no ℏ).**

---

## FOR THE VERIFIER / ATTACK SURFACE

**★ #1 thing to attack: the "area form ⟹ ℏ" shortcut.** The tempting bad inference is: "the S² area
form ω_H1 is the symplectic form, symplectic form ⟹ quantization ⟹ ℏ, done." Attack it — and confirm
it is INVALID here — on these grounds: (a) ω is a symplectic FORM (a dimensionless 2-form on the
compact target); a ℏ is a dimensionful SCALE that says "this much symplectic area = one quantum
state." Geometric quantization SUPPLIES that scale as its input (λ=ℏk/2, F6 P-1) — it does not derive
it. Removing the imported rule removes the scale. (b) Q_H∈ℤ is a dimensionless integer, not an
action. (c) The area form is STATIC (a target/spatial object); a ℏ lives in the TIME-action, and the
native time-action is second-order (Task 5). If the verifier can exhibit a NATIVE, dimensionful,
anchored action-per-cycle WITHOUT importing geometric quantization / a Schrödinger form / canonical
commutators / the measured ℏ, then Outcome 7 flips to Outcome 6 — that is the falsifier.

**Other attack points:**
1. **Task 5 line 1 (no term in the action).** Re-derive that L2+L4 (and the metric measure) contain
   no linear-in-∂_t n term. Try: does the OFF-DIAGONAL / momentum-constraint channel G^t_r (the
   "first-order phase channel" flagged in QUANTIZATION_MAP §1) hide a genuine ∫dt A·∂_t n once the
   time row is live? P4 (`p4_time_live_results.md`) found G^t_r is O(ω) LINEAR in ω — attack whether
   that linear-in-ω momentum constraint IS a first-order symplectic term in disguise (my read: it is
   a CONSTRAINT G^t_r=source, not a term in the matter action; but this is the strongest place to
   look for a first-order structure and deserves a hard independent look).
2. **Task 5 line 2 (Berry=0).** Confirm #53's flat-connection result is not scoped away by the
   revised-N4 whole-cell backreaction (h_AB cell-filling) — does the backreacted moduli space acquire
   a Berry curvature the rigid-rotor calc missed? #53's real/P-T-even argument should survive (h_AB
   target-scalar, no_selector Target 4d), but check the connection on the FULL moduli space, not just
   the internal rotor.
3. **Task 5 line 3 (seal forbids first-order).** Attack the parity claim: is the phase coordinate θ
   genuinely t→−t ODD, or could the seal act on it as a combined P×T (the competing involution on
   record, `F4_seal_boundary_MAP.md` (d)) under which a first-order term is EVEN and survives? If a
   native involution makes ∫A·∂_t n seal-invariant, line 3 weakens (lines 1–2 still hold).
4. **CF-2 (gauge vs DOF).** Confirm the orientation zero-mode is a genuine modulus (not pure gauge)
   AND that promoting it to θ(t) is legitimate (a slow collective-coordinate, not a spurious gauge
   motion). If it is pure gauge, CF-2 fires and even the second-order rotor is illusory.
5. **Anti-import / data-blind audit.** Confirm NO geometric quantization, Schrödinger form, canonical
   commutator, or measured ℏ entered; confirm the only numbers are geometric (4π, integer Q_H,
   π₄=ℤ₂) and the couplings ξ,κ stayed symbolic/free; confirm no particle label was used.

---

## BOTTOM LINE

**Structural i is native** (Task 1, CAS-exact; F6 N-2 re-confirmed) — J_n²=−1 and ω is the compatible
Kähler form on the target. **ℏ is NOT native (Outcome 7).** The native time-live action for the
phase/orientation coordinate is a **rigid-rotor, second-order ½Iθ̇²** (moment of inertia from the
e^{2φ}/c² time-weight); there is **NO native first-order symplectic/Berry/Wess-Zumino term** — it is
absent from L2+L4 (#49), the rotor Berry connection is exactly flat (#53), and the seal t→−t disfavors a
non-topological first-order term (its projecting-out is NODE-1 open) while the only continuous θ-term
candidate ∫F∧F vanishes identically (ω∧ω=0 on S², H⁴=0) and the discrete π₅(S²)=ℤ₂ offers only a sign,
not a ℤ theta-angle to anchor one (Task 5, load-bearing; lines 1+2 are the decisive, independent legs).
The Hopf helicity Q_H is a dimensionless topological INTEGER (Task 2), not an
action quantum. Clean failures CF-3/4/5/6 fire; CF-1/2 do not. **The "area form ⟹ ℏ" shortcut is
refuted:** the native structure supplies the phase space, structural i, and a charge integer, but NOT
the dimensionful symplectic SCALE — quantizing the rotor still requires an EXTERNAL ℏ (postulate A /
P-1), exactly the input the discipline forbids importing. This DERIVES (rather than merely parks) the
F6 verdict: i = area form is native; the i-flow/ℏ clock is a genuine, structural gap. **DRAFT — owes
a blind verifier.**
