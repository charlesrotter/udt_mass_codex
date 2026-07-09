## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | MAP / DERIVE (Einstein + barotropic tangential EOS scan) |
| **Source** | External closed-form pass (Charles-relayed); unifies c-edge + center “window” |
| **Local check** | SymPy full nonlinear on \(A=1-(r/X)^\beta\) — Einstein faces, \(R\), \(p_t/\rho\) |
| **Build-on grade** | **DERIVED within CHOSE EOS closure** · **NOT** WR-L re-centering family · **NOT** Charles-canon macro |
| **Observing or targeting?** | OBSERVE solution space of reciprocal + Einstein + \(p_t=w\rho\); flag window point |

### Premise ledger

| Premise | Tag |
|---------|-----|
| Simple reciprocal metric | THEORY |
| Einstein readout \(G^\mu{}_\nu\) continuum | CHOSE / working continuum language (not native UDT source) |
| \(p_r=-\rho\) automatic on reciprocal SSS | **DERIVED** (identity on this metric class) |
| \(p_t=w\cdot\rho\) barotropic tangential | **CHOSE** (minimal closure for scan) |
| DEC / causality \(|p_t|\le\rho\) \(\Rightarrow\) \(w\ge -1\) (for \(\rho>0\)) | **CHOSE** regularity/energy condition (common; not UDT-derived) |
| Residual re-centering / WR-L family \(A=(1-r/X)^\alpha\) | **Different family** — do not conflate |
| de Sitter as macro canon | **NOT assumed** — Charles ruling OPEN |

---

# EOS power family: window collapses to \(w=-1\) (de Sitter)

## 0. Two families — do not mix

| Family | Form | Provenance |
|--------|------|------------|
| **Residual re-centering (WR-L)** | \(A=(1-r/X)^\alpha\) | no residual throne + wall package → \(\alpha=1\) ⇒ L |
| **EOS power (this tile)** | \(A=1-(r/X)^\beta\) | reciprocal + Einstein + \(p_t=w\rho\) |

They **agree only at L**: \(\alpha=1\) and \(\beta=1\) both give \(A=1-r/X\).

They **disagree at de Sitter**:  
\(A=1-(r/X)^2\) \(\neq\) \((1-r/X)^2\).

This tile **does not** derive de Sitter from WR-L re-centering. It derives a **window point inside the EOS power family**.

---

## 1. Closed form (CAS verified)

Reciprocal SSS ⇒ \(G^t{}_t=G^r{}_r\) ⇒ **\(p_r=-\rho\) automatic** (Einstein readout convention).

Impose \(p_t=w\rho\) (**CHOSE**). System closes on:

\[
\boxed{A(r)=1-\Bigl(\frac{r}{X}\Bigr)^{\beta},\qquad \beta=-2w.}
\]

Local check: \(p_t/\rho=-\beta/2=w\) exactly; \(p_r/\rho=-1\).

| Member | \(\beta\) | \(w\) | \(A\) |
|--------|-----------|-------|-------|
| **L** | 1 | \(-1/2\) | \(1-r/X\) |
| **de Sitter** | 2 | \(-1\) | \(1-r^2/X^2\) |

---

## 2. Center curvature (full nonlinear)

\[
R=(\beta+1)(\beta+2)\,\frac{r^{\beta-2}}{X^\beta}.
\]

(Local: exact match to Einstein-trace convention used in prior center docs.)

**Center-regular** (finite \(R\) at \(r=0\)):

\[
\boxed{\beta\ge 2\qquad\Leftrightarrow\qquad w\le -1.}
\]

**Correction to prior \(A'(0)\) heuristic:** fractional powers can have \(A'(0)=0\) or \(\infty\) depending on \(\beta\); the invariant criterion is \(\beta\ge 2\), not merely “linear cusp.”

- L (\(\beta=1\)): \(R=6/(Xr)\) — singular (matches prior center passes).  
- dS (\(\beta=2\)): \(R=12/X^2\), \(\rho=3/(8\pi X^2)\) **uniform**, finite everywhere.

Kretschmann / regularity consistent with \(\beta\ge 2\) window for smooth center (external; L singular already banked).

---

## 3. Nested window → single point

