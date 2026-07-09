## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | PONDER / MAP (zoom-out) |
| **Frame** | elegance uncover + SNe shape clues |
| **Slice** | mathematical properties of SNe-near **named** candidates |
| **Observing or targeting?** | MAP properties — SNe ranked them; **not** crowning |
| **Build-on grade** | **LEAD map** |
| **Related** | `simple_metric_SNe_shape_clue_results.md`, `UDT_ELEGANCE_UNCOVER.md` |

### Premise ledger

| Item | Tag |
|------|-----|
| Full light + \(D_A=r\) | DERIVED held |
| Candidates L, P (near data); H (fail, contrast) | named theory objects |
| SNe χ² | clue rank only |
| Winner derived | **OPEN** |

---

# Zoom-out — math of the promising candidates

SNe (full cov, 1 offset) put three **named** laws on the table:

| ID | Law (sketch) | χ²/dof | Role here |
|----|----------------|--------:|-----------|
| **L** | Linear ceiling \(A=1-r/X\) | **0.91** | promising |
| **P** | Hyperbolic boost + **P_ell** join | **1.02** | promising |
| **H** | Hyperbolic boost + **J1** | 2.17 | contrast (fails SNe) |

More than one elegant stack can exist; data say **L** and **P** sit near the envelope, **H** does not.  
Below: **what each *is* mathematically**, side by side — so the next derive knows what to aim at.

---

## 1. One-page comparison

| Property | **L** linear ceiling | **H** hyp + J1 | **P** hyp + P_ell |
|----------|----------------------|----------------|-------------------|
| **What fixes \(A\)?** | Continuum/MS family \(A=1-r/X\) (or power \(p=1\)) | Composition \(x=X\tanh\phi\) + metric \(A=e^{-2\phi}\) | Same boost \(A(x)\) as H |
| **What fixes chart?** | Areal \(r\) is the wall chart | **J1:** \(r\equiv x\) | **P_ell:** \(x\equiv\ell=\int e^{\phi}dr\) |
| **Kinematic reach group** | **No** (not from \(\oplus\)) | **Yes** | **Yes** (on \(x\)) |
| **Free EOS** | No — Einstein reads \(\rho,p\) | No | No (if \(A(x)\) held) |
| **Scales** | one: wall \(X=r_{\max}\) | one: \(X=x_{\max}=r_{\max}\) | **two related:** composition \(X\), areal \(r_{\max}=X(\frac{\pi}{2}-1)\) |
| **\(M_{\mathrm{wall}}\)** | \(X/2\) | \(X/2\) | \(r_{\max}/2=\frac{X}{2}(\frac{\pi}{2}-1)\) |
| **\(\rho\)** | \(1/(4\pi X r)\) | \((2X+x)/(4\pi x(X+x)^2)\) | pullback of boost \(A\) onto areal \(r(\phi)\) |
| **\(p_r\)** | \(-\rho\) | \(-\rho\) | \(-\rho\) |
| **\(p_t/\rho\)** | **\(-\frac12\) constant** | \(-\frac{X^2}{(X+x)(2X+x)}\) varies | varies with depth |
| **\(d_L/X_{\mathrm{eff}}\)** | \(z(z+2)=(1+z)^2-1\) | \(u^2(u^2-1)/(u^2+1)\) | \(e^{2\phi}\,r(\phi)/X\) (integral) |
| **Low-\(z\)** | \(\sim 2X\,z\) (scale in \(X\)) | \(\sim X z+\frac32 X z^2\) | \(\sim X z + 1\cdot X z^2+\cdots\) (\(a_2/a_1\sim 1\)) |
| **Proper distance to wall** | \(2X\) (finite) | \(X(1+\pi/2)\) (finite) | wall is \(x\to X\) **by definition** of proper path |
| **Relational “wall always ahead at \(X\)”** | not from composition group | **yes** (composition) | **yes** on \(x\); areal map distorts |
| **SNe shape** | near | fail (stiff) | near–mid |

