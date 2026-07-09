## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE |
| **Slice scope** | simple metric; MS continuum \(A=1-2m/r\), \(m'=4\pi r^2\rho\); full light readout; no χ² in solve |
| **Observing or targeting?** | OBSERVE solution space — residual DEMO only after inventory |
| **Comparator scaffolds** | LCDM not used in solve; residual demo self-contained |
| **Verifier status** | SELF-SCRIPT `python3 simple_metric_S2_sourced_space.py` |
| **Build-on grade** | **CONDITIONAL** (probe densities FREE; MS GR-form) |
| **Re-run commands** | `python3 simple_metric_S2_sourced_space.py` |

### Premise ledger

| Item | Tag | Enters claim? |
|------|-----|---------------|
| Simple metric + MS identity | THEORY / GR-form geometric | Y |
| Probe \(\rho\) families | FREE named probes | Y as space tiles |
| Full light | DERIVED readout | Y after solve |
| No imposed \(A(X)=0\) BC | honesty | Y |
| Residual demo | DATA after | N as selector |

### What is NOT claimed

- Dust probes are fundamental UDT matter.
- A profile is canon because residual is small.
- Vacuum was wrong to check (S1 stands).

### Do not build on

- χ² from demo as join/FE selection.

---

# S2 RESULT — Sourced MS solution space

**Script/JSON:** `simple_metric_S2_sourced_space.py` · `simple_metric_S2_sourced_space_out.json`  
**Prior:** S1 vacuum inventory (no outer ceiling in vacuum)

---

## Lay summary

We turned **matter** on in the simplest geometric way the metric already knows:

- mass grows with density: \(m' = 4\pi r^2\rho\)  
- clocks/lapse: \(A = 1 - 2m/r\)  
- stretch: \(1+z = 1/\sqrt{A}\)  
- brightness: full light \(d_L = (1+z)^2 r\) **after** the solve  

**Uncovering:** with enough continuum mass, solutions **do** develop **infinite redshift at a finite sphere size** (\(A\to 0\) at finite \(r\)). Vacuum (S1) did not.  

So the **outer sphere ceiling** is a **sourced** geometric character — mass enough that compactness hits 1 — not an invented shell fluid and not present in empty space.

---

## What emerged (characters)

| Probe continuum | Hits \(A\to 0\) at finite \(r\)? | Low-\(z\) \(d_L\) class (readout) |
|-----------------|----------------------------------|----------------------------------|
| Constant \(\rho\) | **Yes** (critical ball) if dense enough | **soft** \(\sim z^{0.5}\) (regular center) |
| Gaussian blob | **Yes** if central density high enough | soft when center-dominated |
| \(\rho \propto 1/r\) | **Yes** at \(r=1/k\) exactly | **near-linear** \(\sim z^{1}\) |
| \(\rho \propto 1/r^2\) | only if strong enough | various |

**21 runs:** 18 hit \(A\to 0\).

### Geometric identity recovered (not invented)

\[
\rho = \frac{k}{4\pi r}
\quad\Rightarrow\quad
m=\frac{k}{2}r^2,
\quad
A=1-kr
\quad(A=0\ \text{at}\ r=1/k).
\]

That **is** the lead profile \(A=1-r/X\) with \(X=1/k\).  
It **sits inside the MS solution space** once that continuum is allowed — not a Pantheon spline.

---

## Residual DEMO (after inventory — not selector)

| Solution character | χ²/dof (1 offset) |
|--------------------|------------------:|
| MS \(\rho\propto 1/r\) → \(A=1-r/X\) | **0.91** |
| MS const \(\rho\) critical | ~**24** |
| MS dense gauss | ~**24** |

Same split as before: **linear-type center + ceiling** vs **regular soft center + ceiling**.  
Demo **illustrates** the character theorem; it does **not** promote \(\rho\propto 1/r\) to fundamental matter.

---

## Orchestra reading (elegant)

| Sector | Role |
|--------|------|
| Vacuum (S1) | redshift / local horizons / open depth-limited space |
| Continuum mass (S2) | **can** produce outer \(A\to 0\) at finite \(r\) |
| Full light | fixed readout |
| Charles \(X\) | max sphere size when that edge **emerges** |
| Composition tanh | separate instrument (not required for this edge) |

**Solver-first:** S1 absence of outer ceiling was not a dead end; **source sector was off**. S2 turns it on and the character appears.

---

## What is still open (honest)

1. **Which continuum is native** (action-derived), not a FREE probe?  
2. \(\rho\propto 1/r\) origin singularity vs linear Hubble tradeoff — already mapped.  
3. Multi-probe with the **emerged** edge solutions.  
4. Connection, if any, of composition/\(x_{\max}\) group law to this MS edge.

---

## One-line

**Sourced MS solution space develops outer infinite-redshift at finite sphere size when mass is sufficient; \(\rho\propto 1/r\) realizes \(A=1-r/X\) as a continuum solution (not an invented fit); regular fills hit the edge with soft low-\(z\) — next is native source from the action, not residual ranking.**
