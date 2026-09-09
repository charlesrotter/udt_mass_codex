# LG2 review evidence and resource record

Reviewer /root/lg2_review, exact model UNKNOWN, fresh separate context.
All calculation commands ran from /home/udt-admin/udt_mass_codex, one at a time,
with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1. The unchanged
runner is udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py,
SHA256 8ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef.
Its enforced limits are 512 MiB address space, 60 seconds CPU and wall timeout.
Python 3.10.12; SymPy 1.13.1. No GPU, PDE solve or long production run.

The exact invocation pattern was:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_localized_geometry_campaign_2026-09-09/step_02/review/NAME /home/udt-admin/udt_mass_codex python3 -B udt_localized_geometry_campaign_2026-09-09/step_02/review/SCRIPT [ARG]

Each capture's JSON stores the full child command and working directory.

| NAME | SCRIPT / ARG | Start UTC | Seconds | Exit | Meaning |
|---|---|---|---:|---:|---|
| independent_algebra_run | independent_algebra.py | 17:41:09.006472 | 0.718298 | 0 | Pre-candidate-exposure independent exact algebra |
| direct_checks_run | direct_checks.py | 17:43:44.547940 | 0.391606 | 0 | Post-exposure candidate invariant and source-map check |
| catch_central_parity | hostile_claims.py central_parity | 17:45:07.982997 | 0.738863 | 1 | Expected red: rotation survives weak parity |
| catch_raw_blend | hostile_claims.py raw_blend | 17:45:08.843363 | 0.727741 | 1 | Expected red: cutoff does not solve constraints |
| catch_raised_map | hostile_claims.py raised_map | 17:45:09.693472 | 0.426201 | 1 | Expected red: variable raising changes derivative |

Peak recorded child RSS was 62412 KiB. All five runs completed without timeout.
The three exit-1 runs are intentional rejected false claims, not lost diagnostics
or failed good-candidate checks. They reuse reviewer algebra and establish no
extra independence axis. No hard-coded aggregate assertion count is claimed.

## Source access, correspondence and scope

Read the on-disk bounded startup/protocol chain and the load-bearing sources
identified in SOURCE_FIRST.md. Verified every entry of the parent's existing
SOURCE_SHA256SUMS against disk. That correspondence check included some
manifest entries whose contents were not made load-bearing; it does not mean
all those sources were scientifically re-reviewed. G303/G315/G324 exact sources
and G310/G312 adoption records were read directly. LG1's candidate and whole
direct review were read as permitted reviewed UNPROMOTED dependencies.

Additional source pins at stage A:

    498a04779a831259969abe64f5140b7d1b24d3d5e5505b464b24726f8dab2313  CAMPAIGN_LOG.md (question snapshot)
    bcbeafc7f19bf29a298244bac7664748668175fe8b4a53f4a7d13db1c258098e  step_01/CANDIDATE.md
    ee5d02291a6ce45a3ddc7763fa103a4ef666458b049970b142d0ab459f538698  step_01/review/DIRECT_REVIEW.md
    8653bb2162b54965c9fe0a74a17aa5cb1da9114b6289b15fb8f46cc4b30b2a63  udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01/EXACT_DERIVATION.md

The campaign log is expected to acquire later execution entries. Its stage-A
hash identifies the source-first question snapshot, not a claim that a living
log must remain byte-identical forever.

Primary gluing-method source:
https://arxiv.org/pdf/gr-qc/0301073 (v2, printed 11 Jul 2003; 87 pages).
Accessed 2026-09-09 through web and a separately downloaded PDF. Sandbox curl
failed with DNS resolution, and an approved network retry succeeded. Download
command, from the repo root:

    curl -fL --max-time 45 https://arxiv.org/pdf/gr-qc/0301073 -o udt_localized_geometry_campaign_2026-09-09/step_02/review/chrusciel_delay_gr-qc_0301073v2.pdf

Used pdftotext -layout for inspection, and pdftoppm on printed page 4 followed
by local image inspection to verify covector index placement. The web PDF
screenshot route partly failed with a cache miss, so it was not relied on for
that conclusion. Source-first stage inspected the exact theorem statements,
fixed-reference inverse construction, weighted definitions and applications;
the review did not reconstruct the entire 87-page paper.

At the parent's request the unmodified public PDF, complete text extraction and
one rendered page were moved from review/ to the task-specific temporary folder
/tmp/udt-lg2-review-source-PAduim/. This is a recoverable move, not deletion.
The source-first note is unchanged. It describes the original inspection state;
this later relocation explains where the referenced full text is now retained.

    953f003fe179d5f686284b5755fcd4df381d3bbd3e9897bc11605650f3832dbb  /tmp/udt-lg2-review-source-PAduim/chrusciel_delay_gr-qc_0301073v2.pdf
    3eb968ce77de33f4b0c4ec7fa6b4661c8329aa0a9054ed8bf74693cbe2efa4cf  /tmp/udt-lg2-review-source-PAduim/chrusciel_delay_gr-qc_0301073v2.txt

The temporary path is not a durable repository evidence dependency; URL/version/
hash identifies the external mathematical method. A bounded search for primary
corrections returned the original paper and author/publisher copies; no relevant
erratum was identified in that search. This is not a proof that no erratum exists.
Only the specified primary paper is load-bearing in the theorem application.

The parent's original freeze and focused repair manifests independently passed.
Original candidate, source-first note, initial objection, repair and final review
remain distinct. Checksums attest byte correspondence, not scientific truth or
independence. Full365's existing failure is unchanged; no banking was attempted.
