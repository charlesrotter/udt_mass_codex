# M10 / M11 CLOSURE RECORD — the S²-vs-S³ object identity + the cos-θ texture

**Mode:** OBSERVE, METRIC-LED, DATA-BLIND (no mass / ratio / spectrum / wall number loaded,
computed, or compared — grep-confirmed on this doc and the scripts re-run). CPU sympy, bounded,
single process. READ-ONLY on all committed docs; this is the only new file.
**Driver:** Claude Opus 4.8 (1M), agent for udt_mass_codex. **Date:** 2026-06-21. **NOT canon.**
**Status:** record-candidate (reconciliation + re-run of the existing committed scripts; the
underlying settle already carries a passing blind verifier — see §1). NOT itself a fresh blind pass;
ATTACK block invites one.

Closes the M10/M11 rows of FOUNDATIONAL_ASSUMPTIONS_LEDGER.md to a CLEAN state per Charles's
"finish everything." Read with: `S2_S3_OBJECT_IDENTITY_MAP.md`, `s2_s3_identity_results.md` +
`s2_s3_identity_VERIFIER.md`, `fourth_component_sourced_results.md` (the FAILED prior attempt),
`F0_SYSTEMATIC_AUDIT_results.md` (the row that flagged "unexecuted"), `F2_matter_action_forcedness_results.md`
(rides the S² target), `native_dilation_weight_derivation_results.md` + `matter_regrade_derived_operator_results.md`
(used S² as given), `CANON.md` C-2026-06-14-1.

---

## 0. THE HEADLINE RECONCILIATION (the thing F0 got wrong)

F0 (M10) flagged the S² settle as **"the dedicated settling MAP is same-day and UNEXECUTED; a prior
settling attempt FAILED its verifier (permits ≠ demands)."** That flag is **factually incorrect**, and
this is the central finding of this closure. The git/file record is decisive:

| time (2026-06-19) | event |
|---|---|
| 22:48 | `S2_S3_OBJECT_IDENTITY_MAP.md` committed (the MAP F0 saw) |
| 22:53–22:58 | `s2_s3_identity_derive.py` / `_stability.py` / `_texture.py` written + run |
| **23:00** | **`s2_s3_identity_results.md` committed** — the EXECUTED settle (commit "Settle S2-vs-S3 object identity (facet B) = S2") |
| **23:07** | **`s2_s3_identity_VERIFIER.md`** — independent blind adversarial verifier, NET VERDICT **"the S² settle STANDS. 'No fork' is correct."** |
| 2026-06-21 07:47 | F0 audit committed — flags the settle "UNEXECUTED" |

So the settle was **executed AND blind-verified two days BEFORE F0**. F0 conflated the 22:48 MAP with
the executed-and-verified results that landed an hour later, and inherited the stale tripwire from the
*earlier, genuinely-failed* attempt (`fourth_component_sourced_results.md`, 2026-06-18) — a different
document. The P2 MAP's ledger line 65 ("RESOLVED = S², DEMANDS-level, blind-verified 2026-06-19;
s2_s3_identity_results.md + _VERIFIER.md") was **correct**; F0's "CLAIMED-DERIVED-BUT-UNSHOWN" tag and
the ledger's "OPEN-ish / unexecuted-settling caveat" (line 45) are **stale and should be retired**.

I re-ran the three committed scripts and independently reproduced their load-bearing outputs (§1–§2 below).

---

## 1. M10 — IS THE MATTER CARRIER S² OR S³? — **SETTLED = S² (DEMANDS-level, blind-verified)**

The native L2+L4 action does **not source a stable 4th component**. The matter object is the **unit
3-vector (S²)**. This is a genuine DEMANDS (necessity), not a permits, on three independent legs — and,
crucially, it survives BOTH inflation directions (the lesson from the failed prior attempt). I
reproduced each leg with sympy this session.

### (i) STRUCTURAL — the native L4 is intrinsically 3-component (a theorem)
The canon native four-derivative term is built from the 3-vector cross product
`F_mn = ε_abc n_a ∂_m n_b ∂_n n_c` (CANON C-2026-06-14-1, `native_skyrme_derive.py`). `ε_abc` is a
**3-index** symbol — STRUCTURALLY BLIND to any n_4 (n_4 appears nowhere in F). Reproduced:
`∂L4_native/∂(∂_μ n_4) ≡ 0` for all μ. The only L4 that "sees" n_4 is the **non-native
Lagrange-identity** form (the imported S³ route). *(Correction inherited from the verifier: the doc's
footnote "Lagrange-L4 has ∂/∂n_4 = 0" is FALSE — a sympy `real=True` symbol-mismatch bug; the
Lagrange-L4 genuinely depends on n_4. NOT load-bearing — the verdict rests on the NATIVE L4's
blindness, which is verified-true. Recommend correcting that one footnote in the source doc.)*

