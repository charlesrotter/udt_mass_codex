# K-A develop — lapse-harmonic vacuum on the simple metric

**Date:** 2026-07-08 · **Mode: OBSERVE / develop**  
**Law:** \(\Delta A=0\) with \(A=e^{-2\phi}\), i.e. \(G_{\theta\theta}=0\) on the simple metric (CAS identity).  
**Foundation:** `simple_metric_third_path_derive.md`  
**Status:** PROVISIONAL working development of the K-A branch. Not Charles canon.

---

## 1. Law and solution space

### Equation

\[
\Delta A = 0, \qquad A=e^{-2\phi},
\quad
\Delta = \frac1{r^2}\partial_r\bigl(r^2\partial_r\bigr)
\quad\text{(flat areal Laplacian).}
\]

Spherical solutions:

\[
\boxed{A(r) = C_0 + \frac{C_1}{r}}
\quad (A>0 \text{ on the domain}),
\quad
\phi = -\frac12\ln A.
\]

Under residual chart shift \(\phi\to\phi+\lambda\), \(A\to e^{-2\lambda}A\). If \(C_0>0\), set **\(C_0=1\)** by that shift (no loss of physics).

### Branches (after \(C_0=1\) when possible)

| Branch | \(A\) | Domain | Horizon? |
|--------|-------|--------|----------|
| **Schw-like** | \(1-r_s/r\) (\(r_s>0\)) | \(r>r_s\) | **Yes** \(r=r_s\) |
| **No-horizon** | \(1+b/r\) (\(b\ge 0\)) | \(r>0\) | No |
| **Pure \(1/r\)** | \(C_1/r\) (\(C_0=0\)) | \(r>0\) | \(\phi\to+\infty\) as \(r\to 0\) only |
| **\(C_0<0\)** | needs \(r<r_{\mathrm{out}}\) | finite outer chart | outer zero of \(A\) possible |

**Primary macro/c-edge interest:** Schw-like branch \(A=1-r_s/r\).

---

## 2. Schw-like branch = standard Schwarzschild areal metric

On the simple UDT metric, \(g_{rr}=e^{2\phi}=1/A\).  
With \(A=1-r_s/r\):

\[
ds^2 = -\Bigl(1-\frac{r_s}{r}\Bigr)c^2 dt^2 + \Bigl(1-\frac{r_s}{r}\Bigr)^{-1}dr^2 + r^2 d\Omega^2.
\]

That **is** the Schwarzschild line element (areal radius).  
So K-A on the Schw branch is not a weird cousin of GR vacuum — it **is** GR’s vacuum SSS solution, recovered as **“lapse is areal-harmonic.”**

**Scale:** \(r_s\) free (solution constant). In GR, \(r_s=2GM/c^2\); here same role if \(G,c\) enter the Einstein constant later. No hand cosmological \(x_{\max}\).

---

## 3. \(c\)-analogy / edge structure (honest)

### Infinite redshift (static observers)

Observer at \(r_0>r_s\) with chart \(\phi(r_0)=0\):

\[
\phi_{\mathrm{chart}}(r) = -\frac12\ln\frac{A(r)}{A(r_0)},
\quad
1+z = e^{\phi(r_s)-\phi(r_0)} = \sqrt{\frac{A(r_0)}{A(r_s)}}.
\]

As emission radius \(r_s\to r_s^+\) (approach horizon):

\[
A(r_s)\to 0 \quad\Rightarrow\quad z\to\infty.
\]

**Passes:** diverging dilation/redshift effect as the edge is approached.

### Unattainability (careful)

| Path | To horizon \(r\to r_s^+\) |
|------|-------------------------|
| Static observer family | Cannot sit at \(r_s\) (infinite \(z\), \(g_{tt}\to 0\)) |
| Radial **proper distance** \(\ell=\int e^{\phi}dr=\int dr/\sqrt{A}\) | **Finite** as lower limit \(\to r_s\) (unlike K-UW log divergence) |
| Free-fall (GR lore) | Crosses in finite proper time |
| Coordinate time for distant static observer | Signal delay \(\to\infty\) |

So K-A Schw edge is **\(c\)-like as a horizon / infinite-redshift surface**, not as “infinite proper distance wall” (that was K-UW).  
Still the standard geometric edge of vacuum GR — and it matches Charles’s “φ→∞ at finite chart radius.”

### Outer infinity

As \(r\to\infty\): \(A\to 1\), \(\phi\to 0\) (after chart fix at infinity) — asymptotically flat, **not** an outer \(c\)-wall.  
The \(c\)-like structure is the **inner** horizon edge of the exterior chart, not “edge of the universe at large \(r\).”

