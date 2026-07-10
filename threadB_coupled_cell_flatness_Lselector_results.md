# Thread B — coupled round cell: α-source + transverse stress → flatness / L-selector

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE (bounded run of the pre-registered tests, settled α-coefficient) |
| **Slice scope** | Round Branch-P cell. TWO formulations: (a) 1-D interior-P→seal→exterior-G **shooting** with **PRESCRIBED** I_r(r), I_4th(r) (deficit/flatness probe); (b) f2d closed **finite-mirror** cell (H=0), fully self-consistent (φ,ρ,f). Z=8, ξ=κ=1, N=1. Static, diagonal, round (no shear). |
| **Observing or targeting** | OBSERVING. No mass/SNe/lump targeted. α frozen (CHOSE); ran BOTH formulations; disentangled the α-source from the T_AB channel. |
| **Coefficient** | **SETTLED**: S = −(α/2)·ξ·e^{αφ}·ρ²·I_r (anchor-verified, `verify_alpha_coeff_ANCHORED.py`, all 3 anchors PASS). Confirmed live in BOTH solvers (see §0). For α<0 the direct source is **POSITIVE** (adds to (ρ²φ')', supports radial structure). |
| **Verifier status** | Coefficient = anchor-verified (three independent KNOWN-CORRECT results — base φ-EOM, base ρ-EOM, verified T_AB — pin the ONE normalization; it reads off −α/2). Numeric runs are bounded self-checked pilots, NOT independently blind-verified. Purity harness run post-edits (see §1). |
| **Build-on grade** | **CONDITIONAL** (coefficient firmly settled; probe T1/T2/T3 ride a PRESCRIBED I_r; self-consistent f2d cell drains matter → no closed flat cell — and the convergence check (§2.1) shows the drain is a genuine residual minimizer of this bounded solve, not an under-iteration artifact). Do NOT bank as a closed cell. |
| **Re-run commands** | `python3 verify_alpha_coeff_ANCHORED.py` (coefficient) · `python3 cell_solver_round.py --probe --asrc -0.5 --amp 0.3` (probe) · `scratchpad/run_f2d_threadB.py --mode table --Nr 16 --Nth 8 --maxit 40` and `--mode single --Nr {12,16,24} --maxit {40,120}` (f2d + convergence). f2d driver invoked with `PYTHONPATH` = repo root. |

---

## 0. Coefficient confirmed live in code (settled: S = −(α/2)·ξ·e^{αφ}·ρ²·I_r)

The φ-eq direct matter source is **S = −(α/2)·ξ·e^{αφ}·ρ²·I_r** in
`Z(ρ²φ')' = 4e^{-2φ}ρ'² + S`. This is anchor-verified (`verify_alpha_coeff_ANCHORED.py`):
the ONE reduced-action normalization that reproduces (1) the base φ-EOM, (2) the base ρ-EOM,
**and** (3) the verified transverse stress T_AB uniquely reads off the coefficient −α/2. The two
competing conventions (+α, −α/2) are adjudicated: the +α script is disqualified because its bespoke
geometry Lagrangian fails anchor (1) (it flips the base φ-EOM RHS sign and drops the ∫sinθ dθ = 2
angular factor on geometry only). **For α<0, S>0** — the direct source ADDS to (ρ²φ')'.

Both solvers implement this coefficient with a switchable `ASRC_C` whose settled value is **−0.5**:

- **`cell_solver_round.py`** (line 38, φ'' RHS): `phipp += ac*al*xi*np.exp(al*phi)*Ir/Z`.
  This is φ'' += S/(Zρ²) (ρ² cancels). With `ac=-0.5`: φ'' += −0.5·α·ξ·e^{αφ}·I_r/Z, i.e.
  S = −(α/2)·ξ·e^{αφ}·ρ²·I_r. **✓ matches settled.**
- **`cell_solver_f2d.py`** (residual convention). Line 257 defines the φ-residual as
  `phi_ode = φ'' − RHS_base` (=0 on-shell). Line 262 then does
  `phi_ode = phi_ode − ASRC_C·α·ξ·e^{αφ}·I_r/Z`, which moves S/(Zρ²) onto the RHS of φ''. With
  `ASRC_C=-0.5` this is S = −(α/2)·ξ·e^{αφ}·ρ²·I_r. **✓ matches settled.**

No code fix was needed — the default `ASRC_C=-0.5` in both files already equals the settled −(α/2)ξ.
(`ASRC_C=+1` remains a switch reproducing the old doc value; not used for the banked runs.)

---

## 1. What was run (files unchanged this pass; α frozen CHOSE ∈ {−0.5, −1, −2})

**Probe (round shooting):** `cell_solver_round.py --probe --asrc -0.5` sweeps (φ'_c, r_s) with a
PRESCRIBED bump I_r(r), I_4th(r) (peak `amp`, vanishing at both ends per the f_r=0 mirror BC) active
in the interior; deficit = ρ'/e^φ − 1 at infinity. **The prescribed I_r is a labeled PROBE** (imposed,
not solved from the S² map f) — the shooting picture has no S² PDE, so real self-consistent I_r is
tested only in f2d.

**Self-consistent (f2d closed cell):** full coupled (φ, ρ, f) round finite-mirror cell (H=0 closure),
LM/jacrev solve, seed L₀=1.0, ρ₀≈0.707. I_r,I_4th are SELF-CONSISTENT from f (no imposition).

**Premise ledger:** **α = CHOSE** (frozen {−0.5,−1,−2}, no retune). **ASRC_C = −0.5 = DERIVED**
(anchor-verified settled coefficient). **Z=8** CHOSE-fixed. **ξ=κ=1** CHOSE-units. **N=1**
DERIVED-topological. Probe I_r,I_4th = **PRESCRIBED** (tagged everywhere). Grid/iters: probe = scipy
solve_ivp (rtol 1e-9); f2d = Nr∈{12,16,24}, Nth=8, LM maxit∈{40,120}, budget≤180s, ONE process, no
concurrent GPU.

**pytest:** `python3 -m pytest tests/ -q` → **69 passed, 1 xfailed, 1 failed**. The one failure is the
pre-existing unrelated hygiene-header doc gap (`test_covered_results_have_hygiene_header`), not touched
by this work; no solver code was edited this pass.

---

## 2. T1 / T2 / T3 TABLE (settled coefficient ASRC_C = −0.5)

| Test | Prescribed-I_r shooting probe (round) | Fully self-consistent f (f2d closed cell) |
|------|----------------------------------------|-------------------------------------------|
| **T1** deficit=0 flat cell for α<0? | **YES.** Deficit lifts from the stuck −0.9 baseline and **crosses 0** for all α∈{−0.5,−1,−2}: e.g. r_s=5→8 takes deficit −0.65→+0.18. **But the crossing is primarily the T_AB (ρ-channel) matter effect** — it also crosses with the α-source OFF (α=0). The α<0 source only **modulates** the flat-closing r_s (a secondary effect; §2.2). | **NO closed flat cell.** The coupled solve DRAINS the matter (I_r → ~5e-6) and shrinks L (1.0 seed → ~0.014 at low residual); φ stays ~−2.5e-3. Same drain at α=0 and every α<0 — the α-source is ∝ I_r, which is the quantity vanishing, so it cannot hold it up. Convergence check (§2.1): the drain is a genuine minimizer, not an under-iteration artifact. |
| **T2** r_s single-valued, matter selects L? | **YES (matter selects L).** At fixed matter the flat-closing r_s is single-valued and **nearly φ'_c-independent** (deficit changes <2% across φ'_c 0→1.2 at fixed r_s). It moves **monotonically with amplitude** (bigger matter ⇒ smaller flat cell). | **N/A / weak.** Matter amplitude is not a free input — it drains to ~0, so no L is selected in the self-consistent solve. |
| **T3** finite core vs ρ→0 collapse? | **Finite core, NO ρ→0 collapse.** min interior ρ = r_c = 0.1 always (ρ rises monotonically outward). The inward −κN²I_4th/ρ³ term did not drive collapse at these amplitudes. Small cells (r_s≲2) fail to bound (exterior collapse), unrelated to the core. | **No ρ core collapse.** ρ stays ≈0.709–0.710 (flat); the degeneracy is in **L**, not in a ρ→0 core. |

### 2.1 CONVERGENCE CHECK on the self-consistent drain (α=−1, ASRC_C=−0.5) — is it physical-to-this-solver or a numeric artifact?

Three axes varied; the drain (I_r→small, L→small) is **ROBUST**, not budget/grid noise:

| Axis | Setting | final Φ=‖F‖² | L (seed 1.0) | I_r,mean | q_raw |
|------|---------|-------------|--------------|----------|-------|
| **iterations** | Nr=16, maxit=40 | 6.8e-3 | 0.112 | 2.9e-4 | +1.0e-4 |
| | Nr=16, maxit=120 | 1.3e-4 | **0.014** | **4.5e-6** | +2.3e-7 |
| **resolution** | Nr=12, maxit=40 | 5.0e-3 | 0.096 | 2.1e-4 | +6.1e-5 |
| | Nr=16, maxit=40 | 6.8e-3 | 0.112 | 2.9e-4 | +1.0e-4 |
| | Nr=24, maxit=40 | 6.9e-3 | 0.115 | 3.1e-4 | +1.2e-4 |
| **α (endpoint)** | Nr=16, maxit=120, α=0 | 1.3e-4 | 0.0144 | 4.6e-6 | +2.2e-7 |
| | Nr=16, maxit=120, α=−2 | 1.3e-4 | 0.0143 | 4.5e-6 | +2.4e-7 |

**Verdict — drain is genuine (not an under-iteration/grid artifact):**
1. **Iteration axis is the decisive one.** As the residual is driven DOWN (Φ 6.8e-3 → 1.3e-4 at Nr=16),
   L and I_r do NOT stabilize at a finite value — they drop FURTHER (L 0.112→0.014, I_r 2.9e-4→4.5e-6),
   monotonically. So the better-converged the solve, the more complete the drain: **L→0, I_r→0 IS the
   residual minimizer** of this bounded closed-mirror cell. The intermediate "L~0.11" at maxit=40 is
   merely an under-converged snapshot on the way down — the opposite of a rescue.
2. **Resolution axis does not rescue it.** At fixed iteration budget, Nr=12/16/24 give a resolution-stable
   snapshot (L~0.10–0.11); finer grids do not open a finite-L cell. (Higher Nr sits at slightly higher
   Φ for equal iters — more DOF, same budget — consistent with axis 1.)
3. **α-independent endpoint.** The converged drain endpoint is the same for α=0 and every α<0
   (L≈0.014, I_r≈4.5e-6); only q_raw modulates minutely. The α<0 restoring source, though correctly
   signed (S>0), is ∝ I_r and so vanishes with it — it cannot support a quantity that is itself draining.

This is a solver-completeness statement about THIS bounded static round closed-mirror solve: its
residual minimizer sends the matter content and the cell size toward zero. It is NOT (this pass) a
metric verdict — the open question stays: whether some ON degree of freedom left OUT here (non-round /
shear, a non-static channel, a different closure) can sustain I_r>0 in a closed cell.

### 2.2 α-source vs T_AB disentangle (round probe, φ'_c=0.3, amp=0.3), flat-closing r_s

The α-source is a **secondary modulation** on top of a flat cell that the T_AB (transverse-stress)
matter channel already produces on its own. With the settled coefficient (ASRC_C=−0.5, S>0 for α<0),
the α<0 source pushes the flat-closing r_s slightly LARGER than T_AB alone. Across α∈{−0.5,−1,−2} the
deficit-zero crossing shifts by only ~1–2% (r_s in the 5–8 range), monotone in amplitude. T_AB alone
already crosses deficit=0; the α-source does not create the flat cell, it nudges where it closes.

---

## 3. Honest reading (for the PONDER — not a verdict)

1. **The α-source cannot bootstrap structure from nothing** — it is ∝ I_r. In the self-consistent
   closed cell the matter I_r drains toward zero and L shrinks (present already at α=0), so the α-term
   becomes ~1e-6 and is indistinguishable across α and (as a further check) across the two coefficient
   conventions. The hoped "S ∝ e^{αφ}ρ²I_r SUPPORTS I_r vs draining" is **not realized** in this
   bounded static closed-mirror solve: a source proportional to the vanishing quantity cannot hold it
   up. The convergence check (§2.1) shows this is the genuine residual minimizer of THIS solve, not an
   under-iteration artifact.
2. **A flat cell DOES exist when matter is present (T_AB), and matter then selects L** — but shown only
   with a **PRESCRIBED** I_r. The open question the self-consistent drain leaves is exactly the
   frontier's: *can any ON degree of freedom sustain I_r>0 in a closed cell?* At Nr≤24, static + round,
   it does not.
3. **The coefficient is now settled** (§0, anchor-verified): −(α/2)ξ, positive source for α<0. This
   fixes the sign/factor the earlier doc/charter got wrong (they had +α·ξ). It changes WHICH WAY α<0
   nudges r_s in the probe, but does NOT change either headline (flat exists via T_AB; self-consistent
   closed cell drains).

## 4. NOT claimed
- NOT: a self-consistent flat bounded cell closes (the closed cell drains; the flat cell used a
  PRESCRIBED I_r).
- NOT: the α-restoring channel supports matter structure (negligible once I_r drains; untested where
  I_r is held up by something else / another ON DOF).
- NOT: any mass, ratio, SNe, or cosmology result. No dS. No lump/particle.
- NOT: convergence to a nonzero cell — the f2d minimizer sends L, I_r → 0 (the more converged, the
  smaller). The drain is characterized, not salvaged.

---

## Solver-first MAP (post-pilot)

**`threadB_f2d_drain_solver_first_MAP.md`** — DOFs left out; next GPU = non-round + topological boundary, still static.

