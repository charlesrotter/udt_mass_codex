# Exact derivation and classification basis

This document records mathematical identities used in the census. None is a
field equation, an action choice, a density law, or a physical branch
selection.

## 1. Configuration and ontology

The prospective configuration is

```text
X=(metric/coframe, any native matter fields, slice/observer protocol,
   seal and boundary/corner data, gluing/moduli, connection/lattice data,
   topology sector).
```

Two branches remain live. In `CALIBRATED_METRIC_PRIMARY`, proper measures are
metric objects once their domains are supplied. In
`CONFORMAL_CLASS_PRIMARY_REQUIRING_REPRESENTATIVE`, the corresponding physical
values require a representative. For a constant representative change
`g -> Omega^2 g`,

```text
V4 -> Omega^4 V4,
V3 -> Omega^3 V3,
A2 -> Omega^2 A2,
int_Sigma sqrt(h) R -> Omega int_Sigma sqrt(h) R.
```

The exact weights prevent the two ontology branches from being silently
spliced into one complete observable definition.

## 2. Metric measures and their complete first channels

With `H_ab=delta g_ab`, a fixed spacetime region has

```text
delta V4 = 1/2 int_M sqrt(|g|) g^ab H_ab.
```

With `H_ij=delta h_ij`, a fixed spatial region has

```text
delta V3 = 1/2 int_Sigma sqrt(h) h^ij H_ij.
```

For a fixed nonnull boundary of intrinsic dimension `k`,

```text
delta A_k = 1/2 int_Bk sqrt(|gamma_k|) gamma^AB delta gamma_AB.
```

If the hypersurface moves outward by normal displacement `chi_n`, the area
also contains

```text
int_B sqrt(gamma) K chi_n,
```

using `K_AB=(1/2)L_n gamma_AB`. For a spatial two-boundary `k=2`; for a
nonnull codimension-one spacetime seal `k=3`. Null or type-changing boundaries
require a different measure/normal formalism. Volume integrals similarly
acquire swept-volume terms. Corners, gluing data, changing moduli, and a
physical boundary functional add further channels. Thus the fixed-domain bulk
formula is exact but not the complete finite-cell response.

Pure trace-free angular variations have zero first variation of proper volume.
This is a precise projection statement; it does not say every possible global
observable is blind to angular shape.

## 3. Density quotient

If a same-solution native total mass `M[X]` and proper volume `V[X]` existed,

```text
rho=M/V,
delta rho=(delta M-rho delta V)/V.
```

The quotient rule is exact. It does not supply `M`, select `V`, or define their
common domain. No unconditional native total-mass functional is present in the
registered record, so this is a conditional interface rather than a current
observable.

## 4. Integrated curvature comparison

For the mathematical candidate

```text
I_R[h]=int_Sigma sqrt(h) R[h],
```

the metric variation with respect to `H_ij=delta h_ij` is

```text
delta I_R = int_Sigma sqrt(h)(1/2 R h^ij-Ric^ij)H_ij
          + int_boundary sqrt(gamma)
              n^i(nabla^j H_ij-nabla_i tr(H)).
```

In an orthonormal Ricci eigenframe, the trace-free variation
`H=diag(1,-1,0)` produces

```text
delta I_R|bulk,TF = -r1+r2.
```

So metric curvature can carry a trace-free angular response that volume alone
cannot. The calculation establishes availability, not native selection. The
same registered premises admit infinitely many curvature functionals and
boundary improvements with different covectors.

## 5. Local, path-global, stratified, and discrete objects

- Riemann, Ricci, Weyl, scalar curvature, Cartan components, and toric
  connection curvature are local geometric data.
- Open-path Levi-Civita transport is an endpoint-frame map. Based-loop
  holonomy is a group element; conjugacy data remove the base-frame choice.
  Both change under a nonconstant conformal representative change. The exact
  identity `delta integral_gamma S=integral_gamma delta S` belongs only to the
  abelian torus connection on a fixed path; it does not verify Levi-Civita
  holonomy.
- Continuous torus-connection holonomy and discrete `GL(2,Z)` monodromy are
  different objects with different variation types.
- For a primitive character, distinguish
  `q_w=w^T H^-1 w`, `ell_w=sqrt(q_w)`, the systole value `min q_w`, and the
  argmin set `W_min`. Their exact fixed-character variations are
  `delta q_w=-w^T H^-1(delta H)H^-1 w` and
  `delta ell_w=delta q_w/(2 ell_w)`. At a tie, the ordinary directional
  derivative of `min q_w` is the minimum active slope, its Clarke
  subdifferential is the active-gradient convex hull, and `W_min` itself is a
  set-valued jump. Physical lengths additionally need common angular scale and
  period data.
- `X_max` is presently typed as a supremum, not a proved attained maximum. A
  first variation through a maximizing pair exists only if the supremum is
  attained by a unique stable pair with a unique regular controlling geodesic.
  Nonattainment has no such derivative; cut loci and multiple maximizers are
  nonsmooth/set-valued. The universal UDT separation `D_g` remains open.
- Cap, gluing, orientation, topology, Hopf, Chern, winding, and degree labels
  are discrete on a smooth fixed sector. They cannot be used as infinitesimal
  response coordinates.

## 6. Units and observational anchors

For `c^a G^b`, the `(L,M,T)` exponents are

```text
(a+3b, -b, -a-2b).
```

No `a,b` give a length or a mass density. The combination `c^2/G` has units
of mass per length. A separately supplied length `X` would allow
`c^2/(G X^2)` to have density units, but neither dimensional consistency nor
the observed values of `c_E` and `G_obs` select `X` or a state functional.

## 7. Counterfamilies

The following exact controls share the currently relevant premise type while
changing the response:

1. `S0=(x^2+y^2)/2` and `S1=S0+lambda*x*y` share the realized root at the
   origin but have different off-shell covectors.
2. `B=lambda_b*q^2/2+mu_b*T` changes both boundary-field and boundary-shape
   equations without changing a supplied bulk equation.
3. `C0=u` and `C1=(1+x^2)u` have the same real zero set and different
   conormal normalization.
4. `F0(u)=0` and `F1(u)=u/2` have the same fixed point `u=0` but different
   fixed-point linearizations.
5. Distinct loops, lifts, completions, and conformal representatives change
   global readouts while retaining the same local metric type.

Therefore a root, window, fixed point, local identity, or supplied realized
configuration does not determine a differentiable physical closure section.

## 8. Two-arrow bootstrap test

The correct working architecture remains

```text
A(X,O)=0,
O-R[X]=0.
```

The census finds exact conditional recomputation maps for several possible
components of `O`; it does not find a registered principle that selects the
component list, physical ontology, targets, normalizations, dual pairing, or
boundary/global completion. `ASSEMBLY_BLOCKER_LEDGER.tsv` proves that taking a
union of individually useful components cannot repair those shared blockers.
No complete `R[X]` or `A(X,O)` exists on one coherent domain. This conclusion
is bounded to the preregistered 26 candidate families and twelve principles.
