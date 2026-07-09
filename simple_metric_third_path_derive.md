# Why both kinetics work — and a third law from the metric

**Date:** 2026-07-08 · **Mode: DERIVE / OBSERVE** (simple metric only).  
**Guides:** K-R1 and K-UW as geometric poles; \(c\)-analogy.  
**CAS:** Einstein \(G_{\theta\theta}\), flat Laplacians, residuals.  
**Status:** PROVISIONAL synthesis — not Charles canon. No free \(D_A\). No hand \(x_{\max}\).

---

## 1. The question

We have two vacuum engines on the same metric:

| | **K-R1** | **K-UW** |
|--|----------|----------|
| Kinetic | \(\sqrt{-g}\,e^{2\phi}g^{rr}(\phi')^2\) | \(\sqrt{-g}\,g^{rr}(\phi')^2\) |
| EL | \((r^2\phi')'=0\) | \(\Box_g\phi+e^{-2\phi}(\phi')^2=0\) |
| Solution | \(\phi=\phi_\infty-q/r\) | \(e^{-\phi}=C_0+C_1/r\) |
| Strength | bulk shift-clean | \(c\)-like horizon |

**Ask:** Why does each “work”? Can the metric force a **third** law that uses both as guides?

---

## 2. Why each works (geometric meaning)

### Shared arena

\[
ds^2 = -e^{-2\phi}c^2\,dt^2 + e^{2\phi}\,dr^2 + r^2\,d\Omega^2.
\]

Natural **metric scalars** (areal chart \(r\)):

| Symbol | Meaning | Relation |
|--------|---------|----------|
| \(\phi\) | dilation potential | R1 additive depth |
| \(\psi=e^{-\phi}\) | **clock-rate factor** \(\sqrt{-g_{tt}}/c\) | |
| \(A=e^{-2\phi}\) | **lapse** \(-g_{tt}/c^2\) | \(A=\psi^2\) |

Flat radial Laplacian on areal \(\mathbb{R}^3\):

\[
\Delta f = \frac1{r^2}\partial_r\bigl(r^2 f'\bigr).
\]

Harmonic functions with spherical symmetry: \(f=C_0+C_1/r\).

### K-R1 — “\(\phi\) is Coulomb”

\[
(r^2\phi')'=0 \quad\Longleftrightarrow\quad \Delta\phi = 0
\quad\text{(same as flat Laplace on \(\phi\))}.
\]

**Why it works:** treats **depth \(\phi\)** as the object that should be source-free / harmonic in the areal chart; matches **R1** (only \(\phi'\) in bulk kinetic after reciprocal cancellation); probe = self-consistent.

**Why it fails \(c\)-edge:** harmonic \(\phi\) is smooth for \(r>0\); \(\phi\to\phi_\infty\) at infinity; no finite-\(r\) blowup.

### K-UW — “clock rate \(\psi\) is Coulomb”

Solution \(e^{-\phi}=C_0+C_1/r\) means:

\[
\Delta\psi = 0, \qquad \psi=e^{-\phi}.
\]

**Why it works:** \(\psi\) is the **physical clock factor** in the metric; requiring it to be areal-harmonic is a clean geometric condition. The UW kinetic EL is exactly the variational form that produces \(\Delta\psi=0\) (CAS: EL residual 0 on this family).

**Why it is \(c\)-like:** if \(C_0+C_1/r_*=0\) with \(r_*>0\), then \(\psi\to 0\), \(\phi\to+\infty\), \(A\to 0\), proper distance to \(r_*\) **diverges** — horizon.

**Why it was demoted:** bulk kinetic depends on bare \(\phi\) (shift **not** a symmetry of the action).

---

## 3. Third path — “lapse \(A\) is Coulomb” (from the Einstein tensor)

### Computation (CAS)

On the simple metric, the Einstein tensor angular component satisfies:

\[
G_{\theta\theta} = \frac12\, r^2\, \Delta\!\left(e^{-2\phi}\right)
\quad\text{(up to the exact factor verified: } G_{\theta\theta}/(r^2\Delta A)=\tfrac12\text{)}.
\]

Therefore:

\[
\boxed{G_{\theta\theta}=0 \quad\Longleftrightarrow\quad \Delta A=0 \quad\Longleftrightarrow\quad A=e^{-2\phi}=C_0+\frac{C_1}{r}}.
\]

### Solution (third vacuum)

\[
e^{-2\phi} = C_0 + \frac{C_1}{r}
\quad\Rightarrow\quad
\phi = -\frac12\ln\Bigl(C_0+\frac{C_1}{r}\Bigr)
\quad (C_0+C_1/r>0).
\]

Schwarzschild-like branch: \(C_0=1\), \(C_1=-r_s\):

\[
e^{-2\phi} = 1-\frac{r_s}{r},
\quad
\phi = -\frac12\ln\bigl(1-r_s/r\bigr)\ \ (r>r_s).
\]

As \(r\to r_s^+\): \(\phi\to+\infty\), \(g_{tt}\to 0\), \(\int e^{\phi}\,dr\) **diverges** (same \(c\)-like unattainability as K-UW horizon).

### Why this is a real third geometric law

| Object set to harmonic \(\Delta f=0\) | Law | Name |
|--------------------------------------|-----|------|
| \(f=\phi\) | \((r^2\phi')'=0\) | **K-R1** |
| \(f=e^{-\phi}\) | UW vacuum | **K-UW** |
| \(f=e^{-2\phi}=A\) | \(G_{\theta\theta}=0\) | **K-A (third)** |

All three are: **“this metric scalar is source-free Coulomb in areal \(\mathbb{R}^3\).”**  
They differ only in **which scalar**.

### Relation to “vacuum = GR” scar

- Full **EH bulk action** on this family is a **pure boundary term** ⇒ bulk \(\delta S_{\mathrm{EH}}/\delta\phi\equiv 0\) (no EL).  
- Imposing \(G_{\theta\theta}=0\) is **not** “EH bulk extremization” (that is empty).  
- It **is** a geometric condition: **angular Einstein equation on the constrained simple metric**, which CAS reduces to \(\Delta A=0\).

**Tag carefully:**

| Claim | Tag |
|-------|-----|
| \(G_{\theta\theta}\propto\Delta A\) on this metric | **DERIVED (CAS)** |
| \(G_{\theta\theta}=0\) as *the* UDT vacuum law | **CHOSE / GR-component principle** — geometric guide, not forced by EH bulk |
| Matches known Schwarzschild-limit lore in corpus | Consilience with `udt_canonical_geometry.md` (vacuum \(v=e^{-2\phi}\) Laplace) |

So K-A is **derived as an identity + optional vacuum condition**, not smuggled as “full GR.” It is the natural third in the harmonic-scalar triangle.

---

## 4. Triple comparison (guides)

| | **K-R1** (\(\Delta\phi=0\)) | **K-UW** (\(\Delta\psi=0\)) | **K-A** (\(\Delta A=0\)) |
|--|---------------------------|---------------------------|-------------------------|
| Scalar | depth \(\phi\) | clock \(\psi=e^{-\phi}\) | lapse \(A=e^{-2\phi}\) |
| Bulk shift of action | exact (kinetic) | broken | N/A (constraint, not that kinetic) |
| Weak field | \(\phi\sim q/r\) | \(\phi\sim q/r\) | \(\phi\sim r_s/(2r)\) |
| \(c\)-horizon \(A\to0\) finite \(r\) | **No** | **Yes** (\(\psi=0\)) | **Yes** (\(A=0\)) |
| Linear match to Schwarzschild \(A\) | only \(O(1/r)\) after exp | no | **exact** \(A=1-r_s/r\) branch |
| xmax boost \(A=(X-x)/(X+x)\) | no | no | no (still different) |

**Why both original kinetics “work”:** each is harmonic Coulomb for a different metric scalar.  
**Third:** do the same for the **lapse** \(A\) — the component that multiplies \(-c^2 dt^2\).

---

## 5. Preferring among them (analysis, not decree)

| If you prioritize… | Lean |
|--------------------|------|
| Exact bulk \(\phi\)-shift (R1 on action) | **K-R1** |
| Clock-rate harmonic + \(c\)-horizon | **K-UW** |
| Lapse harmonic + GR-limit + \(c\)-horizon | **K-A** |
| “Primary metric function is \(g_{tt}\)” | **K-A** strongest |
| “Primary is additive depth \(\phi\)” | **K-R1** |
| “Primary is clock factor \(\psi\)” | **K-UW** |

**For Charles’s \(c\)-analogy (approach infinite dilation / unattainable edge):**  
**K-UW and K-A both work; K-R1 does not.**

**Between K-UW and K-A:**

- K-A hits the **standard Schwarzschild lapse** exactly (strong GR-limit consilience on this family).  
- K-UW hits \(\psi=0\) when \(A=\psi^2=0\) same horizon set, but \(A=(C_0+C_1/r)^2\) is a **double root** structure (extremal-like), not \(1-r_s/r\).  
- K-A is tied to **\(G_{\theta\theta}=0\)**, a tensor component of the metric’s curvature — not a kinetic-weight ambiguity.

**Working recommendation (provisional):**  
Treat **K-A** as the best **third path** for a simple-metric vacuum that is both **geometric** and **\(c\)-capable**, with K-R1/K-UW as the other two corners of the same harmonic triangle.  
**Do not** pretend EH bulk selected it (scar); **do** state \(G_{\theta\theta}=0\) / \(\Delta A=0\) as the **chosen geometric vacuum condition** on this family, pending Charles.  

**Developed:** `simple_metric_KA_develop.md` (Schw branch = standard horizon; proper distance to horizon finite; outer infinity flat; exotic outer \(C_0<0\) open).

---

## 6. What this does *not* do

- Does not reintroduce free \(D_A\).  
- Does not postulate \(x_{\max}\); \(r_s\) or \(r_*\) remain solution constants (mass scale).  
- Does not restore SQ \(\mathcal{K}\) as exterior engine.  
- Does not close multi-observer relational edge.  
- Does not claim K-A is Charles-canon.

---

## 7. Equations to carry forward (simple metric vacuum)

\[
\begin{align*}
\text{K-R1:}&\quad (r^2\phi')'=0,\\
\text{K-UW:}&\quad \Delta(e^{-\phi})=0,\\
\text{K-A:}&\quad \Delta(e^{-2\phi})=0\quad\bigl(\Leftrightarrow G_{\theta\theta}=0\text{ on this metric}\bigr).
\end{align*}
\]

Horizon branches (K-UW / K-A): finite \(r_*\), \(\phi\to+\infty\), \(\ell\to\infty\).

---

## Plain summary

Both old kinetics work because each says “make **this** metric quantity look like a point charge in ordinary space”: either the depth \(\phi\), or the clock rate \(e^{-\phi}\).  

A third, equally geometric choice is the **lapse** \(e^{-2\phi}\) — and that is exactly what the angular Einstein equation requires on your simple metric. That third law gives the familiar **Schwarzschild-like** hole where dilation runs to infinity at finite radius and you never arrive — the \(c\)-like edge — without free \(D_A\) and without hand-built walls.

**Recommendation:** for a \(c\)-like macro vacuum on the simple metric, **prefer K-A** (lapse harmonic / \(G_{\theta\theta}=0\)) as the leading third path; keep K-R1 as the shift-pure alternative; keep K-UW as the clock-harmonic alternative. Next step if you agree: develop K-A solution space + relational reading only.
