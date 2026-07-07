# DERIVATION — the UDT "dilation boost" from invariance of a maximum distance `x_max`

**Date:** 2026-07-07 (PM) · **Mode:** DERIVE (gated go given by Charles) · **Author:** Claude Opus 4.8 (1M).
**Status: PROVISIONAL — the FORM is derived + CAS-verified; the VALUE of `x_max` is NOT fixed (as in SR); the
"invariance forces the whole metric" claim is SUPPORTED-given-the-canon-skeleton, not fully closed.** Frame:
`udt_max_distance_invariance_FRAME.md`. Generator/CAS: `derive_xmax_boost.py`. No SM import, no `ℏ`; mass never appears.

## What was attempted
The native analog of the von-Ignatowsky derivation of the Lorentz transformation (which forces SR from: relativity
principle + homogeneity + isotropy + group closure, producing an invariant SPEED `c`). Here: **positional relativity
(no preferred position) + isotropy + linearity/group closure + a finite invariant maximum DISTANCE `x_max`** — read off
what it forces. OBSERVE, not impose.

## What is DERIVED (each step CAS-verified in `derive_xmax_boost.py`)
1. **The composition law is forced.** Successive radial displacements compose by the unique **fractional-linear**
   isotropic, associative group law with a finite invariant fixed point `X≡x_max` — it is **LINEARITY** of the
   position-frame map (an assumed input, per the ledger) that pins the Möbius/rational form; associativity +
   fixed-point + isotropy ALONE admit other conjugate-to-addition laws (verifier counterexample `g(x)=x/(X²−x²)`),
   so "forced" means "given linearity + the finite-`x_max` postulate":
   `x₁ ⊕ x₂ = (x₁+x₂)/(1 + x₁x₂/x_max²)`  — commutative, identity 0, associative, has inverses, and `x ⊕ x_max = x_max`
   (nothing exceeds `x_max`); as `x_max→∞` it reduces to naive addition `x₁+x₂` (the Galilean branch). [CAS: all True]
2. **The additive coordinate — the dilation depth `φ` — linearizes it.** `φ(x) = arctanh(x/x_max)` gives
   `φ(x₁⊕x₂) = φ(x₁)+φ(x₂)` — **dilation depths ADD** (the "rapidity" of position). [CAS: tanh-addition identity True]
3. **Physical distance SATURATES:** `x = x_max·tanh(φ)`; `φ:0→∞` maps `x:0→x_max` asymptotically; `dx/dφ→0` at the edge.
4. **The redshift–distance law falls out.** With the canon relation `1+z = e^{φ}` and the derived `φ(x)=arctanh(x/x_max)`:
   `1+z = √[(x_max+x)/(x_max−x)]` — **the relativistic-Doppler form with `β = x/x_max`.** [CAS: derivative test True;
   numeric 4.4e-16] Consequences:
   - `x→x_max`: `1+z→∞` — infinite redshift, time stops, mass diverges (the one saturation, two faces).
   - small `x`: `1+z ≈ 1 + x/x_max` — a **linear redshift–distance law with slope `1/x_max`**. (The slope's inverse is
     the length scale `x_max` itself; earlier drafts named it `c/H₀`/"Hubble length" — STRUCK as a ΛCDM import
     (Charles 2026-07-07). The derivation delivers only the slope `1/x_max`; `x_max` is a free invariant, not a
     cosmological observable.)
5. **Metric consequence (the CHECK target).** With the canon skeleton `ds² = −A c²dt² + A⁻¹dx² + …` (B=1/A, canon
   C-2026-06-14-1) and gravitational redshift `1+z = 1/√A`: `A(x) = 1/(1+z)² = (x_max−x)/(x_max+x)`, so **`A→0` at
   `x=x_max`** — an asymptotic horizon (`g_tt→0` = time stops), the de Sitter-like edge derived rather than installed.

## Premise ledger (scrupulous — this is foundational)
- **POSTULATED (the new physics):** that a *finite* invariant `x_max` exists at all. The von-Ignatowsky structure
  forces EITHER Galilean (`x_max=∞`, naive addition) OR this Lorentzian form (finite `x_max`); choosing finite `x_max`
  IS the postulate, exactly as choosing finite `c` over Galilean-∞ is SR's light postulate. Justified by the resulting
  structure + the canon match, not by a prior derivation. Tagged AS a postulate.
- **ASSUMED (inputs, canon):** linearity+isotropy+group of the position-frame map; the canon redshift `1+z=e^{φ}`; the
  canon metric skeleton `B=1/A` + gravitational redshift `1+z=1/√A` (used only in Step 5).
