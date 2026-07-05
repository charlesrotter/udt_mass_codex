# NODE 1 — The native seal does not kill or quantize a spinning internal phase (Fork-3b, ω≠0 reframe)

**Status: BANKED (Charles 2026-07-04). Blind-verified. No numeric compute — symbolic/CAS derivation.**
Deriver agent a8d2e3c6fbac4dd7a; blind adversarial verifier a9242935198f7945a (SUPPORTED, no refutations,
GR-clean, two revisions folded in). Part of the ω≠0 angular-sector reframe
(`microphysics_reentry_omega_reframe_MAP.md`, NODE 1). Builds on NODE 0.5 (`node05_seal_parity_regrade_results.md`).

## Verdict: outcome (3) — the seal is ω-BLIND. F1 does NOT fire. The reframe survives NODE 1.

**Scoped banked statement (Charles's language, 2026-07-04):**
The native seal does NOT kill or quantize a spinning internal phase. For the uniform-spin ansatz
(χ = Nψ + ωt), the radial internal-charge flux through the seal vanishes. The verifier further showed
this remains **seal-vacuous even for a radial phase twist**, because the seal sits at the target pole
where the winding unwinds (Θ(r_s)=0 ⇒ sin²Θ=0) and internal currents vanish. **Therefore spin
discreteness, if it exists, is NOT a seal property — it must arise from the interior spatial/topological
BVP** (route 2a).

Also banked:
- **Q_int ∝ ω is a genuine conserved OUTPUT, not pure gauge** (leans favorable on clean-failure F2),
  pending full NODE 2 treatment.
- **Flavor II necessarily merges with Flavor I in the bulk** because the spin sources frame-drag
  (T_tψ = ξ sin²Θ ωN ≠ 0 ⇒ g_tψ), but this is an INTERIOR back-reaction, NOT a seal obstruction
  (T_rt=T_rψ=0 ⇒ no spin flux crosses the seal; the g_tψ junction is itself vacuous at the pole).
- No particle labels, no masses, no data.

## Derivation (native L2+L4; symbolic)
Matter action L2=−(ξ/2)g^{mn}G_mn, L4=−(κ/4)(G·G−…), G_mn=∂_mΘ∂_nΘ+sin²Θ ∂_mχ∂_nχ
(native_field_equations_constrained_two_player_results.md:71-73; angular_lagrangian_results.md:58-60).
Ansatz Θ=Θ(r), χ=Nψ+ωt ⇒ ∂_tχ=ω, ∂_ψχ=N, ∂_rχ=0, ∂_θχ=0.

1. **Internal U(1) (χ→χ+α) Noether current = canonical momentum** (χ cyclic): J^m=∂L/∂(∂_mχ).
   J^t_(2)=−ξ sin²Θ g^{tt}ω (charge density, ∝ω ⇒ genuine bulk charge); **J^r_(2)=−ξ sin²Θ g^{rr}∂_rχ=0**.
   L4 gives J^r_(4) ∝ ∂_rχ = 0 as well. **J^r ≡ 0 exact** (both terms), robust to φ,Z_φ,μ,ξ,κ and to g_tψ
   (radial row block-decoupled g^{rm}=g^{rr}δ^{rm}). [verifier V1 SUPPORTED exact]
2. **Seal junction = the NATURAL (Weierstrass–Erdmann) condition [J^r_χ]=0** (analog of the banked
   [π_φ]=0, universe_cell_fold_jc_sigma_results.md:26-30), auto-satisfied ∀ω since J^r≡0. **No essential
   pin on χ** (a U(1) phase mod 2π; σ_φ does not act on the target azimuth; t→−t pins no spatial-surface
   value). ADDITIONALLY: Θ(r_s)=0 ⇒ the azimuth is the target pole (coordinate-singular) ⇒ all χ-currents
   vanish there — a third, independent route to ω-blindness. [verifier V2 SUPPORTED]
3. **False-kill avoided:** demanding bare-phase equality (Nψ+ωt=Nψ−ωt ⇒ ω=0) is illegitimate (phase mod
   2π; only currents physical) — no F1 kill from bare parity. [verifier V3 SUPPORTED]
4. **No periodicity pin:** t→−t is a Z₂ reflection with fixed point (not an S¹ time identification); the
   cell is finite via two RADIAL folds ⇒ no compact time ⇒ no ω·T=2πk. Only N∈ℤ (spatial winding,
   compact ψ) is pinned. [verifier V4 SUPPORTED; caveat: a hypothetical 2nd time-seal → ω_n∝1/T box
   ladder = scale-sliding F7, not a native pin, different container]
5. **Static-metric consistency + frame-drag:** all G_mn are t-independent ⇒ static metric self-consistent
   for the diagonal part; T_tψ=ξ sin²Θ ωN≠0 sources g_tψ (Flavor II not strictly diagonal at full
   self-consistency); T_rt=T_rψ=0 (no spin flux crosses seal); induced g_tψ is odd under t→−t ⇒ Dirichlet
   g_tψ(seal)=0, self-consistent since its source ∝sin²Θ vanishes at the pole ⇒ no ω-pin from frame-drag
   either. [verifier V5 SUPPORTED]

## Scope (honest, verifier V6 SUPPORTED-WITH-REVISION)
The "ω free" verdict is derived for the **uniform-spin (rigid-rotor) ansatz ∂_rχ=0** — honestly labelled,
not a smuggled slice. **Revision folded in:** a radial phase twist (∂_rχ≠0) reintroduces J^r≠0 in the
BULK, but at the seal Θ=0 kills J^r even for a twist ⇒ the JUNCTION stays vacuous; a twist changes the
interior current/profile/energy/spectrum, and any pin would come from the **interior EOM/regularity/global
holonomy, NOT the seal**. The twisted-defect sector is UNMAPPED = the live next question. So the seal is
ω-blind robustly (three routes, and even under a twist).

## Consequences carried forward (NOT resolved here)
- Discreteness relocates to the **interior spatial/topological BVP** (route 2a) — NODE 2/3.
- F2 (gauge-emptiness) leans FAVORABLE (Q_int∝ω genuine) — formally NODE 2.
- NODE 2 back-reaction: the g_tψ interior solve is real (bulk), though seal-vacuous.

## Provenance / discipline
Symbolic/CAS/paper only; no numeric solve, no grid. Native L2+L4 + native Weierstrass–Erdmann junction;
GR-smuggle check CLEAN (no EH term, no generic-scalar substitution; Lense–Thirring l=1 used only as
Category-A reference for the frame-drag structure). Deriver a8d2e3c6fbac4dd7a (2026-07-04); blind
adversarial verifier a9242935198f7945a (2026-07-04): V1–V6 SUPPORTED (V4,V6 with folded revisions), no
refutations. Premise tags: L2+L4 native action THEORY; χ=Nψ+ωt uniform-spin ansatz FREE (scoped;
radial-twist is the more general FREE exploration); Θ(0)=π, Θ(r_s)=0 THEORY (CANON P12).
