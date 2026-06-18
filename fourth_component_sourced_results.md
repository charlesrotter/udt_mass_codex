# Is the FOURTH field component SOURCED, or a PASSENGER? — Results

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit). Mode: **OBSERVE / adversarial audit** (decisive
category-A symbolic+analytic check). **DATA-BLIND** — no particle mass,
ratio, or wall number loaded, computed, or compared. Sizes in units of
L = sqrt(kappa/xi) only. Blind verifier: **PENDING** (attack block at end).

THE QUESTION: the catalog carrier is the unit 4-vector S^3 (SU(2)/Skyrme,
pi_3 baryon charge), adopted in `matter_ansatz_derive.py` (2026-06-15) and
tagged "DERIVED". But the CANONIZED native derivation (C-2026-06-14-1,
`native_stabilizer_results.md` / `native_skyrme_derive.py`) is a unit
3-vector S^2 (omega_H1 = eps_abc area form, pi_2 degree, N=3 because eps_abc
needs exactly 3 components). Is the 4th component n_4 = cosTheta genuinely
SOURCED by the metric/action (=> S^3 real, catalog stands), or an unsourced
PASSENGER (=> native object is S^2, S^3 is an import, catalog re-grade)?

Scripts (commit-grade, this push):
- `fourth_component_sourced_check.py` — Tasks 1,2 (Theta-EL + Theta=pi/2 test).
- `fourth_component_regularity_energetics.py` — Tasks 3,4 (regularity + energetics).
- `fourth_component_adversary.py` — break the verdict (3 attacks).
- numeric cross-check vs committed `complete_metric_batched.theta_ddot`.

Method note: used the EXACT committed objects — the L2/L4 forms and stress()
from `matter_ansatz_derive.py` and `complete_metric_batched.py`, and confirmed
the derived Theta-EL is the SAME equation the engine integrates (theta_ddot).

---

## TASK 1 — the Theta(r) Euler-Lagrange ODE (derived, exact sympy)

From S = INT (L2+L4) sqrt(-g) d^4x with the S^3 hedgehog n4 = (sinTheta sinth
cosps, sinTheta sinth sinps, sinTheta costh, cosTheta), |n4|=1 (verified):

  EL[Theta] ∝  -2kappa r^2 sin^2Theta · Theta''  - r^4 xi · Theta''
               + [Theta'^2 terms in sin(2Theta)] + 4kappa r^2 sin^2Theta Theta' phi'
               - 2 r^3 xi Theta' (... + phi' terms)
               + 2 r^4 xi e^{2phi} sin(2Theta)
               + 2 kappa e^{2phi} sin^3Theta cosTheta   = 0

The two "potential" (gradient-free) source terms are
  **2 r^4 xi e^{2phi} sin(2Theta)  and  2 kappa e^{2phi} sin^3Theta cosTheta.**
These are EXACTLY the source terms in the committed engine `theta_ddot`
(`m^2·2 r^2 xi e^{2phi} sin(2Theta)` and `m^2·2 kappa e^{2phi} sin^3 cos`) —
so the derived EL IS the equation the solver integrates.

## TASK 2 — Theta == pi/2 (n_4 = cosTheta = 0) test — **SATISFIED IDENTICALLY**

