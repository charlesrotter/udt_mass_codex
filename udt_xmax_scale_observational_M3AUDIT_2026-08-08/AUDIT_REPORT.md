# M3-AUDIT — selection-function forensics on the BAO notables (INCREMENTAL)

Contract: `PREREGISTRATION.md` (commit 2d9933d1). Machinery: M2 `v_bao.py` under the
sanctioned `authorize_m3("523f4aca")` mechanism — this work is part of M3-AUDIT under
2d9933d1; both commits are noted in every output. Date 2026-08-08. FORENSICS ONLY:
**F-FIX** — nothing here corrects, reweights, or replaces any banked M3 number; all
recomputed w(θ)/bump values below are diagnostic evidence for GRADES.

## Method notes (honest deviations + audit-level conventions, tagged CHOSE)

- **Checkpoint-reuse limit (disclosed):** the M3 checkpoints persisted only
  region-SUMMED counts (40-bin vectors), not the region-blocked matrices. B2 therefore
  required bounded fresh recomputes of the blocked counts (piecewise, cached in
  `audit_data/blocks/`, staged). The same blocks serve B4: in the frozen cap-combine
  estimator the caps are exactly block-diagonal (no cross-cap pairs), so per-cap LS is
  a restriction of the frozen estimator, not a re-choice. Consistency check: the
  reassembled full-shell w(θ) is compared to the M3 checkpoint per target (reported).
- Frozen settings reused as-is: θ ∈ [0.3°, 12°], 40 log bins, 24 regions/cap,
  weights WEIGHT_COMP×WEIGHT_ZFAIL×WEIGHT_SYS, 4-file split-averaged RR, cap-combine
  union jackknife, LS, cubic-null + Gaussian bump machinery with refine.
- **Flag thresholds (CHOSE, audit-level, stated before grading; raw numbers always
  given so a re-grader can re-threshold):** log-bin width factor = 1.0957 (Δlnθ 0.0914).
  B1 flag: shell edge slope |d ln n/dz| ≥ 2× the tracer median AND a named selection
  landmark inside/adjacent to the shell. B2 flag: any single drop-one region moves
  θ_b by > 1 bin or collapses Δχ² below the shell's null 95th (single-region-driven).
  B3 flag: bump absent in one z-half (θ_b off > 2 bins or Δχ² < null-95th in one half
  while strong in the other = edge-tracking). B4 flag: bump absent/displaced > 2 bins
  in one cap (caveat: single-cap S/N is lower; SGC is the shallower cap). B5 flag:
  θ_b moves > 1% or A_b > 10% with WEIGHT_ZFAIL dropped (mirrors the M3 sys/nosys
  robustness standard). Grade per contract: SELECTION-SUSPECT = ≥2 flags consistent
  with a NAMED selection layer; SKY-ROBUST = clean across the battery; else
  INCONCLUSIVE.

## B1 — dN/dz edge structure (all 9 targets; catalog-level; `audit_data/b1_dndz.npz`,
`b1_summary.json`)

Tracer-wide median |d ln n/dz| (fine bins, weighted, caps combined): LRG 3.52,
QSO 1.58. Landmarks measured from the catalogs' own dN/dz: LRG peak z≈0.80; LRG
half-peak crossing z≈0.973 (the LRG selection-edge thinning: n falls 0.76→0.58→0.36→
0.24→0.15 of peak at z = 0.90/0.95/1.00/1.05/1.095); hard catalog boundary z=1.10.
QSO peak z≈1.58, smooth decline after (n/n_peak = 0.89 at 1.85, 0.78 at 2.00); no
landmark near 1.85–2.00.

