# OB1 source-preserving clarifications

INITIAL_CANDIDATE.md remains byte-identical. Its §4 defines fitted Use B's D as a free
effective delay and explicitly says an unknown frequency-linear instrumental delay leaves
only D_g+d_inst inferable. In §5/Eq8, D_max must therefore bound that TOTAL effective delay,
including any unresolved linear instrumental contribution. A bound on geometric D_g alone
does not suffice when d_inst is unbounded. Independent finite coarse information is required
unless actual frequency spacing is controlled exactly or another valid error treatment is used.

For independent-geometry Use A/Eq9, an instrumental delay must be independently corrected or
covered by the stated delay/phase uncertainty; geometric uncertainty alone cannot excuse an
unbounded optical delay. Keep its error contribution once, with honest provenance and any
correlations; do not fit it using confirmation readings and call the geometry independently
predicted. This makes existing hypotheses explicit and adds no equation, physical premise,
mathematical claim, narrower valid domain or numerical bound.

Parent identified this possible reading ambiguity during direct review. The fresh reviewer
independently said the existing §4 definition supports the mathematics, and recommended this
overlay for practical clarity. Final review owns whether the clarification is sufficient.
Original candidate, author failure/repair history and source-first review seal remain unchanged.

The review also found a reporting error in frozen CHECK_HISTORY.md: the six deliberate failures
are FIVE computation mutations plus ONE deliberately false alias assertion, not six altered
scientific computations. In wrapped_alias the correct aliased readings are still computed and
the equality predicate is deliberately denied. It is an assertion/semantic canary and does not
independently recompute or corrupt the alias mapping. Preserve the code, stdout, manifest and
initial wording as history; this overlay and current closeout supply the corrected classification.
The fresh review reproduced all six expected failures and the original structural-equality
failure. No scientific candidate repair follows from this reporting correction.
