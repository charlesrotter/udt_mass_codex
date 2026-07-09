## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | MAP / OBSERVE |
| **Slice scope** | D_A=r, r→X as z→∞, full light; N=1580 full cov; shape = 1 offset only |
| **Observing or targeting?** | OBSERVE alternatives — **χ² does not promote a law to theory** |
| **Comparator scaffolds** | LCDM Om=0.3 residual reference only |
| **Verifier status** | SELF-SCRIPT (inline characterize 2026-07-09) |
| **Build-on grade** | **LEAD** |
| **Re-run commands** | re-run characterize block in session / extend later to `simple_metric_J1_alt_ceiling.py` |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| Charles J1 intuition | x_max = sphere-size ceiling | CHOSE | Y |
| Full light | d_L=(1+z)² D_A | DERIVED | Y |
| Hyp tanh + φ_metric | current package | POSTULATE composition | Y as baseline |
| A=1−r/X family | alternate approach to r→X | CHOSE explore profiles | Y as contrast only |

### What is NOT claimed

- That A=1−r/X is the correct UDT law (even if residual looks good).
- That we may switch laws because χ² improved (imposition).

### Do not build on

- Adopting B/C as foundation without native FE/metric derive.

---

# Can “x_max = sphere size” be derived differently?

## Your concern (fair)

Under **current** package:

- J1: \(D_A = r = x\)
- hyperbolic: \(x = X\tanh\phi\), \(1+z=e^{\phi}\)
- full light: \(d_L=(1+z)^2 x\)

the **shape** \(d_L(z)/X\) is **completely fixed**. Only overall scale is free.  
R2 baseline χ²/dof ≈ **2.17** is therefore **as good as that specific derivation gets** — not “we haven’t optimized yet.”

You can accept “a bit under LCDM.” **~2.2 vs ~0.88 is too far** for a flagship distance law. Agreed as a **hygiene/program** judgment (not “must win χ²”).

---

## Two different ideas people merge

| Idea | Meaning |
|------|---------|
| **Sphere-size ceiling** | There is a max areal radius \(X\); \(D_A=r\to X\) as stretch → ∞ (your decades intuition) |
| **Hyperbolic composition** | Displacements compose with bound \(X\) like velocities with \(c\) ⇒ **unique** \(x=X\tanh\phi\) if rapidity = metric \(\phi\) |

The **current package glues them together**: composition bound **and** sphere ceiling **and** \(\phi=\mathrm{arctanh}(r/X)\).

They can be **separated**:

> **Keep:** max sphere size \(X\), \(D_A=r\), full light, \(r\to X\) as \(z\to\infty\).  
> **Drop (for explore):** forcing \(\phi=\mathrm{arctanh}(r/X)\) from the velocity-addition analogy.

Then how you **approach** the ceiling is a **different derivation** (lapse \(A(r)\), FE, junction, …) — not a free SNe fit function.

---

## Characterize: same ceiling, different approach laws

All below: **\(D_A=r\)**, **full light**, **\(r\to X\) as \(z\to\infty\)**, scale free (1 offset).  
**Not** half light. **Not** free \(D_A(r)\).

| Law | How \(r(z)\) arises | χ²/dof | RMS | mean res \(z>0.6\) |
|-----|---------------------|-------:|----:|-------------------:|
| **A. Hyp tanh (current)** | \(\phi=\mathrm{arctanh}(r/X)\), \(1+z=e^{\phi}\) | **2.17** | 0.307 | −0.60 |
| **B. \(A=1-r/X\)** | \(\phi=-\frac12\ln A\), \(1+z=1/\sqrt{A}\) ⇒ \(r/X=1-1/(1+z)^2\), \(d_L/X=(1+z)^2-1\) | **0.91** | 0.158 | −0.02 |
| **C. \(A=(1-r/X)^2\)** | \(r/X=1-1/(1+z)\), \(d_L/X=(1+z)^2-(1+z)\) | **1.29** | 0.218 | −0.38 |
| LCDM ref | scaffold | 0.88 | 0.154 | −0.04 |
| Hyp **half** light | forbidden method | 1.19 | 0.196 | +0.29 |

### Low-\(z\) feel (series)

| Law | \(d_L/X\) |
|-----|-----------|
| Hyp tanh | \(z + 1.5 z^2 + \cdots\) |
| \(A=1-r/X\) | \(2z + z^2\) |
| \(A=(1-r/X)^2\) | \(z + z^2\) |

(Overall scale absorbed by offset; **shape** of higher orders + mid/high \(z\) matters.)

### Structural note

Whenever \(D_A\to X\) and full light holds, **far** asymptotic is always of order \(d_L \sim X(1+z)^2\).  
The **mid-path** (how fast \(D_A\) rises toward \(X\)) is what changes residuals a lot — hyp tanh rises in a way that is **harsh** under full light; linear lapse \(A=1-r/X\) is much gentler on the data **in this characterize pass**.

---

## Direct answers

### 1. Is 2.17 as good as J1 + **hyperbolic tanh** gets?

**Yes.** No hidden shape dial left in that package.

### 2. Is 2.17 as good as “\(x_{\max}\) = sphere size” can ever get?

**No.** That intuition only requires a **sphere ceiling** \(D_A=r\le X\), \(r\to X\) at infinite stretch.  
It does **not** require the **tanh composition** law. Other native \(A(r)\) / \(\phi(r)\) approaching the same ceiling change \(r(z)\) a lot (table above).

### 3. Different **derivation** (not fit) — what would count?

| Allowed | Not allowed |
|---------|-------------|
| Derive \(A(r)\) or \(\phi(r)\) from metric FE / geometric condition with edge at \(r=X\) | Fit free \(\phi(r)\) or free \(D_A(r)\) to SNe |
| Keep full light + \(D_A=r\) + ceiling \(X\) | Return to half light to rescue tanh |
| K-A / MS / horizon-style conditions as **mine** (Principle 4/7 care) | χ² upgrades CHOSE→DERIVED |

**Lead (not theory):** \(A=1-r/X\) is the Schwarzschild-like “lapse dies at finite areal radius” family already in the K-A trail — residual ~**0.91** under full light is a **strong invitation to re-derive from that geometric edge**, not to “adopt because Pantheon likes it.”

---

## Program split (clean)

```text
Package 1 — Hyperbolic COMPOSITION (like c for displacements)
  unique tanh law if rapidity = metric φ
  + J1 ⇒ locked shape ⇒ residual ~2.17 under full light
  Status: elegant; SNe-harsh under full light

Package 2 — Sphere-size CEILING X (your long intuition)
  D_A = r → X, full light
  approach law φ(r) or A(r) from metric/FE (open)
  Status: same intuition about X; room for better r(z) without fitting
  Lead: A=1−r/X class (~0.91 characterize) needs native derive
```

You can keep **“\(X\) is max sphere size”** and still ask for a **different derivation of the approach**, without abandoning J1’s spirit (sphere label = the distance that hits the ceiling).

---

## One-line

**Tanh+J1+full light is stuck at ~2.17; “x_max = sphere size” is not stuck there if the approach to the ceiling is derived differently (e.g. geometric A→0 at r=X) — characterize shows A=1−r/X ~0.91, which is a lead for derivation, not a licensed fit.**
