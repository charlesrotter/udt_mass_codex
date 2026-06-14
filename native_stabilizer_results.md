# Native Stabilizer for the Angular Soliton — Results

Date: 2026-06-14. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **DERIVE** (gated,
foundation-securing — authorized by Charles). Frame: CRITICAL_UNIVERSE_FRAME.md
/ CATALOG_FRAME.md / CANON C-2026-06-14-1. **DATA-BLIND, foundation-scoped** —
NO particle mass, ratio, or wall number loaded, computed, or compared. Sizes
are reported only in units of the intrinsic length L = sqrt(kappa/xi).

THE QUESTION (gated, authorized): does UDT's OWN structure provide a NATIVE
stabilizer term for the angular soliton (one that evades Derrick collapse and
pins a definite SIZE), or are the textbook stabilizers (Skyrme term, potential)
only imports? Per charter: an import is a HYPOTHESIS about a native object — if
it FALLS OUT of our objects it named something real; if not, drop it.

Scripts (commit-grade, this push):
- `native_skyrme_derive.py` — Task 1, sympy CPU symbolic identity.
- `native_derrick_derive.py` — Task 2, sympy CPU Derrick scaling + EOS prep.
- `native_profile_bvp.py` — Tasks 2/3, V100 torch float64 + scipy BVP +
  mpmath deep-phi anchors. Log: `/tmp/native_profile_bvp.log`.
- `native_potential_check.py` — Task 4, sympy CPU.

Blind verifier: **PENDING** (verifier-before-record discipline; attack-here
block at the end).

