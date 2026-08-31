# G307 preregistration

Date: 2026-08-30
Pre-outcome parent HEAD: `9385ea2f`

## Question

On the bounded positive round G305/G306 completion, classify exactly how a supplied directed
observer relation and its screen data reduce the two-family Hopf-member ambiguity, then audit
whether active premises populate those data.

## Frozen landing candidates

1. `COMPLETE_RELATION_ALREADY_SELECTS_AND_POPULATES_ONE_PHYSICAL_HOPF_MEMBER`
2. `SUPPLIED_DIRECTED_GERM_SELECTS_ONE_MEMBER_PER_CHIRAL_FAMILY__SIGNED_TRANSVERSE_SCREEN_GERM_SELECTS_ONE_MEMBER_CONDITIONALLY__ACTIVE_PREMISES_POPULATE_NEITHER__PHYSICAL_MEMBER_REMAINS_OPEN`
3. `EVEN_SIGNED_SCREEN_COMPLETE_GERM_LEAVES_A_CONTINUOUS_MEMBER_FAMILY`
4. `NO_G306_HOPF_MEMBER_EXTENDS_A_GENERIC_REGULAR_DIRECTED_GERM`
5. `INCONSISTENT_OR_UNCLASSIFIED`

No landing may be strengthened after outcomes. Candidate 2 is the working hypothesis, not the
selected result.

## Exact checks

The production route must, without external packages:

- rederive left/right quaternion matrices and their metric/skew/complex-structure identities;
- prove existence and uniqueness of `u_L` and `u_R` for every regular unit `(p,v)`;
- prove both candidates agree on `span{p,v}` and therefore on the entire common great-circle route;
- prove their restrictions to the oriented transverse screen are opposite quarter-turns;
- count the remaining members at every data level in the registered ladder;
- preserve G299/G300's distinction between an available control germ and a populated lawful query;
- assert that metric and reciprocal kernel are unchanged.

## Independent and hostile checks

An implementation-distinct standard-library verifier must sample both chiralities, multiple radii,
random regular points/tangents/screens, and independently reconstruct the two members. Hostile
controls must reject at least: metric-only member selection, point-only direction selection,
one-member directed-germ count, path-only chirality selection, equal screen twist signs, supplied
screen called physically populated, normalized helicity called scale/mass, G300 query ownership
promotion, kernel change, and export outside the round completion.

## Certification contract

- Production algebra: exact, all assertions pass.
- Independent replay: at least 10,000 nonvacuous checks; maximum numerical error below `2e-10`.
- Hostile controls: every registered mutation caught.
- Premise audit: current exact registry passes; G298/G299/G300/G305/G306 ownership boundaries
  remain active.
- Maximum grade before fresh external review: `INTERNALLY_DERIVED_AND_INDEPENDENTLY_VERIFIED_WITH_CAVEATS`.

Any failure lands candidate 5 or a weaker explicit partial result.
