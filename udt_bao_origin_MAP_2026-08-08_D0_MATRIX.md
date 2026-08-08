# D0 — BAO-origin discrimination matrix (MAP-GRADE)

Date 2026-08-08 | branch grok | Contract: `udt_bao_origin_MAP_2026-08-08.md` (§2 ledger, §5 D0).
MODE: assembly from BANKED results ONLY — no new derivation, no data contact, ZERO BOSS contact
(CP4 honored: no BOSS file, listing, or metadata touched). NOT COMMITTED by D0.

Sources (the only ground used):
- `udt_xmax_scale_observational_M2_build_2026-08-07/D1_FORMULAS.md` (theta=ell/r(z); radial
  trichotomy; low-z degeneracy; P1 min-angle floor; AP-like ratio) — "D1F" below.
- `udt_xmax_scale_observational_M3_runs_2026-08-07/SNE_RESULTS.md` CONSOLIDATED — "SNE".
- `udt_xmax_scale_observational_M3_runs_2026-08-07/BAO_RESULTS.md` CONSOLIDATED — "BAO".
- `udt_xmax_scale_observational_M3AUDIT_2026-08-08/AUDIT_REPORT.md` CONSOLIDATED — "AUD".
- `udt_xmax_O2_measure_table_2026-08-07/DERIVATION_NOTES.md` CONSOLIDATED — "O2".
- `udt_xmax_O3_approach_classes_2026-08-07/DERIVATION_NOTES.md` CONSOLIDATED — "O3".
- The MAP itself §2 (per-origin recorded predictions) — "MAP§2".
- `udt_bao_origin_D1_static_transfer_2026-08-08/DERIVATION_NOTES.md` CONSOLIDATED (verified
  LEAD, R1 SUSTAINED-AMENDED + R2 AMENDED, 2026-08-08) — "D1C" (O-C static row only).
- SYNTHESIS PASS (2026-08-08, third pass — cross-package statements legally live HERE):
  `udt_bao_origin_D2_timelive_transfer_2026-08-08/DERIVATION_NOTES.md` CONSOLIDATED (verified
  LEAD) — "D2C"; its R1 `ADVERSARIAL_REVIEW_1_recompute.md` — "D2-R1".
  `udt_bao_origin_D4_oscillating_2026-08-08/DERIVATION_NOTES.md` CONSOLIDATED (verified LEAD)
  — "D4C". (Both NOT committed at their own step; consolidated + two reviews each.)
- FOURTH PASS (2026-08-08): `udt_bao_origin_D3_native_scale_2026-08-08/DERIVATION_NOTES.md`
  CONSOLIDATED (verified LEAD; R1 SUSTAINED-AMENDED overturn-failed + R2 AMENDED no-falsifier)
  — "D3C". Fills O-B's row; closes the matrix. NOT committed at its own step.

Numeric anchor available to any row that needs the fitted frame (F-ANCHOR premise travels):
SNe-fitted P1 (mode A/zCMB): inv_n = 0.947 [0.9284, 0.9658] (n ≈ 1.06); mode B: X_eff = 2086 Mpc,
R_w(best n) = 2202.6 Mpc; n=1 exclusion 2.82σ (zCMB), 3.89σ (zHD column) [SNE]. NO ell is banked
(no BAO-alone X-range; the ~70 Mpc-scale ell is stated-not-fitted context) [BAO].

## THE MATRIX (rows = origins; columns C1–C6; every cell = DERIVED(cite) / DEFINITIONAL /
## UNDERIVED(owner) — an over-filled matrix is the failure mode)

