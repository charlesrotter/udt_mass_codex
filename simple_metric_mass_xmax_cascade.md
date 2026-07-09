# Consilience cascade C3–C4 — mass–distance lock under hyperbolic reach

**Date:** 2026-07-08 · **Mode: DERIVE / MAP**  
**Postulate:** `simple_metric_xmax_POSTULATE.md` (Charles accepted, working)  
**Hyperbolic form:** `simple_metric_hyperbolic_derive.md`  
**Status:** PROVISIONAL cascade — pure-number lock under a **named join** of charts; not full SNe.

---

## 0. Goal

Lock

\[
x_{\max} \longleftrightarrow M_{\mathrm{tot}}
\]

through \(G,c\) and geometry, so the hyperbolic sky law has a **scale**, without fitting Pantheon first.

---

## 1. Held structure

\[
x = X\tanh\phi,
\quad
A = e^{-2\phi} = \frac{X-x}{X+x},
\quad
1+z = e^{\phi} = \sqrt{\frac{X+x}{X-x}}
\quad (X\equiv x_{\max}).
\]

Simple metric: \(A=e^{-2\phi}\), \(g_{rr}=1/A\).

---

## 2. Misner–Sharp mass on this metric (geometric)

For the simple UDT / reciprocal SSS form,

\[
m(r) = \frac{c^2 r}{2G}\bigl(1-A(r)\bigr)
\quad\Leftrightarrow\quad
A = 1 - \frac{2Gm}{c^2 r},
\]

with \(r\) the **areal** radius (area \(=4\pi r^2\)).

