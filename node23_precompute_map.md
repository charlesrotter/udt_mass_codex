# NODE 2/3 PRE-COMPUTE MAP — the route-2a stabilizer question (Fork-3b, ω≠0)

**Mode: MAP only — armchair/CAS/linearized-structure. NO full solve, NO nonlinear solve. DATA-BLIND
(no labels, no masses, no observational numbers). DERIVE stays gated.**
Author: driver (Opus), 2026-07-04, after NODE 1 banked (`node1_seal_spin_verdict_results.md`: the seal is
ω-blind; discreteness relocated to the interior). Q1–Q3 CAS-assembled by agent a0e17dcb5c6b55033 (sympy
scratchpad, all bracket signs + frame-drag operator CAS-checked); Q4/Q5 + forks = driver synthesis.

Preserved premises (Charles): universe=N=0 ground state; mass-emergence P-only; native S² carrier; N=3 +
1+3+5 + structural-i native, q/η targets; no lepton masses/labels/data. Flavor II primary (φ static, the
matter phase spins χ=Nψ+ωt); the seal is ω-blind (NODE 1); 3a demoted.

---

## Q1 — the native rotating junction / Noether-charge condition (seal now known vacuous)

The rotating cell adds exactly ONE new field: the stationary l=1 frame-drag `g_tψ = j(r) sin²θ`. Its
native BCs (derived, not posited):
- **j(0)=0** (regularity, l=1; j~r² leading) — DERIVED.
- **j(r_s)=0 (Dirichlet)** — from the counter-rotating mirror: g_tψ is odd under t→−t; the seal glues the
  cell to its ω→−ω image whose drag is j→−j, so continuity forces j(r_s)=0, with **j′(r_s) FREE = the
  angular-momentum / gravitomagnetic flux OUTPUT** — the exact structural analog of the depth flux seal
  q=Z_φρ²φ′. DERIVED (same NODE-1 logic; node05:55 gives the identical odd→Dirichlet for the off-diagonal).
- The frame-drag junction is **ω-permitting**: its source T_tψ ∝ sin²Θ(r) vanishes at BOTH folds
  (sin²Θ(0)=sin²π=0, sin²Θ(r_s)=sin²0=0), so angular momentum J=∫T_tψ is a pure BULK output; the seal
  constrains the response j, not ω.

**All static-sector BCs unchanged** (φ Dirichlet φ(r_s)=0 / q output; ρ′ Neumann; core even fold
φ′(0)=ρ′(0)=0; Θ(0)=π, Θ(r_s)=0). **VERDICT: no junction anywhere constrains ω** — consistent with NODE
1. Discreteness, if any, is interior (Q3/Q4).

## Q2 — the minimal coupled interior system (everything-on for this bounded ansatz)

Driving invariant (CAS-exact): `X = e^{−2φ}Θ′² + sin²Θ · B(r)`, with the **load-bearing bracket**
```
B(r) = N² g^{ψψ} + ω² g^{tt} + 2ωN g^{tψ}
     = +N²/(ρ²sin²θ)  −  ω² e^{2φ}/c²  +  2ωN·(j e^{2φ}/c²ρ²) .
```
- **Θ(r) EOM (L2, exact):** `(1/√−g) d/dr[√−g ξ e^{−2φ}Θ′] = ξ sinΘcosΘ · B(r)`. **L4 reinforces the
  IDENTICAL bracket** (CAS: |ω_H1|² = g^{rr}Θ′² sin²Θ · B) — the sign structure is not a two-derivative
  artifact.
