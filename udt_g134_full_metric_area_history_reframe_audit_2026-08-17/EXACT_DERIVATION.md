# G134 exact derivation — full-metric area rule and physical-history reframe

Date: 2026-08-17

## 1. Landing

The full-metric area bilinear is a faithful repackaging of the complete metric, including common
scale, once its complete cross-plane values are supplied. It is not merely another reduced pair
scalar.

It therefore supplies a nontrivial **relation-network admissibility condition**: arbitrary
independent plane areas and cross-areas do not assemble into a metric. Locally, metric-induced area
bilinears occupy a ten-dimensional locus inside the twenty-one-dimensional space of symmetric
bivector bilinears.

It does not supply a **physical-history selector**. Every regular Lorentz metric automatically
induces one lawful area bilinear. Current Reciprocity and co-presence premises do not add an
equation assigning its numerical values or choosing one smooth field from that metric-induced
locus.

The bounded landing is

```text
AREA_BILINEAR_METRIC_FAITHFUL;
RELATION_NETWORK_ADMISSIBILITY_REFRAMED;
COMPLETE_AREA_VALUES_EQUIVALENT_TO_COMPLETE_METRIC_VALUES;
PHYSICAL_HISTORY_VALUE_LAW_OPEN.
```

## 2. Type and notation

Let `V` be a real vector space of dimension `n>=3`, and let `g` be a nondegenerate symmetric
bilinear form. Its induced symmetric bilinear form on bivectors is

```text
A_g(u wedge v,w wedge z)
  =g(u,w)g(v,z)-g(u,z)g(v,w).                       (1)
```

For a simple bivector `B=u wedge v`,

```text
A_g(B,B)=det(g restricted to span(u,v)).             (2)
```

For a timelike observer plane this is negative, and `sqrt(-A_g(B,B))` is its positive area norm.
The complete object is a section of `Sym^2(Lambda^2 T* M)`. Individual plane self-areas are only
its diagonal values on simple bivectors.

## 3. Complete `A_g` determines `g` up to sign

### Theorem

Let `g` and `h` be nondegenerate symmetric bilinear forms on `V`, with `dim V>=3`. Then

```text
A_h=A_g  iff  h=+g or h=-g.                          (3)
```

When the UDT clock-negative/ruler-positive Lorentz signature convention is fixed in four
dimensions, `-g` has the opposite inertia convention, so only `h=g` remains.

### Proof

There is a unique invertible `g`-self-adjoint map `S` such that

```text
h(u,v)=g(Su,v).
```

Using (1),

```text
A_h(u wedge v,w wedge z)
  =A_g(Su wedge Sv,w wedge z)
  =A_g((Lambda^2 S)(u wedge v),w wedge z).           (4)
```

Because `A_g` is nondegenerate on `Lambda^2 V`, equality `A_h=A_g` implies

```text
Lambda^2 S=I.                                        (5)
```

For every independent `u,v`, equation (5) says `Su wedge Sv=u wedge v`, so `S` preserves every
two-plane. In dimension at least three, any line is the intersection of two distinct two-planes;
therefore `S` preserves every line. A linear map preserving every line is `S=lambda I`. Equation
(5) then gives `lambda^2=1`, hence `S=+I` or `S=-I`. The converse follows immediately because (1)
is quadratic in the metric. QED.

### Consequence

A complete smooth area-bilinear field that is known to be metric-induced reconstructs the smooth
metric pointwise, up to the globally fixed sign convention. Once those numerical area values are
physically supplied, no second selector is needed between them and the metric history.

## 4. Local information count and the eleven compatibility directions

In four dimensions:

```text
dim Sym^2(T*) = 10,
dim Sym^2(Lambda^2 T*) = 6*7/2 = 21.
```

The exact Jacobian of `g -> A_g`, written in ten metric coordinates and twenty-one independent area
coordinates, has rank ten at both the Minkowski metric and an independently chosen generic rational
Lorentz metric. Its left nullspace has dimension eleven.

The analytic differential is injective at every nondegenerate `g`: if `k(u,v)=g(Su,v)`, the
linearized area map is the induced Lie-algebra action

```text
u wedge v -> Su wedge v + u wedge Sv.
```

That representation is faithful for dimension at least three. Its vanishing first forces `S` to
be scalar, and the scalar action is `2 lambda I`, so `lambda=0`.

