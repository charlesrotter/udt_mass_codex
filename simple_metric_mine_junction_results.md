## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE (GR corpus mine) |
| **Slice scope** | Israel junction; reciprocal simple metric both sides; exterior Schw vacuum |
| **Observing or targeting?** | OBSERVE matching fallout — not building a shell cosmology |
| **Mine vein** | Israel / thin shell / star matching (GR corpus) |
| **Verifier status** | SELF CAS |
| **Build-on grade** | **LEAD** |
| **Re-run** | `python3 simple_metric_mine_junction.py` |

### Premise ledger

| Item | Tag |
|------|-----|
| Israel junction formalism | GR **mine method** |
| Interior reciprocal continuum | E-package on simple metric |
| Exterior \(A=1-r_s/r\) | Einstein vacuum on reciprocal |
| Thin shell as ontology | **not** adopted — character only |

### What is NOT claimed

- Thin shell is the UDT edge mechanism.
- Power-ceiling family is a star.
- Junction selects \(p\) or \(X\).

---

# Mine pass — junction / matching under reciprocal metric

**Prior:** SSS Einstein + EH-constraint mines.  
**Ore:** Israel junction, stellar matching, thin shells.  
**Smelt:** both sides on simple metric (reciprocal); exterior = Schw vacuum; interior = E-map continuum tiles.

---

## Lay summary

GR knows how to glue an inside region to an outside vacuum (stars, shells). We asked what that glue does **after** positional reciprocity locks the metric form.

**What falls out:**

1. **Continuous clocks on the glue surface** ⇔ continuous \(A\) ⇔ continuous Misner–Sharp mass (no mass jump without a shell).  
2. The **cosmic ceiling** family \(A=1-c r^p\) (lapse dies at finite radius, \(A\) **falling** as \(r\) grows) is a **different animal** from a **star interior** meant to match an outside Schwarzschild region (where \(A\) **rises** toward flatness).  
3. You **cannot** smoothly (\(C^1\)) match that ceiling family to an exterior Schw vacuum for \(p>0\).  
4. You **can** match with a **thin shell** (continuous \(A\), jump in \(A'\)): surface energy density comes out **zero** in the standard Israel read, with **tangential** surface stress only — anisotropic shell, singular if pushed to the \(A\to0\) edge.  
5. So: **filled cosmos / critical wall** (no outside vacuum) and **localized star + exterior** are two **different** solution-space rooms. Mining does not force a shell as the UDT edge.

---

## 1. Setup

Both sides (reciprocal simple metric):
\[
ds^2=-A\,dt^2+A^{-1}dr^2+r^2 d\Omega^2.
\]

| Side | \(A\) |
|------|--------|
| Exterior \(+\) | \(1-r_s/r\) (Einstein vacuum) |
| Interior \(-\) | continuum tile, e.g. \(1-c r^{p}\) or free |

Junction surface \(r=R\).

Induced metric continuity \(\Rightarrow\)
\[
A_-(R)=A_+(R).
\]
With MS \(m=r(1-A)/2\), that is **\(m_-(R)=m_+(R)=r_s/2\)**.

---

## 2. Extrinsic curvature / Israel (character formulas)

Unit radial normal (increasing \(r\)): \(n^r=\sqrt{A}\).

\[
K^t{}_t=\frac{A'}{2\sqrt{A}},\qquad
K^\theta{}_\theta=\frac{\sqrt{A}}{R}.
\]

If \(A\) continuous, \([K^\theta{}_\theta]=0\). Jump lives in \(A'\):
\[
[K^t{}_t]=\frac{A_+'-A_-'}{2\sqrt{A(R)}}.
\]

Israel surface stress (standard sign convention as in script):
\[
S^t{}_t=0,\qquad
S^\theta{}_\theta=\frac{A_+'-A_-'}{16\pi\sqrt{A(R)}}
\quad\text{(when \(A\) continuous)}.
\]

So **surface energy density \(\sigma=-S^t{}_t=0\)**, **tangential stress** \(\propto [A']\) — anisotropic thin shell if \([A']\neq0\).

Smooth \(C^1\) match: \(A_+'=A_-'\) \(\Rightarrow\) no shell.

---

## 3. Ceiling tile vs exterior Schw

Interior \(A_-=1-r/X\), exterior \(A_+=1-r_s/r\).

**\(A\) continuity:** \(r_s=R^2/X\), \(m=R^2/(2X)\).

**Derivatives at \(R\):**
\[
A_-'=-\frac1X,\qquad A_+'=+\frac1X
\quad\Rightarrow\quad [A']=\frac2X\neq0.
\]

Thin shell with
\[
S^\theta{}_\theta=\frac{1}{8\pi\sqrt{X(X-R)}}
\]
(and \(S^t{}_t=0\)). As \(R\to X\) (shell at the wall), \(A\to0\) and shell stress **diverges**.

---

## 4. No \(C^1\) match for power-lapse family

Interior \(A=1-c r^p\) (\(c>0,p>0\)): \(A'=-c p r^{p-1}<0\) (lapse **deepens** outward).

Exterior Schw: \(A'=r_s/r^2>0\) (lapse **relaxes** outward).

Matching \(A\) and \(A'\) at \(R\):
\[
c R^{p+1}=r_s,
\quad
-c p R^{p-1}=c R^{p-1}
\quad\Rightarrow\quad p=-1,
\]
impossible for \(p>0\).

**Fallout:** E-map **cosmic ceiling** slices are **not** star interiors for vacuum Schw exteriors.  
They are **global filled** geometries (wall = end of chart / critical compactness), unless one adds a shell or changes the exterior.

---

## 5. Two rooms in solution space (mine clarity)

| Room | Character | Exterior vacuum Schw? |
|------|-----------|------------------------|
| **Star-like** | \(A\) increases toward surface; \(C^0\) or \(C^1\) match; MS mass = \(r_s/2\) | **Yes** (standard mine) |
| **Filled cosmos / ceiling** | \(A\to0\) at finite \(X\); critical \(M=X/2\); \(A'\) wrong sign for Schw match | **Not \(C^1\)**; shell optional and singular at wall |
| **Thin shell cosmos** | Force \(A\) cont. + \([A']\neq0\) | Legal GR object; \(\sigma=0\), anisotropic \(S^\theta{}_\theta\); **not** selected as UDT ontology here |

S6 “continuous \(p\)-map” lives mainly in the **filled / global** room when used for outer walls — do not silently reread it as nested stars.

---

## 6. What this does *not* do

- Does not pick thin shell as UDT edge mechanism (red if we did).  
- Does not kill E-map continuum; it **classifies** matching.  
- Does not unify R1.  
- Junction “edge” ≠ automatic CMB story.

---

## 7. Next veins

1. **Star-like reciprocal interiors** with \(A'>0\) near surface (rebuild interior catalog under \(p_r=-\rho\) + match Schw).  
2. **Pure filled cosmos** without exterior (already E-map) — junction N/A.  
3. **Matter in constrained EH** sourcing.  
4. Soft reciprocity (free \(\nu+\lambda\) asymptotically).

---

## One-line

**Junction mine: mass/lapse continuity is clean; cosmic ceiling tiles cannot \(C^1\)-match exterior Schw (wrong \(A'\) sign) — filled-wall and star+exterior are different rooms; thin shell is possible but anisotropic/singular at \(A=0\) and not adopted as a mechanism.**
