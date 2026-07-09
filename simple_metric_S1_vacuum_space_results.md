## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE |
| **Slice scope** | simple metric vacuum; φ-only forks; full light = readout only |
| **Observing or targeting?** | OBSERVE solution space — **no χ² in solve loop** |
| **Comparator scaffolds** | NONE in inventory |
| **Verifier status** | SELF-SCRIPT `python3 simple_metric_S1_vacuum_space.py` |
| **Build-on grade** | **CONDITIONAL** (scoped vacuum characters) |
| **Re-run commands** | `python3 simple_metric_S1_vacuum_space.py` |

### Premise ledger

| Item | Tag | Enters claim? |
|------|-----|---------------|
| Simple metric \(D_A=r\) | THEORY | Y |
| Forks K-R1, W=1, K-UW, K-A | THEORY/FORK native | Y |
| Vacuum \(L_m=0\) | SCOPED | Y |
| Full light | DERIVED readout | Y after solve |
| Sphere ceiling \(X\) | CHOSE diagnostic only | N as BC |

### What is NOT claimed

- UDT false. Matter cannot help. A hand profile is the solution.
- SNe ranking of forks.

### Do not build on

- Imposing \(A(X)=0\) because vacuum lacks it.

---

# S1 RESULT — Vacuum solution-space inventory

**Script/JSON:** `simple_metric_S1_vacuum_space.py` · `simple_metric_S1_vacuum_space_out.json`  
**MAP:** `simple_metric_solution_space_MAP.md`

---

## Lay summary

We asked the **empty** simple metric (no matter source): what kinds of dilation profiles already exist?

**Main uncovering:**  
Vacuum solutions give **redshift**, **local horizons**, or **open space with limited depth** — but **not** a filled-universe “maximum sphere size” where space grows and clocks die at a large outer radius.  

That matches the earlier geometric point: an **outer sphere ceiling** wants **mass/compactness**, not empty space.  
Next is **sourced** solution space (S2), not a new mechanism fluid for SNe.

---

## Character table (vacuum)

| Fork | What it is | Far behavior | \(A\to0\) at finite \(r\)? | Outer sphere ceiling? |
|------|------------|--------------|---------------------------|------------------------|
| **K-R1** | \(\phi\) Coulomb | \(\phi\to\) finite plateau | No | **No** — open \(r\), finite max \(z\) |
| **W=1** | uncompensated bulk | quasi-plateau (SQ source dies) | No | **No** |
| **K-UW** | clock factor harmonic | flat at ∞; wall at \(r_*\) | **Yes** (horizon) | **No** — wall is **inward** from exterior, not growing outer max sphere |
| **K-A / Schw** | lapse harmonic + vacuum energy | flat at ∞ | **Yes** at \(r_s\) | **No** — **local** hole, not cosmic outer ceiling |

Full light readout everywhere: \(d_L=(1+z)^2 r\) **after** the solution is known.

---

## Resolution shapes that **do** appear (vacuum)

| Shape | Where |
|-------|--------|
| Redder then **limited depth** | K-R1, W=1 |
| **Horizon** (infinite \(z\), finite \(r\)) | K-UW, K-A |
| Asymptotically flat exterior | K-A Schw |
| Open proper distance to infinity | K-R1, W=1 |
| Divergent proper distance to wall | K-UW |

## Shapes that **do not** appear (vacuum)

| Shape | Status |
|-------|--------|
| Filled **outer** sphere ceiling (\(r\) large, \(A\to0\) as max cosmic size) | **Absent** in S1 |
| Gentle full-light SNe map from vacuum alone | Not expected; vacuum not that object |
| Regular center + linear Hubble + full light + \(D_A=r\) | Still blocked by series theorem |

---

## Implication (solver-first, elegant)

Charles’s sphere-size ceiling is a question to the **sourced** geometry:

> Who in the **matter-filled** solution space develops compactness → 1 at finite outer \(r\)?

That is **Misner–Sharp / critical continuum** territory already flagged in K-A matter notes — **uncover \(m(r)\)**, not invent \(A(r)\) for Pantheon.

Hand profiles (tanh, \(A=1-r/X\)) remain **probes to compare** after S2, not replacements for the space.

---

## S2 preview (next)

| Step | Content |
|------|---------|
| Named source | dilated dust probe and/or MS \(\rho\) from Einstein identity |
| Observe | which solutions develop \(A\to0\) at finite \(r\); center characters; \(d_L(z)\) readout |
| Bound | modest grids; no χ² inside integrator |
| Ceiling diagnostic | report if/when Charles-\(X\)-like behavior **emerges** |

---

## One-line

**Vacuum simple-metric solution space: redshift and local horizons exist; a filled outer sphere-size ceiling does not — next uncover sourced solutions, not residual-ranked lapse shapes.**
