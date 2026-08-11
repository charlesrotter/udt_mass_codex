# Complete CMB observation-query map — audit report

## Verdict

`VERIFIED-AFTER-SPECIFIED-CORRECTIONS`.

The actual CMB query has now been separated into fourteen typed layers across all eighteen frozen
geometry families. No registered family owns a complete physical CMB realization. This is a clean
ownership result, not a negative result about UDT and not a claim that no realization exists.

## What was learned

The old CMB comb calculation is one middle layer: conditional scalar mode locations followed by a
two-parameter attributed comparison with TT peak positions. A physical peak is not just an
eigenvalue. It additionally needs a metric-derived observer-sky angular map and a rule saying which
modes carry nonzero power. Exact finite countermodels show that one fixed spectrum supports
different peak sets—or zero power—under different covariances.

The complete angular orchestra remains live. The C1/general-screen work proves that angular
mixing is richer than the old equatorial ladders. But angular richness alone does not select a
physical screen, relation realization, source covariance, or population.

## Census

- frozen sources: `16/16`, SHA-256 exact;
- registered families: `18/18`, exactly `F00`--`F17`, no duplicates;
- query layers: `14`;
- observable classes: `4`;
- complete physical CMB query realizations owned: `0`;
- ranked families: `0`;
- TT-power predictions: `0`;
- polarization predictions: `0`;
- historical attributed position-diagnostic families: exactly `F00`;
- banked controls retained: `10,080` C0 scalar roots and `15,420` C1 matrix elements.

The artifact-consistency verifier passes `21/21`; all `10/10` preregistered validator mutations
are caught. These local checks are not presented as independent semantic evidence. The exact
spectrum-versus-power countermodel passes `6/6`.

## Observer/local guard

This audit concerns inter-observational-frame relations. `c_E` remains the local clock/ruler
calibration. `c_eff^(pair)` remains a conditional terminal pair-cone readout and is not local signal
speed. Co-presence is not signalling. `X_max` is the working observer-pair asymptote only.

## Four evidence gates

1. **Preregistered:** yes, commit `09056c83`, before result tables or scripts.
2. **Full or bounded:** full over the exact frozen `F00`--`F17` family universe and sixteen-source
   semantic scope; it is not a census of every conceivable UDT completion.
3. **Independent:** yes at the semantic gate: the sealed `gpt-5.4` reviewer directly inspected the
   sixteen frozen sources, reproduced all counts, found no omitted physical CMB query or response
   law, and returned `VERIFIED_AFTER_SPECIFIED_CORRECTIONS`. Locally, a separate standard-library
   implementation checks artifact consistency without importing the renderer; it does not derive
   semantic ownership from prose. The ten mutations test that validator and are not a second
   independent proof.
4. **Premises:** audited in `PREMISE_LEDGER.tsv`; no conditional screen, operator, boundary,
   profile, population, `X_max`, or observer-query choice is promoted.

## Next gate

Construct the same explicit observer-sky query and its screen Jacobi map on the round F01 and
axis-regular mixing-on F02 controls before any eigensolve or fit. This should reveal whether the
two historical affine projection freedoms are replaced by complete geometry or remain genuinely
query/source owned.

Do not restart FD2, fit peaks, select F01/F02, activate bootstrap, infer local propagation, add
source weights, run polarization, or claim a CMB prediction from this map.

## External-review adjudication

The reviewer accepted the type split, the `F00`--`F17` ownership census, the spectrum-versus-power
no-go, the scalar/polarization distinction, and the proposed F01/F02 pre-eigensolve control. Its
three evidence-label corrections are incorporated without changing any scientific table:

- `derive_cmb_query_map.py` is identified as a deterministic renderer;
- `verify_cmb_query_map_artifact_consistency.py` is identified as an artifact-consistency checker;
- `run_catch_proofs.py` is identified as a mutation harness for that checker.

The raw verdict is preserved in `EXTERNAL_REVIEW_RAW.md`; the preregistered correction boundary is
preserved in `EXTERNAL_REVIEW_CORRECTION_PREREGISTRATION.md`.
