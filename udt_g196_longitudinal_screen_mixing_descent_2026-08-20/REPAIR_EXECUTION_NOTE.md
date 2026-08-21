# G196 repair execution note

Date: 2026-08-21

Both preregistered repairs were implemented without changing the metric family, candidate formulas,
saved production result, saved independent numerical result, saved hostile-control result, census,
or tolerances.

R1 now separates the independently implemented Torch metric-jet/Riemann/connection/tide checks from
the formula-level direct-versus-ordered Jacobi IVP regression. The original preregistration remains
visible with a dated post-review correction.

R2 sets Python's in-process `tempfile.tempdir` from the already declared `TMPDIR` before Torch import
only when `G196_NO_WRITE=1`. It neither creates a temporary file nor affects normal evidence-producing
execution.

The full registered package replay was run with `TMPDIR`, `TMP`, and `TEMP` all pointing to an
existing mode-`0555` directory. It exited zero with:

- 17 exact production assertions;
- 204 numerical histories and 5,313 assertions;
- maximum tide error `8.881784197001252e-16`;
- maximum screen-connection error `2.220446049250313e-16`;
- maximum factorization error `1.5420713317393364e-11`;
- minimum sampled nonvertex determinant `1.7099989610881957e-4`;
- 9/9 hostile catches;
- fresh/sealed artifact identity and stale-artifact rejection;
- 8/8 source-manifest rows;
- zero entries created in the non-writable runtime directory.

This locally closes R1 and R2. Repair-only external confirmation remains pending. The bounded
scientific landing is unchanged.
