# Exact derivation — pair-first relational-plane reconstruction

Date: 2026-08-12

## 1. Bounded result

The preregistered primary landing is obtained:

```text
PAIR_FIRST_CONDITIONAL_RESOLUTION
```

A supplied regular timelike observer-pair immersion carries its own pair-relative tangent plane.
The Lorentz metric then supplies its unique orthogonal positive screen. In the registered complete
coframe chart, the full angular/mixing/embedding contribution to the induced pair metric is one
positive-semidefinite Gram term. Conditional pair evaluation therefore does not require curvature
to choose a universal ambient reciprocal/angular split.

This is not a derivation of the immersion. The founding source owns the clock/ruler channel type,
its reciprocal pairing, and the exponential character of a supplied depth. It does not by itself
choose paired events, ruler evolution, a branch, or a physical pair surface.

## 2. Three different planes that must not be conflated

### 2.1 Founded channel plane

The founding presentation starts with

```text
q=(c_E dt,dr)^T,
K=[[0,1],[1,0]],
D(delta)=diag(exp(-delta),exp(+delta)).
```

This is an ordered two-channel clock/ruler space. In the founding spherical chart, `dt` and `dr`
also provide a chosen local cotangent realization. Dual Reciprocity and continuous composition
derive the reciprocal character after `delta` is supplied. They do not covariantly select a
physical comparison surface in a general complete metric.

### 2.2 Realized pair plane

Let a typed query supply a regular immersion

```text
F:Sigma^2 -> (M^4,g).
```

At every regular point, `dF` is injective, so

```text
E_pair=dF(TSigma)
```

is a rank-two subspace of the ambient tangent space. If `h=F^*g` has Lorentzian signature, then
`E_pair` is a nondegenerate timelike two-plane. It is canonical relative to `(g,F)` and independent
of any ambient coframe presentation.

### 2.3 Pair-relative screen

Define

```text
H_pair=E_pair^perp.
```

Nondegeneracy gives the direct sum

```text
TM|F(Sigma)=E_pair direct-sum H_pair.
```

The ambient metric has inertia `(1,3)` and the pair plane has inertia `(1,1)`. Additivity of
inertia for an orthogonal direct sum therefore gives inertia `(0,2)` on `H_pair`: the screen is
positive definite. No Petrov, Ricci, derivative, preferred congruence, or aether selector is needed
for this conditional split.

An arbitrary pointwise plane field need not integrate. Here integrability is not inferred: the
surface `F` was supplied, and `E_pair` is its tangent bundle by construction.

## 3. Complete-coframe pullback

On a regular local `2+2` chart write the complete coframe and metric as

```text
E=[[B,0],[Q S,Q]],
g=E^T eta_4 E,
eta_4=diag(eta_2,I_2),
eta_2=diag(-1,+1).
```

Here `B` is a regular clock/ruler block, `Q` is a regular positive-screen coframe, and `S` is an
arbitrary real mixing matrix. Split the Jacobian of the supplied pair immersion as

```text
dF=J=[Y;Z].
```

The complete coframe evaluated on the pair tangents is

```text
E J=[B Y; Q(SY+Z)].
```

The first fundamental form is therefore exactly

```text
h=J^T g J
 =Y^T B^T eta_2 B Y +(S Y+Z)^T q(S Y+Z),          (1)
q=Q^T Q>0.
```

Equation (1) is the complete local orchestra formula. It does not attach an angular correction
after a reciprocal calculation. It first forms the complete metric pullback; the terminal
reciprocal coordinate is read only afterward.

## 4. The simple reduced object

When the base projection `Y` is invertible, use the pair-domain basis in which that projection is
the identity. Define

```text
W=Z Y^-1,
C=S+W.
```

Then

```text
Y^-T h Y^-1=B^T eta_2 B+C^T q C.                 (2)
```

Thus the first fundamental form sees ambient mixing `S` and the realized surface slope `W` through
their combined relative screen displacement `C`. The pair metric alone cannot invert that sum to
recover `S` and `W` separately. This is an evaluator non-identifiability statement, not a claim
that changing `(g,F)` while preserving `C` is gauge.

The `C=0` limit recovers the pure base metric exactly.

## 5. Complete pointwise solution space of the Gram contribution

For every real `C`,

```text
P=C^T q C
```

is positive semidefinite because

```text
v^T P v=(Cv)^T q(Cv)>=0.
```

Conversely, every positive-semidefinite `2 x 2` matrix `P` occurs. With positive square roots,

```text
C=q^-1/2 P^1/2
```

gives `C^T q C=P` (choosing symmetric roots). Hence the image is exactly the full `PSD(2)` cone,
not a selected subset.

Adding a positive-semidefinite form to a Lorentzian two-form cannot increase its negative index,
and its originally positive direction remains positive. The complete pointwise inertia atlas is
therefore:

```text
(1 negative,0 zero,1 positive)  Lorentzian pair plane;
(0 negative,1 zero,1 positive)  degenerate boundary;
(0 negative,0 zero,2 positive)  positive pair surface.
```

All three are retained. Only the first supports the calibrated Lorentzian terminal readout; the
others are characterized rather than discarded as solver failures.

