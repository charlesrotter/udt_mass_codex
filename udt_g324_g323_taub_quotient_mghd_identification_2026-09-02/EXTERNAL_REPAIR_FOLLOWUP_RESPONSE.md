# G324 External Repair Follow-Up Response

Date: 2026-09-02

No concrete incomplete repair was found within R1-R3. Within the sealed scope, the repaired package now closes the previously identified theorem-interface gap, the replay commands work literally in clean writable copies, and the bounded scientific landing remains unchanged.

## Intake Authentication

- I authenticated the sealed intake chain under `/intake` by checking that [REVIEW_MANIFEST.sha256](/intake/REVIEW_MANIFEST.sha256:1) matches the SHA-256 of [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:1), then verifying every manifest-listed payload hash. All 46 manifest entries verified successfully.
- This includes the authenticated payload [GLS_PRIMARY_SOURCE_EVIDENCE.json](/intake/package/GLS_PRIMARY_SOURCE_EVIDENCE.json:1), which records `arXiv 1704.00353v4`, related DOI, PDF SHA-256 `069c6f4bcb1c1569ec8546f8579250c6128f1f3fa893516bb3a147a1570cf92a`, theorem label `Theorem 2`, location on PDF pages 1-2, the two bounded fragments, and the formal theorem transcription at [lines 9-23](/intake/package/GLS_PRIMARY_SOURCE_EVIDENCE.json:9).
- The underlying GLS PDF bytes are not present anywhere in `/intake`, and the review instructions forbid outside retrieval. Accordingly, I authenticated the sealed evidence record and its field values as part of the sealed intake, but I did not recompute the PDF hash against the original PDF file.

## R1

- The repaired source-evidence record is materially different from the unresolved version. [GLS_PRIMARY_SOURCE_EVIDENCE.json](/intake/package/GLS_PRIMARY_SOURCE_EVIDENCE.json:20) now records the exact hypotheses fragment, [line 21](/intake/package/GLS_PRIMARY_SOURCE_EVIDENCE.json:21) records the endpoint fragment, [line 22](/intake/package/GLS_PRIMARY_SOURCE_EVIDENCE.json:22) gives the formal transcription, and [line 23](/intake/package/GLS_PRIMARY_SOURCE_EVIDENCE.json:23) states the orientation-neutral use in G324.
- The repaired proof in [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:142) uses that interface exactly. It first proves future timelike geodesic completeness at [lines 122-124](/intake/package/EXACT_DERIVATION.md:122), then assumes a proper time-oriented `C2` extension and invokes the imported theorem only to obtain a boundary-ending timelike geodesic at [lines 154-156](/intake/package/EXACT_DERIVATION.md:154).
- The earlier unauthenticated time-dual step is gone. The repaired proof explicitly says at [lines 156-158](/intake/package/EXACT_DERIVATION.md:156) that, after orienting the theorem-supplied geodesic toward its endpoint, future completeness rules out the future-directed case, so the endpoint geodesic must be past-directed. It also explicitly says no separate time-dual theorem or one-sided boundary assertion is used.
- The remaining localization step is then internal to G324: finite positive `R` endpoints are excluded in section 4 at [lines 133-140](/intake/package/EXACT_DERIVATION.md:133), so the only remaining endpoint direction is `R -> 0` at [lines 160-169](/intake/package/EXACT_DERIVATION.md:160), where the already-derived Kretschmann blow-up yields the `C2` contradiction.
- The premise ledger now declares the same theorem interface the proof consumes. [PREMISE_LEDGER.tsv](/intake/package/PREMISE_LEDGER.tsv:15) records GLS Theorem 2 as an imported mathematical method giving an orientation-neutral timelike endpoint in any `C0` extension, with G324 future completeness forcing the endpoint past-directed. That matches the repaired proof and no longer understates the import.

Conclusion on R1: accepted. Within the sealed scope, the repaired theorem interface is sufficient for the proof and no unauthenticated past-boundary or time-dual import remains load-bearing.

## R2

- The first three registered commands are the literal lines in [REPLAY_COMMANDS.txt](/intake/package/REPLAY_COMMANDS.txt:1).
- Each producer now creates the requested parent directory before writing: [derive_taub_mghd.py:166-168](/intake/package/derive_taub_mghd.py:166), [verify_independent.py:209-211](/intake/package/verify_independent.py:209), and [run_catch_proofs.py:42-44](/intake/package/run_catch_proofs.py:42).
- In a fresh writable copy under `/work` with no `.review_runtime/` directory present, I ran the first three commands literally, in order, from the copied package directory:

```text
python3 -S derive_taub_mghd.py --output .review_runtime/DERIVATION_RESULT.json
python3 -S verify_independent.py --output .review_runtime/INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output .review_runtime/CATCH_PROOF_RESULT.json
```

- All three commands succeeded, created `.review_runtime/` themselves, and reproduced the sealed artifacts exactly. I verified exact reproduction externally with `cmp -s` against `/intake/package/DERIVATION_RESULT.json`, `/intake/package/INDEPENDENT_VERIFICATION.json`, and `/intake/package/CATCH_PROOF_RESULT.json`.

