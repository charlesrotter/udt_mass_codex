# Exact nonlinear derivation

## 1. Complete regular coframe

The registered coframe is

```text
theta0 = exp(-phi) dx0
theta1 = exp(+phi) dx
Theta  = D eta
eta    = (dy,dz)^T + S(dx0,dx)^T
D      = [[exp(sigma/2-alpha), k exp(sigma/2-alpha)],
          [0,                      exp(sigma/2+alpha)]] .
```

All amplitudes are arbitrary smooth functions of `(x0,x)`. Let `E0,E1` be
the horizontal orthonormal derivatives dual to `theta0,theta1` on such
torus-invariant scalars. Define

```text
u_a = E_a phi,     s_a = E_a sigma,     a_a = E_a alpha,
h_a = exp(-2 alpha) E_a k,
f = (f2,f3)^T = D(dS)_(theta0 wedge theta1).
```

Then the right logarithmic derivative of the angular zweibein is

```text
K_a = (E_a D) D^-1
    = [[s_a/2-a_a, h_a],
       [0,           s_a/2+a_a]].
```

## 2. Exact structure equations

Direct exterior differentiation gives

```text
d theta0 = u1 theta0 wedge theta1,
d theta1 = u0 theta0 wedge theta1,
d Theta  = (K0 theta0 + K1 theta1) wedge Theta
           + f theta0 wedge theta1.
```

No expansion has been made. The complete component form is in
`STRUCTURE_EQUATIONS.tsv`.

The dual-frame commutator is

```text
[E0,E1] = -u1 E0 - u0 E1 - f2 E2 - f3 E3.
```

For a torus-invariant scalar the last two terms act trivially. Thus `phi`
does not merely multiply an angular block: its reciprocal clock/ruler
anholonomy enters the derivative algebra used by every angular amplitude.

## 3. Coframe integrability

Because `K=dD D^-1` is a right Maurer-Cartan form,

```text
dK - K wedge K = 0.
```

In the orthonormal base this is exactly

```text
E0(s1)-E1(s0) + u1 s0 + u0 s1 = 0,
E0(a1)-E1(a0) + u1 a0 + u0 a1 = 0,
E0(h1)-E1(h0) + u1 h0 + u0 h1
                    + 2 a0 h1 - 2 a1 h0 = 0.
```

Substitution makes all four `d^2 theta^a` vanish exactly. These equations are
compatibility identities among channels derived from the same zweibein. They
are not equations of motion.

## 4. Levi-Civita connection

Solving

```text
d theta^a + omega^a_b wedge theta^b = 0,
omega_ab = -omega_ba
```

gives one set of 24 coefficients. In lower-index form the six independent
one-forms are

```text
omega01 =  u1 theta0 - u0 theta1 - f2/2 theta2 - f3/2 theta3
omega02 =             - f2/2 theta1 + (a0-s0/2) theta2 - h0/2 theta3
omega03 =             - f3/2 theta1 - h0/2 theta2 - (a0+s0/2) theta3
omega12 =  f2/2 theta0              + (a1-s1/2) theta2 - h1/2 theta3
omega13 =  f3/2 theta0              - h1/2 theta2 - (a1+s1/2) theta3
omega23 = -h0/2 theta0 - h1/2 theta1.
```

The machine-readable table is `CONNECTION_COEFFICIENTS.tsv`. Exact
substitution returns zero torsion and exact metric antisymmetry.

## 5. Curvature and its contractions

For

```text
Omega^a_b = d omega^a_b + omega^a_c wedge omega^c_b,
```

the calculation retains all derivatives and quadratic products. All 36 slots
`Omega_ab|cd` are generically nonzero in the registered family. They satisfy
lower-pair antisymmetry, two-form antisymmetry, Riemann pair exchange, the
first Bianchi identity, and symmetric Ricci contraction exactly.

The exact scalar contraction is

```text
R = [4 E0(s0) + 4 E0(u0) - 4 E1(s1) + 4 E1(u1)
     + 4 a0^2 - 4 a1^2 + f2^2 + f3^2 + h0^2 - h1^2
     + 3 s0^2 - 3 s1^2 + 4 s0 u0 + 4 s1 u1
     + 4 u0^2 - 4 u1^2] / 2.
```

At the neutral coframe, correctly converting orthonormal derivatives back to
coordinate jets reproduces the previously banked scalar-curvature rate form
exactly. In particular, an orthonormal derivative such as `E0(u0)` contains
an anholonomy product even when the corresponding coordinate second jet is
zero. This is why simply replacing it by a coordinate second derivative would
lose a factor.

## 6. Nonlinear ensemble graph

The full Riemann-component census contains derivative terms for all six
families and 19 of the 21 possible unordered quadratic family pairs (self
pairs included). The only absent direct pairs are

```text
PHI_ANHOLONOMY -- CONNECTION_CURVATURE_1
PHI_ANHOLONOMY -- CONNECTION_CURVATURE_2.
```

The remaining graph is connected. `phi` couples directly to angular common
scale, reciprocal angular shape, and angular shear. Each connection-curvature
channel couples to those angular families. Thus there is an exact indirect
path from `phi` to both connection-curvature channels through the angular
geometry.

This is a tensor-component dependency atlas in the registered triangular
coframe. The Riemann tensor is intrinsic; an individual graph edge or channel
name is not by itself frame-independent physics. The scalar contraction also
shows cancellations: it retains direct `phi`--common-scale products but no
direct `phi`--reciprocal-shape or `phi`--shear product.

## 7. What Bianchi does and does not do

With zero torsion, the first identity follows from `D^2 theta=Omega wedge
theta=0`. The second follows algebraically from

```text
dOmega + omega wedge Omega - Omega wedge omega = 0.
```

The independent graded-word expansion cancels term by term. Neither identity
selects an amplitude profile or supplies a response one-form, action, source,
boundary functional, density law, or global branch. They constrain how a
chosen metric hangs together; they do not tune the metric.

## 8. Global scope

The local equations apply exactly on regular charts admitting the registered
coframe. Caps, mirrors, monodromies, orientation reversal, singular strata,
and rank transitions require their registered chart/gluing data. The general
FC11 anholonomic no-orbit family is not globally exhausted by this toric
coframe; only connection-horizontal local witnesses are represented. No
completion is selected and no complete on-shell profile has been constructed.

## 9. Density boundary

Density is absent from every equation above. A later Lambda-CDM-centered
bracket is authorized only as an imported comparison-centered exploration,
not as a UDT derivation. Until a native density-to-geometry response law places
`rho_tot` in the metric closure, changing a density number cannot honestly
modify these solutions; it would only append an unlicensed source term.
