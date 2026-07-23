# Preregistration correction

Date: 2026-07-23

The preregistered source universe incorrectly named:

```text
native_hopfion_topology_audit_2026-07-19/STATUS_LEDGER.tsv
```

The tracked load-bearing file is:

```text
native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv
```

This correction was discovered by an existence check before any authorized
navigation file or synthesis output was mutated.

`PREREGISTERED_SOURCE_UNIVERSE.tsv` remains unchanged as historical evidence.
`CORRECTED_SOURCE_UNIVERSE.tsv` is the controlling source list. Its only
change is the S21 path substitution above; the 25 identities and roles are
otherwise unchanged.
