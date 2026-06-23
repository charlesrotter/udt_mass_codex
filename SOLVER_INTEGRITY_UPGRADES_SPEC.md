# SOLVER INTEGRITY UPGRADES — build spec for the CLI

**For:** Claude Code, working in the live repo. **From:** Charles.
**Goal:** stop silent shortcutting / SM-import / DOF-freezing at WRITE time, not via after-the-fact audit.
**Discipline:** build P1 first, verifier-before-record on each, commit script WITH a results doc. Do NOT
mark a box done until its acceptance test passes. Anti-hang: bound every run; never freeze a DOF to make a
test pass.

---

## P1 — PURITY HARNESS (build first)  →  `tests/test_solver_integrity.py`

A pytest suite that runs on every solver change. Four checks, each anchored to a real past bug:

- **Liveness** (the "off-diagonals built but dead" bug). For each off-diagonal + time DOF
  (g_rθ, g_rψ, g_θψ, g_tr, g_tθ, g_tψ): perturb it, assert ‖Δresidual‖ > tol. FAIL = that DOF is dead /
  the production residual is secretly diagonal.
- **Provenance lint** (the smuggled `kap8=0.05` bug). Scan the active operator/solver source for bare
  numeric literals; FAIL on any constant not carrying a tag `# DERIVED|POSTULATED|FREE|IMPORTED`. Pin the
  known ones: kap8 == 1 (DERIVED), X in the healthy negative window, a(φ)=e^{φ}.
- **Limit recovery** (standing, not one-off). Assert all: Schwarzschild→0; flat→<1e-13; ω→0 returns the
  static soliton bitwise; baseline a=−1 reproduces the prior P2 result bitwise; round→box-control.
- **Native-object guard** (the S³ Skyrme import). Assert the live matter path uses n=x/r (S²/π₂). FAIL if
  a `Θ(core)=mπ` Skyrme BC appears anywhere in the active operator.

**Acceptance:** suite green on current main; then deliberately reintroduce each of the 4 historical bugs in
a scratch branch and confirm the matching test goes RED. (Prove it catches them.)

---

## P2 — OPERATOR FROM THE ACTION  →  codegen + equality test

- One source-of-truth action file: `S = ∫√−g [ e^{2φ}R + X e^{2φ}(∂φ)² + e^{2φ}L_m ]`.
- Generate Einstein/EL/stress symbolically (sympy/autograd) FROM that action. Minimize hand-coded operator
  pieces — that's where every import crept in.
- **Acceptance:** a test asserting the generated operator == symbolic EL of the action to machine precision.
  Any hand-written operator term must either be deleted or justified with a `# DERIVED` tag + matching
  symbolic check.

---

## P3 — DISCIPLINE AS SKILLS  →  `.claude/skills/`

Factor the binding disciplines out of CLAUDE.md / HANDOFF.md into auto-loading SKILL.md files:

- `solver-first/SKILL.md` — the 4-question mismatch protocol (out? numeric? frozen DOF? unexplored?).
- `verifier-before-record/SKILL.md` — what a clean blind pass requires.
- `no-shortcuts/SKILL.md` — run P1 harness; anti-freeze / anti-import checklist.
- `completeness-map/SKILL.md` — the ten criteria + standing questions.

**Acceptance:** a fresh session auto-loads them; each is ≤1 screen; CLAUDE.md points to them instead of
inlining the full text.

---

## P4 — CROSS-MODEL VERIFY (load-bearing calls only)

- For native-vs-import classifications and any "must-quantize"-class verdict, add an option to run the blind
  verifier on a DIFFERENT model family (or a fresh zero-context instance), not another same-model subagent.
- **Acceptance:** documented command/flag; used on the next import classification; disagreement is logged,
  not silently dropped.

---

## P5 — SHRINK THE LIVE STATE

- New `LIVE.md`: current frontier + next action ONLY, ruthlessly pruned, nothing not true right now.
- Move the rest of STATE.md into dated archive/git. Kill the "READER NOTE / inoculation" banners once the
  live file is short enough not to need them.
- **Acceptance:** a fresh agent can act correctly from LIVE.md alone, without stale-next-step risk.

---

## ORDER
P1 → P2 → P3, then P4/P5 as bandwidth allows. P1 is the keystone: it converts every other discipline from
"agent remembered to check" into "the machine fails loudly." Report each as a short results doc; Charles
signs off canon.
