# G233 exact derivation — primary-profile Cartan closure discriminator

Date: 2026-08-23

## 1. Bounded arena

The only metric input is the declared primary static-spherical reciprocal areal family

\[
g=-f(r)c_E^2dt^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0.
\]

Choose one regular orbit \(r_0>0\) and the invariant log-areal coordinate

\[
s=\log(r/r_0).
\]

The test profiles are

\[
\phi_b(s)=s^3+c s^4+b s^5.
\]

The parameters \(b,c,r_0\) are exact discriminator values, not proposed physical coefficients.
No profile is fitted or selected.

## 2. Direct full-metric scalar curvature

In coordinates \((t,s,\theta,\varphi)\), the full metric is

\[
g=\operatorname{diag}
\left(-c_E^2f,\frac{r_0^2e^{2s}}f,r_0^2e^{2s},r_0^2e^{2s}\sin^2\theta\right).
\]

Direct Christoffel and Ricci contraction gives

\[
\mathcal R=\frac{e^{-2s}}{r_0^2}
\left[-f_{ss}-3f_s+2(1-f)\right].
\]

This is the full four-dimensional scalar curvature, not an imported field equation or a reduced
tidal ansatz.

The outward unit areal-radial vector is

\[
n=\frac{e^{-s}\sqrt f}{r_0}\,\partial_s
=\frac{e^{-s-\phi}}{r_0}\,\partial_s.
\]

Direct connection evaluation gives \(\nabla_n n=0\). Therefore, for scalar curvature,

\[
(\nabla^k\mathcal R)(n,\ldots,n)=n^k\mathcal R.
\]

## 3. Exact G231-state collision

For two values of \(b\), every metric component and every partial derivative through total order
four agrees at \(s=0\). Only the \(tt\) and \(ss\) components first differ at fifth order; angular
components are independent of \(b\).

Every component of \(R\), \(\nabla R\), and \(\nabla^2R\) is a universal expression in the metric
jet through orders two, three, and four respectively. Hence the two metrics have exactly the same
complete G231 state in the common coordinate and adapted orthonormal-frame identification:

\[
(R,\nabla R,\nabla^2R)_{b_1}
=(R,\nabla R,\nabla^2R)_{b_2}.
\]

This is stronger than agreement of a selected scalar summary.

## 4. Invariant next-order separation

Direct substitution gives

\[
\begin{aligned}
\mathcal R|_0 &=0,\\
n\mathcal R|_0 &=\frac{12}{r_0^3},\\
n^2\mathcal R|_0 &=\frac{24(2c-1)}{r_0^4},\\
n^3\mathcal R|_0 &=\frac{12(20b-24c+1)}{r_0^5}.
\end{aligned}
\]

Thus

\[
\boxed{
\Delta\left[(\nabla^3\mathcal R)(n,n,n)\right]
=\frac{240\,\Delta b}{r_0^5}.
}
\]

Because \(\nabla g=0\), derivatives of \(\mathcal R\) are contractions of the corresponding
derivatives of the full Riemann tensor. The outward unit \(n\) is fixed invariantly by increasing
areal radius on this regular stratum. The displayed difference is therefore not a coordinate or
frame artifact.

## 5. Arbitrary finite-order obstruction

Let the candidate state contain the complete curvature tower through \(\nabla^N R\). It depends on
the metric jet through order \(N+2\). Compare

\[
\phi_b(s)=\phi_0(s)+b s^{N+3}.
\]

All members share the metric \((N+2)\)-jet and hence the complete curvature state through
\(\nabla^N R\).

The highest derivative term in scalar curvature is

\[
\mathcal R
=\frac{2e^{-2s}f}{r_0^2}\phi_{ss}
+\text{terms with lower derivatives of }\phi.
\]

Applying \(n^{N+1}\), the first differing term at the quiet orbit is

\[
\boxed{
\Delta\left[n^{N+1}\mathcal R\right]_0
=\frac{2(N+3)!}{r_0^{N+3}}\,\Delta b.
}
\]

It is nonzero for distinct \(b\). Therefore no local finite-order natural state built from the
metric jet can carry one family-uniform autonomous derivative law over the unrestricted primary
profile arena.

This does not exclude a nonlocal law, an infinite-jet state, or a separately founded smaller
family.

## 6. Fixed-member and finite-family controls

For one completely supplied \(\phi(r)\), areal radius is the symmetry-reduced Cartan coordinate and

\[
e_{\hat r}=e^{-\phi}\partial_r.
\]

The member therefore has a finite local Cartan evaluator whose structure functions already contain
the supplied profile.

For the separately declared G204 family

\[
\phi(x)=\frac{a}{2^n}x^2(x^2-1)^n,
\qquad x=r/r_0,
\]

the reduced state \((x,a,r_0;n)\) closes conditionally:

\[
e_{\hat r}x=\frac{e^{-\phi(x;a,n)}}{r_0},
\qquad e_{\hat r}a=e_{\hat r}r_0=e_{\hat r}n=0.
\]

Every local invariant and its radial derivative is a function of that finite state. This is a
lawful control, but the profile family remains `CHOSE` and its parameters remain unselected.

## 7. Exact scoped result

```text
FIXED_MEMBER_CARTAN_DESCENT_IS_EVALUATIVE
__FINITE_G204_CLOSURE_IS_FAMILY_CONDITIONAL
__UNRESTRICTED_PRIMARY_PROFILE_HAS_NO_UNIVERSAL_FINITE_JET_AUTONOMOUS_CLOSURE
__VALUED_PAIR_NETWORK_ENCODES_BUT_DOES_NOT_GENERATE_PROFILE
```

The negative applies only to local finite-order natural autonomous laws uniform over the
unrestricted primary static-spherical profile family. It is not a no-go for full UDT, time-live or
nonspherical histories, nonlocal/global admissibility, infinite-state closure, dynamics, or a
future metric-derived smaller family.
