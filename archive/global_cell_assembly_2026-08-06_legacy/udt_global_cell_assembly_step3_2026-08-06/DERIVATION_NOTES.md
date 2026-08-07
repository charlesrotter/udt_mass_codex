# Step-3 derivation notes — closure/profile/data discrimination (LEAD / UNBANKED)

Date: 2026-08-06. Contract: `PREREGISTRATION.md` (frozen; obeyed). Status of every line:
LEAD / UNBANKED until the two adversarial reviews land. Nothing committed by this agent.
F-DATA rail: NO data file touched, NO fit, NO chi2 — sympy symbolic only (`step3_checks.py`,
13/13 PASS, exit 0). All expansions exact leading-order series, no linearization-as-result
(Taylor-with-remainder bookkeeping; every "leading" carries its explicit order).

**Standing caveat (travels verbatim on EVERY claim below):** "S (the 2026-07-01 law-set +
phi-blind sources) is UNFORCED (08-06 free-data inference) but the unique banked candidate;
conditional robust across Routes A/B." Further scope: round-static Branch-P reduction, ratio
level, Route-A orientation, even-core inner end per the source-doc cell geometry (itself a
closure CHOSE — Step-2 caveat 2), anchor RE-SCOPED to "some Delta phi > 0" (value demoted per
C-2026-08-06-2), D3 never decisive alone, no G18 ruling, no mass content.

## §0 Ground (cited at source; no producer code imported)

- Law-set S metric (Step-2 §0): ds² = −e^{−2φ}c²dt² + e^{2φ}dr² + ρ²dΩ; flux identity
  Φ := Zρ²φ', Φ' = 4e^{−2φ}ρ'² (exact, source-blind); Z > 0 anchor-forced (Route-A).
