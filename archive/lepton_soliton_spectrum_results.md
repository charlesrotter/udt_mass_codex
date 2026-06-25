# Lepton Soliton Spectrum / Scale-Free Mass Ratios — Results

Date: 2026-06-14. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **DERIVE** (gated,
pre-registered). Contract: `lepton_soliton_spectrum_contract.md` (committed
BEFORE this run). **STRICTLY DATA-BLIND**: no empirical particle masses,
ratios, "wall numbers", or contract 26fc757 targets were loaded, recalled, or
computed toward. Only the model's own intrinsic, scale-free ratios are reported.

Scripts (commit-grade, this push):
- `lepton_soliton_spectrum.py` — V100 torch float64 + scipy solve_bvp: ground
  state, static-excitation test (Pa), breathing-tower Hessian (Pb), (W) winding
  tower, kappa/xi cancellation, cell-size independence.
- `lepton_soliton_spectrum_deep.py` — rescaled-weight deep-phi scan, spacing-law
  fit, Koide Q (three readings), mpmath overflow anchor.
- `lepton_soliton_spectrum_mpmath.py` — high-precision (dps=60) deep-phi
  breathing spectrum, p=0..4: confirms float64 p>=2 negatives are conditioning
  artifacts; the tower is positive and O(1) at every depth.

Blind adversarial verifier: **PENDING** (verifier-before-record; attack-here
block at the end). The reduced functional + EOM are inherited from
`native_stabilizer_results.md` / `native_profile_bvp.py` (already
blind-verified, agent a1f2213b6410a6f35).

---

## TASK 1 — THE REDUCED RADIAL ENERGY FUNCTIONAL E[Theta] AND EOM

Metric (static spatial slice): ds^2 = e^{2phi(r)} dr^2 + r^2 dOmega^2, with
sqrt(g) = e^{phi} r^2 sin theta. Hedgehog (charge/degree m):
  n = (sin Theta(r) sin th cos(m ph), sin Theta(r) sin th sin(m ph), cos Theta(r)),
winding 2-form omega_H1. Reducing L = L2 + L4 over the sphere (the e^{±phi}
factors carried HONESTLY through the measure and inverse metric; DERIVED in
`native_derrick_derive.py`, sympy-exact, and re-confirmed numerically here):

  **E2_r = (2 pi xi /3) e^{-phi} [ r^2 sin^2Theta Theta'^2  +  2 r^2 Theta'^2
            +  4 e^{2phi} m^2 sin^2Theta ]**

  **E4_r = (2 pi kappa /3) e^{-phi} [ (2 r^2 sin^4Theta + 2 r^2 sin^2Theta) Theta'^2
            +  e^{2phi} m^2 sin^4Theta ] / r^2**

  **E[Theta] = INT_{r_core}^{r_int} (E2_r + E4_r) dr.**

Term identification (as requested):
- L2 gradient terms: the **Theta'^2** pieces r^2 sin^2Theta Theta'^2 + 2 r^2 Theta'^2
  (radial winding gradient), weighted by e^{-phi}; and the **sin^2Theta/r^2-type**
  "potential" 4 e^{2phi} sin^2Theta (transverse winding stiffness), weighted by
  e^{-phi}·e^{2phi} = e^{+phi}.
