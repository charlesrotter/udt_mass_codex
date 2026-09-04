# G346 audit report — directional angular-area reciprocity

Date: 2026-09-04
Grade: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## What was tested

G346 asked one metric-led question: after G342--G345 have supplied a two-screen Jacobi position
block, endpoint observer frequencies, metric screen forms, and the symmetric determinant scalar,
does the metric itself define the two directional infinitesimal screen-area per celestial-solid-
angle Jacobians?

The question was preregistered and pushed at commit `9a037558` before any outcome command ran. The
frozen formulas were not repaired or retuned after execution.

## Result

The bounded answer is yes:

```text
A_1<-0 = omega_0^2 abs(det B_10) sqrt(det q_1 det q_0)
A_0<-1 = omega_1^2 abs(det B_01) sqrt(det q_0 det q_1)
A_1<-0/A_0<-1 = (omega_0/omega_1)^2
sqrt(A_1<-0 A_0<-1) = 1/Dhat_10
A_2<-0 = hhat_1 A_2<-1 A_1<-0
```

The formulas follow from the fixed-frequency metric sky musical map `p=omega q theta`, the metric
solid-angle and screen-area forms, G343 reversal, G344 stationary endpoint algebra, and G345's
accepted scalar. No optical reciprocity theorem, inverse-square law, luminosity model, detector,
probability, or observational-distance convention was used.

## Provenance and premise audit

- The metric, reciprocal kernel, angular sector, and owner-provisional response equation are
  unchanged.
- Universal Reciprocity/DDR and the G312 premises remain owner-adopted provisional postulates, not
  derived or canonized.
- The exact Taub/Kasner spacetime, normal-observer congruence, endpoints, ray, and compact lift are
  supplied.
- Fixed observer frequency defines the bounded celestial-direction query; it is a declared query
  calibration, not a population or emission law.
- All common affine scales, marked events, projective directions, endpoint orders, and passive
  endpoint `GL(2)` coordinates remain free and were covered.
- Each compact lift remains a separate label. Nothing selects or sums routes.
- No matter, mass, observation, physical scale, or `X_max` entered.

## Evidence

- Production: `11204/11204`; largest recorded error `3.542999227335031e-14`.
- Implementation-distinct verification: `4251/4251`; direct log-time RK4 Jacobi columns included;
  largest recorded error `9.98350167131679e-11`.
- Hostile mutations: `20/20` caught.
- Fresh external review: authenticated all 29 payloads, reproduced the `19/19` sealed aggregate,
  independently reconstructed the principal identities, and accepted without required repair.
- Repository guards: exact 329-row premise verifier passed; full suite passed 221 tests with the
  one pre-existing documented xfail.
- Analytic coverage: positivity on the entire noncoincident positive-time segment follows from the
  one-sign integral representation of both `B` channels; coordinate, affine, reversal, mean, and
  sewing laws are determinant identities rather than sampled extrapolations.
- Principal and coincidence behavior: both exact axes retained; directional Jacobians vanish
  quadratically at coincidence.

## Four banking gates

1. Preregistered: `PASS` — commit `9a037558` predates all outcome execution.
2. Full space or bounded scope justified: `PASS` — full stated noncoincident endpoint/direction/
   gauge tile; generic spacetimes, observers, finite beams, transfer, and populations explicitly
   excluded.
3. Independently verified on the load-bearing premise: `PASS` — implementation-distinct quadrature
   plus direct Jacobi integration passed, followed by a fresh external scratch reconstruction.
4. Every premise audited: `PASS` — `PREMISE_LEDGER.tsv`; no untyped physical import.

Accordingly the bounded result is externally accepted. The reviewer retained the non-blocking
warning that unconditional, string-based, and text-token guards are evidence-integrity sentries,
not mathematical proof; the analytic derivation and independent reconstructions remain the
load-bearing evidence.

## Maximum conclusion

G346 can at most add two exact infinitesimal metric angular-area Jacobians, their squared-frequency
reversal, their inverse-G345 geometric mean, and stationary sewing on the supplied conditional
G340--G345 family. It does not add brightness, flux, luminosity, probability, amplitude,
electromagnetic transfer, selected observational distance, route/population, generic stability,
occupancy/history selection, matter/mass, physical scale, `X_max`, or canon.
