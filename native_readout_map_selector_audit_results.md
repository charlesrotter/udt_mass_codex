# Native Readout-Map — the Target-Selector Audit (first test of the general readout-map problem)

**Date:** 2026-07-06 · **Driver:** Claude Opus 4.8 (1M) · **Mode:** MAP → OBSERVE (armchair / CAS-symbolic, DATA-BLIND, no compute solves). · **Frame:** C(a) isotropic round whole cell, no private seal, hopfion working hypothesis (n: cell→S², charge = Hopf Q_H ∈ π₃(S²)=ℤ).

## The question (pre-registered by Charles, 2026-07-06)

Framed as the **first test of the larger native readout-map problem**: *does UDT's own readout give the equal-thirds
share (q=1/3), or the summed scalar (Q=1)?* The no-selector theorem (`no_selector_audit_results.md`, verifier
ac28a9c57dcfd18be) had already reduced this to a single crisp test:

> **A selector must break target-SO(3)** — carry a genuine *target-space* index pointing at ONE internal channel. A
> source that is *scalar in target space* cannot select (dispositive). A source that breaks target-SO(3) only
> *spontaneously* (a FREE unpinned zero-mode) is spontaneous orientation, not selection (averaging restores the
> scalar). A selector counts ONLY if the target index is DERIVED and the axis PINNED. **Spatial** anisotropy ≠
> **target** anisotropy — a spatial axis is a selector only if spatial→target locking is derived AND the locked
> target axis is pinned.

**Rules honored:** no private seal/cell; no SM charge import; no hand-picked target axis; no "the torus picks an axis"
without derived+pinned spatial→target locking; scalar-in-target ⇒ cannot select; new term by hand ⇒ new physics.

**Pre-registered outcomes:** A = native selector derived (then compute if it forces q=1/3); B = no selector among the
named structures (bank: q=1/3 unforced under current action/readout); C = selector only by adding a new target-indexed
coupling (identify minimal form, mark not-native); D = need a broader readout-map program (open as next node).

## Result — OUTCOME B (primary), with C-form identified and a D-pointer

**No target-indexed selector is derivable from any of the four named native sources. q=1/3 remains UNFORCED under the
current UDT action + frame C(a); the native public charge readout is the summed scalar Q=1.** The negative is
**solve-independent** (a pure symmetry fact, below). This EXTENDS the no-selector theorem from "no selector under the
current action" to "no selector obtainable from any of the four candidate native sources, and no solve of the current
action+frame can produce one."

### The five audit nodes (each armchair + own CAS check; each cites blind-verified priors)

| Source | Verdict | Why (target character) |
|---|---|---|
| **Seal / involution** | B — target-scalar | Every seal op (σ_φ depth mirror φ→−φ; t→−t temporal mirror; JC1/JC2) lives on spacetime/depth/time/metric slots. The one target-touching op (χ→−χ on the spinning phase; equivalently the antipode n→−n) is a *uniform* reflection that fixes only the free n_∞ zero-mode and leaves all three shares ⟨n_a n_b⟩=δ_ab/3 **equal** (CAS-exact). No target index → no selector. |
| **Time-live / spinning** | B — spontaneous-only (+ requires-external-ℏ) | The rotor generator J_n(v)=n×v IS a target vector, but its axis is the FREE orientation zero-mode (equivariance-locked to the unpinned n_∞). The native time-live action is a 2nd-order rigid rotor ½Iθ̇² with **no** 1st-order Berry/WZ term (a 1st-order term would be t→−t-odd, seal-forbidden; the only continuous θ-term ∫F∧F≡0 on S²). Any discretization rides an **imported ℏ** (postulate A) and even then quantizes the *projection magnitude*, never *pins the axis*. |
| **φ-angular coupling** (Charles's prime suspect) | B — spatial-angular, not target-angular | Native matter is φ-**blind** (δS_m/δφ=0; the e^{2φ}·L_m coupling is non-native, drove the basin-A runaway). The ONE native φ-angular coupling — Branch P, `Z_φ(r²φ')' = 4e^{-2φ}` — is **spatial**-angular: the chain n→T_μν→h_AB→𝒦→φ is target-blind at every arrow after n. A metric function is a *spacetime* object and **structurally cannot** carry a target index. |
| **Whole-cell flux / read-surface** | B — target-scalar (single-axis projector needs a hand-picked axis) | Enumerated native read-surface observables (CAS): dilation flux Π_φ is target-**blind**; degree & Hopf Q_H are target-**scalars** (=1); vector moments ∮n_a =0; 2-tensors ∮n_a n_b ∝ δ_ab (isotropic, traceless part 0). The read-surface supplies only a **spatial** normal ê_r, never a target ê_a. A 1/3-projector ∮n_a²ω_H1 must hand-pick a → new physics. *(The vanishing vector moment / isotropic 2-tensor are symmetry COROLLARIES of the unbroken target-SO(3), i.e. consistency, not a second independent leg — the independent content is that no native ê_a exists to project against.)* |
| **Spatial→target locking (cross-cutting crux)** | B — spontaneous orientation, **solve-independent** | Equivariance (diagonal SO(2)) locks the spatial torus axis to n_∞ — but as a **RELATIVE** lock (rotate space *and* target together), CAS-exact, and only *given* axial symmetry (which is seed-suggested + numerically consistent, **not** derived-unique). The locked target axis n_∞ is a **FREE zero-mode**: on the isotropic cell energy depends on space only through rotation-scalars, so the whole orientation-S² is degenerate. **Global target-SO(3) (target rotated, space fixed) stays an exact symmetry of the *backreacted* functional** (source T_μν[n] is target-scalar). ⇒ a spatial-axis pin **never transmits** to a target-axis pin. |

