#!/usr/bin/env python3
"""S74-005 cleanup-arc Phase 2: §5 composite-matter wholesale retirement.

- Extracts active doc §5 (lines 758-993, including supersession-framing note at 760).
- Appends new IH §49.10 sub-section with verbatim §5 preservation.
- Replaces active doc §5 with stub (forward-pointer to IH §49.10).
- Applies forward-pointer cross-reference updates throughout active doc.
- Preserves historical-narrative references at dispatch coverage tables (S64-002+).
"""
import shutil

ACTIVE = "docs/udt_active_results.md"
IH = "docs/udt_investigation_history.md"

shutil.copy(ACTIVE, "/tmp/active_pre_S74_005.md")
shutil.copy(IH, "/tmp/ih_pre_S74_005.md")

with open(ACTIVE) as f:
    ad = f.readlines()
with open(IH) as f:
    ih = f.readlines()

# Pre-edit verification
assert ad[757].startswith("## §5. Composite-matter Phase 2 forward-arc"), f"Expected §5 header at 758: {ad[757][:60]!r}"
assert ad[993].startswith("## §6. Predictive scorecard"), f"Expected §6 at 994: {ad[993][:60]!r}"
# Extract §5 content: lines 758-993 (1-indexed) = indices 757-992 (0-indexed)
section5 = ad[757:993]
assert len(section5) == 236, f"§5 should be 236 lines, got {len(section5)}"

# Build IH §49.10 section content
section_header = """### §49.10 [S74-005 cleanup-arc Phase 2: active doc §5 composite-matter Phase 2 forward-arc wholesale retirement] (originally active doc §5.1 through §5.11 + supersession-framing status note within §5, Sessions 62-67)

> **S74-005 cleanup-arc Phase 2 retirement (2026-05-18; commit on `reorg/cleanup-2026-02`).** Active doc §5 composite-matter Phase 2 forward-arc retired wholesale to this IH §49.10 sub-section. Per Trimble S72 bloat.md cleanup-arc diagnostic + S74-005 charter §1, Phase 2 of three-phase active-doc bloat reduction (sibling to S74-004 Phase 1 §49.9 retirement). Active doc §5 substantive territory **STRUCTURALLY EXHAUSTED at S67-001** per S67-001 reconnaissance (all three §5.11 candidates NOT-ADMISSIBLE) + S67-002 audit (§241-BASIS-INTACT dual-support reinforcement); banner self-flagged at §5.11 pre-retirement. Retirement-ready per dispatch §5.11 banner.
>
> **Retired here:** active doc §5 wholesale (§5.1 through §5.11 + supersession-framing status note at active-doc line 760 within §5 [post-S74-004 line attribution]).
>
> **Replaced at active doc:** §5 stub (single paragraph) forward-pointing to this IH §49.10 sub-section. §5.1–§5.11 sub-section identifiers preserved at IH §49.10 with original numbering scheme (sub-sections appear verbatim below at original §5.1, §5.2, ..., §5.11 attribution; readers of active doc following §5.x cross-references resolve here).
>
> **Side-effect retirement (S74-004 Phase 0 flagged item):** the supersession-framing status note within §5 at active-doc line 760 [post-S74-004 line attribution] retired AS PART OF §5 wholesale retirement. Its interpretive-guard role (directing readers AWAY from stale S66-004 "singular substantive forward direction" framing in §5.x prose) becomes moot when underlying §5.x prose retires. The remaining 2 supersession-framing status notes at active doc (lines 384 §3.2 area + 996 §6.2 area pre-S74-005) carry forward at active doc, flagged at S74-004 Phase 0 for Phase 3 retirement when underlying §3.x + §6.2 prose condenses (separate Charles tier-gate at S74-006 or carry-forward to S75+).
>
> **Phase 3 cleanup-arc** (lower-priority §3.x + §6.2 condensation; would retire the remaining 2 supersession-framing notes as side-effect): chartered separately at Charles tier-gate post-S74-005 close. Decision at S74-005 close re: whether Phase 3 chartering is worth doing at S74-006 vs carry-forward to S75+ (depending on post-S74-005 active doc line-count + main-context bandwidth needs for Stage 5 cosmology pivot).

> **Verbatim preservation of active doc §5 follows.** Original active-doc line attribution at retirement-execution time: §5 heading at line 758 (post-S74-004) through §5.11 closing at line 993 (just before §6 header at line 994). Total 236 lines preserved.

---

"""