- **DERIVED:** the composition law, `φ(x)=arctanh(x/x_max)`, the saturation, the redshift–distance law, `A(x)`, the
  horizon at `x_max`. All CAS-verified.
- **OPEN / NOT delivered:**
  1. **The VALUE of `x_max` is NOT fixed by the form — and CANNOT be a function of `c,G` (or `c`) alone** (Charles
     2026-07-07). Two reasons, both import-free: (i) UNITS — `c` is distance/time and `G` still carries a mass, so no
     combination yields a pure length (`c` alone needs a time; `c,G` need a mass); this is dimensional homogeneity, NOT
     the smuggled Planck/`ℏ` objection. (ii) SCALE-FREEDOM — UDT's vacuum is scale-free (canon: matter is the
     scale-breaker), so its own closure fixes the SHAPE not the RULER: the marginal edge `x_max=2GM/c²` with the
     metric's own curvature energy `M~(c²/G)x_max` makes `x_max` CANCEL (scale-invariant). ⇒ **`x_max` is a FUNDAMENTAL
     INVARIANT in its own right — a max LENGTH as primitive as `c` is a max SPEED — set/measured, not derived** (you
     don't derive `c` from `G` either). This is the same fact as "UDT predicts RATIOS, not absolute scales": `x_max` IS
     the ruler. [A natural TIME or MASS from the theory could convert it; the vacuum supplies neither.]
  2. **The load-bearing claim "invariance FORCES the metric" is SUPPORTED, not CLOSED.** Step 5 derives `A(x)` FROM the
     invariance GIVEN the canon `B=1/A` skeleton — it does not yet DERIVE that skeleton from the invariance. Closing it
     = showing invariance forces `B=1/A` + the rest, not just `A(x)`.
- **TRIPWIRE honored:** nothing imposed (the composition law + `φ(x)` are forced/derived, not guessed); `x_max` left
  free (NOT data-targeted to 1101 — data-blind); the redshift-distance law is REPORTED as a prediction, not fit.

## The checkable next step (OBSERVE, no fit)
Does our ACTUAL native metric `A(x)` (from the field equations) match `(x_max−x)/(x_max+x)` — i.e., does it have a
horizon (`A→0`) at a finite `x_max`? If yes, the invariance is already living in the metric we derived (the frame
confirmed, `x_max` sitting in the signature beside `c`). If the native `A(x)` has a DIFFERENT edge structure, that
adjudicates the postulate. The check is on the STRUCTURE (is there a finite edge at all), independent of `x_max`'s
value — which is the free ruler, not a `c,G` output. Also open: the full metric-forcing (Step 5 closes `A(x)` given the
`B=1/A` skeleton, not the skeleton itself).

## VERIFIER
**Blind adversarial pass — 2026-07-07, agent `a1473cf2856c41237`. PASS (sound-but-modest, as the doc states); one
wording overclaim fixed (Step 1, now folded in above).** Ran `derive_xmax_boost.py` unmodified — all 10 CAS checks
reproduce True. Independent re-derivation (NOT importing the script): composition law commutative/associative/`x⊕X=X`
exactly/Galilean limit — all confirmed; arctanh-linearization `atanh((u₁+u₂)/(1+u₁u₂))=atanh u₁+atanh u₂` max err 7e-15
over 2000 pts; `e^{arctanh u}=√((1+u)/(1−u))` max err 3.6e-15 (the doc's derivative-test/4.4e-16 claim honest);
small-x `1+z=1+x/X+x²/(2X²)+…` ⇒ `x_max=c/H₀` correct; Step-5 `A=(X−x)/(X+x)`, horizon at `x=X` confirmed. Verdicts:
(1) algebra CONFIRMED (no error); (2) "forced" HONEST — finite-`x_max` correctly tagged a POSTULATE with the Galilean
alternative stated, SR-light-postulate analogy fair; (3) **uniqueness was a MILD WORDING OVERCLAIM** — associativity+
fixed-point+isotropy alone don't pin the Möbius form (explicit counterexample `g(x)=x/(X²−x²)`); LINEARITY (already in
the ledger) does — **FIXED above**; (4) NON-CIRCULAR + honestly labeled (`1+z=e^φ` and the `B=1/A` skeleton tagged
ASSUMED; Step 5 SUPPORTS-not-CLOSES stated); (5) value of `x_max` HONEST/self-correcting (form doesn't fix it; `c/H₀`
needs a rate; frame's `c,G`-alone hope explicitly corrected); (6) DATA-BLIND confirmed (`x_max` symbolic, not fitted to
1101; mass never appears). **Net: the FORM is correctly derived + CAS-verified; the two OPEN items (VALUE of `x_max`;
full metric-forcing) are honestly flagged; no data-targeting, not circular.**
