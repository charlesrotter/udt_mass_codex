# N5d Stage-2 Misner-Sharp / EMBEDDED-BOUNDARY SELECTOR AUDIT (π₂ static S-Dir; DESIGN/PROVISIONAL/Outcome D)

**Date:** 2026-07-06 (EOD-3) · **Author:** Claude Opus 4.8 (1M). **Derivation/audit only — NO code, NO pilot, NO
Class-B edit, NO S-JC2/FIX-2/higher-ℓ/time-live, NO finite-L target/penalty/anchor/mass-data/z_CMB.** Status: **DESIGN
/ PROVISIONAL / Outcome D.** π₂ static S-Dir tile ONLY. **NO Outcome A/B, NO pin/continuum, NO π₃, NO physics verdict.**
Synthesis of already-blind-verified repo results (file:line) + a sign derivation. Question: does the native
embedded/Misner-Sharp boundary package supply a CLOSED, DATA-BLIND L-selection framework, or is absolute L cosmic?

## 1. The embedded boundary package (native, derived)
Two-domain shared-seal (cell↔ambient) corner variation `δS|_seal=(π_cell−π_amb)Δq+(H_amb−H_cell)δr_s=0`
(`embedded_cell_closure_H_amb_results.md:19-34`) gives, together with the seal JCs:
| # | boundary equation | source | status |
|---|---|---|---|
| B1 | induced-metric continuity `[h_AB]=0` (ρ, transverse 2-geom continuous) | JC1 premise, `seal_matching_junction_results.md` | DERIVED |
| B2 | φ boundary condition (Class A vs B, see §3) | canon C-2026-07-04-1; `seal_matching_junction_results.md:49-56` | DERIVED classification |
| B3 | momentum match `π_cell=π_amb` (JC1 `[√h Z_φ φ']=0` + JC2 `[π^{AB}]=0`) | `seal_matching_junction_results.md:14-40` | DERIVED |
| B4 | Hamiltonian match `H_cell(r_s)=H_amb(r_s)` (the SIZE-selecting closure) | `embedded_cell_closure_H_amb_results.md:31-34` | DERIVED (blind adb6620f) |
| B5 | Misner-Sharp balance `m=−q−q²/r+…`, `Π_φ=−Z_φM=Z_φq` | `H4_N2_farfield_reduction_results.md:67-73`, `H4_N5b:63,77` | DERIVED (blind) |
For a VACUUM ambient (H_amb=0, π_amb=0) B4→`H_cell=0` and B3→`π_cell=0` (Class-A mirror, q=0). A GRADIENT-carrying
ambient (universe cell) makes B3/B4 non-trivial ⇒ q≠0 and a selected size. **B4 is the L-selector; it needs H_amb.**

## 2. Misner-Sharp / q / Π_φ SIGN DERIVATION (item 2/3)
**Derived metric identity (NOT a convention).** Far-field match: `(1−2m/ρ)=e^{−2φ}ρ'²` with the Coulomb tail
`φ=−q/r`, `φ(∞)=0`, `ρ=r`. Expand `e^{−2φ}=1+2q/r+2q²/r²`, `ρ'=1`:
```
1 − 2m/r = 1 + 2q/r + 2q²/r²   ⇒   m = −q − q²/r + O(1/r²)      [H4_N2:67-73, blind-verified]
⇒  M ≡ (O(1/r) mass) = −q ;   the genuine nonlinear −q²/r departs at O(1/r²).
```
This ties |M| to |q| by the METRIC — orientation-fixed once (φ=−q/r, M = 1/r-coefficient of the potential) are set.

**q_raw and its sign.** `q_raw = Z ρ_s² φ'(r_s)` (`cell_solver_f2d.py:375`). Far-field `φ'=q/r²` ⇒ at the seal
`q_raw ≈ Z ρ_s² (q/r_s²) ≈ Z·q` (ρ_s≈r_s) — **q_raw and q share sign** (factor Z>0). `Π_φ = Z·q_raw`
(`cell_solver_f2d.py:376`) = the Gauss-budget flux (`H4_N5b:63`: `Π_φ(R)=−2∫√h𝒦=Q_φ`). `M_readout=−q_raw`
(`SIGN_CONVENTION=−1`, `cell_solver_f2d.py:377`) — **the code follows the DERIVED `M=−q`.**

