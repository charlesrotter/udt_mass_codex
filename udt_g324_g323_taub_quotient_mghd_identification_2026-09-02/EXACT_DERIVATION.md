# G324 exact derivation — smooth maximality of the registered Taub quotients

Date: 2026-09-02

## 1. Question and ownership

G323 derived the explicit quotient metric

\[
g_\mu=-\frac{R}{\mu}\,dR^2+\frac{\mu}{R}\,dX^2
      +R^2(dy^2+dz^2),
\qquad R>0,\quad\mu>0,
\tag{1}
\]

with the registered compact translation lattice. It proved that each fixed G320 datum embeds as a
complete Cauchy graph, but stopped short of identifying (1) with the datum's G322 maximal globally
hyperbolic development (MGHD).

This derivation closes only that mathematical interface. The active `Ric=0` sector remains
conditional on the owner-adopted provisional premises recorded in `PREMISE_LEDGER.tsv`. The two
global existence/extension results are imported mathematical methods, not UDT postulates.

## 2. Proper-time form and exact curvature

Set

\[
T=\frac{2}{3\sqrt\mu}R^{3/2}.
\tag{2}
\]

Then the radial term in (1) is exactly `-dT^2`. After constant rescalings of the three spatial
coordinates, (1) is the compact Kasner metric

\[
g=-dT^2+C_X^2T^{-2/3}dX^2
  +C_\perp^2T^{4/3}(dy^2+dz^2),
\tag{3}
\]

with exponents

\[
(p_X,p_y,p_z)=\left(-\frac13,\frac23,\frac23\right),
\qquad \sum_i p_i=\sum_i p_i^2=1.
\tag{4}
\]

The Kasner identities give `Ric=0`. An independent direct tensor contraction gives

\[
\boxed{\mathcal K:=R_{abcd}R^{abcd}=\frac{12\mu^2}{R^6}}.
\tag{5}
\]

Thus the spacetime is regular for every finite positive `R`, while the scalar invariant diverges as
`R -> 0`.

Also

\[
g^{-1}(dR,dR)=-\frac\mu R<0,
\tag{6}
\]

so `R` is temporal. Choose the time orientation in which `R` increases. On any compact interval
`0<a<=R<=b<infinity`, causal coordinate speeds are bounded. Since the spatial quotient is compact,
an inextendible causal curve cannot stop inside such a slab. Consequently `R` ranges from zero to
infinity on every inextendible causal curve and each constant-`R` torus is Cauchy, reproducing the
G323 global-hyperbolicity gate.

## 3. Exact timelike reach

The three translation symmetries give conserved momenta

\[
p_X=\frac\mu R\dot X,
\qquad p_y=R^2\dot y,
\qquad p_z=R^2\dot z.
\tag{7}
\]

Writing `kappa=g(dot gamma,dot gamma)`, the normalization identity is

\[
\dot R^2=p_X^2+\frac{\mu P}{R^3}-\kappa\frac\mu R,
\qquad P=p_y^2+p_z^2.
\tag{8}
\]

For a unit timelike geodesic, `kappa=-1`, so the right side is strictly positive. Its sign cannot
turn; in the chosen future orientation `dot R>0`, and every future timelike geodesic has
`R -> infinity`.

Its future proper-time reach is

\[
\Delta\tau=\int^{\infty}
\frac{dR}{\sqrt{p_X^2+\mu P/R^3+\mu/R}}.
\tag{9}
\]

If `p_X` is nonzero, then for `R>=1`

\[
\frac{d\tau}{dR}\ge
\frac{1}{\sqrt{p_X^2+\mu(P+1)}},
\tag{10}
\]

and (9) diverges. If `p_X=0`, then

\[
\frac{d\tau}{dR}\ge
\sqrt{\frac{R}{\mu(P+1)}},
\tag{11}
\]

and it again diverges. Therefore

\[
\boxed{(M,g_\mu)\text{ is future timelike geodesically complete}.}
\tag{12}
\]

Toward `R=0`, the integrand instead behaves as `R^(3/2)` when `P>0` and as `R^(1/2)` when
`P=0`; the past end has finite proper-time reach. This locates an incomplete end but does not by
itself prove inextendibility.

## 4. No finite-positive-`R` endpoint

