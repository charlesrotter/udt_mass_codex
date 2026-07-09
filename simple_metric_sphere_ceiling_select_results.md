## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE / OBSERVE |
| **Slice scope** | \(D_A=r\), ceiling \(A(X)=0\), full light; static SSS |
| **Observing or targeting?** | OBSERVE selection structure — **not** χ² law-picking |
| **Comparator scaffolds** | LCDM residual reference only where quoted |
| **Verifier status** | SELF-SCRIPT / CAS session; `simple_metric_sphere_ceiling.py` |
| **Build-on grade** | **LEAD** |
| **Re-run commands** | `python3 simple_metric_sphere_ceiling.py` · residual block in build script |

### Premise ledger

| Item | Tag | Enters claim? |
|------|-----|---------------|
| Full light + \(D_A=r\) | DERIVED / THEORY | Y |
| Ceiling \(r\to X\), \(A\to0\) | CHOSE Charles sphere-size | Y |
| \(A=1-r/X\) | CHOSE geometric lead | Y as lead |
| Const-ρ critical \(A=1-r^2/X^2\) | THEORY GR-style fill | Y as rejected sibling |
| Regular center \(\phi\sim r^2\) | THEORY smooth | Y as constraint |

### What is NOT claimed

- Unique FE derivation of \(A=1-r/X\) complete.
- Canon. Half light.

---

# Selection structure for sphere-ceiling approach

## 1. Theorem (already banked, reapplied)

Under **full light** + **\(D_A=r\)** + **smooth center** \(\phi\sim ar^2\):

\[
d_L\sim\sqrt{z}\quad(z\to 0)
\]

**Linear Hubble fails.**  
(`simple_metric_lowz_linear_native_derive.md`)

**Consequence for ceiling models:**  
Any “nice” constant-density fill that is regular at the origin and hits \(A=0\) at \(r=X\) is in this class.

---

## 2. Constant-density critical sibling (rejected for low-\(z\))

Standard MS fill with \(\rho=\mathrm{const}\) and \(A(X)=0\):

\[
A=1-\frac{r^2}{X^2},\qquad \rho=\frac{3c^2}{8\pi G X^2}
\]

- **Regular** density at \(r=0\)  
- Same **sphere ceiling** spirit  
- Full light residual: χ²/dof ~ **24** (catastrophic)  
- Low-\(z\): \(d_L\sim\sqrt{z}\) as predicted  

So: **cannot** “fix the origin” with constant density without destroying nearby distance law under full light.

---

## 3. Why \(A=1-r/X\) sits in a special slot

### Geometry

\[
A=1-\frac{r}{X},\quad A'=-\frac{1}{X}=\mathrm{const},\quad
m=\frac{c^2 r^2}{2GX},\quad
\rho=\frac{c^2}{4\pi G X r}
\]

- Compactness \(2Gm/(c^2 r)=r/X\) **linear** in sphere size  
- Hits critical compactness **exactly at** \(r=X\)  
- \(\phi'(0)=1/(2X)\neq 0\) — **mild center irregularity**, same *kind* of price as linear Hubble (Lane A)

### Power family \(A=1-(r/X)^n\) (characterize, not fit)

| \(n\) | Low-\(z\) class | χ²/dof (full light, 1 offset) |
|------:|-----------------|--------------------------------:|
| 0.5 | bad | ~86 |
| **1** | **linear** \(d_L\sim 2z+\cdots\) | **~0.91** |
| 1.5 | intermediate | ~11 |
| 2 | \(\sim\sqrt{z}\) | ~24 |
| 3 | worse | ~41 |

Among this **one-parameter geometric family** with fixed ceiling \(A(X)=0\), **\(n=1\) is the unique member with linear low-\(z\)** (because \(\phi'(0)\neq0\) only for \(n=1\) in the sense of leading \(\phi\sim r\) from \(A=1-u^n\approx 1-n(r/X)+\cdots\) wait:

\(A=1-(r/X)^n\), near 0: \(A\approx 1-(r/X)^n\).  
For \(n>1\), \(A=1-O(r^n)\) with \(n\ge2\) ⇒ \(\phi\sim r^n\) or \(r^2\) ⇒ soft center.  
For \(n=1\), \(A=1-r/X\) ⇒ \(\phi\sim r/(2X)\).  
For \(n<1\), more singular at 0.

So **\(n=1\) is selected by linear Hubble + power-law ceiling family**, not by Pantheon optimization over free functions.

**Still not:** unique among *all* functions \(A(r)\). Only: **special inside \(A=1-(r/X)^n\)**.

---

## 4. Geometric reading (selection lead)

| Condition | Gives |
|-----------|--------|
| Vacuum \(\Delta A=0\) / Schw | \(A=1-r_s/r\) — **inner** horizon style, not outer ceiling at large \(r\) |
| Outer ceiling \(A(X)=0\), \(A(0)=1\), **constant \(A'\)** | **\(A=1-r/X\)** uniquely |
| Outer ceiling + **regular \(\rho(0)\)** + full light + linear Hubble | **In tension** (theorem §1) |

**Lead selection principle (named, not yet action-derived):**

> Among static SSS models with \(A(0)=1\), \(A(X)=0\), and **uniform gradient of lapse** \(A'=\mathrm{const}\), the profile is **exactly** \(A=1-r/X\).

That is a clean geometric CHOSE of “simplest edge,” parallel to how one picks linear potentials — **not** a free SNe spline.

**Owed:** promote “constant \(A'\)” from a FE / variational statement if possible (or accept as geometric simplicity postulate parallel to xmax).

---

## 5. Origin irregularity — reframe (not a bug to erase with const ρ)

Under full light + \(D_A=r\):

| Center type | Nearby \(d_L\) | Ceiling fill |
|-------------|----------------|--------------|
| Smooth \(\phi\sim r^2\), regular \(\rho(0)\) | \(\sim\sqrt{z}\) **fail** | e.g. \(A=1-r^2/X^2\) |
| \(\phi'(0)\neq 0\) (as in \(A=1-r/X\)) | \(\sim z\) **OK** | live lead |

So the \(\rho\sim 1/r\) singularity is the **matter dual** of the linear-\(\phi\) center needed for Hubble.  
“Tame the center” **cannot** mean “force regular ρ(0)” without a **different** low-\(z\) mechanism (other chart, other light rule — both closed/hostile).

**Working posture:** accept mild central irregularity as the price of linear Hubble on this ladder; document it; don’t half-light patch.

---

## 6. Status of packages

| Package | Role now |
|---------|----------|
| Sphere ceiling \(A=1-r/X\) | **Live LEAD** distance law under Charles sphere-size \(X\) + full light |
| Hyp tanh composition | Contrast / possible *other* sector (displacements), **not** live SNe map |
| Const-ρ critical | Structural foil (regular center fails low-\(z\)) |

---

## One-line

**Constant-\(A'\) edge \(A=1-r/X\) is the unique power-family ceiling with linear Hubble; regular const-ρ critical is unique-ish regular fill but fails low-\(z\); origin singularity of the lead is tied to that Hubble requirement — next is FE meaning of constant \(A'\), not χ² retune.**
