# Hopfion — workstation dispatch: G/P switch (post Phase 2)

**Date:** 2026-07-10 · **Branch:** `grok` · **MAP first, then bounded apply** · GPU only if a numeric gate is frozen

---

## 0. Job in one line

**Settle (or honestly leave open) the hopfion exterior branch** by promoting and **applying** the banked G/P switch criterion to the **H3 hopfion** — not by adding more core sources. Phase 2 already showed compact sources cannot de-box a vacuum-P exterior.

---

## 1. Sync

```bash
git fetch origin && git checkout grok && git pull origin grok
cd /path/to/udt_mass_codex
```

---

## 2. Why this job (do not re-open)

| Closed / banked | Implication |
|-----------------|-------------|
| Phase 2: fixed-Q isorotation does **not** de-box exterior | Stop core source-engineering |
| G/P exterior probe: P⇒drift, G⇒plateau | Mass flux class = branch class |
| Carrier = posit; H3 exists | Right object is hopfion, not hedgehog |
| Topology alone ≠ switch | STOP if any “Q_H forces P” appears |

**Mass de-box requires changing the exterior equation (G vs P), not the core.**

---

## 3. Read order (binding)

| # | File | Why |
|---|------|-----|
| 1 | **This file** | Job bounds |
| 2 | `hopfion_phase2_metric_backreaction_results.md` | Why G/P is the remaining gate |
| 3 | `gp_switch_criterion_results.md` | N1∧N3 / χ criterion (DERIVED scoped, not canon) |
| 4 | `H4_GP_switch_hopfion_MAP.md` | Hopfion-specific switch MAP; CF-S tripwires |
| 5 | `hopfion_mass_background_coupling_MAP.md` | Mass lane orientation |
| 6 | `hopfion_GP_exterior_probe_results.md` | P drift / G plateau baseline |
| 7 | `matter_carrier_provenance_audit_results.md` | Carrier posit |

Optional: `H4_N4rev_sign_certification_results.md` §7 (CF2⟺switch; parked transverse frame).

---

## 4. Work plan (two stages — do not skip Stage A)

### Stage A — MAP (no heavy compute; **deliver first**)

Write `hopfion_GP_switch_apply_MAP.md` (or extend `H4_GP_switch_hopfion_MAP.md` with a 2026-07-10 addendum) that freezes:

1. **Criterion restatement for the hopfion**  
   - Switch = N1∧N3 (χ gauge-rigid) per `gp_switch_criterion_results.md`  
   - Discriminator = **χ-pinning / interior**, not 𝒦≠0 alone, not topology  

2. **What is already DERIVED vs OPEN on the hopfion**  
   - Local 𝒦≠0 (N3-ish core): DERIVED lean from H4  
   - N1 (pin √A / toroidal scales): **OPEN — the crux**  
   - N2 meaningful only via N3  

3. **Honest probe design (replaces tautological G-match)**  
   - Forward measure of exterior class already done (drift/plateau)  
   - **New:** interior χ / φ′-flatness / net source non-cancellation diagnostics on **H3 field + native channels only**  
   - δq≠0 ⇒ active-P (one-way); δq=0 ⇒ need interior φ′ flatness to split dead-G vs flux-neutral-P  

4. **Remaining gates named (do not invent)**  
   - Z_φ consilience fork (A free / B=8)  
   - Seal-matching / frame C(a): **no private G|P wall at ℓ_hopf** (retired cell smuggle)  
   - φ_amb unpinned (data-blind modulus)  

5. **Pre-register numeric tests** (only if Stage B is justified) — see §5  

6. **Red list** (copy §7) frozen in the MAP  

**Deliverable Stage A:** MAP file + short “ready / not ready for Stage B” line.  
**If not ready:** bank MAP as LEAD and stop — do not force a solve.

### Stage B — Bounded apply (only after Stage A frozen)

Only if Stage A names a **single, non-tautological, non-topology** numeric discriminator:

| Arm | Purpose |
|-----|---------|
| **H3 object** | Real field only (`prod_an256` or regenerated N≥192 production hold) |
| **Interior χ / pin diagnostics** | Measure whether hopfion toroidal geometry pins χ (N1) under native definitions |
| **Exterior class** | Reuse plateau/drift integrator as **control**, not as branch decision |
| **δq=0 branch** | Interior φ′-flatness check if net flux vanishes |

**Anti-hang:** one process; no concurrent GPU; bound iters/grid; throughput-limited OK.  
**Do not** re-run Phase 2 isorotation de-box attempts.

---

## 5. Pre-registered tests (Stage B — freeze in Stage A before run)

| ID | Question | Pass language |
|----|----------|----------------|
| **S-T1** | Does the hopfion supply N1 (pinned transverse scale / χ rigidity) under the frozen definition? | yes / no / undecided |
| **S-T2** | With N3 from core 𝒦, does N1∧N3 hold ⇒ **P-interior** lean? | yes / no / undecided |
| **S-T3** | Exterior flux class under native P (control): still drift? | expect **drift** (sanity) |
| **S-T4** | If net δq~0: is interior φ′ flat (dead-G-like) or structured (flux-neutral-P)? | classify |
| **S-T5** | No topology→branch; no private seal at ℓ_hopf | must hold |

**Not a success criterion:** producing a preferred mass number or forcing plateau by hand.

---

## 6. Out of scope (red)

- More fixed-Q / isorotation / compact-source engineering to de-box exterior  
- f2d hedgehog mass claims  
- Branch-G clean-q tautology; r_lo cherry-pick δm  
- “Q_H forces active-P”  
- Private G|P wall at hopfion radius (retired sealed cell)  
- G=8πT mass  
- SM / lepton / SNe  
- Canonize the switch without Charles  

---

## 7. Deliverables

### Stage A (required first)
- `hopfion_GP_switch_apply_MAP.md` (or dated addendum to `H4_GP_switch_hopfion_MAP.md`)  
- Premise ledger + ready/not-ready for Stage B  
- Commit + push `grok`

### Stage B (only if ready)
- `hopfion_GP_switch_apply_results.md` + small JSON  
- T1–T5 table; grade CONDITIONAL/LEAD until blind pass  
- Update LIVE NEXT only after bank  
- Optional: dedicated blind adversarial pass before hard-BANK  

---

## 8. Suggested routing language for LIVE (after Stage A)

If MAP only:  
`NEXT = Stage B apply if MAP green; else residual L time-live parallel.`

If Stage B banks active-P or dead-G character:  
`NEXT = interpret mass/flux under that character + φ_amb table; not source shopping.`

---

## One-line for the implementer

**MAP the hopfion G/P switch (χ/N1 crux, no topology slogans); only then run a bounded interior pin diagnostic on H3 — Phase 2 already killed core source-engineering for de-box.**
