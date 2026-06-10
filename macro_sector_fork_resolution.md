# Macro Sector Fork Resolution

Status: SYNTHESIS + CANONIZATION RECOMMENDATION — not canonical until
Charles signs off. Created: 2026-06-10.
Sources: udt_canonical_geometry.md (legacy SNe/BAO/Misner-Sharp machinery,
exact line citations below), /home/udt-admin/UDT current dispatches
(post-S117 state), AUDIT.md (S116 CMB EE dispatch, dropped by Charles).
This is a recon synthesis, not a new derivation; the one theorem applied
(C2, areal-chart equivalence) is banked in
native_positional_dilation_distance_readings.py. New file only.

## The question put to the macro sector

The rho-dynamics derivation (rho_dynamics_derivation_results.md) left a
three-way canonization fork: (1) the reading of "distance" in P0
(areal vs other); (2) the growth canon (unbounded vs strict-monotone
dilation); (3) the areal potential beta(rho). Charles directed: the
answers to (1) and (2) may lie in the macro sector — examine the SNe/BAO
work.

## Finding 1 — the macro sector canonizes the AREAL reading, by data

Every load-bearing macro observable treats r as the areal radius, with
phi = phi(r_areal), and the stack is validated against data:

```text
D_A = r              "the metric has r^2 dOmega^2, making r an areal
                      radius" (CG section 1.3, line 120)
d_L = r(z) * (1+z)   flux dilution over 4 pi r^2 spheres + one redshift
                      factor 1+z = e^phi (CG lines 1932-1936; current
                      dispatches CG section 28.2, archived VR 34.9)
D_M(z) = r(z)        BAO transverse distance = areal radius directly
m(r) = (c^2 r/2G)(1 - e^{-2phi})   Misner-Sharp mass — definitionally
                      an areal-radius object (CG line 1401)
```

Validation: Pantheon+ 1701 SNe, chi2/dof = 0.9397 (z > 0.01 cut),
RMS 0.164 mag — BEATING LambdaCDM (1.03) at zero vs six fitted
cosmological parameters, with the locked cubic profile
phi = (3/2)x - cos(pi/5)x^2 + (2/3)x^3, x = mu_g r, coefficients
algebraically fixed by the Diophantine triple. DESI DR1 BGS
framework-neutral BAO agrees at 0.90 sigma.

**Consequence via the banked C2 theorem** ([B=1/A in the areal chart]
<=> rho = ±r + const): if the dilation coordinate is canonized as the
areal radius — which is what the data-validated machinery already
assumes operationally — then **rho = r is FORCED**, P0's silent areal
choice becomes a theorem, and with the threshold rigidity theorem:

```text
BRANCH (iii) IS DEAD IN THE STATIC SECTOR.
No saturating areal function, no static throats, no threshold lifting.
The "uncovered metric function" is not rho.
The beta(rho) derivation is MOOT in statics.
```

Honest scope notes: (a) the macro data probes Gpc scales; a particle-
interior rho-structure at fm scales is not directly excluded by the
fits — it is excluded by canonizing the READING (the principle is
scale-global per the one-geometry charter). (b) The locked cubic is
ansatz-conditional (D-POLY-1) — but the areal role of r is independent
of the profile family; it sits in the observable definitions themselves.

## Finding 2 — the growth-canon question is SUPERSEDED: the macro domain is finite

The macro phi grows monotonically from phi(0)=0 to
phi(r_CMB) = ln(1101) = 7.003974 at r_CMB = 9.164 Gpc — and the domain
ENDS there. Per current canon (Theory Rule 5, static universe): "the
domain ends at the cosmological boundary; there is no beyond." The
universe is a finite cell with the CMB as its boundary surface. The
sourced cosmological profile is not a vacuum (the "vacuum gap": vacuum
alone reaches only phi ~ 0.75 of the needed 7.0), so the C=0 vs C>0
vacuum-selection question does not arise at macro scope.

So neither growth canon ("unbounded" vs "strict-monotone") is what the
macro sector instantiates. The actual macro canon is:

```text
MONOTONE GROWTH ON A FINITE DOMAIN TERMINATED BY A PHYSICAL BOUNDARY.
```

The mirror statement on the matter side (phi -> -phi, inside-out):
monotone decrease into the cell, terminated by the core endpoint. Both
sides are finite cells with monotone dilation — the same canon, mirrored.

## Finding 3 — the structural consequence for native discreteness

The open-domain threshold theorems (open_domain_discreteness_results.md,
native_threshold_rigidity_theorem.py) assumed r -> infinity with f -> 1.
**In the real UDT universe that premise does not hold: there is no
spatial infinity.** The probe's domain is [0, r_CMB]. Consequences:

1. **Branch (ii) — the compact domain — is realized BY THE COSMOLOGY,
   not by a cell-local mechanism.** Discreteness of the spectrum is
   automatic on the finite domain. The box-control scaling
   (omega ~ 1/R_box) is reinterpreted: the box is real, and it is the
   universe.
2. **But the scale is wrong for particle masses by construction:**
   omega ~ c/r_CMB is a Gpc-scale frequency. Finite-universe
   discreteness exists and is native, but it cannot BE the particle
   spectrum without a scale-decoupling mechanism (~40 orders). The
   discreteness question therefore transforms one final time: not
   "where does discreteness come from" (answer: the finite universe)
   but "what makes particle-scale cells spectrally autonomous from the
   global domain" — which is the mass-hierarchy question in yet
   another guise.
3. **Where Charles's phi-angular hunch survives:** the threshold
   theorems exclude only STATIC configurations. The macro CMB machinery
   (AUDIT.md) lives entirely in the NONSTATIONARY phi-angular sector —
   the rung-2 weld ties the angular metric perturbation H1 to the
   breathing field: d_r(e^{-2phi0} H1) = 2 d_t(delta phi) + d_t K - ...
   This is exactly a dynamical phi-angular interaction equation, derived
   from the metric, already validated against CMB structure. The
   "enlightened equations" Charles pointed at are the time-dependent
   weld equations — and time-dependence is precisely the scope exclusion
   of every no-go proved so far. The surviving native-discreteness
   candidates are: (a) nonstationary phi-angular bound structures
   (breather-class, weld-coupled); (b) the transfer-ladder route (which
   never needed a continuum threshold); (c) multi-cell/ensemble
   asymptotics.

## Canonization recommendation (Charles decides)

1. **Canonize R-areal**: "positional dilation grows with the areal
   radius" — it is what the data-validated macro stack already assumes,
   it makes P0's rho = r a theorem instead of a silent choice, and it
   closes branch (iii) statics cleanly. Cost: the static throat/
   effective-mass scenario dies (it was already failing to find a native
   beta).
2. **Replace the growth canon with the finite-cell canon**: monotone
   dilation on a finite domain with a physical boundary, mirrored across
   phi -> -phi. This dissolves the C=0/C>0 question at macro scope and
   aligns the matter-cell picture with the universe-cell picture.
3. **Redirect the discreteness program** to the nonstationary
   phi-angular sector (the weld equations), the transfer ladder, and
   ensembles — with the scale-autonomy question stated as the sharp
   target.

## Provenance

Recon agents 2026-06-10 (legacy corpus extraction; current-dispatch
extraction with Charles's layout guidance: root-level dispatch_* current,
validations/ stale). Exact formulas and line numbers as cited. The C2
theorem application is the only inferential step; it is banked and
verifier-confirmed (native_positional_dilation_distance_readings.py,
verifier ae8a655ed2fa4045f with the Killing-time amendment, which does
not affect the binary conclusion here).