### The load-bearing synthesis (why this is solve-independent, not gated)

The spin and flux nodes each flagged one possible overturn: *could the gated non-perturbative whole-cell solve (N5d)
energetically pin the spatial torus axis, and thereby (via equivariance) pin n_∞?* The crux node closes it by a pure
symmetry argument:

1. The equivariance lock is **relative** (the unbroken diagonal SO(2) = simultaneous space+target rotation), NOT an
   absolute spatial↔target identification.
2. The full **backreacted** energy functional (n, h_AB, φ all on) is still **target-SO(3)-invariant**, because the
   backreaction is sourced by the target-scalar stress T_μν[n] (CAS T4: L2 and L4 Skyrme stress both target-invariant)
   — h_AB and φ carry no target index; h_AB T^AB is target-scalar; the loop generates no target-indexed coupling.
3. Therefore **global target rotation (space fixed) is a flat zero-mode direction regardless of any spatial pinning.**
   Pinning a *spatial* axis (breaking spatial SO(3)) does NOT pin the *target* axis.

⇒ The N5d solve would refine the *locking structure* (settle axial-vs-generic minimizer) but **cannot change the pin
verdict**: axial ⇒ relative lock but the pair co-rotates freely; generic ⇒ no lock but the whole config's global
target orientation is still a zero-mode. **In neither case is anything pinned.** The verdict needs no PDE solve.

### C-form (identified, marked NOT native)

A selector is possible **only** by adding a natively-*derived* target-SO(3)-breaking coupling. The three minimal forms
(named by the theorem, confirmed here to be absent from all four native sources):
- a **target-space anisotropy V_ab** in the action (absent: L2+L4 are manifestly target-SO(3)-invariant, CAS T2);
- a **target-charged background** that couples to one n_a (absent: frame C(a) is target-blind; the seal/flux are target-scalar);
- a **native single-axis projector** in the readout (absent: every native read-surface observable is a target-scalar; a projector must hand-pick ê_a).
None is supplied by seal, spin, φ-angular, or flux under the current action+frame. **Adding one by hand = new physics
(outcome C), not a derivation.**

### D-pointer (the general readout-map problem, reframed — for Charles)

Framing this as the first test of the general **native readout-map** problem paid off: the audit shows the problem
**splits into two orthogonal threads**, and this audit closes only the first:
- **(i) target-channel selection** (which internal channel is public) — **CLOSED here as B / new-physics**: solve-independent, needs a derived target-SO(3)-breaking coupling.
- **(ii) depth/size discreteness** (which *magnitudes* are public) — **still ALIVE**: the φ-angular hunch survives here. Branch P's `Z_φ(r²φ')'=4e^{-2φ}` is the hunch emerging natively, is intrinsically finite-domain (no asymptotic vacuum), and the D2b flux LADDER quantizes DEPTH/PROFILE. This is a *distinct* readout-map node (magnitude, not channel) and is NOT touched by this audit's negative.

So the honest "broader program" is not "we are stuck" but "the readout-map's *target-channel* axis is closed; its live
axis is *depth/size*." Whether to open (ii) as the next formal node is Charles's call.

