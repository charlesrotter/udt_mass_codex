## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE |
| **Focus** | Kaleidoscope K2–K3 on residual L (inter-frame appearance) |
| **Build-on grade** | **LEAD** (structure observed; not yet blind-verified banked) |
| **Machine** | `simple_metric_kaleidoscope_K2_out.json` |

# K2 — What residual place does to appearance between seats

**Binding:** same geometry; seats differ → observations transform. Not “physics changes with \(r\).”

**Package:** residual L, \(A=1-r/X\) in a global chart; stationary redshift \(1+z=\sqrt{A_o/A_s}\); proper radial \(dl=dr/\sqrt{A}\); Etherington \(d_L=(1+z)^2 D_A\).

---

## ★ Interesting structure (report to Charles)

### 1. Local “Hubble” is seat-dependent — pure residual

Near any seat, redshift rises with proper distance as
\[
H_{\mathrm{loc}}=\frac{1}{2X\sqrt{A_o}}\,.
\]
Center (\(A_o=1\)): \(H=1/(2X)\).  
At \(A_o=1/4\) (\(r_o=0.75X\)): \(H\) is **twice** the center value.

Same universe. Deeper residual seat → steeper local stretch of \(z\) vs proper distance. That is kaleidoscope, not a different local law.

### 2. Identity: wall is always one “Hubble length” away

On L, proper distance from seat \(o\) to the wall is \(2X\sqrt{A_o}\). Therefore
\[
\boxed{H_{\mathrm{loc}}\times(\text{proper remaining to wall})=1}
\]
**at every seat.**

Lay: wherever you sit, your local redshift gradient times how much proper room is left to the wall is exactly one. The wall is always “one local Hubble-length” of proper residual away — relational, no preferred center.

### 2b. ★ This identity *characterizes* L (not a coincidence)

General residual \(A(r)\) with a wall \(A(X)=0\): local gradient is
\[
H_{\mathrm{loc}}=-\frac{A'}{2\sqrt{A}}=-\frac{d\sqrt{A}}{dr}\,.
\]
Requiring \(H_{\mathrm{loc}}\times L_{\mathrm{remain}}(r)=1\) **at every seat** forces the ODE
\[
u\,u''+(u')^2=0\quad(u=\sqrt{A})\quad\Rightarrow\quad A=\alpha+\beta r
\]
i.e. **linear residual**. With \(A(0)=1\) and wall \(A(X)=0\):
\[
A=1-\frac{r}{X}\quad\text{(exactly L).}
\]
Hyperbolic paint \(A=(X-r)/(X+r)\) and quadratic \(A=1-(r/X)^2\) **fail** the identity (product seat-dependent, ≠1).

**Kaleidoscope meaning:** “every seat sees the wall one local Hubble-length away” is not a generic residual fact — it **selects L** among residual paints. L is the residual map with a universal seat–wall Hubble ruler.

### 3. Off-center eye: angular diameter from residual

Small stick, observer not at center, nearly radial line of sight (null geodesic, small impact parameter):
\[
D_A=\frac{r_s-r_o}{\sqrt{A_o}}\,.
\]
Flat limit \(A_o\to1\): \(D_A\to r_s-r_o\) (chord). Residual at the **observer** rescales the angle: \(\alpha\sim\sqrt{A_o}\). Numeric match to the formula at the \(10^{-5}\) level in the scan.

So two seats looking at the **same** stick disagree on angle not only from geometry of place, but from each seat’s residual depth in the angle measure.

### 4. Fixed ruler: radial vs transverse stretch grows with depth

Center seat, fixed proper sticks (radial and transverse). Diagnostic
\[
\frac{\Delta z/\theta}{H_0\,r_s}
\]
runs \(\sim 1.1\to 10\) from \(r_s=0.1X\) to \(0.9X\) (using center \(H_0=1/(2X)\)).  
Radial redshift span of a stick outruns the naive \(H_0\times\)angle conversion more and more toward the wall — pure residual AP-style distortion (no fluid, no sound horizon).

### 5. Mild sky residual \(A=H(r)+G(\theta)\) (K3 peek)

With \(H=1-r/X\) and small \(G=\varepsilon P_2(\cos\theta)\):

- On a fixed areal sphere \(r_s\), **\(z\) depends on direction** (same place on the sphere, different residual along different rays).
- Half-amplitude grows toward the wall (at \(\varepsilon=0.05\), \(r_s=0.85X\): \(z_{\max}/z_{\min}\sim 1.4\)).
- Wall itself deforms: \(r_{\mathrm{wall}}(\theta)/X=1+G(\theta)\) (not round).

Visual anisotropy without a new force — residual sky only. (MS mass for non-spherical \(A\) is **not** the spherical formula; continuum costs angle-dependent stress — side note, not imposed away.)

---

## K4 sketch (character only)

From one seat (center), one residual coordinate \(\xi=r/X\) locks:

| Readout | Form on L |
|---------|-----------|
| \(1+z\) | \(1/\sqrt{1-\xi}\) |
| \(D_A\) | \(r=X\xi\) |
| \(d_L\) | \(X\,z(z+2)\) |
| stick angle | \(\ell/r\) |
| \(H_{\mathrm{loc}}\) (center) | \(1/(2X)\) |

SNe / angular-size / “local H” are **different instruments on the same inter-frame map**, not separate mechanisms. Multi-probe work = read the same kaleidoscope several ways.

---

## Premise ledger

| Item | Tag |
|------|-----|
| Residual L \(A=1-r/X\) | WORKING paint |
| Stationary \(1+z=\sqrt{A_o/A_s}\) | THEORY (static reciprocal metric) |
| \(D_A=r\) at center | THEORY (areal spheres) |
| Off-center \(D_A=(r_s-r_o)/\sqrt{A_o}\) | DERIVED small-angle / leading impact parameter |
| \(G(\theta)\) amplitude \(\varepsilon\) | FREE (observe family) |
| Observing or targeting? | OBSERVE appearance maps |

---

## Scope / not claimed

- Not a Pantheon refit; not BAO fluid.  
- Off-center \(D_A\) is leading small-angle (exact integral for large impact still open).  
- \(H_{\mathrm{loc}}\times L_{\mathrm{remain}}=1\) for all seats **characterizes** linear residual (= L under \(A(0)=1\), wall at \(X\)).  
- Composition: \(1+z\) multiplies along seat chains (exact). Finite-stick \(D_A\) tracks small-angle formula to \(\sim 1\%\) at \(\ell\sim 0.2X\).  
- LEAD, not banked verdict.

---

## One-line

**“Wall = one local Hubble-length from every seat” characterizes residual L; local \(H\), angles, and ruler stretch are inter-frame maps — kaleidoscope, not local law change.**
