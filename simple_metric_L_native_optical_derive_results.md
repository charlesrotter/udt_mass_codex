## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE |
| **Frame** | dotted line; L working winner (mass lock + SNe); nativeness path |
| **Slice** | force L embedding from optical-depth principle on reciprocal metric |
| **Observing or targeting?** | DERIVE uniqueness of \(r/X=1-A\) under a **named** principle — not χ² |
| **Build-on grade** | **LEAD / CONDITIONAL** on principle P-opt below |
| **Re-run** | `python3 simple_metric_L_native_optical_derive.py` |

### Premise ledger

| Item | Tag | Chose or derived? |
|------|-----|-------------------|
| Reciprocal simple metric | THEORY | derived from R1–R3 frame |
| \(A=e^{-2\phi}\) | THEORY | identity on metric |
| Fermat optical radial \(\mathrm{d}\ell_{\mathrm{opt}}=\mathrm{d}r/A\) | THEORY (static optical geometry on this metric) | derived |
| **P-opt:** \(\mathrm{d}\ell_{\mathrm{opt}}=\kappa\,\mathrm{d}\phi\) (const \(\kappa\)) | **WORKING PRINCIPLE** | **named — not yet reduced further** |
| Wall / bound \(X=\kappa/2\) | from P-opt + \(\phi\to\infty\) | derived |
| Einstein continuum readout | E-room working | GR-form lean |
| Full light | DERIVED | optics |
| Mass lock \(M=X/2\) | DERIVED under L | identity |
| SNe | character only | clue, not used in derive |

### What is NOT claimed

- P-opt is Charles-canon.  
- No other native route exists.  
- SNe prove P-opt.

---

# Path: native L (or something extremely close)

## Charles’s read (accepted as path)

**L** (\(r/X=1-A\)) is the joint winner largely because **mass lock and \(x_{\max}\) are the same scale** — fundamental to the residual picture.  

**Next job:** show L is **native**, or find a **near-native** neighbor.  
Not: reopen fluid menus.

---

## Native route found: optical depth = place depth

### Principle (P-opt)

On the static reciprocal metric, light’s radial Fermat measure is
\[
\mathrm{d}\ell_{\mathrm{opt}}=\frac{\mathrm{d}r}{A}.
\]

**P-opt:** optical radial advance is proportional to dilation-depth advance:
\[
\boxed{\frac{\mathrm{d}r}{A}=\kappa\,\mathrm{d}\phi}
\quad(\kappa=\mathrm{const}>0).
\]

**Slogan (lay):** *as you go deeper in place, light’s optical path meters that depth evenly — one tick of depth, one tick of optical path.*

### Derivation (unique L)

\[
A=e^{-2\phi}
\quad\Rightarrow\quad
\mathrm{d}r=\kappa\,e^{-2\phi}\,\mathrm{d}\phi.
\]

Integrate from the observer \(\phi=0\), \(r=0\):
\[
r(\phi)=\kappa\int_0^{\phi}e^{-2\psi}\,\mathrm{d}\psi=\frac{\kappa}{2}\bigl(1-e^{-2\phi}\bigr)=\frac{\kappa}{2}\bigl(1-A\bigr).
\]

Identify the bound
\[
X:=\frac{\kappa}{2}
\quad\bigl(r\to X\ \mathrm{as}\ \phi\to\infty\bigr).
\]

\[
\boxed{\frac{r}{X}=1-A}.
\]

**That is L.** No free function left.

### H fails P-opt

For \(r=X\tanh\phi\),
\[
\frac{\mathrm{d}r}{A\,\mathrm{d}\phi}=X\,e^{2\phi}\mathrm{sech}^2\phi
\]
**not constant.** H is incompatible with P-opt.

### Package that falls out with L

| Piece | Status under P-opt + spine |
|-------|----------------------------|
| \(A=1-r/X\) | **forced** |
| \(1+z=1/\sqrt{A}\) | metric |
| \(d_L/X=z(z+2)\) | full light + L |
| \(\rho=1/(4\pi X r)\), \(p_r=-\rho\), \(p_t=-\rho/2\) | Einstein readout |
| \(M=X/2\) | mass lock = same \(X\) as optical bound |
| Composition \(A_1 A_2=A_{12}\); chart ⊕ | residual product / L⊕ |
| SNe shape | already near (clue, not used here) |

---

## Why this is “native enough” to work with (tagged)

| Strength | Caveat |
|----------|--------|
| Uses only metric + optical geometry + one principle | P-opt is still a **principle**, not reduced to pure R1–R3 |
| Uniquely forces L (not a fit) | Another principle might force H (e.g. pure rapidity chart) |
| Ties light and place (elegant for UDT) | Optical geometry is static GR-corpus standard — allowed mine, applied natively here |
| Mass lock and \(x_{\max}\) coincide automatically | — |

**Working status:** P-opt is the **best native door we have** for L.  
Elevate or replace only with something stricter that still recovers L (or a neighbor as good on mass lock + SNe).

---

## Alternate native-ish doors (same target L)

| Principle | Result |
|-----------|--------|
| \(p_t=-\rho/2\) + reg + wall | unique \(A=1-r/X\) (continuum face) |
| Chart \(r/X=1-A\) (“room left \(=XA\)”) | defines L |
| P-opt (this tile) | **derives** chart from light+depth |

P-opt is preferred as **primary** because it motivates the chart from **light ↔ place**, not from a stress ratio slogan alone. Continuum half-ratio then **follows**.

---

## Something “very close” if P-opt is rejected

If P-opt is too strong, near-L charts (e.g. \(F=\phi/(1+\phi)\)) are SNe-adjacent but:

- **break** single-scale mass lock elegance, or  
- lack a clean optical identity, or  
- reintroduce free shape.

**Bar for “very close”:** must keep **one \(X\)** with \(M=X/2\) and residual spine, and stay SNe-near without free functions.  
So far **exact L** is the only named law that clears that bar cleanly. Neighbors are not free upgrades.

---

## Path forward (locked)

1. **Hold L + P-opt as working native package** (tagged).  
2. Stress-test P-opt (relational observers, multi-probe character, dynamics later).  
3. Seek **stricter** derivation of P-opt from positional dilation alone — or a replacement principle with same L output.  
4. Do **not** drift back to H as cosmology paint without new evidence; keep H as \(c\)-reference.  
5. Do **not** χ²-shop near-L free functions.

---

## One-line

**Charles’s path is right: L wins on mass lock + SNe; nativeness via “optical path meters dilation depth” forces \(r/X=1-A\) uniquely on the reciprocal metric — working native L, principle P-opt still the hinge to harden.**
