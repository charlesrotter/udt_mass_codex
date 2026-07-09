# Native low-\(z\) linear Hubble — derive under true optics

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit) |
| **Mode** | DERIVE |
| **Slice scope** | static origin full light |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | NONE |
| **Verifier status** | see body |
| **Build-on grade** | **CONDITIONAL** |
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


**Date:** 2026-07-09 · **Mode: DERIVE / MAP**  
**Prior:** DA native, sourced observe, free-\(D_A\) low-\(z\) hunt, cross-sector root check, “where this takes us.”  
**Status:** PROVISIONAL theorems under named premises. No Pantheon retune.

---

## 0. Held premises

| # | Premise | Tag |
|---|---------|-----|
| P1 | Simple metric, chart-origin observer | THEORY / live |
| P2 | Geometric \(D_A=r\) | DERIVED (prior tile) |
| P3 | \(1+z=e^{\phi}\), \(\phi(0)=0\) | THEORY |
| P4 | \(d_L=(1+z)^2 D_A=r\,e^{2\phi}\) | THEORY (n=2) |
| P5 | Linear Hubble = \(d_L\sim H^{-1}z\) as \(z\to 0^+\) (some finite scale) | OBSERVE target (data class), not a fit |

---

## 1. Theorem L1 — leading series

Expand \(\phi(r)=a_1 r+a_2 r^2+a_3 r^3+\cdots\) near the origin.

\[
z=e^{\phi}-1=a_1 r+\Bigl(\tfrac{a_1^2}{2}+a_2\Bigr)r^2+O(r^3)
\]

\[
d_L=r\,e^{2\phi}=r+2a_1 r^2+O(r^3).
\]

### Case A — linear leading term \(a_1\neq 0\)

\[
z\sim a_1 r\quad\Rightarrow\quad r\sim\frac{z}{a_1},
\qquad
d_L\sim r\sim\frac{z}{a_1}.
\]

**Linear Hubble.** Scale \(1/|a_1|\) is the low-\(z\) ruler (native length, not \(H_0\) language required).

