# RECON-A — The Cosmology / Macro Side of UDT (the part that WORKS)

Agent: RECON-A (repo-wide recon feeding forward VISION). Date: 2026-06-19.
Scope: macro/cosmology sector — SNe, CMB, BBN, BAO, the redshift law, the
cosmic phi(r) profile, Misner-Sharp closure. Sources read: udt_validated_results.md
(scorecard), udt_active_results.md (current canonical CMB-observable ontology after
the S99/S104/S105 audits), macro_sector_fork_resolution.md, AUDIT.md (EE dispatch),
udt_canonical_geometry.md (metric + Misner-Sharp). NOT committed.

---

## 0. The metric and the one redshift law (the spine)

All macro observables hang off the single static metric (CG §1.3, line 72):

    ds^2 = -e^{-2phi(r)} c^2 dt^2 + e^{+2phi(r)} dr^2 + r^2 dOmega^2

with phi = phi(r_areal) (r is the AREAL radius — a theorem, canonized; rho=r forced
via the C2 areal-chart equivalence, macro_sector_fork_resolution.md Finding 1).
From it:
- **Redshift law (zero-parameter, derived):** `1 + z = e^{phi(r)}` (VR §12987; cleaned
  2BO form `1+z = e^{phi_s - phi_o}`). The cosmic side runs from phi(0)=0 to
  phi(r_CMB) = ln(1101) = 7.003974 at r_CMB = 9.164 Gpc. The domain ENDS there — the
  universe is a finite cell, CMB = its boundary (no spatial infinity).
- **Distance law:** D_A = r; d_L = D_A (1+z) = r e^{phi(r)} (ONE factor of 1+z, not
  two — VR §4.1, §306). D_M(z) = r(z) (BAO transverse). All areal-radius objects.
- **Misner-Sharp quasi-local mass (CG §10.3, line 1401):**
  `m(r) = (c^2 r / 2G)(1 - e^{-2phi(r)})`. Evaluated at the boundary in the deep-well
  limit (e^{-2phi_*} ~ 8e-7 negligible) this is the closure that sets c^2 / the
  cosmic mass. CR-412 N=2 scaffold gives M_MS = 1.9e53 kg (~15% of the LCDM total-mass
  estimate) with rho>0, Bianchi satisfied.

The cosmic phi(r) profile (VR §1.1) — the "geometric polynomial":

    phi(r) = (3/2) mu_g r - cos(pi/5) mu_g^2 r^2 + (2/3) mu_g^3 r^3

coefficients {3/2, cos(pi/5), 2/3} algebraically fixed by the angular Diophantine
triple (j, l, |kappa_max|) = (1/2, 1, 3) — the SAME constants as the lepton-mass
sector. One scale parameter mu_g. CAVEAT: the polynomial is Frobenius-irregular at
r=0 (the linear term is forbidden at a regular origin) — it is an effective
outer-domain expansion, NOT a regular-origin vacuum solution (CR-408). An N=2
regular-origin scaffold (r^2+r^3 basis, BC+BS-determined, zero free params) closes
the full Einstein system cleanly and is the cleaner-physics alternative, but its
coefficients are empirical, not algebraic. Both carry the OPEN D-POLY-1 ansatz flag.

---

## 1. THE MACRO SUCCESSES (what UDT fits, how many params, how well)

### 1.1 Supernovae — the cleanest win (SOLID)
- Law: `d_L = r e^{phi(r)}`, r(z) from the geometric polynomial. **100% metric-derived.**
- Pantheon+ full covariance (CR-327c, VR §34.9):
  - z>0.01 cut (1590 SNe): **chi2/dof = 0.9397**, RMS 0.164 mag — **BEATS published
    LambdaCDM chi2/dof ~ 1.03 with 0 vs 6 fitted cosmological parameters.** Only the
    absolute magnitude M is fitted (1 param, an unavoidable SNe nuisance).
  - Full set (1701, z=0.00122–2.26): chi2/dof = 1.1059, RMS 0.183.
  - Diagonal-only chi2/dof = 0.512 (over-optimistic; full-cov is the honest number).
