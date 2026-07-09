## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE (GR corpus mine) |
| **Slice scope** | static SSS Einstein tensor; two metric functions → UDT reciprocal restriction |
| **Observing or targeting?** | OBSERVE what falls out — not targeting glue or SNe |
| **Mine vein** | GR SSS reduction / Einstein eqs / MS (corpus) × positional reciprocal metric |
| **Verifier status** | SELF CAS (full curvature components) |
| **Build-on grade** | **LEAD** (structure fallout); Einstein package still GR-form conditional as UDT-native |
| **Re-run** | `python3 simple_metric_mine_SSS_Einstein.py` |

### Premise ledger

| Item | Tag |
|------|-----|
| GR static SSS toolkit | **mine method** |
| UDT reciprocal: \(\nu=-\phi\), \(\lambda=+\phi\) | THEORY (simple metric) |
| \(G=8\pi T\) continuum read | GR-form on ansatz |
| R1 vacuum | contrast only |

### What is NOT claimed

- Einstein package is proven native UDT.
- R1 is wrong.
- Cosmology model selected.

### Do not build on

- Pasting GR vacuum as UDT vacuum without package tag.
- Gluing Coulomb to Schwarzschild by a mechanism.

---

# Mine pass — SSS Einstein under positional reciprocity

**Method:** `simple_metric_GR_corpus_mine_MAP.md`  
**Ore:** standard static spherical GR (two metric potentials).  
**Smelt:** restrict to simple-metric reciprocity (positional dilation form).  
**Ask:** what field equations / continuum identities **fall out**?

---

## Lay summary

GR usually allows two independent radial warps for a static ball (time-warp and radial-warp).  
UDT’s simple metric **locks them together** (reciprocal positional dilation): if clocks run as \(e^{-\phi}\), rulers run as \(e^{+\phi}\).

**What falls out when you put Einstein’s equations on that locked metric:**

1. Energy density and radial pressure are **no longer independent** — you always get **\(p_r = -\rho\)**.  
2. Empty space (Einstein vacuum) is **Schwarzschild-type** lapse \(A=1-r_s/r\), **not** the Coulomb \(\phi\) from the thin R1 action.  
3. Equilibrium (conservation) collapses to a simple relation between density slope and tangential pressure.  
4. The two packages we already mapped are **the same split GR sees** once reciprocity is on: free SSS vs locked SSS vs pure scalar kinetic.

No new mechanism. Clearer origin story for the scar and the two maps.

---

## 1. GR starting point (two functions)

\[
ds^2 = -e^{2\nu(r)}c^2 dt^2 + e^{2\lambda(r)}dr^2 + r^2 d\Omega^2
\]

CAS Einstein mixed components (symbolic):

\[
\begin{aligned}
G^t{}_t &= \frac{-2r\lambda' - e^{2\lambda} + 1}{r^2}\,e^{-2\lambda},\\
G^r{}_r &= \frac{2r\nu' - e^{2\lambda} + 1}{r^2}\,e^{-2\lambda},\\
G^\theta{}_\theta &= \cdots(\nu'',\nu',\lambda')
\end{aligned}
\]

**Fallout without UDT:** \(G^t{}_t\) and \(G^r{}_r\) are **independent** → \(\rho\) and \(p_r\) independent → ordinary TOV territory.  
Vacuum \(G^t{}_t=0\Rightarrow e^{-2\lambda}=1-C/r\) (standard mass function).

---

## 2. Smelt: UDT reciprocal restriction

Simple metric = positional reciprocity:
\[
\nu = -\phi,\qquad \lambda = +\phi
\qquad\bigl(A=e^{2\nu}=e^{-2\phi}=e^{-2\lambda}\bigr).
\]

**Falls out immediately:**
\[
G^t{}_t = G^r{}_r
\quad\Rightarrow\quad
\boxed{p_r = -\rho}
\]
for **any** \(\phi(r)\) (any continuum read from \(G=8\pi T\)).

This is the scar-corrected identity, now seen as:

> **Einstein continuum + reciprocal positional metric \(\Rightarrow\) radial tension equals density.**

Not a fluid assumption. A **metric-ansatz + Einstein** identity.

---

## 3. Vacuum fallout (Einstein package on reciprocal metric)

\[
\rho=0 \;\Rightarrow\; 1-A-rA'=0 \;\Rightarrow\; \boxed{A=1+\frac{C}{r}}
\]
(\(C=-r_s\) for the usual horizon branch).

\[
\phi = -\tfrac12\ln A = -\tfrac12\ln\bigl(1-r_s/r\bigr)
\quad\text{(not Coulomb)}.
\]

| Package | Vacuum on simple metric |
|---------|-------------------------|
| Einstein-on-ansatz (this mine) | **Schwarzschild-type** \(A=1-r_s/r\) |
| R1 vary-\(\phi\) (A-primary) | **Coulomb** \(\phi=a-q/r\) |

Coulomb has **nonzero** Einstein \(\rho_E\) in general — so R1 vacuum is **not** Einstein vacuum under reciprocity.

**Mine fallout:** GR+reciprocal dilation does **not** reproduce R1 vacuum. The package split is structural in the corpus transform, not an accident of our residual checks.

---

## 4. Hydrostatic fallout under \(p_r=-\rho\)

Standard anisotropic conservation (GR form, \(\nu\) from \(g_{tt}\)):
\[
p_r' = -(\rho+p_r)\nu' - \frac{2}{r}(p_r-p_t).
\]

With \(p_r=-\rho\) and \(\nu=-\phi\):
\[
\boxed{\rho' + \frac{2}{r}(\rho + p_t) = 0}.
\]

Check on ceiling tile \(A=1-r/X\): \(\rho\propto 1/r\), \(p_t=-\rho/2\) — identity holds.

**Meaning:** once radial stress is locked, “equilibrium” only constrains how \(p_t\) tracks \(\rho'\).  
On the E-map power family \(A=1-cr^p\), this is already encoded in \(p_t/\rho=-p/2\).

---

## 5. What this mine does *not* settle

| Open | Why |
|------|-----|
| Is Einstein-on-ansatz **native UDT**? | Still GR-form package; principle 7 open |
| Is R1 native? | Different action; shift-clean; no Einstein vacuum |
| Third package? | e.g. vary full metric **before** imposing reciprocity; or different bulk weight — unentered |
| Cosmology slice \(p\) | Still not selected |

---

## 6. Green next veins (from this pass)

1. **Vary free \(\nu,\lambda\) in EH, then impose \(\nu+\lambda=0\) as constraint** (Lagrange) — does an action for \(\phi\) fall out, or only constraints?  
2. **Interior catalogs** (const density, polytrope) re-solved with forced \(p_r=-\rho\) — pure character census.  
3. **Junction / exterior Schw + interior reciprocal fill** — matching at a surface (edge language).

---

## One-line

**Mining SSS Einstein under UDT reciprocity: independent GR pressures collapse to \(p_r=-\rho\); Einstein vacuum is Schw-type not Coulomb; hydrostatic reduces to \(\rho'+2(\rho+p_t)/r=0\) — package split is structural fallout, not a residual bug.**
