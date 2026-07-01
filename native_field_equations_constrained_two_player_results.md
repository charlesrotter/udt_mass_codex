# Native UDT Field Equations — the Constrained-Two-Player Frame (G/P regimes)

**Date:** 2026-07-01. **Provenance:** derivation by Charles (2026-07-01, in-session); every
load-bearing algebraic claim CAS-verified by the driver (sympy, `verify_native_fieldeq.py`, all
checks TRUE); blind-adversarial verifier pass recorded below. **Status:** DERIVED skeleton +
verified; the G↔P *switch criterion* is the open target. NOT yet canon (Charles canonizes).

This doc fills the acknowledged "KEY SILENCE" (relativistic_metric_rederivation: R1–R3 pin only the
metric FORM, nothing about the field equations). It supersedes the live two-player scalar-tensor
frame (φ outside g) as the NATIVE frame — see "Implications."

---

## 0. The pivotal structural fact (why the project was stuck)

For the canonical UDT metric, the Einstein–Hilbert action `√-g·R` is a **pure boundary term** on the
reciprocal (B=1/A) family:

    r²R = d/dr[ 2r(1-e^{-2φ}) + 2r²e^{-2φ}φ' ]        (CAS-verified)

So **bare EH has ZERO bulk content for UDT** — it yields no interior equation for φ. "Vacuum = GR"
was never a result; it was the emptiness of EH-on-this-family showing through (the Principle-7 scar).
The native bulk dynamics for φ must come from elsewhere; identifying that source IS the field-equation
question.

---

## 1. Canonical metric, measure, native operator

    ds² = -e^{-2φ(r)}c²dt² + e^{2φ(r)}dr² + r²dΩ²
    √-g = c r² sinθ                        (φ-FREE — dilation factors cancel under B=1/A)
    □_g φ = (1/r²) d/dr( r² e^{-2φ} φ' )    (exact nonlinear operator; CAS-verified)

R (from scratch, CAS-verified):
    R = e^{-2φ}(-4φ'² + 2φ'' + 8φ'/r) + 2/r² - 2e^{-2φ}/r²

---

## 2. Probe vs self-consistent — RESOLVED by the R1 weight

The R1 shift-invariant kinetic density is `√-g · e^{2φ} g^{rr} φ'²`. Since `√-g` is φ-free and
`e^{2φ}g^{rr}=e^{2φ}·e^{-2φ}=1`, this density = `c r² sinθ · φ'²` — it has **no explicit φ, only φ'**.
Therefore probe (g fixed) and self-consistent (φ IS the metric) variation COINCIDE:

    δ[ ∫ r² φ'² ] = 0   ⇒   (r² φ')' = 0                (CAS-verified)

(The "extra `e^{-2φ}φ'²` term" that distinguishes probe from self-consistent appears ONLY with the
UNWEIGHTED kinetic `g^{rr}φ'²`; the R1 weight removes the ambiguity. The two weightings give DIFFERENT
vacua — see §3 — so the weight is physically consequential, not cosmetic.)

---

## 3. Vacuum solution — escapes GR collapse (CAS-verified)

R1-weighted (principled):     (r²φ')'=0  ⇒  φ = φ_∞ - q/r  ⇒  g_tt = -e^{-2φ_∞+2q/r}
Unweighted self-consistent:   □φ+e^{-2φ}φ'²=0  ⇒  e^{-φ}=C₀+C₁/r  ⇒  g_tt = -(C₀+C₁/r)²

Both are **NOT Schwarzschild** `-(1-2M/r)` (exponential / squared lapse, not rational). The naive
"one-player ⇒ GR collapse" claim is FALSE once the bulk action is the shift-invariant kinetic rather
than the empty EH R-term.

**NONLINEAR-ESCAPE caveat (blind-verifier, Principle-2 relevant):** `g_tt=-e^{-2φ_∞+2q/r}` MATCHES
Schwarzschild to FIRST order (`M=-q`); the two differ ONLY at `O(1/r²)` and beyond (`+2q²` etc.). So the
departure from GR is entirely NONLINEAR — good (weak-field automatically GR/Newton-like, solar-system-safe)
AND a Principle-2 flag: the departure is INVISIBLE under linearization, so it must never be linearized away.

---

## 4. Channel-corrected matter is φ-BLIND (directly)

The native S² field matter L2 = -(ξ/2)g^{mn}G_mn, L4 = -(κ/4)g^{mp}g^{nq}(G_mp G_nq - G_mq G_np),
G_mn = ∂_m n·∂_n n. Shift-invariance forces the matter to couple to the UNDILATED (bare) inverse metric
channels (per-channel weights e^0/e^{2φ}/e^{4φ} ≡ replace g^{mn}→ḡ^{mn}; CAS-verified channel ledger).
Consequently, in the constrained-static frame the matter action carries NO explicit φ:

    δS_m[ḡ^{-1}, n] / δφ = 0

**Matter does NOT directly source φ.** (This is why the live `e^{2φ}·L_m` / `e^{2φ}T` coupling drove
the spurious "dilaton runaway basin A" — that coupling is NOT native.) Native matter instead sources φ
INDIRECTLY, through the geometry:   n → h_AB → K → φ   (only in Branch P; see §6).
[Premise: rides the R1+P5 shift-derivation levers, both tagged CHOSE upstream.]

---

## 5. The constrained-two-player metric + action

φ is NOT an independent scalar riding outside g (the live frame), NOR fully slaving g. It is the
LONGITUDINAL dilation field; the TRANSVERSE 2-geometry h_AB is independent:

    ds² = -e^{-2φ}c²dt² + e^{2φ}dr² + h_AB(r,θ,ψ) dx^A dx^B ,   A,B ∈ {θ,ψ}
    √-g = c √h                              (φ-free; CAS-verified)

Transverse extrinsic curvature (normal n^i = e^{-φ}∂_r):
    K_AB = ½ e^{-φ} ∂_r h_AB ,   𝒦 := K_AB K^AB - K²
For h_AB = r²Ω_AB:  K = 2e^{-φ}/r,  𝒦 = -2e^{-2φ}/r²    (CAS-verified)

Shared forced skeleton:
    S = ∫ c√h [ (Z_φ/2)φ'² + R^{(2)}[h] + 𝒦_branch + L_m^UDT ]

with the FORK in 𝒦_branch (𝒦 carries shift-weight -2, so it must be compensated by e^{2φ} to preserve
R1, or left uncompensated to break it):

---

## 6. The G/P FORK — two REGIMES, not a global choice (Charles 2026-07-01)

**Branch G — strict depth-gauge, CONTINUUM EXTERIOR.** Global φ→φ+λ is an EXACT symmetry; compensate
𝒦 by e^{2φ} (`𝒦_G = e^{2φ}𝒦 = ¼ 𝒢^{ABCD}h'_AB h'_CD`, φ-free). φ decouples from h_AB in the bulk:

    (r²φ')' = 0   ⇒   φ = φ_∞ - q/r         [scale-free, asymptotically flat, Coulomb-like]

Clean but structureless — no preferred scale except boundary data. The natural branch for continuum
exterior / asymptotic vacuum.

**Branch P — angular scale PHYSICAL, FINITE-CELL / MICROPHYSICS.** The sphere's transverse size is
physical, so the angular sector BREAKS the depth-shift (𝒦 left uncompensated). φ sourced by angular
curvature (CAS-verified, for h_AB=r²Ω):

    Z_φ (r²φ')' - 4e^{-2φ} = 0        i.e.   Z_φ(r²φ')' = 4e^{-2φ}

This IS the native φ-angular coupling (the standing discreteness hunch, emerging not posited).
**DISCRIMINATOR (load-bearing):** P has NO asymptotically-constant vacuum — as r→∞ with φ→φ_∞,φ'→0,
the LHS→0 but RHS→4e^{-2φ_∞}≠0 (contradiction). So **P is intrinsically FINITE-DOMAIN.** This maps P
to the finite-cell regime and G to the continuum-exterior regime:
**SCOPING (blind-verifier — must travel with the discriminator):** claims 8–9 assume (a) `h_AB=r²Ω`
held FIXED (not co-varied), (b) `𝒦` UNcompensated, (c) `Z` constant. The no-vacuum contradiction is
driven by the uncompensated `-2e^{-2φ}/r²` source surviving as r→∞; for GENERAL transverse `h_AB` (or
if `h_AB` co-varies / `𝒦` is compensated) the RHS need not be a fixed positive constant and the
contradiction need not hold. Directly relevant to the switch-criterion derivation, where `h_AB` may vary.

    continuum exterior / asymptotic vacuum   →  Branch G
    finite cell / microphysical angular      →  Branch P
    transition/boundary between them         →  a MATCHING problem

**The next derivation target is NOT "G or P?" but the SWITCH CRITERION:**
> Branch P is admissible only if FINITE ANGULAR GEOMETRY breaks the global depth-shift symmetry.
Candidate switches (to prove/falsify): (1) finite angular-cell boundary; (2) nontrivial topology of
n:S²→S²; (3) a transverse curvature invariant that cannot be gauged away; (4) a BC fixing angular size
so the global φ-shift is no longer a redundancy.

---

## 7. Premise ledger (chose/derived)

| ingredient | status |
|---|---|
| EH `√-g R` = boundary term on canonical family | DERIVED (CAS) |
| native operator □_g φ; √-g φ-free | DERIVED (CAS) |
| R1 weight ⇒ kinetic density φ-free ⇒ probe=self-consistent | DERIVED (CAS) |
| vacuum φ=φ_∞-q/r (weighted); escapes Schwarzschild | DERIVED (CAS) |
| matter φ-blind (δS_m/δφ=0) | DERIVED **conditional on R1+P5 (CHOSE) shift levers** |
| constrained metric FORM (φ longitudinal, h_AB transverse) | **CHOSE** (natural ADM split, not yet forced) |
| Branch G equation (r²φ')'=0 | DERIVED given G (strict R1) |
| Branch P equation Z(r²φ')'=4e^{-2φ}; no asymptotic vacuum | DERIVED given P; **P breaks R1 in the angular sector** |
| G/P switch criterion | **OPEN — next derivation target** |

---

## 8. Implications for the recent program

- **The basin saga is explained + retired.** A's "dilaton runaway" was driven by `e^{2φ}T`, a
  NON-native coupling; native matter is φ-blind. The X-kluge → e^{2φ}-weight → frame audit chain was
  chasing a real artifact. The whole classify-only basin picture is superseded by this frame result.
- **The live solver is the WRONG frame.** It uses φ-outside-g scalar-tensor (independent warps + a
  separate φ). Native UDT is constrained-two-player (φ = longitudinal dilation IN the metric, h_AB
  transverse). A new solver in this frame is the eventual target — NOT yet (record + switch-criterion first).
- **Matter's role clarified:** matter shapes h_AB / topology / boundary, and (only in P) sources φ
  through 𝒦. The clean chain n→h_AB→𝒦→φ replaces the artifact n→e^{2φ}T→φ.

---

## 9. VERIFIER

- **CAS (driver, 2026-07-01, `verify_native_fieldeq.py`):** all 6 load-bearing claims TRUE — √-g φ-free;
  □_g φ operator; R identity; EH boundary identity; R1-weighted density φ-free + (r²φ')'=0 + φ=φ_∞-q/r
  non-Schwarzschild; unweighted e^{-φ}=C₀+C₁/r; constrained 𝒦=-2e^{-2φ}/r²; Branch P equation.
- **Blind-adversarial (agent `ab54541f21112469b`, 2026-07-01, independent from-scratch sympy — built the
  metric + Christoffels/Ricci itself, did not use the driver's algebra):** ALL 9 load-bearing claims
  **CONFIRMED**. No substantive errors. Three honest caveats folded in above: (i) the GR-escape is NONLINEAR
  (g_tt matches Schwarzschild to O(1/r), M=-q; departs at O(1/r²) — Principle-2 flag); (ii) Branch P's EL
  comes out as the overall-negative of the stated form (EOM identical, sign convention only); (iii) claims
  8–9 (P finite-domain) are SCOPED to h=r²Ω / fixed-transverse / uncompensated-𝒦 — general h may differ.

## 10. OPEN (next)
Derive the G↔P **switch criterion** (the domain condition under which finite angular geometry breaks the
depth-shift). Prove or falsify: "P admissible only if finite angular geometry breaks global depth-shift."
Then (later) the G↔P matching problem, and a constrained-two-player solver.
