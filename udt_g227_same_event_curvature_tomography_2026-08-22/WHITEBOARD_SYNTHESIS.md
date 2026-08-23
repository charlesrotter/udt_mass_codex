# G227 whiteboard synthesis — what can actually constrain a null network?

Date: 2026-08-22

## Question

After G226 derived the conformal-symplectic phase evaluator on each supplied composable null chain,
does a finite family of such germs at one event obey any further metric-native compatibility, or
does the metric merely evaluate arbitrary independently supplied edge data?

## Conference verdict

Abstract graph composition is not the missing restriction.  An arbitrary assignment of
`CSp+(4,R)` matrices to the generating edges of a free path groupoid extends functorially to paths.
Multiplier composition, endpoint-gauge cancellation, inverse ruler carry, and loop conjugacy are
therefore important typing and evaluation laws, but they do not by themselves force different
outgoing directions to belong to one metric.

The first genuinely cross-direction metric-native joint is **common-curvature realizability**.
At one event, every infinitesimal null screen tide must have the form

\[
\mathcal T_k(X,Y)=R(X,k,Y,k)
\]

for one algebraic Riemann tensor `R`, not one freely chosen symmetric matrix per direction.  This
gives a finite-dimensional, falsifiable compatibility condition on independently assigned phase
germs.

## The silent mode

In four dimensions the algebraic Riemann space has dimension 20.  The constant-curvature tensor

\[
K_{abcd}=g_{ac}g_{bd}-g_{ad}g_{bc}
\]

is invisible to every null screen because `g(k,k)=g(X,k)=0` implies

\[
K(X,k,Y,k)=0.
\]

The complete null tidal sky can therefore recover at most 19 curvature modes.  The conjectured
sharp result is that this is the only null-silent mode.  One non-null sectional/timelike tidal
datum is nonzero on `K` and should restore rank 20.

## Why this is newer than G114 and G226

- G114 classified common-source loops, beam-image Lagrangian intersections, and matrix holonomy.
- G226 joined the proper-clock multiplier, inverse ruler carry, screen rotation, and full Jacobi
  phase on supplied chains.
- G227 asks whether multiple **infinitesimal directional generators at one event** are projections
  of one and the same 20-component curvature tensor.

The proposed result is a realizability and tomography theorem, not another loop-closure rule.

## Hard ceiling

Success would reject synthetic collections of directional tides that cannot come from one metric
jet.  It would also reconstruct the local algebraic curvature after one non-null datum is added.
It would not choose the numerical curvature values, a global metric history, actually populated
observers, physical emission branches, dynamics, sources, or boundary conditions.  A complete
valued compatible relation network may itself encode the metric history; compatibility does not
generate its values from finite anchors.

## Strong counterexample to branch selection

Flat `R x T^3` admits distinct winding null geodesics with identical flat curvature, unit clock
ratio, and flat Jacobi phase.  Common curvature, Bianchi identities, G226 composition, and all
local compatibility gates can hold while no one winding branch is selected.  G227 must not be
promoted into a population or preferred-path theorem.

