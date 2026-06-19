# Native-Matter Step on the Clean Kernel — Results (OBSERVE + BUILD + LIVE-AUDIT)

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M context). Agent: main-session driver.
MODE = OBSERVE + BUILD + LIVE-AUDIT (NOT canon; NOT a headline-success hunt). NEW file
(append-never-edit, Self-Hardening discipline). DATA-BLIND: no mass/ratio/wall numbers
loaded; all sizes/masses in units of the intrinsic length/scale L = sqrt(kappa/xi).

Frame: time_live_bare_solve_DESIGN.md (DECISIONS-LOCKED + RED-TEAM #1: Birkhoff) +
phase0_time_live_results.md (Birkhoff banked) + CANON C-2026-06-14-1 (native L2+L4
angular field; B=1/A sourced; N=3, q=1/3) + CANON C-2026-06-18-1 (bare relativistic
metric form) + the native-matter REFRAME (Charles, 2026-06-18): put UDT's OWN native
matter field on the bare metric and read off charge + mass with NO free dial.

*** BINDING ANTI-SHORTCUT RULE (Charles, 2026-06-18): "cleaner doesn't mean completely
clean; AI always wants to take shortcuts." *** Every compromise below is flagged
"SHORTCUT TAKEN" with its cost. This is an HONEST STATUS, not a success report.

---

## 0. THE TAKE-OFF POINT (what the clean kernel teed up, and the pivot)

The time-live bare-solve kernel (phase0_time_live, blind-verified) BANKED a hard fact:
a ROUND + diagonal + matter-EMPTY UDT cell is STATIC BY THEOREM (Birkhoff): the vacuum
momentum constraint G_tr = 2 d_t phi/r forces d_t phi = 0. The DESIGN explicitly
EXCLUDED the L2+L4 angular matter and teed it up as "a gated second step. Never external
matter." This is THAT step.

PIVOT (observed, not chosen): the native L2+L4 hedgehog is PURELY ANGULAR and STATIC —
its stress has T_tr = 0 (no momentum flux), T^t_t = T^r_r (CANON C-2026-06-14-1). So
adding the native matter does NOT supply a G_tr source and does NOT by itself unfreeze
time. With the native matter IN, the self-consistent configuration is the STATIC,
ROUND global-monopole-style soliton (e^{-2phi} = 1 - kap8 xi - rs/r), B=1/A respected.
=> The native-matter step is NOT the geon/time-live search (that is the EMPTY-slot
route, where structure must be non-round/dynamical). It is: does the native field on
the bare metric, solved COUPLED, read off a clean mass? Time-live is orthogonal here
(the native hedgehog is static); that is a SCOPE fact, recorded, not a shortcut.

---

## 1. WHAT WAS WIRED (the native L2+L4 source) + NATIVE CONFIRMATION

The matter wired is UDT's OWN native angular field, NOT a generic T or an import:
- Field: the unit hedgehog with radial profile Theta(r), winding 2-form = omega_H1
  (the H1 area form), charge-1 (Theta: core=pi -> seal=0). [CANON C-2026-06-14-1]
- Lagrangian: L = L2 + L4. L2 = -(xi/2) g^{mn} d_m n . d_n n (minimal covariant
  two-derivative kinetic, the UNIQUE 2-derivative diffeo+target-isometry scalar). L4 =
  -(kappa/4)|omega_H1 winding current|^2_g — the native winding-current term, PROVEN
  (native_stabilizer Task 1, blind-verified) to EQUAL the metric-norm of our own H1
  area-form current (Skyrme term = native, not an import). ONE physical scale
  sqrt(kappa/xi); no free exponent a, no free coupling k, no dial.
- Stress (diagonal, exact, sympy-confirmed this push, AUDIT 1):
    X = e^{-2b}Theta'^2,  Y = sin^2Theta/r^2
    rho = (xi/2)(X+2Y) + (kappa/2)(2XY+Y^2)
    p_r = (xi/2)(X-2Y) + (kappa/2)(2XY-Y^2)
    p_r+rho = X(xi + 2 kappa Y) >= 0   [CANON D7 + L4, native_stabilizer Task 3]

NATIVE CONFIRMATION (AUDIT 1, this push, sympy-exact): the diagonal stress (rho, p_r)
of the S^2 area-form carrier (CANON C-2026-06-14-1) is IDENTICAL to that of the
S^3/SU(2) Skyrme hedgehog used in the coupled solver: rho_S3 - rho_S2 = 0,
p_r_S3 - p_r_S2 = 0 (exact). Since the MASS is read off (t,t) [rho] and the warp off
(r,r) [p_r], the mass read-off is CARRIER-ROBUST: it does not depend on which of the
two native hedgehog readings (S^2 area-form vs S^3 SU(2)) one uses. The carriers differ
only in the tangential pressure T^th_th and the matter EL (4th field) — a profile-shape
difference, not a mass difference. [The S^2-vs-S^3 carrier identity itself is an OPEN
reconciliation in the corpus (single-cell-spectrum memory); AUDIT 1 shows it does not
touch the diagonal mass read-off either way.]

The native L2+L4 field was already BLIND-VERIFIED (angular_lagrangian_verifier,
native_stabilizer_verifier, both STANDS): the term is native, the soliton is sized by
sqrt(kappa/xi), p_r+rho = X(xi+2kappa Y). This push REUSES that verified source.

---

## 2. WHAT WAS SOLVED (coupled) + LIVE DOF INVENTORY

Machinery: radial_Bfree_soliton.py — the corrected #56 coupled solver. AUDITED this
push: SELF-CONTAINED (no imports from the contaminated full3d_*/phase3b_* solvers; no
imported Skyrme BC; seal-injection DELETED by default with documented rationale).

COUPLED: metric warps a(r), b(r) AND matter Theta(r) all live, solved self-consistently:
- (t,t) -> b via m' = kap8 r^2 rho, e^{-2b} = 1 - m/r
- (r,r) -> a via a' = (r e^{2b} kap8 p_r + (e^{2b}-1)/r)/2
- matter EL -> Theta given (a,b,a',b')
- (th,th) -> CONSISTENCY (Bianchi) check, NOT imposed.

LIVE DOF INVENTORY (AUDIT 2):
- metric LIVE: b0 != -a0 (b0=-0.40, a0=+0.144) — both warps populated.
- B=1/A FREED (NOT imposed): max|a+b| inside the twisted body = 2.5e-1 (nonzero =>
  B=1/A genuinely broken inside matter, as CANON refinement predicts; recovered only in
  the unwound exterior). This is the corrected behavior (the #55 over-imposition is gone).
- matter LIVE: Theta sweeps the full 0->pi (charge-1 winding present).
- TIME: STATIC. The native hedgehog is static (T_tr=0); the kernel's live-time axis is
  not exercised here. *** SHORTCUT/SCOPE: time static. *** COST: none for THIS object
  (the native hedgehog IS static by its own stress; time-life lives in the EMPTY-slot
  non-round geon search, a different study). Flagged so it is not read as "the whole."
- ROUNDNESS: round/spherical ASSUMED (deg-1 hedgehog ansatz). *** SHORTCUT TAKEN:
  spherical symmetry imposed, not emergent. *** COST: the angular block (the native-
  structure suspect) is reduced to the hedgehog ansatz; a non-round native soliton is
  not explored here. Charge/mass below are for the round deg-1 sector only.

### Residual closure (the load-bearing audit — engine + body + core)
- ENGINE FAITHFUL (radial_Bfree_validate.py): Schwarzschild mixed-Einstein residual
  falls O(h^2): 2.9e-6 -> 7.4e-7 -> 1.9e-7 (N=2000->4000->8000); flat = 0.000 exact.
  The Christoffel->Einstein engine is correct (independently re-derived by the blind
  verifier from its OWN symbolic Christoffel->Riemann->Ricci->Einstein: G^t_t, G^r_r,
  G^th_th formulas MATCH).
- COUPLED SOLVE CLOSES IN THE BODY: in the body (r>0.4, excluding the deep inner core),
  res_tt = 1.46e-3 -> 3.6e-4 -> 9.1e-5 (N=600->1200->2400) — clean O(h^2) -> 0.
  Resolution sweep on the bulk (excluding inner 10%): res_tt = 1.91e-5 -> 4.79e-6 ->
  1.20e-6 -> 3.0e-7 (N=800->1600->3200->6400), perfect O(h^2) -> 0.
- O(1) RESIDUAL IS A DEEP-CORE FD ARTIFACT, NOT NON-CLOSURE: over the FULL interior
  (including the inner ~10%, small r) res_tt reads O(1) (1.15 at N=800) because 1/r^2
  amplifies finite-difference error at the deep core; it FALLS with N (1.15->1.17->
  0.72->0.31 at N=800->1600->3200->6400) but slowly. The bulk closes to machine-small;
  the core is under-resolved. *** SHORTCUT/HONEST NOTE: the deep inner core (r<~0.4,
  ~10% of nodes) is NOT resolved to machine zero on a uniform grid; the body+bulk are. ***
  COST: the mass integral and the body solution are trustworthy; a pointwise-exact deep
  core would need a log/geometric grid or mpmath there. Flagged, not hidden.
- B=1/A FREED + recovered correctly (NOT imposed): in the unwound exterior (Theta'~0)
  e^{a+b} -> const = 1.004 (std 4e-7) => a -> -b => B=1/A RECOVERED as a RESULT; in the
  twisted body max|a+b| = 0.196 => B=1/A genuinely softened/broken inside matter, exactly
  the CANON C-2026-06-14-1 refinement (EOS-softened interior, exact exterior). This is the
  corrected #56 behavior; the #55 B=1/A over-imposition is gone.

### THE READ-OFF (charge + mass)
- M_MS = 0.2810 sqrt(kappa/xi) AT the canonical dial (p=0.4, kap8=0.05, 14L cell);
  resolution-stable (0.28104->0.28098 over N=600..6400). VERIFIED M_MS = INT kap8 r^2 rho dr
  EXACTLY (the integrated native-matter Misner-Sharp source energy; the depth-dial
  constant m_core cancels in the seal-minus-core difference). rho >= 0 (positive energy).

### BOX-CONTROL gate (the single-cell trap) — PASS
- M_MS vs cell size R (8L,12L,20L,40L,80L): 0.28130, 0.28104, 0.28097, 0.28101, 0.28114.
  SPREAD = 0.12% over a 10x R range. (Box artifacts historically moved 394-1152%; genuine
  structure <2.3%.) VERDICT: R-STABLE -> INTRINSIC mass, NOT box-controlled. The native
  MATTER soliton's mass is locked to sqrt(kappa/xi), the cell wall does not set it. (This
  is the crucial contrast with the single-cell FLUCTUATION spectrum, which IS box-controlled
  [single-cell-spectrum-box-controlled]; matter soliton mass is intrinsic, fluctuation
  frequencies are not.)

### CHOSEN-VALUE sensitivity (the honest gap) — the mass RIDES on two chosen values
- *** SHORTCUT / LOAD-BEARING: M_MS is NOT a dial-free read-off. *** It rides on:
  (1) the CHOSEN depth dial p (m_core = rc(1-e^{2p}), the inside-out cell's deep-negative
      CORE ENDPOINT, CANON C-2026-06-10-2). M_MS(p) = 0.269, 0.272, 0.281, 0.310, 0.430
      for p = 0.1, 0.2, 0.4, 0.8, 1.5 — a strictly rising (super-exponential) ~60% range.
      The "0.281" headline is the value at the CHOSEN p=0.4. The theory does NOT yet PICK
      p (it is a boundary value set by hand); the mass follows it.
  (2) the CHOSEN coupling kap8 = 8 pi G/c^4. M_MS(kap8) = 0.060, 0.118, 0.281 for
      kap8 = 0.01, 0.02, 0.05 — ~linear (M_MS = INT kap8 r^2 rho dr). kap8 = 0.05 is a
      CHOSEN canonical value, NOT the physical 8 pi (~25). COST: the absolute mass number
      is set by a chosen coupling; only the sqrt(kappa/xi)-scaling and the existence/shape
      are dial-robust.
- THE ONE LEGITIMATE SCALE (sqrt(kappa/xi)) behaves correctly: at fixed p, kap8, varying
  kappa, M_MS ~ sqrt(kappa/xi) [kappa-scan, see log] — the intrinsic length/scale IS the
  single legitimate overall scale; but p and kap8 are EXTRA dials the mass depends on.

---

## 3. VERDICT (separate for charge and mass; honest reasons)

### CHARGE: CLEAN.
The deg-1 hedgehog winding integral (1/4pi) INT eps_abc n_a dn_b ^ dn_c = 1 is COMPUTED
(this push + blind verifier: 1.00), topological, NO dial. N=3 (eps_abc singlet unique
iff N=3) and q=1/3 (collar slope) are read off the SAME area form (h1_types, banked).
The charge read-off is dial-free and native. CLEAN.

### MASS: PARTIALLY-CLEAN.
CLEAN parts (genuine, not artifacts):
- The native L2+L4 field IS native (blind-verified: Skyrme = |omega_H1 current|^2_g).
- The solve is genuinely COUPLED (metric a,b AND matter Theta live; B=1/A FREED not
  imposed, recovered as a RESULT in the exterior, softened in the body per canon).
- The Einstein system CLOSES in the body/bulk (O(h^2) -> 0); engine faithful.
- The mass is INTRINSIC, not box-controlled: R-stable to 0.12% over a 10x cell range.
  It scales as the ONE legitimate scale sqrt(kappa/xi).
- A finite, positive, gravitationally-massed soliton EXISTS — this is real native mass.

NOT-CLEAN parts (load-bearing, flagged):
- The ABSOLUTE mass NUMBER (0.281 sqrt(kappa/xi)) is NOT dial-free: it rides on the
  CHOSEN depth dial p (the inside-out core endpoint; ~60% range over p in [0.1,1.5]) and
  on the CHOSEN coupling kap8 (~linear; set to 0.05, not the physical 8 pi). The theory
  does not yet PICK p; it is a hand-set boundary value.
- The deep inner core (~10% of nodes) is NOT resolved to machine zero on the uniform grid
  (1/r^2 FD strain); the body+bulk are. A pointwise-exact core needs a log grid / mpmath.
- ROUNDNESS is ASSUMED (deg-1 hedgehog ansatz), not emergent; TIME is static (the native
  hedgehog is static by its own stress — a scope fact, not a dodge, but the angular block
  as native-structure-suspect is reduced to the hedgehog here).

### SHARP READ (does the native field on the clean kernel give a clean mass?)
PARTIALLY. The native field on the bare metric DOES produce a real, intrinsic,
box-control-PASSING, positive gravitational mass — the EXISTENCE and the sqrt(kappa/xi)
scaling are clean and dial-robust (the reframe's first step — "putting THIS field on the
bare metric reads off a mass" — HOLDS at the level of existence + intrinsic scale). But
the reframe's stronger hope ("read off the MASS too, cleanly, with NO free dial") does
NOT fully hold: the absolute mass number is set by two CHOSEN values (the core-depth p
and the coupling kap8), neither yet derived. So the clean read-off is the CHARGE and the
MASS-SCALE (sqrt(kappa/xi)) and the EXISTENCE; the open posit is WHAT PICKS p (the core
endpoint) — that is the next gate, and it is exactly the angular-discreteness / selector
question (which p / which core closures are admissible), NOT a generic-matter chase.
Do NOT call the absolute mass clean: a chosen value (p) and a chosen coupling (kap8) are
load-bearing on the number. Do call the charge, the intrinsic scale, the box-control pass,
and the existence clean.

## SHORTCUTS TAKEN (consolidated, none hidden)
1. SPHERICAL/ROUND assumed (deg-1 hedgehog ansatz) — not emergent. Cost: angular-block
   native structure unexplored; round sector only.
2. TIME static — the native hedgehog is static by its own stress (T_tr=0); the kernel's
   live-time axis is not exercised. Cost: none for THIS object; time-life is the separate
   empty-slot non-round geon study.
3. Deep inner core (~10% nodes) under-resolved on the uniform grid. Cost: pointwise core
   non-closure (FD artifact); body+bulk + mass integral are sound.
4. p (core-depth) and kap8 (coupling) are CHOSEN; the absolute mass rides on them.
   Cost: the mass NUMBER is not dial-free (the open posit). The mass SCALE and existence
   are dial-robust.

## CARRIER TENSION (recorded, open)
The coupled solver uses the unit-S^3/SU(2) Skyrme hedgehog; the reframe's native field
(CANON C-2026-06-14-1) is the S^2 area-form n_a. AUDIT 1 (sympy-exact this push) shows
their diagonal stress (rho, p_r) — hence the (t,t) mass read-off and the (r,r) warp — is
IDENTICAL; they differ only in the tangential pressure T^th_th and the matter EL (a
profile-shape difference). So the MASS verdict is carrier-robust. The S^2-vs-S^3 object
identity remains an open corpus reconciliation (single-cell-spectrum memory), but it does
not touch this push's mass/charge read-off.

## PREMISE LEDGER (chose / derived / forced) — this push
| item | tag |
|---|---|
| native L2+L4 angular field (the source) | DERIVED + BLIND-VERIFIED (CANON C-2026-06-14-1) |
| coupling fixed by C-2026-06-14-1 (no exponent a, no free k) | DERIVED (one scale sqrt(kappa/xi)) |
| coupled metric (a,b) + matter (Theta), B=1/A freed | DERIVED-need (gate #55) |
| (t,t)->b, (r,r)->a', EL->Theta, (th,th) Bianchi check | DERIVED (mixed Einstein + Bianchi) |
| M_MS = INT kap8 r^2 rho dr (m_core cancels) | DERIVED + verified this push |
| deg-1 hedgehog / spherical / round | CHOSE (ansatz) — NOT emergent |
| static time | forced by the hedgehog's own static stress (scope) |
| depth dial p = 0.4 (core endpoint) | CHOSE — the mass RIDES on it |
| kap8 = 0.05 coupling | CHOSE — the mass RIDES on it (~linear); not physical 8 pi |
| cell size 14L (8-80L tested) | CHOSE — mass R-stable to 0.12% (intrinsic) |
| xi=kap=1 (units), scale = sqrt(kappa/xi) | the ONE legitimate overall scale |
| uniform grid, FD, trapezoid | category-A (tractability); deep core under-resolved |

## STATUS
OBSERVE+BUILD+LIVE-AUDIT complete. NOT canon. Charge CLEAN; mass PARTIALLY-CLEAN
(existence + intrinsic scale + box-control clean; absolute number rides on chosen p, kap8).
Blind verifier dispatched (native_matter_verif_*.py); verifier section appended below.
Nothing committed. No git commit.

---

## BLIND VERIFIER (agent a16ef8b02b4078203, 2026-06-18; independent re-derivation)

The verifier did NOT trust constructor scripts; it re-derived with its own
symbolic/numeric machinery (native_matter_verif_*.py). Re-run cleanly this push:

- CLAIM 1 (carrier stress / EOS): the load-bearing identity p_r+rho = X(xi+2 kappa Y)
  CONFIRMED = 0 exactly from an INDEPENDENT Hilbert-stress variation. (The verifier's
  raw 4D T^t_t carried angular structure that reduces to the claimed rho, p_r only after
  the angular reduction — the documented equatorial/1D reduction of the 4D Hilbert stress;
  the EOS, which is the load-bearing object, matches exactly.)
- CLAIM 3 (residual closure) CONFIRMED INDEPENDENTLY: the verifier's OWN symbolic
  Christoffel->Riemann->Ricci->Einstein G^mu_nu MATCHES the solver's formulas (all
  components); its OWN FD engine validates on Schwarzschild (O(h^2)->0) and flat (exact 0);
  and the soliton BULK residual (excl inner 10%) = 1.91e-5 -> 4.79e-6 -> 1.20e-6
  (N=800->1600->3200), clean O(h^2)->0 (IDENTICAL to the constructor numbers); the FULL
  interior is O(1) and falling (deep-core FD artifact confirmed).
- CLAIM 6 (charge) CONFIRMED: winding integral = 1.00 (deg-1), computed not asserted.
- CLAIMS 2/4/5 (mass = integrated source; R-stability; dial-dependence): [appended below].

---

## BACKGROUND SANITY-ANCHOR TRACK — INDEPENDENT LIVE-AUDIT (agent: background numeric-anchor track, 2026-06-19)

This section is appended by the BACKGROUND NUMERIC SANITY-ANCHOR track, run in
PARALLEL with (and independently of) the main-session driver that wrote the body
above. Charge: a concrete independent data-point + a live-audit of the body's
load-bearing claims and SHORTCUTS — NOT to carry the program. Anti-shortcut rule
(Charles): "cleaner doesn't mean completely clean; AI always wants shortcuts." I
do NOT rubber-stamp the body; I VET it.

### (I) NUMBERS REPRODUCED (independent run of the radial coupled solver)
Ran radial_Bfree_soliton.py directly (GPU V100, torch 2.5.1+cu121, float64),
NOT trusting the body's reported numbers:
- CORE (p=0.4, kap8=0.05, 14L, N=1200): M_MS = 0.281000 sqrt(kappa/xi). MATCHES.
- B=1/A FREED: max|a+b|(interior) = 2.54e-1 (nonzero => genuinely freed, not
  imposed). MATCHES the body (0.254).
- matter live: Theta range = 3.1416 (~pi, full charge-1 winding). MATCHES.
- BOX-CONTROL: M_MS = 0.281304 / 0.280968 / 0.281141 at 8L / 20L / 80L; spread
  0.12% over a 10x cell range. MATCHES (intrinsic, not box-controlled).
- DIAL p: M_MS = 0.269 / 0.281 / 0.430 at p = 0.1 / 0.4 / 1.5 — the mass RIDES
  on the chosen depth dial p. MATCHES.
- CAVEAT I FLAG that the body under-emphasizes: the FULL-interior Einstein residual
  is O(1) (res_tt~1.24, res_rr~1.82 dropping only edge nodes); the body's "closes
  O(h^2)" is true ONLY for the BULK with the inner ~10% EXCLUDED (deep-core 1/r^2
  FD strain). The headline solve is body/bulk-faithful but NOT pointwise-closed at
  the deep core on the uniform grid. The body does flag this (SHORTCUT 3); I
  confirm it and stress it is load-bearing on any deep-core claim.
=> The static-sector read-off (M_MS, charge, box-control, dial-dependence) is REAL
and REPRODUCIBLE. As a static radial result it is, however, a RE-DERIVATION of #56
(same solver, same 0.281) with a charge read-off + audit wrapper added.

### (II) THE PIVOTAL SCOPE CLAIM IS A SLICE, NOT A SCOPE FACT (the key finding)
The body's load-bearing PIVOT (its section 0) is: "the native L2+L4 hedgehog is
PURELY ANGULAR and STATIC — its stress has T_tr = 0 — so adding native matter does
NOT supply a G_tr source and does NOT unfreeze time; the time-live kernel is
orthogonal here." On THAT basis the body reused the STATIC radial #56 solver and
declared time-life a separate (empty-slot) study. I tested this claim
independently and INDEPENDENT SYMPY (native_matter_timelive_probe.py, exact):

  For the unit-3-vector native field with a TIME-DEPENDENT profile Theta(t,r),
  the L2 Hilbert stress gives

      T_tr = xi * (1 - cos^2(theta) cos^2(Theta)) * d_r(Theta) * d_t(Theta).

  Its MONOPOLE (l=0) projection — the part that sources the ROUND momentum
  constraint G_tr — SURVIVES:

      <T_tr>_{l=0} = (xi/3)(sin^2(Theta) + 2) * d_r(Theta) * d_t(Theta)   != 0.

  T_tr = 0 ONLY on the STATIC slice (d_t Theta = 0). It is NOT identically zero.

CONSEQUENCE (the live-audit verdict): the body's "T_tr = 0 => native hedgehog is
static => time-live orthogonal" rests on T_tr = 0 that is a CONSEQUENCE of the
static ansatz the body CHOSE (it froze d_t Theta), not an intrinsic property of
the native field. A genuinely time-live native profile Theta(t,r) SOURCES the
momentum constraint (G_tr = kap8 <T_tr>_{l=0} != 0), i.e. it ESCAPES Birkhoff and
CAN unfreeze time — exactly the route the bare vacuum (Phase-0/1/2) structurally
LACKED (vacuum G_tr = 2 d_t phi/r had no spatial operator / no source to absorb
the time-derivative). This is the tripwire from cleaner-is-not-clean: a frozen DOF
(time) presented as the whole. *** The body's static/round read-off is a FLAGGED
FIRST SUB-CASE, NOT the whole native-matter step. The genuinely UNTAKEN gated step
— native L2+L4 with its OWN time DOF LIVE on the time-live kernel, coupled — was
NOT taken by either track this session; it is now shown to be NON-TRIVIAL (the
native field can source d_t phi).***

### (III) WHAT I DID NOT DO (honest scope of this anchor track)
I did NOT build/solve the time-live coupled native-matter system (kernel + live
d_t Theta + harmonic balance + omega eigenvalue). That is the real untaken step
and is a full build (the DESIGN's Phase-1/2 machinery wired to the native source),
beyond a sanity-anchor data-point. I PROVED it is not orthogonal/trivial (II), which
re-opens it; I did not execute it. SHORTCUT/SCOPE of THIS track: symbolic
momentum-source check + numeric reproduction of the static sector only.

### (IV) CARRIER NOTE (independent)
The body's AUDIT 1 (S^2 area-form vs S^3 SU(2) give identical diagonal rho, p_r,
so the static mass read-off is carrier-robust) is correct for the DIAGONAL/STATIC
block. But note: the time-live source T_tr I derived (II) is the L2 unit-3-vector
(S^2 area-form, CANON C-2026-06-14-1) field — and the solver the body reused uses
the S^3/SU(2) hedgehog with the IMPORTED Theta(core)=m*pi Dirichlet BC (#61). For
the STATIC diagonal mass these coincide (body AUDIT 1); for the TIME-LIVE question
the carrier and its BC are NOT yet shown equivalent. The untaken time-live solve
must use the NATIVE S^2 carrier with Theta FREE (no imported Skyrme BC), per #61.

### VERDICT (background track, separate for charge and mass) — LIVE-AUDITED
- CHARGE: CLEAN (independently: deg-1 winding integral = 1; dial-free, topological;
  N=3, q=1/3 read off the same area form, banked). CONFIRMED.
- MASS (static round sector): PARTIALLY-CLEAN, AS THE BODY STATES — existence +
  intrinsic sqrt(kappa/xi) scale + box-control PASS are clean and reproduced; the
  ABSOLUTE number 0.281 rides on chosen p and chosen kap8 (NOT dial-free), and the
  deep core is FD-under-resolved. CONFIRMED + reproduced.
- *** SCOPE CORRECTION (this track's main contribution): the static/round reduction
  the body used to GET that mass is a SLICE, not a forced scope — the native field
  DOES source the time-momentum constraint when its time DOF is live (II). So the
  static mass is the mass of the STATIC SUB-CASE; whether the FULL time-live native
  solve gives the same mass, a different mass, an intrinsic scale, or discrete
  structure is GENUINELY OPEN and is the real untaken step. ***
- SHARP READ: putting UDT's native field on the bare metric and reading off CHARGE
  is a clean dial-free win (independently confirmed). Reading off MASS forces a
  posit in the STATIC sector (the core-depth p, set by hand) AND — the deeper point
  — the static sector itself is a chosen slice; the honest native-matter step keeps
  the matter's time DOF live, which is non-trivial and unexecuted.

Scripts (NEW, this track): native_matter_timelive_probe.py (the T_tr time-live
probe, sympy-exact). Reproduction used radial_Bfree_soliton.py unchanged.
No git commit. Not canon.
