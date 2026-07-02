# Embedded run (H_cell=H_amb, MODEL ambient) — embedding rescues finiteness; no band; points to Class-B

**Date:** 2026-07-02. **Mode:** OBSERVE (the embedded run, gated + rulings blind-verified). **Driver:**
Claude Code. **Scripts:** `cell_solver_f2d_embedded_run.py` (+ `scratch_f2d_embedded_summary.json`),
reusing the CAS-verified operators of `cell_solver_f2d.py` and the two-tier filter of
`cell_solver_f2d_N2.py`. **Status:** **BLIND-VERIFIED 2026-07-02 (agent a9b99b1, PASS + structurally
strengthened) — bankable as a scoped PROVISIONAL result.** UNLABELED. **NOT a discreteness/frame verdict.**
Foundation: `embedded_run_mini_MAP.md`, `embedded_run_gate_rulings.md` (Rulings 1-2 blind-verified),
`embedded_cell_closure_H_amb_results.md`, `seal_matching_junction_results.md` (derived Class-A/B parity).

## Headline (lay first)
Two findings, both blind-verified:
1. **Embedding RESCUES FINITENESS (the mechanism claude.ai predicted, confirmed).** Matching the seal
   field VALUES to an ambient gives the geometry a genuine **finite anchored stationary point** — at
   every (a,L), N=1 and N=2 (Φ~1e-16, byte-identical under maxit 40→800), while the CLOSED (mirror) cell
   at the same point **stalls with ρ inflating** (the dilution runaway). Pinning the seal structurally
   closes the escape direction that killed the closed cell.
2. **But NO genuine matched cell / NO band on this MODEL slice** — and the obstruction is STRUCTURAL and
   is already-derived physics: a smooth-**mirror-core** cell relaxes to a **gradient-free** interior
   (π_φ,s≈0, q≈0 = **Class A**), so it cannot **momentum-match** a **gradient-carrying** ambient. Points
   cleanly to **Class-B** (charged/pinned core) or a **turning-point (gradient-free) ambient** as next.

## The structural reason (verifier-derived; more than a solver relaxation)
The φ-EOM integrates to **`(Zρ²φ') ' = 4 e^{−2φ} ρ'² ≥ 0`** (verified to 2e-11 on the solved field). The
mirror core forces π_φ,c = Zρ²φ'|_c = 0 (confirmed ~1e-13). Therefore **π_φ,s ≥ 0 always**, and is built
up ONLY by interior ρ-gradients. The dilation-flux match R3 = π_φ,s − π_φ,amb (= π_φ,s − 4 for the model
charged ambient) can cross zero only if the interior develops enough ρ-gradient to reach π_φ,s=4 — but
the interior **drains to flat** (40 strong-gradient seeds all return to π_φ,s≈0.007). So R3 is
**single-signed (~−3.8 to −4.0) with ZERO sign-changes** across a∈[0.55,2.0] × 5 seeds. No
gradient-carrying matching branch exists.

## Broader framing (verifier refinement — do not over-read "charge")
The full obstruction is **gradient-free core vs gradient-carrying ambient in BOTH momenta.** The
ρ'-continuity residual R4 (~+9) is actually LARGER than the flux residual R3 (~−4). The Class-A/B
(charge, q) reading — mirror core → q≈0 → needs a Class-B seal source to match a charged ambient
(consistent with `seal_matching_junction_results.md`; the q=0 ambient probe confirms R3→0 there while
R4 stays ~+4) — captures the R3 FACET. The complete statement is: **a gradient-free (mirror-core) cell
cannot momentum-match a gradient-carrying ambient**; Class-B / charge is one face of it.

## MODEL ambient (labeled MODEL, not the derived universe value)
Ambient sampled on the native radial family (R-areal theorem, `(r²φ')'=0`): `φ_amb=−q/a, ρ_amb=a,
π_φ,amb=Zq, π_ρ,amb=−4e^{2q/a}, m_amb=μ/a²`, all mutually consistent (a genuine P-tangent, not
arbitrary); `H_amb=H_geo(amb)+m_amb` DERIVED. MODEL constants q=0.5, μ=1.0, Z=8 chosen round/sane BEFORE
any residual (no sculpting). The derived Branch-P/F5-critical universe value is DEFERRED.

## Scheme + counting (faithful to Ruling 1; verifier PASS on correctness + non-bias)
Over-by-1 (a free): at fixed (a,L) the interior field BVP is square with inner mirror (φ'_c=ρ'_c=f_r,c=0)
+ outer Dirichlet matches (1)(2) + f_r,s=0; the leftover momentum (3)(4) and matter (5) conditions are
residuals; a 2D root-find over (a,L) targets R3=R4=0, then R5 checked. **Not self-inflicted:** ρ' is FREE
at the seal (a gradient branch is geometrically allowed — none exists); the complementary Scheme B
(impose ambient slopes as Neumann) fails to converge 0/6 (forcing the gradient drives φ→runaway). Both
schemes agree ⇒ the obstruction is a property of the EOM, not the imposition.

## Filters
Adapted Derrick (Ruling 2) + two-tier stability filter are wired; **not reached** (no genuine matched
cell existed to filter) — phase-4 correctly skipped, not faked.

## Scope / premises (carry this stamp)
ONE slice: Nr=16, Nθ=12; Z=8; N∈{1,2}; **MODEL** ambient (q=0.5, μ=1.0); ξ=κ=1; smooth-mirror
(Class-A/uncharged) core; round, static, minimal L2+L4. Nonexistence of a gradient-carrying matching
branch is **numerical (40 seeds) + structural (the ≥0 flux identity), NOT an analytic proof.** All
CHOSE/THEORY/MODEL tagged. NOT a discreteness or frame verdict.

## VERIFIER
**Blind adversarial pass — 2026-07-02, agent `a9b99b1`. PASS (all 4 load-bearing claims), result
STRENGTHENED.** Independent bounded re-check (own script, not the JSON): (1) embedding→finite stationary
point CONFIRMED (byte-identical maxit 40→800; closed cell inflates) — caveat: rescued config is flat/
gradient-free (real coupled solution, not a structured interior). (2) momentum obstruction CONFIRMED +
structurally derived (the (Zρ²φ')'=4e^{−2φ}ρ'²≥0 identity; 40-seed gradient hunt all drain to flat; zero
sign-changes). (3) scheme faithful to Ruling 1 and NOT biasing the gradient-free outcome (ρ' free;
Scheme B 0/6 corroborates). (4) Class-A/B reading supported but is one facet of the broader gradient-free
obstruction (R4>R3). (5) no hollow checks; gate sound; MODEL labeled; NO band sculpted. **Direction
(Class-B charged core / gradient-carrying-or-turning-point ambient next) is SOUND** — a Class-A mirror
core is structurally q≈0, so a matching cell, if it exists, must be Class-B (motivated, not a patch).