Conclusion on R2: accepted.

## R3

- The fourth registered command is the literal line [REPLAY_COMMANDS.txt:4](/intake/package/REPLAY_COMMANDS.txt:4): `python3 -S verify_package.py`.
- Static inspection shows that [verify_package.py](/intake/package/verify_package.py:110) now does what R3 requires. It creates a fresh temporary tree at [lines 112-115](/intake/package/verify_package.py:112), copies the package there while excluding `.review_runtime` at [line 116](/intake/package/verify_package.py:116), copies each registered source from [SOURCE_MANIFEST.tsv](/intake/package/SOURCE_MANIFEST.tsv:1) into the fresh temp tree at [lines 117-121](/intake/package/verify_package.py:117), reads the literal replay commands from [REPLAY_COMMANDS.txt](/intake/package/REPLAY_COMMANDS.txt:1) at [lines 122-125](/intake/package/verify_package.py:122), and executes the first three lines literally with `subprocess.run(shlex.split(line), cwd=replay_package, ...)` at [lines 132-135](/intake/package/verify_package.py:132).
- The verifier then checks that the produced files are at the literal advertised paths under `replay_package/.review_runtime/...` at [lines 137-139](/intake/package/verify_package.py:137), and confirms that the current invocation is command four at [line 140](/intake/package/verify_package.py:140). There is no silent substitution to different output locations.
- I also ran the fourth line literally in a fresh `/work` copy. It passed and reported the expected replay assertions, including `literal_replay_exit:...`, `literal_replay_output:...`, `literal_replay_exact:...`, and `current_invocation_is_command_4`.

Conclusion on R3: accepted.

## Scientific Boundary

- The repaired package preserves the same explicit metric imported from G323 at [EXACT_DERIVATION.md:7-14](/intake/package/EXACT_DERIVATION.md:7), matching the G323 source statement at [sources/.../EXACT_DERIVATION.md:52-58](/intake/sources/udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01/EXACT_DERIVATION.md:52).
- It preserves the same curvature obstruction `12 mu^2 / R^6` at [EXACT_DERIVATION.md:50-55](/intake/package/EXACT_DERIVATION.md:50), matching G323 at [sources/.../EXACT_DERIVATION.md:75-82](/intake/sources/udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01/EXACT_DERIVATION.md:75).
- It preserves the same causal/timelike first integral at [EXACT_DERIVATION.md:75-90](/intake/package/EXACT_DERIVATION.md:75), consistent with the G323 global-development boundary formula at [sources/.../EXACT_DERIVATION.md:257-266](/intake/sources/udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01/EXACT_DERIVATION.md:257).
- It preserves the same G322 MGHD category: per-datum, data-preserving, globally hyperbolic maximality only, as stated in the G322 source at [sources/.../EXACT_DERIVATION.md:92-127](/intake/sources/udt_g322_g321_maximal_globally_hyperbolic_development_2026-09-01/EXACT_DERIVATION.md:92) and [160-169](/intake/sources/udt_g322_g321_maximal_globally_hyperbolic_development_2026-09-01/EXACT_DERIVATION.md:160).
- It preserves the G323 lattice modulus rather than redefining the science: G324 explicitly says G323 already derived `Q(Gamma)` and that equation (15) "neither modifies nor refits" it at [EXACT_DERIVATION.md:196-212](/intake/package/EXACT_DERIVATION.md:196), matching the accepted G323 source definition at [sources/.../EXACT_DERIVATION.md:199-224](/intake/sources/udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01/EXACT_DERIVATION.md:199).
- The bounded conclusion is unchanged and still conditional: the preregistered landing token is unchanged at [EXACT_DERIVATION.md:216-220](/intake/package/EXACT_DERIVATION.md:216), the open `C0` boundary is still explicitly retained at [EXACT_DERIVATION.md:177-178](/intake/package/EXACT_DERIVATION.md:177) and [STATUS_LEDGER.tsv:10-15](/intake/package/STATUS_LEDGER.tsv:10), and [DERIVATION_RESULT.json](/intake/package/DERIVATION_RESULT.json:2) still records `false` for `C0_past_inextendibility_proved`, physical occupancy selection, physical topology selection, physical scale selection, and `Xmax_selected`, while leaving `metric_changed`, `kernel_changed`, and `angular_sector_changed` false at [lines 45-55](/intake/package/DERIVATION_RESULT.json:45).

Conclusion on scientific boundary: no scientific claim changed. The repairs alter only support, replay robustness, and replay certification.

## Overall Conclusion

Within the sealed intake and the repair-only scope, R1-R3 are complete and the unchanged bounded landing is now supported. I did not find a remaining load-bearing theorem-interface gap, a missing producer-path repair, or a verifier path-substitution issue.

ACCEPT__R1_R2_R3_COMPLETE__BOUNDED_LANDING_UNCHANGED
