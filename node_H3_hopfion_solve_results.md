# H3 — Native Q_H=1 hopfion solve: SOLVE = D-grade (tool-limited); route survives on FS theory + analytic scaling

**Status (verifier-CORRECTED 2026-07-05, agent a2199a0aa1218ddc0): the SOLVE component is D-grade / tool-limited,
NOT A. At accessible resolution (N≤96) the relaxation COLLAPSES to vacuum (Q→0, E→0); the reported "E=314, Q≈0.79"
is a best-field checkpoint of a decaying transient, and "virial-balanced E2=E4" is a THEOREM, not a numeric
finding (the runs show E2/E4→∞ during collapse). Per the pre-registration's own item-8 ("reproduce the known
minimizer as proof the method RESOLVES the object"), that benchmark is NOT met ⇒ outcome D. THE ROUTE STILL
SURVIVES, but on EXTERNAL grounds: (i) the flat-R³ Faddeev–Skyrme reduction is exact + clean (verified); (ii) the
Q_H Whitehead measurement is correct + validated (verified); (iii) FS hopfion existence + stability is ESTABLISHED
mathematics (Faddeev's quartic term evades Derrick collapse — the object is stable in the continuum, so the
lattice collapse = a resolution pathology, the MISMATCH→SOLVER reading, NOT a route-kill); (iv) the scaling
ℓ_hopf∝√(κ/ξ) is ANALYTICALLY FORCED by dimensional analysis, robust to the numeric shortfall. So the OWED
N≳256 rerun is genuinely LOAD-BEARING (it decides A-vs-D), not a cosmetic precision polish. The former headline
"PROVISIONAL-A (exists + scaling)" is REPLACED by: EXISTENCE rests on FS theory; SCALING rests on dimensional
analysis; the SOLVE numerically demonstrated neither at N≤96.**

Solver agent a09b70a1539145abb (GPU V100, torch float64, single process, anti-hang honored). Under the frozen
verified contract `H3_hopfion_solve_preregistration.md`. **Scripts COMMITTED (rerun the precision closure from
here): `hopfion_arc_scripts_2026-07-05/` (`fs_hopfion.py` = FS energy + Whitehead Q_H; `drive_ckpt.py`,
`drive_stereo.py`, `drive_val.py`; `analyze_final.py`; see its README).** Field checkpoints (*.npz, 50–98 MB)
were NOT committed — regenerate them. NOTE (verifier): `drive_ckpt.py`/`drive_stereo.py` keep the lowest-E field
with Q≥Qmin, i.e. a snapshot of the field MID-COLLAPSE — this best-field-checkpoint methodology must be surfaced
(it was buried in the drivers) when the N≳256 rerun is designed.

## What H3 is (contract-verified)
Native L2+L4 on N=0, φ-blind + ρ=r theorem ⇒ EXACTLY the flat-R³ Faddeev–Skyrme energy
E=∫[(ξ/2)|∂n|² + (κ/4)F_ij²], F_ij=n·(∂_i n×∂_j n). So H3 = resolve the KNOWN Q_H=1 FS hopfion natively + report ℓ_hopf/ρ_c(ξ).

## Findings
- **Q_H measurement VALIDATED (verifier-CONFIRMED, clean)** (Whitehead integral, A from ∇²A=−∇×B FFT): on clean
  degree-1 Hopf seeds |Q_H|→1 by O(h²) Richardson (0.863,0.914,0.951,0.965 → 1.00 at N=48/64/96/128; doc's
  0.877/0.941/0.965 reproduced). Null test: constant field → Q=0.00000 exactly. |divA|≈1e-16 (Coulomb gauge
  honored). Not faked by a pin. Sign ±1 = the H2 hopfion/anti-hopfion mirror. **This is the one solve output that
  cleanly stands.**
- **EXISTENCE — from FS THEORY, NOT from this solve (verifier-CORRECTED — the old "outcome A / the solve resolves
  it" was a FALSE PASS).** The Q_H=1 FS hopfion is an established stable soliton (Faddeev 1975; Battye–Sutcliffe,
  Hietarinta–Salo minimizers) — the quartic L4 term evades Derrick collapse in the continuum. BUT this solve does
  NOT exhibit it: at N≤96 the Hopf seed UNWINDS within ~150–300 relaxation steps (Q: 0.94→0.30→0.00, E→0,
  E2/E4→∞). The reported "finite localized virial-balanced ring" is a best-field checkpoint of that collapse, not
  a resolved stationary object. **"virial-balanced E2=E4" is a THEOREM (Derrick: x→λx ⇒ E2∝λ, E4∝λ⁻¹ ⇒
  stationarity forces E2=E4), CONTRADICTED by the accessible-resolution numerics (E2/E4≈6→∞) — it was mis-stated
  as a numeric finding.** The lattice collapse = the known shrink-through-the-lattice pathology (core below grid
  spacing) = MISMATCH→SOLVER (tool-limited), NOT a statement the object is absent.
