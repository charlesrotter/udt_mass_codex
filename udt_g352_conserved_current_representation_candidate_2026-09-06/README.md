# Decision brief — conserved-current representation candidate

Date: 2026-09-06. Current status: VERIFIED-WITH-CAVEATS, UNPROMOTED CONDITIONAL CANDIDATE.
Accepted-source snapshot: `3a31db478b094efc9bce5291349b552aed95059c`.
Fresh separate-context review of frozen candidate `a4525d21` found no substantive
mathematical defect or required repair. See the
[review summary](review_2026-09-06/REVIEW_SUMMARY.md). The authorized verification
cycle is complete. This remains recoverable candidate evidence, not scientific
promotion or an accepted dependency; original construction files remain frozen.

## What the reviewed argument establishes conditionally

The supplied smooth G352 product has a local covariant current representation:

    C = [s(lambda)/(DeltaTheta J)] grad Theta,
    div C=0,             -g(u,C)=Gamma.

J is the metric screen-area density in the supplied label chart. The proposed
argument shows it is also the metric volume factor in phase/ray/label coordinates.
The current is unique for the FIXED supplied product, phase and geometry. It
does not determine that product or supply physically populated content.

The converse has strictly more freedom:

    C = [F(Theta,lambda)/J] grad Theta,   F>=0 smooth.

Conservation removes dependence along the ray-flow parameter but does not impose
the same population on neighboring phase sheets. G352's chosen product requires
the further condition F=s(lambda)/DeltaTheta, relative to its fixed phase and
cross-phase identification. That condition is already a supplied realization
choice, not newly adopted by this candidate.

In plain language: this route connects the supplied smooth measure/readout to a
spacetime current without adding a physical equation. It does not explain what
is carried or how much. The remaining data freedom defeats selection by this
representation alone, not every conceivable metric-native realization route.

## Ownership and limits

- Metric: supplies local screen area, volume, gradient and observer contraction.
- Owner-provisional G351/G352 premises: conservation of supplied content and
  the specified clock-rate reading, not a populated physical object.
- Chosen realization: supplied phase/spacing, cross-phase identification and
  continuous phase-independent product.
- Candidate: a local smooth representation and exact comparison-class converse.

All claims are restricted to a regular local flow box with smooth nonnegative
density. Zero is retained; ratios require nonzero density. No caustic, singular
measure, atomic count, global extension, detector, light, energy, source, physical
population, action, matter, history, scale, X_max or canon follows. The prior
normalized-cone result remains unpromoted and is not needed as an accepted input.

## Evidence at construction

The general argument is in CANDIDATE_ARGUMENT.md, not inferred from check counts.
The first exact baseline and recorded replay each passed 43 assertions. Six
intentional implementation mutations failed at their specified AssertionError:
missing area factor, coordinate-only divergence, always-zero divergence, treating
all phase densities as products, missing observer frequency, and missing passive
label Jacobian. CHECK_RESULTS.json preserves actual child exits and both streams.
No capture-wrapper exit is used as a test verdict.

A stdlib-only rational recomputation from saved inputs agrees on two cut areas
16 and 100, frequencies 1 and 1/2, absolute readouts 7/30 and 7/375, and ratio 2/25.
It uses a separate implementation but the SAME author/context, not independent
review. The fresh reviewer first reconstructed from accepted sources without
this argument/code/results, then directly challenged the frozen candidate. Its
independently implemented full-map differentiation and exterior-product check
also reproduced the readouts, including an off-origin transverse-observer control.

No accepted-source full production suites or empirical/global tests are claimed.
The parent ran the existing 335-row premise verifier successfully during
construction and at closure; exact streams accompany the completed review record.
Twelve existing focused policy/startup tests passed. The original 13-file candidate
was frozen before direct review. No scientific repair was needed; an incorrect
working-directory manifest invocation and its correct-directory verification are
retained as operational history. The review found no required unresolved repair.
Exact reviewer model is UNKNOWN; different-model review is UNTESTED. These claims
remain local, smooth and conditional; integrated rates still require the accepted
frequency-integrability condition when asserted.

No accepted scientific grades, sources, LIVE, manuscript or CANON were changed.
The completed infrastructure audit and fixed-snapshot manuscript remain separate
from the open physical-realization frontier. Backup completeness and pre-reboot
unsaved-state disposition remain UNVERIFIED; ScratchDisk blocks archive-dependent
tasks only. Protected payloads and original unrelated local work remain untouched.
