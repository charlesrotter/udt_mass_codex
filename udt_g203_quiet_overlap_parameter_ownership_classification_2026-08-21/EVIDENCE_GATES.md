# G203 evidence gates

Date: 2026-08-21

## Preregistered

Pass. `MAP.md`, `PREREGISTRATION.md`, and the frozen source manifest were committed and pushed at
`f1fa632a` before implementation.

## Bounded completeness

Pass within the declared local analytic primary-spherical quiet-crossing classification. Center,
turning, finite-path, nonspherical, time-live, global, and downstream applications are omitted.

## Independent verification

Pass. A standard-library exact-rational implementation does not import production code or read its
artifact. It exercises 20,000 distinct parameter/germ cases and 280,011 assertions.

## Premise audit

Pass at the package level. Descriptor invariance is separated from numerical selection;
observational calibration is separated from theory derivation. Completed-pair Dual Reciprocity
remains working, not canon.

## Mechanical gates

- package replay: pass; 70 production assertions, 280,011 independent assertions across 20,000
  distinct cases, ten hostile catches, eight source hashes, and byte-stable no-write replay;
- 187-row premise registry update: pass;
- repository tests: pass, 118 passed and one expected xfail;
- diff check: pass;
- protected local work remains untouched.
