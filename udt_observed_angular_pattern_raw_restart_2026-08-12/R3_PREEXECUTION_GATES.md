# R3 pre-execution gates

Date: 2026-08-13
Status: `PASS__ONE_REAL_SELECTION_STRUCTURAL_SMOKE__NO_COVARIANCE_OUTCOME_REVIEWED`

This note records the last operational gate before the preregistered 194-selection R3 covariance
run. It does not amend the scientific scope, block geometry, estimator, rank threshold, tolerances,
anchors, or maximum conclusion in `R3_PREREGISTRATION.md`.

## Frozen production state

- branch/commit at smoke launch: `grok` / `1e107500`;
- local and `origin/grok` divergence immediately before launch: `0 0`;
- production program: `run_r3_covariance_atlas.py` as committed at `1e107500`;
- engine: TreeCorr `5.1.3`, eight CPU threads, float64 arrays, no GPU;
- memory stop: 16 GiB;
- restart unit: one complete selection cell.

## Real-catalog structural smoke

The smoke called the unchanged production `execute_selection` function on the first catalog-ordered
selection, `CMASS_North_f1_g00`. It used the exact registered 20x deterministic random subset and
all four weight lanes. The helper and its output were confined to
`/tmp/udt_r3_real_smoke_PyupS1/`; they are operational evidence, not R3 scientific outputs.

Exact launch:

```bash
MPLCONFIGDIR=/tmp/udt_mpl \
PYTHONPATH=/tmp/udt_corrfunc_r2:/tmp/udt_treecorr_r2:/home/udt-admin/udt_mass_codex/udt_observed_angular_pattern_raw_restart_2026-08-12 \
python3 /tmp/udt_r3_real_smoke_PyupS1/run_one.py
```

Structural return:

- process exit: 0;
- selected galaxies: 8,228;
- selected randoms: 164,560;
- all nine central component comparison records completed;
- all twelve lane/resolution covariance records completed;
- central curve shape: `(4,119)`;
- covariance shapes: `(4,119,119)` at NSIDE 4, 8, and 16;
- eigenspectrum shapes: `(4,119)` at NSIDE 4, 8, and 16;
- all required stored arrays finite;
- wall time: 78.928 seconds;
- peak RSS: 3.143 GiB;
- checkpoint size: 1,786,263 bytes.

TreeCorr warned that some full-footprint NSIDE=16 labels contained no objects in this narrow shell.
This is expected: the registered code retains only blocks occupied by the shell's selected random
catalog and requires every selected galaxy to lie in that active support.

## Outcome-blindness statement

The helper asserted execution, central-engine agreement, record counts, finiteness, and array shapes.
No covariance entry, diagonal, eigenvalue, rank, scale, shell comparison, angular feature, or physical
interpretation was printed or reviewed. The smoke therefore does not supply an R3 outcome and cannot
be used to retune the frozen design.

## Launch decision

The structural and resource gates pass with headroom under the frozen 16 GiB stop. The full
preregistered run may proceed unchanged. Elapsed time remains operational only and is not a
scientific stop condition.