| target | edge slopes (lo,hi) | in-shell slope | edge ratio hi/lo | tilt z̄ | B1 verdict |
|---|---|---|---|---|---|
| LRG 0.95–1.00 (8.8° outlier) | −5.8, −8.9 | −9.4 | 0.66 | −0.078 | **FLAG**: half-peak crossing z≈0.973 INSIDE the shell; slopes 1.6–2.5× median; NGC hi-edge steeper than SGC (−9.7 vs −7.3) |
| LRG 1.05–1.10 (1.17° outlier) | −11.0, n/a (catalog cut) | −10.6 | 0.63 | −0.088 | **FLAG**: abuts the hard z=1.10 catalog boundary at ~15% of peak density; steepest slopes (3× median); NGC/SGC asymmetric (−13.0 vs −7.2) |
| QSO 1.85–2.00 (0.71° outlier) | −3.2, −2.3 | −0.8 | 0.90 | −0.020 | ~2× median slope but smooth region, no landmark; SGC nearly flat vs NGC −4: mild cap asymmetry — **no flag** |
| LRG 1.00–1.05 (thread ctrl) | −8.9, −11.0 | −9.0 | 0.68 | −0.074 | **FLAG (symmetry)**: equally steep as the outlier shells, same thinning layer — steep dN/dz alone does NOT discriminate outlier from thread |
| LRG 0.70–0.75 (thread) | +0.1, +1.5 | +2.5 | 1.12 | +0.021 | near the LRG peak; mild — no flag |
| LRG 0.90–0.95 (thread) | −2.1, −5.8 | −5.2 | 0.78 | −0.044 | entering the thinning (hi edge 1.6× median) — marginal, no flag alone |
| QSO 0.95–1.10 (thread) | −1.2, +1.1 | +1.5 | 1.20 | +0.036 | mild — no flag |
| QSO 1.10–1.25 (thread) | +1.1, +0.0 | +1.3 | 1.22 | +0.032 | mild — no flag |
| LRG 0.75–0.80 (fitter-level) | +1.5, −0.1 | +3.9 | 1.18 | +0.032 | straddles the LRG peak (curvature max) — noted for B6 context |

B1 alone convicts no shell (it is one flag at most); it names the layer for the two
LRG outliers (selection-edge thinning; hard z=1.10 boundary) AND shows the thread
control shares the layer — carried to the synthesis.

## B6 — LRG 0.75–0.80 constrained refit (from the M3 checkpoint w/σ; `audit_data/b6_constrained.json`)

Frozen bump machinery with the refine step's center clipped to the frozen window
[0.3°, 12°] (the grid stage is in-window by construction; only the unbounded
Nelder–Mead refine could leave — and did, in the banked run). Both variants:

- Grid-stage best center = 11.46° = the LAST θ bin (window top). Unconstrained refine
  ran to 70.7° (sys) / 71.1° (nosys) with σ_b pinned at the 1.5 cap and A_b ≈ −0.85 —
  the classic signature of a broad Gaussian tail absorbing a large-θ boundary trend.
- Constrained refit: center RAILS at 12.0° exactly, Δχ² = 9.77 (sys) / 8.75 (nosys),
  A_b ≈ −0.028 — below the shell's own null-mock 95th (≈10.9): NOT a trigger even
  before look-elsewhere.

**B6 verdict: the nominal 70.7° center is a fitter window-edge artifact — there is no
interior bump in this shell; the "bump" term is absorbing a monotone trend at the top
of the window.** (Report-only; the banked M3 record — already flagged non-load-bearing
— stands untouched. F-FIX honored.)

## Drift-direction note (B1 × thread synthesis; `audit_data/drift_note.json`)

