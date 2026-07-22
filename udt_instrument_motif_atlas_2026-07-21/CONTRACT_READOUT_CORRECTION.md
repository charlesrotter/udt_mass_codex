# Contract Readout Correction

Date: 2026-07-21

Status: `PREREGISTERED_BEFORE_CORRECTED_CONTRACT_REPLAY`

The first run of `verify_package_contract.py` failed at `line-plus-three shapes`. The saved canonical
family strings are:

- `1;3` with `N0_P1_Z0;N1_P2_Z0`;
- `1;3` with `N0_P3_Z0;N1_P0_Z0`.

The contract expected the second **unordered** signature set in the opposite text order,
`N1_P0_Z0;N0_P3_Z0`. The building-block ledger used the same line-first prose ordering. The raw
primitive blocks and scientific census are correct; the combined census strings sort ranks and
signatures canonically and must not be read as ordered rank-to-signature pairs.

Correction contract:

1. preserve all scientific artifacts unchanged;
2. make the verifier expect the exact saved canonical strings;
3. render `BUILDING_BLOCK_LEDGER.tsv` signature alternatives as explicit unordered sets so no
   rank/signature positional pairing is implied;
4. rerun the contract and retain this correction layer.