| origin | C1 theta(z) drift across thread | C2 radial signal class | C3 BOSS replication | C4 tracer-universality/phase | C5 amplitude/z | C6 other distinct signatures |
|---|---|---|---|---|---|---|
| **O-A** intrinsic, frame-mapped | DERIVED: monotone FALL (gentle under fitted P1: −0.40 bins z 0.925→1.025, −1.07 bins 0.725→0.925). E2 tension noted (below). | DERIVED (class only): trichotomy Δz_BAO grows/const/decays (P1/P2/P3); GROWS under fitted P1. Amplitude needs frozen ell — UNDERIVED(freeze-point). | YES — definitional (real structure, same sky): same (theta, z) features [MAP§2]. | Scale SHARED across tracers (definitional: one structure); per-tracer amplitude UNDERIVED (needs a tracer/bias model — outside banked machinery). | UNDERIVED (needs a structure model; outside this arc's machinery). | P1 minimal-angle floor theta→ell/R_w as z→∞ [D1F §3, O2 (B)]; AP-like ratio Δz/(z·theta)→1 at z→0, all profiles [D1F §4]. |
| **O-B** orchestra-generated | CONDITIONAL, now RESOLVED at root [D3C]: no NATIVE ell is banked ⇒ any ell is POSITED free-data (or discreteness-supplied). IF posited z-independent + proper, banked forms ⇒ same gentle fall as O-A [D1F §3, P-STATIC-RULER]; the drift then reads out the posited ell's z-behavior, not a native law. | Same conditional [D1F §4]: trichotomy applies to any static proper ruler; but the ruler itself is posited/discreteness-gated, not native [D3C]. | YES + possibly tracer-dependence signatures [MAP§2, stated not derived]. | Possibly tracer-DEPENDENT (matter couples) — but coupling is NOT derivable at the banked layer (no matter dynamics banked) [D3C tracer-inheritance note]; named inheritance only. | Rides the posited/discreteness scale's amplitude — no native amplitude law [D3C]. | **THE AMOUNT — DERIVED NEGATIVE [D3C, verified LEAD]:** NO native second amount at the banked layer (under SS9 lock chart / central observer / D2 stamps). Every candidate = X × {free param n, free-data-conditioned threshold μ_c/ρ·s=1/fold, observer-supplied θ_x via k_p, or the length-inert parameter-free spacing=1}. O-B's scale requires EITHER posited free-data (ell/X) OR the discreteness program firing (μ quantization under a compact/winding target — characterized-not-run, F-SCOPE). |
| **O-C** pure viewing artifact | DERIVED, STATIC (D1) + TIME-LIVE (D2): the map is SCALE-TRANSPARENT — featureless mixing field in ⇒ featureless anisotropy out; NO native angular scale time-live either [D2C, stamps: Gaussian-riding SS5, ansatz-scoped SS9, below the fold onset]. A scale can only be INHERITED via 3 routes (see cell notes), never made. Window break θ_break ~ Δℓ_p/r(z) rides the time-live dictionary smoothly [D1C, D2C §7d]. E2's reversed drift stays not-a-target (F-RETRO). | DERIVED, STATIC (D1) + TIME-LIVE (D2): no native Δz scale below the fold; the map's ONLY native non-analyticities are THRESHOLDS-not-scales (amplitude edge μ_c=|s−1/ρ|; depth locus ρ·s=1; the FOLD A_t=−A·A_r — the one new time-live failure mode, a condition on free profile DATA) [D2C]. At the fold a z-space caustic (dN/dz pileup) appears. Below fold: featureless [Gaussian-riding, ansatz-scoped]. | YES — any survey of the same sky depth (the view, not the galaxies) [MAP§2]. | DERIVED, TIME-LIVE (D2): tracer phase is FORCED — the operator is tracer-blind + achromatic ⇒ any pattern that exists is phase-identical across tracers; tracer-dependence enters ONLY through per-tracer selection windows [D2C T3']. (Static-layer this was vacuous; time-live it is a real forced signature.) | DERIVED, STATIC (D1) + TIME-LIVE (D2): scale-transparent (power-laws in ⇒ power-laws out); no z-feature below fold [D2C, Gaussian-riding/ansatz-scoped]. | The map is proven an HONEST COURIER (D1 static + D2 time-live below fold): it transports/preserves scales, never manufactures them [D2C; see Convergences]. Cross-tracer phase-identity (C4) is O-C's sharp signature. |
| **O-D** residual mundane | No prediction machinery. Banked negative: the one measured selection channel (dN/dz z̄-tilt) is quantitatively dead for the drift (≤0.01 bins vs ~1–1.5 observed, sign-incoherent) [AUD]. Unaudited layers remain (INCONCLUSIVE grades) — UNDERIVED/none. | No machinery; no coherent radial prediction exists to derive — expectation of incoherence is stated, not derived. | **NON-replication** — DEFINITIONAL (decorrelated systematics); the cheapest kill available [MAP§2]. | Tracer-SPECIFIC (each tracer has its own selection layers) — definitional; no phase prediction. | No stable prediction (noise conspiracies). | Its live room is the audited record itself: the INCONCLUSIVE cells (LRG 0.90–0.95, QSO 1.10–1.25, QSO 1.85–2.00) and the power-limited caveats on two SKY-ROBUST thread cells [AUD final grade table]. |
| **O-E** oscillating geometry | DERIVED, STATIC/μ=0 scope (D4): the induced localized angular scale θ_osc(z) = λ_p(z)/r(z), λ_p = λ(1+z)^(1−2m), drifts per parametrization m (areal λ(1+z)/r; proper λ/r; optical λ/((1+z)r)) — the drift READS OUT m [D4C C8b]. LIVES in the map+window channel ONLY; per-shell w(θ) stays featureless (see C6). Visibility: window ≥ one λ_p cycle [D4C P-D12]. Time-live: UNDERIVED(D4b/D2). | DERIVED, STATIC/μ=0 scope (D4): TRICHOTOMY on nm (=O2 finiteness table read as oscillation-fate): nm<1 FREEZES near wall; nm=1 log-periodic RIDE; nm>1 SUPERCRITICAL COMPRESS → non-monotone z(r) = "redshift caustics", dN/dz fold spikes at J=0 [D4C 2(g,h)]. Cycle spacing Δz_cyc = λ(n/2R_w)(1+z)^(1+2/n−2m). | YES — definitional (geometry is there for any survey) [MAP§2 (i)]; the phase is derived-coherent (C4). | DERIVED (D4): TRACER-UNIVERSAL + phase-coherent — operator carries only {z,n,R_w,λ,ε,m,osc}; achromatic ⇒ every tracer at same z inherits SAME modulation, SAME phase; isotropic, z-locked; tracer-dependence only via selection windows [D4C 3(c), free-symbol audit]. | DERIVED, STATIC/μ=0 scope (D4): amplitude ε<1 (admitted-kinematic); the Hubble residual envelope ∝ u/(1−u) FADES with z at rate (1+z)^(−2/n) (tied to the distance-law n) [D4C C4a-c]. | DERIVED (D4): Δμ(z) residual with EQUAL CYCLE SPACING in ξ_m=(1+z)^(−2(1−nm)/n) — generically NOT in z (z-periodic only at optical n=2); ANTI-PHASE LOCK δθ/θ=−δd_L/d_L; LOUDNESS HIERARCHY (dN/dz louder than Δμ by exactly r·Φ′, phase-advanced π/2); optics component PARTIAL (achromatic+d_L/θ derived; surface-brightness open) [D4C 3(a,b,d,e)]. |

*(O-C row: static cells from D1 [D1C], time-live cells now filled from D2 [D2C]. O-E row:
now filled from D4 [D4C] (static/μ=0 scope). The CURRENT-SCORECARD lines for O-C and O-E were
rewritten in this same synthesis pass; O-A/O-B/O-D lines are unchanged from the first pass.)*

### Cell notes (citations + the E2 tension, stated neutrally)

- O-A/C1: theta_BAO(z) = ell/r(z) with dr/dz > 0 for every menu profile [D1F §1, §3] ⇒ a fixed
  proper ruler's angle falls monotonically with z. The bin numbers are the audit's propagation
  through the fitted P1 (n = 1.06, context curve) [AUD drift note]. The certified E2 fact: the
  observed drift across the strong shells runs OPPOSITE this fall by ~1–1.5 bins [BAO
  CONSOLIDATED amendment]; the audit graded the tension REAL — no measured selection channel
  explains it, thread centers stable [AUD CONSOLIDATED]. Stated as tension, not verdict.
- O-A/C2: Δz_BAO(z; ell) = ell·(−A′/2A)|_{r(z)}; P1 (ell·n/2R_w)(1+z)^(2/n) GROWS, P2 const,
  P3 decays [D1F §4]. The z-trend duplicates the c₂ trichotomy — an independent-leg class
  discriminator. Numeric prediction requires ell frozen at the freeze-point; the radial
  ESTIMATOR itself is unbuilt (owed) [BAO CONSOLIDATED].
- O-A/C3 vs O-C/C3 vs O-E/C3: all three predict BOSS replication — replication alone does NOT
  separate O-A/O-B/O-C/O-E; it kills only O-D. The separators among the replicators are C4
  (phase/tracer behavior) and C1/C2 shapes once D1/D2/D3 fill them.
- O-B/C1-C2 conditionality: the banked forms carry the P-STATIC-RULER posit + proper-ruler
  realization tag [D1F premise tags]; O-B inherits them only under "static z-independent
  proper ell" — that premise is exactly what D3 must derive or refute, so the cell is
  conditional, not filled.
- O-D/C1: honesty both ways — the audit killed the measured channel but its scope line is
  explicit: shell-center displacement only; a z-dependent clustering-amplitude mix is a
  different channel, only indirectly probed [AUD drift note scope sentence].
- O-C the THREE inheritance routes (a scale is never map-made, only inherited) [D2C §3]:
  (1) μ's own angular correlation carries a localized feature → the map transports it as
  θ(z)=s_feat/r(z); (2) μ's amplitude crosses a native THRESHOLD (μ_c=|s−1/ρ| or ρ·s=1 —
  these are thresholds, not scales); (3) the free profile data realize a dictionary FOLD.
  Plus the D1 window-set route (per-tracer selection window). Every no-feature verdict rides
  the SS5 Gaussian-statistics stamp (LOAD-BEARING) and the SS9 time-live lock-form ansatz.
- O-E/C1-C6 scope: STATIC/μ=0, lock+areal-anchor chart, central observer, n>0, r-only
  multiplicative oscillation class, test sources, O(ε) laws inside the P-D11 validity domain
  [D4C SCOPE]. Landing = D4-ADMITTED (KINEMATIC — no native law is banked, so no dynamical
  admissibility is claimed); the trichotomy restrictions are structure INSIDE admission.

## CONVERGENCES (SYNTHESIS — the arc's structural findings; cross-package, cite both + D2-R1)

Cross-package statements legally live here (the matrix/synthesis step), not in any single
package. Two findings, both neutral — no origin preferred:

- **(a) The D2 fold and the D4 supercritical caustics are THE SAME OBJECT.** D2-R1 proved it
  (`S5_fold_static_limit_is_Ar_zero`): the static limit of D2's fold condition A_t=−A·A_r
  (set A_t=0) gives A_r=0 — exactly D4's J=0 caustic locus [D2-R1 "D2 fold vs D4 caustics:
  SAME mathematical object"; D4C 2(h) J=0; D2C §7b/§7d]. One creased-dictionary phenomenon
  reachable from TWO origins: as O-C's time-live fold (structure in the free profile DATA)
  or as O-E's supercritical redshift-caustic (nm>1 oscillation piling cycles at the wall).
  The static route reaches it only OUTSIDE class-(i) monotone profiles (A_r=0 needs a
  non-monotone A), the time-live route from generic profile time-dependence [D2-R1].
- **(b) O-C, O-E, and O-B are three variants of ONE question: WHERE DOES THE STRUCTURE LIVE
  — in the matter, in the profile, or in the comparison field?** O-B = structure in the
  matter (a native clustering scale); O-E = structure in the PROFILE (an oscillatory metric
  component the galaxies trace); refined O-C = structure in μ's OWN field (the comparison
  map's mixing field carries it) — see the three inheritance routes above. In EVERY regime
  examined the MAP ITSELF is proven an HONEST COURIER: D1 (static) and D2 (time-live, below
  the fold) both show it transports and preserves scales but never manufactures one from
  featureless input [D1C; D2C SCALE-TRANSPARENT, stamps riding]. So the discriminating
  question is not "does the view invent the pattern" (it does not, in the regimes derived) but
  "which of matter / profile / μ-field SOURCES the structure the honest courier then carries."
  Stated as the arc's structural finding, no origin favored; the fold/caustic (a) is the one
  place the courier itself creases — and it is a condition on DATA (profile or amplitude), not
  a manufactured scale.

## CURRENT-SCORECARD (per origin vs the explananda; neutral, no ranking, no verdict)

The explananda (copied from MAP §1):
E1 the sky-robust thread (2.3–2.4°, z 0.70–1.10, two tracers; grades: control SKY-ROBUST
strongest, two more power-limited, two INCONCLUSIVE); E2 the certified drift-direction tension
(opposite the intrinsic-ruler gentle fall, ~1–1.5 bins; selection channels audited dead);
E3 the stated-not-fitted magnitude consistency (thread near theta = ell/r(z), ell ~ 70
Mpc-scale on the SNe-fitted wall); E4 the nulls (ELG quiet everywhere; graded-out artifacts
are NOT explananda).

- **O-A**: accounts for E1 (real structure ⇒ a detectable coherent feature) and E3 (the
  magnitude sits on its own frame relation); STRAINS against E2 (its derived drift direction is
  the one the data certifiably runs opposite to); silent on E4 (ELG quiet needs a per-tracer
  amplitude story it does not have — UNDERIVED, so silent rather than strained).
- **O-B** [UPDATED post-D3]: conditionally as O-A on E1/E3 (same frame relations IF a static
  proper z-independent ell is POSITED) and then shares O-A's E2 strain; silent on E4. The AMOUNT
  is now DERIVED-NEGATIVE [D3C]: O-B has NO native scale of its own at the banked layer, so it
  accounts for E1/E3 only by IMPORTING free-data (an ell/X ratio) — no better than O-A on those
  — OR by the discreteness program firing (μ quantization, characterized-not-run). Its
  once-sharpest signature (a derived ell VALUE) does not exist natively; the honest reading is
  O-B collapses to "O-A with a posited ruler" unless discreteness supplies the amount.
- **O-C** [UPDATED post-D1/D2]: machinery now DERIVED (routes + thresholds + fold, with the
  Gaussianity SS5 and lock-form-ansatz SS9 stamps). It STRAINS against E1 as a bump-maker: the
  honest courier is scale-transparent, so it does NOT manufacture the per-shell thread from
  featureless input — a viewing-artifact account of E1 REQUIRES an inherited feature in μ's own
  field (route 1) or a fold (route 3), which is then an assumption about the field/profile, not
  a free product of the view; silent on E2/E3 until such an inherited feature is posited (F-RETRO
  bars steering to E2's reversed drift). On E4: the FORCED cross-tracer phase-identity makes
  ELG-quiet a genuine strain if any O-C pattern exists (all tracers should carry it) — now a
  derived tension, not undecided.
- **O-D**: accounts for (at most) the INCONCLUSIVE cells; STRAINS against E1 (the control cell
  is SKY-ROBUST on every powered test), E2 (the measured channel is dead two orders of
  magnitude; thread centers carry no instability that could tilt them coherently), and E3 (a
  noise conspiracy landing near one ell/r(z) curve in two tracers is unquantified); its clean
  discriminator is C3 non-replication; consistent with E4 by construction (systematics need
  not appear in ELG).
- **O-E** [UPDATED post-D4]: full derived signature set (θ_osc drift, ξ_m spacing, anti-phase
  lock, loudness hierarchy, trichotomy, visibility). HONEST LIMIT on E1: an admitted oscillation
  BELOW caustics puts its angular imprint θ_osc in the map+window (depth-projection) channel —
  per-shell w(θ) stays FEATURELESS [D4C 3(b)]. So E1's per-shell degree-scale bumps are NOT
  directly accounted by a sub-caustic oscillation; O-E's native angular home is the projected
  window channel, and per-shell bumps would need the SUPERCRITICAL/caustic regime (nm>1) or an
  inherited-feature route. Silent on E2/E3 (F-RETRO: no steering to the numbers). On E4: forced
  tracer-universality + z-locked phase makes ELG-quiet a derived strain if any O-E pattern
  exists. Its cheapest own test = the SNe-residual periodicity (scan ξ_p family + ln(1+z) edge,
  NOT z), preregistrable on in-hand data (F-RETRO-discounted, disclosed) [D4C 3(e)].

## DERIVATION-DEBT (D1/D2/D3/D4 ALL DELIVERED — MATRIX COMPLETE; only named post-freeze
## inheritances + the radial estimator + ell-freeze remain; each later prereg freezes against this list)

**D1 — static angular transfer function — DELIVERED [D1C], verified LEAD.** All five deliverables
discharged (scale-transparent static map; window-set break; radial-leg asymmetry). O-C static
cells filled.

**D2 — time-live extension — DELIVERED [D2C], verified LEAD.** All five + the mixing question
discharged (scale-transparent time-live below the fold; forced tracer phase; fold A_t=−A·A_r the
one new time-live non-analyticity; static limit recovers D1). NAMED POST-FREEZE INHERITANCES
[D2C inheritance list] — after the freeze-point, NOT blocking the matrix: (1) source back-
reaction/self-lensing; (2) off-center observers; (3) generic B(t,r)/g_tr chart beyond the SS9
lock-form ansatz (exact forms change, qualitative verdict plausibly survives); (4) non-Gaussian
statistics beyond the all-order argument (the SS5 stamp is LOAD-BEARING); (5) metric-realization
frame-pair + coefficient match for channel (i) (P-D2-5); (6) t-/r-varying mixing along a
sightline; (7) fold-onset × window-break interaction.

**D4 — O-E oscillating geometry — DELIVERED [D4C], verified LEAD** (was flagged an unowned menu
gap in the first pass; now owned and derived). C1-C6 filled (static/μ=0 scope). NAMED POST-FREEZE
INHERITANCES [D4C]: caustic-regime statistics beyond the fold-spike; the TIME-LIVE oscillation
(D4b — standing wave vs static profile, the λ_t channel; meets D2 at the shared fold, Convergences
(a)); accrual dynamics (O-E's own dynamical step, underived by contract); ε(r)-envelope forms;
the surface-brightness/image-level optics component (only achromatic + d_L/θ half derived).

**D3 — O-B's native scale — DELIVERED [D3C], verified LEAD (LANDED: D3-NO-AMOUNT, first-class).**
The AMOUNT question is answered NEGATIVE at the banked layer: no native second amount exists
(exhaustive I1-I5 inventory + R1 completeness sweep, 40/40 machine-checks). O-B's row filled.
The sharpened standard that emerged: "supply an amount" = SELECT a separation, not merely be a
pure number — the sole parameter-free banked number (reciprocal-κ spacing=1) is length-inert (a
(1+z) distance-duality convention-ratio). NAMED POST-FREEZE / GATED CONTINUATIONS [D3C]: the
fork = O-B's BAO scale is EITHER posited free-data (ell/X) OR the discreteness program's first
real job — μ quantization under a compact/winding target (the phi-angular discreteness hunch),
characterized-then-gated here (F-SCOPE, not run). Tracer coupling to any such scale = named
inheritance only (no matter dynamics banked).

**Cross-cutting debts (owned outside D1–D4; named so the freeze-point sees them):**
- **All four derivation legs (D1/D2/D3/D4) are now DELIVERED** — the matrix is COMPLETE (all
  five origins' rows derived-or-scoped). No un-delivered derivation leg remains.
- **The radial ESTIMATOR is unbuilt** [BAO CONSOLIDATED, owed]: every row's C2 is untestable
  against data until it exists, regardless of derivation status.
- **ell freeze**: O-A/C2's numeric radial prediction and any numeric theta(z) overlay need an
  ell frozen at the freeze-point (none is banked; F-SCOPE).
- The O-E SNe-residual periodicity test needs its own prereg (in-hand data; F-RETRO
  discounted and disclosed as such) [MAP§2 (iii)].

## MATRIX-CLOSED (2026-08-08, fourth pass — D3 fills O-B)

**The discrimination matrix is COMPLETE: all five origins (O-A…O-E) have every C1-C6 cell
DERIVED(cite) or scoped-UNDERIVED(owner), and all four derivation legs (D1/D2/D3/D4) are
delivered and verified-LEAD.** D3's landing (D3-NO-AMOUNT) collapsed the last conditional row:
O-B has no native scale at the banked layer, so its BAO account forks to posited free-data
(then it is "O-A with a posited ruler") or the discreteness program. **NEXT STEP = THE
FREEZE-POINT** (the arc's preregistered commit): freeze predictions + the ell nuisance-range
before BOSS/radial data are opened (F-RETRO), then build the owed radial estimator. The
freeze-point commit + owner's gate belong to the arc, not to D0/D3.

— D0 assembly agent (Fable), 2026-08-08. First pass = matrix from banked machinery; second
pass = O-C static cells from D1 [D1C]; THIRD (synthesis) pass = O-C time-live cells from D2
[D2C], O-E cells from D4 [D4C], the CONVERGENCES section, scorecard + debt; FOURTH pass = O-B
row from D3 [D3C], matrix marked COMPLETE, MATRIX-CLOSED note added. CP4: zero BOSS/data
contact throughout. NOT committed (owner's gate + the freeze-point commit belong to the arc).
