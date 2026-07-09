## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | CHARTER / pre-register (dispatch) |
| **Status** | Ready for workstation — **not** auto-launched |
| **Audience** | Anthony / driver / external implementer |
| **Builds on** | `cell_solver_round.py`, `udt_phi_blindness_relaxation_results.md`, `simple_metric_alpha_restoring_probe_results.md` |
| **Does NOT chase** | Native continuum dS (closed for any α) |

---

# CHARTER — full self-consistent cell solve (Thread B, honest content)

## Frame (binding)

- UDT redshift = **frame-relation** \(1+z=e^{\phi(r)}\), observer-centered — no cosmic dS ball to fill (`udt_canonical_geometry.md` §1.4).  
- Residual **L** + Charles ruling **(A)**: \(\phi=0\) seat = regime boundary macro residual ↔ micro cell.  
- **dS native closed for any α** — `simple_metric_dS_native_any_alpha_closed_results.md`. Do not retarget this solve at dS.  
- Goal: **bounded cell + matter L-selector + restoring channel**, not cosmology fit.

## Question (METRIC-LED)

Does the \(\alpha\neq 0\) restoring channel, with full transverse matter stress, **close a flat bounded cell**, and does **matter select \(L\)** (\(r_s\))?

## Fields

| Field | Role |
|-------|------|
| \(\phi(r)\) | dilation |
| \(\rho(r)\) | transverse / areal size function |
| S² map \(n\to f_r\) | \(I_r\) **and** transverse stress \(T_{AB}\) |

## Equations (native package — edit in place on existing solver; no parallel v2)

**Interior (Branch P):**

\[
Z(\rho^2\phi')'=4e^{-2\phi}\rho'^2+\alpha\, e^{\alpha\phi}\,\rho_m^2\, I_r
\]

\[
\rho''=2\phi'\rho'-\frac{Z}{4}\rho e^{2\phi}\phi'^2+\underbrace{T_{AB}\text{ transverse stress}}_{\text{load-bearing new term}}
\]

\(+\) \(n/f\) EOM for the S² map.

**Exterior (G, vacuum):**

\[
(\rho^2\phi')'=0,\qquad \rho''=-\frac{Z}{4}\rho\phi'^2.
\]

**Seal junctions:** \([Z\rho^2\phi']\) continuous \(=q\); \(\rho'_P=e^{2\phi_s}\rho'_G\); \(\phi,\rho\) continuous.

(Exact coefficient forms: re-derive from native action in implementer pass — match `cell_solver_round` / founding action; **blind-verify the transverse matter-stress operator** as the one new load-bearing term.)

## Pre-registered tests (freeze before run)

| ID | Question | Pass/fail (characterize, don’t retune) |
|----|----------|----------------------------------------|
| **T1** | Exists deficit\(=0\) bounded cell for \(\alpha<0\)? | yes / no / throughput-limited |
| **T2** | Is \(r_s\) (\(=L\)) single-valued in matter amplitude/scale (matter selects \(L\))? | yes / no / weak |
| **T3** | Core: finite vs \(\rho\to 0\) collapse (bears on seat ruling A)? | report structure |

## Discipline

- **α CHOSE** (p16 verdict C): freeze \(\alpha\in\{-0.5,-1,-2\}\) — no retune after.  
- **Blind-verify** transverse matter-stress operator by independent re-derivation before trusting T1–T3.  
- Test-matter → real S² stress (no fake ρ glue).  
- **Halt-don’t-salvage** on collapse; report deficit, \(\rho\) core, \(r_s\).  
- **ANTI-HANG:** Nr≤16/24; cap Newton/Krylov iters; **one** process; no concurrent GPU; bound budget → “throughput-limited” OK.  
- Observing, not targeting masses/SNe.  
- `pytest tests/` purity when editing solver.

## Out of scope

- Continuum dS / \(\Lambda\) native fill.  
- Free \(D_A\).  
- P_ell.  
- χ² cosmology.  
- Mechanism patches if T1 fails (solver-first: missing term, numeric, frozen DOF, incomplete space).

## Prior probe (do not re-claim as full solve)

`simple_metric_alpha_restoring_probe_results.md`: α<0 pulls deficit toward flat + L-coupling; cannot close alone without \(T_{AB}\).

## Deliverable

Results doc + (if T1/T2 interesting) blind verifier pass before bank. Update LIVE only after verify.

---

## One-line dispatch

**Full self-consistent \((f,\phi,\rho)\) cell: does α≠0 + transverse stress close a flat cell and pin \(L\)? Not a dS hunt.**
