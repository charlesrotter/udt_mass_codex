# P02 full-local-jet strata and repeated-tidal completion — audit report

Date: 2026-07-27
Status: `OBSERVED BOUNDED LOCAL OFF-SHELL ATLAS; VERIFIED-WITH-CAVEATS`

## Return

P02 mapped the preregistered causal and matrix-rank strata of the complete
triangular coframe at one local point.  P02-A retained all 23,040 attempts in
11,520 exact Cartesian strata.  It produced 15,459 finite local witnesses,
2,973 sampled coordinate-static causal no-witnesses, and 4,608 exact static
rank incompatibilities.

P02-A did not actually construct the repeated screen-tidal seam: it only
observed whether repetition happened in its initially generated Hessians.
That scope defect was recorded before P02-B.  P02-B then froze all 4,198
constructed zero-Hessian bases and released every allowed symmetric Hessian
component.  At every base, the numerical affine response onto
`(T22,T23,T33)` has full rank three.  All three registered targets

```text
T_AB = lambda delta_AB,   lambda = -shell^2, 0, +shell^2
```

were constructed and re-evaluated at all 4,198 bases: 12,594 of 12,594
candidates passed.

This resolves the local construction question in the exact bounded arena.  It
does **not** select repeated tides.  The opposite lesson is more important:
with unconstrained local Hessians, a repeated screen tide is freely
constructible and therefore cannot by itself distinguish a physical UDT
branch.  Any genuine selection must come from structure absent here, such as
global compatibility, a native equation, a variation domain, or a boundary
completion.

## P02-A exact census

| attempt status | count |
|---|---:|
| `CONSTRUCTED` | 15,459 |
| `NO_CAUSAL_WITNESS_AT_SAMPLED_VALUE` | 2,973 |
| `STRUCTURALLY_INCOMPATIBLE_HESSIAN_RANK` | 2,304 |
| `STRUCTURALLY_INCOMPATIBLE_SHIFT_RANK` | 2,304 |

All 15,459 constructed attempts were numerically finite.  Their curvature
operator ranks were:

| rank | count |
|---:|---:|
| 0 | 72 |
| 1 | 2 |
| 3 | 251 |
| 6 | 15,134 |

The static shift-rank-four and static collective-Hessian-rank-eight strata are
exactly incompatible because a coordinate-static first jet has only three
available derivative columns and its symmetric spatial Hessian has only six
available component columns.  The coordinate-static causal no-witness counts
are outcomes at the sampled point values in the triangular chart; they are not
global or invariant no-go results.

P02-A registered 111 repeated-tolerance attempts, but 110 had zero tidal
magnitude and the sole nonzero hit was not reproduced in its second attempt.
None of 3,119 constructed null attempts intersected that accidental set.  The
append-only `P02A_INTERIM_SCOPE_CORRECTION.md` prevents that observation from
being misread as an obstruction.

## P02-B exact census

The frozen base universe contains:

| founded-`dphi` class | bases | three target candidates | constructed |
|---|---:|---:|---:|
| zero | 1,296 | 3,888 | 3,888 |
| timelike | 804 | 2,412 | 2,412 |
| null | 802 | 2,406 | 2,406 |
| spacelike | 1,296 | 3,888 | 3,888 |

There are 2,880 dynamic and 1,318 coordinate-static bases.  Every one of their
12,594 response matrices has numerical row rank three.  Consequently, within
this sampled affine two-jet arena, the three independent screen-tidal
components can be prescribed locally.  The fixed-target solution fibers have
numerical kernel dimension 77 for the 80-component dynamic Hessian arena and
45 for the 48-component coordinate-static arena.  These are chart-component
counts, not physical degrees of freedom.

The solved collective Hessian ranks are:

| rank | count |
|---:|---:|
| 0 | 110 |
| 1 | 1,102 |
| 3 | 2,778 |
| 4 | 8,604 |

