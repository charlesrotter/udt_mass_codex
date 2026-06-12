"""
S85-002 migration execution:
1. Build IH §49.11 sub-section with retired content.
2. Insert into IH file before §50.
3. Replace active doc line 424 (D-OBSARCH-2 cell) with consolidated version.
4. Replace active doc §4.10 status notes block with consolidated version.
"""

import re
from pathlib import Path

# ============================================================
# Read all source files
# ============================================================
active_doc_path = Path('docs/udt_active_results.md')
ih_path = Path('docs/udt_investigation_history.md')

active_lines = active_doc_path.read_text().splitlines(keepends=True)
ih_lines = ih_path.read_text().splitlines(keepends=True)

# ============================================================
# Build IH §49.11 content
# ============================================================
# Retired §4.10 status notes (lines 819-924 inclusive, 0-indexed 818-923)
retired_4_10 = ''.join(active_lines[818:924])

# Retired D-OBSARCH-2 verdict letters
retired_d_obsarch = Path('/tmp/s85_002_d_obsarch_retiring.txt').read_text()

ih_49_11_content = f"""### §49.11 [S85-002 cleanup-consolidation: active doc §4.10 status notes (post-S74-003 through post-S84-001) + active doc §3.4 D-OBSARCH-2 CMB-PEAK verdict letters (S78-001 through S84-001) retired] (originally active doc §4.10 status notes + §3.4 D-OBSARCH-2 CMB-PEAK row verbose verdict-letter chain, Sessions 74-84)

> **S85-002 cleanup-consolidation dispatch retirement (2026-05-20; commit on `reorg/cleanup-2026-02`).** Per S85-002 dispatch charter §1 Part 1 active doc consolidation pass + retired-content-migration-to-archived-VR-and-investigation-history discipline at framework-level scope. Two retirement scopes consolidated at this IH §49.11 sub-section:
>
> **(1) Active doc §4.10 status notes retirement scope (sibling to §49.9 S74-004 cleanup-arc Phase 1 §4.10 retirement at S68-S74 scope).** §4.10 status notes from post-S74-003 close (2026-05-18) through post-S84-001 close (2026-05-20) retired to IH §49.11.1 below. Cumulative S75-S84 substantive arc canonical-record-grade ground PRESERVED at substantive content scope at CG §28 + §29 + §30 + §30.7 + §31 (sub-sections + cross-reference structure) + active doc §3.4 D-items registry + §3.8 cosmology methodology cluster narrative + canonical Form-T transport identity at §1.4 + §1.6 frame-relation closure (CLOSURE-PARTIAL canonical-content scope). Substantive findings within retired status notes ALREADY landed at canonical record at original dispatch attribution; this §49.11.1 sub-section preserves the verbatim status note prose for archive purposes.
>
> **(2) Active doc §3.4 D-OBSARCH-2 CMB-PEAK verdict letter chain retirement scope.** Verbatim verdict letter chain (S78-001 substantive PONDER + S78-002 verifier round-trip + S79-001 audit-first reconnaissance + S79-002 substantive PONDER + S79-003 verifier round-trip + S80-001 audit-first reconnaissance + S81-001 substantive PONDER + S83-001 substantive PONDER + S84-001 verifier round-trip on cumulative S81-S83 Mode (iv) candidacy arc) retired to IH §49.11.2 below. Substantive content + verdict letter wording preserved at original `dispatch_SXX_XXX/AUDIT.md` per individual dispatch attribution; this §49.11.2 sub-section preserves the active doc verbatim cell prose for archive purposes.
>
> **Replaced at active doc §4.10:** retain S85-001 status note as most-recent + recent-arc context cluster reference annotation pointing to this IH §49.11.1 sub-section.
>
> **Replaced at active doc §3.4 D-OBSARCH-2 CMB-PEAK cell:** retain BAO AMPLITUDE + BAO DISTANCE current sub-status + CMB-PEAK S85-001 most-recent reconnaissance verdict as current narrative + reference annotation pointing to this IH §49.11.2 sub-section for the retired verdict letter chain.
>
> **Migration discipline integrity per S85-002 charter §0:** all retired content preserved verbatim at this IH §49.11 sub-section with attribution chain. Reference-only annotations at canonical-record-source-section (active doc §4.10 + §3.4) preserve continuous accessibility chain. Substantive content within retired status notes was already canonical-record-grade landed at original dispatch attribution (CG sub-sections + active doc D-items + §3.8 cluster + §4 F-flag registry); §49.11 preserves verbatim prose for archive purposes only — no substantive content recovery dependency on §49.11.
>
> **No substantive content retraction or modification at S85-002.** Consolidation reduces procedural overhead at active doc canonical-record-source-section scope; substantive canonical content preserved at original landing venues + verbatim archive at §49.11.

#### §49.11.1 Active doc §4.10 status notes (post-S74-003 close through post-S84-001 close; 23 status notes verbatim from active doc §4.10 at S85-002 retirement time)

The following 23 status notes were retired from active doc §4.10 at S85-002 cleanup-consolidation. Each preserves verbatim content as registered at original dispatch close per F-cand-S67-004-d substrate-direction-audit discipline + S85-002 charter §0 retired-content-migration discipline. Reference-only annotation at active doc §4.10 ("Status notes for dispatches S74-003 through S84-001 retired to IH §49.11.1; see this section for verbatim content").

{retired_4_10}

#### §49.11.2 Active doc §3.4 D-OBSARCH-2 CMB-PEAK verbose verdict letter chain (S78-001 substantive PONDER through S84-001 verifier round-trip; 10 verdict letter sub-sections verbatim from D-OBSARCH-2 cell at S85-002 retirement time)

The following 10 CMB-PEAK verdict letter sub-sections were retired from active doc §3.4 D-OBSARCH-2 row cell at S85-002 cleanup-consolidation. Each preserves verbatim cell prose as registered at original dispatch landing per F-cand-S67-004-d substrate-direction-audit discipline + S85-002 charter §0 retired-content-migration discipline. Reference-only annotation at active doc §3.4 D-OBSARCH-2 CMB-PEAK ("Verbose verdict letter chain for dispatches S78-001 through S84-001 retired to IH §49.11.2; see this section for verbatim cell prose").

Note: this content was originally inline within the single-line D-OBSARCH-2 table cell as concatenated narrative; the verdict letters are space-separated within the source markdown line. They are preserved here as-is to allow direct comparison with the original cell content if reconstruction is required.

```text
{retired_d_obsarch}
```

---

"""

