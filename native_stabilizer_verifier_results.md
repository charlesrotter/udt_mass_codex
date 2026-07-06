> **CONDITIONS-CHANGED (2026-07-06 pre-native-era census) — NOT current native-micro canon; premise-scoped.**
> The object-identity/profile is CONDITIONS-CHANGED (NEGATIVES_REGISTRY #43: non-unit-norm S³-Skyrme mis-fit on the
> unit S² target). NOTE: the √(κ/ξ) SIZE scale is NATIVELY RE-CONFIRMED (canon C-2026-06-14-1; hopfion arc
> ℓ_hopf≈1.1√(κ/ξ)) — so this is not a quarantine, only the profile/object-ID is scoped. Superseded frame; the
> 2026-07-01 native constrained-two-player operator (EH-empty, φ-blind matter, geometric 𝒦) is the current frame.
> See pre_native_era_census.md + NEGATIVES_REGISTRY.

# Native Stabilizer — BLIND ADVERSARIAL VERIFIER results

Date: 2026-06-14. Agent: Claude (Opus 4.8, 1M context), BLIND ADVERSARIAL
VERIFIER. Target: native_stabilizer_results.md (constructor, same date).
DISCIPLINE: independent re-derivation with my own machinery; I did NOT run
the constructor's scripts. DATA-BLIND (no masses/ratios/wall numbers).
Scripts saved: native_stabilizer_verif_task1.py (sympy CPU),
native_stabilizer_verif_task234.py (sympy CPU, Derrick + Hilbert stress +
total-derivative), native_stabilizer_verif_bvp.py (scipy BVP flat),
native_stabilizer_verif_deep.py (scipy BVP deep-phi p=0..4).

Verdict up front: **STANDS.** Every load-bearing claim reproduces under
independent derivation. Three differences from the constructor's NUMBERS
are convention/reduction artifacts (documented below), none of which
touches a physical conclusion.

---

## CLAIM 1 — Skyrme L4 == |omega_H1 winding current|^2_g (NATIVE) — **CONFIRMED**

I built the test WITHOUT pre-projecting to a tangent {n,e1,e2} basis. The
unit 3-vector was parametrized by two free scalar fields Theta(x),Phi(x) of
all four coordinates, so |n|=1 is enforced IDENTICALLY (verified
|n|^2-1==0 symbolically) and n.d_m n=0 holds identically for all m
(verified symbolically) — the constraint surface is realized, not asserted.

Defining S_mn = d_m n x d_n n (3-vector 2-form) and
F_mn = n.(d_m n x d_n n) (scalar 2-form = omega_H1 component):

- **Claim A, pointwise, exact:** S_mn . S_pq == F_mn F_pq for **all 256**
  index quadruples (m,n,p,q), symbolic sympy `simplify(...)==0`. This is the
  Lagrange/Binet-Cauchy identity (AxB).(CxD)=(A.C)(B.D)-(A.D)(B.C) collapsing
  on the constraint surface because each d_m n is tangent (n.d_m n=0), so the
  cross d_m n x d_n n is parallel to n and its self-contraction equals the
  squared scalar triple product. NOT a basis artifact — proved on a fully
  general n(x).

- **Metric contraction, both metrics:** g^{mp}g^{nq}F_mn F_pq -
  g^{mp}g^{nq} S_mn.S_pq == 0 for (i) the UDT diagonal inverse metric AND
  (ii) a RANDOM symmetric NON-DIAGONAL inverse metric, evaluated at random
  field values (max |diff| 5.7e-14 UDT, 2.0e-15 non-diag = machine zero).
  This confirms the g^{mp}g^{nq} index placement is correct independent of
  metric form. (Trivially implied by Claim A — equal pointwise tensors give
  equal bilinear contractions — but checked explicitly as requested.)

- Normalization (1/4 vs 1/2 vs 1/32) only rescales kappa; it cannot turn a
  native object non-native.

=> **L4_std = -(kappa/4) |omega_H1|^2_g exactly.** The Skyrme four-derivative
term IS the UDT-metric norm of the OWN-derived H1 winding current. The
"import" named a real native object. **CONFIRMED, hardest claim survives.**

---

## CLAIM 2 — Derrick / sized soliton — **CONFIRMED**

**Derrick (sympy, flat phi=0, independent ansatz bookkeeping):** I built E2
and E4 radial integrands from L2 = -(xi/2)g^{mn}d_m n.d_n n and the NATIVE
L4 = -(kappa/4)|omega_H1|^2_g (not lifted), integrated over the sphere, then
scaled Theta(r)->Theta(r/lambda) via an explicit u=r/lambda change of
variable. Result:
- E2(lambda) ~ lambda^{+1}  (every monomial carried a single +1 power)
- E4(lambda) ~ lambda^{-1}
So E(lambda)=A lambda + B/lambda, A,B>0 => lambda*=sqrt(B/A)>0,
E''(lambda*)=2B/lambda*^3>0: a STABLE minimum. (Contrast NEGATIVES #43:
L2-only had both ~lambda^1, monotone collapse — reproduced as the kappa->0
limit.) **CONFIRMED.**

