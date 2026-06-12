# W1 — Native w-Stiffness Derivation: Results (Routes A, B, C)

Date: 2026-06-11 (continuation session). Driver: Claude.
Declaration: w_stiffness_push_declaration.md (committed d75101f BEFORE
any route ran; metric-led in method; forced-object motivation declared).
Scripts (committed with this doc): w_stiffness_routeA_enlarged_class.py
(34/34), w_stiffness_routeB_forced_completion.py (70/70),
w_stiffness_routeC_sector_audit.py (41/41 on rerun; an earlier "42"
was a grep off-by-one), w_stiffness_routeA_verifier.py (23 checks),
w_stiffness_routeB_verifier.py (48/48), w_stiffness_routeC_verifier2.py
(47/47; the first VC script stalled in an open-ended sp.solve and was
killed unfinished — its conclusions were treated as absent, and one of
its draft conclusions was subsequently refuted by VC2).
Verifier passes (blind, adversarial, independent machinery): VA = agent
aa52d048f52d62d44, VB = agent ace1d6f9c1b798845 (2026-06-11), VC2 =
agent a72516ed81b0c55a6 (2026-06-12). Every route below is
recorded WITH its verifier amendments folded in; nothing here is
pre-verifier wording.

## Headline

THE NATIVE w-STIFFNESS SECTOR IS NOT IN THE EXISTING THEORY. Three
independent routes, each verifier-adjudicated:

- **Route A (theorem, VA-amended):** the C1 density is FIRST-JET IN
  g_tt ONLY (through the definitional tie phi = -(1/2) ln f) and
  zeroth-jet in every other metric component — verified on a fully
  generic 10-function metric (all components functions of all four
  coordinates, no axisymmetry, no staticity, g_rr untied). NO
  enlargement of the metric class can make C1 itself supply w- or
  shear-derivative terms, for any shape mode not entering the tied
  slot g_tt. The P1 structural lemma is a property of C1 + the tie,
  not of the reduction.
- **Route B (negative-of-forcing, VB-amended):** the balance /
  forced-completion method that uniquely forced D* in the rho sector
  CANNOT force a w-stiffness: every banked configuration has w = 0,
  and every w-jet-quadratic Euler-Lagrange term is identically
  invisible on w = 0 configurations — so no survival demand built
  from the banked stack selects among stiffness candidates. The
  surviving completion family is parametrized by free functions and
  GROWS with jet order.
- **Route C (premise-scoped negative, VC):** every banked non-C1
  native sector (two-form flux, H1 collar source, S_phi0/DtN,
  responsive source, licensed completion family) is zeroth-jet in the
  entire angular block — the exact w-analog of "no native sector
  carries rho'". The stiffness is not hiding in the banked inventory.

Consequence: deriving the w-stiffness sector requires a NEW NATIVE
PRINCIPLE — a second-jet-in-the-angular-block density that the
program does not yet possess and that C1, the balance method, and the
banked sectors provably cannot supply. The species identification
sharpens: on the P1 class the shape-derivative carrier is exactly the
second-jet/curvature species (Route A S5, VA-confirmed by coefficient
extraction), and the EH density's by-parts reduction is itself a
survival-passing member of the Route-B family (VB) — the question is
no longer "what carries w-stiffness" but "what native principle
SELECTS a member" (selection-problem reframe, see Frontier below).

## Route A — class-enlargement audit (34/34 + VA 23 checks)

Question: is the P1 lemma ("q and w enter with no derivatives at any
nonlinear order") a property of C1 or of the reduction?

**Answer: of C1 + the tie, on every class.** The C1 integrand
-(c/8) sqrt(-g) g^{mu nu} f_mu f_nu / f differentiates only
f = -g_tt; all other metric components enter algebraically (inverse
metric + volume). VA verified this on a strictly more hostile class
than the route's (10 free functions of all coordinates) and confirmed
by simplified-coefficient extraction (not just atom census).

Exact structures banked (all VA-confirmed, all-sign symbolic):
- Enlarged static class (g_thetatheta = r^2 P, g_phiphi =
  r^2 sin^2(theta) Q independent, q free): after the unique
  q-elimination (q* unique because the bracket is LINEAR in q),
  L_eff = -(c/8) sin(theta) sqrt(Q/P) |X_e - Y| / f,
  X_e = f r^2 P f_r^2, Y = f_theta^2.
- Shape forces: dL/dw = -(c/8) sin(theta) r^2 f_r^2 (pure radial
  source — the conformal mode is sourced by f_r, not f_theta);
  dL/ds = -(c/4) sin(theta) e^{-2s} f_theta^2 / f (pure phi-angular).
- **Strictly-emptier theorem:** on the fully freed angular block,
  joint (q,P,Q)-stationarity forces f globally constant (connected
  domain) or the degenerate corner X_e = Y — even the formed
  spherical f that survived P1 is killed. Enlarging the class makes
  C1 statics emptier, not richer.
- Degeneracy identity: D2(q*) proportional to (X_e - Y)^2/(X_e + Y)^2
  — the P1 corner locus IS metric degeneracy (exact polynomial
  identity).
- P1 dictionary (checked entry-by-entry against the rescued
  pde_p1/derive_system.py): P1's single shape field is the SHEAR
  mode (unimodular angular block); the conformal/determinant mode is
  what P1's primary class excluded (and pde_p1 had probed once as
  the "breathing mode" variant). The route prompt's suspicion was
  inverted.

