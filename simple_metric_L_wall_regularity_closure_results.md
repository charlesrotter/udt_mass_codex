## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE (principle-closure via accepted wall package) |
| **Source** | Charles sharper attack + **Charles accepts wall conditions** (session) |
| **Verification** | CAS/numeric — `simple_metric_L_wall_regularity_closure_out.json` |
| **Build-on grade** | **DERIVED** under package **WR-L** (below) — not free chart / not SNe-selected |
| **Prior** | `simple_metric_L_equivalence_principle_GAP.md` · bare NPC attack FAIL |

### Premise ledger

| Item | Tag |
|------|-----|
| Simple reciprocal metric, \(A=e^{-2\phi}\) | THEORY (R1–R3 / simple metric) |
| Additive \(\phi\), multiplicative \(A\) | THEORY |
| Finite areal wall radius \(X\), \(A(0)=1\) | WORKING (\(x_{\max}\)) |
| Affine areal re-centering: \(r'=r-r_0\), \(X'=X-r_0\) | **WR-L axiom** (residual re-centering / no residual throne) |
| Wall package: ∞ optical, finite proper, finite \(G^\theta{}_\theta\) at wall | **WR-L axioms** — **Charles accepts** (2026-07-09) |
| Observing or targeting? | DERIVE selection inside residual family |

---

# WR-L — wall-regular residual selector

**Named package (Charles-accepted axioms + residual re-centering):**

\[
\boxed{
\text{R1–R3 + residual re-centering + WR-L wall regularity}
\Rightarrow
A=1-r/X.
}
\]

### WR-L conditions

1. **Residual composition / re-centering**  
   \(A_{12}=A_1A_2\), and no residual throne (affine areal re-center: \(r'=r-r_0\), \(X'=X-r_0\)) gives the family  
   \[
   A=\Bigl(1-\frac{r}{X}\Bigr)^{\alpha}.
   \]

2. **Finite proper room**  
   \[
   \ell=\int\frac{dr}{\sqrt{A}}<\infty.
   \]

3. **Infinite optical reach**  
   \[
   \ell_{\mathrm{opt}}=\int\frac{dr}{A}=\infty.
   \]

4. **No curvature/shell singularity at the wall**  
   \[
   G^\theta{}_\theta=\tfrac12 A''+\frac{A'}{r}
   \]
   remains finite as \(r\to X\).

---

## Step 1 — Family from residual re-centering

With \(u=r/X=F(\phi)\), \(F(0)=0\), \(F(\infty)=1\), re-centering forces
\[
F(\phi_0+\Delta\phi)=F(\phi_0)+\bigl(1-F(\phi_0)\bigr)F(\Delta\phi).
\]

**C¹ solutions:** \(F(\phi)=1-e^{-\lambda\phi}\) (\(\lambda>0\)).  
Since \(A=e^{-2\phi}\):
\[
\boxed{\frac{r}{X}=1-A^{s},\qquad s=\frac{\lambda}{2}}
\quad\Leftrightarrow\quad
\boxed{A=\Bigl(1-\frac{r}{X}\Bigr)^{\alpha},\quad\alpha=\frac1s}.
\]

**L** is \(s=\alpha=1\): \(r/X=1-A\).

---

## Step 2 — Wall tests select \(\alpha=1\)

Near the wall \(\varepsilon=1-r/X\to0^+\), \(A=\varepsilon^{\alpha}\):

| Condition | Requirement |
|-----------|-------------|
| Infinite optical wall | \(\alpha\ge 1\) |
| Finite proper wall | \(\alpha<2\) |
| Finite \(A''\) / \(G^\theta{}_\theta\) | inside \(1\le\alpha<2\), only \(\alpha=1\) (pref. of \(A''\propto\alpha(\alpha-1)\varepsilon^{\alpha-2}\) vanishes) |

- \(\alpha\ge2\): proper distance diverges.  
- \(1<\alpha<2\): optical+proper OK; **curvature blows up** at wall.  
- \(\alpha=1\): only point with **all three**.

\[
\boxed{\alpha=1\ \Rightarrow\ A=1-\frac{r}{X}\ \Leftrightarrow\ \frac{r}{X}=1-A.}
\]

Verified: FE for \(F\); \(A''=0\) only at \(\alpha=1\) in the band; numeric max\(|A''|\) on truncated grid zero only at \(\alpha=1\).

---

## Step 3 — Stress and P-opt are consequences (not hinges)

Once L is selected by WR-L:

\[
A=1-\frac{r}{X}
\quad\Rightarrow\quad
p_t=-\frac{\rho}{2}
\quad\text{(Einstein readout on reciprocal metric)},
\]

\[
A=1-\frac{r}{X}
\quad\Rightarrow\quad
\frac{dr}{A}=2X\,d\phi
\quad\text{(P-opt with }\kappa=2X\text{)}.
\]

The old equivalence triangle is **anchored** by WR-L; \(S_r=S_A\) is a **theorem** (\(S_r=A^\alpha\) equals \(A\) iff \(\alpha=1\)), not a taste.

| Face | Role under WR-L |
|------|------------------|
| WR-L wall package + re-centering | **Selector** (accepted axioms) |
| \(p_t=-\rho/2\) | **Consequence / dual confirmation** |
| P-opt \(\mathrm{d}r/A=\kappa\mathrm{d}\phi\) | **Consequence / dual confirmation** |
| \(S_r=S_A\) | **Theorem** on L |

---

## Status tag (binding wording)

\[
\boxed{\text{DERIVED from simple metric + residual composition + accepted wall-regularity axioms (WR-L).}}
\]

**Not:** SNe-selected · stress-ratio slogan · free chart shopping · forced by bare R1–R3 alone.

**Honest scope:** L is forced **inside** the residual family once WR-L axioms are admitted. Charles accepts those wall conditions (2026-07-09). Not automatic from metric + \(\phi\)-additivity without the re-centering and wall package.

### What remains open (not L form)

- Absolute scale \(X\) / one ruler.  
- Center regularity (\(\rho\sim1/r\) continuum face) — separate from **wall** regularity.  
- Time-live residual dynamics; high-\(z\) BAO character.  
- Full Charles **canon line** in `CANON.md` if/when he wants that ledger entry (form is already DERIVED under WR-L).

---

## Relation to prior FAIL

Bare NPC-1 + vague “survival” without areal subtraction → **FAIL** (does not force L).  
**WR-L:** residual re-centering → family; wall package → \(\alpha=1\) → L.

---

## One-line

**WR-L (residual re-centering + finite proper + infinite optical + regular wall curvature) selects \(A=1-r/X\); stress and P-opt become duals — DERIVED under Charles-accepted WR-L, not bare R1–R3 alone.**