Cost: \(\phi'(0)=a_1\neq 0\).

### Case B — smooth even leading \(a_1=0\), \(a_2\neq 0\)

\[
z\sim a_2 r^2\quad\Rightarrow\quad r\sim\sqrt{z/a_2},
\qquad
d_L\sim r\sim\sqrt{z/a_2}.
\]

**Square-root law** \(d_L\propto\sqrt{z}\).  
CAS: \(\lim_{r\to 0}d_L^2/z=1/a_2\).

This is exactly the compensated-dust / free-\(D_A\) regular-center observe.

### Case C — \(a_1=0\) but force \(d_L\sim z\)

Impossible under P1–P4: \(d_L\sim r\) and \(z\sim r^2\) cannot give \(d_L\sim z\).

\[
\boxed{
\text{Under P1–P4: linear low-}z\;d_L
\;\Longleftrightarrow\;
\phi'(0)\neq 0
\;\text{(linear leading }\phi\sim a_1 r\text{)}.
}
\]

---

## 2. Theorem L2 — regularity conflict (smooth center)

A scalar field on a smooth Riemannian center in polar coordinates normally admits an **even** expansion in proper radius (\(\phi=\phi(0)+c\,\ell^2+\cdots\)), so \(\partial_\ell\phi\to 0\) at the point.

Here the radial coordinate is areal \(r\), and near a regular center \(r\sim\ell\).  
Then \(\phi'(0)=0\) is the smooth-center expectation ⇒ **Case B** ⇒ **no linear Hubble** under P4.

| Demand | Implication |
|--------|-------------|
| Smooth center (\(\phi'(0)=0\)) | \(d_L\sim\sqrt{z}\) under true n=2 |
| Linear Hubble under true n=2 | \(\phi'(0)\neq 0\) (irregular / conical / non-smooth chart) |

**This is a theorem of the package P1–P4, not a failed scan.**  
Free \(D_A\) does not remove it if \(D_A\sim r\) and \(\phi\sim a r^2\) (prior hunt).

---

## 3. Theorem L3 — operational package vs geometric \(D_A=r\)

**Operational package** (old SNe + BAO \(D_M=r\)):

\[
D_M^{\mathrm{(ops)}}=r,
\qquad
d_L^{\mathrm{(ops)}}=r(1+z)=(1+z)\,D_M^{\mathrm{(ops)}}.
\]

**Geometric + Etherington** (P2+P4):

\[
D_A=r,
\qquad
D_M^{\mathrm{(geom)}}=(1+z)r,
\qquad
d_L^{\mathrm{(geom)}}=(1+z)^2 r.
\]

Compare:

\[
d_L^{\mathrm{(ops)}}=r(1+z)=D_M^{\mathrm{(geom)}}=\frac{d_L^{\mathrm{(geom)}}}{1+z}.
\]

So:

| Claim set | Consistent? |
|-----------|-------------|
| Ops package alone (no claim \(D_A=r\) in Etherington) | Internally OK as \(d_L=(1+z)D_M\) with \(D_M=r\) |
| Geometric \(D_A=r\) + n=2 + ops \(d_L=r(1+z)\) as **true luminosity** | **INCONSISTENT** |
| Geometric \(D_A=r\) + n=2 + ops formula as **\(D_M\)** only | **Consistent** (prior root diagnosis) |

\[
\boxed{
\text{Cannot hold simultaneously: }
(D_A=r\text{ geometric})
\;\wedge\;
(d_L^{\mathrm{true}}=r(1+z)).
}
\]

One of them must go. Banked geometry drops the second as luminosity.  
The old scorecards kept the second and mis-spoke the first.

---

## 4. Relational seat — does it evade L1–L2?

Elegant frame: every observer has \(\phi=0\) at **their** seat; no preferred center.

**If** each observer’s local chart is again the simple metric with **that observer at \(r=0\)**, then L1–L2 apply **per seat**. Relational isotropy **reproduces** the same low-\(z\) dichotomy locally; it does not dissolve it.

**Only if** the metric about a generic observer is **not** that simple origin form (different normal coordinates, time-live, non-SSS, …) can low-\(z\) change without \(\phi'(0)\neq 0\) in areal \(r\).

| Reading | Low-\(z\) fate |
|---------|----------------|
| Relational = copy of simple metric at each origin | Same theorem L1–L2 |
| Relational = different local geometry | OPEN — requires derive, not slogan |

**Present status:** relational language alone is **not** a free escape hatch from L2.

---

## 5. What already “chose” \(\phi'(0)\neq 0\)

| Construction | Near origin | Low-\(z\) \(d_L\) under n=2 |
|--------------|-------------|----------------------------|
| Compensated dust, regular | \(\phi\sim ar^2\) | \(\sim\sqrt{z}\) FAIL |
| Free \(D_A\) smooth center | same class | \(\sim\sqrt{z}\) FAIL |
| Locked cubic | \(\phi\sim\tfrac32\mu_g r+\cdots\) | linear OK; **irregular** origin |
| Hyp \(x=X\tanh\phi\), J1 \(r=x\) | \(\phi\sim r/X\) | linear OK; **\(\phi'(0)=1/X\neq 0\)** |

So hyp+J1 and the cubic **already live on the irregular-origin side of L1**.  
That is why they can have linear low-\(z\); their SNe failures are **high-\(z\) shape**, not the \(\sqrt{z}\) disease.

**Clue:** the “successful” operational profiles smuggled **linear \(\phi\)**; regular FE probes forbade it.

---

## 6. Where this takes the program (ordered)

### Closed by this tile

1. Under simple metric + origin + n=2, **linear Hubble ⇔ linear \(\phi\)** (L1).  
2. **Smooth center ⇔ \(\sqrt{z}\) law** (L2).  
3. **Ops \(d_L=r(1+z)\) as true \(d_L\) is incompatible with geometric \(D_A=r\)** (L3).  
4. Free \(D_A\) does not break L2 (prior).  
5. Relational slogan alone does not break L2.

### Live fork (must choose a lane — MAP, not yet pick for Charles)

| Lane | Content | Price |
|------|---------|-------|
| **A. Irregular / linear-\(\phi\) origin as theory** | Accept \(\phi\sim a_1 r\) (or derive why); keep \(D_A=r\), n=2 | Must **derive** the linear term (not cubic smuggle); then re-do profile/high-\(z\) |
| **B. Smooth center, change low-\(z\) map** | Keep \(\phi'(0)=0\) | Must drop or modify P4 or P2 (hard — n=2 and \(D_A=r\) banked) |
| **C. Observer chart ≠ simple origin form** | Relational local metric different | Big derive; not started |
| **D. \(r\) is not geometric \(D_A\) in ops** | Ops package as \(D_M=r\) | SNe need true \(d_L=(1+z)^2 D_A\) with \(D_A\neq r\) or \(D_A=r/(1+z)\) — latter not geometric |

**Purist lean (driver recommendation, not Charles-canon):**  
**Lane A** is the least violent given banked P2–P4: admit that **macro \(\phi\) is odd/linear at the chart origin** (as hyp and cubic already do), and make that **derived or postulated cleanly** (twin of “finite \(x_{\max}\)”), then solve high-\(z\) under true n=2 without free \(D_A\) fits.

Lane B fights banked optics/geometry.  
Lane D fights geometric \(D_A=r\).  
Lane C is the elegant long game if A fails.

### Immediate next work (if continuing without Charles re-aim)

1. **Name** linear origin as working posture (Lane A) with ledger tag POSTULATE/DERIVE-OWED — parallel to \(x_{\max}\).  
2. Under Lane A + n=2 + \(D_A=r\): **OBSERVE** which profiles with \(\phi'(0)\neq 0\) exist from simple-metric operators (hyp already; sourced with \(Q_0\neq 0\); K-A; …) and their **high-\(z\)** \(d_L\) — characterize, not SNe-tune.  
3. Keep free \(D_A\) available only if Lane A high-\(z\) stalls **and** a derived \(D_A\neq r\) appears.

---

## 7. One-line

**Under the simple metric at the chart origin with true n=2, linear Hubble requires \(\phi'(0)\neq 0\); a smooth center forces \(d_L\sim\sqrt{z}\). The old SNe/BAO package is inconsistent with geometric \(D_A=r\) if \(r(1+z)\) is true luminosity. Next fork: own the linear origin (Lane A) or change chart/optics — not free functions.**