- mu_g is DEGENERATE with M (shifts the curve vertically, absorbed by M), so the
  distance-redshift SHAPE is effectively mu_g-independent (RMS 0.058 mag vs LCDM).
  No H0, Omega_m, Omega_Lambda anywhere.
- Purity: highest — Pantheon+ magnitudes/redshifts are near-raw; SALT2 corrections
  nearly model-independent. **This is the flagship macro result and it is clean.**

### 1.2 BAO — honest, uncontaminated, mid-grade (SOLID with one OPEN)
- Native drag scale, ZERO LCDM inputs: `r_d = pi r_*,CMB 1000 / l_A^micro`, with
  `l_A^micro = 2 pi r_* E2/(E1 I2)` from the micro Dirac eigenvalue ratio
  (E2/E1=5.9017, I2=0.82296) -> l_A^micro = 314.9, **r_d = 91.4 Mpc**. The earlier
  z_drag=1060 LCDM import was DELETED; UDT has no drag epoch / no decoupling era.
- D_M/r_d vs 8 surveys at locked derived mu_g = 0.2473 (zero free params): **RMS 3.8%**;
  DESI Lya (cleanest data) best at **+1.8%**. All deviations POSITIVE — consistent
  with LCDM-fiducial contamination in the galaxy surveys (which use LCDM mocks).
