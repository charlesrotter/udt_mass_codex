# G208 preregistration — radial-screen mixing robustness

Date: 2026-08-21

## Exact tests

1. **Composition dependency.** For arbitrary supplied `g_A` and pair immersion `F`, verify that
   `g_hat=e^(2 Omega)g_A` gives the same unparametrized null paths, affine relation
   `d lambda_hat=e^(2 Omega)d lambda_A`, pullback `h_hat=e^(2 omega)h_A`, and completed depth
   `Phi_hat=Phi_A-omega`. This decides that common scale plus G207 shear factorizes and need not be
   treated as a prior independent mechanism.
2. **Local mixing algebra.** In an adapted `h0`-orthonormal basis, put `s=|W|` and prove

   \[
   C=\begin{pmatrix}0&s&0\\s&0&0\\0&0&0\end{pmatrix},
   \qquad
   A=e^C.
   \]

   Derive eigenvalues `exp(+s),exp(-s),1`, positivity, `det A=1`, Lorentz signature, and
   `det g_C=det g_0` without calling ambient volume gauge.
3. **Exact radial causal law.** Derive the mixed radial-screen block of `h_C` and minimize over the
   screen velocity at fixed `dr/dt`. Test the sharp inequality

   \[
   \left|\frac{dr}{dt}\right|
   \le f\sqrt{\cosh(2s)}.
   \]

   Identify its equality direction and prove that the unchanged G207 bound is not retained when
   `s` is nonzero.
4. **Growth-controlled global causality.** For every finite time slab `I`, assume a radial envelope
   `s<=b_I(r)` with

   \[
   \int^\infty\frac{dr}{f(r)\sqrt{\cosh(2b_I(r))}}=\infty.
   \]

   Prove or refute that `t` remains Cauchy and `g_C` globally hyperbolic. Bounded mixing must be
   included as a corollary, not assumed as the whole class.
5. **Static null survivor.** For every globally bounded smooth static `C`, compare the optical
   metric `H_C=h_C/f` to the complete G205 optical metric and prove or refute null completeness of
   `g_C=f[-dt^2+H_C]` using the exact affine factor `d lambda=f d lambda_bar`.
6. **Compact-time-live survivor.** Classify smooth mixers that are exactly G205 outside a compact
   time slab and have uniform spatial/operator and relative time-derivative bounds inside it. Use
   causal radial control and the exact null-energy equation; do not infer a universal theorem for
   unbounded live mixing.
7. **Smooth static failure witness.** Fix an axis `a`, use the smooth vector fields
   `R=x^i partial_i` and `U=a cross x`, and construct a center-regular pure mixer with equatorial
   rapidity `sigma(r)=4 phi(r)`. Along the contracting-eigenline spiral

   \[
   r\,d\varphi=-\frac{dr}{\sqrt f},
   \]

   verify that its optical length is

   \[
   \sqrt2\int e^{-\sigma}\frac{dr}{f}
   =\sqrt2\int f\,dr<\infty.
   \]

   Use Riemannian incompleteness to prove or refute global hyperbolicity and null completeness.
   The witness is a chosen control, not a physical history.
8. **Completed pair response.** For `J_i=alpha_i partial_t+v_i`, derive

   \[
   (h_C)_{ij}=-f\alpha_i\alpha_j+h_0(Av_i,Av_j),
   \qquad
   \Phi_C=-\frac12\log[f\alpha_0^2-h_0(Av_0,Av_0)].
   \]

   Classify static-clock, untouched-screen, radial, and generic mixed clock strata. Ambient
   determinant one must not be conflated with pair-area or completed-depth blindness.

## Certification contract

- Production: exact symbolic matrix exponential, determinant, eigenvalue, Schur-complement causal
  law, factorization, witness length, and completed-pair algebra.
- Independent: a separately written rational boost-parameter implementation with at least 10,000
  distinct exact local metric/pair cases, plus an independent optical-length and causal-bound
  derivation that imports no production code or artifacts.
- At least 18 hostile catches covering factorization order, trace, determinant, positivity, radial
  bound, equality direction, bounded/static/time-live scope, witness smoothness, optical length,
  global-hyperbolicity versus null-completeness typing, pair response, mechanization ceiling,
  physical-history selection, and `X_max`.
- Saved artifacts replay byte-identically under `UDT_NO_WRITE=1`.
- Fresh cold adversarial review before final banking.

## Falsification

The strongest candidate landing fails if the factorization order changes any tensorial output, if
the sharp radial bound is wrong, if the slab condition permits finite-time escape, if a bounded
static mixer is null incomplete, if the compact-time survivor fails, if the explicit unbounded
static witness has infinite optical length or remains globally hyperbolic/null complete, or if the
completed pair fails to hear a radial clock component.

## Scope lock

This is one supplied configuration-space tile. It does not classify timelike/spacelike
completeness, trace-changing modes, time-space shift, arbitrary full spatial mixing, a physical
history law, transfer, observations, action/source/matter, or `X_max`.
