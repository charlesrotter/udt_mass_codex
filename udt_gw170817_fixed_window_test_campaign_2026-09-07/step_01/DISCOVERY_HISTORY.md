# FW1 discovery history

Before candidate freeze or strain exposure, metadata_checks.py incorrectly
asserted that every proposed off-source window had all127 DQ bits. The first
metadata_run failed at that actual assertion; stdout/stderr/command are saved.
The event's padded support passed, but not every background support does.
Repair: retain the fixed all127/transient-free predicate and discard background
windows that fail it; do not weaken the predicate. Sort survivors, first12 for
PSD training and all remaining for reference. Report reduced counts; too few
references must narrow attainable rank resolution, not pretend full counts.
The preceding code is reconstructible by reversing the recorded substitutions:
eligible set/filter logic replaces the unconditional DQ/injection asserts;
the first version refused existing extracts, the current version reuses only
the explicitly named metadata-mask extracts from the same checksum-verified
files. No strain sample or outcome influenced this change. This is pre-candidate
metadata discovery, not a repair of a reviewed scientific result.
