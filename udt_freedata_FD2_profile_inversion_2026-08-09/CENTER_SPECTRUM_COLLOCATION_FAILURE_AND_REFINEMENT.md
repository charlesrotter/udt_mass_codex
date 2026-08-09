# Center-spectrum Phase-I collocation failure and preregistered refinement

Date: 2026-08-09  
Timing: shooting/collocation result inspected; refinement frozen before rerun

The blind center-spectrum run found all 84 positive shooting roots. The exact flat Bessel controls,
shooting wall residual (`2.07e-11` maximum), and shooting/collocation frequency agreement
(`6.66e-9` maximum relative difference) pass. The run nevertheless fails the preregistered
independent-method gate:

- seven `m=+/-1` collocation solves exhausted the 30,000-node cap;
- maximum collocation wall residual is `8.14e-8`, above the frozen `1e-8` line;
- no observational value was loaded.

The `m=+/-1` collocation scaling used `R(Y0)=1` even though the regular Frobenius branch is
`R~r^|m|`; at `r0~1e-7` this inflates the outer solution by about `1e7`. Freeze the correction:

1. use physical Frobenius normalization `R0=r0^|m|`, `F0=|m| p0 r0^(|m|-1)` in shooting and
   collocation;
2. set collocation `tol=1e-9`, `max_nodes=100000`;
3. retain the original shooting tolerances and every frozen pass threshold;
4. rerun all 84 roots—no selective rerun and no failed row removed;
5. preserve the first return at
   `center_spectrum_phase1_failed_collocation.json`, SHA-256
   `99da4d4383d39b421a3802c878f05d416dfbcb2ebb31a6d00fe8c871746eebe0`.

If any collocation status or wall-residual gate still fails, the correction remains
`NUMERICALLY_OPEN` and the observational phase stays sealed.