**VA amendments (binding wording):** (i) "zeroth-jet in the metric" is
wrong as stated — first-jet in g_tt via the tie; (ii) the universal
quantifier carries the proviso "for shape modes not entering g_tt": a
conformal factor on the whole metric, or an alternative tie (e.g. phi
tied to the angular determinant), DOES acquire shape derivatives. The
tie phi = -(1/2) ln(-g_tt) is therefore a LOAD-BEARING PREMISE of this
negative; if the tie is ever revised, this entry is CONDITIONS-CHANGED
(registry entry below). VA also found route-script defects (E2b, S4b,
G3b vacuous/duplicated; positive-only sampling — honest independent
check count ~29, mitigated by VA's all-sign proofs).

## Route B — forced completion / balance method (70/70 + VB 48/48)

Question: does demanding survival of the banked solutions force a
unique completion D*_w, as it forced D* in the rho sector?

**Answer: no — and the reason is structural, not the route's original
homogeneity argument (VB amendment).** The rho precedent worked
because C1's rho-tadpole is nonzero ON the banked vacuum. The route
argued the w-tadpoles vanish on every spherical configuration
(homogeneity). VB sharpened: banked DATA-BLIND positives (M2 library
cells, collars) DO have f_theta != 0, reviving inhomogeneity in both
the w- and q-channels (EL_w = -(c/4) sin(theta) f_theta^2/f, EL_q =
-(c/4) sin(theta) f_r f_theta there) — but the revival STILL cannot
force a stiffness, because every w-jet-quadratic EL term is
identically invisible on w = 0 configurations, and every banked
configuration has w = 0. Selection would need a banked w != 0
solution, which is exactly what doesn't exist (registry #21/#22).
Circle closed: the theorems that force the stiffness also block its
selection by survival demands.

Banked structures (VB-confirmed unless marked):
- The completion family: all 28 shape-ideal-squared monomials
  (ideal I = (w, q, f_theta, w_r, w_theta, q_r, q_theta), arbitrary
  smooth coefficients) pass survival + spherical-vanishing; the family
  is larger still (f_r-bearing members like alpha(q) f_r f_theta also
  pass — VB); under-determination GROWS at second jet (alpha w w_rr
  passes — VB V2.6). Negative controls genuinely fail.
- **The D_cell fork (VB discovery, first-class, for Charles):**
  D_cell = (c/4) sin(theta) [w f_theta^2/f + q f_r f_theta] cancels
  both cell tadpoles pointwise for EVERY f, leaves the f-equation and
  macro untouched — under C1 + D_cell the banked Class-A cells become
  EXACT full-system statics WITH NO STIFFNESS AT ALL. A stiffness-free
  member resurrects static cells (with w identically 0 and no
  w-dynamics). Registry #21-relevant; non-unique (D_cell + any
  stiffness member also works). This is a completion-ambiguity fork,
  not a derivation: nothing selects D_cell either.
- Shaped solutions exist as exact algebra for the representative
  member D_rep = kappa sin(theta) (r^2 w_r^2 + w_theta^2):
  f = C + a/r, q = 0, w = (A r^ell + B r^{-ell-1}) P_ell(cos theta),
  verified ell = 1,2,3, macro untouched. **VB amendments:** every such
  member is AXIS-SINGULAR (elementary flatness needs w = 0 on axis;
  no nontrivial axis-regular superposition exists — powers of r
  independent), so on axis-containing CANON C-2 cells the axis-regular
  shaped static sector of C1 + D_rep (f spherical, q = 0) is EMPTY;
  action finite on finite cells, bounded below and shaped-costs-more
  for kappa > 0, UNBOUNDED BELOW for kappa < 0, and kappa's sign is
  unforced. Acceptance test (a) is NOT met by D_rep; the existence
  datum is mechanism-level only (the unbalanceable-tadpole obstruction
  is removable), not a matter solution.