### (ii) DYNAMICAL — no native term holds a finite n_4; the only n_4 motion DESTROYS the object (the crux)
With a fully-live 4th-component angle X(r) (X=0 ⇒ S², X live ⇒ S³), the X-direction potential
(reproduced exactly this session, `s2_s3_identity_stability.py`):
- `dV/dX|_{X=0} = 0` (X=0 IS a critical point), and
- **`d²V/dX²|_{X=0} = −4π(2κm² + r²ξ(m²+1))·e^{A+B}/r² < 0`** (all coefficients positive) — so **X=0 is
  a MAXIMUM**, and `d²V/dX²|_{X=π/2} = +4π ξ(m²+1)·e^{A+B} > 0` is the minimum.

The DEMANDS reading (and the reason this is NOT the failed permits-argument): X=0 being unstable does
NOT mean n_4 is sourced. The only downhill direction (X: 0→π/2) drives `n → (0,0,0,1)`, the **trivial
constant map** — the 3-vector amplitude `|cos X| → 0`, so the (θ,ψ) winding COLLAPSES and the S²
charge `Q = 4πm·cos³X → 0` (charge-destroying). This is the textbook global-monopole/O(4) σ-model
**unwinding-to-vacuum** instability, NOT the nucleation of a stable S³ soliton. The verifier independently
confirmed (own orthogonal Y(r) parametrization) that the would-be S³ minima sit at **|Y*|² = 1 +
r²ξ(m²+1)/(2κm²) > 1 — OUTSIDE the unit ball |n_4|≤1**, i.e. non-physical; inside Y∈[−1,1] the only
critical point is Y=0 and V decreases monotonically to the |Y|=1 vacuum. Even **L4 alone** produces no
interior S³ well. So: **charged matter is DEMANDED to sit at n_4=0 (S²); a finite n_4 can only be
IMPOSED by an external boundary condition** (the Skyrme Θ(core)=m·π import).

> NOTE on a cosmetic blemish (verifier-flagged, re-confirmed this session): the printed "VERDICT LOGIC"
> boilerplate in `s2_s3_identity_stability.py` is written for the *minimum* (d²V>0) case while the
> *computed* curvature is negative (maximum). The script's print text reads awkwardly against its own
> number, but the RESULTS DOC §1(ii) reasons the maximum case correctly (via charge destruction). Math
> and verdict are correct; only the script's print boilerplate is mismatched.

### (iii) SYMMETRY — the metric supplies no S³ isometry / no π₃-protecting field
`#50` (su3_field_test, blind-verified): the metric connection is U(1)×SO(3)×SO(3,1). The only internal
rotation is **SO(3) = Isom(S²)**; there is NO metric-supplied SU(2) = Isom(S³). The symmetry that would
protect/source a π₃ object is natively absent.

### Both inflation directions refuted (the tripwire that killed the prior attempt)
- **permits→is** (the prior failure): AVOIDED. S² is "no native source/stabilizer for finite n_4 + the
  only n_4 motion annihilates the charge" — a DEMANDS, not "the EOM permits X=0."
- **unstable→S³**: ALSO refuted. The instability is charge-destroying unwinding to the trivial vacuum,
  not S³-nucleation (Q=4πm·cos³X → 0; would-be S³ minima non-physical at |Y*|>1).

### Why the prior attempt failed, and why this one does NOT
The 2026-06-18 `fourth_component_sourced_results.md` was killed by its verifier on TWO grounds: (a) the
slice→frame inflation ("EOM permits Θ=π/2" → "object IS S²"); (b) its conditional on `r_core=0.05`
being a CHOSEN cutoff, and its Axis-C break — the **energy minimizer SWEEPS given the BC Θ(core)=m·π**.
The 2026-06-19 settle defuses BOTH: (a) it argues from absence-of-source + charge-destruction
(DEMANDS), never from "permits"; (b) it does NOT rely on r_core — the would-be S³ minima are
non-physical (|n_4|>1) on the WHOLE domain independent of r→0 (§4 of the source doc scopes r→0 as
decoupled). The Axis-C objection — "the minimizer sweeps given Θ(core)=m·π" — is itself answered:
Θ(core)=m·π **IS** the imported S³ assumption; with the BC NOT imposed, no native term holds the sweep.
That is exactly the permits/demands distinction the failed attempt missed.

