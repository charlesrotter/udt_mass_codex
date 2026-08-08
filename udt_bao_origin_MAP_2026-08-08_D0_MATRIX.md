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

Numeric anchor available to any row that needs the fitted frame (F-ANCHOR premise travels):
SNe-fitted P1 (mode A/zCMB): inv_n = 0.947 [0.9284, 0.9658] (n ≈ 1.06); mode B: X_eff = 2086 Mpc,
R_w(best n) = 2202.6 Mpc; n=1 exclusion 2.82σ (zCMB), 3.89σ (zHD column) [SNE]. NO ell is banked
(no BAO-alone X-range; the ~70 Mpc-scale ell is stated-not-fitted context) [BAO].

## THE MATRIX (rows = origins; columns C1–C6; every cell = DERIVED(cite) / DEFINITIONAL /
## UNDERIVED(owner) — an over-filled matrix is the failure mode)

| origin | C1 theta(z) drift across thread | C2 radial signal class | C3 BOSS replication | C4 tracer-universality/phase | C5 amplitude/z | C6 other distinct signatures |
|---|---|---|---|---|---|---|
| **O-A** intrinsic, frame-mapped | DERIVED: monotone FALL (gentle under fitted P1: −0.40 bins z 0.925→1.025, −1.07 bins 0.725→0.925). E2 tension noted (below). | DERIVED (class only): trichotomy Δz_BAO grows/const/decays (P1/P2/P3); GROWS under fitted P1. Amplitude needs frozen ell — UNDERIVED(freeze-point). | YES — definitional (real structure, same sky): same (theta, z) features [MAP§2]. | Scale SHARED across tracers (definitional: one structure); per-tracer amplitude UNDERIVED (needs a tracer/bias model — outside banked machinery). | UNDERIVED (needs a structure model; outside this arc's machinery). | P1 minimal-angle floor theta→ell/R_w as z→∞ [D1F §3, O2 (B)]; AP-like ratio Δz/(z·theta)→1 at z→0, all profiles [D1F §4]. |
| **O-B** orchestra-generated | CONDITIONAL: IF the native ell is z-independent and proper, the banked forms apply ⇒ same gentle fall as O-A [D1F §3, P-STATIC-RULER tag]. Whether ell is z-dependent/other-realized = UNDERIVED(D3). | Same conditional: trichotomy applies to any static proper ruler [D1F §4]; realization + z-dependence = UNDERIVED(D3). | YES + possibly tracer-dependence signatures [MAP§2, stated not derived]. | Possibly tracer-DEPENDENT (matter couples; MAP§2) — signature shape UNDERIVED(D3). | UNDERIVED(D3). | The AMOUNT: a native ell needs x_max/M_total or a discreteness scale (mu seed) [MAP§2]; a derived ell VALUE is O-B's sharpest signature — UNDERIVED(D3). |
| **O-C** pure viewing artifact | DERIVED, STATIC/mu=0 scope (D1): the static map imprints NO angular scale — featureless in ⇒ featureless out PROVEN; refinement (R1-V2): any finite observation WINDOW adds a smooth projection break θ_break ≈ Δℓ_p(bin)/r(z) — window-set, not map-made; the metric controls only its smooth depth-drift [D1C]. Time-live: UNDERIVED(D2). E2's reversed drift stays not-a-target (F-RETRO). | DERIVED, STATIC/mu=0 scope (D1): NO Δz scale creatable (no-extremum theorem); the static radial imprint = the growing stretch J(z) = (n/2R_w)(1+z)^(2/n) plus ONE depth-scale bend (only scale n·(1+z₁)); derived angular/radial leg asymmetry [D1C]. mu static inertness carried as scope. Time-live: UNDERIVED(D2). | YES — any survey of the same sky depth (the view, not the galaxies) [MAP§2]. | DERIVED-PARTIAL, STATIC/mu=0 scope (D1): the OPERATOR is tracer-BLIND (achromatic; no tracer parameter exists in T) — but the phase-identity signature is VACUOUS at the static layer (no T-generated pattern exists to share a phase) → UNDERIVED(D2) [D1C]. The window-break location is per-tracer (a feature of map-plus-window, not of T) [D1C]. | DERIVED, STATIC/mu=0 scope (D1): value-preserving at fixed proper separation (w = C(s), depth-independent); at fixed angle w ∝ r(z)^(−γ), monotone fall, no feature in z. Time-live: UNDERIVED(D2) [D1C]. | Cross-tracer identity (C4) is itself the distinct signature; any D1 featureless result is SCOPED static, never final (CP2) [MAP §3]. |
| **O-D** residual mundane | No prediction machinery. Banked negative: the one measured selection channel (dN/dz z̄-tilt) is quantitatively dead for the drift (≤0.01 bins vs ~1–1.5 observed, sign-incoherent) [AUD]. Unaudited layers remain (INCONCLUSIVE grades) — UNDERIVED/none. | No machinery; no coherent radial prediction exists to derive — expectation of incoherence is stated, not derived. | **NON-replication** — DEFINITIONAL (decorrelated systematics); the cheapest kill available [MAP§2]. | Tracer-SPECIFIC (each tracer has its own selection layers) — definitional; no phase prediction. | No stable prediction (noise conspiracies). | Its live room is the audited record itself: the INCONCLUSIVE cells (LRG 0.90–0.95, QSO 1.10–1.25, QSO 1.85–2.00) and the power-limited caveats on two SKY-ROBUST thread cells [AUD final grade table]. |
| **O-E** oscillating geometry | UNDERIVED — and NO owning D-item exists in the §5 menu (gap flagged below). An oscillating A(r) is OUTSIDE the frozen O2/O3 monotone family; any such work carries its own class declaration (F-SHOP-CLASS analog) [MAP§2]. | UNDERIVED (same gap; a geometric oscillation would need its own radial-imprint derivation). | YES — definitional (the geometry is there for any survey; same pattern, same phase) [MAP§2 (i)]. | TRACER-UNIVERSAL: all tracers ride the same geometry — same pattern, SAME PHASE [MAP§2 (i), recorded, cite-not-derive]. | UNDERIVED. | Recorded in MAP§2 (ii)–(iv): an OPTICS component (background light modulated too); oscillatory SNe-Hubble-residual periodicity at the corresponding spacing (cheap preregistrable, F-RETRO-discounted, disclosed); phase-coherence structure across z-shells. |

*(O-C row updated 2026-08-08 post-D1 [D1C]: static-layer cells filled, time-live cells left
UNDERIVED(D2) as before. The CURRENT-SCORECARD §below predates D1 and, for O-C's static
layer only, is superseded by the row.)*

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
- **O-B**: conditionally as O-A on E1/E3 (same frame relations IF static proper z-independent
  ell — D3's question) and then shares O-A's E2 strain; silent on E4; additionally owes the
  AMOUNT (a native ell source) before it accounts for anything in its own right.
- **O-C**: silent on E1, E2, and E3 — its machinery (the transfer function) is entirely
  underived (D1/D2); E2's reversed drift is its open invitation, not yet its account (F-RETRO);
  on E4: IF the derivation yields cross-tracer identity, ELG-quiet becomes a strain — undecided
  until D1/D2.
- **O-D**: accounts for (at most) the INCONCLUSIVE cells; STRAINS against E1 (the control cell
  is SKY-ROBUST on every powered test), E2 (the measured channel is dead two orders of
  magnitude; thread centers carry no instability that could tilt them coherently), and E3 (a
  noise conspiracy landing near one ell/r(z) curve in two tracers is unquantified); its clean
  discriminator is C3 non-replication; consistent with E4 by construction (systematics need
  not appear in ELG).
- **O-E**: silent on E1, E2, E3 (no machinery; no owning work item yet); on E4: recorded
  tracer-universality (same pattern, same phase) makes ELG-quiet a potential strain once
  derived — undecided; its recorded signatures (SNe-residual periodicity, optics component,
  phase coherence) are preregistrable tests, not yet accounts.

## DERIVATION-DEBT (what D1/D2/D3 must produce to complete their rows; each later prereg
## freezes against this list)

**D1 — static angular transfer function (O-C's first slice, scoped):**
1. Existence: does the static comparison map imprint ANY angular feature on a statistically
   plain source field at DR1-like depths? (Featureless = first-class AND scoped "static".)
2. If features: the theta(z) drift law across z-shells (fills O-C/C1, static-scoped).
3. Cross-tracer behavior: identical pattern AND phase across tracers at same z, yes/no
   (fills O-C/C4 — the sharp signature).
4. Amplitude vs z (fills O-C/C5, static-scoped).
5. The radial-statistic imprint, or an explicit scoped statement of static-layer silence
   (fills O-C/C2, static-scoped; mu static inertness carried as scope).
   Duties: premise ledger per solve, every sector ON/OFF tagged (F-FREEZE); no steering
   toward E2's reversed drift (F-RETRO); observe-mode; two reviews.

**D2 — time-live extension (clock→screen mixing un-tabled; angular + mu genuinely on):**
1–5. The same five deliverables with time live — each either supersedes or scopes D1's
   static answer; a static null may never be quoted unscoped (CP2).
6. Explicitly: does the mixing channel entering lambda_t modulate the VIEW (O-C) and does
   mu's defect acquire any kinematic role beyond the static layer? (Its static inertness is
   scope, not prior.)
   Duties: bounded symbolic first (anti-hang rules for any numerics); full ON/OFF ledger.

**D3 — O-B's native scale (separately gated; discreteness-adjacent; mu seed's first live test):**
1. The AMOUNT: does the between-frames physics supply a native length — from x_max/M_total,
   the mu/discreteness territory, or another derived invariant? (No ell may be posited.)
2. The ell value or its scaling relation (comparison to the stated ~70 Mpc-scale happens only
   AFTER the frozen commit — F-RETRO).
3. z-dependence and realization: is the native ell z-independent and proper? If yes, the banked
   D1F forms complete O-B/C1-C2 (gentle fall + P1-growing radial); if no, D3 owes the modified
   drift/radial law.
4. The tracer-coupling signature (fills O-B/C4): how matter's coupling to the generated scale
   depends (or not) on tracer type.

**Cross-cutting debts (owned outside D1–D3; named so the freeze-point sees them):**
- **O-E has NO owning work item** in the MAP §5 menu: its C1/C2 cells need a metric-led
  oscillating-solution derivation (own class declaration — outside the frozen O2/O3 monotone
  family; F-SHOP-CLASS analog). Flagged as a menu gap for Charles; D0 does not invent a D4.
- **The radial ESTIMATOR is unbuilt** [BAO CONSOLIDATED, owed]: every row's C2 is untestable
  against data until it exists, regardless of derivation status.
- **ell freeze**: O-A/C2's numeric radial prediction and any numeric theta(z) overlay need an
  ell frozen at the freeze-point (none is banked; F-SCOPE).
- The O-E SNe-residual periodicity test needs its own prereg (in-hand data; F-RETRO
  discounted and disclosed as such) [MAP§2 (iii)].

— D0 assembly agent (Fable), 2026-08-08. CP4: zero BOSS contact. Not committed by D0;
two reviews + the freeze-point commit belong to the arc, not to this step.
