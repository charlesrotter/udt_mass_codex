## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE (center regularity vs residual re-centering) |
| **Source** | External third pass (sharper); Charles-relayed |
| **Local check** | SymPy expansion \(A=1+br+cr^2\); \(A'(0)\) on residual family |
| **Build-on grade** | **DERIVED** mutual exclusion · **FORK** for Charles (axiom scope of re-centering) |
| **Siblings** | `simple_metric_WR_L_center_nogo_atlas_results.md` · `simple_metric_WR_L_center_invariants_second_pass_results.md` |

### Premise ledger

| Premise | Tag |
|---------|-----|
| Simple reciprocal metric | THEORY |
| Residual re-centering functional equation (no residual throne) | **WR-L axiom** (global vs wall-asymptotic = fork) |
| Wall package \(\alpha=1\) | CANON WR-L |
| Center-regular = finite \(R,K\) at \(r=0\) | DERIVED geometry criterion |
| Imported core/cutoff | NOT used |

---

# Residual re-centering and center regularity are mutually exclusive

## Upgrade from prior pass

Second pass tagged “\(A=1-r/X\) down to \(r=0\)” as **CHOSE extrapolation** (WR-L silent at wall-only).

**This pass sharpens:** if residual re-centering holds as an **exact global** residual form, the center singularity is **forced**, not a free inward paint job.

\[
\boxed{\text{residual re-centering}\ \bot\ \text{center regularity}}
\quad\text{(on the simple reciprocal areal chart).}
\]

---

## 1. Center-regularity criterion (general \(A\))

Near \(r=0\):

\[
A(r)=1+b r+c r^2+\cdots,\qquad b=A'(0).
\]

Full-nonlinear CAS (local + external):

\[
R=-\frac{6b}{r}-12c+\cdots,\qquad
K=\frac{8b^2}{r^2}+\cdots.
\]

(Local: \(R\) series matches; \(K\) leading \(8b^2/r^2\).)

Therefore:

\[
\boxed{\text{center-regular}\ \Longleftrightarrow\ A'(0)=0\ \Longleftrightarrow\ A=1+O(r^2).}
\]

Then \(R(0)=-12c\), \(K\) finite (quadratic core). Linear cusp \(b\neq0\) ⇒ \(R,K\to\infty\).

---

## 2. Residual family never center-regular

Re-centering forces (WR-L Step 1):

\[
\frac{r}{X}=1-A^{s}\quad\Leftrightarrow\quad A=\Bigl(1-\frac{r}{X}\Bigr)^{\alpha},\quad\alpha=\frac1s.
\]

\[
A'(0)=-\frac{\alpha}{X}\neq 0\quad(\alpha>0).
\]

(Local: \(\lim_{r\to0}A'=-\alpha/X\); re-center form \(A'|_{0}=-1/(Xs)\).)

\[
\boxed{\text{No member of the residual re-centering family is center-regular.}}
\]

Wall package picking \(\alpha=1\) does not create a center-regular option inside the family — **there is none**.

The functional solution is **rigid**: it cannot produce \(A'(0)=0\) while remaining residual-recentered with finite wall \(X\).

---

## 3. Structural price

\[
\boxed{
\text{``No residual throne'' / residual re-centering exact globally}
\Rightarrow
A'(0)\neq 0
\Rightarrow
\text{center curvature singularity.}
}
\]

The singularity is the **price of re-centering**, structurally — not an optional paint accident at the origin.

**Prior CHOSE tag revised (scope):**

| Claim | Old tag | New tag |
|-------|---------|---------|
| Wall form from WR-L wall package | DERIVED | DERIVED (unchanged) |
| Global exact residual form including seat | framed as silent/CHOSE extrapolation | **If re-centering is exact globally → singularity FORCED** |
| Re-centering only wall-asymptotic | — | **Fork (B)** — then regular core possible, WR-L = exterior |

---

## 4. Fork (Charles ruling — axiom question)

### (A) Re-centering exact (global residual form)

Center = genuine reachable curvature singularity.  
Macro L-metric **cannot** be literal vacuum at \(r=0\): either \(r=0\) is excised (always local “matter”/non-vacuum readout), or the observer never sits at exact \(\phi=0\).

### (B) Re-centering wall-asymptotic only

May relax near center → regular quadratic core \(A=1+O(r^2)\) permitted.  
Then WR-L derives the **exterior/wall** form; \(A=1-r/X\) is **not** the whole line.

**Not for the external model to pick** — axiom / ontology scope.

---

## 5. Structural rhyme: c-edge and center

| End | Failure mode |
|-----|----------------|
| Wall \(\phi\to\infty\) | historical \(c\)-edge / bulk self-quench issues; optical wall is separate success under WR-L |
| Center \(\phi\to0\) | re-centering forces \(A'\neq0\) cusp |

Shared character (external note — **lead**, not theorem):

\[
\boxed{
\text{Pure vacuum L-form is a clean }exterior\text{ that does not self-supply the matter content it needs at either end.}
}
\]

Honest character of “the one”: exterior residual metric, not a global vacuum on \([0,X]\).

---

## 6. Relation to atlas pass

Atlas (re-centering ≠ manifold coord transform) remains compatible with **(A)** if seats are residual charts with punctured diagonals, or with **(B)** if only wall asymptotics recenter.

Mutual exclusion is the sharper **global SSS + exact re-centering** theorem; atlas is the multi-seat consistency story.

---

## Status tags

| Claim | Tag |
|-------|-----|
| Center-regular \(\Leftrightarrow A'(0)=0\) | **DERIVED** |
| Residual family \(\Rightarrow A'(0)\neq0\) | **DERIVED** |
| Re-centering exact \(\bot\) center-regular | **DERIVED** |
| Fork (A) vs (B) | **OPEN — Charles** |
| “Clean exterior, not global vacuum” | **LEAD / character** (not canon) |

---

## One-line

**Exact residual re-centering forbids a smooth center (\(A'(0)\neq0\) for the whole family); the center singularity is structural, not optional paint — Charles must rule whether re-centering is global (A) or wall-asymptotic (B).**

---

## Related: EOS power window (same day)

**`simple_metric_EOS_power_window_dS_results.md`** — different family \(A=1-(r/X)^\beta\). Under CHOSE \(p_t=w\rho\)+DEC, only \(w=-1\) (dS) is regular at center *and* wall. L is singular \(\beta=1\). Does **not** replace re-centering exclusion; offers optional Charles path (macro dS + L as boundary member / fork B).

