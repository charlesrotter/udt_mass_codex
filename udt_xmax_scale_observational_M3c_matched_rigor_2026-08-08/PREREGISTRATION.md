# M3c PREREGISTRATION — matched-rigor covariance re-run — FROZEN

Date 2026-08-08 | branch grok | Charles's ruling: "research how DESI/BOSS cleaned up their data
(avoiding LCDM methods), firm the covariance or anything else necessary, download more data if
needed, rerun with matched rigor... stabilize before banking." Committed BEFORE the re-run sees
its effect on the ruler/feature question. Basis: METHODOLOGY_MAP.md (Phase-1 research).

## 0. The anti-steering lock (load-bearing — we have SEEN the M3/M3b data)

Every rigor upgrade below is adopted for STATISTICAL CORRECTNESS + LCDM-NEUTRALITY, decided
here BEFORE observing its effect on the feature/ruler/tracer-split question. F-STEER (both
directions): a firmed covariance that WEAKENS the features to nothing is a first-class,
equal-temperature outcome — we are as prepared to find "the features were covariance artifacts"
as "they survive." No upgrade may be added/dropped after seeing its ruler effect (F-RETRO).

## 1. Frozen upgrades ADOPTED (all NEUTRAL per the map; ranked)

1. **FULL bin-bin covariance** replacing the M3 diagonal jackknife (the direct fix for the
   flagged caveat). Method, in priority order with pre-declared fallback:
   (a) PRIMARY: many-region delete-one JACKKNIFE full C from the catalogs, with N_regions
   chosen >= N_theta_bins + 15 so C is invertible (recount with finer regions — bounded, GPU);
   (b) FALLBACK if recount over-budget: BOOTSTRAP-resample the existing 24 region-blocked
   counts (banked) to a full C, AND/OR reduce N_theta_bins so 24 > N_bins+2 (invertible from
   banked counts, zero recount). The θ-binning under (b) is FROZEN here: 12 log bins on
   [0.3,12] deg. All routes are data-only (no mocks, no theory P(k)).
2. **Hartlap (2007) + Percival (2014) factors** on C^-1 and on parameter errors (mandatory for
   a noisy inverted sample covariance). Frozen formulae.
3. **Integral-constraint correction** (Roche-Eales, from RR only — neutral) applied to w(θ).
4. **Full randoms** (undownsample; DESI up to available, BOSS random0+random1) to cut RR shot
   noise below the JK variance — bounded per anti-hang; GPU pair counts.
5. **PIP bitweights** for fiber collisions — ADOPTED-IF-FEASIBLE only (heavy; may defer to a
   named follow-up if acquisition/among-realization cost exceeds the overnight budget — its
   deferral is disclosed, not silent, and does not block the covariance core).

## 2. Frozen FORBIDDEN (F-IMPORT-LCDM, from the map)

Reconstruction; fiducial z->distance/comoving conversion + the whole 3D ξ(s)/P(k) path;
r_d/acoustic templates/D_V-r_d; ALL mock covariances (EZmock/QPM/Patchy/GLAM/Abacus — DESI
DR1's shipped covariance uses these => we build our OWN data covariance); NX/NZ/NBAR/COMOVING/DC
columns; FKP as-shipped (reimplement natively from ANGULAR number density if used at all — S/N
weight only). WEIGHT_SYS kept as a with/without variant (ML over-correction hazard).

## 3. The re-run (frozen scope)

Re-run BOTH DESI (the M3 sky-robust + full shell set) and BOSS (M3b shells) with the firmed
full covariance + Hartlap/Percival + IC + fuller randoms. Re-assess, under PROPER errors:
- (a) per-shell feature significance (does the detection survive bin-bin covariance? global
  trials-corrected p recomputed with the full C);
- (b) the same-z tracer split (LRG vs QSO at z~1.02) — real under proper C, or covariance
  noise? THIS is the load-bearing re-test (the C2 caveat);
- (c) the frozen ell=58.34 threading / any stable scale, DESI and BOSS, under proper C;
- (d) the DESI-vs-BOSS coherence comparison, matched-rigor.
Pipeline otherwise = the M3 frozen machinery (LS, bump search full-window no-seeding,
look-elsewhere) with covariance swapped in. mu is NOT invoked here (M3c is a DATA-rigor step,
pure observation-space; the mu-on-default ruling governs the THEORY lane, not this measurement).

## 4. Outcomes (all first-class, equal temperature)

- **M3c-SURVIVES:** features + tracer-split survive proper covariance -> the phenomenon firms;
  the coupling forward-lead keeps its empirical hook.
- **M3c-DEFLATES:** features/split weaken markedly under proper covariance -> they were
  substantially covariance/S-N artifacts; the C2 caveat is vindicated; M3/M3b significances
  get a point-of-use downgrade (banked results AMENDED, not deleted — honest correction).
- **M3c-MIXED / M3c-OBSTRUCTED(component/budget):** partial; disclosed.

## 5. Process

Phase 3 build+rerun: one build agent (covariance machinery from banked counts first = the cheap
core; then recount/full-randoms if budget), synchronous foreground bounded runs, NO monitors,
GPU workhorse + amended-v2 spot-check, checkpointed. Phase 5: blind results-verifier (re-run the
covariance from banked counts; audit F-STEER neutrality; confirm no mock/fiducial leak). Then
HOLD for Charles — nothing banks/amends M3/M3b until he reviews. Verified-LEAD ceiling.
