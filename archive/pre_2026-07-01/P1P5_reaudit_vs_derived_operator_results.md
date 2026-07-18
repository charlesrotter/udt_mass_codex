> **SUPERSEDED / CONDITIONS-CHANGED (2026-07-06 supersession sweep) — NOT a native-micro UDT result; mine for history.**
> Rode the PRE-NATIVE scalar-tensor 'derived operator' (e^{2φ}R + X e^{2φ}(dφ)², a=e^{+φ}), superseded 2026-07-01 by the native
> constrained-two-player operator (EH-empty, φ-blind matter, geometric 𝒦). Already premise-tagged in this sweep. UNVERIFIED auditor
> triage (self-labeled NOT canon); its whole reference operator is superseded; forwarded box-control/must-quantize inherit the S³-object
> CONDITIONS-CHANGED scope; re-run against the native operator before use.

# P1–P5 RE-AUDIT vs the Newly-Derived Operator — did the recent work affect any P-result?

**Mode:** READ-ONLY infrastructure audit (no solves, no edits). **Driver:** Claude Opus 4.8 (1M),
agent for udt_mass_codex. **Date:** 2026-06-21. **NOT canon. Record-candidate** (no blind verifier
pass yet — this is an audit re-grade, not a new physics result).

**Question (Charles):** DID THE RECENT WORK AFFECT ANY OF THE P1–P5 RESULTS? Answered result-by-result,
from the primary docs (not summaries), classifying impact + naming the specific new-operator doc that
re-established or changed each.

**The foundation change this session (the cause of the re-grade):**
- gravity = two-player scalar-tensor `S = INT sqrt(-g)[e^{2phi}R + X e^{2phi}(dphi)^2]`, phi independent
  => **vacuum != GR** (box f survives). (`native_dilation_weight_derivation_results.md`)
- matter coupling **a(phi) = e^{+phi}** (NOT -1), now PHYSICAL/non-absorbable; new exterior = scalar-tensor
  hair, B=1/A breaks once hair is live. (`matter_regrade_derived_operator_results.md`)
- the full operator built EXACTLY (no hybrid needed). (`P5e_proper_results.md`,
  `static_soliton_rerun_derived_operator_results.md`, `STEP2_timelive_matter_results.md`)
- "no privileged depth" IS a (anisotropic) scale symmetry; box-control = its fingerprint.
  (`scale_symmetry_bootstrap_analysis_results.md`)

Classifications used:
- **INTACT** — operator-agnostic MACHINERY (discretization/solver/re-pose/gate); survives unchanged.
- **SUPERSEDED-BUT-REESTABLISHED** — a physics verdict that used the old operator/a=-1 but was RE-RUN on
  the new operator this session and SURVIVES; old run superseded, conclusion stands.
- **CHANGED** — a result the new work genuinely changes.
- **UNCHECKED-GAP** — used the old operator, NOT re-checked on the new operator this session (the loud flag).

---

## PER-RESULT CLASSIFICATION TABLE

