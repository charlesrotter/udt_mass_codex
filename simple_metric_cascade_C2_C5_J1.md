# ⚠ PRINCIPLE-7 / join note (2026-07-09)

Mass-lock faces that quote \(M\leftrightarrow X\) via Misner–Sharp \(2GM/c^2\) are **GR-form conditional** — see  
`simple_metric_mass_xmax_cascade.md` banner + `simple_metric_WR_L_external_triple_blind_audit_results.md`.  
Do not present as native UDT prediction. WR-L selects residual form \(A=1-r/X\), not this mass packaging.

---

# Cascade continue — J1 stress-test, relational (C2), n=2 optics sketch (C5)

**Date:** 2026-07-08 · **Mode: OBSERVE / MAP**  
**Prior:** `simple_metric_mass_xmax_cascade.md` (C3–C4 under J1)  
**Postulate:** `simple_metric_xmax_POSTULATE.md`  
**Status:** PROVISIONAL consilience tiles. No free \(D_A\). No Pantheon fit.

---

## 1. J1 stress-test (\(r \equiv x\)?)

### What J1 says

The compositional distance \(x\) in

\[
x = X\tanh\phi, \quad A=\frac{X-x}{X+x}
\]

is the **same** radial label as the **areal** coordinate \(r\) of the simple metric (area \(=4\pi r^2\)).

### Why J1 is almost forced on the live metric

Live simple metric:

\[
ds^2 = -A\,c^2 dt^2 + \frac{dr^2}{A} + r^2 d\Omega^2,
\quad A=e^{-2\phi}.
\]

- There is **one** radial chart \(r\).  
- Reciprocity already sets \(g_{rr}=1/A\).  
- Angular part fixes **areal** meaning of \(r\).

The hyperbolic derive introduces \(x\) as the chart in which displacements **compose** with bound \(X\).  
If that chart is **not** \(r\), we need a second radial function \(r(x)\) — i.e. a free transverse/areal profile vs compositional distance — which is exactly the **free \(D_A\)** direction we quarantined.

| Option | Meaning |
|--------|---------|
| **J1** | \(x=r\): one chart; mass lock \(X=2GM/c^2\) holds as written |
| **¬J1** | \(r=r(x)\): reopens free areal vs distance — quarantined unless reopened on purpose |

**Verdict (working):**  
On the **simple-metric-only** program, **J1 is the consistent default**, not an extra decoration.  
It is still **named** (compositional interpretation of the areal chart), but refusing it reopens the quarantined generality.

**Residual risk:** areal \(r\) may not be the best *operational* “distance” for composition (radar, luminosity, …). Then one defines operational \(x_{\mathrm{op}}(r)\) and rewrites the group law there — **later**, if data demand it. Not a free function of two variables like free \(D_A(r)\).

---

## 2. Relational reading (C2)

### Wanted

- No preferred cosmic **place**  
- Bound is a **distance** ahead of **you**  
- Same *kind* of law for every observer  

### Construction (kinematic)

1. Each observer sets \(\phi=0\) at their event (chart).  
2. \(X=x_{\max}\) is an **invariant** of the composition group (same for all, like \(c\)).  
3. In **their** distance chart, far reach is \(x\to X^-\), \(\phi\to+\infty\), always **farther**.  
4. Homogeneity of the far sky: compression \(dx/d\phi\to 0\) near the bound → thin high-\(z\) shell in every direction from that seat.

### What is **not** claimed

- That a single global SSS chart with one origin is the ontology of the universe.  
- That filled \(m(x)=c^2 x^2/(G(X+x))\) is how every observer labels mass without transformation.  

**C2 status:** **Structurally consistent** with the postulate + frame-relation spirit; **not** a multi-observer metric atlas derivation. Enough to keep “no preferred place” from contradicting the hyperbolic law.

| Item | Status |
|------|--------|
| C2 relational | **PASS (structural)** — detail atlas OWED if needed |