Question (contract §2): could selection gradients tilt bump centers coherently
opposite the predicted gentle fall (the verifier's ~1–1.5-bin tension)? Channel
tested: a dN/dz gradient pulls the shell's effective z̄ off the midpoint, so the
"shell-center" θ is really θ(z̄). Measured: |z̄ − z_mid| ≤ 0.0027 across all nine
targets (worst: QSO 0.95–1.10). Propagated through the SNe-fitted P1 reference
curve (n = 1.06 — context curve of the stated consistency observation, not a fit),
the implied θ-center shifts are **|Δ| ≤ 0.010 log-bins**, against a predicted
inter-shell fall of −0.40 bins (z 0.925→1.025) and −1.07 bins (0.725→0.925) and an
observed ~1–1.5-bin opposite drift. Signs are incoherent across the thread (both ±).
**Verdict: the dN/dz-edge z̄-tilt channel is quantitatively dead — two orders of
magnitude too small and not sign-coherent; the drift-direction tension is NOT
explained by this selection layer.** (Scope honesty: this tests the shell-center
displacement channel only; a z-dependent clustering-amplitude mix inside a shell is
a different channel and is probed indirectly by B3's z-halves.)

## Reproduction check (validates the audit block path)

For every one of the 9 targets, the reassembled full-shell w(θ)/σ from the audit's
fresh region-blocked counts matches the M3 checkpoint **bit-identically**
(max |Δw| = 0.0, max |Δσ| = 0.0, all 40 bins). The audit blocks are exact
decompositions of the banked counts. (`audit_data/b2b4_*.json`, field `repro_check`.)

## B2 — drop-one-region θ_b stability (union 48 regions, frozen bump refit per
leave-one-out curve, full-sample σ; `audit_data/b2b4_*.json`)

| target | max move (bins) | regions >1 bin | min Δχ² vs shell null-95th | verdict |
|---|---|---|---|---|
| LRG 0.95–1.00 (8.8°) | **31.1** | **13 of 48** | 15.6 vs 10.9 (stays sig.) | **FLAG**: position wildly region-dependent — a "feature" is always present but WHERE it is depends on which sky region is dropped |
| LRG 1.05–1.10 (1.17°) | 0.10 | 0 | 13.8 vs 10.9 | region-stable |
| QSO 1.85–2.00 (0.71°) | **23.0** | 2 | **8.9 vs 10.6 (de-triggers)** | **FLAG**: single-region-driven — dropping one region both moves the center 23 bins and kills the trigger |
| LRG 1.00–1.05 (ctrl) | 0.36 | 0 | 40.9 vs 10.5 | region-stable, strongly |
| LRG 0.70–0.75 | 0.55 | 0 | 11.1 vs 10.0 | region-stable (margin thin) |
| LRG 0.90–0.95 | 1.40 | 1 | 19.1 vs 11.2 | marginal single-region excursion, stays significant — no flag |
| QSO 0.95–1.10 | 0.29 | 0 | 14.8 vs 9.8 | region-stable |
| QSO 1.10–1.25 | 0.12 | 0 | **8.9 vs 10.4 (de-triggers)** | position stable but WEAK: drop-one can push below trigger — weakness note, not a selection flag |
| LRG 0.75–0.80 | 1.04 (of the 70.7° artifact) | 1 | 6.9 vs 10.3 (never a trigger) | consistent with B6: no real interior bump to stabilize |

## B4 — per-cap NGC vs SGC (restriction of the frozen estimator; per-cap 24-region
jackknife; global-max bump fit per cap — caveat: per-cap S/N is lower, SGC shallower)

