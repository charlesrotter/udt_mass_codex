# Structure hygiene protocol (process integrity — not physics truth)

**Date:** 2026-07-09 · **Charles:** make structure hygiene as bulletproof as possible; physics proof is **after** hygiene.  
**Status:** Working protocol for drivers + Charles. Complements CLAUDE.md; does not replace canonization.

---

## 0. Two different jobs (never conflate)

| Job | Question | Who decides |
|-----|----------|-------------|
| **Structure hygiene** | Is the work **honestly constructed**? (premises visible, joins tagged, no silent freeze, no merit-filter posing as derivation, re-runnable checks) | Process + machine gates + periodic audit + Charles challenge |
| **Physics proof** | Is nature like this? | Native derives, validators, data, **Charles canon** |

Hygiene can be **strong** while physics is still **open**.  
Strong hygiene **does not** prove physics. Weak hygiene makes “proofs” untrustworthy.

**Sand** = untagged choices + χ²-driven freezes + scaffolds treated as theory + claims wider than the slice.  
**Hygiene** = stop sand from accumulating under later work.

---

## 1. Defense in depth (four layers)

```text
L1  MACHINE (physics-blind)     — cannot lie about imports/tags presence; CAN be gamed with fake labels
L2  ARTIFACT CONTRACTS          — every result file carries a fixed header; missing fields = not banked
L3  PERIODIC SELF-AUDIT         — re-grade LIVE claims; demote over-promotion
L4  CHARLES + BLIND VERIFIER    — human merit later; zero-context attack on load-bearing rungs
```

No single layer is bulletproof. **Stack them.**

---

## 2. Layer L1 — machine (keep physics-blind)

**Already live (use, don’t reinvent):**

| Gate | File / skill | Checks |
|------|----------------|--------|
| Purity / no-shortcuts | `tests/test_solver_integrity.py`, skill `no-shortcuts` | Numeric imports, frozen DOF honesty |
| Solution-space | `tests/test_solution_space_gate.py`, skill `solution-space-not-imposition` | Provenance + tag **presence**; **never merit** |
| Corral triggers | CLAUDE.md DRIVER TRIGGERS + hooks | Pause tokens (easiest / cured / mechanism / …) |

**Rule:** Machine gates may only check **provenance** and **honesty of tags**, never “is the residual good / is it a lump.”

**Optional harden (when macro scripts stabilize):**  
Register macro observe scripts in a small allowlist + require a `# PREMISE_LEDGER:` block parseable by a dumb AST/regex test (tag strings present — not that tags are true).

---

## 3. Layer L2 — artifact contract (every banked note)

**Copy-paste template:** `HYGIENE_HEADER_TEMPLATE.md`  
**Machine gate:** `tests/test_hygiene_header.py` (run: `python3 -m pytest tests/test_hygiene_header.py`)  
Covered globs are listed in that test (macro/hyp trail first; expand as other domains adopt).

**No result is “banked” for later building unless the file has this header (or equivalent section):**

```markdown
## HYGIENE HEADER
- Date / mode: MAP | OBSERVE | PONDER | DERIVE
- Slice scope: (e.g. static SSS, chart origin, N=1580 full cov)
- Observing or targeting? OBSERVE | TARGET (if TARGET: stop or reframe)
- Premise ledger: table with columns  Item | Value/role | Tag (THEORY/DERIVED/POSTULATE/CHOSE/FREE/HABIT/SCAFFOLD) | Enters claim?
- What is NOT claimed:
- Comparator scaffolds: (e.g. LCDM Om=0.3 residual only — not target)
- Verifier status: NONE | SELF-SCRIPT | BLIND-PENDING | BLIND-PASS (id/date)
- Build-on grade: DEMO | LEAD | CONDITIONAL | BANKED-FOR-STRUCTURE
```

**Build-on grades (hygiene, not physics):**

| Grade | May later work treat it as…? |
|-------|------------------------------|
| **DEMO** | Illustration only; do not chain |
| **LEAD** | Hypothesis to explore; chain only with re-tag |
| **CONDITIONAL** | OK to chain **if** listed premises held |
| **BANKED-FOR-STRUCTURE** | Hygiene-clean structure step; still not Charles-physics-canon |

