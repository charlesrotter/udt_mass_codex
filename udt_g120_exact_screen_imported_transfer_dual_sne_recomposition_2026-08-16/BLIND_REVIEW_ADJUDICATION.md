# G120 blind-review adjudication

Date: 2026-08-16

Reviewer: fresh read-only Codex subagent context

## First landing

`REPAIR_REQUIRED`

The reviewer independently reproduced the transfer algebra, both raw likelihood returns, and the
hostile `T=1` mismatch. It found no defect in the core conditional result. It required three
evidence/scope repairs: restrict the P1 areal-radius interpretation to outgoing `Z>=1`; replace a
vacuous slope assertion; and make exact package replay noncircular.

## Final landing

`REPAIRS_VERIFIED__CORE_CONDITIONAL_RESULT_STANDS`

All mandatory repairs and optional hardening are implemented. The reviewer reran the package,
confirmed every gate passed, verified that the temporary-copy replay preserved the live result
bytes, and found no leftover temporary directory.

## Accepted maximum conclusion

On the declared G119 central-spherical branch and outgoing catalog `Z>1` domain, importing
`eta=1,epsilon=1/Z` yields `T=1/Z`, `d_L=Z^2R`, and the conditional P1 radius curve. Pantheon+ and
DES frozen no-refit likelihoods are preserved. No native transfer/light theory, complete physical
history, terminal depth, Lambda-CDM relation, or `X_max` follows.
