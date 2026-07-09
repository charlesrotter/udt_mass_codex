# Hyperbolic distance law — derivation from metric + dilation composition

**Date:** 2026-07-08 · **Mode: DERIVE (thin, elegant).**  
**Aim:** Get \(x = x_{\max}\tanh\phi\) (and cascade) with every premise tagged.  
**CAS:** `derive_xmax_boost.py` + session checks (all composition / rapidity identities TRUE).  
**Status:** PROVISIONAL. Form derived under named premises; **value** of \(x_{\max}\) not fixed here.  
**Not:** free \(D_A\), SQ bulk EL, hand numerical \(x_{\max}\), BB.

---

## 0. Target (elegance)

\[
\boxed{x = x_{\max}\,\tanh\phi
\qquad\Leftrightarrow\qquad
\phi = \mathrm{arctanh}\!\left(\frac{x}{x_{\max}}\right)}
\]

- **Limit of a distance** \(x_{\max}\), not a place on a map  
- Always the **far** end of reach: \(x\to x_{\max}^-\) as \(\phi\to+\infty\), never crossed  
- Pairs with redshift \(1+z=e^{\phi}\) (observer at \(\phi=0\))

---

## 1. What the **metric alone** already gives

Simple UDT metric:

\[
ds^2 = -e^{-2\phi}\,c^2\,dt^2 + e^{2\phi}\,dr^2 + r^2\,d\Omega^2.
\]

| Fact | Status |
|------|--------|
| Lapse \(A \equiv -g_{tt}/c^2 = e^{-2\phi}\) | **Identity** on this metric |
| \(g_{rr} = e^{2\phi} = 1/A\) | **Identity** (reciprocity) |
| Static redshift \(1+z = e^{\Delta\phi}\) | **Derived** from \(g_{tt}\) ratios |
| \(\phi\) additive under composition of dilations | **From R1–R2** (metric founding): dilations compose → exponential; depth \(\phi\) **adds** |

**Honest limit:** the metric **does not** by itself name a coordinate \(x\) and force \(\phi=\mathrm{arctanh}(x/x_{\max})\).  
It **does** force: once you have a distance coordinate \(x\) tied to depth by the boost law below, the **lapse and redshift cascade** (steps 4–5).

So: **metric + dilation composition supply the skeleton; one structural premise supplies the bound.**

---

## 2. Premise ledger (chose vs derived)

| # | Item | Tag |
|---|------|-----|
| P0 | Simple metric + R1–R3 (incl. reciprocal \(A\cdot g_{rr}=1\)) | THEORY |
| P1 | No preferred position; isotropic radial displacements form a **group** | THEORY / analogy to SR relativity principle for **position** |
| P2 | Displacement maps are **fractional-linear** (linear fractional) in a chart \(x\) | **NAMED** (same class as von Ignatowsky / 1D isotropic homogeneous); not free chaos of laws |
| P3 | There exists a **finite** invariant distance bound \(X=x_{\max}\) (fixed point of composition) | **POSTULATE** — twin of “finite \(c\)” vs Galilean \(\infty\); **not** derived from \(c,G\) alone |
| P4 | Chart \(x\) is the **distance-like** radial label for that composition (not areal \(r\) a priori) | NAMED identification |
| D1–D5 | Composition law, rapidity \(\phi\), saturation, redshift–distance, \(A(x)\) | **DERIVED** (CAS) |

**Without P3:** composition can be Galilean \(x_1+x_2\) (\(X\to\infty\)) — no hyperbolic saturation.  
**P3 is the physics choice**, as “light speed is finite” is for SR — not a mechanism term in a Lagrangian.

---

## 3. Derivation chain (CAS-checked)

### Step 1 — Composition law (from P1–P3 + P2)

Unique isotropic associative law with identity \(0\), inverses, and fixed point \(X\):

\[
\boxed{
x_1 \oplus x_2 = \frac{x_1+x_2}{1+x_1 x_2/X^2}
}
\]

- \(x\oplus X = X\) (nothing exceeds \(X\))  
- \(X\to\infty\) ⇒ \(x_1+x_2\) (naive addition)

### Step 2 — Additive depth = metric \(\phi\)

The map that **linearizes** \(\oplus\) is rapidity:

\[
\boxed{\phi = \mathrm{arctanh}\frac{x}{X}}
\quad\Rightarrow\quad
\phi(x_1\oplus x_2)=\phi(x_1)+\phi(x_2).
\]

**Why this \(\phi\) is the metric’s \(\phi\):**  
R1–R2 already make dilation depth **additive** under composition of dilations.  
Identifying that additive parameter with the metric field \(\phi\) is the **native join** (same role as rapidity vs velocity in SR).

### Step 3 — Hyperbolic saturation (the function you asked for)

\[
\boxed{x = X\tanh\phi}
\]

