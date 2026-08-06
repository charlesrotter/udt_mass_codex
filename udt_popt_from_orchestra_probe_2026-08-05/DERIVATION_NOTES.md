# Derivation notes — P-opt from the orchestra

Date: 2026-08-05. **STATUS: LEAD / UNBANKED. NOT A RESULT.** Two adversarial reviews owed;
external review owed for any bank. Four-check N/A to a lead. No data/fit touched (target A).

## Result (exact, self-checked only): OP-INDEPENDENT

The orchestra structure does NOT derive P-opt. Verified points:
1. The reciprocal-lock metric g_tt=-A c^2, g_xx=1/A gives g_tt*g_xx = -c^2 for **ANY** radial
   profile A(x). The lock does not constrain the profile.
2. Depth phi=-1/2 log A; the reciprocity relation delta(p,q)=phi(p)-phi(q) is antisymmetric
   for **ANY** A(x). Observer Reciprocity (as observer-comparison symmetry) does not constrain
   the profile.
3. Fermat optical path dl_opt = dx/A is derived. **P-opt** (dl_opt = kappa dphi, kappa const)
   is the EXTRA condition; it integrates uniquely to A = 1 - x/X (the L profile).
4. An alternate profile (H-type, A~sech) is equally reciprocal-lock + reciprocity consistent
   but violates P-opt (dl_opt/dphi not constant). So P-opt is a genuinely INDEPENDENT,
   profile-selecting principle, not forced by the orchestra's reciprocal form + reciprocity.

**Conclusion:** the orchestra derives the reciprocal FORM (A=e^{-2phi}), not the radial
PROFILE A(x). P-opt fixes the profile. The orchestra leaves the profile FREE — it is exactly
the class of thing the orchestra explicitly does not select (the free `a` / the unselected
cocycle/law). So the z(z+2)=0.91 SNe validation is **NOT upgraded to native**; it remains
conditional on P-opt. This is the null / non-owner-pleasing outcome (matches the pre-analysis).

## The reframing (honest, NOT a rescue): P-opt = the law gate, so SNe is informative about the law
P-opt says "light's optical path is an affine parameter of the depth flow" — a specific
profile/law choice. Since the orchestra leaves the profile open, **P-opt is the same class of
open problem as selecting the orchestra's free parameter / the response law.** Consequences,
all honest and useful:
- The SNe validation's "conditional on P-opt" is NOT a separate weakness; it is the SAME
  law-selection gate that this session's three probes all pointed at. One gate, not two.
- The z(z+2)=0.91 fit is effectively a **prediction of "the law produces the L profile
  A=1-r/X."** Deriving the law TESTS it: law -> L profile => SNe native; law -> other profile
  => SNe prediction changes.
- Therefore SNe DATA is informative about the law BEFORE the law is derived: the excellent
  fit is a **target/constraint** for the response-first law program (the law should yield
  ~A=1-r/X to keep the SNe agreement). This is a genuine, non-shopping use of the data.

## What the two reviews must attack
- Review A: STEELMAN OP-DERIVED. Apply Observer Reciprocity FULLY (to null/optical paths,
  round-trip light, cocycle single-valuedness, the full equivariance) and try hard to FORCE
  P-opt. If reciprocity properly applied does fix the profile, OP-INDEPENDENT is a lazy giveup.
- Review B: attack the reframing + hunt OP-PARTIAL. Do the BANKED GLOBAL constraints — the
  x_max asymptote (phi->infty at x_max, G14), regularity, finite-cell canon — partially fix
  the profile independently of the full law (pushing toward L)? Is P-opt a distinct, more
  fundamental optical principle than "a generic law choice"? Verify the baseline (z(z+2),
  0.91, conditional-on-P-opt) is represented correctly.

## CONSOLIDATED CORRECTION (2026-08-05): both reviews confirm OP-INDEPENDENT; corrections + a tension

Files: ADVERSARIAL_REVIEW_A_steelman_derived.md (VERDICT PASS), ADVERSARIAL_REVIEW_B_global_reframe.md (VERDICT NARROW).

