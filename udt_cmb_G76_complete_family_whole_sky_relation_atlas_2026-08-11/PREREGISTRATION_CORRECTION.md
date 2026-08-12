# G76 preregistration correction — F01 whole-sky gate

Date: 2026-08-11

Base preregistration commit: `c3c2699d`

Status: correction recorded before solver construction or any G76 sky response.

## Error

The original preregistration required the three `q=0` F01 rows to reproduce an “identity sky map.”
That conflated the local G68 Jacobi normalization `D=sI` with G74's off-center whole-sky endpoint
relation. From an observer at `(1/4,0,0)` to the first crossing of the sphere `|X|=1`, the F01 map
is generally not pointwise identity. G74 proves and numerically records it as a degree-one global
diffeomorphism.

## Corrected gate

Replace every G76 requirement of pointwise F01 identity by both:

1. all three zero controls reproduce the corresponding frozen G74 level-4 endpoint arrays within
   maximum chord error `5e-6`; and
2. each has complete crossing, no negative or near-zero faces at the registered mesh threshold,
   and degree drift within the common `5e-4` convergence threshold, consistent with the exact G74
   degree-one theorem.

No other preregistered value, profile, threshold, output, or allowed conclusion changes.