- **A1-native claim WITHDRAWN (VB refutation, recorded as the route's
  error):** the route claimed EL_w[sqrt(-g) R] = 2 sin(theta) on
  spherical backgrounds, hence "no C1 + kappa EH admits the banked
  vacuum — the metric's own refusal of the EH import." VB showed the
  2 sin(theta) is an operator artifact (first-order EL applied to a
  second-order density; the missing +d_theta^2(dL/dw_thetatheta) term
  cancels it exactly, validated against EL = -sqrt(-g) G^{mu nu}
  d g_{mu nu}). TRUE result: on the P1 class the EH density
  contributes ZERO to all three field equations on every spherical
  configuration — C1 + kappa EH admits the banked vacuum for EVERY
  kappa. The banked vacuum's nonzero Einstein content
  (G^t_t = (C-1)/r^2) sits entirely in the directions the P1 ansatz
  freezes (tt+rr trace, rho). The rho-sector A1 refusal
  (a^2/(2 r^3), rho_dynamics_derivation_results.md) is INVISIBLE on
  this class and still stands on the (f,rho) class. Consequences:
  (i) the no-forcing verdict strengthens (EH's by-parts reduction is
  itself a survival-passing w-derivative carrier inside the family);
  (ii) the guardrail's refusal of the EH import can NOT cite a
  P1-class dynamical refusal — its basis remains principle 1
  (derivation provenance) and the rho-sector result only.
- Convention erratum (VB): the route's T3 "verbatim" tadpole match
  with pde_p1 was a string-level coincidence (q = 0 branch at c = +2
  vs q* branch at c = -2; double sign flip). Physical content
  compatible; label corrected here.

## Route C — second-sector audit (41/41 + VC2 47/47)

Question: do the banked non-C1 sectors carry angular-block
derivatives?

**Answer: no — every banked non-C1 ACTION sector is zeroth-jet in the
entire angular block (VC2 re-scope: "the banked ACTION stack,
statics").** On the general angular block (g_thetatheta = r^2 A,
g_phiphi = r^2 sin^2(theta) B) — and, VC2-strengthened, with
off-diagonal g_thetaphi on as well — the union of differentiated
functions across the whole banked action stack is {f}: no dA, dB, dq
anywhere, at any order, so no w-, shear-, or breathing-derivative;
on-shell rescue is structurally impossible (S6). NAMED EXCLUSION
(VC2): the weld CONSTRAINT identities are constraint-grade objects,
not action pieces — the rung-2 weld carries d_t K (an angular-block
amplitude derivative), but it is a derived delta-T_tr = 0 identity,
and K = 0 is forced on the native branch by the perturbed R-areal
canon. VC2 also closed the re-solving loophole exactly: by the
dual-potential theorem the on-shell flux density differentiates only
the potential psi at ALL orders in q (the banked monopole is
psi0 = Q_f/r), and Q_f is topologically protected — re-solving
Maxwell on q-on/w-on backgrounds cannot smuggle angular-block
derivatives in; nonlocal dw-dependence starts only at O(q^3).