- Admitted classes (Step-2, CONSOLIDATED): 𝒜_fold = {ρ'(r_c)=0, ρ'(r_s)=0, φ slaved via the
  φ-IVP from φ'(r_c)=0, one anchor scalar}; 𝒜_glue = 𝒜_fold's superclass with the seam ρ-pin
  DROPPED (inner even-core end UNCHANGED — Step-2 §II: "Cell geometry unchanged"). Both carry
  the anchor. φ flat-then-strictly-rising (CUT-3): φ' = 0 exactly on [r_c, r*], φ' > 0 on
  (r*, r_s]. Finite core ρ_c > 0 BANKED (07-02 R2, blind-verified; re-cited at Step 2).
- L-lead: φ_L = −(1/2)ln(1−r/X); OUTSIDE 𝒜_fold (both ends, 2 independent facts); OUTSIDE
  𝒜_glue via the INNER end only; BULK-INSIDE S via the exact quadrature ρ₊ (Step-2 §III:
  u = ρ'/ρ solves 4(m/X)u² − (Z/m)u − Z/(2m²) = 0, m = X−r, two real nonzero roots).
- Redshift readout (canon C-2026-07-02-1 form): 1+z = e^{Δφ}, Δφ = φ(emit) − φ(obs); static
  lapse N = e^{−φ} gives this exactly (no expansion). c_eff two-point ratio = (1+z)^{−2}
  (canon C-2026-08-06-1; identity re-verified, check C7).
- WR-L observer seat at source: `simple_metric_L_native_optical_derive_results.md:72`
  ("Integrate from the observer φ=0, r=0"); `simple_metric_DA_native_derive.md:55` ("observer
  at r=0, φ(0)=0 by gauge (relational seat = chart origin)"). x_max = the observer-pair
  dilation asymptote, an OUTPUT, "NOT a wall/edge/center" (G14, assembly MAP:23).
- Etherington bank at source: `simple_metric_DA_native_derive.md:80` "Banked: d_L = (1+z)²D_A
  with 1+z = e^{φ} (static)", and §1 there: D_A = r holds FOR THE OBSERVER AT CHART ORIGIN
  (rays converge to a point; angular coefficient = r² with areal radius → 0 at the seat).
- Prior low-z theorem at source (`simple_metric_lowz_linear_native_derive.md` §2): under
  P1–P4 a smooth-center seat (φ'(0)=0, φ ~ a₂r²) gives d_L ∝ √z — no linear onset. Q3b below
  is the S-cell sharpening of that banked observe (the cell core forces MORE flatness).

## §Q3a The observer seat: adjudication (cited; both cases carried)

The two banked pictures do NOT place the same local structure under the observer:

1. **Cell picture (canon C-2026-07-02-1):** the anchor is Δφ = φ(CMB fold) − φ(core) with the
   OBSERVED CMB redshift 1+z_CMB = e^{Δφ}. The static readout 1+z = e^{φ(emit)−φ(obs)} makes
   this equality hold IFF φ(obs) = φ(core) — the canon's own redshift statement pins the
   receiver to the φ-floor. Within both admitted classes the φ-floor is the flat segment
   [r_c, r*] (CUT-3), where φ' = 0 IS FORCED (even-core pin + flux identity). So the cell
   record's seat = core (or anywhere on the flat segment; all such seats are φ'=0 seats).
   The canon does not use the word "observer"; the pin is via the readout equality. Honest
   tag: DERIVED-from-canon-form, one inference step (surfaced, reviewable).
2. **WR-L picture:** the observer sits at the chart origin r=0 with φ(0)=0 — a RELATIONAL
   seat ("relational seat = chart origin", DA_native:55), and there φ_L'(0) = 1/(2X) ≠ 0:
   the seat is NOT a critical point of φ. x_max is observer-relative (G14), so every
   observer carries this seat in their own chart.

**Adjudication: the seats AGREE in position-label (inner end, "r=0"/core) at ratio level
(the φ-shift between conventions is absorbable, Step-2 C3 lemma) but CONFLICT in the forced
local germ: cell-core seat has φ'(obs) = 0 (forced); WR-L seat has φ'(obs) = 1/(2X) ≠ 0.**
The record does not adjudicate which germ is the physical observer's — this is exactly the
three-way tension at seat level, not a resolvable citation question. Per contract: BOTH
cases carried below — (i) core/φ-floor seat (φ'(obs)=0), (ii) off-critical seat
(φ'(obs)≠0: off-core in the cell classes, or the inner-end seat under the free-core fork).
Note the post-re-scope freedom: an off-core seat re-anchors the observed CMB span to
φ(fold)−φ(r_obs) < Δφ_cell — admissible now that the anchor is "some Δφ > 0" (re-scope),
but it BREAKS the exact canon equality 1+z_CMB = e^{Δφ_cell} (named cost, carried in Q3d).

## §Q3b.0 Which distance (the 08-06 lesson: no silent substitution)

Three candidate radial measures from the observer at r_obs: chart Δr (GAUGE — rejected),
proper d = ∫_{r_obs}^{r} e^{φ(s)}ds (the metric's own ruler — PRIMARY), areal ρ(r)
(REJECTED as a distance-from-observer in these classes: ρ(seat) ≥ ρ_c > 0 banked — it does
not vanish at any admissible seat, so it is not a distance from the observer at all; used
below only as the labeled AREAL-EXCESS variable ρ − ρ(seat) where informative). d_L enters
only via the banked Etherington form, cited with its own seat condition (§Q3c.2). Every
z-expansion below is stated in proper d; conversions are printed, not substituted.

## §Q3b Fold-class low-z structure (exact leading orders)

### §Q3b.1 Core seat (φ'(obs)=0 forced): the onset is QUARTIC — not linear, not quadratic

Setup: seat at r_c (any flat-segment seat is identical up to an exact z≡0 plateau, below);
t := r − r_c. Even-core pin: ρ'(r_c) = 0, generic member ρ' = a t + O(t²), a := ρ''(r_c) ≠ 0.
Flux identity with Φ(r_c) = 0 (φ'(r_c)=0 pin):
  Φ(t) = ∫₀ᵗ 4e^{−2φ}ρ'² = (4/3)e^{−2φ_c}a²t³(1+O(t)),  φ' = Φ/(Zρ²),
  φ(t) − φ_c = [a²e^{−2φ_c}/(3Zρ_c²)] t⁴ (1+O(t))    [C1a/C1b PASS: t¹,t²,t³ coeffs ≡ 0].
The pin kills z', z'', z''' at the seat — one order FLATTER than the prereg's contemplated
"quadratic onset", and flatter than the banked smooth-center √z observe (lowz_linear doc §2),
because S adds the ρ-pin: φ''(r_c) = 4e^{−2φ_c}ρ'(r_c)²/(Zρ_c²) = 0 too.
With 1+z = e^{φ(r)−φ_c} and proper d = e^{φ_c}t(1+O(t⁴)):

  **z(d) = [ρ''(r_c)² e^{−6φ_c} / (3 Z ρ_c²)] · d⁴ + O(d⁵)**    [C1c PASS]

Exact leading coefficient in class data (ρ''(r_c), ρ_c, Z, φ_c = −Δφ_cell under the canon
convention φ(fold)=0; note the depth amplification e^{−6φ_c} = (1+z_CMB)⁶). General
activation order ρ' ~ a t^α (α ≥ 1, C² class): z ~ t^{2α+2}, coefficient
4a²e^{−2φ_c}/((2α+1)(2α+2)Zρ_c²) [C2 PASS] — onset order ≥ 4 for EVERY member; degeneracy
only raises it. Flat-segment seat r_obs < r*: z ≡ 0 EXACTLY out to the activation, then the
same ≥ 4-order onset in distance-past-activation. Measure-robustness (no silent
substitution): order 4 in proper d, order 4 in chart Δr, order 2 in areal EXCESS ρ−ρ_c
[C1d PASS: z = 4e^{−2φ_c}/(3Zρ_c²)·(ρ−ρ_c)²] — LINEAR in none. Sign: φ monotone ⇒ z ≥ 0
all-sky; round symmetry at the inner-end seat ⇒ ISOTROPIC. **Verdict (S-caveat above): the
fold-class core seat has NO linear (and no quadratic) Hubble onset — z starts at d⁴.**

### §Q3b.2 Off-core seat (r_obs > r*): linearity restored, but with a forced LEADING dipole

Generic off-core seat: p₁ := φ'(r_obs) > 0 (strict on (r*, r_s]), p₂ := φ''(r_obs)/2,
φ₀ := φ(r_obs). Exact series + exact reversion to proper d [C3-rev PASS]:
  OUTWARD:  z_out(d) = p₁e^{−φ₀} d + p₂e^{−2φ₀} d² + O(d³)    [C3a PASS]
  INWARD:   z_in(d)  = −p₁e^{−φ₀} d + p₂e^{−2φ₀} d² + O(d³)
Leading order IS restored: H_* := e^{−φ₀}φ'(r_obs) (= dφ/dℓ_proper at the seat). But the
same-distance asymmetry is exact and UNSUPPRESSED [C3b PASS]:
  **dipole  (z_out − z_in)/2 = H_* d + O(d³)   — the ENTIRE leading signal;**
  **monopole (z_out + z_in)/2 = (e^{−2φ₀}φ''₀/2) d² + O(d³) — quadratic only.**
General direction (round cell, off-center seat): z depends only on endpoint φ (static
readout), and φ(source) − φ₀ = φ'₀·δr with proper displacement radial component
δr = e^{−φ₀}d·cosθ + O(d²) ⇒ z(d,θ) = H_* d cosθ + O(d²): a PURE DIPOLE at leading order.
Half the sky is BLUESHIFTED at leading order (z_in < 0); the sky-averaged (monopole) law is
QUADRATIC at every off-core seat, with coefficient (e^{−2φ₀}φ''₀/2), φ''₀ from the φ-EL:
φ'' = 4e^{−2φ}ρ'²/(Zρ²) − 2φ'ρ'/ρ. Characterization only (no sky-data comparison): the
off-core rescue buys directional linearity at the price of a leading-order, order-unity
anisotropy (dipole/monopole → ∞ as d → 0), plus the Q3a canon-equality break.

## §Q3c Glue-class low-z structure

### §Q3c.1 As admitted at Step 2: IDENTICAL to the fold at low z (closure-blind result)

𝒜_glue differs from 𝒜_fold ONLY at the seam (ρ'(r_s) pin dropped; B free). The low-z
expansion around any interior seat never reaches r_s: every Q3b formula (quartic core onset,
off-core dipole/monopole) carries VERBATIM to 𝒜_glue — the even-core inner end is shared
("Cell geometry unchanged", Step-2 §II). **Finding the prereg framing did not anticipate:
leading-order low-z structure is SEAT- and INNER-END-determined, OUTER-CLOSURE-BLIND. The
fold-vs-glue discrimination cannot be made at low-z onset level within the source-doc cell
geometry; linear onset is generic exactly where φ'(obs) ≠ 0 is available — off-core seats
in BOTH classes (with the dipole cost), never the core seat in EITHER.**

### §Q3c.2 The WR-L seat (r=0, φ_L'(0) = 1/(2X) ≠ 0): the fork row + z(z+2) at chart level

The seat with φ'(0) ≠ 0 at the INNER END exists in NEITHER admitted class (the even-core pin
forbids it; L is outside 𝒜_glue via the inner end — Step-2 §II.4). It requires the
FREE-CORE INNER-END FORK (Step-2: "a fork, not a finding" — relaxing the source-doc cell
geometry). Under that fork, with φ = φ_L and the observer at r=0, φ(0)=0:
  1+z = e^{φ_L(r)} = (1−r/X)^{−1/2};  banked Etherington d_L = (1+z)²D_A, D_A = r
  (`simple_metric_DA_native_derive.md:69,80`) ⇒ **d_L/X = z(z+2) EXACTLY** [C4 PASS] —
  the record's reproduction verified symbolically; low-z: z = d_L/(2X) + O(d_L²), i.e.
  H_* = 1/(2X) [C4b PASS], isotropic (inner-end seat, round symmetry). No fitting.
TWO exact S-embedding residues (found here, offered to review; they CONDITION the row, they
do not void the chart-level identity as banked):
  (R-a) **ρ = r is NOT the S-realization of φ_L**: u = 1/r fails the Step-2 §III quadratic
  identically [C5 PASS]. The S-embedded L carries ρ₊ ≠ r; the WR-L simple metric (angular
  coefficient r²) and the S-cell metric (ρ₊²) share g_tt, g_rr — so z(d_proper) and the
  LINEAR onset carry exactly — but the AREAL sector differs, and d_L = (1+z)²·(areal-based
  D_A) need not equal (1+z)²·r in-cell.
  (R-b) **No areal center is S-available even under the fork**: u₊ is finite at r=0
  (u₊(0) = (Z+√(Z²+8Z))/(8X) [C6 PASS]), so ρ(0) = ρ(r₀)·exp(−∫ u₊) > 0 — ρ → 0 at the seat
  is impossible along the L-branch. The banked D_A = r derivation is seat-conditional on
  areal radius → 0 at the observer (DA_native §1); in-cell D_A must be re-derived (OPEN,
  named). **So: linear onset generic and exact at this seat; the z(z+2) d_L-shape is
  chart-level-exact as banked, S-embedding of its d_L readout CONDITIONAL on the open
  in-cell D_A identification.** (S-caveat above travels.)

## §Q3d The pairing table (every cell carries the §-header S-caveat verbatim by reference)

Columns: D1-lin = low-z LINEAR Hubble onset (model-independent leg; observed law is a
sky-mean/monopole law); D1-shape = the z(z+2) d_L structure (structural only); D2 = some
Δφ_cell > 0; D3 = CMB value (interpretation-conditional, NEVER decisive alone).

| Pairing | D1-lin | D1-shape z(z+2) | D2 | D3 |
|---|---|---|---|---|
| fold × core seat | **STRUCK** (z = K d⁴ exact, K = ρ''(r_c)²e^{−6φ_c}/3Zρ_c²; no linear, no quadratic term — §Q3b.1) | **STRUCK** (z(z+2) forces dz/dd_L\|₀ = 1/(2X) ≠ 0 [C4b] vs quartic seat; PLUS φ_L ∉ 𝒜_fold, 2 exact facts, Step-2 §I.4; PLUS ρ_c > 0 vs the D_A = r seat condition) | consistent (Step-2 Q2a) | conditional-consistent (canon equality holds at this seat) |
| fold × off-core seat | **CONDITIONAL** (directional linearity restored, H_* = e^{−φ₀}φ'₀; named rescue = anisotropic-linear reading; COST: pure leading dipole H_*d cosθ, half-sky blueshift, sky-mean quadratic (e^{−2φ₀}φ''₀/2)d² — §Q3b.2) | **STRUCK** (φ_L ∉ 𝒜_fold seat-independently; both ρ-pins unsatisfiable under φ_L — Step-2 §I.4(ii)) | consistent | conditional (re-anchors span; canon equality broken — Q3a cost) |
| glue × core seat | **STRUCK** (identical to fold × core — closure-blind, §Q3c.1) | **STRUCK** (inner end: φ_L'(r_c) ≠ 0 vs even pin; ρ_c > 0 vs center seat — Step-2 §II.4) | consistent | conditional-consistent |
| glue × off-core seat | **CONDITIONAL** (identical to fold × off-core, same dipole cost) | **STRUCK** (via inner end only, as at Step 2) | consistent | conditional (as above) |
| glue × free-core-fork inner seat (WR-L germ; NOT an admitted-class row) | **STRUCTURALLY-CONSISTENT** (isotropic linear, H_* = 1/(2X) for L [C4b]) | **CONDITIONAL** (chart-level EXACT [C4]; S-embedding residues R-a (ρ₊ ≠ r [C5]) + R-b (no areal center, u₊(0) finite [C6]) ⇒ in-cell D_A derivation = named open cost — §Q3c.2) | consistent (bulk quadrature carries any span) | conditional (seat at φ-floor of the fork geometry; equality form retained) |

Row-5 price, stated exactly: adopt the free-core inner-end fork (= abandon the source-doc
even-fold core, the fold-doc universe-cell geometry; Step-2 flagged it "a fork, not a
finding") AND adopt the glue outer closure (fold's seam ρ-pin also excludes L) AND derive
the in-cell D_A (open). It is the ONLY row with an unconditional D1-lin pass.

### The three-way tension {fold, L/SNe-structure, S} — what must give, per surviving pairing

1. **Keep the fold (source-doc geometry, canon-flavored):** the L/SNe leg gives TWICE —
   z(z+2) exactness gives at every seat (exact strikes), and D1-linearity gives either
   entirely (core seat: quartic) or as a monopole law (off-core: sky-mean quadratic +
   leading dipole). S itself untouched. D2/D3 survive.
2. **Keep the L/SNe structure whole (D1-lin isotropic + z(z+2)):** the fold gives at BOTH
   ends — its seam ρ-pin (choose glue) AND its shared even-core inner end (the free-core
   fork). S itself survives (L is bulk-inside S), with the named residue that z(z+2)'s d_L
   readout is chart-level pending in-cell D_A (R-a/R-b). This is G18-pressure territory:
   CANON-ADJACENT, flagged for Charles, NO ruling here.
3. **S gives:** NOT FORCED by anything above — both resolutions live inside S. Named only as
   the outermost escape; S remains "unforced but the unique banked candidate" (caveat).

### Landed outcome class: **S3-MIXED** (with a CANON-ADJACENT flag)

Not S3-FOLD-STRUCK verbatim: its rider "glue is sole survivor" did NOT land — glue AS
ADMITTED is equally struck/conditional at low z (closure-blind §Q3c.1); the only clean
D1-consistent row rides the free-core fork, which is outside both admitted classes. Not
S3-FOLD-VIABLE(cond) alone: the fold's surviving pairing (off-core) still has z(z+2) struck
unconditionally, so the SNe-shape leg gives regardless. Hence S3-MIXED, componentwise:
- FOLD: struck on D1-shape at every seat (exact); struck on isotropic D1-lin at the core
  seat (quartic); conditional-only rescue = off-core anisotropic-linear (order-unity dipole
  cost + canon-equality break). Owner-favorable class does NOT clear D1 — stated plainly
  (F-STEER head 1); the strikes are exact, not driver judgment calls (F-STEER head 2: the
  restored-linearity and the fork row are reported with full force, no over-deflation).
- GLUE (as admitted): same low-z verdicts; its Step-2 admits-all advantage buys NOTHING at
  low z. GLUE + free-core fork: the sole structurally-consistent D1 row, conditional on the
  fork + open in-cell D_A. CANON-ADJACENT: fold under D1 pressure ⇒ G18 flag for Charles,
  no ruling (F-SCOPE).

## Caveats (each travels with every claim)

1. Header S-caveat verbatim; round-static Branch-P; ratio level; Route-A orientation
   (Route-B monotone object not re-derived here — Step-2 caveat 5 inherited).
2. Even-core inner end = source-doc geometry, itself a closure CHOSE (Step-2 caveat 2); the
   free-core row is labeled fork-not-finding wherever it appears.
3. Anchor re-scope (C-2026-08-06-2): all results value-independent; only e^{−6φ_c} = (1+z_CMB)⁶
   in the quartic coefficient is value-riding (symbolic, re-parameterizable). D3 never
   decisive alone; no G18 ruling; no mass content.
4. The Q3a cell-seat pin is DERIVED-from-canon-form (one inference step: the readout equality
   pins φ(obs) = φ(core)); both seat cases carried throughout per contract.
5. Generic-member statements (a = ρ''(r_c) ≠ 0; p₁ > 0 off-core) are labeled; degenerate
   members only FLATTEN onsets further (C2) — no strike weakens under degeneracy.
6. Characterize-not-filter: no solution was discarded; every row is reported with its exact
   onset. No numerical fit, no chi2, no data file (F-DATA clean). Checks: `step3_checks.py`
   13/13 PASS exit 0 (sympy exact; series with explicit orders; no float anywhere).
7. LEAD / UNBANKED pending the two adversarial reviews (algebra/at-source; classification/
   steer/scope). Suggested first attacks: the Q3a receiver-pin inference; the C3 reversion
   orders; whether the D_A = r seat condition is truly load-bearing for the D1-shape strikes
   (it is the newest link: R-a/R-b).

## One-line

Within S, low-z structure is seat- and inner-end-determined and outer-closure-blind: the
forced φ'(core) = 0 seat starts the Hubble relation at d⁴ (exact), any φ' ≠ 0 seat restores
linearity only with a leading-order dipole, and the lone fully-linear isotropic row is the
WR-L germ — available only outside both admitted classes via the free-core fork: S3-MIXED,
fold under D1 pressure, CANON-ADJACENT flag raised, nothing ruled.

## CONSOLIDATED (2026-08-06, both reviews in): S3-MIXED SUSTAINED — AMENDED A1-A4

Files: ADVERSARIAL_REVIEW_1_algebra.md (SUSTAINED, no cell changes; independent-method recomputes),
ADVERSARIAL_REVIEW_2_classification.md (SUSTAINED-AMENDED A1-A4; independent source verification).

**Algebra fully confirmed (R1, independent method):** the core-seat QUARTIC onset stands (t^1-t^3
identically zero; d^4 coefficient exact); the transplant hypothesis FAILS (BOTH phi'(r_c)=0 AND
rho'(r_c)=0 are CORE pins from stationarity at source :37-38,106 — the seam pin is separate);
counterfactual: even without the rho-pin the onset is quadratic and the LINEAR term still dies, so
NO strike flips either way. Outer-closure-blindness confirmed (phi slaved from the inner end; glue
relaxes nothing inner). The off-core dipole confirmed exact; the BOOST ESCAPE REFUTED (kinematic
dipole is d-independent; a position dipole ~ H*d cannot be cancelled beyond one shell). C4-C6
confirmed (z(z+2) exact at the fork seat, slope 1/(2X)=H*; rho=r not an S-solution under phi_L;
rho(0)>0 forced — the D_A conditionality is genuinely load-bearing). Seat inference confirmed as
scoped (canon pins the phi-VALUE; phi'=0 is class-conditional — the fork's floor point has phi'!=0
with the equality retained).

**AMENDMENTS APPLIED (R2):**
- **A1:** fold x off-core D1-linearity re-graded **STRUCK-IN-EFFECT** — the rescue is named-but-
  DEAD (the derivation itself shows the dipole/monopole grow without bound; and R1 refuted the
  boost absorption). Rail ruling recorded: citing D1's qualitative preregistered content (no
  half-sky blueshift; linear sky-mean) is legitimate characterization; F-DATA = fit/chi2/file only.
- **A2:** "fold gives at BOTH ends" REWORDED — unconditional D1 pressure is **SEAT-SIDE ONLY**; the
  outer-seam leg rides the z(z+2)=>phi_L identification (conditional on the open in-cell D_A); and
  **COVERAGE GAP logged: free-core-inner x fold-outer was never analyzed by Step 2** — the fold at
  the OUTER seam is not struck; open pending that class.
- **A3:** row-5's "unconditional pass" STRUCK — no row is unconditionally D1-clean in-cell; the
  sole survivor (glue + free-core fork seat) is CONDITIONAL on the open in-cell D_A derivation.
- **A4:** the **RECORD-SEAT-CONFLICT** promoted to a named flag CO-EQUAL with G18-pressure: canon's
  cell readout seats the receiver at the phi-floor (slope class-conditionally zero) while banked
  WR-L seats the observer at a chart origin with phi'=1/(2X)!=0 — verified at both sources; D1
  discriminates between these two banked PICTURES more sharply than between fold and glue. The
  step's most consequential output.

**FINAL LABEL: S3-MIXED — the floor-seat is struck by D1 for BOTH closures as-admitted (quartic
onset; off-core rescue dead); the sole surviving pairing is glue + the free-core fork seat,
conditional on the in-cell D_A; fold-at-the-outer-seam is OPEN (coverage gap), not struck.** All
within S (caveat verbatim); D3 never decisive; G18 flag-not-ruling; same-repo review caveat + the
external bar travel. Errors caught ran in opposite directions (no directional steer).