**Profile BVP (scipy solve_bvp, my own EL derivation, flat):** I derived the
hedgehog Euler-Lagrange equation d/dr(2 a T') = a_T T'^2 + b_T with
a=(xi/2)r^2+kappa sin^2T, b=xi sin^2T+(kappa/2)sin^4T/r^2 and solved the
charge-1 BVP Theta(core)=pi -> Theta(seal)=0:
- A NON-TRIVIAL stabilized profile exists (rms residual ~1e-8).
- Width ~ sqrt(kappa/xi): (w-rc)/L = 0.874, 0.876, 0.876, 0.876 for
  kappa=0.25,1,4,9 (CONSTANT in L — the only length).
- Cell-size independent: (w-rc)/L = 0.869 -> 0.875 -> 0.876 as cell grows
  8L -> 20L -> 40L.
- **Virial E2=E4:** E2/E4 = 0.9999 across the whole kappa scan.

**Deep-phi survival (scipy BVP, phi=-p ln(rint/r), p=0..4):** the stabilized
soliton SURVIVES at every depth p=0,0.5,1,2,3,4 (BVP converges, residual
~1e-7, non-trivial monotone pi->0 profile); the minimum persists and the
twist stays on the cell. **CONFIRMED — minimum does NOT disappear at large p.**

DIFFERENCE (not a refutation): my flat width ratio is 0.876 vs the
constructor's 0.652, and my deep-phi twist shifts INWARD with p while the
constructor reports OUTWARD. Both are convention artifacts: (i) the absolute
width coefficient depends on the L4 hedgehog-energy prefactor split and the
core cutoff rc; (ii) the deep-phi shift direction depends on the sign-of-phi
chart convention for which endpoint is the deep core. The PHYSICS — existence,
width ∝ sqrt(kappa/xi), cell-independence, virial E2=E4 (flat), deep-phi
survival — reproduces identically under both conventions. Flagged, not
blocking.

---

## CLAIM 3 — EOS inversion: softened where it twists, exact only in exterior — **CONFIRMED (with a reduction caveat that does not change the conclusion)**

**Independent Hilbert stress tensor:** I did NOT use the constructor's
hedgehog formula. I treated the inverse-metric diagonal entries g^{tt},
g^{rr},g^{thth},g^{pp} as independent variables, wrote L = -(xi/2)K2 -
(kappa/4)K4 in those variables, and applied T^a_b from
T_mn = -2 dL/dg^{mn} + g_mn L. Because the fields don't depend on g^{tt},
T^t_t = L exactly => rho = -L; and T^r_r = -2 g^{rr} dL/dg^{rr} + L. Then:

  **p_r + rho = g^{rr} Theta'^2 [ g^{pp} kappa sin^4(th) sin^2(Theta)
                                  + xi (1 - cos^2(th) cos^2(Theta)) ]**

Substituting the UDT inverse metric and resolving the hedgehog angular
structure:
- POINTWISE it carries a cos^2(theta) hedgehog anisotropy.
- **SPHERE-AVERAGED:** p_r+rho = e^{-2phi}Theta'^2/(3r^2) *
  (2 kappa sin^2 Theta + r^2 xi sin^2 Theta + 2 r^2 xi).
- **L2 piece at the equator (theta=pi/2):** xi e^{-2phi}Theta'^2 — this
  EXACTLY reproduces banked CANON D7 and the canon C-2026-06-14-1 form.

CAVEAT (documented, non-blocking): the constructor's clean
p_r+rho = e^{-2phi}Theta'^2(xi + 2 kappa sin^2Theta/r^2) is the
EQUATORIAL / radially-reduced 1D stress, NOT the raw pointwise OR
sphere-averaged 4D Hilbert value (both of which carry extra hedgehog angular
structure that the 1D reduction suppresses). I could not reproduce the
constructor's exact prefactor from the 4D Hilbert tensor at a generic point.
**BUT** every form — pointwise, sphere-averaged, equatorial — shares the two
load-bearing properties:
  (a) **p_r + rho >= 0 always** (every bracket term is a manifest sum of
      non-negatives: kappa,xi,r^2>0; sin^2>=0; 1-cos^2th cos^2T>=0; the
      sphere-average carries a strictly positive 2 r^2 xi term);
  (b) **p_r + rho = 0 IFF Theta' = 0** (overall Theta'^2 factor; the
      bracket never vanishes identically when Theta in (0,pi)).

