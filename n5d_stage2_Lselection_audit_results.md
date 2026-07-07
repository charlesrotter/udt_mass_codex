# N5d Stage-2 L-SELECTION AUDIT — embedded / critical-universe coupling (π₂ static S-Dir; DESIGN/PROVISIONAL/Outcome D)

**Date:** 2026-07-06 (EOD-3) · **Author:** Claude Opus 4.8 (1M). **Derivation/audit only — NO code, NO pilot, NO
implementation, NO S-JC2/FIX-2/higher-ℓ/time-live, NO finite-L target/penalty/anchor/mass-data.** Status: **DESIGN /
PROVISIONAL / Outcome D.** π₂ static S-Dir tile ONLY. **NO Outcome A/B, NO pin/continuum, NO π₃ claim, NO physics
verdict.** Synthesis of already-blind-verified repo results (cited file:line) + a DOF argument + two cheap
forward-eval tests run here (both self-correcting). Where a claim is my synthesis vs derived-elsewhere is marked.

## 0. Banked inputs (from the gauge audit, blind-verified)
Soft mode = removable ρ-rescale + φ-offset GAUGE (2-pin [ρ(r_c),φ(r_c)] fix, no physics change); after gauge-fix,
H(r_s)=0 does NOT pin L (free-L runs away, incl. negative L); Class-A mirror cells have q_raw=M_readout=0 (φ'(r_s)=0).

## 1. Closed-cell residual after φ/ρ gauge quotient + DOF count
The gauge-quotiented system = the free-L residual (φ-ODE + φ-mirror(2), ρ-ODE + ρ-mirror(2), f-PDE + f_r-mirror,
Hseal, shear-ODE + shear-core + shear-seal) **+ 2 gauge pins [ρ(r_c)=const, φ(r_c)=const]**, with the **Class-A seal**
BC φ'(r_c)=φ'(r_s)=0 (`cell_solver_f2d.py`, "smooth mirror fold, Class A"). Remaining free DOF after the 2 pins:
- physical fields φ(r),ρ(r),f(r,θ),a2(r) — determined by the ODEs+BCs at any given L;
- **the cell length L — 1 remaining scalar, UNPINNED** (H(r_s)=0 is gauge-dependent/degenerate w.r.t. L).

⇒ **DOF after gauge quotient = exactly ONE unselected scalar: L.** The static S-Dir tile is underdetermined by one
condition on the cell size.

## 2. L-flat-direction diagnosis (item 3)
- **The isolated tile provably CANNOT select L:** free-L solves run L away (to ~1e3, 1e6, and negative L) at
  Hseal~0 (gauge audit, blind-verified). H(r_s)=0 is satisfied along the whole L-curve.
- **The flat direction is NOT a simple geometric rescaling:** tested here — applying (ρ→αρ, L→αL, φ/f/a2 unchanged)
  to a relaxed L=1 cell gives ‖F‖²=9.0 (α=½), 0.56 (α=2), i.e. NOT a solution ⇒ naive scaling is not the symmetry.
- **No physical observable distinguishes the L-family:** q_raw ≡ 0 for every Class-A mirror cell (φ'(r_s)=0), so the
  seal flux cannot label L (gauge audit; this session's 2nd self-correction retracted "q_raw∝L ⇒ modulus").
- **Verdict (item 3): primarily (b) — L is a modulus requiring an EXTERIOR matching condition**, because the isolated
  tile cannot pin it and carries no scale. Its internal character (pure scaling redundancy (a) vs physical modulus vs
  coordinate artifact) is NOT settled by the isolated tile and does not need to be — the operative fact is that
  **L-selection is inherently EXTERNAL/embedding**, consistent with vacuum being scale-free and the π₂ topological
  matter carrying no intrinsic length (memory: matter is the scale-breaker but a winding DEFECT is scale-covariant;
  the SCALE is cosmic — the universe cell's Misner-Sharp mass, memory `dynamic-msscale-synthesis`).

## 3. Native embedded-cell matching candidates (item 4) — all DERIVED from UDT geometry
| candidate | equation | source (file:line) | status |
|---|---|---|---|
| **JC1 dilation-flux continuity** | `[√h Z_φ φ'] = 0`; round `q=(r²φ')_seal` | `seal_matching_junction_results.md:14-27` | DERIVED (CAS+blind) |
| **JC2 transverse-momentum continuity** | `π^{AB}=c√h W_χ e^{-φ}(K^{AB}−Kh^{AB})`; `[π^{AB}]=0` | `seal_matching_junction_results.md:29-40` | DERIVED |
| **Embedded closure (Hamiltonian match)** | `H_cell(r_s) = H_amb(r_s)` | `embedded_cell_closure_H_amb_results.md:31-34` | DERIVED (blind adb6620f) |
| **Embedded momentum match** | `π_cell = π_amb` (= JC1+JC2 cell↔ambient) | `embedded_cell_closure_H_amb_results.md:31-34` | DERIVED |
| **Criticality closure** | `E_m(r_c)=2` (⇔ `c²=2GM/R`, `H_tot(fold)=0`) | `universe_cell_fold_jc_sigma_results.md:55-57`; `H4_N5a:41-46` | closure DERIVED; frame ADMITTED; **scale NOT pinned** |
| **Misner-Sharp boundary balance** | `m=−q−q²/r+…`; `M=−q` (O(1/r)); `Π_φ=−Z_φM=Z_φq` | `H4_N2_farfield_reduction_results.md:67-73`; `H4_N5b:63,77` | DERIVED; boundary/seal quantity |

## 4. Classification of each candidate (item 5)
- **`H_cell(r_s)=H_amb(r_s)` (embedded Hamiltonian match): THE independent, native L-selector.** Derived from the
  two-domain shared-seal corner variation; it is a NEW condition (the ambient/universe cell's H_amb selects which cell
  SIZES close) — NOT implied by the isolated interior rows. This is the geometric L-selector the audit was looking for.
- **`π_cell=π_amb` (=JC1/JC2 cell↔ambient):** the flux/momentum continuity; makes the cell CHARGED (q≠0) and matches
  the flux to the exterior. Independent (replaces the Class-A mirror π_cell=0).
- **JC1/JC2 alone:** already the seal continuity structure; for a vacuum ambient they REDUCE to the Class-A mirror
  (π_cell=0, H_cell=0, q=0) — i.e. already-implied, no new L-selection.
- **Criticality `E_m(r_c)=2` / `c²=2GM/R`:** a DERIVED closure but it is ONE relation with the scale R UNPINNED
  (`H4_N5a:104-116`); it gives a mass–size RELATION, not an absolute L. The only thing that would pin R is the depth
  anchor φ_seal=7.004=ln(1+z_CMB) — which is z_CMB DATA (forbidden data-blind). Frame is ADMITTED (sub-canon), not derived.
- **MS boundary balance:** the charge/mass readout of the embedded seal (q=Zρ_s²φ'), not itself an L-selector.
- **Inadmissible (correctly excluded, item 6):** none of the above fixes L numerically or uses mass data; the ONE
  data-dependent scale-pin (z_CMB via φ_seal=7.004) is explicitly rejected here (data-blind). The universe MS mass as a
  STRUCTURAL scale-setter is canon (finite-cell), but it is a COSMIC input, not an isolated-tile quantity.

## 5. Can the static mirrored tile ever produce a nonzero readout? (item 7) — NO
Class-A mirror (φ'(r_s)=0) ⟹ q_raw=Zρ_s²φ'(r_s)=0 IDENTICALLY. A nonzero physical readout REQUIRES **Class B**:
Dirichlet φ(r_s)=0 with φ' FREE (canon C-2026-07-04-1; `seal_matching_junction_results.md:49-56`), which permits (not
forces) q≠0. So the readout MUST move to the **exterior-matched / Class-B seal** — NOT the isolated mirror. This is the
same isolated→embedded transition as L-selection: **q≠0 and L-selection are unlocked by the SAME move** (Class A→B +
exterior match). It does NOT require the time-live sector: canon's sector split puts the STATIC seal under the spatial
mirror σ_φ (Dirichlet φ(r_s)=0), a static-sector condition. (Open convention flag: M=−q vs M=+q sign + the p_F
factor-of-2 are UNPINNED — `cell_solver_f2d.py:361-364`, `H4_N2:73`; they matter once charge is live.)

## 6. Decision table (item 8)
| question | answer |
|---|---|
| Does embedded matching provide an admissible L-selector? | **YES** — `H_cell=H_amb` (+ `π_cell=π_amb`), native + derived + independent. |
| Does it preserve the 2-pin gauge fix? | **SUBSUMES it** — Class-B Dirichlet φ(r_s)=0 removes the φ-offset gauge; matching ρ to the scale-carrying ambient removes the ρ-scale gauge. The 2 pins were stand-ins for the missing exterior. |
| Does it preserve q_raw=0? | **NO — and that's the point** — Class-B (φ' free) makes q≠0; the charge lives at the embedded seal. |
| Does it require changing the seal BC? | **YES** — Class A (Neumann φ'=0) → Class B (Dirichlet φ(r_s)=0, φ' free). |
| Does it require time-live terms? | **NO for the static seal** (sector split: static-φ under σ_φ). Time-live is a separate sector. |
| Is implementation safe to gate next? | **NO (not as a quick static gate)** — the STATIC embedded-cell EXISTENCE is TOOL-LIMITED: the depth-stiffness wall (`NEGATIVES_REGISTRY.md:20-32`, CHECKPOINT/no-blocking-authority, STATIC-A0 class only, CONDITIONS-CHANGED under ω≠0). And the ABSOLUTE scale is unpinned without a cosmic anchor. |

## 7. Answers to the required report items
1. **DOF after gauge quotient:** exactly ONE unselected scalar — L.
2. **L-flat diagnosis:** the isolated static Class-A tile cannot pin L (free-L runs away, incl. negative L); the flat
   direction is not a simple geometric rescaling; q≡0 gives no physical distinguisher ⇒ L-selection is inherently EXTERNAL.
3. **Candidate embedded equations:** JC1 `[√h Z_φ φ']=0`, JC2 `[π^{AB}]=0`, embedded closure `H_cell(r_s)=H_amb(r_s)`,
   momentum match `π_cell=π_amb`, criticality `E_m(r_c)=2`/`c²=2GM/R`, MS balance `M=−q`.
4. **Which is native + independent:** the embedded Hamiltonian match **`H_cell(r_s)=H_amb(r_s)`** (with `π_cell=π_amb`) —
   the one genuinely new L-selecting condition; it is derived, native, and not implied by the interior rows.
5. **Can the static mirrored tile produce nonzero readout?** NO — Class A ⟹ q≡0; needs Class B (Dirichlet φ(r_s)=0).
6. **L-selection solved / open / points-to-fork?** NOT solved by the isolated tile; **it POINTS to the
   embedded/critical-universe fork** — which is native and derived but (i) tool-limited on the static-A0 slice
   (depth-stiffness wall), (ii) absolute-scale-unpinned without a cosmic anchor (universe MS / z_CMB, cosmic input).
7. **Recommended next gate (Charles decides — reasoning, not a directive):** do NOT re-bang the walled static-A0
   embedded matching. The audit shows the earlier fork options CONVERGE: static-isolated cannot select L; static-embedded
   is walled; the depth-stiffness wall is CONDITIONS-CHANGED under ω≠0. So the live routes are (a) **reframe to
   SCALE-FREE RATIOS** — accept that absolute L is cosmic (the universe cell's MS mass sets it) and take the isolated
   tile's SHAPE/ratios as the deliverable (matches the data-blind "predict RATIOS" posture); or (b) **the embedded + ω≠0
   (rotating/time-live) sector**, where the depth-stiffness wall no longer applies and the charged Class-B seal is
   natural. Both are bigger than a static gate; (a) is the lower-risk, purity-clean next step. A prerequisite for ANY
   charged/embedded work is the Class-A→Class-B seal-BC change (Dirichlet φ(r_s)=0) — implementation, so Charles-gated.
8. **Scope:** π₂ axisymmetric static S-Dir tile only. No Outcome A/B, no pin/continuum, no π₃ verdict.

## 8. Not a physics verdict
This is a native-geometry L-selection audit. It localizes L-selection to the embedding/cosmic sector and identifies
`H_cell=H_amb` as the native selector, but banks no closure, no scale, no charge — the embedded existence is
tool-limited and the absolute scale is cosmic. DESIGN / PROVISIONAL / Outcome D; π₂ tile only.