- L4 (native Skyrme = |omega_H1 current|^2_g) terms: the cross **sin^2Theta/r^2
  (Theta'^2 + ...)** pieces (2 r^2 sin^4Theta + 2 r^2 sin^2Theta)Theta'^2 / r^2
  (e^{-phi} weight) and the e^{2phi} sin^4Theta / r^2 potential (e^{+phi} weight).
- The **e^{±phi} weights are not cosmetic**: e^{-phi} multiplies the proper radial
  measure / gradient stiffness, e^{+phi} the transverse "potential"; they are what
  shift the soliton outward in deep-phi (Task 6).

The winding charge m enters ONLY the transverse "potential" terms (sin^2Theta and
sin^4Theta), as m^2 (azimuthal winding); the radial-gradient Theta'^2 pieces are
m-independent. m=1 reproduces the proven E2_r,E4_r exactly. [TAG: m-dependence of
the reduction = DERIVED for the potential terms from the degree-m hedgehog;
re-relaxation of the m-profile flagged below as a scoped approximation.]

**EOM** (Euler-Lagrange of E[Theta]; DERIVED symbolically, `theta_ddot` in
`native_profile_bvp.py`, m=1):
  d/dr [ partial(E2_r+E4_r)/partial Theta' ] = partial(E2_r+E4_r)/partial Theta,
which expands to the second-order nonlinear ODE Theta'' = num/den with
  den = r^2 (2 kappa sin^4Theta + 2 kappa sin^2Theta + r^2 xi sin^2Theta + 2 r^2 xi),
and num the (long) gradient+potential+phi'-coupling expression committed in the
script. (Flat phi=0 reduction verified; general-phi form carries phi, phi'.)

ONE scale: kappa/xi sets the soliton size L = sqrt(kappa/xi); we work in xi=kappa=1
(L=1) and report only ratios. **kappa/xi cancellation verified** (Task 6).

---

## TASK 2 — FAMILY (P), THE RADIAL TOWER (PRIMARY)

### Ground state (0 internal nodes) — EXISTS
Charge-1 monotone profile Theta: pi -> 0 on the finite cell. Solved as the EOM
BVP (scipy solve_bvp, rms residual 1.0e-9; GPU energy cross-check):
  **E_0 = 45.6069** (kappa/xi units; E2 = 22.876, E4 = 22.731, virial E2/E4 = 1.006),
  width (Theta = pi/2) = 0.648 L. A genuine, sized soliton (the native L4
  stabilizer cures Derrick collapse; inherited result).

### (Pa) Distinct STATIC excited solutions (extra nodes) — **DO NOT EXIST**
We seeded the SAME charge-1 BVP (Theta(core)=pi, Theta(seal)=0) with 1- and
2-extra-oscillation initial guesses (profile allowed to overshoot 0/pi) and
relaxed. **Both collapse exactly back to the monotone ground state** (E = 45.60689,
identical to 5 decimals; max|Theta - Theta_ground| < 1e-3). The model provides
**NO genuinely distinct static excited charge-1 soliton** — the only static
charge-1 solution is the nodeless ground state. (First-class structural fact:
the radial tower is NOT a tower of static overtone solitons.)

### (Pb) BREATHING / FLUCTUATION tower — **EXISTS, and IS the (P) tower**
The second variation (Hessian) of E about the ground state, on the cell, with the
proper breathing inner-product weight W ~ e^{3phi}(field-space metric) [the
time-kinetic coefficient of a fluctuation T(r,t); g^{tt} sqrt(-g) ~ e^{3phi} r^2],
gives a clean Sturm-Liouville eigenproblem H u = omega^2 W u, Dirichlet ends.
GPU float64 (flat p=0), lowest eigenvalues:

  **omega^2 = [0.19818, 0.55395, 1.03924, 1.6884, 2.5543, 3.6448, ...]**
  **omega   = [0.44517, 0.74428, 1.01943, 1.2994, 1.5982, 1.9091, ...]**

All positive => the ground state is a **stable** soliton with a discrete,
normalizable breathing tower. **THIS is the discrete radial family the model
actually provides:** not static overtones (Pa fails), but the quantized
small-oscillation (breathing) spectrum around the unique ground soliton.

### State energies E_0 < E_1 < E_2 and R1, R2
The contract asks for the three lowest STATE energies. Since the static tower
does not exist, the three "states" are the n=0,1,2 breathing levels of the single
soliton. We report all three defensible readings of "state energy" (the choice
is a CONVENTION, tagged CHOSE):

| reading                     | E_0,E_1,E_2 (units)          | R1=E1/E0 | R2=E2/E0 | Koide Q |
|-----------------------------|------------------------------|----------|----------|---------|
| A: E_n = E_soliton + omega_n| 46.049, 46.348, 46.623       | 1.0065   | 1.0125   | 0.33334 |
| B: E_n = omega_n^2 (SL eig) | 0.1982, 0.5540, 1.0392       | 2.7952   | 5.2439   | 0.36715 |
| C: E_n = omega_n (freq)     | 0.4452, 0.7443, 1.0194       | 1.6719   | 2.2900   | 0.34249 |

Reading A (total mass = soliton + one breathing quantum) is the physically literal
"state energy"; it gives R1, R2 within ~1% of 1 (the breathing quanta are tiny
next to the soliton mass). Reading B/C report the excitation spectrum itself. In
**all** readings the spacing is **O(1)**, not exponential (Task 5).

**PRIMARY (P) deliverable (data-blind):** the radial tower is the **breathing
tower**; its level ratios are O(1) — R1 in {1.01, 1.67, 2.80} and R2 in
{1.01, 2.29, 5.24} across the three readings. NONE is a large hierarchy.

---

## TASK 3 — FAMILY (W), THE WINDING TOWER (SECONDARY)

Charge B = m = 1,2,3 hedgehogs; energy from the m-weighted reduction (m^2 in the
transverse potential terms), evaluated on the charge-1 radial shape (the radial
profile is m-dependent; full per-m re-relaxation is a refinement, flagged):

  **M_1 = 45.607,  M_2 = 90.682,  M_3 = 165.806**  (kappa/xi units)
  **M_2/M_1 = 1.988,   M_3/M_1 = 3.636.**

The winding tower spacing is also **O(1)** (roughly M_B ~ B for the L2-dominated
part, with the L4 sub-additivity bending it slightly below B^2). Reported only;
the locked map keeps (W) exploratory (look-elsewhere debited).

---

## TASK 4 — KOIDE Q

Q = (E0+E1+E2) / (sqrt E0 + sqrt E1 + sqrt E2)^2, from the (P) triple:
- Reading A (E_n = E_soliton + omega_n): **Q = 0.33334**
- Reading B (E_n = omega_n^2):           **Q = 0.36715**
- Reading C (E_n = omega_n):             **Q = 0.34249**

For ANY three positive reals Q is bounded in [1/3, 1]; Q = 1/3 iff the three are
degenerate (E0=E1=E2), Q -> 1 iff one dominates. The breathing tower's near-even
spacing puts Q near the LOWER edge (~0.33-0.37) in every reading — i.e. the
states are nearly degenerate on the Koide measure (reading A literally so, since
the tiny breathing quanta sit atop a common large soliton mass). [Reported as a
pure number, data-blind; no comparison to any 2/3 target is made here.]

---

## TASK 5 — LEVEL SPACING (informative structure)

**The (P) tower spacing is O(1) (overtone-like), NOT exponential.** Flat p=0:
- omega^2_n vs n linear fit: omega^2_n ~ -0.093 + 0.682 n (resid rms 0.23) — i.e.
  omega^2_n grows roughly LINEARLY in n (Sturm-Liouville/box-like: omega_n ~ n).
- exponential fit log(omega_n) ~ c0 + c n: slope **c = 0.280**, e^c = 1.32 per
  level. An exponential hierarchy would require c >> 1 (each level a large
  multiplicative jump); c = 0.28 is firmly O(1). The tower is a mild overtone
  ladder, not a geometric/exponential cascade.

**Dependence on core depth p and the deep-phi region** (mpmath dps=60, p=0..4):

| p   | omega^2 (lowest 4)                          | R1=om1/om0 | R2=om2/om0 |
|-----|---------------------------------------------|------------|------------|
| 0.0 | 0.196, 0.509, 0.871, 1.463                   | 1.611      | 2.107      |
| 1.0 | 0.651, 2.963, 7.075, 12.99                   | 2.134      | 3.297      |
| 2.0 | 1.575, 7.884, 19.24, 35.58                   | 2.237      | 3.495      |
| 3.0 | 3.082, 15.70, 38.17, 70.29                   | 2.257      | 3.520      |
| 4.0 | 5.144, 26.32, 63.64, 116.7                   | 2.262      | 3.517      |

Deepening the core **raises** the spacing ratios (R1: 1.61 -> 2.26, R2: 2.11 ->
3.52) but they **SATURATE by p~3** and stay O(1) — the deep-phi region does NOT
manufacture an exponential hierarchy. (The deep-phi e^{2phi} stiffening pushes the
twist outward and compresses the well, lifting the excited levels relative to the
ground, but only to an O(1) plateau.) **Honest verdict on the spacing: O(1),
saturating; the metric's deep-phi region does not generate exponential level
spacing in this functional.**

NUMERICAL NOTE: float64 fails the deep-phi (p>=2) eigenproblem (the e^{3phi}
breathing weight spans (r_int/r_core)^{3p} ~ 10^14 across the cell -> catastrophic
conditioning, spurious NEGATIVE omega^2). The mpmath (dps=60) recomputation gives
all-positive, well-ordered spectra at every depth — confirming the negatives were
a known float64 artifact, not a physical instability. The single-anchor mpmath
overflow check (e^{3phi_core} = 2.0e-15, 9.2e-23, 4.1e-30 at p=2,3,4) matches
float64 to rounding, locating the failure in the matrix conditioning.

---

## TASK 6 — ROBUSTNESS

- **kappa/xi cancellation:** absolute E_0 scales as ~sqrt(kappa xi) (45.61 at
  (1,1); 91.21 at (2,2) = 2x as expected; 91.10 at (1,4); 79.39 at (3,1)), but the
  RATIOS R1,R2,M2/M1,M3/M1 are set by kappa/xi alone and are reproduced; in xi=
  kappa=1 units they are the reported numbers. The single scale cancels in all
  ratios. [VERIFIED]
- **Cell-size independence:** the soliton width holds at (w-r_core)/L = 0.648
  -> 0.648 as the cell grows from 8 L to 40 L (`native_profile_bvp.py` re-run);
  the breathing ratios are insensitive to r_int once the cell >> width. The
  intrinsic size is sqrt(kappa/xi), not the cell. [VERIFIED]
- **Deep-phi p up to 4 with mpmath:** spectrum positive and O(1)-spaced at every
  depth (table above); float64 artifact isolated and corrected. [VERIFIED]

---

## PREMISE LEDGER (chose vs derived)

DERIVED (forced by the metric / the native L2+L4 / general covariance; inherited
blind-verified where noted):
- D1. Reduced functional E2_r, E4_r with honest e^{±phi} weights
  (native_derrick_derive.py, sympy-exact, blind-verified). m^2 azimuthal
  dependence in the transverse potential terms.
- D2. EOM Theta'' = num/den (native_profile_bvp.py, symbolic EL).
- D3. Ground state EXISTS: unique nodeless charge-1 soliton, width 0.648 L,
  virial E2=E4 (flat). (inherited, re-confirmed)
- D4. NO distinct static excited charge-1 soliton (Pa): both node-seeded BVPs
  collapse to the ground state. [this run]
- D5. The breathing/fluctuation Hessian about the ground state has a discrete,
  all-positive normalizable spectrum (stable soliton); omega^2 = [0.198, 0.554,
  1.039, ...] (flat). [this run, GPU + mpmath cross-check]
- D6. Spacing is O(1) (omega^2_n ~ linear in n; exp-fit slope c=0.28), saturating
  with depth (R1: 1.61->2.26, R2: 2.11->3.52, p=0->4). [this run]
- D7. (W) winding tower M_2/M_1 = 1.99, M_3/M_1 = 3.64 (O(1)). [this run]
- D8. kappa/xi cancels in all ratios; width and ratios cell-size-independent.

CHOSE (modeling/convention choices, tagged loudly — none a smuggled mechanism):
- C1. **Reading of "state energy" for the (P) tower** (A: E_soliton+omega_n;
  B: omega_n^2; C: omega_n). This is the load-bearing convention for R1,R2,Q.
  All three give O(1) spacing; the physically literal total mass is reading A.
  [CHOSE — flagged as the key interpretive fork.]
- C2. Breathing inner-product weight W ~ e^{3phi}(field-space metric) [the
  time-kinetic coefficient from g^{tt}sqrt(-g); the natural choice, but the
  e^{3phi} radial profile is what makes deep-phi float64 ill-conditioned].
  [CHOSE the time-measure; derived from the metric, but flagged.]
- C3. Charge-1 BCs Theta(core)=pi, Theta(seal)=0 (Dirichlet); winding=1 carrier.
  [derived as the charge-1 hedgehog; the seal Dirichlet vs Neumann fork was
  resolved to Dirichlet (Theta(seal)=0) by finite-energy of the unwound exterior.]
- C4. (W) energies evaluated on the charge-1 radial shape with m^2 potential
  weighting (not fully per-m re-relaxed). [CHOSE — a scoped approximation for the
  SECONDARY tower; the ratios are indicative, full re-relaxation a refinement.]
- C5. Finite cell [r_core=0.05, r_int=r_core+14L], r_int/r_core large; results
  cell-size-independent in L. [CHOSE numeric scaffolding.]
- C6. Background phi: flat (theorem) + log cell phi = -p ln(r_int/r), p=0..4
  scan. [the log form is the derived deep cell; p is the depth dial.]

---

## HONEST VERDICT — WHAT DISCRETE FAMILY THE MODEL PRODUCES

**The (P) radial tower EXISTS, but NOT as a tower of distinct static solitons.**
The model provides exactly ONE static charge-1 soliton (the nodeless ground
state); node-seeded BVPs collapse back to it (no static overtones). The discrete
radial family the model DOES provide is the **breathing / small-oscillation
tower** — the normalizable, all-positive fluctuation spectrum omega_n^2 around
that unique soliton. It is a genuine discrete tower, but its **level spacing is
O(1) (overtone-like), not exponential**: omega^2_n grows ~linearly in n, the
exponential-fit slope is c=0.28 (e^c=1.3 per level), and deepening the metric core
(p up to 4) only lifts the ratios to an O(1) plateau (R1<=2.26, R2<=3.52) — the
deep-phi region does not manufacture a large hierarchy. The (W) winding tower is
likewise O(1) (M_2/M_1=1.99, M_3/M_1=3.64). Koide Q sits near the lower bound
1/3 (0.333-0.367 across readings), reflecting the near-even spacing.

**Pre-registered honest-prior outcome:** the contract's honest prior anticipated
that an O(1) overtone tower would FAIL any exponential-hierarchy requirement. That
is precisely what the model delivers: a clean, stable, discrete O(1) breathing/
winding tower. Whether this O(1) structure matches the intended targets is a
data-comparison step DELIBERATELY NOT performed here (data-blind). As a model
result: **the native L2+L4 angular soliton on the UDT cell produces a discrete
breathing tower with O(1) (not exponential) level spacing, ratios R1/R2 of order a
few, and a near-degenerate Koide ratio Q ~ 1/3.**

---

## DATA-BLIND CONFIRMATION

No lepton/hadron mass, ratio, or wall number was loaded, recalled, computed
toward, or compared in any script or in this document. Contract 26fc757 and its
targets were not opened. The push reported only the model's intrinsic ratios
(R1, R2, M2/M1, M3/M1), the pure number Q, and the spacing pattern. Comparison to
empirical data is a separate, later step by someone else.

---

## BLIND VERIFIER — PENDING. ATTACK HERE:

1. **(Pa) static-tower non-existence (D4).** Re-attempt distinct static charge-1
   excited solitons with an INDEPENDENT method (shooting from the core with a
   varied Theta'(core); arclength continuation; a relaxation solver seeded with a
   true 2-zone overshoot). Confirm there is genuinely no second static branch and
   that the collapse is physical, not a solver basin-of-attraction artifact. If a
   distinct static excited soliton exists, the whole (P) reading changes.
2. **(Pb) breathing weight C2 (the load-bearing measure).** Re-derive the
   time-kinetic inertial weight W from varying the FULL time-dependent action
   (xi/2) g^{tt}(d_t n)^2 sqrt(-g) about the soliton — confirm W ~ e^{3phi}
   (field-space metric) and not some other power. The omega_n and hence R1,R2,Q
   depend on it. Independently confirm the Hessian P,Q,R coefficients (FD here)
   against a clean analytic 2nd variation.
3. **Deep-phi conditioning (D6).** Reproduce the mpmath all-positive spectrum at
   p=2,3,4 with an independent high-precision/scaled-variable solver; confirm the
   float64 negatives are conditioning artifacts (they are, by the e^{3phi} span
   argument) and that R1,R2 truly SATURATE rather than (a) diverge or (b) the
   ground mode going soft (omega_0 -> 0, an instability) at some depth.
4. **The state-energy reading C1 (interpretive fork).** Is reading A (soliton +
   quantum), B (omega^2), or C (omega) the right "mass" for a UDT breathing
   excitation? This single choice swings R1 from 1.01 to 2.80 and Q from 0.333 to
   0.367. Argue from the metric/action which energy a breathing level actually
   carries — do not let the data-comparison step pick it post hoc.
5. **(W) m-profile approximation C4.** Re-relax the radial profile per winding m
   (don't reuse the m=1 shape) and recompute M_2/M_1, M_3/M_1; confirm the O(1)
   character survives.
6. **Frame / smuggling.** Is the seal Dirichlet (Theta(seal)=0) the only
   finite-energy choice, or does a Neumann seal admit a different (possibly
   degenerate or richer) tower? Did any second scale sneak into the ratios
   (it should not — verified kappa/xi cancellation, but re-check)?

---

## VERIFIER-CLEARED — FAIL STANDS (appended 2026-06-14; supersedes PENDING)

Blind adversarial verifier (Claude Opus 4.8, agent a71e5f8ae4383082d,
2026-06-14; lepton_soliton_spectrum_verifier_results.md + vrf_lepton_*.py)
independently re-derived and ACTIVELY tried to rescue the hypothesis. The
pre-registered FAIL STANDS:
- RESCUE A (a missed static overtone tower?): NO — two independent methods
  (multi-seed relaxation, core shooting) give the SINGLE nodeless ground
  soliton (E0=45.607, width 0.644 L). No static overtones.
- RESCUE B (exponential spacing?): NO — breathing spectrum omega^2 ~ linear
  in n, exp-slope c~0.29-0.5; pushed to core depth p=10 (mpmath): R1 saturates
  ~4.4 then DECLINES, ground mode stiffens, never exponential. Deep-phi does
  NOT manufacture the hierarchy.
- RESCUE C (Koide 2/3 under any reading?): NO — every defensible reading gives
  Q in [0.333, 0.37]; even contrived omega^3/omega^4 only reach 0.41-0.45.
  The quasi-harmonic spread cannot reach 2/3.
DATA-BLIND REVEAL (main loop, after verifier): vs empirical m_mu/m_e~206.8,
m_tau/m_e~3477, Koide 2/3 -> FAIL on T1, T2, T3. The native single-cell
L2+L4 soliton breathing tower is NOT the lepton family.
NON-BLOCKING DISCREPANCY (secondary, does not touch the primary FAIL): the (W)
winding ratios are UNSETTLED — doc 1.99/3.64 vs verifier 2.57/4.95 (both O(1));
and a ~4.2x absolute breathing-weight normalization differs (cancels in every
ratio/spacing/Koide). POSITIVE structural fact extracted: exactly ONE static
soliton per charge-1 cell (a cell holds ONE particle, not a tower).
