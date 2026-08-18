# G152 exact derivation — does the pair immersion own the connecting chord?

Date: 2026-08-17

## 1. Three different vectors

Let \(F(\tau,\sigma)\) be one supplied smooth regular calibrated pair immersion with commuting
coordinate tangents

\[
J_0=F_*\partial_\tau,
\qquad
J_1=F_*\partial_\sigma.
\]

Write its induced metric exactly as

\[
h=-T^2(d\tau+\beta d\sigma)^2+L^2d\sigma^2,
\qquad T,L>0.
\]

The normalized clock and orthogonal ruler are

\[
u=J_0/T,
\qquad
r=J_1-\beta J_0=Ln.
\]

Therefore

\[
\boxed{J_1=\beta T u+Ln.}
\]

The pair immersion owns \(J_1\), and its metric owns \(r\). The working positional chord is a third
object,

\[
\xi=\rho n,
\qquad
\rho=X_{\max}\tanh\phi_{\rm pair}.
\]

Collinearity does not imply equality, and orthogonalizing \(J_1\) does not automatically preserve
its coordinate-variation role.

## 2. Exact magnitude and shift conditions

The terminal pair formula gives

\[
\phi_{\rm pair}=\frac12\log(L/T),
\qquad
\rho=X_{\max}\frac{L-T}{L+T}.
\]

For an orientation label \(\epsilon=\pm1\), equality with the oriented orthogonal ruler,

\[
\xi=\epsilon r,
\]

holds exactly when

\[
\boxed{\rho=\epsilon L.}
\]

Equivalently,

\[
\boxed{T=L\frac{X_{\max}-\epsilon L}{X_{\max}+\epsilon L},}
\]

or

\[
\boxed{X_{\max}^{(\epsilon)}
=\epsilon L\frac{L+T}{L-T}.}
\]

For positive \(T,L,X_{\max}\), either oriented branch requires \(0<L<X_{\max}\) and
\(\epsilon(L-T)>0\). The two branches exchange clock/ruler dominance.

Equality with the oriented coordinate variation is stronger:

\[
\boxed{\xi=\epsilon J_1
\iff \rho=\epsilon L\ \text{and}\ \beta=0}
\]

as a field on the comparison neighborhood. A pointwise zero of \(\beta\) is insufficient for the
derivative statements below.

The displayed `X_max` expression is a candidate readout conditional on this identification. A
universal constant would require the same candidate to remain constant across the supplied family.
Nothing here proves that Nature makes the identification or fixes that constant.

## 3. Exact normalized-flow commutator

Let

\[
f=\rho/L,
\qquad
\xi=f r.
\]

Although \([J_0,J_1]=0\), the normalized clock \(u=J_0/T\) and the orthogonal ruler need not
commute. Direct calculation gives

\[
\boxed{
[u,\xi]
=L\,u(f)n
+f\left[J_1(\log T)-u(\beta T)\right]u.}
\]

Define

\[
\kappa=J_1(\log T)-u(\beta T).
\]

For nonzero \(f\), the working chord is a connecting field exactly when

\[
\boxed{u(f)=0,\qquad \kappa=0.}
\]

If \(\xi=\epsilon r\) as a field, then \(f=\epsilon\) is already constant and only \(\kappa=0\)
remains. In the stronger coordinate-variation subcase with \(\beta=0\) throughout the neighborhood,

\[
\kappa=J_1(\log T),
\]

so proper-time synchronization across the family requires

\[
\boxed{J_1(T)=0.}
\]

Thus the pair immersion owns all ingredients needed to *test* connecting carry, but terminal
reciprocity does not make the test pass automatically.

## 4. Exact counterexamples

1. **Regular but unequal.** With \(T=1,L=3/2,X_{\max}=4,\beta=1/5\), the terminal chord magnitude is
   \(\rho=4/5\), neither oriented ruler magnitude \(\pm3/2\).
2. **Equality without carry.** Let \(X_{\max}=2\),
   \(L(\sigma)=1+\sigma/10\), and
   \(T=L(2-L)/(2+L)\), with \(\beta=0\). Then \(\rho=L\) everywhere, but at \(\sigma=0\),
   \(\kappa=J_1\log T=-1/30\), so \([u,\xi]\ne0\).
3. **Carry without equality.** With constant \(T=1,L=2,X_{\max}=3,\beta=0\), one has
   \(\rho=1\), hence \(f=1/2\), while \([u,\xi]=0\). The carried chord is only half the natural
   ruler variation.
4. **Shift separates the two variations.** At \(T=1/3,L=1,X_{\max}=2\), terminal magnitude matches
   the positive ruler branch. With constant \(\beta=1/7\), \(\xi=r\) may be carried, but
   \(J_1=(1/21)u+n\ne\xi\).

These prove that magnitude identity, coordinate identity, and connecting carry are independent
conditions.

## 5. Maximum conclusion

```text
PAIR_IMMERSION_OWNS_COORDINATE_AND_ORTHOGONAL_VARIATIONS_BUT_NOT_THEIR_IDENTIFICATION_WITH_WORKING_XI__
EXACT_MAGNITUDE_SHIFT_LAPSE_AND_COMMUTATOR_CONDITIONS_CLASSIFIED__
UNIVERSAL_XMAX_WOULD_REQUIRE_CANDIDATE_CONSTANCY_ACROSS_THE_SUPPLIED_FAMILY__
PHYSICAL_IDENTIFICATION_QUERY_HISTORY_DYNAMICS_XMAX_VALUE_AND_COMPLETION_OPEN
```

