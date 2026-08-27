# G283 exact derivation — arbitrary neighboring curvature survives the owned identities

Date: 2026-08-27

## 1. Fixed complete-metric family

Let $T(u)$ be any smooth symmetric $2\times2$ matrix on a bounded interval and set

\[
g_T=-2\,du\,dv+dx^2+dy^2-x^iT_{ij}(u)x^j\,du^2.
\]

Along the central null relation $x=y=0$, every member has the same metric, vanishing first metric
jet, vanishing Christoffel symbols, affine parameter, parallel screen, and central transport. Direct
coordinate computation gives

\[
R_{uiuj}=T_{ij}(u),
\qquad
\left.\partial_j\Gamma^i{}_{uu}\right|_{x=y=0}=T_{ij}(u).
\]

Thus the three functions in $T$ enter precisely at the metric two-jet—or equivalently the first
transverse derivative of the connection—while every datum through the central first jet remains
fixed.

## 2. Algebraic and differential compatibility

For arbitrary symbolic entries $T_{xx},T_{xy},T_{yy}$ and arbitrary independent derivatives
$T'_{xx},T'_{xy},T'_{yy}$, the complete Riemann pair symmetries, algebraic Bianchi identity, and
differential Bianchi identity all vanish exactly in every indexed slot. This is expected but
decisive: these identities constrain independently assigned curvature tables to come from one
connection; they do not prescribe the three functions.

The same applies to Cartan exterior closure and the Ricci commutator. The family is an explicit
smooth Lorentz metric with its Levi-Civita connection, so it is already a realization of those
identities for every smooth $T$. G231's classifying derivative data are supplied here by the
arbitrary function and its derivatives; Cartan integration does not manufacture their values.

## 3. Jacobi and relation-network home

The screen Jacobi equation is

\[
D''+T(u)D=0,
\qquad D(0)=0,
\qquad D'(0)=I.
\]

Its first-order generator is

\[
A_T(u)=
\begin{pmatrix}
0&I\\
-T(u)&0
\end{pmatrix}.
\]

For every symmetric $T$,

\[
A_T^TJ+JA_T=0.
\]

Therefore each interval transfer is symplectic, reverses by inversion, and composes exactly through
middle events. These properties make a coherent path-labelled neighboring-relation network for
every regular $T$; they do not select one network.

The independent standard-library replay directly rebuilt the metric derivatives and curvature in
128 exact rational cases, checking 207,360 component/Bianchi assertions. It also propagated 64
seeded matrix histories. Every interval transfer was symplectic and composed/reversed within
$6.44\times10^{-15}$, and all 64 cases differed from flat optical area.

## 4. Trace-free and primary controls

The trace-free subfamily

\[
T(u)=
\begin{pmatrix}
p(u)&q(u)\\
q(u)&-p(u)
\end{pmatrix}
\]

retains two arbitrary smooth functions. This does not adopt a GR vacuum equation; it shows that
even that stronger mathematical subfamily would not select the neighboring response.

Separately, the G262 primary one-lapse hierarchy remains an exact rewrite of an arbitrary positive
$N(r)$: its mass aspect and angular traces depend on $N,N',N''$ without producing a residual.
The primary control and the complete null witness therefore agree on the logical boundary.

## 5. Identity-role census

`IDENTITY_CENSUS.tsv` distinguishes genuine nonidentity compatibility from value selection. G225,
G227, G228, G231, Jacobi propagation, and G274 can reject inconsistent independently assembled
data. None rejects an explicit regular $g_T$, and none determines $T(u)$. This preserves their
substantial geometric content while preventing compatibility from being promoted to dynamics.

## 6. Bounded conclusion

On the frozen source and witness arena,

```text
ARBITRARY_SMOOTH_TIDAL_HISTORY_SURVIVES_OWNED_IDENTITIES
__VALUE_LAW_STILL_MISSING
```

G282's three mathematical homes are now shown constructively to carry the same surviving
function-valued freedom. G283 does not prove that no future UDT principle can constrain it and does
not choose a field equation, action, source, observation, scale, history, population, or
$X_{\max}$.
