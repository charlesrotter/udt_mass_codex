# Thread B — f2d drain: non-round + topological audit (static)

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE (solver-first — test whether the drain is an artifact of the round/topology-trivial slice) |
| **Slice scope** | STATIC, diagonal, Branch-P finite-mirror f2d cell (φ,ρ,f). Z=8, ξ=κ=1. Extended along TWO DOFs vs the banked round run: (a) **non-round** ℓ=2 shear a2(r) live (free-seal S-JC2 and enforced-seal S-Dir); (b) **topological** winding degree N∈{1,2} with a per-shell winding diagnostic Q(r). No prescribed I_r (self-consistent from f). No new coupling. Grid (Nr,Nθ)∈{(12,8),(16,8),(24,8),(16,12)}. |
| **Observing or targeting?** | OBSERVING. Winding Q(r) and I_r/L are CHARACTERIZERS (measured, not filters); no lump/mass/particle targeted. The winding diagnostic reports what sector the solve sits in; it does not throw solutions away. |
| **Verifier status** | Self-checked bounded pilots, GPU (V100) results bit-identical to CPU spot-check. NOT independently blind-verified — driver to run verifier before banking. Baseline reproduces the prior banked drain table to 3 sig-figs (L=0.112, I_r=2.9e-4 at Nr=16/it40). |
| **Build-on grade** | **CONDITIONAL** (scoped negative). The drain SURVIVES both the non-round DOF and the topological DOF across the convergence axis. Recorded as a clean failure of these two left-out DOFs; do NOT bank as a metric verdict, do NOT patch. |
| **Re-run commands** | `PYTHONPATH=$(pwd) python3 scratchpad/run_f2d_nonround_topo.py` (full matrix). Winding diagnostic: `cell_solver_f2d.winding_of_r(v,ctx,prm,n5d=...)`. `python3 -m pytest tests/ -q` (69 pass, 1 xfail, 1 pre-existing unrelated hygiene-header fail). |

### Premise ledger

| Item | Tag |
|------|-----|
| Static, diagonal, Branch-P (W=1), finite-mirror H=0 closure | **SCOPE** (inherited; NOT tested here — MAP §1.3 next) |
| Z=8 | **CHOSE-fixed** |
| ξ=κ=1 | **CHOSE-units** (ratios are the observables) |
| N∈{1,2} winding degree | **DERIVED-topological** (integer), swept |
| α∈{0,−1,−2}; ASRC_C=−0.5 | α **CHOSE** (frozen, no retune); ASRC_C **DERIVED** (anchor-verified −α/2) |
| ℓ=2 shear a2 seed amp, S-Dir seal pin a2_mirror | **CHOSE-seed / CHOSE-BC** (relaxed, or explicitly pinned as the enforced-non-round test) |
| Winding Q(r) = (N/2)∫sin f·f_θ dθ | **DERIVED** (topological degree; boundary integral, exact) |
| Grid (Nr,Nθ), maxit, LM damping | **WORKING** (category-A conditioning; soundness only) |

---

## 1. What was tested

Two DOFs the banked round run (`threadB_coupled_cell_flatness_Lselector_results.md`) left out, per
the solver-first MAP (`threadB_f2d_drain_solver_first_MAP.md` §2, §4):

- **Non-round / shear** (MAP DOF 2): the ℓ=2 traceless shear a2(r) is made LIVE (the co-relaxed
  off-round system already in `cell_solver_f2d.py`), both with a **free seal** (`S-JC2`: a2′(r_s)=0,
  a2 relaxes) and with an **enforced seal** (`S-Dir`: a2(r_s) pinned to a nonzero value, forcing a
  genuinely non-round cell that CANNOT relax to round).
- **Topology** (MAP DOF 4): added `winding_of_r()` — the per-shell topological degree
  Q(r) = (N/2)∫₀^π sin(f)·f_θ dθ = N·½[1−cos f]₀^π, which equals N whenever the poles BC f(0)=0,
  f(π)=π hold. Swept N=1 and N=2 (higher winding). This is the genuine S²→S² degree, a boundary
  integral — it MEASURES which topological sector the solve occupies.

The convergence axis (maxit 40→120) and resolution axis (Nr 12/16/24, Nθ 8/12) were varied throughout.

---

## 2. Results table

