# Reconstruction architecture implied by the working posit

## The correct mathematical home

The working posit does not require a scalar optimizer or even a single-valued map. Its least
committal mathematical form is a correspondence.

Let:

- `C` be the complete configuration space, including boundary and completion data;
- `O` be independently typed global data;
- `K subset O x C` be the admissibility correspondence saying which complete configurations are
  legal for which global data; and
- `R:C -> O` be the local-to-global recomputation map, when it is defined.

Then the bootstrap solution set is the intersection

```text
S_boot = K intersect Graph(R)
       = {(O,X) : (O,X) in K and O=R[X]}.
```

This form preserves multiple branches and sectors. It does not require `K` to be the zero set of a
scalar, to be single-valued in either direction, or to have a preferred ordering called
“optimization.”

If a differentiable local section `A(X,O)=0` represents `K`, then joint variation belongs to the
full `(X,O)` tangent space. The intrinsic first-order response is the conormal space of `K`, not one
preferred normalized residual. A physical response one-form, action, or evolution law would require
additional ownership beyond the set `K`.

## What the metric already supplies

The current record supplies part of `K` at the kinematic completion boundary:

```text
completion datum C  ->  allowed endpoint/joint fiber F_C.
```

Exact instances are:

- `Graph(M)` endpoint fibers for registered monodromies;
- nested transformed-jet matching for seam regularity;
- conditional cap-jet values and regularity inside the supplied toric completion.

These are genuine restrictions on local data. They arise from constructing one global geometry,
not from an action or matter model.

Ordinary cover descent belongs here too, but it is universally reconstructive: compatible local
pieces glue back to every admitted complete geometry. It checks well-definedness without selecting
which complete geometry is physical.

## What is still missing

The partial completion correspondence does not yet contain:

- a native interior response or evolution condition;
- a complete physical global-state readout;
- native total energy, mass, or density;
- a physical completion/boundary selector;
- a full relation across causal, rank-changing, and query strata; or
- a persistence criterion for local structures.

Consequently, closing the existing relation with its own completion readout only says that an
already-complete geometry has the completion it has. It does not select among complete geometries.

## Exact nonselection controls

Two admissible covers of a four-coordinate control both have local-data dimension six and overlap
constraint rank two. Each descent space therefore has dimension four, exactly the original global
space. Restricting, refining, and gluing returns the same four coordinates.

Adding a two-component free readout graph gives total constraint rank four in eight variables and
nullity four. Thus every original configuration remains possible.

The eight registered monodromy graphs are all distinct two-dimensional subspaces of the
four-dimensional endpoint-pair space. However:

- 16 graph pairs intersect only at zero;
- 12 graph pairs share a nonzero one-dimensional endpoint line; and
- the zero endpoint pair lies in all eight graphs.

Local endpoint data therefore do not generally reconstruct one unique completion.

Finally, the same symmetric readout `o=x1+x2` and the same observer exchange admit multiple
inequivalent symmetric relations. On the fixed 16-point rational witness set, the reconstruction
identity retains all 16 points, while two nontrivial relations retain two and four different
points. These are logic controls, not proposed UDT laws. They prove that readout, frame symmetry,
and the demand for nontrivial mutual admissibility do not determine the relation's formula.

## Bounded conclusion

The working posit determines the *type* of the missing joint and rules out the reconstruction
identity as a physical selector. The current metric supplies a nonempty partial kinematic
admissibility correspondence at global joins. It does not yet derive the complete interior return
relation.

This is a better-defined table leg, not the completed table.
