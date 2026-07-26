# Observer-pair triangle-consistency audit

Date: 2026-07-26

Preregistration commit: `18e8de6`

Grade: `VERIFIED_WITH_CAVEATS`

## Result first

Triangle consistency does **not** unconditionally select the remaining
complete-coframe screen response `lambda`.

It does produce one sharp conditional theorem. For the fixed-observer finite
directional family,

```text
[E_lambda(n;q),E_lambda(m;r)]
 = (q-q^lambda)(r-r^lambda)[P_n,P_m].
```

Consequently, if UDT is additionally required to use one flat,
endpoint-only, path-independent comparison rule in a common observer frame
for every generic direction and depth, then `lambda=1` is uniquely forced.
That is the clock-democratic `1+3` lift: all three spatial directions receive
the ruler weight.

The premise doing the selection is not currently founded. A properly typed
endpoint groupoid,

```text
T_AB=F_B D_lambda(phi_B-phi_A) F_A^-1,
```

obeys reversal and `T_BC T_AB=T_AC` for **every** `lambda`. It works because
one full coframe has been supplied at each endpoint. UDT has not yet derived
that endpoint section.

With pair-dependent direction frames the middle factors are not the same and
leave the exact mismatch

```text
M_B=F_(B|C)^-1 F_(B|A).
```

That mismatch is the smallest missing object: a native endpoint solder,
transition rule, or connection/transport section relating pair-specific
frames.

## Why lambda=1 is useful but not closure

At `lambda=1`, the fixed-observer map is spatially isotropic, so it commutes
with pure spatial rotations of the direction frame. The transition matrix is
not thereby erased. More decisively, changing the timelike observer gives

```text
[E_1(u;q),E_1(v;r)]
 = (q^-1-q)(r^-1-r)[P_u,P_v],
```

which is nonzero for generic noncollinear observers. The exceptional value
solves direction dependence around one fixed observer; it does not collapse
complete frame reciprocity to an abelian scalar rule.

## Holonomy ruling

The generic nonidentity loop is a real obstruction to the strong flat
common-frame route. It is not automatically a contradiction. In a curved
geometry, a path-dependent loop may be holonomy. Current UDT records supply
conditional Cartan/Levi-Civita transport once a complete metric branch and
path are given, but they do not select that branch, path, endpoint section,
or a connection that can noncircularly choose the physical lift.

Thus neither “all loops must be identity” nor “the loop is physical
curvature” is currently derived.

## Complete bounded classification

- Abstract founded reciprocal pair: exact additive cocycle.
- Common fixed-observer frame: `lambda=1` unique only under universal flat
  path independence; parallel, orthogonal, and zero-depth exceptions retained.
- One endpoint frame per event: exact groupoid for every `lambda`.
- Pair-dependent frames: explicit middle transition remains.
- Changing observer axes: noncommutative even for `lambda=1`.
- Global finite cells: cover, cut locus, seams, branch, and transport remain
  open.
- `c_E`, `G_obs`, and provisional `hbar`: scalar calibration cannot select a
  frame section or connection; `hbar` was not activated.

## Meaning for the open gate

The audit narrows rather than closes the open gate. The missing structure is
not another scalar coefficient. It is a rule that tells the complete metric
how pair-specific observer/ruler frames at neighboring comparisons are the
same, rotated, or transported.

If a later UDT premise derives flat endpoint-only comparison, `lambda=1`
becomes downstream immediately. If instead the complete metric derives a
connection or nontrivial holonomy, the full `lambda` family cannot be rejected
by the flat commutator alone.

No action, carrier, source, density, bootstrap optimizer, boundary, mass,
`X_max`, topology, or physical dynamics was selected.

## Evidence gates

1. **Preregistered:** yes, commit `18e8de6` before outcome algebra.
2. **Full or bounded:** complete for all eight registered composition routes,
   sixteen local/global strata, and the finite directional exponential
   family; not arbitrary connections or solved finite cells.
3. **Independent:** yes, a standard-library `Fraction` reconstruction with no
   SymPy or production import checks generic loops, exceptional strata,
   endpoint factorization at `lambda=2`, pair-frame mismatch, and changing
   observers.
4. **Premises audited:** yes. Flatness, endpoint section, pair path, observer,
   connection, global branch, scalar anchors, action, and matter premises are
   separately stamped.

No fresh external-model review was authorized; that is the caveat.

Maximum conclusion:

```text
BOUNDED_TRIANGLE_CONSISTENCY_CLASSIFICATION_FOR_REGISTERED_ROUTES;
LAMBDA_ONE_UNIQUE_ONLY_UNDER_STRONG_COMMON_FRAME_FLAT_PATH_INDEPENDENCE;
PROPER_ENDPOINT_GROUPOID_NONSELECTING;
ENDPOINT_SOLDER_OR_CONNECTION_SECTION_REMAINS_OPEN.
```
