# ARCHIVED from LIVE.md (2026-07-07) — N5d Stage-2 static S-Dir arc detail + Stage-2b pinned formulas

> Archived out of LIVE.md to keep the first-read file lean. This is the DETAILED narrative of the now-CLOSED
> Stage-2 static arc (the historical RESUME-HERE) + the Stage-2b pinned formulas. Canonical records = the
> result docs (`n5d_stage2_*_results.md`, `n5d_stage2a_cas_results.md`, `n5d_stage2b_gate05_report.md`) and the
> live code (`cell_solver_f2d.py`). LIVE.md's CURRENT-STATE block + the arc-chain fence are the frontier.

**➤➤ (HISTORICAL RESUME-HERE, superseded) the static S-Dir π₂ collapse is now fully DIAGNOSED and
BLIND-CONFIRMED (gauge audit, `n5d_stage2_gauge_audit_results.md`). The soft mode is a MIX:** (1) a **removable
global ρ-rescale + φ-offset GAUGE** (cos(v_ρ,ρ)=+1.000, cos(v_φ,1)=+1.000; Hseal moves along it while ρ-shape/matter-
moments/q_raw stay fixed ⇒ Hseal is gauge-dependent) — a **2-pin category-A fix [fix ρ(r_c) + fix φ(r_c)]** removes it
(cond 3.4e8→7.6e7, workable-not-pristine; q_raw invariant to 1e-13) and gives a well-conditioned Hseal=0 closed cell
at a CHOSEN L; PLUS (2) an **undetermined L flat direction** — even after the gauge-fix, H(r_s)=0 does NOT pin L (a
free-L solve runs L away to ~1e3/1e6/negative at Hseal~0). **Unique closure OPEN.** ⚠ **SELF-CORRECTION (2nd this
session, blind-caught): my "q_raw varies with L ⇒ L is a physical modulus" was WRONG — q_raw=Zρ_s²φ'(r_s)≡0 on-shell
for EVERY Class-A mirror cell (φ'(r_s)=0 is a mirror BC), so q_raw can't distinguish L-cells; the q_raw-vs-L trend I
saw was a convergence residual.** So whether L is a physical modulus vs a scaling redundancy is ITSELF OPEN (q_raw≡0
can't tell — and the seal flux + M_readout are structurally ZERO for these mirror cells). **BLIND VERIFIER (agent
`a2969cef559b1ac72`, neutral gauge-vs-modulus framing, forbidden the audit scripts): gauge CONFIRMED, 2-pin fix
CONFIRMED (cond~8e7 caveat), L-modulus PARTIAL (conclusion "no unique L / OPEN" confirmed; the q_raw evidence
refuted).** Records: `n5d_stage2_gauge_audit_results.md` + `n5d_stage2_gauge_audit.py`. **The category-A work is DONE:
the φ/ρ gauge ambiguity is removed; what remains is L-SELECTION.**

**L-SELECTION AUDIT DONE (2026-07-06, `n5d_stage2_Lselection_audit_results.md`; native-geometry synthesis of
blind-verified repo results + 2 self-correcting forward-eval tests):** after gauge quotient exactly ONE unselected
scalar remains = L, and the **isolated static Class-A tile PROVABLY cannot select it** (free-L runs away incl.
negative L; the flat direction is NOT a simple geometric rescaling — tested; q≡0 gives no distinguisher). ⇒
**L-selection is inherently EXTERNAL/embedding.** The native, derived, independent L-selector is the **embedded
Hamiltonian match `H_cell(r_s)=H_amb(r_s)` (+ `π_cell=π_amb`)** (`embedded_cell_closure_H_amb_results.md`). Key
structural results: (i) **q≠0 and L-selection are unlocked by the SAME move** — Class-A mirror (φ'(r_s)=0, q≡0) →
Class-B (Dirichlet φ(r_s)=0, φ' free, q≠0) + exterior match; the current tile is the legitimate ISOLATED Class-A
completion (NOT a superseded BC — checked CANON.md directly; class choice = Charles's call). (ii) embedding SUBSUMES
the 2 gauge pins (Class-B Dirichlet removes φ-offset; ambient-match removes ρ-scale). (iii) **the static embedded
route is TOOL-LIMITED (depth-stiffness wall, `NEGATIVES_REGISTRY.md:20-32`, CONDITIONS-CHANGED under ω≠0)** and the
ABSOLUTE scale is unpinned without a cosmic anchor (universe MS / z_CMB=data-forbidden). (iv) static seal ⇒ NO
time-live needed (sector split). **NEXT = a CHARLES fork decision** (none unprompted): the audit shows the forks
CONVERGE — recommend (a) **reframe to SCALE-FREE RATIOS** (absolute L is cosmic; take the tile's shape/ratios,
matches the data-blind "predict RATIOS" posture — lower-risk, purity-clean) OR (b) the **embedded + ω≠0
(rotating/time-live) sector** (where the depth-stiffness wall lifts and the charged Class-B seal is natural). A
prerequisite for any charged/embedded work = the Class-A→Class-B seal-BC change (Dirichlet φ(r_s)=0), which is
implementation (Charles-gated). Open convention flag: M=−q vs M=+q sign + p_F factor-of-2 (matter once charge is live).
**MS/EMBEDDED-BOUNDARY SELECTOR AUDIT DONE (`n5d_stage2_MS_boundary_selector_audit_results.md`):** the embedded/MS
package (B1 `[h_AB]=0`, B3 `π_cell=π_amb`, B4 `H_cell=H_amb`=size-selector, B5 `m=−q−q²/r`) is a CLOSED native
data-blind framework for a mass–size RELATION + ratios but does NOT select absolute L (B4 needs the ambient/universe
MS mass; only pin = z_CMB via φ_seal=7.004 = DATA-forbidden). SIGN: **`M=−q` DERIVED** (metric identity `m=−q−q²/r`,
code-consistent `M_readout=−q_raw`, gives POSITIVE mass with φ'(r_s)<0); `M=+q`=reporting deviation; genuinely-open
tension = φ-depth-sign (φ<0 deep) ↔ positive-mass-far-field (φ>0) reconciliation (Charles's canon call); p_F factor
separate+unpinned. Data-blind deliverables = RATIOS (compactness `2M/R=1`, shape profiles; with Class B, mass ratios
`M_i/M_j=q_i/q_j`); Class-A NOW gives q=M=0 (shape ratios only). Class-B impl = bounded seal-BC swap (φ'(r_s)=0→
φ(r_s)=0), safe as a DIAGNOSTIC (flag isolated-charge consistency + DOF recount), gated. **Honest static-tile
deliverable = RATIOS, not absolute mass/size.**
**CLASS-B SEAL DIAGNOSTIC DONE (`cell_solver_f2d.py` `seal_phi="A"|"B"` + `n5d_stage2_classB_diagnostic.py`/`_results.md`;
Class A default byte-identical, pytest 67/1xfail):** Class B = outer φ row φ'(r_s)=0 → DIRICHLET φ(r_s)=0 (φ' free ⇒
q live). RESULT: **Class B REMOVES the φ-offset gauge (drop-Hseal cond 4.76e9→1.47e4; hard null gone) and turns
Hseal=0 from gauge-slideable into a REAL closure (correct charged-cell behavior). BUT the ISOLATED static Class-B tile
does NOT cleanly close: fixed-L OVER-determined (Phi=0.12 at good cond 1.2e4, Hseal≠0), free-L (133×133) STALLS (L
stuck at seed). q_raw at residual floor → NOT genuine; NO absolute L selected.** Points (as the MS/L-selection audits
predicted) to needing an EXTERIOR/receiver for the seal flux (embedding); mass ratios gated behind a Class-B solver
advance OR the embedding fork. **NO Outcome A/B, NO pin/continuum, NO π₃; π₂
tile ONLY; DESIGN/PROVISIONAL/Outcome D.** (Session chain, all committed+pushed+blind-verified: Stage-2b impl
`6a0ac15` → preflight READY → S-Dir pilot=L-COLLAPSE `652b484` → mechanism mis-diagnosed `f02f3f9` → RETRACTED
`d729dd4` → soft-mode blind-CONFIRMED `5c6f6ac` → gauge audit = ρ/φ-gauge + L-flat, q_raw≡0 (here). LESSON, now TWICE:
I over-read a residual/valley artifact as physics twice this session; NEUTRALLY-framed blind verifiers caught both —
frame every verifier to adjudicate, never to confirm my read. Pinned-formula block below stands.)**

**What Stage-2b implemented (all pinned, CAS + blind-verified — the historical build reference below is retained):**
Read `n5d_stage2_corelaxed_matter_DESIGN.md` + `n5d_stage2a_cas_results.md` (§1-8) + `n5d_stage2b_gate05_report.md`
(λ=−½). **THE PINNED FORMULAS (all CAS + blind-verified; now LIVE in `cell_solver_f2d.py` `fields()`/`H_of_r()`):**
- **Off-round f-PDE** (Stage-2a §1, λ-free, matches base at s=0): `A/f_r = ξρ²sinθ + κN²sin²f·e^{s}/sinθ`;
  `B/f_θ = ξ·e^{−s}·sinθ + κN²sin²f/(ρ²sinθ)`; `pot = (N²sinf cosf/sinθ)[e^{s}(ξ+κf_r²) + κf_θ²/ρ²]`; `s = a2(r)P2(μ)`.
- **Live shear source** (REPLACES the frozen `Tshear`/`src`): `Tshear_live = −(ρ²/4)·T_s` with
  `T_s = (ξ/ρ²)[N²e^{s}sin²f/sin²θ − f_θ²e^{−s}] + (κN²/ρ²)f_r²e^{s}sin²f/sin²θ` — the **λ=−1/2** coupling
  (Gate-0.5, blind-verified: NOT the naive +(ρ²/2)T_s, which was 2× + sign-flipped). φ-blind, h_AB-side.
- **ρ-EOM matter term: UNCHANGED** (Stage-2a §6: `δS_m/δρ` is s-independent → already the base's `ξρI_r − κN²I_4θ/ρ³`).
- **φ off-round correction: UNCHANGED** (certified `n5d_shear.phi_source_offround_correction = +(1/5Z)e^{−2φ}a2'²`).
- **Off-round Hseal** (Gate-0.1 + Gate-0.5): base H **+ shear kinetic `+(1/10)e^{−2φ}ρ²a2'²`** + off-round matter
  moments `−(ξ/2)ρ²I_r + (ξ/2)(I_θ^{e^{−s}} + N²I_s^{e^{s}}) − (κN²/2)I_4r^{e^{s}} + (κN²/2)I_4θ/ρ²` (fold `e^{±s}`
  INSIDE the θ-integral: I_θ×e^{−s}, I_s×e^{s}, I_4r×e^{s}; I_r, I_4θ unchanged) − 2. → base H at s=0.
- **Frozen `stress_profiles.npz`: RETIRED from the residual** (embedding audit §4d/§4g invalidated it for verdicts);
  keep only as an OPTIONAL initial-guess seed. **S-Dir = first well-posed tile; S-JC2 constant-a2 null UNCHANGED (no FIX-2).**
**TESTS (DONE — GREEN, `tests/test_n5d_stage2.py`, 8 required gates as 12 functions):** round-limit (s=0→base
byte-identical) · φ-blindness · self-stress (source = −(ρ²/4)T_s, NOT +(ρ²/2)) · rigid hedgehog (T_s(L2)=0 @
s=0,f=θ,N=1) · no-flat-source (residual byte-unchanged with npz/source_interp disabled) · Hseal round-limit ·
K=1/5 pin (H shear kinetic ↔ φ-correction) · preflight (square, finite Jac, both BCs, FIX-1 on, bounded, one
foreground process). Also updated: `test_n5d_roundlimit` (rigid null), `test_n5d_offround` (live-source φ-blind),
`test_n5d_pullback` (frozen src/Tshear now a SEED helper, guarded OUT of the residual). **ANTI-HANG binding. NO
finite-L target/penalty/barrier/anti-collapse/fitted-scale/mass-anchor. TOPOLOGY: π₂ tile ONLY — CANNOT bank
Outcome A/B for the π₃ hopfion question (open premise for Charles).** Stage-2 PILOT = SEPARATE Charles gate (above).
Status: DESIGN/PROVISIONAL/Outcome D throughout.
**Do NOT run `branchGP` (fenced wrong frame).**
**COMMIT + PUSH discipline (binding, standing): commit per logical milestone (the residual edit, then each test as
it passes) AND `git push origin main` in the SAME step as every commit** (Charles 2026-07-06 — never leave commits
local; see CLAUDE.md "Repo discipline" + memory `always-push-on-commit`). End every commit body with the
`Co-Authored-By` trailer.
