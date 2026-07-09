# MAP — Reconstruct the earlier SNe validator (root-error as pointer)

**Date:** 2026-07-09 · **Mode: MAP / OBSERVE**  
**Why:** The n=1 Pantheon “win” rode a √-type optics error. If that was a **simple root** on an otherwise accurate stack, the validator is a **pointer** to a correct overall model — not a result to throw away.  
**Data:** `Data/Pantheon+SH0ES.dat` + `Data/Pantheon+SH0ES_STAT+SYS.cov`  
**Related:** `luminosity_distance_n2_optics_results.md`, `simple_metric_pantheon_xmax_fit_results.md`, CG §12.7–12.8, RECON-A §1.1

---

## 0. Stance

| Do | Do not |
|----|--------|
| Reconstruct the **actual stack** the old scorecard used | Re-canonize 0.166 mag under n=1 |
| Tag every layer: derived / ansatz / error | Invent new knobs to re-win Pantheon |
| Ask: *if only the root is wrong, what object was right?* | Call cubic+μ_g “proven micro→macro” without re-grading |
| Use the pointer under **banked n=2** | Fit free \(D_A(r)\) surfaces |

---

## 1. The earlier validator — reconstructed stack

### 1.1 Metric (spine)

\[
ds^2 = -e^{-2\phi(r)}c^2 dt^2 + e^{2\phi(r)}dr^2 + r^2 d\Omega^2
\]

| Item | Role | Tag |
|------|------|-----|
| Reciprocal SSS form | R1–R3 style simple metric | THEORY (live frame) |
| \(r\) areal | area \(=4\pi r^2\) | THEORY (canon areal reading) |
| \(1+z = e^{\phi(r)}\) | static redshift, observer \(\phi_o=0\) | THEORY |

### 1.2 Background profile (locked cubic)

\[
\boxed{
\phi(r)=\tfrac32\mu_g r - \cos(\pi/5)\,\mu_g^2 r^2 + \tfrac23\mu_g^3 r^3
}
\]

