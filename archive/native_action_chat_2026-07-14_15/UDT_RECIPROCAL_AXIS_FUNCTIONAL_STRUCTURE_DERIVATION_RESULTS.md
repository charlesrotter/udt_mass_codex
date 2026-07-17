# UDT reciprocal-axis functional structure — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | `grok` at `64af120`; pre-existing dirty work preserved |
| Mode | Exact analytic off-shell and principal-jet audit; DATA-BLIND |
| Frozen map | `UDT_RECIPROCAL_AXIS_FUNCTIONAL_STRUCTURE_MAP.md`, SHA-256 `b1f6a58c59655b997404db7014f683a8d9edc1dc970664b8732b7236c211a10a` |
| Verifier | `verify_udt_reciprocal_axis_functional_structure.py` — 31/31 checks pass |
| Metric status | Reciprocal single-axis completion remains CONDITIONAL |
| Action status | Metric-only conformal branch remains UNIQUE-CONDITIONAL |
| GPU | Not used or warranted |
| Independent verification | OPEN |
| Banking | None; `LIVE.md` and `CANON.md` untouched |

## 0. Result

The metric-derived reciprocal-axis sector is a concrete nonlinear carrier-like geometry, but it is
not the historical first-derivative `S^2` functional.

For the exact one-coordinate jet

\[
g_{00}=-q^{-1},
\qquad
g_{ij}=\delta_{ij}+(q-1)n_i n_j,
\qquad
n=(\cos\theta,\sin\theta,0),
\]

define at one point

\[
u=q',\qquad v=q'',\qquad p=\theta',\qquad s=\theta''.
\]

Full four-dimensional curvature gives the exact sum of squares

\[
\boxed{
\begin{aligned}
C^2={}&
\left(\frac vq-\frac{u^2}{q^2}-\frac{q-1}{q}p^2\right)^2\\
&+\frac{\big((q-1)s+2up\big)^2}{q}\\
&+\frac{\big(u^2-(q-1)q(2q+1)p^2\big)^2}{3q^4}.
\end{aligned}
}
\]

This is nonlinear, exact, and nonnegative in the tested static one-coordinate sector. No
linearization, finite difference, field equation, or fitted coefficient was used.

Two decisive consequences follow:

\[
\boxed{
\text{the reduced metric functional contains irreducible }(q'')^2
\text{ and }(\theta'')^2;
}
\]

and

\[
\boxed{
\text{the }RP^2/S^2\text{ axis topology is not a topology of the unrestricted metric space.}
}
\]

The first makes this a genuine higher-derivative geometric carrier. The second follows because the
axis becomes unobservable at the regular isotropic locus `q=1`.

## 1. Exact invariant census

With the curvature convention implemented in the verifier,

\[
R=-\frac{u^2}{2q^2}-\frac{(q-1)^2}{2q}p^2.
\]

Writing `d=q-1`,

\[
\begin{aligned}
R_{\mu\nu}R^{\mu\nu}={}&
\frac{v^2}{2q^2}+\frac{d^2s^2}{2q}
-\frac{vu^2}{q^3}-\frac{d(q+1)vp^2}{2q^2}
+\frac{d(q+1)sup}{q^2}\\
&+\frac{3u^4}{4q^4}
+\frac{(3q^2+1)u^2p^2}{2q^3}
+\frac{d^2(3q^2+2q+3)p^4}{4q^2},
\end{aligned}
\]

and

\[
\begin{aligned}
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}={}&
\frac{2v^2}{q^2}+\frac{2d^2s^2}{q}
-\frac{4vu^2}{q^3}-\frac{d(q+3)vp^2}{q^2}
+\frac{2d(3q+1)sup}{q^2}\\
&+\frac{11u^4}{4q^4}
+\frac{(11q^2+6q-1)u^2p^2}{2q^3}
+\frac{d^2(11q^2+10q+11)p^4}{4q^2}.
\end{aligned}
\]

The verifier independently confirms

\[
C^2=Riem^2-2Ric^2+\frac13R^2
\]

at twelve exact mixed jets, together with all Riemann symmetries, the first Bianchi identity, Ricci
symmetry, and Weyl tracelessness.

## 2. Irreducible second-jet sector

Set all first jets to zero. A pure depth second jet gives

\[
p=s=u=0,\quad v\ne0
\quad\Longrightarrow\quad
C^2=\frac{v^2}{q^2}.
\]

A pure axis second jet gives

\[
p=u=v=0,\quad s\ne0
\quad\Longrightarrow\quad
C^2=\frac{(q-1)^2}{q}s^2.
\]

Neither can be converted into a first-derivative quartic density by a boundary integration: after
variation their principal Euler operators contain fourth derivatives.

Thus the pre-registered outcome is

\[
\boxed{\text{IRREDUCIBLE SECOND-JET SECTOR}.}
\]

This is not an objection imported from another theory. It is the direct differential order of the
UDT-motivated metric functional.

