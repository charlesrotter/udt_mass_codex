# K-A continued — exotic outer branch + sourced lapse

**Date:** 2026-07-08 · **Mode: OBSERVE**  
**Prior:** `simple_metric_KA_develop.md`  
**Metric:** simple only. **Status:** PROVISIONAL.

---

## 1. Einstein components on the simple metric (CAS)

With \(A=e^{-2\phi}\) and \(g_{rr}=1/A\), \(g_{tt}=-A c^2\):

\[
G^{t}{}_{t} = \frac{A + r A' - 1}{r^2}
= -\frac{1}{r^2}\frac{d}{dr}\bigl[r(1-A)\bigr]
\]

\[
G_{\theta\theta} = \frac12 r^2\, \Delta A
\quad\Rightarrow\quad
G_{\theta\theta}=0 \Leftrightarrow \Delta A=0.
\]

**Misner–Sharp mass** (standard form, geometric on this metric):

\[
m(r) = \frac{c^2 r}{2G}\bigl(1-A(r)\bigr)
\quad\Leftrightarrow\quad
A = 1 - \frac{2Gm}{c^2 r}.
\]

Then

\[
G^{t}{}_{t} = -\frac{2G}{c^2 r^2}\frac{dm}{dr}
\quad\text{(up to \(c\)-factor bookkeeping in \(T\))}
\]

so **\(dm/dr=0\)** in vacuum ⇔ \(A=1+C/r\) (after residual \(\phi\)-shift sets the constant term to 1).

---

## 2. Full vacuum vs \(G_{\theta\theta}=0\) only

| Condition | Solution for \(A\) |
|-----------|-------------------|
| \(G^{t}{}_{t}=0\) (and then \(G_{\theta\theta}=0\) auto for this ansatz) | \(A=1+C/r\) |
| \(G_{\theta\theta}=0\) only (\(\Delta A=0\)) | \(A=C_0+C_1/r\) (includes \(C_0\neq 1\)) |

**Schw exterior (physical vacuum):** \(A=1-r_s/r\), \(m=\mathrm{const}=c^2 r_s/(2G)\).  
**K-A as full vacuum** = that family (not the exotic \(C_0\neq 1\) without stress).

---

## 3. Exotic outer branch \(C_0<0\)

### Form

\[
A = -\alpha + \frac{\beta}{r}, \quad \alpha>0,\ \beta>0,
\quad
r_{\mathrm{out}} = \frac{\beta}{\alpha},
\quad
A>0 \ \text{for}\ 0 < r < r_{\mathrm{out}}.
\]

As \(r\to r_{\mathrm{out}}^-\): \(A\to 0^+\), \(\phi\to+\infty\) — **outer** infinite-redshift surface.

### Not full vacuum

\[
G^{t}{}_{t} = \frac{-\alpha-1}{r^2} \neq 0.
\]

So this is **not** empty K-A vacuum; it requires a **distributed source** with

\[
G^{t}{}_{t} \propto -\frac{\alpha+1}{r^2}
\]

(everywhere in the chart) — **not** a compact ball. Exotic as a “whole-space” stress, not a star exterior.

### Proper distance to outer edge

Numeric (\(\alpha=1,\beta=2\Rightarrow r_{\mathrm{out}}=2\)): \(\ell\) to \(r_{\mathrm{out}}-\varepsilon\) **stays finite** as \(\varepsilon\to 0\) (same class as Schw horizon, not K-UW log wall).

### Verdict

| Claim | Status |
|-------|--------|
| Outer \(\phi\to\infty\) at finite \(r\) on simple metric | **Possible** as a profile |
| As K-A **vacuum** | **No** (\(G^{t}{}_{t}\neq 0\)) |
| As cosmology without weird infinite-extent source | **Poor** |
| Inspiration | Outer edge needs **sourced** equations, not vacuum \(\Delta A=0\) alone with \(C_0<0\) |

**Exotic vacuum outer edge: closed as a dead end for pure vacuum.** Outer \(c\)-edge ⇒ **matter / nontrivial \(T_{\mu\nu}\).**

---

## 4. Sourced K-A (matter) — geometric skeleton

Keep simple metric. Einstein (GR form as **reference structure** on this metric; \(G,c\) enter as constants):

\[
G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}.
\]

### Angular equation (generalizes \(\Delta A=0\))

\[
G_{\theta\theta} = \frac{8\pi G}{c^4} T_{\theta\theta}
\quad\Rightarrow\quad
\frac12 r^2 \Delta A = \frac{8\pi G}{c^4} T_{\theta\theta}.
\]

Vacuum: \(T_{\theta\theta}=0\Rightarrow\Delta A=0\) (K-A).  
With pressure / anisotropic stress, **\(\Delta A\) is sourced** — \(A\) need not be Coulomb.

### Energy equation (mass function)

