# Exact derivation — complete-coframe physical comparison functor

## 1. Pointwise extension space

The founded two-channel generator is

```text
H=diag(-1,+1).
```

In the registered positive triangular four-coframe chart, every constant complete extension has
generator

```text
X = [[H, 0],
     [C, K]],
```

with an arbitrary `2 x 2` lower mixing block `C` and upper-triangular `2 x 2` angular block `K`.
Thus the extension fiber has four mixing plus three angular parameters: rank seven at the identity
of the registered triangular chart.

For Lorentz metric `eta=diag(-1,1,1,1)`, the infinitesimal physical metric response is

```text
S_X=X^T eta+eta X.
```

The seven infinitesimal extension tangent directions map to seven independent symmetric-metric directions. In
particular, no nonzero linear combination of these seven directions is a pure infinitesimal local
Lorentz transformation inside this triangular chart. The ambiguity changes pointwise metric
response to first order at the identity; it is not merely seven copies of the same infinitesimal
metric response. This is not a global nonlinear degree-of-freedom count or a count of physical
degrees of freedom.

The exact residual ranks are:

```text
general extension                       7
determinant one                         6
transverse metric invariant             4  (mixing remains)
no base-angular mixing                  3  (angular response remains)
both transverse invariant and no mixing 0  (spectator witness)
```

Therefore determinant one, transverse invariance alone, and no mixing alone do not select the
spectator extension. The angular and shift counterfamilies are exact nonuniqueness witnesses.

## 2. Arbitrary-generator typed path functor

Let a typed path `gamma:p->q` carry metric parallel transport `U_gamma`, a supplied additive signed
depth `rho_gamma`, and a supplied extension generator `X_p` at its source. Define

```text
X_q=U_gamma X_p U_gamma^-1,
D_p(rho)=exp(rho X_p),
A_gamma=U_gamma D_p(rho_gamma).
```

For a second arrow `beta:q->r`, transported functional calculus gives

```text
D_q(rho_beta) U_gamma=U_gamma D_p(rho_beta).
```

Hence

```text
A_beta A_gamma
=U_beta D_q(rho_beta) U_gamma D_p(rho_gamma)
=U_beta U_gamma D_p(rho_beta)D_p(rho_gamma)
=U_(beta o gamma) D_p(rho_beta+rho_gamma)
=A_(beta o gamma).
```

The corresponding reverse arrow is the exact inverse. This proof uses no special angular weight,
spectator assumption, or shift value. It works for every supplied extension member. It does require
the generator at the middle object to be the transported generator
`X_q=U_gamma X_p U_gamma^-1`. If an independently assigned section resets `X_q`, an additional
vertical transition is needed and the displayed proof no longer applies by itself.

This is a positive result: the complete extension ambiguity is compatible with exact path-groupoid
kinematics. It is also a nonselector result: composition cannot choose among parameters because all
of them compose.

The construction is conditional on a typed path, additive depth, and supplied source generator.
Calling those inputs physical is a separate selection question.

## 3. Endpoint collapse and holonomy

An endpoint-only generator independent of the retained path requires every loop holonomy `U` at
the endpoint to satisfy

```text
U X U^-1=X.
```

Infinitesimally, `X` must commute with the holonomy algebra. The registered complete twisted control
has full `so(1,3)` curvature-generated holonomy. An exact rational commutator calculation gives

```text
rank of commutator constraints = 15,
dimension of the centralizer in End(R^4) = 1,
centralizer = {alpha I}.
```

Every founded complete extension has the fixed base block `diag(-1,+1)`, so it cannot be a scalar
multiple of the identity. Therefore no such generator, when inserted on this full-holonomy
control, can descend by conjugation to one path-independent endpoint value. This tests endpoint
descent of `X`; it is not a claim that the complete transport `U_gamma` becomes path-independent.
Nor does it construct a same-class full-holonomy whole-metric representative for every extension
class. E06, E07, and E08 generators all meet the same algebraic obstruction when inserted into the
control.

This is not a universal UDT no-go. The twisted control is an exact off-shell configuration witness,
not a selected whole solution. A reduced-holonomy branch could centralize a non-scalar extension.
No active premise selects full versus reduced holonomy or makes endpoint-only semantics mandatory.

The path-labelled associated-bundle functor from section 2 survives full holonomy exactly.

## 4. Local Lorentz and physical meaning

Under an endpoint coframe change `L`, the generator transforms by conjugation,

```text
X -> L X L^-1.
```

This is enough for a typed associated-bundle object, but not for a unique bare-endpoint physical
operator. E11 names the missing descent/quotient layer. The triangular chart supplies a useful
representative and an injective pointwise metric response; it does not select a global physical
section or decide whether path labels are retained.

## 5. Mechanical twelve-class result

- E01 fixes the founded pair action but is not a complete four-slot functor.
- E02 through E05 classify residual pointwise families of ranks 7, 6, 4, and 3.
- E06 is an exact spectator witness unique only after two extra premises.
- E07 and E08 are exact angular and shift counterfamilies.
- E09 retains all seven parameters under the active physical-metric reading.
- E10 retains six parameters and additionally relies on inactive strong local CSN.
- E11 leaves local-Lorentz-independent physical descent open.
- E12 leaves profile, path, boundary, and global completion open.

Every supplied member has conditional path-labelled composition. No row supplies all twelve gates,
and no row supplies the physical observer/event arrow domain, signed depth on that domain, global
completion, `X_max` join, or response target.

## 6. All-pairs response

Given a sufficiently rich physical pair domain and a realized reciprocal-depth assignment, the endpoint clock map

```text
T_phi(A,B)=phi(B)-phi(A)
```

has infinite functional rank modulo constants in the continuum function space. On `n` discrete
observer objects its incidence rank is only `n-1`. For any supplied extension member `X`, one can
form the formally coframe-valued family

```text
T_phi(A,B) X.
```

The expression is only shorthand until `X` is typed in the appropriate source fiber and transported
to a declared comparison fiber. Neither that typed multiplication nor path composition provides a
native target or equality. The complete extension class leaves `X` ambiguous, while current premises
provide no rule saying what complete path/coframe response the all-pairs clock network must equal or
preserve.

Thus a field-valued compatibility law remains possible and unselected, not refuted.

## 7. Smallest residual

The earliest extension-specific missing object is an active UDT-authoritative, metric-natural,
local-Lorentz-equivariant selection into the associated complete-extension bundle:

```text
Sigma:(complete metric, typed founded pair) -> X in A_H,
```

where `A_H` is the seven-parameter affine family with founded base block `H`. Mere existence of a
natural map is not selection. The rule must be licensed by an active UDT premise and state its
global transition law—path-labelled associated-bundle data, a vertical reset law, or an endpoint
section on a compatible reduced-holonomy branch.

This selector is earlier than a physical `X_max` or bootstrap equation. A complete physical
comparison functor would additionally need a UDT-authoritative observer/event variation domain,
signed depth on those arrows, global completion, and a response target. The already registered
stationary Killing depth is a branch-specific conditional depth control; it may not be spliced to
an extension from another branch by assertion.
