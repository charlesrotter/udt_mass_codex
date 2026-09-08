# BI3 initial candidate freeze — 2026-09-08 18:46UTC

UNPROMOTED, review pending. Before this freeze the parent has NOT read the BI3
reviewer's argument, code, or results. Source-first reviewer sealing precedes
candidate exposure. The following files are fixed, relative to step_03:

    c4b285c4b080fcda9d91c8e70c605fccec132f0a8335638d91b2297d32673ade  CANDIDATE_INITIAL.md
    3525ab5ae013eb8826ee31463368a67ccc9ee5f5faa334f26842de4d17698d4b  check_bi3.py
    9addd55b65014f187f23746b420cbc39d97071358d1b4edb06a9046f183fa821  author_check_01.stdout
    ec8dbe18bcd8e049b8697d15fca8e149bd8cd5cfc636471a2c72d4bb64c13499  author_mutations_01.stdout

Author check: exit0,55 named exact checks,12 fixtures;0.263377606s,48848KiB
maximum RSS. Five actual in-memory program mutations were rejected; full mutant
programs/streams are retained in author_mutations_01.stdout. Mutation driver:
0.306458781s,50400KiB RSS,exit0. Every run is limited to512MiB/60s and single
numerical-library threads. No failed author check or scientific repair before
freeze. A pre-freeze notation edit renamed the CK unknown to U, leaving V for
the unit Ricci eigenvector; no mathematical change.

The mutation run reuses step_02/probe_bi2.py by a recorded in-memory AST
adaptation. Its exact command is in author_mutations_01.json and the original
driver hash plus full adapted driver text are in author_mutations_01.stderr.
That nonempty stderr is deliberate provenance, not an execution failure. A
mutant's enclosing source hash identifies its actual text; its internal
__file__ hash still references the unchanged author file. This driver reuse is
not a mathematical dependency on BI2 and not independent recomputation.

The mathematical dependency is reviewed BI1 only (candidate ce6b36dce14c07049ee9be193ca07989c5ea2f2507d8587c7b978317d0980fbc;
review f68aeba4a80fa7b095122d7ea07bc45e3d0213bddbee1d23d64f96e2cd538c80),
with its two retained author false passes and independent full-tensor repairs
to the supporting evidence. BI2 remains pending and is not used. The CK
convergence theorem and local Einstein-Cauchy method are imported mathematical
methods with declared hypotheses, not consequences of finite checks or new
physical premises. The claim is local on a spatial patch, not globally on S3.
