# M3d PREREGISTRATION — methodology calibration (mock injection + literature cross-check) — FROZEN

Date 2026-08-08 | branch grok | Charles's rulings: "My instinct is to question our methodology...
I find it difficult to believe that we are finding patterns in data that hundreds of other
researchers have looked at with completely different results" → "Preregister and run the
calibration. And the other option is different data sets, maybe even some partially processed
ones that are pre LCDM processing." Committed before the calibration runs. Terminology ruling
in force (BAO = the label; the object = "the observed clustering feature"; "acoustic" only
attributed to the mainstream).

## 0. The frame + the inverted steering guard (load-bearing)

THE EXPECTED OUTCOME IS THE MUNDANE ONE: our pipeline, fed a universe with one true scale,
plausibly manufactures the anomalies (scattered centers, anti-drift, tracer splits) at our S/N —
and the published angular BAO curve plausibly runs through our thread. Hypothesis discipline
therefore INVERTS the usual guard: **F-FAIR-MOCK (primary)** — the mocks must be FAIR, not
rigged to produce artifacts (realistic feature amplitude matched to the published angular BAO
signal strength, realistic densities, the real footprints/randoms; a mock so weak or so noisy
that ANY pipeline would fail is a rigged deflation and fires). The anomalies-survive outcome is
equally first-class and must be equally reachable.

## 1. LEG A — mock injection at known truth (the instrument-fidelity test)

- **Synthetic universes:** RA/DEC/Z catalogs matched per-shell to the REAL DESI densities and
  footprints (reuse the M2 pair-splitting mock generator + the real randoms as the footprint);
  TWO tracer classes matched to LRG and QSO number densities (the split question needs the
  density contrast). Feature injection: ONE true scale via pair-splitting at theta_t(z) =
  ell_t / r_truth(z), amplitude calibrated to the published angular-BAO signal strength (leg-B
  informs this; if leg B is not yet done when A starts, use the M3-measured thread amplitude —
  declared). TWO truth-curve variants (both run; instrument calibration, not cosmology): (i)
  the UDT r(z) (P1 fitted); (ii) a published-shape theta_BAO(z) drift curve (attributed to the
  mainstream; used ONLY as a truth-injection shape for instrument testing — this is Category-A
  calibration, not an ontology import; declared here to keep F-IMPORT-LCDM honest).
- **N_mock = 25 realizations minimum** per truth variant (frozen seeds; more if budget allows,
  disclosed either way).
- **Run the FROZEN pipeline unchanged** (M3 machinery + the M3c 12-bin full-covariance route)
  on every mock exactly as on real data.
- **FROZEN metrics (the calibration numbers):**
  M1: per-shell center recovery bias + scatter vs truth.
  M2: drift-direction recovery rate (how often does a TRUE gentle-fall drift come out flat or
      reversed at our S/N? — the anti-drift false-positive rate).
  M3: **the false tracer-split rate**: P(apparent LRG-vs-QSO split >= 1.75x with >= 3.8 sigma
      under the M3c error machinery | ONE true scale) — THE decisive number for the split.
  M4: center-scatter distribution (does one true scale produce 4-212 Mpc scatter at BOSS-like
      density? a BOSS-density mock arm, 10 realizations, answers the M3b scatter).
- **Frozen interpretation rule:** if M3 shows the observed split is within the false-positive
  distribution (p > 0.05 of arising from one true scale), the split is DOWNGRADED to
  method-artifact-consistent; if the observed split lies outside (p < 0.01), it RE-FIRMS with
  the calibration behind it; between = CAL-MIXED. Same structure for M2/anti-drift.

## 2. LEG B — literature cross-check (the external-consistency test)

Compile the published ANGULAR theta_BAO(z) measurements (the tomographic/angular BAO series:
DES, eBOSS/SDSS angular analyses — the M1-graded cross-check series; their small fiducial
projection correction 0.28-1.44% flagged/removed where documented). Compare their curve to OUR
measured thread theta_b(z) (DESI, full-C errors): does the published curve pass through our
thread within our errors? Frozen metric: per-shell pulls + a global chi2 of (ours - theirs).
Their values enter as PUBLISHED MEASUREMENTS (attributed; cross-check grade per M1 — this leg
tests OUR instrument against THEIR measurements, it does not import their cosmology into any
UDT fit). Also: their QSO/high-z angular results vs our QSO shells (the split's other half).

## 3. THE FOLLOW-ON ARM (recorded, gated, not run now — Charles's second option)

**ALT-DATA:** different datasets, including partially-processed / pre-LCDM-processing ones:
photometric angular catalogs (DES Y6, KiDS, HSC — angular clustering needs no z-conversion),
older spectroscopic (2dF, SDSS main), DESI DR2 when public. Purpose: replication of the
feature + the split question on data with DIFFERENT (or absent) processing chains. Own prereg
+ Charles's go when reached.

## 4. Falsifiers

**F-FAIR-MOCK** (primary, §0). **F-RETRO:** all metrics/thresholds frozen here before any mock
is run; the frozen pipeline untouched. **F-IMPORT-LCDM:** scoped as declared — the mainstream
truth-shape is an instrument-test input, attributed, never a UDT fit ingredient; leg B compares
measurements, imports no cosmology. **F-SCOPE:** deliverable = calibration verdicts on OUR
method + the comparison table; no new cosmology claims. Terminology ruling throughout.

## 5. Outcomes (frozen; all first-class)

**CAL-MUNDANE:** the pipeline manufactures the anomalies at our S/N and/or the published curve
threads our data → the split/anti-drift/scatter DOWNGRADE to method artifacts; the BAO-side
record concludes "our pipeline saw the well-measured BAO feature, poorly"; the coupling
frontier loses its empirical hook (reverts to hunch + the D3 target). **CAL-ANOMALY-SURVIVES:**
fair mocks do NOT produce the split/anti-drift at our S/N AND the published curve misses our
thread → the anomalies re-firm with calibration behind them + external tension declared.
**CAL-MIXED / CAL-OBSTRUCTED(component):** per-metric, disclosed. Blind verifier owed; then
HOLD for Charles. Verified-LEAD ceiling.

## 6. Process

Two parallel agents (A mocks/compute w/ GPU + frozen seeds + checkpoints, no monitors; B
literature/research). Then one blind verifier over both (fair-mock audit is its primary brief).
Then consolidation + HOLD.
