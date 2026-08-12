# G85 preregistration — mixed AM time-live/global-completion atlas

Date: 2026-08-12

Mode: `MAP -> OBSERVE`, metric-led, exact analytic plus bounded CPU verification

## Whole question

For every one of the `196` nonzero-mixing AM controls frozen by G84, what happens to the
`x=2` / `chi=pi/2` completion problem when the complete metric is allowed to use time-live
clock-radial and lapse channels, rather than retaining only the stationary axial cross term?

The calculation will classify regularity, signature, and the causal type of the candidate seam.
It will not ask which completion resembles the desired universe and will not select a physical
profile, topology, scale, endpoint, source, or observable.

## Fixed source universe

`SOURCE_MANIFEST.tsv` freezes eleven source artifacts. The profile universe is exactly the `196`
rows in G84 `PROFILE_COMPLETION_ATLAS.tsv` with nonzero `q(4)`. The G84 zero-mixing row is retained
as a control but is not counted among the mixed rows. No profile may be dropped or ranked.

The G75 authority ends at `0<=x<=1`, equivalently `0<=chi<=pi/6` on the north chart. Any change
outside that region is explicitly `FREE_AND_EXPLORED`; it is not a continuation selected by UDT.

## Metric frame

On the G84 minimal doubled spatial candidate, start from

```text
ds^2/R^2 = u dτ^2 + 2 b dτ dχ + 4 dχ^2
            +4 sin(χ)^2(dθ^2+sin(θ)^2 dψ^2)
            +2 h sin(θ)^2 dτ dψ,
```

where the frozen stationary continuation has `u=-cos(chi)^2`, `b=0`, and
`h=4 sin(chi)^2 q(4 sin(chi)^2)`. Time dependence in `u`, `b`, and `h` is allowed only as an
explicitly labelled completion family. This is a bounded chart on the candidate `R x S^3`, not a
claim that this topology or split is physical.

## Preregistered completion archetypes

Each mixed row is classified under all five archetypes in `COMPLETION_ARCHETYPES.tsv`:

1. `PRESERVE_STATIONARY_GERM`: retain the exact polynomial continuation, `u_H=0`, `b_H=0`.
2. `MIXING_ONLY_TIMELIVE`: allow arbitrary smooth time dependence in `h_H(t)` while retaining
   `u_H=b_H=0`.
3. `RADIAL_SHIFT_TIMELIVE`: retain `u_H=0` and the nonzero mixed seam value while allowing a smooth
   clock-radial shift with `b_H(t)!=0` on the tested time interval.
4. `LAPSE_LIFT_TIMELIVE`: retain `b_H=0` while allowing `u_H(t)<0` on the tested interval.
5. `MIXING_TAPER_BEFORE_SEAM`: preserve the frozen metric on `0<=chi<=pi/6`, then explore smooth
   continuations for which `h_H=0`; both zero-shift and shift-supported subcases are retained.

These are algebraic/regularity archetypes, not dynamics. The symbolic amplitudes and time
frequencies remain `FREE_AND_EXPLORED`; no preferred value is inserted.

## Exact tests

At either equatorial axial fixed point, reduce to the clock-radial block

```text
G_H = [[u_H,b_H],[b_H,4]].
```

The preregistered regular-Lorentz gate is `det(G_H)=4u_H-b_H^2<0`. Pointwise rank cannot be
repaired by time derivatives alone.

Away from the axis, compute the determinant, Schur complement, and the induced seam metric. The
seam is called uniformly null only if its induced metric is degenerate at every angular point.
No coordinate component by itself will be treated as an invariant horizon test.

Constructive completions must:

- equal the frozen G75 control exactly on its authoritative north cell;
- be at least `C2` in the computational witness and admit a stated `C-infinity` bump replacement;
- keep Lorentz signature on the complete candidate domain and bounded time interval;
- retain all nonzero-mixing profile rows; and
- expose every free continuation function and parameter.

## Outcome classification

Every profile/archetype row receives exactly one:

- `POINTWISE_DEGENERATE`;
- `REGULAR_LORENTZ_NONUNIFORM_SEAM_CAUSAL_TYPE`;
- `REGULAR_LORENTZ_UNIFORM_NULL_SEAM`;
- `REGULAR_LORENTZ_NONNULL_SEAM`;
- `CONDITIONAL_ON_NONVANISHING_SHIFT`;
- `OPEN_OUTSIDE_BOUNDED_CLASS`.

The labels characterize; none is a merit filter.

## Falsification and certification

`FALSIFICATION_CONTRACT.tsv` is frozen before calculation. Certification requires:

1. exact determinant and induced-seam algebra from two implementations;
2. one row per `196 x 5` profile/archetype pair, without duplicates;
3. explicit treatment of axis, off-axis, coincidence, and shift-zero times;
4. a constructive global witness on the G84 candidate for each claimed existence class;
5. hostile catches for profile omission, time-derivative rank repair, shift zero crossing,
   false uniform-null promotion, source mutation, and physical-ownership promotion; and
6. the full repository gates before banking.

## Maximum allowed conclusion

At most:

```text
BOUNDED_KINEMATIC_TIME_LIVE_COMPLETION_ARCHETYPE_ATLAS_ON_THE_G84_CANDIDATE.
```

Even a constructive survivor is not a selected UDT history, physical `X_max`, global observer
wall, CMB prediction, source, action, matter law, bootstrap closure, or signalling law. If the
complete-coframe freedom makes all archetypes underdetermined, that underdetermination is the
result; no equation or boundary rule will be invented.
