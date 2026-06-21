# Seal Junction Condition — the sigma-ODD / TIME-ON sector (F4 frontier)

**Mode:** OBSERVE, DATA-BLIND, analytic (CPU sympy/mpmath, no heavy solve).
**Created:** 2026-06-21. **Author:** Claude Opus 4.8 (1M).
**Frame:** F4_seal_boundary_MAP.md §4A — the missing junction condition for the
sigma-ODD / time-on sector, for BOTH candidate involutions. NOT canon.
**Script:** `seal_junction_timeon_check.py` (12 analytic checks, all recorded).
**Reuses (does not edit):** `w7_a_mirror_bc.py` (the sigma-EVEN/Neumann method),
`topo_d3_junction.py` (the actual-parity correction).

---

## 0. ONE-PARAGRAPH ANSWER

The sigma-EVEN seal junction was already computed and gave Neumann / a CONTINUOUS
spectrum. This work computes the **never-before-derived sigma-ODD / time-on** junction,
for BOTH the adopted involution (sigma1 = t→−t) and the competing one (sigma2 = P×T).
**Result: BOTH involutions give a CONTINUOUS seal BC — neither imposes a fixed-radius
discrete-omega quantizer.** Under sigma1 the time-on seal condition is a NODE IN TIME
(`H(seal)=0`, `sin(ωt)`-parts vanish at t=0) that is satisfied for EVERY ω, selecting
none. Under sigma2 the arm is REGRADED to even/Neumann and the seal becomes a radial
method-of-images reflection at the wall, giving a HARMONIC ladder `ω_n ∝ 1/R_cell` that
still slides with the (unpinned, F7) cell radius. **F4 CLOSES analytically for the
seal-as-classical-quantizer question** — the physical seal does NOT rescue a classical
discrete spectrum, making "must-quantize" unconditional with respect to the seal BC.
The F4 *solve* (4B) is therefore **NOT warranted** as a discreteness rescue. (Honest
hinge preserved: the one live nonzero-source possibility selects spinor STATISTICS, not
a discrete mass — a quantum datum, not a classical quantizer.)

---

## 1. THE FIELD CONTENT AND THE TWO INVOLUTIONS

**Time-live field content** (from STEP2 / P5e):
- metric diagonal **A(r), B(r)** (the `g_rr`, and `g_tt = −e^{2φ}` shape) — spatial,
  no bare `dt`-index beyond the `dt²` slot;
- the **time-row off-diagonal H = g_tr** (one `dt`-index) — the channel STEP-2 gauged
  away and P5e found "LIVE dynamically, pinned=0 statically as a gauge mode";
- **φ(t,r)** (sits in `g_tt dt²`);
- **Θ(t,r)** (the hedgehog charge field; static profile Θ(0)=π, Θ(seal)=0);
- the oscillatory content **e^{iωt}** of every time-on fluctuation.

