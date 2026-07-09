## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE (multi-step; metric-led) |
| **Frame** | `UDT_NATURE_LEAN_FRAME.md` |
| **Slice scope** | reciprocal metric + Einstein/MS; filled vs local rooms; hyp J1; star-like C1 |
| **Observing or targeting?** | OBSERVE where metric leads — no SNe shop |
| **Build-on grade** | **LEAD** (room structure + characters) |
| **Re-run** | `python3` session → `simple_metric_rooms_filled_local_out.json` |

### Premise ledger

| Item | Tag |
|------|-----|
| Simple reciprocal metric | THEORY |
| Einstein/MS continuum | E-room working lean |
| J1 for filled hyp sheet | CHOSE working |
| Quartic star ansatz | free-and-explored example family |
| Hyperbolic reach | POSTULATE + derived form |

### What is NOT claimed

- Cosmology = filled hyp. Stars = quartic. Canon joins.

---

# Rooms, filled character, local stars — metric-led continuation

Four steps in one push under the nature lean (no pause for “continue”).

---

## STEP 1 — Two rooms (shared geometry, different global structure)

**Shared (forced on E-room reciprocal continuum):**

- Metric: \(A=e^{-2\phi}\)
- \(p_r=-\rho\) always  
- \(m=r(1-A)/2\)

| Room | Definition | Exterior Schw? | Global reach \(X\)? |
|------|------------|----------------|---------------------|
| **Filled cosmos** | \(A\to0\) at finite \(r_{\mathrm{wall}}\); domain ends at wall; \(M=r_{\mathrm{wall}}/2\) | No \(C^1\) match for ceiling-type fills | Natural home |
| **Local mass** | Vacuum exterior \(A=1-r_s/r\), \(A\to1\) at \(\infty\); mass \(r_s/2\) | Yes (by construction) | Not required |

**Metric-led moral:** one reciprocal geometry, **two solution-space rooms**. Do not force ceiling continua to wear star clothes.

---

## STEP 2 — Filled room character sheet (hyperbolic J1)

Working character (not crowned by data):

\[
A=\frac{X-x}{X+x},\quad
m=\frac{x^2}{X+x}\to\frac{X}{2},\quad
1+z=\sqrt{\frac{X+x}{X-x}}
\]

\[
\rho=\frac{2X+x}{4\pi x(X+x)^2},\quad
p_r=-\rho,\quad
\frac{p_t}{\rho}=-\frac{X^2}{2X^2+3Xx+x^2}
\]

Distances (\(D_A=x\), full light), \(u=1+z\):

\[
\frac{D_A}{X}=\frac{u^2-1}{u^2+1},\quad
\frac{D_M}{X}=\frac{u^3-u}{u^2+1},\quad
\frac{d_L}{X}=\frac{u^4-u^2}{u^2+1}
\]

Low-\(z\): \(d_L/X = z + \tfrac32 z^2 + O(z^3)\) — **linear Hubble** (good character).

| \(z\) | \(x/X\) | \(D_M/X\) | \(d_L/X\) |
|------:|--------:|----------:|----------:|
| 0.1 | 0.095 | 0.105 | 0.115 |
| 0.5 | 0.385 | 0.577 | 0.865 |
| 1.0 | 0.600 | 1.200 | 2.400 |
| 2.0 | 0.800 | 2.400 | 7.200 |

Proper distance to wall: \(\ell/X\to 1+\pi/2\) (**finite**). Unattainability remains **compositional**.

---

## STEP 3 — Local room: star-like match under \(p_r=-\rho\)

### Algebra fallout (important)

On the reciprocal metric,
\[
\rho\propto\frac{1-A-rA'}{r^2}.
\]
Vacuum exterior match **\(C^1\)** requires \(A(R)=1-r_s/R\) and \(A'(R)=r_s/R^2\), which is exactly
\[
1-A(R)-R A'(R)=0 \quad\Leftrightarrow\quad \rho(R)=0.
\]

**Theorem (this slice):** \(\rho(\mathrm{surface})=0\) ⇔ \(C^1\) match to Schw exterior.

### Const-density MS on reciprocal

\(A=1-kr^2\) has \(\rho=\mathrm{const}\neq0\) at surface ⇒ **cannot \(C^1\)-match**.  
\(C^0\) mass match works; \(A'\) jumps (\(A'_-=-2kR\), \(A'_+=+kR\)) — Israel-type shell if idealized.  
(Different from textbook GR interior metric, which is **not** reciprocal.)

### Explicit shell-free family (observe, not unique)

\[
A=1-\alpha r^2+\beta r^4,\quad
\beta=\frac{3\alpha}{5R^2}
\quad(\Rightarrow\rho(R)=0\Rightarrow C^1\text{ auto}).
\]

Samples \(R=1\):

| \(\alpha\) | \(A(R)\) | \(r_s\) | \(A_{\min}\) |
|-----------:|---------:|--------:|-------------:|
| 0.5 | 0.80 | 0.20 | 0.79 |
| 1.0 | 0.60 | 0.40 | 0.58 |
| 1.5 | 0.40 | 0.60 | 0.38 |
| 2.0 | 0.20 | 0.80 | 0.17 |

**Local room lives** on this metric with honest continuum. Filled ceiling family remains the other room.

---

## STEP 4 — Synthesis (where the metric took us)

```
                    simple reciprocal metric
                              |
              +---------------+---------------+
              |                               |
        FILLED COSMOS                      LOCAL MASS
        A→0 at finite wall                 exterior Schw
        M = r_wall/2                       m_surface = rs/2
        reach X natural                    no global X needed
        hyp J1 = working character         C1 ⇔ ρ_surface=0
        (J1 CHOSE)                         quartic family exists
              |                               |
              +------ do not cross-dress -----+
```

| Lead | Status |
|------|--------|
| Nature lean skeleton (reach, reciprocity, closure) | reinforced |
| J1 | still CHOSE working for filled scale lock |
| Continuum shopping \(p\) | still refused as driver |
| Native action | still OPEN |
| Which room is “the cosmos” | OPEN — metric allows both |

---

## One-line

**The reciprocal metric supports two clean rooms—filled critical walls (macro reach home) and local Schw-matched stars (C1 iff surface density vanishes)—with hyperbolic J1 a working filled character and const-ρ reciprocal “stars” needing a shell for C1; no cross-dressing, no fit shopping.**
