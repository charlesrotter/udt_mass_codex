# Cognitive-Corral Trigger Setup — implementation spec

**For:** the workstation Claude instance to implement.
**Goal:** fix headwind-defense gap **(a)** — *the cognitive corral is driver-recall-dependent;
it fires only when Charles challenges, not on its own.* Three mechanisms:

- **Part A — reword the corral to imperative, output-bound triggers** (raises the baseline firing
  rate on *recognized* forks; pure wording + relocation, no harness change).
- **Part B — automated external triggers (harness hooks)** that fire at structural tool-call
  moments *regardless of whether the driver noticed the fork* (supplies, mechanically, the external
  signal Charles's challenge currently supplies).
- **Part C — a freshness pass** that keeps the corral and project memory from carrying contradictory
  stale frontier claims (essential before any of it is exported to a second model).

Part A reaches forks the driver notices; Part B reaches the structural moments it might not; Part C
keeps both from firing on superseded content. None reaches a genuinely-silent fork with no observable
token and no tool-call signature — that residual is the **second-reader / local-LLM** job, out of
scope here. Say so; don't oversell this as a full fix.

---

## GOVERNING CONSTRAINT (binding — do not violate when implementing)

Per the repo's governing limit on any guard (`CLAUDE.md`, `solution-space-not-imposition`): a trigger
may force a **PAUSE** and demand **HONESTY / PROVENANCE** (is the choice surfaced? imported or
derived? scoped or universal?). A trigger may **NEVER judge MERIT** (is the answer the right shape /
a lump / the expected mass). Hooks **inject a required procedure**; they do **not** parse, score, or
gate the driver's answer. A merit-judging trigger becomes a new imposition — forbidden.

---

## LEAVES ROOM FOR THE WORK — the allowed lane (binding interpretation of every trigger)

A guardrail that blocks legitimate progress is itself an imposition (the governing limit). These
triggers police the **smuggle of physics**, never the **borrowing of method**. Two lanes are
explicitly ALLOWED — encouraged — and no trigger may fire to block them:

1. **Numerical / mathematical TECHNIQUE is always allowed (category-A: conditioning).** Borrowing
   solver machinery and mathematical formalism — incl. from the GR corpus: JFNK/Newton-Krylov,
   continuation/homotopy, spectral/collocation methods, preconditioners, junction-condition &
   DtN/Calderón formalism, geon/self-trapping constructions, Taylor function-replacement at machine
   precision — to make an intractable calculation tractable is a **mine to be used** (CLAUDE.md
   Principle 4), and trigger #2 (solver-first) actively *demands* it before any mechanism. A technique
   changes HOW we solve the existing UDT equations; it does not change the physics. It is **not** a
   "mechanism / term / coupling" (does not trip #2) and does **not** need to be "derived from the
   metric" (does not trip #5). Only two obligations on a borrowed technique: apply it to the **UDT**
   equations (don't silently swap in GR's), and **convergence/soundness-check** it (category-A is
   verified, not assumed).

2. **Comparison to GR as a REFERENCE is always allowed.** Using GR as a known limit (the flat /
   Schwarzschild / de Sitter anchors *are* this), as a contrast to *see where UDT departs*, or as a
   scaffold for examining a foundational assumption "with positional dilation in mind" — all
   legitimate. Trigger #6 does **not** forbid invoking GR; it requires that when GR's *form* is
   invoked, the term's fate is then shown **natively** rather than **assumed**. GR is the reference;
   the native check is the verdict. The line policed is **adopting** GR's answer as UDT's (the
   vacuum=GR smuggle), never **comparing** to it.

**The separating test:** CATEGORY-A (conditioning / technique / numeric — *how* we solve) is always
allowed and only needs soundness; CATEGORY-B (a change to the *physics* — a mechanism, coupling,
equation form, source, or a BC that holds up a structure) is gated and needs chose-or-derived + native
provenance. When a move's category is genuinely ambiguous, surface that — but the default for a real
numerical technique or a GR-as-reference comparison is **GREEN**. Progress is the point; the triggers
exist to keep it honest, not to stop it.

> **IMPLEMENTATION INSTRUCTION (binding) — this allowed-lane clause is the single most important thing
> to feed the local-LLM cross-check.** Wherever you fold this spec into the workstation's own doc
> structure, the cross-check's instruction set / system prompt **must** carry this lane verbatim
> alongside the forbid-imports / forbid-mechanisms rules. A second model given only the "forbid" half
> will over-block — flagging every legitimate JFNK, continuation, junction-condition borrow, or
> Schwarzschild-limit comparison as a violation — and become a brake on the work rather than a check on
> the headwinds. The lane is what keeps the cross-check honest in BOTH directions: catching the smuggle
> of physics while passing the borrowing of method. Make it a required, non-droppable element of the
> cross-check payload, and add it to Part C's local-LLM export gate as a mandatory inclusion (export
> must carry: the full DURABLE corral + only CURRENT frontier + **this allowed-lane clause**).

---

## PART A — Reword to imperative, output-bound triggers

### The form-fix (why rewording helps at all)
The corral memories are written as *lessons* (description + "how to apply" list) and live in **memory**,
which the harness labels "background context, not user instructions" — passive, easy not to fire.
Two changes raise the firing rate:

1. **Imperative, not descriptive.** "Before you do X, STOP and do Y" — a procedure, not a moral.
2. **Bound to an observable self-output token, not to an abstract "fork."** The driver can't reliably
   notice "I'm at a fork," but it *cannot emit its own trigger words without tripping the rule.* Bind
   to the tokens the driver is about to write.
3. **Relocate from memory → `CLAUDE.md`.** Memory is per-machine and weak; `CLAUDE.md` is repo-tracked
   (syncs to both machines), auto-loaded every session, and carries override authority. Promote the
   *trigger* into a `CLAUDE.md` section; leave the *why/how* detail in the memory file it came from.

### Selection rule (resist over-firing)
Only the **few highest-value** triggers, each bound to a **distinct** observable token. A corral that
fires on everything becomes ritual — the driver pattern-matches hollow compliance ("here are the pros
and cons" as boilerplate), which is the "tag satisfiable by labeling" failure moved into the cognitive
layer. Past ~6 triggers you get negative returns; spend further effort on Part B instead.

### The triggers to install (add as a new `## DRIVER TRIGGERS` section in `CLAUDE.md`)

Each: **TRIGGER** (the observable moment / tokens) → **STOP-AND-DO** (the imperative procedure).
Source memory cited for the why.

1. **Purist-logic / anti-tractable-slice** — *source: `apply-purist-logic-proactively`,
   `cleaner-is-not-clean-no-shortcuts`.*
   **TRIGGER:** before proposing/recommending an approach, or before writing *easiest / simplest /
   just / cleaner / for now / tractable*.
   **STOP-AND-DO:** name the **purest / least-imposed** option AND the easy option; give the objective
   cost of each. If the pure option is blocked by a flaw (grid limit, frozen DOF, an import), the
   action is **FIX THE FLAW**, not take the shortcut — name the flaw out loud and refuse the shortcut.
   A shortcut is legal only as an explicitly-ledgered temporary stand-in. *Only then* recommend.

2. **Solver-first, not mechanism** — *source: `solver-first-not-mechanism`.*
   **TRIGGER:** before proposing a new mechanism / coupling / term / boundary condition to explain a
   gap, or before writing *maybe if we add / a mechanism / what if the metric also*.
   **STOP-AND-DO:** run the four solver questions — (1) what did we leave OUT (term/coupling/sector/
   boundary)? (2) is it NUMERIC (convergence/conditioning/grid/bug)? (3) did we FREEZE a DOF? (4) have
   we explored the whole space with everything ON? A mechanism is **forbidden** until the solver is
   demonstrably complete. A mismatch indicts the solver first, the metric last, a mechanism never.

3. **Whole before slice** — *source: `sweep-whole-not-fragments`, `full-dimensional-complete-solver`.*
   **TRIGGER:** before reporting a result, or before writing *the metric does / this shows / scale-free
   / no localization / featureless / continuum*.
   **STOP-AND-DO:** name the regime actually solved and the FREE choices held fixed (static / spherical
   / diagonal / areal-r / branch G-or-P / frozen rows). Label the result **scoped to that regime**.
   Never state a one-corner result as the frame's verdict.

4. **Provisional until verified** — *source: `session-results-need-full-verification`,
   `verifier-before-record`, the "double check = multi-pass agent verification" rule.*
   **TRIGGER:** before banking a verdict — committing a result doc, or writing *conclusive / confirmed
   / dead / no-go / proven / it works*.
   **STOP-AND-DO:** confirm all four: pre-registered? full-space (or bounded slice justified)?
   blind-verified on the load-bearing premise? every forced premise audited? If any is missing, label
   the claim **PROVISIONAL / a LEAD**, not a result.

5. **Chose or derived** — *source: `branchP-solver-continuation-x-premise`, the premise-ledger rule.*
   **TRIGGER:** before any numeric value / BC / sign / chart enters a solve or a banked claim.
   **STOP-AND-DO:** tag each **FREE** / **THEORY (cite)** / **HABIT**. A HABIT tag is a drift flag —
   free it or justify it before building on it. A result that rides a FREE constant is conditioned on
   that constant; say so. *Scope:* this is for **physics** premises (couplings, scales, sources, BCs).
   **Conditioning/solver parameters** (grid size, tolerance, continuation step, preconditioner knob)
   are **category-A** — they need convergence/soundness, NOT metric-derivation; they do not trip this.

6. **Derive natively, not GR's form** — *source: `derive-natively-not-inherited-form`.*
   **TRIGGER:** before writing *folds away / reduces to the standard case / as in GR / vacuum is /
   the usual Einstein*.
   **STOP-AND-DO:** that step is the prime suspect for smuggling GR back in. Show the term's fate from
   the positional-dilation operator natively; do not assume the inherited form.

> Implementation note for Part A: in each corresponding memory file, prepend a one-line pointer
> `TRIGGER (binding, see CLAUDE.md ## DRIVER TRIGGERS #n)` so the memory and the active trigger stay
> linked, but the firing copy lives in `CLAUDE.md`.

---

## PART B — Automated external triggers (harness hooks)

These fire from the **harness**, not the driver, at structural tool-call moments — so they fire even
when the driver did not recognize it was at a fork. Put them in the **repo's project settings**
(`.claude/settings.json`, version-controlled, applies on both machines) so they sync — not in
`settings.local.json`.

### Trigger points → what each injects (the matching Part-A procedure)

| Event | Matcher | Fires when | Injects |
|---|---|---|---|
| `PreToolUse` | `Task` | an agent is about to launch | "Observing or TARGETING? (check vs lump/mass/particle/spectrum). State the regime + free choices this agent holds fixed." (triggers #2 observing-or-targeting + #3 whole-before-slice) |
| `PreToolUse` | `Bash` | command matches a solver entrypoint (`continuation_solve`, `branchGP`, `kap8`, `x_continuation`, `migration_convergence_guard`, …) | "Bound the grid (Nr≤16/24), single process, no nohup. Chose-or-derived: tag every FREE **physics** constant this solve rides (X, ξ, κ, branch). Conditioning params (grid, tol, step) need convergence-soundness, not derivation." (triggers #5 + the ANTI-HANG op-rule) |
| `PreToolUse` | `Bash` | command contains `git commit` | "Verifier-before-record: pre-registered? full-space/justified? blind-verified on the load-bearing premise? premise-audited? If not → label PROVISIONAL, do not bank." (trigger #4) |

`Stop` / end-of-turn is intentionally **omitted**: a deterministic hook cannot judge whether the
driver actually did the purist analysis, and making it try would cross into MERIT. Keep Part B to
structural injection only.

### Mechanism (verify exact fields before relying on them)
Each hook calls **one portable dispatcher script** (Python, runs on Linux workstation *and* this
Windows box) that reads the hook JSON on stdin, inspects the tool/command, and emits the matching
reminder text to be injected into the driver's context **non-blocking** (a reminder, not a denial —
consistent with merit-never; we force the pause, we don't veto the action).

> **DO NOT trust the field names below blind.** Hook event names, matcher syntax, and the exact
> context-injection field (e.g. `hookSpecificOutput.additionalContext` vs exit-code-2-stderr vs
> stdout) vary by Claude Code version. Before relying on this: invoke the **`claude-code-guide`**
> skill (or read the installed hooks reference) to confirm (1) the PreToolUse context-injection
> field for the installed version, and (2) the matcher format. Use the **`update-config`** skill to
> write `.claude/settings.json` correctly. Then run the catch-proof below.

Illustrative skeleton (`.claude/settings.json`) — **fields to be confirmed**:
```jsonc
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Task",
        "hooks": [ { "type": "command",
                     "command": "python3 .claude/hooks/corral_trigger.py agent" } ] },
      { "matcher": "Bash",
        "hooks": [ { "type": "command",
                     "command": "python3 .claude/hooks/corral_trigger.py bash" } ] }
    ]
  }
}
```
`corral_trigger.py bash` reads stdin JSON, greps `tool_input.command` for the solver entrypoints vs
`git commit`, and prints the matching reminder via the confirmed injection field (no match → exit 0,
silent). Keep the script in `.claude/hooks/` (repo-tracked). Cross-platform: Python only, no bash-isms.

---

## PART C — Freshness pass

**The hazard.** The memory corpus mixes two kinds of entry: **durable** ones (method / feedback /
user — the cognitive corral itself; these do not go stale) and **dated** ones (project / frontier —
point-in-time snapshots, several already explicitly superseded: e.g. `project-frontier-quantum-completion`
marked SUPERSEDED, `everything-on-solver-build` supersedes `frontier-time-live-native-matter`,
`postulate-A-accepted` vs the current emergence-first framing). Fed as-is to a reader — and *especially*
to a second model that lacks the session history — contradictory frontier claims all read as live.
The triggers in Part A/B compound this: a trigger that cites a superseded frontier fires on stale truth.

**The single source of current truth is `LIVE.md`** (its own first line: if `HANDOFF.md`/`STATE.md`/
memory disagree with it, `LIVE.md` wins). The freshness pass enforces that against the memory corpus.

**The pass (run it as a procedure, not a vibe):**
1. **Classify every memory** `DURABLE` (method/feedback/user) or `DATED` (project/frontier).
2. **DURABLE → leave the content; refresh only stale file:line citations** (the staleness reminder on
   each memory already warns these may be outdated — verify against current code before a citation is
   re-asserted as fact). The cognitive corral does not expire.
3. **DATED → reconcile against `LIVE.md`** and stamp each with exactly one tag in its header:
   - `CURRENT` — agrees with `LIVE.md`; keep.
   - `SUPERSEDED-BY: <memory/LIVE section>` — replaced; keep for history, but the body must open with
     the pointer so no reader takes it as live.
   - `HISTORICAL` — a closed arc; keep as record, flagged not-live.
   A DATED memory that makes a frontier claim and carries **no** tag is a freshness failure — fix it.
4. **Collapse to the pointer where possible:** prefer replacing a DATED frontier body with a one-line
   `see LIVE.md` pointer over maintaining a parallel frontier narrative that will drift again.

**Cadence (binding):** run the freshness pass (a) every push that changes the frontier, and (b)
**mandatorily before exporting the corpus to the local LLM**. The export must carry: the full DURABLE
corral + only `CURRENT` frontier (or `LIVE.md` itself) + **the allowed-lane clause** (see the
implementation instruction in "LEAVES ROOM FOR THE WORK" — non-droppable) — and never untagged DATED
claims.

**Constraint:** freshness checks **PROVENANCE** (is this claim still current?) and **HONESTY** (is the
staleness tagged?) — never **MERIT**. It does not decide whether a frontier claim is *right*, only
whether it is *current and tagged*. Reconciliation of substance stays with Charles + `LIVE.md`.

---

## ACCEPTANCE / CATCH-PROOF (required before declaring done)

Per `verifier-before-record`, prove each trigger actually fires — simulate the bad move, confirm the
reminder appears, then confirm it's silent when it should be:

1. **Agent trigger:** issue any `Task` call → the observing-or-targeting reminder must appear.
2. **Solver trigger:** run a harmless `Bash` echo containing `continuation_solve` → the bound-grid/
   chose-or-derived reminder must appear; an unrelated `Bash ls` → silent.
3. **Commit trigger:** run `git commit` on a throwaway change → the verifier reminder must appear.
4. **Part A:** open a fresh session, confirm the `## DRIVER TRIGGERS` section is in auto-loaded context.
5. **Merit-never audit:** re-read every reminder string — confirm none judges the *answer's shape*
   (no "is this a lump / the right mass / smooth enough"). If one does, rewrite it to demand honesty,
   not merit.
6. **Freshness:** confirm every DATED memory carries a `CURRENT` / `SUPERSEDED-BY` / `HISTORICAL` tag
   and that no untagged frontier claim contradicts `LIVE.md`. Confirm the trigger strings in Part A
   cite only CURRENT frontier (or no frontier). Confirm the local-LLM export gate refuses untagged
   DATED content.

Record the catch-proof (date, agent id) in a results doc and commit, same as any guard.

---

## SCOPE (state honestly when reporting completion)
- **Closes:** recognized forks (Part A, higher baseline firing) + the three structural tool-call
  moments (Part B, recognition-independent).
- **Does NOT close:** a silent fork with no trigger token and no tool-call signature. That residual
  is reached only by an external reader (the local-LLM cross-check / adversarial sub-agent), not by
  any wording or hook. This setup narrows the gap; it does not eliminate it.
