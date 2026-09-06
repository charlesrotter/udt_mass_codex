The saved checkpoint is usable as an operational recovery anchor, but it does not yet justify `READY_FOR_MANUAL_RESTART`.

### Actual local Git state

- Checkout: `/tmp/udt_cold_start_r4_ZjQOSR/repo`
- Branch: `grok`
- `HEAD`: `d5b25b7558ce94c1d8b1a7bd71c4390af063d863` — `Candidate pre-reboot checkpoint`
- Worktree and index: clean after the audit
- Stored tracking comparison: `ahead 1, behind 0` relative to local `origin/grok` at `12e3e5e0`
- No checkout, fetch, pull, internet access, edits, protected-path commands, resume/fork, or solve occurred. Remote freshness is unverified.

### Effective authority chain

1. The controller’s pinned, read-only constraints bound this run.
2. `AGENTS.md` is the primary working-method authority.
3. The current `LIVE.md` block owns current status.
4. The exact 335-row `CURRENT_SCIENTIFIC_PREMISES.tsv` owns scientific grades and source paths; its verifier completed successfully.
5. The matching [HANDOFF.md](</tmp/udt_cold_start_r4_ZjQOSR/repo/HANDOFF.md:7>) block is subordinate to `LIVE.md` and correctly points to the operational checkpoint.
6. `CURRENT_RESEARCH_PROGRAM.md` and `CURRENT_SCIENTIFIC_PREMISES.md` summarize that authority.
7. The required `CLAUDE.md` sections and triggered verifier protocol are shared method instructions; Claude hooks are inactive.
8. `INDEX.md` and `MEMORY.md` are pointers only. `CANON.md` changes require Charles’s sign-off.
9. The work order and [RESTART_CHECKPOINT.md](</tmp/udt_cold_start_r4_ZjQOSR/repo/RESTART_CHECKPOINT.md:1>) carry operational evidence only and cannot change science.

### Current science boundary

The frontier remains G352:

- `phi_pair=delta_AB` is `DERIVED_CONDITIONAL` only on a supplied regular calibrated pair.
- G351 label-measure conservation and G352’s continuous clock-rate readout are owner-adopted provisional premises.
- `T_clock=R A^-1` is accepted only for the explicitly chosen continuous phase/product realization.
- It does not establish light, energy, brightness, a detector law, source, population, distance, matter, history, absolute scale, `X_max`, or canon.
- The next gate is only to MAP/PONDER whether a metric-native carried object realizes the required phase and conserved label measure. No derivation or solve is authorized.

### Operational status

- The checkpoint and handoff pointer are tracked in the candidate commit.
- Recorded R1 and R2 passed with declared read-only limitations; R3 passed with a tool-delay caveat.
- This run satisfies the subject-side R4 criteria: complete ordered orientation, successful premise verification, discovery of the repaired pointer/checkpoint, and no mutation or scientific promotion. Controller capture/review remains needed to record the final R4 verdict.
- `COLD_ORIENTATION_READY`: subject-side pass.
- `PRESERVATION_READY`: blocked.
- `ASTRA_DEPLOYMENT_NOT_YET_TESTED`: unchanged and expected before the owner update.
- Therefore `READY_FOR_MANUAL_RESTART` is not yet supported.

One checksum caveat is nonblocking: `SOURCE_HASHES.sha256` contains the pre-repair `HANDOFF.md` hash. The candidate’s differing bytes are exactly the intended five-line restart pointer, and the candidate commit pins the repaired tree. The checksum file should not be treated as a complete checksum manifest for the candidate tree.

### Concrete blocker

The checkpoint records no separately verified backup or snapshot for protected and other needed untracked workstation content. The owner must confirm that preservation and account for any unsaved state in the unrelated OCCT/inactive Claude processes before reboot.

### First post-restart sequence

After the owner resolves preservation, performs the reboot, and updates Codex through the existing installation route:

1. Launch a genuinely new Codex process from the verified repository—no resume or fork—and use the work order’s post-restart message.
2. Run the mandatory Git sequence while preserving dirt:

```bash
git status --short --branch
git checkout grok
git fetch origin
git pull --ff-only origin grok
git status --short --branch
git log -8 --oneline
```

3. If synchronization changes an automatically loaded instruction source, restart the acceptance process.
4. Repeat the bounded startup reads and orientation before mutation.
5. Verify the resolved Codex binary/version, login status, actual model/provider/profile, and context/memory participation.
6. Recheck processes, GPU state, backup disposition, ScratchDisk mount, and required data path.
7. Run both premise and metric-kernel-account verifiers in an approved writable environment.
8. Run the stale-authority and bounded-permission acceptance cases, then report `READY_TO_RESUME_BOUNDED_WORK` or exact remaining blockers.