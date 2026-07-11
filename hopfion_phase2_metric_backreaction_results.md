## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-10 |
| **Mode** | OBSERVE — Phase 2 φ-backreaction re-probe on the HELD hopfion (frozen-n, tractable first cut), per `hopfion_WORKSTATION_DISPATCH_phase2_metric.md` |
| **Object** | H3-class Q_H=1 hopfion ONLY — banked N=256 `prod_an256.npz` (|Q|≈0.99), frozen n. NEVER the f2d π₂ hedgehog. |
| **Device** | V100 (field load + isorotation moment/source on 256³, GPU float64); 1D radial φ-probe on CPU. ONE process. |
| **Observing or targeting?** | OBSERVE the exterior flux CLASS (plateau vs drift). NOT a mass. A drift outcome is a first-class result (halt-don't-salvage). |
| **Verifier status** | **In-run Branch-G control** (vacuum source OFF) plateaus to machine spread=0 in EVERY run ⇒ integrator sound + test NON-tautological. This is a corollary of the blind-verified `hopfion_GP_exterior_probe_results.md`. **Grade LEAD/CONDITIONAL** — a dedicated blind pass is the remaining step to hard-BANK. |
| **Build-on grade** | **LEAD / CONDITIONAL** — clean negative on Arm B (fixed-Q does not de-box); not a mass, not a branch verdict. |

### Premise ledger

| Item | Tag |
|------|-----|
| Held field = banked N=256 prod_an256 (frozen n) | **BANKED object** (dispatch §3 prefers frozen-n first) |
| Native Branch-P φ-eq Z(r²φ')' = e^{−2φ}[4 + Ŝ_stat(r) + ω²·σ̂_iso(r)] | **NATIVE** (round vacuum P-source 4 ON; no G=8πT) |
| Ŝ_stat = static hopfion shell-projected transverse-trace τ(r) | REAL-FIELD PROXY (class is source-shape-independent, so detail non-load-bearing) |
| σ̂_iso(r) = shell-avg ½[ξ(n_x²+n_y²)+κΣb_i²], ω=Q/I | **DERIVED from field** (I=189.65; ẑ-isorotation kinetic); the iso→φ coupling COEFFICIENT is **CHOSE-scaled** (a time-channel matter source; magnitude swept) |
| n_∞ = (0,0,−1) ⇒ iso source COMPACT (→1.3e-6 by r≈5.4) | **MEASURED** |
| ω(Q=1)=5.3e-3, ω²=2.8e-5 (vs vacuum 4) | **MEASURED** — iso source ~7 orders below vacuum at held Q |
| Z_φ∈{1,8}; φ_amb∈{0.3,3.0} | **FREE**, swept |
| Branch-G control (vacuum OFF) | **CONTROL** (must plateau) |

---

# Phase 2 — fixed-Q backreaction does NOT de-box the exterior

## Arms A / B (+ large-ω sensitivity) — results

Native Branch-P exterior flux class (large-r convergence; G control in every run). Full table:
`hopfion_phase2_metric_backreaction_out.json`.

| arm | Q | ω² | class (P) | G control |
|-----|---|-----|-----------|-----------|
| **A** | 0 | 0 | **DRIFT** (spread 0.85–1.3) | PLATEAU (0) |
| **B** | 1 | 2.8e-5 | **DRIFT** (identical to A) | PLATEAU (0) |
| **B** | 2 | 1.1e-4 | **DRIFT** | PLATEAU (0) |
| sens | ω=0.1 | 1e-2 | **DRIFT** | PLATEAU (0) |
| sens | ω=0.3 | 9e-2 | **DRIFT** | PLATEAU (0) |
| sens | ω=1.0 | 1.0 | **DRIFT** | PLATEAU (0) |

Across Z_φ∈{1,8} and φ_amb∈{shallow 0.3, deep 3.0}: **uniformly DRIFT** in P, **uniformly PLATEAU** in the G control.

## Pre-registered tests

- **T1 — solve exists:** YES. The coupled 1D φ-solve is regular/finite/convergent in every arm and regime.
- **T2 — exterior class:** **DRIFT (boxy-P)** for Arm A AND Arm B. G control plateaus to spread=0 (integrator
  sound; test non-tautological — same code gives plateau for G, drift for P).
- **T3 — regime table:** depth-INVARIANT — drift at shallow AND deep φ_amb, both Z_φ. Class does not move with
  the ambient-coupling knob (only magnitude does).
- **T4 — Q=0 vs Q>0 (THE CRUX):** the isorotation time-source does **NOT** change the exterior class.
  Confirmed not only at the held Q (ω²≈3e-5, negligible) but at ω=1 (ω² comparable to the vacuum source, far
  beyond any held Q) — **still DRIFT.** Reason (verified): the iso source σ̂_iso ∝ (n_x²+n_y²) is **COMPACT**
  (n→−ẑ ⇒ →0 outside the object), so the EXTERIOR (r>r_tex, all matter/time sources →0) is still the pure
  round-vacuum `4e^{−2φ}` — which is exactly what drives the drift. **No compact source can change a
  vacuum-P exterior.**

## Arm C note (relax B=1/A) — structurally triggered, but cannot de-box either

The isorotating core has a time-gradient ⇒ ρ+p_r>0 ⇒ it **cannot** stay reciprocal B=1/A (C-2026-06-14-1
scope; finite-amp MAP). So Arm C (non-reciprocal metric) is structurally triggered. BUT the non-reciprocity is
**core-compact** (the time-source that breaks it →0 outside), so B=1/A is restored in the vacuum exterior, and
Arm C **also cannot change the exterior vacuum**. A full non-reciprocal core solve was NOT run (throughput +
it cannot touch the load-bearing exterior); flagged as structurally present but non-load-bearing for the
exterior class.

---

## What it means (verdict)

**Fixed-Q isorotation backreaction does NOT de-box the exterior in the reciprocal (or core-non-reciprocal)
frame.** The exterior boxiness is a property of the round-vacuum Branch-P source `4e^{−2φ}`, and **every
matter/time/core source available (static stress, isorotation time-gradient, core non-reciprocity) is
COMPACT** — so none can reach or change the exterior vacuum that drives the drift.

**Therefore the mass lane's de-boxing does NOT come from source/metric engineering in the core.** It requires
changing the EXTERIOR EQUATION ITSELF — i.e. **Branch-G (source-free exterior)** — which is the **underived
G/P switch**. This unifies the whole arc: the hopfion-mass question reduces ENTIRELY to the G/P switch
(P: source-on ⇒ drift/whole-cell; G: source-off ⇒ plateau/localized), and **no amount of fixed-Q / isorotation
/ core dynamics can substitute for settling that switch.** Consistent with the bedrock (mass is action-on-a-
posited-carrier, not derivable from the static/reciprocal metric).

**Routing:** STOP adding sources to chase a de-boxed exterior. The real next move is the **G/P switch**
(promote `gp_switch_criterion` — off-round uniqueness already closed; remaining gates = Z_φ consilience fork +
seal-matching — and APPLY it to the hopfion exterior), NOT more Phase-2-style source engineering.

## NOT claimed
- NOT: a mass, a sign, or a branch verdict. Shows P⇒drift, G⇒plateau; does not decide the branch.
- NOT: that the hopfion is massless (Branch-G would give a clean flux; branch undecided).
- NOT: that isorotation is useless for persistence (Phase 1b HOLDS Q_H) — only that it does not de-box the exterior.
- NOT: a full non-reciprocal (Arm C) or full 3D coupled solve — frozen-n reciprocal first cut (+ compact-Arm-C note).
- NOT: topology→branch. NOT: r_lo cherry-pick (class by large-r convergence). NOT: G-shortcut (G only as in-run control). NOT: G=8πT. No huge .npz committed.

---

## Driver doublecheck (2026-07-10, this seat)

Pulled `30c5bd2`. JSON audit of all 24 rows: **class_P=DRIFT** and **class_G=PLATEAU** with **spread_G=0** uniformly.  
Arm B (Q=1) q-profiles match Arm A at the ~1e-6 relative level (ω²≈2.8e-5 negligible vs vacuum 4).  

**Logic check (agree):** once all matter/time sources are compact, exterior r≫r_tex is pure round-vacuum Branch-P \(Z(r^2\phi')'=4e^{-2\phi}\) ⇒ \(dq/dr=4e^{-2\phi}\neq0\) ⇒ drift is structural, not a missed isorotation knob.  

**Caveats kept:** frozen-n first cut; iso→φ magnitude CHOSE-scaled (but ω=1 sensitivity still DRIFT); Arm C not full-solved (compact-core argument only); blind = PARTIAL → **LEAD/CONDITIONAL** grade appropriate.  

**Routing (agree):** stop core source-engineering for de-box; next is **G/P switch** apply-to-hopfion, not Phase 2++.