> **M10 DISPOSITION: SETTLED = S² (DEMANDS-level, blind-verified 2026-06-19).** Carrier target is the
> unit 3-vector / π₂ area form. S³ is NEVER native — it enters ONLY via (a) the Lagrange-identity L4 and
> (b) the Skyrme baryon BC Θ(core)=m·π (both imports; provenance below). Retire the F0
> "unexecuted/CLAIMED-DERIVED-BUT-UNSHOWN" tag and the ledger "OPEN-ish" status — they are stale.

### Provenance (is S³ ever native? — NO)
Reproduced/confirmed: `ε_abcd n_a ∂_r n_b ∂_θ n_c ∂_ψ n_d ≡ 0` on the native field (the 4th internal
slot has no independent DOF to hit) — there is no native 4-index/π₃/WZW invariant; only the 3-index
area form. No committed line DERIVES `ε_abcd`/π₃/WZW from the metric. S³ always imported. (Consistent
with M12 / NEGATIVES_REGISTRY #61: the classical m-catalog rides the imported Θ(core)=m·π, self-tagged
CHOSE.)

---

## 2. M11 — THE cos-θ TEXTURE — **SETTLED = embedding artifact (non-unit chart), not intrinsic**

Reproduced exactly this session (`s2_s3_identity_texture.py`):
- The embedding that produced the texture, `n = (sinΘ sinθ cos mψ, sinΘ sinθ sin mψ, cosΘ)`, is **NOT a
  unit field**: `|n|² = cos²θ cos²Θ − cos²θ + 1 ≠ 1` off the equator. Its `T^θ_θ` carries cos θ — but it
  is not even a map to S² (amplitude varies with θ). The cos-θ "texture" is an artifact of this
  **non-unit chart**.
- The genuine native UNIT deg-1 hedgehog `n = x/r = (sinθ cos mψ, sinθ sin mψ, cosθ)` (`|n|²=1` EXACTLY,
  all θ) has `T^θ_θ = (κm² − m²r²ξ + r²ξ)/(2r⁴)` — **θ-INDEPENDENT (texture-free)** — and **T^t_t = T^r_r
  EXACTLY** (the CANON C-14-1 B=1/A relation holds). Reproduced: `T^θ_θ depends on θ? False`,
  `T^t_t == T^r_r? True`.

> **M11 DISPOSITION: SETTLED = artifact.** The cos-θ texture is an artifact of the non-unit mψ embedding
> (`|n|²≠1`); the correct unit S² hedgehog is texture-free and B=1/A-consistent. NOT a real feature.

> **One honest scope note (verifier, re-confirmed):** texture-freedom is specific to the f(θ)=θ
> degree-1 hedgehog (n=x/r). A generic unit map `n=(sin f(θ)cos mψ,…,cos f(θ))` with f≠θ carries
> θ-structure in T^θ_θ. But the CANON deg-1 carrier IS f=θ (n=x/r) — the embedding the build uses — so
> the artifact verdict for the original motivating texture stands. The texture is not a property of the
> S² object; it was a property of the bad chart.

---

## 3. DOES THE DERIVED OPERATOR FORCE S² OVER S³? — **NO. S² stays INHERITED into the operator work.**

Checked `native_dilation_weight_derivation_results.md` and `matter_regrade_derived_operator_results.md`
(the derived two-player scalar-tensor operator `S_grav = ∫√−g[e^{2φ}R + X e^{2φ}(∂φ)²]`, a(φ)=e^{+φ}).
Both **USE S² as given** (the unit 3-vector n_a / area-form current) and contain **nothing that forces
S² over S³**. The gravity-side derivation is a STATEMENT ABOUT THE LEFT-HAND-SIDE LAW (the operator,
absorbability, conservation, Bianchi) — it never re-opens the matter field's TARGET SPACE, and would
read identically for an S³ field. So the answer to "does the derived operator change M10/M11?" is **no**:
the operator does not source a 4th component, does not supply an SU(2) isometry, and does not select the
target — the S² selection comes entirely from the **matter action** (§1), upstream of the operator. The
operator work is a CONSUMER of M10's result, not a contributor to it.

---

## 4. THE F2-DEPENDENCY NOTE (M10 is LOAD-BEARING on F2 — stated explicitly)

