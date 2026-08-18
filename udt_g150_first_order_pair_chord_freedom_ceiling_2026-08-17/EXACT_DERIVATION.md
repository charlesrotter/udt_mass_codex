# G150 exact derivation — first-order pair-chord freedom ceiling

Date: 2026-08-17

## Result

Within unrestricted smooth regular local metric/query kinematics, there is no additional universal
pointwise algebraic relation among the four named components

\[
\left(\dot\phi_{\rm pair},a_n,\Omega_2,\Omega_3\right).
\]

They can be chosen arbitrarily at any finite pair depth. This closes only that pointwise selector
search. It does not exclude restrictions from a physical query class, other first-order objects,
the next pair-frame jet, metric curvature, dynamics, global completion, or observations.

## Exact counterfamily

Use a local Minkowski chart only as a mathematical counterfamily,

\[
g=\operatorname{diag}(-1,1,1,1),
\]

and a smooth quadratic pair immersion whose marked-point tangent vectors are

\[
J_0=T e_0,\qquad J_1=L e_1,\qquad T,L>0.
\]

The pair metric and depth are

\[
h=\operatorname{diag}(-T^2,L^2),
\qquad
\phi_{\rm pair}=\frac12\log\frac LT.
\]

Thus every positive `T,L` is regular and every finite pair depth is represented. Let

\[
A=F_{\tau\tau},\qquad B=F_{\tau\sigma}.
\]

Direct differentiation of the pullback and normalized frame gives

\[
\boxed{
\dot\phi_{\rm pair}
=-\frac{A^0}{2T^2}+\frac{B^1}{2TL},
\qquad
a_n=\frac{A^1}{T^2},
\qquad
\Omega=\frac{B^2}{TL}e_2+\frac{B^3}{TL}e_3.
}
\]

These are not assumed formulas. The production script derives them from `h`, `partial_tau h`,
`u`, `n`, and their normalized clock derivatives.

## Rank and right inverse

For output order `(dot(phi),a_n,Omega_2,Omega_3)` and jet-variable order
`(A0,A1,B1,B2,B3)`, the Jacobian is

\[
\begin{pmatrix}
-1/(2T^2)&0&1/(2TL)&0&0\\
0&1/T^2&0&0&0\\
0&0&0&1/(TL)&0\\
0&0&0&0&1/(TL)
\end{pmatrix}.
\]

The minor using `(A1,B1,B2,B3)` is

\[
-\frac{1}{2L^3T^5},
\]

which is nonzero for all `T,L>0`. Therefore the map has rank four everywhere in the declared
regular family.

For arbitrary reals `(p,a,omega_2,omega_3)`, choose

\[
A=(0,aT^2,0,0),
\qquad
B=(0,2pTL,\omega_2TL,\omega_3TL).
\]

Substitution returns exactly

\[
(\dot\phi,a_n,\Omega_2,\Omega_3)=(p,a,\omega_2,\omega_3).
\]

Because these jets come from the explicit quadratic polynomial

\[
F(\tau,\sigma)=J_0\tau+J_1\sigma
+\tfrac12A\tau^2+B\tau\sigma+\tfrac12C\sigma^2,
\]

mixed partial compatibility is automatic. Regularity and timelikeness persist in a sufficiently
small neighborhood by continuity.

Surjectivity onto all of `R^4` rules out every nontrivial universal algebraic equation involving
only these four outputs in the declared class, not merely linear relations.

The remaining four-dimensional kernel in the eight components of `(A,B)` carries other first-order
kinematics. For example, `A2,A3` can contribute screen components of `nabla_u u`, `B0` contributes
to shift change, and an unused `A0,B1` combination contributes common-scale change. G150 does not
classify or eliminate those objects.

## Separate implementation replay

Three frozen rational targets were rebuilt from the full pullback and normalized-frame derivative
without importing production code. All were recovered with maximum absolute error `5.55e-17`;
regularity, orthonormality, and screen orthogonality passed at float precision. Because this replay
closely mirrors the production algebra, it is regression evidence. The fresh adversarial reviewer
independently rederived the theorem from the explicit quadratic immersion.

Injected readout mutations omit normalized clock conversion or set both screen components to zero;
both fail the arbitrary-target recovery. The registered targets also directly violate a forced
`dot(phi)=a_n` relation.

At `phi_pair=0`, the pair frame `n` and its `Omega` remain well-defined and free, but the working
position vector `xi=X_max tanh(phi_pair)n` vanishes. Consequently the `a_n` and `Omega` terms in
`nabla_u xi` carry zero `tanh(phi_pair)` weight at that point. Their freedom is a pair-frame result,
not a claim of a nonzero positional chord at coincidence/neutral depth.

## Exact scope ceiling

What is closed:

- no universal pointwise algebraic selector among these four named readouts follows from smooth local
  metricity, pair regularity, and unrestricted pair jets;
- another atlas of arbitrary first-order witnesses cannot discover such a selector.

What is not closed:

- physically admissible-query restrictions;
- relations involving other first-order objects or the kernel jet combinations;
- differential relations involving derivatives of these outputs;
- the next pair-frame jet, metric curvature, Jacobi, or differential relations;
- field equations, dynamics, action, source, bootstrap, global completion, or observations;
- asymptotic, null, degenerate, cut, singular, or coincidence strata.

## Maximum conclusion

```text
UNIVERSAL_ALGEBRAIC_FIRST_ORDER_PAIR_CHORD_SELECTOR_ABSENT_IN_UNRESTRICTED_SMOOTH_REGULAR_METRIC_QUERY_KINEMATICS__
DOTPHI_AN_AND_TWO_OMEGA_COMPONENTS_CONSTRUCTIVELY_INDEPENDENT_AT_ANY_FINITE_PAIR_DEPTH__
NO_ADDITIONAL_UNIVERSAL_ALGEBRAIC_RELATION_AMONG_THESE_FOUR_OUTPUTS__
PHYSICAL_QUERY_RESTRICTIONS_NEXT_PAIR_FRAME_JET_METRIC_CURVATURE_GLOBAL_COMPLETION_DYNAMICS_AND_REGIME_LAW_OPEN
```
