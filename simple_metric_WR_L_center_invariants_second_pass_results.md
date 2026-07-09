## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE (center invariants — second independent external pass) |
| **Source** | External (Grok-class) full-nonlinear SymPy on \(A=1-r/X\); Charles-relayed |
| **Local check** | SymPy: \(R\), \(8\pi\rho\), Kretschmann formula for reciprocal SSS, \(\alpha\)-family limits |
| **Build-on grade** | **DERIVED** invariants · superseded-in-part by re-center exclusion pass |
| **Sibling** | `simple_metric_WR_L_center_nogo_atlas_results.md` (first external + atlas fork) |

### Premise ledger

| Premise | Tag |
|---------|-----|
| Simple reciprocal metric | THEORY |
| WR-L \(A=1-r/X\) as **wall-selected residual form** | CANON C-2026-07-09-1 |
| Exact static φ-only \(A=1-r/X\) **all the way to \(r=0\)** | see **re-center exclusion** (forced if re-centering global) |
| Full nonlinear curvature (no linearization) | METHOD |
| Imported core/cutoff/particle/SNe | NOT used |

---

# Second pass: invariants + WR-L scope at the center

## Verdict (external, adopted)

\[
\boxed{(1)\ \text{true curvature singularity as-written}\ +\ (3)\ \text{WR-L never derived the center.}}
\]

\[
\boxed{\text{Definitely NOT (2) coordinate / readout artifact.}}
\]

---

## 1. Invariants on \(A=1-r/X\) (full nonlinear)

Local SymPy + external agree:

| Object | Value on L |
|--------|------------|
| \(G^t{}_t=G^r{}_r\) | \(-2/(Xr)\) |
| \(8\pi\rho\) (Einstein readout \(\rho=-G^t{}_t/(8\pi)\)) | \(2/(Xr)\) \(\Rightarrow\) \(\rho=1/(4\pi Xr)\) |
| Ricci scalar \(R\) (trace convention \(R=-G^\mu{}_\mu\)) | \(6/(Xr)\) |
| Kretschmann \(K=R_{abcd}R^{abcd}\) | \(8/(X^2 r^2)\) |

All \(\to\infty\) as \(r\to0\).

**Kretschmann formula used (reciprocal SSS \(B=1/A\))** — checks Schwarzschild \(K=12 r_s^2/r^6\); on L:

\[
K=(A'')^2+\frac{2}{r^2}(A')^2+\frac{2}{r^4}(A-1)^2+\frac{4}{r^3}A'(A-1)=\frac{8}{X^2 r^2}.
\]

\(R\) and \(K\) are **frame scalars** ⇒ blow-up is geometry. **Kills (2).**

---

## 2. Reachable / naked (not wall-hidden)

\[
\int_0^{r_*}\frac{dr}{\sqrt{A}}<\infty\quad(r_*<X),\qquad A(0)=1.
\]

Singularity at **finite proper distance** from nearby seats; \(A\to1\) (not a horizon). Reachable / naked relative to the **wall** horizon at \(r=X\).

---

## 3. Generic to the whole power family

For \(A=(1-r/X)^\alpha\), \(\alpha>0\):

\[
\lim_{r\to0} r\,R=\frac{6\alpha}{X},\qquad
\lim_{r\to0} r^2 K=\frac{8\alpha^2}{X^2},\qquad
\lim_{r\to0} r\,G^t{}_t=-\frac{2\alpha}{X}.
\]

(Local SymPy limits confirmed.)

\[
\boxed{\text{No member of the residual family regularizes the center.}}
\]

Wall package picks \(\alpha=1\); it does **not** fix the center. \(\alpha\) is not a center knob.

---

## 4. Scope of WR-L (load-bearing honesty)

WR-L’s four conditions pin:

1. residual composition / re-centering → family,  
2. finite proper **wall**,  
3. infinite optical **wall**,  
4. finite curvature **at the wall**.

**None constrains \(r=0\).**

Therefore:

\[
\boxed{
\text{``}A=1-r/X\text{ down to }r=0\text{'' is the wall form extrapolated inward — CHOSE, not forced.}
}
\]

WR-L neither **derives** nor **forbids** a different near-center form.

**Division of labor:**

\[
\boxed{\text{WR-L is a wall selector, silent at the center.}}
\]

The \(1/r\) is the cost of pushing a wall-regularity form into a region it was never fitted to.

---

## 5. Forced vs open

| | |
|--|--|
| **FORCED** | *If* round-static φ-only \(A=1-r/X\) is exact to \(r=0\), the center is a genuine curvature singularity (\(R,K\to\infty\)), tension-type readout (\(p_r=-\rho\)), reachable. Not removable by re-charting; not an \(\alpha\) knob. |
| **OPEN** | Whether the exact interior *is* \(A=1-r/X\). Regularization requires the metric to **depart** from \(1-r/X\) near \(r=0\) — non-round / time-live / residual content WR-L does not supply. That is (3), recast: not “readout is wrong,” but “the round-static truncation cannot be the exact core.” |

On (4): metric forces a **division of labor** (wall vs center), not a particle.

Did **not** invent core/cutoff, particle, or touch SNe.

---

## 6. Reconciliation with first pass (atlas)

| First pass (`…center_nogo_atlas…`) | This pass |
|------------------------------------|-----------|
| Single-chart singularity **DERIVED** | Same, with full \(K=8/(X^2r^2)\) |
| Smooth \(A=1+O(r^2)\) | Same \(a_1\neq0\) |
| Re-centering ≠ manifold coord transform | Compatible (pair-chart / multi-seat) |
| WORKING lean: residual pair-chart, \(r>0\) | Compatible with **CHOSE extrapolation** story |
| Ontology fork OPEN | Same OPEN interior |

**Joint clean statement:**

\[
\boxed{
\text{WR-L forces the wall form; extending that form to }r=0\text{ is CHOSE;}
\text{ that extension is a true weak curvature singularity;}
\text{ the family cannot cure it; the center is outside WR-L’s mandate.}
}

\]

Both external passes agree: **not (2)**; **(1) as-written**; **(3) as scope**; atlas/pair-chart remains the best *interpretive* lean if one refuses a continuum seat point — still not ontology canon.

---

## One-line

**As-written static L to \(r=0\) is a real naked weak curvature singularity; WR-L never selected the center — inward extrapolation is CHOSE; no \(\alpha\) fixes it; regularization needs metric content beyond wall-only WR-L.**


---

## Superseding sharpness (same day, third pass)

**`simple_metric_WR_L_center_recenter_exclusion_results.md`**

If residual re-centering is **exact globally**, the center singularity is **FORCED** (\(A'(0)\neq 0\) for every family member) — not merely a CHOSE inward paint.  
Wall-only silence remains correct for the **wall package**; the re-centering axiom is what locks the cusp when taken globally. Fork (A)/(B) for Charles.