---

## 2. Candidate L — linear ceiling (deep properties)

### Geometry
\[
A=1-\frac{r}{X},\qquad
\phi=-\frac12\ln A=\frac12\ln\frac{X}{X-r},\qquad
1+z=\frac{1}{\sqrt{A}}=\sqrt{\frac{X}{X-r}}.
\]

### Continuum (Einstein on reciprocal metric)
\[
\rho=\frac{1}{4\pi X r},\qquad
p_r=-\rho,\qquad
p_t=-\frac12\rho.
\]

**Math note:** \(p_t/\rho=-\frac12\) is **constant** — simplest anisotropy in the power family \(A=1-(r/X)^p\) (there \(p_t/\rho=-p/2\); here \(p=1\)).

### Mass
\[
m=\frac{r^2}{2X}\to M=\frac{X}{2}.
\]
Critical closure at the wall — same identity as any \(A(X)=0\).

### Light (full, \(D_A=r\))
\[
\frac{r}{X}=1-\frac{1}{(1+z)^2},\qquad
\boxed{\frac{d_L}{X}=z(z+2)},\qquad
\frac{D_M}{X}=\frac{z(z+2)}{1+z}.
\]
Algebraically the **simplest** closed \(d_L(z)\) of the three.

### Provenance (updated — selection pass)
- **Unique** under continuum condition \(p_t=-\rho/2\) + regularity (\(C_1=0\)) + wall \(A(X)=0\) — `simple_metric_L_P_selection_derive_results.md`.  
- **Also kinematic:** chart \(r/X=1-e^{-2\phi}\) with associative \(\oplus\): \(r_1\oplus r_2=r_1+r_2-r_1 r_2/X\) (not Lorentz).  
- Old “\(p_r=0\) selects this” derivation remains **withdrawn** (scar).  
- Why **half** or why this chart vs \(\tanh\): still **OPEN**.

### Elegance type
**Continuum simplicity** *and* a **second composition geometry** (not the \(c\)-sibling Lorentz group).

---

## 3. Candidate H — hyp + J1 (why it fails as cosmology shape)

### Geometry
\[
x=X\tanh\phi,\quad
A=e^{-2\phi}=\frac{X-x}{X+x},\quad
r\equiv x\ \mathrm{(J1)}.
\]

### Continuum
\[
\rho=\frac{2X+x}{4\pi x(X+x)^2},\quad
p_r=-\rho,\quad
\frac{p_t}{\rho}=-\frac{X^2}{(X+x)(2X+x)}.
\]

### Light
\[
\frac{d_L}{X}=\frac{u^2(u^2-1)}{u^2+1},\quad u=1+z.
\]
Low-\(z\): \(z+\frac32 z^2+\cdots\) — \(a_2/a_1=1.5\) vs LCDM-like \(\sim 0.78\).

### Why SNe hate it (shape, not philosophy)
Distance ratios grow too fast: e.g. \(d_L(1)/d_L(0.1)\sim 20.9\) (hyp) vs \(\sim 14.3\) (linear/LCDM).  
Full light × tanh saturation is **stiff**.

### Elegance type
**Kinematic purity** (composition = \(c\)-sibling) + one scale under J1 — philosophically the “mantelpiece” stack; **empirically stiff** under current join+optics.

---

## 4. Candidate P — hyp + P_ell (why it helps)

