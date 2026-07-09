## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE / DERIVE (harder solution-space tiles) |
| **Frame** | residual spine + L working; angular-on; not easy tiles only |
| **Slice** | Einstein \(G^r{}_\theta\); local-room optical cavities; radial time-live on L; H optical |
| **Observing or targeting?** | OBSERVE what metric does — not BAO |
| **Build-on grade** | **LEAD** |
| **Re-run** | session → `simple_metric_hard_explore_out.json` |

### Premise ledger

| Item | Tag |
|------|-----|
| Reciprocal-\(\phi\) metric | THEORY slice |
| L background / local quartic interiors | WORKING / free explore interiors |
| Probe wave on fixed background | first-cut (radial waves) |
| Einstein \(G^r{}_\theta=0\) as vacuum constraint | geometric |

---

# Harder solution-space explores

Not the easy SNe/radial-only path. Four harder looks at what the metric does.

---

## HARD 1 — Angular residual is Einstein-constrained (exact)

On the reciprocal metric with \(\Phi(r,\theta)\), CAS gives the mixed Einstein component:

\[
G^{r}{}_{\theta}=e^{-2\Phi}\bigl(\partial_r\partial_\theta\Phi-2\,(\partial_r\Phi)(\partial_\theta\Phi)\bigr).
\]

**Vacuum constraint** \(G^{r}{}_{\theta}=0\):

\[
\partial_r\partial_\theta\Phi=2\,(\partial_r\Phi)(\partial_\theta\Phi)
\quad\Leftrightarrow\quad
\partial_r\bigl(e^{-2\Phi}\partial_\theta\Phi\bigr)=0
\quad\Leftrightarrow\quad
\partial_\theta\Phi=\frac{g(\theta)}{A}.
\]

Integrate:

\[
\boxed{A(r,\theta)=H(r)+G(\theta)}
\]

(with \(A=e^{-2\Phi}>0\)).

| Fact | Meaning |
|------|--------|
| Spherical L | \(G\equiv0\), \(H=1-r/X\) — allowed |
| Free multipoles of \(\Phi\) | **Not** free under Einstein; residual must be **additively separable** |
| Coupling | Geometric, exact, no hand coupling constant |

**Interesting:** Angular-on under Einstein is not “add \(Y_{\ell m}\) to \(\phi\) freely.”  
The residual itself must split as **radial piece + sky piece**. That is a strong native restriction.

(Probe \(\Box\) multipoles ignored this constraint — they were only a first listen.)

---

## HARD 2 — Local room vs filled cosmos for waves

| Room | Optical length | Proper length | Wave character |
|------|----------------|---------------|----------------|
| **Filled L wall** \(A\to0\) | \(\int\mathrm{d}r/A\to\infty\) | \(2X\) finite | Infinite optical throat; spectra densify |
| **Local quartic interior** to surface \(A(R)>0\) | **finite** (examples \(\sim 1.1\)–\(2.6\) for sample \(\alpha\)) | finite | **Finite optical cavity** possible |
| Exterior Schw \(r>R\), no horizon | \(\to\infty\) at spatial infinity | ∞ | Scattering continuum (ordinary GR) |

**Interesting:** Discrete residual “ringing” is **native to the local-mass room** (finite optical interior), **not** to the filled residual wall.  
Filled L can win SNe and mass lock and still be a bad finite drum for residual waves.  
That split is what the metric does — not a preference for easy tiles.

---

## HARD 3 — Radial time-live waves on L

Same densification as angular time-live: \(\ell=0\) towers under cutoff track \(\sim\pi/L_{\mathrm{opt}}(\varepsilon)\).  

**Angular is not the special villain.**  
**Residual death \(A\to0\)** makes the filled cosmos optically infinite for *any* residual wave (radial or angular).

---

## HARD 4 — H wall

H also has \(A\to0\) at finite \(r\) with \(\int\mathrm{d}r/A\to\infty\).  
Optical infinity is a **filled residual-wall** property, not L-only.

---

## Synthesis (non-easy conclusions)

1. **Einstein angular constraint is hard and clean:** \(A=H(r)+G(\theta)\) for vacuum mixed component. Multipole cosmetics on \(\phi\) are the wrong free data.  

2. **Filled residual cosmos:** good for one-scale distances/mass; **bad** as a finite optical cavity for residual oscillations (infinite throat).  

3. **Local residual stars:** finite optical interiors — natural arena for **discrete residual spectra** (still not imported BAO).  

4. **Easy vs hard diverge productively:** L radial cosmology can work while wave physics points at the **other room** or at **non-wall** boundary laws — that is solution-space information, not a contradiction to paper over.

---

## Path implications

| Direction | Why |
|-----------|-----|
| Explore **\(A=H(r)+G(\theta)\)** family under residual spine | Forced by Einstein \(G^r{}_\theta=0\) |
| Local-room residual eigenmodes (finite \(L_{\mathrm{opt}}\)) | Hard wave physics where discreteness can live |
| Multi-probe L distances | Still open; easy but on-line |
| Do not force BAO onto filled L wall cavity | Metric said no to robust finite tower |

---

## One-line

**Harder explores: Einstein forces residual \(A=H(r)+G(\theta)\) when angles turn on; filled residual walls are infinite optical throats for waves (radial or angular); finite residual cavities live in the local-mass room — the metric splits cosmology-scale L from discrete-wave arenas.**
