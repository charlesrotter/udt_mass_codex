# Exact derivation — extension, Cartan reconstruction, and solvability ownership

## 1. What is being distinguished

Four statements are not interchangeable:

1. local representatives glue to one global bundle object;
2. a global configuration or connection exists;
3. geometric definitions obey their integrability identities; and
4. a configuration solves a physical bulk/boundary law.

Only the fourth could supply the missing complete bootstrap return. This audit asks whether the
first three unexpectedly imply the fourth in the current complete-coframe architecture.

## 2. Exact extension descent preserves all seven extension directions

After a smooth reciprocal/screen split has been supplied, the extension data are

```text
h in Sym^2_+(Q*),
sigma in Hom(N,Q).
```

On an overlap with component transitions `P_ij` on `N` and `Q_ij` on `Q`, their exact laws are

```text
h_j = Q_ij^-T h_i Q_ij^-1,
sigma_j = Q_ij sigma_i P_ij^-1.
```

The primary and independent controls use the three-chart cocycle

```text
P01=[[1,1],[0,1]],       P12=[[1,0],[1,1]],
Q01=[[2,1],[1,1]],       Q12=[[1,1],[0,1]],
P02=P12 P01,             Q02=Q12 Q01.
```

Direct transport from chart zero to chart two agrees exactly with transport through chart one for
both `h` and `sigma`. Mapping a seed with three symmetric-screen entries and four mixing entries to
all 21 chart components has rank seven. Thus all seven seed directions survive descent and the
selection rank of cocycle compatibility is zero. Positive definiteness is preserved by the exact
congruence transformation.

This is not peculiar to the finite control. The source-backed global theorem is stronger: positive
screen metrics exist by convex partition-of-unity gluing and `Hom(N,Q)` has a canonical zero
section. Their fibers add no independent existence obstruction after the split. The control is an
exact regression witness for the transformation and dimension statements.

The actual global obstruction is upstream: a realized reciprocal reduction over spacetime may not
exist or be selected. The query-bundle architecture does not require such a section. Therefore that
obstruction is ontology-conditional, not one complete UDT return relation.

## 3. A global coframe is a stronger witness, not the metric's definition

A metric is represented by local coframes with Lorentz transitions. Requiring a single global
coframe additionally requires a tangent-bundle trivialization. It can exclude manifolds, but the
current metric and observer Reciprocity do not require it. Existing complete `R x S3` controls are
constructive witnesses inside a parallelizable class; they do not turn parallelizability into a
universal UDT premise.

Consequently “admits one global tetrad” is a conditional topology restriction, not a derived
complete-interior law.

## 4. Coordinate-integrable coframes are presentation dependent

Begin in a flat two-plane with the closed coframe `(dx,dy)`. Rotate it by the position-dependent
orthogonal matrix

```text
R(x)=[[cos(x), sin(x)],[-sin(x),cos(x)]].
```

The metric is unchanged because `R^T R=I`. Nevertheless, at `x=0`, the coefficient of `dx wedge dy`
in `d theta'_1` is `1`. Thus a coframe can be coordinate-integrable in one orthonormal presentation
and anholonomic in another presentation of the same metric.

The rule `d theta=0` is therefore not local-frame gauge invariant. Adopting it would select a
presentation and remove legitimate coframes; it is not a metric-native return.

## 5. Cartan reconstruction solves for the connection, not for the coframe

For a four-coframe, write its anholonomy as

```text
d theta^a = -1/2 C^a_bc theta^b wedge theta^c.
```

A metric-compatible frame connection has 24 independent coefficients
`Gamma_ab_c=-Gamma_ba_c`. The torsion-free first Cartan equation gives 24 linear equations. The exact
coefficient map has

```text
rank = 24,
nullity = 0.
```

Hence every pointwise anholonomy right-hand side has one metric-compatible torsion-free connection.
The reconstruction places zero additional pointwise constraints on the coframe. It is the
Levi-Civita uniqueness theorem in exact coefficient form.

An arbitrary independently prescribed *field* of structure coefficients must satisfy its own
realizability/Jacobi conditions. But for coefficients obtained from an actual coframe, `d^2=0` and
the Cartan/Bianchi relations are automatic differential identities. They do not distinguish
physical solutions from off-shell metrics.

## 6. Endpoint matching is not a parallel-section condition

For each frozen monodromy matrix `M`, ordinary endpoint descent is

```text
v_plus = M v_minus.
```

Its graph always has dimension two in the four-dimensional endpoint-pair space. A closed parallel
single-valued section adds the stronger equation

```text
M v = v.
```

The exact fixed-space dimensions across the eight frozen matrices are

```text
dimension 0: four matrices,
dimension 1: three matrices,
dimension 2: one matrix.
```

This is a real conditional selector: if parallel single-valued endpoint data are required, holonomy
can reduce or eliminate them. But path-labelled pair-frame comparisons are already globally typed
without this requirement, and current foundations do not demand parallelism. The fixed-space
condition therefore demonstrates what an extra premise could do; it does not derive that premise.

## 7. Why differential solvability is circular here

“Solvability” is not an operator by itself. A bulk solution set requires at least

```text
F[X]=0
```

with a specified operator `F`, domain, gauge treatment, and regularity class. A finite-cell
boundary problem also requires a boundary operator or polarization `B[X]=0`, corner/joint data, and
the relevant function spaces. The current foundation has not selected `F` or `B`.

Using EH, Bach, a carrier equation, or another chosen response to define the solvability set would
produce a conditional branch of that chosen parent law. It cannot derive the parent law or the
bootstrap return that was supposed to select it. This is the exact circularity boundary:

```text
parent law -> solution set
```

is valid, while

```text
unspecified solvability -> parent law
```

is not a typed operation.

Conditional EH and Bach principal symbols illustrate the dependence: both share the metric null
cone on their registered regular control, but have different order, multiplicity, kernels, and
boundary phase spaces. Solvability cannot erase those parent-law distinctions.

## 8. Rank-changing strata remain a real open boundary

The smooth split tile does not cover zero/null depth-gradient strata, projector-rank changes,
defects, or topology changes. A path in an ambient stratified configuration space may cross such a
stratum even though it is not a tangent inside the fixed-rank bundle tile.

This audit neither rejects those configurations nor proves that their extension conditions select
a physical return. They remain the only preregistered metric-native extension class not resolved by
the smooth-tile existence theorem. Exploring them would be a separate solution-space atlas, not a
license to assume that singularity avoidance or smooth continuation is a physical filter.

## 9. Exact bounded conclusion

The current metric gives well-defined global bundle containers, local-to-global compatibility, a
canonical Levi-Civita connection per representative, and completion-dependent local join fibers.
Those are substantial kinematics. They do not supply a nonidentity law on complete smooth coframe
interiors.

Nonidentity conditions appear only after adding a stronger global-coframe, coordinate-integrability,
or parallelism premise, or after choosing the missing bulk/boundary operator. Rank-changing
extension remains open. Therefore:

```text
DERIVED_EXTENSION_EXISTENCE_AND_CARTAN_RECONSTRUCTION_ARE_NONSELECTING;
CONDITIONAL_HOLONOMY_OBSTRUCTIONS_REQUIRE_EXTRA_PARALLELISM;
NATIVE_INTERIOR_RETURN_REMAINS_OPEN.
```
