# PRE-REGISTRATION (frozen): the SIGN of the deep-phi intrinsic fluctuation mode (exact native coefficient)

STATUS: pre-registration, committed BEFORE the run. Derivation track, LOCAL branch
session-2026-06-17 ONLY. NOT canon. Frozen; no retuning.

PROVENANCE: with_L4_fluctuation_results.md + verifier ae590d8c found that the DEEP-phi matter
fluctuation has an INTRINSIC (non-box, R-independent-magnitude) lowest mode -- the first escape of
the box-control wall, in the phi-angular sector -- but with omega^2 < 0 (unstable), and flagged the
sign as hinging on the "#51 S^2-vs-S^3 well coefficient." RECON (Explore, 2026-06-18) RESOLVED #51:
the corpus is INTERNALLY CONSISTENT -- S^2 unit 3-vector target throughout; the factor-2 angular
coefficient is the NATIVE S^2 winding-current/Skyrme-form coefficient (L4 == |omega_H1 current|^2 on
|n|=1, verified ~6e-14 via the stress tensor p_r+rho>=0). So the well coefficient is FIXED, not
ambiguous. => the deep-phi mode's SIGN is now a DETERMINATE computation with the exact coefficient.

CAVEAT (load-bearing, do NOT conflate): p_r+rho>=0 is a BACKGROUND energy-condition fact; it does
NOT guarantee the FLUCTUATION spectrum's lowest eigenvalue is positive. The sign MUST be computed
from the fluctuation operator with the exact native coefficient -- it is genuinely open.

GOAL-CORRECT: emergent quantization. omega^2>0 = a stable intrinsic discrete observable (quantum
face); omega^2<0 = a genuine deep-texture instability (different, important). NOT a mass hunt.

SAFEGUARDS (Charles, binding; this machine lacks the workstation auto-audit):
S1. EXACT NATIVE COEFFICIENT -- derive the second-variation operator from the VERIFIED native action
    E2_r + E4_r (native_stabilizer_results.md:87-92; L2 = -(xi/2)g^{mn}d n.d n, the exact L4), with
    the |n|=1 constraint MANIFEST. NO representative/approximate coefficient (that was the prior
    runs' weak point). State xi, kappa provenance; if a ratio kappa/xi is needed, take it from the
    corpus soliton (cite), tag chose/derived.
S2. REAL stabilized profile Theta(r) from the actual L2+L4 EOM (finite size, E0~45.6). No ansatz.
S3. exact second variation (legitimate); L4 -> 4th-order operator -> the BCs are load-bearing; state
    each, tag, test sensitivity.
S4. DEEP-phi, HIGH PRECISION -- mpmath log-grid (x=ln r) at dps>=50 (the method that beats the
    e^{phi}-span conditioning float64 cannot); convergence-check (>=3 grid sizes); causal toggle
    (phi-angular well ON vs OFF -> does box-control return?). Test >=2 depths (e.g. p=1 and deeper).
S5. GOLDSTONE separation -- identify + remove translation (x3), rotation, iso-rotation/chi, AND the
    dilation/breathing zero mode; verify the lowest non-Goldstone mode is genuine. (At depth the
    translational Goldstone was the shallow l=1 lowest -- re-check at depth.)
S6. VERDICT-HUNTING GUARD -- omega^2>0 (the quantum-face prize) is the DESIRED answer; report the
    exact sign and value even if omega^2<0 (instability) or Goldstone. Absences first-class.
S7. INDEPENDENT BLIND VERIFIER after (re-derive operator + exact coefficient + re-run deep-phi mpmath
    + Goldstone re-check + sign).

## FROZEN MODEL

Native L2+L4 (S^2 unit 3-vector n, target S^2) on ds^2=-e^{-2phi}dt^2+e^{2phi}dr^2+r^2 dOmega^2.
Background = degree-1 stabilized hedgehog Theta(r). Fluctuation = tangent eta (|n|=1 preserved).
Operator = exact second variation of E2_r+E4_r. Exact action forms cited from native_stabilizer_results.md.

## PRE-REGISTERED QUESTIONS + OUTCOMES (no retuning)

D1 -- OPERATOR: state the exact second-variation operator from E2_r+E4_r with the exact native
   coefficient and |n|=1 constraint. Confirm it reduces to the prior runs' operator up to the
   coefficient (and identify exactly where the prior runs used a representative coefficient).
D2 -- PROFILE: real stabilized Theta(r); report.
D3 -- THE SIGN (the deliverable): lowest NON-GOLDSTONE eigenvalue omega^2 in each sector (l=0,1,2),
   at >=2 depths, mpmath dps>=50, convergence-checked, with the causal toggle. Is the deep-phi
   intrinsic mode omega^2 > 0 (stable) or < 0 (unstable)? DEFINITIVE sign + value.
D4 -- INTRINSIC vs BOX re-confirm: at the exact coefficient, is the deep mode still INTRINSIC
   (R-independent magnitude; omega^2 R^2 grows) and the well-OFF case box-controlled? Confirm the
   verifier's finding survives the exact coefficient.
D5 -- INTERPRETATION: if omega^2>0 -> stable intrinsic discrete observable (quantum face); report its
   value/spacing + HONEST SCOPE vs #44 (not the lepton ladder). If omega^2<0 -> genuine deep-texture
   instability; characterize (which sector, onset depth) -- a real physical result.

## SUCCESS / FAILURE (frozen, all first-class)

- QUANTUM-FACE POSITIVE: lowest non-Goldstone omega^2 > 0, intrinsic, in the phi-angular sector at
  depth -> native discrete observable; the box-control wall is genuinely escaped with a STABLE mode.
- INSTABILITY: omega^2 < 0 with exact coefficient, non-Goldstone, intrinsic -> the deep texture is
  unstable in that sector (onset depth) -- important, possibly a constraint on the model.
- ARTIFACT/NULL: the "intrinsic mode" is a Goldstone, or vanishes / becomes box at the exact
  coefficient -> the verifier's lead does not survive; the shallow box-control negative extends.

## PREMISE LEDGER (frozen; chose/derived)

1. Exact native L2+L4 second-variation operator -- DERIVED.
2. kappa/xi ratio (if needed) -- from the corpus soliton; tag chose/derived + test sensitivity.
3. Stabilized Theta(r) -- DERIVED.
4. 4th-order BCs (core + seal) -- LOAD-BEARING; tag + sensitivity.
5. Goldstone subtraction -- DERIVED from symmetries.

LOAD-BEARING for the blind verifier: (a) the EXACT coefficient (vs the prior representative); (b)
the Goldstone separation at depth; (c) the mpmath conditioning at the deepest point.