## Provenance ledger (load-bearing objects)

- FS L2+L4 native action, target-SO(3)-invariant — DERIVED (F2; CAS T2 exact).
- Frame C(a) isotropic whole cell, no private seal — THEORY (no-selector audit; native field eqs).
- Equal-thirds ⟨n_a n_b⟩=δ_ab/3 = per-axis winding, frame-invariant topological invariant — DERIVED (`d1_charge_channel_projection_MAP.md`).
- Equivariance = **relative** diagonal-SO(2) lock; n_∞ = **FREE** zero-mode — DERIVED (CAS T1/T1b, exact).
- Backreaction source T_μν[n] target-scalar ⇒ backreacted functional target-SO(3)-invariant — DERIVED (CAS T4).
- Matter φ-blind (δS_m/δφ=0); e^{2φ}·L_m non-native — DERIVED (`native_field_equations_constrained_two_player_results.md` §4, blind-verified ab54541f21112469b) — conditional on the R1+P5 shift levers (tagged CHOSE upstream).
- Branch-P φ-angular coupling `Z_φ(r²φ')'=4e^{-2φ}` is SPATIAL-angular via n→h_AB→𝒦→φ — DERIVED (native_field_eqs §6, CAS).
- Native time-live action = 2nd-order rotor, no Berry/WZ; ℏ not derived — DERIVED (`i_flow_hbar_clock_MAP.md`, Outcome 7).
- n_∞ = [0,0,−1] in the solver — CHOSE (category-A numerical Dirichlet gauge-fix; NOT a native pin).
- ℏ / quantization-as-a-rule — IMPORT (postulate A); flagged, not used to derive.
- Axial symmetry of the Q_H=1 minimizer — CHOSE (toroidal seed) + numerically consistent, NOT derived-unique.

## Scope / caveats

- Negative is **scoped** to frame C(a) + the current FS L2+L4 action + the hopfion working hypothesis. Overturnable
  ONLY by a natively-derived target-SO(3)-breaking coupling (= new physics, outcome C). Registry: this SHARPENS the
  no-selector theorem (adds solve-independence + the four-source coverage), does not overturn any banked negative.
- q=1/3 and η=1/18 remain OWED, import-dependent targets. This audit does not rescue them cosmetically — it bounds
  where a native rescue could come from (nowhere in the four named sources).
- The depth/size discreteness thread (Branch P) is UNTOUCHED and remains a live lead.

## Verifier

**Blind adversarial pass — VERIFIED (verifier aa75efc94282e7099, Claude Opus 4.8 (1M), fresh zero-context,
2026-07-06).** Independently re-derived the load-bearing claim: generic-R∈SO(3) invariance of the FS stress —
**L2 (all four ∂_μn·∂_νn contractions), L4 Faddeev n·(∂n×∂n), and L4 Skyrme |∂n×∂n|² all `diff=0`** (uses
Ra×Rb=det(R)R(a×b)=R(a×b) for det=1). ⇒ the FULL backreacted functional is exactly target-SO(3)-invariant; the loop
h^AB T_AB[n] generates no free target index at any order; a spatial-axis pin never transmits to a target pin.
**Outcome B is NOT gated on N5d** (the solve can only settle axial-vs-generic minimizer SHAPE, never pin an
orientation). Attacked all three break-vectors (2nd-order h_AB feedback, spatial-pin transmission, hidden-BC pin) —
none breaks it. Extra check: the Hopf/Whitehead θ-term is also target-SO(3)-invariant (SO(3) connected ⇒ preserves
Hopf class), so the spin sector supplies no target index either. No smuggle found in any of the 5 nodes; C-form
enumeration complete (rank-1 + rank-2 fixed target tensors exhaust the generating set; no 4th form, no 5th native
source in single-cell C(a)); D-split honest and orthogonal. Load-bearing claim rests ONLY on the exact target-SO(3)
invariance of a target-scalar action — derivation-grade, does NOT ride any CHOSE/IMPORT lever (in particular it is
insulated from the upstream R1+P5 "matter φ-blind" CHOSE: even a non-native e^{2φ}L_m coupling is target-scalar).
Verifier note (folded in): the argument is in fact STRONGER than stated — it holds for ANY matter action whose
n-dependence is target-scalar. Recommendation: bank as-is. Classification: CONSISTENCY / PROVEN-to-symmetry within
frame C(a)+FS action, overturnable only by a natively-derived target anisotropy (= outcome C).
