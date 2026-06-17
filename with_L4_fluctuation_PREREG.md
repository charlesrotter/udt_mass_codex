# PRE-REGISTRATION (frozen): the WITH-L4 (stabilized) matter fluctuation operator

STATUS: pre-registration, committed BEFORE the run. Derivation track, LOCAL branch
session-2026-06-17 ONLY. NOT canon. Frozen; no retuning after the run.

PROVENANCE: the matter-sector V exam (matter_sector_potential_results.md + verifier a29669db)
showed the L2-ONLY operator is box-controlled and its tachyon is a DROPPED-L4 (Derrick) artifact;
the WITH-L4 (Skyrme-stabilized) operator -- which gains a k^4 stiffness that CAN host an INTRINSIC
(non-box) bound mode the L2-only run is structurally blind to -- is the UNTESTED LIVE QUESTION.
This run does it WITH L4.

GOAL-CORRECT: emergent quantization (the quantum structure of the matter guiding wave). Intrinsic
discrete bound modes = "discrete observables" = a quantum face. NOT a mass hunt (LATER-15); honest
scope vs #44 enforced (F5).

SAFEGUARDS (Charles, binding -- this machine lacks the workstation auto-audit):
S1. Derive the WITH-L4 fluctuation operator (exact second variation of L2+L4 around the hedgehog)
    FROM SCRATCH; do NOT import. L4 must be INCLUDED (the whole point) -- no dropping the stabilizer.
S2. REAL background: solve the L2+L4-stabilized hedgehog profile from its actual EOM (finite size;
    cite + compare to the corpus soliton, E0~45.6, lepton_soliton_spectrum_results.md). No ansatz.
S3. The fluctuation operator is the exact second variation (legitimate, no approximation). The L4
    term makes it 4th-order in space -> MORE BCs needed; the BCs are LOAD-BEARING (conjecture A
    turned on BCs). Tag each chose/derived; test sensitivity.
S4. BOX-CONTROL TRAP-TEST (the crux): any discrete mode MUST be tested by varying the cell size R
    (>=4 values, factor >=10) -- INTRINSIC (R-independent / depth-controlled) vs BOX-CONTROLLED
    (~1/R^2). Box-control is a NEGATIVE.
S5. ZERO-MODE SAFEGUARD: identify + separate the Goldstone zero modes (translation, rotation,
    iso-rotation) from genuine bound modes. A zero mode is a symmetry, NOT a quantum feature.
S6. CONNECT TO #44: the radial (l=0) breathing spectrum is ALREADY KNOWN (O(1)-spaced, depth-flat,
    intrinsic; lepton_soliton_spectrum_results.md). RELATE to it (consistency); do NOT claim it as new.
S7. VERDICT-HUNTING GUARD: an intrinsic discrete spectrum is the DESIRED answer; report the exact
    structure even if box-controlled, only-Goldstone, or empty. Absences are first-class.
S8. INDEPENDENT BLIND VERIFIER after (re-derive operator + re-run trap-test + zero-mode check).

## FROZEN MODEL

Action: native L2 (S^2 sigma-model) + L4 (native four-derivative stabilizer) on the static UDT
metric ds^2=-e^{-2phi}dt^2+e^{2phi}dr^2+r^2 dOmega^2. Background = degree-1 stabilized hedgehog
Theta(r). Fluctuation eta = tangent perturbation (2 real = 1 complex on S^2 tangent plane), the
matter guiding wave. Exact forms cited from native_stabilizer_results.md,
angular_lagrangian_results.md, lepton_soliton_spectrum_results.md, whole_metric_full_solve_results.md.

## PRE-REGISTERED QUESTIONS + OUTCOMES (no retuning)

F1 -- OPERATOR: derive the exact L2+L4 second-variation operator for eta, full (radial + angular
   sectors), including the phi-angular potential V (sin^2Theta/r^2 + e^{-2phi}Theta'^2 + curvature),
   the U(1) tangent-bundle connection, and the L4 k^4 stiffness. State it exactly.
F2 -- PROFILE: solve the L2+L4 hedgehog Theta(r); report + compare to corpus.
F3 -- RADIAL (l=0): intrinsic discrete modes? Compare to the known breathing tower (#44) -- do
   they MATCH (consistency)? Run the S4 trap-test. (Expected: intrinsic, matching #44.)
F4 -- ANGULAR (l>=1) WITH V (the NEW question): does the phi-angular potential V produce DISTINCT
   intrinsic discrete modes in the angular sectors? Run the S4 trap-test (intrinsic vs box). Does
   the phi-angular coupling add discrete structure beyond breathing? Separate Goldstone (S5).
F5 -- EMERGENT-QUANTIZATION READING + HONEST SCOPE: are the intrinsic modes "discrete observables"
   of the matter guiding wave (a quantum face)? State scope vs #44 (NOT the lepton hierarchy;
   O(1) spacing). No inflation.

## SUCCESS / FAILURE (frozen, all first-class)

- POSITIVE: the full WITH-L4 operator has INTRINSIC (S4-passing, non-Goldstone) discrete modes,
  INCLUDING in the phi-angular (l>=1) sectors -> the matter guiding wave carries native discrete
  observables (a quantum face), consistent with the known breathing tower. (If the phi-angular V
  adds distinct intrinsic structure, that is the new content.)
- NEGATIVE: all non-Goldstone modes box-controlled, OR only the already-known breathing tower with
  the angular V adding nothing intrinsic, OR empty. A clean (premise-scoped) negative.
- PARTIAL: radial intrinsic (matches #44) but angular box-controlled / Goldstone-only.

## PREMISE LEDGER (frozen; chose/derived)

1. L2+L4 second-variation operator = the matter guiding-wave operator -- DERIVED.
2. Stabilized hedgehog Theta(r) -- DERIVED (solved here).
3. 4th-order BCs (core regularity + finite-cell/seal) -- LOAD-BEARING; tag + test sensitivity (S3).
4. Angular harmonic sector / eigenvalue -- scan low l.
5. Zero-mode subtraction -- DERIVED (Goldstone count from the symmetries).

LOAD-BEARING PREMISE flagged for the blind verifier: the 4th-order BCs (premise 3) and the
intrinsic-vs-box diagnosis in the angular sector (F4) -- plus the Goldstone separation (did any
"bound mode" turn out to be a zero mode?).
