# WR-L solution-space closure audit — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic DERIVE + self-CAS; DATA-BLIND |
| Repository | `grok` at `64af120`; pre-existing dirty work preserved |
| MAP frozen first | `UDT_WRL_SOLUTION_SPACE_CLOSURE_MAP.md`, SHA-256 `891905afd7516bd27af9b1f0f5b55a314b5c74ec0f0c6bdb1219a85b44abf6ae` |
| Symbolic verifier | `verify_udt_wrl_solution_space_closure.py` — **55/55 checks pass**, SymPy 1.13.3 |
| GPU | Not used; no determined numerical problem emerged |
| Independent verification | **OPEN** |
| Build-on grade | **PROVISIONAL ANALYTIC LEAD**, not banked and not canon |

No carrier, observed mass, density, fitted parameter, hard cutoff, GR field equation, or EH action is
used.  The live WR-L macro lane and the particle-mass lane remain separate.

## 0. Result

The owner's conjecture was productive.  A sharp constraint really is visible in the WR-L solution
itself:

\[
\boxed{
\left(D^2+\frac{{}^{(3)}R}{4}\right)N=0
=\left(D^2+\frac{R}{6}\right)N,
\qquad N=\sqrt{1-r/X}.
}
\]

It has a finite normalizable lapse mode and a finite wall flux,

\[
\int_\Sigma N^2dV=\frac{64\pi}{105}X^3,
\qquad
\Phi_N(X)=\oint D_iN\,dS^i=-2\pi X.
\]

The identity characterizes

\[
A(r)=1+a r+\frac br.
\]

Boundedness at the seat removes (b/r); (A(0)=1) and (A(X)=0) then give WR-L.  Equivalently,
WR-L is the unique fixed-endpoint minimizer of the simple positive radial functional

