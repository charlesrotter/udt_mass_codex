# G189 fresh adversarial review request

Review the sealed G189 package as a cold mathematical and statistical audit. Do not defend UDT and
do not continue the research.

## Required checks

1. Reconstruct the static-query frequency ratio from the metric and verify the signs in
   `Z=exp(phi_s-phi_o)`.
2. Verify that G188/G119 plus the explicitly imported transfer gives `d_L=Z^2 d_A` and, centrally,
   `d_L=Z^2 R` without duplicating the screen.
3. Verify that a supplied monotone profile gives
   `d_L(Z)=Z^2 phi_inverse(log Z+phi_o)` and that the metric form alone does not select the inverse.
4. Verify the exact P1 retyping as one `phi(R)` profile.
5. Adversarially test the regular-center correction: does `R=R0 tanh(phi)` necessarily imply a
   nonzero first radial derivative and therefore fail smooth rotationally invariant central-scalar
   regularity?
6. Rerun both SNe calculations from the sealed data. Confirm that the candidate contains no P1
   shape parameter and only one analytic magnitude offset per catalog.
7. Audit the preregistered ceilings and landing. A statistical criticism may change the strength
   of the observational wording but must not turn this bounded control into a kernel verdict.
8. Check that the alternate transfer control is not used to select a transfer law after seeing the
   outcome.
9. Search for shared-code false independence, hidden `X_max`, post-readout angular factors,
   Lambda-CDM distances, or protected/repository dependencies.

## Required landing

Return exactly one primary grade:

```text
G189_ACCEPTED_WITH_STATED_BOUNDS
G189_ACCEPTED_WITH_REPAIRS
G189_SCIENTIFIC_LANDING_REQUIRES_REGRADE
G189_REJECTED
```

State separately whether the metric-to-flux factorization, regular-center type failure, numerical
negative, and localization of P1 to profile/frequency history each survive.

## Replay

From the sealed intake root, use:

```bash
G189_DES_ROOT="$PWD/external_data" \
python3 udt_g189_p1_free_metric_flux_interface_2026-08-20/verify_package.py
```

The review is read-only. Inspect only the sealed intake; do not edit files or continue the
research.
