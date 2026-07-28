# Exact derivation — full-screen Hopf/toric regrade

## Scope

This is exact static/global geometry in two explicitly distinct families:

1. the chosen twisted `R x S3` block-screen coframe with arbitrary smooth interior
   `P:S3->GL(2,R)`; and
2. the registered toric interval taxonomy when an effective `T2` action is separately supplied.

Neither family is selected as the physical universe. Pair–screen metric off-blocks, `E0(P)`, an
action, source, carrier, boundary functional, density/bootstrap fixed point, mass, and dynamics are
not loaded.

## 1. What a full screen supplies—and does not

For

```text
(theta2,theta3)^T=P(sigma1,sigma2)^T,
h=P^T P=[[A,B],[B,C]],
```

`h` has area plus two shears. A local left `O(2)` rotation of `P` is coframe gauge. If the screen is
oriented, its metric supplies the canonical complex structure

```text
J_h = 1/sqrt(det h) [[B,C],[-A,-B]],
J_h^2=-I,                 J_h^T h J_h=h.
```

This survives every positive full screen, but it has no real eigenline. It supplies an oriented
quarter-turn, not a preferred circle generator or toric lattice direction.

Nor is an arbitrary full screen toric. The global allowed screen

```text
P=exp[epsilon Re(z1)] I  on S3
```

is smooth and invertible. Its screen metric is the Hopf-fiber-invariant background
`sigma1^2+sigma2^2` multiplied by `exp[2 epsilon Re(z1)]`, whose derivative along the standard
phase rotation is generically nonzero. This scalar factor cannot be hidden by a coframe rotation.
Thus the full screen family contains global non-`T2`-invariant configurations. Toric formulas apply
only after a global effective torus action and screen equivariance are present.

## 2. The contact object already in the twisted S3 coframe

The chosen pair sector is

```text
theta0=exp(-phi)(c_E dt+alpha sigma3),
theta1=exp(+phi)sigma3.
```

With `dphi=p1 theta1+p2 theta2+p3 theta3`, the exact Cartan system gives

```text
dtheta1=dphi wedge theta1+t1 theta2 wedge theta3,
t1=kappa exp(phi)/det(P).
```

Hence

```text
theta1 wedge dtheta1=t1 theta1 wedge theta2 wedge theta3 !=0
```

for nonzero `kappa`, finite `phi`, and invertible `P`. The ruler form is contact throughout this
chosen coframe family, independently of both screen shears.

Its Reeb field is obtained without an action or equation. Writing `E1,E2,E3` for the dual spatial
frame, direct contraction gives

```text
R_theta1=E1+(p3/t1)E2-(p2/t1)E3.
```

Contact is not periodicity. In standard Hopf coordinates let

```text
alpha0=cos(eta)^2 dxi1+sin(eta)^2 dxi2,
alpha=f(eta) alpha0,
f=exp[k cos(2eta)].
```

The exact Reeb frequencies are

```text
a=[1-2k sin(eta)^2]/f,
b=[1+2k cos(eta)^2]/f.
```

At `eta=pi/4`, `k=sqrt(2)/2`, their ratio is `3-2sqrt(2)`. The orbit on that torus is not closed.
This smooth positive exact counterexample forbids promoting the contact property of `theta1` to a
free circle action.

## 3. Founded-depth normalization exposes a stronger conditional bundle

The founded pair relation itself gives

```text
boxed: alpha0=exp(-phi) theta1=sigma3.
```

This is not strong local CSN and is not a Weyl-gauge claim. It is the explicit algebraic inverse of
the already-derived ruler dilation inside the chosen coframe.

The Maurer–Cartan relation becomes

```text
dalpha0=d sigma3
       =kappa sigma1 wedge sigma2
       =kappa/det(P) theta2 wedge theta3.
```

Thus `alpha0` remains contact for every invertible full screen. In the frozen Hopf-coordinate
convention,

```text
sigma3=cos(eta)^2 dxi1+sin(eta)^2 dxi2,
xi1,xi2 each have period 2 pi.
```

For `V=partial_xi1+partial_xi2`, `sigma3(V)=1` and the fiber integral is `2 pi`. With quotient
coordinate `delta=xi1-xi2`,

```text
d sigma3=-2 sin(eta)cos(eta) d eta wedge d delta,
(1/(2 pi)) integral_S2 d sigma3=-1
```

in this orientation, hence magnitude one. Therefore on the registered global `S3=SU(2)`
Maurer–Cartan coframe, `alpha0` is the standard free Hopf principal connection and the quotient is
`S2` with `|c1|=1`.

This statement has three distinct grades:

1. **Coframe-conditional:** `alpha0=sigma3` and its free Hopf action are exact on the chosen global
   Maurer–Cartan `S3` coframe for all `P`.
2. **Metric-intrinsic overlap witness:** on a positive slice where the complete metric itself
   identifies the reciprocal ruler line, the induced spatial metric dual of its fiber generator,
   divided by its squared norm, is again `sigma3`. The existing C01–C06 intrinsic-pair family gives
   a bounded overlap witness; persistence for every general `P` is not proved.
3. **Metric quotient:** the full screen metric descends to the `S2` quotient only if it is invariant
   or equivariant under the fiber action. An arbitrary allowed `P` need not satisfy that condition.

The full screen therefore does not destroy the conditional Hopf bundle, but neither does it make
the bundle a universal metric-selected structure.

## 4. Torus-orbit connection in the registered cohomogeneity-one gauge

Now separately suppose an effective cohomogeneity-one `T2` action is supplied and its positive
torus-orbit metric block is

```text
h(s)=[[A(s),B(s)],[B(s),C(s)]]>0
```

