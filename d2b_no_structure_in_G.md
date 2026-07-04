# D2b (Q3) — "Branch G admits no finite self-closing structure": derivation attempt, verdict SPLIT

**Date:** 2026-07-04. **Contract:** `microphysics_D2_two_regime_MAP.md` Q3 (approved as written).
**Mode:** CAS-only, no solves, data-blind. **Scripts (all PASS):** `d2b_reduction_flux_cas.py` (13),
`d2b_closure_endcases_cas.py` (9), `d2b_matter_escape_cas.py` (12), `d2b_routeB_mixing_cas.py` (6).
**Status: BANKED, BLIND-VERIFIED (agent a9cfb0141acd701ee, all attacks HOLD + the Route-B T-G1 extension — see VERIFIER RECORD at end; commit 9f94d8b).
discipline applied: the candidate theorem would CONFIRM the standing picture, so escapes were
hunted with priority; one escape REFUTES the strong wording (§4-E1).

**Branch-scoping input check (task item): R1/R2/T1 are P-ONLY.** Both universe-cell docs state
their regime as "round-static **Branch-P** reduction" (`universe_cell_vacuum_impossibility_results.md`
header + ledger; `universe_cell_fold_jc_sigma_results.md:10`), and their proofs ride the P-source
`4e^{−2φ}ρ'²` (the monotone-flux engine). **Nothing transfers to G for free**; every G statement
below is derived fresh from the banked two-player action
(`native_field_equations_constrained_two_player_results.md:85-113`). The banked "round
Birkhoff-frozen" results (#62-64, `timelive_nonround_native_solve_results.md`) are earlier-frame,
time-sector-scoped — used only as corroboration, never load-bearing.

---

## 1. Definition (stated, tagged CHOSE-definitional)

**A finite self-closing Branch-G structure** = a finite radial domain [r₁, r₂], ρ > 0 throughout
(banked cell definition), solving Branch G's field equations in the bulk (𝒦_G = e^{2φ}𝒦, φ-free
compensation), with BOTH ends closed by the DERIVED closure menu — even fold (pins φ'=ρ'=0), odd
fold (pins φ=fold-constant, ρ'=0; φ' free), or a regular center — with no reference to anything
outside the domain, and (banked CHOSE posture, carried) passing the free-endpoint transversality
closure H_tot(end)=0. This is the exact analog of what the universe cell does in P. A G-domain
bounded by a **G|P interface is definitionally NOT self-closing** (an interface requires a P side;
that configuration is the A1/A2 composite architecture, out of scope here).

**End-menu exhaustiveness (derived, pointwise class):** a fold identification must be a bulk
symmetry of L_G. L_G depends on φ only through φ'², so the field maps are φ→φ+c (continuity at the
fold ⇒ c=0 ⇒ even fold) and φ→2a−φ (odd fold, ANY reflection constant a — see §4-E2); the
ρ-identification is forced to ρ→ρ (fold-JC doc: "for Branch G the match is exact and uniquely
solvable"). Remaining end-types: regular center; ρ→0 degeneration (excluded by the banked ρ>0 cell
definition). Pointwise class itself: CHOSE (banked, loophole probed there).

## 2. Branch G's derived structure (script 1, all CAS)

Round reduction on h=ρ²Ω, per 4π (same normalization that reproduces the banked
L_P = (Z/2)ρ²φ'² − 2e^{−2φ}ρ'² + 2 — reproduced exactly as a control):

    L_G = (Z/2)ρ²φ'² − 2ρ'² + 2          [NEW: the G round reduction]

- **Global shift φ→φ+λ EXACT** in L_G (any λ); broken in L_P by −2(e^{−2λ}−1)e^{−2φ}ρ'² ✓ banked.
- **φ-EL is SOURCE-FREE for ANY φ-blind matter: (Zρ²φ')' = 0.** The flux Φ = Zρ²φ' is EXACTLY
  CONSTANT — not merely monotone as in P. This is the single load-bearing fact of the whole doc.
- **ρ-EL: −4ρ'' = Zρφ'² + ∂L_m/∂ρ** — matter DOES gravitate in G (task question answered: the
  L2+L4 carrier sources the h-sector exactly as in P, minus the e^{2φ} prefactor; it sources φ in
  NEITHER branch directly — in P, φ's source is the geometric e^{−2φ}ρ'² term, which G's
  compensation deletes). Matter cannot locally tell G from P: L_m is identical in both.
- **H = (Z/2)ρ²φ'² − 2ρ'² − 2 + E_m conserved** (autonomy, matter included).
- **Fold pins in G** (Weierstrass–Erdmann, mirror extension): even fold pins φ'=ρ'=0; odd fold
  pins φ(r_s)=a, ρ'(r_s)=0, φ' free — same shape as banked P pins.
