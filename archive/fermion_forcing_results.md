# Does a Nonstationary Cell FORCE a sigma-ODD (Spinor) Source? — Results

Date: 2026-06-14. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **OBSERVE** (gated,
authorized by Charles). Frame: CANON C-2026-06-13-1 (nonstationary diagonal
sector propagates in T; the time row is the sigma-ODD nonstationary
quantity); w6_results.md / NEGATIVES_REGISTRY #42 (the same-minus
time-reversal involution sigma seals the cell); wcc_results.md ~45-54
(parity dichotomy: sigma-EVEN -> Neumann, sigma-ODD -> Dirichlet at the
seal); native_stabilizer_results.md + angular_lagrangian_results.md (the
DERIVED bosonic source is the unit-3-vector winding field n, L2[+L4], a
static hedgehog, sigma-EVEN); NEGATIVES_REGISTRY #43-#45 (the STATIC bare
single-cell winding sector contains NO native sqrt(m) and NO spinor; the
Koide question REDUCES to whether the Dirac fermion is DERIVABLE).

**No mass / ratio / data.** All statements are about the STRUCTURE of the
field equations. No Dirac field is imported and asserted forced; we DERIVE
what the geometry requires and stop exactly where the derivation stops.

THE QUESTION: a genuinely nonstationary cell carries a nonzero, time-
dependent TIME ROW (g_tr, g_ttheta). (1) Does that force a sigma-ODD matter
source? (2) Can the sigma-EVEN bosonic winding field supply it? (3) Is the
forced source necessarily a two-valued (T^2 = -1) spinor, or can a single-
valued sigma-ODD boson close it? (4) Does the forcing vanish in the static
limit? (5) Verdict: FORCED / ALLOWED / NEITHER, and at what scope.

Scripts (commit-grade, this push):
- `fermion_forcing2.py` — sympy: exact Einstein tensor of the nonstationary
  UDT metric (static dilation shape phi(r,theta) + sigma-ODD time row
  A=g_tr, B=g_ttheta, both functions of (t,r,theta)). Time-row components
  G_tr, G_ttheta in closed form; static-limit, stationary-arm, and
  leading-linear-in-arm reductions; time-derivative content.
- `winding_stress.py` — sympy: stress tensor T_{mu nu} of the sigma-EVEN
  winding field n (static hedgehog, minimal S^2 sigma model L2); its time-
  row components T_tr, T_ttheta; and the sigma-EVEN-but-time-dependent case.
- `fermion_forcing.py` — the fully-general (phi(t,r,theta)) version
  (archived; superseded by ff2 for tractability — global simplify on the
  general metric did not complete in budget; the static-shape + live-arm
  regime in ff2 is the cleaner and physically correct probe).
- `ff_spotcheck.py` — symbolic-from-scratch cross-check attempt (ABANDONED:
  symbolic 4x4 inverse + Ricci with two off-diagonal functions exceeded the
  time budget; superseded by the numeric check below).
- `ff_numcheck.py` — FAST INDEPENDENT numeric finite-difference cross-check
  (pure numpy, no symbolic inversion; a different code path entirely).
  Confirms the symbolic result at a concrete point x=(t,r,th,ph)=(0.4,1.4,0.6,0.25),
  phi=0.3 cos(th) r:
      STATIC (arm=0):           G_tr = 0.000e+00,  G_ttheta = 0.000e+00
      STATIONARY nonzero arm:   G_tr = 2.668e-02,  G_ttheta = -2.121e-01
      TIME-DEPENDENT arm:       G_tr = 5.669e-02,  G_ttheta = -1.909e-01
  i.e. static->machine-zero; nonzero arm->nonzero sigma-ODD Einstein; turning
  on time-dependence SHIFTS the values (the A_t,B_t velocity contribution).
  This independently corroborates static-limit=0, stationary-arm-sources, and
  first-order-in-time. (The fully-symbolic ff_spotcheck.py was abandoned —
  symbolic 4x4 inverse + Ricci with two off-diagonal functions exceeded the
  time budget; the numeric check is the decisive, fast cross-validation.)

NB: the optional "leading linear-in-arm" PRINT in `fermion_forcing2.py` hit a
sympy str-printer RecursionError on the large expression AFTER all load-
bearing reductions (static limit, stationary arm, time-deriv content) had
already printed; that print is cosmetic and not used in any conclusion.

