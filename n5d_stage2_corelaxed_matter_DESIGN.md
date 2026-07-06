# N5d Stage-2 — Co-Relaxed Matter Solver DESIGN (design only; no code, no pilot)

**Date:** 2026-07-06 · **Author:** Claude Opus 4.8 (1M) · **Status:** DESIGN / PROVISIONAL · no physics verdict,
no Outcome A/B, no continuum lead. Preserves FIX-1 (equilibration), Registration-B (current-L pullback), and the
blind-verified **ρ²/2** source measure factor as infrastructure. Retires Stage-1's **frozen flat hopfion source**
as a verdict tool (diagnostic only) per the §4g embedding audit.

## 0. Framing — what changes from Stage-1 (and what does NOT)

Stage-1 solved the base round matter `f(r,θ)` **plus a FROZEN, imported, flat-space hopfion ℓ=2 shear source**
`sh2(r)`. The embedding audit (§4g) showed that source cannot support a pin/continuum verdict: it lives in a flat
metric (ρ=r, φ=0) while the cell has ρ≠r, carries an O(1)–O(few) uncomputed (r/ρ)^{2..4} component regrade, and is
scale-incompatible with the compact hopfion.

**Stage-2 principle:** the matter is **co-relaxed inside the live off-round N5d cell**, and the shear source is the
**live matter's OWN traceless transverse stress** `T_s = T^θ_θ − T^ψ_ψ`. No flat stress enters the residual.

**Critical existing infrastructure:** `cell_solver_f2d` **already co-solves the native axisymmetric S² winding
matter** `f(r,θ)=θ+u(r,θ)` simultaneously with φ, ρ, L (base rows: φ-ODE, ρ-ODE, f-PDE, Hseal, mirror BCs). So
Stage-2 is NOT a new matter solver. It is three principled edits, all derived from ONE native off-round action:
(i) make the matter feel the shear (off-round metric `e^{±s}` factors in the f-PDE + moments), (ii) replace the
frozen `Tshear` in the shear row by the live `T_s[f,ρ,s]`, (iii) rederive φ/ρ EOMs off-round. At `s=0` (round)
every row must reduce byte-for-byte to the current base.

## 1. Variables (unchanged layout)

`u_vec = [ φ(Nr), ρ(Nr), u_field(Nr·Nth), a2(Nr), L ]` — identical to the N5d layout.
- **φ(r)** — dilation (longitudinal).
- **ρ(r)** — areal radius (transverse trace scale; `√h = ρ² sinθ`).
- **f(r,θ) = θ + u(r,θ)** — native S² map: `n = (sin f·cos Nψ, sin f·sin Nψ, cos f)`, axisymmetric, winding
  degree N (integer). This is the **live, co-relaxed** matter (was frozen-external in Stage-1).
- **a2(r)** — live ℓ=2 traceless shear amplitude, `s(r,θ) = a2(r)·P2(μ)`.
- **L** — cell length; physical `r(ζ) = rc + (L/2)(ζ+1)`.

**PREMISE LEDGER (tag before any solve):** N winding = DERIVED-topological (integer). **TOPOLOGICAL-SECTOR PREMISE
(flag, Charles-gated):** the base map is an axisymmetric S²/π₂ winding *defect*; the frontier working-hypothesis
particle is a π₃ *hopfion* (3D Hopf linking). The axisymmetric (r,θ) reduction carries π₂ winding, NOT full π₃
linking. Stage-2 co-relaxes the π₂-sector native matter; whether the pin/continuum question *requires* the full
π₃ hopfion (⇒ a 3D co-relaxed matter, much heavier) is an OPEN premise to settle with Charles, not decided here.
Z_φ = CHOSE-fixed; ξ, κ = FREE-units (κ/ξ sets the absolute scale; ratios are the observables).

## 2. Native matter action (off-round, φ-blind, h_AB-side)

