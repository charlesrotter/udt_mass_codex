# Near-miss operator explore (repo + git history + re-probe)


## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit / original work date may differ) |
| **Mode** | OBSERVE |
| **Slice scope** | see body — retrofit default LEAD |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | see body |
| **Verifier status** | SELF-SCRIPT or NONE — see body; not blind-pass unless stated |
| **Build-on grade** | **LEAD** |
| **Re-run commands** | see body / associated `*.py` if any |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| See body of this document | full ledger in sections | mixed — re-read body | Y |

### What is NOT claimed

- Physics canon (Charles only). Hygiene grade ≠ nature proof.
- Claims wider than **Slice scope** above.

### Do not build on (if any)

- Anything tagged CHOSE/explore in the body without re-stating premises.

---

**Date:** 2026-07-08 · **Mode: OBSERVE / inspiration**  
**Scope:** Simple metric arena; \(c\)-analogy test; **no** free \(D_A\); **no** hand \(x_{\max}\) as live FE.  
**Prior:** `simple_metric_operator_inspiration_SEARCH.md`  
**Status:** PROVISIONAL exploration log.

---

## 1. Git history timeline (relevant commits)

| Commit | Date-ish (message) | Content |
|--------|--------------------|---------|
| `f766478` | Native FE two-player | Simple metric; \(\Box_g\phi\); **R1-weighted** \((r^2\phi')'=0\); **unweighted** \(\Box\phi+e^{-2\phi}(\phi')^2=0\Rightarrow e^{-\phi}=C_0+C_1/r\); G/P \(\mathcal{K}\) fork |
| `af286a6` | Native geometric action | \(R^{(2)}+W\mathcal{K}\); hardens SQ \(e^{-2\phi}\) path |
| `4a4f00b` / `867ead9` | \(x_{\max}\) frame + derive | Dilation boost: \(\phi=\mathrm{arctanh}(x/X)\), \(A=(X-x)/(X+x)\) |
| `5ecc901` | Strip H₀ from \(x_{\max}\) | \(X\) not from \(c,G\) alone |
| `28bf314` / `4940daf` | Reframe / archive | \(x_{\max}\) as invariant **distance** demoted; keep \(\phi\to\infty\) edge idea + frame-relation |
| `0742063` | Cosine ≠ two-player | Vacuum two-player **no** finite \(\phi\to\infty\) edge; edge **matter-sourced** (scoped) |
| `3dc5f84` etc. | Branch P / X-continuation | Pre-native \(X=-2e5\) etc. — contaminated era |

**Lesson from history:** the project **already found** (i) a kinematic \(c\)-twin and (ii) a vacuum with finite-\(r\) lapse zero, then **moved** to R1-weighted geometric action that **self-quenches** — good for purity, bad for \(c\)-edge.

---

## 2. Re-probe: unweighted vacuum (★ near-miss)

### Equation (simple metric)

\[
\Box_g\phi + e^{-2\phi}(\phi')^2 = 0,
\qquad
\Box_g\phi = \frac1{r^2}\partial_r\bigl(r^2 e^{-2\phi}\phi'\bigr).
\]

**Exact solution (CAS residual 0):**

\[
e^{-\phi} = C_0 + \frac{C_1}{r}
\quad\Rightarrow\quad
A \equiv e^{-2\phi} = \left(C_0+\frac{C_1}{r}\right)^2,
\quad
g_{tt} = -c^2 A.
\]

### \(c\)-criteria (numeric + analytic)

Take \(C_0=1\), \(C_1=-r_*\) with \(r_*>0\). Then \(e^{-\phi}\to 0^+\) as \(r\to r_*^+\):

| Probe | Result |
|-------|--------|
| \(\phi\to+\infty\) at **finite** \(r_*\) | **YES** |
| \(g_{tt}\to 0\) (time stops) | **YES** |
| Proper \(\ell=\int e^{\phi}\,dr\) as lower limit \(\to r_*^+\) | **DIVERGES** (numeric: grows as \(\sim|\ln\varepsilon|\)) |
| Redshift \(1+z=e^{\Delta\phi}\) as approach \(r_*\) | \(\to\infty\) |

**⇒ Passes bulk \(c\)-like geometric tests** that R1-weighted Coulomb and SQ geometric EL **fail**.

### Flaw (why it was set aside)

| Issue | Note |
|-------|------|
| Comes from **unweighted** kinetic \(g^{rr}(\phi')^2\), not R1 density \(\sqrt{-g}\,e^{2\phi}g^{rr}(\phi')^2\) | Probe ≠ self-consistent split; project preferred R1 weight |
| Not the same profile as xmax boost | Unweighted: \(e^{-\phi}\propto 1/r\); xmax: \(\phi=\mathrm{arctanh}(x/X)\) ⇒ \(A=(X-x)/(X+x)\) — **different families** |
| Domain / singularity structure | Needs careful exterior/interior reading (\(r>r_*\) vs \(r<r_*\)) |

### Inspiration (not automatic canon)

If the live goal is a **\(c\)-like edge**, this family is the **strongest simple-metric vacuum EL already in the founding native FE doc** that actually produces one.  
Re-opening it means reopening the **R1 kinetic weight** choice — a real principle fork, not free \(D_A\).

---

## 3. Re-probe: xmax boost structure (★★★ form)

### Content (`derive_xmax_boost.py`, commit `867ead9`)

\[
\phi = \mathrm{arctanh}\frac{x}{X},
\quad
x = X\tanh\phi,
\quad
1+z = e^{\phi} = \sqrt{\frac{X+x}{X-x}},
\quad
A = \frac{X-x}{X+x}\to 0\ \ (x\to X).
\]

### vs unweighted vacuum

| | Unweighted EL solution | xmax boost |
|--|------------------------|------------|
| \(\phi(r)\) | \(-\ln(C_0+C_1/r)\) | \(\mathrm{arctanh}(r/X)\) if \(x=r\) |
| \(A=e^{-2\phi}\) | \((C_0+C_1/r)^2\) | \((X-r)/(X+r)\) |
| Same? | **No** | Different rational structure |

Both give **\(A\to0\) / \(\phi\to\infty\)** at a finite chart location, but **not the same ODE solution**.

### Flaw

Postulates finite \(X\); later demoted as distance-invariance over-read; lasting value = **frame-relation + asymptotic edge form**.

### Inspiration

**Target check** (already in that doc): does a *derived* \(\phi(r)\) produce \(A\to0\) at finite chart radius?  
Unweighted vacuum: **yes** (for suitable \(C_0,C_1\)).  
R1 Coulomb: **no**.  
SQ geometric: **no**.

---

## 4. Other history notes (shorter)

| Item | Git / doc | Takeaway |
|------|-----------|----------|
| Branch-P \(U=e^{2\phi}-1\) | archive characterization | **Non-SQ** potential; packaging scar; runaway to \(\phi\sim0\), not clean \(r_*\) edge |
| Geometric action `af286a6` | closed G/P on \(\mathcal{K}\) | Solid for purity; **SQ exterior** — *away* from \(c\)-edge |
| Cosine reconcile `0742063` | vacuum no edge | Aligns with SQ/Coulomb refusal; “matter-sourced edge” still needs **non-SQ** matter channel |
| MS \(f\to0\) | B1 / seal | Same horizon face; GR-form mass caution |
| Matter weight \(e^{(a+1)\phi}\) | git `af7785e`, `abd8f74` (pre-native “departure = one number \(a+1\)”) | **Non-SQ if \(a+1>0\)** as \(\phi\to+\infty\); often ST/import scar; shows repo once varied **source weight** freely |

### Extra from delayed git pickaxe

- `unweighted` / `Box phi` / `C0,C1` land on **`f766478`** + `verify_native_fieldeq.py` (confirms founding dual vacuum).  
- `arctanh` lands on **`867ead9`** xmax boost.  
- Pre-native **`a(phi)` matter coupling** (`af7785e`) = another non-SQ *knob* era — use as inspiration for “weight matters,” not as live free parameter.

---

## 5. Synthesis for live simple-metric program

| Path | Status after this explore |
|------|---------------------------|
| Keep only R1-weighted + \(\mathcal{K}\)/dilated dust | Clean provenance; **fails** \(c\)-edge |
| **Unweighted vacuum** | **Passes** \(c\)-geometry tests; **fails** preferred R1 kinetic story — **live candidate to re-weigh** |
| xmax boost | Best **kinematic template**; \(X\) free ruler; check = \(A\to0\) at finite chart |
| \(U=e^{2\phi}-1\) | Best **non-SQ bulk** memory; needs re-derivation, not paste |
| Free \(D_A\) | Still quarantined; not required for unweighted horizon |

**Recommended next concrete tile (when continuing):**  
Side-by-side **principle ledger** for R1-weighted vs unweighted kinetic on the simple metric (what each preserves, what \(c\)-edge each allows), plus explicit map of unweighted horizon domain — still no free \(D_A\), no hand \(X\).

---

## Plain summary

Git history shows we once had two near-hits: a **boost-like** law that *looks like* SR with a max distance, and an **older vacuum equation** whose solution really does send dilation to infinity at a finite radius so you never quite arrive. We later preferred a “cleaner” kinetic weighting that **removes** that horizon and gives Coulomb plateaus instead. For a \(c\)-like edge, that older unweighted vacuum and the xmax *shape* are the best inspiration in the repo — flawed, but much closer than the self-quenching operators we used recently.
