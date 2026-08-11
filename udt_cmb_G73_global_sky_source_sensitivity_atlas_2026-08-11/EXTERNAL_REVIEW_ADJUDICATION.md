# G73 external-review adjudication

Date: 2026-08-11

External landing: `VERIFIED_WITH_CAVEATS`.

Effective evidence state:
`EXTERNALLY_VERIFIED_WITH_TOPOLOGY_SCOPE_CAVEAT_CLOSED_LOCALLY`.

## Science adjudication

The reviewer upheld the load-bearing G73 result:

- regular bijective sky response with pointwise `GL+(2)` response is exactly source-invertible;
- strong shear obeys the derived angular-compression law and retains source amplitude;
- scalar pullback remains distinct from vector/tensor response and physical TT/polarization;
- repeated-source directions, multibranch arrivals, rank loss, and detector combination are
  distinct mathematical types;
- all physical source, endpoint/profile, scale, detector, branch-combination, and TT/TE/EE/BB
  owners remain open.

The reviewer verified all `32/32` sealed hashes before source use and independently recomputed every
G68 map directly from `FINITE_PATH_ATLAS.tsv`. Its strongest row was again `G68_F02_AM_P20`, with
`chi=0.00232380596997883897`, singular-value ratio `1.00465842883942136`, and anisotropy gain
`0.465842883942135799%`. The tiny final-digit differences from the banked values are ordinary
floating-point route differences and do not change the weak-anisotropy classification.

## Caveat and correction

The reviewer identified one wording risk: “singularity is required” is correct for nontrivial
repeated whole-sky smooth `S^2 -> S^2` self-imaging, but too strong as a universal statement.
Different topology, partial-sky domains, or branch-labelled relations may admit regular
noninjective/multibranch structure.

`TOPOLOGY_SCOPE_CORRECTION.md` and `TOPOLOGY_SCOPE_LEDGER.tsv` close this caveat without rewriting
the reviewed package. The general condition is global noninjectivity/branching; singular or
critical behavior is required only under the explicit whole-sky `S^2` self-map hypotheses.

## Status ledger

- `DERIVED`: regular source recovery; strong-shear angular law; conditional whole-`S^2` covering
  theorem.
- `OBSERVED`: all 21 G68 rows regular and weakly anisotropic.
- `CHOSE_QUERY`: G68 stationary/equatorial profiles, endpoint, screens, and affine calibration.
- `CONDITIONAL`: source/observer sky topology, global relation class, strong-shear realization.
- `WORKING`: `X_max`, bootstrap, co-presence/global completion, and SNe compatibility.
- `OPEN`: physical global sky relation, source statistics, endpoint/profile/scale, branch weights,
  detector law, caustic continuation, and TT/TE/EE/BB observable map.

## Next gate

Map the complete symbolic-scale observer-sky relation by topology and critical structure: bijective,
regular multi-cover where topology permits it, branch-labelled, critical/fold, and singular. Do not
fit a CMB pattern or assume whole-sky `S^2` self-map topology before it is supplied.