Target map `n: cell → S²`, `n = (sin f cos Nψ, sin f sin Nψ, cos f)`, `f=f(r,θ)` (axisymmetric ⇒ `∂_ψ f = 0`,
`∂_ψ(Nψ)=N`). Live off-round metric `h_θθ = a = ρ²e^s`, `h_ψψ = ρ²e^{−s} sin²θ`, radial metric `g_rr` (state the
solver's radial convention explicitly in 2a), `√h = ρ² sinθ` (s-independent — the trace scale).

- **L2 (sigma / Faddeev quadratic):** `L2 = (ξ/2) g^{μν} ∂_μ n·∂_ν n =
  (ξ/2)[ f_r²/g_rr + f_θ²/(ρ²e^{s}) + N² sin²f/(ρ²e^{−s} sin²θ) ]`.
- **L4 (Faddeev–Skyrme quartic):** `L4 = (κ/4) F_μν F^μν`, `F_μν = n·(∂_μ n × ∂_ν n) = sin f (∂_μ f·∂_ν(Nψ) −
  ∂_ν f·∂_μ(Nψ))`. Nonzero: `F_rψ = N sin f f_r`, `F_θψ = N sin f f_θ`. ⇒
  `L4 = (κ/2)[ F_rψ²/(g_rr h_ψψ) + F_θψ²/(h_θθ h_ψψ) ]`.
- **φ-BLIND:** `L_m` contains NO φ (only ρ, s, f, g_rr). φ enters only the geometric sector (the `e^{−2φ}`
  measure / back-reaction), never as a direct matter source. **h_AB-side only:** all matter–metric coupling is
  through `h_AB` (ρ, s) and `g_rr`; no `e^{2φ}` on the matter (that was the retired scalar-tensor kluge).

## 3. Source generation — T_s from the LIVE matter (no flat import)

The shear source is the matter's traceless transverse stress, **derived from L_m** (not imported):
- **By variation (canonical):** `δS_m/δs = (√h/2)(T^θ_θ − T^ψ_ψ)` with `δh_θθ = h_θθ δs`, `δh_ψψ = −h_ψψ δs`.
  This is exactly the coupling whose measure weight the blind-verified **ρ²/2** result already fixed — so the
  ρ²/2 emerges AUTOMATICALLY from varying the total action w.r.t. s; no external factor is pasted on.
- **Candidate derived structure (TO BE CAS-VERIFIED in 2a; the −g_μν L trace part cancels in the difference):**
  - `T_s(L2) = (ξ/ρ²)[ f_θ² e^{−s} − N² sin²f · e^{s}/sin²θ ]`,
  - `T_s(L4) = − κ N² sin²f f_r² · e^{s}/(g_rr ρ² sin²θ)`.
  Round + rigid check: at `s=0, f=θ, N=1`, `T_s(L2) → (ξ/ρ²)[1 − 1] = 0` (the rigid hedgehog carries NO shear —
  matches the known `ξ(1−N²)cosθ` rigid residual); the shear is sourced by the deviation `u`, by `N≠1`, and by L4.
- **Residual assembly (same as N5d):** `shear_res(r) = Σ_j w_j P2(μ_j)·(E_s_geom + T_s)_j`, with `E_s_geom` the
  existing `EAB_shear_row`. Because both `E_s_geom` and `δS_m/δs` are the action-density form (ratio=1, §4f), the
  ρ²/2 weight is carried identically on both sides — **verify** the coded `T_s` equals `(ρ²/2)·(T^θ_θ − T^ψ_ψ)`
  as a self-stress consistency test (§7).
- **No flat-source dependence:** `stress_profiles.npz` may seed `u`'s initial guess ONLY; it must NOT appear in the
  residual. (Registration-B's current-L pullback becomes moot for the source since there is no external profile;
  the coordinate map `r(ζ)=rc+(L/2)(ζ+1)` stays.)

## 4. Coupled residual (one native off-round action → all rows)

Derive every row by varying the TOTAL action `S = S_geo[φ,ρ,s] + S_m[f,ρ,s,g_rr]` w.r.t. each field; each must
reduce to the current base row at `s=0`.
1. **φ-equation** (`δ/δφ`): off-round φ-ODE — the base φ-ODE **+** the off-round correction `+(1/5Z)e^{−2φ}a2'²`
   already in `n5d_shear.phi_source_offround_correction`. φ stays blind (no direct matter term).
2. **ρ-equation** (`δ/δρ`): off-round ρ-ODE — the base ρ-ODE with the matter moments generalized off-round (the
   round `I_r, I_4θ` pick up `e^{±s}` in their contractions). At `s=0` = base ρ-ODE exactly.
3. **matter f-equation** (`δ/δf`): off-round elliptic f-PDE — the base `d_r(A f_r)+d_θ(B f_θ) − (…)` with the
   coefficients carrying the shear: `A ⊃ ξ ρ²e^{s} sinθ + κN² sin²f e^{s}/sinθ`, `B ⊃ ξ sinθ e^{−s}? …` (exact
   `e^{±s}` placement from 2a). This is the coupling that makes `f` feel `a2` → co-relaxation.
4. **shear a2-equation** (`δ/δs`, ℓ=2 Galerkin): `Σ w P2 (E_s_geom + T_s[f,ρ,s]) = 0` — the genuinely new,
   self-consistent shear row (§3).
5. **Hseal closure**: `H(r_s)=0` (the free-boundary transversality row) — unchanged in form; generalize `H_of_r`
   to include the off-round shear/matter contributions so it stays the conserved radial Hamiltonian (CAS-check
   `dH/dr=0` on-shell off-round in 2a).
6. **Whole-cell BCs (unchanged):** mirror `φ'=ρ'=f_r=0` at both ends; poles `f(r,0)=0, f(r,π)=π`; shear core
   `a2'(rc)=0`; shear seal per §5. Square count preserved (adding no new unknowns/rows vs N5d).

## 5. Gauge / BC policy

- **S-Dir is the first well-posed tile** (Dirichlet shear seal `a2(rs)=a2_mirror`; the constant-a2 mode is pinned;
  the §4-audit showed S-Dir's shear operator is full-rank/solvable).
- **S-JC2** constant-a2 null is **acknowledged, NOT fixed in this design.** Optional, separately-gated subsection
  (for LATER Charles approval, not part of Stage-2 build): a purely-numerical gauge pin (fix `∫a2` or `a2` at one
  interior node) that removes the unobservable constant offset — **provenance/soundness only, never merit**; it
  would make S-JC2 a post-gauge cross-check of S-Dir, not an independent verdict. Do not implement until approved.

## 6. Anti-collapse discipline (binding)

- **No** finite-L target, penalty, barrier, anti-collapse term, mass-anchor, or fitted scale. κ/ξ remain FREE.
- If **L collapses**, report it as **solver/closure behavior** (as in Stage-1), never patch it. Note (observation,
  not imposition): co-relaxed matter sets its OWN areal stress structure, which *may* change how ρ(r)/L behave vs
  the frozen-source run — we OBSERVE what emerges; we do not steer ρ(r) toward the matter scale.
- The purity/imposition gates (`tests/test_solution_space_gate.py`) must stay green: the T_s source is numeric-
  from-the-action (provenance-clean), not a smuggled shape.

## 7. Minimal implementation plan (staged; tests BEFORE any pilot)

**Stage 2a — DERIVE + CAS-VERIFY (symbolic, no solve):**
- Vary the off-round `S_geo+S_m` w.r.t. φ, ρ, f, s; produce the four EOMs + off-round `H`. CAS-verify each reduces
  to the current base row at `s=0` (and the round matter reduction at `a2=0`).
- CAS-verify `T_s(L2)`, `T_s(L4)` (§3) and that `δS_m/δs = (√h/2)(T^θ_θ−T^ψ_ψ) = (ρ²/2)(T^θ_θ−T^ψ_ψ)` (ties to
  the blind-verified ρ²/2). Independent blind re-derivation of `T_s` (fresh agent) before banking 2a.

**Stage 2b — IMPLEMENT (edit `cell_solver_f2d.py` in place; git-as-git; update `n5d_shear.py`):**
- off-round f-PDE coefficients (`e^{±s}`), off-round ρ/φ moments, the live-`T_s` shear row (delete the frozen
  `src`/`Tshear` from the residual path; keep it importable as a diagnostic seed only), off-round `H_of_r`.

**Tests that MUST pass before a pilot is allowed:**
1. **Round-limit recovery** — `s=0 (a2=0)` ⇒ residual byte-identical to the current base (extend the existing
   `test_roundlimit_base_rows_identical`); `a2=0` shear rows vanish.
2. **φ-blindness** — shifting φ at fixed ρ,f,a2 leaves the matter f-PDE, the ρ moments' matter part, and the
   shear `T_s` unchanged (only the geometric φ/`e^{−2φ}` pieces move).
3. **Self-stress consistency** — the coded shear-row source equals `(ρ²/2)·(T^θ_θ−T^ψ_ψ)` computed independently
   from the live f (CAS identity + a numeric node check).
4. **No flat-source dependence** — a test/grep that the residual imports NO `stress_profiles.npz` value (only an
   optional initial-guess seed for u); removing the npz must not change the residual.
5. **ρ²/2 emergence** — the variation-derived shear source matches the blind-verified `ρ²/2` normalization.
6. **Assembly/preflight** — square (len(u)=len(F)), finite Jacobian, both seal BCs, base-row match 0.0.
- **Bounded / anti-hang:** Nr≤16–24, Nth=8, LM maxit≤30, FIX-1 equilibration on, ONE clean foreground process,
  NEVER background-poll a solve. Fixed-background eigen/linear diagnostics are cheap; the coupled dense-LM is the
  flooring tool — recompute on saved fields where possible.

## 8. Decision gates

**Before a Stage-2 PILOT is allowed (ALL required):** 2a CAS checks pass + independent blind re-derivation of
`T_s` + all 2b tests (1–6) green + preflight both BCs + FIX-1 equilibrated conditioning demonstrably manageable at
a *structured* state (not the collapsed degenerate one) + a clean premise ledger (topological sector flagged,
Z_φ/ξ/κ tagged).

**Counts as TOOL-LIMITED (Outcome D):** non-convergence (Φ floored above tol), Jacobian at the float64 floor after
equilibration, or an L-collapse that prevents a read — reported as solver/closure behavior, no A/B, exactly as
Stage-1.

**Counts ONLY as an S-Dir TILE LEAD (not A/B):** a CONVERGED S-Dir solve yielding a pin-or-continuum readout for
the ℓ=2, axisymmetric-matter, Branch-P, static, block-diagonal tile — labeled SCOPED to that corner, with its
premise set; a LEAD for Charles to ponder, never a banked result.

**CANNOT be banked as Outcome A/B until ALL:** (a) higher-ℓ shear included (not ℓ=2-only); (b) BC-fork survival
(S-Dir and a gauge-fixed S-JC2 agree); (c) co-relaxed source (this Stage-2) — done; (d) the topological-sector
premise (π₂ defect vs π₃ hopfion) settled with Charles; (e) blind-verifier pass on the load-bearing rows; (f)
Charles's explicit go (DERIVE is gated). Absent any one, the result stays PROVISIONAL / a LEAD.

---
**Stop:** design + implementation plan only. No code written, no pilot run. No physics verdict, no Outcome A/B, no
continuum lead. Next action is Charles-gated: approve/adjust this design (esp. the topological-sector premise and
the S-JC2 gauge subsection) before Stage 2a derivation begins.
