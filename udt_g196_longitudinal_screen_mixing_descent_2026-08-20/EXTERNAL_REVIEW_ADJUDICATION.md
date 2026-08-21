# G196 external-review adjudication

Date: 2026-08-21

## Landing

`G196_DIRECTIONAL_DESCENT_ACCEPTED_WITH_CAVEATS`

The external reviewer accepted the bounded exact theorem for the displayed positive `a(eta)`,
arbitrary-real `M(eta,z)` affine coframe family and one supplied central outgoing germ. It found no
surviving algebra, sign, basis, factor-order, no-caustic, alias-scope, or claim-scope defect.

The review live-replayed the exact metric/connection/curvature derivation with all 17 assertions
true, the hostile controls with 9/9 mutations caught, and the eight-row source manifest. It also
verified that all sealed intake hashes were unchanged after review.

## Retained bounded theorem

On the declared family and germ:

- longitudinal dependence descends to `D_plus = partial_eta + partial_z`;
- the screen connection is `C_s = 2 Omega`;
- the coordinate equation factors as
  `(D_plus - 2 M^T)(D_plus + 2 M)Y = 0`;
- the ordered representation is `D = a L K`, with `L' = -2 M_bar L` and
  `K' = L^-1 L^-T`;
- the exact positive-Gram argument gives `det(D) > 0` at every nonvertex point on each connected
  regular outgoing-ray interval;
- pure rotation supplies connection carry but no independent focusing tide.

## Required evidence repairs

The reviewer identified two narrow evidence defects that do not change the theorem:

1. The Torch metric-jet, curvature, screen-connection, and tide contractions are independently
   implemented, but the interval Jacobi comparison is formula-driven regression: its direct
   second-order and ordered `L,K` systems share the separately coded candidate coefficient builder.
   Current prose must not call that IVP comparison a fully independent metric-to-Jacobi
   re-derivation.
2. The sealed replay needs a Torch-import-safe no-write path. In a strictly read-only sandbox,
   Torch's optional import chain rejected every temporary directory before the numerical verifier
   began.

Both repairs are preregistered separately before implementation. Until they are completed and
re-reviewed, the package grade is
`EXTERNALLY_ACCEPTED_BOUNDED_THEOREM__EVIDENCE_REPAIRS_PENDING`.

## Local repair outcome

Both preregistered repairs subsequently passed the full local no-write package replay under a
mode-`0555` declared temporary directory, with the complete 204-history census, artifact identity,
and zero runtime-directory entries. Fresh repair-only external review then ran the exact registered
replay in a strictly read-only sandbox. It exited zero in `1336.947` seconds; all 38/38 scope hashes
matched before and after and `.review_runtime` remained empty. R1 and R2 are therefore externally
closed with landing `G196_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED`. The final bounded grade is
`EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS`.

No canonization is implied. The result does not cover arbitrary complete metrics or coframes, all
directions, selected physical histories, transfer or observations, or `X_max`.