- **SCALING — ANALYTICALLY FORCED (the load-bearing deliverable, robust).** E∝√(ξκ), ℓ_hopf∝√(κ/ξ) follow from
  dimensional analysis of E=∫[(ξ/2)|∂n|²+(κ/4)F²] (E*=2√(ξκ·I2·I4), λ*∝√(κ/ξ)) — resolution-independent, holds
  whether or not a hopfion is numerically resolved. The two-coupling runs (ratio 2.05≈√4, ring 2.0=√4) are
  CONSISTENT but near-circular (the functional scales this way regardless; both runs are collapsing-transient
  checkpoints), so they confirm the ALGEBRA, not a resolved object. ⇒ **ℓ_hopf ≈ 1.1√(κ/ξ); ℓ_hopf/ρ_c ∝ 1/√ξ**
  (ρ_c∝√κ). ξ FREE/data-blind ⇒ f(ξ), not a number. This deliverable survives the D-grade solve.
- **PRECISION / RESOLUTION SHORTFALL (now DECISIVE, not cosmetic):** at N≤96 the relaxation collapses; the
  best-field checkpoints sit at Ehat=E/√(ξκ)=314–322 with Q_H≈0.79. (The "vs published FS 275" comparison is
  UNVERIFIED within the verifier's scope — the 275 minimizer-energy normalization was not confirmed against
  literature, so the "16% high" number is provisional too.) A stable resolved minimizer was NOT produced ⇒
  outcome D. The N≳256 rerun must decide A-vs-D.

## Frozen outcome: D (tool-limited) for the SOLVE; route survives on FS theory + analytic scaling (verifier-CORRECTED)
The SOLVE did NOT numerically resolve a stationary Q_H=1 hopfion at N≤96 (collapse to vacuum; Q≈0.79 checkpoint;
E2≠E4) ⇒ per the pre-reg's own item-8/outcome-D definition this is **D, tool-limited** — NOT the A it was first
banked as. Route → H4 is preserved ONLY because: existence = established FS mathematics (external to this solve),
and the H4-input ℓ_hopf/ρ_c ∝ 1/√ξ = analytically forced (external to this solve). NOT C (FS hopfion known +
native reduction exact ⇒ suspect tool, not nonexistence). **No affirmative NUMERIC existence claim is banked;
the N≳256 rerun is load-bearing for that.**

## VERIFIER RECORD (verifier-before-record)
- **Blind adversarial verifier — agent a2199a0aa1218ddc0, 2026-07-05** (zero-context, re-ran the solver, hunted
  false passes). Grades: Energy functional PASS (clean FS, no smuggled metric/GR factor); Q_H Whitehead PASS
  (correct + validated, null test 0, seed→1); Virial PASS-as-theory / FALSE-PASS-as-finding (numerics show
  E2/E4≈6→∞, never 1); Scaling PASS (analytically forced) but weak as numeric evidence (near-circular);
  Honesty PASS-WITH-CAVEAT (headline honest but UNDER-DISCLOSED the collapse-to-vacuum + best-field-checkpoint
  methodology); Provenance PASS (no GR/metric smuggled; FFT-Poisson + Adam/arrested-Newton + boundary pin =
  allowed category-A technique). **VERDICT: downgrade the SOLVE component to D (tool-limited); route survives on
  FS theory + analytic scaling only.** Corrections above applied per this verdict.

## OWED before clean bank (top next-session actions)
1. ~~Blind adversarial verifier~~ — DONE (agent a2199a0aa1218ddc0, 2026-07-05; see VERIFIER RECORD). It downgraded
   the solve to D and corrected the false pass; corrections applied above.
2. **Finer-grid (N≳256) / specialized minimizer — NOW LOAD-BEARING (decides A-vs-D, not cosmetic):** the N≤96
   relaxation COLLAPSES; the rerun must produce a STABLE stationary Q_H=1 minimizer (E2=E4 realized, Q integer on
   the RELAXED field, ring stable, R_box-independent) to earn outcome A. Design notes: (a) resolve the core
   (grid spacing ≪ ℓ_hopf ≈ 1.1√(κ/ξ), so h and box must scale together with a fine core); (b) use a genuine
   arrested-Newton / full minimizer that holds the Q-barrier (not a checkpoint of a decaying Adam run); (c)
   independently confirm the literature FS minimizer energy normalization before quoting any "% high"; (d) surface
   the best-field-checkpoint methodology explicitly. This is a category-A numerical-technique push (how we solve),
   ANTI-HANG binding (bound grid, ONE process, foreground, never background-poll).
Existence + ℓ_hopf/ρ_c ∝ 1/√ξ currently rest on FS THEORY + DIMENSIONAL ANALYSIS (external to the solve); the
N≳256 rerun is what converts the NUMERIC existence claim from D to A. H4 (backreaction/gravitation/mass; the
dynamical bulk-vs-core-pinning verdict) + a ξ-anchor are the next physics AFTER A is earned; the physical charges
q/η + the i-flow/ℏ clock remain owed (H2).
