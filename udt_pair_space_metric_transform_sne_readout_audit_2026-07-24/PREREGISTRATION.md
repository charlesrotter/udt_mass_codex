# Pair-space metric-transform and SNe-readout audit preregistration

Date: 2026-07-24

Base: `148f84ea467d9716f8706c161efd45d0a381ecaa`

Compute: CPU-only exact algebra followed by a no-retune replay of two already
registered Pantheon+SH0ES readouts.

Mode: metric-led and observing, not targeting.

## Whole question

The repository contains three exact bounded profile shapes downstream of
different conditional structures:

1. anchored projective depth, `f_T(s)=tanh(s)`;
2. WR-L proper radial depth, `f_E(s)=1-exp(-s)`;
3. the conditional round B19 angular depth,
   `f_R(s)=(2/pi) atan(sinh(2s))`.

This audit asks:

- does composing any of these profiles with an already supplied
  observer-rest metric produce a mathematically valid bounded pair distance?
- what composition law and nonlocal/path-length distinction does each profile
  have?
- which complete metric-to-redshift-to-optics readouts can legitimately be
  compared to the existing SNe observations?
- does the observed SNe contrast select a pair-distance profile, or does it
  test a different metric readout?

## Bounded regime

Covered:

- a supplied metric space `(M,d)` with `d>=0`;
- positive symbolic `X` and `kappa`;
- the three fixed normalized profiles above;
- exact monotonicity, concavity, subadditivity, triangle inequality, endpoint
  behavior, and collinear composition;
- the existing 1,580-object Pantheon+SH0ES cut and full covariance;
- exactly one additive magnitude offset;
- only the two already complete and registered SNe readouts:
  WR-L areal/optical `d_L/X=z(z+2)` and projective J1
  `d_L/X=u^2(u^2-1)/(u^2+1)`, `u=1+z`.

Not covered:

- deriving the base observer-rest metric or event pairing;
- selecting `X`, `kappa`, or one of the three profiles;
- equating a pair metric with local proper length, areal distance, optical
  distance, signal travel, or a full spacetime metric;
- resolving cut-locus angular transport;
- deriving a global UDT diameter or numerical `X_max`;
- scoring WR-L proper depth, B19, FC12, or the temporal-phi family as SNe laws
  without their missing redshift/areal/optical joins;
- BAO, CMB, black-hole, density, action, source, carrier, or GPU work.

## SNe firewall

All pair-space algebra and candidate classifications are fixed before the SNe
replay. SNe data may reproduce the existing score of a complete registered
readout. They may not:

- choose a profile;
- repair or complete a missing optical join;
- convert an areal-radius result into a proper-distance result;
- promote the retired imposed `P_ell` model;
- tune an exponent, scale shape, or additional nuisance parameter.

The data and covariance are pinned in `SOURCE_LINEAGE.tsv`.

## Certification contract

Certification requires:

1. exact proof that every accepted transform is increasing, concave,
   subadditive, and therefore preserves the metric axioms;
2. explicit proof that the transforms are generally not intrinsic path-length
   metrics;
3. exact associative collinear composition laws inherited from additive base
   distance;
4. a complete candidate/readout disposition with no SNe score where a required
   join is absent;
5. independent standard-library algebra plus a separate full-covariance SNe
   replay;
6. exercised catch-proofs for profile selection, distance-readout conflation,
   missing joins, retuning, and physical overclaim;
7. source-hash replay, repository gates, and the documented test baseline.

## Maximum allowed conclusion

At most this audit may establish a conditional mathematical family of bounded
observer-pair metrics from the three registered profiles, distinguish those
pair metrics from local length and optical/areal readouts, and reproduce which
already complete SNe readout is observationally favored within the registered
comparison.

It may not select a universal UDT pair law, derive `X_max`, infer new
cosmological physics, explain BAO/CMB/black holes, or strengthen any action,
source, carrier, boundary, or mass claim.
