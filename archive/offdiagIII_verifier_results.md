# Off-Diagonal Angular Row III — BLIND ADVERSARIAL VERIFIER REPORT

Verifier: independent hostile blind verifier, agent id **vf-odiii-9f3c1a47**
(Claude Opus 4.8, 1M). Date: **2026-06-13**. Own machinery (own sympy 1.13.1
Christoffel/Ricci build; own torch float64 GPU reproduction). Log:
`/tmp/offdiagIII_verify.log`. Scripts: `/tmp/odiii_verify_A.py`,
`/tmp/odiii_verify_A3.py`, `/tmp/odiii_verify_A4.py`, `/tmp/odiii_verify_B.py`,
`/tmp/odiii_verify_D.py`. Append-only; new file (charter discipline).

Posture (per hypothesis discipline): I aimed HARDEST at FINDING a native
bounding term the challenger missed — because finding one FLIPS the verdict to
"the static class CAN host a finite shaped type," the most consequential
outcome and the one that would REOPEN the static class against the program's
standing anti-invention direction. I attacked the EH-tautology claim from
scratch (independent `√−g R`), the full axial sector, the #36 Stokes argument,
and the nonstationary handoff's well-posedness.

================================================================
## VERDICT: **CONFIRMED with a PARTIAL (kill-shot D) scope correction.**

NO native bounding term exists in the static single-cell C1 class. The STEP-3
"static class cannot host the completion" verdict STANDS and is in fact
**stronger** than the challenger argued (kill-shot A). But the **handoff is not
a clean cure** — the nonstationary route, taken as "add the wave term,"
RELOCATES the pathology into a Hadamard-ill-posed angular Cauchy problem; the
"flip region = medium edge, not a particle locus" reading is at least as
well-supported as the live-route reading (kill-shot D).

================================================================
## (A) IS THE FULL ACTION AT MOST 2ND-ORDER / FIRST-ORDER IN GRADIENTS? — CONFIRMED, and STRONGER.

**A1 (own machinery).** The dilation-kinetic + algebraic-ON density, built with
phi, q (=g_rθ), w (=sphere-shape) ALL carried as functions of (r,θ): max
derivative order = **1**, and `density.has(d q) = False`, `density.has(d w) =
False`. Only phi-gradients appear. The C1 EL is therefore at most 2nd-order;
NO native higher-derivative term. CONFIRMED.

**A2 — the decisive hostile probe (the EH-remainder the prompt demanded).** I
independently computed the Einstein–Hilbert scalar `√−g R` on the SAME
dilation-tie 4-metric (full Christoffel→Ricci→R, own sympy). It DOES carry
SECOND derivatives of q and w: `∂²_{rθ}q`, `∂²_θ w`, `∂²_{rθ}w` (and `∂²phi`).
So `√−g R` is NOT first-order — the challenger's flat phrasing "the density is
first-order" is true ONLY because **`√−g R` is NOT in the UDT action**. This is
the crux, so I pressed it three ways and the challenger SURVIVES on all three:

1. **Provenance.** UDT_REBUILD.md §1 is explicit: the action is the C1
   dilation-kinetic `S_φ = −(c/2)∫ e^{−2φ}(∂φ)²√−g` alone; the vacuum field
   equation `φ″+2φ′/r−2φ′²=0` derives from `S_φ`, NOT from `√−g R`. The metric
   IS phi; B=1/A forces `G^t_t=G^r_r` identically — the Einstein "source" is the
   tautological `G/8πG`, with no independent dynamical `√−g R` term. Admitting
   `√−g R` to mine its q,w 2nd-derivatives is the **forbidden import**
   (principle 1). This is the standing ruling (W1 registry #24 ERRATUM:
   "EH-import prohibition rests on principle-1 provenance"; and EH contributes
   ZERO to the P1 field equations on spherical configs).