Per-sector exact structures:
- Flux: L_flux = -(Q_f^2/(2 mu)) sin(theta) (1+w)/(r sqrt(D)),
  D = r^2 (1+w)^2 - f q^2 — exactly w-BLIND at q = 0; no derivative
  of any field. New algebraic structure: the flux w-tadpole
  dL_flux/dw = +(Q_f^2/(2 mu)) sin(theta) f q^2/(r D^{3/2}) —
  positive, vanishes on the diagonal class and on spherical. VC2
  qualifiers (binding on any future citation): the opposition to the
  C1 w-force is Delta > 0 BRANCH-CONDITIONAL (on the opposite branch
  the C1 force has the tadpole's sign), and at O(q^2) on-shell the
  envelope identity carries a same-order sign-definite SCREENING term
  (1/2)<a*, G' a*> with G' = -(f v/mu sin(theta))(d_r a)^2 — the
  tadpole alone is not the on-shell w-force. Not a stiffness (no
  derivatives), but registry-relevant: the P1 corner theorem ("C1
  drives the shape sector to metric degeneracy") is C1-ONLY; on the
  flux-on q-on class the corner conclusion needs re-derivation
  (conditional on Pflux).
- H1 collar source: w-blind (literal and coordinate lifts), algebraic
  in w at q != 0 (proper lift); reading-independent verdict.
- S_phi0/DtN: pi_w, pi_q, dL/dw_theta vanish identically for the
  total stack — w-fluctuations carry zero gradient stiffness and zero
  DtN content; no boundary functional built from the banked stack can
  carry w boundary data.
- Responsive source: the banked Hessian integrand IS the C1 angular
  second variation in f-harmonic directions (exact identity; both
  banked couplings V_a1g1 = -sqrt(5) kappa/(2F), V_a0g0 =
  -sqrt(15) kappa/(3F) reproduced) — it inherits the C1 theorems.
- Scoped flag (route): the banked monopole flux rep is Maxwell-on-shell
  on diagonal backgrounds only; at q != 0 it needs re-solving (the
  zeroth-jet verdict is rep-independent, but solution-level angular
  dependence of Q_f on q-on backgrounds is an open scoped question).

## Registry updates (appended as NEGATIVES_REGISTRY.md #23-#25;
## the D_cell fork and the EH erratum are folded into #24; the W2
## seal negatives are #26)

- #23: C1 supplies no angular-block derivatives on ANY metric class
  (first-jet in g_tt only). PREMISES: the definitional tie
  phi = -(1/2) ln(-g_tt); shape modes outside g_tt; C1 alone.
  CONDITIONS-CHANGED trigger: any revision of the tie.
- #24: the balance/forced-completion method cannot select a
  w-stiffness from banked-survival demands (method-level negative;
  family grows with jet order). Carries the D_cell fork (awaiting
  Charles) and the EH erratum: "EH refused dynamically on the P1
  class" is wrong (VB); the EH-import prohibition rests on principle
  1 provenance + the rho-sector A1 result only.
- #25: the banked ACTION stack (statics) is zeroth-jet in the angular
  block — the w-analog of "no native sector carries rho'" — with the
  weld constraint identities as NAMED exclusions and the VC2 flux
  qualifiers recorded.

## Frontier after W1 — the corrected frame (per Charles, 2026-06-11)

The push proved a trichotomy: the existing theory CANNOT contain the
forced object (A: not in C1 on any class; C: not in the banked
sectors), and the program's selection tool CANNOT choose it (B:
survival demands are blind at w = 0). PROCESS CORRECTION (Charles
caught this mid-session): the trichotomy is the preamble the previous
session's close had already priced in — "forced object" MEANT not in
the inventory. The close's queue head also named the actual route and
the target's fingerprint, which this push's declaration dropped. They
are restored here verbatim and define W2:

1. **The named route** (nonstationary_opener_results.md:117-120,
   binding): "the EH remainder itself remains forbidden as an import;
   the target is its native derivation from positional-dilation first
   principles — principle 4's GR-corpus mine, transformed." I.e.,
   transform the GR second-jet/curvature corpus under the positional-
   dilation map and explore the transformed objects natively. W1's
   routes never ran this; it is the W2 push.
2. **The structural fingerprint** (ibid.:85-88): the w-force direction
   flips across the radial sonic locus g = f f_r^2 - f_T^2/f = 0 —
   "the surviving phi-angular interaction under C1 alone; the
   stiffness sector will dress exactly this." Any derived candidate
   must couple to the sonic-locus flip — a sharper filter than the
   three acceptance tests, and W1's verified structures now add to
   it: spherical-vanishing, axis-regularity (VB: the simplest member
   fails it), bounded-below action (VB: kappa-sign must be derived,
   not chosen), and the tie-premise (VA).
3. **The perfect-square heuristic**: forced native structure has
   twice arrived as a perfect-square completion in a dilation-weighted
   variable (rho sector: (1/4)[(f rho)']^2 in u = f rho; time row:
   Q^2 + 4 f D2 P f_T^2 = (fP + D2 f_T^2)^2). The angular sector's
   u-variable has never been identified — an organizing question for
   W2, not a mechanism import.
4. **The selection demand**: W1-B proved static survival cannot
   select; the close's secondary queue item (the theta-dial selector
   = the persistence condition for the h > h_c seal family, the
   theory's only T-bounded oscillatory sector) is therefore promoted
   to the candidate selection principle inside W2, not after it.
5. Subordinate W1 finding kept on the table: the tie
   phi = -(1/2) ln(-g_tt) is the unique derivative channel (VA); a
   first-principles interrogation of what dilation ties to belongs
   inside route 1's scope ("a metric function not yet uncovered" —
   Charles's standing hunch wording).

Acceptance-test status: not faced (no derived candidate exists yet).
W1's deliverable is the theorem-grade trichotomy + the restored W2
frame above.
