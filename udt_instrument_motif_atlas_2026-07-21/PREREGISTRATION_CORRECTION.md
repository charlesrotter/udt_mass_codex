# Preregistration Correction — Nonempty-Lattice Edge Count

Date: 2026-07-21

Parent preregistration commit: `ba2d662`

Status: `PREREGISTERED_BEFORE_ANY_NEW_MOTIF_OUTCOME`

The original preregistration correctly froze all 31 nonempty subsets of five instrument groups but
incorrectly counted 80 directed one-bit addition edges among those subsets. The full five-dimensional
Boolean lattice has `5 * 2^4 = 80` upward edges only when the empty subset is retained. Five of those
edges originate at the excluded empty subset and terminate at the singleton instruments.

The exact registered edge count for the nonempty subset lattice is therefore:

`80 - 5 = 75` edge types and `75 * 6,144 = 460,800` original edge rows.

All references to 80 edge types or 491,520 original edge rows in `PREREGISTRATION.md` are superseded
by 75 and 460,800 respectively. Catch-proofs K03 and K04 must reject any edge registry that does not
contain exactly those 75 unique source/destination identities. The 31-family registry, 190,464
family-row count, nonlinear family count, classifications, premises, and maximum conclusion are
unchanged.

