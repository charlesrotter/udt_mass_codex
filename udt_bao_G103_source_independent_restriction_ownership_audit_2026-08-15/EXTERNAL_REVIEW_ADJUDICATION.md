# G103 external-review adjudication

Date: 2026-08-15

The external verdict `PASS_WITH_CAVEATS` is accepted. It found no algebraic, typing, source-scope,
outcome-blindness, or conclusion-ceiling blocker.

## Post-review reproducibility repair

The reviewer could not directly rerun the four scripts in a read-only seal because each script
attempted to refresh its saved JSON after completing the calculation. It therefore used a
non-writing shadow harness and reproduced every result. After the review, an output-neutral
`UDT_READ_ONLY_REPLAY=1` switch was added to those four scripts. It changes no calculation, fixture,
gate, or stored result; it suppresses only the final file write. Both normal and read-only modes are
regression-tested before banking.

## Accepted scientific ceiling

The current complete-history identities are locally permissive when the observer-query realization
and source pair measure remain supplied. They enforce legal sky/network/measure assembly but do not
select a nontrivial BAO-like pattern in the frozen regular local/first-jet source universe. This is
not a global no-go. Criticality, topology, bootstrap, source-history coupling, and the physical
history/query law remain `OPEN`.

No BOSS curve, covariance, descriptor, singular vector, or feature was read.
