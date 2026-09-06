# Decision brief — conserved-current representation candidate

Date: 2026-09-06. Initial status: UNREVIEWED, UNPROMOTED CONDITIONAL CANDIDATE.
Accepted-source snapshot: `3a31db478b094efc9bce5291349b552aed95059c`.
The approved work order includes separate-context review and one bounded repair
cycle. This initial checkpoint is recoverable evidence, not scientific acceptance.

## What the argument proposes

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

In plain language: this route would connect the existing measure/readout to a
spacetime current without adding a physical equation. It would not explain what
is carried or how much. Failure of a proposed uniqueness-from-metric claim here
would not exclude every metric-native realization route.

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
16 and 100, frequencies 1 and 1/2, absolute readouts 7/30 and 7/375, and ratio2/25.
It uses a separate implementation but the SAME author/context, not independent
review. The fresh reviewer first reconstructs from accepted sources without this
argument/code/results, then directly challenges the frozen candidate.

No accepted-source full production suites or empirical/global tests are claimed.
The parent ran the existing 335-row premise verifier successfully during
construction; exact closure capture will accompany the completed review record.
The original candidate must be frozen before direct review; failures and repairs
remain in the review history.

No accepted scientific grades, sources, LIVE, manuscript or CANON were changed.
The completed infrastructure audit and fixed-snapshot manuscript remain separate
from the open physical-realization frontier. Backup completeness and pre-reboot
unsaved-state disposition remain UNVERIFIED; ScratchDisk blocks archive-dependent
tasks only. Protected payloads and original unrelated local work remain untouched.
