## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE / PONDER (CAS; full curvature re-derive) |
| **Slice scope** | simple metric; Einstein continuum vs R1+dust EL; critical/closure mass; **G^r_r scar** |
| **Observing or targeting?** | OBSERVE route consistency + critical-matter vocabulary — not targeting forced unify |
| **Comparator scaffolds** | none |
| **Verifier status** | SELF-SCRIPT `python3 simple_metric_S4_reconcile_critical.py` (full curvature CAS) |
| **Build-on grade** | **LEAD** — route map + scar correction; S3 dust-selection **CONDITIONS-CHANGED** |
| **Re-run commands** | `python3 simple_metric_S4_reconcile_critical.py` |

### Premise ledger

| Item | Tag | Enters claim? |
|------|-----|---------------|
| Simple metric \(A=e^{-2\phi}\) | THEORY | Y |
| Einstein \(G^\mu{}_\nu\) from full curvature CAS | DERIVED this tile | Y |
| Old S3 \(G^r_r=(-A+rA'+1)/r^2\) | **FALSE** (scar) | only as correction |
| Critical \(M=X/2\) when \(A(X)=0\) | DERIVED identity | Y |
| R1 + \(L_m=-\rho r^2 e^{-2\phi}\) | probe action | Y for mismatch |
| S3 “\(p_r=0\Rightarrow A=1-r/X\)” | **INVALID selection** (bad \(G^r_r\)) | N as theorem |

### What is NOT claimed

- Routes already unified.
- New unique native selection for \(A=1-r/X\) (open after scar).
- Canon E-primary vs A-primary.

### Do not build on

- S3 radial-dust selection as derived.
- “Critical density makes R1 EL match Einstein ceiling.”

---

# S4 reconcile — critical matter *closes* the sphere; a formula scar reopened the continuum

**Ask (Charles):** reconcile Einstein continuum vs R1+dust EL; keep in view a **critical amount of matter** that may resolve tensions (another phrasing of **closes**).

---

## Lay summary

Three separate ideas got tangled. Untangled:

1. **Critical matter closes the geometric sphere.**  
   If the outer wall is “lapse dies at finite size \(X\)” (\(A(X)=0\)), the total mass **must** be \(M=X/2\) (units \(c=G=1\)). Vacuum cannot make that wall. **Enough matter closes the ball.** That hunch is right and clean.

2. **Critical matter does not glue the thin R1 action to the Einstein continuum.**  
   On the ceiling shape \(A=1-r/X\), the R1+dust equation still fails by an \(r\)-dependent residual. Dialing total mass does not fix a shape mismatch.

3. **Scar found while reconciling:** S3’s “radial dust \(p_r=0\) uniquely selects \(A=1-r/X\)” used a **wrong** \(G^r_r\) formula.  
   Full curvature on the simple metric shows a hard identity:
   \[
   p_r = -\rho \qquad\text{(always, for any }A(r)\text{)}.
   \]
   You **cannot** have static radial dust (\(p_r=0\), \(\rho>0\)) on this metric.  
   The profile \(A=1-r/X\) is still a real continuum solution — but with **\(p_r=-\rho\)**, **\(p_\perp=-\rho/2\)**, not dust. Its uniqueness must be re-derived (or left as a characterized family), not claimed from \(p_r=0\).

---

## 1. Vocabulary: what “closes” / “critical amount” means

Misner–Sharp identity on the simple metric:
\[
m=\frac{r}{2}\bigl(1-A\bigr),\qquad A=e^{-2\phi}.
\]

| Phrase | Meaning here |
|--------|----------------|
| **Closes** | Outer wall \(A\to 0\) at finite sphere size \(X\) |
| **Critical amount** | \(M_{\mathrm{crit}}=m(X)=X/2\) — the mass that **matches** that wall |
| **Mean critical density** | \(\bar\rho=3/(8\pi X^2)\) |

**Always true:** any solution with \(A(X)=0\) has \(m(X)=X/2\).  
The distribution of mass can vary; the **total** at the wall is fixed by geometry.

| Stage | Edge? | Role of critical mass |
|-------|-------|------------------------|
| S1 vacuum | **No** outer wall | No \(M\) growing to compactness 1 |
| S2 sourced MS probes | Wall **can** appear | enough mass → closure |
| Ceiling \(A=1-r/X\) | Wall at \(X\) | \(M=X/2\) by identity |

This is the same *kind* of idea as a filled cosmos at the compactness wall — **not** a FLRW \(\Omega\) import, but honest geometric closure.

**Critical amount resolves:** vacuum-vs-edge tension.  
**Critical amount does not resolve:** R1 EL vs Einstein residual (below).

---

## 2. Scar: wrong \(G^r_r\) in S3 (load-bearing)

### What S3 claimed
\[
G^r{}_r \stackrel{\text{old}}{=}\frac{-A+rA'+1}{r^2}
\quad\Rightarrow\quad
p_r=0\Rightarrow A=1+Kr
\quad\Rightarrow\quad
A(X)=0\Rightarrow A=1-r/X.
\]

### What full curvature gives (vacuum Schw check: all \(G=0\))

For \(ds^2=-A\,dt^2+A^{-1}dr^2+r^2 d\Omega^2\):

\[
\boxed{
G^t{}_t = G^r{}_r = \frac{r A' + A - 1}{r^2}
}
\]
\[
G^\theta{}_\theta = G^\phi{}_\phi = \frac{A''}{2}+\frac{A'}{r}
\]

\[
\boxed{
\rho = \frac{1-A-rA'}{8\pi r^2},
\qquad
p_r = -\rho,
\qquad
p_\perp = \frac{r A'' + 2 A'}{16\pi r}
}
\]

**Old vs correct \(G^r_r\):** differ by \(2(A-1)/r^2\).  
For \(A=1-r/X\) that error is exactly what faked \(p_r=0\).

### Consequence (solver-first, not mechanism)

| Claim | Status after scar |
|-------|-------------------|
| \(p_r=0\) with \(\rho>0\) on simple metric | **Impossible** (\(p_r=-\rho\)) |
| \(p_r=0\Rightarrow A=1+Kr\Rightarrow A=1-r/X\) | **INVALID** (false \(G^r_r\)) |
| \(A=1-r/X\) as a continuum with \(M=X/2\) | **Still valid** as a profile |
| Correct stresses on that profile | \(\rho=1/(4\pi X r)\), \(p_r=-\rho\), \(p_\perp=-\rho/2\) |
| True \(p_r=0\) solutions | \(\rho=0\), \(A=1+C/r\) (Schw family); regular origin ⇒ flat only |

**S3 build-on grade:** dust-selection theorem **CONDITIONS-CHANGED / withdrawn**.  
**Keep:** ceiling profile as characterized continuum; full-light ladder; critical mass identity; residual demos as demos only.

---

## 3. Correct continuum for the ceiling profile

\[
A=1-\frac{r}{X},
\quad
\rho=\frac{1}{4\pi X r},
\quad
p_r=-\rho,
\quad
p_\perp=-\frac12\rho,
\quad
M=\frac{X}{2}
\]

| Stress | Meaning |
|--------|---------|
| \(p_r=-\rho\) | **Identity of the simple metric** (not a free continuum choice) |
| \(p_\perp=-\rho/2\) | For this profile (\(A''=0\)): anisotropic tension |
| \(M=X/2\) | Critical amount that **closes** the sphere |

Full light readout (unchanged geometry):
\[
\frac{d_L}{X}=z(z+2),\qquad
\frac{D_M}{X}=\frac{z(z+2)}{1+z}.
\]

**What can still select this profile (open, not forced here):**  
linear lapse \(A''=0\) with \(A(0)=1,A(X)=0\); or \(\rho\propto 1/r\); or \(p_\perp=p_r/2\).  
Those are **characterize tags**, not yet a native uniqueness theorem after the scar.

---

## 4. R1+dust EL still does not host this continuum

Compensated probe:
\[
Z(r^2\phi')'=2\rho\, r^2 e^{-2\phi}.
\]

On the ceiling with Einstein \(\rho\):
\[
\frac{(r^2\phi')'}{2\rho\, r^2 A}
=\pi X^2\frac{2X-r}{(X-r)^3}
\quad\text{(\(r\)-dependent; no constant \(Z\))}.
\]

| \(r/X\) | residual ratio |
|--------:|---------------:|
| 0.1 | \(\sim 8.2\) |
| 0.5 | \(\sim 38\) |
| 0.9 | \(\sim 3500\) |

**Critical \(M=X/2\) does not erase this** — scaling \(\rho\) does not make the ratio constant.  
\(\rho\) that would satisfy R1 EL on the same \(A\) diverges as \(r\to X\) and is not the Einstein \(\rho_E\).

Joint “Einstein \(\rho_E(A)\) **and** R1 EL”: local series exist (flat; special-\(Z\) branches) — **not** \(A=1-r/X\).

---

## 5. Route map after scar + critical-mass clarity

```
                 simple metric (A = e^{-2φ})
                           |
         +-----------------+------------------+
         |                                    |
  Einstein continuum                    R1 + L_m probe
  (full G from curvature)               (vary φ)
         |                                    |
  identity p_r = -ρ                     EL for φ
  ρ, p_⊥ from A(r)                      free ρ probe
  ceiling A=1-r/X = one profile         ceilings from S2-style
  M=X/2 closes if A(X)=0                may differ
         |                                    |
         +-------- do not glue without -------+
                      residual = 0
```

| Posture | Honest content |
|---------|----------------|
| **E-primary** | Geometry defines \(T=G/8\pi\); simple metric **forces** \(p_r=-\rho\); pick/derive \(A(r)\) (ceiling is one family); critical \(M\) closes edge |
| **A-primary** | Solve R1+dust EL; report ceilings; don’t impose false dust |
| **Joint** | Overconstrained; not the S3 ceiling |
| **Critical matter** | Closes **sphere**; does not close **operator split** |

---

## 6. What the critical-matter hunch gets right

| Tension | Critical amount? |
|---------|------------------|
| Vacuum / no outer \(X\) | **Yes — closes** with \(M=X/2\) at the wall |
| Hand \(x_{\max}\) vs sourced edge | **Yes — language:** \(X\) is where \(A=0\); mass matches |
| R1 vs Einstein residual | **No** |
| Fake \(p_r=0\) uniqueness | **No** — scar; different issue |

---

## 7. Program state

| Piece | Status |
|-------|--------|
| Full light ladder | DERIVED (scoped) |
| \(M=X/2\) closes \(A(X)=0\) | **DERIVED identity** — critical amount language OK |
| S3 dust selection | **WITHDRAWN** (wrong \(G^r_r\)) |
| Ceiling profile \(A=1-r/X\) | Valid continuum; stresses corrected; **selection reopened** |
| Simple metric continuum identity | \(\boldsymbol{p_r=-\rho}\) always |
| R1+dust vs Einstein | Still split; critical mass not a glue |
| BAO \(D_M\) character | Next multi-probe tile (shape still well-defined) |

---

## 8. Next (elegant)

1. **Ponder with Charles:** after the scar, is E-primary continuum (own \(p_r=-\rho\), \(p_\perp\)) the live macro reading, or A-primary EL space?  
2. **Re-open selection** of \(A(r)\) without false dust — observe solution space (linear lapse / \(\rho\propto 1/r\) as tags only).  
3. **BAO transverse character** with fixed \(D_M/X=z(z+2)/(1+z)\) if ceiling profile kept as explore law.  
4. Optional: native action whose EL **is** Einstein on this metric (not thin R1).

---

## One-line

**Critical matter \(M=X/2\) closes the geometric sphere; it does not close the R1–Einstein residual — and reconcile CAS found S3’s dust selection was a wrong-\(G^r_r\) scar: on the simple metric \(p_r=-\rho\) always, so the ceiling is an anisotropic continuum with \(p_r=-\rho\), \(p_\perp=-\rho/2\), not radial dust.**