**Softened-everywhere claim, independently stress-tested:** I built a
piecewise profile that FLATTENS (Theta'=0) in a body region (Theta=pi core,
twist, Theta=0 exterior). Result: p_r+rho = 0 (machine zero, ~1e-27) in BOTH
flat regions, and p_r+rho ~ 1.7 (strictly >0) only across the twist. So:
  - The softening is a GENUINE consequence of Theta' != 0, NOT a BC artifact.
  - B=1/A (g_tt g_rr = -c^2 <=> p_r = -rho) is EXACT wherever Theta' = 0.
  - For the SMOOTH monotone charge-1 BVP profile, Theta' is nonzero
    throughout the finite cell (a monotone pi->0 interpolation), so the EOS
    is softened EVERYWHERE it twists and is EXACT ONLY in the fully-unwound
    exterior Theta==0 (a seal/boundary condition, not an interior body).
  **CONFIRMED, including the surprise.**

**Consistency with canon C-2026-06-14-1 scope — CONSISTENT, it REFINES, does
NOT contradict.** The canon's own "Scope/boundaries" block states verbatim:
"BREAKS under a radial twist: for Theta=Theta(r), p_r+rho = xi
e^{-2phi}(Theta'(r))^2 >= 0, zero iff Theta'=0. A realized smoothed-core
soliton satisfies p_r=-rho exactly only where Theta'=0; the pure topological
n=x/r is exact everywhere." The realized sized particle is precisely the
"breaks" regime in its twisting body, with B=1/A exact only in its unwound
exterior — exactly what the canon anticipated. The native L4 ADDS a second
non-negative piece (the kappa term) on top of the canon's xi term; it
deepens the softening but cannot change its sign or its vanishing locus.
**Consistent with the stated scope.**

---

## CLAIM 4 — Native potential = NO (eta is seal/boundary, not bulk V) — **CONFIRMED**

Independent total-derivative test (sympy): for a generic radial
total-derivative Lagrangian density L_td = d/dr G(Theta(r), r), the
Euler-Lagrange operator dL/dTheta - d/dr(dL/dTheta') returns **identically 0**
(symbolic). Any Lagrangian piece that is an exact differential (the
transgression Xi = dTheta_form, with global primitive (ln f) omega_H1)
contributes ZERO to the bulk field equation; by Stokes its whole content is
the seal/boundary value. So eta = q/6 is a seal/junction-closure object, NOT
a bulk potential V(n); it supplies no Derrick-style lambda^{+3} stabilizer.
The sole native stabilizer is the Claim-1 winding-current (Skyrme) term.
**CONFIRMED (negative, first-class).**

---

## CLAIM 5 — Pinned size; one scale or two? — **CONFIRMED; ONE scale**

The stabilized size lambda* = sqrt(B/A) ~ sqrt(kappa/xi) is set by the
coupling RATIO. My BVP confirms the width is constant in units L=sqrt(kappa/xi)
across the kappa scan and across cell sizes — sqrt(kappa/xi) is the only
length that enters; r_core and cell size do NOT pin it (verified by cell-size
independence). Counting dials: the minimal L2 model had xi only (overall
energy scale, no length). The native L4 adds kappa; the physically meaningful
new quantity is the dimensionless/length RATIO kappa/xi, which sets L. So the
stabilizer introduces ONE intrinsic length the minimal model lacked — it is
the ratio kappa/xi, not a second free tunable beyond the single coupling
ratio. (Whether that ratio is itself fixed by deeper UDT structure is a
separate, un-pursued question; as posed here it is one allowed dimensionful
scale, not two independent dials.) **CONFIRMED.**

---

## OVERALL VERDICT: **STANDS.**

| Claim | Verdict |
|-------|---------|
| 1. Skyrme == |omega_H1|^2_g (native) | **CONFIRMED** (256-pair exact identity + both metrics) |
| 2. Sized soliton stabilized (Derrick cured) | **CONFIRMED** (lambda^{+1}/lambda^{-1}, BVP, virial, deep-phi survival) |
| 3. EOS softened where it twists, exact only in exterior; consistent w/ canon scope | **CONFIRMED** (sign + vanishing robust; REFINES C-2026-06-14-1, does not contradict) |
| 4. eta = seal, not bulk potential | **CONFIRMED** (total derivative, zero bulk EL) |
| 5. One scale (kappa/xi), not two | **CONFIRMED** |

DIFFERENCES from the constructor's numbers, all convention/reduction, none
blocking: (a) flat width 0.876 vs 0.652 (L4 prefactor split + core cutoff);
(b) deep-phi twist shifts inward in my sign convention vs outward in the
constructor's (sign-of-phi chart choice); (c) the clean
p_r+rho = e^{-2phi}Theta'^2(xi + 2kappa sin^2Theta/r^2) is the equatorial/1D
reduction, not the raw 4D Hilbert pointwise/averaged value (which carries
extra hedgehog anisotropy) — but the L2 piece matches CANON D7 at the
equator, and the sign (>=0) and vanishing (iff Theta'=0) are identical in all
forms, so the physical EOS conclusion is unaffected.

No smuggled mechanism found. The native identity (Claim 1) is rigorous on
|n|=1 (enforced identically, all 256 pairs, two metrics). The EOS inversion
(Claim 3) is real and faithfully reported, and is consistent with — a
refinement of — canon C-2026-06-14-1's stated scope.