| P-result | Old-operator conclusion it recorded | Operator/assumption it USED | Class | New-operator doc that re-established / changed it |
|---|---|---|---|---|
| **P1 (off-diag wiring)** | Spatial off-diagonals wired to general Einstein; round recovers to floor; static matter sources no (r,ψ)/(θ,ψ) shear; e_rt a coarse-Nth response. | **POLE-STABLE HYBRID** general Einstein (small-shear approx); **a=-1**; B=1/A free; time zeroed. | **INTACT (machinery)** + one CHANGED sub-claim | Machinery (off-diag wiring, the general-Einstein residual structure) is operator-agnostic — `matter_regrade` §5 explicitly carries "solver MACHINERY". BUT the off-diag wiring was built ON the hybrid, which the EXACT operator (`P5e_proper`) now supersedes; and the **a=-1 baseline P1 ran is no longer the GR baseline** (a=e^{+phi}). The off-diag *wiring* survives; the *physics observation* (no shear from static matter) was re-confirmed only round/static, not on the scalar-tensor operator. |
| **P2 (native S² matter EL, 3-D, off-diag-aware)** | Matter EL is 3-D on the genuine UNIT S² carrier and varies on the FULL off-diagonal metric (FD-gate proven); L4==native cross-L4; deg-1 node; (r,θ) shear genuine, (r,ψ)/(θ,ψ) zero. | a=-1 frozen; hybrid metric; native S² carrier. | **INTACT (carrier+EL machinery) + SUPERSEDED-BUT-REESTABLISHED (native-ness)** | `matter_regrade` §5 CARRY list: **L2/L4 native-ness, S² carrier settlement, T^t_t=T^r_r inside matter, charge** all carry over (covariance/topology arguments, operator-independent — explicitly so). The EL machinery is a contained swap. The a=-1 the EL was weighted with is superseded (now e^{2phi}); the EL *structure* (autograd on full metric) is reused intact by `static_soliton_rerun` / `STEP2` / `P5e_proper`. |
| **P3 (a(phi) coupling)** | `G^mu_nu = (8πG/c⁴)e^{(a+1)phi}T`, **curvature side UNCHANGED, vacuum=GR**; **a=-1 = the GR baseline (absorbable)**; a!=-1 = a DECLARED, UNFORCED, NON-absorbable exploration knob. | **OLD OPERATOR EXPLICITLY**: EH curvature side, vacuum=GR, a=-1 absorbable by the EH Bianchi tautology. | **CHANGED (the biggest one)** | `matter_regrade_derived_operator_results.md` (§2–3, blind-verified): the EH Bianchi tautology that made a=-1 "absorbable -> UDT=GR on matter" is **DEAD** (`nabla E != 0`). **a(phi)=e^{+phi} is now DERIVED and PHYSICAL**, not an unforced knob; the curvature side is NOT GR. P3's entire premise ("vacuum=GR, a=-1 baseline, a!=-1 optional") is overturned. The *wiring machinery* (weight on action density -> stress+EL consistently) is reusable, but the value, status, and physical meaning all CHANGED. |
| **P3 FIX (ruler-integral weight)** | The running-a source weight should be the ruler integral `W=exp(INT(a+1)dphi)` (rate-law-unique), not the product form. | Same old-operator e^{(a+1)phi} arc. | **INTACT (derivation) / re-scoped value** | The ruler-integral derivation (a composition/rate-law identity) is operator-agnostic and stays correct as the right way to build a running-a weight. But it was built around the now-superseded "a under-determined, a=-1=GR admissible" framing; on the derived operator a(phi)=e^{+phi} is FORCED, so the running-a exploration it served is re-scoped with P3. |
| **P4 (time-live wiring + containment)** | Live time row wired into the P1–P3 stack; containment BITWISE (omega->0 == static P3 soliton); T_tr Birkhoff-escape anchor; round diagonal G^t_t Birkhoff-frozen. | hybrid Einstein; a=-1 (k=0, W=1); native S²; open time. | **INTACT (machinery) + SUPERSEDED static anchor** | The time-live WIRING (harmonic balance, T_tr-sources-G_tr, open-time containment logic) is operator-agnostic infrastructure. Its containment anchor was the **a=-1 static P3 soliton on the hybrid** — that anchor is superseded by the new static soliton (`static_soliton_rerun`). The genuinely-coupled, EXACT-operator version of P4's job is `STEP2`/`P5e_proper`, which re-establish the same containment + Birkhoff-escape structure on the derived operator. |
| **P5a (JFNK + physics PC)** | FAILS the gates; root cause = J^TJ rank-deficiency (~22% nullspace) from the body-mask edge-excision; triggers re-pose/KEH. | committed residual (old operator), as a pure SOLVER de-risk. | **INTACT (machinery / pure numerics)** | Operator-agnostic. The rank-deficiency diagnosis and PC failure are properties of the discretization, not the curvature operator. `matter_regrade` §5 carries "JFNK/dense-LM" machinery. Unaffected. |
| **P5a' (re-pose to full-rank + JFNK rescue)** | Re-pose makes J full-rank; JFNK rescued; beats #60 stall. ALSO exposed: committed residual's zero set is a SOLUTION MANIFOLD (angular Einstein under-determined). | committed residual (old operator), pure solver. | **INTACT (machinery)** — but the manifold finding is operator-independent and STILL OPEN | The re-pose + JFNK rescue are pure numerics, operator-agnostic (carried in `matter_regrade` §5). The exposed solution-manifold / angular-Einstein under-determination is a discretization property that does NOT depend on the operator and remains an open solver issue carried forward (NOT closed by the new operator). |
| **P5b (light PC -> floor + PC-independence)** | PC->floor PASS at Nr=12; PC-INDEPENDENCE FAIL at Nr=12 (9.3% M_MS spread, near-null edge manifold); collapse-at-Nr>=16 throughput-limited/OPEN. | committed residual (old operator), pure solver. | **INTACT (machinery)** — open numeric thread unchanged | Operator-agnostic numerics. The PC-independence / manifold-collapse question is a discretization issue independent of the operator; still open, unaffected by the operator change. |
| **P5c (basins + stability / family question)** | Five same-charge basins at Nr=12; round = dominant lowest-energy locally-stable attractor; off-round = shallow metastable side-wells melting to round. NOT a flat family. | OLD operator (full3d_newton, a=-1, hybrid); fixed-metric + coupled probes. | **UNCHECKED-GAP (physics) + INTACT (method)** | The constraint-respecting stability METHOD is operator-agnostic. BUT the basins, their energies (|S|, M_MS), the melt hierarchy, and the "round-dominant, others metastable" family verdict were ALL computed on the **old operator (a=-1, hybrid Einstein)** and were **NOT re-run on the derived operator** this session. The new static soliton (`static_soliton_rerun`) re-derives the single round object's structure, but the **multi-basin / family landscape was not re-mapped on vacuum!=GR + a=e^{phi}**. FLAG. |
| **P5d (round time-live OBSERVE)** | Round time-live channel = classical CONTINUUM; inertia M = machine floor (Birkhoff); only live channel = first-order G^t_r; box-controlled K~1/R². | hybrid Einstein; a=-1 (W=1); native S²; round channel. | **SUPERSEDED-BUT-REESTABLISHED** | `STEP2_timelive_matter_results.md` + `P5e_proper_results.md` re-run the time-live solve on the DERIVED operator with PHYSICAL matter and reproduce the box-control/continuum verdict — `STEP2` blind-verifier: "the last classical redoubt is CLOSED, reproducing #65 on the corrected foundation". P5d's round-channel continuum conclusion STANDS; its old-operator run is superseded by STEP2/P5e_proper. |
| **off-round classical discreteness gate (P5e)** | Off-round l>=2 channel carries a REAL classical oscillator (M!=0) but its low spectrum is a CELL-set continuum (omega~1/R); classical discreteness = NO. | full clean stack (P4 hybrid + a=-1 ruler k=0); fixed off-round background, l=2. | **SUPERSEDED-BUT-REESTABLISHED** | `P5e_proper_results.md` (the genuinely fully-coupled, multi-harmonic, free-omega, finite-amplitude, full off-diagonal time-row solve on the DERIVED operator) + `STEP2` reproduce box-control WITHOUT the old shortcuts. P5e_proper verifier: "must-quantize survives the audit ... on the full coupled machinery." The fixed-background off-round box-control conclusion STANDS; superseded by the coupled exact-operator re-run. (Throughput caveat: P5e_proper's clean cell window is R in [8,12]; STEP2's linear gate spans R=4..64 and is verifier-graded AIRTIGHT on R-scaling.) |

