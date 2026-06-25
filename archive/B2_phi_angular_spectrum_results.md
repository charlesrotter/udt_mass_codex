# B2 — The phi-angular SPECTRUM / discreteness (algebraic derive + provenance audit)

**Mode:** ALGEBRAIC DERIVE (exact symbolic) **+ IMPORT-PROVENANCE AUDIT.**
TRACK B / STEP B2 of ALGEBRAIC_MATTER_PATH_PLAN.md.
**Agent:** claude-opus-4-8[1m]. **Date:** 2026-06-19.
**Status:** NOT canon. Working algebraic-derive + audit record. Append-only.
**Script:** `B2_spectrum_native_audit.py` (sympy-exact; the three load-bearing
facts below are re-derived machine-exact, NO grid / box / cutoff / numeric PDE
as instrument).
**DATA-BLIND:** no lepton wall numbers (contract 26fc757) and no empirical
mass/ratio loaded anywhere in this work — verified by inspection of the script.

---

## 0. The question (B2, restated)

Does an EXACT, DISCRETE mass/type SPECTRUM emerge ALGEBRAICALLY from the native
phi-angular structure — as an eigenvalue / recursion / representation condition,
with discreteness GUARANTEED by the algebra (not a numeric scan)? Target
scale-free RATIOS (B1's O1 scale cancels in ratios). This is the project's
central open question (discreteness / generations), posed algebraically.

B1 named the obstructions: **O1** free overall scale; **O2** the charge<->mass
bridge is monopole-only, needs "exterior angular structure beyond the bare tail"
(Charles's phi-angular suspect); **O3** no native charge-SUM => static cost gives
no spectrum. B1's pointer: a discrete spectrum "would have to come from ... a
standing-wave / eigenvalue condition ... the transfer-ladder/junction territory
B2 reserves and which is UNAUDITED / not-yet-native today."

**Headline answer (honest):** **NATIVE NON-CLOSURE.** Every candidate spectrum
machinery the corpus names is either an **IMPORT/UNAUDITED ansatz** (transfer
ladder, junction condition, index theorem) or a **NATIVE object that was directly
tested and PROVEN not to discretize** (the seal/mirror-fold, the angular sector,
the monodromy/closed-time condition). No native eigenvalue/recursion condition
exists today that yields a discrete phi-angular spectrum. The discretizer is
**MISSING, not merely uncomputed** — and the audit shows WHY (an exact algebraic
obstruction, §3[A]). No spectrum was manufactured by importing a transfer matrix,
by box-eigenvalues, or by fitting.

---

## 1. PROVENANCE AUDIT TABLE — the spectrum machinery (guardrail A)

Each candidate spectrum object: **NATIVE-with-derivation** / **IMPORT** /
**UNAUDITED**. Evidence is file:line from the corpus, cross-checked by three
independent reconnaissance passes this session (transfer/junction; seal/weld;
closed-time) and B1's table. Verbatim load-bearing quotes retained.

| # | Spectrum object | Provenance verdict | Could it discretize? | Evidence / derivation |
|---|-----------------|--------------------|--------------------|-----------------------|
| 1 | **Transfer ladder** `r=C·g^d`, `T=e^{−sη}I_N`, `γ=tr(T)=N e^{−sη}` | **IMPORT/UNAUDITED — self-declared ANSATZ** | NO (hand-imposed integers; data-falsified) | "## 57. Minimal epsilon **transfer-matrix model**" / "the gamma **ansatz** can be written as the trace of a simple transfer matrix" (negative_phi:3801,3805). "But **the derivation is still missing**" — three undischarged requirements (negative_phi:3854). "**without pretending to derive the full transfer ladder**" (negative_phi:14388). Pre-registered frozen falsification: "**NO HIT, NO LEAD, anywhere**" (lepton_ladder_test:60-83). |
| 2 | **Junction condition** (depth `d=2L`, same-minus matching) | **UNAUDITED — REFUTED as derived** | NO (no PDE closure ever computed) | "**B. THE d=2L JUNCTION COUNT — READING-GRADE, not forced (REFUTED as derived)** ... **No junction-condition computation was done**" (dpf_verifier:85-90). "a junction **COUNT reading, not a junction-condition computation**" (dpf_verifier:155). "the load-bearing **junction-condition gap**" (dpf_results:222-226). |
| 3 | **Israel junction (GR corpus)** | **IMPORT — named as a mine-map, never executed** | n/a (template, not run into UDT closure) | "Israel junction conditions ... metric jump algebra only, not Einstein matter sourcing" — listed as a GR-corpus map, never derived into a native seal closure (negative_phi:11813-11816). |
| 4 | **Seal / weld = same-minus MIRROR FOLD = TIME REVERSAL `t→−t`** | **NATIVE — DERIVED, blind-verified** | **NO — single boundary number; tested, does not discretize** | Derived: exact det identity `det g4 ∝ (b−fqa)²` on D=0 => regular Lorentzian fold not edge (w6:40-46, blind-verified); "**sigma IS f_T → −f_T — sigma is TIME REVERSAL on the crease**" (w7:52-54); parity BC `σ-even→Neumann / σ-odd→Dirichlet` (w7:57-58). BUT its content is ONE number: `D=4π(ln f)_seal` (h1_types:42-47), `= [DISCRETE 4π] × [CONTINUOUS, FREE (ln f)_seal]` (h1_types:80-82); `dD/dE≠0`, "**No lattice, no jump**" (h1_types:102-103); "the metric's field equations **IMPOSE NO QUANTIZATION on (ln f)_seal**" (h1_types:105). All four candidate quantizers (flux/holonomy/regularity/q=1/3) FAIL (h1_types:130-150). |
| 5 | **Seal + angular sector (the phi-angular bridge as an eigenvalue cond.)** | **NATIVE — and DIRECTLY TESTED** | **NO — proven round-only; exact algebraic root** | Whole-Closed-Cell solve, blind-verified: "the seal closure supports NO angular structure that the bulk damps. The closed cell is STILL one round type" (wcc:74-75); min angular bifurcation gap **0.648 > 0**, grid/horizon-robust (wcc:85-94). EXACT ROOT (re-derived here §3[A]): the angular nonlinearity `−v_θ²` linearizes to **EXACTLY ZERO** about the θ-flat round background, so the operator is the pure sign-definite dressed Laplacian (wcc:107-116). |
| 6 | **Closed-time / nonstationary "selector"** (generations home) | **ASSERTED-POINTER-ONLY — DROPPED 2026-06-18; classical no-go** | **NO (classical) — periodicity not native; condition closes for all** | "Time itself is an INTERVAL ... periodic faces ... | **CHOICE (the closed-time hinge)**", ω a *free* eigenvalue (time_live_DESIGN:203,72). Seal is `t→−t` reflection => time is an INTERVAL not a CIRCLE, "**no time-circumference T forced ... underived hinge**" (NEGATIVES_REGISTRY:1546-1551). "**closed-time thread DROPPED** — a rhythm needs no time-loop" (HANDOFF:43, STATE:152). Monodromy test: "**Δχ=2πn is satisfied for EVERY omega ... NO condition ... There are no D_n**" (monodromy_depth:134-143). Nonstationary opener: C1 elliptic in T, "**configurations are 4D boundary-value equilibria**", oscillatory sector is "**real, unselected**" (nonstationary_opener:20-40,79-84). |
| 7 | **Index theorem** (AS / APS) | **IMPORT — scope-mismatch HALT** | NO (inapplicable) | standard index theorems need closed Riemannian / APS BC; UDT is Lorentzian + Neumann => inapplicable; native version NOT derived (B1 table #11; udt_canonical:5912). |
| 8 | **Representation theory** `End(H1)=3⊗3=1+3+5` | **NATIVE alphabet — but NOT a set of cells** | **NO — a decomposition of ONE operator space** | "1+3+5 is a **decomposition of ONE operator space**, not a set of distinct cells: the θ-varying pieces (3 and 5) are PURE DAMPING under any seal closure ... the metric does NOT stabilize a 3-cell or 5-cell distinct from the round 1-cell" (h1_types:87-97). The weights `W(P)={1/4,5/12,2/3}` ORDER but are "a classification ladder, not a set of realized types" (h1_types:95-97). spin-3/"7" is ABSENT (numerology, registry #35). |
| 9 | **Second seal => S²×S¹ => integer (Chern) family** | **PARKED / UNBUILT open route** | possibly (hinges on unbuilt #37 core closure) | "if the core is a finite second seal, H²=ℤ gives an integer family of types" — explicitly unbuilt (topo:29; NEGATIVES_REGISTRY:756). |
| 10 | **Standing wave trapped between two reflecting seals** (time-live geon) | **DESIGN-ONLY / UNRUN; bare vacuum so far BARREN** | unknown (program, not result) | "the reflecting seal lets the radiation return so a standing-wave mode can persist" — design doc for an unrun program (time_live_DESIGN:25-28,62-68). Bare-vacuum geon Phases 0-2b came back barren: "Vacuum is barren in UDT as in GR — you need matter" (HANDOFF:47-49; NEGATIVES #62-64). |

**Audit conclusion:** Of the named spectrum machinery, the only **NATIVE-with-
derivation** objects are the **seal/mirror-fold** (#4), the **seal+angular
operator** (#5), and the **rep-theory alphabet** (#8) — and ALL THREE were
directly tested and **proven NOT to discretize a dynamical spectrum**. Every
object that *would* give a recursion/ladder (transfer ladder #1, junction #2/#3,
index #7) is **IMPORT or UNAUDITED ansatz**, and where tested against data the
ladder MISSES (#1). The closed-time selector (#6) is an asserted pointer, now
DROPPED, with a classical no-go. The two routes that could still discretize
natively (#9 second seal, #10 trapped standing wave) are **UNBUILT**.

---

## 2. The phi-angular bridge posed as an eigenvalue condition (what B2 was asked to try)

B1's O2 = "the ℓ=1 drive needs exterior angular structure beyond the bare tail"
= Charles's phi-angular suspect. B2's positive task: pose that bridge as a
standing-wave / eigenvalue condition — the angular structure (area form / the
n-field beyond monopole, ℓ≥1) coupled to the radial dilation — and ask if the
spectrum is DISCRETE by construction.

The corpus already POSED EXACTLY THIS and SOLVED IT (the Whole-Closed-Cell,
`wcc_results.md`, blind-verified): live differential angular field ℓ=1,2,3 +
the seal mirror-fold closure, eigenvalue/bifurcation spectrum. **Result: round-
only, gap 0.648 > 0, no discrete bound tower.** So the phi-angular bridge AS AN
EIGENVALUE CONDITION on the audited-native objects has been built and does not
produce a spectrum. The reason is an EXACT algebraic obstruction, not a numeric
limitation — re-derived in §3.

---

## 3. The EXACT algebraic obstruction (re-derived this session, sympy-exact)

`B2_spectrum_native_audit.py` re-derives the three load-bearing facts machine-
exact (no grid/box/cutoff). All three returned the blocking value:

**[A] The angular nonlinearity `−v_θ²` linearizes to EXACTLY ZERO about the
round background — so the phi-angular eigenvalue operator is sign-definite
DAMPING at every harmonic, with no soft/bound mode.**
```
v = v0(r) + eps·u(r,theta),   v0 theta-independent (round background, v0_theta=0)
L_nl = -(v_theta)^2
d/d_eps L_nl |_{eps=0} = -2 v0_theta u_theta = 0      (since v0_theta = 0)   [EXACT]
=> angular fluctuation operator = pure dressed Laplacian e^{2v0}(u_thth+cot th u_th)
=> eigenvalue -l(l+1)·W(r),  W>0  =>  < 0 for all l>=1  =>  PURE DAMPING
```
This is THE reason no phi-angular spectrum exists: a sign-definite damping
operator has no discrete bound tower, and the seal closure (a boundary condition)
cannot soften a sector whose linear operator is sign-definite. **This is an exact
algebraic fact about the native angular Lagrangian, guaranteed by the algebra —
exactly the kind of guarantee the algebraic path was supposed to provide, here
delivering a NEGATIVE.** (Charles's phi-angular suspect: the coupling EXISTS, but
at linear order about the only stable background it VANISHES — so it does not, on
these objects, supply the discretizer.)

**[B] The transgression is EXACT => one seal number => no recursion, no eigenvalue.**
```
INT_S2 omega_H1 = INT sin(theta) dtheta dphi = 4*pi          [EXACT, = H^2(S^2,Z) deg-1]
D = INT Xi = 4*pi*(ln f)_seal = [DISCRETE 4pi] x [CONTINUOUS (ln f)_seal]
dD/dE = 4*pi*(ln f)_seal'(E)  != 0  generically  => CONTINUOUS depth, NO lattice
```
The only DISCRETE factor is the topological `4π` (already banked as q=1/3, N=3 in
B0/B1). It is a single boundary 2-form datum, NOT a mode spectrum. No recursion
lives in the transgression because it is exact (zero bulk Euler-Lagrange content).

**[C] The closed-time / monodromy single-valuedness condition closes for every
frequency/depth => selects no discrete `D_n`.**
```
Delta_chi = 2*pi   (identically; NO-MONODROMY, no induced internal twist)
d/d_omega Delta_chi = 0,  d/d_D Delta_chi = 0    => independent of (omega, D)
2*pi*n = Delta_chi  closes for n=1 at EVERY (omega, D)  =>  NO D_n selected
```

**Net:** [A] kills the angular eigenvalue route, [B] kills the transgression-
recursion route, [C] kills the closed-time-quantization route — each an exact
statement, not a numeric scan. **No native eigenvalue/recursion condition for a
phi-angular spectrum survives.**

---

## 4. Connection to the standing hunch (honest)

- **Charles's phi-angular discreteness suspect:** the audited-native phi-angular
  COUPLING is real (the transgression `(ln f)·ω_H1` is radial × angular, and the
  angular nonlinearity `−v_θ²` is genuinely a coupling term). But §3[A] shows
  that at linear order about the only stable (round) background the angular
  nonlinearity VANISHES exactly, so this coupling does NOT discretize a spectrum
  on the present objects. The hunch is not refuted as a DIRECTION — it is shown
  that its realization requires structure NOT in the current native set:
  specifically a background that is NOT θ-flat (a non-round carrier), so that
  `v0_θ ≠ 0` and the nonlinearity's linear variation is non-zero. That is exactly
  the "exterior angular structure beyond the bare tail" O2 named, and exactly the
  non-round direction CANON C-2026-06-18-1 / the time-live program point to —
  but it is **UNBUILT** (table #9, #10), so the discretizer is still MISSING a
  native object.

- **The prior closed-time / nonstationary pointer:** AUDITED as asserted-pointer-
  only, DROPPED 2026-06-18 ("a rhythm needs no time-loop"), with a classical
  no-go (monodromy closes for all ω; nonstationary sector is 4D-elliptic, the
  oscillatory family "unselected"). The corpus explicitly RESERVES one un-run
  construction — a **Euclidean periodic-time path integral** (the standard
  Matsubara origin of discreteness, NEGATIVES_REGISTRY:1561-1563) — but nobody
  has shown the metric FORCES a period β; it is named as the open quantum
  frontier, not constructed, and the project's current direction is that no
  separate quantum/closed-time sector is needed at all.

---

## 5. Premise ledger (exact-from-corpus / derived / chosen — every non-exact step flagged)

| Premise | Tag | Note |
|---------|-----|------|
| `INT_S2 omega_H1 = 4*pi`, deg-1 H²(S²,ℤ) | **derived-here exact, NATIVE** | re-derived in script; the one discrete factor |
| `D=4π(ln f)_seal`, `dD/dE≠0`, depth continuous | **exact-from-corpus, NATIVE** | h1_types:42-105; ADV-1..4 quantizers all fail |
| seal = mirror-fold = `t→−t` time reversal | **exact-from-corpus, NATIVE, blind-verified** | w6:40-46, w7:52-58 |
| `−v_θ²` linearizes to 0 about round bg | **derived-here exact, NATIVE** | script [A]; matches wcc:107-116 (blind-verified) |
| angular eigenvalue `−l(l+1)·W`, W>0 (damping) | **derived-here exact, NATIVE** | sign-definite => no discrete tower |
| `End(H1)=1+3+5` alphabet (not realized cells) | **exact-from-corpus, NATIVE** | h1_types:87-97; 3,5 pieces are pure damping |
| transfer ladder `r=C·g^d`, `T` | **IMPORT/UNAUDITED ansatz, data-falsified** | negative_phi:3801-3854; lepton_ladder_test:60-83 |
| junction depth `d=2L` | **UNAUDITED — REFUTED as derived** | dpf_verifier:85-90,155 |
| index theorem | **IMPORT — scope-mismatch HALT** | B1 #11 |
| closed-time periodicity β | **CHOICE / asserted-pointer, DROPPED** | time_live_DESIGN:203; HANDOFF:43 |
| monodromy `Δχ=2π`, indep of (ω,D) | **derived-here / exact-from-corpus** | script [C]; monodromy_depth:134-143 |
| second-seal S²×S¹ Chern family | **PARKED / UNBUILT** | topo:29 — not used to claim a spectrum |
| trapped standing-wave geon | **DESIGN-ONLY / UNRUN, bare vacuum barren** | time_live_DESIGN; NEGATIVES #62-64 |
| any specific number/ratio as evidence | **none** | no rational promoted to evidence; see §6 |

---

## 6. Numerology guardrail (B) + DATA-BLIND status

- **DATA-BLIND: PASS.** No lepton wall numbers (contract 26fc757) or any
  empirical mass/ratio appear in `B2_spectrum_native_audit.py` or this doc.
- **No bare integer/rational promoted to evidence.** The only constants in the
  derivation (`4π`, `−l(l+1)`) are exact geometric/topological facts, not fits.
  No new rational identity is claimed, so no TEST-B classifier run is required —
  the deliverable is a **non-closure with a named obstruction**, which is
  import/numerology-clean by construction.
- The data-falsified transfer ladder (#1) is recorded as a falsified IMPORT, NOT
  used to support any claim. No spectrum was fit to or read off any data.

---

## 7. Honest read — does a discrete spectrum emerge from native phi-angular algebra?

**NO — clean, native NON-CLOSURE, with the obstruction NAMED and re-derived exact.**

- **NOT clean-emergence and NOT partial-emergence.** Unlike B1 (which had a
  CLEAN charge side), B2 has **no** native object that produces a discrete
  spectrum. Every machinery that would give a recursion/ladder is IMPORT or
  UNAUDITED ansatz (and the one that yields numbers is data-falsified). Every
  NATIVE object (seal, angular operator, rep alphabet) was directly tested and
  **proven not to discretize** — and §3[A] gives the EXACT algebraic reason: the
  phi-angular nonlinearity vanishes at linear order about the only stable
  background, so the angular operator is sign-definite damping with no discrete
  tower. The algebraic path delivered the GUARANTEE it promised — here, a
  guaranteed NEGATIVE.

- **The named obstruction (B2's deliverable):** *there is no native
  eigenvalue/junction/recursion condition that discretizes a phi-angular
  spectrum.* The seal is one continuous number (not an eigenvalue condition); the
  angular sector linearizes to pure damping (no bound tower); the transgression
  is exact (no recursion); the closed-time condition closes for all ω (selects
  nothing); the transfer-ladder/junction/index machinery that could provide a
  recursion is IMPORT/UNAUDITED and must NOT be banked. **B2 awaits a native
  eigenvalue/junction condition that does not yet exist.**

- **What the obstruction POINTS to (not a result, a direction — no false
  convergence):** the one structural gap is that the angular discretizer vanishes
  *about a θ-flat round background*. It would be non-zero about a NON-ROUND
  carrier (`v0_θ ≠ 0`). The two corpus routes that could supply that — a SECOND
  mirror seal giving S²×S¹ (an integer Chern family, table #9) and a standing
  wave trapped between reflecting seals on a non-round carrier (the time-live
  geon, table #10) — are both **UNBUILT**, and the bare-vacuum version came back
  barren (matter needed). So the realization of Charles's phi-angular hunch is
  **still missing a native object**: a non-round (matter-sourced) carrier on which
  the angular nonlinearity does not vanish, closed by the native mirror seal.
  That is the precise, single, named next target — stated as a target, not a
  convergence narrative, and NOT pursued by importing a transfer matrix or by
  box-eigenvalues.

- **Import status:** the verdict is **NOT import-contaminated** in the sense of
  resting a claimed spectrum on an import — because **no spectrum is claimed.**
  The honest result is that the only objects that COULD give one natively are
  proven-negative, and the recursion machinery in the corpus IS import/unaudited,
  which is exactly why no spectrum can be banked.

---

## 8. One-line summary

On the AUDITED-NATIVE objects, **no discrete phi-angular mass/type spectrum
emerges**: the native seal is a single continuous number (not an eigenvalue
condition), the native angular nonlinearity linearizes to EXACTLY ZERO about the
round background (sign-definite damping, no bound tower — re-derived exact), the
transgression is exact (no recursion), and the closed-time condition closes for
all frequencies (selects nothing) — while every recursion/ladder machinery
(transfer ladder, junction, index) is IMPORT/UNAUDITED and one is data-falsified.
**B2 is a clean native NON-CLOSURE; the named obstruction is "no native
eigenvalue/junction condition exists," and the single direction it points to (a
non-round, matter-sourced carrier closed by the native seal) is UNBUILT — not
imported, not box-derived, not fit.**
