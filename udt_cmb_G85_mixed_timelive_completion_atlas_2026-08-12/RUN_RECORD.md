# G85 run record

## Environment

```text
CPU-only analytic/bounded verification
Python 3.10.12
SymPy 1.13.1
NumPy 2.2.6
pytest 9.1.1
```

No GPU process or long-running solve was launched.

## Commands

```text
python3 udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/derive_completion_atlas.py
python3 udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/verify_independent.py
python3 udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/run_catch_proofs.py
python3 udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/verify_package.py
python3 udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/verify_repository_gates.py
```

Every command exited `0`. The JSON artifacts are the raw deterministic stdout payloads. Their
SHA-256 identities are:

```text
1eb2ba55d54005f909a093dcacdf1e16509b096d3a0b52e5f843a2bac8043ffd  DERIVATION_RESULT.json
6b6fb6923871b63183b7abbd4e3cbf8d677b0295ac74f898da1f8ed73627b298  INDEPENDENT_VERIFICATION.json
9c8dd2fb7429a2a9c8b667154a4f527bf8c35c44f28760fd52a03cbfd4077275  CATCH_PROOF_RESULT.json
71a95b03b3b45242fe1687623126ba8b6b00d92a7551e8683116fb16d1075d09  PACKAGE_VERIFICATION.json
94c94dcf88da0742b71dea6a9224a46fe597cedaabe32bd31fffb11b2859b445  REPOSITORY_GATES.json
```

The production atlas SHA-256 is
`459c74c6e6775d27ac727540e691dc62588054b60b77340c53a96eee6775d3b7`.

## Bounds

The numerical witness uses a `17 x 33` time/radial gate grid (`561` checks) only to support the
symbolic signature proof. It is not a continuum search, fit, or physical simulation. The analytic
gate inequalities and smooth bump construction own the existence claim.
