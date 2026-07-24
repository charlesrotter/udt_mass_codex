# Historical phi-equation salvage audit

Date: 2026-07-24

Base: `d000d9caace162723084941816077aa97dbf3c78`

Preregistration: `ea33657`

Grade: **VERIFIED-WITH-CAVEATS**

## Result

The old work contains useful exact mathematics, but it does not contain the
missing universal UDT `phi` law.

What is incorporated:

1. the reciprocal metric's `phi`-independent volume density in the static
   spherical control;
2. the exact radial scalar d'Alembertian;
3. the exact identity `Box_g phi=-G^theta_theta`;
4. the probe-versus-self-consistent variation fork;
5. the `sinh(mu r)/(mu r)` profile as a conditional linear probe control.

What is rejected as native UDT:

1. the chosen quadratic action as a metric-derived action;
2. the `mu^2 phi` screening term and `mu` scale as metric-selected;
3. the arbitrary source slot as a native source;
4. the fixed-background equation as the self-gravitating metric equation;
5. the linear micro profile as a universal profile;
6. the assertion that one screened equation governs every regime.

## Decisive correction

The historical derivation varies a scalar while keeping the metric fixed.
That correctly gives

```text
(Box_g-mu^2)psi=-S.
```

If the varied field is the same `phi` that determines `g[phi]`, the
Euler-Lagrange operator changes by exactly

```text
exp(-2phi)(phi')^2.
```

The old equation is therefore a valid conditional probe equation, not a
derived self-gravitating law for the metric profile.

## Current-work relevance

This correction helps the current program in two ways:

- it gives exact static controls for any future complete `phi` equation;
- it prevents a familiar screened-scalar template from being mistaken for
  the missing native action/source or observer-pair transition law.

It does not close the current gate. The old centered scalar equation supplies
no observer recentering, endpoint/event pairing, angular-screen transport,
path-family composition, or finite-cell cocycle.

The current bounded next question remains the complete-coframe
longitudinal-transverse observer transition. If a future branch supplies an
actual native `phi` equation and variation domain, the salvaged identities
become regression checks for its static spherical reduction.

## WR-L cross-check

For

```text
phi_WRL=-1/2 log(1-r/X),
```

the exact scalar operator is

```text
Box_g phi_WRL=1/(Xr).
```

Thus WR-L is not a zero-source solution of the historical screened equation
for any finite constant `mu`. The successful WR-L clock/area SNe readout
remains an independently supplied conditional profile; this audit neither
invalidates nor derives it.

## Evidence

- production reduced-action replay: 8/8 exact checks;
- independent direct four-dimensional tensor/EL reconstruction: 4/4 checks;
- historical source identity fixed at
  `1dba7fa26a7a658d1dabdce6d98974b52f007cb85a33796f2a80e05995b97b62`;
- original-checkout metadata now has 55 paths: the previously recorded 54
  metadata-only paths plus the explicitly supplied untracked `phiequations.md`;
  no dirty path was modified;
- prior June native-versus-posited and probe-versus-self evidence reproduced;
- CPU only; no solve, fitting, GPU work, action selection, source selection,
  profile selection, or research-artifact mutation.

No fresh external-model or zero-context agent was authorized, so the grade is
`VERIFIED-WITH-CAVEATS`, not canon.

## Original-file disposition

The original untracked historical file remains byte-identical and unmodified.
It is not copied into active authority because every useful formula is already
present in tracked evidence and is reproduced in this audit. Its overclaims
are scientifically discarded; the historical artifact itself is preserved.
