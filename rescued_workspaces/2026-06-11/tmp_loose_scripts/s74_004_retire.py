#!/usr/bin/env python3
"""S74-004 cleanup-arc Phase 1 retirement: atomic file edits.

- Extracts lines 717-896 from active doc (9 session-state status notes verbatim).
- Inserts new IH §49.9 sub-section into IH at line 7514 with verbatim preservation.
- Removes lines 717-896 from active doc + adds stub-pointer.
"""
import shutil

ACTIVE = "docs/udt_active_results.md"
IH = "docs/udt_investigation_history.md"

# Backups (in addition to git backup tags)
shutil.copy(ACTIVE, "/tmp/active_pre_S74_004.md")
shutil.copy(IH, "/tmp/ih_pre_S74_004.md")

# Read both files
with open(ACTIVE) as f:
    ad = f.readlines()
with open(IH) as f:
    ih = f.readlines()

# Pre-edit verification
assert ad[715].strip() == "", f"Expected blank at line 716 (idx 715), got: {ad[715]!r}"
assert ad[716].startswith("> **⚠ Status note (2026-05-18, post-S74-002"), f"Expected post-S74-002 at 717, got: {ad[716][:80]!r}"
assert ad[895].startswith(">"), f"Expected blockquote at line 896 (idx 895), got: {ad[895][:80]!r}"
assert ad[896].strip() == "", f"Expected blank at line 897 (idx 896), got: {ad[896]!r}"
assert ad[897].startswith("**Notable at S65-004 close"), f"Expected F-cand registry at 898, got: {ad[897][:80]!r}"

# Extract verbatim status notes (lines 717-896 in 1-indexed = indices 716-895)
notes_verbatim = ad[716:896]
assert len(notes_verbatim) == 180, f"Expected 180 lines, got {len(notes_verbatim)}"

# Build IH §49.9 section content
section_header = """### §49.9 [S74-004 cleanup-arc Phase 1: active doc §4.10 session-state status-note retirement] (originally active doc §4.10 status notes from post-S68-002 through post-S74-002 close, Sessions 68-74)

> **S74-004 cleanup-arc Phase 1 retirement (2026-05-18; commit on `reorg/cleanup-2026-02`).** Active doc §4.10 was carrying 13 stacked status notes pre-S74-004 (9 session-state notes at §4.10 + 1 retained current-state note at §4.10 + 3 supersession-framing load-bearing-now notes at §3.2/§5/§6.2 non-§4.10 sections). Per Trimble S72 bloat.md cleanup-arc diagnostic + S74-004 charter §1, Phase 1 of three-phase active-doc bloat reduction.
>
> **Retired here:** 9 session-state-snapshot status notes spanning post-S68-002 close (2026-05-15) through post-S74-002 close (2026-05-18).
>
> **Retained at active doc §4.10:** 1 current-state note (post-S74-003 close). For current canonical counter state see active doc §4.10 retained note + CLAUDE.md standing block + HANDOFF.md session-state.
>
> **Flagged load-bearing-now at active doc (NOT retired at Phase 1):** 3 supersession-framing notes at non-§4.10 sections (line 384 §3.2 + line 938 §5 + line 1174 §6.2). These are interpretive guards directing readers AWAY from stale S66-004 framing in §3.2/§3.8/§5.x/§6.2.5 prose toward current §5.11 "STRUCTURALLY EXHAUSTED AT S67-001" label. Charter §3 sub-choice 9 (halt-don't-salvage) requires suspension of retirement for load-bearing-now content not duplicated elsewhere; these 3 notes will retire as Phase 2 (§5 composite-matter wholesale retirement) + Phase 3 (§3.x/§6.2 manuscript-grade-observation condensation) retire the underlying prose. S74-004 AUDIT.md §1 honest scope-limitation report.
>
> **Phase 2 + Phase 3 of cleanup-arc:** chartered separately at Charles tier-gate post-S74-004 close. Phase 2 retirement of §5 composite-matter prose ~200 lines (cleaner shape per S74-004 charter Notes: §5.11 banner already self-flags STRUCTURALLY EXHAUSTED at S67-001). Phase 3 lower-priority §3.x/§6.2 condensation if applicable post-Phase 2.

> **Verbatim preservation of 9 retired status notes follows.** Original active-doc line attribution at retirement-execution time: 717 (post-S74-002) / 740 (post-S74-001-RETRY) / 760 (post-S73-004) / 778 (post-S72-002b) / 802 (post-S71-001a) / 820 (post-S70-003+S70-004a) / 839 (post-S69-004) / 856 (post-S68-004; "Earlier status note" label) / 878 (post-S68-002; "Earlier status note" label). Counter values + structural-depth references + F-candidate registry advances at each note represent the canonical counter-state-snapshot at that session's close; current canonical counter state lives in the retained post-S74-003 status note at active doc §4.10 + CLAUDE.md standing block + HANDOFF.md session-state.

---

"""