on the principal orbit region. In the registered orthogonal interval gauge—or when only the
orbit-torus component is being stated—for a supplied primitive circle generator
`w=(m,n)`, its normalized metric-dual connection is

```text
A_w = q1 dxi1+q2 dxi2,

q1=(A m+B n)/(A m^2+2Bmn+C n^2),
q2=(B m+C n)/(A m^2+2Bmn+C n^2).
```

It obeys `A_w(w)=1`. Replacing `h` by `Omega^2 h` changes neither coefficient. This is algebraic
common-factor cancellation, not a local scale-gauge theorem.

For any integral vector `u=(r,s)`, horizontal projection gives

```text
h_B(u,u)=h(u,u)-h(w,u)^2/h(w,w)
        =det(h) det(w,u)^2/h(w,w).
```

In a unimodular fiber/base basis, the quotient angular coefficient is `det(h)/h(w,w)`. The two-shear
sector collectively changes the local connection/curvature and quotient metric: an off-diagonal
shear changes `A_w`, while the complementary shape mode can change the base metric without changing
`A_w`. It is not true that each shear must change each object. Neither changes the topological class
after the bundle, cap lattice, and fiber are fixed.

A completely general invariant three-metric may also contain `ds dxi_i` cross terms. They add a
basic radial component `[k(s).w/h(w,w)] ds` to the full metric-dual connection. On an interval it can
be removed by an angular/fiber gauge when endpoint regularity permits. In either description it
does not change the cap lattice or Euler/Chern class; the displayed two-coefficient formula is not
being claimed as the full connection in every toric gauge.

An explicit full-screen family on the standard `S3` caps is

```text
h_epsilon = [[cos(eta)^2, epsilon sin(eta)^2 cos(eta)^2],
             [epsilon sin(eta)^2 cos(eta)^2, sin(eta)^2]],
```

positive on the principal region for `|epsilon|<2`. For `w=(1,1)`, shear changes `q1,q2` locally,
but `q1+q2=1`, `q1(0)=1`, and `q1(pi/2)=0`. Therefore

```text
integral A_w wedge dA_w=-4 pi^2
```

in the registered orientation/period convention for every member of this sheared family. The unit
class survives; the local geometry does not become unique.

## 5. Cap lattice, freeness, and the non-unit counterfamily

Let primitive torus cycles `v_minus,v_plus in Z2` collapse at two smooth caps. Their determinant

```text
p=|det(v_minus,v_plus)|
```

classifies the standard toric completion: `p=0` gives the same-cycle class, `p=1` gives `S3`, and
`p>1` gives a lens class with additional gluing data.

Under an effective cohomogeneity-one `T2` action, two primitive smooth caps, and no additional
exceptional orbit, a primitive circle `w` is free at both caps exactly when

```text
|det(v_minus,w)|=|det(v_plus,w)|=1.
```

To see the class rather than assume it, choose `u` with `det(w,u)=1` and write

```text
v_minus=a_minus w+b_minus u,
v_plus =a_plus  w+b_plus  u.
```

Freeness gives `b_minus,b_plus=plus_or_minus 1`. The two cap trivializations differ by

```text
e=a_minus/b_minus-a_plus/b_plus.
```

Therefore the quotient is a smooth `S2` and, up to orientation,

```text
|c1|=|e|=|a_minus b_plus-b_minus a_plus|
    =|det(v_minus,v_plus)|=p.
```

The old unit result is the `p=1` member, not the general result. There are exact infinite
counterfamilies. For every positive integer `k`, take

```text
v_minus=(k+1,k),
v_plus =(k,k+1),
w=(1,1).
```

Then

```text
det(v_minus,w)=+1,
det(v_plus,w)=-1,
p=2k+1.
```

These are exchange-related smooth primitive caps with a free diagonal circle and non-unit odd
Chern magnitude. Likewise `(1,0),(1,p)` with `w=(0,1)` supplies the `L(p,1)` principal-bundle
family for every positive `p`. Thus angular exchange, freeness, and a full screen do not select the
unit class across registered completions.

## 6. Corrected N22 and T18

### N22

The old diagonal reciprocal-toric witness remains exact in its subfamily. The full-screen
rederivation adds a more robust conditional route:

```text
founded ruler leg theta1
  --remove its founded exp(phi) depth-->
normalized ruler/contact form sigma3
  --on the chosen global Maurer-Cartan S3 coframe-->
free Hopf circle and unit principal bundle,
```

independent of both screen shears. This is a genuine improvement in the conditional bridge. It is
not carrier emergence because the complete `S3` coframe is not selected, metric-intrinsic ruler
ownership is only proved on a bounded overlap family, arbitrary `P` need not descend, the quotient
metric is not forced round, and one bundle projection is not `Map(S3,S2)` or an action.

### T18

The old two-gate wording is too narrow. The enlarged geometry has two alternative conditional
routes:

- **toric-screen route:** derive a global effective `T2` reduction and invariant full screen;
  then select cap lattice and a free primitive circle; then establish full-screen descent;
- **normalized-contact route:** select the complete twisted `S3` coframe with its founded ruler
  ownership; normalize by founded depth; then establish that the realized full screen descends.

Neither route is selected by current Reciprocity, finite-cell data, or bootstrap. The first retains
`p=0`, `p=1`, lens, boundary, orbifold, and non-toric countermodels. The second makes the unit bundle
automatic only after the unselected global `S3` coframe is supplied.

## Maximum conclusion

The full screen does not invalidate the conditional Hopf bridge. It exposes a stronger
founded-depth-normalized contact/Hopf-bundle route on the chosen twisted `S3` coframe and proves
that its unit topology is insensitive to both screen shears. It simultaneously proves that the
general screen supplies no toric symmetry, cap class, free fiber, metric descent, round quotient,
carrier configuration space, action, or physical selector by itself.
