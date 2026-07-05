# H3 — Native Q_H=1 hopfion solve: OUTCOME A (blind-verified) — a stable, localized, virial-balanced Q_H=1 hopfion is numerically resolved

**Status (2026-07-06, blind-verified A — verifier agent af9b56bc845e0eb97): the production rerun RESOLVES the
object. A topology-preserving arrested-Newton minimizer + a Derrick scale-mode accelerator, on a resolution
ladder, produces a STABLE, LOCALIZED, VIRIAL-BALANCED Q_H=1 hopfion on the flat-R³ Faddeev–Skyrme reduction of
native L2+L4. All four pre-registered success criteria are met: |Q|≈1 held, finite nonzero energy, localized
toroidal structure, stable virial. This OVERTURNS the earlier D-grade verdict (which was correct FOR THE
ADAM-SOLVE — that unwound; see history below). MISMATCH→SOLVER vindicated: the coarse-lattice collapse was a
resolution pathology, not a route-kill, exactly as the Vakulenko–Kapitansky bound (continuum Q=1 ⟹ E≥c>0)
predicts. Solver/driver: `hopfion_arc_scripts_2026-07-05/drive_production.py` (arrested-Newton + Derrick rescale
+ coarse-to-fine restart).**

**Evidence ladder (bounded GPU, single foreground process, anti-hang honored):**
| N | L | h | \|Q\| | E2/E4 | Ehat=E/√(ξκ) | verdict |
|---|---|---|------|-------|------|---------|
| 96 | 5 | 0.105 | 0.98 → **0** | → ∞ | 309 → **0** | UNWINDS (lattice pathology; D at this resolution) |
| 160 | 5 | 0.063 | 0.985 | 1.000* | 285.9 | HOLDS + CONVERGED |
| 224 | 7 | 0.063 | 0.984 | 1.000* | 285.4 | box-independent (L 5→7: ΔEhat 0.16%) |
| 256 | 6 | 0.047 | **0.992** | 0.999* | 286.5 | grid-converged; \|Q\|→1 with h |

**Load-bearing control (verifier): with the Derrick rescaler OFF, pure arrested-Newton from the N=256 field
KEEPS E2/E4≈0.99, |Q|=0.99, Ehat≈285 for hundreds of steps while still DESCENDING in energy — NOT the
E2/E4→∞ collapse the coarse grids show. So the rescaler does NOT manufacture the virial balance; the object is
a genuine stationary point.** (ξ=κ=1 is a FREE/data-blind gauge choice; the physics is the dimensionless FS
hopfion + the scaling ℓ_hopf/ρ_c ∝ 1/√ξ, unchanged.)

**★ THREE HONEST CAVEATS (verifier-required; all resolution-level, none touching existence):**
1. **|Q|≈0.99, NOT certified integer-to-3-digits.** It trends monotonically to 1 with resolution
   (0.985@N160 → 0.992@N256); the continuum VK theorem forbids non-integer, so this is a lattice-precision gap,
   not topology doubt. Do NOT write "Q_H=1 exactly" — write "|Q|≈0.99, integer-consistent + trending to 1."
2. **The exact "E2/E4=1.000" is a rescaler last-snapshot value** (the * in the table); the genuine
   arrested-Newton equilibrium sits at E2/E4 ≈ **0.99** (≈1% imbalance = O(h²) lattice breaking of the exact
   continuum scaling symmetry). State "virial-balanced to ~1%," not "E2=E4 exactly."
3. **Ehat ≈ 285–286 is the internally-converged value; the absolute-vs-published-FS-minimizer comparison is
   NOT established here** (the "~275" was never verified against literature; box+grid convergence is solid, the
   published-normalization match is not). Do not quote a "% high" without confirming the literature normalization.

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
- **EXISTENCE — NUMERICALLY RESOLVED (outcome A, blind-verified) via the production rerun.** With a
  topology-preserving arrested-Newton minimizer (Battye–Sutcliffe standard, NOT the unconstrained Adam of the
  first solve) + a Derrick scale-mode accelerator + a coarse-to-fine resolution ladder, a stationary Q_H=1
  hopfion HOLDS and CONVERGES for N≥160 (see the ladder table above): |Q| held ≈0.985–0.992 (trending to 1 with
  h), E2/E4→~0.99–1.00, energy converged Ehat≈285–286, a genuine localized off-axis torus (⟨ρ⟩=1.28, core ring
  where n hits the antipode of n_∞ at ρ≈1.17, on-axis vacuum hole). Box-independent (L 5→7: ΔEhat 0.16%) and
  grid-converged. The N=96 UNWINDING (Q→0, E→0) is confirmed to be the shrink-through-the-lattice pathology
  (core below grid spacing), suppressed once the grid protects the topology — exactly the Vakulenko–Kapitansky
  prediction (continuum Q=1 ⟹ E≥c>0, so E→0 requires the LATTICE to violate topology). MISMATCH→SOLVER
  vindicated: the first solve's D was a tool artifact, not the object's absence. **[HISTORY: the FIRST solve
  (Adam, agent a09b70a1539145abb) UNWOUND and its "E=314/Q≈0.79/virial-balanced" was a best-field checkpoint of
  a decaying transient — correctly caught as a FALSE PASS by verifier a2199a0aa1218ddc0 → D. The production
  rerun overturns that D by RESOLVING the object with the right minimizer.]** The Derrick "E2=E4" is the exact
  minimizer theorem (x→λx ⇒ E2∝λ, E4∝λ⁻¹ ⇒ stationary at E2=E4) and it is now a genuine numeric FINDING
  (rescaler-OFF control holds E2/E4≈0.99), not just a theorem — subject to caveat ★2 (~1% lattice offset).
