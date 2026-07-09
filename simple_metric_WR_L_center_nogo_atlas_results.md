## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | MAP / DERIVE (center of static WR-L) |
| **Source** | External clean MAP/DERIVE (Charles-relayed multi-part) + local CAS check |
| **Local check** | Sympy identities — `G^t_t`, expansion \(a_1\), L re-centering algebra (this session) |
| **Build-on grade** | **DERIVED no-go** (center-included global SSS) · **WORKING lean** (residual pair-chart) · **not full ontology canon** |
| **Prior** | WR-L C-2026-07-09-1 / 1a; wall-regular, center OPEN |

### Premise ledger

| Premise | Tag |
|---------|-----|
| Simple reciprocal metric, \(A=e^{-2\phi}\) | THEORY |
| WR-L \(A=1-r/X\) | CANON C-2026-07-09-1 |
| \(r\) areal (\(4\pi r^2\)) | THEORY |
| Einstein/curvature as **geometry readout** | DERIVED (diff geom) |
| Einstein readout = physical material density | **NOT assumed** |
| Imported core / cutoff / particle smoothing | **NOT used** |
| \(r=0\) is ordinary smooth interior point of one global manifold | **FORK premise** (Branch A) |
| WR-L is seat-centered residual chart, domain \(r>0\) | **FORK premise** (Branch B — working lean) |

**Observing or targeting?** OBSERVE what static WR-L forces at the center; classify. No mechanism fix.

---

# Center of static WR-L: no-go + atlas fork

## 1. Metric at seat

\[
A(r)=1-\frac{r}{X},\qquad A(0)=1,\quad A'(0)=-\frac1X,\quad A''(0)=0.
\]

Smooth areal center in local Cartesian \(r=\sqrt{x^2+y^2+z^2}\) requires a radial scalar to be even:

