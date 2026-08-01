# Stability derivation-closure sweep — audit report

Date: 2026-08-01  
Base: `c38953cfe6cf36facdbc9f4670aabc3ffd17e2b2`  
Preregistration: `ef3d788b85ec36d87298c2ea56740f4ae7593a27`  
Status: `CLOSED_PASS_AFTER_REQUIRED_COLD_AMENDMENTS`

## Result first

**Outcome: `DERIVATION_SWEEP_MIXED_WITH_SCOPED_OBSTRUCTION`.** The blanket upstream sweep
adjudicates all fifteen registered objects across the five active families. It derives three exact
nonselection results but closes none of the missing native objects and advances no computation
readiness.

1. **F02/F07:** formal module compatibility survives; one common nonzero on-shell field, whole
   equation, differentiable boundary, and premise stack remain open.
2. **F01:** the frozen wall/period structure fixes at most lower germ data. Boundary responses with
   the same value and first germ have arbitrary second germ and different Hessians. N4 is typed but
   has no frozen equation. Full trace-active stability remains germ-conditional.
3. **F05:** the ring identities classify completion and mass branches but do not determine a
   response or perturbation domain. Exact opposite-Hessian controls prove the nonimplication.
4. **F04:** one static finite-box carrier-conditional solution does not select physical time,
   physical boundary, carrier section/transport, or bootstrap membership. Exact same-static-data
   flow and fixed-point controls prove the missing-law scope.

No family is discarded. F01's separately bounded local lambda-Schur CPU candidate is unchanged;
all other broader stability work remains blocked. Zero families are GPU-ready.

## Mechanical census

- frozen sources: 1,558 unique paths, unchanged;
- groups: 4/4;
- active families: 5/5 (`F01`, `F02`, `F04`, `F05`, `F07`);
- missing objects: 15/15, exactly one status each;
- object statuses: 3 `DERIVED_SCOPED_OBSTRUCTION`, 2 `FORMAL_COMPATIBILITY_ONLY`, 4
  `PARTIAL_CONSTRAINT_ONLY`, 6 `UNDERDETERMINED_NO_NATIVE_OBJECT`, and 0
  `NOT_APPLICABLE_AFTER_UPSTREAM_RESULT`;
- exact driver controls: 16/16;
- exercised fail-closed catches: 15/15;
- readiness promotions: 0;
- stability/GPU solves: 0/0.

## Scope discipline

The countermodel functionals and flows are logic controls only. No P4 response was transferred to
the ring or Hopfion family. No Hopfion operator was transferred elsewhere. The round `S2`, `L2+L4`,
and computational box retain `POSIT`, conditional/chosen, and solver-boundary status. The bootstrap
remains a working two-arrow schema with both maps open.

The F01 obstruction is limited to the frozen `jet<=2` wall/period/seal scope. A future native N4
equation could regrade it. The F05 and F04 controls prove failure of implication from the currently
frozen identities/static data; they do not rule out future native response or time laws.

## Cold-review adjudication

The fresh standard-library/Fraction verifier found two object-status errors and one source-scope
leak. All were corrected without changing algebra, outcome, or readiness:

1. `O14` is underdetermined, not inapplicable; no upstream result removes the needed
   time-perturbation/topology-propagation rule. Correction was preregistered at `419a235`.
2. `O05` is partial, not formal-only; separate module premise stacks do not establish one common
   stack. Correction was preregistered at `1132319`.
3. a transient prose dependence on a later coupling ledger outside the 1,558-path freeze was
   removed; Q02 rests only on frozen A04-A06.

The corrected cold pass returns 32/32 independent checks and rejects 21/21 genuine mutations. The
four independent artifacts and their hashes are recorded in `INDEPENDENT_REVIEW.md`.

## Four gates before banking

1. **Preregistered:** yes, source/group/object/status/outcome universes committed before derivation.
2. **Full or bounded scope justified:** yes, complete over the registered four groups, fifteen
   objects, and branch census; future N4/unregistered physics explicitly outside scope.
3. **Independently verified:** yes, fresh cold different-route verifier, 32/32 checks and two
   deterministic byte-identical runs.
4. **Every premise audited:** yes within the frozen scope; 21/21 false promotions rejected.

The package is bankable at its bounded source/logic-audit ceiling.

## Evidence

See `EXACT_DERIVATION.md`, `OBJECT_STATUS_LEDGER.tsv`, `GROUP_RESULT_LEDGER.tsv`,
`BRANCH_CENSUS.tsv`, `SOURCE_AUTHORITY_LEDGER.tsv`, `EXACT_CONTROL_LEDGER.tsv`,
`Q02_CONDITION_TRACE.tsv`, `READINESS_DELTA.tsv`, `DERIVATION_RESULT.json`, `VERIFICATION_RESULT.json`, and
`CATCH_PROOFS.tsv`, plus `INDEPENDENT_REVIEW.md`, `INDEPENDENT_RESULT.json`,
`INDEPENDENT_RAW.jsonl`, and `INDEPENDENT_VERIFIER.py`.

## Stop line

No navigation update, `grok` integration, action/carrier/boundary/time/bootstrap adoption,
stability solve, T4, GPU work, particle/mass claim, or canonization is authorized by this sweep.
