# R1G readout-provenance correction report

## Corrected ruling

Direct inspection confirms the preregistered expectation. A downstream
Einstein-tensor or Misner–Sharp comparison does not feed the tested native
functional, variation, EOM, coupling, or solver in the reaudited files.
Therefore it remains a disclosed comparison readout rather than `MIXED`
operator provenance.

The corrected B02/B03 totals are 29 `NATIVE_2026-07-01`, two `MIXED`, and one
`OPEN`. The corrected affected-cascade total is 121
`NATIVE_2026-07-01`, zero `MIXED`. All lifecycle and migration-safety rulings
remain unchanged.

## Direct dataflow audit

| File/scope | Tested operator path | Standard-theory or imported role | Ruling |
|---|---|---|---|
| `cascade_bv16_cas.py` | Y1–Y2 derive native L/EL/H before Y3 | Einstein/MS downstream only | `NATIVE_2026-07-01`; `REFERENCE_ONLY` |
| `cascade_bv16_rungs.py` | native shoot, L, H complete first | epsilon/MS diagnostic after solve | `NATIVE_2026-07-01`; `REFERENCE_ONLY` |
| `cascade_or_energy_cas.py` | C4–C9 derive native L/EL/H | C10–C14 Einstein/MS comparison | `NATIVE_2026-07-01`; `REFERENCE_ONLY` |
| `cascade_or_energy_numeric.py` | native IVP and L/H quadrature | MS/epsilon comparison after solve | `NATIVE_2026-07-01`; `REFERENCE_ONLY` |
| `cascade_or_energy_rung1_and_alignment.py` | native rung solver and banked L | MS/epsilon sign-alignment readout | `NATIVE_2026-07-01`; `REFERENCE_ONLY` |
| `verify_universe_bv2_f_einstein.py` | explicit native phi/rho EOM substitutions | G and MS are audited outputs | `NATIVE_2026-07-01`; `REFERENCE_ONLY` |
| `phi_source_derivation.py` | `exp(alpha*phi)` multiplies `Grr` in L2 and is varied | alpha=-2 imported physical-metric coupling; other nonzero alpha free | `MIXED`; enters action/EOM |
| `homog_alpha_test.py` | augmented EOM contains `alpha*exp(alpha*phi)*rho^2` | same imported/free coupling family | `MIXED`; enters tested EOM |

The exact, machine-readable dependencies are in
[READOUT_PROVENANCE_CORRECTION_AUDIT.tsv](READOUT_PROVENANCE_CORRECTION_AUDIT.tsv).

## C12 family

The complete five-file `C12_ENERGY_ORIENTATION` family uses the July 1 native
round-static action/EOM or their native solver outputs. Einstein/MS quantities
are calculated afterward to compare energy readings; none is an input to the
action, variation, EOM, coupling, potential, initial-value solve, or Hamiltonian.
Every C12 row therefore records:

- `operator_provenance=NATIVE_2026-07-01`;
- `imported_action_or_coupling=NONE`;
- `comparison_readout=GR_EINSTEIN_TENSOR;MISNER_SHARP`;
- `role=REFERENCE_ONLY`.

This does not promote the Einstein reading to native UDT physics. It preserves
the non-native readout disclosure while keeping the operator-provenance axis
about the operator actually tested.

## Exercised guards

The independent verifier actively corrupts the records and confirms rejection
when a reference-only readout demotes native provenance, when its disclosure is
deleted, or when a load-bearing imported alpha coupling is mislabeled
reference-only. The five prior coverage/provenance guards also remain active.

No research artifact or current registry was edited, and no move or integration
is authorized.
