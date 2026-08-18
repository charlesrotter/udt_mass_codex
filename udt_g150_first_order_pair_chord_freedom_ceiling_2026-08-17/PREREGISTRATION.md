# G150 preregistration — first-order pair-chord freedom ceiling

Date: 2026-08-17

## Question

Does regular local metric/query kinematics impose any additional universal algebraic relation among

\[
\dot\phi_{\rm pair},\qquad a_n,\qquad \Omega\in H_{\rm pair}
\]

beyond the exact G148 decomposition and orthonormal-frame identities?

The decisive test is constructive. If an arbitrary quadruple
`(p,a,omega_2,omega_3)` can be realized at a marked point by one smooth regular metric and pair
immersion at any finite pair depth, then no nontrivial universal algebraic first-order relation can
follow from metricity and pair regularity alone.

## Exact bounded regime

- local flat Lorentz metric `eta=diag(-1,1,1,1)` used as a counterfamily, not imported dynamics;
- one smooth quadratic timelike pair immersion near a marked point;
- arbitrary positive pair scales `T,L`, hence arbitrary finite
  `phi_pair=(1/2)log(L/T)` and arbitrary common scale;
- first derivatives along the normalized pair clock only;
- no field equation, action, source, bootstrap, observations, boundary, global completion, or
  physical query restriction;
- null, degenerate, cut, singular, global, and asymptotic endpoint strata excluded.

## Registered construction

At the marked point choose

\[
J_0=T e_0,\qquad J_1=L e_1,\qquad T,L>0,
\]

and write

\[
A=F_{\tau\tau},\qquad B=F_{\tau\sigma}.
\]

The preregistered proposed output map is

\[
\dot\phi_{\rm pair}=-\frac{A^0}{2T^2}+\frac{B^1}{2TL},
\qquad
a_n=\frac{A^1}{T^2},
\qquad
\Omega=\frac{B^2}{TL}e_2+\frac{B^3}{TL}e_3.
\]

For arbitrary target `(p,a,omega_2,omega_3)`, the registered right inverse is

\[
A=(0,aT^2,0,0),\qquad
B=(0,2pTL,\omega_2TL,\omega_3TL).
\]

The symbolic output Jacobian with respect to `(A0,A1,B1,B2,B3)` must have rank four for all
`T,L>0`. The unused jet directions are allowed to remain free.

## Premise ledger

| item | status | ownership |
|---|---|---|
| G148 first-jet identity | `DERIVED` on supplied smooth regular pair | frozen source |
| G149 genuine spacetime realization | `VERIFIED_WITH_CAVEATS` | frozen source |
| flat local counterfamily | `CHOSE_MATHEMATICAL_COUNTERFAMILY` | sufficient only against universal kinematic relation |
| arbitrary quadratic pair jets | `free-and-explored` | no physical query law claimed |
| target quadruple | symbolic arbitrary real values | not observations or fit |
| physical history/query restriction | `OPEN` and omitted | may later reduce freedom |

## Certification and falsification contract

The bounded theorem requires:

1. exact regularity and orthonormality at the marked point;
2. direct derivation of all four output components from the pullback and normalized pair frame;
3. exact rank four of the output map for arbitrary positive `T,L`;
4. exact symbolic recovery of arbitrary targets under the registered right inverse;
5. independent numerical replay of every preregistered rational target;
6. catches for missing normalized-clock factor, missing screen channel, and a forced false relation;
7. explicit restriction of the no-go to universal algebraic first-order relations under the stated
   unrestricted smooth-query class.

The theorem fails if the rank drops generically, a target cannot be realized, or independent replay
disagrees.

## Maximum conclusion

At most:

```text
UNIVERSAL_ALGEBRAIC_FIRST_ORDER_PAIR_CHORD_SELECTOR_ABSENT_IN_UNRESTRICTED_SMOOTH_REGULAR_METRIC_QUERY_KINEMATICS__
DOTPHI_AN_AND_TWO_OMEGA_COMPONENTS_CONSTRUCTIVELY_INDEPENDENT_AT_ANY_FINITE_PAIR_DEPTH__
G148_IDENTITY_AND_FRAME_ORTHOGONALITY_EXHAUST_THIS_BOUNDED_FIRST_ORDER_KINEMATIC_CONTENT__
PHYSICAL_QUERY_RESTRICTIONS_CURVATURE_GLOBAL_COMPLETION_DYNAMICS_AND_REGIME_LAW_OPEN
```

