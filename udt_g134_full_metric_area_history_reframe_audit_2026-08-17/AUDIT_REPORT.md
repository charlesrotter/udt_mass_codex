# G134 audit report — full-metric area rule and physical-history reframe

Date: 2026-08-17

Status:

`FRESH_ADVERSARIAL_FOLLOWUP_PASS__AREA_BILINEAR_METRIC_FAITHFUL__RELATION_NETWORK_ADMISSIBILITY_REFRAMED__HISTORY_SELECTION_OPEN__VERIFIED_WITH_CAVEATS`

## Result

The full-metric bivector area bilinear is faithful to the complete Lorentz metric, including common
scale. In dimension at least three, `A_g=A_h` implies `h=+g` or `h=-g`; the fixed UDT
clock-negative/ruler-positive convention removes the minus branch.

In four dimensions the map has ten inputs and twenty-one symmetric bivector outputs. Its exact
Jacobian has rank ten, so metric-induced complete area data have local codimension eleven inside
arbitrary symmetric area-bilinear data. This is a real closure condition on independently supplied
observer-plane and cross-plane relations.

The result does **not** select a physical history. Every smooth regular Lorentz metric automatically
produces one such compatible area field. Current Reciprocity fixes the reciprocal channel grammar
on supplied depth, and co-presence supplies conditional common-solution semantics; neither assigns
the numerical area/metric field.

## The conceptual reframe

The area rule is more than an evaluator of one plane but less than an evolution law.

- Metric-first: it evaluates and faithfully repackages the supplied `g`.
- Relation-first: it rejects arbitrary mutually incompatible plane data and, when complete values
  and cross-plane soldering are present, reconstructs `g`.
- Physics-first: it does not say which compatible numerical field Nature realizes.

Thus a complete valued area field does not need a second “history selector”; it already represents
the history. The remaining open joint is the law, if any, that owns its values and evolution.

## Evidence

- preregistered and pushed at commit `bfff5a9a` before outcome execution;
- exact SymPy route: 23/23 checks pass;
- independent standard-library `Fraction` route: 19/19 checks pass;
- catch-proof route: 5/5 over-promotion guards pass;
- exact rank 10 and local codimension 11 at Minkowski and an independent generic rational Lorentz
  metric;
- exact conformal weight, determinant identity, sign kernel, self-area ambiguity, cross-area
  resolution, reciprocal/unipotent separation, and two-history countermodel exercised;
- premise verifier passed immediately before preregistration;
- fresh external adversarial review accepted the mathematical landing and independently reran all
  four check suites;
- repair-only external follow-up verified the corrected 19/20/21 intake counts, every current
  intake hash, and the unchanged mathematical landing, returning `FOLLOWUP_PASS`.

One implementation-only repair replaced a structural SymPy equality with a simplified zero-matrix
residual. The fresh reviewer then required one intake-count field clarification. The external
repair-only follow-up passed. Neither repair changed an equation, candidate, premise, witness, or
landing.

## Maximum current conclusion

`VERIFIED_WITH_CAVEATS` in the bounded regular pointwise/overlap scope: complete `A_g` is equivalent
to complete `g` up to the fixed sign convention, and metricity supplies nontrivial compatibility
constraints on arbitrary relation-network area data.

Still `OPEN`: a nonidentity physical value/evolution/global-admissibility law; physical query and
cross-plane soldering data; singular and global completion; observations; `X_max`; action, source,
bootstrap, matter, mass, and signalling.
