"""
S85-002 migration extraction:
1. Active doc line 424 D-OBSARCH-2 cell — split into keep portion (BAO AMPLITUDE + DISTANCE + CMB-PEAK S85-001 + OBSERVABLE-CLASS + CG cross-refs) and retire portion (CMB-PEAK verdict letters S78-001 through S84-001).
2. Active doc §4.10 status notes (lines 819-924) — already extracted.
"""

import re

# Read line 424
with open('docs/udt_active_results.md', 'r') as f:
    lines = f.readlines()

line_424 = lines[423]  # 0-indexed
print(f"Line 424 length: {len(line_424)} chars")

# Find all "★ CMB-PEAK sub-scope" markers
markers = [m.start() for m in re.finditer(r'\*\*★ CMB-PEAK sub-scope', line_424)]
print(f"CMB-PEAK markers found at positions: {markers}")

# Find the OBSERVABLE-CLASS column boundary
obs_class_match = re.search(r'\| \*\*OBSERVABLE-CLASS', line_424)
print(f"OBSERVABLE-CLASS column starts at: {obs_class_match.start() if obs_class_match else 'NOT FOUND'}")

# Strategy: retain everything BEFORE the SECOND CMB-PEAK marker (= S85-001 stays at full content; S84-001 onwards retire)
# Wait — re-read: order in the cell is S85-001 first (most recent, added at S85-001 commit), then S84-001 (added at S84-002 dispatch), then older.
# So we want to keep the FIRST CMB-PEAK marker (S85-001) and retire FROM the SECOND CMB-PEAK marker (S84-001) ONWARDS UNTIL the OBSERVABLE-CLASS column starts.

keep_until = markers[1]  # second marker = S84-001 start
retire_until = obs_class_match.start()  # OBSERVABLE-CLASS column starts here

# Verbose: print first 200 chars of each CMB-PEAK marker for verification
for i, pos in enumerate(markers):
    snippet = line_424[pos:pos+150]
    print(f"\nMarker {i+1} at pos {pos}: {snippet[:120]}...")

# Extract keep prefix (before second CMB-PEAK marker) + retire content + keep suffix (OBSERVABLE-CLASS onwards)
keep_prefix = line_424[:keep_until]
retire_content = line_424[keep_until:retire_until]
keep_suffix = line_424[retire_until:]

print(f"\nKeep prefix length: {len(keep_prefix)}")
print(f"Retire content length: {len(retire_content)}")
print(f"Keep suffix length: {len(keep_suffix)}")

# Write retire content to file
with open('/tmp/s85_002_d_obsarch_retiring.txt', 'w') as f:
    f.write(retire_content)
print("\n/tmp/s85_002_d_obsarch_retiring.txt written")

# Build consolidated cell line: keep_prefix + brief retirement annotation + keep_suffix
retirement_annotation = " **★ CMB-PEAK sub-scope verbose verdict-letter history (S78-001 + S78-002 + S79-001 + S79-002 + S79-003 + S80-001 + S81-001 + S82-001 + S83-001 + S84-001 verbatim cumulative chain) retired at S85-002 cleanup-consolidation dispatch to investigation history §49.11.2 — see `dispatch_SXX_XXX/AUDIT.md` per individual dispatch for full verdict letter content; canonical-record-grade ground preserved at substantive content scope at CG §31 + §31.5.2 + active doc §3.4 + active doc §3.8 (eleventh-element + sixteenth-element CANDIDATE narrative); S85-001 sub-status above carries current cumulative state.** "

new_line_424 = keep_prefix + retirement_annotation + keep_suffix
print(f"\nNew line 424 length: {len(new_line_424)} (was {len(line_424)}; saved {len(line_424) - len(new_line_424)} chars)")

# Write new line to file for diagnostic
with open('/tmp/s85_002_d_obsarch_new_line.txt', 'w') as f:
    f.write(new_line_424)
print("/tmp/s85_002_d_obsarch_new_line.txt written")
print("\nReady for replacement via sed/Edit.")
