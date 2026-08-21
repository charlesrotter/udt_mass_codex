# G202 evidence gates

Date: 2026-08-21

## Preregistration

`MAP.md` and `PREREGISTRATION.md` were committed and pushed at `8503a413` before confirmatory
implementation.

## Bounded completeness

The theorem covers local quiet-overlap jets, analytic nondegenerate sign-crossing order, an infinite
positive odd profile family, finite smooth-anchor nonselection, and dimensional monomial candidates.
It does not select a physical global history, scale, coefficient, or observation interface.

## Independent verification

- production: exact SymPy profile, amplitude, anchor-jet, and dimensional systems; 32/32;
- independent: standard-library exact-`Fraction` polynomial and dimension replay;
- 20,000 profile cases, 1,000 finite-anchor counterfamilies, 170,003 assertions;
- no production import or artifact read;
- hostile catches: 9/9.

## Premise audit

The primary slice is declared.  The reference scale, analytic regularity class, profile, and anchors
remain supplied or conditional.  The cubic is explicitly a control.  Dimensional combinations are
not physical laws.  No fit, transfer, `X_max`, source, action, matter, bootstrap, or protected work
enters.

## Mechanical gates

- package replay: pass; 32 production assertions, 170,003 independent assertions across 20,000
  profile cases and 1,000 anchor controls, nine hostile catches, nine source hashes, and no-write
  replay;
- premise verifier: pass on the 186-row registry;
- repository tests: pass, 117 passed and one expected xfail;
- diff check: pass;
- protected local work remains untouched.
