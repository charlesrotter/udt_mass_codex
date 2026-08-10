# Preregistration — calibrated observer-pair map owner atlas

Date: 2026-08-09
Mode: MAP before OBSERVE; metric-led; analytic/exact CPU
Authorization: Charles Rotter, “proceed”
Base: `grok` at `3ad41b15551d31cc2c6da5bf8313b6531f4f0279`

## Whole question

The terminal reciprocal-`c_E` audit derived a unique clock/ruler log-imbalance on a **supplied
regular A-calibrated pair metric**. It did not derive the physical pair map whose pullback supplies
that metric.

This atlas asks:

```text
Given only the complete Lorentzian metric/coframe, UDT's ordered observer query, and each
candidate's explicitly disclosed query or branch data, what calibrated two-dimensional pair maps
exist; what inputs own them; how do they compose; and where do they become branch-valued or fail?
```

The task is to classify the candidate space, not to obtain a preferred `phi`, CMB profile, particle,
or cosmology.

## Frozen candidate arena

The six families in `CANDIDATE_ARENA.tsv` are frozen before opening their branch-specific evidence.
No family may be dropped because it is nonunique, singular, path-dependent, or inconvenient.

1. orthogonal exponential/Fermi observer tubes;
2. pair surfaces integral to a complete-coframe-selected two-plane distribution;
3. stationary intrinsic Killing-flow pair surfaces as a conditional positive control;
4. general accelerated observer tubes with independently disclosed direction evolution;
5. exponential/Jacobi families through cut loci, caustics, and multiple-geodesic strata; and
6. pair maps carried through a third observer versus independently rebuilt pair maps.

## Mathematical type

A candidate supplies, on its declared domain,

```text
F: Sigma -> (M,g),
y^0=c_E tau_A,
y^1=s_A,
h=F^*g.
```

The atlas tests whether `F` is a regular immersion, whether its A-calibration is owned and carried,
and whether the terminal coordinate

```text
phi_pair=(1/4)log[(-det h)/h_00^2]
```

is defined. That formula is a readout of a supplied calibrated `h`; it is not used to select `F`.

## Premise ledger

| Item | Tag | Use |
|---|---|---|
| complete Lorentzian metric/coframe | `pinned-by-THEORY` | supplied UDT geometry; cited sources frozen before OBSERVE |
| measured `c_E` | `pinned-by-THEORY/OBSERVED` | dimension-matches A's proper time and ruler parameter |
| ordered observer query | `free-and-classified` | each legal query is retained; no preferred observer |
| A worldline and proper-time parameter | `free-and-classified` unless branch intrinsic | not silently derived from the metric |
| B event/worldline and event pairing | `free-and-classified` | readout does not select B |
| initial spacelike ruler direction | `free-and-classified` | every admissible direction retained |
| direction evolution rule | `free-and-classified` | Fermi-Walker, coframe-carried, Killing-carried, and unspecified controls remain distinct |
| Levi-Civita connection/exponential/Jacobi map | `pinned-by-THEORY` as geometry | physical comparison ownership remains tested, not assumed |
| complete-coframe two-plane distribution | `conditional supplied structure` | integrability and uniqueness tested; no plane selected by habit |
| Killing/conformal/recurrent structure | `conditional branch data` | positive controls only; never generalized universally |
| cut-locus branch/path | `free-and-classified` | all branches reported; no shortest or smoothest postselection |
| pointwise `phi` | `conditional presentation` | not inserted as an independent field |
| `X_max` | `WORKING_FOUNDATIONAL_FRAME` | asymptotic gate only; no value/profile/wall |
| source, action, carrier, boundary, bootstrap functional | `not supplied` | no candidate may invent one |
| numerical values, boundary conditions, fit targets | `none` | exact symbolic classification only |

There are no `pinned-by-HABIT` physical inputs. Mathematical chart choices are presentation tools
and must be removed by covariance checks.

## Frozen atlas axes

Every family receives one row for each of these axes:

1. exact object and arrow typing;
2. owned versus supplied data;
3. local existence and uniqueness;
4. complete-coframe/metric dependence;
5. A-calibration and parameter propagation;
6. endpoint-frame and chart covariance;
7. composition through an intermediate observer;
8. compatibility with an owned signed-depth cocycle if promoted physically;
9. cut-locus, caustic, rank-loss, null, and degenerate strata;
10. global continuation and topology; and
11. exact maximum allowed interpretation.

## Frozen dispositions

Each family/axis lands in exactly one of:

- `DERIVED_FROM_METRIC_AND_DECLARED_QUERY`;
- `CONDITIONAL_QUERY_DATA`;
- `CONDITIONAL_BRANCH_STRUCTURE`;
- `LOCAL_ONLY_BRANCH_VALUED`;
- `FAILS_REQUIRED_TYPE`;
- `OPEN_NOT_DECIDED_BY_CURRENT_FOUNDATION`.

These labels characterize provenance and mathematical type. They do not rank scientific merit.

## Exact controls

The analytic controller must independently expose:

- the universal pullback/clock-ruler-shift decomposition for a generic rank-two Jacobian;
- normal-neighborhood origin calibration for exponential tubes;
- the Frobenius obstruction for a candidate coframe two-plane distribution;
- the Killing-flow pullback and norm-ratio positive control;
- acceleration/direction-evolution terms in a general observer tube without importing GR observer
  dynamics;
- rank loss of `dExp` at conjugate/caustic strata and branch multiplicity at cut loci;
- the chain rule for compatible carried maps versus the absence of a canonical composition for
  independently rebuilt tapes; and
- a counterexample showing that equal terminal readouts do not identify one unique pair map.

Finite-dimensional algebra must have a second implementation without SymPy. Global claims must
state precise hypotheses and may remain theorem-backed classifications rather than numerical tests.

## Falsification and certification contract

A candidate is not metric-derived when any load-bearing worldline, event pairing, direction,
transport, branch, calibration, or normalization is inserted without being owned by the declared
query or branch.

A universal-owner claim fails if:

- another inequivalent candidate survives the same owned inputs;
- the construction is only local but is stated globally;
- composition uses independently rebuilt calibration data as though they were carried;
- the pair map becomes rank-deficient or branch-valued and one branch is silently selected;
- a coordinate identity is mistaken for a metric-natural map;
- a conditional Killing or stationary structure is generalized to all branches; or
- the terminal `phi_pair` formula is used as an acceptance filter on candidate maps.

Certification levels:

- `DERIVED`: exact construction/classification from the metric plus explicitly owned query data;
- `CONDITIONAL`: construction depends on disclosed query or branch data;
- `OPEN`: current premises do not own a required choice;
- `REJECTED_SCOPED`: a named candidate fails a stated type/covariance/composition gate.

## Maximum allowed conclusion

At most the atlas may classify the complete frozen arena and identify the smallest still-unowned
datum common to the surviving physical-map candidates. It may derive a unique owner only if all
other candidates fail on the same fully owned inputs.

It may not derive or select an action, source, carrier, matter law, mass, boundary, bootstrap
optimizer, `X_max` value/profile, physical `c_eff`, CMB spectrum, signalling law, preferred observer,
or canon entry. No GPU work or numerical fitting is authorized.
