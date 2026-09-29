# Integration review check plan

This is a direct review after source-first, pilot and full-candidate exposure,
not a cold or blind review. The initial integration target is the exact file
map in INTEGRATION_CANDIDATE_FREEZE.json. No original source or root file is
changed by this reviewer.

Question: do the repaired mathematical domains preserve the results, and do
the typed dependency and review guards preserve their declared correspondence?
The mathematics remains metric-led and premise-relative. Code controls below
test version/routing behavior, not physical truth or review independence.

Independent small driver: load the guard as the subject under test; construct
new in-memory synthetic attestations; test its actual acceptance/rejection of
missing or changed review reports, and inspect changed-source propagation for
the G310 correction and completed-pair seams. Synthetic fixtures are labelled
and are never saved as actual reviews. Compare ASTs of original premise-verifier
functions against the attributed HEAD. No parent test functions are imported.

Resources: CPU, Python standard library, threads1 via the existing capture
utility; 60 seconds/512 MiB; no GPU, external data or original-file writes.
All output goes to this review directory. The synthetic inputs are
free-and-explored regression controls, not physical choices. A failure is a
bounded guard defect, not a mathematical refutation. Stop before acceptance
if a declared source/review correspondence is missing. Maximum conclusion:
reviewed conditional reconstruction and bounded maintenance correspondence,
with retained branches and unperformed checks explicitly identified.