| target | NGC θ_b (Δχ², A_b) | SGC θ_b (Δχ², A_b) | verdict |
|---|---|---|---|
| LRG 0.95–1.00 | 16.75° (13.5, −0.106) | 5.72° (6.5 n.s., −0.009) | **FLAG**: combined 8.8° is a compromise of a broad NGC large-θ dip and an insignificant SGC; no cap-consistent feature at 8.8° |
| LRG 1.05–1.10 | 1.20° (19.8, −0.019) | 2.84° (6.0 n.s., +0.010) | **FLAG (caveated)**: NGC-only; SGC insignificant, displaced, opposite sign |
| QSO 1.85–2.00 | 0.24° (7.3 n.s., +0.029) | 0.86° (10.8 marginal, −0.010) | **FLAG**: caps disagree in sign AND location; neither cap alone is significant at the combined center |
| LRG 1.00–1.05 (ctrl) | 2.54° (24.9, +0.014) | 2.37° (38.6, +0.017) | cap-CONSISTENT, independently significant in BOTH caps — the strongest sky-like signature in the battery |
| LRG 0.70–0.75 | 2.54° (13.0, +0.008) | 4.29° (5.6 n.s., −0.007) | NGC-dominant; SGC insignificant (low-S/N caveat) — soft note, no hard flag |
| LRG 0.90–0.95 | 2.48° (15.9, +0.008) | 0.10° (11.5, −0.473 at θ_min edge) | **FLAG (caveated)**: thread bump is NGC-driven; SGC's dominant feature is a θ_min-edge grab elsewhere |
| QSO 0.95–1.10 | 1.42° (17.8, −0.007) | 1.14° (3.2 n.s., −0.006) | NGC-dominant; SGC weak but same sign, near center — no hard flag |
| QSO 1.10–1.25 | 2.10° (5.1 n.s., +0.003) | 2.00° (6.0 n.s., +0.006) | cap-consistent centers/signs; each cap individually sub-threshold (weak but coherent) — no flag |
| LRG 0.75–0.80 | 6.08° (8.0 n.s., +0.37) | 6.0e5° (8.5 n.s., A~4e10 runaway) | fitter runaway in BOTH caps — corroborates B6 (window-edge/degenerate tail, no interior bump) |

## B3 — sub-shell z-split (fresh bounded half-shell counts, frozen pipeline per half;
`audit_data/b3_*.json`; caveat stated up front: each half has ~1/4 the pair counts, so
the GLOBAL-MAX bump search in a half can be noise-dominated when the full-shell
Δχ² ≲ 20 — for weak bumps B3 discriminates poorly and is graded accordingly)

| target | lo-half θ_b (Δχ²; bins from full) | hi-half θ_b (Δχ²; bins) | verdict |
|---|---|---|---|
| LRG 0.95–1.00 (8.8°) | 6.88° (26.2; 2.7b) | 12.21° (16.5; 3.5b) | **FLAG**: no common center — the large-θ dip's apparent scale slides with z inside the shell (6.9°→12.2°, window top), consistent with a broad survey-scale gradient, not a localized sky scale |
| LRG 1.05–1.10 (1.17°) | 3.51° (18.7; 11.9b) | 0.92° (13.2; 2.6b) | **FLAG (edge-tracking)**: the 1.17° feature is absent from the lo half's max entirely; the near-match sits in the hi half — the catalog-boundary side (z 1.075–1.10, density-collapse tail) |
| QSO 1.85–2.00 (0.71°) | 0.81° (11.9; 1.4b) | 0.55° (12.5; 2.8b) | borderline: present-ish both halves but center drifts 0.81°→0.55°; hi half > 2 bins — soft flag |
| LRG 1.00–1.05 (ctrl) | 2.25° (41.4; 0.9b) | 2.30° (16.1; 0.6b) | **PERSISTENT: same center in both halves, strongly significant** — sky-like |
| LRG 0.70–0.75 | 0.99° (7.7 n.s.; 9.5b) | 6.49° (18.2; 11.0b) | neither half's max at 2.37° — but full-shell Δχ² is only 14.7: S/N-limited, INCONCLUSIVE component (not scored as a selection flag) |
| LRG 0.90–0.95 | 6.51° (19.2; 11.1b) | 2.36° (43.8; 0.1b) | **asymmetric**: the 2.34° bump lives in the HI half (same center, Δχ² 43.8 > full-shell) and is absent from the lo half's max — z-localized toward the thinning side; caveated flag |
| QSO 0.95–1.10 | 2.77° (12.2; 7.4b) | 1.46° (10.4; 0.5b) | center persists in hi half; lo half grabs elsewhere weakly — mixed, S/N-limited, no hard flag |
| QSO 1.10–1.25 | 6.04° (10.6; 11.7b) | 10.79° (5.8 n.s.; 18.0b) | weakest thread bump (full Δχ² 11.1) vanishes in halves — S/N-limited, INCONCLUSIVE component |
| LRG 0.75–0.80 | 3.23° (10.9; 33.5b) | 8.55° (17.1; 22.9b) | no consistent feature anywhere — corroborates B6 (no interior bump) |