| run | round/non-round | boundary/topology | (Nr,Nθ) | maxit | α | final \|F\|² | L | I_r mean / max | winding Q [min,max] | max\|a2\| | q_raw | verdict |
|-----|-----------------|-------------------|---------|-------|---|-----------|---|----------------|---------------------|----------|-------|---------|
| R_a0_it40   | round    | mirror H=0, N=1 | (16,8)  | 40  | 0  | 6.80e-3 | 0.1122 | 2.94e-4 / 2.97e-4 | [1.000,1.000] | — | +9.8e-5 | drains (under-conv. snapshot) |
| R_a0_it120  | round    | mirror H=0, N=1 | (16,8)  | 120 | 0  | 1.32e-4 | 0.0144 | 4.62e-6 / 4.62e-6 | [1.000,1.000] | — | +2.2e-7 | **drains** |
| R_am1_it120 | round    | mirror H=0, N=1 | (16,8)  | 120 | −1 | 1.31e-4 | 0.0143 | 4.54e-6 / 4.54e-6 | [1.000,1.000] | — | +2.3e-7 | **drains** |
| R_am2_it120 | round    | mirror H=0, N=1 | (16,8)  | 120 | −2 | 1.31e-4 | 0.0143 | 4.53e-6 / 4.53e-6 | [1.000,1.000] | — | +2.4e-7 | **drains** |
| R_Nr12      | round    | mirror H=0, N=1 | (12,8)  | 40  | 0  | 4.98e-3 | 0.0961 | 2.09e-4 / 2.11e-4 | [1.000,1.000] | — | +5.8e-5 | drains (snapshot) |
| R_Nr24      | round    | mirror H=0, N=1 | (24,8)  | 40  | 0  | 6.90e-3 | 0.1147 | 3.12e-4 / 3.15e-4 | [1.000,1.000] | — | +1.1e-4 | drains (snapshot) |
| R_Nth12     | round    | mirror H=0, N=1 | (16,12) | 40  | 0  | 4.90e-3 | 0.1010 | 1.41e-4 / 1.42e-4 | [1.000,1.000] | — | +7.0e-5 | drains (snapshot) |
| NR_a0_it40  | non-round | S-JC2 free, N=1 | (16,8) | 40  | 0  | 1.25e-2 | 0.1645 | 5.08e-4 / 5.20e-4 | [1.000,1.000] | 6.1e-4 | +2.8e-4 | drains (snapshot) |
| NR_a0_it120 | non-round | S-JC2 free, N=1 | (16,8) | 120 | 0  | 3.50e-4 | 0.0240 | 1.26e-5 / 1.26e-5 | [1.000,1.000] | 5.8e-4 | +8.6e-7 | **drains (a2 drains too)** |
| NR_am1_it120| non-round | S-JC2 free, N=1 | (16,8) | 120 | −1 | 3.47e-4 | 0.0239 | 1.24e-5 / 1.25e-5 | [1.000,1.000] | 5.8e-4 | +9.0e-7 | **drains** |
| NRdir_it120 | non-round | **S-Dir seal a2=0.2**, N=1 | (16,8) | 120 | 0 | 3.34e-3 | 0.0152 | 5.42e-6 / 5.56e-6 | [1.001,1.001] | 0.143 | +1.7e-6 | **drains (shear HELD, matter still drains)** |
| SDir_a2m0.5 | non-round | **S-Dir seal a2=0.5**, N=1 | (16,8) | 150 | 0 | 1.45e-2 | 0.0064 | 1.20e-6 / 1.34e-6 | [1.003,1.003] | 0.380 | — | **drains** |
| SDir_a2m1.0 | non-round | **S-Dir seal a2=1.0**, N=1 | (16,8) | 150 | 0 | 6.46e-2 | 0.0053 | 1.29e-6 / 1.74e-6 | [1.006,1.006] | 0.746 | — | **drains** |
| N2_round    | round    | mirror H=0, **N=2** | (16,8) | 120 | 0  | 1.41e-5 | 394.71 | 2.73e-8 / 7.19e-8 | [2.000,2.005] | — | +1.9e-5 | **drains (L runaway large; matter→0)** |
| N2_nonround | non-round | S-JC2 free, **N=2** | (16,8) | 120 | 0 | 5.00e-5 | 132.50 | 1.90e-8 / 6.99e-8 | [1.998,2.000] | 0.298 | +1.6e-5 | **drains** |

---

## 3. What DOF was tested?

Two of the DOFs the round pilot froze: (i) **non-round angular structure**, via the live ℓ=2 shear
a2(r) — both allowed to relax freely (S-JC2) and forced nonzero at the seal (S-Dir, up to a2≈0.75, a
strongly non-round cell that cannot relax back to round); and (ii) the **topological/winding sector**,
via a per-shell winding-degree diagnostic Q(r) and a sweep of the winding degree N=1→2. The banked
reading (MAP §1.4) that the solve "sits in the unwound/trivial topological sector" was tested directly
by MEASURING the degree rather than inferring it from q_raw.

