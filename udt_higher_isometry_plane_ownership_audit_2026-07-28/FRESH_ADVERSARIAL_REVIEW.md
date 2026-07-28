REFUTED

The package’s exact algebra largely passes, but its load-bearing generic-selection theorem is not established.

Concrete findings:

1. The `3×3` orbit Gram matrix, determinant `-b c_E²`, Lorentzian inertia, response matrix, characteristic polynomial, and leakage formulas are correct on the principal-orbit region `b>0`. At toric caps `b=0`, the orbit rank drops and `G₃⁻¹X(G₃)` is undefined; R01/R02 need that explicit scope.

2. The plane parameterization
   `span(K+rV+sY, mV+nY)` exhausts the relevant subgroups. Allowing real `(m,n)` is an exhaustive superset of closed rational circle lines. Constant Gram determinant is invariant under constant plane-basis changes.

3. The generic proof has a fatal quantifier error. It proves that determinant constancy as a polynomial identity under independently varied formal variables forces `n=0`, then `s=0`. It does not prove uniqueness for a fixed generic metric.

   In the admitted effective `T²` family, all orbit invariants `u,f,b` are functions of one cohomogeneity-one coordinate `ρ`. A fixed metric supplies only

   ```text
   dF/dρ = F_u u' + F_f f' + F_b b' = 0,
   ```

   allowing cancellations. The three first jets are not independently available tangent directions. Moreover, a curve `ρ↦(u,f,b)` locally necessarily satisfies functional relations, so “no functional relation” does not define the claimed realizable open stratum. A transversality/residual-set theorem or fixed-profile necessary-and-sufficient classification is missing.

   Therefore R03, R04, R08, the first sentence of `AUDIT_REPORT.md`, and
   `GENERIC_SELECTION_WITH_EXACT_EXCEPTIONAL_MULTIPLE_PLANE_STRATA` must be downgraded. The algebra currently proves only family-wide identity robustness of `span(K,V)`; generic fixed-metric uniqueness remains `OPEN`.

4. The preregistered classification of response rank, eigenlines, invariant subspaces, and every degeneracy was not completed. The characteristic polynomial and selected `df=0`/reciprocal-rate strata are insufficient as an exhaustive degeneracy atlas.

5. The smooth countercontrol is valid. With
   `f=cos(2η)`, `u=1+ε sin²(2η)`, and spatial metric `u⁻¹g_round`, the cap expansions are smooth, the slice is compact and complete, and both `(1,1)` and `(1,-1)` circle actions are primitive, period-`2π`, and free. The isometry `(z₁,z₂)↦(z₁,\bar z₂)` exchanges them; this strengthens the natural nonselection conclusion. Universal unique-plane selection is therefore genuinely refuted within the bounded family.

6. The theorem of exactly two unoriented primitive free circle lines for unimodular two-cap `S³` is correct. There is no orientation or enumeration-bound error. An additional independent census passed for 616 cap bases.

7. The distinction between full `D₃` response and restricted plane-by-plane response is mathematically honest. Neither is currently a complete metric-only selector.

8. Dependence on the chosen `A,V` and `f=A(Y)` is adequately disclosed as conditional on the registered descended Hopf family. Founded `phi` enters the clock diagnostic, not the metric-only constant-area scan. No forbidden physical selection was found.

9. The Berger/round rows are not supported by the production script, independent verifier, or frozen-source evidence. They are plausible standard controls but must receive explicit derivations or be downgraded to unverified illustrations. The 24 mutation catches mostly protect stored labels/counts; they do not catch the genericity quantifier failure.

Exact reruns:

- Production: exit `0`, 135/135 checks; stdout byte-identical, SHA-256 `f8ad7c7c339b71ec6e86c19c8a638e7f6aef236ff91477dbce3a9d8b0957f44`.
- Independent: exit `0`, 292/292 checks and 232 cap bases; stdout byte-identical, SHA-256 `a3808e1a41a27c6a3235c8d0b919f9714219d04b46f44691c63e383b787d580b`.
- Frozen sources: 26/26 replayed; identity SHA-256 `e85ad7db71c6041a1690973ba932a59db973253fdfedc3e40dd1a60b5977a482`.
- Current-premise verifier: `PASS`.

Maximum presently supportable conclusion: universal plane selection is refuted by an exact smooth countercontrol; the orbit algebra, topology theorem, and identity-level uniqueness calculation survive; generic fixed-metric plane selection remains open pending a valid cohomogeneity-one genericity theorem and complete exceptional-stratum classification.