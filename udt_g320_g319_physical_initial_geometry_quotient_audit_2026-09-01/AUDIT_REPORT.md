# G320 internal audit report

Date: 2026-09-01

## Result

```text
G319_FREEDOM_NOT_PURE_REPRESENTATION__SCALE_FREE_INTRINSIC_CURVATURE_SEPARATES_LAWFUL_PROFILES__DECLARED_GAUGE_DUPLICATES_QUOTIENTED__NO_COMPLETE_MODULI_OR_PHYSICAL_DATA_SELECTION
```

## Findings

1. The physical comparison was performed on reconstructed `(gamma,K)`, not raw `psi` or seeds.
2. The exact invariant `Q_R=(integral R dmu)/Vol^(1/3)` is diffeomorphism and homothety invariant.
3. The positive profiles `psi_n=3/2+(1/5)cos(nx)` have the same volume but
   `Q_R(n)=n^2 Q_R(1)`.
4. G319's arbitrary-positive-profile theorem makes every integer mode lawful after a sufficiently
   large free `J0`; hence the registered family contains at least countably many inequivalent
   physical initial geometries.
5. Modes `1--4` were explicitly reconstructed in both signs at `d=Lambda=0,J0=100`; direct physical
   constraint residuals remained below `3.6e-15` and `J0` drift below `8.6e-14`.
6. Phase translations and reflections preserved all registered invariant summaries.
7. Nonconstant conformal-seed rewrites preserved both the physical metric and trace-free tensor.
8. An implementation-distinct verifier used different profiles, modes `1,3,5`, sample count, seed
   rewrite, and `J0`; it rebuilt Ricci by index loops and upheld the separator and constraints.
9. The result proves that G319 freedom is not purely representation. It does not classify every
   equivalence class or choose physical initial data.
10. The metric, reciprocal kernel, angular cancellation, scale, observations, and `X_max` are unchanged.

## Evidence counts

- production assertions: 290;
- independent assertions: 59;
- hostile mutations caught: 26/26;
- production controls: 4 modes x 2 signs at 16,384 periodic points;
- independent controls: 3 different modes x 2 signs at 3,072 points, plus isometry controls.
- current exact premise registry: pass;
- full repository suite: 215 passed and one known documented xfail.

## External adversarial review

The fresh external `gpt-5.4` reviewer authenticated all 32 manifest payloads, reran all four
registered commands in an ephemeral copy, and found all five generated artifacts byte-identical.
It independently rederived the curvature formula, integrated identity, homothety-neutral
separator, exact `n^2` mode scaling, and regular G319 reconstruction. It found no scientific defect
inside the bounded scope and returned
`G320_ACCEPTED__GENUINE_INITIAL_GEOMETRY_FREEDOM_UPHELD`.

## Remaining scope

The audit does not cover the complete G319 moduli quotient, nonflat primary seeds, multidimensional
profiles, nondiagonal tensors, `B=0` crossings, evolution, stability, physical topology, population,
sources, matter/mass, observations, scale, physical history, or `X_max`.

## Review status

`EXTERNALLY_ACCEPTED_BOUNDED`. This establishes real initial-geometry breadth in the registered
G319 family after the declared quotient. It remains neither a complete moduli classification nor
a physical-data, population, scale, or history selector.