**Rule:** LIVE “NEXT” may only point to DEMO/LEAD as *work*, not as *foundation*, unless grade ≥ CONDITIONAL and premises restated.

---

## 4. Layer L3 — periodic structure audit (your request)

**Cadence (pick one and stick to it):**

| Trigger | Action |
|---------|--------|
| Every **major LIVE frontier change** | Mini-audit: premise re-grade of TOP claims |
| Every **~1–2 working days** of driver push, or end of arc | Full self-audit file (see template below) |
| Before **any** “bank / push / multi-probe claim” | Full audit + blind verifier on load-bearing rung |

**Full audit deliverable:** one file  
`simple_metric_session_self_audit_YYYY-MM-DD.md` (or domain prefix) containing:

1. Guardrail checklist (pass/partial/fail)  
2. Premise re-grade table (sold as vs honest tag)  
3. Scaffold inventory (LCDM, M_B, cuts, MS form, …)  
4. Over-promotions to **demote in LIVE this session**  
5. Build-on grades for each live claim  
6. Explicit **“do not build on”** list  

**Audit success criterion (hygiene):** LIVE and MEMORY match the demotions; no claim sits higher than its grade.

**Example already run:** `simple_metric_session_self_audit_2026-07-09.md`.

---

## 5. Layer L4 — human + blind verifier

| Role | Hygiene job |
|------|-------------|
| **Charles** | Catch frame smuggle early; canonize physics later; challenge “preferred after χ²” |
| **Blind verifier** | Zero-context: re-run scripts, attack load-bearing premise, hunt false passes (skill `verifier-before-record`) |
| **Driver** | Cannot self-certify BANKED-FOR-STRUCTURE without header + script re-run + (for high stakes) blind pass |

**Rule:** χ² improvement **never** upgrades CHOSE → DERIVED. Only a derive or Charles can.

---

## 6. Anti-patterns (automatic demotion)

If any of these appear, **max grade = LEAD** until fixed:

| Anti-pattern | Demote because |
|--------------|----------------|
| Join adopted after residual improved, uniqueness unproven | Imposition |
| “Prefer X” in LIVE without CHOSE tag | Over-promotion |
| LCDM/Om/H0 as fitness | Scaffold → target |
| MS/Einstein form used as “UDT proved mass” without GR-form flag | Principle 7 |
| Slice result stated as frame verdict | Whole-before-slice |
| “Cured / works / only thing left” | Corral trigger / false convergence |
| Half light or \(D_A=r/(1+z)\) “geometry” to restore SNe | Method relapse |
| Free \(D_A(r)\) fit surface | Quarantine breach (unless scoped hunt) |

---

## 7. Minimal workflow (every push)

```text
1. MAP  — premise ledger first (even 5 lines)
2. OBSERVE/DERIVE — bounded; tags on every pin
3. Write result with HYGIENE HEADER + build-on grade
4. Re-run listed scripts (commands in file)
5. If LIVE updates: demote anything audit would flag
6. Periodic full audit (L3) before chaining multi-probe claims
7. Physics proof / canon — only after hygiene + Charles
```

---

## 8. What “bulletproof as possible” means here

| Can approach strong | Cannot make absolute |
|---------------------|----------------------|
| No silent freezes | Driver always truthful about intent |
| No untagged joins | Fake tags that look honest |
| No χ²→theory promotion | Charles offline forever |
| Re-runnable numeric claims | Wrong physics with clean tags |
| Regular demotion of LIVE | Ignoring STRUCTURE_HYGIENE.md |

**Residual risk:** a sophisticated driver can still write pretty tags. Mitigation = **Charles challenge + blind verifier + machine physics-blind gates + short audit cadence**. That is the practical ceiling.

---

## 9. Relation to existing skills

| Skill | Hygiene role |
|-------|----------------|
| `solution-space-not-imposition` | No merit filters in gates |
| `verifier-before-record` | Blind attack before bank |
| `no-shortcuts` | Purity harness |
| `solver-first` | Mismatch ≠ new mechanism |
| `completeness-map` | One tile, not whole frame |

This file = **orchestration** of those for macro/hyp work and periodic audit.

---

## 10. One-line

**Structure hygiene = stacked, physics-blind process controls so later proofs sit on named premises and re-runnable checks — not on AI narrative sand; physics truth remains a separate step under Charles.**