Prior context (given, blind-verified earlier): coupled_cell_soliton_results.md
(B3b: minimal two-derivative L2 angular hedgehog Derrick-COLLAPSES, both terms
~lambda^1, no sized soliton — NEGATIVES_REGISTRY #43); h1_types_results.md
(omega_H1 = eps_abc n_a dn_b ^ dn_c the N=3/q=1/3 winding 2-form; eta=q/6=1/18
the seal/transgression action density). Metric: ds^2 = -e^{-2phi}c^2 dt^2 +
e^{2phi}dr^2 + r^2 dOmega^2; sqrt(-g)=c r^2 sin theta.

---

## TASK 1 — IS THE SKYRME TERM NATIVE? (the make-or-break) — **YES, DERIVED**

We do NOT lift the textbook Lagrangian. We build TWO objects and test whether
they are the same.

(A) Our OWN derived winding/topological current 2-form (from omega_H1):
        F_{mn} = eps_{abc} n_a d_m n_b d_n n_c  =  n . (d_m n x d_n n)
    [a SCALAR-valued antisymmetric 2-form, the metric-free triple product;
     this is exactly the H1 area-form current, omega_H1 components.]
    Its UDT-metric norm:  |F|^2_g = g^{mp} g^{nq} F_{mn} F_{pq}.

(B) The standard Skyrme/Faddeev four-derivative term for a unit 3-vector:
        S_{mn} = d_m n x d_n n   [a 3-VECTOR-valued antisymmetric 2-form]
        L4_std = -(kappa/4) g^{mp}g^{nq} S_{mn} . S_{pq}.

**Derived pointwise identity (sympy, exact, all 4x4x4x4 index pairs):**
On the constraint surface |n|=1 (=> d_m n _|_ n, so each d_m n lies in the
tangent 2-plane to S^2 at n), the Lagrange identity (a x b).(c x d) =
(a.c)(b.d) - (a.d)(b.c) collapses to

        **S_{mn} . S_{pq} == F_{mn} F_{pq}     for ALL m,n,p,q.**

(Reason: with n the unit normal and d_m n tangent, |d_m n x d_n n| = the area
spanned = |n . (d_m n x d_n n)|; the vector cross product is parallel to n, so
its self-contraction equals the squared scalar triple product. Verified
symbolically, not asserted — `native_skyrme_derive.py` step [2] returns True.)

**Metric contraction (sympy, exact):** with the UDT inverse metric
g^{mn} = diag(-e^{2phi}/c^2, e^{-2phi}, 1/r^2, 1/(r^2 sin^2 th)),

        g^{mp}g^{nq} F_{mn}F_{pq}  -  g^{mp}g^{nq} S_{mn}.S_{pq}  ==  0.

Therefore:

        **L4_std = -(kappa/4) |omega_H1 winding current|^2_g.**

**VERDICT (Task 1): the Skyrme four-derivative term IS the UDT-metric norm of
our OWN derived H1 winding current omega_H1, up to the (kappa/4) normalization.
It is NATIVE.** The "Skyrme import" named a real UDT object: the squared
topological current of the omega_H1 area form, contracted with the UDT inverse
metric. We keep the native version. (chose: the overall coefficient kappa>0 and
its (1/4) convention — a normalization, not a mechanism. derived: that the term
equals |omega_H1|^2_g.)

---

## TASK 2 — DERRICK / STABILIZATION IN THE UDT METRIC — **SIZED SOLITON EXISTS**

Ansatz (derived carrier): unit-3-vector ell=1 hedgehog with radial profile,
n = (sinTheta(r) sinth cosph, sinTheta(r) sinth sinph, cosTheta(r)); winding
2-form = omega_H1; charge 1 fixed by Theta(core)=pi -> Theta(seal)=0.

**Proper-energy functionals on the UDT static slice (sympy, honest e^{phi}
measure; native_derrick_derive.py):** with sqrt(g)=e^{phi} r^2 sin th,
- E2_r = (2pi xi/3) e^{-phi} [ r^2 sin^2Theta Theta'^2 + 2 r^2 Theta'^2
         + 4 e^{2phi} sin^2Theta ]                              (the #43 L2)
- E4_r = (2pi kappa/3) e^{-phi} [ (2 r^2 sin^4Theta + 2 r^2 sin^2Theta)Theta'^2
         + e^{2phi} sin^4Theta ] / r^2                          (the NATIVE L4)

**Derrick scaling Theta(r) -> Theta(r/lambda) (sympy, exact, flat phi=const):**

        **E2(lambda) ~ lambda^{+1},   E4(lambda) ~ lambda^{-1}.**

So E(lambda) = A lambda + B/lambda with A,B > 0. Then
        dE/dlambda = A - B/lambda^2 = 0  =>  lambda* = sqrt(B/A) > 0,
        E''(lambda*) = 2B/lambda*^3 > 0  =>  a STABLE minimum.

The minimal L2-only model had BOTH terms ~lambda^1 (monotone, collapse,
NEGATIVES_REGISTRY #43). The NATIVE L4 supplies the missing lambda^{-1} branch.
**A finite preferred size now EXISTS where the minimal model collapsed.** The
e^{2phi} factors multiply A and B and SHIFT lambda* but (both being positive)
do NOT remove the minimum. (chose: nothing here — exponents derived. The
constant-phi count is the clean theorem; deep-phi is solved numerically below.)

**Actual profile BVP solved (V100 torch float64 + scipy solve_bvp, rms residual
~1e-8; native_profile_bvp.py):**

- **Flat background (phi=0):** a NON-TRIVIAL stabilized profile Theta(r)
  interpolating pi->0 EXISTS and minimizes E. Half-twist radius (Theta=pi/2)
  in units L=sqrt(kappa/xi): (w-r_core)/L = 0.62, 0.65, 0.67, 0.68 for
  kappa = 0.25, 1, 4, 9 (mean 0.652, std 0.024). **The soliton width tracks
  sqrt(kappa/xi)**, the ONLY length in the problem. Cell-size independent:
  (w-rc)/L holds at 0.645->0.648 as the cell grows from 8L to 40L.

- **Virial / Derrick on the actual numeric solution:** E2(lambda)/lambda and
  E4(lambda)*lambda are constant to all printed digits; E2 lambda + E4/lambda
  minimizes at lambda = 1.000; the BVP sits on the stationary point. **Virial
  E2 = E4 holds (E2/E4 = 1.005 at xi=kappa=1, ~1.00 across the kappa scan).**

- **Deep-phi background phi = -p ln(r_int/r), p = 0.5, 1, 2:** the stabilized
  soliton SURVIVES. The e^{-phi}/e^{2phi} weights stiffen the deep core and push
  the twist OUTWARD: (w-rc)/L = 0.65 -> 1.31 -> 2.52 -> 6.18 for p = 0, 0.5, 1,
  2 (phi_core = 0, -2.74, -5.48, -10.97). In curved background the Derrick
  exponents shift with the e^{phi} weights so E2=E4 no longer holds
  (E2/E4 = 1.01 -> 1.99 -> 4.35 -> 31.6) — EXPECTED (the metric reweights the
  virial), not a failure: the BVP is still the stationary profile of the
  curved-background functional (residual ~1e-8). mpmath dps=40 anchors confirm
  float64 is exact at these depths (rel-err ~1e-16, r_int/r_core=240, p<=2);
  deeper cells need mpmath.

**VERDICT (Task 2): with the native L4 the angular soliton has a STABLE finite
size lambda* = sqrt(B/A), set by the ratio kappa/xi and the geometry. A sized
soliton EXISTS where the minimal (#43) model Derrick-collapsed.** Exponents:
E2 ~ lambda^{+1}, E4 ~ lambda^{-1} (flat); reweighted but still bounded with a
minimum in deep-phi.

---

## TASK 3 — THE EOS INTERPLAY (B=1/A) — softens with the profile; honest map

**Full diagonal stress tensor derived (L2 + native L4; native_profile_bvp.py,
numeric match to 5.7e-14).** With X = e^{-2phi} Theta'^2 and Y = sin^2Theta/r^2,
and rho = -T^t_t, p_r = T^r_r:

    rho  = (xi/2)(X + 2Y) + (kappa/2)(2XY + Y^2)
    p_r  = (xi/2)(X - 2Y) + (kappa/2)(2XY - Y^2)

    **p_r + rho = X (xi + 2 kappa Y)
                = e^{-2phi} Theta'^2 (xi + 2 kappa sin^2Theta / r^2)  >= 0.**

The xi*X piece exactly reproduces the banked CANON D7 obstruction
(p_r+rho|_L2 = xi e^{-2phi} Theta'^2); the native L4 ADDS the 2 kappa X Y piece
(both >= 0). So p_r+rho is controlled by X = e^{-2phi} Theta'^2 — it vanishes
iff Theta' = 0.

**EOS MAP — the naive "soften only in the core" expectation is INVERTED; report
carefully (OBSERVED, not targeted):** (p_r+rho)/rho is governed by the ratio
X/Y (radial gradient vs angular curvature): X >> Y => ratio -> 2 (max soft);
X << Y => ratio -> 0 (exact). On the actual flat solution **Theta' never
vanishes anywhere inside the finite cell, so the EOS B=1/A (g_tt g_rr = -c^2) is
SOFTENED EVERYWHERE in the cell — there is NO exact interior region.** The
softening is non-monotone: (p_r+rho)/rho dips to its MINIMUM 1.13 at
(r-rc)/L ~ 0.41 (the inner shoulder where the twist concentrates and the
angular curvature Y dominates, X<Y over (r-rc)/L in [0.12, 0.56]), and rises to
2.00 BOTH at the core (Theta' large) AND in the gradient-dominated exterior
tail. Deep-phi (p=1) shows the same qualitative pattern (softened across the
cell, peak 2.00).

**Where B=1/A holds EXACTLY:** only where Theta' truly flatlines — i.e. the
sealed/trivial exterior Theta == 0 (the body/exterior once the twist has fully
unwound), a BOUNDARY/seal condition, NOT an interior one. The smooth pi->0 BVP
profile never reaches Theta'=0 strictly inside the finite cell, so EOS exactness
is a seal question. **This refines the picture: the stabilized profile does not
hand back a clean B=1/A body; B=1/A is exact only in the unwound exterior, and
the entire twisted core+shoulder is EOS-softened (1.13 <= (p_r+rho)/rho <= 2).**
(This is a faithfully reported surprise — the prior B3a pure-hedgehog had
p_r=-rho EXACT because Theta=theta gave Theta'=0 in r; introducing a genuine
radial profile necessarily softens, as CANON D7 already warned.)

---

## TASK 4 — NATIVE POTENTIAL CANDIDATE — **NO bulk potential falls out**

Candidate: the seal action density eta = q/6 = 1/18, tied to the transgression
Xi = dTheta_transgression (h1_types_results.md). **Test (sympy,
native_potential_check.py):** Xi = dTheta is EXACT (it has the global primitive
Theta_transgression = (ln f) omega_H1); by Stokes its ENTIRE content is the
boundary (seal) value D = 4pi (ln f)_seal. A Lagrangian piece that is a total
derivative has IDENTICALLY ZERO bulk Euler-Lagrange contribution (verified:
EL[d/dr G(Theta,r)] = 0 symbolically).

**VERDICT (Task 4): eta is STRICTLY a boundary/seal (junction-closure) object,
NOT a bulk potential.** It does not supply a Derrick-style V(n) that pins the
hedgehog orientation in the bulk. The native stabilizer is the winding-current
(Skyrme) term of Task 1, NOT a potential. No metric-derived bulk V(n) was found
to fall out. (Negative, first-class: the potential import did NOT name a native
bulk object; eta's real native role is the seal closure, a different sector.)

---

## TASK 5 — THE STRUCTURAL PAYOFF (report only; NO mass/ratio extracted)

With the native L4, the soliton SIZE is **PINNED**: lambda* = sqrt(B/A), set by
the ratio kappa/xi and the metric geometry (flat: width ~ 0.65 sqrt(kappa/xi);
deep-phi: reweighted outward but still finite and bounded). This replaces the
free continuum of the minimal model (#43, where size was an unpinned dial). This
is the foundation-securing result: **the metric's own winding-current term gives
the angular particle a DETERMINED size**, not a free one.

DATA-BLIND HELD: no particle mass, no ratio, no wall number was computed,
loaded, or compared. Sizes are in units of L = sqrt(kappa/xi) only.

DISCRETENESS NOTE (do NOT hunt — gated): the size is pinned by the CONTINUOUS
ratio kappa/xi; nothing discrete appeared in this push (one charge-1 soliton,
one size per (kappa,xi,cell)). Whether a DISCRETE family emerges (e.g. from
charge-N towers, seal quantization, or phi-angular coupling) is a separate gated
question, explicitly NOT pursued here.

---

## PREMISE LEDGER (chose vs derived)

DERIVED (fell out of UDT objects / exact symbolic / solved BVP):
- Skyrme L4 = |omega_H1 winding current|^2_g, exactly, all index pairs [Task 1].
- E2 ~ lambda^{+1}, E4 ~ lambda^{-1} (flat); stable minimum lambda*=sqrt(B/A)
  [Task 2].
- Existence + width ~ sqrt(kappa/xi) of the flat stabilized profile; survival
  and outward shift in deep-phi; virial E2=E4 (flat) [Task 2, BVP].
- p_r+rho = e^{-2phi}Theta'^2 (xi + 2kappa sin^2Theta/r^2); L2 piece = CANON D7;
  L4 piece = 2kappa X Y [Task 3].
- EOS softened wherever Theta' != 0; exact only in unwound exterior (Theta'=0)
  [Task 3].
- eta is a total-derivative (seal) object, zero bulk EL => no bulk potential
  [Task 4].

CHOSE (provisional, tagged; none is a smuggled mechanism):
- kappa > 0 and its (1/4) normalization convention [Task 1] — a coefficient,
  not a mechanism; sets the SCALE of L but not the existence of a minimum.
- xi > 0 (the L2 coupling, inherited from #43) [given].
- Charge-1 BC Theta(core)=pi, Theta(seal)=0 (the omega_H1 winding=1 carrier)
  [derived as the N=3/q=1/3 carrier; the specific pi->0 endpoints are the
  charge-1 hedgehog choice].
- Background phi: flat (theorem) and the deep-cell log phi=-p ln(r_int/r)
  with p=0.5,1,2 (the #41/B1 cell profile) [the log form is the derived deep
  cell; p is the cell depth dial, chosen for the scan].
- Finite cell [r_core, r_int] with r_int/r_core=240 in the BVP [the finite-cell
  canon; the ratio is a numeric choice, results are cell-size-independent in L].
- Static slice (dropped t); hedgehog ell=1 ansatz [the derived carrier].

---

## HONEST VERDICT

**A native stabilizer IS derived.** The Skyrme four-derivative term is not an
import in disguise — it IS the UDT-metric norm of our own derived omega_H1
winding current (Task 1, exact). With it, the angular soliton acquires a STABLE,
PINNED finite size lambda* = sqrt(B/A) ~ sqrt(kappa/xi) (Task 2, derived
exponents + solved BVP), curing the #43 Derrick collapse. The native potential
candidate (eta) does NOT supply a bulk stabilizer — it is strictly a seal/
boundary object (Task 4, negative). So: ONE native stabilizer (the winding-
current term), and it pins a size. The foundation question — "is the sized
particle a real native object or only an import" — is answered: **NATIVE, and it
pins a size.** Caveat carried honestly: the stabilized radial profile SOFTENS
the B=1/A EOS everywhere it twists (Task 3); B=1/A is exact only in the unwound
exterior. This is a real structural consequence of giving the soliton a profile,
recorded, not buried.

---

## BLIND VERIFIER — PENDING. ATTACK HERE:

1. **Task 1 identity:** re-derive S_{mn}.S_{pq} vs F_{mn}F_{pq} on a fully
   GENERAL n(x) WITHOUT pre-projecting to the tangent plane (carry the
   constraint |n|=1 and n.d_m n=0 as side relations, then simplify). Confirm the
   identity is NOT an artifact of the {n,e1,e2} basis choice. Check the metric
   contraction with a NON-DIAGONAL test metric to confirm g^{mp}g^{nq} placement
   is correct. Confirm L4_std normalization convention (some texts use 1/4, some
   1/2, some 1/32) does not change "native vs not" (it does not — only the
   coefficient).
2. **Task 2 Derrick:** confirm E2~lambda^1, E4~lambda^-1 INDEPENDENTLY (different
   ansatz parametrization). Re-solve the BVP with an independent solver (e.g.
   relaxation or a different shooting code) and confirm width ~ sqrt(kappa/xi)
   and virial E2=E4 (flat). Stress the deep-phi survival claim at larger p
   (p=3,4) with mpmath — does the minimum persist or does the outward shift run
   the twist off the cell?
3. **Task 3 EOS:** re-derive T^m_n by varying the action w.r.t. the metric
   (Hilbert tensor), NOT from the hedgehog formula, and confirm p_r+rho =
   e^{-2phi}Theta'^2(xi+2kappa sin^2Theta/r^2). Confirm the "softened everywhere"
   claim is a genuine consequence of Theta' never vanishing, not a BC artifact —
   try a profile that DOES flatten in a body region and check EOS recovers.
4. **Task 4:** confirm eta/the transgression is genuinely total-derivative and
   that NO other UDT object (curvature scalar, seal density, phi-gradient term)
   supplies a bulk V(n) with the right Derrick scaling (lambda^{+3}). Look for a
   smuggled-out native potential.
5. **Frame:** is the charge-1 pi->0 BC the only native choice, or does the seal
   mirror-fold (sigma-even Neumann / sigma-odd Dirichlet) permit a DIFFERENT
   endpoint that changes existence? Is sqrt(kappa/xi) the ONLY length, or did a
   hidden scale (cell size, r_core) sneak into the "pinned size" claim?

---

## VERIFIER-CLEARED (appended 2026-06-14; supersedes the PENDING line)

Blind adversarial verifier (Claude Opus 4.8, agent a1f2213b6410a6f35,
2026-06-14; native_stabilizer_verifier_results.md + native_stabilizer_verif_*.py)
independently re-derived all five claims (own sympy / EL / scipy BVP / Hilbert
stress; constructor scripts NOT run). VERDICT: STANDS.
- (1) Skyrme term == |omega_H1 current|^2_g: CONFIRMED on |n|=1 (S_mn.S_pq ==
  F_mn F_pq all 256 index pairs; metric contraction == to machine zero for the
  UDT-diagonal AND a random non-diagonal metric — not a basis artifact). The
  stabilizer is NATIVE: the metric-norm of our own derived H1 winding current.
- (2) Sized soliton: CONFIRMED. E2~lambda^{+1}, E4~lambda^{-1} => stable
  lambda*=sqrt(B/A); kappa->0 reproduces the #43 collapse; charge-1 BVP gives
  a non-trivial profile, width ~ sqrt(kappa/xi), cell-size-independent, virial
  E2=E4 (0.9999), deep-phi survival p=0..4.
- (3) EOS inversion: CONFIRMED + consistent with canon C-2026-06-14-1 scope.
  p_r+rho = e^{-2phi}Theta'^2(xi + 2 kappa sin^2 Theta/r^2) >= 0, = 0 iff
  Theta'=0; for the monotone pi->0 profile Theta'!=0 throughout, so B=1/A is
  exact ONLY in the unwound exterior. REFINES (does not contradict) the canon.
- (4) Native potential: NO — eta=1/18 is the exact transgression (total
  derivative, zero bulk EL); a seal/boundary object, not a bulk V(n).
- (5) ONE scale: size pinned by the single ratio kappa/xi; no second tunable.
Non-blocking convention diffs (flat width 0.876 vs 0.652; deep-phi twist
direction sign-of-phi chart; the clean p_r+rho formula is the equatorial/1D
reduction of the raw 4D Hilbert stress) — none touch the load-bearing chain.
