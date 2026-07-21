# Metric-native two-pair reciprocal-reduction selector audit

Date: 2026-07-21

## Result first

The metric-wide selector audit found one genuine piece of the hoped-for elegant structure, but not
the complete derivation.

The conformal metric, orientation, scalar depth, and ordinary curvature data do **not** select a
second reciprocal pair everywhere. They can select angular axes only on non-isotropic strata where
a particular trace-free Hessian or curvature tensor is nonzero and has a simple spectrum. Those
constructions fail exactly on flat, round, constant-curvature, zero-gradient, or repeated-eigenvalue
strata. Different admissible tensors can also select different axes, and current UDT supplies no
priority rule.

The finite-cell seal gives a sharper result. Conditional on choosing one of the complete seal lifts
whose angular action is a reflection, the positive angular metric and the seal determine a unique
complementary reciprocal reflection at the seal, up to global sign/exchange:

```text
M = J_q R,
M^2 = I,
tr(M) = 0,
M is q-self-adjoint,
R M R = -M.
```

Here `J_q` is the oriented metric complex structure of the positive two-dimensional screen and `R`
is its angular seal reflection. This theorem survives exact nonzero base-angular coupling at both
registered `mu=4` and `mu=9` witnesses.

But the complete angular seal lift is not selected. The registered `+I` and `-I` angular lifts have
no nonzero anticommuting second pair at all, while the axis-reflection and local Hopf-exchange lifts
do. And even in a reflection lift, the theorem is seal-local: carrying `M` consistently into the
bulk requires a connection whose holonomy commutes with the full reciprocal endomorphism. Current
UDT does not derive that bulk reduction or the transport premise.

The exact status is therefore:

```text
NO_UNCONDITIONAL_METRIC_NATIVE_TWO_PAIR_SELECTOR_IN_AUDITED_CLASS;
DERIVED_CONDITIONAL_SEAL_LOCAL_COMPLEMENTARY_PAIR;
SEAL_LIFT_SELECTION_AND_BULK_HOLONOMY_REDUCTION_OPEN.
```

This is real narrowing. The missing principle is no longer an unspecified angular mechanism. It is
the possible statement that **complete Reciprocity makes the finite-cell seal seed a globally
integrable two-pair reduction**. That statement is not present authority and was not adopted.

## Lay interpretation

The metric by itself tells us the shape of the local measuring screen, but a perfectly round screen
has no marked direction. It cannot tell us which way should stretch while the perpendicular way
shrinks. Curvature can mark directions when the screen is uneven, but the marks disappear wherever
the geometry becomes perfectly symmetric.

The seal is different. If the seal acts like a mirror inside the angular screen, it already marks
one axis. The metric supplies the perpendicular axis. Together they define the second grow/shrink
pair almost automatically.

That sounds like the missing answer, but two joins remain:

1. UDT currently allows complete seals that do not contain that angular mirror.
2. A direction marked at the universe's seal does not automatically tell every interior point how
   to orient itself. It must be carried inward without giving different answers along different
   paths.

Thus we found a plausible boundary seed, not yet the whole-universe law.

## Why the metric alone cannot mark the second pair

On a positive two-dimensional screen, rotations preserve the metric. A metric-natural
self-adjoint endomorphism must commute with those rotations. Exact linear algebra leaves only a
scalar multiple of the identity. Adding trace zero forces that scalar to vanish, so it cannot be a
normalized reciprocal reflection.

Orientation supplies the Hodge operator `J_q`, but

```text
J_q^2 = -I,
```

not `+I`. It supplies a quarter-turn, not two real reciprocal eigenlines.

Supplying the founding longitudinal plane determines its metric-orthogonal positive screen, even
with coordinate cross terms. It does not remove the screen's residual rotation freedom. A non-null
`d phi` can distinguish one line and its complement, but it does not by itself split the remaining
screen and fails wherever `d phi=0`.

These are stabilizer statements, not failures of a particular coordinate choice.

## What Hessian and curvature can do

Every nonzero symmetric trace-free two-dimensional screen tensor has the form

```text
S = [[a,b],[b,-a]],
S^2 = (a^2+b^2) I.
```

Therefore

```text
M_S = S / sqrt(a^2+b^2)
```

is an exact local reciprocal involution. A projected trace-free Hessian of `phi` is conformally
natural on a screen where `d phi` has no screen component: the conformal correction is pure trace
and disappears. Trace-free Ricci, an electric curvature block, or another symmetric curvature
concomitant can work similarly on a simple-spectrum stratum.

This is useful but not a universal selector:

- `S=0` makes normalization undefined;
- round and constant-curvature screens have no trace-free curvature axis;
- repeated curvature spectra restore continuous rotations;
- two legitimate tensors such as `diag(1,-1)` and `[[0,1],[1,0]]` select different axes; and
- current UDT supplies no rule giving Hessian, Ricci, Weyl, or a combination priority.

Consequently curvature can diagnose a reduction already present on a favorable stratum. It does
not supply a complete reduction through every branch and degeneracy.

## Exact seal-local theorem

Let `(E,q)` be the positive screen at the finite-cell seal and let the angular part of the complete
seal be a `q`-orthogonal reflection `R`. Once an orientation is chosen, `q` supplies its compatible
quarter-turn `J_q`. An orientation-reversing reflection obeys

```text
R J_q R = -J_q.
```

Define

```text
M = J_q R.
```

Then exact algebra gives

```text
M^2=I,
tr(M)=0,
M^T q=q M,
R M R=-M.
```

Changing orientation sends `M` to `-M`, which exchanges its two reciprocal eigenlines. Without the
metric relation, seal inversion alone leaves the continuous family