- **φ-equation — a genuine FORK (P16, the underived time-kinetic sector; do NOT hand-impose GR's form):**
  φ-blindness δS_m/δφ=0 was STATIC-scoped; turning on ω activates the time channel.
  - *channel-corrected (matter stays φ-blind):* φ-eq unchanged `Z_φ(ρ²φ′)′=4e^{−2φ}`; ω-binding loses its
    e^{2φ} depth-weight (becomes depth-uniform).
  - *raw (as-written L2):* matter now SOURCES φ, source `= −2e^{−2φ}Θ′² − 2ω²e^{2φ}sin²Θ/c²` — **the ω²
    piece is a new φ-source the static cell structurally lacked = the depth×spin (φ-angular) coupling of
    the founding hunch.** OPEN — flagged, not resolved armchair.
- **ρ/metric:** G^θ_θ fixes g_rr=e^{2φ}; the static winding EOS T^t_t=T^r_r (⇒ B=1/A) is preserved but
  gains an O(ω²) correction (kinetic T^t_t ⊃ +½ξ|g^{tt}|ω²sin²Θ + the momentum T_tψ).
- **Native frame-drag (l=1) equation** — computed from the native metric's OWN Ricci (framedrag.py), NOT
  GR's Lense–Thirring template: `−½j″ + (2φ′²−φ″)j − (φ′ρ′−ρ″)j/ρ + (ρ′²/ρ²)j = κ₈ e^{2φ} ξ ωN sin²Θ`.
  The `+j/r²` is the native l=1 centrifugal term; the φ′ pieces are the native depth-dressing; only κ₈'s
  normalization carries a Category-A GR-reference tag. Source bulk-peaked (vanishes at both folds).

## Q3 — THE CRUX: ω is a genuine RESTORING/SELECTING term, not a harmless shift (decided armchair)

**The sign is CAS-exact and decided by the metric signature — the two channels carry opposite sign:**
```
N² g^{ψψ} = +N²/(ρ²sin²θ) > 0   (spacelike winding  — REPULSIVE gradient)
ω² g^{tt} = −ω² e^{2φ}/c²   < 0   (timelike rotation — ATTRACTIVE/BINDING)
```
This is **boson-star/Q-ball structure emerging NATIVELY** (not imported — it falls out of the L2+L4 signs):
the static cell (ω=0) has B>0 everywhere — a purely repulsive winding potential with **no binding term at
all**; switching on ω introduces a **new negative-definite contribution the static cell structurally
lacked.** Both L2 and L4 carry it ⇒ robust.

**ω-tunable interior sign-flip radius r*(ω):** B(r*)=0 at `ρ(r*)e^{φ(r*)} = Nc/ω` — winding-repulsion
dominant inside r*, ω-binding dominant outside; r* moves outward as ω falls. So ω supplies an **internal,
ω-tunable scale** — structurally a scale-selector, not an offset.

**The honest tension with the E2 depth-stiffness wall (both directions):** the static E2 wall is core
depth-stiffness — the radial weight e^{−2φ} blows up in the core (e^{−2φ_c}≈1.2×10⁶). The ω-binding rides
the INVERSE weight e^{2φ} (e^{2φ_c}≈8×10⁻⁷). So **the ω-binding help is exponentially SUPPRESSED exactly
in the deep core where the wall lives, full-strength only near the seal (e^{2φ}→1).** ω genuinely adds a
correctly-signed binding term (NOT inert), but it operates in the outer shell, not directly against the
core stiffness. (Under the channel-corrected φ-blind branch the e^{2φ} drops out and the binding becomes
depth-uniform — **the sign crux survives either way**; only the depth-profile of the help changes. This is
exactly why the Q2b P16 fork is load-bearing: the raw/founding-hunch branch is the one where spin ALSO
enters the φ-equation, i.e. can reach deeper than the outer shell.)

**DECIDED armchair:** ω is restoring (opposite sign), a new term absent statically, with an ω-tunable
flip radius; depth-suppressed in the core (raw branch); no junction quantizes it (Q1).
**UNDECIDABLE armchair (→ the one gated computation):** whether the binding is SUFFICIENT to defeat the
depth-stiffness collapse and open a finite existence window ω_min<ω<ω_max. The exact minimal test = the
**ω-augmented second-variation (Jacobi) / Derrick-scaling test of the reduced Θ-energy on the REAL φ(r)**:
either (a) E(λ;ω) under r→λr — does an interior stationary radius appear for some ω?, or (b) lowest
eigenvalue of the Jacobi operator `−(√−g ξe^{−2φ}δΘ′)′ + √−g ξ cos2Θ·B(r) δΘ` — does it cross from
negative (static collapse mode) to ≥0 as ω rises? Bounded 1-D radial pass, Nr≤16–24, on SAVED φ,Θ fields
(must be the real depth-stiff φ — a flat-φ toy would not decide it). This is the NODE-3 F4 check.

## Q4 — discreteness: spatial node-count / winding closure, NOT an ω_n frequency tower

- **The ω_n tower route is ruled OUT.** No junction quantizes ω (Q1); ω is a CONTINUOUS modulus. An ω_n∝1/R
  tower would be box-controlled = P-A refused = clean-fail F3. So there is no frequency tower to build.
- **The discrete carrier is the TOPOLOGICAL WINDING N∈ℤ** (already native, π₂(S²)=ℤ) — possibly joined by
  a radial node-count of Θ (the same structure that made the universe ladder N=0..22 a spatial-profile
  count, `ladder_theorems_AB_C`). For each integer N, ω is a continuous family parameter (boson-star-like:
  a curve, not a tower). So a "catalog" would be indexed by the integer winding (and any radial node
  index), with ω a continuous modulus that closure may restrict to a BAND (an existence window), not
  quantize.
- **Therefore route-2a (topological/BVP) is the ONLY live discreteness route here** — exactly as the MAP
  anticipated. The reframe's job is to supply EXISTENCE + STABILITY of the integer-labelled cells, not a
  new quantum number from ω.

## Q5 — clean F3/F4 failure criteria (pre-registered BEFORE any nonlinear solve)

The reframe is cleanly FALSIFIED / the wall un-escaped if the ONE bounded Jacobi/Derrick-with-ω test shows:
- **F4-fail (no escape):** the ω-augmented Jacobi eigenvalue stays NEGATIVE (static collapse mode survives)
  for ALL ω up to the ansatz ceiling (where ω²e^{2φ}≥N²g^{ψψ} onsets an ergoregion / superradiance /
  breaks static-metric validity) — i.e. no ω opens a stable interior stationary radius / existence window.
  Equivalent Derrick form: E(λ;ω) has no interior stationary point for any admissible ω.
- **F4-quantitative (depth-unreachable):** the binding IS correctly signed but so depth-suppressed that the
  ω needed to bind the core would first create an ergoregion / violate the static ansatz — honest verdict:
  "the wall is a core-depth property outer-shell spin cannot reach" (⇒ pivot to the P16 raw branch, or
  reframe again).
- **F3 (tower) — pre-discharged:** already excluded (ω continuous; no junction quantizes it). Only re-arises
  if someone tries to force an ω_n tower — we will not.
- **Look-elsewhere guard (before ANY positive):** any claimed existence window must survive the 3-cell
  persistence test and appear at ≥2 independent (N, background) points; a single (N,ω) closure is a
  look-elsewhere false positive.
- **Anti-import guard:** the boson-star/Q-ball structure is a Category-A REFERENCE only; existence-window
  expectations must NOT be imported — the Jacobi test is run natively, observe-not-target (no "make it
  bind").

## Premise ledger (chose/derived)
| object | status |
|---|---|
| inverse-metric signs, B-bracket, r*(ω), frame-drag operator | DERIVED (CAS) |
| ω = opposite-signed binding term (not a shift) | DERIVED (CAS, both L2 & L4) |
| L2+L4 native action; κ₈ normalization | THEORY (κ₈ = Category-A GR-reference on normalization only) |
| Q2b φ-sourcing / depth-weight (φ-blind vs raw) | FORK/OPEN = P16 (underived time-kinetic sector) |
| ω, Z_φ, μ, ξ, κ | FREE (do not pin) |
| metric form, ρ=r, Θ(0)=π/Θ(r_s)=0 nodes, concentric embedding | CHOSE/FREE (P8–P10; concentricity habit broken per Charles) |
| sufficiency (does binding defeat collapse) | UNDECIDED → the one gated NODE-3 solve |

## The two decisions this MAP surfaces (Charles's to call)
1. **The P16 φ-sourcing fork (Q2b).** Does spin source φ (raw branch = the founding depth×spin hunch, and
   the only branch where spin reaches the core) or stay φ-blind (channel-corrected, outer-shell only)? This
   is the underived time-kinetic sector — resolving it may itself require a small native derivation (the
   e^{2φ}-weighted time-kinetic term we parked at P16), and it is arguably the more fundamental fork than
   the solve. Do NOT hand-impose GR's form.
2. **The compute gate.** The sufficiency question is undecidable armchair; the ONE bounded, pre-registered
   computation that decides it is the ω-augmented Jacobi/Derrick test on the real φ(r) (Nr≤16–24, 1-D, saved
   fields — NOT the full nonlinear solve). Authorizing it crosses the compute boundary held so far. It is
   the natural NODE-3 step and is F4-pre-registered here.