- \(\phi:0\to+\infty\) maps \(x:0\to X\) **asymptotically**  
- \(dx/d\phi = X\,\mathrm{sech}^2\phi \to 0\) as \(\phi\to\infty\) (distance saturates; bound stays **farther**, never a place you occupy as \(x=X\))

### Step 4 — Redshift–distance (cascade from metric redshift)

Metric: \(1+z=e^{\phi}\) (observer at \(\phi=0\)).  
With step 2–3:

\[
\boxed{1+z = \sqrt{\dfrac{X+x}{X-x}}}
\]

(\(u=x/X\): \(e^{\mathrm{arctanh}\,u}=\sqrt{(1+u)/(1-u)}\) — CAS derivative identity).

- \(x\to X\): \(z\to\infty\)  
- small \(x\): \(1+z \approx 1 + x/X\)

### Step 5 — Lapse on the simple metric (cascade)

On the simple metric, \(A=e^{-2\phi}\) and static \(1+z=e^{\phi}=1/\sqrt{A}\) (observer at \(\phi=0\), source at \(\phi\)).  
Hence:

\[
\boxed{A(x)=\frac{X-x}{X+x}}
\quad\Rightarrow\quad
A\to 0 \ \text{as}\ x\to X
\]

(\(g_{tt}\to 0\): time stops at the distance bound — horizon **in the distance chart**, not “a preferred town” in space.)

Consistency check: \(\phi=\mathrm{arctanh}(x/X)\) ⇒ \(e^{-2\phi}=(X-x)/(X+x)=A\). **Matches.**

---

## 4. What “from the metric” means here (precise)

| Derived **using** the metric | Not from metric line element alone |
|------------------------------|-------------------------------------|
| \(A=e^{-2\phi}\), \(g_{rr}=1/A\) | Finite \(X\) (P3) |
| \(1+z=e^{\phi}\) | That the radial **distance** chart is the \(x\) of the group law (P4) |
| Join additive rapidity ↔ metric \(\phi\) (R1–R2) | Value of \(X\) in meters |

**One sentence:**  
The metric gives the **dilation and redshift skeleton**; the hyperbolic map is what you get when **positional composition** has a **finite distance invariant**, the same way Lorentz velocity addition is what you get when composition has a finite speed invariant.

---

## 5. Cascade “the rest falls into place” (what follows, what doesn’t)

| Cascades immediately | Still open |
|----------------------|------------|
| \(x=X\tanh\phi\) | Dynamics: *why* a solution realizes this \(x(\phi)\) globally |
| \(1+z=\sqrt{(X+x)/(X-x)}\) | Relation of \(x\) to areal \(r\) (gauge / solution) |
| \(A=(X-x)/(X+x)\) on simple metric | \(X \leftrightarrow M_{\mathrm{tot}}\) via \(G,c\) (closure / pure number) |
| \(c\)-like: bound is **distance**, always farther | Absolute meters from \(c,G\) only (impossible without mass scale in the pair) |

**Mass cascade (your conjecture, not derived here):**  
If closure forces \(X = k\, GM_{\mathrm{tot}}/c^2\) with pure \(k\), then \(M_{\mathrm{tot}}\) and \(X\) lock; ratios can be fixed without free cosmological knobs. That is **next**, not this form derivation.

---

## 6. Contrast with field-equation shortlist (do not confuse)

| Vacuum law | Profile | Hyperbolic reach? |
|------------|---------|-------------------|
| K-R1 \(\Delta\phi=0\) | \(\phi\sim q/r\) | **No** |
| K-UW \(\Delta e^{-\phi}=0\) | \(e^{-\phi}=C_0+C_1/r\) | Horizon in **areal** \(r\), not same as \(X\tanh\phi\) |
| K-A \(\Delta A=0\) | \(A=1-r_s/r\) | Horizon **place** in areal \(r\) (mass); not distance-saturation law |
| **This derive** | \(\phi=\mathrm{arctanh}(x/X)\) | **Yes** — limit of **distance** \(x\) |

Hyperbolic reach is a **kinematic / compositional** law for **distance vs depth**.  
K-A is a **curvature** vacuum for **areal** chart.  
They can later **agree in a gauge** or stay dual descriptions — not forced identical in this note.

---

## 7. One-line result

**Given the simple metric’s dilation/redshift structure and a finite invariant maximum distance for positional composition, the hyperbolic law \(x=x_{\max}\tanh\phi\) (and \(A=(x_{\max}-x)/(x_{\max}+x)\), \(1+z=\sqrt{(x_{\max}+x)/(x_{\max}-x)}\)) is derived; \(x_{\max}\) remains the free ruler until mass/closure locks it.**

---

## Plain summary

The metric already knows exponential redshift and an additive depth \(\phi\).  
If **how far** you can go has a finite bound — the twin of “how fast” has bound \(c\) — then math forces the **hyperbolic** link between depth and distance, same family as SR rapidity.  
Nothing about a special place: the bound is **how far**, always the far end of the scale.  
Value of that bound waits on mass/closure; the **function** is what cascades the rest of the kinematic sky.
