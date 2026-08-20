# G191 audit — nonconformal time-live mixing join

Date: 2026-08-20

## Landing

```text
ONE_EXACT_NONCONFORMALLY_FLAT_TIMELIVE_MIXING_WITNESS_JOINS_FREQUENCY_AND_FULL_MATRIX_SCREEN
__PARAMETRIC_BRANCH_IS_MONOTONE_AND_POST_VERTEX_NONCAUSTIC_IN_THE_DECLARED_DOMAIN
__NO_STATIC_PROFILE_OR_POST_READOUT_ORCHESTRA_REQUIRED
```

Current grade:

```text
EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS
```

## Result

The preregistered complete coframe has nonzero trace-free screen curvature when `mu!=0`, so it is
not merely a conformally flat time-live control. Its completed central pair fixes the outgoing null
germ. Direct metric reconstruction then gives

\[
Z=(1+2H\lambda)^{-1/2}
\]

and the full matrix Jacobi map with eigenmodes

\[
f_+=\frac{\sqrt q}{2\sqrt2\mu}
\sinh\!\left(\frac{\sqrt2\mu}{H}\log q\right),
\qquad
f_-=\frac{\sqrt q}{2H}\log q.
\]

Both modes are positive after the vertex. Frequency is strictly monotone, so this particular
control has no frequency turn or post-vertex caustic and admits a single-valued local `d_A(Z)`.

The cross-screen entry `(f_+-f_-)/2` is nonzero without a fitted coefficient. At `mu=0` the result
reduces exactly to G190. At `H=0` it reduces to G188 after the declared affine normalization.

## Verification

- exact symbolic metric, Christoffel, Riemann, affine, frequency, and Jacobi residuals vanish;
- 20,000 independent random coframe/metric frames pass;
- 256 implementation-distinct RK4 branches pass;
- 387,680 independent assertions total;
- maximum frequency error `9.153788838034416e-14`;
- maximum Jacobi error `2.609086280358497e-10`, below `2e-9`;
- 15 hostile mutation and semantic catches pass.

The independent verifier had one documented numerical limit-probe repair before acceptance;
production and the scientific landing were unchanged.

The first external review found only a sealed-replay packaging defect. The preregistered repair
changed no scientific artifact. A corrected 36-file replay passed end-to-end, and the repair-only
external follow-up returned `G191_ACCEPTED_WITH_STATED_BOUNDS` with no remaining repair.

## Maximum conclusion

G191 is an exact mathematical witness that G190 survives simultaneous time dependence and live
mixing inside one complete metric. It does not identify the physical history, populate observer
pairs, derive transfer or luminosity, predict SNe, select branches globally, or determine `X_max`.
