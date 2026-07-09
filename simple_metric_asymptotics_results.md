# Simple-metric asymptotics (φ only, \(D_A=r\))


## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit / original work date may differ) |
| **Mode** | OBSERVE |
| **Slice scope** | see body — retrofit default LEAD |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | see body |
| **Verifier status** | SELF-SCRIPT or NONE — see body; not blind-pass unless stated |
| **Build-on grade** | **LEAD** |
| **Re-run commands** | see body / associated `*.py` if any |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| See body of this document | full ledger in sections | mixed — re-read body | Y |

### What is NOT claimed

- Physics canon (Charles only). Hygiene grade ≠ nature proof.
- Claims wider than **Slice scope** above.

### Do not build on (if any)

- Anything tagged CHOSE/explore in the body without re-stating premises.

---

**Date:** 2026-07-08 · **Mode: OBSERVE**  
**Foundation:** `SIMPLE_METRIC_MACRO.md` (CAS-clean φ-only derivation)  
**Script / data:** `simple_metric_asymptotics.py`, `simple_metric_asymptotics_data.json`  
**Frame:** `UDT_ELEGANT_FRAME.md`  
**Status:** PROVISIONAL characterization of **vacuum** simple-metric equations. Not a free-\(D_A\) result. Not a theory death notice.

---

## Premises

| Item | Tag |
|------|-----|
| Metric \(ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2\) | LIVE simple |
| Field = \(\phi(r)\) only | LIVE |
| \(W\in\{e^{2\phi},1\}\), \(Z=1\) rep. | FREE fork / FREE scale |
| Vacuum (\(L_m=0\)) | Scoped this tile |
| Observing or targeting? | **Observing** |

---

## Equations (from simple metric only)

| \(W\) | Vacuum EL | Exact / structure |
|-------|-----------|-------------------|
| \(e^{2\phi}\) | \((r^2\phi')'=0\) | \(\phi=\phi_\infty-q/r\) exact |
| \(1\) | \(Z(r^2\phi')'=4e^{-2\phi}\) | \(Q:=r^2\phi'\) **strictly increasing** (\(Q'>0\)) |

---

## Elegant probes

- **Redshift out:** \(\phi\) increases with \(r\) (observer at \(r_0\), \(\phi(r_0)=0\)).  
- **Hard barrier:** \(\ell=\int e^{\phi}\,dr\) or null \(\int e^{2\phi}\,dr\) finite as reach → end, with large \(z\).  
- **No preferred center:** chart origin vs cosmology ontology kept separate.

---

## Results

### \(W=e^{2\phi}\) (compensated) — exact

For \(q>0\), observer at \(r_0\) with \(\phi(r_0)=0\):

\[
\phi(r)=q\Bigl(\frac{1}{r_0}-\frac{1}{r}\Bigr)\ \ (r\ge r_0)
\quad\Rightarrow\quad
\phi\to\frac{q}{r_0}\ \text{as}\ r\to\infty
\]

| Probe | Result |
|-------|--------|
| Redshift out | **YES** |
| \(z_{\max}\) | \(e^{q/r_0}-1\) **finite** |
| \(\ell\to\infty\) | **diverges** |
| Hard barrier | **FAIL** (open infinity, finite max depth) |
| \(r=0\) | singular if \(q\neq 0\) (chart) |

### \(W=1\) (uncompensated) — structure + numeric

**Exact:** \(Q=r^2\phi'\) strictly ↑ (numeric min \(\Delta Q>0\)).

**Outward** from \(r_0=1\), \(\phi=0\), many \(u_0=\phi'\):

- \(\phi\) **rises**, then flattens toward a **finite** plateau \(\sim 2.5\)–\(3\) (weakly start-dependent).  
- Late shape ≈ Coulomb: \(\phi\approx\phi_\infty-Q/r\) (resid \(\sim 10^{-2}\) on sample).  
- \(\ell(R)\) **grows with** \(R\) (e.g. \(u_0=0.5\): \(\ell(10)\sim47\), \(\ell(500)\sim6\times 10^3\)) → **no hard barrier** in vacuum.

**Inward** toward \(r\to 0\): \(\phi\) hits large positive (cap) — deep dilation at small \(r\) in this chart.

| Probe | Result |
|-------|--------|
| Redshift out | **YES** |
| Hard barrier | **FAIL** (open \(\ell\); finite practical \(\phi_\infty\)) |
| Center chart | singular-looking as \(r\to 0\) |

---

## Scoreboard (simple metric, vacuum only)

| \(W\) | Redshift out | Hard dilation barrier | Notes |
|-------|--------------|------------------------|-------|
| \(e^{2\phi}\) | YES | NO | Exact Coulomb |
| \(1\) | YES | NO | Source dies as \(\phi\) rises; quasi-plateau |

**Scoped claim:** On the **simple metric, vacuum, these two bulk weights**, looking out you get **redder then limited depth**, not **infinite-depth impassable edge**.

**Does not claim:** UDT false; matter cannot change this; free \(D_A\) must return; BB anything.

**Does claim:** Clean provenance — operators varied **φ only** on \(D_A=r\).

---

## Relation to quarantined “P3 fail”

Old P3 numerics looked similar (φ↑, finite plateau, open \(\ell\)).  
Difference: **this** tile is **allowed** as evidence about the **simple vacuum equations**.  
The quarantine was for **using free-\(D\) truncations as if they were simple-theory verdicts** and for free-\(D\) cosmology theater — not for forbidding φ-only asymptotics on \(D_A=r\).

---

## Next (still simple metric)

1. **Ponder \(W\):** both vacuum weights open-infinity with finite asymptotic depth — barrier not from vacuum \(W\) alone on this metric.  
2. **Same-metric continuum** \(L_m=-\rho r^2 e^{-2\phi}\): asymptotics of  
   - \(Z(r^2\phi')'=2\rho r^2 e^{-2\phi}\) (compensated + dust)  
   - \(Z(r^2\phi')'=4e^{-2\phi}+2\rho r^2 e^{-2\phi}\) (uncompensated + dust)  
   Still characterize, no sky fit.  
3. Relational multi-observer only after a candidate single-chart barrier exists.

---

## Plain summary

On the simple UDT metric with only \(\phi\) dynamical, vacuum solutions that look outward get **deeper dilation then level off** — redshift grows then **caps**, and you can still go arbitrarily far in proper distance. That is what **these vacuum operators do**, derived cleanly. A hard “can’t get past” edge is **not** showing up in vacuum on this metric yet; next is the same metric **with matter in the action**, or a principle choice — not free \(D_A\) and not a new edge field.
