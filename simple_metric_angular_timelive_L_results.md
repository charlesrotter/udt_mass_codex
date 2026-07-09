## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE |
| **Frame** | angular-on; time-live multipoles; L residual background |
| **Slice** | probe wave operator for residual depth on \(A=1-r/X\); multipoles \(Y_{\ell m}\) |
| **Observing or targeting?** | OBSERVE spectrum character — not targeting BAO peak |
| **Build-on grade** | **LEAD** (scoped; probe operator + wall cutoff) |
| **Re-run** | `python3 simple_metric_angular_timelive_L.py` |

### Premise ledger

| Item | Tag |
|------|-----|
| Background L | WORKING |
| Wave eq. for probe \(\phi\) on fixed L metric | first-cut operator (not full Einstein backreaction) |
| BC: regular origin + \(u\to0\) near wall | CHOSE quiet-wall / Dirichlet proxy |
| Wall cutoff \(\varepsilon\) | numeric necessity; continuum limit studied |

### What is NOT claimed

- Full GR perturbation spectrum.  
- BAO peak derived.  
- Discrete tower survives continuum wall limit.

---

# Time-live angular multipoles on L

Static multipoles were the wrong object for “oscillations.” This tile does **time dependence**.

## Operator (units \(X=1\), then restore)

Static metric coefficients of L. Scalar wave equation for residual-depth probe:

\[
-\frac{1}{A}\partial_{tt}\phi+\frac{1}{r^2}\partial_r(r^2 A\,\partial_r\phi)+\frac{1}{r^2}\nabla_{S^2}^2\phi=0.
\]

Ansatz \(\phi=e^{-i\omega t}u(r)Y_{\ell m}\):

\[
\bigl(r^2 A u'\bigr)'-\ell(\ell+1)u+\frac{\omega^2 r^2}{A}u=0.
\]

Scaling \(r=X\xi\), \(\Omega=\omega X\):

\[
\frac{\mathrm{d}}{\mathrm{d}\xi}\Bigl(\xi^2 A\frac{\mathrm{d}u}{\mathrm{d}\xi}\Bigr)-\ell(\ell+1)u+\Omega^2\frac{\xi^2}{A}u=0,
\quad A=1-\xi.
\]

---

## Results

### 1. Finite cutoff → discrete tower
With domain \(\xi\in[\varepsilon,1-\varepsilon]\) and Dirichlet at ends, FD eigenproblem yields a **positive discrete** \(\Omega_{n\ell}\) tower. Example \(\varepsilon=2\cdot10^{-3}\), \(N=500\):

| \(\ell\) | first \(\Omega\) values (approx) |
|--------:|----------------------------------|
| 1 | 0.61, 1.16, 1.68, 2.19, … |
| 2 | 0.75, 1.34, 1.88, … |
| 3 | 0.87, 1.48, 2.04, … |

Gaps \(\Delta\Omega\sim 0.5\) at that cutoff.

### 2. Scaling
\[
\omega_{\mathrm{phys}}=\frac{\Omega}{X}.
\]
Any true geometric frequency is set by the **reach scale** \(X\).

### 3. Continuum wall limit — the interesting point
Optical radial length on L:
\[
L_{\mathrm{opt}}=\int_0^{r}\frac{\mathrm{d}r'}{A}=-\,X\ln\Bigl(1-\frac{r}{X}\Bigr)\xrightarrow{r\to X}\infty.
\]
Proper length stays **finite**: \(\ell_{\mathrm{proper}}\to 2X\).

As wall cutoff \(\varepsilon\to0\), \(L_{\mathrm{opt}}=-\ln\varepsilon\to\infty\) and the numerical mean spacing tracks \(\sim\pi/L_{\mathrm{opt}}\) (within grid error at small \(\varepsilon\)):

| \(\varepsilon\) | mean \(\Delta\Omega\) (ℓ=1) | \(\pi/L_{\mathrm{opt}}\) |
|---------------:|----------------------------:|------------------------:|
| \(10^{-2}\) | 0.70 | 0.68 |
| \(10^{-3}\) | 0.47 | 0.45 |
| \(10^{-4}\) | 0.43 | 0.34 |
| \(10^{-5}\) | 0.42 | 0.27 |

(Small-\(\varepsilon\) mismatch is grid; trend is **densification**, not a stable finite gap.)

**Thus:** a clean, cutoff-independent discrete “cavity” spectrum with \(\Delta\omega\sim\mathrm{const}/X\) **does not survive** sending the quiet wall all the way to \(A=0\). The residual wall is an **infinite optical throat**.

---

## Interesting conclusion (lay + precise)

**Lay:**  
You can walk to the outer wall in **finite** proper distance (a finite cosmos in rods).  
But for **light-like residual waves**, the wall is as far as **infinite optical depth** — because residual clocks die and the optical measure is \(\mathrm{d}r/A\).  
So angular-time oscillations on L don’t live in a finite drum with neat overtones \(n\pi c/L\); they see a **bottomless optical well** at the wall. Artificial cutoffs invent fake discrete towers that **collapse into a continuum** as the wall is approached.

**Precise:**  
On L, finite proper size + **infinite** Fermat radial length to the residual wall ⇒ time-live multipole “eigenvalues” under wall Dirichlet densify as \(\varepsilon\to0\). Native oscillatory angular structure is **not** a robust finite geometric line spectrum from this BC alone.

**Ties to P-opt:** P-opt sets \(\mathrm{d}r/A=\kappa\mathrm{d}\phi\), and \(\phi\to\infty\) at the wall ⇒ optical path to the wall **diverges** — same fact, now in the wave spectrum.

**Scoped negatives / opens:**
- Not “no oscillations exist” (continuum / scattering / different BC remain).  
- Not BAO.  
- Full Einstein backreaction untested.  
- Finite spectrum might reappear with **different wall physics** (mirror before \(A=0\), dynamical wall, discrete residual, etc.) — only if **derived**, not fitted.

---

## One-line

**Time-live multipoles on L scale as \(1/X\), but because optical depth to the residual wall is infinite while proper size is finite, a quiet-wall discrete overtone tower densifies away — L is a finite proper cosmos and an infinite optical cavity for residual waves.**
