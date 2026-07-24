# Exact bootstrap-aware closure derivation

## 1. Scope

This is an invariant local-plus-global availability audit, not a solution of
unknown field equations. Let an observer/path choice and a regular
Lorentzian metric supply:

- a two-dimensional Riemannian screen;
- its self-adjoint tidal endomorphism `T`;
- the reciprocal clock rate `a=d delta/d lambda`; and
- the induced screen covariant derivative `D_lambda`.

No screen basis, matter carrier, source, action, density value, boundary
functional, or completion is chosen.

## 2. What the screen geometry can select

In any orthonormal screen frame write

```text
T = [[u,v],
     [v,w]].
```

The invariant discriminant is

```text
Delta = (tr T)^2 - 4 det T
      = (u-w)^2 + 4 v^2.
```

Because `T` is self-adjoint, `Delta>=0`. When `Delta=0`, `T` is proportional
to the identity and no screen line is selected. When `Delta>0`, it has two
distinct metric-defined eigenlines. Their projectors are polynomial
functions of `T`:

```text
P_plus  = (T-k_minus I)/(k_plus-k_minus),
P_minus = (k_plus I-T)/(k_plus-k_minus).
```

They conjugate correctly under every screen rotation. This supplies an
unordered pair of lines, not yet a reason to choose one.

## 3. The clock match can choose one line

The parent pointwise generator result requires one screen curvature
eigenvalue to be

```text
K_clock = -a^2.
```

This can be expressed without naming an eigenvector:

```text
chi_clock = det(T+a^2 I)
          = a^4 + a^2 tr(T) + det(T).
```

On the simple-spectrum domain,

```text
chi_clock=0
```

means exactly one eigenvalue is `-a^2`. The matched line is then intrinsic.
Define `Q=T+a^2 I`. Since `Q` has eigenvalues zero and `tr Q`, its kernel
projector is

```text
P_clock = I - Q/tr(Q)
        = I - (T+a^2 I)/(tr(T)+2a^2).
```

The denominator is nonzero precisely because the other eigenvalue is
different. Cayley-Hamilton gives

```text
P_clock^2=P_clock,
Q P_clock=0,
tr(P_clock)=1.
```

This is the main structural advance of the audit:

> Simple tidal spectrum plus the clock-curvature equation selects the screen
> line and makes tidal invariance automatic.

The line does not have to be separately inserted.

## 4. Parallel transport is independent

On the simple-spectrum domain, a spectral line remains parallel exactly
when

```text
D_lambda P_clock=0.
```

Equivalently,

```text
[T,D_lambda T]=0.
```

In an instantaneous eigenframe with eigenvalues `k1!=k2` and screen rotation
rate `omega`, both expressions vanish exactly when `omega=0`. The
commutator's off-diagonal magnitude carries the factor
`(k1-k2)^2 omega`.

Thus the clock match can select a line, but it does not by itself stop the
line from rotating along the path.

## 5. Pointwise match versus path connection

For `K=-a^2`, use the scalar Jacobi and reciprocal generators

```text
A_J = [[0,1],[a^2,0]],
A_R = diag(-a,+a).
```

Every nondegenerate pointwise eigen-intertwiner has the form

```text
H = [[f,g],
     [-af,ag]],
det H = 2afg.
```

It obeys `A_J H=H A_R` pointwise. A path-level change of variables must
instead obey

```text
D_lambda H = A_J H - H A_R.
```

For the pointwise eigen-intertwiner, the right-hand side is zero. With
nonzero columns, `D_lambda H=0` requires constant column normalizations and
`D_lambda a=0`, unless an additional metric-derived connection or
normalization term changes the natural generator comparison.

Therefore:

- the eigenvalue equation is a pointwise intrinsic selection;
- it is not a complete irreducible path cocycle when the clock rate varies.

## 6. What total proper density can vary

For a same-solution native mass and proper volume,

```text
rho_tot = M_native/V_proper,
```

the exact first variation is

```text
delta rho_tot
  = (delta M_native-rho_tot delta V_proper)/V_proper.
```

For a spatial metric varied covariantly,

```text
delta V_proper
  = (1/2) integral sqrt(h) h^{ij} delta h_ij.
```

The volume term is pure trace. It vanishes against a trace-free screen
variation and therefore cannot by itself split the two tidal eigenvalues or
select a screen line.

The mass variation can in principle be anisotropic:

```text
delta M_native/delta h_ij.
```

That functional derivative could alter the local metric equation, create a
simple screen spectrum, and enforce `chi_clock=0`. But current UDT has no
off-shell native mass functional or complete matter-to-metric source law.
The number `rho_tot` is not a substitute for this derivative.

## 7. Three bootstrap meanings

### After-solution admissibility

The currently recorded owner principle says that realized matter-bearing
solutions occupy a narrow density window. Applied after a solution exists,
it filters complete solutions but contributes no Euler equation. It cannot
enforce any local solder gate.

### Varied global density constraint

A functional such as `F(rho_tot)=0` could contribute local equations only
after `M_native[g,fields]`, its variation domain, the same-solution proper
volume, and boundary terms are defined. This route is mathematically viable
but presently only a form.

### Complete simultaneous closure

A noncircular bootstrap would vary local fields, the metric, the finite-cell
boundary/global variables, and any multiplier in one problem. It could in
principle change the source-free curvature and select the intrinsic
projector above. No registered current branch supplies that complete
system.

## 8. Source-family and completion census

`EQUATION_FAMILY_GATE_MATRIX.tsv` classifies all 28 registered equation
families. `COMPLETION_BOOTSTRAP_ATLAS.tsv` classifies all 12 registered
finite-cell families.

Results:

- zero equation families contain a complete simultaneous native
  metric–matter–boundary bootstrap;
- zero completion rows contain a complete `(g,phi,matter)` witness with a
  density response argument;
- B19 remains a complete conditional transverse geometry with round
  isotropic positive screen curvature and no nontrivial clock solder;
- WR-L retains its exact local scalar clock/area relation but its round
  radial screen is isotropic and its positive curvature fails the pointwise
  clock match;
- the conditional Hopfion can carry directional structure only after its
  carrier/action/background premises are supplied; it is not a native
  source response;
- the bootstrap selector family explicitly leaves the varied functional and
  representative map open.

## 9. Correct regrading

The B19 and WR-L failures remain exact within their tested source-free or
conditional branches. They are not universal no-go theorems for a
self-consistent matter-filled UDT universe.

A future native bootstrap could change `T`. To close the present route it
would have to produce, on a complete branch:

```text
Delta>0,
det(T+a^2 I)=0,
[T,D_lambda T]=0,
global descent of P_clock,
and path-connection compatibility.
```

No one of these is promoted to a new field equation here.
