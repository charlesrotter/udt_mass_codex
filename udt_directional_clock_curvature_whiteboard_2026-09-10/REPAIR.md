# DCI1 check-only repair R1

The fresh reviewer found no scientific defect in the candidate formula or witnesses,
but identified one vacuous author diagnostic: `static_time_constancy` differentiated
q0 only after `origin` had substituted t=0. That ordering cannot establish constancy
along the central observer worldline. The initial run remains exit 0; the check is
explicitly EXCLUDED as evidence in checks/AUTHOR_01_EXCLUSION.json.

The original author source is preserved byte-for-byte as checks/INITIAL_check_candidate.py,
matching the check_candidate.py entry in INITIAL_REVIEW_FREEZE.json. Its author_01
stdout/stderr/run record are unchanged. The initial scientific candidate and all other
initial-freeze files remain unchanged; source pins, equations, witnesses and scope do not change.

R1 computes the scalar slope before substituting only x=y=z=0, retains t, and checks
both its exact central value and derivative. A time-dependent mutant q+t demonstrates
the former false pass (differentiate after t=0 gives zero) and the repaired rejection
(retain t gives derivative one). This is a real check-order catch, not an added physics
condition or a repair of the static metric. Stationarity and the partner's spatial-only
calculation already supplied substantive support for the claim.

The corrected script is re-run into author_02 outputs. Focused re-review must check
the changed diagnostic, demonstrated old false pass, original-byte preservation, and
unchanged scientific argument. No initial failure or review qualification is erased.
