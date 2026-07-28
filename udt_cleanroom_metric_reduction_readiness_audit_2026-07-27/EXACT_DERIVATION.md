# Exact clean-room reduction derivation

## 1. Current configuration chart

The bounded complete coframe uses

```text
theta0 = exp(-phi) dx0
theta1 = exp(+phi) dx
(theta2,theta3)^T = D[(dy,dz)^T+S(dx0,dx)^T]

D = [[exp(sigma/2-alpha), k exp(sigma/2-alpha)],
     [0,                      exp(sigma/2+alpha)]].
```

The eight amplitudes are

```text
q=(phi,sigma,alpha,k,S10,S11,S20,S21).
```

This is a bounded chart, not a native field census. `phi` is the founded pair's
logarithmic depth and contributes no additional scalar beyond the coframe.

At the neutral point, the eight coframe tangents are

```text
phi:   diag(-1,+1,0,0)
sigma: diag(0,0,1/2,1/2)
alpha: diag(0,0,-1,+1)
k:     E_23
S10:   E_20       S11: E_21
S20:   E_30       S21: E_31.
```

They have exact coframe rank eight. Under
`delta g=delta E^T eta E+E^T eta delta E`, their metric tangents also have
exact rank eight. Therefore none of these chart directions can be dropped at
the regular neutral point merely because it is invisible to the metric.

## 2. What Cartan's equations actually determine

For an orthonormal coframe, a metric connection has 24 independent local
coefficients `omega_(ab)c`, antisymmetric in `a,b`. The first Cartan equation

```text
d theta^a + omega^a_b wedge theta^b = 0
```

gives a `24 x 24` exact linear system of rank 24. It uniquely determines the
torsion-free metric connection **from the coframe and its first jets**. It
places zero differential equations on freely supplied coframe profiles.

The second Cartan equation

```text
Omega^a_b=d omega^a_b+omega^a_c wedge omega^c_b
```

then defines curvature. Bianchi identities follow from these definitions.
Neither becomes a metric evolution law until a separate current UDT response
equation constrains the curvature or coframe.

## 3. One-coordinate reduction

Let every chart amplitude depend on one coordinate `s`. Then

```text
K_s=(partial_s E)E^-1
   =sum_A q'^A (partial E/partial q^A) E^-1.
```

The metric maps the eight arbitrary first jets into connection and the eight
arbitrary second jets, together with quadratic first-jet terms, into curvature.
It does not set any of those outputs equal to a selected response. Thus, in the
fixed chart,

```text
live profile directions                 8
metric-supplied profile equation rank   0
closure deficit                         8.
```

Regularity and causal conditions are inequalities or branch labels. Caps,
periods, and mirrors are global compatibility data. None supplies the missing
bulk differential rank.

The stationary twisted `S3` witness makes this freedom concrete: every smooth
finite profile satisfying its nondegeneracy/slicing inequalities remains a
law-neutral configuration. The reduced constant-depth product is a fixed
control, not a nontrivial evolution law. The two must not be spliced.

## 4. `1+1` time-dependent reduction

Let `q=q(t,x)`. There are 16 independent base first-jet directions and eight
time-principal second-jet directions. The right logarithmic coframe derivatives

```text
A_t=(partial_t E)E^-1,
A_x=(partial_x E)E^-1
```

obey

```text
partial_t A_x-partial_x A_t-[A_t,A_x]=0.
```

The production control evaluates this exactly on the noncommuting determinant-
one matrix

```text
E=[[1+t x,t],[x,1]]
```

and obtains the zero matrix. This is mixed-partial integrability for every
smooth invertible `E`; it does not select `partial_t^2 q`. Consequently

```text
time-principal directions                    8
metric-supplied evolution principal rank     0
evolution closure deficit                    8.
```

A method-of-lines discretization would only replace spatial derivatives by a
matrix. It cannot manufacture the missing continuum response.

## 5. ODEs that do close on supplied configurations

The metric does supply exact conditional path equations:

```text
geodesic:
  dx^mu/dlambda = v^mu
  dv^mu/dlambda = -Gamma^mu_ab v^a v^b

parallel transport:
  dV^mu/dlambda = -Gamma^mu_ab v^a V^b

projected screen transport:
  D_v s = H nabla_v s = 0

Jacobi transport:
  D J/dlambda = W
  D W/dlambda = -R(J,v)v                  [sign convention fixed here].
```

Their first-order state/equation ranks are respectively `8/8`, `4/4`, `2/2`,
and `8/8`. They require a supplied smooth metric plus the indicated path,
screen, geodesic, and initial data. They reveal transport, caustics, mixing,
and holonomy within a configuration. They do not determine the configuration.

## 6. Exact readiness ruling

The registered current metric kinematics close four classes of pathwise ODE
on supplied configurations. They do not close either the tested background
profile ODE or the tested `1+1` time-live metric system. A background numeric
solve would necessarily add hidden equations or freeze live directions.

This is bounded to the current premise set and tested reductions. It does not
exclude a future metric-native global, higher-jet, variational, boundary, or
bootstrap response. It identifies the equation type that would have to be
derived before a background solve is honest.