- **SCALING — ANALYTICALLY FORCED + numerically consistent.** E∝√(ξκ), ℓ_hopf∝√(κ/ξ) follow from dimensional
  analysis of E=∫[(ξ/2)|∂n|²+(κ/4)F²] (E*=2√(ξκ·I2·I4), λ*∝√(κ/ξ)) — resolution-independent. ⇒ **ℓ_hopf ≈
  1.1√(κ/ξ); ℓ_hopf/ρ_c ∝ 1/√ξ** (ρ_c∝√κ). ξ FREE/data-blind ⇒ f(ξ), not a number. (Earlier two-coupling
  "confirmations" were near-circular collapsing checkpoints; the deliverable never depended on them — it is
  forced by the functional and now sits atop a genuinely-resolved object.)

## Frozen outcome: A — a stable virial-balanced Q_H=1 hopfion is numerically resolved (blind-verified af9b56bc845e0eb97)
The production rerun RESOLVES the object: all four pre-registered A-criteria met (|Q|≈1 held, finite nonzero
energy, localized toroidal, virial-balanced-to-~1%), box-independent + grid-converged, with the load-bearing
rescaler-OFF control confirming the balance is a genuine stationary point (not manufactured). ⇒ **outcome A**,
overturning the first solve's D. The three ★ caveats (|Q| integer-consistent+trending not certified-to-3-digits;
E2/E4=1.000 is a rescaler snapshot vs ~0.99 true equilibrium; absolute-vs-published normalization not
established) are resolution-level and do NOT touch existence. Route → H4 now stands on a NUMERICALLY-RESOLVED
native hopfion (no longer only on FS theory + dimensional analysis, though those remain the independent backstop).

## VERIFIER RECORD (verifier-before-record)
- **Blind adversarial verifier — agent a2199a0aa1218ddc0, 2026-07-05** (zero-context, re-ran the solver, hunted
  false passes). Grades: Energy functional PASS (clean FS, no smuggled metric/GR factor); Q_H Whitehead PASS
  (correct + validated, null test 0, seed→1); Virial PASS-as-theory / FALSE-PASS-as-finding (numerics show
  E2/E4≈6→∞, never 1); Scaling PASS (analytically forced) but weak as numeric evidence (near-circular);
  Honesty PASS-WITH-CAVEAT (headline honest but UNDER-DISCLOSED the collapse-to-vacuum + best-field-checkpoint
  methodology); Provenance PASS (no GR/metric smuggled; FFT-Poisson + Adam/arrested-Newton + boundary pin =
  allowed category-A technique). **VERDICT (on the FIRST solve): downgrade the SOLVE component to D (tool-limited).**
  This verdict was CORRECT for the Adam solve it examined; it is now SUPERSEDED as the H3 verdict by the
  production rerun below (which uses a different, topology-preserving minimizer).
- **Blind adversarial verifier — agent af9b56bc845e0eb97, 2026-07-06** (zero-context, independently recomputed
  E/E2/E4/Q on the saved converged fields, ran the honest localization + null tests, and ran the load-bearing
  rescaler-OFF control). Grades: **A** Derrick-rescaler-does-NOT-manufacture-balance PASS (rescaler-OFF pure
  arrested-Newton holds E2/E4≈0.99, |Q|=0.99, Ehat≈285 while descending — the decisive refutation of the
  "manufactured balance" suspicion); **B** Q_H recompute PASS (0.985/0.984/0.992, null test 0, trending to 1);
  **C** resolution story PASS (N=96 unwinds, N≥160 holds; VK bound correctly invoked); **D** box+grid
  convergence PASS (Ehat 285–286 across L=5/6/7, N=160/224/256; grid_sample restart sound, identity resample
  reproduces E exactly); **E** localized torus PASS (⟨ρ⟩=1.28, core ring ρ≈1.17 — the driver's `Rring` per-point
  metric IS buggy, flagged, use ⟨ρ⟩); **F** provenance PASS (flat h³ = honest ρ=r reduction, no GR smuggled; all
  technique category-A + sound). **VERDICT: A is HONEST and SUPPORTED — a solid A with ~1% resolution-level
  offsets, correctly overturning the prior D, provided the three ★ caveats are disclosed (they are, above).**

## OWED / next (H3 is now outcome A; these strengthen or follow it)
1. ~~Blind verifier on the first solve~~ DONE (a2199a0aa1218ddc0 → D on the Adam solve). ~~Load-bearing N≳256 A-vs-D
   rerun~~ DONE (production rerun → **A**, blind-verified af9b56bc845e0eb97). Both recorded above.
2. **Optional precision closure (NOT gating A):** push N≥320 / a spectral or higher-order Q_H to certify integer
   |Q| to 3 digits and pin the arrested-Newton equilibrium E2/E4 without the rescaler snapshot; independently
   confirm the literature FS minimizer-energy normalization if an absolute-energy comparison is ever wanted. The
   `drive_production.py` `Rring` diagnostic is buggy (per-point argmax) — replaced by the ⟨ρ⟩ volume metric.
3. **H4 (the next physics, now on a resolved hopfion):** φ-backreaction (localized 𝒦→φ well; gravitation; MASS;
   the dynamical bulk-vs-core-PINNING verdict) + a ξ-anchor (turns ℓ_hopf/ρ_c ∝ 1/√ξ into a definite
   particle-vs-cell verdict). Still OWED from H2: physical charges **q=1/3, η=1/18** (import-dependent, separate
   native re-derivation, NOT from Q_H) + the **i-flow/ℏ clock**. J(s) light-deflection lever remains frame-robust,
   un-gated.
