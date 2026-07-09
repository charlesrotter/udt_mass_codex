# MAP — Distance profile hunt: exact-power clue & 1D vs 2D/3D

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit) |
| **Mode** | MAP |
| **Slice scope** | MAP only |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | NONE |
| **Verifier status** | see body |
| **Build-on grade** | **LEAD** |
| **Re-run commands** | see body / N/A |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| See body | full ledger | mixed | Y |

### What is NOT claimed

- Physics canon. Hygiene grade ≠ nature proof.
- Scope wider than slice above.

### Do not build on (if any)

- CHOSE/explore items without restating premises.

---


**Date:** 2026-07-09 · **Mode: MAP / armchair zoom-out**  
**Charles:** profile off by exact root is the clue (not a fudge √); dimensional 1D vs 2D/3D question.  
**Status:** Working map for the **profile layer** after full light count is fixed.

---

## 0. Where we are (shared language)

| Layer | Status |
|-------|--------|
| **A. Light count** | **Closed as method:** energy × rate (same stretch twice) + area → full brightness rule \(d_L=(1+z)^2 D_A\). Old SNe used one stretch → exact power error. |
| **B. Distance profile** | **Open:** under full light, what is \(D_A(z)\) or \(r(z)\) from geometry? Old profile + full light is systematically off; clue = **clean powers**, not messy noise. |

Hunt = **Layer B**. No multiplying by a root to restore the old fit.

---

## 1. Power ledger (what each “2” is for)

Under full light and chart-origin \(D_A=r\):

| Factor | Role | “Dimension” |
|--------|------|-------------|
| Energy \(1/(1+z)\) | photon weaker | **1D along the ray** |
| Rate \(1/(1+z)\) | fewer arrivals | **1D along the ray** (same factor) |
| Area reciprocity | source-area distance \((1+z)D_A\) | links ray stretch to **2-sphere** |
| Flux \(\propto 1/D_{\mathrm{sa}}^2\) | spread on sphere of directions | **2D surface** (power 2 on distance) |

Assembled: \(d_L=(1+z)^2 D_A\).

**Old root error:** undercounted **1D ray** (one stretch, not two).  
**Not:** “used 3D volume dilution \(1/r^3\) by mistake.”  
**Not:** the geometric \(1/r^2\) sphere factor by itself.

So the exact root in the **old fit** is a **1D light** scar.  
The **profile** may still have a **different** exact-power scar from mixing **jobs of distance** (below).

---

## 2. Two jobs of “distance” (the dimensional fork for profiles)

On the simple metric, the label \(r\) is asked to do **two jobs**:

| Job | What it is | Dimensional dress |
|-----|------------|-------------------|
| **AREAL** | Sphere area \(=4\pi r^2\) → angle-size distance \(D_A=r\) | **2-sphere in 3D space** |
| **PATH** | How far along a radial path: composition \(x\), or proper length \(\ell=\int e^{\phi}\,dr\) | **1D chain** |

**J1** (working join in the hyp cascade): PATH chart \(x\) **is** the same number as AREAL \(r\).

That may be too strong.  
Hyperbolic max-distance is naturally a **1D composition** law (like adding velocities).  
Areal \(r\) is naturally a **3D spherical** label.  
Identifying them is a **dimensional join**, not forced by “there exists \(x_{\max}\)” alone.

### CAS contrast (linear \(\phi=ar\), full light)

| Object | vs \(z\) | Character |
|--------|----------|-----------|
| Areal \(r\) | \(\ln(1+z)/a\) | logarithmic in stretch |
| Proper 1D \(\ell\) | \(z/a\) | linear in \(z\) at all \(z\) |
| True \(d_L=r(1+z)^2\) | \((1+z)^2\ln(1+z)/a\) | very stiff at high \(z\) |

If one **wrongly** took \(D_A=\ell\) (1D proper length as angle distance):

\[
\frac{d_L^{(\ell)}}{d_L^{(r)}}=\frac{\ell}{r}=\frac{z}{\ln(1+z)}
\]

