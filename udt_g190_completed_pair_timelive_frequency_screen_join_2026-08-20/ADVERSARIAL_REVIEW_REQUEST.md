# G190 fresh adversarial review request

Review the sealed G190 package as a cold mathematical and type-ownership audit. Do not defend UDT
and do not continue the research.

## Required checks

1. Reconstruct the orthonormal pair frame from the completed pullback and verify that `U +/- N`
   are exactly the two future normalized null directions in the pair plane.
2. Check the ownership claim carefully: does this derive only the local null initial germ, while a
   later endpoint intersection and physical observer population remain supplied/branch-typed?
3. Verify the frequency ratio and the sign of
   `d omega/d lambda = -k^a k^b nabla_a U_b`. Check the affine/nonaffine boundary and common-ray
   rescaling invariance.
4. Verify that the initial screen is the orthogonal complement of the completed pair plane and that
   the finite propagation is exactly G188's quotient-screen matrix Jacobi system, without
   scalarization or a new carry coefficient.
5. Verify the inverse-function statement: the parametric `(Z,D)` response is always the primary
   regular-branch object; `d_A(Z)` is only local where frequency is one-to-one, with the declared
   noncaustic qualification.
6. Independently reconstruct the conformal time-live control, including affine `k`, frequency,
   screen tide, Jacobi solution, and `d_A(Z)=-log(Z)/(H Z)` on the declared interval.
7. Check that G189 and G116 are downstream specialization/regression checks and were not used to
   construct the general result.
8. Search for hidden P1, static `phi(R)`, `R(Z)`, `X_max`, fit, post-readout angular score, native
   radiative-transfer claim, or physical-history-selection claim.
9. Rerun `verify_package.py --no-write` from the sealed intake and inspect independence claims rather than
   accepting self-reported JSON.

## Required primary grade

Return exactly one:

```text
G190_ACCEPTED_WITH_STATED_BOUNDS
G190_ACCEPTED_WITH_REPAIRS
G190_SCIENTIFIC_LANDING_REQUIRES_REGRADE
G190_REJECTED
```

State separately whether each survives:

- completed pair to normalized local null germ;
- endpoint frequency and differential evolution;
- full matrix screen join;
- time-live exact witness;
- local `d_A(Z)` descent condition;
- G189/G116 post-result specialization status;
- the stated ownership ceiling.

The intake is read-only. Do not edit files or continue the research.

## No-write replay

```bash
python3 udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20/verify_package.py --no-write
```
