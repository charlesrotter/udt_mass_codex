# Macro Contamination Map

Status: provenance audit, not canonical. Created: 2026-06-10.
Trigger: Charles's standing flag (CANON.md): the Planck blackbody
derivation rides quarantined/withdrawn mass-emergence theories — do not
build on sand. This map grades every layer of the CMB observable chain
by provenance so macro work knows exactly what is load-bearing sand.
Recon sources: AUDIT.md (S116), /home/udt-admin/UDT canonical geometry +
dispatches (exact quotes and sections in the recon record). New file
only.

## Layer grades

| Layer | Grade | Notes |
| --- | --- | --- |
| Perturbation theory (delta-phi, RW gauge) | GEOMETRY | clean |
| Weld / momentum constraint (either form) | GEOMETRY | derived fresh; S116 + weld_status_results.md |
| Angular power ell^4 (spin algebra + parity) | GEOMETRY | clean |
| Radial weights r^2 e^{-3phi0}; weld-derived H1 weight | GEOMETRY | Tolman measure, clean |
| Native radial function + centrifugal cutoff | GEOMETRY | clean |
| Projection / radial-correlation form | GEOMETRY | clean (pure-Bessel form is flagged scaffolding) |
| Background profile phi0(r) as a FIT | DATA-FIT | Pantheon+ 0.94, DESI 0.90 sigma stand on data |
| Profile coefficients "derived, zero free params" | QUARANTINED-RIDE | the Diophantine triple (j,l,kappa) is legacy particle-sector content; the LABEL is sand, the fit is not |
| mu_g = pi*sqrt(pi/3)/13 | QUARANTINED-RIDE | the 13 is the legacy quantum-number sum; VALUE rides it; as a fitted scale it survives as DATA-FIT |
| BAO comb scale (Delta-ell ~ 297) | DATA-FIT / INPUT | observational |
| Temperature model: -delta-phi (Sachs-Wolfe piece) | GEOMETRY | Tolman redshift, clean |
| Temperature model: +1/4 delta-rho/rho (intrinsic piece) | QUARANTINED-RIDE | the 1/4 is Stefan-Boltzmann via the UDT blackbody (CG 11.7), which rides quantized Form-T Dirac matter — the flagged sand. NOTE: the ell(ell+1) structure of delta-rho is GEOMETRY (from G^t_t); only the coefficient's justification and the re-emergence labeling are sand |
| Recycling drive P(omega) (coherence, throughput) | QUARANTINED-RIDE + INPUT | the dissolution/re-emergence ontology; EE-TT phase and amplitude ride it |

## The critical finding for the weld discriminator

The asymmetric set — everything that differs between the native weld
(f phi0' H1 = 2 d_t dphi, algebraic) and the Einstein weld
(d_r(e^{-2phi0}H1) = 2 d_t dphi + d_t K, differential) — is entirely
GEOMETRY: the constraint form, the H1 radial structure, the
weld-derived weight. **No quarantined layer enters asymmetrically.**
The contamination (blackbody 1/4, mu_g's 13, recycling drive) is
common-mode or interpretive.

Therefore the discriminator CAN run honestly, as a differential test,
with this scoping (binding):
1. Conclusions are conditional: "given the common pipeline (flagged
   layers above held fixed as hypothetical), the data prefers weld X."
2. The discriminating observables must be weld-form-sensitive RADIAL
   structure (where the two welds genuinely differ), not amplitude
   channels that ride the recycling throughput (epsilon ~ 1-4) or the
   intrinsic-term coefficient.
3. The TT redshift channel (-delta-phi alone) is the cleanest fully
   geometric observable; predictions riding +1/4 delta-rho/rho carry
   the hypothetical flag explicitly.
4. Per the prior verifier's caution (weld_status_results.md): the PHASE
   channel may not discriminate (both welds give H1 ~ d_t dphi in
   time); the radial-weight channel is where they differ — exactly the
   channel the map grades GEOMETRY-clean.

## Standing consequences

- If the blackbody derivation is withdrawn entirely, the temperature
  model reverts to delta-T/T = -delta-phi alone and the ell^4 EE
  overshoot returns as the standing prediction — the S116 fix is
  conditional on the flagged sand. (The geometric half of the fix, the
  ell(ell+1) structure of delta-rho, survives; the coefficient does
  not.)
- The profile and all Gpc-scale normalizations survive as honest FITS
  (data-validated) even though their "zero free parameters" labels ride
  the quarantined triple. Re-grading the coefficients as fitted inputs
  changes no computation, only labels — recorded here so no future
  session cites "derived coefficients" as evidence.
- Tier-D / transfer-ladder work is micro-sector and untouched by this
  map.
