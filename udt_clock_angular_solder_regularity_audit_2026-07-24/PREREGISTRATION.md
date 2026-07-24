# Clock/angular solder regularity audit — preregistration

Date: 2026-07-24

Base: `aa654ce4eb696f5170a6b8366350071ff30134dd`

Compute: bounded CPU-only exact algebra

## Whole question

Can one positional-depth variable carry both the founding reciprocal clock
comparison and the conditional reciprocal-toric/Hopf angular depth inside one
regular complete finite-cell metric?

This is a metric-led classification. It does not ask which branch resembles
the desired universe and does not use an action, field equation, source,
carrier, density, mass, or empirical fit.

## Bounded regime

The audit covers static, diagonal, cohomogeneity-one Lorentzian coframes with:

1. the registered founding clock character `exp(-phi)`;
2. its fixed-pairing reciprocal depth character `exp(+phi)`;
3. a reciprocal angular pair `exp(-kappa phi), exp(+kappa phi)`, with every
   finite `kappa>0`;
4. positive physical common amplitudes retained explicitly rather than
   quotiented by strong local CSN;
5. the ordinary-frame normalization at `phi=0`;
6. both primitive round/toric caps and open/asymptotic ends; and
7. the conditional round spatial control
   `tan(eta)=exp(2 kappa phi)`.

The relative angular unit `kappa` is free and explored analytically over all
finite positive values. Reversal and circle exchange cover the opposite
orientation.

## Frozen solder families

| ID | Family | Exact definition | Maximum possible conclusion |
|---|---|---|---|
| F01 | isolated clock on round space | `N=exp(-phi)` with round spatial metric and `tan(eta)=exp(2 kappa phi)` | cap regularity only |
| F02 | fixed-pairing double reciprocal solder | `theta0=C exp(-phi)c dt`, `theta3=l C exp(phi)dphi`, `theta1=R exp(-kappa phi)dxi1`, `theta2=R exp(kappa phi)dxi2` | same-scalar diagonal compact/open viability |
| F03 | positive smooth physical common-factor round solder | `Omega_phys^2[-exp(-2phi)c^2dt^2+h_round]`, with `Omega_phys` smooth, finite, and nonzero at both caps | whether a regular physical common factor repairs F01 |
| F04 | open/asymptotic fixed-pairing family | F02 with arbitrary positive `C(phi),R(phi)` and no assumed cap | necessary endpoint relations; no profile selection |
| F05 | separated-role round control | constant-lapse round branch with angular depth only | logical control; no clock/angular join |
| F06 | patchwise, shifted, time-live, nonintegrable, or observer-pair realization | retained but not represented by F01--F05 | `OPEN_OUTSIDE_BOUNDED_CLASS` only |

Lorentz/coframe relabelings that leave the metric unchanged are not counted as
new physical families. Cross-pairings are tested algebraically; if their
weights differ they cannot preserve the same fixed pairing, and if the
weights agree they are a relabeling or a constrained subfamily of F02.

## Physical and mathematical choices

- `c=c_E`: `OBSERVED` calibration anchor.
- Reciprocal-c and dual Reciprocity: `FOUNDING`.
- Exponential characters: `DERIVED_CONDITIONAL` on composition, regularity,
  and the chosen sign/unit.
- Lorentzian metric readout: `POSIT / CHOSE`.
- Clock/depth slot identification: `CONDITIONAL`.
- Reciprocal-toric angular metric and Hopf coordinate: `CONDITIONAL`.
- Identity of clock depth and angular depth up to `kappa`: `TESTED_POSIT`.
- Positive physical common amplitudes `C,R,Omega_phys`:
  `free-and-explored` subject only to stated regularity.
- Strong local CSN: `CHALLENGED_OWNER_POSTULATE_NOT_DERIVED`; it is not used
  to erase any amplitude.
- Round caps and static diagonality: `CHOSE` bounded controls.
- Action, source, carrier, boundary functional, mass, density, and global
  observer pairing: `OPEN` and absent.

## Certification and falsification contract

The result is certified only if:

1. fixed-pairing algebra independently forces opposite exponents within each
   pair;
2. the F01 and F02 cap asymptotics are derived for arbitrary finite positive
   `kappa`;
3. a curvature scalar or invariant, not metric appearance alone, tests each
   alleged cap singularity;
4. ordinary normalization and the `kappa=1` round control replay exactly;
5. F03 cannot be called a repair unless its physical metric remains smooth,
   finite, and nondegenerate at both original caps;
6. F04 remains unselected whenever arbitrary profiles survive;
7. no conclusion is extended to F06; and
8. an independent implementation plus exercised corruption catches pass.

The compact obstruction is falsified if any finite `kappa>0` in F01 or F02
has a smooth, finite, nonzero lapse and finite curvature at both primitive
caps. The physical-common-factor ruling is falsified if a smooth positive
nonzero factor cancels the leading curvature divergence without changing the
cap completion. The algebraic classification is falsified if a genuinely
distinct fixed-pairing diagonal solder is omitted.

## Maximum allowed conclusion

At most:

```text
WITHIN_THE_STATIC_DIAGONAL_FIXED_PAIRING_RECIPROCAL_TORIC_CLASS,
SAME_SCALAR_CLOCK_ANGULAR_SOLDER_IS_REGULAR_AT_BOTH_CAPS
OR IS_NOT; OPEN_OR_NONDIAGONAL_REALIZATIONS_REMAIN_OPEN.
```

No complete UDT action, `X_max`, matter emergence, density closure, or global
universe claim can be derived by this audit.
