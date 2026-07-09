# OBSERVE-4 — Nondim reduction + outer asymptotics (vacuum B)

**Date:** 2026-07-08  
**Mode:** OBSERVE.  
**Script / data:** `macro_vacuum_B_observe4.py`, `macro_vacuum_B_observe4_data.json`  
**Prior:** O1–O3.  
**Status:** PROVISIONAL — refines O3 “SURVIVE” (finite window ≠ eternal outer).

---

## Premise ledger

| Item | Tag |
|------|-----|
| Vacuum B throat seeds | as O2–O3 |
| Outer runs to r=50 (and 200) | method bound FREE |
| Observing or targeting? | **Observing** |

---

## A. Nondimensional structure

### Flux form (exact rewrite)

\[
F = e^{-2\phi} D',\qquad G = D^2 \phi'
\]

\[
F' = -\frac{Z}{4}\frac{G^2}{D^3},\qquad
G' = \frac{4}{Z}\, e^{2\phi}\, F^2
\]

(with \(D>0\), \(Z>0\): \(F'\le 0\), \(G'\ge 0\) as before).

### \(d = \ln D\)

Eliminates absolute scale of \(D\). CAS reduced EL in \((\phi,d)\); no bare \(D_*\) remains.

### Scale-out (numeric)

Same \((Z,u_*)\), \(D_*\in\{0.5,1,2\}\):  

\(\max|\Delta\phi|\) and \(\max|\Delta(D/D_*)|\) \(\sim 10^{-15}\) — machine identity.

**⇒ O3 result “\(u_{\mathrm{crit}}\) independent of \(D_*\)” is structural, not accidental.**

### First integral

No elementary conserved \(H(F,G)\) independent of \((\phi,D)\) found. **OPEN** (not claimed impossible). Controls remain the mono pair \((F,G)\).

---

## B. Outer asymptotics (throat → large \(r\))

Seed: \(r_*=1\), \(\phi_*=0\), \(D_*=1\), \(D'_*=0\), vary \(Z\) and \(u_*=\phi'_*\).

### B1. Positive \(u_*\) (φ increases outward) — **all pinch**

| \(Z\) | \(u_*\) | \(r_{\mathrm{pinch}}\) (approx) | \(\phi\) at pinch |
|------|---------|----------------------------------|-------------------|
| 1 | 0.05 | 18.6 | ≈ 3.35 |
| 1 | 0.10 | 9.8 | ≈ 3.35 |
| 1 | 0.15 | 6.9 | ≈ 3.36 |
| 1 | 0.20 | 5.4 | ≈ 3.36 |
| 4 | 0.05–0.2 | 12.6 → 3.9 | ≈ 2.72 |
| 8 | 0.05–0.2 | 10.1 → 3.3 | ≈ 2.41 |

**Pattern:**

- Every tested \(u_*>0\) hits **\(D\to 0\) at finite \(r\)** (including those that “SURVIVE” O3’s window \([0.05,5]\)).  
- For fixed \(Z\), **pinch φ clusters** (nearly independent of \(u_*\)); smaller \(u_*\) only **delays** the pinch (larger \(r_{\mathrm{pinch}}\)).  
- Larger \(Z\) → earlier pinch for same \(u_*\), lower pinch-φ cluster.

**Correction to O3 language:**  
O3 **SURVIVE** = “still alive inside a finite chart window.”  
It is **not** “globally regular to infinity” for \(+u_*\). Honest asymptotic class for \(+u_*\) throat seeds: **finite-r outward pinch.**

### B2. Negative \(u_*\) (φ decreases outward) — **long-lived**

| \(Z\) | \(u_*\) | to \(r=50\) | \(D(50)\) | \(\phi(50)\) |
|------|---------|-------------|-----------|--------------|
| 1 | −0.1 | ok | 0.940 | −5.18 |
| 1 | −0.2 | ok | 0.940 | −10.40 |
| 4 | −0.1 | ok | 0.782 | −6.14 |
| 4 | −0.2 | ok | 0.782 | −12.40 |
| 8 | −0.1 | ok | 0.616 | −7.67 |
| 8 | −0.2 | ok | 0.616 | −15.63 |

Ultra: \(Z=1\), \(u_*=-0.1\), to \(r=200\): still ok, \(D\approx 0.940\), \(\phi\approx -21.1\), slopes small in \(D\), φ still falling.

**Pattern (scoped):**

- \(D\) falls a little from the throat then **appears to approach a Z-dependent plateau** \(D_\infty(Z) < D_*\) (same \(D(50)\) for \(u=-0.1\) and \(-0.2\) at fixed \(Z\) in this sample).  
- \(\phi\) continues **downward** (roughly secular); no pinch of \(D\) seen out to 200.  
- This is the vacuum throat sector that is **not** immediately outer-singular.

### B3. Trivial \(u_*=0\)

Exact plateau: \(D\equiv 1\), \(\phi\equiv 0\).

---

## C. Refined vacuum map (O1–O4)

| Class | Outer fate (throat seed, vacuum B) |
|-------|--------------------------------------|
| Polar smooth origin | Blocked (O1) |
| Throat \(u_*=0\) | Eternal flat |
| Throat \(u_*>0\) | **Finite-r outward pinch** (delay ∝ 1/u roughly); O3 “S” only window-local |
| Throat \(u_*<0\) | **Long outer life**; \(D\to D_\infty(Z)\)-like; φ keeps decreasing in runs |
| Inward from throat | Mild; no pinch in deep probes (O3) |

**Sign of \(\phi'\) at the bulge is load-bearing** for outer regularity — not a small detail.

---

## What this does *not* say

- Not that \(u_*<0\) is “the cosmology” (chart choice of φ direction / observer orientation still free).  
- Not proven \(D\to D_\infty\) mathematically (numeric plateau; open for proof).  
- Not that \(\phi\to-\infty\) is physical “edge” (could be chart / incomplete; redshift law still \(e^{\Delta\phi}\)).  
- Not sources; not fallback C (B still has a nonempty long-lived sector: flat + negative-\(u\) throats).  
- Not a fit for Z.

---

## Incremental next (when ready)

1. **OBSERVE-5a:** analytic / sharper numeric on \(D_\infty(Z)\) for \(u_*<0\) (does plateau really exist? φ′ asymptotics?).  
2. **OBSERVE-5b:** re-express ±u under φ → −φ and r orientation — is asymmetry only a chart convention?  
3. Still later: \(L_m\).

**Recommend 5b first** (cheap principle check): if flipping φ sign maps +u pinch family to −u long family, the “two fates” are one orbit under discrete symmetry — important before over-interpreting sign.

---

## Plain summary

The equations only care about **relative** sphere size, not absolute throat width.  
If φ **rises** as you go out from the widest sphere, vacuum B always seems to **pinch the sphere shut** at finite radius (sooner if the slope is steeper).  
If φ **falls** outward, the sphere size **settles toward a smaller floor** and the solution can run a long way, with φ still dropping.  
So the finite “survival windows” of O3 for rising-φ were real but temporary; the lasting vacuum throat branch in these runs is **flat or outward-falling φ**.
