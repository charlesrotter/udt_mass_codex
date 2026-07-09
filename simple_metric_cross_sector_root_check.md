# Check — Was the root error only in the SNe validator?

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit) |
| **Mode** | MAP |
| **Slice scope** | corpus audit |
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


**Date:** 2026-07-09 · **Mode: MAP / OBSERVE (corpus audit)**  
**Clue (Charles):** root may have appeared only in SNe, not BAO/CMB scaffolding — check, don’t assume.  
**Status:** PROVISIONAL audit of **what formulas were used**, not a re-fit of BAO/CMB.

---

## 0. What “the root error” means here

Banked optics (2026-07-08): with geometric \(D_A=r\) at chart origin,

\[
d_L = (1+z)^2 D_A = r\,e^{2\phi}.
\]

**Root error (SNe scorecard):** used

\[
d_L^{\mathrm{(old)}} = r\,e^{\phi} = r(1+z)
\]

i.e. one factor of \(e^{\phi}=\sqrt{g_{rr}}\) short — or equivalently **\(D_M\) labeled as \(d_L\)**.

---

## 1. Sector-by-sector: what distance law was actually used?

| Sector | Observable in validator / scorecard | Formula used | Used wrong \(d_L=r(1+z)\)? |
|--------|-------------------------------------|--------------|---------------------------|
| **SNe** | distance modulus ← \(d_L\) | \(d_L=r e^{\phi}=r(1+z)\) (CG §12.8 historical; CR-327c) | **YES — load-bearing** |
| **BAO transverse** | \(D_M/r_d\) | \(D_M=r(z)\) (RECON-A; CG §29.1) | **No \(d_L\)** — different symbol |
| **BAO radial** | \(D_H\) | \(D_H=1/(\phi'(r)\,(1+z))\) (CG §29.2); survey \(D_H\) OPEN/mismatch | No \(d_L\) |
| **CMB peaks (legacy poly)** | multipole positions / projection | geometric kernel, \(r\), weights \(e^{-3\phi}\); **not** SNe \(d_L\) | **No** |
| **CMB Tolman** | \(T_{\mathrm{obs}}\) | \(T\propto e^{-\phi}=(1+z)^{-1}\) (correct temperature redshift) | N/A (not \(d_L\)) |
| **CMB intensity / Tolman \(I\)** | surface brightness | \((1+z)^4\) class (n=2-consistent) noted in n=2 results | **Opposite** of n=1 |
| **Number-count / dipole** | flux / \(d_L\) in some closed forms | often \(d_L=r e^{2\phi}\) **n=2** (CG §27.2) | **No — used n=2** |

**Verdict on the narrow clue:**  
The **false Pantheon win** is **SNe-local**: only the SNe validator put the wrong \(d_L\) formula on the critical path.  
BAO and CMB scaffolding **did not** call `d_L = r(1+z)` for their main scores.

That is a real clue — with the caveats in §3–4.

---

## 2. BAO in more detail (not innocent, different bug class)

### What BAO used

\[
\boxed{D_M(z)=r(z)}
\]

with \(r\) inverted from \(1+z=e^{\phi(r)}\) (same cubic / same \(\mu_g\) family as SNe).

Survey comparison: \(D_M/r_d\) (transverse). \(D_V\) often demoted; \(D_H\) **OPEN** (does not match cleanly).

### Relation to the root

Etherington ladder (with geometric \(D_A=r\)):

| Name | Should be | Corpus BAO | Corpus SNe |
|------|-----------|------------|------------|
| \(D_A\) | \(r\) | said \(D_A=r\) (geometry) | said \(D_A=r\) |
| \(D_M\) | \((1+z)r\) | **used \(D_M=r\)** | — |
| \(d_L\) | \((1+z)^2 r\) | — | **used \(d_L=(1+z)r\)** |

So:

- SNe error = missing one \((1+z)\) on the way to **\(d_L\)**.  
- BAO choice = missing one \((1+z)\) on the way to **\(D_M\)** *if* \(D_A=r\) is held.

**Single consistent “wrong package” that fits both scorecards:**

\[
r \;\longleftrightarrow\; D_M^{\mathrm{(ops)}},
\qquad
d_L^{\mathrm{(ops)}} = (1+z)\,r,
\qquad
\text{and do not use }D_A=r\text{ for Etherington}.
\]

That package is **internally consistent** (standard \(d_L=(1+z)D_M\)) and matches:

- SNe n=1 formula,  
- BAO \(D_M=r\).

It **conflicts** with **geometric** \(D_A=r\) + full Etherington \(d_L=(1+z)^2 D_A\).

So BAO did **not** share the SNe **symbol** `d_L`, but it **did** share the **chart labeling** “areal \(r\) plays the role of comoving \(D_M\).”

**Not “BAO was only a fit with no structure.”**  
**Also not “BAO used correct n=2 \(d_L\).”** It never needed \(d_L\).

---

## 3. CMB in more detail (weak as a distance-ladder clue)

| Layer | Role of distance / redshift | Root-error contact |
|-------|----------------------------|--------------------|
| Tolman \(T\) | one power of \(e^{-\phi}\) | Correct; not \(d_L\) |
| Projection weights | \(e^{-3\phi}\), \(r^2\), Bessel/\(C_\ell\) kernels | Geometric; not SNe \(d_L\) |
| Legacy acoustic / sound-horizon scaffolding | heavily **demoted** (S99 wave purge; LCDM ontology) | Unreliable as theory evidence |
| Peak **positions** micro-route | Dirac eigenvalues / angular algebra | Not \(d_L(z)\) ladder |
| Surface brightness \((1+z)^4\) | n=2-like intensity | **Contradicts** n=1 SNe law if both taken seriously |

**Honest grade:** CMB does **not** validate n=1, and mostly **does not test** the SNe \(d_L\) formula.  
Much of the old CMB “fit” stack is **scaffolding / demoted** — so “CMB looked fine without the root error” is **not** strong evidence the root is harmless outside SNe. It mostly means **CMB wasn’t scoring \(d_L\)**.

Number-count / dipole (when using flux) often used **n=2** explicitly — intra-theory **split conventions** were already on record (CG §27.12 one-factor vs two-factor).

---

## 4. Known dual convention (corpus already noticed the split)

CG §27.12 documents both:

- **One-factor** \(d_L=r e^{\phi}\) — SNe / CR-327 lineage  
- **Two-factor** \(d_L=r e^{2\phi}\) — number-count / some BAO amplitude work  

They argued first-order dipole formulas are **sum-invariant** under the choice — which **hides** the conflict for those observables but **does not** make SNe n=1 correct.

So: the root was **concentrated in SNe as a scorecard**, but the **convention split was multi-sector**, not a single typo in one file.

---

## 5. Clue assessment

| Claim | Grade |
|-------|--------|
| Wrong \(d_L=r(1+z)\) was **load-bearing only for SNe** | **TRUE** |
| BAO/CMB validators used the same wrong \(d_L\) | **FALSE** |
| BAO is therefore clean / correct distance theory | **FALSE** — used \(D_M=r\), partner labeling to the SNe package |
| CMB proves the metric distance ladder without the root | **WEAK** — different observables; much scaffolding demoted |
| “Only SNe mattered so fix is SNe-only patch” | **FALSE** — chart role of \(r\) is shared with BAO |
| Useful pointer | **YES** — root is **\(d_L\)-assembly / naming**, not a universal factor missing from every macro formula |

---

## 6. How this feeds the live hunt

1. **Root A** stays: SNe called \(D_M\) luminosity distance (or dropped one \(\sqrt{g_{rr}}\)).  
2. **BAO** suggests the operational success package was  
   \(r \sim D_M\), \(d_L \sim (1+z)r\) — i.e. **\(r\) as comoving-like**, not geometric \(D_A\) in the Etherington slot.  
3. That **reinforces** the earlier pointer without reviving free \(D_A\) as a fit surface: the tension is  
   **geometric \(D_A=r\)** vs **operational \(r \leftrightarrow D_M\)**.  
4. CMB is **not** a strong independent conviction either way on this root.  
5. Low-\(z\) \(\sqrt{z}\) problem (regular origin) is **orthogonal**: it is about \(\phi(r)\) asymptotics under true \(d_L=(1+z)^2 D_A\), not about which sector used n=1.

---

## 7. One-line

**Checked: the false SNe win is from a \(d_L\) formula BAO/CMB did not use; BAO instead used \(D_M=r\), which is the consistent partner of that SNe package if \(r\) is comoving-like — so the clue is real (root is \(d_L\)-local as a bug) but not “BAO/CMB are clean theory.”**