**OP-INDEPENDENT CONFIRMED from both directions.** Review A attacked hardest with the FULL
Reciprocity structure (my original argument used only weak antisymmetry — under-powered; A
supplies the stronger justification) and every lever failed: full cocycle composition holds
for arbitrary profile; groupoid single-valuedness is automatic in the 1D radial sector;
round-trip/radar reciprocity closes for any A. Review B confirmed the banked global
constraints do not fix the profile toward L (explicit counterexample A_H=(X-r)/(X+r) passes
every global gate yet isn't L).

**STRENGTHENED (Review A) — P-opt is not merely un-forced, it is naturality-DISFAVORED.** There
is no canonical reciprocity-invariant parametrization forcing "optical path = depth." The
reciprocal flow admits several equally-natural canonical parameters, each giving a DIFFERENT
profile: uniform depth per null-geodesic AFFINE parameter -> A EXPONENTIAL (the most natural);
per Fermat optical path -> A LINEAR (P-opt); per proper distance -> A QUADRATIC. The MOST
natural (affine) choice gives exponential, NOT L. Also: light is not an eigenvector of the
reciprocal strain (timelike stretch != spacelike), so the depth cocycle lives on the
TIMELIKE/clock sector — light carries no reciprocity depth for reciprocity to make affine.

**CORRECTIONS to this note (Review B):**
1. "ANY profile A(x)" OVERSTATED. Correct: the banked global constraints (x_max asymptote
   A->0 at wall, regularity A(0)=1, finite-cell, near-wall exponent beta in [1,2)) fix a
   CONSTRAINED FAMILY; P-opt selects L WITHIN it; the global gates do NOT reach L on their own.
2. RETRACTED — the reframing bullet "the law should yield ~A=1-r/X to keep the SNe agreement"
   SMUGGLES TARGETING (data-favored profile as design goal for the undelivered law) — exactly
   the SNe-shopping this probe's own prereg named as primary hazard. STRUCK. Third steering
   slip caught by review this session.
3. "P-opt = the orchestra's free parameter" OVER-FLATTENS. P-opt is a rigid axiom (light
   meters depth via Fermat length), not a 1-parameter knob. Keep "same open LAW gate"; drop
   "same as the free parameter."

**CORRECTED VERDICT:** the phi+orchestra formulation does NOT upgrade the native SNe fit
(z(z+2), chi^2/dof=0.91) to native. It stays conditional on P-opt, and naturality mildly
DISFAVORS P-opt (natural parametrization -> exponential profile, not the linear L that fits
SNe). So target (A) FAILED: the fit is not secured, and the orchestra makes P-opt look like a
specific, non-privileged physical principle.

**THE HONEST TENSION (stated WITHOUT targeting):** the SNe data favors the LINEAR (L) profile;
Review A's naturality lean is toward the EXPONENTIAL profile. These need not agree. The actual
response-first law will yield SOME profile; whether it is L (SNe-native), exponential
(naturality-leaning, likely poorer SNe), or other is undetermined here. The legitimate reading
is that the z(z+2)=0.91 fit is an EMPIRICAL TEST the eventual law must face — not a shape the
law should be built toward. If the derived law gives exponential and SNe wants linear, that is
a real problem to be adjudicated by derivation + data, not by design. Nothing banks.

## MODERATION (2026-08-05, prompted by Charles): the x_max kernel excludes the naturality-exponential

Charles: "the profile is exponential — that's what leads to x_max/the asymptote — but at z<1 it
is essentially linear and just starting to depart; a scale issue." Checked exactly; he is right,
and my prior "naturality disfavors L/P-opt" gloss OVER-DEFLATED. Verified facts:

1. **The x_max kernel EXCLUDES Review A's naturality-preferred exponential-A** (A=e^{-r/X}):
   its max PROPER distance integral(1/sqrt(A)) diverges -> NO finite maximum separation ->
   VIOLATES the owned x_max kernel (G14). The L profile (A=1-r/X) has FINITE proper distance to
   x_max (= 2X) -> satisfies the kernel. So the null-affine-"natural" exponential that Review A
   said disfavors L is itself KERNEL-INCOMPATIBLE. Once x_max (a more fundamental owned
   commitment than a parametrization-naturality preference) is imposed, the naturality objection
   to L collapses.
2. **The L profile IS the "exponential" character Charles means** — not an exponential metric
   function, but the exponentially-diverging REDSHIFT/DEPTH the linear A produces: 1+z=1/sqrt(1-u)
   -> infinity and phi -> infinity as u->1 (the x_max asymptote), while at low z, z ~ u/2 (linear
   Hubble). So L is "essentially linear at z<1, developing the x_max/redshift asymptote at high
   z" exactly as described. The "scale issue" reading is correct.
3. Caveat (kept honest, NOT retracted): OP-INDEPENDENT STILL HOLDS — the orchestra does not
   derive P-opt. Within the KERNEL-COMPATIBLE finite-x_max family (L, and Review B's H=(X-r)/(X+r),
   etc.), P-opt selects L. So "why L rather than another finite-x_max profile" is the residual
   open question. But L is now aligned with BOTH the x_max kernel AND SNe, and is NOT
   naturality-disfavored (the naturality pick was kernel-excluded). The distance-law check
   confirms the exponential-A would fit SNe badly (offset-removed shape ratio E/L: 1.10 at z=0.1,
   1.46 at z=0.5, 1.85 at z=1) — but that profile is kernel-excluded anyway, so no tension.

**Net correction to the prior verdict:** strike "naturality mildly disfavors P-opt/L." Corrected:
once the x_max kernel is imposed, the naturality-exponential is excluded, and L (SNe-fitting) is
kernel-consistent. The honest residual is narrower and non-deflationary: P-opt is not
orchestra-DERIVED, but it selects the SNe-and-kernel-consistent L within a small finite-x_max
family. Discipline note: this MODERATION is owner-favorable; the integrals are elementary and
verified, but the "kernel overrides naturality" synthesis is an interpretation and would benefit
from its own adversarial pass before any bank. Nothing banks.