\[
\mathcal I[A]
=\frac12\int_0^X\left[r(A')^2+\frac{(A-1)^2}{r}\right]dr.
\]

This is the strongest action lead yet found directly from the selected metric.  It is also an
**inverse variational characterization**, not a derived native UDT action.  The metric does not fix
its off-shell provenance, boundary generator, or normalization, and a tempting covariant-looking
lapse functional fails when the reciprocal metric relation is varied consistently.

The action-independent verdict is therefore:

\[
\boxed{
\begin{gathered}
\text{WR-L contains a simple exact zero-mode/minimum structure and a finite lapse flux;}\\
\text{it does not by itself select a unique action, global completion, mass, compactness,}\\
\text{or matter carrier.  The hidden-constraint lead is real; closure remains OPEN.}
\end{gathered}}
\]

## 1. What the wall selector already fixes

Before wall regularity, residual re-centering gives

\[
A_\alpha(r)=\left(1-\frac rX\right)^\alpha.
\]

The exact endpoint measures are

\[
L_{\rm prop}=\int_0^X A_\alpha^{-1/2}dr
=\frac{X}{1-\alpha/2}\quad(\alpha<2),
\]

\[
L_{\rm opt}=\int_0^X A_\alpha^{-1}dr
\begin{cases}
<\infty,&\alpha<1,\\
=\infty,&\alpha\ge1,
\end{cases}
\]

and

\[
V_\alpha
=4\pi X^3B\!\left(3,1-\frac\alpha2\right)
\quad(\alpha<2).
\]

The already-banked combination of finite proper radius, infinite optical radius, and wall curvature
regularity selects \(\alpha=1\).  For WR-L,

\[
L_{\rm prop}=2X,
\qquad
V_X=\frac{64\pi}{15}X^3,
\qquad
r_*=-X\ln(1-r/X)\longrightarrow\infty.
\]

This fixes the dimensionless shape.  It does not yet say that the static patch is the complete
universe.

## 2. The two endpoints say different things

For

\[
ds^2=-A c^2dt^2+A^{-1}dr^2+r^2d\Omega^2,
\qquad A=1-r/X,
\]

the exact invariants are

\[
R=\frac{6}{Xr},
\qquad
{}^{(3)}R=\frac{4}{Xr},
\qquad
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
=\frac{8}{X^2r^2}.
\]

### Seat \(r=0\)

The seat is a true curvature singularity at finite proper distance.  It also violates the smooth
center condition \(A'(0)=0\).  The singularities are integrable on the static slice,

\[
\int_\Sigma R\,dV=32\pi X,
\qquad
\int_\Sigma{}^{(3)}R\,dV=\frac{64\pi}{3}X,
\qquad
\int_\Sigma K\,dV=\frac{64\pi}{X},
\]

but integrability does not make the center smooth.  A complete theory must therefore choose a
regime transition, remove the seat from the manifold, resolve it with another solution, or abandon
exact global re-centering.  WR-L alone does not choose among them.

### Wall \(r=X\)

At the wall,

\[
R(X)=\frac6{X^2},
\qquad K(X)=\frac8{X^4};
\]

there is no curvature singularity.  With \(\tau=ct\),

\[
v=\tau+r_*,
\qquad dr_*/dr=A^{-1},
\]

the metric becomes

\[
ds^2=-A\,dv^2+2\,dv\,dr+r^2d\Omega^2.
\]

Its \((v,r)\) determinant is \(-1\), including at \(A=0\).  Therefore the metric has a regular
Lorentzian continuation through the wall.  In the static chart, radial light takes infinite (t)
to approach (X); in the regular chart, the ingoing null curves (v=\text{constant}) cross it.
Timelike crossing curves also exist: a curve with (dv/d\lambda=1) and
(dr/d\lambda=-q<0) has norm \(-A-2q\), which remains negative at the wall.

Thus **asymptotic approach in static time is DERIVED**, while **invariant unattainability by every
physical worldline is not**.  Making (X) a terminal boundary exactly analogous to the massive-body
speed limit (c) needs an additional domain/observer rule.

## 3. The metric-born lapse identity and flux

On a static slice let

\[
N=\sqrt A,
\qquad dV=\frac{r^2\sin\theta}{\sqrt A}\,dr\,d\theta\,d\varphi.
\]

For every reciprocal static (A(r)), direct geometry gives

\[
D^2N=N\left(\frac12A''+\frac{A'}r\right).
\]

For WR-L this becomes

\[
D^2N=-\frac{N}{Xr}
=-\frac{{}^{(3)}R}{4}N
=-\frac R6N.
\]

The outward normal flux through a sphere is

\[
\Phi_N(r)
=\oint n^iD_iN\,dS
=4\pi r^2\sqrt A\,N'
=-\frac{2\pi r^2}{X}.
\]

Consequently,

\[
\Phi_N(0)=0,
\qquad
\Phi_N(X)=-2\pi X,
\qquad
\int_\Sigma D^2N\,dV=-2\pi X.
\]

This is a clean finite geometric datum.  It is not a conserved vacuum charge: it varies with the
enclosing radius because (D^2N\ne0).  Nor does geometry supply the coefficient, sign convention,
or boundary primitive needed to call it mass.

The finite result is not an arbitrary cancellation.  For (f=A^p),

\[
\Phi_p(r)
=-\frac{4\pi p r^2}{X}A^{p-1/2}.
\]

At the wall this vanishes for (p>1/2), is finite and nonzero at (p=1/2), and diverges for
(0<p<1/2).  The metric lapse (N=A^{1/2}) sits exactly at the finite-flux threshold.

## 4. Exact inverse variational characterization

The curvature-lapse identity for a general reciprocal (A) is equivalent to

\[
r^2A''+rA'-A+1=0.
\]

Its full solution is

\[
A=1+a r+\frac br.
\]

Requiring (A) bounded at the seat removes (b/r); imposing (A(0)=1) and (A(X)=0) fixes
(a=-1/X).  This reproduces WR-L without the residual functional equation, although the
curvature-lapse equation itself was discovered from WR-L and has not been independently postulated
or derived.

The same ODE is the Euler equation of

\[
\mathcal I[A]
=\frac12\int_0^X\left[r(A')^2+\frac{(A-1)^2}{r}\right]dr.
\]

Completing the square gives

\[
\mathcal I[A]
=\frac12\int_0^Xr\left(A'-\frac{A-1}{r}\right)^2dr
+\frac12\left[(A-1)^2\right]_0^X.
\]

For fixed endpoints (A(0)=1, A(X)=0),

\[
\mathcal I\ge\frac12,
\]

with equality exactly when

\[
rA'=A-1
\quad\Longrightarrow\quad
A=1-r/X.
\]

This is an exact global-minimum theorem.  It also makes the remaining scale degeneracy explicit:

\[
\mathcal I[A_{\rm WR-L}]=\frac12
\]

for every (X>0).

### Why this is not yet the UDT action

The functional was reconstructed after knowing the solution.  Current UDT premises do not yet
derive its areal-(r) measure, its ((A-1)^2/r) term, its off-shell re-centering law, or its boundary
primitive.  Many inverse functionals and total-derivative representatives can share the same
stationary profile.

A more geometric-looking temptation is

\[
\mathcal J[N;\gamma]
=\frac12\int_\Sigma\left[(DN)^2-\frac14{}^{(3)}R\,N^2\right]dV.
\]

Varying (N) while holding (gamma) fixed gives the desired zero-mode equation.  But UDT
reciprocity ties (gamma_{rr}=N^{-2}).  Substituting that relation first and varying the actual one
field (N) gives, on WR-L,

\[
E_N^{\rm reciprocal}ig|_{\rm WR-L}
=\frac{r(5r-6X)}{8X(X-r)}\ne0.
\]

So \(\mathcal J\) is not a reciprocal one-field action for WR-L.  Treating (N) and (gamma) as
independent would be a new off-shell field-space premise.  This is the same kind of
restrict-then-vary issue that the action program must audit, not bypass.

## 5. Global-completion branches remain distinct

| Branch | What is added | Consequence | Status |
|---|---|---|---|
| Causal extension | Continue the regular (v,r) metric through (A=0) | Horizon is not a physical outer boundary; time-live waves see an infinite optical channel | Locally available from metric; global topology OPEN |
| Terminal static cell | Declare (0<r<X) complete | Finite proper volume and a boundary flux; requires a domain law and boundary action | CHOSE if adopted |
| Reflected/glued static slice | Glue another finite proper-distance copy at the extremal sphere | Can make a compact spatial slice; duplicates the singular-center problem and needs gluing data | CHOSE if adopted |
| Seat transition | Replace/excise the (r=0) regime | May cure the true singularity; matching and dynamics unknown | OPEN |

Metric regularity permits the first branch but does not globally forbid the others.  The founding
statement that (X) is unattainable will have to specify whether it means static-chart asymptotics,
a relational-domain boundary, or invariant causal inaccessibility; these are inequivalent.

## 6. Metric-derived operator census

The metric does not supply one unique “matter operator.”  Two immediate scalar choices already
differ.

### 6.1 Four-dimensional scalar probe

For

\[
\psi=e^{-i\omega t}Y_{\ell m}(\Omega)R(r),
\]

the metric d'Alembertian gives

\[
-\frac{d}{dr}\left(r^2A R'\right)+\ell(\ell+1)R
=\frac{\omega^2}{c^2}\frac{r^2}{A}R.
\]

With (u=rR) and (dr_*/dr=A^{-1}),

\[
-\frac{d^2u}{dr_*^2}+V_\ell u
=\frac{\omega^2}{c^2}u,
\]

\[
V_\ell
=A\left[\frac{\ell(\ell+1)}{r^2}-\frac1{Xr}\right].
\]

For every \(\ell\ge1\), (V_\ell>0) on (0<r<X), but (V_\ell\to0) as
(r_*\to\infty).  The horizon is therefore a scattering endpoint, not a finite optical drum; it
does not produce an isolated positive frequency scale.  In the \(\ell=0\) channel, (u=r) is an
exact zero-energy resonance, but it is not wave-normalizable because

\[
\int_0^X\frac{r^2}{A}\,dr=\infty.
\]

The negative \(\ell=0\) potential and singular seat make any further stability statement dependent
on the center completion.  No carrier conclusion follows from this scalar probe.

For a static multipole (f(r)Y_{\ell m}),

\[
(r^2Af')'-\ell(\ell+1)f=0.
\]

If the endpoint term vanishes, exact integration gives

\[
\left[r^2Aff'\right]_0^X
=\int_0^Xr^2A(f')^2dr
+\ell(\ell+1)\int_0^Xf^2dr.
\]

Thus no nonzero \(\ell\ge1\) solution is regular at both endpoints.  The previously observed
wall-loud branch is not a numerical accident; it is forced when the regular-seat solution carries a
nonzero horizon boundary term.  The only finite static \(\ell=0\) solution is constant, and it is
not normalizable in the time-live wave norm above.

### 6.2 Static-slice Laplace-Beltrami probe

The spatial operator is instead

\[
-D^2f
=-\frac{\sqrt A}{r^2}\frac{d}{dr}\left(r^2\sqrt A f'\right)
+\frac{\ell(\ell+1)}{r^2}f.
\]

Its interval has finite proper length, but the horizon end is a finite-area boundary of the static
slice.  Dirichlet, Neumann, Robin, gluing, and Lorentzian-through-horizon domains give different
spectra.  The metric does not select one.  Spatial discreteness obtained after choosing a reflecting
domain would therefore be **CONDITIONAL**, not a matter-emergence derivation.

The finite lapse zero mode is a background geometric identity.  Calling it a carrier or an onset
mode requires precisely the action/field interpretation still missing.

## 7. Why compactness and absolute mass remain absent

Set

\[
x=\frac rX,
\qquad \tau=\frac{ct}{X}.
\]

Then

\[
ds^2=X^2\left[-(1-x)d\tau^2+(1-x)^{-1}dx^2+x^2d\Omega^2\right].
\]

Every dimensionless equation is independent of (X).  Curvatures scale as (X^{-2}), frequencies
as (c/X), volume as (X^3), and the raw lapse flux as (X).  Neither (G) nor a native mass
appears.  Therefore the dimensionless compactness

\[
\chi=\frac{GM}{c^2X}
\]

is not a variable in the metric-only solution space.

An action could declare a normalized boundary generator proportional to (-\Phi_N(X)), in which
case the geometry would immediately give (M\propto c^2X/G).  The proportionality constant is the
missing action/charge normalization; choosing it is not a derivation.  The familiar GR compactness
readout is permitted only as comparison and is not used here.

## 8. Particle-lane firewall

This result does not derive, assume, or reject the reopened (S^2) carrier.  It also does not merge
the macro lapse identity with the conditional H3 identity

\[
D^2N=\kappa_gN\rho_4.
\]

Indeed WR-L has (D^2N=-N/(Xr)<0).  Under the conditional H3 sign choice
\(\kappa_g>0\) and \(\rho_4\ge0\), the two source equations have opposite signs.  They therefore
cannot be identified as the same solution without additional structure.  This is a scope firewall,
not a falsification of either separate lane.

## 9. Gate verdicts

| Gate | Verdict | Decisive reason |
|---|---|---|
| A — unique global completion | **OPEN / FAILS uniqueness** | Regular causal extension, terminal-cell, gluing, and seat-transition choices are inequivalent |
| B — metric-only charge | **LEAD but not PASS** | \(\Phi_N(X)=-2\pi X\) is finite, but radius-dependent and unnormalized |
| C — metric-only matter onset | **FAILS** | Operator, field, inner product, center domain, and horizon domain are not unique |
| D — compactness selection | **FAILS** | WR-L is homothetic; no mass variable occurs; even \(\mathcal I_{\min}=1/2\) for every (X) |

## 10. What to do next

No GPU solve is justified.  The next work is a cold analytic provenance test:

1. independently reproduce the endpoint, flux, zero-mode, and inverse-functional algebra;
2. classify local second-order functionals allowed by positional dilation, reciprocity, and residual
   re-centering **off shell**;
3. test whether any such class uniquely yields
   \(r^2A''+rA'-A+1=0\) with a distinguished boundary primitive;
4. adversarially search for inequivalent allowed actions with the same WR-L extremal;
5. separately force the meaning of “unattainable (X)” against the explicit causal continuation.

If the operator is uniquely forced, this becomes the missing native-action seed.  If counteractions
survive, the metric has supplied a beautiful on-shell identity but not the dynamical law.

## 11. Self-audit

- No GR field equation, EH action, fluid, quantum mechanism, Standard Model input, fitted parameter,
  or hard physical cutoff was used.
- The full nonlinear metric was retained.
- Horizon coordinate behavior was separated from invariant curvature and causal continuation.
- The seat singularity was not hidden by finite integrated curvature.
- The lapse zero mode was not renamed matter.
- The inverse functional was labeled reconstructed, not native.
- Spatial and spacetime operators, and their boundary domains, were kept separate.
- Independent verification remains required before any banking or CANON/LIVE change.

## 12. Reproduction

In an environment with SymPy 1.13.3:

```bash
python3 verify_udt_wrl_solution_space_closure.py
```

The script checks 55 exact statements.  Passing verifies the encoded algebra only; it does not
select the physical action, boundary ontology, carrier, mass normalization, or global topology.
