# Conditional curvature-to-phase/current candidate

Status at freeze: UNPROMOTED CANDIDATE; separate-context direct review pending.
Exact scope and recipe: WORK_ORDER.md, frozen at commit 6ac76b46; accepted source
snapshot b304c89f567b9bc301239b631d7a84c91485767d. All assertions below concern
the supplied constant-real-A family, not generic Ricci-flat metrics. No physics
is inferred merely from naming a geometric tensor.

## 1. Inputs and maximum conclusion

Take a regular local chart with

\[
 g=-2du\,dv+dx^2+dy^2+Hdu^2,\qquad H=A(x^2-y^2),\quad A\ne0.
\]

Supply a time orientation; for components let \(\partial_v\) be future.
G313 admits this metric branch conditionally in its inherited owner-provisional
vacuum arena. It does not choose this as an actual physical history. The new
quadratic Weyl/dual recipe is an explicitly chosen mathematical operation, NOT
an accepted UDT physical current or response equation. G351/G352 supply their
provisional conservation/readout interpretations and the chosen product target,
not an identification of this candidate with populated physical content.

The proposed result is existence and fixed-recipe uniqueness of a geometric
null phase gradient/current on this branch, with a compatible local geometric
product measure under a specified label identification. No universal route,
physical population, source, detector, carrier, mass, light, scale or canon.

## 2. Full quadratic tensor, not just an observer contraction

Write \(\ell=du\). In the convention frozen in the work order the only
independent curvature components are

\[
 R_{uxux}=-A,\qquad R_{uyuy}=A;
 \qquad R_{ab}=0,\quad W=R.
\]

All other nonzero lower components follow by the two pair antisymmetries and
pair interchange. There are no lower v indices in W. This follows directly from
\(R_{uiuj}=-\tfrac12H_{,ij}\): the nonzero Christoffel symbols are
\(\Gamma^v_{ux}=\Gamma^v_{xu}=\Gamma^x_{uu}=-Ax\) and
\(\Gamma^v_{uy}=\Gamma^v_{yu}=\Gamma^y_{uu}=Ay\).
In particular \(\Gamma^u_{ab}=0\) and \(\det g=-1\).

For \(\epsilon_{uvxy}=+1\), the first-pair dual has transverse block
\({}^\star W_{uiuj}=\begin{pmatrix}0&A\\A&0\end{pmatrix}\).
Its remaining components again have one u and one transverse index in each
pair. This dual can be checked directly by raising the last two epsilon
indices with \(g^{uv}=-1,g^{uu}=0,g^{xx}=g^{yy}=1\).

In

\[
 B_{abcd}=g^{ef}g^{hi}
 (W_{aech}W_{bfdi}+{}^\star W_{aech}{}^\star W_{bfdi}),
\]

any contracted lower u would have to pair with a lower v, which is absent.
Consequently the contracted indices must all be transverse, and the four
uncontracted indices must all be u. The two squared transverse norms are
\(2A^2\) each. Thus the FULL tensor identity is

\[
                 B=4A^2\,\ell^{\otimes4}.                 \tag{1}
\]

Reversing volume orientation changes the sign of the dual but not B. Reversing
the Riemann sign changes W and its dual together and also leaves B unchanged.
This argument covers every constant real nonzero A, not only the saved examples.

## 3. Root, normalization, closure and conservation

Set \(b=\sqrt{2|A|}>0\). Equation (1) has exactly two real covector fourth
roots, \(\pm b\,du\). To see full covector uniqueness, any root \(\eta\)
has \(\eta(\partial_u)^4=4A^2\ne0\); its mixed \((u,u,u,z)\) components force
\(\eta(z)=0\) for every z in the kernel of du. The remaining coefficient
has only the two real signs. The supplied time orientation selects

\[
 \beta=-b\,du,\qquad C=\beta^\sharp=b\,\partial_v.        \tag{2}
\]

Both full covector magnitude and sign are fixed for THIS recipe. No prescribed
phase or free amplitude function was inserted. An arbitrary future timelike U
can compute the same covector by

\[
 \beta_a=-\frac{B_{abcd}U^bU^cU^d}
                   {[B_{bcde}U^bU^cU^dU^e]^{3/4}}.       \tag{3}
\]

Indeed \(U^u>0\), so numerator/denominator cancel to (2), independent of U's
normalization or transverse components. U is a removable algebraic auxiliary,
not a preferred physical observer. Equation (3) is used only on this nonzero
positive pure-fourth-power class; it is not a general tensor-root algorithm.

Since b is spacetime constant and \(\Gamma^u_{ab}=0\),

\[
 \nabla_a\beta_b=0,\quad g^{-1}(\beta,\beta)=0,\quad
 d\beta=0,\quad \nabla_aC^a=0.                            \tag{4}
\]

The explicit local primitive is \(\Theta=-bu+\Theta_0\). Its sole primitive
freedom with (2) fixed is an additive constant on a connected patch. Multiplying
the gradient is NOT another root of the same B. C is parallel and therefore an
affinely parameterized null geodesic generator; no affine normalization is lost
by taking only a hypersurface restriction.

At A=0 recompute the recipe: W=B=0 and the only real fourth root is zero. There
is no nonzero phase from this recipe there. Substituting zero into (3) is invalid;
flat spacetime still admits independently supplied nonzero null phases. The
formula b(A) tends continuously to zero but is not smooth in the parameter at
zero; no smooth nondegenerate extension through A=0 or perturbative stability
claim is made.

