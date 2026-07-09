## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE |
| **Slice scope** | simple metric; Einstein/MS identities; static; \(p_r=0\) continuum condition |
| **Observing or targeting?** | DERIVE from metric identities — residual DEMO only after |
| **Comparator scaffolds** | residual DEMO uses Pantheon; **not** used in selection |
| **Verifier status** | SELF-SCRIPT `python3 simple_metric_S3_native_dust_ceiling.py` (CAS + numeric) |
| **Build-on grade** | **CONDITIONS-CHANGED** — dust-selection **WITHDRAWN** (wrong \(G^r_r\)); see `simple_metric_S4_reconcile_critical_results.md` |
| **Re-run commands** | `python3 simple_metric_S4_reconcile_critical.py` (correct \(G\)); old S3 script is scar record |

### ★ SCAR (2026-07-09 reconcile)

Old formula \(G^r_r=(-A+rA'+1)/r^2\) is **false**. Full curvature:
\(G^t_t=G^r_r=(rA'+A-1)/r^2\) ⇒ **\(p_r=-\rho\) always** on the simple metric.
Radial dust \(p_r=0\) with \(\rho>0\) is **impossible**.  
Profile \(A=1-r/X\) **survives** as continuum with \(\rho=1/(4\pi Xr)\), \(p_r=-\rho\), \(p_\perp=-\rho/2\), \(M=X/2\);
**uniqueness from \(p_r=0\) does not.**

### Premise ledger

| Item | Tag | Enters claim? |
|------|-----|---------------|
| Simple metric | THEORY | Y |
| \(m=r(1-A)/2\), Einstein \(G\) components | GR-form geometric on this metric | Y |
| \(p_r=0\) (radial dust) | **CHOSE continuum class** / named condition | Y |
| Outer \(A(X)=0\) | Charles sphere ceiling | Y |
| Full light | DERIVED readout | Y |
| Action-fundamental matter | OPEN | N |

### What is NOT claimed

- Full UDT matter action derived.
- Isotropic perfect fluid ( \(p_\perp\) generally ≠ 0 ).
- Canon. χ²-selected law.

### Do not build on

- Ignoring anisotropy tag.

---

# S3 — Native selection: radial dust ⇒ sphere-ceiling lapse

**Script:** `simple_metric_S3_native_dust_ceiling.py`  
**Prior:** S1 vacuum (no outer ceiling) · S2 MS probes (ceiling emerges with mass)

---

## Lay summary (elegance)

We did **not** pick \(A=1-r/X\) because Pantheon liked it.

We asked the simple metric:

> If the continuum has **no radial pressure** (static “dust” along the radius), what lapse profiles are allowed?

The geometry answers with a **unique family**:

\[
A = 1 + K r
\]

Charles’s outer sphere ceiling \(A(X)=0\) with regular \(A(0)=1\) fixes \(K=-1/X\):

\[
\boxed{A = 1 - \frac{r}{X}}
\]

That is **uncovering what the metric + dust condition already do** — the same profile that S2 found when we put \(\rho\propto 1/r\), and that residual demos found gentle under full light.

---

## Derivation (exact)

On the simple metric (\(c=G=1\)):

\[
m=\frac{r}{2}(1-A),
\qquad
G^{t}{}_{t}=\frac{A+rA'-1}{r^2},\qquad
G^{r}{}_{r}=\frac{-A+rA'+1}{r^2}
\]

\[
\rho=-\frac{G^{t}{}_{t}}{8\pi},\qquad
p_r=\frac{G^{r}{}_{r}}{8\pi}
\]

**Radial dust:** \(p_r=0\)

\[
r A' - A + 1 = 0
\quad\Rightarrow\quad
A'=\frac{A-1}{r}
\quad\Rightarrow\quad
\boxed{A=1+Kr}
\]

**Outer ceiling** \(A(X)=0\), **\(A>0\)** for \(r<X\): \(K=-1/X\)

\[
\boxed{A=1-\frac{r}{X},
\quad
\rho=\frac{1}{4\pi X r},
\quad
p_r=0,
\quad
M_{\mathrm{tot}}=\frac{X}{2}}
\]

\[
1+z=\frac{1}{\sqrt{A}},
\quad
\frac{d_L}{X}=(1+z)^2-1=z(z+2)
\quad\text{(full light)}
\]

CAS: `dsolve` of the ODE; numeric \(m'=4\pi r^2\rho\) holds.

---

## Honest continuum tags

| Quantity | Value | Note |
|----------|--------|------|
| \(p_r\) | \(0\) | selecting condition |
| \(\rho\) | \(1/(4\pi X r)\) | positive for \(r\in(0,X)\) |
| \(p_\perp\) | **generally ≠ 0** | anisotropic continuum — **not** isotropic perfect fluid dust |
| Center | \(\rho\sim 1/r\), \(\phi'(0)\neq 0\) | linear Hubble price (already uncovered) |

So: **radial dust**, not “ideal gas star.”  
Still geometric, still no free \(A(r)\) fit.

---

## How this closes the arc (solver-first)

| Stage | Result |
|-------|--------|
| S1 vacuum | No outer sphere ceiling |
| S2 free \(\rho\) probes | Ceiling **emerges** with mass; \(\rho\propto 1/r\) recreates \(A=1-r/X\) |
| **S3** | \(p_r=0\) **selects** \(A=1-r/X\) uniquely with outer zero |

Residual demo (after derive): χ²/dof ~ **0.91** under full light — **character check**, not the reason the law exists.

---

## What remains open (not mechanisms)

1. Derive **radial dust** \(p_r=0\) from the **UDT action** (or show it is the natural static continuum).  
2. Meaning of **tangential stress** (anisotropy) — uncover, don’t paste isotropy.  
3. Multi-probe with \(d_L/X=z(z+2)\).  
4. Composition/tanh as a **separate** sector if still wanted.

---

## One-line

**On the simple metric, static radial dust \(p_r=0\) forces \(A=1+Kr\); a sphere-size ceiling \(A(X)=0\) uniquely gives \(A=1-r/X\) with \(\rho\propto 1/r\) and full-light \(d_L/X=z(z+2)\) — uncovered geometry, not an invented SNe profile.**
