# Preregistration source-manifest correction

Date: 2026-08-11

The first fail-closed source replay stopped before the observational fit because the registered
SHA-256 for
`udt_pair_instrument_mixing_solution_space_audit_2026-08-10/AUDIT_REPORT.md` omitted its final
hexadecimal character.

```text
registered: 38dd5e943c5c0e1e68a3ed52bbaee9d88c45fcb24d4acea73c0e9b8e871ac8e
actual:     38dd5e943c5c0e1e68a3ed52bbaee9d88c45fcb24d4acea73c0e9b8e871ac8e8
```

An independent read-only comparison found no other mismatch among the 19 manifest rows. This is a
clerical correction only: no source, premise, candidate, tolerance, outcome class, or scientific
formula changes. The initial preregistration commit preserves the error historically. The corrected
manifest is committed before the numerical replay resumes.
