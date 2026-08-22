# G223 preregistration

Date: 2026-08-22

## Hypotheses

Let `Sigma` be one supplied regular Lorentzian pair surface with null vertical line
`V=ker(d pi)`. In an adapted chart `i`, set

\[
K_i=\partial_{\lambda_i},
\qquad J_i=\partial_{y_i},
\qquad a_i=-h(J_i,K_i)>0.
\]

Allow smooth positive foliation-preserving affine overlaps

\[
y_j=f_{ij}(y_i),
\qquad
\lambda_j=\alpha_{ij}(y_i)\lambda_i+b_{ij}(y_i).
\]

## Preregistered claims to test

1. The exact tangent and coefficient laws are

   \[
   K_j=\alpha^{-1}K_i,
   \quad
   J_j=(f')^{-1}(J_i-q\alpha^{-1}K_i),
   \quad
   a_j=a_i/(f'\alpha),
   \]

   where `q=alpha' lambda_i+b'`.

2. The metric canonically defines a nondegenerate mixed line pairing

   \[
   \mathcal A\in (T\Sigma/V)^*\otimes V^*,
   \qquad
   \mathcal A([X],v)=-h(X,v),
   \]

   represented by `a_i dy_i tensor [d lambda_i]`.

3. After choosing a clock coframe `tau_i=dy_i`, the ruler density
   `vartheta_i=a_i[d lambda_i]` transforms with inverse clock weight,

   \[
   \vartheta_j=(f')^{-1}\vartheta_i.
   \]

   It is a genuine global vertical covector only after a compatible clock trivialization is fixed.

4. The oriented pair area form

   \[
   \epsilon_h=a_i,dy_i\wedge d\lambda_i
   \]

   is invariant under all declared positive overlaps.

5. A chosen full representative `a_i d lambda_i` is not overlap invariant when `alpha` or `b`
   varies with `y`. Its closedness is therefore not the invariant global obstruction.

6. A local scalar `s_i` satisfying

   \[
   [ds_i]=\vartheta_i\quad\hbox{on }V
   \]

   always exists on an interval-fiber chart, with a representative
   `s_i=a_i(y_i) lambda_i+s_0(y_i)`. Requiring the stronger equality
   `ds_i=a_i d lambda_i` in that same horizontal chart forces `partial_y a_i=0`.

7. A global ordinary scalar requires, in addition, a global clock trivialization and compatible
   fiber potentials: zero vertical periods and a Cech overlap mismatch that is a coboundary. With a
   global source section and interval fibers these conditions are sufficient.

8. G216 clock composition supplies the transition weight on clock lines. It does not supply an
   isomorphism between the vertical lines of distinct `AB` and `BC` ribbons. If such vertical
   gluing maps are supplied and obey their own cocycle, `mathcal A` and the clock-trivialized ruler
   densities carry functorially. Otherwise no full ruler-density product is defined.

9. The foliation-preserving null overlap group and G214's clock-line-preserving triangular group
   intersect in the diagonal subgroup at a point. On that common subgroup the G214 determinant
   density and the G223 mixed-pairing law agree exactly.

## Mandatory controls

1. identity, inverse, and triple-overlap composition for `(f',alpha,q)`;
2. direct metric congruence under a nonconstant affine scale and origin shift;
3. invariance of `mathcal A` and the oriented area form;
4. inverse clock weight of `vartheta`;
5. explicit example where `d(a d lambda)` changes under an allowed affine chart change while the
   vertical density class and metric are unchanged;
6. local exact fiber potential for nonconstant `a(y)`;
7. closed-fiber positive-period obstruction;
8. G214 diagonal intersection and G216 chain-rule compatibility;
9. reject any claim that scalar clock composition alone identifies distinct vertical bundles.

## Falsification contract

The landing fails if any regular retained overlap violates the tangent, metric, density, area, or
cocycle laws; if local fiber integration fails on an interval chart; if a chart-dependent exterior
derivative is promoted to an invariant obstruction; or if distinct pair ribbons acquire a product
without an explicit vertical gluing map.

## Maximum conclusion

At most:

```text
METRIC_OWNS_NONDEGENERATE_CLOCK_RULER_LINE_PAIRING_ON_SUPPLIED_NULL_RIBBON
__RULER_DENSITY_HAS_EXACT_INVERSE_CLOCK_OVERLAP_WEIGHT
__LOCAL_FIBER_COORDINATE_EXISTS_BUT_GLOBAL_SCALAR_NEEDS_TRIVIALIZATION_AND_CECH_PERIOD_GATES
__G216_CLOCK_COMPOSITION_DOES_NOT_BY_ITSELF_SUPPLY_CROSS_RIBBON_VERTICAL_CARRY
```

