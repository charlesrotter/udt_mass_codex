## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE |
| **Slice scope** | simple metric; free \(\rho\propto r^\alpha\) and free \(A=1-c r^p\); readout character only |
| **Observing or targeting?** | **OBSERVE** — continuous character map; no winner; no χ²; no survey fit |
| **Comparator scaffolds** | none |
| **Verifier status** | SELF-SCRIPT `python3 simple_metric_S6_deeper_census.py` |
| **Build-on grade** | **LEAD** (structure map of continuum space) |
| **Re-run commands** | `python3 simple_metric_S6_deeper_census.py` |

### Premise ledger

| Item | Tag | Enters claim? |
|------|-----|---------------|
| MS \(m'=4\pi r^2\rho\), \(A=1-2m/r\) | GR-form geometric on simple metric | Y |
| Power-law / power-lapse probes | **free-and-explored** | Y as census |
| Full light / \(D_A=r\) | DERIVED readout | Y character |
| Preferred \(\alpha\) or \(p\) | — | **N** |

### What is NOT claimed

- A preferred density exponent or macro law.
- BAO/SNe agreement for any tile.
- R1 EL agreement.

### Do not build on

- Using low-\(z\) power or BAO ratios to “pick the right” \(p\).

---

# S6 — Deeper free continuum census

**Prior:** S5 tile census after scar.  
**This tile:** denser free families; structure map of what changes together.

---

## Lay summary

We scanned **many** allowed continuum fills (not one profile):

- densities like \(\rho \propto r^\alpha\) for a range of \(\alpha\);
- lapses like \(A = 1 - c\, r^p\) for a range of \(p\).

**What the space is doing (pattern, not a pick):**

1. **Walls are always critical** — whenever \(A\) dies at finite size \(X\), mass is \(X/2\). No exception in the scan.  
2. **How matter is piled near the center** sets the low-redshift light law (soft \(\sqrt{z}\) vs linear \(z\) vs in between).  
3. **Tangential stress tracks the same shape** — \(p_\perp/\rho\) is fixed by the profile, not an extra free fluid knob.  
4. **BAO distance shape** (how \(D_M\) grows with \(z\)) **differs by tile** when you normalize the same way — useful later as a character probe, **not** used here to crown a winner.

Still exploring. Still no mechanism.

---

## 1. Free \(\rho = \rho_0 r^\alpha\)

MS integrate; edge when \(A\le 0\).

| \(\alpha\) | Edge often? | Typical low-\(z\) \(d_L\sim z^{P}\) when edged | \(p_\perp/\rho\) (mid, sample) |
|-----------:|:------------|-----------------------------------------------:|-------------------------------:|
| \(-1.5\) | often | (noisy near center) | \(\sim -0.25\) |
| \(-1\) | yes | \(\mathbf{P\sim 1.01}\) | \(\sim -0.5\) |
| \(-0.5\) | yes | \(P\sim 0.68\) | \(\sim -0.75\) |
| \(0\) (const) | yes if dense enough | \(\mathbf{P\sim 0.51}\) | \(\sim -1\) |
| \(+0.5\) | yes | \(P\sim 0.41\) | \(\sim -1.25\) |
| \(+1\) | yes | \(P\sim 0.34\) | \(\sim -1.5\) |
| \(+2\) | yes | \(P\sim 0.26\) | \(\sim -2\) |

At every recorded edge: **\(m/(X/2) \approx 1\)** (critical close identity, numeric).

**Continuous map:** more central density weight (more negative \(\alpha\)) → stiffer low-\(z\) light; emptier center (positive \(\alpha\)) → softer than \(\sqrt{z}\).

---

## 2. Free \(A = 1 - c\, r^p\)

Exact family: edge at \(X = c^{-1/p}\), always \(M=X/2\).

\[
\rho \propto r^{p-2},\qquad
\frac{p_\perp}{\rho} = -\frac{p}{2}
\quad\text{(CAS/numeric mid-point)}
\]

| \(p\) | \(\rho\) center | low-\(z\) \(P\) | \(p_\perp/\rho\) |
|------:|-----------------|---------------:|-----------------:|
| \(1\) | \(\propto 1/r\) (linear-type) | \(\sim 1.01\) | \(-1/2\) |
| \(2\) | const | \(\sim 0.51\) | \(-1\) |
| \(3\) | \(\propto r\to 0\) | \(\sim 0.34\) | \(-3/2\) |
| \(4\) | \(\propto r^2\to 0\) | \(\sim 0.26\) | \(-2\) |

Same map as the \(\alpha = p-2\) density line. **One continuous family**, two coordinatizations (\(\rho\) or \(A\)).

Former “linear ceiling” = **\(p=1\) slice**. Former “const density ball” = **\(p=2\) slice**. Neither is selected — both are coordinates on the same map.

---

## 3. BAO \(D_M\) shape character (no survey data)

Identity: \(D_M = r(1+z) = r/\sqrt{A}\).  
Report **ratios** \(D_M(z)/D_M(0.5)\) so overall scale drops out.

| Tile | \(D_M(0.2)/D_M(0.5)\) | \(D_M(1)/D_M(0.5)\) | \(D_M(1.5)/D_M(0.5)\) |
|------|----------------------:|--------------------:|----------------------:|
| linear \(p=1\) (T3) | **0.440** | **1.80** | **2.52** |
| quadratic \(p=2\) | 0.593 | 1.55 | 2.05 |
| power \(p=3\) | 0.655 | 1.47 | 1.91 |
| const-\(\rho\) MS sample | 0.593 | 1.55 | 2.05 |

T3 analytic \(D_M/X = z(z+2)/(1+z)\) matches the linear row.  
**Shapes are distinguishable** across the map — later multi-probe can *characterize* a slice; this tile does **not** fit BAO.

---

## 4. Structure map (orchestra-style)

| Knob in the space | What moves with it |
|-------------------|--------------------|
| Center concentration (\(\alpha\) or \(p\)) | low-\(z\) \(d_L\) power; BAO shape ratios |
| Overall density scale \(\rho_0\) or \(c\) | whether / where wall sits; **not** the shape class at fixed \(p\) |
| Hitting the wall | forces critical \(M=X/2\) |
| Stress anisotropy | locked to \(p\): \(p_\perp/\rho = -p/2\) on power-lapse family |

**Not free in this continuum:** independent \(p_r\) (always \(-\rho\)); independent “dust switch.”

---

## 5. Still open / still refused

| Open | Refused |
|------|---------|
| Which slice (if any) is native from a full UDT action | Picking \(p=1\) for SNe-ish linear low-\(z\) |
| A-primary EL solution space depth | Adding a term so R1 hosts a chosen \(p\) |
| Data character of BAO/SNe **after** slice is theory-selected | χ²-shopping \(p\) |

---

## One-line

**Free continuum space is a continuous map: center pile-up sets low-\(z\) and BAO shape, every wall is critical \(M=X/2\), anisotropy tracks the same map — \(p=1\) and \(p=2\) are slices, not winners; no mechanism, no selection.**