ih_insert = list(section_header.splitlines(keepends=True))
ih_insert += notes_verbatim
# Add trailing blank if not present
if not ih_insert[-1].endswith("\n"):
    ih_insert[-1] += "\n"
ih_insert += ["\n"]

# Insert into IH at index 7513 (between line 7513 blank and line 7514 ---)
# Pre-verify: ih[7511] is §49.8 end content (line 7512), ih[7512] is blank (line 7513), ih[7513] is --- (line 7514)
assert "See also CG §25.0" in ih[7511], f"Expected §49.8 end at idx 7511, got: {ih[7511][:80]!r}"
assert ih[7512].strip() == "", f"Expected blank at line 7513 (idx 7512), got: {ih[7512]!r}"
assert ih[7513].strip() == "---", f"Expected --- at line 7514 (idx 7513), got: {ih[7513]!r}"

# Insert: keep ih[0:7513] (lines 1-7513), then §49.9 content, then ih[7513:] (lines 7514+)
new_ih = ih[:7513] + ih_insert + ih[7513:]
with open(IH, "w") as f:
    f.writelines(new_ih)

# Build active doc stub-pointer
stub_pointer = """> **Prior status notes (9 session-state snapshots spanning post-S68-002 close through post-S74-002 close) RETIRED to IH §49.9 at S74-004 cleanup-arc Phase 1 (commit on `reorg/cleanup-2026-02`; verbatim preserved at IH).** Current canonical counter state is the post-S74-003 status note immediately above + CLAUDE.md standing block + HANDOFF.md session-state. For historical session-state snapshots from S68-002 through S74-002, see IH §49.9. Phase 2 (§5 composite-matter wholesale retirement) + Phase 3 (§3.x/§6.2 supersession-framing notes; retire when underlying prose retires) deferred to subsequent dispatches at Charles tier-gate.

"""

stub_lines = list(stub_pointer.splitlines(keepends=True))

# Remove lines 717-896 from active doc + insert stub-pointer after retained note (line 716 blank kept; line 897 blank kept)
# ad[0:716] = lines 1-716 (through blank at 716)
# ad[716:896] = lines 717-896 (status notes to retire)
# ad[896:] = lines 897+ (blank then F-cand registry)
# Result: ad[0:716] + stub_lines + ad[896:]
new_ad = ad[:716] + stub_lines + ad[896:]
with open(ACTIVE, "w") as f:
    f.writelines(new_ad)

# Verification
with open(ACTIVE) as f:
    ad_new = f.readlines()
with open(IH) as f:
    ih_new = f.readlines()

print(f"Active doc: {len(ad)} → {len(ad_new)} lines (delta {len(ad_new)-len(ad):+d})")
print(f"IH:         {len(ih)} → {len(ih_new)} lines (delta {len(ih_new)-len(ih):+d})")
print(f"Net cleanup: {(len(ad)-len(ad_new))} lines removed from active doc")
print()
print("Active doc retained-note + stub-pointer boundary (lines 715-720):")
for i in range(714, 720):
    if i < len(ad_new):
        print(f"  {i+1}: {ad_new[i][:120].rstrip()}")