ih_insert = list(section_header.splitlines(keepends=True))
ih_insert += section5
if not ih_insert[-1].endswith("\n"):
    ih_insert[-1] += "\n"
ih_insert += ["\n"]

# Insert into IH at appropriate point (before existing --- separator at line 7711 = idx 7710)
# Pre-verify the separator location
sep_idx = None
for i in range(7700, 7720):
    if ih[i].strip() == "---":
        sep_idx = i
        break
assert sep_idx is not None, "Couldn't find --- separator after §49.9"
# Pre-verify: ih[sep_idx] is ---, ih[sep_idx+1] is blank, ih[sep_idx+2] is "Session 25 (Chandra)..."
assert ih[sep_idx].strip() == "---"
assert ih[sep_idx+2].startswith("Session 25 (Chandra)") or ih[sep_idx+1].startswith("Session 25 (Chandra)"), f"Pattern check: ih[{sep_idx+1}]: {ih[sep_idx+1][:60]!r}, ih[{sep_idx+2}]: {ih[sep_idx+2][:60]!r}"

# Insert §49.10 BEFORE the --- separator
new_ih = ih[:sep_idx] + ih_insert + ih[sep_idx:]
with open(IH, "w") as f:
    f.writelines(new_ih)

# Build active doc §5 stub
stub = """## §5. Composite-matter Phase 2 forward-arc — STRUCTURALLY EXHAUSTED AT S67-001 (retired to IH §49.10 at S74-005)

Composite-matter Phase 2 forward-arc (S62–S67) retired wholesale to **IH §49.10** at S74-005 cleanup-arc Phase 2 dispatch (commit on `reorg/cleanup-2026-02`; verbatim preserved at IH with original §5.1–§5.11 numbering scheme). **Substantive territory at canonical content STRUCTURALLY EXHAUSTED at S67-001** per S67-001 reconnaissance (all three §5.11 canonical-content extension candidates NOT-ADMISSIBLE: C1 alternative non-traceless matter `NOT-ADMISSIBLE-PER-FOUNDATIONAL-METRIC-DERIVATION-CHAIN`; C2 Yukawa + C3 derivative cross-coupling `NOT-ADMISSIBLE-AT-CANONICAL-ACTION-CONTENT-WITHOUT-IDENTIFIABLE-DERIVATION-CHAIN`) + S67-002 §241 multi-sector architecture basis audit (§241-BASIS-INTACT dual-support reinforcement; canonical-action-architecture layer + Form-T spinor-bilinear-structure layer; operationally independent given canonical-tetrad substrate). **Categorical-extension territory** narrowed per SE-S67-001-2 to (α) revising §1.0 metric-derivation chain or (β) revising canonical input set / sector-architecture; both require separate Charles tier-gate with substantive case for revising foundational structure. Not active forward-direction at S74+.

**Forward-pointer convention:** all §5.x cross-references throughout active doc + CG resolve at **IH §49.10** sub-sections (§5.1 through §5.11) verbatim. For full content of §5.1 (operational scope) + §5.2 (canonical translation-consistency violation Δ formula at archived VR §255) + §5.3 (four-mechanism reconnaissance verdict) + §5.4 (forward-direction territory revised post-S66-003) + §5.5 (L1 MD joint BC derivation DERIVED at S65-001) + §5.6 (L3 MF closure mechanism STRUCTURAL-FINDING at S65-003) + §5.7 (L2 MC-refined inherited pre-emption) + §5.8 (L4 MB-refined STRUCTURAL-FINDING at S66-003) + §5.9 (CG §8.5.4 vs §8.5.5 source-formula label distinction; F138-5) + §5.10 (forward-arc disposition) + §5.11 (canonical-content extension territory STRUCTURALLY EXHAUSTED), see IH §49.10.

**S74+ forward direction:** composite-matter Phase 2 is NOT live forward-direction at S74+. Dim-baryon side-arc was set aside at S74-003; Stage 5 cosmology fleshing recommended as next substantive territory (D-CMB-2BO-1 + D-T2-KALEIDOSCOPE-1 + D-OBSARCH-2 Phase 1 + D-SNE-PROJ-1 H119 + BAO under new CG §27); see active doc §4.10 post-S74-003 retained status note for substantive arc continuation candidates.

---

"""