2. **EVEN IF one illegitimately admitted `√−g R`, it does NOT bound the
   pathology** (my `odiii_verify_A4.py`, concrete background φ0=ar+b·cosθ). The
   second variation of `√−g R` in (δq,δw) has Euler–Lagrange principal symbols:
   - **EL_δw:** coeff[∂²_r] = `4 r² sinθ e^{−2φ0}` > 0 (a RADIAL stiffness);
     **coeff[∂²_θ] = 0**, coeff[∂²_{rθ}] = 0.
   - **EL_δq:** highest derivative order = **0** (the `∂²_{rθ}q` term in the
     density is a total derivative — it drops out of q's EL entirely).
   The pathology is a wrong-sign **angular** (∂²_θ) Laplacian (K_θ<0). The
   EH-remainder supplies **ZERO ∂²_θ structure on either off-diagonal field.**
   So even the forbidden import cannot bound the relevant direction. The
   challenger's verdict is thereby STRONGER than stated: not merely "EH is
   absent," but "EH, even if present, furnishes no angular bounding term."

3. **W1 reconciliation.** This settles the #21/#23–25 "forced w-stiffness /
   EH-remainder species" route in the NEGATIVE for the angular operator: the
   EH-remainder's only 2nd-order content on w is RADIAL (∂²_r), consistent with
   #23 ("C1 first-jet in g_tt only") and #24's erratum (EH zero on P1 spherical
   field equations). No native angular bounding term hides there.

================================================================
## (B) DO u,v / ANY THIRD COMPONENT CARRY KINETIC BOUNDING TERMS? — NO. CONFIRMED.

The challenger checked two "w"s (sphere-shape g_θθ, time-θ g_tθ). I extended to
the **full axial triple** — g_tφ=u, g_rφ=v1, g_θφ=v2 — added live to the
dilation-kinetic density (`odiii_verify_B.py`). Result: `density.has(d u) =
density.has(d v1) = density.has(d v2) = False`; max derivative order = 1
(phi-gradients only). The axial u,v are **purely ALGEBRAIC in statics**,
exactly as angular_completeness states ("no kinetic terms at any order"). Their
elimination at m≠0 IS the dpv flip — i.e. they are part of the **cause** of the
attractive flip (the reversed centrifugal `−f0·dpv²/sin²θ`), NOT a higher-
derivative cure. No third static off-diagonal component carries a kinetic
bounding term. CONFIRMED.

================================================================
## (C) IS #36 BULK-INVISIBLE? — CONFIRMED (with one honest nuance).

`d ln f ∧ ω_H1 = d[(ln f)ω_H1]` is EXACT ⇒ by Stokes it is a pure boundary
integral ⇒ ZERO contribution to the bulk EL ⇒ it cannot modify the bulk K_θ or
add a bulk higher-derivative term. #37 confirms it is σ-EVEN and EXACT
(dynamics-invisible because exact, not by parity). My own torch reproduction
confirms the numeric face: the maximal boundary term (Dirichlet, α=1e8) leaves
lam0(65,129,257) = [−484.7,−1940.0,−7761.2] **bit-identical** to α=0; the
divergence is driven by high-frequency INTERIOR modes that vanish at the
endpoints. A pure BC cannot bound a bulk wrong-sign Laplacian. CONFIRMED.