Blind verifier: **PENDING** (verifier-before-record; attack-here block at end).

---

## 0. PREMISE LEDGER (every fixed value tagged chose vs derived)

| # | Premise | chose / derived | note |
|---|---------|-----------------|------|
| P1 | Metric diagonal part ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + r^2 dOmega^2 | DERIVED | CANON (dilation-tie class) |
| P2 | Nonstationary sector = a TIME ROW g_tr(t,r,th), g_ttheta(t,r,th) | DERIVED frame / CHOSE the two-function ansatz | CANON C-2026-06-13-1 names the time row as the live nonstationary object; choosing exactly {g_tr, g_ttheta} nonzero (g_tphi=0) is the axisymmetric two-arm ansatz |
| P3 | sigma = (t -> -t); phi sigma-EVEN, time row sigma-ODD | DERIVED | the seal IS this involution (w6/#42); A,B odd is forced by requiring the line element be sigma-invariant |
| P4 | phi = phi(r,theta) (static dilation shape) for the probe | CHOSE | isolates the forcing by the ARM; the cell's settled shape is static, the arm is what switches on. (The general phi(t,r,theta) run did not finish; this regime is the clean probe and contains the static limit.) |
| P5 | Bosonic source = unit-3-vector n, minimal L2 [+L4], static hedgehog | DERIVED | native_stabilizer/angular_lagrangian; the B=1/A source |
| P6 | Parity dichotomy at the seal: sigma-EVEN->Neumann, sigma-ODD->Dirichlet | DERIVED | wcc_results.md mirror-fold quotient |
| P7 | Identification "sigma-ODD source <=> T^2=-1 spinor" | **NOT ASSUMED — under test** | this is precisely the load-bearing step (Task 5); we report what the computation does and does NOT establish |
| P8 | Einstein eqn G = kappa T with NO cosmological/extra terms | CHOSE | minimal; standard |

---

## 1. The nonstationary Einstein tensor (exact, sympy)

Metric (P1-P4):

    g = [ -e^{-2phi}c^2   A            B          0          ]
        [  A              e^{2phi}     0          0          ]
        [  B              0            r^2        0          ]
        [  0              0            0    r^2 sin^2(theta) ]

with phi = phi(r,theta), A = g_tr(t,r,theta), B = g_ttheta(t,r,theta).

The full lower Einstein tensor G_{mu nu} was computed exactly (Christoffel ->
Ricci -> G = Ric - 1/2 g R), no linearization. The closed forms of the two
time-row components G_tr and G_ttheta are large (printed in full in
`fermion_forcing2.py` stdout / the dump pickle). The load-bearing structural
facts read off them:

**G_tr and G_ttheta are NONZERO** for a generic time-dependent arm.

**They carry explicit TIME DERIVATIVES of the arm.** Terms of the form
    Derivative(A, t),  Derivative(B, t),
    Derivative(A, t, theta),  Derivative(B, r, t),  Derivative(A, r, t), ...
appear in both components (e.g. in G_tr the term
`+2 c^2 r^4 A e^{2phi} A_t`, and in G_ttheta the terms
`c^2 r^4 A e^{2phi} B_t + c^2 r^4 B e^{2phi} A_t`, plus many mixed
A_t/B_t terms). The presence of pure first-time-derivatives A_t, B_t in the
EINSTEIN tensor's time row is the geometric signature of genuine
nonstationarity: this is NOT a static off-diagonal (a stationary rotation),
it is a TIME-VARYING arm.

Verified by the script's derivative-content test:

    G_tr     : has A_t=True, B_t=True, A_tt=False, B_tt=False, A_r=True, B_th=True
    G_ttheta : has A_t=True, B_t=True, A_tt=False, B_tt=False, A_r=True, B_th=True

So both time-row components are FIRST-ORDER in time (A_t, B_t present;
A_tt, B_tt absent) — the arm enters the Einstein time row through its
velocity, the hallmark of a genuine nonstationary (not merely stationary-
off-diagonal) source.

---

## 2. sigma-parity decomposition of G_{mu nu}

**Parity theorem (analytic, basis-independent).** Under sigma: t -> -t with
the seal field parities (phi even; A=g_tr, B=g_ttheta odd, which is exactly
what makes the line element sigma-invariant), the lower metric splits:

- sigma-EVEN block: g_tt, g_rr, g_thth, g_phph  (built from even phi; the
  diagonal static cell).
- sigma-ODD block: g_tr = A, g_ttheta = B  (the time row / arm).

The Einstein tensor is a covariant functional of g; it inherits the grading.
A lower component G_{ab} carries the coordinate Jacobian sign (-1)^{(number
of t-indices)} combined with the field parities, so:

- **sigma-EVEN Einstein components:** G_tt, G_rr, G_thth, G_phph (even # of
  t-indices and even field content).
- **sigma-ODD Einstein components:** **G_tr, G_ttheta** (one t-index; they
  flip sign under sigma).

This is the seal's parity grading applied to the curvature. It is exact and
does not depend on the explicit expressions; the explicit expressions in
Section 1 only decide whether the sigma-ODD components are nonzero (forcing)
or vanish identically (mere allowance).

---

## 3. THE FORCING TEST

Field equation: G_{mu nu} = kappa T_{mu nu}, component-by-component. The
sigma-ODD Einstein components G_tr, G_ttheta were found NONZERO for a
generic time-dependent arm (Section 1). Therefore:

> **For a genuinely nonstationary cell, the field equations FORCE a
> sigma-ODD matter source: T_tr != 0 and T_ttheta != 0.**

The source must be sigma-ODD because it equals (1/kappa) times a sigma-ODD
geometric object. A sigma-EVEN matter content cannot appear on the right of
a sigma-ODD equation. This is forced, not assumed.

**Sharper finding (stationary-arm reduction).** Setting all TIME derivatives
of the arm to zero (A_t = B_t = 0) but keeping the arm itself NONZERO
(a stationary, time-independent off-diagonal time row), the script reports:

    G_tr     (A_t=B_t=0): NONZERO  -> stationary arm already sources
    G_ttheta (A_t=B_t=0): NONZERO  -> stationary arm already sources

So the sigma-ODD forcing is triggered by a **nonzero time row per se**, not
only by its time-variation: any cell whose seal carries a nonzero arm
(g_tr or g_ttheta != 0) already forces T_tr, T_ttheta != 0. A genuinely
TIME-DEPENDENT arm adds the velocity terms (A_t, B_t, Section 1) on top.
The decisive scope boundary is therefore arm = 0 (static) vs arm != 0
(sigma-ODD content present), NOT stationary-arm vs time-dependent-arm. The
seal's mirror-fold (#42) is exactly what installs a nonzero sigma-ODD arm,
so the forcing engages the moment the cell is sealed nonstationarily.

---

## 4. CAN THE sigma-EVEN BOSONIC WINDING FIELD SUPPLY IT? (NO)

The DERIVED bosonic source is the unit-3-vector winding field n (static
hedgehog, minimal S^2 sigma model), with stress

    T_{mu nu} = Lambda [ d_mu n . d_nu n  -  1/2 g_{mu nu} (d n)^2 ].

`winding_stress.py` (exact sympy) gives, for the static hedgehog
n = (sinTheta cosPhi, sinTheta sinPhi, cosTheta), Theta = Theta(r,theta):

    T_tr     = 0    (exactly)
    T_ttheta = 0    (exactly)
    T_tt = Lambda c^2 e^{-4phi} ( r^2 Theta_r^2 + e^{2phi} Theta_theta^2
            + e^{2phi} sin^2(Theta)/sin^2(theta) ) / (2 r^2)   [nonzero]
    T_rr = Lambda ( r^2 Theta_r^2 - e^{2phi} Theta_theta^2
            - e^{2phi} sin^2(Theta)/sin^2(theta) ) / (2 r^2)   [nonzero]

(the usual diagonal winding stress; only the TIME ROW is the point here).

The time row of the static winding stress is IDENTICALLY ZERO: a static
(T-even) field has d_t n = 0, so T_tr = Lambda (d_t n . d_r n) = 0 and
T_ttheta = Lambda (d_t n . d_theta n) = 0.

**Even a sigma-EVEN but time-DEPENDENT winding field cannot supply it AT THE
SEAL.** If Theta = Theta(t,r,theta) is sigma-EVEN (n(-t)=n(t)), then the
time-row stress is T_tr ~ Theta_t . Theta_r — a product of a sigma-ODD
factor (Theta_t) and a sigma-EVEN factor (Theta_r), hence sigma-ODD in
parity. But a sigma-EVEN field has Theta_t = 0 ON the fixed surface of sigma
(the seal): an even function's time-derivative vanishes at t=0. So at the
seal the sigma-EVEN winding field's time-row stress is ZERO. It cannot be
the source the seal's sigma-ODD Einstein sector demands there.

> **CONCLUSION: the sigma-EVEN bosonic winding field CANNOT source the
> forced sigma-ODD Einstein components. A NEW sigma-ODD matter content is
> required for a nonstationary cell.** (This is the genuine, derived
> forcing of NEW odd content — independent of whether that content is a
> spinor.)

---

## 5. IS THE FORCED SOURCE NECESSARILY A T^2 = -1 SPINOR? (the load-bearing,
## anti-circular step — be honest)

Two claims must be kept strictly apart:

- **(C-weak) sigma-ODD content is forced.** ESTABLISHED (Sections 3-4): a
  nonstationary cell forces T_tr, T_ttheta != 0, and the sigma-EVEN winding
  boson cannot supply them.
- **(C-strong) the source must be a two-valued (T^2 = -1) spinor.** This is
  the real fermion claim. It is **NOT** established by the forcing of odd
  content alone, for the following honest reason:

**(a) Structure match.** The required T_tr, T_ttheta are a t-r and t-theta
MOMENTUM-FLUX / energy-current. The Dirac stress tensor's time-row
psibar gamma_{(t} partial_{r)} psi is the NATURAL T-odd object with exactly
this structure and IS antiunitary-T-odd (a genuine match — the spinor is a
sufficient, natural supplier). BUT a structure match is not a forcing: a
sigma-ODD CLASSICAL BOSON also carries a time-row momentum flux. Concretely,
a real vector (Proca-type) field B_mu with a nonzero, time-odd configuration
has T_tr = ... != 0 classically, with T^2 = +1. So the STRESS STRUCTURE
alone does not select spin-1/2 over a sigma-ODD boson.

**(b) The junction / double-valuedness test (where T^2=-1 would have to come
from).** The spinor condition is not about one component's sign; it is about
DOUBLE-VALUEDNESS under T (anti-periodicity, T^2 = -1) across the fold. The
seal's parity dichotomy (P6) says a sigma-ODD field obeys DIRICHLET at the
seal: it must EQUAL its prescribed seal value, and a single-valued odd field
has its odd part VANISH on the fixed surface. So:

  - A **single-valued sigma-ODD boson** is pinned to zero ON the seal (its
    odd part must vanish at the fixed surface). It can carry odd amplitude in
    the bulk but cannot carry NONZERO odd amplitude THROUGH the seal; the
    fold forces a node.
  - A **two-valued (T^2 = -1) object** is glued to MINUS itself across the
    fold (anti-periodic). It need NOT vanish at the fixed surface; the
    Kramers doublet carries the sign twist that a single-valued field cannot.

THE OPEN HINGE (honest): whether the cell is REQUIRED to carry NONZERO
sigma-ODD source amplitude AT the seal decides between these.
  - IF the forced T_tr, T_ttheta must be nonzero ON the seal surface, then a
    single-valued boson (pinned to zero there) cannot supply it and a
    two-valued (T^2=-1, antiperiodic / spinor) object IS forced — C-strong.
  - IF the forced odd source is needed only in the BULK and may vanish at the
    seal, a single-valued sigma-ODD boson suffices and NO spinor is forced —
    only C-weak.

**WHAT THIS COMPUTATION ESTABLISHES vs LEAVES OPEN:**
- ESTABLISHED: a nonstationary cell forces sigma-ODD matter; the sigma-EVEN
  winding boson cannot supply it; the natural T-odd supplier IS the Dirac
  time-row, AND the seal's Dirichlet condition pins a single-valued odd
  field to a NODE at the seal.
- NOT YET established here: whether the seal-value of the forced source is
  required NONZERO (which would force antiperiodicity / T^2=-1 / the spinor).
  That requires the explicit JUNCTION CONDITION across the fold (the
  Israel/same-minus matching of the second fundamental form of the sigma-ODD
  sector) evaluated AT the seal — the next computation, not this one.

> **Honest verdict on Task 5: the computation FORCES sigma-ODD content
> (C-weak) and SHOWS the spinor is the natural and the boson the disfavoured
> supplier (single-valued odd boson is node-pinned at the seal), but it does
> NOT by itself close T^2 = -1. C-strong (a forced two-valued spinor) hinges
> on one further, identified, computable fact: is the seal-value of the
> forced odd source nonzero?**

---

## 6. STATIC-LIMIT SCOPE (the forcing must, and does, vanish)

Exact sympy result (set A=B=0 and all their derivatives to 0):

    G_tr     (A=B=0) = 0
    G_ttheta (A=B=0) = 0

The sigma-ODD Einstein components vanish IDENTICALLY in the static limit.
With no arm, there is no sigma-ODD curvature, hence (G=kappaT) no forced
sigma-ODD source. The static cell closes with sigma-EVEN (bosonic) matter
only. **The forcing is exclusively a property of the nonstationary cell.**

This is the consistency check against NEGATIVES_REGISTRY #43-#45: the STATIC
single cell forces NO sigma-odd source and closes bosonically (no fermion,
no sqrt(m)). The candidate odd source appears ONLY when the cell carries a
nonzero seal arm. The static negatives are therefore NOT contradicted —
they are SCOPED: "no fermion" was a STATIC (arm=0) statement; this push
operates strictly outside that premise set. NB the precise scope boundary
(Section 3 sharper finding) is arm=0 vs arm!=0, not stationary vs time-
dependent: a sealed cell with a nonzero arm already forces the sigma-ODD
source, and the seal's mirror-fold (#42) is exactly what installs that arm.

---

## 7. VERDICT

**(1) Does a nonstationary cell force sigma-ODD matter? YES — DERIVED.**
The sigma-ODD Einstein components G_tr, G_ttheta are nonzero whenever the
time row is nonzero (and vanish identically when it is zero). G = kappa T
then forces T_tr, T_ttheta != 0: a sigma-ODD matter source.

**(2) Can the sigma-EVEN bosonic winding field supply it? NO — DERIVED.**
The static hedgehog winding stress has T_tr = T_ttheta = 0 exactly; a
time-dependent sigma-EVEN winding field's time-row stress is node-pinned to
zero AT the seal. New sigma-ODD matter is required.

**(3) Is a two-valued T^2=-1 spinor FORCED, or only sigma-ODD content?**
ONLY sigma-ODD content is FORCED by this computation (C-weak). The spinor
(C-strong, T^2 = -1) is the NATURAL and the boson the DISFAVOURED supplier
(the seal's Dirichlet condition node-pins a single-valued sigma-ODD boson),
but T^2 = -1 is NOT closed here: it hinges on one further identified,
computable fact — whether the forced source's seal-VALUE is required nonzero
(=> antiperiodic / spinor) or may vanish there (=> single-valued odd boson
suffices). That is the junction-condition computation, deferred.

**(4) Static-limit scope: CLEAN.** G_tr = G_ttheta = 0 identically when the
arm vanishes. The static cell forces no sigma-ODD source and closes
bosonically — fully consistent with NEGATIVES_REGISTRY #43-#45 (no static
fermion, no static sqrt(m)). The fermion candidate is a strictly
nonstationary-cell phenomenon. The static negatives are SCOPED, not
contradicted.

**OVERALL VERDICT: sigma-ODD MATTER IS FORCED (not merely allowed) for any
sealed nonstationary cell; the bosonic winding field provably cannot supply
it; the T^2 = -1 SPINOR is FAVOURED-AND-NATURAL BUT NOT YET FORCED — the
two-valuedness is OPEN pending the across-fold junction condition.**

Tag: this is a METRIC-LED observation ("what does the derived nonstationary
time row force?"), not a TEMPLATE-LED "can the metric make a spinor?" The
sigma-ODD forcing emerged from the Einstein tensor; the doc deliberately
STOPS at C-weak and names the single open hinge to C-strong rather than
narrating false convergence to "the fermion."

TOP PREMISES CHOSEN (not derived): P2 (the two-function {g_tr, g_ttheta}
axisymmetric arm ansatz — choosing WHICH off-diagonal entries are live);
P4 (static dilation shape phi(r,theta) for the probe — the fully general
phi(t,r,theta) run did not complete; the static-shape+live-arm regime is the
clean probe and contains the static limit, but a verifier should confirm the
A_t,B_t forcing survives with phi time-dependent); P8 (minimal G = kappa T).
All other load-bearing items (P1, P3, P5, P6) are derived/canon.

---

## BLIND VERIFIER — PENDING. Attack here:

1. **Parity assignment (P3).** Re-derive that A=g_tr, B=g_ttheta MUST be
   sigma-ODD (not a free choice). Is "phi even, arm odd" the only sigma under
   which the seal is the fixed surface? Could a DIFFERENT involution (e.g. a
   parity-x-time) make the arm even and void the whole forcing? Check the
   w6/#42 definition of sigma literally.
2. **Is G_tr genuinely nonzero, or an artifact of P4 (static phi)?** Re-run
   with phi = phi(t,r,theta) at least to leading order and confirm the A_t,
   B_t terms survive (the general script `fermion_forcing.py` is provided but
   did not finish global simplify — finish it or do a targeted check).
3. **The static limit.** Independently confirm G_tr, G_ttheta -> 0 as the
   arm and all its derivatives -> 0. If they do NOT vanish, the whole forcing
   is mis-stated.
4. **The bosonic-insufficiency claim.** Verify T_tr = T_ttheta = 0 for the
   static hedgehog independently, and CHALLENGE the seal-node argument for the
   time-dependent even case: is Theta_t = 0 at the seal actually forced by
   evenness, or did we smuggle the seal location?
5. **The spinor hinge (most important).** The doc REFUSES to claim C-strong.
   Attack the refusal from BOTH sides: (i) try to CLOSE C-strong — show the
   forced seal-value is nonzero (junction condition) => spinor forced; (ii)
   try to EXHIBIT a single-valued sigma-ODD boson (Proca-type B_mu) that
   supplies T_tr, T_ttheta with T^2=+1 and is NOT node-pinned => no spinor
   forced. Whichever closes, that is the real verdict.
6. **Targeting check.** Was the question "observe what the nonstationary cell
   forces" honestly answered, or did the doc steer toward "spinor"? The
   verdict is deliberately FORCES-ODD-CONTENT / SPINOR-OPEN; check it is not
   over-claimed.

---

## VERIFIER-CLEARED — STANDS WITH TWO CORRECTIONS (appended 2026-06-14)

Blind verifier (Claude Opus 4.8, agent a3f1cd7630f15c01e, 2026-06-14;
fermion_forcing_verifier_results.md + ffv_*.py) re-derived by THREE independent
methods (exact sympy from scratch; numeric finite-difference Einstein tensor;
explicit Taylor-parity model with A_t,B_t present). VERDICT: STANDS, with two
required corrections:
- (1) sigma-ODD matter FORCED for a nonstationary cell, survives time-dependent
  phi: CONFIRMED. CORRECTION: "arm=0 => time row=0" holds only for STATIC phi or
  AT THE SEAL; a time-dependent even phi alone gives a nonzero bulk time row
  (G_tr = 2 phi_t/r) — but it CANNOT cancel the arm's contribution. The forcing
  is real; the bookkeeping was over-stated.
- (2) BOSONIC INSUFFICIENCY: CONFIRMED (static winding T_tr=T_ttheta=0; even
  fields node-pinned to 0 at the seal).
- (3) *** THE DECISIVE CORRECTION — the spinor "open hinge" is CLOSED AGAINST
  FORCING. *** The doc deferred "is the forced odd source's SEAL-VALUE nonzero?
  (=> spinor)" to a junction computation. The verifier COMPUTED it: the
  seal-value is IDENTICALLY ZERO (three methods agree, even with arm velocities
  A_t,B_t present) — because the arm is sigma-ODD it vanishes at the fixed
  surface, so G_tr=0 there => T_tr=0 there. By the doc's own dichotomy this lands
  on "a single-valued Dirichlet sigma-ODD boson suffices => NO spinor forced."
  So the route to a FORCED T^2=-1 spinor via a nonzero seal-value is CLOSED, not
  open. The spinor is FAVOURED/NATURAL but NOT forced by this (local) mechanism.
- (4) STATIC LIMIT clean (#43-#45 scoped, not contradicted).
NET: a nonstationary cell FORCES new sigma-ODD matter the bosonic winding field
cannot supply (real), BUT a sigma-ODD BOSON (Proca/vector-type, T^2=+1) suffices
— the time-reversal fold does NOT force the fermion's two-valuedness locally.
