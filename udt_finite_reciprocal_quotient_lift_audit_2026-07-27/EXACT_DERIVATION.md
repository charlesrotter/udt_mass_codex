# Exact derivation — finite reciprocal quotient lifts

## 1. What is supplied and what is not

The founded two-channel result supplies the additive finite action

```text
B(phi) = diag(exp(-phi), exp(+phi))
```

on an ordered clock/ruler pair. This audit supplies a local vector-space exact sequence only as a
query:

```text
0 -> S -> V -> B -> 0,
```

where `dim(V)=4` and the screen kernel `S` has dimension two. Neither the existence of this exact
quotient as physical UDT structure nor a global realization of it is assumed derived.

Choose a temporary splitting `V=B+S` and let `pi=[I_2,0]`. A finite lift `F(phi)` induces the founded
action exactly when

```text
pi F(phi) = B(phi) pi.
```

For a general block matrix this equation is equivalent to

```text
F(phi) = [[B(phi), 0],
          [L(phi), Q(phi)]].
```

The exact quotient therefore forces the zero upper-right block and makes the screen invariant. It
does **not** make `L` or `Q` constant, exponential, or triangular. Subject to `F(0)=I`, quotient
preservation alone leaves four arbitrary smooth components in `L(phi)` and four in invertible
`Q(phi)`, with `L(0)=0` and `Q(0)=I`.

The exact algebra gives eight independent pointwise quotient constraints and eight remaining
function components.

## 2. Adding a complete one-parameter group law

Now add the stronger condition

```text
F(phi_2) F(phi_1) = F(phi_1+phi_2).
```

For a regular finite-dimensional one-parameter representation, differentiation at zero gives one
constant generator, and the representation is

```text
F(phi)=exp(phi X),
X = [[H, 0],
     [C, K]],
H = diag(-1,+1).
```

Here `C` and `K` are arbitrary real `2 x 2` matrices. Thus the full quotient-representation class
has eight generator parameters, not seven. Its exact finite lower block is

```text
L(phi) = integral_0^phi exp((phi-t)K) C exp(tH) dt.
```

Every member composes and reverses exactly. This is a theorem **if** the complete lift is required to
be a representation. The founded pair group law by itself does not license that stronger complete-
coframe premise.

## 3. First metric response and the missing eighth direction

With

```text
eta = diag(-1,+1,+1,+1),
g(phi)=F(phi)^T eta F(phi),
```

the first metric jet is

```text
g'(0) = X^T eta + eta X
      = [[2 I_2, C^T],
         [C,     K+K^T]].
```

The map from the eight quotient-group generator parameters to `g'(0)` has exact rank seven. Its
one-dimensional kernel is precisely the screen rotation algebra `so(2)`. Writing

```text
K = S + w J,
S = [[a,b],[b,d]],
J = [[0,1],[-1,0]],
```

shows the structure transparently: the response fixes all four entries of `C` and the three entries
of symmetric `S`, but it cannot see the rotation rate `w` at first order.

This also locates the earlier seven-parameter positive-triangular chart. It chose one screen flag and
thereby one representative from this one-parameter fiber. Its seven metric-response directions
remain independent, but the chart was not the complete set of exact quotient representations.

## 4. Self-adjoint and triangular representatives

The unique full `eta`-self-adjoint representative of a supplied first metric response is

```text
A = (1/2) eta^-1 g'(0).
```

When `C` is nonzero, its upper-right block is `(1/2) eta_B C^T`, so it does not preserve the screen
kernel and is not in the exact quotient class. It becomes a quotient generator only on the no-mixing
stratum `C=0`. Setting only the screen skew part to zero (`w=0`) is always a valid quotient
representative, but it is an extra representative choice, not full metric self-adjointness when
`C` is nonzero.

A chosen ordered screen flag gives two equally admissible triangular sections:

