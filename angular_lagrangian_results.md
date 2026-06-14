# The Angular-Sector Lagrangian and p_r = -rho ("B=1/A inside matter") — Results

Date: 2026-06-14. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Frame:
CRITICAL_UNIVERSE_FRAME.md / CATALOG_FRAME.md. GATED DERIVATION authorized
by Charles (2026-06-14): construct UDT's angular-sector Lagrangian FROM THE
PROJECT'S OWN DERIVED OBJECTS, derive its stress tensor in the UDT
background, and TEST whether it gives p_r = -rho (equivalently
g_tt g_rr = -c^2, the "B=1/A" relation, holding INSIDE matter).

Scripts (commit-grade, this push):
- `angular_lagrangian_derive.py` — symbolic GR (sympy, CPU): field id,
  kinetic term, stress tensor, EOS test, anchor, back-reaction. 10/11
  print-checks PASS; the one "FAIL" is a sympy log-branch artifact in a
  symbolic `==`, disproven below (the integral DOES equal G1 exactly).
- `angular_lagrangian_anchor.py` — fast standalone anchor reductions.
- `angular_lagrangian_gpu_spotcheck.py` — V100 torch float64 spot-check:
  p_r+rho = 0 to MACHINE ZERO (0.000e+00) over 4096 random
  (r,theta,phi,phi(r)) points; CPU asserts pass; native G1 integral
  matches closed form to <1e-13.
Blind verifier: PENDING (verifier-before-record discipline; attack-here
block at the end).

THE EXACT QUESTION (external_source_analysis.py:3-4,27): the UDT static
spherical metric obeys a pure geometric identity
  g_tt g_rr = -c^2  <=>  G^t_t = G^r_r  <=>  p_r = -rho.
