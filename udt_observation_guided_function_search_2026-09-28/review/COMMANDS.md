# Reviewer commands and exposure chronology

All paths are relative to `/home/udt-admin/udt_mass_codex` unless absolute.
Review identity and runtime versions: SOURCE_FIRST_PINS.json,
INDEPENDENT_RAW_F2.json, INDEPENDENT_ANALYTIC.json. CPU only, <=2 threads,
2-GiB address-space limit set inside both calculation scripts, 600-second
external command timeout. No author code was imported by either script.

1. Independently ran `git status --short --branch`, `git rev-parse HEAD` and
   later `git branch --show-current`; parent top-level synchronization attributed.
   Read AGENTS/current source scope, required CLAUDE sections and triggered
   protocols. Saved source-first frame at 12:10:43 UTC before current candidate,
   code or outcome exposure. Read additional source reports/public release schema
   and likelihood before outcomes; SOURCE_SUPPLEMENT_PINS.json records those.
2. After parent authorized data exposure, independently wrote raw F2 code from
   the frozen equations, then ran:

   `timeout 600s python3 udt_observation_guided_function_search_2026-09-28/review/independent_raw_f2.py > udt_observation_guided_function_search_2026-09-28/review/independent_raw_f2.stdout 2> udt_observation_guided_function_search_2026-09-28/review/independent_raw_f2.stderr`

   Exit 0, elapsed process wall time about .68 seconds. Scientific output and
   input hashes: INDEPENDENT_RAW_F2.json; no stderr. Read actual fit outcomes
   only after this implementation/run. Compared full F2/validation/AP arrays
   with saved artifacts; NUMERICAL_COMPARISON.json records differences.
3. Parent sealed integrated candidate at 12:13:28 UTC. Read candidate and
   derivations, followed by fitting/alias/AP implementations and source-method
   statements. Verified all 132 construction files against their sealed SHA-256
   and sizes with a separate Python hash loop: CONSTRUCTION_CHECK.json.
4. Independently wrote exact/high-precision inverse/tail check and ran:

   `timeout 600s python3 udt_observation_guided_function_search_2026-09-28/review/independent_analytic.py > udt_observation_guided_function_search_2026-09-28/review/independent_analytic.stdout 2> udt_observation_guided_function_search_2026-09-28/review/independent_analytic.stderr`

   Initial exit 1 was a SymPy logarithm-branch artifact in a divergent real
   integral; original script/stdout/stderr are preserved as INITIAL_*.
   A read-only diagnostic printed seven check booleans, isolating the affine
   integral, and showed `integrate(1/(1-T),(T,-oo,0))` returning `oo-I*pi`
   while `limit(log(1-T),T,-oo)` returns `oo`. A positive-variable substitution
   repaired the check without changing the mathematical integral.
   Next exit 1 occurred only while serializing a SymPy integer after all
   scientific assertions passed; script/stdout/stderr are preserved as
   SERIALIZATION_FAILURE_*. Explicit integer conversion repaired packaging.
   The final command exited 0 in about .28 seconds with empty stderr.
   INDEPENDENT_ANALYTIC.json records exact root counts, 65-digit quadrature and
   metric-derived Ricci expression. ANALYTIC_REVIEW.md gives direct arguments.
5. Inspected parent's saved full-premise capture, stdout tail and stderr;
   exit 0 and PASS are documented in its checks/. Full audit not repeated.
   Independently viewed the original and corrected BAO PNGs with view_image.
   Inspected plotting script and repaired score JSON directly; no fitting was
   performed during presentation review. Initial verdict: INITIAL_REVIEW.md.

Shell read commands used `cat`, bounded `sed`, `head`, and path-scoped `rg`;
they did not access protected payloads. The independent alias scan uses the
raw primary release only. Read-only source-method excerpts were obtained with
the standard-library HTMLParser; no new download or external message was sent.
No mutation/catch guard was introduced, no author solver rerun was called
independent, and no additional finite sweep was used as a completeness proof.