## 6. Exact terminal modulation

In calibrated pair coordinates let

```text
B=[[T,T beta],[0,L]],
B^T eta_2 B=
  [[-T^2,-T^2 beta],
   [-T^2 beta,L^2-T^2 beta^2]],
P=[[a,d],[d,e]].
```

The complete induced pair metric is

```text
h00=-T^2+a,
h01=-T^2 beta+d,
h11=L^2-T^2 beta^2+e.                            (3)
```

On the A-calibrated timelike stratum

```text
A=T^2-a>0,
det(h)<0,
```

the unique terminal decomposition gives

```text
T_pair^2=A,
beta_pair=(T^2 beta-d)/(T^2-a),
L_pair^2=h11+h01^2/A,
-det(h)=T_pair^2 L_pair^2.                       (4)
```

Consequently

```text
kappa_pair=(1/4)log[-det(h)],
phi_pair=(1/4)log[-det(h)/h00^2]
        =(1/4)log[L_pair^2/T_pair^2],
c_eff^(pair)/c_E=T_pair/L_pair.                  (5)
```

Equations (3)--(5) prove the user's orchestra statement in its cleanest local form. Screen scale,
angular shape, mixing, and the pair embedding first alter the full Gram data `(a,d,e)`. The scalar
`phi_pair` is then extracted from the completed pair metric. `c_E` calibrates the terminal ratio;
it does not select the surface.

The Gram term is positive semidefinite, but `phi_pair` need not change monotonically because its
clock, cross, and ruler entries enter a Lorentzian determinant and ratio together.

## 7. Covariance checks

Three exact presentation checks pass:

1. A pair-domain change `J -> J R` gives `h -> R^T h R`.
2. A screen-frame rotation `Q -> OQ`, `O^T O=I`, leaves `q=Q^TQ` and `h` unchanged.
3. `C=0` recovers `B^T eta_2 B`, including the base values of `T`, `L`, and `beta`.

The terminal scalars in (5) require the declared A-calibrated coordinates. They are not asserted
to be invariant under arbitrary pair-coordinate changes that destroy that calibration.

## 8. Why this does not derive the physical relation

In flat `1+1` geometry, fixed worldlines

```text
A(y)=(y,0),
B(v)=(v,ell)
```

admit the exact family

```text
F_k(y,s)=(y+k s/ell,s).
```

Every member has

```text
h_k=[[-1,-k/ell],[-k/ell,1-k^2/ell^2]],
det(h_k)=-1,
phi_pair=0,
```

while pairing A's event `y` with B's event `y+k`. The same metric, observers, `c_E`, and terminal
reciprocal depth therefore retain different realizations. Pair-first evaluation removes the need
for an ambient plane selector; it does not make the physical realization emerge from bare
observer labels.

## 9. Regrade of the curvature excavation

The curvature-principal and first-curvature-derivative atlases remain valid maps of intrinsic
ambient structure. Their failure to recover the registered split on most complete metric jets no
longer blocks conditional observer-pair evaluation:

- where curvature owns a plane coincident with `E_pair`, it supplies additional intrinsic
  structure;
- where it owns a different plane or higher-rank distribution, those structures can be decomposed
  relative to `E_pair direct-sum H_pair`;
- where it owns no unique plane, the supplied pair immersion still has its own tangent/normal
  split.

No prior negative is erased. Its role is narrowed: those audits answer whether ambient curvature
selects the registered split, not whether a realized comparison possesses a pair plane.

## 10. Evidence

The SymPy production derivation passes 11 exact identities. A separately expressed stdlib
`Fraction` implementation passes:

```text
160/160 direct pullbacks,
160/160 reduced Gram identities,
160/160 pair-coordinate covariance checks,
160/160 screen-frame covariance checks,
34/34 encountered regular terminal reconstructions,
5/5 flat counterfamily rows,
1 exact tangent/normal positivity witness.
```

## 11. Exact bounded landing

```text
PAIR_FIRST_CONDITIONAL_RESOLUTION__THE_FOUNDING_OWNS_AN_ORDERED_CLOCK_RULER_CHANNEL_TYPE_AND_
RECIPROCAL_CHARACTER__A_SUPPLIED_REGULAR_TIMELIKE_PAIR_IMMERSION_OWNS_ITS_PAIR_RELATIVE_TANGENT_
PLANE_AND_UNIQUE_POSITIVE_ORTHOGONAL_SCREEN__THE_COMPLETE_COFRAME_PULLBACK_COMBINES_BASE_SCREEN_
MIXING_AND_EMBEDDING_DATA_BEFORE_TERMINAL_PHI_IS_READ__NO_UNIVERSAL_AMBIENT_CURVATURE_SELECTOR_IS_
REQUIRED_FOR_CONDITIONAL_PAIR_EVALUATION__THE_PHYSICAL_IMMERSION_EVENT_PAIRING_BRANCH_GLOBAL_
COMPATIBLE_RELATION_FAMILY_HISTORY_ACTION_SOURCE_AND_DYNAMICS_REMAIN_OPEN.
```
