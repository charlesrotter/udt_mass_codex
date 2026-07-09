## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE |
| **Slice scope** | simple metric; correct Einstein continuum after S3 scar; free A/ρ tiles; R1 contrast; readout character |
| **Observing or targeting?** | **OBSERVE** solution space — no unique selection; no χ² selector |
| **Comparator scaffolds** | none in solve |
| **Verifier status** | SELF-SCRIPT `python3 simple_metric_S5_reopened_space.py` |
| **Build-on grade** | **LEAD** (census / map of space) — not a preferred profile |
| **Re-run commands** | `python3 simple_metric_S5_reopened_space.py` |

### Premise ledger

| Item | Tag | Enters claim? |
|------|-----|---------------|
| Correct \(G\) (full curvature) | DERIVED (S4 reconcile) | Y |
| \(p_r=-\rho\) identity | DERIVED | Y |
| Probe \(A(r)\) / \(\rho\) tiles | **free-and-explored** | Y as census only |
| Full light / \(D_A=r\) readout | DERIVED when used | Y character only |
| Preferred ceiling for SNe | — | **N** |

### What is NOT claimed

- Any tile is *the* macro law.
- Linear ceiling uniqueness (withdrawn).
- R1 and Einstein already agree on a continuum.
- BAO/SNe fit.

### Do not build on

- Ranking tiles by residual.
- Restoring false \(p_r=0\) dust selection.

---

# S5 — Re-opened solution space (after scar)

**Prior:** S4 reconcile withdrew S3 dust uniqueness; identity \(p_r=-\rho\); critical \(M=X/2\) closes edge.  
**Question:** What continuum characters exist on the simple metric **without** false dust and without profile shopping?

---

## Lay summary

We put the metric back on the table with the **corrected** stress rules and asked only: **what kinds of solutions show up?**

Hard facts of the space (every solution):

1. Radial pressure is locked: **\(p_r = -\rho\)** (not a free “dust or not” choice).  
2. If the outer wall is “lapse dies” at size \(X\), total mass is **always** \(M=X/2\) (critical amount **closes** the sphere).  
3. Different density shapes give different centers and different walls — a **census**, not a winner.

The old favorite linear ceiling is **one tile**. Regular balls (soft low-\(z\)) are other tiles. Vacuum is another. The thin R1 action does **not** sit on the generic Einstein tiles.

No mechanism added. No χ² used to pick.

---

## 0. Structural identities (all \(A\))

