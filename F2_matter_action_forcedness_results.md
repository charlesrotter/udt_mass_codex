# F2 — Is {L2, L4} the COMPLETE, FORCED native matter action? — Analytic OBSERVE

**Mode:** OBSERVE, METRIC-LED, DATA-BLIND. Settling FOUNDATIONAL_ASSUMPTIONS_LEDGER F2.
Goal = the matter sector of a TRUSTWORTHY COMPLETE solver, NOT a spectrum match. No mass /
ratio / wall number loaded, consulted, or derived.
**Driver:** Claude (Opus 4.8, 1M context), 2026-06-21. **Compute:** CPU only, bounded sympy
(strain-eigenvalue algebra, inverse-metric shift weights). NO heavy solve.
**Status:** UNVERIFIED (no blind verifier pass yet) — record-candidate, not banked. NOT canon.
Scripts (/tmp, uncommitted): `f2_scale_checks.py`, `f2_scale_terms.py`, `f2_derrick.py`,
`f2_s2_4deriv.py`, `f2_areaform_V.py`, `f2_l6.py`.

Builds on (read to confirm): `angular_lagrangian_results.md` (+verifier; L2 unique 2-deriv,
L4 = |omega_H1|^2 native, blind-verified), `native_matter_step_results.md` (the coupled
soliton; Derrick necessity of L4), `udt_matter_source_MAP_results.md`,
`scale_symmetry_bootstrap_analysis_results.md` (the NEW depth-shift dilatation tool),
`CANON.md` C-2026-06-14-1 + refinement (the S^2 carrier; the explicit "ROBUST to native
additions: a Skyrme term, a potential V(n), or the eta-seal coupling" scope line).

---

## 0. THE QUESTION + THE ONE-LINE ANSWER

Is the native matter action {L2 + L4} **FORCED** (uniquely selected), **MINIMAL-BUT-NOT-
UNIQUE** (admissible extras survive), or **INCOMPLETE** (a principle requires a missing term)?

> **VERDICT: MINIMAL-BUT-NOT-UNIQUE.** {L2, L4} is *necessary* (L2 forced as the unique
> 2-derivative scalar; a 4-derivative term forced PRESENT by Derrick) and the *cleanest*
> choice (L4 is the only 4-derivative term with native area-form provenance). But it is
> **not the unique admissible action**: at least TWO further terms survive every forcing
> principle we can apply — **(i) a second, independent 4-derivative invariant `X^2`**
> (the squared-L2-density, admissible by invariance but NOT area-form-native), and
> **(ii) a 6-derivative area-current term `L6`** (admissible and area-form-native, just
> subleading). A **potential `V(n)` is the one candidate the principles actually FORBID**
> — killed by the full target-SO(3) isometry (the same symmetry that made L2 unique) —
> UNLESS the target symmetry is reduced by a separate structural posit (the seal/eta
> boundary object or a preferred axis). The new scale-symmetry tool does NOT discriminate
> among the angular terms (all are scale-neutral), so it does not force {L2,L4} either;
> its content is different (it identifies the angular sector as the scale-neutral one and
> time/radial gradients as the breakers).

So F2 is settled as **assembled-from-a-principled-but-non-unique-basis**, not forced. The
honest deliverable is the named list of survivors below.

---

## 1. THE ADMISSIBLE-TERM BASIS (enumeration, with provenance)

Field: unit 3-vector `n_a`, |n|=1, target S^2 (CANON C-2026-06-14-1). Build all diffeo-scalar,
target-isometry-covariant terms, organized by derivative order. `D_mu n` ≡ covariant gradient;
the strain tensor is `S_munu = D_mu n . D_nu n` (symmetric); on the 2-dim target it has at most
TWO nonzero eigenvalues `l1, l2 >= 0`.

| Term | derivative order | explicit form | provenance | chose/derived |
|---|---|---|---|---|
| **V(n)** | 0 | a target potential | FULL-SO(3) V = const (trivial); non-trivial V needs a preferred axis | admissible only if SO(3)→subgroup (posit) |
| **L2** | 2 | `(xi/2) g^{ab} D_a n . D_b n` = `(xi/2)(l1+l2)` | the UNIQUE 2-deriv diffeo+SO(3) scalar | **DERIVED-unique** (angular_lagrangian D3) |
| **L4_native** | 4 | `(kappa/4)|omega_H1|^2 ~ l1 l2` | = pullback-of-area-form squared (winding-current norm) | **DERIVED native + blind-verified** |
| **X^2** | 4 | `(g^{ab}D_a n.D_b n)^2 ~ (l1+l2)^2` | squared-L2-density; NOT an area-form pullback | admissible by (b); **NOT area-form-native** |
| **L6** | 6 | area-current^2, `B_mu B^mu ~ (l1 l2)^2`-type | = topological-current squared (area-form built) | admissible + area-form-native; subleading |

**The 4-derivative space is EXACTLY 2-dimensional on the S^2 target** (sympy, `f2_s2_4deriv.py`):
the symmetric strain has only two eigenvalues, so degree-2 invariants are spanned by
`{(l1+l2)^2, l1 l2}` = `{X^2, |omega_H1|^2}`. There is no third 4-deriv invariant (the
2-dim target caps the strain rank — the standard "two Skyrme invariants" statement, here
verified native rather than imported). **L4_native is the antisymmetric/Jacobian combination
`l1 l2`; `X^2` is the orthogonal symmetric combination `(l1+l2)^2` — a genuine SECOND admissible
4-derivative term that {L2,L4} omits.**

---

## 2. THE FORCING PRINCIPLES APPLIED (which term each kills/keeps)

### (a) THE SCALE (DEPTH-SHIFT) SYMMETRY — the new tool [the headline test]

Under the dilatation `phi -> phi + lambda` (CANON; scale_symmetry doc), the metric scales
`g_tt -> e^{-2lam} g_tt`, `g_rr -> e^{+2lam} g_rr`, **angular block unchanged**,
`sqrt(-g) -> unchanged` (B=1/A makes the depth factors cancel — sympy confirmed
`sqrt(-g) = c0 r^2 sin th`, phi-free). So a matter ACTION term `S = INT sqrt(-g) L`
scales ENTIRELY through the inverse-metric contractions in `L`:

```
g^tt weight e^{+2lam}  (time channel) | g^rr weight e^{-2lam} (radial) | g^ang weight 1 (angular, INVARIANT)
```

Per-channel shift weights (exponent of e^{lam}), `f2_scale_terms.py`:

| term | time channel | radial channel | **angular channel** |
|---|---|---|---|
| V(n) | 0 | 0 | **0 (invariant)** |
| L2 | +2 | −2 | **0 (invariant)** |
| L4 | +4 / 0 (t-r) | −4 | **0 (invariant)** |
| L6 | … | … | **0 (invariant)** |

**RESULT (the scale-symmetry forcing test):** for the purely-angular (transverse-winding)
hedgehog — the configuration the whole program uses — **EVERY derivative is angular, so
EVERY candidate term (V, L2, L4, L6) is scale-INVARIANT.** The depth-shift dilatation
**does NOT discriminate among the angular matter terms and therefore does NOT select
{L2,L4}.** This is a real (slightly negative) result: the new forcing tool, applied to F2,
does not narrow the basis.

What the scale symmetry DOES say about matter is structural, not selective:
- The **angular sector is the scale-NEUTRAL sector** — any number of angular-derivative
  invariants is scale-allowed (consistent with: an isolated angular soliton is a scale-free
  family, omega~1/R box-control; scale_symmetry doc Sec 2).
- The **breakers are the TIME and RADIAL gradient channels** (nonzero weights ±2,±4,…) —
  exactly the angular+time breakers the weight-derivation already flagged. So "matter is the
  scale-symmetry breaker" is carried by a term's TIME/RADIAL derivative content, not by which
  angular invariant it is. (Matter pins a length `l=sqrt(kappa/xi)` because the couplings
  xi,kappa are dimensionful — scale_symmetry verifier Claim 2 — not because the shift selects
  a term.)

> **(a) verdict: the scale symmetry FORCES nothing in F2 and FORBIDS nothing among the
> angular terms — all are scale-neutral. It is NOT the principle that selects {L2,L4}.**

### (b) TARGET-ISOMETRY (SO(3)/S^2) + DIFFEO INVARIANCE [the one that BITES]

This is the principle that made L2 unique (the only 2-deriv diffeo+SO(3) scalar). Applied
to the rest of the basis (`f2_areaform_V.py`):
- **L2, L4, X^2, L6: all PASS** (each is a diffeo + SO(3) scalar).
- **V(n): a FULL-SO(3)-invariant function of n (|n|=1) can only be CONSTANT** — trivial, no
  dynamics. A *non-trivial* potential (e.g. an easy-axis `1 - n_3`, the pion-mass analog)
  requires a PREFERRED target direction, i.e. it **breaks SO(3) → SO(2)**.

> **(b) verdict: the SAME target-isometry that forces L2's uniqueness FORBIDS a non-trivial
> V(n).** V survives ONLY if the native target symmetry is reduced below full SO(3) — which
> is a separate structural posit (the seal/eta boundary object is the candidate axis-breaker;
> CANON lists eta as a seal/boundary object, NOT a bulk potential). So **with the full target
> SO(3), V is killed; {L2,L4} loses no completeness to V.** This is the strongest forcing
> result of the audit.

### (c) THE H1 AREA-FORM STRUCTURE [the one that PROMOTES L4]

`omega_H1 = eps_abc n_a dn_b ^ dn_c` is the pullback of the S^2 target area 2-form; L4 = its
metric-norm. In strain eigenvalues `|omega_H1|^2 ~ l1 l2` (the Jacobian-squared / antisymmetric
combination). Among the two admissible 4-deriv terms:
- **L4_native = `l1 l2`** IS an area-form pullback → **NATIVE (selected by (c)).**
- **X^2 = `(l1+l2)^2`** is NOT built from the area form at all → admissible by (b) but
  **fails the area-form-provenance test (c): admissible-but-not-native.**

So **(c) is the principle that lifts L4 above the other 4-derivative invariant** — it gives
L4 its native provenance and demotes X^2 to "allowed but not native." It does NOT *forbid*
X^2 (X^2 still satisfies (a),(b),(d)); it only denies X^2 native status.

Does the area-form structure FORBID V? **No.** The winding charge `Q = (1/4pi) INT omega_H1 =
deg(n)` is purely topological (metric- and V-free); adding `INT sqrt(-g) V(n)` shifts the
profile/energy but cannot change the integer winding. So V is *compatible* with the
topological structure — V is killed by (b), not by (c).

> **(c) verdict: the area-form structure SELECTS L4 over X^2 (provenance), and is COMPATIBLE
> with (does not forbid) V and L6.** It is the principle that earns L4 its native badge.

### (d) DERRICK / STABILITY NECESSITY [forces a 4-deriv PRESENT, not L4 specifically]

Flat-space Derrick counting in D=3 space (`f2_derrick.py`): `E_k(L) ~ L^{3-k}` →
`E0(V)~L^3, E2~L^1, E4~L^{-1}, E6~L^{-3}`.
- `{L2 alone}`: `E~L^1`, monotone → collapses to L=0. **No soliton** (banked #43). FORBIDDEN.
- `{L2, V alone}`: both `~L^{+}` → both shrink. FORBIDDEN.
- A term rising as L→0 is REQUIRED to balance L2. **L4 (`L^{-1}`) qualifies — but so does
  L6 (`L^{-3}`).** `{L2,L4}`, `{L2,L6}`, `{L2,L4,L6}`, `{V,L4}`, `{L2,V,L4}` ALL pass.

> **(d) verdict: Derrick FORCES the PRESENCE of ≥1 higher-than-2-derivative term (so L2 alone
> is excluded — L4's CLASS is necessary) but does NOT uniquely pick L4, and does NOT forbid V
> once a stabilizer is present.** Combined with (c): of the stabilizer candidates, L4 is the
> area-form-native one — so (c)+(d) together make {L2,L4} the *natural minimal* stabilized
> action, but {L2,L6} and {L2,L4,L6} remain admissible alternatives/extensions.

---

## 3. SURVIVOR TABLE (each term × each principle)

| term | (a) scale | (b) SO(3) | (c) area-form | (d) Derrick | NET |
|---|---|---|---|---|---|
| **L2** | invariant | **unique 2-deriv** | (n/a) | needs partner | **FORCED present (unique 2-deriv)** |
| **L4** | invariant | pass | **native (selected)** | qualifies as stabilizer | **present + natively privileged** |
| **X^2** | invariant | pass | NOT native | qualifies as stabilizer | **SURVIVES as admissible non-native 4-deriv** |
| **L6** | invariant | pass | native (current^2) | not required, allowed | **SURVIVES (subleading, native)** |
| **V(n)** | invariant | **FORBIDDEN (full SO(3))** | compatible | shrinks alone | **KILLED by (b)** unless SO(3) reduced |

**Two terms survive every principle: `X^2` (admissible, non-native) and `L6` (admissible,
native-but-subleading).** One term is forbidden: `V(n)` (by the full target SO(3)). L2 and L4
are present-and-privileged but their privilege is provenance (c) + uniqueness/stability
(b),(d), NOT a uniqueness of the whole action.

---

## 4. WHAT THE SURVIVORS WOULD ADD (honest, data-blind)

- **`X^2` (the squared-L2-density, `(l1+l2)^2`):** a second 4-derivative coupling. It adds a
  SECOND independent 4-deriv scale beside kappa. Like L4 it stabilizes against Derrick collapse,
  but it is a DIFFERENT contraction (symmetric vs antisymmetric strain), so it changes the
  soliton PROFILE and hence the spectrum. It does NOT carry the winding-current/area-form
  meaning. Its omission from {L2,L4} is a CHOICE (cleanest-native), not a derivation.
  *(Note for later: like L4 it is purely-angular on the hedgehog, so by the
  angular_lagrangian verifier strengthening it also preserves T^t_t=T^r_r and does NOT break
  B=1/A — the EOS/B=1/A canon is unaffected; only the spectrum would move.)*
- **`L6` (area-current squared):** a 6-derivative term with genuine area-form/topological
  provenance. Adds a third scale; subleading at long range. Standard in Skyrme phenomenology;
  here it is admissible-and-native, just not required. Its omission is justified as
  "leading-order truncation," which is a legitimate but explicit modeling choice.
- **`V(n)` (IF the target symmetry is reduced):** would introduce a Compton-like mass scale
  for the angular field and a long-range exponential tail (changing the soliton size law from
  pure `sqrt(kappa/xi)`). Forbidden under full SO(3); admissible only with a named axis-breaker
  (the seal/eta is the candidate, but eta is canonically a BOUNDARY object, not a bulk V —
  so promoting it to a bulk potential would itself be a new posit to flag).

---

## 5. RECONCILIATION WITH THE EXISTING CORPUS

The existing CANON scope line for C-2026-06-14-1 already states: *"ROBUST to native additions:
a Skyrme term, a potential V(n), or the eta-seal coupling all preserve T^t_t = T^r_r (they
change T^theta_theta and the solid-angle-deficit value only). So B=1/A does NOT hinge on the
minimal-model choice; the SPECTRUM (masses) will, but the EOS does not."* This audit is
**consistent with and sharpens** that line:
- It confirms the corpus's own admission that {L2,L4} is a MINIMAL model on the EOS axis (the
  EOS/B=1/A is robust to additions; the SPECTRUM is the model-sensitive part).
- It ADDS the forcing analysis the corpus lacked: it NAMES the survivors (X^2, L6), shows the
  4-deriv space is exactly 2-dim on S^2, identifies (c) area-form as the principle that
  privileges L4, and — the one genuinely new constraint — shows (b) full-SO(3) FORBIDS the
  bulk V the corpus had listed as merely "robust-to." So the corpus over-counted V as a free
  admissible addition; under full target SO(3) it is actually forbidden in the bulk.
- The new scale-symmetry tool, applied here for the first time to F2, returns NEUTRAL on the
  selection question (all angular terms scale-invariant) — a clean negative for that tool's
  power over F2, recorded so it is not re-attempted hopefully.

---

## 6. PREMISE LEDGER (chose / derived)

| # | premise / claim | status |
|---|---|---|
| F2-1 | Field = unit 3-vector n, target S^2 (the carrier) | DERIVED (CANON C-2026-06-14-1) — itself an upstream posit, not re-opened here |
| F2-2 | sqrt(-g)=c0 r^2 sin th, phi-free (B=1/A) | DERIVED (sympy, this push) |
| F2-3 | shift weights: g^tt→e^{+2lam}, g^rr→e^{-2lam}, ang→1 | DERIVED (from CANON metric, this push) |
| F2-4 | all purely-angular terms (V,L2,L4,L6) scale-invariant | DERIVED (this push) — the (a) neutral result |
| F2-5 | 4-deriv space on S^2 is EXACTLY 2-dim {X^2, |omega|^2} | DERIVED (strain-eigenvalue algebra, sympy) |
| F2-6 | L4 = |omega_H1|^2 = `l1 l2` = area-form pullback (native); X^2 not | DERIVED (this push) + upstream blind-verified |
| F2-7 | full-SO(3) V(n)=const; non-trivial V breaks SO(3)→SO(2) | DERIVED (this push) — the (b) forbidding result |
| F2-8 | Derrick: ≥1 higher-deriv stabilizer REQUIRED; L4 not unique | DERIVED (Derrick counting; #43 banked) |
| F2-9 | winding Q topological, V- and metric-free (V doesn't spoil topology) | DERIVED (standard, restated) |
| C-F2-a | Derrick used as FLAT-SPACE surrogate (the curved/coupled Derrick could shift coefficients) | CHOSE (tractability) — counting verdict robust, exact balance not |
| C-F2-b | "full target SO(3) is the native symmetry" (the load-bearing premise for forbidding V) | CHOSE/inherited — it is the SAME assumption L2's uniqueness rests on; if the carrier's native symmetry is actually reduced, V re-enters |
| C-F2-c | restricted to the S^2 (pi_2) carrier; the S^3/SU(2) carrier tension (open corpus reconciliation) not re-litigated here | SCOPE |

---

## 7. VERDICT (one paragraph)

**{L2, L4} is MINIMAL-BUT-NOT-UNIQUE, not FORCED.** L2 is forced (unique 2-derivative
diffeo+SO(3) scalar); a 4-derivative stabilizer is forced PRESENT by Derrick; and among the
exactly-two 4-derivative invariants on the S^2 target, the H1 area-form structure NATIVELY
privileges L4 = |omega_H1|^2 over the orthogonal X^2 = (L2-density)^2. So {L2,L4} is the
**cleanest, most-native minimal stabilized action** — that is a real positive. But it is **not
the unique admissible action**: the second 4-derivative invariant **X^2** (admissible by
invariance, just not area-form-native) and the 6-derivative area-current term **L6** (admissible
AND native, merely subleading) both survive every forcing principle and would each move the
SPECTRUM (not the EOS / B=1/A, which is robust). The one term the principles genuinely FORBID is
a bulk potential **V(n)** — killed by the full target SO(3), the very symmetry that made L2
unique — unless the target symmetry is deliberately reduced by a separate posit (the seal/eta
axis), which would itself need flagging. The **new scale-symmetry tool returns NEUTRAL** on F2
(every purely-angular term is scale-invariant; the shift's content is to mark the angular sector
scale-neutral and time/radial gradients as the breakers, not to select a term). **F2 therefore
resolves as: the matter action is ASSEMBLED from a principled but non-unique basis — necessary
core {L2, L4}, two named admissible extras {X^2, L6}, one forbidden term {V(n) under full SO(3)}
— and the spectrum-relevant incompleteness is the choice to truncate at {L2,L4}, made explicit
here rather than left implicit.** This is the honest middle answer the task asked for; the
clean "unique" was not available and was not manufactured.

---

## 8. ATTACK HERE (for a blind verifier)

1. **The (a) neutral result.** Re-derive the inverse-metric shift weights and confirm EVERY
   purely-angular term is scale-invariant (so the scale symmetry does NOT select {L2,L4}). Check
   whether the RADIAL-gradient piece of a realized (twisted) soliton — which DOES carry a g^rr
   (weight −2) — gives the scale symmetry any residual selecting power once Theta'(r) ≠ 0. (My
   claim: it makes the term a breaker, not a selector — verify.)
2. **The (b) V-forbidding result (load-bearing).** Confirm a full-SO(3)-invariant V(n) with
   |n|=1 is necessarily constant, so any non-trivial V breaks the target symmetry. Then judge
   whether the corpus's "robust to a potential V(n)" line (CANON scope) should be re-scoped to
   "V is forbidden in the bulk under full SO(3); admissible only with an axis-breaker."
3. **The exactly-2-dim 4-deriv space (F2-5).** Re-derive via strain eigenvalues that on a 2-dim
   target the degree-2 invariants are spanned by `{(l1+l2)^2, l1 l2}` — exactly two — so X^2 is a
   genuine second admissible term and there is no third. (Guard against a hidden third invariant
   from covariant-derivative-of-strain terms that might IBP to lower order.)
4. **The X^2 vs L4 provenance split (c).** Confirm `l1 l2` is the area-form pullback (Jacobian)
   and `(l1+l2)^2` is not built from the area form — i.e. (c) genuinely distinguishes them.
5. **Derrick robustness (d).** The counting is flat-space; check the curved/coupled Derrick does
   not change WHICH terms can stabilize (only coefficients), so the "L4 not unique stabilizer"
   conclusion survives the actual UDT background.

---

## VERIFICATION (2026-06-21) — blind adversarial pass, agent a4aa12aa522f06b6c
SUPPORTED (verdict honest, not over/under-claimed). Independent sympy recompute.
- **B1 (4-deriv space exactly 2-dim {X^2, |omega_H1|^2}): SUPPORTED — with a SCOPE TAG:** true for invariants
  built ALGEBRAICALLY from the first-derivative strain S_munu=Dn.Dn (the standard Skyrme basis); 4-deriv scalars
  involving SECOND derivatives (e.g. (box n)^2) are non-strain-algebraic and lie outside this count. Read "no
  third" as strain-class, not literally all 4-derivative scalars. (Scope tag, not a refutation.)
- **B2 (V(n) FORBIDDEN under full SO(3)): SUPPORTED** (most-attacked claim, survives). SO(3) acts transitively
  on S^2; the only invariant of a unit vector is |n|^2=1, so any invariant V is CONSTANT — non-trivial V is
  genuinely impossible under full SO(3) (re-enters only if reduced to SO(2)). The corpus correction stands.
- **B3 (scale symmetry NEUTRAL on angular-term selection): SUPPORTED** (correct negative result).
- **B4 ({L2,L4} MINIMAL-BUT-NOT-UNIQUE): SUPPORTED.** Necessary core {L2,L4}; admissible extras {X^2, L6}
  (move masses, not the EOS/B=1/A); V forbidden under full SO(3). Declines a false "unique" — calibrated.
LOAD-BEARING PREMISE (verifier): the verdict rests on the carrier target being FULL SO(3) (same assumption L2's
uniqueness already uses); if the target symmetry is reduced, V re-enters.
