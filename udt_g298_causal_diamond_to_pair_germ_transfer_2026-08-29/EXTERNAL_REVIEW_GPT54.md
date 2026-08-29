# G298 fresh external adversarial review — gpt-5.4

Date: 2026-08-29

## Verdict

The core algebra survives. The reviewer independently reproduced the comparison-clock typing,
both Gram matrices, W1 recovery, and the active-screen rank-three separator. It found no
higher-severity algebra defect.

The original landing required an exact type repair. The evidence proves two natural,
gauge-inequivalent regular **projections** from one richer complete path-labelled relation state;
it does not prove that both projected pair one-jets are equally complete. In particular, `J_L`
forgets the transported source ruler and its path carry.

The maximum supported landing is therefore:

```text
MULTIPLE_INEQUIVALENT_NATURAL_PAIR_ONE_JET_PROJECTIONS_SURVIVE_FROM_THE_DERIVED_COMPLETE_RELATION_STATE
__NO_UNIQUE_TRANSFER_TO_G2_IS_OWNED
```

Grade: `INTERNALLY_DERIVED_WITH_CAVEATS` pending repair-only verification.

## Independent derivation retained

For one supplied regular future-null leg, let

```text
r = omega_X / omega_Y > 0
```

and decompose the target clock in the transported source frame as

```text
U_Y = Gamma U_X_tilde + a n_X_tilde + W,
a = Gamma - 1/r,
Gamma = (r + 1/r + r ||W||^2)/2.
```

Then the transported-source projection

```text
J_T = (r U_Y, n_X_tilde)
```

has pair Gram matrix `[-r^2, r a; r a, 1]` and determinant
`-r^2(1+a^2)`. The target-local projection

```text
J_L = (r U_Y, n_Y)
```

has pair Gram matrix `diag(-r^2,1)`. W1 returns `Phi=-log(r)` on both.

When `W=w e_2`, the determinant of `(r U_Y,n_X_tilde,n_Y)` is `-r^2 w`. It is nonzero for active
screen carry, so the image planes are gauge-inequivalent.

## Required repairs and disposition

1. Replace every unqualified claim that `J_L` is an equally complete physical pair germ with the
   exact natural-projection statement. **Applied.**
2. Make the landing explicitly concern non-unique projections from the richer relation state.
   **Applied.**
3. Describe the independent verifier as an algebraic projection witness only; it cannot certify
   semantic completeness or physical ownership. **Applied.**
4. Remove two vacuous self-equality assertions noted in the production and independent scripts.
   They were replaced with computed target-local Gram-matrix checks. **Applied.**

## Boundary

The review does not select a physical projection, higher pair surface, route population, metric
history, scale, observation, or `X_max`. A repair-only follow-up must verify the registered repairs
before the result is banked or promoted to the startup surface.