— a **clean function**, but **not** the pure \((1+z)\) root of the old half-light error.  
Different scar → different wrong job.

**Moral:** exact powers diagnose **which job was mis-assigned**, not “multiply by √.”

---

## 3. Clue table (what exact-power patterns suggest)

| Pattern under full light | Suggests |
|--------------------------|----------|
| Off by exactly \((1+z)\) vs an old half-light profile | Still comparing to **half-light** expectations; or profile was built under half light |
| Low \(z\): \(d_L\sim\sqrt{z}\) | Smooth center \(\phi\sim r^2\) (power of origin), not 3D volume |
| Low \(z\): \(d_L\sim z\) | Linear \(\phi\sim r\) (path-like leading) |
| High \(z\): \(d_L\) grows like \((1+z)^2\times\)(saturating \(D_A\)) | AREAL \(D_A\to\) const (hyp-like) + full light → very stiff |
| Ratio involving \(z/\ln(1+z)\) | PATH proper \(\ell\) mixed into \(D_A\) |
| BAO liked \(D_M\sim r\), SNe liked \(d_L\sim r(1+z)\) under half light | Operational package treated \(r\) as **PATH/comoving-like**, not pure AREAL in Etherington |

Charles’s “exact root” clue fits **Layer A** tightly and **Layer B** as “look for clean job-mix scars,” not a fudge.

---

## 4. Dimensional hypothesis (working)

**H-dim (provisional):**  
The distance-profile problem is at least partly **categorical**:

> We are solving a **1D** relational path/composition problem (dilation along lines of sight, max reach, how stretches add) while the metric’s \(r\) is a **2-sphere / 3D-embedded** areal label — and/or while **spherical radial** field math (\(r^2\) weights) is read as pure 1D.

**Not claimed:** that free 2D/3D functions should be fitted.  
**Claimed as hunt frame:** every candidate profile must declare:

1. Which object is **AREAL** \(D_A\)?  
2. Which object is **PATH** (composition / proper)?  
3. Which object enters **full light** \(d_L=(1+z)^2 D_A\)?  
4. What is **derived** vs **joined by hand**?

If (3) uses a PATH object as if it were AREAL without derive → expect **clean wrong powers**.

---

## 5. What to do next (ordered, still MAP→OBSERVE)

| Step | Action | Purpose |
|-----:|--------|---------|
| 1 | Keep full light fixed (Layer A closed as method) | No return to half count |
| 2 | **Ledger every profile** (cubic, hyp, dust, MS) with jobs AREAL / PATH / \(d_L\) input | Make dimensional mix visible |
| 3 | For hyp: **split** “\(x=X\tanh\phi\) is PATH” from “\(D_A=x\)” (drop J1 as default) | Purest 1D composition without forcing 2-sphere label |
| 4 | Ask metric: is there a **derived** map PATH→AREAL? (not free \(D_A(r)\)) | Only if a native relation appears |
| 5 | Only then score sky as **demo** of residual shape | Not a fit campaign |

### Step 3–5 tile (2026-07-09) — DONE explore

**Record:** `simple_metric_path_areal_split_results.md`  
Join **P_ell**: PATH \(x\) = proper radial length ⇒ \(D_A=r(x)=\int_0^x e^{-\phi}\,du\).  
Full-cov demo: J1 χ²/dof≈**2.17** → P_ell ≈**1.02** (LCDM ref≈0.88).  
**Support:** PATH vs AREAL over-join was load-bearing for hyp stiffness.  
**Open:** why composition \(x\) = proper (P_ell still CHOSE); residual high-\(z\); re-derive mass lock without J1.

**Easy wrong path:** set \(D_A=r/(1+z)\) because it restores old numbers.  
**Purist path:** name jobs; derive joins; characterize.

---

## 6. One-line

**Light count is fixed (two 1D stretch hits); the open hunt is the distance profile under that rule, guided by exact-power clues that flag mixing 1D path/composition with 2-sphere areal \(r\) — not a fudge factor and not 3D volume dilution.**