# ============================================================
# Insert IH §49.11 before §50 in IH file
# ============================================================
# Find the line index where "## §50." starts
section_50_idx = None
for i, line in enumerate(ih_lines):
    if line.startswith('## §50.'):
        section_50_idx = i
        break

if section_50_idx is None:
    raise RuntimeError("Could not find ## §50. header in IH file")

print(f"§50 header found at IH line {section_50_idx + 1} (0-indexed {section_50_idx})")

# Insert §49.11 content before §50 header
new_ih_lines = ih_lines[:section_50_idx] + [ih_49_11_content] + ih_lines[section_50_idx:]
ih_path.write_text(''.join(new_ih_lines))
print(f"IH §49.11 inserted; new IH line count: {len(new_ih_lines)} (was {len(ih_lines)}; added {len(new_ih_lines) - len(ih_lines)} lines + {len(ih_49_11_content)} chars)")

# ============================================================
# Build consolidated §4.10 content for active doc
# ============================================================
# Retain S85-001 status note (lines 817-818, 0-indexed 816-817) verbatim
# Then add reference annotation pointing to IH §49.11.1
# Then preserve the §4.10 trailing content (lines 925+ which is §4.11 header)

# Lines 813-818 are header + blank + post-S85-001 status note + blank
# Lines 819-924 are the retired status notes  
# Line 925 is the §4.11 header

# Find the actual line 817 (post-S85-001 status note) and 818 (post-S85-001 blank trailing)
# We retain lines 813-818 (header + blank + S85-001 status note) and replace 819-924 with reference

retain_4_10_header = ''.join(active_lines[812:818])  # lines 813-818 (header + blank + S85-001 + blank)

reference_annotation_4_10 = """> **⚠ Reference annotation (2026-05-20, post-S85-002 cleanup-consolidation):** Earlier §4.10 status notes for dispatches **post-S74-003 close (2026-05-18) through post-S84-001 close (2026-05-20)** — 23 status notes spanning S74-003, S74-005, S75-002 Phase B, S75-004, S75-005, S76-001/002/003/004/005/006, S77-001/002/003/004, S78-001/002/003, S79-001/002/003, S80-001, S81-001, S82-001, S84-001 — **retired to investigation history §49.11.1 at S85-002 cleanup-consolidation dispatch** (verbatim content preserved; reference-only annotation here per S85-002 retired-content-migration discipline). Substantive findings within retired status notes were already canonical-record-grade landed at original dispatch attribution: see CG §28 (SNe) + §29 (BAO distance) + §30 (bokeh-class $r_d$ Recognition) + §30.7 (ΛCDM-mechanism-absence) + §31 + §31.5.2 (CMB peak structure + Possibility B reframe) + active doc §3.4 D-items registry + §3.8 cosmology methodology cluster (eleventh-element + sixteenth-element CANDIDATE) + §4 F-flag registry. Current S85-001 close status note above carries current cumulative state. No substantive content lost; only procedural overhead reduced.

"""

# Active doc §4.10 trailing content starts at line 925 (the §4.11 header)
trailing_4_10 = ''.join(active_lines[924:])  # lines 925+ (§4.11 header onwards)

# Reconstruct active doc
new_active_lines_part = (
    ''.join(active_lines[:812])  # everything before §4.10 header
    + retain_4_10_header  # §4.10 header + blank + S85-001 status note + blank
    + reference_annotation_4_10  # NEW reference annotation
    + trailing_4_10  # §4.11 onwards
)

# ============================================================
# Now also replace line 424 (D-OBSARCH-2 cell)
# ============================================================
# We need to do this on the new_active_lines_part since we've already modified the file structure
# Re-parse to find line 424 in new structure
new_active_lines = new_active_lines_part.splitlines(keepends=True)
print(f"\nAfter §4.10 consolidation: active doc has {len(new_active_lines)} lines (was {len(active_lines)})")

# Line 424 (the D-OBSARCH-2 row) is still at the same 0-indexed position because §4.10 is later in the file
new_line_424 = Path('/tmp/s85_002_d_obsarch_new_line.txt').read_text()
new_active_lines[423] = new_line_424  # 0-indexed
print(f"Line 424 replaced (new length: {len(new_line_424)} chars)")

# Write final active doc
active_doc_path.write_text(''.join(new_active_lines))
print(f"\nFinal active doc line count: {len(new_active_lines)}")
print("S85-002 Phase 1 active doc consolidation + IH §49.11 migration COMPLETE.")