```text
upper flag: w=+b,  K=[[a,2b],[0,d]],
lower flag: w=-b,  K=[[a,0],[2b,d]].
```

They share the same first metric response and are generically distinct. A ninety-degree screen
rotation exchanges which triangular flag is displayed. The metric and ordered reciprocal pair do
not privilege either flag.

## 5. When screen rotation is gauge and when it is finite metric data

Equality at first order is not equality of finite metric paths. Comparing `w` to `0`, the exact
second-jet difference with no mixing is

```text
Delta g''(0)|_S =
  [[-4 b w,       2 w (a-d)],
   [ 2 w (a-d),   4 b w]].
```

For nonzero `w`, this vanishes exactly when the symmetric screen response is isotropic:
`S=lambda I`.

Even on that isotropic screen, a general nonzero mixing block makes the rotation visible. With
`C=[[c00,c01],[c10,c11]]`, the cross-block difference is

```text
Delta g''(0)|_(B,S) =
  [[-c10 w, c00 w],
   [-c11 w, c01 w]].
```

For nonzero `w`, it vanishes exactly when `C=0`. Consequently the screen rotation is finite-metric
representative freedom only on the combined stratum

```text
C=0 and S=lambda I.
```

There the screen exponential factors exactly as

```text
exp(phi(lambda I+wJ)) = exp(lambda phi) R(w phi),
```

and `R^T R=I`, so every `w` gives the same finite metric. Everywhere else a nonzero change of `w`
changes the analytic metric path already at second order. It is then inequivalent finite metric
data, despite lying in the first-response kernel.

## 6. Quotient preservation, metric equality, and group composition are independent gates

Let `R(t)` be the rational half-angle `SO(2)` rotation and form

```text
F(phi)=diag(I_2,R(phi^2)) diag(B(phi),I_2).
```

This is an exact smooth quotient lift, starts at the identity, and gives the same complete metric as
the spectator lift for every `phi`. Yet exact rational evaluation at `phi=1,2` shows
`F(1)F(1) != F(2)`, and `F(-1)F(1) != I`. Thus even a fixed-metric quotient lift need not extend the
founded composition or reversal law.

Conversely, every constant-generator quotient representation composes and reverses. Composition
does not choose `C`, `S`, or `w`; it only changes functional freedom into eight constant generator
parameters.

## 7. Global finite-cell requirements

The local block form becomes a global quotient extension only if:

1. the pointwise screens assemble into an invariant rank-two subbundle;
2. local quotient maps and founded pair actions agree on overlaps;
3. local generators obey the correct conjugacy/transition cocycle;
4. a triangular section, if used, is supported by a global screen flag rather than a chart choice;
5. monodromy and finite-cell gluing preserve the claimed reduction.

If the quotient action is written identically on every overlap, the induced pair transition must
intertwine `H`. A global triangular choice requires transitions that preserve its screen flag. A
general screen rotation changes that flag, and nontrivial screen topology or monodromy can obstruct a
single global choice.

At the scalar seal `phi=0`, every regular group lift equals the identity. The seal value therefore
has zero selector rank for `C`, `S`, `w`, or a flag. Derivative, normal, quotient, or gluing data could
constrain them only if separately derived.

## 8. Bounded conclusion

The finite classification is now exact:

- block-lower form is `DERIVED_IF_EXACT_QUOTIENT`;
- a constant eight-parameter generator is `DERIVED_IF_COMPLETE_GROUP_LAW`;
- a fixed first metric response leaves an exact one-parameter screen-rotation family;
- the seven-parameter triangular chart is `CONDITIONAL_ON_SCREEN_FLAG`;
- screen rotation is representative-only on the isotropic unmixed stratum and is generically
  inequivalent finite metric data;
- physical quotient semantics, the complete response, a global flag/section, and a physical
  observer/path realization remain `OPEN`.

No action, source, carrier, boundary law, bootstrap closure, `X_max`, mass, or dynamics follows.