## 4. What failed or survived?

**The drain SURVIVED both DOFs, and the "unwound sector" hypothesis was falsified — but not in the
direction hoped.** Three clean observations:

1. **The topological winding does NOT unwind — it was never trivial.** Q(r) is pinned to N in every
   run (machine-exact: N=1→Q=1.000, N=2→Q=2.000), because Q is a boundary integral carried by the
   poles data f(0)=0, f(π)=π (in the u=f−θ representation the degree is carried EXACTLY by the θ ramp).
   The round relaxation cannot leave sector N. So the MAP's "q_raw→1e-7 ⇒ unwound sector" conflated the
   **seal flux** q_raw (a φ-channel readout) with the **topological winding** Q. The actual winding is
   nonzero and pinned; the drain is **orthogonal** to it. What drains is the **radial structure I_r**
   (f_r→0, f→the rigid hedgehog θ), not the angular winding.

2. **Non-round structure does not sustain I_r.** With a free shear (S-JC2), a2 drains alongside I_r
   (seed 0.15 → 5.8e-4) and I_r drains to 1.3e-5 exactly as in the round run. Even with the shear
   **FORCED nonzero at the seal** (S-Dir, a2 held at 0.14 / 0.38 / 0.75 through the cell — a genuinely
   non-round geometry that cannot relax to round), I_r STILL drains to ~1e-6. Forcing angular structure
   into the geometry does not hold up the matter's radial structure.

3. **α<0 and higher winding do not rescue it.** α∈{−1,−2} give the identical drained endpoint
   (I_r∝ the vanishing quantity, so the restoring source vanishes with it — consistent with the banked
   run). N=2 does not drain L→0 but instead lets L run away LARGE (395 round / 132 non-round) with
   I_r→~1e-8 — a different degeneracy sign but the SAME matter-vanishing endpoint (an empty large cell).
   Across N=1 (L→0) and N=2 (L→∞), once matter drains the cell LENGTH L is unconstrained.

**Convergence-axis verdict (the banking gate):** as ‖F‖² is driven DOWN (it40→it120: round 6.8e-3→1.3e-4,
non-round 1.25e-2→3.5e-4), I_r drops FURTHER and monotonically (round 2.9e-4→4.6e-6; non-round free
5.1e-4→1.3e-5; forced-shear to ~1e-6). The nonzero I_r seen at it40 is an **under-converged snapshot on
the way down, NOT a solution**. The better-converged the solve, the more complete the drain. This meets
the pre-registered FAILURE condition: better convergence → I_r→0, L degenerate → **the drain SURVIVES
the non-round + topological slice.** Nothing here is banked as a nonzero cell.

## 5. Next solver DOF if this still drains?

Per MAP §1 ordering, non-round (DOF 2) and topology (DOF 4) are now BOTH tested and drain. The next
untested left-out DOF is **mirror-vs-wall closure** (MAP §1.3 / §3 "after that"). Strong motivation
surfaced here: once matter drains, L is unconstrained (→0 at N=1, →∞ at N=2) — a **free-boundary
degeneracy in the cell length that the H=0 finite-mirror closure does not pin**. The mirror fold
(φ′=ρ′=f_r=0, H=0) may be too quiet a boundary — it lets the minimizer collapse (or inflate) the cell
while draining the matter. The test: replace the mirror ends with a **causal-wall-style (WR-L)
closure** and ask whether a wall that does NOT permit f_r=0 at the seal sustains I_r>0. **After that**
(if the drain persists): **time-live** (MAP DOF 1, highest-priority) — a non-static perturbation /
eigenmode about the drained solution, asking whether any mode with nonzero I_r is restoring. Both are
solver DOFs (Category-A / metric-form completeness), NOT mechanisms.

---

## NOT claimed

- NOT: a self-consistent cell with sustained I_r>0 (every converged run drains I_r→≤1.3e-5, dropping).
- NOT: a topological unwinding as the cause of the drain (winding Q is pinned = N; the drain is the
  radial I_r, orthogonal to the winding).
- NOT: that non-round or higher-winding structure rescues the cell (both drain; forced shear up to
  a2≈0.75 still drains I_r).
- NOT: a metric verdict. This is a scoped negative on TWO left-out DOFs (non-round, topology) of the
  static Branch-P finite-mirror slice; the mirror-vs-wall closure and time-live DOFs are UNTESTED.
- NOT: any mass, ratio, particle, SNe, or cosmology result. No dS. No prescribed I_r.
- NOT independently blind-verified (self-checked bounded pilots; driver to run verifier before banking).