Substituting Theta == pi/2 (=> Theta' = Theta'' = 0):

  **Theta-EL |_{Theta=pi/2} == 0   (exact, sympy simplify).**

Both the L2-only part (kappa->0) and the L4-only part (xi->0) vanish
SEPARATELY. The mechanism is structural: every Theta-source term carries a
factor sin(2Theta) or sin^3Theta cosTheta, all of which vanish at Theta=pi/2.
Numeric cross-check against the committed `theta_ddot` in a deep-phi
background: |Theta''| = 3e-11 (finite-difference noise; symbolically 0).

> **n_4 == 0 is a CONSISTENT BULK solution. The equation of motion does NOT
> force the 4th component.** The bulk EOM is the decisive test, and it does
> not source n_4.

## TASK 3 — core regularity fork — **finite cell REMOVES the pressure**

At Theta=pi/2 the texture density is rho(pi/2) = (kappa/2 + r^2 xi)/r^4, and
the radial energy integrand rho·r^2 = xi + kappa/(2r^2).
- (a) On a domain reaching r=0: INT kappa/(2r^2) dr ~ kappa/(2a) -> +inf as
  a->0. Strict-origin regularity WOULD force the sweep (Theta(0)=pi => Y(0)=0).
- (b) But the COMMITTED UDT cell has a FINITE inner radius **r_core = 0.05 > 0**
  (`complete_metric_sweep_stageA.py`: `rc = 0.05`), with Dirichlet ends
  Th(core)=m·pi, Th(seal)=0. At r_core=0.05 the integrand is FINITE
  (= 200 kappa + xi). **The r->0 divergence is OUTSIDE the cell. Regularity
  pressure is removed; Theta==pi/2 is perfectly regular on the finite cell.**

The finite-cell canon (no spatial infinity, inner seal, r bounded from 0)
SELECTS the fork in which the 4th component is NOT needed for regularity.

## TASK 4 — energetics + charge

- **Theta-direction potential** V(Theta) = xi sin^2/r^2 + (kappa/2) sin^4/r^4 is
  MAXIMIZED at Theta=pi/2 (d2V/dTheta2|_{pi/2} = -2(kappa + r^2 xi)/r^4 < 0),
  minimized at the poles Theta=0,pi. So Theta=pi/2 is a critical point of the
  EL (Task 2) but UNSTABLE in the Theta direction — the global-monopole /
  texture unwinding instability.
- **BUT unwinding to a pole DESTROYS the object:** at Theta=0/pi, n4 ->
  (0,0,0,±1), a CONSTANT map, (theta,ps) winding collapses, charge -> 0. An
  unstable maximum is not a "source" — rolling in does not produce a stable
  sourced-n_4 soliton, it produces the trivial vacuum. The configurations that
  carry the pi_2 winding keep Theta=pi/2.
- **Charge:** the sweep is required ONLY for the pi_3 (S^3 baryon) charge. The
  pi_2 degree (S^2, the canonized omega_H1 area-form) is carried by the
  (theta,ps) winding ALONE with Theta==pi/2. So charge conservation forces the
  sweep ONLY IF one has already assumed the S^3 charge — circular as a
  justification for S^3.

## TASK 5 — the connection/source argument (#50) + the "any target dim" claim

- The canonized native winding current F_mn = eps_abc n_a d_m n_b d_n n_c uses
  **exactly 3 components** (a,b,c in {1,2,3}); it is STRUCTURALLY BLIND to a
  4th component. n_4 enters only the |n|=1 normalization, never the native
  charge current. The native L4 = |F|^2_g was derived (`native_skyrme_derive.py`)
  on |n|=1 with d_m n TANGENT to S^2 (the 2-plane reduction d_m n = a_m e1 +
  b_m e2) — an S^2 construction.
- **#50 (su3_field_test, blind-verified):** the metric's connection lives only
  in U(1) x SO(3) x SO(3,1); the spin connection of a real symmetric metric is
  so(3,1)-valued (antisymmetric — a theorem). SO(3) rotates a 3-vector (target
  S^2); the target DOF beyond the real 3-vector get NO native gauge field and
  are unphysical passengers. This bears DIRECTLY on the S^3 4th component: the
  SO(3) the metric supplies is exactly the isometry of S^2, not of S^3.
- **The "Lagrange identity valid for any target dim" justification** in
  `matter_ansatz_derive.py` is NOT a sourcing argument. It states only that the
  FORMULA S_mn.S_pq = (d_m n.d_p n)(d_n n.d_q n) - (d_m n.d_q n)(d_n n.d_p n)
  still COMPUTES if you feed it a 4-vector. It does not show the metric SOURCES
  the 4th component — the action evaluates on any field you hand it; that the
  arithmetic works for a 4-vector says nothing about whether the metric forces
  a 4th DOF. (And `matter_ansatz_derive.py` itself flags that the S^3 stress and
  the banked S^2 energies are from DIFFERENT fields and do NOT agree.)

---

## VERDICT — the 4th component is a **PASSENGER**; native object is **S^2**

**SOURCED is REFUTED; the catalog's S^3 carrier rests on an import (the
pi_3/Th(core)=pi boundary choice), and must be re-graded.**

