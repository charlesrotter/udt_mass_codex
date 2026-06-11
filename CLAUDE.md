# UDT Mass Codex — Working Charter

Claude drives this project (handed over by Charles 2026-06-10). Charles
canonizes; nothing is canonical without his sign-off.

## Charles's working principles (binding, embed in every plan)

1. **Uncover what the metric is doing. Do not import or create
   mechanisms.** Every coupling, source, or operator must be derived from
   the UDT metric/action, never posited because it would help.
2. **No approximations or linearizations except as short-lived hypothesis
   development** — never as stated results or as inputs to other
   calculations. (Legacy warning: exp(-2·phi0) ~ 5 at hadronic depth;
   linearization is invalid by ~5x there.)
3. **We are not recreating Standard Model entities or analogs. We match
   observations.** SM names (quark, color, gauge) are labels only until
   the metric demands them.
4. **The GR corpus is a mine**: large bodies of GR mathematics (boundary
   terms, constraint equations, junction conditions, DtN/Calderon theory,
   geon/self-trapping literature) can be transformed under positional
   dilation and explored natively.
5. **The orchestra metaphor**: mass emergence is expected to be a
   composition of sectors playing together (radial phi, angular,
   boundary, topology) — invisible if any instrument is probed alone.
   Null results on solo instruments do not rule out the ensemble.
6. **Zoom out often.** No tunnel vision. Re-read STATE.md and step back
   before each new push.

Charles's standing physical hunch (2026-06-10): native discreteness will
come from an INTERACTION of the phi sector and the angular sector —
perhaps through a metric function not yet uncovered. Treat phi-angular
coupling as the prime suspect for the discreteness gap.

## Session workflow

- **Maximize the use of subagents to preserve main context** (Charles,
  2026-06-10): delegate reconnaissance, implementation, verification, and
  doc-drafting to agents; keep only distilled reports in the main loop.
  Present the process plan before launching long pushes.
- **Use the GPU** (Charles, 2026-06-11): a Tesla V100-PCIE-32GB is
  available via PyTorch (`torch.linalg`, float64, cuda=True; note
  nvidia-smi/NVML is broken — driver mismatch — but torch works fine;
  expect an NVML warning, ignore it). Production eigensolves, scans,
  and flow sweeps should use batched torch float64 (~14 ms per
  1024² symmetric eigensolve batched; 6x single-solve). Keep mpmath/
  sympy on CPU for high-precision anchors and symbolic identities;
  GPU results get CPU spot-checks at a few points per run.

## Repo discipline (the Self-Hardening culture — do not soften)

- Research-record markdown docs are append-never-edit; committed audit
  scripts are immutable. New work = new files.
- **Verifier-before-record**: every result (positive or negative) gets a
  blind adversarial verifier pass, recorded in its results doc with agent
  id and date, before commit.
- **Pre-register before testing**: falsification contracts (frozen model,
  candidate lists, tolerances, look-elsewhere accounting) are committed
  BEFORE the test runs. No retuning after.
- Calibrate, never dramatize. Failures are recorded as failures. Negative
  results are first-class deliverables.
- Null-test discipline: exact rational matches are cheap (small-rational
  coverage ~16-23%, see dimension_ladder_null_audit.md). New value
  identities must pass the TEST-B-style classifier (generalize, solve,
  check N-specificity) before being banked as evidence.
- **Negative results are scoped, never absolute** (Charles, 2026-06-11):
  every banked negative/no-go carries its PREMISE SET (background,
  source treatment, boundary conditions, domain class, truncation,
  method). The living index is NEGATIVES_REGISTRY.md. When any premise
  is later revised or refuted, every negative carrying it is flagged
  CONDITIONS-CHANGED in the registry and loses blocking authority until
  re-graded under the new conditions. Check the registry at every push
  plan and every premise-changing result.
- **Hypothesis discipline** (Charles, 2026-06-11: "I'm trying to find
  what's real, not what confirms my priors"): Charles's physical
  pictures are direction, not evidence. Aim verifiers hardest at
  results that would confirm the standing picture; accommodations to a
  hypothesis are pre-registered, never retrofitted after a residual.
- Commit per result; push to github.com/charlesrotter/udt_mass_codex.

## Canon

Charles-canonized statements live in CANON.md (append-only). As of
2026-06-10: R-areal reading (rho = r is a theorem; branch-(iii) statics
closed), the finite-cell canon (no spatial infinity; universe and matter
cells are finite mirrored domains), and the discreteness-program
redirect (nonstationary weld sector / transfer ladder / ensembles).

## Orientation

- Load STATE.md first (frontier snapshot), then INDEX.md (repo map).
- Main research record: negative_phi_native_geometry.md (31k lines,
  pre-spectrum) and particle_spectrum_native_geometry.md (spectrum stage).
- Audit/prosecution record: mass_emergence_canonical_geometry.md
  (binding Self-Hardening Protocol — re-read before editing anything).
- Legacy (superseded, mine for structure only): udt_canonical_geometry.md
  via legacy_hadron_survivor_filter.md.