**Involution 1 (adopted, W6 same-minus):** `σ1 : t → −t`. On the metric arm this is
`(a,b) = (g_tr, g_tθ) → (−a,−b)` (`w7_a_mirror_bc.py` A2/B1); the fixed surface of T.
**Involution 2 (competing, on record):** `σ2 : P×T` — a spatial reflection P composed
with T (`fermion_forcing_verifier_results.md:91-92`: "a different involution (P×T)
would regrade … a DIFFERENT seal").

**CRITICAL FRAME NOTE (load-bearing, surfaced for the verifier).** The W6 *fold* lives
at the **spatial** crease D=0 (`D = r²W − fq²`), and the canon seal (C-2026-06-10-2) is
a **spatial/radial** boundary (mirrored across φ→−φ at the φ=0 interface). But the W6
*involution acting at that crease* is read as **time-reversal** (`w7_results.md:52-54`).
So the seal is a SPATIAL surface whose gluing symmetry is (read as) temporal. This is
exactly the row-conditional grade (d) in the F4 MAP. The analysis below holds the seal
at its spatial location and asks what each involution's parity assignment does there —
which is the honest reading and the one that actually bears on the radial spectrum.

---

## 2. FIELD PARITIES — derived, per involution

Parity is forced by requiring `ds²` invariant under σ (the same theorem used for the
sigma-EVEN result; `fermion_forcing_results.md` P3, `w7_a_mirror_bc.py` B1). Each `dt`
under T:t→−t contributes one sign; each `dr` under P:r→(reflected) contributes one sign.

| Field | slot | σ1 = t→−t | σ2 = P×T (P = radial fold) |
|---|---|---|---|
| **A, B** (spatial diagonal) | `dr²`, `dt²` shape | EVEN → **Neumann** | EVEN → **Neumann** |
| **φ(t,r)** (in `g_tt dt²`) | two `dt` | **EVEN → Neumann** | EVEN (two dt) → Neumann |
| **H = g_tr** (the arm) | one `dt`, one `dr` | **ODD → Dirichlet** | **EVEN → Neumann** (dt·dr both flip) |
| **Θ static hedgehog** | scalar, no `dt` | EVEN → Neumann | EVEN → Neumann |
| **δΘ time-on fluctuation** | `cos(ωt)` / `sin(ωt)` | cos EVEN, **sin ODD → Dirichlet** | regraded with the spatial fold |
| **e^{iωt}** | → e^{−iωt} | cos EVEN, sin ODD | cos EVEN, sin ODD (T part) |

**The key regrade (verified `[4b]`):** the arm `g_tr dt dr` carries BOTH a `dt` and a
`dr`. Under σ1 (only `dt` flips) it is **ODD**. Under σ2 = P×T (both `dt` and `dr` flip)
it is **EVEN**. This is the "P×T would regrade" fact, now made explicit: the time-on
sector that is Dirichlet-pinned under σ1 becomes Neumann-free under σ2.

---

## 3. THE SEAL BC ON THE TIME-ON SECTOR — explicit, per involution

### Involution 1 (σ1 = t→−t) — the adopted reading

The sigma-ODD fields are `{H, sin(ωt)-parts of every fluctuation}`. The derived
dichotomy (σ-ODD → Dirichlet) gives the **explicit seal BC**:

```
    H(seal) = 0                     (the arm vanishes at the seal)
    [sin(ωt) parts](seal) = 0       (odd-in-time fluctuations node at t=0)
    d_n φ(seal) = 0,  d_n A = d_n B = 0,  d_n Θ_static = 0   (even → Neumann)
```

**This is a NODE IN TIME at the fixed surface t=0**, NOT a radial eigen-condition.
Checks `[2c][2d]`: `sin(ω·0) = 0` identically in ω — the condition is satisfied for
EVERY ω and selects NONE. The even/cos sector's Neumann condition
`d_t cos(ωt)|₀ = −ω sin(0) = 0` is likewise automatic. **VERDICT: CONTINUOUS in ω.**
The omega-spectrum is then set entirely by the OUTER RADIAL wall (r=R) — exactly the
generic Dirichlet box the four solves scanned — so it remains `ω ~ n/R`, box-controlled
(`[3a]`). σ1's seal does NOT rescue a fixed-radius spectrum.

### Involution 2 (σ2 = P×T) — the competing reading

Here the arm H is regraded to EVEN (Neumann). The genuinely-new content is that P (the
spatial/radial fold about the wall) makes the seal a **radial reflection junction at the
physical wall r=R** — a method-of-images doubling of `[0,R]` to `[0,2R]` with a
reflection at R. The **explicit seal BC** is the reflection (Neumann for even radial
modes, Dirichlet for odd):

```
    even radial sector:  d_r(field)(R) = 0     -> ω_n = nπ/(2R)
    odd  radial sector:  field(R) = 0          -> ω_n = (n+½)π/(2R)
```

Checks `[4c][4d]`: this is a **HARMONIC ladder** with spacing **∝ 1/R_cell**. It is a
genuine discrete *set* at fixed R, but (i) it is harmonic (1:2:3…, the wrong pattern —
F4 counter-weight §5.1) and (ii) it **slides with R_cell**, which is NOT natively pinned
(F7, ~10⁴⁰ autonomy gap). So under any legitimate physical-size variation the whole
ladder rescales — it fails the F4 "box-vs-physical" gate. **VERDICT: CONTINUOUS in
scale** (a box-like harmonic ladder, not a fixed-radius non-harmonic quantizer).

---

## 4. THE QUANTIZER TEST — where a discrete spectrum could have hidden

A genuine fixed-radius quantizer needs a **Robin/antiperiodic** seal condition
`α·field + β·d_n field = 0` whose ω-set is **R-INDEPENDENT**. Check `[5a]`:

- **σ1** → a time-node, ω-independent (selects no ω);
- **σ2** → a radial reflection, R-scaled (selects no fixed ω).

**Neither involution yields such a condition.** Both reduce to either a trivially-
satisfied time node or a box-scaled harmonic reflection. There is no seal-sourced
Robin term that would pin a discrete ω at a fixed physical radius. This is the same
structural outcome as the ONE previously-computed junction (σ-EVEN/Neumann/ρ-flat,
`h1_types_results.md:108-110`: "glues the datum SYMMETRICALLY with NO normal-derivative
constraint that would discretize the value") — now confirmed to extend to the σ-ODD /
time-on sector under BOTH involutions.

### The honest hinge (preserved, `[5b]`)

`fermion_forcing_results.md:273-275` named one open fact: IF the forced σ-ODD source has
a **required-nonzero seal value**, a single-valued odd boson is Dirichlet-pinned to a
node, forcing **antiperiodicity (T²=−1)**. Honest read: that antiperiodicity is a
**spinor / statistics selector** (a 2-valued double cover), **NOT an ω-quantizer**. It
would pick fermionic statistics, not a discrete mass set. So even if that hinge closes
"nonzero," the CLASSICAL ω-spectrum stays continuous — consistent with, not contrary to,
must-quantize. (Whether the source is forced nonzero remains the named open computation;
it does not change the quantizing-vs-continuous verdict for the classical spectrum.)

---

## 5. VERDICT

| Involution | σ-ODD seal BC on the time-on sector | Quantizing or Continuous? |
|---|---|---|
| **σ1 = t→−t** (adopted) | `H(seal)=0`, `sin(ωt)`-parts node at t=0 (Dirichlet-in-time); even fields Neumann | **CONTINUOUS** — time node, ω-independent; radial wall still sets ω~n/R |
| **σ2 = P×T** (competing) | arm regraded EVEN/Neumann; radial reflection at r=R (Neumann even / Dirichlet odd) | **CONTINUOUS** — harmonic ladder ∝1/R, slides with unpinned R_cell |

**BOTH give CONTINUOUS** (matching the already-computed σ-EVEN result). Therefore:

- **F4 CLOSES analytically** for the seal-as-classical-quantizer question. The physical
  seal — under either candidate involution, for the σ-ODD/time-on sector that was never
  before imposed — does NOT impose a discrete-spectrum BC at a fixed physical radius.
- **The F4 solve (4B) is NOT warranted** as a discreteness rescue. The analytic close at
  4A is exactly the cheap outcome the MAP anticipated (§4 interrogation tag: "if the
  derivation shows the seal imposes a plain symmetric value-glue with no normal-derivative
  constraint … the answer may be 'no change' BEFORE any solve").
- This makes the session's **"must-quantize" verdict unconditional with respect to the
  seal BC** — the one load-bearing caveat the F4 MAP flagged is resolved in the
  "continuous" direction.

**What WOULD still warrant a solve (scoped, not now):** only a THIRD structure not on
record — e.g. the parked S²×S¹ second-seal doubling (F0 D2), which gives an integer
Chern family rather than a reflection ladder — could change this. That is a different
*container* (a topology choice, §6.3 of the MAP), NOT the seal BC, and is out of scope
here. The seal *junction condition itself*, for both involutions on record, is settled
continuous.

---

## 6. PREMISE LEDGER (chose / derived)

| # | Premise / choice | Status | Note |
|---|---|---|---|
| L1 | σ1 = t→−t acts on the arm as (a,b)→(−a,−b); fixed surface t=0 | **DERIVED** | `w7_a_mirror_bc.py` A2/B1, reused exactly. |
| L2 | σ-parity from `ds²`-invariance (one sign per dt/dr index) | **DERIVED** | `fermion_forcing_results.md` P3; standard junction theorem. |
| L3 | σ-EVEN→Neumann, σ-ODD→Dirichlet dichotomy | **DERIVED** | `w7_results.md:57-58`; the method this work extends to the odd sector. |
| L4 | H=g_tr is σ1-ODD, σ2-EVEN (the regrade) | **DERIVED** | dt·dr index count; `[4b]`. The competing-involution fork made explicit. |
| L5 | σ2's P = **radial fold about the wall r=R** | **CHOSE** | A concrete reading of "P" giving the seal a radial action. A different P (e.g. through-core) would relocate but not de-harmonicize the ladder; flagged. **← verifier eye.** |
| L6 | The seal sits at a fixed SPATIAL location; the involution acting there is read temporal | **DERIVED-conditional** | The row-conditional grade (d). The whole "which involution" fork (F4 MAP §6.1) is held OPEN by running both. |
| L7 | Cell radius R not natively pinned | **OPEN (F7)** | The ~10⁴⁰ autonomy gap; why even σ2's discrete ladder is scale-continuous. |
| L8 | "nonzero forced source ⇒ antiperiodicity" hinge | **OPEN, named** | `fermion_forcing_results.md:273-275`; affects statistics, NOT the classical ω-spectrum. |

**Analytic-settled vs needs-the-solve:** the parities (L1-L4), the explicit seal BCs
(§3), and the quantizing-vs-continuous verdict (§5) are **analytic-settled** — no solve
needed; this is the cheap close. **Needs-no-solve** for the seal-BC question. A solve
would only be warranted for a *different container* (S²×S¹, L5-alternative P, or a
not-on-record involution), which is out of F4-seal-BC scope.

**Honest counter-weights carried (from F4 MAP §5):** (1) harmonic-ladder triviality —
even σ2's discrete ladder is 1:2:3 (wrong pattern); (2) F7 — R not pinned, so the ladder
predicts nothing absolute; (3) the one prior computed junction was already flat/Neumann.
All three POINT THE SAME WAY as this work's verdict (continuous), strengthening it.

---

## ATTACK-HERE (for the blind adversarial verifier)

1. **The load-bearing premise: is the σ1 seal a TIME surface (t=0) or a RADIAL surface?**
   If the seal is genuinely RADIAL (canon C-2026-06-10-2 mirrors across φ→−φ at the φ=0
   *interface*, a radial location; the W6 fold is at D=0, a *spatial* crease), then a
   σ1 = t→−t involution acting at a *spatial* surface is geometrically odd: t→−t fixes
   t=0 (a temporal slice), not a radial surface. **Resolve:** does the W6 reading place
   the seal at t=0 or at D=0(r)? If at D=0(r), then σ1's "time reversal" is a gluing
   symmetry of the radial crease (the two mirror cells share the crease and are related
   by t→−t), in which case the parity assignment still applies to fields AT that radial
   crease — but re-examine whether the Dirichlet-in-time conclusion (`sin(ω·0)=0`)
   transfers, since the node would be in t at a *fixed r=crease*, not at t=0 globally.
   **This is the single point most likely to flip the verdict** and is graded
   DERIVED-conditional (L6). Charles flagged exactly this as the open fork (MAP §6.1-6.2).

2. **σ2's P choice (L5):** I took P = radial fold about r=R. Try P = inversion through
   the core, or P = the angular antipode. Does any P give the arm a parity that produces
   a Robin (not Neumann/Dirichlet) radial condition with an R-INDEPENDENT ω? If yes, σ2
   could quantize and the solve IS warranted.

3. **Is "Dirichlet-in-time = no ω selection" too quick?** A Dirichlet node in time at a
   single instant t=0 on a finite *time* domain `[−T,T]` (if the cell is also temporally
   finite) would, with a SECOND temporal seal, give `ω_n = nπ/(2T)` — a temporal box
   ladder. Check: is the cell temporally finite (two time-seals)? If so the time node
   DOES quantize ω (∝1/T) — but still box-controlled in T (same F7 disease). Confirm the
   verdict survives (it should: still scale-sliding), but the reasoning in §3 changes.

4. **The regrade (`[4b]`):** verify `g_tr dt dr` is EVEN under P×T and ODD under T by an
   independent index count. If the arm is actually ODD under both, σ1 and σ2 do not
   differ and the "run both" gate collapses to one case.

5. **Did I smuggle "continuous" because it's the must-quantize-friendly answer?** The
   discipline was OBSERVE-not-target. Counter-check: the σ2 reflection junction DID
   produce a discrete set (`ω_n = nπ/2R`) — I called it continuous only because it slides
   with R (F7). If Charles rules R is physically pinned, σ2 becomes a genuine QUANTIZER
   and the verdict flips to "warrant the solve." The verdict is **conditional on F7
   staying open** — state that loudly.

---

## VERIFICATION (2026-06-21) — blind adversarial pass, agent a7945cd9a367aa488
SUPPORTED — F4 genuinely CLOSES (central conclusion confirmed + STRENGTHENED). Independent recompute of every
load-bearing piece (provenance of w7/topo_d3 scripts checked, no fabricated citations).
- **H=g_tr parity (THE load-bearing fact): SUPPORTED** — independent index-count + a covariant rank-2 Jacobian
  route both reproduce: g_tr ODD under sigma1=t->-t (Dirichlet), EVEN under sigma2=P×T (Neumann); A,B,phi,Theta
  EVEN under both. The verdict does not rest on an inverted parity.
- sigma1 time-node does NOT quantize omega: SUPPORTED (sin(omega*0)=0 identically in omega; the node sits at the
  symmetry-fixed point of the odd coordinate -> no constraint; unlike a SPATIAL node sin(kR)=0). Continuous,
  box-controlled by the outer radial wall.
- sigma2 harmonic ladder omega_n=n*pi/(2R) ∝ 1/R: SUPPORTED (generic 1-D box ladder, 1:2:3, NOT a non-trivial
  fixed-radius quantizer).
- **must-quantize UNCONDITIONAL regardless of F7: SUPPORTED — the doc UNDERSTATED it.** Even if R_cell is PINNED
  (F7 closed), sigma2 gives only a HARMONIC ladder — pinning fixes the scale, NOT the pattern (still 1:2:3), which
  is not the observed non-harmonic mass pattern. **CORRECTION to this doc's ATTACK-HERE #5 ("verdict flips to
  warrant the solve if R pinned"): TOO GENEROUS — even pinned, the seal can only produce a trivial harmonic
  ladder, so NO solve is warranted as a rescue of the observed spectrum.** Honest split: "seal gives no discrete
  set AT ALL" is F7-conditional; **"seal gives no spectrum matching OBSERVATION" is UNCONDITIONAL.**
- time-surface vs radial-crease fork: PARTIAL — verdict survives EITHER reading (radial-crease + t->-t still acts
  only on the time label -> Dirichlet on which time-mode survives, NOT a radial sin(k r_c)=0 quantizer; the
  radial-action branch = sigma2's harmonic ladder). Neither yields a non-harmonic fixed-radius quantizer. The
  fork does not flip the verdict (the clean "sigma1 = pure time node" phrasing is contingent on the temporal
  reading; held DERIVED-conditional).
- No isometric P yields a mixed Robin (R-independent) condition; a Robin would need a derived surface source,
  correctly left open as the statistics hinge (T^2=-1 antiperiodicity selects spinor STATISTICS, a QUANTUM datum,
  NOT a classical omega-ladder).
BOTTOM LINE: BANK. F4 CLOSES — the seal is NOT a non-trivial classical quantizer under either involution on
record. **"Must-quantize" is now UNCONDITIONAL with respect to the seal BC for the observed (non-harmonic)
spectrum** — the load-bearing F4 caveat under the central conclusion is RESOLVED.