## 4. Induced amount and the G352 product comparison

Use \(\theta=\Theta-\Theta_0=-bu\), \(r=v/b\) and retain labels (x,y).
Then

\[
 g=2d\theta\,dr+dx^2+dy^2+
       \tfrac12\operatorname{sgn}(A)(x^2-y^2)d\theta^2,
 \qquad C=\partial_r.
\]

With the original volume form \(du\wedge dv\wedge dx\wedge dy\),

\[
 j=\iota_C\mathrm{vol}_g=-b\,du\wedge dx\wedge dy
                        =d\theta\wedge dx\wedge dy.      \tag{5}
\]

It is horizontal and invariant under the local C flow and thus descends to its
local three-dimensional quotient. Taking positive density removes orientation
signs: \(d\Xi=|d\theta|\otimes dxdy\). This is a geometric amount measure.
For any specified finite-area label patch V, the chosen Brinkmann cross-phase
identification and any supplied constant \(\Delta>0\), set

\[
 d\mu=\Delta\,dxdy\big|_V,\qquad
 d\Xi=\frac{|d\Theta|}{\Delta}\otimes d\mu.              \tag{6}
\]

Thus a phase-independent continuous product representation exists locally on
the supplied product patch. Finite mu follows from finite area of V, not from
the full infinite plane or an inferred populated edge. No physical cutoff is
introduced. The chosen coordinates demonstrate one identification; neither C's
generator flow within each phase nor this calculation selects which labels on
different phases denote the same physical content.

Every cut \(\theta=\theta_i,r=\tau_i(x,y)\) has intrinsic metric
\(dx^2+dy^2\), even for nonconstant smooth tau. Hence J=1, s=Delta and the
G351 mathematical density is n=Delta. For any supplied future unit timelike U,

\[
 \omega=-U\cdot\beta=bU^u>0,\qquad
 \Gamma=\frac{\omega}{\Delta}\frac{s}{J}
        =\omega=-g(U,C).                                  \tag{7}
\]

These are identities for this smooth geometric measure and the G352 chosen
continuous readout. They do not derive an atomic crossing count, singular
measure, physical detector response, populated source or energy per crossing.

## 5. Four distinct scaling operations

1. Passive null-coordinate change \(u'=a u,v'=v/a\), a>0, gives
   \(A'=A/a^2,b'=b/a\). Then \(-b'du'=-bdu\): the tensor/current is
   unchanged. A's displayed component is not an invariant selected scale.
   The nontrivial mixed-chart recomputation additionally checks full covariance.

2. G352 phase gauge \(\Theta'=a\Theta+c,\Delta'=a\Delta\) at FIXED C and
   mu leaves Xi and Gamma unchanged. The new raised phase gradient is
   \(k'=(d\Theta')^\sharp=aC\); current representation becomes C=(1/a)k'.
   It does not remain C=k'. Here s remains Delta, not Delta'. Replacing mu by
   Delta' dxdy while also setting C=k' would change amount/current; it is not
   the fixed-input gauge. A rescaled phase gradient is not the fixed-B root.

3. Constant metric homothety \(g\mapsto h^2g\), h>0, gives lower
   \(W\mapsto h^2W\), lower B and beta unchanged, \(C\mapsto h^{-2}C\),
   \(\mathrm{vol}\mapsto h^4\mathrm{vol}\), and j,Xi,mu,area multiplied
   by h^2. A unit observer becomes U/h and Gamma becomes Gamma/h.
   This is not a passive coordinate change or selection of the metric's scale.

4. Replacing the fixed recipe by \(q^4B\), q>0, would scale beta and C by q
   at fixed metric. It is a DIFFERENT chosen recipe, not residual freedom of
   the root in (1). Fixed-recipe uniqueness says nothing about physical choice
   of its coefficient or adoption of any such recipe.

With length coordinates and the metric proper-length convention, A has units
L^-2 and Theta is dimensionless. Equation (5) has units L^2: its transverse
amount scales as area, as the homothety check independently exposes. Declaring
this a dimensionless physical population count would need a justified
identification/conversion, not merely a relabeling of coordinates or choosing
Delta. G351's abstract measure permits amount units; G352 supplies no such
physical identification here. This test does not decide whether an accepted
bridge, an alternative realization, no identification, or an additional premise
would ultimately be warranted.

## 6. Evidence limits and adverse outcomes

The analytic component-support argument supplies the family-wide identity;
symbolic full 4D arrays check its algebra. Four rational A witnesses, cut/observer
controls and deliberate mutations check implementation paths, not generic
vacuum existence or a completeness theorem. A stdlib saved-artifact check is a
distinct arithmetic implementation by the SAME author/context, not review.

The initial baseline failure and pre-freeze correction are retained: symbolic
real-A simplification could not certify a division-derived expression across
A=0. Exact positive/negative symbolic branches now certify equivalence, while
the flat tensor/root is recomputed separately. No tolerance was loosened and
neither sign was discarded. Direct candidate review remains a separate gate.

Failure of a full tensor, root, closure, covariance or product identity would
refute/narrow this proposed local construction. Such failure has not appeared
in the author checks. In contrast, area-valued amount, unselected support and
cross-phase identification, flat degeneration and recipe choice already count
against any STRONGER claim that the calculation selects G352 physical content
or supplies a universal native physical law. They do not refute the stated
local geometric existence claim. No acceptance or scientific promotion follows.
