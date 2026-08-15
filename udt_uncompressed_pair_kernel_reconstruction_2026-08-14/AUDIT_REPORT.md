# UDT uncompressed complete-pair evaluator reconstruction

Date: 2026-08-14  
Current grade: `VERIFIED-WITH-CAVEATS__FRESH_EXTERNAL_SEMANTIC_REVIEW_PASSED`

## Primary result

The preregistered landing is

```text
FULL_UNCOMPRESSED_TERMINAL_EVALUATOR_DERIVED
__NO_SCALAR_MU_OWNED
__PHYSICAL_PAIR_AND_HISTORY_OPEN
```

For a supplied complete coframe

```text
E=[[B,0],[Q S,Q]]
```

and supplied rank-two pair realization

```text
J=[Y;Z],
```

the exact pair metric is

```text
h
 = Y^T B^T eta_2 B Y
   +(S Y+Z)^T Q^T Q(S Y+Z).
```

On the regular calibrated Lorentzian pair stratum,

```text
phi_pair = (1/4)log[(-det h)/h00^2],

c_eff^(pair)/c_E
 = exp(-2phi_pair)
 = (-h00)/sqrt(-det h).
```

Thus the reciprocal/base, screen, four-component mixing, and pair-embedding data are combined into
one pair metric before the terminal endpoint ratio is read. The user's “orchestra inside the pair”
framing is correct in this conditional evaluator sense.

## What was corrected

The previous package compressed the angular/mixing/embedding contribution to

```text
P=(S+ZY^-1)^T Q^TQ(S+ZY^-1)
```

before studying a fixed-`P` reciprocal response.

That compression is exact and sufficient for the zero-order A-calibrated pair metric. It does not,
however, retain:

- screen-frame representatives;
- ambient mixing `S` separately from pair embedding `ZY^-1`;
- rotating screen motion invisible to `(P,dot P)`;
- a physical history for `P`;
- a unique scalar mixing variable.

The earlier strict intermediate trace minimum therefore remains a lawful **conditional diagnostic at
fixed compressed data**, but it is not a derived physical quiet-middle regime or regime score.

## Time-live result

The full exact derivative retains

```text
dot B, dot Q, dot S, dot Y, dot Z
```

separately. An exact generic rational witness and independent black-box replay show every one of
those blocks can change `phi_pair`.

At the pure-base point `Q=I,S=0,Y=I,Z=0`, the first derivatives of screen/mixing channels vanish
because the Gram term begins quadratically. This prevents the project from mistaking local
first-order silence for a derived middle-regime suppression law.

The live identity is still kinematic. It does not provide the five histories.

## `mu` result

Modern complete-coframe mixing is `S in Mat(2,R)`. The July `mu_old` is a scalar modulus of a
different conditional mixed-base ansatz. No source-owned map identifies them.

The complete pair Gram data admit many inequivalent invariant scalar summaries, including `tr(P)`
and `sqrt(det P)`. No current premise selects one. The correct status is

```text
NO_SCALAR_MU_OWNED
```

within this algebraic evaluator—not “mu was set to zero,” and not “mu has been derived.”

## Verification

- preregistration committed and pushed at `ad9a8090` before outcome inspection;
- all exact symbolic production checks pass;
- standalone stdlib `Fraction` replay imports neither SymPy nor production code and passes;
- shrinking-step live checks converge;
- all five generic black-box sensitivities are nonzero;
- omitted-`dQ`, omitted-`dS`, omitted-`dY`, omitted-`dZ`, and flipped-`dB` mutations are caught;
- source SHA-256 entries match.
- repository regression suite: `90 passed, 1 xfailed`; the xfail is the registered matter-lane
  `test_no_habit_pins` gate and is unrelated to this evaluator.

A fresh sealed external `gpt-5.4` adversary verified the exact 28-file scope and independently
reproduced the pullback, a regular singular-`Y` witness, all five live sensitivities, the terminal
ratio identity, the compression fibers, and the `mu` type result. It returned
`VERIFIED_WITH_CAVEATS` with no blocking defect. See `EXTERNAL_ADVERSARIAL_REVIEW.md` and
`EXTERNAL_REVIEW_ADJUDICATION.md`. The result remains non-canonical because its physical ownership
limits remain open, not because an evidence gate is pending.

## Maximum justified conclusion

UDT now has a no-shortcut conditional evaluator for one supplied complete metric and one supplied
observer-pair realization. It confirms that the full orchestra is internal to the pair readout and
that `c_eff/c_E` is the terminal ratio of the completed pair metric. It does not yet derive the
physical pair realization, its time/regime history, a scalar `mu`, `X_max`, an action, a source, or a
bootstrap law.

## Next bounded scientific question

After the passed adversarial review, the next question should be preregistered from the uncompressed
identities:

> Does the metric and the founding ordered-comparison semantics supply any nonidentity compatibility
> law relating the live blocks `B,Q,S,Y,Z` across overlapping observer pairs, beyond the kinematic
> pullback and composition identities?

That question seeks the missing score without assuming one, fitting observations, or reviving a
compressed fixed-`P` regime template.