Single most decisive piece of evidence (exact):

  **Theta-EL |_{Theta = pi/2} == 0   (sympy, exact; L2-part and L4-part
  vanish separately; matches the committed engine theta_ddot to 3e-11).**

n_4 = cosTheta = 0 is a consistent solution of the very equation of motion the
solver integrates. Nothing in the action forces the 4th component off zero in
the bulk; the only thing that pushes it (the r->0 regularity divergence) lies
OUTSIDE the committed finite cell (r_core = 0.05); the only thing that requires
the sweep (the pi_3 baryon charge / Th(core)=pi BC) is the S^3 assumption
itself; and the canonized native winding current eps_abc is structurally blind
to n_4. #50 independently shows the metric supplies only SO(3) (the S^2
isometry), not the S^3 structure.

**Conditional clause (stated exactly):** the verdict is conditional on the
inner boundary being at FINITE r (r_core > 0) — the committed finite-cell canon.
IF the cell were taken to reach the strict origin r=0, the L4 energy divergence
kappa/(2r) of the Theta=pi/2 texture WOULD force a regularizing sweep
(Theta(0)=pi), sourcing n_4 by regularity. The committed cell (r_core=0.05,
Dirichlet seal) is NOT that case, so under the actual UDT cell geometry the 4th
component is a passenger. The whole S^3-vs-S^2 question therefore reduces to a
single BC fact: **does the matter cell reach r=0, or seal at finite r_core?**
The committed geometry seals at finite r_core => S^2.

Did NOT find any: (a) bulk EL source for n_4; (b) native current depending on
n_4; (c) regularity demand for n_4 on the finite cell; (d) native SO(3,1)/U(1)
connection acting on the S^3 4th direction; (e) energetic minimum at n_4 != 0
(the n_4 != 0 poles are the trivial charge-0 vacuum). All five would be needed
to call n_4 sourced; none holds.

---

## BLIND VERIFIER — PENDING. ATTACK HERE:
1. Re-derive the Theta-EL independently (different parametrization / Hilbert
   stress conservation div T = 0 along Theta) and confirm Theta=pi/2 solves it.
   Confirm the L2-only and L4-only sources vanish SEPARATELY at pi/2.
2. Confirm the committed cell inner radius is genuinely finite (r_core=0.05) and
   the Dirichlet Th(core)=pi is a CHOSEN BC, not forced by any junction/seal
   derivation. Is there a committed seal condition that secretly demands a
   regular-at-origin core (=> the sweep) on the actual cell?
3. Attack the charge claim: is the NATIVE conserved topological charge truly the
   pi_2 degree (omega_H1, eps_abc) and not a pi_3 current that the metric also
   sources? Exhibit a native 4-component current if one exists.
4. Attack the energetics: is the Theta=pi/2 texture stabilized by the L4
   GRADIENT energy against the unwinding for SOME nontrivial (theta,ps) winding,
   or does it always unwind? (Either way, does unwinding source a stable n_4 or
   just trivialize?)
5. Targeting check: was PASSENGER reached by deriving the absence of a source,
   or steered? Confirm no S^2 result was imported to force the verdict.

---

## BLIND VERIFIER VERDICT — 2026-06-18 (verifier agent b7e3a4f0c1d29856)