---

## (i) IMPORTS in P1–P5 still standing

- **The winding/charge boundary condition (the #61 sector index).** P1/P2/P3 use the deg-1 NODE core
  (Theta(core)=pi, sin=0), explicitly NOT the forbidden m*pi twist ladder (grep-verified in each P-doc).
  `matter_regrade` §5 CARRY list keeps "the winding-BC import verdict (#61)" as **operator-independent**
  (a provenance fact about the catalog's sector index). So this import is UNTOUCHED by the operator change —
  it remains a standing import to be retired separately, not re-graded by this session. The seal/charge
  BC is independently re-examined on the NEW foundation in `seal_junction_condition_results.md`
  (both involutions give a CONTINUOUS seal BC — no classical quantizer), consistent with box-control.
- **The core cutoff rc=0.05 (the #61 scar).** Inherited by P1/P4/P5d as a scoped freeze ("P6 retires it").
  Operator-independent; still standing.
- **xi, kappa (the scale-breaker l=sqrt(kappa/xi) value) and the p-selector.** `matter_regrade` §6: "NOT
  TOUCHED by this re-grade (remain open)." Still chosen, not derived; unchanged by the operator.

## (ii) FROZEN items / APPROXIMATIONS the new work exposes or removes

- **The POLE-STABLE HYBRID (small-shear approximation) is now SUPERSEDED by the EXACT full operator.**
  P1, P4, P5d ALL ran on the hybrid (Weyl backbone + bracket delta), valid only for small shear
  (A <~ 0.1; P2 explicitly flagged T^r_th=3.47 would push e_rt "outside the P1 hybrid's small-shear
  validity"). This session built the FULL operator EXACTLY with no hybrid:
  `P5e_proper` ("built in 3.3s ... no hybrid needed; the full variational EL"), `static_soliton_rerun`,
  `STEP2`. **Status:** the hybrid is removed for the time-live/coupled physics verdicts (those are now
  on the exact operator). It is NOT yet removed for: P1's spatial-off-diagonal observation, P5a/a'/b's
  solver-rank work (those used the committed hybrid residual). Those conclusions still RELY on the
  hybrid's validity in the regime they ran (small shear / round / linear-level), which is the regime the
  hybrid is valid in — so they are not invalidated, but they are NOT yet re-confirmed on the exact operator.
- **a=-1 weight (=1) is REMOVED as the physical value.** Frozen in P1/P2/P4/P5d as "GR baseline"; the
  derived weight is e^{2phi} (a=e^{+phi}). This is the CHANGED item, not just a freeze lifted: a=-1 is no
  longer the baseline, it is simply wrong for the derived operator. (`matter_regrade` §2.1: the teeth come
  from the OPERATOR, not from a=+1 vs -1 — but the value is nonetheless now fixed, not free.)
- **"vacuum = GR / classical metric is a continuum, period" is RE-OPENED then RE-CLOSED differently.**
  The old headline rested on EH-frozen vacuum. New work: vacuum != GR (box f survives), so the classical
  metric does MORE (a structural door). BUT the discreteness question still closes the same way:
  `STEP2`/`P5e_proper` show the genuinely-coupled derived operator STILL box-controls => "discreteness
  still requires quantization" SURVIVES on the corrected foundation (now demonstrated, not assumed).

## (iii) S²-vs-S³ settlement and the new operator

- The S²-vs-S³ carrier settlement (S² unit 3-vector is the genuine native carrier; S³ 4th component was
  the #61 import) is an **action-target / covariance argument**, NOT a curvature-operator argument.
  `matter_regrade` §5 carries it explicitly as operator-independent ("the action terms are unchanged").
  **The new operator does NOT touch the S²-vs-S³ settlement** — it remains INTACT. (F2's matter-action
  forced-ness audit, also this session, works entirely on the S² carrier and likewise does not depend on
  the gravity operator.)

---

## BOTTOM LINE — SURVIVE / CHANGED / GAP split

**SURVIVE (INTACT machinery — operator-agnostic, unchanged):**
- P1 off-diagonal general-Einstein WIRING (the residual structure)
- P2 native S² UNIT carrier + full-metric autograd EL MACHINERY; L2/L4 native-ness; S²-vs-S³ settlement;
  charge / N=3 / q=1/3 read-off; T^t_t=T^r_r inside matter
- P4 time-live wiring (harmonic balance, T_tr->G_tr Birkhoff-escape logic, open-time containment)
- P5a (JFNK PC failure + rank-deficiency diagnosis), P5a' (re-pose/JFNK rescue + manifold finding),
  P5b (light-PC->floor + PC-independence thread) — all pure numerics, fully operator-agnostic
- The P3-FIX ruler-integral derivation (a composition/rate-law identity)

**SUPERSEDED-BUT-REESTABLISHED (old run dropped, conclusion re-confirmed on the derived operator):**
- **P5d** (round time-live = classical continuum) — re-established by `STEP2` + `P5e_proper`
- **off-round classical discreteness gate** (box-controlled, no classical tower) — re-established by
  `P5e_proper` (fully-coupled exact operator) + `STEP2` (verifier-graded airtight on R-scaling)
- The "discreteness requires quantization" headline these supported — SURVIVES on vacuum!=GR + physical matter

**CHANGED (genuinely overturned/revised by the new work):**
- **P3** — the largest change. "vacuum=GR, a=-1 absorbable baseline, a!=-1 unforced knob" is OVERTURNED
  by `matter_regrade`: a(phi)=e^{+phi} is DERIVED and PHYSICAL, the absorbability tautology is dead,
  the curvature side is not GR.
- **The soliton EXTERIOR** (P2/P3-era global-monopole + Schwarzschild, B=1/A exact) -> scalar-tensor
  {m,q} hair, B=1/A breaks once hair is live. (`matter_regrade` §4, `static_soliton_rerun` confirmed:
  GR + a TINY 1/r hair at healthy X; B=1/A break dominated by an operator-INDEPENDENT matter-kinetic term.)
- **Every M_MS mass NUMBER read at a=-1 + hybrid** (P0/P1 0.29; P2/P3 122.98; P5c basin energies) -> needs
  re-run on the derived operator. `matter_regrade` §5 RE-SCOPED list: "every mass number read at a=-1+EH
  (needs re-run)." (Data-blind: the numbers were never banked as physics.)
- **The hybrid small-shear approximation** -> superseded by the exact full operator for coupled/time-live
  physics (built in 3.3s, no hybrid).

**UNCHECKED-GAP (used old operator, NOT re-checked on the new operator — the loud flags):**
1. **P5c basins + family/stability landscape (the most important gap).** The five-basin map, their
   energies, the melt hierarchy, and the "round-dominant, off-round = shallow metastable side-wells, NOT a
   flat family" verdict were computed on the OLD operator (a=-1, hybrid). They were NOT re-run on
   vacuum!=GR + a=e^{+phi}. The single round object's static structure was re-derived (`static_soliton_rerun`),
   but the LANDSCAPE of distinct same-charge solutions and their relative stability was not. Charles's
   standing "family question" answer (no flat family) rests on an un-re-graded old-operator landscape.
2. **P1's spatial off-diagonal SHEAR observation on the exact operator.** P1/P2 found static matter sources
   no (r,ψ)/(θ,ψ) shear and a genuine (r,θ) shear — on the hybrid + a=-1. The scalar-tensor operator adds
   live phi-hair terms to E^t_t - E^r_r (the t/r collapse breaks); whether the off-diagonal SHEAR pattern is
   unchanged on the exact operator with physical matter was not re-checked (time-live H was re-checked by
   STEP2/P5e_proper; the static SPATIAL off-diagonals were not).
3. **The P5a'/P5b solution-MANIFOLD / angular-Einstein under-determination on the exact operator.** This is an
   operator-independent discretization issue (so it carries), but it was diagnosed on the committed hybrid
   residual and its resolution (does the manifold collapse at Nr>=16?) remains OPEN and was not advanced or
   re-checked against the exact-operator residual this session.

**One-line answer to Charles:** Yes — the recent work AFFECTED P-results, but cleanly and mostly upward.
The SOLVER MACHINERY (P1 wiring, P2 carrier/EL, P4 time-wiring, P5a/a'/b numerics) is INTACT. The
core discreteness verdicts (P5d round-continuum, off-round box-control => must-quantize) are
SUPERSEDED-BUT-REESTABLISHED on the derived operator (STEP2 + P5e_proper). The genuine CHANGES are
P3 (a=-1->a=e^{+phi}, vacuum!=GR, absorbability dead), the soliton exterior (->scalar-tensor hair),
and every old-operator M_MS number (needs re-run). The standing UNCHECKED-GAP that most deserves a
re-grade is **P5c's multi-basin family/stability landscape**, never re-run on vacuum!=GR + physical matter.

---

**STATUS: UNVERIFIED auditor triage (read-only classification, not a physics result). The actionable finding — P5c is an un-re-graded gap — is the load-bearing item; a verifier pass on this audit's COMPLETENESS (did it miss any un-re-graded P-result?) is warranted before the gap list is treated as exhaustive.**

---

## B0 COMPLETENESS-CHECK CORRECTION (2026-06-21, agent a488bcabf7fcde972) — one hidden gap found
The triple-check found ONE mis-classification: the **OFF-ROUND l>=2 classical-discreteness gate**
(offround_classical_discreteness_results.md) was labeled SUPERSEDED-BUT-REESTABLISHED, but P5e_proper/STEP2
re-ran only the ROUND object's breathing spectrum on the derived operator — the off-round angular-warp oscillator
(M!=0, the distinct geometry the gate actually tested, partly built on the un-re-graded P5c off-round basins) was
NEVER solved on vacuum!=GR + a=e^phi. RE-CLASSIFY it as UNCHECKED-GAP #4 (it also rode the pole-stable HYBRID in
the off-round/non-small-shear regime = a hybrid-validity concern). The three named gaps + imports list were
otherwise CONFIRMED complete. *** CONSOLIDATION: gap #1 (P5c angular basins), gap #4 (off-round discreteness gate),
the F8 non-spherical residual, and B1's radial-only scope ALL reduce to ONE gap = the OFF-ROUND / NON-SPHERICAL /
ANGULAR sector has never been run on the DERIVED operator. Closing it = port the derived operator into the full3d
3-D off-round solver (a BUILD). This is the key remaining solver-completeness gap — and where the phi-angular
hunch lives. ***