### B2 depth note (outliers)

- LRG 0.95–1.00: the 13 destabilizing regions span BOTH caps (9 NGC + 4 SGC), and the
  drop-one refit center ranges **0.50°–11.03°** — the 8.8° position is essentially
  unconstrained under region removal. Signature of a survey-wide gradient (many regions
  each carrying a piece of a broad trend), not one bad patch and not a localized sky scale.
- QSO 1.85–2.00: dropping NGC region 13 moves the center to 0.085° — the refine runs
  BELOW the 0.3° window floor (same unbounded-refine pathology class as B6) — and the
  minimum drop-one Δχ² (8.9) falls under the shell's null-95th (10.6): the trigger
  itself is single-region-fragile.

## B5 — WEIGHT_ZFAIL on/off (fresh bounded counts, zfail dropped on data AND randoms
— verified: WEIGHT_ZFAIL varies on both, 41–59% of rows ≠ 1; `audit_data/b5_*.json`)

| target | θ_b sys → nozfail | Δθ | ΔA_b | verdict |
|---|---|---|---|---|
| LRG 0.95–1.00 | 8.821 → 8.941 | **+1.37%** | +3.1% | **FLAG** (> the 1% bar the M3 sys/nosys standard set) |
| LRG 1.05–1.10 | 1.169 → 1.169 | +0.02% | −0.4% | clean |
| QSO 1.85–2.00 | 0.710 → 0.694 | **−2.27%** | +2.0% | **FLAG** |
| LRG 1.00–1.05 (ctrl) | 2.438 → 2.439 | +0.02% | −0.0% | clean |
| LRG 0.70–0.75 | 2.365 → 2.366 | +0.02% | +0.2% | clean |
| LRG 0.90–0.95 | 2.337 → 2.339 | +0.10% | −0.5% | clean |
| QSO 0.95–1.10 | 1.392 → 1.401 | +0.62% | −1.8% | clean |
| QSO 1.10–1.25 | 2.052 → 2.051 | −0.06% | +1.5% | clean |
| LRG 0.75–0.80 | 70.67 → 70.57 (artifact) | −0.14% | −0.3% | stable artifact (n/a) |

The only two zfail-sensitive positions are two of the three outliers; every thread
shell mirrors the M3 sys/nosys weight robustness. (Driver note, disclosed: the
background count driver was externally killed — harness task status "killed", no
Python exception in any log — after banking RR2 of the final cap-unit
(LRG 0.75–0.80 nozfail NGC); the unit was completed by a bounded foreground rerun
from the banked pieces (RR3 + assembly, 6.0 min). No data loss; B5 ran for all 9
targets. Separately: the unrelated stray process killed by the main session at
~13:30 shared no files with this audit; no anomalies observed in any audit log.)

## FINAL GRADES (contract §4; flags = positive evidence of selection structure;
power-limited tests contribute nothing either way; raw numbers above allow re-grading)

