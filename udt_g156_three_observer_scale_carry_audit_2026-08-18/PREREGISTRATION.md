# G156 three-observer common-scale carrier and carry audit

Date: 2026-08-18

Status at registration: `PREREGISTERED__NO_G156_OUTCOME_INSPECTED`

## Whole question

For a supplied regular calibrated pair metric

\[
h=-T^2(dy^0+\beta dy^1)^2+L^2(dy^1)^2,
\qquad
\kappa=\tfrac12\log(TL),
\]

does the complete metric itself supply a coordinate-natural positive common-scale carrier, and how
does that carrier lawfully compare across a composable three-observer chain
\(A\to B\to C\)?

The audit must distinguish three different questions:

1. whether each regular pair plane owns an intrinsic scale line and metric section;
2. whether a **supplied** physical/query carry induces a gauge-invariant scalar scale character;
3. whether the active metric theory chooses a nonisometric carry, nonzero scale holonomy, or an
   evolution/history law for \(\kappa\).

## Bounded regime

- regular oriented time-oriented Lorentzian pair planes with positive \(T,L\);
- complete pair pullbacks before terminal readout;
- positive density and half-density lines;
- shared-carrier, supplied-carry, single-query, and genuine-overlap regimes already banked in
  G141--G144;
- three composable observer states and invertible orientation-preserving two-dimensional carries;
- the exact 19 sources frozen in `SOURCE_MANIFEST.tsv` at repository commit `b42c771d`.

This is metric-led. It is not a search for a field equation or a desired asymptotic behavior.

## Excluded from this test

- the protected curvature atlas, stopped native-on-shell draft, unbanked pair-response work, and G88;
- an action, source, matter, mass, Maxwell-like, bootstrap, carrier, boundary, or fitted law;
- SNe, BAO, CMB, \(X_{\max}\) value, AM seam, or any observational outcome;
- singular or null pair planes, cut loci, topology change, and orientation-reversing carries;
- promotion of common scale to gauge or of conditional carry to physical history evolution.

## Objects and notation fixed in advance

At observer state \(i\), let

\[
\ell_i=\nu_{h_i}^{1/2}
\]

be the positive metric half-density on the pair plane. In a calibrated basis,
\(\ell_i=e^{\kappa_i}|dy_i^0\wedge dy_i^1|^{1/2}\).

For a supplied carry \(M_{BA}:V_A\to V_B\) and endpoint triangular metric frames \(R_i\), set

\[
C_{BA}=R_BM_{BA}R_A^{-1},
\qquad
\sigma_{BA}=\tfrac12\log|\det C_{BA}|.
\]

The preregistered three-observer scale defect is

\[
\Omega^{\rm sc}_{ABC}
=\sigma_{BA}+\sigma_{CB}-\sigma_{CA}.
\]

No claim that \(M_{BA}\) is metric-selected is built into these definitions.

## Preregistered outcomes

Exactly one primary landing will be returned:

- `NO_SCALE_CARRIER`: no coordinate-natural positive line/section is supplied by a regular pair
  metric;
- `LOCAL_LINE_ONLY`: the metric supplies a local scale carrier, but no lawful gauge-invariant
  scalar carry exists even after a typed carry is supplied;
- `CONDITIONAL_FLAT_SCALE_CARRY`: the metric supplies the positive half-density carrier and every
  supplied typed carry induces a gauge-invariant determinant character; single-query and genuine
  overlap carries are flat or endpoint-exact, while the metric does not select a nonisometric
  cross-query carry or \(\kappa\) history;
- `METRIC_OWNED_NONTRIVIAL_SCALE_CONNECTION`: the metric alone selects a nonisometric scale carry or
  connection with nonzero scale holonomy;
- `MIXED_HOLONOMIC_SCALE_CARRY`: different already-owned regimes force both endpoint-exact and
  nontrivially holonomic metric scale carries.

## Certification and falsification contract

The result must pass all of the following:

1. exact verification of every source hash and byte count;
2. coordinate covariance of the positive half-density carrier;
3. endpoint-frame gauge invariance and composition of \(\sigma\);
4. exact derivation of the three-observer scale defect;
5. a counterexample testing whether zero scalar scale defect implies full matrix carry closure;
6. separate checks for one-query chart carry, genuine overlap, Levi-Civita metric transport, and an
   arbitrary nonisometric supplied carry;
7. an independent implementation with randomized exact or high-precision trials;
8. mutation catches for every principal category error;
9. the current premise and package verifiers.

The registered landing is falsified if the half-density is not coordinate-natural, if \(\sigma\)
fails gauge invariance or additivity, if metric-compatible Levi-Civita transport has nonzero scale
character, or if the active sources construct a unique nonisometric carry between otherwise
unglued queries.

## Maximum conclusion

G156 may classify the mathematical carrier and conditional three-observer scale-carry law already
contained in the complete pair metric. It may not derive a physical history, select a universe,
choose a cross-query comparison, activate a new connection, fix \(\kappa\), or canonize a result.
