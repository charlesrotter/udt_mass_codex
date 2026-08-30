# G303 run record

Date: 2026-08-30

## Preregistration

```text
42e31303 Preregister G303 nonlinear Cauchy classification
```

This commit was pushed before production or outcome artifacts existed.

## Production

```text
BOTH_G301_CLASSES_HAVE_THE_SAME_LOCAL_CAUSAL_PRINCIPAL_SYSTEM__TRACEFREE_DATA_ARE_THE_UNION_OVER_ONE_CONSTANT_SCALAR_DATUM__WELLPOSEDNESS_DOES_NOT_SELECT
assertions=79
generic constraints: H=0, M_i=0
tracefree constraints: H=2 Lambda constant, M_i=0
```

## Independent replay

```text
G303 independent verification PASS (59 assertions)
Ric=3h^2 g, R=12h^2, H=6h^2=2 Lambda
```

The repaired independent route computes the full coordinate Ricci tensor of a time-live exponential
spatial metric, constructs the nine-dimensional kernel of the metric trace map without the
production projector, and uses connected-tree rank constructions. It imports no production
function.

## Hostile replay

```text
G303 concrete hostile mutations PASS (10/10)
```

The repaired suite mutates actual Bianchi, trace, Hamiltonian, constancy, projector, principal,
kernel-dependency, nesting, and momentum formulas. It contains no hard-coded selection Boolean.

## Direct reciprocal dependency replay

```text
G303 direct reciprocal dependency census PASS
second-normal-jet Jacobian rank=0; generated evolution residuals=0
```

This is a bounded syntax/dependency result for the registered pair readouts, not a new evolution
law or a claim about every future coupling.

## Preserved first package failure

The first package replay searched `LAY_REPORT.md` for the exact phrase `one number`, while the
document correctly said `one additional number`. The semantic guard was repaired to the exact
existing wording. No formula, landing, premise, or result changed.

The first repaired package replay also compared a phrase across a Markdown line break without
normalizing whitespace. The guard was changed to compare normalized words; no evidence wording or
scientific result changed.

## External review and registered repairs

The valid sealed GPT-5.4 review returned `VERIFIED_WITH_CAVEATS` and retained the one-constant and
fixed-sector well-posedness classification. Commit `4c030845` preserved the response and repair
contract before the repair outcomes existed. Repairs R1-R6 made the lawful-data compatibility,
raw-rank-nine versus completed-rank-ten distinction, imported theorem status, direct reciprocal
dependency result, concrete mutation tests, trace-kernel independence, and review packaging
explicit. The earlier network-invalid review session remains discarded.

## Repository gates

```text
G303 package verification PASS (24 required files)
PASS: 285-row current scientific premise registry
197 passed, 1 expected xfail in 136.32s
```

The xfail is the existing registered matter-sector habit-pin item; G303 does not touch that sector.
The repaired status is `EXTERNALLY_VERIFIED_WITH_EXPLICIT_CONDITIONAL_CAVEATS`; neither residual nor
a realized history is selected.