| target | B1 | B2 | B3 | B4 | B5 | GRADE |
|---|---|---|---|---|---|---|
| **LRG 0.95–1.00 (8.8°)** | FLAG | FLAG | FLAG | FLAG | FLAG | **SELECTION-SUSPECT (5/5)** — named layers: LRG selection-edge thinning (dN/dz half-peak crossing z≈0.973 inside the shell) + redshift-failure completeness (zfail-sensitive position). The 8.8° dip's position is region-unconstrained (0.5°–11°), cap-inconsistent, z-incoherent, and weight-sensitive: a survey-scale selection gradient signature, not a localized sky scale. |
| **LRG 1.05–1.10 (1.17°)** | FLAG | clean | FLAG | FLAG (cav.) | clean | **SELECTION-SUSPECT (3 flags)** — named layer: the hard z=1.10 catalog boundary + steepest selection-tail slopes (3× median, cap-asymmetric). Feature is NGC-only and tracks the boundary half. Honest minority evidence: region-stable within NGC and weight-robust — a sky reading is not excluded, but ≥2 flags align with the named boundary layer. |
| **QSO 1.85–2.00 (0.71°)** | note (cap-divergent dN/dz slopes) | FLAG | soft flag | FLAG | FLAG | **SELECTION-SUSPECT (3 hard flags)** — named layer (weakest naming of the three): cap-/region-dependent QSO selection depth (measured: NGC dN/dz declining −4 while SGC ~flat in-shell; caps disagree on the feature in sign AND location; one region kills the trigger; zfail-sensitive). Alternative reading recorded: a fragile noise-grab. Either way not sky-robust. |
| **LRG 1.00–1.05 (thread ctrl, 2.44°)** | note (shares steep layer) | clean (strongest) | PERSISTENT | cap-consistent, both sig. | clean | **SKY-ROBUST** — region-stable (0.36 bins), same center in both z-halves, independently significant in BOTH caps, weight-robust. Also the symmetry anchor: it sits on the SAME steep dN/dz layer as the outliers — steep selection alone does not manufacture flags. |
| LRG 0.70–0.75 (2.37°) | clean | clean (thin margin) | unpowered | soft note (SGC n.s.) | clean | **SKY-ROBUST** (caveats: B3 unpowered at this bump strength; B2 trigger margin thin) |
| LRG 0.90–0.95 (2.34°) | marginal (thinning onset) | clean-marginal | FLAG (cav.: hi-half-localized) | FLAG (cav.: SGC θ_min grab) | clean | **INCONCLUSIVE** — only caveated flags; cannot separate z-localized sky clustering (bump strengthens in the 0.925–0.95 half, same center) from thinning-onset selection; position itself is region/weight-stable |
| QSO 0.95–1.10 (1.39°) | clean | clean | mixed (unpowered lo) | no hard flag | clean | **SKY-ROBUST** (caveat: NGC-dominant; SGC same-sign near-center but n.s.) |
| QSO 1.10–1.25 (2.05°) | clean | stable but de-triggerable | unpowered | cap-consistent, each n.s. | clean | **INCONCLUSIVE** — battery underpowered at this feature strength; nothing selection-positive found; every powered position test consistent |
| LRG 0.75–0.80 (70.7°) | peak-straddle | never a trigger | no consistent feature | fitter runaway both caps | stable | **B6 verdict: CONFIRMED fitter window-edge artifact** — grid best = last bin; constrained refit rails at 12.0° below trigger; not a sky feature and no selection layer required |

### Synthesis + drift direction

The battery separates cleanly: the thread (2.3–2.4° LRG cells + QSO 0.95–1.10) is
region-stable, cap-consistent (where powered), z-persistent (where powered) and
weight-robust; the three off-thread outliers each accumulate ≥3 selection-consistent
flags. The audit therefore ATTACHES (annotation only, F-FIX): the M3 consistency
observation's outlier caveat is now graded — the 8.8° and 0.71° hits are
SELECTION-SUSPECT with named layers, 1.17° SELECTION-SUSPECT with minority sky
evidence. The thread drift-direction tension (opposite the predicted fall,
~1–1.5 bins) is NOT selection-explained by the measured dN/dz z̄-tilt channel
(≤0.01 bins, sign-incoherent — two orders too small) and the thread centers carry
no B2/B4/B5 instability that could tilt them coherently: the tension stands as a
property of the measurements, adjudication to M3b/radial (F-SCOPE: no physics
conclusion here).

### Falsifier discharge