F2 (`F2_matter_action_forcedness_results.md`, RESOLVED = minimal-but-not-unique) **RIDES the S²
/ full-SO(3) target throughout**. Its forcing arguments are not target-neutral:

- **L2 uniqueness** ("the unique 2-derivative diffeo+SO(3) scalar") is an SO(3)=Isom(S²) statement.
- **The 4-derivative space is EXACTLY 2-dimensional** `{X², |ω_H1|²}` *because* the strain on the
  **2-dim S² target** has at most two eigenvalues (`f2_s2_4deriv.py`). On an S³ target the strain rank
  and the invariant count change.
- **V(n) is FORBIDDEN** *by the full target SO(3)* (a full-SO(3)-invariant function of a unit 3-vector is
  necessarily constant) — F2's single strongest new forcing result.
- F2's own ledger says so: **C-F2-b** = "full target SO(3) is the native symmetry … CHOSE/inherited — it
  is the SAME assumption L2's uniqueness rests on; if the carrier's native symmetry is actually reduced,
  V re-enters"; **C-F2-c** = "restricted to the S² (π₂) carrier; the S³/SU(2) carrier tension … not
  re-litigated here [SCOPE]." The ledger scoreboard line for F2 ends: **"Verdict rests on the carrier
  target = full SO(3)."**

**Therefore:** F2's whole forcedness verdict is CONDITIONAL on M10. With M10 now SETTLED = S²
(DEMANDS-level, §1), that conditional is **DISCHARGED**: F2's S²/full-SO(3) premise is not merely an
inherited posit — it is the verified native target. The dependency is real and now SATISFIED, not a
hanging risk. (This UPGRADES F2's standing slightly: its load-bearing premise C-F2-b is no longer
"CHOSE/inherited, re-opens if the carrier symmetry is reduced" — the carrier symmetry being full SO(3)
is exactly what §1's three necessities establish. Recommend F2's C-F2-b/C-F2-c be cross-referenced to
this closure.)

---

## 5. PREMISE LEDGER (this closure)

| # | Choice | CHOSE / DERIVED | Note |
|---|---|---|---|
| native action L2+L4 | the cross-product (ε_abc) L4 of CANON C-14-1 | DERIVED (canon) | the genuinely native L4; the Lagrange-identity form is the import (≠ native for d>3) |
| metric form | ds² = −e^{2A}dt² + e^{2B}dr² + r²dΩ², A,B free (B=1/A NOT pre-imposed) | DERIVED (CANON C-18-1) | B=1/A emerges (§2), not assumed |
| field ansatz | unit 4-vector with X(r) (or orthogonal Y(r)) fully live | DERIVED-general | most general 4th-component sweep; not a slice |
| static / round | static, axisymmetric hedgehog | CHOSE (scope) | a target-space question, settled where the carrier is defined; time-live does not re-open WHICH target the field maps to |
| r_core | finite cutoff in committed solves | CHOSE (flagged) | DECOUPLED from M10 (would-be S³ minima are non-physical at |n_4|>1 on the whole domain, independent of r→0) — this is what defused the prior attempt's r=0 conditional |
| reproduction scope | re-ran the 3 committed scripts; did NOT run a 4th independent blind pass | CHOSE | the existing blind verifier (2026-06-19) already STANDS; ATTACK block invites a fresh one |

---

## 6. NET DISPOSITIONS (the clean state)

- **M10 (S² vs S³ object identity): SETTLED = S²** — DEMANDS-level, three independent necessities
  (structural / dynamical / symmetry), BOTH inflation directions refuted, blind-verified 2026-06-19.
  NOT used-as-given-with-caveat; genuinely DEMANDED. The F0 "unexecuted" flag and the ledger "OPEN-ish"
  status are STALE (the settle predates F0 by two days, with a passing verifier) — retire them.
- **M11 (cos-θ texture): SETTLED = embedding artifact** — the texture is an artifact of the non-unit mψ
  chart; the canon unit hedgehog n=x/r is texture-free and B=1/A-consistent. One honest scope note: this
  is for the canon f(θ)=θ deg-1 carrier (the one the build uses); a generic non-canon profile f≠θ would
  carry θ-structure — but that is not the native object.
- **Derived operator: does NOT force S²** — the operator USES S² as given and is a consumer of M10, not
  a contributor; S² selection is purely a matter-action result, upstream.
