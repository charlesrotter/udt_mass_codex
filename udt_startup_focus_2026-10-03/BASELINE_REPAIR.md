# Editorial provenance repair

The initial SFC1 baseline was copied from CPW1 with only HEAD replaced; its
origin/time/source hashes and startup description still described the earlier
ESR state. The mathematical reviewer caught this metadata error before acceptance.
INITIAL_BASELINE.json preserves the exact erroneous candidate. INITIAL_INTEGRATION_FREEZE.json
preserves its initial accepted-map proposal; no acceptance was bound to it.
BASELINE.json now records actually checked HEAD/origin and76 preserved untracked
names, plus explicitly reconstructed git-HEAD pre-edit source hashes. Its UTC is
the repair measurement time, not a fabricated original snapshot time. The
WORK_ORDER accurately retains observed startup actions. No scientific source,
central meaning, equation or protected payload changed. Both reviewers receive
the corrected freeze and must review the repair before acceptance.
