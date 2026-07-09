## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE / OBSERVE |
| **Slice scope** | static SSS, \(D_A=r\), ceiling \(r\to X\), full light; N=1580 STAT+SYS |
| **Observing or targeting?** | OBSERVE demo residual; **law not selected by χ²** |
| **Comparator scaffolds** | LCDM Om=0.3 residual **reference only** |
| **Verifier status** | SELF-SCRIPT `python3 simple_metric_sphere_ceiling.py` · `python3 simple_metric_sphere_ceiling_build.py` |
| **Build-on grade** | **LEAD** (geometric non-vacuum profile; FE uniqueness OPEN) |
| **Re-run commands** | same |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| \(D_A=r\), \(r_{\max}=X\) | sphere-size ceiling (Charles) | CHOSE posture | Y |
| Full light | \(d_L=(1+z)^2 D_A\) | DERIVED | Y |
| \(A=1-r/X\) | approach to ceiling | **CHOSE geometric lead** (K-A/MS family), not FE-unique | Y |
| \(\rho\propto 1/(Xr)\) | implied by MS + this \(A\) | DERIVED from MS+profile | Y as consequence |
| \(M=c^2X/(2G)\) | bound mass | DERIVED given profile+MS | Y as relation |
| Hyp tanh package | contrast | POSTULATE composition | Y as contrast |
| Pantheon residual | demo | DATA | N as theory selector |

### What is NOT claimed

- \(A=1-r/X\) is the unique UDT solution.
- Multi-tension solved. Canon.
- Half light. Free \(D_A\) fit. χ²-forced law.

### Do not build on

- Promoting this profile solely because χ²≈0.91.

---

# Build: sphere-ceiling \(A=1-r/X\) (different derivation of max sphere size)

**Code:** `simple_metric_sphere_ceiling.py`  
**Build script:** `simple_metric_sphere_ceiling_build.py`  
**Prior:** `simple_metric_J1_alt_sphere_ceiling_MAP.md`

---

## Learning notes

| Idea | Plain |
|------|--------|
| Sphere ceiling \(X\) | Largest areal radius; you only approach it as redshift → ∞ |
| Lapse \(A\) | Clock rate factor; \(A\to 0\) means infinite redshift |
| \(A=1-r/X\) | Clocks die **linearly** as sphere size hits the ceiling (simple geometric edge) |
| Full light | Brightness still uses **two** stretch factors |
| Why not vacuum | Empty space on this metric wants \(A=1-r_s/r\) (Schw), not \(1-r/X\) |

---

## 1. Native geometric status (honest)

### What we keep from Charles

- **Max sphere size** \(X\): \(D_A=r\), \(r\to X^-\) as stretch → ∞.  
- **Full light** (not negotiable).  
- **Not** the tanh composition package as the only approach law.

### Profile

\[
\boxed{A(r)=1-\frac{r}{X},\qquad 0\le r<X}
\]

\[
\phi=-\frac12\ln A=-\frac12\ln\Bigl(1-\frac{r}{X}\Bigr),
\qquad
1+z=\frac{1}{\sqrt{A}}=\frac{1}{\sqrt{1-r/X}}
\]

\[
\boxed{\frac{r}{X}=1-\frac{1}{(1+z)^2},
\qquad
\frac{d_L}{X}=(1+z)^2-1=z(z+2)}
\]

### Vacuum vs matter (Principle 7 / solver-first)

On the simple metric, Einstein \(G^{t}{}_{t}=(A+rA'-1)/r^2\):

| Profile | \(G^{t}{}_{t}\) | Meaning |
|---------|------------------|---------|
| Schwarzschild \(A=1-r_s/r\) | \(0\) | vacuum exterior |
| **\(A=1-r/X\)** | \(-2/(Xr)\) | **not vacuum** |

Misner–Sharp (GR-form geometric on this metric):

\[
m(r)=\frac{c^2 r}{2G}(1-A)=\frac{c^2 r^2}{2GX},
\qquad
M_{\mathrm{tot}}=\frac{c^2 X}{2G}\ \text{as }r\to X^-
\]

\[
\rho=\frac{c^2}{4\pi G X r}
\quad(c=G=1:\ \rho=1/(4\pi X r))
\]

So this is a **filled** continuum with **critical compactness at finite outer radius** — same *kind* of idea as the K-A “outer edge needs matter / compactness → 1” trail (`simple_metric_KA_outer_and_matter.md`), **not** empty K-A Coulomb.

**Tag:** geometric **lead** compatible with Charles’s sphere ceiling; **not** yet “the unique solution of the UDT action.”

### Contrast: hyp tanh (still available as composition story)

| | Tanh + J1 | \(A=1-r/X\) ceiling |
|--|-----------|---------------------|
| Sphere ceiling | \(r\to X\) | \(r\to X\) |
| Approach | \(\phi=\mathrm{arctanh}(r/X)\) | \(\phi=-\frac12\ln(1-r/X)\) |
| \(d_L/X\) | \((1+z)^2\frac{(1+z)^2-1}{(1+z)^2+1}\) | \((1+z)^2-1\) |
| Vacuum? | generally filled hyp mass profile | filled \(\rho\propto 1/r\) |
| SNe shape (1 offset) | χ²/dof **2.17** | χ²/dof **~0.91** (demo) |

---

## 2. Characterize residual (demo only)

| Model | χ²/dof | RMS | 〈res〉 \(z>0.6\) |
|-------|-------:|----:|-----------------:|
| **\(A=1-r/X\) full light** | **0.910** | 0.158 | ≈ 0 |
| Hyp tanh J1 full light | 2.167 | 0.307 | −0.60 |
| LCDM Om=0.3 **ref** | 0.881 | 0.154 | ≈ 0 |

**Calibration (CHOSE \(M_B=-19.25\)):** \(X\sim\) few Gpc class, \(M_{\mathrm{tot}}=c^2X/(2G)\) — same lock formula as J1 hyp, different path to \(A\to0\).

**Hygiene:** residual **supports exploring** this geometric edge; it does **not** by itself make the law derived.

---

## 3. What “building” means here

**Delivered:**

1. Clean module API for the ceiling law.  
2. Explicit **source** and **mass** ledger (non-vacuum).  
3. Split from tanh composition package.  
4. Rerunable residual demo under full light.  
5. Honest tags: LEAD, not canon.

**Still owed for theory solidification:**

1. Is \(A=1-r/X\) selected by a **native** FE / action / junction condition (not only MS + ansatz)?  
2. Regularity at \(r=0\): \(\rho\sim 1/r\) **blows at the origin** — structural issue (like other central singularities); needs completion or chart care.  
3. Multi-probe under same \(r(z)\).  
4. Relation (if any) between this ceiling and hyperbolic **composition** (maybe composition is about something else than \(r\)).

---

## 4. Origin caveat (important)

\(\rho\propto 1/r\) diverges as \(r\to 0\).  
So this profile is a **whole-domain geometric edge model**, not a polished regular-center cosmology.  
That is a **solver/profile completeness** issue (solver-first), not a reason to reintroduce half light.

---

## One-line

**Built sphere-ceiling \(A=1-r/X\) under full light and \(D_A=r\): non-vacuum critical edge with \(M=c^2X/(2G)\); residual demo ~0.91 vs tanh’s 2.17; LEAD for native FE selection, not χ²-canonized theory.**
