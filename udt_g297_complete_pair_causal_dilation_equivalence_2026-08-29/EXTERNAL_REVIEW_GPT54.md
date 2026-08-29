# G297 fresh external adversarial review — gpt-5.4

Date: 2026-08-29

## Verdict

The bounded landing survives:

```text
OWNER_CLARIFICATION_IS_SUBSTANTIVE_BUT_THE_TWO_LEG_COMPLETE_TRANSFER_REMAINS_UNDERDEFINED
__NO_UNIQUE_NONIDENTITY_FORM_YET
```

The reviewer reproduced 125 production checks, 20,000 independent cases / 50,002 assertions as
sealed, the no-write replay, and five hostile catches from a writable ephemeral copy. It found no
reason to weaken the scientific landing, but required three repairs before evidentiary closure.

## Findings and required repairs

### High — implementation-independence wording

The sealed independent verifier read `DERIVATION_RESULT.json` to check the production result
envelope. The claims “no production import” and “neither production code nor production outputs”
were therefore too strong.

Required repair: either remove the production-result read or weaken the independence language.

Disposition: **repaired by removing the production-result read**. The independent verifier now
performs 20,000 cases and 50,000 assertions without reading production code or production output.

### Medium — B-centered derivation not generally written

The general two-leg formula was written explicitly only for the A-centered construction. The
B-centered formula was explicit only in the moving-flat control, while the status ledger claimed a
general conditional derivation.

Required repair: add the general B-emission/B-return derivation or weaken the status.

Disposition: **repaired by adding the general observer-reversed construction** from `b_-(a)` and
`b_+(a)`, including its two physical null-arrow slopes and conditional scope.

### Medium — sealed replay command contract

The registered commands were written as direct invocations, but result writers cannot write into a
sealed read-only intake. A package-only ephemeral copy also requires `G297_SOURCE_ROOT` to point to
the intake containing the source-manifest paths.

Required repair: document the writable-copy/source-root prerequisites or self-stage them.

Disposition: **repaired in `COMMANDS.md` and `run_catch_proofs.py`**. The command contract now copies
the entire intake to a writable ephemeral directory and sets `G297_SOURCE_ROOT`; both the package
verifier and hostile-catch runner honor the inherited root.

## Answers to the registered questions

1. The A-centered derivation was general. The sealed B-centered evidence was correct in flat and
   static controls but had not been independently and generally written out.
2. The static-lapse and active-screen controls refute only the naive scalar collapse. They do not
   select or reject a metric history.
3. The map
   `C_g: D_g/G_D -> G_2(g)/G_F`
   is correctly identified as still underdefined.
4. The repaired package does not define W6 co-presence by radar midpoint and does not introduce
   instantaneous-signalling language.
5. The algebraic scope was bounded correctly, apart from the independence overclaim.
6. No surviving overclaim was found on complete-history selection, general tidal reconstruction,
   branch population, or gauge descent.
7. Frozen candidate landing 2 follows after the three bounded repairs; no further weakening is
   needed.

## Review boundary

The reviewer inspected only the authorized sealed intake, used a writable ephemeral copy for the
registered checks, did not edit repository evidence, and did not continue the research.
