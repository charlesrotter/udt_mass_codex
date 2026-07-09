## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE (GR corpus mine) |
| **Slice scope** | Einstein–Hilbert static SSS; free \(\nu,\lambda\); reciprocity constraint \(\nu+\lambda=0\) |
| **Observing or targeting?** | OBSERVE action/EL fallout — not targeting glue to R1 |
| **Mine vein** | EH + constraint (from mine MAP next list) |
| **Verifier status** | SELF CAS |
| **Build-on grade** | **LEAD** |
| **Re-run** | `python3 simple_metric_mine_EH_constraint.py` |

### Premise ledger

| Item | Tag |
|------|-----|
| EH action on static SSS | GR mine |
| Reciprocity \(\nu+\lambda=0\) | UDT simple metric THEORY |
| Substitute-before-vary vs constrain-then-vary | method honesty |
| R1 action | contrast |

### What is NOT claimed

- EH+constraint is proven native UDT action.
- Multiplier dynamics with full matter sector complete.

---

# Mine pass — EH with free warps, then reciprocity constraint

**Prior mine:** SSS Einstein restrict → \(p_r=-\rho\), Schw vacuum ≠ Coulomb.  
**This vein:** same physics from the **action** side: when does a φ equation fall out?

---

## Lay summary

There are two ways to put “UDT reciprocity” into Einstein’s action:

**A. Substitute first**  
Write the metric already locked (\(\nu=-\phi\), \(\lambda=+\phi\)), *then* vary \(\phi\).  
**Fallout:** the bulk equation for \(\phi\) is **empty** (we already saw this in S9). The interesting vacuum condition is **lost** as a bulk EL — it hides in boundary/total-derivative structure.

**B. Vary free warps, then constrain**  
Vary both time-warp and radial-warp in EH, *then* demand \(\nu+\lambda=0\).  
**Fallout:** the two Euler–Lagrange expressions **agree** on that surface, and setting them to zero **recovers Schwarzschild-type vacuum** \(A=1+C/r\). A Lagrange multiplier can absorb the common value; the dynamics are Einstein’s equation on the reciprocal family.

So: **Einstein vacuum on the simple metric is real, but it is not “the EL you get by stuffing reciprocity into EH and varying φ.”**  
It **is** “Einstein’s variational problem with reciprocity as a constraint (or as on-shell restriction of the free SSS equations).”

That is why E-primary and “φ from EH” felt confusing — different order of operations.

---

## 1. Free static SSS EH (CAS)

Metric: \(ds^2=-e^{2\nu}dt^2+e^{2\lambda}dr^2+r^2 d\Omega^2\).

Reduced bulk density \(\propto e^{\nu+\lambda} r^2 R\) (angles stripped).

Vacuum EL (CAS):
\[
\begin{aligned}
\mathrm{EL}_\nu &\propto \bigl(2r\lambda' + e^{2\lambda}-1\bigr)\,e^{\nu-\lambda},\\
\mathrm{EL}_\lambda &\propto \bigl(-2r\nu' + e^{2\lambda}-1\bigr)\,e^{\nu-\lambda}.
\end{aligned}
\]

These are the standard vacuum Einstein content (equivalent to \(G^t{}_t=G^r{}_r=0\) up to factors). **Nontrivial** — free SSS EH is a real variational theory for two functions.

---

## 2. Substitute reciprocity into \(L\) first, then vary \(\phi\)

\[
\nu=-\phi,\;\lambda=+\phi
\quad\Rightarrow\quad
L=L(\phi),\;
\mathrm{EL}_\phi \equiv 0.
\]

**Fallout:** no bulk φ field equation from this order of operations (matches S9).  
You cannot recover Schw vacuum as “EL=0” this way; the vacuum condition is not that EL.

---

## 3. Restrict equations (or multiplier), do not substitute into \(L\) first

On the surface \(\lambda=-\nu\):
\[
\mathrm{EL}_\nu\big|_{\lambda=-\nu}
=
\mathrm{EL}_\lambda\big|_{\lambda=-\nu}
=
2-2(2r\nu'+1)e^{2\nu}.
\]

Difference is **zero** — multiplier consistency OK:
\[
L\supset \mu(r)\,(\nu+\lambda)
\quad\Rightarrow\quad
\mathrm{EL}_\nu+\mu=0,\;
\mathrm{EL}_\lambda+\mu=0
\]
compatible when \(\mathrm{EL}_\nu=\mathrm{EL}_\lambda\) on the surface.

Set \(\mathrm{EL}_\nu|_{\lambda=-\nu}=0\):
\[
(2r\nu'+1)e^{2\nu}=1.
\]
With \(A=e^{2\nu}\) (lapse factor; \(A=e^{-2\phi}\) when \(\nu=-\phi\)):
\[
A+rA'=1
\quad\Rightarrow\quad
\boxed{A=1+\frac{C}{r}}
\]
same Einstein vacuum as the tensor mine.

**Fallout:** constrained EH **does** select Schw-type vacuum on the reciprocal family — as **equations**, not as substituted-φ EL.

---

## 4. Dictionary (mine clarity)

| Procedure | What falls out |
|-----------|----------------|
| Free \(\nu,\lambda\) EH vary | Full SSS Einstein vacuum |
| Plug \(\nu=-\lambda\) into **equations** | Reciprocal Einstein package (E-map vacuum + continuum with matter) |
| Plug \(\nu=-\lambda\) into **action** then vary one φ | **Empty** bulk EL |
| R1 kinetic vary φ | Coulomb vacuum (different) |
| Critical mass / \(p_r=-\rho\) continuum | Lives in **equation** package (tensor or constrained EH eqs), not in substituted-φ EH |

---

## 5. Native-status tag (honest)

| Claim | Tag |
|-------|-----|
| Constrained EH reproduces Einstein-on-reciprocal | DERIVED (this mine) |
| Therefore UDT *is* EH+reciprocity | **NOT forced** — still GR-form package choice |
| Substituted-φ EH is the UDT dynamics | **False** (empty EL) |
| R1 equals constrained EH | **False** |

---

## 6. Next veins

1. **Junction:** reciprocal interior \(A=1-cr^p\) matched to exterior Schw (Israel) — edge character.  
2. **Matter in constrained EH:** how \(L_m\) sources \(\mathrm{EL}_\nu\) under lock.  
3. **Before freeze:** leave \(\nu+\lambda\) free and only demand asymptotic reciprocity / R1 on observables — third package probe.

---

## One-line

**EH mine: free warps give real Einstein ELs; stuffing reciprocity into the action before varying kills the φ equation; imposing reciprocity on the equations (or with a multiplier) recovers Schw-type vacuum — E-primary is constrained-Einstein, not substituted-φ EH, and still not R1.**
