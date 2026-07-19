# Fresh adversarial review

Date: 2026-07-19

Reviewer context: fresh isolated CPU-only adversarial context; no repository edits

Verdict: **PASS after correction, with the package's bounded-scope caveats.**

## Substantive error caught before banking

The draft general Gaussian-curvature calculation for the conditional axis metric used only
`g_00 R^0_101`. Away from a diagonal point, lowering the first curvature index also requires
`g_01 R^1_101`. The original preregistered point `x=0,a=4` was unaffected because `g_01=0` there,
but the saved general expression was wrong.

The derivation now retains the full contraction and independently checks a non-diagonal point. The
correct result is

\[
 K=-\frac{a-1}{a}\cos(2x),\qquad
 K(0,4)=-\frac34,\qquad
 K(\pi/6,4)=-\frac38.
\]

The verifier contains a fail-closed mutation catch for omission of that term.

## Independent exact checks

For

\[
 e^3=dy+u(r)dx,\qquad q=u',
\]

the independently derived torsion-free connection is

\[
 \omega_{12}=-\frac q2e^3,\quad
 \omega_{13}=-\frac q2e^2,\quad
 \omega_{23}=\frac q2e^1.
\]

It gives

\[
\begin{aligned}
\Omega_{12}&=-\frac{3q^2}{4}e^{12}-\frac{q'}2e^{13},\\
\Omega_{13}&=-\frac{q'}2e^{12}+\frac{q^2}{4}e^{13},\\
\Omega_{23}&=\frac{q^2}{4}e^{23}.
\end{aligned}
\]

Torsion and both Bianchi identities vanish. For `u=lambda(1-r^2)^3`, `u,u',u''` vanish at
`r=+-1`, while at `r=1/2,lambda=1`,

\[
 q=-\frac{27}{16},\qquad q'=\frac98.
\]

The independent coordinate-curvature witness is `729/1024`. This establishes equal *chosen*
endpoint jets with different interior curvature and local loop transport. It does not establish
different global holonomy groups or a family of complete UDT solutions.

For

\[
 h=I+(a-1)n\otimes n,\qquad n=(\cos x,\sin x,0),
\]

the independent axis result above gives, at `x=0,a=4`,

\[
 R=-\frac32,\qquad C_{abcd}C^{abcd}=\frac34,
\]

while

\[
 n\cdot(\partial_xn\times\partial_yn)=0.
\]

Therefore `C^2 != F^2` in this chosen metric class. No global numerical ordering follows.

Under constant `g -> s^2 g` in four dimensions,

\[
 \sqrt{|g|}\to s^4\sqrt{|g|},\qquad
 R\to s^{-2}R,\qquad C^2\to s^{-4}C^2.
\]

EH density has weight `s^2`; Weyl-squared density has weight `1`. Shared curvature ancestry is not a
Cartan identity deriving EH from a `C^2` stage.

## Scope audit

The corrected package does not promote:

- local Cartan identities into dynamics;
- holonomy into matter;
- one comparison family into a global theorem;
- the single-axis metric into native UDT structure;
- the open admissibility/soldering gate into a unique new postulate.

Retaining transverse shear, twist, shifts, and off-diagonal sectors is consistent with current
authority because C0/C1 leave the transverse block, full time-live geometry, lapse/shift response,
and variation domain open. This means those sectors must remain available during completeness
testing; it does not mean nonzero twist or shear has been physically derived.

Maximum honest conclusion: Cartan geometry is metric-derived per chosen representative and exposes
reciprocal/angular interaction cleanly, but current UDT premises do not select a holonomy reduction,
identify holonomy as matter, or close the `C^2`-to-EH bridge.
