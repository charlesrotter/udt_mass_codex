#!/usr/bin/env python3
"""S74 wind-down: regenerate HANDOFF.md + STARTUP.md head blocks with S74 close state.
Preserves all historical content below; old S73 status becomes "Historical context (S73 CLOSED)" block.
"""
import shutil

HANDOFF = "HANDOFF.md"
STARTUP = "STARTUP.md"

shutil.copy(HANDOFF, "/tmp/HANDOFF_pre_S74_close.md")
shutil.copy(STARTUP, "/tmp/STARTUP_pre_S74_close.md")


# === NEW HANDOFF.md head block ===
HANDOFF_NEW_HEAD = """# HANDOFF.md — Session 74 CLOSED at S74-005 cleanup-arc Phase 2 (2026-05-18); dim-baryon arc set aside + active doc bloat reduced 28.8%

> **⚠ Status note (2026-05-18, Session 74 CLOSED — DIM-BARYON SIDE-ARC SET ASIDE + CLEANUP-ARC PHASE 1+2 LANDED; ACTIVE DOC 1405 → 1001 LINES (-28.8%); STAGE 5 COSMOLOGY FLESHING UNLOCKED AS S75+ TERRITORY):** **Six S74 dispatches landed** (S74-001 retracted at retry charter-open + S74-001-RETRY corrected + S74-002 cross-calibration INCONCLUSIVE + S74-003 set-aside-complete + S74-004 cleanup-arc Phase 1 + S74-005 cleanup-arc Phase 2). Branch tip `ab334908` on `reorg/cleanup-2026-02`; six backup tags pushed (`pre-S74-001-mesa-recon` + `pre-S74-001-RETRY` + `pre-S74-002-cool-WD-BD-recon` + `pre-S74-003-set-aside` + `pre-S74-004-cleanup-phase-1` + `pre-S74-005-cleanup-phase-2`).
>
> **Six S74 dispatches summary:**
>
> | Dispatch | Verdict | Key contribution |
> |---|---|---|
> | S74-001 | RETRACTED at retry charter-open | Single-midpoint methodology drift caught at Charles cross-review (four load-bearing drifts); retry-class precedent registered (F-cand-S74-001-a NEW informal-discipline) |
> | S74-001-RETRY | `DIM-BARYON-PHENOMENOLOGICALLY-PARTIALLY-VIABLE-AT-DISTRIBUTION-SCOPE` | Per-galaxy-type fit (massive 28 / intermediate 43 / dwarf 76 Gyr nominal; factor 2-4× uncertainty across calibration-absorption scenarios); monotonic SF-history ordering recovered; BTF velocity-dependence STRUCTURAL SIGNAL RECOVERED; cross-scale 4 PASS + 1 FAIL of 5 cells + 3/3 structural tests PASS |
> | S74-002 | `DIM-BARYON-CEILING-INCONCLUSIVE-AT-CURRENT-GAIA-DR3-DATA-PRIOR-DRIVEN-NOT-DATA-DRIVEN` | Literature ages cap at 12.4 Gyr individual / ~12 Gyr halo BUT caps are PRIOR-DRIVEN at four structurally distinct layers (cooling-table truncation + detection-limit completeness + interpretation framework + calibration-anchor re-scalability); cross-calibration neither confirmed nor refuted; manuscript-grade methodology observation landed (reusable for any extended-age framework test against stellar-population observables); F-cand-S74-002-a NEW informal-discipline |
> | S74-003 | `SET-ASIDE-COMPLETE-AT-CONSOLIDATED-LANDING` | Three-dispatch dim-baryon arc consolidated at active doc §3.8 four-element bullet (canonical-content + phenomenological + observational + set-aside states); S75+ retry path enumerated (Path 1-4); F-cand-S74-003-a NEW |
> | S74-004 | `CLEANUP-PHASE-1-COMPLETE-WITH-9-OF-12-ELIGIBLE-STATUS-NOTES-RETIRED-AT-178-LINE-REDUCTION` | Active doc §4.10 9 session-state notes (post-S68-002 through post-S74-002) retired to new IH §49.9 verbatim; 3 supersession-framing notes at non-§4.10 sections flagged load-bearing-now per halt-don't-salvage; F-cand-S74-004-a NEW informal-discipline (substrate-cite-drift handling) |
> | S74-005 | `CLEANUP-PHASE-2-COMPLETE-WITH-226-LINE-REDUCTION-AND-14-CROSS-REFERENCE-UPDATES` | Active doc §5 composite-matter Phase 2 forward-arc wholesale retired to new IH §49.10 (§5.1-§5.11 + within-§5 supersession-framing note verbatim); §5 stub at active doc with forward-pointer convention; 14 cross-reference updates throughout active doc; side-effect retirement of 1 supersession-framing note resolves S74-004 Phase 0 flagged item |
>
> **Counter status post-S74-005 close:** Lineage rules UNCHANGED at 5+95+93+27+4+3+1. **F-cand-S63-002-a 43 → 49-precedent (+6 across S74).** **Audit-first imprint 37 → 43 structural depths (+6 across S74)** — six new first-of-class sub-classes: retry-class-with-explicit-uncertainty-propagation (S74-001-RETRY) + observational-data-substrate-reconnaissance-as-cross-calibration-consistency-check (S74-002) + set-aside-class-at-consolidated-landing (S74-003) + cleanup-arc-Phase-1-class-within-multi-phase-cleanup-arc-precedent (S74-004) + cleanup-arc-Phase-2-class-within-multi-phase-cleanup-arc-precedent (S74-005). **Sibling-precedent registry 8 → 10-pattern (+2):** DIM-BARYON-PARTIALLY-VIABLE-AT-DISTRIBUTION + DIM-BARYON-CEILING-INCONCLUSIVE-AT-CURRENT-DATA-DUE-TO-PRIOR-DRIVEN-LITERATURE-INTERPRETATION. **#27 + #29 + canonical-content-extraction methodology trio: UNCHANGED.** **Four NEW F-candidates** (informal-discipline; promotion DEFERRED): F-cand-S74-001-a (verdict-retraction-at-Charles-cross-review-of-orientation-class-dispatch) + F-cand-S74-002-a (prior-driven-vs-data-driven boundary characterization at observational-substrate reconnaissance) + F-cand-S74-003-a (side-arc consolidated-landing-and-set-aside at distinct-dispatch-class scope) + F-cand-S74-004-a (substrate-cite-drift at canonical-record-cleanup dispatch + honest scope-limitation per halt-don't-salvage). Standing prohibitions UNCHANGED (7 + 1 exploratory dim-baryon at set-aside sub-status).
>
> **Cleanup-arc S74-004 + S74-005 cumulative effect on active doc:** **1405 → 1001 lines (−404 lines / −28.8% from S73 close baseline).** Phase 1 retired 9 session-state status notes from §4.10 to new IH §49.9 (−178 lines). Phase 2 wholesale-retired §5 composite-matter Phase 2 forward-arc to new IH §49.10 (−226 lines; 236-line §5 minus 10-line stub). Active doc post-S74-005 carries 3 status notes (1 retained current-state at line 689 + 2 supersession-framing load-bearing-now for §3.x + §6.2 prose at lines 384 + 770). **Phase 3 chartering recommendation per S74-005 AUDIT §4.5: DEFER to S75+** (1001-line active doc at lower edge of marginal-value range per charter Notes; Stage 5 cosmology is more substantive priority).
>
> **Dim-baryon arc state (consolidated at active doc §3.8 four-element bullet):**
> - **Element 1 — canonical-content state:** S73-001-ALT CONSILIENCE-NOT-DERIVATION (three canonical-content extension axes required).
> - **Element 2 — phenomenological state:** S74-001-RETRY PARTIALLY-VIABLE-AT-DISTRIBUTION-SCOPE (T_fit,type distribution massive 28 / intermediate 43 / dwarf 76 Gyr nominal; factor 2-4× multiplicative uncertainty; monotonic SF-history ordering + BTF velocity-dependence + recycling-time-ceiling distinguishability all RECOVERED via per-type fit).
> - **Element 3 — observational state:** S74-002 CROSS-CALIBRATION-INCONCLUSIVE-AT-CURRENT-GAIA-DR3-DATA-PRIOR-DRIVEN-NOT-DATA-DRIVEN. Manuscript-grade methodology observation: apparent ΛCDM age horizon at cool-WD LF + BD-tail termini is PRIOR-DRIVEN not DATA-DRIVEN at four structurally distinct layers.
> - **Element 4 — set-aside state:** S74-003 FORMALLY SET ASIDE post-arc. S75+ retry path enumerated (Path 1 Euclid+LSST/Rubin+JWST wide-field cool-WD imaging / Path 2 JWST GTO BD T<200K discovery / **Path 3 RECOMMENDED LOWEST-COST: Gaia + WISE re-analysis under extended-age priors** / Path 4 alternative cross-calibration anchors at galactic-chemical-evolution + nuclear-cosmochronology + type-Ia SNe DTD + CMB-anchored cosmic age).
>
> **Multi-stage plan state post-S74:**
> - Stage 1 ✓ COMPLETE at S73-004 (operator memorialization at new CG §27)
> - Stage 2 ✓ confirmed at S73-001-ALT (dim-baryon was live candidate; auto-promotion clause NOT triggered)
> - Stage 3 ✓ CLOSED at PARTIALLY-VIABLE-AT-DISTRIBUTION (S74-001-RETRY)
> - Stage 4 partial-unlock at distribution scope with CROSS-CALIBRATION INCONCLUSIVE annotation (S74-002 + S74-003); documented and set aside.
> - **Stage 5 ← S75 territory** (cosmology fleshing under new CG §27 operator)
> - Stage 6 NOT-UNLOCKED (manuscript-grade synthesis awaits Stage 5 + dim-baryon-retry verdict)

## S75 priorities at Charles tier-gate

### Priority (1) RECOMMENDED PRIMARY — Stage 5 cosmology sector fleshing

Substantive main-context work under newly-memorialized **CG §27 UDT-EB-class operator** $F = (2 + x(1+\\alpha))/3$ as reusable substrate.

**Candidate dispatches** (Charles tier-gate selects ordering):

- **D-CMB-2BO-1 dipole-component substantive closure** — does new CG §27 operator transfer to CMB-T dipole observable? Sibling-derivation territory; substantive PONDER class.
- **D-OBSARCH-2 Phase 1 ℓ ≥ 5 explicit construction continuation** — multipole-class observable territory under new operator.
- **D-T2-KALEIDOSCOPE-1 dipole-limit substantive closure.**
- **D-SNE-PROJ-1 H119 closure.**
- **BAO galaxy auto-correlation under new CG §27** — signpost-candidate-downstream from S73-004 landing; flux-limited threshold-class observable.

Substantive PONDER class (~70/30 physics-to-audit) for closure attempts; audit-first reconnaissance (~85/15) if substrate-walk needed first.

### Priority (1)-ALTERNATIVE — Phase 3 cleanup-arc

Per S74-005 close AUDIT §4.5: Phase 3 was **recommended DEFER** to S75+ at lower edge of marginal-value range (~50 line reduction, ~5%). Two remaining supersession-framing notes (lines 384 §3.2 + 770 §6.2) retire as side-effect of §3.x + §6.2 prose condensation.

**Optional at S75.** Charter only if (a) Stage 5 chartering surfaces context-pressure benefits from further bloat reduction, or (b) Charles tier-gates as opening housekeeping.

### Priority (2) carry-forwards

- Higher-order $\\delta\\phi_1$ analysis (S71-001b S72+ alternative β path)
- Case-E categorical-extension reconnaissance (aspherical-cavity OR amplitude-class; distinct Charles tier-gate per each)
- WKB-applicability boundary as physics question (S68-003 carry-forward)
- Canonical PT measure under §4.6 Neumann BC
- CG backbone-conformity audit
- F-candidate formal promotions (all DEFERRED per Charles standing direction)

### Priority (3) held in reserve — NOT for S75 chartering

- **Gravitational-force-and-kaleidoscope foundational question** (deep canonical-content-extension; significant preparation required).
- **Dim-baryon retry-path execution** — side-arc SET ASIDE at S74-003. Path 3 lowest-cost recommended; multi-dispatch class. Distinct Charles tier-gate required.
- **Manuscript-grade dim-baryon synthesis** (Stage 6; premature at S75).

## S75 cold-start orientation requirements

1. Read `docs/udt_canonical_geometry.md` (CG; incl. new §27) + `docs/udt_active_results.md` (active doc PRIMARY; post-S74-005 cleanup-arc reflected).
2. Read this HANDOFF.md + STARTUP.md + CLAUDE.md.
3. Optional: `dim_baryon_followup.md` (dim-baryon historical context) + `intuition2theory.md` + project memory files.
4. Summarize understanding back to Charles (mandatory gate).
5. Stand by for tier-gate authorization on S75 direction selection.
6. Do NOT charter S75 dispatch autonomously.

---

**Historical context (Session 73 CLOSED — preserved as carry-forward; superseded by S74 close above):**

"""