- OPEN: the radial D_H = (1+z)/phi'(r) does NOT match survey-extracted D_H; the
  Alcock-Paczynski ratio is off by 1.39–3.02x (H23), reduced to ~1.07 once the
  coordinate 1+z factor is restored (H25). Registered as an estimator/feature-kernel
  problem, NOT a validated UDT closure. D_V compression is declared inapplicable to a
  static metric (D_H/D_M ~ 2–11x vs FLRW's ~1–3x), so only the transverse comparison
  is made.

### 1.3 BBN / light elements — algebraic, ZERO new params (SOLID structurally, CAVEATED on rates)
All from the metric + locked particle-sector params (no eta, no primordial epoch):
- **Y(He-4):** geometric floor `Y_em = (r_b/r_*)^3 = 1/phi_gold^3 = sqrt(5)-2 = 0.2361`
  (exact algebraic identity, verified <1e-8; r_*/r_b = golden ratio to +0.024%). Sub-
  cavity supports exactly kappa=+-1 -> 4 nucleon slots -> He-4 doubly-magic. Stellar
  increment Delta ~ 0.009 (recycling fixed point, 6 cycles) -> Y ~ 0.245 (<1%).
- **D/H = alpha/(9 pi^3) = 2.615e-5** vs observed 2.527e-5 (+3.5%).
- **Li-7 problem STRUCTURALLY RESOLVED:** no hot primordial epoch -> no Li-7 over-
  production; steady-state destruction >> production gives naturally low Li-7/H.
- Nuclear binding via angular closure: B(He-4)=C/5 (-0.37%), B_d=C/63 (+0.61%),
  B(He-3)=C/18 (+1.47%), B(Li-7)=5C/18 (-0.22%), m_n-m_p=(5/4)alpha C (-0.77%).
- CAVEAT: the recycling fixed point uses observationally-based (not metric-derived)
  rates (R_burn from Salpeter IMF+SN yields; f_rec from Eddington; f_dest estimated);
  tau_n is +8.6% (attributed to accumulated param errors). The Y FLOOR is exact;
  the stellar increment lands on observations via modeled astrophysical estimates.

### 1.4 CMB — the most worked, and the most reframed (see §4 for the honest grade)
- **Peak POSITIONS (the strong, clean part):** micro Dirac eigenvalues directly
  predict CMB peak positions, T_CMB-INDEPENDENT, zero fitted params: EE 3% RMS
  (kappa=-1), TT 6.9% (parity doublet sqrt(kappa=-1 * kappa=-3)) (VR §39.8). On the
  sourced polynomial, WKB2 peak law gives peaks 1–7 at 1.32% RMS (1 param mu_g) or
  1.72% (zero params, micro l_A).
- **Peak AMPLITUDES (the cr329 framework):** 24-parameter framework, ALL 24 traced to
  angular quantum numbers (Category-2 unresolved-origin count = ZERO at ground state),
  0 fitted COSMOLOGICAL params, 1 calibration amplitude. Full-resolution Planck
  chi2/dof: **TT 1.70 / TE 1.49 / EE 1.45** (Session-17 integrated cr329) vs LCDM
  (6p) 1.03/1.04/1.04. At l>1500 all three ~1.1 (match LCDM). The TT backbone (95%
  of structure) is DERIVED from angular decoherence on S^2; power-law replacement is
  catastrophic (chi2=48.9), so it is real physics not overfit.
- **Joint SNe+BAO+CMB:** the single MICRO-derived mu_g = pi mu/13 = 0.2473 Gpc^-1
  (zero fitted params) gives joint chi2/N = 0.565 (vs 0.560 optimized). Per-probe
  preferred mu_g: SNe 0.239, BAO 0.237, CMB 0.256, micro 0.247 — 7.8% spread
  (honest mild tension, not failure).

---

## 2. WHAT IS SOLID vs CAVEATED (honest grade)

| Result | Metric-pure? | LCDM-calibrated leans? | Grade |
|---|---|---|---|
| Redshift law 1+z=e^phi | YES (derived from ds^2) | none | SOLID / canonical |
| d_L = r e^phi, D_A=r, D_M=r | YES | none | SOLID |
| SNe Pantheon+ chi2/dof 0.94 | YES (shape mu_g-indep) | M fit (unavoidable) | SOLID — flagship |
| BAO D_M/r_d 3.8% RMS | r_d native (micro) | survey D_V uses LCDM fiducial | SOLID-ish; D_H OPEN |
| Y(He-4) floor sqrt(5)-2 | YES (exact algebra) | none | SOLID structurally |
| BBN stellar increment / rates | partial | R_burn/f_rec/f_dest modeled est. | CAVEATED |
| CMB peak POSITIONS | micro-derived, T-indep | none | SOLID |
| CMB peak AMPLITUDES (cr329) | angular-derived params | Planck pipeline ~3-5% LCDM floor | CAVEATED (see §4) |
| Misner-Sharp closure M~1.9e53 kg | YES (Einstein-closed) | "15% match to LCDM total" is the check, not input | SOLID (15% is loose) |

**Data-contamination ladder (UDT's own, VR §42):** SNe = NONE (best fits) -> BAO Lya
= low (+0.2%) -> BAO galaxy = mild (LCDM mocks, 0.2–3.7%) -> CMB Planck binned =
SIGNIFICANT (foreground/beam/binning assume LCDM transfer functions; 3–5% systematic
floor). Pattern: cleaner data -> better UDT fit. The ~5% CMB peak-height residual
SATURATES the LCDM contamination floor — sub-percent is unreachable without a
LCDM-free CMB reduction. Honest and self-aware.

---

## 3. THE PARAMETERS (locked geometric set + the scale-autonomy gap)

Locked parameters (VR §0, "at the locked parameters"):
- **phi_0 = -cos(pi/5)** = -0.809 (vacuum depth at origin) — DERIVED (pentagon/golden)
- **mu^2 = pi/3** (micro screening mass squared) — DERIVED
- **r_* = 6.98755** (microphysical cavity radius) — DERIVED/locked
- **C = 4 pi^2 m_e r_* = 140.96 MeV** (mass anchor) — fixed by the electron anchor m_e
- **mu_g = pi mu / 13 = pi sqrt(pi/3)/13 = 0.2473 Gpc^-1** (cosmic screening mass) —
  DERIVED from micro quantum numbers (CG §12.8); the ONE cosmic scale, zero-fitted.

External inputs (NOT fitted, conversion/anchor): c, G, m_e, T_CMB, T_starlight, hbar.
All five geometric params are derived from ds^2, not fitted. The macro fits use **zero
fitted cosmological parameters** (SNe fits only M; cr329 fits only 1 amplitude).

**THE SCALE-AUTONOMY GAP (the central macro limitation):** the cosmic scale does NOT
bridge to particles. mu_g and r_CMB live at Gpc; finite-universe discreteness is
native and automatic (box on [0, r_CMB]) but omega ~ c/r_CMB is a Gpc-scale frequency
— wrong for particle masses by ~40 orders of magnitude (macro_sector_fork_resolution.md
Finding 3). The mass scale C is set by the ELECTRON anchor m_e (external), not by the
cosmic geometry. So the macro sector fixes RATIOS and SHAPES; absolute particle scale
is a separate (open) input. Gravity being scale-invariant (STATE 2026-06-19) gives
ratios/shapes only; the one absolute scale UDT admits cosmically is
7.004 = ln(1+z_CMB), admitted only because the metric allows it (not hand-inserted).

---

## 4. WEAKNESSES / CONTAMINATIONS / OPEN ISSUES in the macro sector

1. **The CMB-observable ONTOLOGY was substantially RE-AUDITED and demoted (S99-008 ->
   S99-010 -> S104 -> S105).** This is the biggest honesty flag and it post-dates the
   VR scorecard:
   - The entire Branch-C wave-physics CMB machinery (cavity-quantization,
     Bohr-Sommerfeld at cosmic scope, acoustic scale l_A, sound horizon, WKB peak law,
     the "71.886 alignment factor as load-bearing") was found to be **LCDM-borrowed
     scaffolding** and RETRACTED as the cosmological observable mechanism (banner at
     udt_active_results.md lines 3, 5). It is migrated to investigation-history.
     (The Branch-M MICRO Form-T eigenmode content KEEPS; only its EXTENSION to the
     CMB via the reflexive bridge is contamination.)
   - The canonical CMB observable is now the **§229 frame-relation closure** —
     `C_l^UDT(r) = int e^{-3phi_0(r')} |K_l|^2 P_src dr'` — a PURE geometric projection
     from ds^2 (Tolman + emission), NO wave physics. The kernel is a pure-Bessel
     kinematic projection W(r) = r^2 e^{-3phi_0(r)}. Status: CLAIM-PENDING-VERIFICATION
     (single-dispatch; full verifier round-trip pending).
   - **S104/S105 FALSIFIED the peak source and showed the peaks were a fit, not
     geometry:** real cosmic structure shows ONE BAO bump (~150 Mpc), not seven peaks;
     the rms matter contrast at the postulated scales is 70–640x larger than the CMB
     needs; the S103 "7/7 Planck TT peaks reproduced" was **source-driven + convention-
     driven (thin-shell L_l = pi r_CMB / l), 0% geometry-driven.** Canonical UDT's
     actual SMOOTH thermal source through the geometric kernel predicts a **PEAKLESS
     angular spectrum** (active doc §1.6.5 demotion banner, 2026-05-29). The CMB peak
     reproduction is therefore NOT currently canonical-content load-bearing. The peak
     question is explicitly OPEN ("keep searching," Charles). **=> The cr329 1.45–1.70
     chi2/dof amplitude success in the VR scorecard sits on the demoted wave-physics
     ontology; it survives as a historical/Form-T-sector record, not as the canonical
     cosmological derivation.**

2. **The EE small-scale "overshoot" (the named open issue) — status: REOPENED, not
   closed (AUDIT.md, D-CMB-EE-PROJECTION-SPIN-1, S116):**
   - Derived spin-algebra result: scalar breathing source (spin-0) x spin-2
     polarization costs ed^2 -> l^4 angular power, FORCED (not a photon-transport
     import; the pure-metric reframe cannot soften it). l^4 over-predicts the Planck EE
     peak ~2x (peak l~1900–2085 vs Planck 1004). UDT's distortionless metric forbids a
     Silk-damping analog -> EE rises through l^4 -> upgraded to a DERIVED,
     LCDM-DISTINGUISHING falsifiable signature.
   - THEN reopened: the projection had used the flat-space j_l (LCDM-isotropy / Gate-10
     reduction). The NATIVE UDT radial function carries a centrifugal cutoff at
     l_max = 1+z, bringing the EE peak to ~1000 ≈ Planck 1004 — CONSISTENT but
     conditional on omega_drive = c/r_CMB, NOT YET FORCED. So the EE overshoot is
     currently an open, conditional item, not a clean pass and not a clean falsification.
   - S116 also derived that the temperature observable was INCOMPLETE: dT/T = -delta_phi
     (Sachs-Wolfe) was only half; the intrinsic re-emergence term +(1/4)delta_rho/rho
     (Stefan-Boltzmann, c=1/4 derived) makes TT trace the breathing DENSITY (tidal,
     l(l+1)) and collapses the EE/TT ratio from l^4 to l^0 — fixing the overshoot as a
     TT base-model artifact. Mechanism DERIVED; full Planck peak-by-peak match PENDING.

3. **The probe-vs-self-gravitating cosmological-profile flag:** the geometric polynomial
   and the §229 LOS measures treat phi as a fixed background a test field/photon
   propagates through. Whether the cosmological phi(r) is a genuine self-gravitating
   solution (full Einstein closure) vs a probe profile is exactly what CR-408/CR-412
   interrogate: the polynomial is NOT a regular-origin vacuum/self-gravitating solution
   (Frobenius-irregular at r=0); only the N=2 BC-determined scaffold self-consistently
   closes Einstein (with the metric identity g_tt g_rr = -c^2 FORCING T^t_t = T^r_r,
   i.e. p_r = -rho dark-energy-like EOS — DERIVED from the metric, not imported). The
   matter Lagrangian that produces CR-412's T^mu_nu is an OPEN finite-candidate question
   (pure EM / scalar+potential / Dirac+EM / null dust). So the cosmic profile's
   self-gravitating provenance is partially open and ansatz-conditional (D-POLY-1).

4. **D_H / Alcock-Paczynski BAO mismatch (OPEN, §1.2 above):** radial distance in the
   static metric does not map cleanly to survey-extracted D_H; first-principles BAO
   feature kernel and feature scale are unresolved.

5. **The ~150 Mpc absolute clustering scale is settled as an INPUT, not derived**
   (S109, Eddington-Dirac large number); only the dimensionless relative spacings are
   left open. Absolute cosmic scale generally enters via the single ln(1+z_CMB)=7.004
   anchor.

6. **Retracted cruft (recorded honestly):** the "phase-coherence ruler" r_d (uniform-
   amplitude Fourier kernel) was retracted as ad hoc AI-generated cruft (VR §3.1); the
   earlier double-counted d_L = r e^phi (1+z) was corrected; the z_drag=1060 LCDM
   import was deleted from BAO; the H-MOND a_0 coincidence was RETRACTED (tidal accel
   ~1e-16 m/s^2 at galactic scale, ~6 orders below MOND). Galaxy rotation curves /
   dark-matter gap remain UNSOLVED for all galaxy types (D-RE-2-OPEN).

---

## 5. BOTTOM LINE (the side Postulate-A-UDT KEEPS)

UDT's macro sector is genuinely strong on the parts driven directly by the metric's
geometry and the one redshift law `1+z=e^{phi}`: **SNe (beats LambdaCDM, 0 vs 6 cosmo
params, cleanest data), the BBN light-element FLOORS (exact golden-ratio algebra, Li-7
problem dissolved), BAO (honest 3.8%/+1.8% with a fully native r_d), and CMB peak
POSITIONS (micro-derived, T-independent)** — all from a SINGLE derived cosmic scale
mu_g = pi mu / 13 = 0.2473 Gpc^-1 and ZERO fitted cosmological parameters. The metric,
the areal reading, the redshift law, the distance laws and Misner-Sharp closure are
clean and canonical.

The honest CAVEATS are concentrated in the CMB AMPLITUDE/anisotropy machinery: the
cr329 1.45–1.70 chi2/dof headline rests on a wave-physics ontology that the framework
ITSELF later audited as LCDM-borrowed and demoted (S99–S105); the canonical geometric
CMB observable currently predicts a PEAKLESS smooth-source spectrum, the seven-peak
match was shown to be source/convention-driven not geometry-driven, and the EE peak
location is an open, conditional (not forced) item. The cosmic profile's self-
gravitating provenance is ansatz-conditional (D-POLY-1), and the cosmic scale does NOT
bridge to particle masses (~40-order autonomy gap) — the macro sector fixes ratios and
shapes, with the absolute scale entering through external anchors (m_e micro,
ln(1+z_CMB)=7.004 cosmic). Galaxy rotation/dark-matter and the BAO D_H/AP branch remain
open. Net: the metric-pure distance+redshift+light-element layer is the durable macro
win; the CMB-anisotropy peak layer is the actively-reframed, partially-retracted frontier.