**Macro reading tension (honest):**  
Cosmology often wants a **far** edge. K-A Schw gives a **central-mass horizon**.  
Relational reuse (every observer?) does **not** by itself turn one black-hole exterior into a full cosmic background.  
Still the best **simple-metric vacuum** with true \(\phi\to\infty\) at finite \(r\).

---

## 4. Redshift law (relational chart)

For two static observers on the same exterior:

\[
1+z = \sqrt{\frac{A(r_{\mathrm{obs}})}{A(r_{\mathrm{src}})}} = \sqrt{\frac{1-r_s/r_{\mathrm{obs}}}{1-r_s/r_{\mathrm{src}}}}.
\]

- Source closer to horizon than observer ⇒ **redshift**.  
- Same formula as standard Schwarzschild gravitational redshift.  
- Consistent with UDT \(1+z=e^{\Delta\phi}\) once \(\phi=-\frac12\ln A\).

Weak field (\(r\gg r_s\)): \(\phi\sim r_s/(2r)+\cdots\), Newtonian match with \(r_s\sim 2GM/c^2\).

---

## 5. Other K-A branches (brief)

| Branch | Notes |
|--------|-------|
| \(A=1+b/r\) | No horizon; \(\phi\) finite; like “negative mass” sign; fails \(c\)-edge |
| \(A=C_1/r\) | \(\phi\to+\infty\) only as \(r\to 0\); singular origin |
| \(C_0<0\) | Possible **outer** zero of \(A\) at finite \(r_{\mathrm{out}}\) — exotic sign; **flag for later** if one wants outer edge without free \(D_A\) |

**Outer-edge teaser (not developed):** \(A=C_0+C_1/r\) with \(C_0<0\), \(C_1>0\) gives \(A=0\) at \(r_{\mathrm{out}}=-C_1/C_0>0\) and \(A>0\) for \(r<r_{\mathrm{out}}\). That is a **finite outer horizon** chart. Signs look non-standard vs positive mass; tag **OPEN / exotic**, not discarded without a look.

---

## 6. Relational notes (no preferred center)

| Point | Content |
|-------|---------|
| \(\phi=0\) | Always a **chart choice** for one observer |
| \(r_s\) | Solution parameter (mass), not a preferred “cosmic center” by itself — but the **geometry is centered** on a mass in this SSS chart |
| Macro cosmos | One Schwarzschild mass is **not** yet “the universe”; it **is** the vacuum exterior law under K-A |
| Frame-relation | Same as GR: gravitational redshift between static shells; multi-center / cosmological assembly is **later** |

K-A does **not** by itself solve “no preferred center cosmology.” It solves “simple metric vacuum with \(c\)-like horizon.”

---

## 7. Premise ledger

| Item | Tag |
|------|-----|
| Simple metric | LIVE |
| \(\Delta A=0\Leftrightarrow G_{\theta\theta}=0\) | DERIVED identity; **vacuum condition CHOSE** (geometric) |
| Not from EH bulk EL | Honest (EH empty on family) |
| Schw branch | Full GR vacuum SSS |
| \(r_s\) free | Solution constant / mass |
| Free \(D_A\) | Quarantined |
| Outer exotic \(C_0<0\) | OPEN |

---

## 8. Where this leaves the three laws

| Law | Role now |
|-----|----------|
| **K-A** | **Working vacuum for \(c\)-horizon** on simple metric (develop here) |
| **K-UW** | Alternate horizon (infinite proper distance); clock-harmonic |
| **K-R1** | Shift-pure Coulomb; no horizon; F1 bulk |

**SQ geometric \(\mathcal{K}\) / dilated-dust exterior** remain **far** for \(c\)-edge (self-quench).

---

## 9. Next

1. Optional: map **exotic outer** \(C_0<0\) branch carefully (signs, energy).  
2. Matter: how continuum sources **modify** \(\Delta A=0\) (Einstein with \(T_{\mu\nu}\)) — derived, not SQ paste.  
3. Relational multi-mass / cosmology — only after vacuum K-A is held.

---

## Plain summary

The third path says: make the **clock-rate squared** (the lapse) look like a simple \(1/r\) field in ordinary space. That **is** the Schwarzschild outside of a mass — dilation goes crazy at a finite radius (the horizon), redshift for hovering observers goes to infinity, and that **is** the classic geometric “you don’t sit beyond this” edge.  

It is **not** yet a full centerless cosmos by itself; it **is** the clean simple-metric vacuum that finally matches the \(c\)-style edge you’ve been pointing at. The other two laws are still meaningful: pure shift (Coulomb) and pure clock-harmonic (different horizon).
