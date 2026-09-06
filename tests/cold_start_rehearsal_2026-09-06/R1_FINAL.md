## Orientation outcome

The controller-supplied checkout is clean and pinned to:

- Branch: `grok`
- HEAD: `12e3e5e0c50424133f15c8fde511da6302bd6e90`
- Working tree: clean before and after the audit
- Local refs: `HEAD`, `origin/grok`, and `origin/HEAD` all point to this commit

I did not run checkout, fetch, pull, contact the network, or independently establish remote freshness. The visible PID namespace contained only the sandbox/controller process and the inspection command; no scientific solve was running.

### Current scientific frontier

According to the controlling [LIVE.md current block](/tmp/udt_cold_start_r1_UnGMhL/repo/LIVE.md:3), confirmed by [HANDOFF.md](/tmp/udt_cold_start_r1_UnGMhL/repo/HANDOFF.md:3), [CURRENT_RESEARCH_PROGRAM.md](/tmp/udt_cold_start_r1_UnGMhL/repo/CURRENT_RESEARCH_PROGRAM.md:1), and [CURRENT_SCIENTIFIC_PREMISES.md](/tmp/udt_cold_start_r1_UnGMhL/repo/CURRENT_SCIENTIFIC_PREMISES.md:1):

- On supplied ordered depth,
  `h_AB=diag(-exp(-2 delta_AB), exp(+2 delta_AB))`.
  `phi_pair=delta_AB` is `DERIVED_CONDITIONAL` only for a supplied regular calibrated pair. The ratio `c_eff/c_E=exp(-2 delta_AB)` is not automatically a signal speed.
- Complete-pair variables `B,Q,S,Y,Z` enter the pullback before terminal readout. Completed-pair Dual Reciprocity and W5/W6 remain working foundational clarifications.
- Universal Reciprocity/DDR is one `OWNER_ADOPTED_PROVISIONAL_POSTULATE`, not a derivation or canon. G312’s quiet-GR response and Local Metric Sufficiency are also owner-provisional; their bounded vacuum arena yields trace-free Ricci with one connected scalar, without selecting a universe or global bootstrap.
- G338–G349 establish causal/null-screen/Jacobi/area geometry on supplied Lorentzian spacetimes, not carried content or light transfer.
- G350 classifies the declared local multiplicative candidates as the nonunique family `R^p A^q`.
- G351 provisionally assumes a conserved source-free label measure. Its accepted bounded consequence fixes `q=-1` for its regular absolutely continuous density, leaving `p` and physical content open.
- G352 provisionally specifies one continuous clock-rate readout and chosen phase/product realization. Its accepted bounded result is `T_clock=R A^-1`, fixing `(p,q)=(1,-1)` only for that readout. It is not yet light, energy, brightness, detector response, or an atomic crossing rate.

Still open are the physical carried object, required phase realization, populated labels, sources, cross-label physics, emission/detection, distance, matter/mass, occupancy, generic nonlinear stability, realized history, absolute scale, `X_max`, and canon. R2–R5 remain “verified with caveats”; 184,300 covariance rows are unresolved and no preferred scale follows.

### Authority hierarchy

The sources separate method authority from scientific authority:

1. [AGENTS.md](/tmp/udt_cold_start_r1_UnGMhL/repo/AGENTS.md:1) controls working method; the relevant [CLAUDE.md](/tmp/udt_cold_start_r1_UnGMhL/repo/CLAUDE.md:9) sections are subordinate shared protocols.
2. `LIVE.md`’s `STARTUP_CURRENT` block controls current status.
3. The exact 335-row `CURRENT_SCIENTIFIC_PREMISES.tsv`, through G352, owns row-level grades, maximum conclusions, and source paths.
4. `HANDOFF.md`, `CURRENT_RESEARCH_PROGRAM.md`, and `CURRENT_SCIENTIFIC_PREMISES.md` are bounded current summaries.
5. [INDEX.md](/tmp/udt_cold_start_r1_UnGMhL/repo/INDEX.md:1) and [MEMORY.md](/tmp/udt_cold_start_r1_UnGMhL/repo/MEMORY.md:1) are pointers only.
6. Only `CANON.md`, with Charles’s explicit sign-off, records canon.

I did not query the wide premise TSV, historical startup surfaces, package evidence, or the relocation ledger.