**Positive-mass check (fixes the physical orientation).** A positive attractive mass needs `g_tt=−(1−2GM/rc²)` ⇒
`e^{−2φ}=1−2GM/rc²` ⇒ `φ=+GM/rc²>0` far-field ⇒ `φ'(r_s)<0` ⇒ `q_raw<0` ⇒ `q<0` ⇒ `M=−q>0`. **So `M=−q` yields
POSITIVE mass with `φ'(r_s)<0` — self-consistent.** ⇒ **`M=−q` is the CANONICAL (metric-derived) convention; `M=+q`
(the depth/size node) is a REPORTING deviation** (opposite q-sign or `M≡−m_geom`).

**The residual, UNRESOLVED tension (Charles's canon call — NOT adjudicated here).** The positive-mass far-field wants
`φ>0` OUTSIDE, but the depth convention has `φ<0` DEEP (`e^{−2φ₀}~5` at hadronic depth ⇒ φ₀<0). These require φ to
CHANGE SIGN between the deep interior and the far field (or a dilation-sign convention distinct from GR's potential).
This φ-depth-sign vs positive-mass reconciliation is the open item behind the `M=−q` / `M=+q` flag
(`cell_solver_f2d.py:361-364`, `H4_N2:73`). **The `p_F` factor-of-2 (`Q=2p_F`) is a SEPARATE normalization convention,
also UNPINNED** (`H4_N2:73`, `H4_backreaction_mass_MAP.md:157`).

**Verdict (item 4):** `m=−q−q²/r` and `M=−q` are DERIVED (metric/orientation-fixed, code-consistent). What is merely
REPORTING: the alternative `M=+q` labeling and the `p_F` factor. What is genuinely OPEN: the φ-depth-sign ↔ positive-
mass reconciliation (a canon call), and the `p_F` factor-of-2.

## 3. Is Class B canonically required for nonzero readout? — YES
Class-A mirror ⟹ `φ'(r_s)=0` ⟹ `q_raw=Zρ_s²φ'≡0` ⟹ `M_readout=0`. A nonzero readout REQUIRES **Class B**: Dirichlet
`φ(r_s)=0` with `φ'` FREE (canon C-2026-07-04-1 `CANON.md:373`; permits, does not force, q≠0 —
`seal_matching_junction_results.md:46-47`). Canon puts the STATIC seal under the spatial mirror σ_φ ⇒ Dirichlet
`φ(r_s)=0`. So **Class B is the canonical static exterior-matched seal for a CHARGED cell; Class A is the isolated
chargeless completion** (class choice = universe-vs-matter, Charles holds, `seal_matching_junction_results.md:63`).

## 4. Does the MS/embedded package select absolute L? (item 5/6) — NO; only a relation + ratios
- **Not absolute L.** B4 `H_cell=H_amb` ties the cell to the ambient; without `H_amb` (the universe cell / its MS
  mass), the size is unset. The criticality closure `E_m(r_c)=2 ⇔ c²=2GM/R` is ONE relation with R UNPINNED
  (`H4_N5a:104-116`); the only absolute-scale pin is `φ_seal=7.004=ln(1+z_CMB)` = **z_CMB DATA (forbidden here).**
- **Only a mass–size RELATION + dimensionless RATIOS.** In geometric units (G=c=1) the derived, data-blind content is:
```
   compactness:      2M/R = 1           (critical, from E_m(r_c)=2 / c²=2GM/R)   [derived closure; frame admitted]
   mass–charge:      M = −q             (+ nonlinear m=−q−q²/r)                   [derived metric identity]
   shape:            ρ(r)/ρ(r_s),  φ(r)−φ(r_s),  a2(r),  f(r,θ)   all dimensionless profiles
   (cross-cell)      M_i / M_j = q_i / q_j   — a pure number if ≥2 charged cells exist
```
  These are RATIOS / dimensionless; the ABSOLUTE M (or R, or L) is the single missing dimensionful input.

## 5. Scale-free deliverables available NOW vs what needs Class B (item 8)
- **NOW (Class A, current tile):** only the geometric SHAPE ratios (ρ-profile, φ-profile shape, a2, f, compactness
  2M/R). But `q=M=0` for Class A, so **NO mass and NO mass-ratios** from the current tile.
- **Needs Class B (nonzero q):** any MASS or mass-RATIO deliverable. A cross-cell mass ratio `M_i/M_j=q_i/q_j` would be
  a scale-free number computable from two Class-B cells — **IF** an isolated Class-B charged cell is consistent (open:
  a net seal flux needs an exterior / the mirror-fold image to receive it; §6).
- **Never from the static tile:** the absolute mass/size scale (cosmic).

## 6. What remains cosmic/external (item 6)
The single dimensionful scale (absolute M, R, or L) is COSMIC — set by the universe cell's Misner-Sharp mass (the
finite-cell canon; memory `dynamic-msscale-synthesis`), whose only data-blind fixation would be the universe-cell
solution itself (not the isolated matter tile) and whose empirical anchor (z_CMB via φ_seal=7.004) is DATA-forbidden
here. **So absolute L is irreducibly external; the static π₂ tile's honest deliverable is RATIOS.**

## 7. What Class-B implementation would need (item 7/9; do NOT implement)
A bounded seal-BC swap in the residual: replace the outer φ-mirror row `φ'(r_s)=0` with the Dirichlet row
`φ(r_s)=0`, leaving `φ'(r_s)` free (→ q output). Consequences to handle: (i) the φ-offset gauge is REMOVED (Dirichlet
pins φ at the seal) — recheck the DOF count/closure; (ii) `q=Zρ_s²φ'(r_s)` becomes a live nonzero output; (iii) the
ISOLATED-Class-B consistency question — a net seal flux needs the exterior/mirror image to receive it (flux
conservation), so an isolated charged static cell may be ill-posed without the ambient or the fold-image treatment.
**Safe to gate NEXT as a bounded DIAGNOSTIC** (does a Class-B static cell close? what q, what compactness, does L
behave differently?) — but it is NOT a physics result on its own (isolated-charge consistency + L-still-cosmic), and
it is Charles-gated implementation.

## 8. Required-report answers
1. **Embedded boundary equations:** B1 `[h_AB]=0`, B2 φ-BC (Class A/B), B3 `π_cell=π_amb` (JC1+JC2), B4
   `H_cell(r_s)=H_amb(r_s)` (size-selector), B5 MS balance `m=−q−q²/r`.
2. **MS/q/Π sign:** `m=−q−q²/r`, `M=−q` DERIVED (metric-fixed, code-consistent `M_readout=−q_raw`); `q_raw` shares sign
   with `q`; `M=+q` is a reporting deviation; open tension = φ-depth-sign ↔ positive-mass; `p_F` factor UNPINNED.
3. **Class B canonically required for nonzero readout?** YES (Class A ⟹ q≡0; Dirichlet φ(r_s)=0 needed).
4. **L selected or only related?** Only a mass–size RELATION (`2M/R=1`) + dimensionless ratios; absolute L NOT selected.
5. **Scale-free ratio deliverables NOW:** geometric shape ratios + compactness; mass-ratios need Class B.
6. **Cosmic/external:** the single absolute scale (M/R/L) — universe-cell MS mass; empirical anchor z_CMB DATA-forbidden.
7. **Class-B implementation safe to gate next?** As a bounded DIAGNOSTIC, yes (Charles-gated); flag the isolated-charge
   consistency + DOF recount; it does not by itself select L (still cosmic).
8. **Scope:** π₂ static S-Dir tile only; no Outcome A/B, no pin/continuum, no π₃ verdict.

## 9. Bottom line (not a physics verdict)
The embedded/MS boundary package is a CLOSED, native, data-blind framework for a mass–size RELATION and ratios, but
it does NOT supply an absolute L: the size-selector B4 needs the ambient/universe MS mass, which is cosmic. `M=−q` is
the derived convention. Nonzero mass needs Class B. So the static π₂ tile's data-blind deliverable is RATIOS (and,
with Class B, mass ratios); the absolute scale is irreducibly cosmic. DESIGN/PROVISIONAL/Outcome D; π₂ tile only.