---

## 3. n=2 optics sketch (C5)

### Held optics (banked earlier)

\[
d_L = (1+z)^2 D_A
\]

(n=2 forced; n=1 Pantheon fit demoted.)

### Under J1 + hyperbolic

Areal diameter distance:

\[
D_A = r = x = X\tanh\phi = X\frac{(1+z)^2-1}{(1+z)^2+1}
\]

(with \(1+z=e^{\phi}\)).

Luminosity distance:

\[
\boxed{
d_L(z) = (1+z)^2 D_A
= X\,(1+z)^2\frac{(1+z)^2-1}{(1+z)^2+1}
}
\]

Equivalently \(d_L/X = (e_z^4 - e_z^2)/(e_z^2+1)\) with \(e_z=1+z\).

### Low \(z\)

\[
\frac{d_L}{X} = z + \frac32 z^2 + O(z^3)
\]

(CAS series).  
Leading behavior: \(z \approx x/X\) and \(d_L \approx x\) — the **single scale is \(x_{\max}=X\)** (restore \(c\) only when converting units of length/time). Scale language stays **native** (\(x_{\max}\), \(M_{\mathrm{tot}}\)) — not FLRW cosmology imports.

### What this is / is not

| Is | Is not |
|----|--------|
| Closed **form** prediction once \(X\) fixed | A Pantheon residual |
| n=2 + hyperbolic + J1 | Proof of fit quality |
| Scale dependent on \(X=2GM/c^2\) | Free \(w_0,w_a\) cosmology |

**C5 status:** **Form ready**; **numeric FAIL** — `simple_metric_pantheon_xmax_fit_results.md` (hyp RMS≈0.31 vs LCDM-ref≈0.15; high-\(z\) systematic).

---

## 4. Checklist update

| # | Item | Status |
|---|------|--------|
| C0–C1 | Hyperbolic + small-\(x\) | DONE |
| C3–C4 | \(X=2GM/c^2\), closure identity under J1 | DONE (conditional J1) |
| **J1** | \(r\equiv x\) | **DEFAULT under simple metric** (stress-tested) |
| **C2** | Relational | **PASS structural** |
| **C5** | n=2 \(d_L(z)\) form | **DONE form**; data check OWED |
| C6 | Local Schw vs filled hyperbolic | Distinguished (local hole vs whole) |
| Scale pin | One absolute ruler | OWED (not 1101 inside derivation) |

---

## 5. How we’re doing (cascade)

```text
Postulate x_max          ████████████  accepted
Hyperbolic form          ████████████  derived
J1 (r = x)               ████████░░░░  default on simple metric
Mass lock k=2            ████████████  under J1
Relational C2            ███████░░░░░  structural pass
n=2 d_L form             ████████░░░░  formula ready
SNe / CMB numbers        ██░░░░░░░░░░  not run (scale policy next)
```

---

## 6. Next options

1. **Pre-register** a single scale-pin policy in **native variables** (fix \(X=x_{\max}\), or one angular scale in terms of \(X\)) — **then** optional SNe residual under n=2 (no retune).  
2. **CMB depth** as downstream check (\(\phi\approx\ln(1101)\) ⇒ shell at \(x\approx X\)) — not foundation.  
3. **Stop and ponder** with Charles before any data.

---

## Plain summary

On the simple metric, treating compositional distance as the areal radius is the **honest default** (otherwise we reopen free size). Relationally, every observer can have the same kind of far **distance** bound ahead. With n=2, luminosity distance is a **closed formula** in \(z\) once \(x_{\max}\) is known:

\[
d_L = x_{\max}\,(1+z)^2\frac{(1+z)^2-1}{(1+z)^2+1}.
\]

Mass and \(x_{\max}\) already lock with factor 2. What’s left for “does it work on the sky?” is **one clean scale pin** and a **pre-registered** test — not more operators.