| Piece | Claimed origin | Honest tag |
|-------|----------------|------------|
| Coefficients \(3/2\), \(\cos(\pi/5)\), \(2/3\) | Angular Diophantine \((j,\ell,\|\kappa_{\max}\|)=(1/2,1,3)\) | **ALGEBRAIC under cubic ansatz** (CG §12.7) |
| Polynomial **form** (cubic in \(r\)) | Not forced by FE | **ANSATZ** (D-POLY-1 open) |
| \(\phi'(0)\neq 0\) | Frobenius-irregular at origin | **SCOPED** envelope, not regular vacuum core |
| \(\mu_g=\pi\mu/13=0.2473\,\mathrm{Gpc}^{-1}\) | Micro quantum sum | **CLAIMED bridge** (re-grade separately; SNe shape almost μ_g-degenerate with \(M\)) |

**Operational SNe use:** invert \(1+z=e^{\phi(r)}\) → \(r=r(z)\); only absolute magnitude offset free.

### 1.3 Distance law (the root)

**What the scorecard used (CG §12.8 historical, now bannered ERROR):**

\[
\boxed{d_L = r\,e^{\phi(r)} = r\,(1+z)
\qquad\text{(n=1)}}
\]

**Native optics (banked 2026-07-08):**

\[
\boxed{d_L = (1+z)^2 D_A = r\,e^{2\phi}
\qquad\text{(n=2, if }D_A=r\text{)}}
\]

**Root reading:** \(e^{\phi}=\sqrt{g_{rr}}\). n=1 multiplies by \(\sqrt{g_{rr}}\) once; n=2 multiplies by \(g_{rr}=e^{2\phi}\).  
Charles’s “root/power” instinct: **CONFIRMED** as the optics bug (`luminosity_distance_n2_optics_results.md`).

### 1.4 Scoring (CR-327c lineage)

| Item | Value |
|------|--------|
| Data | Pantheon+ SH0ES |
| Cut | typically \(z>0.01\), drop calibrators for cosmology |
| Free params | **1** (absolute \(M\)); no \(H_0,\Omega_m\) language in UDT fit |
| Historical full-cov claim | \(\chi^2/\mathrm{dof}\approx 0.94\), RMS \(\approx 0.16\) mag |
| **Reproduced here (full STAT+SYS)** | \(\chi^2/\mathrm{dof}=\mathbf{0.9355}\), RMS \(=\mathbf{0.1640}\) mag |

Reproduction confirms: the **machinery + cubic + n=1** still scores that way on Charles’s local files.

---

## 2. What fails when only the root is “fixed” naively

Hold cubic \(r(z)\), set \(D_A=r\), switch to n=2:

| Model | Full-cov \(\chi^2/\mathrm{dof}\) | RMS |
|-------|----------------------------------:|----:|
| **Old validator** \(d_L=r(1+z)\) | **0.94** | **0.164** |
| Naive n=2 \(d_L=r(1+z)^2\) | **4.56** | **0.471** |
| Hyperbolic n=2 (recent) | 2.17 | 0.307 |
| LCDM \(\Omega_m=0.3\) ref | 0.88 | 0.154 |

**Lesson:** “Multiply the old formula by one more \((1+z)\)” **destroys** the fit. The root is not a decorative typo on a finished law; it is **entangled** with what \(r\) was doing in the formula.

---

## 3. The pointer (if the old \(d_L\) shape was right and n=2 is right)

### 3.1 Logical identity (counterfactual vs native)

Banked optics:

\[
d_L = (1+z)^2\, D_A
\]

Old numerical success:

\[
d_L^{\mathrm{(old\ numbers)}} = r_{\mathrm{cubic}}(z)\,(1+z)
\]

**Counterfactual pointer** (keep old *numbers* under n=2):

\[
D_A^{\mathrm{(pointer)}}(z)
= \frac{r_{\mathrm{cubic}}(z)}{1+z}
= r_{\mathrm{cubic}}(z)\, e^{-\phi}
\]

That recovers the old score by algebra — **not** a derivation of geometric \(D_A\).

**Native derive (2026-07-09):** `simple_metric_DA_native_derive.md`  
For observer at chart origin on the simple metric, **geometric \(D_A=r\) is forced**.  
Then \(r(1+z)=D_M\equiv(1+z)D_A\), and the old formula is **correct \(D_M\) mislabeled as \(d_L\)** (missing final \((1+z)=\sqrt{g_{rr}}\)).  
So the better “correct component” reading is **\(D_M=r(1+z)\)**, not “native \(D_A=r/(1+z)\)”.

### 3.2 Naming scar (likely the same √ family)

Standard static/FLRW bookkeeping:

| Symbol | Role | Optics |
|--------|------|--------|
| \(D_A\) | angular diameter distance | area |
| \(D_M\) | “comoving” / transverse comoving | \(D_M=(1+z)D_A\) |
| \(d_L\) | luminosity | \(d_L=(1+z)D_M=(1+z)^2 D_A\) |

Old UDT package said:

- \(D_A = r\) (areal chart)  
- \(d_L = r(1+z)\)  

That is **internally** the package  
“\(D_M = r\), \(d_L = (1+z)D_M\)”  
with **\(D_A\) mis-named as \(r\)** instead of \(r/(1+z)\).

So the √ error and the **\(D_A\) vs \(D_M\) label** may be **one scar**:

- Wrong: call areal \(r\) the thing that multiplies only one \((1+z)\).  
- Right under n=2: either \(d_L=r(1+z)^2\) **if** \(D_A=r\), **or** keep the good \(d_L\) shape only if \(D_A=r/(1+z)\).

### 3.3 What the pointer does *not* claim

| Not claimed | Why |
|-------------|-----|
| \(D_A=r e^{-\phi}\) is derived from the metric | **POINTER only** — forced if old shape + n=2 both kept |
| Cubic is the native FE solution | Still D-POLY-1 ansatz; irregular at 0 |
| μ_g micro bridge is proven by SNe | Shape nearly offset-degenerate |
| Free \(D_A(r)\) is reopened | One **specific** relation \(D_A=r/(1+z)\) is the pointer, not a free function |

---

## 4. Layer-by-layer ledger (chose / derived / error)

| # | Layer | Content | Tag |
|---|-------|---------|-----|
| L0 | Metric form | reciprocal SSS + areal \(r\) | THEORY |
| L1 | Redshift | \(1+z=e^{\phi}\) | THEORY |
| L2 | Etherington n=2 | \(d_L=(1+z)^2 D_A\) | THEORY (banked) |
| L3 | **Old optics** | \(d_L=r(1+z)\) | **ERROR** (√\(g_{rr}\) once) |
| L4 | Identify \(D_A=r\) | areal = diameter distance | THEORY *if* ops use areal spheres; **in tension** with L3 |
| L5 | Cubic \(\phi(r)\) | locked coefficients | ANSATZ form + algebraic coeffs |
| L6 | Invert \(r(z)\) from cubic | operational chart | DEPENDS on L5 |
| L7 | One offset \(M\) | SNe nuisance | UNAVOIDABLE |
| L8 | **Pointer** | \(D_A = r_{\mathrm{cubic}}/(1+z)\) under L2+old shape | **HYPOTHESIS** for join, not mechanism |

**Tension already visible in the old stack:** L3 and L4 cannot both be right once L2 is enforced. The scorecard kept L3+L4; n=2 forces a choice.

---

## 5. Why this is a pointer to a possible correct model

1. **The sky shape the cubic+n=1 hit is not garbage** — full cov \(\chi^2/\mathrm{dof}\approx 0.94\), competitive with ΛCDM ref, one nuisance only.  
2. **The only banked local error in the distance formula is the root** (n=1 vs n=2).  
3. **Preserving that shape under correct optics** yields a **unique** \(D_A(z)\) given the cubic chart: \(D_A=r/(1+z)\).  
4. That object is **not** “free \(D_A\)”; it is a **single structural re-identification**:  
   *the radial label that solves the cubic redshift map is \(D_M\)-like, not \(D_A\)-like* — or equivalently areal \(D_A\) is diluted by one redshift factor relative to that label.  
5. **Same √ family** as the hyp residual clue (\(\sim\sqrt{1+z}\)): half or whole powers of \(e^{\phi}\) in the wrong slot.

### Cascade hope (Charles’s line)

If the true fix is “which length is \(r\) in the line element / in the SNe map,” then:

- SNe optics  
- hyp vs cubic stiffness  
- maybe MS mass chart and “comoving vs areal” BAO readings  

can move **together** — without dark fluids.

---

## 6. What to derive next (gated; not tonight’s free-for-all)

**MAP questions (order):**

1. **On the simple metric alone**, is there a native geometric length  
   \(\ell(r,\phi)\) equal to \(r e^{-\phi}\) (or \(r/\sqrt{g_{rr}}\), etc.) that **must** enter Etherington as \(D_A\)?  
   Or is areal area-radius still forced as \(D_A\)?

2. **Does the cubic \(r(z)\) secretly play \(D_M\)?**  
   If yes, write the validator as:  
   \(1+z=e^{\phi(D_M)}\), \(d_L=(1+z)D_M\), \(D_A=D_M/(1+z)\) — which is **n=2 in disguise** and matches the old numbers.  
   Then the bug was **only naming** \(D_A=r\), not the optical powers.

3. **Metric exponent / \(\phi\) normalization:**  
   could \(g_{rr}=e^{2\phi}\) vs a half-rapidity field explain why one √ was dropped in the prose derivation of §12.8?

4. **Do not** first re-fit cubic coefficients under n=2 — that targets SNe and smuggles.  
   **Do** first settle (1)–(2) in pure geometry.

---

## 7. Reproduction anchors (this session)

```text
OLD n=1 cubic:     chi2/dof = 0.9355  RMS = 0.1640   (full STAT+SYS)
naive n=2 cubic:   chi2/dof = 4.5646  RMS = 0.4712
pointer DA=r/(1+z): identical to OLD (by algebra)
hyp n=2:           chi2/dof = 2.1665  RMS = 0.3074
LCDM Om=0.3 ref:   chi2/dof = 0.8805  RMS = 0.1541
```

Script lineage for cubic score: same invert as `sne_test_derived_n.py` / CG §12.7; data under `Data/`.

---

## 8. One-line

**Earlier SNe validator = simple metric + locked cubic \(r(z)\) + wrong n=1 optics; numbers still reproduce (χ²/dof≈0.94). Naive n=2 on the same \(r\) fails hard. The pointer: keep the good \(d_L\) shape under true n=2 ⇒ \(D_A = r_{\mathrm{cubic}}/(1+z)\) — i.e. the old \(r\) was \(D_M\)-like, and the root error was labeling / which length multiplies which powers of \(e^{\phi}\), a possible trunk fix for more than SNe.**
