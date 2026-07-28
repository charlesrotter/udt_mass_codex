# Post-verdict legacy ODE/time-live provenance addendum

The clean-room verdict was committed first at `6c89b7a`. Only afterward were
the contents of prior files named `time_live`, `timelive`, or `evol*` inspected.
No prior script was executed.

## Census

Exactly 21 tracked Python files match the preregistered name rule. They fall
into eight coherent equation families:

| family | files | actual equation provenance | current ruling |
|---|---:|---|---|
| old coupled GR/`S2` | 3 | Einstein equations plus supplied `S2` `L2+L4` action, harmonic balance, reduced/frozen background | historical; not a current native solve |
| old scalar/source evolution | 5 | independently evolved scalar/profile plus chosen two-exponential potential and spherical/radial boundary data | historical; current founded `phi` does not authorize it |
| `S2` stress probe | 1 | conditional `S2` `L2+L4` stress calculation | retained only as carrier-conditional comparison |
| nonround Sturm-Liouville proxy | 5 | linearized legacy scalar equation, chosen profiles and finite-box boundary data | historical scoped proxy |
| `w`-channel evolution | 2 | separately supplied wave action, source branches, `kappa`, and frozen/quasistatic geometry | historical; not current native dynamics |
| simple-`L` angular spectrum | 1 | fixed background, selected angular operator, Dirichlet endpoints, epsilon cutoff | conditional spectral readout only |
| `C2`/EH characteristic flux | 2 | explicitly conditional Bach and EH comparison lanes | retained comparison mathematics; neither action is selected |
| spherical areal polarization | 2 | metric-kinematic areal identities and conditional spherical representative | retained conditional kinematics, not evolution |

Counts:

```text
scripts                                                21
first introduced before 2026-07-01                    16
first introduced after 2026-07-01                      5
retained conditional non-background scripts            5
historical or currently blocked scripts                16
current native background/time-live solve authority     0
```

## Consequence

The warning was correct. The older scripts do not supply a shortcut around the
clean-room closure deficit. Most evolve equations that are now known to contain
a supplied action, imported GR closure, a POSIT carrier, an independently
treated scalar, chosen source potential, frozen background, proxy operator, or
boundary pins.

Two later audit families remain useful because they never claimed to solve the
background: conditional `C2`/EH characteristic comparisons and spherical areal
kinematics. The `S2` stress probe also remains meaningful only inside its stated
carrier premise. None supplies current native metric evolution.

The exact path-by-path hashes, introducing commits, equation families, choices,
and rulings are in `LEGACY_TIME_SYSTEMS.tsv`.

## Fail-closed controls

The independent verifier rejects a missing or duplicate path, any hash change,
promotion of a conditional action comparison, promotion of spherical kinematics
to background evolution, or authorization of any one of the 21 scripts as the
current native background solve. It also proves the clean-room production-result
Git blob is unchanged from commit `6c89b7a`.