The Hessian Frobenius norm ranges from 0 to 662.467, with median 0.272902.  No
candidate reached the preregistered `1e6` large-Hessian classification.  The
maximum linear residual is `3.27e-13`; the maximum full-curvature
re-evaluation residual is `8.38e-11`, below the frozen `1e-8` gate.  All three
target signs, all angular-shape classes, all shift-value ranks, and every
represented first-jet rank class construct.

After construction, curvature remains varied rather than collapsing to a
single geometry: 12,102 candidates have full six-dimensional curvature-
operator rank, while the rest populate ranks zero through five.  Only 156
candidates have pair/screen Ricci mixing below the registered zero tolerance.
Repeated screen tides therefore do not force the rest of the local geometry
to one form.

## Verification

- GPU production: one Tesla V100-PCIE-32GB process, float64, 9.09 seconds,
  383,059,968 peak allocated bytes.
- Affine superposition: 128 preregistered controls; maximum scaled error
  `2.07e-16` against `1e-10`.
- Independent CPU reconstruction: 32 fixed anchors, direct local Taylor
  metric plus fourth-order four-dimensional finite differences, without
  importing the production module.  Maximum tidal-component error is
  `2.51e-7` and scalar-curvature error is `1.11e-7`, each against `2e-4`.
- Independent package replay: 32 of 32 checks and 15 of 15 deliberate
  corruption catches pass.
- Raw P02-B atlas SHA-256:
  `4d91131519f4da3979949d5ba13626337bcf2e71cda4c877cc31c417d8832515`.

No fresh external-model semantic review was available in this pass.  The
numerical verifier is independently structured but was written in the same
working session, so the grade remains `VERIFIED-WITH-CAVEATS`.

## Premise and completeness audit

- Question: metric-led local configuration-space mapping, not a target search
  for a particle, action, or desired branch.
- Founded `phi`: `DERIVED` reciprocal logarithmic depth; not an independent
  native scalar.
- Complete triangular coframe: exact extension-class representative, but its
  physical selection is `OPEN`.
- Point values, first jets, and Hessians: `free-and-explored` inside the frozen
  Cartesian strata.
- Shells 0.30 and 1.00 and Sobol coverage: `pinned-by-HABIT` numerical controls,
  not physical scales or frequencies.
- Pair/screen split and repeated-tidal readout: chart-supplied and
  `CONDITIONAL`.
- Strong local CSN: inactive.
- Action, equation, source, carrier, density, bootstrap, boundary, topology,
  global finite cell, physical time evolution, stability, mass, and `Xmax`:
  absent and `OPEN`.

In the ten-part completeness map, P02 covers a bounded local metric-field
configuration tile with all four coordinate jet directions live.  It does not
cover an action, Euler-Lagrange equations, a domain, boundary conditions,
topology, a dynamical class, global branches, stability, or a physical regime
of validity.

## Four evidence gates

1. **Preregistered:** yes.  P02-A was registered before its atlas; the P02-B
   correction, candidates, targets, tolerances, and resource bounds were
   committed before its solve.
2. **Full space or bounded scope justified:** bounded local two-jet arena only;
   every omitted layer is explicit.
3. **Independently verified on the load-bearing premise:** yes computationally,
   by a separately structured CPU Riemann reconstruction and package replay;
   fresh external-model review remains absent.
4. **Every premise audited:** yes for this package through
   `PREMISE_LEDGER.tsv` and this report.

## Maximum conclusion

`OBSERVED`: in the exact frozen P02-B base universe, the unrestricted allowed
metric Hessians make every symmetric two-dimensional screen-tidal target
locally constructible to the registered tolerance.  Null `dphi` and repeated
tides are locally compatible.  Repetition is neither obstructed nor selected.

P02 does not establish a global finite-cell metric, a native equation,
dynamics, a preferred causal class or tidal sign, or any physical UDT branch.
The next justified map must move from isolated local jets to global
compatibility rather than drilling into another locally prescribable curvature
target.
