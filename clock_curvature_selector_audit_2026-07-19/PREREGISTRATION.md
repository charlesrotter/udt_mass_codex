# Clock–Curvature Selector Audit — Preregistration

Date: 2026-07-19  
Base: `674641832fe449c6fbe4a1a8ae6e6d949fd686cc`  
Branch: `codex/clock-curvature-selector-audit-2026-07-19`

## Whole question

Does the currently registered UDT foundation—Reciprocity, Common-Scale Neutrality (CSN), finite-cell structure, and bootstrap closure—force the static clock–curvature equation

`D_h^2 N + (R4/6) N = 0`

(equivalently on the WR–L branch, `D_h^2 N + (R3/4) N = 0`), or is this equation only an identity after the WR–L representative/profile has already been selected?

The bounded domain is the complete static, spherically symmetric reciprocal metric family

`ds^2 = -A(r)c^2 dt^2 + A(r)^(-1)dr^2 + r^2 dOmega^2`, `N=sqrt(A)`,

including regular finite cells with `A(0)=1`, `A(X)=0`, `A>0` on `0<=r<X`. This does not cover rotating, nonspherical, time-live, matter-coupled, or nonzero-shift geometries.

## Frame and premise ledger

- UDT metric and reciprocal clock/ruler pairing: **pinned-by-THEORY** from the current frontier and cited lineage.
- CSN as local common rescaling before physical scale/representative selection: **pinned-by-THEORY** from the current foundation ledger.
- Finite-cell seat and wall (`A(0)=1`, `A(X)=0`): **pinned-by-THEORY** only for the bounded finite-cell audit.
- Static spherical zero-shift chart and areal radius: **free-and-explored** bounded representation, not a universal UDT theorem.
- WR–L profile `A=1-r/X`: **candidate**, not assumed in the general-family test.
- Clock–curvature equation: **candidate selector**, not an accepted field equation.
- Vacuum, EH equations, Bach equations, GR observer mechanics, carrier, source, and matter action: **not assumed**.
- `c` is the terrestrial/solar observational clock anchor and `G` the gravitational scale anchor; neither supplies a length by itself: **pinned-by-THEORY/OBSERVED** as recorded at the current frontier.
- Boundary conditions beyond the finite-cell seat/wall, action boundary completion, and native source: **OPEN**.

## Preregistered derivations and adversarial tests

1. Derive `R4`, `R3`, and `D_h^2 N` for arbitrary twice-differentiable `A(r)` and reduce both proposed identities without inserting WR–L.
2. Solve the resulting profile equation. Test whether regular seat plus one finite wall selects WR–L only after the clock–curvature equation is supplied.
3. Construct the explicit deformation

   `A_epsilon(y)=(1-y)[1+epsilon*y*(1-y)]`, `y=r/X`,

   and check positivity, seat, wall, reciprocal pairing, wall asymptotics, curvature regularity, and the clock–curvature residual. This is a bounded non-entailment countermodel only to the extent that it satisfies each enumerated premise; it is not automatically a complete UDT universe.
4. Rewrite the four-dimensional identity covariantly as a contraction involving the selected static clock direction, and record every extra structure needed to do so.
5. Apply a local common-scale transformation `g -> exp(2 sigma) g`, `N -> exp(sigma)N`. Determine whether zero clock–curvature residual is preserved. Also test whether any simple spatial operator `D_h^2 N + a R3 N` can be locally scale-covariant with the physical lapse weight.
6. Audit Reciprocity, CSN, finite-cell structure, bootstrap, angular geometry, action choice, and boundary completion separately. Do not infer an equation from its success on WR–L.
7. Independently verify every load-bearing symbolic identity using a separate direct SymPy implementation and exercised mutation/catch proofs.

## Certification and falsification contract

The current UDT structure will count as forcing the equation only if the audit finds a premise-traceable derivation before selecting WR–L or a physical conformal representative, and the equation survives the transformations declared equivalent by CSN without an unregistered compensator or gauge choice.

The forcing claim fails if any explicitly admissible reciprocal finite-cell metric violates it, if the equation is obtained only by substituting WR–L, or if local CSN transformations do not preserve its zero set.

The deformation counts as a complete countermodel only if every relevant foundational premise is explicitly verified. If its status under an unresolved premise is unknown, the maximum language is “non-entailment within the stated reciprocal finite-cell representation,” not a complete-foundation counterexample.

## Maximum allowed conclusion

At most this audit may conclude one of:

- `DERIVED` across the stated complete metric family;
- `UNIQUE-CONDITIONAL` as a profile selector only after an additional declared equation/representative premise;
- `CONDITIONAL` post-scale candidate;
- `OPEN`.

It may not canonize a field equation, choose an action, derive a carrier/source/mass, claim a complete bootstrap, launch GPU work, or resume repository reorganization.

Because a fresh external-model adversarial review is not presently authorized, a positive load-bearing return cannot exceed `VERIFIED-WITH-CAVEATS` even after independent in-package algebraic replay.

