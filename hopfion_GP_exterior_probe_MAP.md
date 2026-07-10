## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-10 |
| **Mode** | MAP — FROZEN exterior-probe design + pre-registered T1–T3 (no retune after run) |
| **Parent** | `hopfion_GP_exterior_NEXT_CHARTER.md` · `hopfion_mass_background_coupling_MAP.md` |
| **Object** | **H3 Q_H=1 hopfion ONLY** (`prod_an256.npz`; shell-projected `h4_scripts/stress_rtheta_h3.npz`). NEVER the f2d π₂ hedgehog. |
| **Observing or targeting?** | OBSERVE the exterior readout CLASS. NOT "show a mass." NOT "show active-P." Halt-don't-salvage on box-control. |
| **Build-on grade** | MAP / pre-work — no mass or branch claim until T1–T3 banked with a verifier. |

### Premise ledger

| Item | Tag |
|------|-----|
| Real H3 field: r_tex ≈ 3.9 (texture edge, measured); source concentrated r≲2 | **MEASURED** from the real object |
| Native Branch-P φ-eq: Z(r²φ')' = 4e^{−2φ} + S(r) (round vacuum P-source **ON** everywhere; S = hopfion source, →0 beyond r_tex) | **NATIVE** (2𝒦→φ channel; no G=8πT) |
| S(r) shape/scale from real H3 shell-projected transverse trace τ(r) | **REAL-FIELD PROXY** — exact −2𝒦 needs backreaction; the exterior CLASS is probed, not the inner detail (T2 tests sensitivity) |
| Z_φ ∈ {1, 8} | **FREE fork** (swept) |
| φ_amb (ambient depth; set via inner φ_c → resulting φ_∞) | **FREE physical modulus** (swept; regime table, not one number) |
| Inner BC: regular core φ'(r_c)=0 (u(r_c)=0) | **NATIVE regularity** (not a cherry-picked r_lo) |
| r_c, r_max, ODE tol | **category-A** (soundness only) |

---

# FROZEN exterior probe — does the H3 hopfion exterior read active-P, dead-G, or flux-neutral?

## The honest test (replaces the tautological q≡q)

Forward-integrate the **native Branch-P φ-equation with the P-source ON** (not dropped to G):

    u = r²φ' ,  q = Z·u ,  u'(r) = (4 e^{−2φ} + S(r))/Z ,  φ'(r) = u/r²

from a **regular core** (u(r_c)=0, φ(r_c)=φ_c) outward to r_max ≫ r_tex. In the exterior (r>r_tex, S=0)
the equation is the pure round Branch-P vacuum Z(r²φ')'=4e^{−2φ}. **MEASURE** the flux q(r) across
exterior radii:

- **PLATEAU** (q→const as r grows): the P-source **self-quenched** (φ deepened, e^{−2φ}→0) ⇒ a conserved,
  cutoff-free asymptotic flux ⇒ **active-P with a clean mass-like flux** (if q≠0) OR **flux-neutral** (if q→0).
- **DRIFT** (q keeps growing ∝ ∫4e^{−2φ}): the source never quenches ⇒ **no conserved localized flux ⇒ boxy-P**.
- **φ'→0 flat** (q→0 plateau): **flux-neutral / dead-G-like ⇒ massless-conductor character**.

The plateau-vs-drift is a REAL property of the integrated ODE (source ON), not an assumed G form. It is
NOT cutoff-tested by moving an inner r_lo (forbidden); it is tested by whether q **converges** at large r.

## Pre-registered tests (characterize, DO NOT retune)

- **T1 — exterior readout class** ∈ {active-P (q plateaus, ≠0), dead-G / flux-neutral (q→0), boxy-P (q drifts),
  undecided/boxy}. Report the class + the plateau q or the drift rate.
- **T2 — regime sensitivity:** class + q vs **φ_amb** (shallow < φ_crit=½ln(32/Z_φ) < deep) and **Z_φ∈{1,8}**.
  A regime TABLE, not one number. (Ambient-depth is the "background coupling" knob.)
- **T3 — no topology→branch:** Q_H is never used to infer the branch. The discriminator is the integrated
  flux behavior (χ / self-quench), not the Hopf charge.

## δq=0 ambiguity guard
Even if active-P, the exterior q may plateau at ~0 (flux-neutral). Report q's plateau VALUE with its sign,
and whether it is robustly ≠0 across φ_amb/Z_φ or hovers at 0. A near-0 plateau is **flux-neutral-P**, a
first-class result (massless-conductor), NOT a box-control failure and NOT to be patched to nonzero.

## Red (binding)
- Branch-G clean-q shortcut / the q≡q tautology.
- Cherry-pick inner cutoff r_lo (the CF2 box-control move) — regularity BC only, and CLASS via large-r
  convergence, never via r_lo choice.
- Transfer the f2d hedgehog drain to the hopfion.
- Identify the residual-L seat singularity with the hopfion core.
- New couplings / G=8πT to force a nonzero flux.
- Retune S(r) / φ_amb after seeing q to land a preferred class.

## Success/fail
- **active-P with robust q≠0 across the regime** → δm/flux becomes *meaningful to interpret* (still NOT an SM mass; conditioned on φ_amb).
- **dead-G / flux-neutral** → bank it: massless / flux-conductor CHARACTER is a result.
- **boxy-P (drift, φ_amb-sensitive with no convergence)** → bank "exterior undecided in the static reciprocal frame; needs the non-boxy backreaction frame (secondary: fixed-Q + metric DOFs)."

## One-line
**Integrate the native P-source-ON φ-equation from the real H3 core outward; classify the exterior flux as plateau (clean/flux-neutral) or drift (boxy) across φ_amb/Z_φ — no G shortcut, no r_lo cherry-pick.**