\[
\boxed{A(r)=1+O(r^2)\quad(r\to0)\quad\Leftrightarrow\quad A'(0)=0.}
\]

This is **ordinary smooth geometry**, not GR matter import: \(A=1+a_1 r+\cdots\) is not differentiable at the origin unless \(a_1=0\) (\(\nabla A\sim a_1 \hat r\) has no unique limit).

WR-L has \(a_1=-1/X\neq0\) → **not** a smooth ordinary manifold point.

---

## 2. Curvature (single chart) — CAS checked

For reciprocal SSS,

\[
G^t{}_t=G^r{}_r=\frac{A+rA'-1}{r^2},\qquad
G^\theta{}_\theta=\tfrac12 A''+\frac{A'}{r}.
\]

On WR-L: \(A'=-1/X\), \(A''=0\):

\[
G^t{}_t=G^r{}_r=-\frac{2}{Xr},\qquad
G^\theta{}_\theta=-\frac{1}{Xr}.
\]

Einstein **readout** (if used): \(\rho=1/(4\pi X r)\), \(p_r=-\rho\), \(p_t=-\rho/2\) — matches L stress face.

Trace / scalar face used by external audit:

\[
G^\mu{}_\mu=-\frac{6}{Xr}\quad\Rightarrow\quad R=-G^\mu{}_\mu=\frac{6}{Xr}
\]

(local check: \(G^\mu{}_\mu\) and \(R\) claim consistent with that convention).

Kretschmann reported as \(K\sim 8/(X^2 r^2)\) (external; scales as \(1/r^2\)).

**Enclosed readout mass integrable:** \(4\pi r^2\rho\sim r/X\), \(m(r)\to0\) — **weak/integrable** singularity, not infinite point mass.

\[
\boxed{r=0\text{ is an invariant curvature singularity of static WR-L if included in the manifold.}}
\]

Not a pure coordinate artifact (areal \(r\) fixed by area; scalars diverge).

**Not** automatically a UDT physical matter core — density is Einstein-style readout, not yet derived material source (Principle 1 / 3).

---

## 3. General center-regularity theorem (reciprocal SSS)

\[
A=1+a_1 r+a_2 r^2+\cdots
\quad\Rightarrow\quad
G^t{}_t=\frac{2a_1}{r}+3a_2+\cdots,\quad
G^\theta{}_\theta=\frac{a_1}{r}+3a_2+\cdots.
\]

Finite center curvature \(\Rightarrow\) \(\boxed{a_1=0}\). Local sympy series: confirmed.

WR-L is the linear residual falloff case — singularity is **generic** to \(a_1\neq0\), not an accident of readout language.

---

## 4. Wall vs center

WR-L is **wall-regular** (∞ optical, finite proper, finite wall curvature) and **center-irregular**.

\[
\boxed{\text{WR-L cannot be a smooth static metric on the closed interval }[0,X].}
\]

At most smooth on \(\boxed{0<r<X}\).

Geodesics (external): radial null \(\dot r=\pm E\) reaches \(r=0\) in finite affine parameter; timelike also reaches with \(A\to1\). Center-included ⇒ **geodesically incomplete** as well as curvature-singular.

---

## 5. Atlas / re-centering test — decisive (CAS checked)

Seat \(O\): \(A_O=1-r/X\).  
Seat \(B\) at \(r=b\): residual re-centering

\[
A_{\mathrm{new}}=\frac{A_O(r)}{A_O(b)}\quad\Rightarrow\quad A_B(r')=1-\frac{r'}{X'},\quad r'=r-b,\ X'=X-b.
\]

Algebra: \(A_{\mathrm{new}}=(X-r)/(X-b)=A_B\) — **confirmed**.

If this were an ordinary coordinate change on **one global manifold**, scalar curvature must agree on overlap. With \(R\sim 6/(Xr)\) in each chart’s own residual coordinate:

\[
R_O(b+\varepsilon)\to\frac{6}{Xb}\quad\text{(finite)},\qquad
R_B(\varepsilon)\to\infty.
\]

They **do not** agree.

\[
\boxed{
\text{L re-centering is not an ordinary coordinate transformation of one global spacetime manifold.}
}
\]

---

## 6. Classification vs original four options

| Option | Status |
|--------|--------|
| (1) Ordinary physical matter singularity | **Reject as forced** — readout ≠ derived material; seats do not share one pointwise \(R\) field |
| (2) Pure coordinate artifact | **Reject** — single-chart \(R\), \(K\) diverge; areal \(r\) geometric |
| (3) Continuum-only / needs further structure | **Secondary open** — static global continuum interpretation fails |
| (4) Something else forced by the metric | **Primary** — weak invariant **self-diagonal / chart-seat** curvature cusp |

\[
\boxed{
\rho\sim 1/r\text{ is the Einstein-readout shadow of a real curvature singularity}
\text{ of a }single\text{ static L chart at its seat.}
}
\]

\[
\boxed{
\text{UDT has not thereby derived a physical matter core or particle source.}
}
\]

---

## 7. Forced fork (no-go)

### Branch A — WR-L as global SSS spacetime including \(r=0\)

Center = real weak curvature singularity + geodesic incompleteness.  
**Mathematically allowed, center-singular.** Poor fit for “regular observer seat.”

\[
\boxed{\text{center-included global WR-L is no-go under smooth-seat regularity.}}
\]

### Branch B — WR-L as observer/residual appearance chart

Domain \(0<r<X\); \(r=0\) = **punctured seat / self-observation diagonal**, not a physical continuum point.  
Re-centering = residual chart change, **not** manifold coordinate transform (atlas test).

\[
\boxed{\text{WORKING lean: L is a seat-centered residual metric on pair-space / off-diagonal observation.}}
\]

**Not elevated to CANON ontology** until Charles decides.

---

## 8. Ontological hinge (next)

Not a patch. The math forces a decision:

\[
\boxed{
\text{Is }r=0\text{ a local manifold point, or the excluded self-diagonal of residual observation?}
}
\]

| If… | Then… |
|-----|--------|
| Seat is interior continuum point | smooth \(A=1+O(r^2)\) forced → global WR-L **no-go** |
| Seat is residual chart pole (\(r>0\)) | smooth-center condition **does not apply** → WR-L wall-regular macro chart **survives** |

Related open (not solved here): multi-chart atlas without ever requiring a physical continuum \(r=0\); time-live / angular sectors.

---

## 9. What this does **not** do

- Does **not** overturn WR-L wall selection or \(A=1-r/X\) as residual form.  
- Does **not** revive P_ell or MS \(2GM/c^2\) as native mass.  
- Does **not** import a core/cutoff.  
- Does **not** claim particle spectrum from \(\rho\sim1/r\).

---

## Status tags (binding)

| Claim | Tag |
|-------|-----|
| \(a_1=0\) for smooth center; WR-L \(a_1\neq0\) | **DERIVED** |
| Single-chart \(R\sim1/r\), invariant singularity if \(r=0\) included | **DERIVED** |
| Integrable weak singularity (\(m\to0\)) | **DERIVED** (readout) |
| L re-centering ≠ ordinary coord transform (curvature mismatch) | **DERIVED** |
| Center-included global WR-L no-go under smooth seat | **DERIVED** (conditional on Branch A premise) |
| Residual pair-chart / self-diagonal reading | **WORKING LEAN** (best UDT fit; Charles may canonize later) |
| Ontological seat decision | **OPEN** |

---

## One-line

**Static WR-L is wall-regular but center-irregular on \([0,X]\); \(\rho\sim1/r\) is a real single-chart curvature cusp, not a coordinate fake and not a derived particle core; re-centering is not a global-manifold chart change — so L is best read as an off-diagonal residual appearance chart until Charles decides the seat ontology.**

---

## Second independent pass (same day)

**`simple_metric_WR_L_center_invariants_second_pass_results.md`**

Adds: full nonlinear \(K=8/(X^2 r^2)\); singularity **generic in \(\alpha\)** (no family member regularizes center);
WR-L **silent at center** — \(A=1-r/X\) to \(r=0\) is **CHOSE extrapolation**; division of labor wall vs center;
reachable/naked (finite proper distance, \(A(0)=1\)).

Joint: (1)+(3), not (2). Atlas / pair-chart lean unchanged as interpretation, not ontology canon.