- **F-FIX: DISCHARGED.** No corrected measurement, reweighting, or revised banked
  number exists anywhere in this audit; every recompute above is graded evidence;
  banked M3 results stand untouched; grades attach as provenance annotations.
- **F-STEER: DISCHARGED.** Identical battery on all 9 targets (tables above cover
  every cell); the thread control faced every test the outliers faced; one thread
  shell (LRG 0.90–0.95) was itself flagged-to-INCONCLUSIVE and two convenient cells
  were NOT acquitted to SKY-ROBUST — the audit convicted and declined to acquit on
  evidence, not convenience.
- **F-IMPORT-LCDM: INTACT.** Loader whitelist/blacklist untouched (all access via
  v_bao under authorize_m3(523f4aca)); no NX/WEIGHT_FKP/_rec anywhere; no fiducial
  cosmology; the only curve referenced (P1, n=1.06) is the SNe-fitted native profile
  used as stated context for the drift note, never fitted here.
- **F-SCOPE: honored** — grades + evidence only; no mechanism language.

Battery cost: 72 cap-block units fresh-counted (18 sys full-shell + 36 half-shell +
18 nozfail; ~9 CPU-hours, 4 workers), all pieces cached in
`audit_data/blocks/`; nothing truncated — full battery on all nine targets.
Audit agent: M3-AUDIT forensics agent (Fable), 2026-08-08. Blind adversarial review
of this audit: OWED (contract §6).

## CONSOLIDATED (2026-08-08, blind review in): AUDIT SUSTAINED-AMENDED — verified grades

`AUDIT_REVIEW.md`: every load-bearing number reproduced (B2 ranges, B5 shifts, drift note,
bit-identity reconfirmed independently on two targets); F-FIX/F-STEER discharged; the
driver-failure recovery legitimate. AMENDMENTS APPLIED (supersede the grade table above):
- **QSO 1.85–2.00 REGRADED: SELECTION-SUSPECT → INCONCLUSIVE (NOT-SKY-ROBUST).** The ≥2
  NAMED-layer contract standard was not met (one layer-specific flag only — B5 −2.27%; the B2/
  B4 signatures are noise-consistent; B1 found no landmark). The fragile-noise-grab alternative
  is co-equal. Downstream discount of the 0.71° hit unchanged.
- **LRG 1.05–1.10 evidence-prose corrected:** the B3 "hi-half near-match" is itself 2.64 bins
  off the full-shell center (over the audit's own threshold) — "tracks the boundary half" was
  interpretive; the valid flag is the ABSENT lo-half + the B1 hard-boundary layer. Grade
  unchanged (SELECTION-SUSPECT, 3 flags → the two solid ones carry it with B4 NGC-only).
- Reviewer strengthening recorded: the 8.8° shell's min drop-one Δχ² = 15.6 > null-95 — even
  there, SOMETHING real is present; it is the position/scale that selection scrambles beyond
  use. And the control-shell argument is UNDERSTATED if anything (the control's selection edges
  are steeper than the 8.8° shell's; zero flags anyway).

**FINAL GRADE TABLE (amended):** SELECTION-SUSPECT: LRG 0.95–1.00 (5/5), LRG 1.05–1.10 (3).
SKY-ROBUST: LRG 1.00–1.05 (control, strongest), LRG 0.70–0.75, QSO 0.95–1.10 (power-limited
caveats carried). INCONCLUSIVE: LRG 0.90–0.95, QSO 1.10–1.25, QSO 1.85–2.00 (regraded).
B6-ARTIFACT: LRG 0.75–0.80. Drift-direction tension: REAL (no selection channel explains it;
thread centers stable) → M3b / radial / origin work. Banked M3 results untouched; grades are
annotations. Four-check: preregistered (2d9933d1); bounded (full symmetric battery, no
truncation, one disclosed single-unit recovery); blind-reviewed; falsifiers discharged.
**Status: verified GRADES (same-session review; external bar travels).**
