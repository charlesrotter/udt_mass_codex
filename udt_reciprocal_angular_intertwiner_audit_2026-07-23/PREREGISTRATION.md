# Complete-metric reciprocal–angular intertwiner audit preregistration

Date: 2026-07-23

## Bounded question

The immediately preceding audit established exact conditional global descent
of the value-level reciprocal character

```text
D(phi)=diag(exp(-phi),exp(+phi))
```

even where the derivative-based `3+3` realization degenerates. It did not
derive a physical reciprocal–angular soldering.

This audit asks:

> Does the complete registered metric supply a frame-independent,
> non-block-diagonal invariant that naturally identifies the reciprocal
> backbone with the angular sector, without first choosing that
> identification?

This is a metric-led invariant and type audit. It is not a search for a
particle, Hopf carrier, preferred topology, action, source, or desired
cosmology.

## Frozen base and nonduplication boundary

Base commit:
`9403690fa3940f482364eb034bed67fd2a0d260d`.

Earlier work already established, and receives no new credit here:

- the abstract reciprocal character and its `Z2` normalizer;
- the exact seal-local mixed Lorentzian readout family;
- complete two-parameter parity-compatible metric cross blocks for the
  registered constant angular seal lifts;
- the failure of those cross blocks, orientation, cocycles, CSN, and volume
  normalization to select the mixed-base modulus;
- the chart dependence of cross-block component labels;
- the field-assisted reciprocal `3+3` two-form reduction on nonnull-`dphi`
  strata; and
- exact conditional reciprocal-toric/Hopf compatibility.

The new object is the complete **intertwiner/naturality classification**
under the continuous reciprocal character, angular representation, seal
transition, full metric, and dimensional `c` anchor.

## Whole-frame objects and premise treatment

Use the dimension-matched reciprocal coframe

```text
theta_rec=(c dt, dx_parallel).
```

The observational `c` anchor is never set to a new physical value or treated
as optional. Algebra may use the dimension-matched basis, where `c` is
carried by the coframe conversion map rather than hidden in a dimensionless
coefficient.

| Object | Status and treatment |
|---|---|
| `c:T -> L` and `c^-1:L -> T` | `FOUNDING` plus `OBSERVED` numerical anchor; pinned |
| Reciprocal character on `E_rec` | `DERIVED-CONDITIONAL`; exact input |
| Positive CSN class | `FOUNDING`; no representative selected |
| Complete four-metric amplitudes | free and explored in registered real Lorentzian class |
| Abstract angular two-plane | registered sector; its physical realization remains conditional |
| Angular continuous representation | free and classified; identity, reciprocal, inverse-reciprocal, and general real generator retained |
| Angular seal lift | all registered `+I`, `-I`, reflection, and exchange classes retained |
| Metric reciprocal–angular cross block | free and explored, including zero and every registered parity-compatible nonzero family |
| `dphi` two-form `3+3` reduction | exact on nonnull strata; no global persistence or owner assumed |
| Physical reciprocal/angular slot identification | `OPEN`; candidate conclusion, never input |
| Angular length normalization | `OPEN`; `c` supplies time–length conversion, not an angular radius |
| Completion, action, source, carrier, density, mass | excluded as selectors |

## Exact algebraic classification

Let

```text
L=diag(-1,+1),             D(phi)=exp(phi L),
A(phi)=exp(phi B)
```

on the reciprocal and angular two-planes. For a candidate angular-to-
reciprocal map `S`, solve the full infinitesimal intertwiner equation

```text
L S = S B.
```

The classification must include:

1. all real `2x2` generators `B`, by rank of the solution `S`;
2. the condition for an invertible soldering;
3. the identity-angular, reciprocal-angular, inverse-reciprocal, repeated
   weight, rotation/Jordan, and general semisimple cases;
4. the dimension and moduli of every solution family; and
5. exact rank-zero, rank-one, and rank-two witnesses.

No preferred angular generator may be inferred from the existence of an
intertwiner.

## Seal and global compatibility

For every registered angular seal lift `R_ang`, solve

```text
F_rec S = S R_ang
```

and intersect it with the continuous-character solution space where both
structures are supplied. Determine separately:

- existence of an invertible intertwiner;
- uniqueness up to scale and frame gauge;
- orientation and parity;
- compatibility with the reciprocal cocycle;
- whether any complete finite-cell row supplies the required angular
  representation rather than merely admitting it.

All twelve registered completion families must receive a ruling. No type row
may be promoted to a complete on-shell `(g,phi)` witness.

## Complete-metric naturality and circularity tests

For a general symmetric block metric

```text
g=[[H,C],[C^T,Q]],
```

test:

1. whether `C=0` and `C!=0` remain admissible under the same founded data;
2. whether `C` is invariant under angular frame changes or requires supplied
   reciprocal/angular projectors;
3. whether a metric-derived construction can contract the abstract
   reciprocal bundle with tangent/angular data without already supplying a
   bundle map;
4. whether the nonnull-`dphi` rank-three reciprocal sectors canonically
   select an angular two-plane or retain transverse rotational freedom; and
5. whether any proposed invariant survives nonlinear chart/coframe
   transformations as an object rather than a component pattern.

An expression is circular if it uses the desired reciprocal/angular
decomposition to manufacture the map claimed to derive that decomposition.

## Explicit `c`-anchor tests

Write the raw-coordinate conversion as

```text
C_c=diag(c,1),            theta_rec=C_c(dt,dx_parallel).
```

Verify:

- `C_c` commutes with the reciprocal character in the dimension-matched
  coframe;
- restoring raw units gives the temporal coefficient `-c^2 exp(-2phi)`;
- changing the positive numerical anchor `c` cannot change the existence or
  rank of an intertwiner;
- `c` can calibrate clock versus ruler units but cannot silently provide the
  missing angular length/radius normalization; and
- no result demotes `c` merely because exact rank calculations can use
  dimensionless coordinates.

## Falsification and certification contract

The working separation fails if:

- the general real intertwiner equations yield a unique nonzero mixed map
  under the founded data;
- the complete metric supplies a canonical reciprocal and angular projector
  without assuming either;
- every admissible zero-cross-block countermodel violates a binding premise;
- the registered angular sector already carries a unique reciprocal
  continuous representation and seal lift;
- `c` fixes the angular normalization as well as clock–ruler conversion;
- the `dphi` `3+3` object canonically contains a unique angular two-plane;
- a claimed invariant is only a block component in a chosen chart; or
- any action, source, topology, carrier, density, mass, or boundary
  functional is imported.

Certification requires deterministic exact algebra, a separate independent
implementation, exercised mutation catches, source hashes, a fresh
zero-context adversarial review, repository tests, frozen-manifest replay,
and CPU-only execution.

## Maximum allowed conclusion

The strongest positive conclusion is:

`COMPLETE_METRIC_SUPPLIES_A_UNIQUE_FRAME_INDEPENDENT_NONBLOCK_RECIPROCAL_ANGULAR_SOLDERING_WITH_C_EXPLICIT`.

The strongest conditional/nonselection conclusion is:

`NONBLOCK_RECIPROCAL_ANGULAR_INTERTWINERS_EXIST_EXACTLY_FOR_MATCHED_REPRESENTATIONS_BUT_THE_COMPLETE_METRIC_RECIPROCITY_CSN_C_ANCHOR_SEAL_AND_FINITE_CELL_DO_NOT_SELECT_THE_MATCH__C_FIXES_CLOCK_RULER_CONVERSION_NOT_ANGULAR_NORMALIZATION`.

No action, matter, Hopf-carrier, mass, scale-closure, or universe-selection
claim is permitted.
