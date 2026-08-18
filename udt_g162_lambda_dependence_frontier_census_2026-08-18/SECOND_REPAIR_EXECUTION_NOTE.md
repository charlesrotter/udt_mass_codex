# G162 second-repair execution note

Date: 2026-08-18

The first post-`0060721c` run passed all 14 production checks and then stopped in the independent
source-crosswalk check. `SOURCE_OBJECT_CROSSWALK.tsv` assigned S02 to D07 although D07's frozen
census citations are S04 and S05. The repair removes only `D07` from S02. It changes no object,
class, formula, source manifest, result, or claim ceiling. The correction is banked before rerun.