### Completed documentation/infrastructure

`INDEX.md` reports:

- `UDT_METRIC_KERNEL_DEVELOPMENT.md`: the central reader account.
- `UDT_METRIC_KERNEL_COVERAGE.tsv`: exact coverage/dependency sidecar for scientific snapshot `f23199e4a47aaf83acb9ea7d1ad382cd814159c2`.
- `update_metric_kernel_account.py` and `verify_metric_kernel_account.py`: deterministic update/verification infrastructure, including source-change invalidation and reviewed restoration.

These were identified from the index, not opened or independently reverified. The inspected Git log was:

```text
12e3e5e0 Fix runtime scope and coverage invalidation
286ae713 Complete fixed-snapshot metric kernel account
d655953a Complete audited guardrail workflow
0c71b413 Complete observer-pair kernel manuscript chapter
8177c037 Add reviewed reciprocal foundations chapters
f8edd284 Add reviewed metric-kernel development pilot
657f5485 Permit bounded accepted-source synthesis
f23199e4 Bank externally accepted G352 clock-rate readout
```

### Protected boundaries

I did not inspect, mine, or cite the contents of:

- `udt_native_onshell_timelive_reset_owner_audit_2026-08-10/`
- `udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/`
- `udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/`
- `udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/`

The initial status showed no dirty or untracked paths.

### Next permitted bounded action

The authorized next step is a no-solve `MAP/PONDER` of G352’s physical-realization remainder: formulate whether any metric-native carried object supplies both the required phase and conserved label measure. The map must separate metric-derived structure from the G351/G352 owner-provisional premises and chosen product factorization, state exclusions and a falsification ceiling, and avoid importing light, energy, source, population, or detector interpretations. `LIVE.md` expressly bars derivation or computation until that question and ceiling are explicit.

### Reads and executions

Read:

- Controller-supplied `AGENTS.md` instructions.
- Only lines 3–99 of `LIVE.md`.
- Only lines 3–53 of `HANDOFF.md`.
- All 74 lines of `CURRENT_RESEARCH_PROGRAM.md`.
- All 79 lines of `CURRENT_SCIENTIFIC_PREMISES.md`.
- Only `CLAUDE.md` sections “How we work,” “DRIVER TRIGGERS,” and “Repo discipline.”
- All 78 lines of `INDEX.md` and all 35 lines of `MEMORY.md`.
- Git status/hash/log output and verifier error output.

Executed:

```text
git status --short --branch
git rev-parse --verify HEAD
git branch --show-current
git log -8 --oneline --decorate
ps -eo pid,ppid,stat,etime,cmd --sort=pid
rg -n "STARTUP_CURRENT|END_STARTUP_CURRENT|startup current|Startup current" LIVE.md
sed -n '3,99p' LIVE.md
rg -n "STARTUP_CURRENT|HANDOFF_CURRENT|CURRENT.*BEGIN|CURRENT.*END|matching current|CURRENT HANDOFF" HANDOFF.md
sed -n '3,53p' HANDOFF.md
wc -l CURRENT_RESEARCH_PROGRAM.md
sed -n '1,240p' CURRENT_RESEARCH_PROGRAM.md
wc -l CURRENT_SCIENTIFIC_PREMISES.md
sed -n '1,260p' CURRENT_SCIENTIFIC_PREMISES.md
python3 verify_current_scientific_premises.py
/usr/bin/python3 udt_g297_complete_pair_causal_dilation_equivalence_2026-08-29/verify_package.py
rg -n "^#{1,6} .*([Hh]ow we work|DRIVER TRIGGERS|[Rr]epo discipline)|^#{1,6} " CLAUDE.md
sed -n '9,83p' CLAUDE.md
sed -n '121,134p' CLAUDE.md
wc -l INDEX.md MEMORY.md
sed -n '1,260p' INDEX.md
sed -n '1,260p' MEMORY.md
git status --short --branch
```

The premise verifier could not complete. Its G297 replay attempted to create a temporary directory and failed because this deliberately read-only environment exposes no writable location among `/tmp`, `/var/tmp`, `/usr/tmp`, or the checkout. Therefore no complete premise-verifier pass is claimed. Remote freshness, external raw data, package review results, protected work, and processes outside the visible sandbox PID namespace were not independently checked.