# Audit report — native flux/luminosity-law ownership

Date: 2026-08-15

## Result

For a supplied regular complete metric history and supplied typed null/screen observer query, the
metric-derived endpoint and Jacobi structures fix

```text
Z = exp(phi_pair),
d_G = Z d_A,
d tau_s/d tau_o = 1/Z.
```

Therefore, for differential emitted luminosity `L_Omega`, radiative survival `eta`, and endpoint
energy ratio `epsilon`, the exact regular-branch factorization is

```text
F_o   = L_Omega eta epsilon/(Z^3 d_A^2),
d_L^2 = Z^3 d_A^2/(eta epsilon)     [after source isotropy is supplied].
```

The Wronskian proof of `d_G=Z d_A` is general on the regular Levi-Civita screen-Jacobi stratum and
does not freeze the angular or mixing sectors. Time dependence and anisotropic screen response are
retained inside `D_f`.

## Nonselection theorem

For all real `p,q`, the regular positive character family

```text
epsilon=Z^-p,
eta=Z^-q
```

compose and reverse exactly on a matched observer network. They give

```text
d_L = Z^[(3+p+q)/2] d_A.
```

Thus the founded endpoint character, Reciprocity, exact composition, and complete angular/mixing
geometry do not select the remaining transfer product `eta epsilon`.

The power laws exhaust the positive character family under continuity, measurability, or local
boundedness. Composition and reversal alone admit still more pathological Cauchy characters. This
larger algebraic class strengthens rather than weakens the nonselection conclusion.

The historical relation is recovered conditionally from

```text
eta=1,
epsilon=1/Z,
```

which yields `d_L=Z^2 d_A`. That closure is compatible with the rebuilt kernel but is not currently
metric-derived. It requires a conserved carrier/current or wave action and a physical null-momentum
energy readout.

## Source regrade

The July luminosity audit correctly identified the clock, energy, and reverse-area factorization,
but its claim that minimal Maxwell and photon-number conservation were already metric-derived is no
longer authoritative. Current G13 owns only conditional toric `F=dS` and the identity `dF=0`; G16 and
G21 leave action, source, current, measure, boundary, and normalization open.

Therefore the recent G65/G93 classification of `d_L=Z^2d_A` as a conditional flux readout was
correct. This audit narrows that conditional to one exact positive transfer product rather than
refuting the relation.

## Evidence

- exact symbolic screen-determinant, Wronskian, flux, luminosity-distance, composition, and reversal
  checks in `derive_flux_factorization.py`;
- standard-library rotated anisotropic screen and direct energy/time/area bookkeeping replay in
  `verify_flux_factorization_independent.py`;
- three factor-drop catch proofs;
- current-authority source census with the superseded Maxwell promotion isolated.

Internal exact results:

```text
Wronskian derivative                         0 exactly
reverse determinant factor                  Z^2 exactly
independent reverse-transpose error          1.7763568394002505e-15
maximum independent area-ratio error        1.1102230246251565e-15
maximum independent factorization error     1.5543122344752192e-15
maximum character composition error         2.220446049250313e-16
factor-drop catches                         3/3
```

## Scope and omissions

This is one regular-branch propagation theorem, not a complete luminosity theory. It excludes
caustics, multiple-image aggregation, absorption/scattering, detector bandpass, source anisotropy,
intrinsic luminosity, physical history selection, and global completion. Those are classified, not
silently set to zero.

## Four gates

1. Preregistered: **PASS** before native-source census and new algebra.
2. Full or bounded: **PASS for the declared regular single-branch factorization**; global/singular
   and material-transfer strata remain open.
3. Independently verified: **PASS WITH CAVEATS** by a standard-library route and a fresh sealed
   zero-context algebraic/semantic reconstruction.
4. Premises audited: **PASS internally**; geometry, source, carrier, energy, current, isotropy, and
   detector roles are separated.

## Grade

```text
EXTERNALLY_VERIFIED_WITH_CAVEATS
__GEOMETRIC_RECIPROCITY_AND_Z3_FACTOR_OWNED_CONDITIONALLY
__RADIATIVE_TRANSFER_PRODUCT_OPEN
__HISTORICAL_Z2_LAW_COMPATIBLE_CONDITIONAL_CLOSURE
```

The accepted external landing is
`VERIFIED_WITH_CAVEATS__Z3_GEOMETRIC_CLOCK_FACTOR__TRANSFER_PRODUCT_OPEN`.

No SNe fit, physical history, `X_max`, BAO/CMB result, action, matter, mass, or bootstrap law follows.
