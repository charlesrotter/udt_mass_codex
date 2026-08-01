# Stability/action boundary bridge — exact derivation

## 1. Typed question

Let `V_route` be the tangent space of one registered action route and let `V_F01` be the exact
conditional F01 tangent space in the variables `(p,f,h,lambda/mu)`, with its separate R05/R06 and
Dirichlet/free-right domains. An action-to-F01 boundary bridge requires more than equations with a
similar derivative count. It requires an explicit map

```text
J : V_F01 -> V_route
```

on a common background such that all of the following can actually be pulled back:

```text
J* (bulk linearization),
J* (boundary one-form),
J* (boundary Hessian),
and the admissible trace domain.
```

An on-shell embedding, equality of bulk equations, an action reduction, pullback of a boundary
one-form, and equality of boundary Hessians are different statements. None implies all the others.

The frozen source census contains no registered `J` for C2/Bach, EH, or the proposed two-stage
route. More importantly, the gate audit identifies the missing mathematical data rather than
arguing from vocabulary absence: no shared F01 background, field identification, tangent map,
trace-domain image, or boundary-Hessian pullback is supplied.

## 2. What derivative order does say

For a one-dimensional second-order control,

```text
L2 = (u')^2 / 2,
delta integral L2 dx = integral (-u'') v dx + [u' v].
```

The boundary one-form contains the value trace `v`.

For a fourth-order control,

```text
L4 = (u'')^2 / 2,
delta integral L4 dx = integral u'''' v dx + [u'' v' - u''' v].
```

The boundary one-form contains both `v` and `v'`. This justifies the limited structural analogies:
EH-like second-order bulk equations naturally expose a lower boundary jet, while a C2/Bach-like
fourth-order bulk exposes a larger polarization. It does not identify `u` with any F01 variable,
construct the P4 response, preserve R05/R06, or fix a wall Hessian.

## 3. Exact counterfamily: same bulk, different boundary Hessian

For any constant `kappa`, define

```text
L_tilde = L + d(kappa u^2 / 2)/dx.
```

The added term has zero bulk Euler derivative. Therefore `L` and `L_tilde` have exactly the same
bulk equation. Their boundary one-forms differ by

```text
Delta Theta = kappa u v,
```

and their second variations differ by

```text
Delta H_boundary[v,v] = kappa v^2.
```

Since `kappa` is arbitrary, a shared bulk Euler equation or derivative order cannot determine the
quadratic boundary response. This is the same load-bearing distinction already exposed by the
frozen Arm-C boundary-charge algebra, now applied directly to the F01 ownership question.

## 4. Route adjudications

### Pre-scale C2/Bach

Historically, the registered result is a `UNIQUE-CONDITIONAL` bulk class under unrestricted
metric-only variation and the other enumerated class premises. Current premise rows G04/G10 make
strong local CSN challenged and inactive unless Charles explicitly reauthorizes a stated
counterfactual branch. The C2/Bach route is therefore
`INACTIVE_WITHOUT_STRONG_CSN_PREMISE__COUNTERFACTUAL_ONLY` here, not an active action candidate.
Even in that counterfactual class, its fourth order supplies only a relevant
boundary-polarization analogy. Its reciprocal-constraint implementation, finite-cell
fourth-order boundary/corner action, common F01 background, reduction to `(p,f,h,lambda/mu)`, and
trace-domain map are all absent. Its boundary functional is expressly open. The route cannot own
the F01 second germ.

### Post-scale EH

The registered result is `CONDITIONAL` after a physical representative has been selected. It has a
second-order boundary-type analogy, but the representative, F01 background, field/tangent map,
finite-cell GHY/corner prescription, reference, normalization, and trace-domain image are absent.
The required bootstrap selection may not be assumed. The route cannot own the F01 second germ.

### Proposed two-stage bridge

The registered two-stage idea has the form

```text
pre-scale class -> selected representative -> post-scale dynamics.
```

Neither arrow has been completed as the map required here. In particular, there is no theorem
matching fourth- and second-order degrees of freedom, tangent quotients, boundary polarizations,
charges, or F01 trace domains across the stages. It remains a diagram, not a bridge.

## 5. Relation to the verified F01 result

Inside its declared conditional P4 model, F01 has an exact joint Hessian and the four local domains
are all index one after the constant `lambda/mu` direction is restored. That internal map is real
and is retained as `YES_CONDITIONAL_ONLY`. The present audit does not alter that calculation.

What remains open is the inverse ownership question: whether a native complete-metric law selects
the P4 response and fixes the Hessian-active second wall germ. The action routes do not currently
answer it.

## 6. Result

`PARTIAL_ANALOGIES_ONLY__F01_BOUNDARY_BRIDGE_OPEN`

The analogies are real but insufficient. Zero exact action-route maps survive all twelve gates.
No action, physical boundary, source, carrier, bootstrap operation, or stable matter is selected.