### Split of duties
| Sector | Object |
|--------|--------|
| **Composition / reach** | \(x=X\tanh\phi\), bound \(X\) |
| **Rods** | \(x=\ell=\int_0^r e^{\phi}\,dr'\) |
| **Spheres / light** | still \(D_A=r\), \(d_L=(1+z)^2 r\) |

Inversion:
\[
\frac{\mathrm{d}r}{\mathrm{d}\phi}=X\,e^{-\phi}\mathrm{sech}^2\phi,
\quad
\frac{r_{\max}}{X}=\frac{\pi}{2}-1\approx 0.5708.
\]

### Mass lock
Wall in **areal** radius: \(A\to0\) as \(\phi\to\infty\), \(m\to r_{\max}/2\).  
Composition scale \(X\) and mass scale \(r_{\max}\) differ by a pure number — still **no free EOS**, but **two related rulers**.

### Light
\[
d_L=(1+z)^2 r(\phi),\quad \phi=\ln(1+z),\quad
\frac{r}{X}=\int_0^{\phi}e^{-\psi}\mathrm{sech}^2\psi\,\mathrm{d}\psi.
\]
No elementary closed form; well-defined 1D integral.  
SNe: χ²/dof≈1.02 — **hyp kinematics without J1’s over-join**.

### Elegance type
**Kinematic reach kept**; **J1 dropped**. Cost: closed-form \(d_L\) and single-scale identity \(M=X/2\) are lost; gain: rods own the composition chart.

### Sample map (how \(r\) lags \(x\))

| \(\phi\) | \(x/X\) | \(r/X\) | \(A=e^{-2\phi}\) |
|--------:|--------:|--------:|-----------------:|
| 0.1 | 0.100 | ~0.090 | 0.819 |
| 0.5 | 0.462 | ~0.352 | 0.368 |
| 1.0 | 0.762 | ~0.490 | 0.135 |
| 2.0 | 0.964 | ~0.554 | 0.018 |

Areal radius **lags** compositional depth → less aggressive \(d_L\) growth than H.

---

## 5. What they share (UDT spine)

All three (on E-room read of reciprocal metric):

1. Simple metric reciprocity \(A=e^{-2\phi}\)  
2. \(p_r=-\rho\) (identity)  
3. Full light, \(D_A=r\)  
4. Finite outer wall \(A\to0\) with critical areal mass \(m=r_{\mathrm{wall}}/2\)  
5. No free dark-fluid function \(w(z)\)

**Spine is shared. Branch is: what fixes \(A\), and which length is the composition chart.**

---

## 6. Zoom-out fork (where elegance can go next)

```
                    shared UDT spine
                           |
          +----------------+----------------+
          |                                 |
   fix A from KINEMATICS              fix A from CONTINUUM family
   (composition + bound X)            (e.g. power p, Einstein read)
          |                                 |
     join?                           p selected how?
     ├─ J1: H  — elegant, SNe fail         ├─ p=1: L — simple, SNe near
     └─ P_ell: P — SNe better              └─ p≠1: SNe die in scan
```

| Path | Need for elegance+fit |
|------|------------------------|
| **L wins** | Derive \(A=1-r/X\) (or \(p=1\)) without χ² and without false dust |
| **P wins** | Derive P_ell (rods = composition) and accept two related scales |
| **Hybrid** | Composition fixes something weaker than full \(A(x)\); continuum supplies the rest — only if native, not a fudge |
| **H as kinematics only** | Keep hyp as reach philosophy; don’t force J1 cosmology |

---

## 7. Property “beauty” scores (subjective, for ponder — not data)

| | L | H | P |
|--|:-:|:-:|:-:|
| Closed-form light | ★★★ | ★★★ | ★ |
| Composition/\(c\)-sibling | ★ | ★★★ | ★★★ |
| Single scale | ★★★ | ★★★ | ★★ |
| Continuum simplicity (\(p_t/\rho\)) | ★★★ | ★★ | ★★ |
| Relational group law | ★ | ★★★ | ★★★ |
| SNe shape | ★★★ | ★ | ★★ |

No row is a vote. It shows **tradeoffs**: L is algebraically dull and empirically good; H is philosophically sharp and empirically stiff; P is a compromise that **splits join from kinematics**.

---

## 8. One-line

**Promising candidates share reciprocal spine and critical walls; they split on whether \(A\) comes from composition (H/P) or continuum simplicity (L), and whether composition is areal (J1) or proper (P_ell) — SNe like L and P, not H; next is derive, not average them.**