Suppose a geodesic has a finite affine/proper parameter endpoint while `R` remains in `[a,b]` with
`0<a<b<infinity`. Equation (8) bounds `dot R`; (7) bounds every spatial coordinate velocity. The
metric and its Christoffel symbols are smooth and bounded on the compact quotient slab
`[a,b] x T3`. The geodesic state remains in a compact subset of the tangent bundle, so the ordinary
geodesic continuation theorem extends it inside (1). This contradicts inextendibility.

Equivalently, the image of a compact slab is compact and therefore closed in any Hausdorff
extension. An extension-boundary endpoint cannot lie at finite positive `R`.

## 5. The orientation-neutral extension-endpoint argument

G324 imports the bounded interface recorded in `GLS_PRIMARY_SOURCE_EVIDENCE.json` from Galloway,
Ling, and Sbierski. Their Theorem 2 states, in formal transcription, that a smooth, at least `C2`,
time-oriented, globally hyperbolic Lorentzian manifold admitting a `C0` extension contains a
timelike geodesic with an endpoint on the extension boundary. The evidence record gives the exact
source version, PDF SHA-256, theorem number and page location, and two exact fragments totaling 23
words. The
theorem itself does not privilege the future or past direction.

These are Lorentzian-geometry theorems, not physical UDT laws.

Assume for contradiction that (1) has a proper time-oriented `C2` Lorentzian extension; it is also a
`C0` extension, so the imported theorem supplies a boundary-ending timelike geodesic in (1). Orient
that geodesic toward its extension endpoint. It cannot be future-directed, because (12) proves
future timelike geodesic completeness. It must therefore be past-directed. No separate time-dual
theorem or assertion about a named one-sided boundary is used.

Section 4 excludes a finite positive limiting radius, and a past-directed timelike curve cannot run
from finite `R` to `R=infinity`. Therefore the boundary geodesic must have

\[
R\longrightarrow0.
\tag{13}
\]

But in a `C2` extension the Riemann tensor and the scalar (5) are continuous and finite in a
neighborhood of the endpoint. Equation (5) diverges along (13), a contradiction. Thus

\[
\boxed{(M,g_\mu)\text{ admits no proper time-oriented }C^2
\text{ Lorentzian extension}.}
\tag{14}
\]

This proves the regularity needed for the smooth MGHD interface. It does **not** prove that the
past singular end is `C0`-inextendible.

## 6. Identification with the G322 MGHD

Fix one registered G323 datum. G323 gives a data-preserving Cauchy embedding of its explicit
quotient into the smooth MGHD supplied conditionally by G322. An isometric embedding between
equal-dimensional manifolds has open image. If that image were proper, the MGHD would be a proper
smooth—and hence `C2`—time-oriented Lorentzian extension of (1), contradicting (14).

Therefore the embedding is onto:

\[
\boxed{\text{each registered explicit G323 quotient is its fixed datum's smooth G322 MGHD}.}
\tag{15}
\]

This is a per-datum theorem. It does not select a datum.

## 7. Transfer of the compact-lattice modulus

G323 already derived the unmarked invariant

\[
\mathcal Q(\Gamma)=
\frac{\operatorname{covol}_{\ell_X}(\Gamma\cap\ell_X)}
{\sqrt{\operatorname{covol}_{E_\perp}(\pi_{E_\perp}\Gamma)}}
\tag{16}
\]

and proved it strictly mode-dependent for the registered integer family. Equation (15) identifies
each MGHD with its explicit quotient; it neither modifies nor refits (16). Hence two registered
quotients with different `Q(Gamma)` cannot become the same unmarked MGHD.

The opposite-`K` conclusion also remains exactly G323's: one time-unoriented metric and its two
opposite time orientations. G324 adds no universe/anti-universe interpretation.

## 8. Exact landing and boundary

Preregistered landing:

```text
EXPLICIT_TAUB_QUOTIENTS_ARE_SMOOTH_MGHDS__REGISTERED_LATTICE_MODULUS_SURVIVES
```

Status: `PASS_PENDING_REPAIR_ONLY_EXTERNAL_FOLLOWUP`.

Derived conditionally in the registered family:

- future timelike geodesic completeness;
- no proper time-oriented `C2` Lorentzian extension;
- equality of each explicit quotient with its smooth per-datum G322 MGHD;
- survival of G323's registered compact-lattice modulus at MGHD level.

Still open or inactive:

- past `C0` inextendibility;
- stability and perturbations;
- other topologies, lattices, data, sources, and full UDT sectors;
- physical datum/topology/orientation/occupancy selection;
- scale attachment, observation, mass, and physical `X_max`.

The UDT metric, reciprocal kernel, and angular sector are unchanged.