"B=1/A inside matter" is therefore TRUE iff the matter source satisfies
p_r = -rho. A canonical scalar phi does NOT (gives p_r+rho = e^{-2phi}
phi'^2 > 0). HYPOTHESIS UNDER TEST: UDT's angular/topological sector (the
n-field whose winding is omega_H1) IS a source with p_r = -rho, which would
DERIVE B=1/A inside matter as a theorem.

---

## TASK 1 — FIELD IDENTIFICATION (native)

DERIVED (h1_types_results.md:31-37, 159-166): the angular degree of freedom
is the unit 3-vector `n_a`, |n|=1, target S^2, whose winding density IS the
H1 area form
  omega_H1 = eps_abc n_a dn_b ^ dn_c = sin(Theta) dTheta ^ dvarphi,
  INT_S2 omega_H1 = 4*pi   (the deg-1 generator of H^2(S^2,Z)).
The carrier rank N=3 (eps_abc singlet unique iff N=3) and the public charge
slope q=1/3 (d ln f = -q d ln r) are carried by this same n-field
[DERIVED h1_types:159-164].

The hedgehog / radial-winding configuration is
  n_a = x_a/|x| = (sin Theta cos varphi, sin Theta sin varphi, cos Theta),
  Theta = theta.
This is the degree-1 map S^2(space) -> S^2(target). VERIFIED numerically:
winding density n.(n_th x n_ph) = sin theta, and
(1/4pi) INT eps_abc n_a dn_b ^ dn_c = 1 (deg-1 H^2 generator) [PASS].
TAG: field identity = DERIVED (cite h1_types:31-37,159); hedgehog = the
deg-1 representative = DERIVED.

## TASK 2 — THE KINETIC TERM (provenance, honest)

The minimal Lagrangian density built from the n-field gradient and the
UDT metric measure is
  L_angular = -(xi/2) g^{mu nu} (d_mu n_a)(d_nu n_a) ,   measure sqrt(-g),
with sqrt(-g) = c r^2 sin theta (the phi factors CANCEL:
e^{-phi}e^{+phi}=1 — a UDT-specific fact, g_tt g_rr=-c^2).

PROVENANCE / "chose or derived?":
- The contracted object (d_mu n_a)(d_nu n_a) is FORCED: it is the ONLY
  diffeo-scalar, target-isometry-invariant, two-derivative quantity the
  n-field admits. The winding 2-form omega_H1 is TOPOLOGICAL (metric-free)
  and contributes NO stress (confirmed TASK 6). [DERIVED-as-unique]
- That it is contracted with the UDT g^{mu nu} and weighted by the UDT
  sqrt(-g) is FORCED by general covariance + the UDT measure. [DERIVED]
- The prefactor -(xi/2) (sign + normalization xi) is CHOSEN — the minimal
  canonical-kinetic normalization; xi is the single coupling. [CHOSE]
- NO potential and NO higher-derivative (Skyrme) term added. [CHOSE —
  minimal model; Skyrme term absent, flagged]

Hedgehog gradient invariant: X = g^{mu nu} d_mu n . d_nu n = 2/r^2 (pure
transverse; d_t n = d_r n = 0) [PASS]. The anchor (TASK 5) is what decides
whether this minimal choice IS the project's own functional or an import.

## TASK 3 — STRESS TENSOR (hedgehog in the UDT background)

For L = -(xi/2) g^{ab} dn_a.dn_b the stress is
  T_{mu nu} = xi (d_mu n_a)(d_nu n_a) + g_{mu nu} L,   L = -(xi/2) X.
Raising one index with the UDT inverse metric (sympy, exact):

  T^t_t      = -xi/r^2      =>  rho     = xi/r^2
  T^r_r      = -xi/r^2      =>  p_r     = -xi/r^2
  T^theta_th =  0           =>  p_theta = 0
  T^phi_phi  =  0           =>  p_phi   = 0

All four [PASS]. NOTE: T^t_t = T^r_r = -xi/r^2, and both are INDEPENDENT of
phi(r) (the e^{-2phi}, e^{+2phi} factors cancel against g^{mu nu} and the
gradient structure). This is the global-monopole / solid-angle-deficit
stress, here DERIVED from our n-field, not posited.

## TASK 4 — THE EOS TEST: p_r + rho

  p_r + rho = (-xi/r^2) + (xi/r^2) = 0    EXACTLY.

[PASS] p_r + rho == 0 IDENTICALLY for the hedgehog n=x/r, INDEPENDENT of
phi(r) and of r. The equation of state p_r = -rho holds IDENTICALLY for the
radial-winding (degree-1) configuration.

GPU confirmation (angular_lagrangian_gpu_spotcheck.py, V100 float64): over
4096 random points in (r, theta, phi, phi(r)),
  max |p_r + rho| = 0.000e+00   (machine zero),
  max |p_theta| = 3.6e-15, max |rho - xi/r^2| = 7.1e-15.
CPU per-point assert PASSED (<1e-12).

SCOPE / the exact obstruction for non-hedgehog n: it is SPECIAL to n=x/r.
For a radial twist Theta=Theta(r) the same construction gives
  p_r + rho = xi e^{-2phi} (Theta'(r))^2  >= 0,
vanishing IFF Theta'(r)=0 (pins the hedgehog) [PASS]. So p_r=-rho is a
THEOREM of the radial-winding (pure-transverse) configuration and FAILS the
moment the winding map acquires a radial profile (d_r n != 0). The
hedgehog's vanishing radial gradient is exactly why its only stress is the
transverse winding, which the metric reads as p_r=-rho.

## TASK 5 — THE ANTI-SMUGGLING ANCHOR (native vs textbook import)

The decisive check. The project's anisotropy mode (dpf2_results.md:30-41;
exterior_cavity_results.md:47) is f = F(1 + kappa cos theta), with derived
angular potential P = (3 a^2/8F) G1, a = F kappa/sqrt3,
  G1 = (2k + (k^2-1) L)/k^3,   L = ln((1+k)/(1-k)),
  H(kappa) := -2 P_F = L/(2k) - 1 = kappa^2/3 + kappa^4/5 + kappa^6/7 + ...

On the kappa-deformed sphere the metric factor 1/g_theta-theta carries
1/(1+kappa cos theta). Reducing the SAME degree-1 hedgehog TRANSVERSE
winding energy sin^2(Theta)/g_thth (Theta=theta) over the deformed sphere
gives the angular reduction integral
  I_native(kappa) = INT_0^pi sin^3(theta)/(1 + kappa cos theta) dtheta.

RESULT — IT MATCHES G1 EXACTLY:
  I_native(kappa) == G1(kappa).
Verified by mpmath (dps=40) and GPU trapezoid at kappa = 0.1, 0.3, 0.5,
0.683095, 0.9: |I_native - G1| <= 6.7e-14 (and exact-to-rounding, 0.0e+00,
at several points). [The symbolic `==` in angular_lagrangian_derive.py
printed FAIL — that is a sympy log-branch (Piecewise kappa>1) artifact, NOT
a real mismatch; the series and the 14-41-digit numeric agreement disprove
it.] The leading coefficient: kappa^2 G1 -> (4/3) kappa^2, and the charge
functional H = -2 P_F has leading term kappa^2/3 [PASS — matches the banked
dpf2/exterior_cavity anchor exactly].

CONCLUSION OF THE ANCHOR: our constructed angular Lagrangian, reduced on the
project's own anisotropy mode, REPRODUCES the project's own derived G1 /
H(kappa) functional EXACTLY (not just to leading order — the entire closed
form). The angular sector we wrote IS the project's own monopole functional;
it is NATIVE, not a textbook import. By the pre-registered rule of TASK 5,
this means the p_r=-rho result of TASK 4 is established by a native object.

## TASK 6 — BACK-REACTION (is G^theta_theta intact? does B=1/A survive?)

The UDT metric Einstein tensor (sympy, exact):
- G^t_t - G^r_r = 0 IDENTICALLY [PASS] — the geometry side of B=1/A; the
  metric already enforces G^t_t = G^r_r.
- G^theta_theta = e^{-2phi}(2 r phi'^2 - r phi'' - 2 phi')/r — the equation
  that fixes g_rr = e^{2phi}.

The hedgehog source has T^theta_theta = 0. Sourcing G^mu_nu = kappa8 T^mu_nu
(kappa8 = 8 pi G/c^4):
- The theta-equation reads G^theta_theta = kappa8 * 0 = 0 — IDENTICAL to the
  vacuum theta-equation, so it continues to enforce the relation that gives
  g_rr = e^{2phi}. The angular source enters ONLY the t/r block, NOT the
  theta-equation that pins g_rr. [intact]
- Because T^t_t = T^r_r (TASK 3) matches the metric identity G^t_t = G^r_r,
  the t- and r-equations COLLAPSE to ONE equation; consistency is automatic.
- Solving the t-equation G^t_t = -kappa8 xi/r^2 gives
  e^{-2phi} = 1 - kappa8 xi - rs/r  — a SOLID-ANGLE DEFICIT (1 - kappa8 xi)
  on top of Schwarzschild: the global-monopole metric, with g_tt g_rr = -c^2
  preserved inside matter.

So B=1/A survives inside matter with this source: the source is exactly of
the type the metric identity demands (T^t_t=T^r_r), and it leaves the
g_rr-fixing theta-equation untouched (T^theta_theta=0).

---

## PREMISE LEDGER (every chosen vs derived item)

DERIVED (forced by our objects / the metric / general covariance):
- D1. Field = unit 3-vector n_a, target S^2; winding = omega_H1, INT=4pi;
  N=3, q=1/3. (h1_types:31-37,159-164)
- D2. Hedgehog n=x/r is the degree-1 generator; winding integral = 1.
  (verified)
- D3. The gradient object (d_mu n_a)(d_nu n_a) is the unique 2-derivative,
  diffeo + target-isometry scalar; omega_H1 carries no metric => no stress.
- D4. Contraction with UDT g^{mu nu} and the sqrt(-g)=c r^2 sin theta
  measure is forced by covariance + the UDT metric (phi cancels in sqrt-g).
- D5. T^t_t = T^r_r = -xi/r^2, T^theta_theta = 0 (exact sympy + GPU).
- D6. p_r + rho = 0 identically for n=x/r, phi-independent (exact + GPU 0.0).
- D7. p_r+rho = xi e^{-2phi}(Theta')^2 for radial twist (the exact
  obstruction; vanishes iff Theta'=0). 
- D8. I_native = INT sin^3/(1+k cos) == G1 (the project's own functional) —
  the native anchor MATCH (mpmath/GPU exact).
- D9. G^t_t = G^r_r identically (metric); theta-equation unchanged by the
  T^theta_theta=0 source => B=1/A preserved inside matter.

CHOSEN (modeling choices, flagged loudly):
- C1. The MINIMAL two-derivative kinetic term, no potential, NO Skyrme
  (higher-derivative) term. The leading-order sigma model. [If a Skyrme or
  potential term were added it would generically give T^theta_theta != 0
  and could perturb the EOS — see attack-here.]
- C2. The prefactor sign and normalization -(xi/2); xi the single coupling
  (cancels in the EOS and in the G1 ratio; sets the deficit magnitude).
- C3. The identification that the dpf anisotropy mode f=F(1+kappa cos th)
  enters the angular reduction as the metric factor 1/(1+kappa cos th)
  multiplying the transverse winding energy. [This is the physically natural
  reading and it is VINDICATED by the exact G1 match (D8) — but the mapping
  itself is a reading, not a separate derivation.]

NOT CLAIMED: no mass, no ratio, no wall-number comparison (data-blind held);
no discrete TYPE family asserted (this is the EOS/B=1/A question, orthogonal
to the rigid-type verdict of h1_types); the Skyrme/multi-soliton sector is
untouched.

## VERDICT (honest, one paragraph)

B=1/A inside matter is DERIVED by this route, for the radial-winding
(degree-1 hedgehog) configuration of UDT's own n-field. The angular sector,
built minimally from the metric measure acting on the n-field whose winding
is omega_H1, produces T^t_t = T^r_r = -xi/r^2 and T^theta_theta = 0, hence
p_r + rho = 0 EXACTLY and phi-independently (sympy-exact and GPU machine-zero
over 4096 points). This is precisely the source the geometric identity
g_tt g_rr=-c^2 <=> G^t_t=G^r_r <=> p_r=-rho demands, and it leaves the
g_rr-fixing theta-equation intact, so B=1/A survives inside matter as a
theorem. The result is NATIVE, not a textbook import: the constructed
Lagrangian, reduced on the project's OWN kappa-anisotropy mode, reproduces
the project's OWN derived functional G1 / H(kappa)=kappa^2/3+... EXACTLY
(the full closed form, mpmath/GPU-confirmed), which is the pre-registered
anti-smuggling pass. The result is PARTIAL/SCOPED in exactly one way: it
holds for the pure radial-winding configuration; a radial twist Theta(r)
re-introduces p_r+rho = xi e^{-2phi}(Theta')^2 >= 0 and breaks the EOS — so
"B=1/A inside matter" is a theorem of the hedgehog/topological sector
specifically, conditional on the minimal (no-Skyrme, no-potential) model
choice C1. Within that scope it is a clean derivation, and it is the first
place in the corpus where the defining UDT relation g_tt g_rr=-c^2 is shown
to be SOURCED (not just postulated) by a derived UDT object.

---

## WHAT THE BLIND VERIFIER SHOULD ATTACK HARDEST

1. THE MINIMAL-MODEL CHOICE C1 (the load-bearing premise). Does adding a
   Skyrme term (the natural next term for a stable finite soliton) or a
   potential break T^theta_theta=0 and hence p_r=-rho? The hedgehog's
   p_r=-rho rides on the pure two-derivative sigma model. A Skyrme term
   ~ (n x dn)^2 generically sources T^theta_theta != 0 — verify whether it
   ALSO preserves T^t_t=T^r_r (some topological terms do) or breaks B=1/A.
   If the stable soliton NEEDS Skyrme, the EOS scope narrows.
2. THE ANCHOR MAPPING C3. Confirm independently that the dpf
   f=F(1+kappa cos th) deformation enters as 1/(1+kappa cos th) in the
   transverse winding reduction (vs some other power), since the EXACT G1
   match (the native verdict) rides on this. The mpmath/GPU match of
   I_native to G1 is strong evidence, but reproduce the reduction from the
   dpf P(F,a) side to close the loop fully.
3. THE radial-twist obstruction D7. Verify p_r+rho = xi e^{-2phi}(Theta')^2
   independently, and whether any PHYSICAL hedgehog profile (regular core ->
   vacuum) must have Theta'!=0 somewhere, which would make p_r=-rho an
   ASYMPTOTIC/leading statement rather than an exact-everywhere one for a
   realized soliton. (For the pure topological n=x/r it is exact; for a
   smoothed-core soliton it may hold only outside the core.)
4. THE sympy "[FAIL]" on Inative==G1. Re-confirm (as done here by mpmath
   dps=40 and GPU) that this is purely a log-branch artifact and the
   integral genuinely equals G1 on (0,1), not a hidden mismatch.

---

## DATA-BLIND CONFIRMATION

No lepton/hadron wall numbers loaded, matched, or consulted in any script or
in this document. No count or ratio was imported. The push was METRIC-LED
(interrogating whether the derived n-field sources the defining UDT relation
g_tt g_rr=-c^2), not template-led. The global-monopole Lagrangian was NOT
lifted from memory and called native: the two-derivative form was argued as
the unique minimal covariant object (D3-D4) and then VINDICATED as native by
the exact reproduction of the project's own G1 functional (D8) — that
reproduction, not an appeal to the textbook, is what licenses calling it the
project's own angular Lagrangian.

---

## VERIFIER-CLEARED (appended 2026-06-14; supersedes the "PENDING" line above)

Blind adversarial verifier (Claude Opus 4.8, agent a4edbefa0e29edfa2,
2026-06-14; angular_lagrangian_verifier_results.md) independently re-derived
every claim with its own sympy/mpmath/torch machinery (constructor scripts
NOT trusted). VERDICT: **STANDS.**
- Anchor C3 (the decisive one): **GENUINE / NATIVE, not reverse-engineered.**
  The integrand sin^3/(1+kappa cos) is the 1/f warp ALREADY PRESENT in the
  project's own dpf density f_theta^2/(4f) (rescued_workspaces/2026-06-11/
  verify_x1/v_c1_closedforms.py:90-99, predating this push); I_native == G1
  to ~1e-48. Non-circular.
- p_r+rho = 0 (hedgehog): CONFIRMED exact, phi-independent, GPU machine-zero.
- Verifier STRENGTHENING: T^t_t = T^r_r holds for ANY purely-angular config
  (no radial gradient), not just the hedgehog; and the EOS is ROBUST (not
  fragile) to native Skyrme/potential additions — they preserve T^t_t=T^r_r
  (changing only T^theta_theta and the deficit value, never the g_tt g_rr=-c^2
  identity, which rides solely on T^t_t=T^r_r).
- Off-hedgehog obstruction C2 + back-reaction C4: CONFIRMED, correctly scoped.

TWO NON-BLOCKING ERRATA (recorded; do not touch the load-bearing chain):
- E1. PROSE conflation of G1 and H. The genuine banked anchor identity is
  I_native == G1 (the bare integral; G1(0)=4/3). H(kappa) = -2 P_F =
  kappa^2/3 + ... is a DOWNSTREAM derivative of P (H(0)=0), a different
  object. The load-bearing claim (the n-field reduction reproduces the
  project's OWN derived G1, exactly) is correct; the sentence at lines
  139-141 mixing "G1 -> (4/3)kappa^2" with "H = kappa^2/3" is loose wording.
- E2. The deficit solution's sign on the solid-angle term (1 - kappa8 xi vs
  1 + kappa8 xi) is a deficit-vs-surplus sign-of-xi/normalization convention;
  the structural result (g_tt g_rr=-c^2 survives; solid-angle + Schwarzschild
  form) is identical either way.
