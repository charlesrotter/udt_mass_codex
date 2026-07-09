# OBSERVE — PATH vs AREAL split on xmax hyperbolic (drop J1 default)


## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit / original work date may differ) |
| **Mode** | OBSERVE |
| **Slice scope** | hyp PATH; P_ell CHOSE explore; N=1580 full cov |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | LCDM Om=0.3 residual ref only |
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

**Date:** 2026-07-09 · **Mode: OBSERVE**  
**Script:** `simple_metric_path_areal_split_observe.py`  
**JSON:** `simple_metric_path_areal_split_out.json`  
**Prior MAP:** `simple_metric_distance_profile_dimensional_MAP.md`  
**Status:** PROVISIONAL — named join explored; not a SNe victory; not free \(D_A(r)\).

---

## 0. Setup (held)

| Item | Choice |
|------|--------|
| Full light | \(d_L=(1+z)^2 D_A\) |
| PATH (1D composition) | \(x=X\tanh\phi\), \(1+z=e^{\phi}\) (xmax postulate) |
| **Not** assumed | \(D_A=x\) (that was **J1**) |

### Two joins compared

| Join | Tag | Content |
|------|-----|---------|
| **J1** | CHOSE (old default) | PATH label = areal: \(D_A=x\) |
| **P_ell** | CHOSE named dimensional join | PATH \(x\) = **proper** radial length: \(dx=e^{\phi}dr\) ⇒ \(D_A=r(x)=\int_0^x e^{-\phi(u)}\,du\) |

P_ell is **not** a free function fit. It is one clean answer to “1D path vs 2-sphere areal.”  
It is still a **join** (why composition distance = proper length) — tag **CHOSE / explore**, not theorem.

---

## 1. Geometry of P_ell

With \(\phi=\mathrm{arctanh}(x/X)\):

\[
e^{-\phi}=\sqrt{\frac{X-x}{X+x}},
\qquad
\frac{r}{X}=\int_0^{x/X}\sqrt{\frac{1-u}{1+u}}\,du.
\]

| \(x/X\) | \(r/X\) | \(r/x\) |
|--------:|--------:|--------:|
| 0.10 | 0.095 | 0.95 |
| 0.50 | 0.390 | 0.78 |
| 0.95 | 0.565 | 0.60 |
| →1 | ≈ **0.571** | →0 |

So under P_ell: **areal radius saturates** near \(0.57\,X\) while PATH proper length still approaches \(X\).  
That is a dimensional split with teeth: 1D reach and 2-sphere size are **not** the same number.

Low \(z\): both J1 and P_ell give \(d_L\sim X z\) (linear Hubble OK).

---

## 2. Shape vs J1 and LCDM (normalized at \(z=0.05\))

| \(z\) | \(d_L\) J1 | \(d_L\) P_ell | LCDM ref | \(\Delta\mu\) P−J | \(\Delta\mu\) P−L |
|------:|-----------:|--------------:|---------:|------------------:|------------------:|
| 0.10 | 2.14 | 2.09 | 2.07 | −0.05 | +0.02 |
| 0.50 | 16.1 | 13.6 | 12.7 | −0.36 | +0.15 |
| 1.00 | 44.7 | 33.8 | 29.7 | −0.60 | +0.28 |
| 2.00 | 134 | 90.5 | 69.9 | −0.85 | +0.56 |

**Reading:** P_ell is **softer** than J1 at high \(z\) (smaller \(D_A\) than \(x\)) — moves **toward** LCDM-like shape, still a bit stiff at the high end.

---

## 3. Pantheon demo (1 offset only; scale free)

Full STAT+SYS, same cut as before:

| Model | χ²/dof | RMS (mag) |
|-------|-------:|----------:|
| **J1** \(D_A=x\) | **2.17** | 0.307 |
| **P_ell** \(D_A=r(x)\) | **1.02** | 0.180 |
| LCDM Ωₘ=0.3 ref | 0.88 | 0.154 |

**Δχ² (J1 − P_ell) ≈ large** — splitting PATH from AREAL **matters a lot**.  
P_ell is **much closer** to data than J1, still short of LCDM ref (not a claim of win).

---

## 4. What this means for the dimensional clue

| Claim | Status |
|-------|--------|
| Exact-power / profile issues can come from **job mix** PATH vs AREAL | **Supported** (this tile) |
| J1 was an over-join | **Likely** — one CHOSE identification drove a large shape error |
| P_ell is the unique derived truth | **Not claimed** — named explore join |
| Free \(D_A(r)\) needed | **Not shown** — one derived integral from a named 1D=proper choice |
| Fudge √ on old half-light | **Still forbidden** |

**Lay:** Treating “how far along the path” as the same number as “how big the sphere is” was the stiff high-\(z\) mistake in the hyp package. Letting path be proper length and sphere size be the integrated areal radius softens the sky law a lot — without going back to half light count.

---

## 5. Open (honest)

1. **Why** should compositional \(x\) equal **proper** length? (P_ell still CHOSE.)  
2. Other PATH meanings (radar, affine, composition without proper) → other \(r(x)\).  
3. Residual vs LCDM at high \(z\) remains — profile hunt not finished.  
4. Mass lock under J1 used \(r=x\); under P_ell, mass–\(X\) relation must be **re-derived**.

---

## 6. One-line

**Dropping J1 and setting PATH \(x\)=proper length so \(D_A=r(x)=\int e^{-\phi}dx\) (full light held) cuts hyp Pantheon χ²/dof from ~2.17 to ~1.02 — strong support that the profile clue is PATH vs AREAL job mix, not a fudge factor; P_ell still a named join, not final theory.**
