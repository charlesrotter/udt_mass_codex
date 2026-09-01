# G317 external adversarial review request

Review only the sealed intake supplied with this request. Do not edit evidence files or continue
the research.

## Question

Does the preregistered evidence justify the bounded landing

```text
EXACT_NONCMC_COUPLED_TORUS_FAMILY_EXISTS_WITH_ZERO_TIDE_AND_TIDAL_SUBBRANCHES
__CONSTANT_PSI_CLASSIFICATION_FORCES_LAMBDA_MINUS_Q_SQUARED
__NO_PHYSICAL_DATA_SELECTION
```

inside the declared constant-`psi`, flat marked-`T3`, diagonal-TT, one-coordinate non-CMC ansatz?

## Required adversarial checks

1. Starting from the sealed G315/G316 equations, independently derive `bar L W`, its divergence,
   the periodic mean subtraction, and `w'=p^6(tau-mu)/2`.
2. Recompute the total diagonal conformal tensor and reduced scalar residual. Check necessity and
   sufficiency of `alpha=2p^6mu/3` and `Lambda=-d^2p^-12=-q^2` for nonconstant `tau`.
3. Attack every coefficient, conformal power, and sign. In particular, distinguish this ansatz's
   negative relation from a global UDT sign theorem.
4. Reconstruct `gamma=p^4delta` and mixed `K=diag(tau,q,-q)` and verify the Hamiltonian and momentum
   constraints directly, not only through the conformal residual.
5. Confirm that nonconstant registered profiles activate the vector source and longitudinal
   correction, so the example is genuinely non-CMC and coupled.
6. Rederive the electric Weyl formula including the `-2Lambda/3` term and the vanishing magnetic
   curl. Determine whether `q=0` is zero initial tide and `q!=0` has nonzero invariant tide.
7. Audit the conditional statement about local flatness for `q=0`; reject any global-completion or
   uncaveated PDE-uniqueness claim.
8. Check whether `q` and `-q` are interchanged by the marked `y-z` axis relabelling.
9. Audit solution-space completeness only within the declared ansatz. Arbitrary `tau(x)`, `p`, `q`,
   and the auxiliary translation kernel must remain visible.
10. Reject promotion of the torus, constant conformal factor, diagonal TT tensor, profile, sign,
    scale, or member into a UDT premise or physical selection.
11. Verify no metric, reciprocal-kernel, angular-cancellation, observational, or premise change was
    smuggled in and no protected work was used.
12. Run all four registered `python3 -S` commands in a writable ephemeral copy.

## Allowed verdicts

- `G317_ACCEPTED__EXACT_NONCMC_INTERLOCK_AND_TIDE_SPLIT_UPHELD`
- `G317_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED`
- `G317_SCIENTIFIC_LANDING_REFUTED`
- `G317_REVIEW_INCOMPLETE`

Identify exact algebraic, geometric, completeness, scope, or provenance defects. Do not select or
canonize data, a history, topology, `Lambda`, scale, physical `X_max`, source, action, matter/mass
law, observation, population, or unique-universe bootstrap rule.
