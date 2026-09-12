# Source-first finite numerical support

The frozen eight cases and tighter worst-case repeat all passed. The distinct
original-connection integrator uses the full diagonal metric and complete
first-derivative arrays to construct Christoffels, then evolves all spatial
positions/slopes and log(k^t). The scalar rapidity implementation independently
assembles the admitted Bessel/constraint expressions. Neither imports new
parent code. Shared source mathematics and SciPy remain shared dependencies.

Across eight cases and129 saved evaluation points per case, maximum relative
frequency disagreement was2.05089056848351e-09, scaled xi disagreement
6.658218014696276e-11, original null residual4.1063056050023684e-09, and
absolute Killing-momentum error2.0269985689935766e-10. The worst frequency
case was the invariant pure-y equatorial ray, and its tighter original-
connection rerun reduced discrepancy to2.1608048683674497e-11. The frozen
thresholds all passed without repairs or changed cases/tolerances.

The captured baseline run exited0 in2.2136349849170074seconds, peak child
RSS78676KiB, under180seconds/2048MiB and one library thread. The independent
connection and reduced implementations both use float64/SciPy; this is finite
floating support, not interval certification or a proof at infinity.

Both actual hostile runs exited1 under the unchanged baseline assertion
`original metric frequency vs reduced rapidity`. Suppressing the complete
lambda response in the original metric produced relative discrepancy
18.56080902598741; inverting its frequency produced0.6527979120269158.
Their stdout, stderr, exact command/capture records and rejecting tracebacks
are retained. The variants exercise actual metric/readout defects; they do
not establish that all possible implementation errors are caught.

Controls cover zero amplitude, both longitudinal signs, each transverse
axis, a mixed tilt, negative amplitude, epsilon1.2, a small but finite tilt,
and two invariant transverse examples. These samples do not cover every
direction/amplitude or test the asymptotic claims numerically. The argument
in SOURCE_FIRST_RECONSTRUCTION.md owns those conditional analytic claims.
No new beam/Jacobi, cut/conjugacy, finite-wavefront, physical-light,
fixed-apparatus, general-equatorial or repeated-late-emission result follows.

Exact output rows live in source_original_geodesics.stdout. The initial
analytic/check seal precedes these outcomes. Parent candidate/code/output
had still not been opened at completion of these runs. Source-first-stage
elapsed allocation was conservatively21:00UTC through the second seal; the
same context remains allocated for direct attack and final fidelity by
21:40UTC. Runtime model/version remains UNATTESTED.
