## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | MAP |
| **Slice scope** | simple metric only; φ(r); static SSS first; full light as **readout**, not selector |
| **Observing or targeting?** | OBSERVE solution space — **not** targeting SNe shape or LCDM |
| **Comparator scaffolds** | Residual demos **after** structure, optional; never fitness |
| **Verifier status** | NONE (map) |
| **Build-on grade** | **LEAD** (program map) |
| **Re-run commands** | N/A |

### Premise ledger

| Item | Tag |
|------|-----|
| Simple metric \(D_A=r\), field \(\phi(r)\) | THEORY |
| Operators W-fork, Z, L_m | FORK / FREE / OPEN (`SIMPLE_METRIC_MACRO.md`) |
| Full light \(d_L=(1+z)^2 r\) | DERIVED readout |
| Charles \(X\) sphere ceiling | CHOSE intuition to **characterize against**, not impose as BC unless derived |
| Solution-space-not-imposition | **binding** |

### What is NOT claimed

- That scanning residuals finds the law.
- That \(A=1-r/X\) or tanh is in the solution space until shown.

### Do not build on

- Imposing ceiling/BC to force a desired \(d_L(z)\).

---

# MAP — Solution space of the metric as path to resolution shapes

**Charles:** computing the solution space of the metric may show the shape of the resolutions.  
**Yes.** That is the UDT path: **uncover what solutions already look like**, then read distances from them — not invent \(A(r)\) to match the sky.

Aligns with: elegance zoom (`simple_metric_macro_elegance_ZOOM.md`), skill `solution-space-not-imposition`, SIMPLE_METRIC_MACRO operators.

---

## 1. Why this is the right move

| Wrong path | Right path |
|------------|------------|
| Guess \(A(r)\) / \(\phi(r)\) for good SNe | Solve **metric EL** → family of \(\phi(r)\) |
| Rank laws by χ² | **Characterize** \(z(r)\), \(d_L(z)\), edge, center **after** solve |
| Add mechanism when residual large | Ask: wrong operator fork? incomplete source? frozen DOF? |
| Freeze ceiling BC because intuition likes it | See whether solutions **develop** a ceiling / barrier |

**Resolution shapes** = shapes that **appear** in the solution space (plateau, Coulomb tail, horizon, barrier, regular/irregular center, …), not shapes we paste on.

---

## 2. What “solution space” means here (concrete)

**Arena (live):** simple metric only  
\[
ds^2=-e^{-2\phi(r)}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2
\]
Field: **\(\phi(r)\)** (+ optional continuum \(\rho\) once sourced honestly).

**Already native operator forks** (`SIMPLE_METRIC_MACRO.md`, harmonic triangle):

| Branch | EL / condition | Known vacuum character |
|--------|----------------|----------------------|
| **K-R1** compensated | \((r^2\phi')'=0\) | Coulomb \(\phi=\phi_\infty-q/r\) — redder then limited depth |
| **Uncompensated W=1** | \(Z(r^2\phi')'=4e^{-2\phi}\) | SQ-type sources; asymptotics explored |
| **K-UW** | \(\Delta e^{-\phi}=0\) | \(e^{-\phi}=C_0+C_1/r\) — \(c\)-like horizon family |
| **K-A** | \(\Delta e^{-2\phi}=0\) / \(G_{\theta\theta}=0\) | \(A=C_0+C_1/r\) — Schw branch \(A=1-r_s/r\) |
| **+ dilated dust** | EL with \(L_m\propto\rho e^{-2\phi}\) | probe continuum; not fundamental matter |

**Readout (after solve, fixed optics):**

\[
1+z=e^{\phi},\quad D_A=r,\quad d_L=(1+z)^2 r
\]

Optional: compare to Charles ceiling idea **as a diagnostic** (“does any solution approach \(A\to0\) at finite \(r\)?”) — **characterize**, don’t impose \(A(X)=0\) unless derived.

---

## 3. What to report from a solution (character, not filter)

For each solved \(\phi(r)\) (or \(A(r)\)):

| Diagnostic | Question |
|------------|----------|
| Center | \(\phi'(0)=0\) or not? \(\rho(0)\) finite? |
| Monotone redshift | \(\phi'\) sign / \(z(r)\) increasing? |
| Far behavior | plateau / Coulomb / \(A\to0\) / \(\ell\) diverge? |
| Compactness | \(2Gm/c^2r\) — approaches 1 anywhere? |
| \(d_L(z)\) shape | linear low-\(z\)? stiff high-\(z\)? (after solve) |
| Ceiling diagnostic | Does \(r\) stay open while \(A\to0\)? |

**Forbidden filter:** discard solutions because SNe residual is large.  
**Allowed later:** with Charles, ask which **characters** match multi-tension goals.

---

## 4. Program (bounded, anti-hang)

| Step | Action | Bound |
|------|--------|-------|
| S0 | Fix operator fork ledger (W, Z, vacuum vs probe \(\rho\)) | MAP tags |
| S1 | **Vacuum solution space** per fork — analytic first (Coulomb, Schw, UW, uncompensated) | closed form + asymptotics |
| S2 | **Sourced** only with **named** continuum (dilated dust probe or MS \(\rho\) from Einstein identity) — scan amounts as FREE | Nr small; one process |
| S3 | For each solution: table of characters §3 | no χ² in the loop |
| S4 | **Then** optional residual **demo** on a few representative solutions | 1 offset; LCDM ref only |
| S5 | Ponder with Charles: which **emerged** shapes are interesting | not auto-promote |

**Anti-imposition:** no BC “must hit \(A=0\) at \(r=X\)” unless that appears from theory or is explicitly tagged CHOSE probe.

**Charles ceiling:** after S1–S3, ask “who in the space approaches a sphere-size barrier?” — discovery, not BC.

---

## 5. Relation to recent LEADs (demote to probes inside the space)

| LEAD | Role in solution-space program |
|------|--------------------------------|
| Hyp tanh + J1 | One **ansatz curve** — check if any FE solution approximates it |
| \(A=1-r/X\) | One **geometric probe** — appears only if some sourced MS solution has \(A'=const\) |
| P_ell | Different length job — not a substitute for solving \(\phi(r)\) |
| Full light | **Fixed readout** for all solutions |

If solution space **never** produces gentle full-light \(d_L\), that indicts **operator/source completeness** first (solver-first), not “add DE.”

---

## 6. Elegance check

Solution-space work is elegant when:

- equations come **only** from simple-metric action/identities;  
- forks are few and named;  
- structure is **reported**, not rewarded for looking like ΛCDM;  
- postulates (\(X\), static, dust probe) stay **visible**.

It fails elegance when the “space” is really a menu of hand \(A(r)\) with residual scores.

---

## One-line

**Yes — map and compute the simple-metric \(\phi(r)\) solution space (operator forks + honest sources), read \(d_L(z)\) afterward, and let barrier/ceiling/linear-Hubble characters emerge; that is uncovering resolutions, not inventing shapes.**