- **NON-ROUND (within the constrained frame):** e^{2φ}(K_ABK^AB−K²) is φ-free for a GENERAL
  symmetric h_AB(r) (CAS), and R⁽²⁾[h], √h, L_m are φ-free ⇒ φ enters the FULL G action only
  through (Z/2)√h φ'² ⇒ φ-EL = (Z A(r)φ')' = 0 with A(r)=∮√h > 0. **The deadness argument below
  is NOT round-scoped** — it holds for any transverse geometry inside the constrained metric form.

## 3. What G lacks vs P — and which lack does the killing (audit of Q3's own parenthetical)

Q3's wording cites four lacks: "φ decoupled + scale-free + no absolute depth + round-G
Birkhoff-frozen". Honest audit — **only the first does the work**:

| cited lack | fate under derivation |
|---|---|
| **φ decoupled (source-free)** | **THE engine.** Φ exactly constant ⇒ end-case table (§4) forces Φ=0 in every canon-form closed domain ⇒ φ ≡ const. Kills: anchor (Δφ=0), seal charge (q=0), the flux ladder (the N=0..22 ladder is the integral of the P-source; source ≡ 0 ⇒ no closures to count), the a_seal/θ₀ laws, accumulation/quantization closure. The φ-angular coupling **does not exist in G at the action level** (𝒦_G φ-free). |
| scale-free | **Vacuum-only.** L_G is exactly scale-covariant (CAS) ⇒ vacuum solutions come in scale families. But the carrier's L4 term (~I_4θ/ρ²) BREAKS it (CAS), and criticality E_m(fold)=2 with the rigid carrier PINS ρ_f² = κN²/(4−ξ(1+N²)) (CAS). "Scale-freedom forbids a pinned size" is FALSE with matter present — this lack does NOT carry the theorem. |
| no absolute depth | **Not load-bearing for closure.** Δφ is shift-invariant; the gauge alone would happily allow Δφ-structure. What kills Δφ is source-freeness, not the gauge. (The gauge DOES make any closure a φ₀-family, but that family is one physical solution.) |
| round-G Birkhoff-frozen | **Not needed.** Replaced by the native non-round argument (§2 last bullet); the banked Birkhoff results are earlier-frame + time-sector corroboration only. |

## 4. The end-case table, the theorems, and the escapes (adversarial)

**End-case table (script 2, CAS):** Δφ = (Φ/Z)·I with I = ∫dr/ρ² > 0. Even fold anywhere ⇒ Φ=0.
Regular center anywhere ⇒ Φ=0 (∫dr/ρ² diverges at ρ→0; CAS). Odd+odd canon (both folds φ→−φ) ⇒
Δφ=0 ⇒ Φ=0. **Every canon-form end-pairing forces Φ=0 ⇒ φ' ≡ 0 ⇒ φ ≡ const (pure gauge).**

**T-G1 (THEOREM, vacuum): Branch G admits no finite self-closing vacuum structure.**
Canon-form: Φ=0 ⇒ ρ''=0 ⇒ ρ linear; any end pins ρ'=0 ⇒ ρ ≡ const; H = −2 ≠ 0 fails the H=0
closure (same gap-2 as P's R1b; the "empty-medium H_target=−2" fork would make it marginal at
every size — canon-blocked, stated, same as the P-side flag). Twisted (E2 below): ρ'' =
−q²/(4Zρ³) strictly one-signed (either sign of Z) ⇒ ρ' strictly monotone after the first fold ⇒
no second ρ'=0 end EXISTS. Center-regular G vacuum = EXACTLY flat (all Riemann components 0,
CAS) with ρ' = e^{φ₀} never 0 ⇒ can never close. **No escape found in vacuum. Unconditional
within the frame (§5).**

**T-G2 (THEOREM, φ-sector deadness / mechanism one-sidedness):** under Route A + canon-form
folds, every finite self-closed G-domain has **φ ≡ const: zero anchor, zero seal flux, and — in
both routes, round or not — a SOURCE-FREE φ-equation: no φ-angular coupling, no monotone-flux
structure, no ladder, no quantization closure.** The banked mass-emergence mechanism (Δφ anchor,
Class-B seal flux q, the integer ladder = closures of the P-source integral, Theorems A/B, F5
criticality as φ-structure) **has no Branch-G realization. "Emergence-as-banked is P-only"
DERIVES.** This is the true content of Charles's retained core.

**The escapes (hunted hardest, per hypothesis discipline):**