CAS: \(G^{t}{}_{t} = (A + r A' - 1)/r^2 = -\frac{1}{r^2}\frac{d}{dr}[r(1-A)]\),  
so \(m\propto r(1-A)\) is the standard integral of the energy equation.

---

## 3. Named join (load-bearing — chose or derived?)

**Join J1 (working hypothesis for this cascade):**  
In the macro distance chart of the postulate, identify

\[
\boxed{r \equiv x}
\]

i.e. the compositional distance coordinate **is** the areal radius for the purpose of MS + hyperbolic \(A(x)\).

| Tag | |
|-----|--|
| **J1** | **CHOSE / working join** — simplest consilience probe; not forced by R1–R3 alone |
| Alternative | \(r=r(x)\) nontrivial → mass lock formula changes; reopen if J1 fails consilience |

Under J1, hyperbolic \(A(x)\) is a profile on the **areal** chart.

---

## 4. Mass profile under hyperbolic \(A\) (DERIVED given J1)

\[
A(x)=\frac{X-x}{X+x}
\quad\Rightarrow\quad
1-A=\frac{2x}{X+x}
\]

\[
\boxed{
m(x)=\frac{c^2}{2G}\,x\,(1-A)
=\frac{c^2}{G}\frac{x^2}{X+x}
}
\]

(CAS: simplifies to \(c^2 x^2/(G(X+x))\).)

| Limit | \(m\) |
|-------|--------|
| \(x\to 0\) | \(m\to 0\) |
| \(x\to X^-\) | \(\boxed{m\to \dfrac{c^2 X}{2G}}\) |

Compactness:

\[
\frac{2Gm}{c^2 x}
= \frac{2x}{X+x}
\to 1
\quad\text{as}\quad x\to X.
\]

**Geometric meaning:** as the distance bound is neared, the universe is **marginally trapped** (\(A\to 0\), compactness → 1).  
That is the **closure** face of the same hyperbolic \(A\), not an extra wall.

---

## 5. Mass–distance lock (C3)

Identify

\[
M_{\mathrm{tot}}
:= \lim_{x\to X^-} m(x)
= \frac{c^2 X}{2G}.
\]

Then

\[
\boxed{
x_{\max} = X = \frac{2 G M_{\mathrm{tot}}}{c^2}
}
\]

i.e. pure number **\(k=2\)** in \(X = k\,GM_{\mathrm{tot}}/c^2\).

| Item | Tag |
|------|-----|
| \(k=2\) | **DERIVED** given hyperbolic \(A\), MS definition, join \(r=x\), \(M_{\mathrm{tot}}=\lim m\) |
| Absolute \(M_{\mathrm{tot}}\) or \(X\) in SI | **Not** fixed by \(c,G\) alone — one scale free until observation or further closure |
| Relation between \(M_{\mathrm{tot}}\) and \(X\) | **Fixed** |

This matches Charles’s intuition: **\(x_{\max}\) depends on total mass**; math gives the **factor 2** under J1, not a free fit.

---

## 6. What “closure” means here (C4)

Under this profile, **closure is not an extra equation**:

- Hyperbolic \(A\) already enforces \(A\to 0\) and \(2Gm/(c^2 x)\to 1\) at \(x\to X\).  
- Distributed mass \(m(x)=c^2 x^2/(G(X+x))\) is **required** by MS + hyperbolic \(A\) (not vacuum Schw, where \(m=\mathrm{const}\)).  
- Density from \(m'(x)\):

\[
m'(x)=\frac{c^2}{G}\frac{x(2X+x)}{(X+x)^2}
\quad\Rightarrow\quad
\rho_{\mathrm{MS}} \sim \frac{m'}{4\pi x^2}
=\frac{c^2}{4\pi G}\frac{2X+x}{x(X+x)^2}
\]

(Positive for \(x\in(0,X)\).)  
**Tag:** \(\rho_{\mathrm{MS}}\) is the density **implied by** the kinematic \(A(x)\) under MS — a **consilience check** against a micro continuum, not a free \(\rho(r)\) fit.

**Vacuum Schw** (\(m=\mathrm{const}\), \(A=1-r_s/x\)) is a **different** solution: local mass, outer flat — **not** the filled hyperbolic cosmos. Both can exist in the theory for different roles (local holes vs whole).

---

## 7. Scale dependence (SNe / CMB)

| Quantity | Depends on |
|----------|------------|
| \(z(x/X)\) | Dimensionless only |
| Physical \(x\), \(d_L\), low-\(z\) slope \(z\sim x/X\) | **\(X=x_{\max}\)** |
| \(M_{\mathrm{tot}}\) | \(M_{\mathrm{tot}}=c^2 X/(2G)\) once \(X\) known (or converse) |

So Charles is right: **fix the mass–\(x_{\max}\) lock (relation) before expecting the sky law to “just work” in Mpc.**  
One absolute calibration (e.g. low-\(z\) distance ladder, or a pre-registered depth+angular pin) still picks the ruler; the theory fixes **\(k=2\)** and the **shape**.

**1101:** pins \(\phi_{\mathrm{CMB}}\approx\ln(1101)\) if 3000 K story is used → \(x/X=\tanh\phi\approx 1\) → CMB shell **at** the bound in distance fraction — **depth** anchor, not a second free scale if \(X\) already set.

---

## 8. Consilience checklist update

| # | Item | Status |
|---|------|--------|
| C0 | Hyperbolic form + \(A(x)\) | DONE |
| C1 | Small-\(x\) linear \(z\approx x/X\) | DONE |
| **C3** | \(X=2GM_{\mathrm{tot}}/c^2\) under J1 + MS + lim \(m\) | **DONE (conditional on J1)** |
| **C4** | Closure \(A\to0\), compactness→1 at bound; filled \(m(x)\) | **DONE as identity of this profile** |
| C2 | Relational multi-observer | OWED |
| C5 | n=2 optics with this chart | OWED |
| C6 | Local Schw limit vs filled hyperbolic | Distinguished above — both geometric |
| J1 | \(r\equiv x\) | **CHOSE — critical** |

---

## 9. Risks (don’t hide)

1. **J1** may be wrong: if areal \(r\neq x\), \(k\) changes.  
2. Hyperbolic \(A(x)\) is **kinematic**; MS density is whatever that profile implies — microphysics may not match \(\rho_{\mathrm{MS}}\).  
3. SNe still unpaid until \(X\) calibrated without circular Pantheon tuning.  
4. Preferred-center: filled SSS chart is centered; relational rewrite still owed (C2).

---

## Plain summary

If the distance bound and the areal radius are the same chart, the hyperbolic lapse **forces** a mass that grows with distance and **hits critical compactness exactly at \(x_{\max}\)**, with

\[
x_{\max}=\frac{2GM_{\mathrm{tot}}}{c^2}.
\]

So mass and max distance lock with **pure factor 2** — the cascade you hoped for — under one clear join. Absolute size still needs one observational ruler; the **relation** is theory.

---

## Next

- Stress-test **J1** (must areal \(r\) be \(x\)?)  
- Or C2 relational / C5 n=2 optics sketch  
- Or pre-register a **single** scale pin (not 1101 in the derivation) for a future SNe test  