```text
[[0,u],[1/u,0]].
```

The metric collapses that continuous freedom to the discrete sign/exchange.

The theorem cleanly separates the registered angular lifts:

- angular `+I`: the anticommutant is zero;
- angular `-I`: the anticommutant is zero;
- axis reflection: `M=J_q R` exists uniquely up to sign;
- local Hopf exchange: the same theorem holds in a conjugate basis.

The deciding fact is not the filename “Hopf.” It is whether the complete angular seal has one fixed
and one reversed direction.

## Non-product cross-coupling check

The result is not an artifact of setting the metric's cross block to zero. For

```text
G = [[H,C],[C^T,I]],
C = [[1/10,1/10],[1/10,-1/10]],
```

the metric-orthogonal screen is embedded by

```text
W(y)=(-H^-1 C y,y),
```

and carries the Schur metric

```text
q_screen=I-C^T H^-1 C.
```

The two exact witnesses give

```text
mu=4: q_screen=diag(51/50,149/150),
mu=9: q_screen=diag(101/100,199/200).
```

Both are positive, seal-invariant, and generate exact full four-dimensional involutions. In the
orthogonal base/screen frame the complete endomorphism is the founding base pair plus `J_q R`; in
the original mixed coordinates it still squares to identity and is inverted by the complete seal.

Thus cross terms do not destroy the boundary theorem. They also do not choose the reflection lift.

## Why the boundary seed is not yet a bulk law

Given a supplied connection, boundary data can always be transported along one chosen path. A
single-valued path-independent result requires every holonomy generator to preserve it. For a
parallel reciprocal endomorphism,

```text
nabla L=0  implies  [Omega,L]=0.
```

A generic rotation holonomy changes a reflection axis. The exact `pi/4` witness conjugates
`diag(1,-1)` to a different reflection. Therefore a seal-local `L` extends globally only when the
connection has the required reduced holonomy.

The parent audit proves that a torsion-free conformal connection preserving normalized `L` is
unique **if it exists**. It does not prove existence, select the boundary `L`, or require the
holonomy reduction. Using that theorem to manufacture the missing bulk law would reverse its logic.

Current finite-cell data supply no angular evolution equation. Current bootstrap can test a future
complete solution but contains no local parallelism, path-independence, or holonomy-centralizer
condition.

## Intrinsic angular geometry adds a second obstruction

The parent's positive full-pair witness used an angular coframe whose only variation was radial. It
was complete for that declared local class. Restoring intrinsic angular connection shows that the
full pair is not generically compatible merely because it fixed the radial-rate mismatch.

For the exact product screen

```text
q=d theta^2+sin^2(theta)d psi^2
```

at `sin(theta)=3/5`, fixed full-pair axes of either orientation give coefficient rank four and
augmented rank five in the torsion-free Weyl compatibility equations. The direct transverse-zero
generator remains compatible at constant `phi` because the angular rotation acts within its zero
eigenspace.

More invariantly, the round screen curvature generates angular rotations that do not commute with
a reflection. Globally, a self-adjoint reciprocal involution on `TS2` would split it into real
eigenline bundles; the unit sphere has Gauss-Bonnet Euler number two, so that global line-field split
is obstructed. A flat torus permits global axes, but then a continuous family survives and the
metric still does not select one.

This does not invalidate the parent's bounded static profile. It shows that “add a second pair” is
not by itself a global solution. The angular topology and connection must participate.

## Relationship to the Hopf clue

The reflection-lift theorem explains why the Hopf-exchange basis repeatedly produces the right
local algebra: it is one representative of the reflection conjugacy class, and `J_q R` supplies the
complementary reciprocal reflection.

But the same local theorem also works for the axis-reflection lift. It does not select toric spatial
periods, a spin lift, `S3` caps, a Hopf section, the round `S2` carrier, or the `L2+L4` action. Those
remain downstream conditional diagnostics.

The result therefore strengthens the structural connection without using carrier success as a
merit filter.

## Scientific consequence

The metric-wide audit does not support adopting “full two-pair Reciprocity” as already derived. It
does support a more exact candidate completion:

> Complete Reciprocity may require a reflection-type finite-cell seal whose metric-defined
> complementary pair extends through the cell as a globally integrable reciprocal reduction.

That sentence contains two genuinely missing derivations:

1. why the complete physical seal has the reflection angular class rather than `+I` or `-I`; and
2. why the seal-local reciprocal reduction must extend through the bulk with reduced holonomy.

If both follow from the metric/finite-cell foundation, the full two-pair structure would no longer
be inserted. If either fails, the direct transverse-zero realization remains the honest founding
extension and the Hopf agreement stays conditional.

No new postulate, action, transport law, topology, carrier, boundary dynamics, source, mass, scale,
GPU result, or canon entry was adopted.

## Four evidence gates

1. **Preregistered:** yes, commit `d3e1a98`, before candidate-source inspection and algebra.
2. **Full space or bounded scope:** complete for the enumerated conformally natural metric,
   orientation, gradient, symmetric screen-tensor, registered seal-lift, and torsion-free conformal
   continuation candidates through second metric-derivative order; not arbitrary higher jets,
   nonlocal spectra, torsion, global covers, or dynamics.
3. **Independent verification:** separate standard-library rational/algebraic reconstruction,
   source/status replay, and exercised fail-closed mutations.
4. **Premise audit:** spacetime realization, complete lift, orientation, degeneracy, transport,
   holonomy, topology, action, carrier, bootstrap, boundary, and scale limits are explicit.

Maximum conclusion:

`UDT_METRIC_NATIVE_TWO_PAIR_SELECTOR_STATUS_CHARACTERIZED`.
