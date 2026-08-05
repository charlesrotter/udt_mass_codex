# Startup/orientation quarantine audit — preregistration

Date: 2026-08-05  
Branch: `grok`  
Base: `f3cdb0153d7f8d50bba3b4dbaf692fd6ff81db83`

## Question

Can the repository's startup surface be made genuinely current and bounded without deleting
historical science, altering research artifacts, or breaking exact-path historical evidence?

## Frozen candidate scope

The only mutable root controls in scope are:

- `LIVE.md`
- `HANDOFF.md`
- `INDEX.md`
- `README.md`
- `MEMORY.md`
- `AGENTS.md`
- the `## Orientation` section of `CLAUDE.md`

`UDT_SCIENTIFIC_FRONTIER_2026-07-19.md` is in the audit universe but is preregistered as an
`IMMUTABLE_HISTORICAL_COMPATIBILITY_PATH`: historical verifiers read its exact root path and
content. It will not be moved or edited, and generic startup will cease to treat it as a current
authority. `CURRENT_RESEARCH_PROGRAM.md`, both current-premise registry files, `CANON.md`, research
artifacts, evidence, scripts, data, manifests, and all R0-R1H records are out of mutation scope.

## Frozen base identities

The exact base identities are recorded in `PRE_CLEANUP_IDENTITIES.tsv`. The protected working-tree
metadata census contains 83 untracked paths and has SHA-256
`131a923e58322166ab247d8f1d8216ca23c8c3119e9c22d126f1efeeb2d61c69` over
`git status --porcelain=v1 -uall`; their contents will not be opened.

## Preregistered transformation

1. Preserve byte-identical full snapshots of all seven mutable controls under
   `archive/startup_orientation_history_2026-08-05/` before changing them.
2. Preserve the exact marked current blocks of `LIVE.md` and `HANDOFF.md`; remove their embedded
   prior layers from the live controls and replace those layers with an archive pointer.
3. Preserve the exact current `MEMORY.md` top; move all `PRIOR TOP` and durable-history material to
   its archived snapshot and leave a pointer.
4. Replace `INDEX.md` and `README.md` with concise current navigation derived only from `LIVE.md`,
   `CURRENT_RESEARCH_PROGRAM.md`, and the current premise registry. Historical family/frontier
   tours remain in their byte-identical snapshots.
5. Remove dated scientific-status narration from `AGENTS.md`. Retain its operational discipline and
   replace the 25-step startup path with a short source-of-truth route.
6. Replace only `CLAUDE.md`'s stale orientation section with a method-only pointer to `AGENTS.md` and
   the current controls. All preceding charter text remains byte-identical.
7. Add a quarantine map, compatibility exception registry, audit report, and fail-closed verifier.

No research claim, equation, premise label, canon statement, source code, data, manifest, or
research artifact may be edited by this audit.

## Certification contract

The result may be called `VERIFIED_STARTUP_ORIENTATION_QUARANTINE` only if:

- every archived full snapshot matches the preregistered Git blob and SHA-256;
- the retained LIVE/HANDOFF current blocks and MEMORY current top match their archived sources
  byte-for-byte;
- exactly one current marker pair remains in LIVE and HANDOFF and no prior marker remains there;
- no `PRIOR TOP`, parent-frontier tour, or prior-checkpoint section remains in live MEMORY, INDEX,
  or README navigation;
- AGENTS has a bounded current route, carries no embedded dated frontier narrative, and preserves
  all binding sections from `## Codex/Claude compatibility` onward byte-for-byte;
- CLAUDE's pre-Orientation charter is byte-identical and its orientation names no scientific
  frontier beyond the current controls;
- the July 19 frontier file remains byte-identical and is explicitly excluded from generic startup;
- all current startup targets and Markdown links resolve;
- the current premise verifier, current-path verifier, six frozen-manifest gate, and full tests pass
  at the documented baseline;
- the protected 83-path metadata hash remains unchanged.

If any gate fails, retain the archive evidence but do not claim the live cleanup verified.

## Maximum conclusion

At most this audit can establish that the repository's startup navigation is current, bounded,
reversible, and provenance-preserving. It makes no scientific or canonization claim.
