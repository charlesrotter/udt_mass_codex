# G228 audit — neighboring-event curvature first variation

Date: 2026-08-23

## Landing

```text
DIFFERENTIAL_BIANCHI_NEIGHBOR_TILE_COMPATIBILITY_DERIVED_CONDITIONALLY
__FROZEN_LINE_AND_INDEPENDENT_TWO_DIRECTION_FIRST_VARIATIONS_ARE_SURJECTIVE
__EVERY_FROZEN_INDEPENDENT_THREE_DIRECTION_TILE_HAS_SIX_SYZYGIES
__FULL_FOUR_DIRECTION_STAR_HAS_TWENTY
__SCREEN_AND_JACOBI_FIRST_VARIATION_IS_CONNECTION_GAUGE_COVARIANT
```

Final bounded grade:

```text
DERIVED_CONDITIONAL__PREREGISTERED__EXACT_PRODUCTION
__INDEPENDENT_FRACTION_REPLAY__ORTHOGONAL_84_SLOT_FULL_INDEX_ANCHOR
__FRESH_THREE_AGENT_ADVERSARIAL_REVIEWED__REPAIRS_VERIFIED
```

## What was learned

G227's eventwise curvature chords do not become mutually restrictive merely by placing two of them
next to each other along one ray. Exact differential-Bianchi algebra shows:

| Directional first variations supplied | Available entries | Compatible rank | Exact restrictions |
|---:|---:|---:|---:|
| 1 | 20 | 20 | 0 |
| 2 | 40 | 40 | 0 |
| 3 | 60 | 54 | 6 |
| 4 | 80 | 60 | 20 |

All 15 nonempty subsets of the frozen rational null tetrad were classified. Every three-direction
subset gives the same `54/60` rank, and the full star reproduces the 60-dimensional algebraic
covariant-derivative-curvature module.

This answers the bounded framing question sharply: a one-chain calculation evaluates a supplied
change; it cannot constrain that change through differential Bianchi. In the frozen spanning
census, the first nonidentity neighboring-event joint is a linearly independent three-direction
congruence tile. This is necessary algebraic differential-Bianchi compatibility, not sufficiency
for a local metric 3-jet or one smooth surrounding geometry.

## Screen and phase join

In a parallel quotient screen,

\[
T'_{AB}=(\nabla_kR)(S_A,k,S_B,k).
\]

In a rotating orthonormal screen, the same statement is

\[
\mathcal D_\lambda T_E=T_E'+[\Omega,T_E]=C^TT'C.
\]

The corresponding first-order Jacobi generator is

\[
A_E=
\begin{pmatrix}
-\Omega&I\\
-T_E&-\Omega
\end{pmatrix},
\]

which is exactly Hamiltonian—and whose fundamental transfer is symplectic—when `T_E` is
symmetric and `Omega` is skew. The screen connection is therefore the required gauge carry of the
metric-derived tide, not a fitted angular instrument.

## Evidence gates currently passed

1. **Preregistered:** yes, commit `b54f4c51`, pushed before execution.
2. **Bounded scope:** yes, one event, one first curvature derivative, one frozen rational null
   tetrad, and one supplied local affine-null screen.
3. **Independent implementation:** yes. Standard-library `Fraction` code separately rebuilt the
   24-by-80 Bianchi matrix, its 80-by-60 kernel, all 15 projection images, and the screen/phase
   controls. Both implementations produced identical load-bearing matrix hashes. A second
   unreduced 84-slot tensor representation independently retained
   algebraic Bianchi and reproduced combined rank `24`, incremental differential rank `20`, module
   dimension `60`, and all subset projections.
4. **Premises audited:** yes in `PREMISE_LEDGER.tsv` and the three-agent adversarial review.

Production controls pass for all 15 subsets. Eleven repaired structural hostile catches pass,
including deleted Bianchi content, false one-ray restriction, isolated-finite-phase ambiguity,
wrong or missing screen commutators, nonsymmetric tide, nonskew connection, and deleted phase-
connection blocks.

## What this does not accomplish

- It does not prove metric-3-jet or smooth-metric realization and does not generate any curvature
  value or metric history.
- It does not select which observers, rays, emitters, or branches exist.
- It does not turn G225's pointwise least-turning screen map into physical transport.
- It does not infer curvature variation from an isolated finite G226 matrix.
- It does not provide dynamics, an action, source, matter, boundary data, `X_max`, radiative
  transfer, an observational prediction, mass, or signalling.

## Lay conclusion

One observer ray is one melody line. Even two nearby directions can vary freely at first order.
With three linearly independent neighboring directions in this frozen census, differential Bianchi
finally removes six independent combinations. That is a necessary test for one surrounding
geometry, not yet a proof that the supplied values realize one. A complete four-direction
neighborhood has twenty such restrictions.

The rotating screen is just the moving sheet music. Its connection term keeps us from mistaking a
turned page for a changed chord.
