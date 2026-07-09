# P3 asymptotics — vacuum \(W=1\), \(D=r\)

**Date:** 2026-07-08 · **Mode: OBSERVE (analytic + bounded numeric).**  
**Equation:** \(Z\,(r^2\phi')' = 4 e^{-2\phi}\)  
**Frame:** `UDT_ELEGANT_FRAME.md` · **MAP:** `macro_sector_MAP.md`  
**Script / data:** `macro_sector_P3_asymptotics.py`, `macro_sector_P3_asymptotics_data.json`  
**Status:** PROVISIONAL. Completes vacuum scoreboard row P3.

---

## Premise ledger

| Item | Tag |
|------|-----|
| Packaging P3: uncompensated \(\mathcal{K}\), areal gauge \(D=r\) | FREE specialization of native skeleton |
| \(Z=1\) representative | FREE overall scale |
| Observer sample chart: \(r_0=1\), \(\phi=0\) | FREE chart placement |
| Observing or targeting? | **Observing** asymptotics, not fitting sky |

---

## Exact structure

### Flux monotonicity

\[
Q(r) := r^2 \phi' , \qquad Q' = \frac{4}{Z} e^{-2\phi} > 0
\]

**\(Q\) is strictly increasing** wherever the solution exists.  
Numeric: \(\min \Delta Q > 0\) on sample paths.

**Consequences:**

- No static \(\phi=\mathrm{const}\) solution (would need \(Q'=0\)).  
- If \(Q\) becomes positive, it stays positive and \(\phi\) is eventually increasing.  
- Negative initial \(Q\) can cross through zero (φ has a minimum) then rise.

### Log coordinate

With \(s=\ln r\):

\[
Z\bigl(\partial_{ss}\phi + \partial_s\phi\bigr) = 4 e^{-2\phi}
\]

Friction \(\partial_s\phi\) + force \(\propto e^{-2\phi}\); no elementary first integral found.

---

## Numeric large-\(r\) behavior (outward)

From \(r=1\), \(\phi=0\), wide range of \(\phi'(1)\), out to \(r=100\)–\(500\):

| Feature | Observation |
|---------|-------------|
| \(\phi(r)\) | **Increases** then flattens toward a **finite** plateau \(\phi_\infty\sim 2.4\)–\(3\) (depends weakly on start) |
| \(\phi'\) | \(\to 0^+\) |
| Late shape | Quasi-Coulomb: \(\phi \approx \phi_\infty - Q/r\) with \(Q\) slowly growing (fit residual \(\sim 10^{-2}\) on \(r\in[50,200]\)) |
| Proper \(\ell=\int e^\phi dr\) | **Grows without bound** as \(r_{\max}\) increases (e.g. \(u_0=0.5\): \(\ell(10)\sim47\), \(\ell(500)\sim6\times10^3\)) |
| Null \(\int e^{2\phi}dr\) | Likewise **diverges** with \(r_{\max}\) |

**Why plateau-ish:** as \(\phi\) rises, \(e^{-2\phi}\) kills the source \(Q'\); \(Q\) almost freezes; motion looks like Laplace/Coulomb, which approaches finite \(\phi_\infty\). Strictly \(Q'\) never zero, so \(\phi_\infty\) is approached but the true mathematical \(\infty\) limit may still creep — **practically and for barrier integrals, reach is open.**

---

## Elegant-criterion score (P3)

| Criterion | Result |
|-----------|--------|
| Redshift looking out (\(\phi\) increases with \(r\)) | **YES** (from sample observer at \(r=1\), \(\phi=0\)) |
| Hard dilation barrier (\(\ell<\infty\) or \(z\to\infty\) at finite reach) | **FAIL** — \(\ell\to\infty\), \(z\to e^{\phi_\infty}-1\) **finite** |
| No preferred-center ontology | **Weak** — gauge \(D=r\) + inward runs hit **φ blowup as \(r\to0\)** (polar singularity); usable only as **observer chart**, not “center of universe” |
| Full elegant macro pass | **FAIL** |

---

## Inward (toward \(r\to0\))

Integrating inward: \(\phi\) runs to **large positive** (hit cap 40) at small \(r\).  
So this gauge naturally has a **deeply dilated singular origin** — consistent with old “Branch P finite-domain / no smooth center” lore, **scoped** to \(D=r\) + this EL.

Not a large-\(r\) edge; a **center** pathology in this chart.

---

## Updated vacuum scoreboard

| ID | Packaging | Macro elegant test |
|----|-----------|-------------------|
| P0 | compensated free \(D\) | FAIL barrier (open, φ→const or weak log) |
| P2 | compensated \(D=r\) Coulomb | FAIL barrier |
| P1 soft | uncompensated free \(D\) | proper barrier, **wrong** redshift direction |
| P1 hard | uncompensated free \(D\) | pinch bag, not large-r edge |
| **P3** | uncompensated \(D=r\) | **redshift out YES; hard barrier FAIL; singular origin** |

**All pure-vacuum rows on the native skeleton, as scored, fail the full elegant macro test.**

---

## What this does *not* say

- Not “positional dilation is wrong.” Metric redshift law is untouched.  
- Not “add an edge mechanism.”  
- Not “matter is proven required” — only that **these vacuum packages don’t complete the macro edge story**. Next is still **metric-led**: free-\(D\) + uncompensated with **redshift-out** class; or **same-action** continuum matter asymptotics — without inventing terms.

---

## Next (still simple)

1. **PONDER (recommended):** vacuum alone, on the written native packages, does not hand a hard far-reach dilation barrier with cosmological look-out. What remains **inside** the skeleton: free \(D\) + \(W=1\) aimed at **φ increasing** + convergent reach (if any class exists); or **matter** as already present in the action form \(L_m\), asymptotics only.  
2. **Optional analytic:** prove \(\phi\to\phi_\infty<\infty\) vs \(\phi\to+\infty\) rigorously for P3.  
3. **Not next:** SNe, BB, seed zoo, new edge field.

---

## Plain summary

The “angular sources φ with spheres size = chart radius” vacuum equation **does** make dilation **increase as you look out**, then **levels off** — like coasting toward a finite depth, not an infinite cliff. You can still walk forever in proper distance; redshift maxes out. Toward the chart origin, φ blows up.  

So P3 is **not** the completed elegant edge. It is a clear, honest piece of what the vacuum metric-operator does.
