# Mini-MAP — the CLASS-B (charged/sourced-core) embedded cell, before compute

**Date:** 2026-07-02. **Mode:** MAP (no compute). **For claude.ai review BEFORE the run** (its ruling:
"draft the mini-MAP on those three, send it back, then run"). **Author:** Claude Code. Foundation:
`cell_solver_f2d_embedded_run_results.md` (embedding rescues finiteness; a mirror core is q≈0=Class A →
can't match a gradient-carrying ambient — blind-verified), `seal_matching_junction_results.md` (derived
seal parity; canon "external charge = dilation flux through the seal"), `embedded_run_gate_rulings.md`.

## 0. Why Class-B (the failure-mode-specific cure, again)
The blind-verified obstruction: a smooth-**mirror** core forces `π_φ,c=0`, and `(Zρ²φ')'=4e^{−2φ}ρ'²≥0`
makes `π_φ,s≥0` built only by ρ-gradients that DRAIN AWAY → a gradient-free (q≈0) cell can't momentum-
match a gradient-carrying ambient. The cure is a **gradient-carrying core**: `π_φ,c=q≠0` = Class B. Three
independently-derived lines converge on it (seal parity; "external charge = seal flux"; the numerical
obstruction) — the strongest signal this program produces (claude.ai).

## 1. THE THREE DERIVATIONS OWED (before the count can be honest)

**D1 — sourced-core junction condition.** Add a core source term to the action, `S_core = q·φ(r_c)`
(a charge q coupling linearly to the dilation at the core — the minimal, physically-motivated source).
Varying φ at the (fixed) core: the natural inner BC shifts from the mirror's `π_φ,c=0` to
    **`π_φ,c ≡ (Zρ²φ')|_{r_c} = q`**  — the canon "external charge = interior dilation flux through the
seal," now at the inner boundary. Minimal Class-B = a φ-charge only: the ρ-sector natural BC is
UNMODIFIED, so **`π_ρ,c=0` (regular ρ core, ρ'_c=0)**. [Tag: linear source = CHOSE-minimal; a ρ-source
or nonlinear source is a variant — see the D-fork in §3. CAS/blind OWED on the variational BC shift.]

