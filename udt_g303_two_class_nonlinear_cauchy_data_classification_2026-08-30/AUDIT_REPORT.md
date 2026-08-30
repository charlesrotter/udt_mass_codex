# G303 audit report

Date: 2026-08-30

## Internal bounded landing

```text
BOTH_G301_CLASSES_HAVE_THE_SAME_LOCAL_CAUSAL_PRINCIPAL_SYSTEM
__TRACEFREE_DATA_ARE_THE_UNION_OVER_ONE_CONSTANT_SCALAR_DATUM
__WELLPOSEDNESS_DOES_NOT_SELECT
```

Status: `EXTERNALLY_VERIFIED_WITH_EXPLICIT_CONDITIONAL_CAVEATS` after registered repairs.

## What was established

- `S_ab=0` plus contracted Bianchi is exactly `Ric_ab=Lambda g_ab`, `dLambda=0` on each connected
  solution region.
- The generic class is its `Lambda=0` sector.
- Harmonic reduction gives the Ricci-flat class and every Bianchi-completed fixed-`Lambda` sector
  the same full metric-wave principal operator and metric null cone; raw `S_ab` remains rank nine.
- Gauss--Codazzi gives `H=0,M=0` for the generic class and `H=2Lambda,M=0` for the trace-free class.
- If `Lambda` is not separately supplied, trace-free initial data obey `M_i=0,D_iH=0` and determine
  the one connected-component constant as `Lambda=H/2`.
- Both classes have the same functional initial-data burden. The trace-free class adds one
  connected-region number, not a scalar function.
- The direct reciprocal dependency census gives zero second-normal-jet Jacobian rank and generates
  no independent Cauchy/evolution residual; it evaluates both developments and selects neither.

## Executable evidence

- production: 79 exact assertions across nonlinear coefficients, three Lorentzian metric samples,
  twelve covectors, raw/full principal ranks, and nine connected graph sizes;
- independent: 59 assertions using a full coordinate Ricci calculation, direct kernels of metric
  trace maps rather than the production projector, and binary-tree incidence ranks;
- hostile mutations: 10 of 10 concrete formula/artifact mutations rejected;
- reciprocal dependency: exact generic two-endpoint readouts have zero dependence on a formal
  second-normal metric jet and generate zero evolution residuals;
- no independent implementation imports a production function.

## Four evidence gates

1. **Preregistered:** yes; commit `42e31303` was pushed before outcome files existed.
2. **Full or bounded scope:** exact inside a connected local boundary-free Cauchy slab and the
   frozen G301 metric-only classes; global completion and other law types remain open.
3. **Independent verification:** production and coordinate/trace-kernel/graph routes agree; the
   external reviewer reran all registered scripts from the sealed runtime.
4. **Premise audit:** harmonic gauge is method only; neither residual, `Lambda`, source, action,
   mass, observation, scale, or realized history was adopted.

## Caveats before stronger status

- Application of standard harmonic-gauge quasilinear-wave and constraint-propagation theorems is
  explicitly imported as mathematics and conditional on their usual smooth local hypotheses.
- No boundary, characteristic, singular, topology-changing, nonsmooth, or global data class was
  tested.
- The external reviewer returned `VERIFIED_WITH_CAVEATS`; all registered wording, independence,
  mutation, reciprocal-dependency, and packaging repairs remain caveated rather than stronger
  physics claims.