Independent re-derivation (angle-integrated 1-D radial action -> EL, a DIFFERENT
route than the constructor's pointwise Hilbert stress). Result: **the headline
"PASSENGER / native object is S^2 / catalog is an import" DID NOT SURVIVE.**
Honest status: **STANDS-CONDITIONALLY, with the physical r=0 question FLAGGED
OPEN** — and the clean "import, re-grade" conclusion is WITHDRAWN.

What the verifier CONFIRMED (the narrow math):
- Axis A: the Theta-EL is satisfied identically at Theta=pi/2 as a CONSTANT
  (L2-only and L4-only sources vanish separately; engine theta_ddot=2.5e-15).
  NUANCE the constructor missed: theta_ddot at Theta=pi/2 with Theta' != 0 is
  0.38, NOT 0 — pi/2 is a solution only as a constant, not as a profile sweeping
  THROUGH the equator.
- Axis D: the native current eps_abc (omega_H1) is structurally blind to n_4 (a
  genuine pi_2 / H^2 degree-1 object) — but the m=1,2,3 CATALOG is indexed by
  Theta(core)=m*pi, the chiral-SWEEP (pi_3-type baryon) count, NOT the pi_2
  area-form degree (complete_metric_sweep_stageB_results.md sec B). The catalog
  WAS built on the swept, n_4-sourced profile.
- Axis E: #50 (metric connection = U(1)xSO(3)xSO(3,1), no SU(3)) is sound, and
  "Lagrange identity valid for any target dim" is arithmetic not sourcing — BUT
  #50 concerns the INTERNAL symmetry on the 3-vector; it does NOT address whether
  the RADIAL chiral angle Theta (= n_4) is dynamically sourced. The claim
  over-extends #50.

What the verifier REFUTED (why the headline fails):
- Axis B (load-bearing): r_core=0.05 is a CHOSEN numerical/grid cutoff — tagged
  literally "[CHOSEN]" in complete_metric_sweep_stageA.py (L131; cell size "FREE
  dimensionful input #39"; rc=0.05 at L146). CANON C-2026-06-10-2 puts the matter
  core at phi -> -inf, which the finite-depth (p~0.4-0.8) committed solve never
  reaches. So r_core=0.05 is NOT a derived seal radius; the physical question
  "does the matter cell reach r=0?" is UNRESOLVED. A numerical cutoff cannot
  settle it. At strict r=0 the L4 texture energy kappa/(2r^2) is non-integrable
  => the sweep WOULD be forced => n_4 sourced by regularity.
- Axis C (strongest break): the charge-1 energy MINIMIZER sweeps. Torch
  relaxation (free interior, BC Theta(core)=pi -> Theta(seal)=0): minimizer E=1.75
  vs E=24.0 for flat Theta=pi/2 (>13x penalty); |n_4=cosTheta|>0.05 over 100% of
  the cell. Theta=pi/2 everywhere also VIOLATES the committed charge-1 BC. So no
  stable charge-1 S^2 representative exists under the committed boundary data; the
  energy-minimizing charged object sources n_4 everywhere, INDEPENDENT of r->0.

THE REAL CRUX (where canon and catalog diverge): the verifier's Axis C used the
BC Theta(core)=m*pi — which is itself the pi_3 baryon (S^3) assumption. So the
energetics favor the sweep GIVEN that BC; they cannot settle which charge is
native. The S^2-vs-S^3 carrier question therefore reduces to TWO entangled,
genuinely-open, decidable questions:
  (a) WHICH CHARGE IS NATIVE — the pi_2 area-form degree (CANON C-2026-06-14-1,
      omega_H1, N=3, q=1/3) or the pi_3 chiral-sweep baryon (the catalog's
      Theta(core)=m*pi BC)? The catalog CHOSE the baryon BC; its provenance
      (derived vs Skyrme import) is UNAUDITED. This is the upstream crux.
  (b) DOES THE MATTER CELL REACH r=0? (finite-cell canon; phi -> -inf core).

VERIFIER RECOMMENDATION (adopted): do NOT re-grade the S^3 carrier / m=1,2,3
catalog as imports on the strength of this argument (the import verdict is
unsupported). EQUALLY, the "S^3 DERIVED" tag remains UNEARNED — what is actually
load-bearing is the pi_3 baryon BC Theta(core)=m*pi, whose provenance is the next
target. CARRIER STATUS = SCOPED-OPEN, hinging on (a)+(b). Methodological note: the
constructor's error was the CLAUDE.md tractable-slice->frame-result inflation
("EOM permits Theta=pi/2" -> "the native object IS S^2"); caught by the verifier.

DURABLE FINDINGS that DO stand (both agents agree): the native CHARGE current
eps_abc/omega_H1 is genuinely S^2/pi_2 and blind to n_4; the metric sources no
SU(3) (#50); the bulk EOM does not source n_4 at the equator; matter_ansatz_derive
itself flags that its committed S^3 stress and S^2 energies come from DIFFERENT
fields (an internal inconsistency, unretracted). These are banked; the carrier
VERDICT is not.
