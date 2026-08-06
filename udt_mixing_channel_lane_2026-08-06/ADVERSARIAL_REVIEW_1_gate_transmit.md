# Adversarial Review 1 — the GAUGE GATE and the TRANSMIT

Reviewer pass: independent sympy reconstruction, NO probe code imported. Date 2026-08-06, branch grok.
Target: `MAP_AND_PREREG.md` + `DERIVATION_NOTES.md`. Scripts (scratchpad, uncommitted):
`rev1_gate.py`, `rev1_gauge2.py`, `rev1_transmit2.py`, `rev1_cobound.py`.

## VERDICT (one line)
**NARROW.** GATE holds — `mu` is a genuine NON-GAUGE invariant of O(1,2). TRANSMIT does NOT hold as a
depth-law route: the O(t²) φ-dependence is real at fixed observer field `k` but is fully absorbable by
`k` for ANY φ, and the consistent mixing is forced into COBOUNDARY (pure-gauge-orbit) form. The
"angular constraint reaches the depth" claim is a **coboundary / free-field artifact**; only the bare
kinematic coupling survives.

## 1. THE GAUGE GATE — CONFIRMED NON-GAUGE (I tried hard to kill it; it survives)

Independent build of `C_A = eta^{-1}A^T eta · A` reproduces the probe exactly:
- `Trace = r²+1/r²+s²−mu²`, `Inv2 = 1+r²s²+s²/r²−mu²r²`, `Det = s²`. `mu` sits in the char-poly
  COEFFICIENTS (trace, Inv2), hence in the EIGENVALUES — not merely eigenvectors.
- **`lambda_time · lambda_radial = 1` iff `mu = 0`**: `solve(lambda_time·r² − 1, mu)` returns **exactly
  `mu = 0`**. This is a TRUE frame-invariant statement (both factors are eigenvalues = O(1,2)-invariant).
  Confirmed real invariant. `mu²` is recoverable from the spectrum alone (trace,Inv2,det → r²,s²,mu²).

**Full endpoint-frame attack (beyond the probe's single boost).** I built the general O(1,2) element
= boost(0-1)·boost(0-2)·rot(1-2)·**null-rotation** (the parabolic/unipotent generator), independent
`L_p` and `L_q`, exact-rational instances, and proved the identity
`Adag(L_q A L_p^{-1})(L_q A L_p^{-1}) = L_p C_A L_p^{-1}` for **every** eta-orthogonal pair
(4/4 trials, char-poly == baseline). Conjugation ⇒ spectrum fixed ⇒ **no O(1,2) frame pair removes
`mu`**, including null rotations and screen-slot rotations the probe never tried.
- The ONLY removal is a **non-eta-orthogonal** move (screen dilation `diag(1,1,d)` changes the spectrum
  but still keeps `mu`; a GL right-shear `A·[[1,0,−mu·r],…]` zeroes the (0,2) entry but is NOT
  eta-orthogonal). These change the metric READING, not an orthonormal frame — illegitimate.

**Gate scope (the honest condition):** NON-GAUGE is conditional on the endpoint group being the metric
isometry group O(1,2) (orthonormal/tetrad frames). That IS the physically correct choice (s = R-ratio
is physical data, absorbed in the tetrad). Verdict: **NOT MIX-GAUGE.** Gate is solid.

## 2. THE TRANSMIT — reproduced, then UNDERCUT (this is where the owner-favorable read fails)

**Reproduction (with a correction).** The timelike depth must be read off the eigenvalue branch
CONTINUOUS to `a²` at `m=0`. The probe's `(Tb−√…)/2` "−" root actually returns `min(a²,s²)` — the
SCREEN eigenvalue when `s<a` — which gives a spurious nonzero O(t⁰). Pinning the correct branch
perturbatively: leg depth `= −log a + m²/(2(a²−s²)) + O(m⁴)`. Then, with the forced coboundary mixing
`m(x,y)=t·(a·k_y − s·k_x)` around triangle P→Q→R→P:
`O(t⁰)=0`, `O(t¹)=0`, `O(t²)≠0` with `∂/∂φ_P ≠ 0` — **the probe's claim reproduces.** Onset O(mu²).

**Why it does NOT transmit a constraint to the depth (three independent kills):**
1. **Absorbable by free `k` for ANY φ.** `solve(loop-O(t²)=0, k_P)` → **exactly 1 solution** for arbitrary
   φ,R,k_Q,k_R. The loop closes for EVERY depth profile by tuning the free observer field. φ is NOT
   pinned — no depth-law. (The probe's own caveat, here promoted to the verdict.)
2. **The consistent mixing is a COBOUNDARY.** Constant `mu` is inconsistent (needs a+s=1); the only
   consistent form is `m = a·k_y − s·k_x`, verified to satisfy the cocycle. A coboundary is the
   gauge-trivial class: it is exactly the orbit of `m=0` under node shears `U(k)=[[1,0,k],[0,1,0],[0,0,1]]`
   (`m → m + s·k_q − a·k_p`, verified). So the whole "transmitting" mixing field is the gauge orbit of
   zero mixing. The `k`-tuning in kill #1 IS moving inside that orbit.
3. **Closure is IMPOSED, not derived.** The eigenvalue-depth is an exact potential difference only at
   `m=0`; demanding it stay closed at `m≠0` is an unmotivated owner choice, not a consequence.

**Consistency note (not a contradiction):** #2's shear `U(k)` is NOT O(1,2) — so it cannot remove
single-arrow `mu` (gate stands), yet it trivializes the groupoid mixing FIELD, and #1 absorbs the loop
by tuning the physical field `k` (data, not a frame change) — so even holding the frame group at O(1,2),
φ stays free. The transmit collapses on every accounting.

**Q2 (quantization):** independently confirmed NO. Pure-mixing holonomy → elliptic rotation,
`cos θ = 1 − m0²/2`, continuous in `m0`. Nothing selects/quantizes `mu`.

## 3. What genuinely survives
Only the **kinematic** statement: the invariant timelike eigenvalue depends on `mu` and `s`
(level repulsion, coeff `1/(2(a²−s²))`, diverging at the a²=s² coalescence). That is "the coupling is
non-gauge and real" — NOT "an angular consistency constraint reaches the depth profile." The landed
class should be **COUPLING-INERT-toward-a-law / NARROW**, not COUPLING-TRANSMITS.

## Strongest single point
The O(t²) loop obstruction — the entire transmit claim — is generated inside the coboundary (pure-gauge)
orbit of zero mixing and is zeroed by tuning the free observer field `k` for ANY depth profile
(`solve → 1 solution`, exact). It therefore imposes NOTHING on φ. The coupling is non-gauge (gate real),
but the "law route to the depth" is a free-field/coboundary artifact.