| Condition | Requirement |
|-----------|-------------|
| Wall exists (c-like: \(A\to0\), ∞ optical, finite proper, finite wall \(G^\theta{}_\theta\)) | broad: \(w<0\) (\(\beta>0\)) |
| Wall + **regular** center | \(\beta\ge 2\) \(\Rightarrow\) \(w\le -1\) |
| + DEC / \(|p_t|\le\rho\) | \(w\ge -1\) (for \(\rho>0\)) |

**Intersection:**

\[
\boxed{w=-1\text{ alone.}}\qquad
A=1-\frac{r^2}{X^2},\quad
\rho=\frac{3}{8\pi X^2},\quad
R=\frac{12}{X^2},\quad
\Lambda=\frac{3}{X^2}\ \text{(if identified).}
\]

The “narrow window” is a **point** — the cosmological-constant / static de Sitter member.

**Honest caveat (external + banked):** uniqueness of \(w=-1\) is derived **within** the CHOSE \(p_t=w\rho\) closure (+ DEC).  
de Sitter’s specialness is also available closure-independently (unique maximally symmetric static metric with a horizon) — so “regular c-edge ⟹ dS/\(\Lambda\)” can be argued more robustly than the EOS scan alone; still **not** UDT-native forced without Charles.

---

## 4. Unification story (character — LEAD)

| Object | Role under this scan |
|--------|----------------------|
| L (\(w=-1/2\)) | **Below** regular window — linear/marginal; center singular (matches re-centering exclusion on L) |
| dS (\(w=-1\)) | Unique regular wall+center+DEC point |
| Old bulk \(c\)-edge self-quench | Source \(\propto e^{-2\phi}\) dies as \(\phi\to\infty\); **\(\Lambda\)-type density is \(\phi\)-independent** — can hold edge open |

Shared character (LEAD, not theorem): pure L vacuum exterior does not self-supply regular matter at both ends; the EOS window’s only regular point is \(\Lambda\).

---

## 5. Relation to WR-L / center forks

| Prior | Interaction |
|-------|-------------|
| WR-L \(A=1-r/X\) from re-centering + wall | **Unchanged as residual form** — this tile is a different closure |
| Re-centering ⊥ center regularity (global residual family) | Compatible: L singular; residual family \(\neq\) dS |
| Fork (A) global re-centering | Still open; L remains singular under (A) |
| Fork (B) re-centering wall-asymptotic / exterior L | External **recommends** pairing with dS interior/edge if Charles adopts \(\Lambda\) macro |

**External’s proposed ruling (for Charles, not auto-adopted):**

> Macro sector = de Sitter causal horizon with \(\Lambda=3/X^2\); L reread as linear/singular boundary member of the EOS scan, not the physical regular interior; that also picks center fork (B).

**Repo status until Charles rules:** **LEAD / MAP**. Do **not** demote WR-L or promote \(\Lambda\) to CANON from this tile alone.

---

## 6. Imposition / purity audit

| Check | Result |
|-------|--------|
| CHOSE EOS \(p_t=w\rho\) surfaced? | **Yes** |
| Einstein continuum as UDT native source? | **Not claimed** — readout language |
| Solution-space scan vs target dS? | Scan collapses to a point — still rides CHOSE barotropic + DEC |
| Residual re-centering used to force dS? | **No** — different family |
| Mechanism shopping? | No particle core; \(\Lambda\) emerges as window point under stated CHOSE |

---

## Status tags (binding)

| Claim | Tag |
|-------|-----|
| \(A=1-(r/X)^\beta\), \(\beta=-2w\) under reciprocal+Einstein+\(p_t=w\rho\) | **DERIVED** (within CHOSE EOS) |
| Center-regular \(\Leftrightarrow\beta\ge 2\) in this family | **DERIVED** |
| Window \(\cap\) DEC = \(\{w=-1\}\) | **DERIVED** (within CHOSE EOS+DEC) |
| L is singular / below window | **DERIVED** (consistent with prior center docs) |
| Macro = dS / \(\Lambda=3/X^2\) | **OPEN — Charles** |
| L demoted to “boundary member only” | **OPEN — Charles** |
| Unifies c-edge fail story | **LEAD character** |

---

## One-line

**Under CHOSE \(p_t=w\rho\) + DEC on reciprocal Einstein, the wall+regular-center window is the single point \(w=-1\) (static de Sitter); L is the singular \(\beta=1\) member — not a re-centering derivation of \(\Lambda\), and not canon until Charles rules.**