stub_lines = list(stub.splitlines(keepends=True))

# Replace lines 758-993 (1-indexed) = ad[757:993] with stub
# Keep ad[:757] (everything before §5 header) + stub + ad[993:] (from §6 onwards)
new_ad = ad[:757] + stub_lines + ad[993:]

# Apply forward-pointer cross-reference updates
# Strategy: bulk replace specific forward-pointer texts with IH §49.10 prefix
# Preserve historical-narrative references at dispatch coverage tables

def update_line(line):
    """Apply forward-pointer cross-reference updates. Returns updated line."""
    original = line

    # §0 TOC reference
    if "Composite-matter Phase 2 forward-arc (§5 — pending S64-005)" in line:
        line = line.replace(
            "Composite-matter Phase 2 forward-arc (§5 — pending S64-005)",
            "Composite-matter Phase 2 forward-arc (§5 stub at active doc; full content retired to IH §49.10 at S74-005)"
        )

    # §1.4 cross-ref list with §5.5 + §5.6
    if "§5.5 L1 forward-arc + §5.6 L3 forward-arc (substantive Phase 2 dispatches select per coupling regime)" in line:
        line = line.replace(
            "§5.5 L1 forward-arc + §5.6 L3 forward-arc (substantive Phase 2 dispatches select per coupling regime)",
            "IH §49.10 §5.5 L1 forward-arc + IH §49.10 §5.6 L3 forward-arc (substantive Phase 2 dispatches select per coupling regime; §5 retired to IH §49.10 at S74-005)"
        )

    # Supersession-framing note at line 384: trim §5.x scope and redirect §5.11 cross-ref
    if "Throughout §3.2 + §3.8 + §5.4 + §5.5 + §5.6 + §5.8 + §6.2.5 below" in line:
        line = line.replace(
            "Throughout §3.2 + §3.8 + §5.4 + §5.5 + §5.6 + §5.8 + §6.2.5 below",
            "Throughout §3.2 + §3.8 + §6.2.5 below (§5.4 + §5.5 + §5.6 + §5.8 retired to IH §49.10 at S74-005)"
        )
        line = line.replace(
            "Current status per §5.11 + §5.10 (S67-003/S67-005 canonical-record-edits)",
            "Current status per IH §49.10 §5.11 + §5.10 (S67-003/S67-005 canonical-record-edits; retired to IH §49.10 at S74-005)"
        )

    # §3.2 line "(full canonical content at §5 below)"
    if "(full canonical content at §5 below)" in line:
        line = line.replace(
            "(full canonical content at §5 below)",
            "(full canonical content at IH §49.10; active doc §5 retired at S74-005)"
        )

    # §3.2 line "superseded S65-004 + S64-005 framings per §5.4"
    if "superseded S65-004 + S64-005 framings per §5.4)" in line:
        line = line.replace(
            "superseded S65-004 + S64-005 framings per §5.4)",
            "superseded S65-004 + S64-005 framings per IH §49.10 §5.4)"
        )

    # §3.2 line "canonical-content extension territory (§5.11) **singular substantive forward direction within composite-matter Phase 2 scope**"
    if "canonical-content extension territory (§5.11) **singular substantive forward direction" in line:
        line = line.replace(
            "canonical-content extension territory (§5.11) **singular substantive forward direction",
            "canonical-content extension territory (IH §49.10 §5.11) **singular substantive forward direction"
        )

    # §3.2 D-COMP-MATTER-L3 cell: "the κGF channel-matching at §5.6 is the same canonical quantity"
    if "the κGF channel-matching at §5.6 is the same canonical quantity" in line:
        line = line.replace("the κGF channel-matching at §5.6 is the same canonical quantity", "the κGF channel-matching at IH §49.10 §5.6 is the same canonical quantity")

    # §3.2 D-COMP-MATTER-L4 cell: "§5.8 below (S66-004 rewrite); §5.11 (canonical-content extension territory promoted"
    if "§5.8 below (S66-004 rewrite); §5.11 (canonical-content extension territory promoted" in line:
        line = line.replace(
            "§5.8 below (S66-004 rewrite); §5.11 (canonical-content extension territory promoted",
            "IH §49.10 §5.8 (S66-004 rewrite); IH §49.10 §5.11 (canonical-content extension territory promoted"
        )

    # §3.2 narrative line "all three §5.11 enumerated canonical-content extension candidates"
    if "all three §5.11 enumerated canonical-content extension candidates" in line:
        line = line.replace(
            "all three §5.11 enumerated canonical-content extension candidates",
            "all three IH §49.10 §5.11 enumerated canonical-content extension candidates"
        )

    # §3.2 narrative "STRUCTURALLY EXHAUSTED at S67-001** (per §5.11 revised label)"
    if "STRUCTURALLY EXHAUSTED at S67-001** (per §5.11 revised label)" in line:
        line = line.replace(
            "STRUCTURALLY EXHAUSTED at S67-001** (per §5.11 revised label)",
            "STRUCTURALLY EXHAUSTED at S67-001** (per IH §49.10 §5.11 revised label)"
        )

    # §3.8 line 465: D-COMP-MATTER forward-direction territory: "canonical-content extension territory (§5.11) promoted at S66-004"
    if "canonical-content extension territory (§5.11) promoted at S66-004 from parallel candidate" in line:
        line = line.replace(
            "canonical-content extension territory (§5.11) promoted at S66-004 from parallel candidate",
            "canonical-content extension territory (IH §49.10 §5.11) promoted at S66-004 from parallel candidate"
        )

    # §3.8 line 466: "See §6.2.2 + §5.6 for full disposition"
    if "See §6.2.2 + §5.6 for full disposition" in line:
        line = line.replace(
            "See §6.2.2 + §5.6 for full disposition",
            "See §6.2.2 + IH §49.10 §5.6 for full disposition"
        )

    # §3.8 line 467: "See §5.8 for full derivation" + "canonical-content extension territory (§5.11) is singular"
    if "See §5.8 for full derivation" in line:
        line = line.replace(
            "See §5.8 for full derivation",
            "See IH §49.10 §5.8 for full derivation"
        )
    if "canonical-content extension territory (§5.11) is singular substantive forward direction" in line:
        line = line.replace(
            "canonical-content extension territory (§5.11) is singular substantive forward direction",
            "canonical-content extension territory (IH §49.10 §5.11) is singular substantive forward direction"
        )

    # §4.10 stub-pointer (S74-004 line 717): update wording to reflect Phase 2 landed
    if "Phase 2 (§5 composite-matter wholesale retirement) + Phase 3" in line:
        line = line.replace(
            "Phase 2 (§5 composite-matter wholesale retirement) + Phase 3 (§3.x/§6.2 supersession-framing notes; retire when underlying prose retires) deferred to subsequent dispatches at Charles tier-gate.",
            "Phase 2 §5 composite-matter wholesale retirement LANDED at S74-005 (see IH §49.10). Phase 3 (§3.x/§6.2 supersession-framing notes; retire when underlying prose retires) deferred to subsequent dispatch at Charles tier-gate."
        )

    # §4.10 F138-7 candidate line 724: "active doc §5.6 (post-S64-005)"
    if "active doc §5.6 (post-S64-005) framed CG §8.5.4" in line:
        line = line.replace(
            "active doc §5.6 (post-S64-005) framed CG §8.5.4",
            "active doc §5.6 (post-S64-005; retired to IH §49.10 at S74-005) framed CG §8.5.4"
        )

    # §6.2 standing prohibition line 834: "superseded S65-004 + S64-005 framings per §5.4"
    if "superseded S65-004 + S64-005 framings per §5.4)" in line and "Phase 2 substantive derivation at forward-direction territory only" in line:
        # already handled above
        pass

    # §6.2 standing prohibition: "Canonical-content extension territory (§5.11) **singular substantive forward direction within composite-matter Phase 2 scope** (S66-004"
    if "Canonical-content extension territory (§5.11) **singular substantive forward direction within composite-matter Phase 2 scope** (S66-004" in line:
        line = line.replace(
            "Canonical-content extension territory (§5.11) **singular substantive forward direction within composite-matter Phase 2 scope** (S66-004",
            "Canonical-content extension territory (IH §49.10 §5.11) **singular substantive forward direction within composite-matter Phase 2 scope** (S66-004"
        )

    # §6.2 standing prohibition line 836: "per §5.6 + §3.2 D-COMP-MATTER-L3 row"
    if "per §5.6 + §3.2 D-COMP-MATTER-L3 row" in line:
        line = line.replace(
            "per §5.6 + §3.2 D-COMP-MATTER-L3 row",
            "per IH §49.10 §5.6 + active doc §3.2 D-COMP-MATTER-L3 row"
        )

    # §6.2-area supersession-framing note (load-bearing-now at active doc per S74-004 Phase 0 flagging; preserved BUT §5.x references within updated to IH §49.10 prefix)
    if "§6.2 standing prohibitions block below contains references to §5.11 canonical-content extension territory" in line:
        line = line.replace(
            "§6.2 standing prohibitions block below contains references to §5.11 canonical-content extension territory",
            "§6.2 standing prohibitions block below contains references to IH §49.10 §5.11 canonical-content extension territory"
        )
        line = line.replace(
            'This framing is **SUPERSEDED** by §5.11 revised label',
            'This framing is **SUPERSEDED** by IH §49.10 §5.11 revised label'
        )
        line = line.replace(
            "Cross-reference: §5.11 revised label + §5.10 forward-arc disposition",
            "Cross-reference: IH §49.10 §5.11 revised label + IH §49.10 §5.10 forward-arc disposition"
        )

    # Dispatch coverage tables (S64-002 + S64-003 + S64-004 + S64-005 etc): historical-narrative references to ported content
    # Pattern: lines starting with "- §5.X" or "| ... §5.X..." in cross-reference summary section
    # These describe past porting actions; references resolve at IH §49.10 with original §5.X attribution
    historical_dispatch_patterns = [
        ("- §5.2 canonical violation Δ formula", "- §5.2 [IH §49.10 §5.2 post-S74-005] canonical violation Δ formula"),
        ("- §5.6 CG §8.5.4 CR-46 full source formula", "- §5.6 [IH §49.10 §5.6 post-S74-005] CG §8.5.4 CR-46 full source formula"),
        ("- §5.3 four-mechanism reconnaissance verdict", "- §5.3 [IH §49.10 §5.3 post-S74-005] four-mechanism reconnaissance verdict"),
        ("- §5.4 composition path", "- §5.4 [IH §49.10 §5.4 post-S74-005] composition path"),
        ("§5.1–§5.10 |", "IH §49.10 §5.1–§5.10 post-S74-005 |"),
        ("§5.2 cross-ref)", "IH §49.10 §5.2 cross-ref post-S74-005)"),
        ("§5.7", "IH §49.10 §5.7 [post-S74-005]") if False else None,  # don't apply to §9.6 § references which have §5.7
        ("§5.6 L3 κGF channel-matching", "IH §49.10 §5.6 L3 κGF channel-matching [post-S74-005]"),
        ("ported at §5.2", "ported at active doc §5.2 [now IH §49.10 §5.2 post-S74-005]"),
        ("ported at §5.3", "ported at active doc §5.3 [now IH §49.10 §5.3 post-S74-005]"),
        ("ported at §5.3–§5.10", "ported at active doc §5.3–§5.10 [now IH §49.10 post-S74-005]"),
        ("F138-5 reference at §5.9 cross-ref", "F138-5 reference at IH §49.10 §5.9 cross-ref [post-S74-005]"),
        ("§9.5 (single-mode Dirac stress-energy; §5.2 cross-ref)", "§9.5 (single-mode Dirac stress-energy; IH §49.10 §5.2 cross-ref [post-S74-005])"),
        ("§9.6 (Pauli-antisymmetrized fermion-pair Slater determinant for L2 substrate at §5.7)", "§9.6 (Pauli-antisymmetrized fermion-pair Slater determinant for L2 substrate at IH §49.10 §5.7 [post-S74-005])"),
        ("§8.5.3a (Rider-1 substrate for L2 at §5.7)", "§8.5.3a (Rider-1 substrate for L2 at IH §49.10 §5.7 [post-S74-005])"),
    ]
    for pat, repl in [p for p in historical_dispatch_patterns if p is not None]:
        if pat in line and "[IH §49.10" not in line and "[post-S74-005]" not in line and "IH §49.10 " + pat not in line:
            line = line.replace(pat, repl)

    return line

