# Post-review ownership correction

Date: 2026-08-10

The preregistered external fork landed at
`DEMOTE_TO_CONDITIONAL_ASSEMBLY_NOT_BRANCH_OWNED`. This correction preserves the preregistration,
source freezes, dispatch, and git history while updating the current package outputs.

Exactly one classification changed:

```text
R17 W01:
COMPLETE_NONISOMETRIC_TRANSITION_OWNED
  -> CONDITIONAL_QUERY_OR_PRESENTATION_TRANSITION_ONLY
```

The exact semidirect formula remains a conditional candidate. The corrected counts are zero
branch-owned complete transitions, five conditional-query/presentation/assembly rows, and all
other disposition counts unchanged. The R04 aggregate wording was corrected because R17 is no
longer an owned complete positive.

The production algebra remains 16/16. Independent controls are 15/15. Exercised catch proofs are
33/33, including rejection of R17 promotion and rejection of removal of its not-owned disclosure.
The corrected atlas SHA-256 is
`070206c8a6a9eaf87f5bc8c29199323400831ff6ac5471944090b9429872cc36`.
