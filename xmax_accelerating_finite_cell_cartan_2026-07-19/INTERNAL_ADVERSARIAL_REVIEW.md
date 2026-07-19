# Internal adversarial correction layer

Date: 2026-07-19

Review status: `REVISE`, then corrected. The core curvature result survived.

A proposed fresh external-model review was not transmitted because explicit authorization to send
private repository contents to that service was absent. The package therefore does not claim the
fresh-context gate. Instead, the load-bearing algebra was attacked through a separate direct
coordinate Christoffel/Riemann implementation and a manual convention/scope audit. The final grade
remains `VERIFIED-WITH-CAVEATS`, not settled physics.

## Correction 1 — finite holonomy sign

For the registered transport convention

\[
 dV+\omega V=0,
\]

parallel transport is `P exp(-integral omega)`. On the restricted time-depth face the connection has
only one commuting `SO(1,1)` generator and Stokes gives `integral_boundary omega=Phi01 J01`.
Therefore

\[
 H_{01}=\exp(-\Phi_{01}J_{01}),
\]

not `exp(+Phi01 J01)` in that convention. Reversing the loop orientation or generator sign reverses
the rapidity sign, while its magnitude and the conclusion of acceleration independence survive.

The derivation result, report, ledgers, independent verifier, and catch-proofs were corrected.

## Correction 2 — positional beta versus beta derivatives

The first draft said all `beta` dependence disappeared from the Cartan curvature. That was too broad.
The exact distinctions are:

- `beta_dot` and `beta_double_dot` generate no curvature in any of the six planes;
- the fully expanded Lie-algebra-valued two-forms in fixed unprimed coordinate one-forms also contain
  no positional `beta` for this representative;
- the orthonormal coefficients and coframe blades separately depend on `psi=phi-beta`, so a measured
  frame component can retain positional-depth dependence; and
- spin-connection component cancellation is stated only in the chosen pulled-back coframe gauge,
  because connection coefficients are gauge-dependent.

The load-bearing pure-acceleration result survives. A stronger claim of position-independent
curvature does not.

## Correction 3 — coordinate cell versus physical UDT cell

The registered integrations use fixed symbolic coordinate faces. They are exact mathematical cells,
not a bootstrap-selected physical UDT cell. A comparison of the same physical cell in two frames must
transform its boundaries; its holonomy is preserved by pullback naturality. The package now states
both facts and does not infer a cell size, norm, or observational threshold.

## Independent route that survived

The verifier independently constructs the full coordinate metric for

\[
 \beta(t)=\tfrac12 a t^2,
 \qquad
 \sigma(u,v)=p u^2+q v^2,
\]

computes all coordinate Christoffels and Riemann components directly, and projects them into the
orthonormal frame. It reproduces the nonzero `01`, `02`, `03`, and `23` curvature forms, the zero
`12` and `13` forms, and zero derivative with respect to the free acceleration parameter. It also
recomputes the time-depth Stokes flux and exact Lorentz holonomy independently of the primary
exterior-form engine.

## Claims that survive

- All six Cartan curvature planes of the declared warped-product representative are computed.
- Reciprocal velocity and acceleration generate no curvature.
- The time-depth coordinate face has exact commuting holonomy with signed rapidity `-Phi01` in the
  registered convention.
- The angular curvature combines `Kbar` with `-1/L^2`.
- Zero integrated angular flux fixes only an area/topology relation if imposed; it does not select a
  round metric.
- Generic finite flux is not generic finite holonomy.
- The physical UDT cell and equivalence crossover remain open.

## Evidence-gate grade

1. Preregistered: `PASS`.
2. Full space or bounded scope: `PASS` for all six planes of the declared representative; general
   twist/shear remains explicitly excluded.
3. Independent load-bearing implementation: `PASS`.
4. Every premise audited: `PASS_WITH_CAVEAT`; the internal audit corrected the sign, gauge, and cell
   semantics, but the requested fresh external context was not authorized or run.
