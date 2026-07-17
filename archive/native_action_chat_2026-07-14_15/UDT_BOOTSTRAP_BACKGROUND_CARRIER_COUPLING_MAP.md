# UDT bootstrap-background carrier coupling — frozen derivation map

## Hygiene

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic background-field expansion; DATA-BLIND |
| Motivation | Owner's bootstrap picture: global geometry creates a nonuniform depth background with which localized carrier geometry interacts |
| Bulk branch | Conditional metric-only `S_C proportional to integral sqrt(-g) C^2` |
| Carrier probe | Conditional reciprocal-axis metric; `RP^2` axis with possible oriented `S^2` lift |
| Empirical densities | Not loaded; no native density or coupling has yet been derived |
| Standard-theory values | Reserved for later comparison/calibration only |
| GPU | Not authorized; quadratic/quartic continuum operator first |
| Banking | None; `LIVE.md` and `CANON.md` untouched |

## 1. Question

Can a nonuniform bootstrap reciprocal-depth background generate, through the metric alone, the
quadratic and quartic carrier terms needed to stabilize an orientation configuration—without an
inserted coupling, mass term, or cutoff?

## 2. Exact manufactured backgrounds

Use a one-coordinate background

\[
q(z)=e^{2\phi(z)}>0
\]

and compare two axis geometries at the evaluation point.

### Transverse background gradient

\[
n=(\cos\theta(z),\sin\theta(z),0),
\qquad n\cdot\nabla q=0\quad(\theta=0).
\]

### Parallel background gradient

\[
n=(\sin\theta(z),0,\cos\theta(z)),
\qquad n\parallel\nabla q\quad(\theta=0).
\]

Define exact jets

\[
u=q',\qquad v=q'',\qquad p=\theta',\qquad s=\theta''.
\]

Build the full four-dimensional metric curvature in both cases before reducing the carrier
functional.

## 3. Pre-registered tests

### T1. Tensor reconstruction

For both alignments compute `R`, `Ricci2`, `Riemann2`, and `C^2` with full nonlinear inverse metric,
connection, and Weyl subtraction. Audit tensor identities and exact mixed jets.

### T2. Background expansion

Subtract the `theta=constant` background density and expand exactly through quartic order in
`p,s`. Identify

\[
\Delta C^2
=a(z)s^2+b(z)ps+K_{\rm raw}(z)p^2+c(z)p^4.
\]

Integrate the `ps` term by parts only with its boundary contribution displayed. Derive the effective
quadratic coefficient `K_eff` in

\[
\int dz\,[a(p')^2+K_{\rm eff}p^2+c p^4].
\]

### T3. Positivity and onset

Determine whether `a>0` and `c>0`, and whether `K_eff` can become negative for an allowed smooth
background. A negative local coefficient is only an onset lead; the full operator and boundary
conditions decide stability.

### T4. WR-L evaluation

Insert the exact WR-L depth

\[
q(r)=\frac1{1-r/X}
\]

only into the alignment whose axis is radial/parallel. Keep `x=r/X` symbolic. Do not use a mass
density inferred from another field equation.

### T5. Smooth-core evaluation

Insert

\[
q(r)=\frac1{1-r^2/X^2}
\]

as the smooth conformal comparison background. Determine whether the carrier quadratic operator
changes sign or loses coercivity.

### T6. Scale-selection gate

A viable bootstrap stabilization lead requires all of:

1. a metric-derived negative or confining quadratic sector;
2. a positive highest-derivative/quartic sector;
3. a determined global domain and boundary variation;
4. no free coefficient controlling the balance;
5. a stationary scale that is not merely wall pinning.

## 4. Acceptance gates

- No Standard Model, observed particle, or cosmological density value in the derivation.
- No identification of metric curvature with native mass density before a charge law exists.
- No freezing `q` without marking the result as a background/probe approximation; a full solution
  must include backreaction.
- No claim of three-dimensional soliton stability from a one-coordinate fluctuation.
- Preserve full nonlinear `q` dependence and distinguish parallel from transverse alignment.

## 5. Possible verdicts

1. **NATIVE BACKGROUND STABILIZATION LEAD:** the derived background operator has the required sign
   structure with no inserted coupling.
2. **BACKGROUND COUPLING BUT NO SCALE CLOSURE:** interaction exists but does not select a stable
   finite carrier.
3. **NO CARRIER COUPLING:** the background drops out after exact identities/boundaries.
4. **OPERATOR UNRESOLVED:** tensor or boundary audits fail.