**D2 — corner condition at a sourced core (the C2 lesson: check the SOURCE's matter/H part explicitly).**
With **r_c FIXED** (minimal; the cell length r_s−r_c is the modulus, EOMs autonomous in r), there is NO
inner corner condition — only the flux BC `π_φ,c=q`. The source `q·φ(r_c)` carries NO r-kinetic term and
NO angular/winding matter (the winding lives in the BULK, not the core), so its H-contribution is purely
geometric (through q) — there is no independent core matter-H condition (contrast the OUTER seal's
E_ang=m_amb, which exists because the winding skin carries angular energy). [Tag: r_c-DYNAMICAL is a
variant — then a corner condition H_cell(r_c) = (source r-Hamiltonian, = q φ'(r_c) term) appears; CAS/
blind OWED to confirm the source carries no hidden matter-H. Do NOT presuppose it away — geometry alone
misled us once (the C2 lesson).]

**D3 — q's status (free / axis / constrained).** Integrate the verified φ-EOM identity
`(Zρ²φ')'=4e^{−2φ}ρ'²` from core to seal:
    **`π_φ,s = q + ∫_{r_c}^{r_s} 4e^{−2φ}ρ'² dr ≥ q`**  (integrand ≥ 0).
So the seal flux is BOUNDED BELOW by the core charge. Imposing the seal flux-match `π_φ,s=π_φ,amb` gives
    **`q = π_φ,amb − ∫4e^{−2φ}ρ'² dr < π_φ,amb`**  — q is CONSTRAINED by the matching + the interior
profile, NOT a free knob and NOT presupposed-quantized. Whether the allowed q values BAND is an OUTPUT of
the counting + run (the obstruction theorem becomes the matching mechanism — claude.ai point 4).
**LEDGER DISCIPLINE (canon):** N (winding sector, a bulk topological integer) ≠ q (public dilation flux
through the seal). Keep rigorously separate; do not conflate or co-quantize by assumption.

## 2. THE COUNTING (with the charged core)
Core unknowns: φ_c, ρ_c, and **q ≡ φ'_c-freedom** (the mirror had φ'_c=0; Class-B frees it → +1 unknown);
ρ'_c=0 pinned (minimal, D1). Cell size r_s (r_c fixed reference). Ambient axis a.
Seal conditions (5, per Ruling 1): φ, ρ, π_φ, π_ρ continuous (4) + E_ang,cell(r_s)=m_amb (1). [H_geo]=0
is automatic given the 4 → C2 adds only E_ang.
| scenario | unknowns | conditions | determinacy | reading |
|---|---|---|---|---|
| **a FIXED** (scan ambient) | φ_c, ρ_c, q, r_s = **4** | 5 | **OVER-by-1** | cells at ISOLATED a → the **Misner–Sharp band**, with **q DETERMINED** at each |
| **a FREE** | φ_c, ρ_c, q, r_s, a = **5** | 5 | **SQUARE** | isolated (a,q) solutions |
**⇒ The charged core relaxes the Class-A over-by-2 to over-by-1** (q supplies the gradient the mirror
lacked). Over-by-1 at fixed a → scanning a, cells close only at isolated a = the band; q read off along
it. **q-along-the-band is the flux/charge structure** (≠ N; label diagnostic, mark derived value later).

## 3. THE ONE REAL FORK (flag before running) — does a φ-only charge close R4?
The blind verifier found the ρ'-continuity miss **R4 (~+9) was LARGER than the flux miss R3 (~−4)**. The
charged core (D1) directly supplies the φ-flux (fixes R3). **Open: can the BULK ρ-profile develop the
ρ'_s needed to match π_ρ,amb (close R4)?** Two outcomes, both honest:
- (i) YES → minimal Class-B (φ-charge, over-by-1) → the band. The clean result.
- (ii) NO → a **ρ-source is also needed** (fully-sourced core: free φ'_c AND ρ'_c). Count then = 5
  unknowns vs 5 at fixed a → SQUARE → a CONTINUUM of a (one cell per ambient — NOT a band). That would
  say the charged core over-relaxes and discreteness needs a different pin. **Watch R4 specifically.**
The run must REPORT which — do not force (i).

## 4. Model ambient (unchanged from the Class-A run; now the flux is matchable via q)
Same 5-number MODEL ambient on the native radial family (`φ=−q_A/a, ρ=a, π_φ,amb=Z q_A, π_ρ,amb=−4e^{2q_A/a},
m_amb=μ/a²`), q_A=0.5, μ=1.0, Z=8, ONE diagnostic axis a, labeled MODEL; derived universe value deferred.

## 5. What the run does / what counts (pre-registered)
Scan a; at each a solve the interior BVP with the CHARGED core (π_φ,c=q free, ρ'_c=0, f pole BCs) +
outer matched seal; the over-by-1 system closes only at isolated a. A **Class-B embedded cell** = all 5
seal conditions met (R3=R4=R5→0) at an isolated a, with q determined, adapted-Derrick-clean (Ruling 2),
two-tier-stable, seed/grid-robust, UNLABELED. Honest alternatives: NO closure even with q (the charge
doesn't rescue the match → deeper obstruction); a CONTINUUM (fork ii); or the band (isolated a + q).

## 6. Owed BEFORE the run (gate — send back for claude.ai)
1. CAS/blind-verify **D1** (the sourced-core natural BC `π_φ,c=q` from the variational source term).
2. CAS/blind-verify **D2** (no hidden core matter-H; the r_c-fixed vs dynamical statement).
3. Confirm the **counting** (over-by-1 at fixed a) and the **R4 fork** framing.
D3's flux-balance `π_φ,s=q+∫4e^{−2φ}ρ'²≥q` already rests on the blind-verified φ-EOM identity.
**Send-back point: claude.ai checks D1/D2, the count, and the R4 fork before anything executes.**