# Apply updates only to non-§5 portion of new_ad (i.e., everything outside stub and beyond stub end)
# Note: new_ad already has stub replacing original §5 lines 758-993
# We update lines BEFORE stub (line 1 through line ~756) and AFTER stub (from beyond stub end)
updated_ad = []
for i, line in enumerate(new_ad):
    updated_ad.append(update_line(line))

with open(ACTIVE, "w") as f:
    f.writelines(updated_ad)

# Verification + report
with open(ACTIVE) as f:
    ad_new = f.readlines()
with open(IH) as f:
    ih_new = f.readlines()

print(f"Active doc: {len(ad)} → {len(ad_new)} lines (delta {len(ad_new)-len(ad):+d})")
print(f"IH:         {len(ih)} → {len(ih_new)} lines (delta {len(ih_new)-len(ih):+d})")
print(f"Net active-doc cleanup: {(len(ad)-len(ad_new))} lines removed from active doc")
print()

# Check for any orphan §5.x references at active doc (lines NOT containing "IH §49.10" or "retired" or dispatch coverage table markers)
import re
orphan_pattern = re.compile(r"§5\.(?!\d+\.)\d+")  # match §5.X but not §5.X.X
historical_markers = ["dispatch coverage", "VR §255", "S64-002", "S64-003", "S64-004", "S64-005", "S64-006", "S64-008", "S64-009", "A5 Composite-matter Phase 2", "PORT-VERBATIM", "Convention compliance fixes", "8.5.5 multi-mode", "S65-001 PONDER §5", "F-cand-S62-002-a Axis 2 sub-scope second-precedent at S66-003"]

orphan_count = 0
orphan_lines = []
for i, line in enumerate(ad_new):
    if orphan_pattern.search(line):
        # Check if this is a historical-narrative line OR a properly-updated forward-pointer (IH §49.10 prefix)
        is_historical = any(marker in line for marker in historical_markers)
        is_updated_pointer = "IH §49.10" in line
        if not is_historical and not is_updated_pointer:
            orphan_count += 1
            orphan_lines.append((i+1, line.strip()[:120]))

print(f"Orphan §5.x references (not IH §49.10-prefixed, not historical): {orphan_count}")
for ln, txt in orphan_lines[:20]:
    print(f"  {ln}: {txt}")
