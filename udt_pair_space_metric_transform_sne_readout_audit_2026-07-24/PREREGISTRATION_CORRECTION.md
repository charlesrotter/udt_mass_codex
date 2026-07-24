# Preregistration correction

Date: 2026-07-24

The first production attempt stopped at source-hash validation before writing
any generated result or ledger. The pinned hash for
`udt_two_observer_separation_selector_audit_2026-07-24/CANDIDATE_OUTCOMES.tsv`
contained a one-character transcription error at hex position 21:

- preregistered typo: `53aa300eb67e47c7ec50d6d8f1e44942be995e30d6f137ee2dac8a19bf2d18ff`
- literal SHA-256: `53aa300eb67e47c7ec50c6d8f1e44942be995e30d6f137ee2dac8a19bf2d18ff`

The file is unchanged. This correction changes no candidate, test, tolerance,
firewall, or maximum conclusion. It is committed before any successful
production or SNe replay.
