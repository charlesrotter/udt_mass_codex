# G308 repair ancestry

The fresh sealed external review was banked at commit `56e0d75e` before any repair was made.

At that point:

- the scientific verdict was `G308_REPAIRABLE_DEFECTS` with no bounded scientific defect;
- `verify_package.py` failed in the sealed `frozen_sources/` layout and passed only after the
  reviewer added ephemeral sibling symlinks;
- the existing non-importing randomized verifier was judged useful but insufficiently distinct
  from the production outer-product construction to carry the full independence label;
- no repair implementation, Hodge/group-orbit verifier, portability verifier, or repaired outcome
  existed.

This file and `REPAIR_PREREGISTRATION.md` are the outcome-blind repair contract. Their parent is
`56e0d75e`; the bounded scientific landing remains unchanged unless a repair falsifies it.