Therefore the metric-induced area locus has local dimension ten and local codimension eleven in
the regular twenty-one-dimensional area-bilinear arena. These eleven directions are genuine
compatibility restrictions on independently assigned plane/cross-plane data. They are not eleven
field equations selecting one of the remaining ten metric functions.

## 5. Common scale is present

For a positive conformal change `g -> Omega^2 g`,

```text
A_g -> Omega^4 A_g.                                  (6)
```

In a bivector basis in four dimensions,

```text
det A_g=(det g)^3.                                    (7)
```

Thus complete numerical `A_g` retains the common metric scale that terminal `phi_pair` and
`c_eff/c_E` discard. This does not source that scale. It says the full area object carries it after
the numerical metric/relation field is supplied.

## 6. Individual plane areas are not the complete object

In one fixed labelled basis, consider

```text
g_+=[[-1, +1/2,0,0], [+1/2,1,0,0], [0,0,1,0], [0,0,0,1]],
g_-=[[-1, -1/2,0,0], [-1/2,1,0,0], [0,0,1,0], [0,0,0,1]].
```

All six coordinate-plane self-areas `A_g(e_i wedge e_j,e_i wedge e_j)` agree, because those
principal minors see the square of the off-diagonal entry. But the cross-area

```text
A_g(e_0 wedge e_2,e_1 wedge e_2)=+1/2 or -1/2
```

separates the two metrics. Hence a list of observer-plane densities is not automatically the full
area bilinear. Cross-plane soldering or enough known complete pullbacks remains load-bearing.

## 7. What Reciprocity contributes

On the abstract founded clock/ruler channel space,

```text
K=[[0,1],[1,0]],
D(delta)=diag(exp(-delta),exp(+delta)),
D^T K D=K,
det D=1.
```

The determinant-one statement makes the action on the two-channel area line trivial. But every
`SL(2)` map preserves that area line. For example,

```text
U=[[1,1],[0,1]],
det U=1,
U^T K U != K.
```

Therefore area preservation alone is weaker than dual Reciprocity and does not select `D`,
`delta`, or the physical comparison map.

Conversely, if a spacetime tangent map preserves the complete `A_g`, then its pullback metric has
the same area bilinear. The theorem gives `L* g=+g` or `-g`; the Lorentz inertia convention excludes
the minus case. Thus the stabilizer of complete `A_g` is the Lorentz isometry group of `g`.

These are different types: founded `D` acts on the abstract reciprocal channel representation,
while complete `A_g` acts on spacetime bivectors. Current premises do not derive a universal solder
identifying every such channel action with a spacetime tangent isometry.

## 8. What co-presence and overlap contribute

If all observer relations are declared to belong to one complete metric solution, their complete
area data must be restrictions of one smooth `A_g` and obey ordinary tensor overlap descent. This
is a strong consistency test on independently supplied relation data.

It is not a numerical value law. For every smooth Lorentz metric `g`, equations (1) and ordinary
tensor transformation already give a smooth compatible `A_g`. Neither co-membership nor overlap
descent adds an equation of the form

```text
F(A_g, derivatives of A_g, global data)=0
```

that excludes one otherwise regular metric history.

## 9. Explicit history nonselection witness

On the same annular central-spherical domain, restore `c_E` if desired and consider

```text
g_s=-s c_E^2 dt^2+s^-1 dr^2+r^2 dOmega^2,
s>0 constant.                                        (8)
```

Every member has the same reciprocal base determinant `-c_E^2`, admits the founded reciprocal
channel structure, and defines one smooth co-present area field. Yet `s=1/4` and `s=4` are
inequivalent: at invariant areal radius `r=1` their scalar curvatures are respectively

```text
R=2(1-s)/r^2 = 3/2 and -6.
```

Their full area bilinears are different, as they must be if the area object is faithful. The area
rule correctly records which history was supplied; its existence does not select between them.

## 10. Reframed physical-history question

The result removes one false gap and preserves one real gap.

- **Removed:** after a complete, metric-induced, numerically valued area field is supplied, there is
  no further question of which metric it represents. It already is the metric in bivector form.
- **Preserved:** the current founding premises do not assign that field's numerical values or give
  its evolution/global-admissibility law.

The clean forward question is therefore not “which history should be selected after evaluating all
planes?” It is:

```text
Do Reciprocity and co-presence supply a nonidentity differential or global condition on the one
complete metric/area field, beyond metricity and ordinary overlap compatibility?
```

G134 finds no such additional condition in the bounded active premise spine. It does not prove that
none exists in a future global, causal, or time-live derivation.