NUANCE (non-simply-connected route, the prompt's kill-shot C probe): #37 leaves
open a winding family (S²×S¹ ⇒ H²=ℤ, or L(p,q) ⇒ H²=ℤ/p) if the matter-cell
core seal is finite, which would make ω_H1 a NON-exact cohomology class. But
even then ω_H1 is a global, integer-valued (Euler/Chern) datum — NOT a local
bulk differential operator. A topology class cannot change the LOCAL principal
symbol K_θ. So bulk-invisibility for the **operator-boundedness** question holds
regardless of the closure topology. (The challenger did not flag this route
explicitly; the conclusion is unchanged, but the argument is now closed against
it.)

================================================================
## (D) IS THE HANDOFF A CURE OR RELOCATION? — RELOCATION (partial correction).

This is where I depart from the challenger's framing. The nonstationary route
(CANON C-2026-06-13-1) adds a 2nd-TIME-derivative wave term but **no new
spatial higher-derivative regularizer.** The would-be angular wave has
dispersion ω² = K_r k_r² + K_θ k_θ². Where the flip lives, K_θ<0, so
(`odiii_verify_D.py`):
  K_θ=−0.274: k_θ=100 → ω²=−2740 → growth rate 52/t.
  K_θ=−2.03 : k_θ=100 → ω²=−20300 → growth rate 142/t.
  K_θ=−303  : k_θ=100 → ω²=−3.0e6 → growth rate 1741/t.
ω is imaginary; growth rate ~ √|K_θ|·k_θ → +∞ as k_θ→∞. **The angular Cauchy
problem is HADAMARD ILL-POSED wherever the flip lives.** The static
unbounded-below spectrum becomes an unbounded GROWTH RATE — the SAME pathology
relocated, not cured. C-2026-06-13-1's c_θ²=e^{−2φ}/r²>0 is the DIAGONAL
sector's speed; the OFF-DIAGONAL on-shell coefficient is K_θ<0, and that is
what sets the angular characteristic in the off-diagonal wave.

A genuine cure requires the closed/nonstationary WHOLE to supply a spatial
higher-derivative (or sign-flipping) term that statics has now shown the action
does NOT contain. Absent that, the handoff is RELOCATION.

HONEST ALTERNATIVE READING (assessed, and I judge it at least co-equal): K_θ
strengthens monotonically TOWARD the seal/medium (registry #38: phi 0.5→−2,
K_θ −0.78→−303). A region where the static operator is unbounded below AND the
angular Cauchy problem is Hadamard-ill-posed is naturally read as **where the
CELL ENDS and becomes medium** — the cell boundary — NOT where a new bounded
shaped particle TYPE lives. The off-diagonal flip may be the geometric SIGNATURE
of the cell edge, consistent with the finite-cell canon (C-2026-06-10-2,
mirrored interface) and the exterior-field/medium picture, rather than a
frontier hosting an undiscovered type.

================================================================
## SURVIVING STATEMENT (corrected scope)

The static single-cell C1 off-diagonal angular operator is UNBOUNDED BELOW
where K_θ<0, and the metric's OWN action supplies NO native term — dropped by
the static truncation — that bounds it: (i) w-shape ABSENT as gradient
(algebraic; even EH gives w only RADIAL stiffness, no angular); (ii) phi-angular
cross is 2nd-order (cause, not cure); (iii) curvature/EH is NOT in the action
(import-forbidden) AND would not bound the angular direction anyway; (iv) #36 is
an exact/cohomological boundary datum, bulk-invisible to the operator. The axial
u,v are algebraic and are part of the flip's CAUSE. **The completion is not in
the static single-cell class — CONFIRMED.** The honest onward reading is NOT
"a live nonstationary route hosts the type" by default: the naive nonstationary
handoff RELOCATES the pathology (Hadamard-ill-posed angular evolution), so the
off-diagonal flip region is, on present evidence, **as likely the cell's
medium-edge as a particle locus.** The next gate must show the closed/
nonstationary WHOLE supplies genuinely NEW structure (a spatial regularizer or a
core-closure topology, #37) — otherwise the frontier should be re-read as the
boundary of the cell, not a new-type frontier.

================================================================
## SELF-AUDIT (anti-confirmation)

I tried hardest to FLIP (find a native bounding term). The one genuine new
object I surfaced — the EH-remainder's q,w 2nd-derivatives in `√−g R` — turned
out (a) not in the action and (b) angular-blind even if admitted, so it did NOT
flip the verdict; it reinforced it. I did NOT bank any by-hand stiffness (the
W2–W8 dead import; the converge.py +1/+3 shifts are correctly flagged forbidden).
My ONE substantive correction is scope, not direction: kill-shot D shows the
handoff is relocation-not-cure, which the challenger's STEP-3 framing under-
weighted by presenting the nonstationary/closed whole as a default live home.