## 3. Exact limiting sectors

### Constant reciprocal depth

For constant `q!=1`,

\[
\boxed{
C^2=a(\theta'')^2+b(\theta')^4,
}
\]

where

\[
a=\frac{(q-1)^2}{q},
\qquad
b=\frac{4(q-1)^2(q^2+q+1)}{3q^2}.
\]

The reduced tangent Euler equation is

\[
2a\theta''''-12b(\theta')^2\theta''=0,
\]

or

\[
\boxed{
\theta''''-rac{8(q^2+q+1)}q(\theta')^2\theta''=0.
}
\]

This is **not** the unrestricted Bach equation. It is only the equation obtained from variations
tangent to this manufactured family.

For an interval, the raw boundary variation is

\[
\left[
\big(4b(\theta')^3-2a\theta'''\big)\delta\theta
+2a\theta''\delta\theta'
\right]_{\partial I}.
\]

Therefore differentiability requires fixing both `theta` and `theta'`, imposing the corresponding
natural conditions, or deriving a compensating boundary functional. None has yet been selected.

### Constant axis

Let `y=ln q`. When the axis is fixed,

\[
\boxed{
C^2=(y'')^2+\frac13(y')^4.
}
\]

This makes the higher-derivative depth cost especially transparent.

## 4. The axis topology is not yet metric topology

The metric depends on the axis only through

\[
(q-1)n\otimes n.
\]

For any smooth `q(x)>0`, define

\[
q_t(x)=1+t\big(q(x)-1\big),
\qquad 0\le t\le1.
\]

Every `q_t` remains positive. At `t=0`,

\[
g(q_0,n)=\operatorname{diag}(-1,1,1,1),
\]

independently of `n`. Thus an arbitrarily knotted `RP^2` axis texture can pass continuously through
the regular isotropic metric and disappear. If `q=1` on the carrier boundary, this homotopy also
preserves that boundary value.

Therefore

\[
\boxed{
\pi_3(RP^2)=\mathbb Z
\text{ classifies the nondegenerate axis field, but not the full metric configuration space.}
}
\]

A conserved Hopf-type metric charge would require a derived prohibition on the isotropic locus,
special global boundary data, or an independent carrier field. None is presently available.

This does not exclude a non-topological metric lump or a globally protected finite-cell solution.
It excludes silently transferring the historical carrier's topological protection to the metric.

## 5. Scale consequence

For any fixed-amplitude static configuration rescaled from size one to size `R`, curvature squared
scales as `R^-4` while spatial volume scales as `R^3`. Hence

\[
\boxed{E_C(R)=\frac{E_C(1)}R.}
\]

In an unbounded or isotropically calibrated domain where that dilation is admissible, a nonzero
finite configuration cannot be stationary at a finite size under the pure pre-scale `C^2` term.
This is a direct scaling result, not a fitted cutoff argument.

It reinforces the already-derived ordering

\[
\boxed{
\text{pre-scale geometry}\to\text{global/finite-cell scale selection}\to
\text{possible finite-size matter}.
}
\]

The universal solution scale `X` or other derived global closure data may change the finite-cell
problem. That has not yet been calculated.

## 6. Off-shell provenance

Under the metric-only premise, `q` and `n` are not additional fundamental fields. They parameterize
a restricted class of metrics. Therefore:

- **DERIVED:** unrestricted variation of `S_C[g]` gives the Bach equation.
- **DERIVED:** substitution `g=g(q,n)` diagnoses exact invariant content.
- **NOT DERIVED:** varying `S_C[g(q,n)]` with respect to `q,n` supplies all metric equations.
- **OPEN:** a covariant reconstruction of `n` from metric eigenstructure through degeneracies.
- **CHOSE if adopted:** treating `n` as an independent `RP^2` or `S^2` matter field.

The conditional axis metric also presupposes a time/space splitting. A time-live covariant axis
formulation would need that splitting to emerge from the metric or be supplied as additional field
content. It has not been derived.

## 7. Honest status and next decision

### Positive

- The UDT metric produces an exact, coefficient-free depth/axis coupling.
- The static one-coordinate Weyl density is a manifest sum of squares.
- The carrier-like sector traces entirely to the conditional UDT metric and locked CSN action
  branch.
- Global scale selection remains a mathematically specific route to finite size.

### Negative/open

- The sector is genuinely fourth order in the reduced variables.
- Axis topology is lost at the regular isotropic metric.
- Pure pre-scale curvature-squared energy has no finite stationary size under free dilation.
- Full covariant time dynamics, finite-cell boundary terms, energy charge, and unrestricted
  localized Bach solutions remain OPEN.

\[
\boxed{
\begin{gathered}
\text{metric-derived orientation strain confirmed;}\\
\text{historical }S^2\text{ carrier not recovered;}\\
\text{metric-only topological protection not obtained;}\\
\text{finite-cell/global-scale closure is now the decisive branch.}
\end{gathered}
}
\]
