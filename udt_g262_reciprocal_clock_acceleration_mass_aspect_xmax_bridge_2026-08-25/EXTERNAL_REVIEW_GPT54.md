# External adversarial review — G262

1. Minor finding: the G262 package missed one already-sealed native nonidentity value relation. The
G262 summary says no source/action/boundary law was derived, but the sealed asymptotic audit already
records the exact raw wall lapse flux

\[
\Phi_{\rm wall}=-2\pi X,
\]

while explicitly denying that this is mass until a generator/normalization is supplied. This is a
repair to reporting scope, not a reversal of the bounded landing.

`ACCEPT_WITH_REPAIRS`

1. **Acceleration attack: accepted.** From

   \[
   ds^2=-f c_E^2dt^2+f^{-1}dr^2+r^2d\Omega^2,\qquad N=\sqrt f,
   \]

   using `x^0=c_E t`, one gets

   \[
   \Gamma^r{}_{00}=\frac12 f f',\qquad u^0=N^{-1},\qquad
   a^r=\Gamma^r{}_{00}(u^0)^2=\frac12 f',
   \]

   and therefore in the outward orthonormal static frame

   \[
   a_{\hat r}=\frac{a^r}{\sqrt f}=\frac{f'}{2\sqrt f}=N'.
   \]

   The dimensional proper acceleration is `c_E^2 N'`.

2. **Mass-aspect and angular-mode attack: accepted.** With

   \[
   \mu=\frac r2(1-f),\quad \mu'=\frac{1-f-rf'}2,\quad
   \mu''=-f'-\frac r2 f'',
   \]

   the residuals are exactly

   \[
   E_0=rf'+f-1=-2\mu',\qquad E_1=rf'+\frac{r^2}{2}f''=-r\mu''.
   \]

   Using G201's

   \[
   A_\parallel=e^{-2\phi}(2p^2+p-q),\qquad
   A_\perp=1-e^{-2\phi}(1+p),
   \]

   with \(f=e^{-2\phi}\), \(p=-rf'/(2f)\), and
   \(q=-r^2(f''f-f'^2)/(2f^2)\), the reviewer recomputed

   \[
   A_\parallel=\frac{r^2f''-rf'}2=-r\mu''+3\mu'-\frac{3\mu}{r},
   \]

   \[
   A_\perp=1-f+\frac{rf'}2=\frac{3\mu}{r}-\mu',
   \]

   so

   \[
   A_\parallel+A_\perp=2\mu'-r\mu''=E_1-E_0.
   \]

   Signs and factors are correct.

3. **`mu` ownership attack: accepted against promotion.** The sealed source set consistently treats
   \(\mu(r)=r(1-f(r))/2\) as only a metric change of variables, and
   \(M=c_E^2\mu/G_{\rm obs}\) as only a conditional GR/Misner--Sharp-style attachment, not native
   UDT mass.

4. **Endpoint-type attack: numerically yes, typewise distinct.** G216 gives

   \[
   \delta_{os}=-(\log d\tau_s/d\tau_o),\qquad
   q_{os}=\frac{d\tau_s}{d\tau_o}=e^{-(\phi_s-\phi_o)},
   \]

   while G243 gives \(Z_{so}=e^{\phi_s-\phi_o}\), and G95 gives under the
   carrier-covector premise

   \[
   \epsilon_{so}=\frac{E_o}{E_s}=\frac1{Z_{so}}.
   \]

   Hence

   \[
   \frac{d\tau_s}{d\tau_o}=q_{os}=\frac{E_o}{E_s}=e^{-(\phi_s-\phi_o)}
   \]

   numerically, but the arrows remain type-distinct exactly as the preregistration repair states.

5. **Mass-character attack: accepted.** Positivity lets \(G(x)=\log F(e^x)\); then

   \[
   F(q_1q_2)=F(q_1)F(q_2)\Rightarrow G(x+y)=G(x)+G(y).
   \]

   Continuity or measurability forces \(G(x)=wx\), so \(F(q)=q^w\). But the sealed founding
   composition law is about positional operators, not a physical mass observable, so the mass
   object, the mass-composition premise, and \(w\) are genuinely unowned.

6. **Projective-limit attack: accepted.** From \(\chi=\tanh\delta\),

   \[
   \chi=\frac{1-e^{-2\delta}}{1+e^{-2\delta}}=\frac{1-q^2}{1+q^2},
   \qquad
   q=\sqrt{\frac{1-\chi}{1+\chi}}.
   \]

   The report correctly separates directional pair-energy zero/infinity from local invariant rest
   mass, and separately from the static-chart compactness limit \(\mu/r\to1/2\) when \(N\to0\) at
   finite areal radius.

7. **Nonselection attack: accepted.** The hierarchy is derived for arbitrary positive \(f\), and
   the explicit counterfamily

   \[
   f_0(r)=1,\qquad f_a(r)=1+\frac{ar^2}{1+r^2},\quad0<a<1
   \]

   shows two distinct profiles satisfying every hierarchy identity. That makes the construction
   evaluative, not a history equation selecting \(\phi\).

8. **Independent replay / mutation-harness attack: accepted with one runtime caveat.**
   `verify_independent.py` is implementation-distinct and uses only the Python standard library; it
   replays exact algebraic identities over 1,000 rational cases without importing production code
   or reading production results. `run_catch_proofs.py` explicitly limits itself to regression
   checks, not independent scientific proof, which is the correct role. The reviewer reran
   `verify_independent.py`, `run_catch_proofs.py`, and `verify_package.py`; all passed. The reviewer
   could not rerun `derive_hierarchy.py` because SymPy was absent in the isolated runtime.

9. **Missed native law attack.** The only already-sealed nonidentity native value law found that
   G262 did not surface is the exact raw wall lapse flux

   \[
   \Phi_{\rm wall}=-2\pi X.
   \]

   The same source immediately blocks promoting it to mass without a complete
   action/generator/normalization, so this does not strengthen the landing to a mass law.

No bounded scientific defect strong enough for `REJECT` is present in the sealed intake. The needed
repairs are to acknowledge the pre-existing raw-flux value law and, if desired, disclose that the
review runtime reproduced the dependency-free replays but not the SymPy production derivation.

## Preservation note

This file preserves the reviewer's substantive return. Intake-local absolute links in the raw
return have been rendered as repository-relative prose; the review transcript and exact launch
artifacts remain in the ephemeral runtime recorded by `TRANSMISSION_RECORD.md`.
