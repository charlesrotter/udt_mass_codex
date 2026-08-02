# Exact derivation — global completion data and local fibers

Date: 2026-08-01  
Base: `e9754af8f93f6f3cd37d2c46fa0247c3c0e7e46d`

## 1. Type of object tested

The audit asks only whether an independently supplied global datum `C` defines a local
compatibility fiber `F_C`.  It does not ask which `C` is physical.  A local fiber here means the
set of endpoint values or jets that descend to the stated completion.

This is kinematic compatibility:

```text
C  ->  F_C subset X_local.
```

It is not an equation of motion, survival weighting, action, source, or bootstrap map.

## 2. Transition monodromy

For a registered transition matrix `M in GL(2,Z)`, descent across the identified endpoints is

```text
v_plus = M v_minus.
```

The compatible endpoint pairs form

```text
Graph(M) = {(v_minus,v_plus) in R2 x R2 : v_plus=M v_minus}.
```

Writing the two constraints with the matrix `C_M = [-M | I]`, acting on the endpoint-pair column,
gives constraint rank two for all eight
registered witnesses.  Hence every graph has dimension `4-2=2`.  Independent exact rational row
reduction shows that all `C(8,2)=28` graph pairs are distinct.  Global monodromy therefore
parameterizes a changing family of local endpoint-matching subspaces even though all members have
the same dimension.

The fixed subspace

```text
ker(M-I)
```

is not the primary descent fiber.  It follows only if one independently asks for a base-constant,
parallel, or fixed section.  Its dimensions for the eight controls are `2,0,0,0,1,0,1,1`; these are
conditional diagnostics only.

The source atlas registers the monodromy family and exact matrices, but most corresponding rows
have transition-descent schemas rather than complete metric witnesses.  This earns
`NATURAL_PARAMETRIC_LOCAL_JOIN_FIBER_SCHEMA`, not a realized physical family.

## 3. Seam regularity

For a scalar endpoint two-jet

```text
(f_minus,f'_minus,f''_minus; f_plus,f'_plus,f''_plus),
```

the ambient dimension is six.  Identity-transition matching through order `k` imposes `k+1`
independent equalities.  The exact control dimensions are therefore:

| join | constraints | fiber dimension |
|---|---:|---:|
| no marked join | 0 | 6 |
| C0 | 1 | 5 |
| C1 | 2 | 4 |
| C2 | 3 | 3 |

The registered general rule is transformed-jet matching through `k`; the scalar identity case is
only a transparent rank control.  Since the physical seam, `k`, and full transition remain
unselected, the result is a `NATURAL_PARAMETRIC_JET_MATCHING_SCHEMA_PHYSICAL_SEAM_OPEN`.

## 4. Smooth cap data

Inside the previously `CHOSE` registered toric two-cap family, a closing cycle

```text
w=x V+y Y,  y!=0,
```

has vanishing moment only if

```text
f_cap=-x/y.
```

The two registered cycles give `f_cap=+1` and `f_cap=-1`.  Smooth cap regularity also gives

```text
b0=0, f1=0, b1=0, u1=0, u0>0,
```

and the exceptional constant stratum has `c=f_cap^2=1`.  Thus the cap choice really changes the
local zero-jet value while sharing the regularity conditions.  Because the parent family and cap
structure are conditional/selected premises, this is one
`NATURAL_PARTIAL_CAP_JET_FIBER_CONDITIONAL_FAMILY`, not a native completion selector.

## 5. Curvature and holonomy

Pointwise curvature is computed from a supplied local metric and is therefore a forward readout.
A prescribed curvature level would define formal level sets only after choosing the level.  A
spectrum requires an operator and domain; an average or integral requires a domain, weight, and
normalization.  None is currently native and choice-free.

Holonomy does define an endpoint transport graph after a metric and path/loop are supplied.  The
complete twisted-`S3` witness has full sampled Lorentz holonomy, and the reciprocal coframe remains
path-labeled rather than endpoint-only.  Imposing `ker(H-I)` would additionally demand a parallel
or invariant section, which current premises do not supply.  Holonomy therefore earns a
conditional transport fiber, not a configuration-admissibility family.

No tested curvature route sends a choice-free instruction back to the local configuration:

```text
curvature_native_return_routes = 0.
```

## 6. Exact result

Completion data naturally parameterize partial local compatibility fibers at the level of
transition descent, seam regularity, and—inside one conditional completed toric family—cap jets.
The current record does not contain a general complete metric witness for the monodromy/seam
schemas, a curvature-derived return law, or a selector of completion.

Maximum conclusion:

```text
PARTIAL_KINEMATIC_GLOBAL_TO_LOCAL_FIBER_FAMILY_ONLY
NO_BOOTSTRAP_DYNAMICS_STABILITY_OR_SELECTION
```