\[
G^{t}{}_{t} = \frac{8\pi G}{c^4} T^{t}{}_{t}
\quad\Rightarrow\quad
\frac{d m}{dr} = 4\pi r^2 \rho_{\mathrm{eff}}
\]

(with \(\rho_{\mathrm{eff}}\) identified from \(T^{t}{}_{t}\) in the static frame — standard MS).

**Static dust** (reference continuum, not φ-blind action paste):

- \(T^{t}{}_{t} = -\rho c^2\) (sign convention as in GR dust),  
- \(T_{\theta\theta}=0\) if isotropic pressureless in orthonormal frame carefully reduced — **actually** dust has \(T_{\hat t\hat t}=\rho c^2\), spatial stresses 0 in rest frame; curved-component bookkeeping must be done carefully for EL vs Einstein.

**Geometric content without fixing dust details:**

1. **Vacuum exterior:** \(m=\mathrm{const}\), \(A=1-r_s/r\), horizon if \(r_s>0\).  
2. **Interior:** \(m'(r)=4\pi r^2\rho\), \(A=1-2Gm/(c^2 r)\).  
3. **Matching:** standard junction at star surface → exterior Schw.  
4. **Outer cosmic edge** (\(A\to 0\) at large \(r\)): needs \(2Gm(r)/(c^2 r)\to 1\) at finite \(r\), i.e. **\(m(r)\) grow so the compactness hits unity** — a **critical / whole-universe** type condition (closure), not vacuum Coulomb.

That last point reconnects corpus **critical universe / Misner–Sharp marginal** without free \(D_A\):  
**edge when \(A\to 0\)**, with \(A=1-2Gm/(c^2 r)\) from the metric identity under K-A + energy equation.

---

## 5. Dilated continuum vs Einstein dust (honest split)

| Coupling | Role |
|----------|------|
| Earlier \(L_m=-\rho r^2 e^{-2\phi}\) | Variational source for **φ-kinetic** packages; **SQ**; gave finite \(\phi_\infty\) |
| Einstein \(G_{\mu\nu}\propto T_{\mu\nu}\) on simple metric | Geometric **constraint on \(A(\phi)\)**; vacuum ⇒ K-A Schw; matter ⇒ MS mass |

These are **not automatically the same principle**.  
Under the K-A lean (curvature/Einstein components on the simple metric), the **consistent** continuum is **stress-energy sourcing Einstein**, not the old SQ kinetic dust as the primary exterior engine.

**Tag:** continuum microphysics (S² channels, etc.) still open; macro continuum **at least** must specify \(T_{\mu\nu}\) on this metric.

---

## 6. Synthesis with \(c\)-analogy

| Setup | \(c\)-like edge? | Where? |
|-------|------------------|--------|
| K-A vacuum Schw | **Yes** (horizon) | **Inner** (mass) |
| K-A exotic \(C_0<0\) vacuum | Profile yes; stress required | Outer chart zero — **not vacuum** |
| K-A + MS matter, compactness → 1 | **Possible outer** \(A\to 0\) | **Whole** if \(2Gm/c^2r\to 1\) at finite \(r\) |
| Old SQ φ-kinetic dust | No | Finite \(\phi_\infty\) |

**Working picture (provisional):**

1. **Simple metric** held.  
2. **Vacuum:** K-A ⇒ Schwarzschild exterior (horizon = local \(c\)-edge around mass).  
3. **Cosmic outer edge:** not vacuum; **sourced** MS compactness approaching 1 (critical universe) — amount of matter **selected by closure**, scale \(\sim GM/c^2\), no hand \(x_{\max}\).  
4. K-R1 remains the shift-pure alternative if horizon is rejected as macro.

---

## 7. Premise ledger

| Item | Tag |
|------|-----|
| \(G^{t}{}_{t}=(A+rA'-1)/r^2\) | DERIVED (CAS) |
| MS \(m\propto r(1-A)\) | DERIVED geometric identity on this metric |
| Full vacuum \(A=1-r_s/r\) | DERIVED from \(G^{t}{}_{t}=0\) |
| Exotic outer as vacuum | **Ruled out** |
| Outer edge via \(2Gm/c^2r\to 1\) | Geometric possibility; existence needs matter model |
| \(G,c\) in Einstein constant | Standard; mass from solution |

---

## Plain summary

The weird “outer horizon with negative constant in \(A\)” is **not empty space** — it needs stress everywhere, so we drop it as vacuum.  

Empty K-A space is **Schwarzschild**: a horizon around a mass (local \(c\)-like edge).  

A **far** edge on the same laws would mean matter fills space until compactness hits the wall (\(A\to 0\)) — the old **critical universe / MS** idea, now tied cleanly to the simple metric and K-A, without free \(D_A\) or a hand-set max distance.

**Next:** MAP a static MS continuum (dust or simple fluid) on the simple metric for **closure** \(A\to 0\) at finite \(r\), or stop for ponder.
