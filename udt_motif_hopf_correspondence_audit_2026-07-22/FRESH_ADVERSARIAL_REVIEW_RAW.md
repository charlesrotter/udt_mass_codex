# Verdict: FAIL

The package’s `COMPLETE_VERIFIED_WITH_CAVEATS` grade and four “YES” evidence gates are not justified. This does not refute the underlying conditional toric/Hopf algebra; it fails the package’s verification claim.

## Blocking findings

1. **A preregistered covariance gate was never exercised.** The contract requires projector matching under coordinate transformations ([PREREGISTRATION.md](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/PREREGISTRATION.md:164)). Neither current verifier transforms the path projectors or their derivatives. Moreover, Frobenius and convergence thresholds use Euclidean component norms ([build_correspondence_atlas.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/build_correspondence_atlas.py:227)), which are chart-dependent. The Frobenius tensor formula itself is valid, but its numerical certification is only for the registered chart.

2. **The claimed independent toric verification is circular.** Production hard-codes the Hessian eigentuples and a standard Hopf map ([derive_toric_control.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/derive_toric_control.py:31)); the independent verifier hard-codes the same formulas rather than deriving them from the metric ([verify_correspondence_independent.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/verify_correspondence_independent.py:283)). The production script hashes `fs_hopfion.py` but never reads or compares its `hopf_seed` implementation. Therefore the report’s “exact independent toric” statement ([AUDIT_REPORT.md](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/AUDIT_REPORT.md:185)) is unsupported by its packaged verifier.

3. **The catch proofs are largely assertions about declared fields, not mutation tests.** Several independent catches are tautologies such as `len(ids[:-1]) != 64`; package catches directly throw an `AssertionError` rather than pass corrupted evidence through the validator ([verify_package.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/verify_package.py:84)). Thus “11/11” and “13/13 catches” overstates validator strength.

4. **Carrier/action accounting is internally contradictory.** The connection and quotient use a supplied equal-weight diagonal action, yet the result records `construction_used_carrier_or_action: false` ([derive_toric_control.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/derive_toric_control.py:90)). The package verifier enforces that false boolean while separately requiring the action-premise string. The report’s prose correctly calls the action supplied, but the machine catch does not audit import.

5. **“Coherent projector bundles” exceeds the sampled evidence.** Stability means equal motif at 17 nodes with matchable labels; it has no continuity-distance gate ([build_correspondence_atlas.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/build_correspondence_atlas.py:418)). Among paths labelled stable, 70 have maximum adjacent component distance above `0.5`, 33 above `1`, and the maximum is `6.57`. A 257-node replay of the worst path retained its motif, so this is not a found counterexample, but the evidence supports sampled continuation—not a continuous bundle theorem or independently verified endpoint transport.

## Checks that did pass

- Both requested verifiers completed and reproduced their banked `PASS_WITH_CAVEATS` outputs byte-for-byte. They were run in a temporary mirror because they write result files; I made no worktree edits.
- All declared frozen manifests and their contents passed SHA-256 checks, including the transitively pinned amplitude-volume and joint-invariant sources.
- All path, summary, and distribution primary keys are unique. Threshold labels match their stored values.
- The Frobenius projector formula has the correct tensor index structure. Nonintegrable rows are well separated in the registered chart: minimum `9.73e-4` versus the `1e-5` gate. Integrable maximum is `5.16e-8`; one row remains uncertain.
- The `8,370` four-line rows are six distinct rank-two planes per midpoint, not duplicate keys. However, the `1+1+2` atlas semantically repeats its primitive rank-two plane as one complementary-split side—8,205 extra diagnostic rows. The report’s headline `6,669/1,536` uses only primitive rows, so it is not inflated by this.
- Open paths are correctly marked `NOT_TESTED_BY_OPEN_PATH`; no holonomy is claimed.
- No local-to-global Hopf promotion occurs. Periodicity, action, caps, orientation, and normalization remain explicit supplied premises.
- No seed-to-relaxed-field identity is claimed ([AUDIT_REPORT.md](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/AUDIT_REPORT.md:161)).

## Independent toric/seed result

I independently derived the Christoffels and mixed Hessian from the stated metric. They reproduce

\[
H^\mu{}_\nu=
\operatorname{diag}\!\left(
0,-A'/A^3,\frac{\Omega'/\Omega-1}{A^2},
\frac{\Omega'/\Omega+1}{A^2}
\right),
\]

the angular gap \(2/A^2\), and the \(\Omega\)-independent connection after supplying \(K=\partial_{\xi_1}+\partial_{\xi_2}\). A direct 1,000-point comparison with the checked-in inverse-stereographic [`hopf_seed`](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/hopfion_arc_scripts_2026-07-05/fs_hopfion.py:19) agreed to \(1.1\times10^{-14}\).

Thus the exact seed-level identity is true, but it is a template/action-conditioned compatibility witness, not a metric selection or carrier derivation.

## Strongest honest maximum conclusion

`OBSERVED_BOUNDED_FIXED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS`

plus

`EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS`.

The overall motif-to-Hopf correspondence remains a `LEAD`: global continuation, toric-stratum selection, circle action, orientation, caps, deformable carrier space, action, relaxed field, dynamics, stability, source, mass, and matter emergence remain open.