# Exact derivation — global/local reconstruction under the bootstrap working posit

## 1. Relation rather than optimizer

Let `C` be a complete configuration space and `O` independently typed global data. The minimal
mathematical statement of mutual admissibility is a relation

```text
K subset O x C.
```

When a same-solution global readout `R:C -> O` exists, closed bootstrap configurations form

```text
S_boot = K intersect Graph(R)
       = {(O,X) : (O,X) in K and O=R[X]}.
```

This is the fiber-product/equalizer form of the working posit. It permits multiple configurations
for one `O`, multiple `O` values for one local pattern, disconnected branches, and stratified
relations. A scalar objective, ordering, or single-valued self-map is not entailed.

If locally `K` is represented as `A(X,O)=0`, changing the residual basis can leave `K` unchanged.
The intrinsic infinitesimal object is therefore its conormal space. Selecting one normalized
response covector, action, or evolution law requires more structure than relation membership.

This section is a formal consequence of the adopted `WORKING POSIT`, not a metric-derived physical
formula.

## 2. Cover reconstruction is exact and nonselecting

Take a four-coordinate exact control `x=(x0,x1,x2,x3)`.

Cover A stores local data

```text
y_A=(x0,x1,x2; x1,x2,x3)
```

with two overlap equations. Its six-dimensional local-data space has constraint rank two and
descent dimension four. The restriction matrix has rank four, the overlap matrix annihilates its
image, and the gluing matrix obeys

```text
Glue_A Res_A = I_4.
```

Cover B refines the same data into

```text
y_B=(x0,x1; x1,x2; x2,x3).
```

It again has local dimension six, overlap rank two, and descent dimension four. Its restriction and
gluing maps have the same identity property. The explicit refinement map obeys

```text
Refine Res_A = Res_B,
Glue_B Refine Res_A = I_4.
```

Thus descent and refinement recover all four original configurations; they select none.

Now add a free two-component readout

```text
R x = (x0+2x1, x1+x2+x3).
```

On the eight variables `(y_A,o)`, the two descent rows plus two graph rows have rank four and nullity
four. The nullity is again the full configuration dimension. Readout plus reconstruction leaves
every `x` admissible.

This finite exact control instantiates the general distinction between well-defined descent and a
physical admissibility relation.

## 3. Completion data provide a partial kinematic relation

For each of the eight registered `GL(2,Z)` matrices `M`, endpoint descent is

```text
v_plus = M v_minus.
```

The compatible data form `Graph(M)` in a four-dimensional endpoint-pair space. Every constraint
matrix `[-M | I]` has rank two, so every graph has dimension two. All 28 graph pairs are distinct.

The overlap of `Graph(M)` and `Graph(N)` is controlled by

```text
(M-N) v_minus = 0,
```

and has dimension `2-rank(M-N)`. Exact evaluation gives:

```text
16 pairs: intersection dimension 0,
12 pairs: intersection dimension 1.
```

The latter share a nonzero line of endpoint data. The zero endpoint pair belongs to all eight
graphs. Hence the global completion changes the legal local joint, but local endpoint data do not in
general reconstruct one unique completion.

The registered seam hierarchy likewise changes the scalar endpoint-two-jet fiber dimensions

```text
NO_JOIN, C0, C1, C2 -> 6,5,4,3.
```

The conditional toric two-cap family fixes opposite local values `f_cap=+1,-1` with shared cap
regularity. Those prior exact facts retain their source premises.

Together these give a metric-native partial relation

```text
K_kin subset CompletionData x LocalJoinData.
```

It is selective on arbitrary local join data but does not select a physical completion or an
interior complete configuration.

## 4. Same readout and symmetry permit inequivalent relations

Use a two-coordinate local control and observer exchange `x1 <-> x2`. Let the invariant readout be

```text
o = R(x) = x1+x2.
```

Three swap-invariant relation representatives are

```text
A_identity  = o-(x1+x2),
A_product   = o-x1*x2,
A_quadratic = o-(x1^2+x2^2).
```

All depend on both `o` and local coordinates before closure. After substituting `o=R(x)`, the first
vanishes identically. On the preregistered 16-point rational grid `{-1,0,1,2}^2`, it retains all 16
witnesses. The other two retain respectively two and four different witnesses.

These are not candidate UDT laws. They are constructive countermodels to the implication

```text
same readout + same observer symmetry + nontrivial mutual-admissibility demand
  => unique relation.
```

## 5. What follows from the working posit

The posit supplies the following type-level requirements:

- independently typed global and local variables before closure;
- a nonidentity relation if the posit is to be falsifiable;
- same-solution intersection with the global readout graph;
- observer/frame and cover/refinement naturality;
- compatibility with boundary, transition, and global-modulus data; and
- permission for multiple branches rather than a unique optimizer.

The current metric record adds one real portion of the relation at global joins. It does not supply
the complete physical `R`, an interior `K`, its differentiable response, or its boundary completion.

## 6. Exact bounded result

```text
WORKING_POSIT -> NATURAL_ADMISSIBILITY_CORRESPONDENCE_TYPE
METRIC_COMPLETION_DATA -> PARTIAL_KINEMATIC_LOCAL_JOIN_RELATION
RESTRICTION_PLUS_GLUE -> IDENTITY_ON_EVERY_ADMITTED_COMPLETE_GEOMETRY
READOUT_GRAPH -> RECORDS_EVERY_SUPPLIED_CONFIGURATION
CURRENT_POSIT_PLUS_METRIC_RECORD -> NO_UNIQUE_OR_COMPLETE_INTERIOR_RETURN
```

Overall outcome:

```text
DERIVED_PARTIAL_KINEMATIC_ADMISSIBILITY_CORRESPONDENCE__
WORKING_POSIT_REQUIRES_BUT_DOES_NOT_DERIVE_COMPLETE_RETURN
```

This is not an impossibility theorem over future metric consequences or additional owner-authorized
premises.
