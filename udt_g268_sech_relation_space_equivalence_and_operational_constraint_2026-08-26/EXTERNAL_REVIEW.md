# G268 fresh external adversarial review

Date: 2026-08-26
Reviewer: external Codex `gpt-5.4`, high reasoning, ephemeral read-only intake
Sealed intake: `/tmp/udt_g268_review_1qapu2yv`
Scope SHA-256: `549d53d6e73c53fdddf92e3b0c8e3d6efd432d290a0194dac52ddc17235a9192`
Manifest SHA-256: `2abcf0c3ace564c57e9da2027aafefeaea9cb098d2431c183a27c782ac81df36`

## Disposition

```text
ACCEPT_WITH_REPAIRS
```

The reviewer accepted all eight scientific/type/scope questions. It found no algebraic, network,
premise-laundering, or widening defect in the bounded landing. It independently reran the package
and all three no-write components and performed separate symbolic spot checks.

Review question 9 failed on evidence quality:

1. The mutation script tested standalone bad statements rather than injecting mutated logic through
   a real verification path.
2. Several production “exact checks” were hardcoded booleans: finite-rank positivity, composition-
   denominator positivity, inverse positivity, zero relation rejection, and zero history rejection.

The reviewer required an evidence-only repair: exercise actual mutated functions through a common
validator, and mechanize the flagged algebraic checks or explicitly downgrade analytic/epistemic
conclusions from the symbolic-check count.

The scientific landing survives unchanged, subject to successful repair verification.

## Final response transcription

Intake-local links are omitted; finding-level wording is retained.

> **Findings**
>
> - Major: the preregistered mutation evidence is not genuine. The contract requires hostile catches
>   against the relevant failure modes in the verification path, but `run_catch_proofs.py` only
>   evaluates standalone tautologies like `1 != 0` and `True is not False`; it does not mutate or
>   probe the production or independent verifier. `verify_package.py` then treats that as proof of
>   `8/8` catches. Review question 9 therefore fails.
> - Moderate: several central “symbolic checks” are hardcoded booleans rather than mechanized proofs,
>   including nonvanishing rank, denominator positivity, inverse positivity on the target space,
>   zero existing-relation rejection, and zero history rejection. The algebraic landing still looks
>   right, but the package overstates how much of it is actually certified.
>
> I independently reran the registered no-write replay and the three component scripts. I found no
> blocking algebra/type/scope defect in the scientific landing itself, and bounded symbolic spot-
> checks supported the key formulas.
>
> **Disposition:** `ACCEPT_WITH_REPAIRS`
>
> Questions 1–8: yes. Question 9: no. The independent rational and no-write replays are genuine, but
> symbolic certification is partly hardcoded and the mutation harness is vacuous rather than a real
> adversarial catch test.
>
> Required repairs: make the mutation suite actually exercise mutated logic, and replace the
> hardcoded booleans with mechanized checks or explicitly downgrade those items from “exact symbolic
> checks.”