- **E1 — φ-flat matter-closed G-cell: REFUTES the strong wording "no finite self-closing
  structure".** Exact counterexample (script 3, all identities CAS-exact): φ ≡ const,
  ρ(r) = ρ₀ + b·sin²(kr) on [0, π/2k], potential-only matter L_m = −U(ρ),
  U = 2 + 8k²(ρ−ρ₀)(ρ₀+b−ρ) — inside D3's banked ADMISSIBLE φ-blind class. Both EOMs hold
  identically; both ends are derived even-fold pins; **H ≡ 0 exactly** (free-endpoint closure);
  **E_m(folds) = 2 exactly** (the F5-critical value). The same configuration **violates the P
  φ-EL** (residual −4e^{−2φ₀}ρ'² ≠ 0): the object class is **G-exclusive** — G is precisely the
  branch where matter may sit φ-inertly; in P matter must organize φ. **Fate:** (i) it is a real
  closed structure with geometric (Misner–Sharp) mass but ZERO dilation content — no anchor, no
  charge, no ladder, nothing the banked emergence mechanism is made of; (ii) it rides the σ-free-
  function channel — D3's own tooth applies verbatim ("a cell closed by choosing σ carries ZERO
  evidential weight"); (iii) for the DERIVED L2+L4 carrier, existence is an OPEN BVP (not CAS-
  decidable), with two sharp sub-results: the winding bound **I_4θ ≥ 1** (Cauchy–Schwarz off the
  pins f(r,0)=0, f(r,π)=π; CAS + numeric spot-checks 1.36/1.83/1.42) makes the carrier's
  −κN²I_4θ/4ρ³ source diverge at any center ⇒ **carrier-threaded G-balls are matter-obstructed**
  (mirror of P's R2); and criticality pins the fold radius (no scale family). The center-free
  two-fold shell is the carrier's only candidate home — same topology P was forced into.
- **E2 — twisted odd folds (G-only exotic).** φ→2a−φ is an exact bulk symmetry of L_G for EVERY a
  (CAS) — in P for NO a (CAS). Two odd folds with different reflection constants a≠b give a
  closed domain with **Φ = Z(b−a)/I ≠ 0**: nonzero flux and Δφ = b−a. This is the shift-symmetry's
  monodromy (a Wilson-line-like twist), possible ONLY in G. **Fate:** vacuum-dead (T-G1's
  concavity kill, CAS); with matter OPEN; but Δφ and q are free CONTINUOUS moduli — a chosen
  input, not an emergent output, so no selection/discreteness; and the canon fold as worded
  (C-2026-06-10-2: φ→−φ) does not license a≠0. **STOP-item 1 for Charles** (§6).
- **E3 — the Route-B mixing term (lands on the standing OWED Z=8/Route-B tension).** The
  compensated mixing term 2√h e^{φ}Kφ' = 4ρρ'φ' is **shift-invariant, hence R1-LEGAL in Branch
  G** (CAS) — the depth-gauge argument cannot exclude it, so the banked mixing-term-free G action
  is itself Route-A-conditional (a sharper form of the known tension, now touching G). Under
  Route B: Φ̃ = Zρ²φ' + 4ρρ' exactly conserved (CAS, matches the banked Route-B P-flux form);
  any closed cell with an even end has Φ̃=0 ⇒ **φ = −(4/Z)ln ρ + c, slaved to the geometry** —
  the "φ ≡ const" WORDING of T-G2 fails; and canon odd+odd cells can carry **q = 4ln(ρ₂/ρ₁)/I
  without any twist** (CAS). **What survives Route B unharmed:** the φ-equation remains
  SOURCE-FREE (no e^{−2φ} term appears either way), φ carries no independent DOF, and no
  ladder/quantization-closure structure exists — **the MECHANISM one-sidedness (T-G2's teeth)
  is Route-robust; only the φ≡const wording is Route-A-conditional.**
- **E4 — G|P-interface-bounded G domains:** excluded by definition (§1); in composites, G's exact
  flux constancy makes it the **conduit** (Coulomb hair, JC1 [Zρ²φ']=0 carries the P-side's q
  through G unchanged) — consistent with, and clarifying, the A1/A2 architectures: **G can CARRY
  flux between P-structures but cannot terminate or close it.**
- **E5 — non-round:** covered inside the constrained frame (§2); no escape there. The genuine
  scope boundary is the constrained metric FORM itself (CHOSE, banked) + staticity (§5).

## 5. VERDICT (with exact premise set)

**The candidate statement as worded — "Branch G admits no finite self-closing structure" — is
REFUTED** (E1: an exact, closure-complete, G-exclusive counterexample inside the banked
admissible matter class). **What DERIVES instead is the sharp pair:**

- **T-G1: no finite self-closing VACUUM structure in Branch G** — theorem, no escape found
  (twisted included).
- **T-G2: no Branch-G realization of the mass-emergence MECHANISM** — in any finite self-closed
  G-domain the dilation sector is dead (φ ≡ const under Route A/canon folds; φ slaved with Φ̃=0
  under Route B), the φ-equation is source-free in every case (round or not, any φ-blind matter),
  and therefore anchor, seal charge, flux ladder, accumulation law, and quantization closure —
  the entire banked emergence chain — cannot arise in G. **Charles's one-sidedness holds at the
  MECHANISM level, not at the bare existence-of-structure level.** What G can still hold is
  φ-inert matter-closed geometry (E1) — mass without the emergence machinery; whether that
  counts as "structure" for the two-regime picture is a PONDER call, not a derivable one.

**Premise set (every result conditioned on it):** (1) constrained two-player metric form, φ
longitudinal — CHOSE (banked); (2) STATIC — frame-wide (nonstationary G, incl. the l≥2 wave
sector, uncovered); (3) matter φ-blind — DERIVED for winding, PREMISE for any bulk sector;
(4) pointwise fold class + φ-continuity at folds — CHOSE (banked, JC2/orbifold); (5) ρ>0 cell
definition — banked; (6) free-endpoint transversality H_target=0 — CHOSE (banked posture; the
H=−2 empty-medium fork flips T-G1's constant cell to marginal — canon-blocked, stated);
(7) Route A action form — inherited CHOSE, now known R1-cannot-force in G (E3); (8) canon fold
form φ→−φ (a=0) — canon-anchored (E2 rides on relaxing it); (9) Z ≠ 0, results otherwise
Z-independent (sign-robust where checked); (10) per-4π round reduction normalization —
convention, controlled by reproducing banked L_P.

**Every CHOSE I made myself:** the §1 definition of "finite self-closing structure"
(CHOSE-definitional, stated); treating H_target=0 as the closure test (carried banked CHOSE);
the E1 counterexample's profile/potential (constructive witness — a choice by nature);
numeric spot-check profiles in the I_4θ bound (illustrative only, the bound is CAS).

## 6. STOP-and-report forks (uncovered here, Charles's calls)

1. **Twisted odd folds (E2):** is a φ→2a−φ (a≠0) identification admissible? Canon wording says
   no; G's gauge structure makes it the natural monodromy sector. If admitted, G gains a
   moduli-family of flux-carrying closed cells (matter case open) — still selection-free.
2. **Does a φ-flat matter-closed G-cell (E1) count as "structure"** for the two-regime picture?
   It has MS mass but zero dilation/emergence content. This decides whether Q3's headline is
   "REFUTED-as-worded, holds-as-mechanism" (my honest reading) or needs re-wording of "structure".
3. **The Route-B tension now touches Branch G** (E3): the mixing term is R1-legal in G, so
   "Branch G = no mixing term" is an unforced Route-A inheritance. The standing OWED item just
   grew a G-side face.
4. **Compactly-supported carrier?** If the winding sector may occupy only a shell (not banked
   either way), a flat-core G-ball with a winding shell becomes an E1-variant candidate; if the
   carrier must thread all shells, centers stay matter-obstructed (I_4θ ≥ 1).

## 7. Verifier note

Owed before any banking: blind adversarial pass on (a) the end-case exhaustiveness argument
(§1/§4 table), (b) the E1 counterexample's admissibility reading of D3, (c) the twisted-fold
consistency (E2), (d) the Route-B G-legality claim (E3). Scripts self-contained; avoid-list
should include this doc.

---
## VERIFIER RECORD (blind adversarial pass — agent a9cfb0141acd701ee, 2026-07-04): ALL ATTACKS HOLD + ONE EXTENSION
T-G1 re-derived (end-case menu complete; extra pairings hunted, none escape; concavity kill
one-signed both Z-signs; center-regular G vacuum exactly flat by the verifier's own full 4D
Riemann computation). **VERIFIER EXTENSION: T-G1 also holds under ROUTE B** (even-end Route-B
vacuum ⇒ φ slaved, ρ''=0 ⇒ constant cell, H=−2≠0; odd+odd ⇒ end-flux |Φ̃|=4√2ρ_end≠0
contradicts Δφ=0) — the theorem is ROUTE-ROBUST, its last implicit conditioning removed.
T-G2 confirmed round AND general-h_AB within the constrained frame; route-robust (mixing term
shift-invariant; Route-B G φ-equation still source-free). The E1 φ-flat massed G-cell
counterexample verified exact by independent CAS (both EOMs, fold pins, H≡0, E_m(folds)=2,
P-EL violation) — the refutation of the strong wording is REAL (hypothesis discipline working:
the deliverer killed its own confirming headline). The four STOP-forks correctly deferred to
Charles. SAFE TO BANK as worded, with the Route-B extension recorded here.