- **F2-dependency: M10 is load-bearing on F2, and now DISCHARGED** — F2's L2-uniqueness, the exactly-2-dim
  4-deriv space, and the V(n)-forbidding result all ride the S²/full-SO(3) target; with M10 settled, that
  premise is verified-native rather than inherited.

Two small recommended housekeeping fixes (cosmetic, not verdict-altering): (a) correct the
`s2_s3_identity_results.md` Part-1 footnote that mislabels the Lagrange-L4 as n_4-independent (sympy
`real=True` bug); (b) correct the `s2_s3_identity_stability.py` printed VERDICT-LOGIC boilerplate (written
for the d²V>0 case while the computed curvature is negative). Both already noted in the 2026-06-19 verifier.

---

## 7. ATTACK HERE (for a fresh blind verifier)

1. **Re-derive the n_4 EOM source** with your own parametrization (orthogonal Y(r), amp=√(1−Y²)).
   Confirm/refute: (a) no native term sources an INDEPENDENT n_4 (source ∝ Y, vanishes at Y=0); (b)
   `d²V/dY²|_0 < 0` (maximum); (c) the would-be S³ critical points lie at |Y*|>1 (non-physical); (d) the
   downhill roll sends Q=4πm·cos³X → 0 (charge-destroying), so the instability is unwinding-to-vacuum,
   NOT S³-nucleation. (Two prior blind agents confirmed all four — re-do from scratch.)
2. **Attack the structural claim** that the native (cross-product) L4 is blind to n_4. Exhibit ANY native
   four-derivative term built from the metric + unit field that DOES source an independent n_4 without
   importing the Lagrange-identity form or a WZW/Hopf π₃ term. If none, §1(i) stands.
3. **Attack the texture verdict.** Confirm the mψ embedding is non-unit (`|n|²≠1`) and the unit hedgehog
   n=x/r has θ-independent T^θ_θ and T^t_t=T^r_r. If a UNIT S² embedding (canon f=θ) carries intrinsic
   θ-texture, M11 is wrong.
4. **Attack the F2 dependency claim.** Is F2's L2-uniqueness / 2-dim-4-deriv / V-forbidding genuinely
   conditional on the S² target (would they change on S³)? If F2 is target-neutral, the "load-bearing"
   framing is wrong.
5. **Attack the timeline reconciliation.** Verify from git/file mtimes that `s2_s3_identity_results.md`
   (23:00) + `_VERIFIER.md` (23:07) were committed 2026-06-19, two days before F0 (2026-06-21 07:47) —
   i.e. that F0's "unexecuted" flag is genuinely stale, not that this doc is back-dating.
6. **Targeting check.** Was S² DERIVED (from absence-of-source + charge-destruction), or steered? Confirm
   no data / catalog / desired-answer was loaded (grep: 0 mass/ratio/wall numbers).

---

## VERIFICATION (2026-06-21) — blind pass, agent a3edae128be9c0dc4
STANDS. The "F0 was WRONG, S^2 is DEMANDED+verified" claim is TRUE (verified):
- F0's M10 flag is FACTUALLY WRONG: s2_s3_identity_results.md (committed 2026-06-19 23:00) + s2_s3_identity_VERIFIER.md
  (23:09, NET VERDICT "the S^2 settle STANDS, 'no fork' is correct") EXIST and settle it; F0 (2 days later)
  conflated the 22:48 MAP with the executed+verified 23:00 results and inherited a stale tripwire from a DIFFERENT
  genuinely-failed doc (fourth_component_sourced, 2026-06-18). => RETIRE the F0/ledger M10 "OPEN-ish" flag.
- M10 = SETTLED = S^2, DEMANDS-level: (i) structural dL4/dn_4 ≡ 0 (eps_abc 3-index — independently sympy-confirmed);
  (ii) dynamical d^2V/dX^2|_0<0 + charge-destruction (downhill = unwinding to vacuum, NOT S^3 nucleation; would-be
  S^3 minima non-physical |Y*|>1); (iii) symmetry SO(3)=Isom(S^2), no SU(2). BOTH inflation directions refuted.
- M11 = SETTLED = embedding artifact (unit hedgehog n=x/r texture-free, T^t_t=T^r_r — sympy-confirmed; the texture
  came from a non-unit embedding). Scope note (specific to the f(theta)=theta deg-1 carrier) honest.
- F2 UPGRADE confirmed: settling M10 at DEMANDS-level DISCHARGES F2's "rests on full-SO(3)" conditional.
(Caveat: this doc leans on the 2026-06-19 verifier, which stands; the verifier independently re-confirmed (i),(iii),(vi).)
