# Exact configuration architecture

## 1. Three spaces must not be conflated

The current evidence distinguishes three different spaces.

1. The physical configuration arena contains the complete Lorentzian metric `g` and, once selected,
   its finite-cell domain, topology, seams, and boundary data.
2. The relational query space contains ordered observer/ruler pairs `(u,n)` and path-labelled arrows
   `gamma`. These say which comparison is being requested.
3. The readout space contains objects derived from the first two layers, including metric transport,
   holonomy, and the conditional reciprocal endomorphism `X_lambda(u,n)`.

An element of query space is not thereby a physical field. A readout depending on a query is not
thereby another physical degree of freedom.

## 2. The exact pair-indexed family

For a supplied future unit timelike observer `u` and orthogonal unit spacelike ruler `n`, define

```text
P_screen = I-P_u-P_n,
X_lambda(u,n) = -P_u + P_n + lambda P_screen.
```

This endomorphism is metric-self-adjoint and has the founded `-1,+1` characters on the supplied
clock/ruler pair. Screen `SO(2)` rotations commute with it, so an oriented screen coframe is not
needed to define this scalar-screen family.

The family is conditional on supplied `(g,u,n,lambda)`. Current evidence does not make it a new
endomorphism field independent of those arguments.

## 3. The democratic lift is a fiberwise special stratum

Using `P_space=I-P_u`, rewrite the family as

```text
X_lambda(u,n) = -P_u + lambda P_space + (1-lambda)P_n.
```

At `lambda=1`,

```text
X_1(u,n) = -P_u + P_space,
```

so the result is independent of `n` for one fixed `u`. This is exactly the conditional democratic
clock-versus-all-space `1+3` lift.

Thus the single local `1+3` lift and the pair-indexed family are not algebraically incompatible
ontologies. The first is a fiberwise stratum of the second. The reverse containment fails: for
generic `lambda != 1`, changing `n` changes `X_lambda`.

This identity does not select `lambda=1` and does not supply a global timelike observer line. A
globally selected single lift and the full query-indexed family can still differ in their global
realization.

## 4. What belongs to the physical metric

The complete metric remains the physical arena. Its angular and pair-screen components are metric
content, even when a chosen chart or coframe makes some cross terms vanish locally. Therefore the
honest unselected bulk candidate is

```text
delta g: full symmetric metric variation,
```

including angular and mixing slots.

This does not prove that every metric tangent survives a future native variation law. It says that
none may be removed now by an unselected complete-coframe lift. Likewise, the seven triangular
extension tangents previously classified are available metric responses in that bounded chart, not
seven fields or seven propagating modes.

## 5. What is gauge

Coordinate changes, local Lorentz coframe changes, and screen `SO(2)` orientation are presentation
directions for the current metric/endomorphism readout. They are quotiented rather than counted as
independent physical variations. A future theory with an independently physical coframe would be a
different premise branch and is not current UDT authority.

## 6. What founded `phi` is—and is not

The foundation derives the additive logarithmic coordinate of the reciprocal pair:

```text
P(phi)=diag(exp(-phi),exp(phi)).
```

This fixes the abstract character and composition law. It does not itself give a functional

```text
delta[g; gamma,(u,n), ...]
```

assigning a physical signed depth to every typed spacetime arrow. Until such a functional is
derived, `delta phi` is not an independent native bulk variation. If the functional is eventually
metric-derived, its variation will be induced by variation of its actual arguments rather than
automatically adding a new scalar field.

## 7. What `lambda` is

`lambda` is the unselected transverse-screen response parameter of the bounded reciprocal
representation family. Comparing constant values is a family or stratum scan. No current source
licenses `lambda(x)`, its gradients, or an independent Euler-Lagrange variation. Calling it a local
field would invent dynamics.

The values `+1`, `0`, and `-1` remain exact notable strata, not selected physics.

## 8. Global and boundary data

Topology, quotient, cap, seam, and complete-branch labels are global sectors, not ordinary
infinitesimal bulk directions. Boundary embedding and boundary data may eventually be fixed or
varied, but the current finite-cell structure has not selected which. A complete variation domain
must state both the bulk tangent space and these global/boundary rules.

## 9. The smallest supported scaffold

The smallest current type-correct scaffold is a stack of layers:

```text
physical metric arena
  + global completion data (open)
  + presentation quotient
  + observer-pair path query groupoid
  + metric-derived relational geometry
  + conditional reciprocal representation bundle
  + physical signed-depth functional (open)
  + downstream response/matter/action (open or conditional).
```

This stack prevents category errors and double counting. It is a derived type organization, not a
selected complete physical configuration, action, or dynamics.

## 10. Exact remainder

The following selections are still required before a complete off-shell domain exists:

- complete founded metric extension and global finite-cell branch;
- the screen response `lambda` or a more general native lift;
- metric-native signed depth on typed arrows;
- physical pair/path/event-pairing rule;
- boundary embedding, boundary data, and their allowed variations; and
- the admissible bulk-plus-boundary variation domain itself.

Response, integrability, action, carrier, source, density closure, mass, and dynamics remain
downstream.