\[
\rho=\frac{1-A-rA'}{8\pi r^2},\qquad
p_r=-\rho,\qquad
p_\perp=\frac{rA''+2A'}{16\pi r},\qquad
m=\frac{r}{2}(1-A)
\]

\[
A(X)=0 \;\Rightarrow\; m(X)=\frac{X}{2}
\quad\text{(critical amount closes)}
\]

---

## 1. Symbolic tile census

| Tile | \(A\) | \(\rho\) (sketch) | Center | Outer \(A=0\)? | R1 EL vs Einstein |
|------|-------|-------------------|--------|----------------|-------------------|
| T1 Schw vacuum | \(1-r_s/r\) | 0 | singular | horizon \(r_s\) | R1 vacuum **no** (\(\phi\) not Coulomb) |
| T2 flat | 1 | 0 | regular | no | R1 vacuum **yes** |
| T3 linear ceiling | \(1-r/X\) | \(\propto 1/r\) | \(A'(0)\neq0\) | **yes** at \(X\) | residual \(r\)-shaped **no** |
| T4 quadratic | \(1-a_2 r^2\) | **const** | regular | **yes** at \(1/\sqrt{a_2}\) | **no** |
| T5 quad+\(r^4\) | … | nearly const + … | regular | possible | **no** |
| T6 \(A=e^{-2q/r}\) | exp | nonzero Einstein ρ | \(A\to0\) at 0 | no finite outer root | R1 **kinetic** Coulomb (LHS=0) but **Einstein ρ≠0** — routes disagree |
| T7 power \(r^3\) | \(1-k r^3\) | \(\propto r\) | regular | **yes** | **no** |

### Characters that emerged

| Character | Where |
|-----------|--------|
| **Vacuum, no outer cosmic wall** | T2 flat; T1 is mass horizon not filled cosmos |
| **Filled wall + critical \(M=X/2\)** | Any tile that reaches \(A=0\) with \(m>0\) (T3, T4, T7, dense numeric probes) |
| **Regular center** \(A\to1,\,A'\to0\) | T2, T4, T5, T7 → low-\(z\) \(d_L\sim z^{1/2}\) class |
| **Linear-type center** \(A'(0)\neq0\) | T3 → low-\(z\) \(d_L\sim z\) class |
| **Isotropic \(p_\perp=p_r\)** | T4 quadratic: both \(=-\rho\) (const density-like) |
| **Anisotropic** \(p_\perp\neq p_r\) | T3: \(p_\perp=p_r/2\); T7 etc. |
| **R1 holds with Einstein ρ** | **Not** on generic sourced tiles; only trivial/special cases |

Numeric free-\(\rho\) probes (MS integrate): soft const ρ may miss edge; denser const / \(\rho\propto1/r\) **hit** \(A\le0\) at finite \(r\) — same S2 moral, under correct \(p_r=-\rho\).

---

## 2. Readout character (not selection)

Under \(D_A=r\), full light: \(d_L=(1+z)^2 r\), \(1+z=1/\sqrt{A}\).

| Tile class | Low-\(z\) \(d_L\) power (numeric character) |
|------------|-----------------------------------------------|
| Regular (quad) | \(\sim z^{0.50}\) |
| Linear ceiling | \(\sim z^{1.00}\) |

**BAO transverse (identity, any tile):**
\[
D_M = r(1+z) = \frac{r}{\sqrt{A}}
\]
Shape of \(D_M(z)\) is **profile-dependent**.  
Special case T3 only: \(D_M/X=z(z+2)/(1+z)\). That is **one** shape in the space — not promoted.

---

## 3. E-primary vs A-primary (still two maps of the space)

| Route | What the space contains |
|-------|-------------------------|
| **E-primary** | All \(A(r)\) (or \(\rho\)) above; stresses fixed by identities; walls when compactness hits 1 |
| **A-primary (R1+dust probe)** | EL \(Z(r^2\phi')'=2\rho r^2 A\); **does not** share generic E-tiles; joint solutions are a **thin** subset (flat; special series — S4) |

**No glue mechanism.** Census first.

---

## 4. What we refuse (imposition check)

| Move | Status |
|------|--------|
| Pick T3 because SNe residual ~0.91 | **Refuse** as selection |
| Restore \(p_r=0\) dust uniqueness | **Refuse** (false) |
| Add term so R1 hosts T3 | **Refuse** (mechanism) |
| Report T3 as one linear-center + ceiling tile | **OK** (characterize) |
| Report critical \(M\) closes wall | **OK** (identity) |

---

## 5. Program state

| Piece | Status |
|-------|--------|
| Continuum identities | **Bankable structure** (scar-corrected) |
| Solution-space census | **This tile** — open, multi-family |
| Unique native \(A(r)\) | **Still open** (not dust) |
| Critical mass closes edge | **Yes** (geometry) |
| Multi-probe | Formulas per tile; data compare **later**, not selector now |
| Next observe | Deeper free-\(\rho\) / free-\(A\) continuum (optional); or BAO **character compare** as observe-not-fit; or native action whose EL = Einstein |

---

## One-line

**Re-opened space: \(p_r=-\rho\) always; walls only with critical mass; many continuum tiles (regular soft vs linear-center ceiling vs vacuum); R1 does not sit on generic Einstein tiles — census only, no profile winner, no mechanism.**