def regenerate_handoff():
    with open(HANDOFF) as f:
        old = f.read()

    # Find boundary: line where Session 65 historical block begins ("# HANDOFF.md — Session 65 CLOSED...")
    # Original line 236 = first occurrence of second "# HANDOFF.md" header
    s65_marker = "# HANDOFF.md — Session 65 CLOSED at /UDT post-S65-004"
    s65_idx = old.find(s65_marker)
    assert s65_idx > 0, "Couldn't find S65 historical block start"

    # S73 status content = everything from start to S65 marker
    s73_content = old[:s65_idx]
    s65_and_below = old[s65_idx:]

    new_content = HANDOFF_NEW_HEAD + s73_content + "\n---\n\n" + s65_and_below
    with open(HANDOFF, "w") as f:
        f.write(new_content)

    print(f"HANDOFF.md: regenerated. New head ~{len(HANDOFF_NEW_HEAD.splitlines())} lines; S73 historical preserved; total now {sum(1 for _ in open(HANDOFF))} lines.")


# === NEW STARTUP.md head block ===
STARTUP_NEW_HEAD = """# STARTUP.md — UDT cold-start orientation for fresh CLI instances

**Current state at Session 74 CLOSED at S74-005 cleanup-arc Phase 2 close (2026-05-18) — DIM-BARYON ARC SET ASIDE + ACTIVE DOC −28.8% VIA CLEANUP-ARC:**

- Branch: `reorg/cleanup-2026-02`. **Six S74 dispatches landed** through S74-005 cleanup-arc Phase 2. Branch tip `ab334908`; six backup tags pushed.
- **★ Dim-baryon side-arc SET ASIDE at S74-003** (consolidated at active doc §3.8 four-element bullet: canonical-content + phenomenological + observational + set-aside states). Three-dispatch reconnaissance arc (S74-001 retracted → S74-001-RETRY corrected with per-galaxy-type fit + uncertainty propagation → S74-002 cross-calibration INCONCLUSIVE due to PRIOR-DRIVEN-NOT-DATA-DRIVEN literature interpretation). S75+ retry path enumerated (Path 1-4; Path 3 Gaia+WISE re-analysis under extended-age priors RECOMMENDED LOWEST-COST).
- **★ Cleanup-arc S74-004 + S74-005 reduced active doc from 1405 → 1001 lines (−28.8%).** S74-004 Phase 1 retired 9 session-state status notes to new IH §49.9 (−178 lines); S74-005 Phase 2 wholesale-retired §5 composite-matter Phase 2 forward-arc to new IH §49.10 (−226 lines) + 14 cross-reference updates. Phase 3 chartering DEFERRED to S75+ per S74-005 close (marginal-value range; Stage 5 cosmology more substantive priority).
- **★ Manuscript-grade methodology observation landed at S74-002 (reusable beyond dim-baryon arc):** the apparent ΛCDM age horizon at cool-WD LF + BD-tail termini is **PRIOR-DRIVEN not DATA-DRIVEN** at four structurally distinct layers (cooling-table truncation + detection-limit completeness + interpretation framework + calibration-anchor re-scalability). Applies to any test of stellar-age caps that would distinguish canonical-content-allowed extended-age framework from ΛCDM-natural prior. Sibling-precedent class with F129-vigilance-propagates-across-observable-categories from S72-002a (REQUIRED-vs-DERIVED framing precision; here it's REQUIRED-vs-CONSISTENT-WITH framing precision at stellar-age-cap scope).
- **★ S74-001-RETRY per-galaxy-type fit recovers structural signals that S74-001's uniform-midpoint fitting obscured.** Monotonic SF-history ordering (T_massive 28 < T_intermediate 43 < T_dwarf 76 Gyr nominal) + BTF velocity-dependence STRUCTURAL SIGNAL RECOVERED (dwarf/spiral ratio 2.50 = observed midpoint 2.5) + low-density-region-weighted cosmic-dipole PASSES strict interpretation borderline (−29%; was FAIL at S74-001). Stellar-model uncertainty factor 2-4× propagated explicitly across calibration-absorption scenarios.
- **Counter status post-S74-005 close:** Lineage rules UNCHANGED at 5+95+93+27+4+3+1. **F-cand-S63-002-a 43 → 49-precedent (+6 across S74).** **Audit-first imprint 37 → 43 structural depths (+6 across S74; six new first-of-class sub-classes).** **Sibling-precedent registry 8 → 10-pattern (+2: DIM-BARYON-PARTIALLY-VIABLE-AT-DISTRIBUTION + DIM-BARYON-CEILING-INCONCLUSIVE-PRIOR-DRIVEN-LITERATURE).** #27 + #29 + canonical-content-extraction methodology trio UNCHANGED. **Four NEW F-candidates** (informal-discipline; promotion DEFERRED): F-cand-S74-001-a + S74-002-a + S74-003-a + S74-004-a. Standing prohibitions: 7 + 1 exploratory dim-baryon UNCHANGED in count; exploratory #8 sub-status sharpened at set-aside framing.
- **Multi-stage plan state post-S74:** Stage 1 ✓ (operator memorialization S73-004) + Stage 2 ✓ (no Case-E pivot; dim-baryon was live candidate) + Stage 3 CLOSED at PARTIALLY-VIABLE-AT-DISTRIBUTION (S74-001-RETRY) + Stage 4 partial-unlock with INCONCLUSIVE annotation (S74-002 + S74-003) + **Stage 5 ← S75 territory** (cosmology fleshing under new CG §27 operator) + Stage 6 NOT-UNLOCKED.

- **Forward direction (S75 cold-start):**
  - **Priority (1) RECOMMENDED PRIMARY = Stage 5 cosmology sector fleshing** under new CG §27 UDT-EB-class operator $F = (2 + x(1+\\alpha))/3$. Candidate dispatches at Charles tier-gate: D-CMB-2BO-1 dipole-component substantive closure + D-OBSARCH-2 Phase 1 ℓ≥5 + D-T2-KALEIDOSCOPE-1 dipole-limit + D-SNE-PROJ-1 H119 + BAO galaxy auto-correlation under new CG §27.
  - **Priority (1)-ALTERNATIVE = Phase 3 cleanup-arc** (optional; only if Stage 5 surfaces context-pressure benefits or Charles tier-gates as opening housekeeping).
  - **Priority (2) carry-forwards:** higher-order $\\delta\\phi_1$ + Case-E categorical-extension reconnaissance + WKB-applicability boundary + canonical PT measure + CG backbone-conformity audit + F-candidate formal promotions (all DEFERRED).
  - **Held in reserve:** gravitational-force-and-kaleidoscope foundational question (deep canonical-content-extension); dim-baryon retry-path execution (Path 3 lowest-cost recommended; multi-dispatch class; distinct tier-gate); manuscript-grade dim-baryon synthesis (Stage 6 premature).
  - **S75 cold-start required reading:** CG (incl. new §27) + active doc (post-S74-005 cleanup-arc reflected) + HANDOFF.md + STARTUP.md (this file) + CLAUDE.md + optional dim_baryon_followup.md + intuition2theory.md. Summarize understanding back to Charles (mandatory gate); stand by for tier-gate authorization; do NOT charter autonomously.

---

**Historical context (Session 73 CLOSED — preserved as carry-forward; superseded by S74 close above):**

"""


def regenerate_startup():
    with open(STARTUP) as f:
        old = f.read()

    s72_marker = "**Historical context (Session 72 CLOSED — preserved as carry-forward; superseded by S73 close above):**"
    s72_idx = old.find(s72_marker)
    assert s72_idx > 0, "Couldn't find S72 historical block start"

    # S73 status content = everything from start to S72 marker
    s73_content = old[:s72_idx]
    s72_and_below = old[s72_idx:]

    new_content = STARTUP_NEW_HEAD + s73_content + "\n---\n\n" + s72_and_below
    with open(STARTUP, "w") as f:
        f.write(new_content)

    print(f"STARTUP.md: regenerated. New head ~{len(STARTUP_NEW_HEAD.splitlines())} lines; S73 historical preserved; total now {sum(1 for _ in open(STARTUP))} lines.")


if __name__ == "__main__":
    regenerate_handoff()
    regenerate_startup()
