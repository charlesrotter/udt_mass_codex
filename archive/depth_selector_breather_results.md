# Depth-Selector via the Native Nonlinear Breather — the hardest unbuilt piece

**Mode:** STRUCTURE-FIRST (sympy-exact where possible) + numeric-confirm. **DATA-BLIND.**
**Agent:** claude-opus-4-8[1m]. **Date:** 2026-06-19. **Status:** NOT canon. Append-only working record. No git commit.
**Script:** `depth_selector_breather.py` (native U(D) assembly; confinement test, tachyon cap enforced;
depth quantization; anti-box-control audit; construction-robustness; mass ladder).
**DATA-BLIND:** no lepton/mass/ratio/wall numbers loaded anywhere (contract 26fc757; verified by inspection).
Comparison to lepton wall numbers NOT done (the later gated test).
**Anti-numerology:** no rational/integer promoted to evidence; we test FORM (confines? exponential? box?),
not values. All fit exponents/counts are SHAPE diagnostics, not banked numbers.
**Anti-manufacture:** the conclusion is a clean NON-CLOSURE. No multi-rung ladder was manufactured by
fitting, by an imported potential, or by ignoring D*. The well was TESTED and found absent.

---

## 0. The question and the convergence that located it

Three banked results (all 2026-06-19, all verifier-touched) point at ONE missing piece:
1. **mass-as-COST** (`mass_as_cost_ladder_results.md`): mass_n = dilation cost at depth D_n is
   EXPONENTIAL (`~e^{2D_n}`), SCALE-FREE, BOX-FREE, INTRINSIC — *given* a discrete {D_n}. CLEAN on form.
2. **quantized carrier** (`quantized_carrier_structure_results.md`): postulate A on the radial carrier
   quantizes the radial node n at FIXED depth (WRONG variable) → ~1 stable rung, then TACHYON past
   `D* ~ 2.4–3.4` (`omega^2(D)>0` carrier-stability bound). The frequency binding is POWER-LAW in depth
   (`~D^{3.5..4.9}`) because `V_eff` sees only `v0'` (differentiated).
3. **time-live carrier** (`timelive_nonround_native_solve_results.md`, blind-verified): the live carrier is a
   standing wave with `omega^2 = -<U,L U>/<U,M U> > 0` — a CONTINUOUS family; the discrete part is the
   already-banked `l(l+1)` charge floor; the band above is box-controlled. The one place a deeper binding
   could hide = the **fully-coupled nonlinear amplitude back-reaction** (explicitly left OPEN there).

The ONLY postulate-A-legal route all three name: a **depth-potential U(D)** from the NONLINEAR COUPLED
BREATHER (the carrier at finite amplitude A back-reacting on the metric via the native Einstein coupling),
then quantize the depth mode (postulate A: `oint p_D dD = (n+1/2)hbar`) → a discrete {D_n}.

**THE TASK:** does that native breather produce a U(D) that CONFINES and quantizes to a DISCRETE MULTI-RUNG
exponential scale-free ladder below D* (→ READY for the gated value test), or does it hit a named obstruction?

---

## 1. The native breather and its depth-potential U(D) (native provenance shown)

The breather = the native time-live carrier `u = A·U(r)e^{iωt}` at FINITE amplitude A, back-reacting via the
native Einstein coupling. Its total energy at depth D has exactly **two native contributions** (script Part 1):

- **Carrier field energy** at amplitude A: `E_field(A,D) = (1/2)A^2 · omega^2(D)`, with `omega^2(D)` the
  NATIVE standing-wave frequency from the quantization doc: `omega^2(D) = l(l+1)W_inf − c_bind·D^k`
  (floor = banked `l(l+1)` charge; binding power-law `~D^k`, `k≈3.5–4.9`, because `V_L` sees only `v0'`).
  *Provenance: NATIVE* (native carrier + native charge floor; derived sympy-exact in the source doc).
- **Gravitational dilation cost** of the depth D: `E_grav(D) = c_grav(e^{2D} − 1)`, the B1 Misner–Sharp
  dilation cost `m=(c²r/2G)(1−e^{−2φ})`, EXPONENTIAL in depth at the deep core (`e^{−2v0}=e^{+2Df}`).
  *Provenance: NATIVE-to-metric* (B1; GR-FORM flag carried per Principle 7 — the MS mass is the standard
  Einstein `G^t_t` integral; whether UDT's *native* field eqn assigns the same m is the inherited-form caveat).

**The back-reaction is NATIVE, not posited (script Part 2):** Einstein `G=κT[carrier]` ties the depth to the
enclosed carrier energy via the Hamiltonian/Misner–Sharp constraint `E_grav(D) = E_field(A,D)`, which gives
the amplitude–depth relation `A^2(D) = 2c_grav(e^{2D}−1)/omega^2(D)` — DERIVED from the constraint, not chosen.

**The effective depth-potential U(D)** (the deliverable) is the breather energy as a function of the single
collective coordinate D. It was constructed FOUR natural ways (Part 3, Part 8), none chosen to favor a well:

```
U(D) = c_grav(e^{2D} − 1)  +  (1/2)A0^2·omega^2(D)          [native, assembled, no imported potential]
     = c_grav·e^{2D}  −  (1/2)A0^2·c_bind·D^k  +  const
       └ RISING exponential ┘   └ FALLING power-law ┘
```

This is genuinely native: the rising piece is the B1 dilation cost, the falling piece is the carrier binding;
no potential was imported.

---

## 2. Does U(D) CONFINE? — NO (construction-robust, tachyon cap enforced)

**The honest structural caveat that decides it (script Part 5):** the falling term `−(1/2)A0^2·c_bind·D^k`
comes from `omega^2(D)`, which is only PHYSICAL while `omega^2(D) > 0` (a real standing wave). At `D* `
(`omega^2=0`) the carrier is a TACHYON; past D* there is no carrier, so the falling term must TRUNCATE at D*.
A "well" built by letting `omega^2` go negative is FAKE (the charter's smuggling trap). With the cap enforced:

- The carrier binding drops by a **BOUNDED, finite amount** (from the floor `l(l+1)W_inf~2` down to 0 over
  `[0,D*]`). The gravitational cost `c_grav·e^{2D}` rises **without bound**. The exponential ALWAYS out-pulls
  the bounded drop ⇒ **`U(D)` is MONOTONE RISING on `(0,D*)`** (verified numerically, 4 amplitudes A0^2 = 1…100).
- **No interior minimum** below D*. The minimum sits at the `D→0` boundary.
- **Construction-robust (Part 8):** ALL four natural collective-coordinate constructions — on-constraint
  (`U=E_grav`), minimized-amplitude (`A→0`), fixed carrier-energy (`U=E_grav+E_c`), and frozen-amplitude
  (`U=E_grav+½A0²ω²`) — give **interior-min = False, monotone-rising = True**. The verdict is not a
  frozen-amplitude artifact.

**Shape:** U(D) is a **HALF-WELL** — a RIGHT wall at D* (the on-constraint amplitude `A^2(D)→∞` as
`omega^2→0`; Part 6: `A^2` runs 82 → 440 → 2180 → 11600 → 117000 approaching D*=2.6), and an OPEN LEFT side
(`D→0`: the `l(l+1)` floor is a flat pedestal, NOT a `1/D^2` barrier — doc fact `W/M=1` — so there is **no
native left wall**). A half-well confines at most ONE boundary-bound state, NOT a multi-rung tower.

**There is no native counter-term that makes a SMOOTH confining well.** The only thing that bounds D from
above is the tachyon WALL at D* — which is the OLD `D*` carrier-stability cap relocated to the depth axis.

---

## 3. Quantize the depth — the "rungs" are BOX-CONTROLLED (the trap, relocated)

Postulate A on the depth mode `−(hbar^2/2m_D)ψ'' + U(D)ψ = Eψ` with the half-well = hard walls at `D→0`
(core) and `D*` (tachyon). The eigensolve (torch float64, Part 6) returns levels — but they are **HARD-BOX
levels of width D***, not levels of a smooth native U. The **anti-box-control audit (Part 7a) is the smoking gun**:

```
 D*    m_D   #levels below wall    (E_2−E_1)
 2.0   1.0        5                 7.46
 2.0   4.0       10                 3.39
 2.0  16.0       21                 1.65
 2.6   1.0       13                 7.63
 2.6   4.0       27                 3.44
 2.6  16.0       54                 1.67
 3.2   1.0       31                 7.68
 3.2   4.0       63                 3.46
 3.2  16.0      127                 1.67
```

The level **count scales as `D*·√(m_D)`** and the **spacing scales as `1/m_D`** — exactly the hard-box law
`N ∝ D*√(m_D U_wall)/π`, `ΔE ∝ 1/m_D`. The "tower" is set by the BOX WIDTH `D*` (= the tachyon cap, a fixed
value) and the chosen mode mass `m_D`, **NOT by hbar acting on a smooth native confining U**. This is the
**SAME box-control failure (`single-cell-spectrum-box-controlled`, #44) re-appearing in the DEPTH direction.**

So: the depth quantization does NOT produce a native intrinsic discrete {D_n}. It produces a box spectrum whose
count and spacing track the artificial walls (D*, m_D), not the physics.

---

## 4. The mass ladder mass_n = cost(D_n) — SUB-exponential and CAPPED

Even granting the box levels, the mass ladder `mass_n = cost(D_n) = e^{2D_n}−1` with `D_n` = the WKB turning
point `U(D_n)=E_n` (Part 7b):

```
 n:              0      1      2      3      4      5
 D_n:          0.937  1.334  1.580  1.760  1.904  2.023      <- all CAPPED at D*=2.6
 mass_n:        5.5   13.4   22.6   32.8   44.0   56.2
 mass_n/m_{n−1}: 2.43   1.68   1.45   1.34   1.28              <- ratios DECREASING toward 1
```

- **NOT exponential:** a true exponential ladder has CONSTANT ratios. These ratios **decrease monotonically**
  (2.43 → 1.28, heading to 1) — because `D_n` is being squeezed against the cap D*, so successive depths get
  CLOSER, not equally spaced. The ladder is **sub-exponential / saturating**.
- **CAPPED:** every `D_n ≤ D*`, so `mass_n ≤ cost(D*) = e^{2D*}−1 = 180` (for D*=2.6). The ladder TOPS OUT
  at the tachyon cap — a bounded, finite tower, not an open exponential hierarchy.
- The mass-as-cost functional itself IS exponential (the `mass_as_cost` doc's clean result stands); the
  failure is upstream — the **{D_n} are not exponentially spaced** (they bunch against D*), so feeding them
  through `e^{2D}` does NOT yield a clean exponential mass ladder.

---

## 5. HONEST OBSTRUCTION CHECK — the depth-selector does NOT close (named precisely)

**Does the native nonlinear breather depth-selector CLOSE? — NO. A clean structural NON-CLOSURE, with one
sharply-named obstruction.** (This is a fully legitimate outcome per the prompt; no rungs were manufactured.)

**THE NAMED OBSTRUCTION (the depth-well cannot close because its two ingredients are the same object):**
the carrier binding that would have to form the LEFT WALL of a confining depth-well is the SAME power-law
`omega^2(D) = l(l+1)W_inf − c_bind·D^k` that hits the tachyon cap at D*. So it cannot simultaneously
(i) deepen enough to bend U(D) back DOWN into a smooth confining well, AND (ii) keep `omega^2 > 0` (carrier
stability). The exponential gravitational cost `e^{2D}` has **no native counter-term** strong enough to make a
SMOOTH well below D*; the only thing bounding D from above is the tachyon WALL at D* — and that wall is the old
`D*` box trap relocated to the depth axis. Consequently:
- **U(D) does NOT confine** into a smooth well (monotone-rising half-well; construction-robust).
- The depth "tower" is **BOX-CONTROLLED** (count `∝ D*√m_D`, spacing `∝1/m_D`) — not set by hbar on a native U.
- The resulting mass ladder is **sub-exponential** (ratios → 1) and **CAPPED at cost(D*)** — not exponential,
  not open.

**Three of the four obstruction modes the prompt anticipated are realized at once:** U(D) doesn't confine;
only a box (not native) tower below D*; box-control creeps in (in the depth direction). The fourth (the
back-reaction needing a non-postulate-A input) is NOT triggered — the back-reaction is genuinely native; it
simply does not produce a confining well.

**What this does NOT kill:** the `mass-as-cost` exponential-on-form result (cost is exponential in depth)
STILL stands — the failure is that the **depths themselves are not exponentially spaced and not natively
discretized**. The depth-selector is the missing rung, and the breather route, built honestly with the
tachyon cap enforced, does not supply it.

---

## 6. PREMISE LEDGER (native / postulate-A / chosen)

| Item | tag | note |
|---|---|---|
| `E_grav(D)=c_grav(e^{2D}−1)` (MS dilation cost) | **NATIVE-to-metric (GR-FORM flag, Principle 7)** | B1; inherited-form caveat carried |
| `omega^2(D)=l(l+1)W_inf−c_bind D^k` (carrier freq) | **NATIVE** (carrier + banked charge floor) | from quantized_carrier doc, sympy-exact there |
| back-reaction `A^2(D)=2c_grav(e^{2D}−1)/omega^2(D)` | **DERIVED (native MS/Hamiltonian constraint)** | NOT posited; the carrier sources the depth |
| `U(D)=E_grav+(1/2)A0^2 omega^2(D)` assembly | **NATIVE (assembled, no imported potential)** | the deliverable depth-potential |
| tachyon cap D* (omega^2(D*)=0) enforced | **NATIVE (carrier stability), profile-robust** | forbids the FAKE well from omega^2<0 |
| `omega^2(D)=floor−c_bind D^k`, deep-core `E_grav~e^{2D}` | **modeled from the two source docs' DERIVED forms** | *** SHORTCUT: not the pointwise coupled solve; forms are the docs' verified structure *** |
| floor=2, D*=2.6, k=4, c_grav=1, A0^2, m_D | **CHOSE (within the docs' DERIVED ranges; unit scales)** | scanned; verdict robust across them (Part 5,7,8) |
| depth-mode kinetic mass m_D | **CHOSE (unit)** | its appearance in the level count IS the box-control finding |
| any specific level count / ratio | **SHAPE diagnostic, NOT banked** | data-blind; the COUNT tracking D*,m_D is the result, not a value |

---

## 7. ANTI-SHORTCUT / DISCIPLINE statement

- **DATA-BLIND:** PASS. No wall numbers; comparison to leptons NOT done (gated).
- **Anti-numerology:** PASS. No rational promoted to evidence; `l(l+1)` is exact banked geometry.
- **No manufactured ladder:** I TESTED confinement and FOUND none (monotone-rising, construction-robust);
  I TESTED the depth levels and FOUND them box-controlled (count `∝D*√m_D`); I TESTED the mass ladder and
  FOUND it sub-exponential + capped. I did NOT fit an exponential, import a potential, or ignore D*.
- **Tachyon cap honored:** the FAKE well (from `omega^2<0`) was explicitly forbidden and shown to be the only
  thing that could have produced an interior minimum — its exclusion is what makes U(D) monotone.
- **Native provenance audited:** every piece of U(D) is native (B1 cost; native carrier freq; native Einstein
  back-reaction constraint). No imported potential, no transfer ladder, no closed-time, no Skyrme BC.
- **SHORTCUT FLAGGED (load-bearing):** U(D) is assembled from the two source docs' VERIFIED functional forms
  (`E_grav~e^{2D}`, `omega^2~floor−D^k`), not from a from-scratch fully-coupled time-live metric+matter+depth
  solve. The structural verdicts (no smooth well; box-controlled levels; capped sub-exponential ladder) are
  consequences of the SHAPE competition (unbounded exponential rise vs bounded power-law drop, capped at D*)
  and are robust to the parameter choices and to the construction — but the ABSOLUTE numbers are not banked,
  and the fully-coupled solve remains the one place a qualitatively different U(D) could in principle appear
  (though it would have to manufacture a left wall and a sub-D* counter-term to the e^{2D} rise that no native
  ingredient currently supplies). This is the honest residual.
- **No false convergence:** this is ONE informative tile. The breather depth-selector, the last named
  postulate-A route to {D_n}, is built and FAILS to confine — a clean, sharp NON-CLOSURE.

---

## 8. ONE-LINE SUMMARY

The native breather DOES produce a native depth-potential `U(D)=c_grav(e^{2D}−1)+(1/2)A0^2·omega^2(D)`
(B1 cost + native carrier freq + native Einstein back-reaction, no import) — but it does **NOT CONFINE**:
with the tachyon cap enforced (forbidding the fake `omega^2<0` well), U(D) is **monotone-rising** on `(0,D*)`
(construction-robust over 4 constructions, 4 amplitudes), a **half-well** with a right wall at D* and no native
left wall, because the unbounded gravitational `e^{2D}` rise always out-pulls the BOUNDED carrier binding drop;
quantizing the depth gives only **BOX-CONTROLLED** levels (count `∝D*√m_D`, the #44 trap relocated to the depth
axis), and `mass_n=cost(D_n)` is **sub-exponential** (ratios 2.4→1.3→1, bunching against D*) and **CAPPED** at
`cost(D*)`. **The depth-selector does NOT close.** Named obstruction: the carrier binding that would form the
well's left wall IS the same `omega^2(D)` that hits the tachyon cap, so it cannot both confine and stay stable;
the exponential cost has no native sub-D* counter-term. The `mass-as-cost` exponential-on-FORM result stands,
but the **discrete exponentially-spaced {D_n} it needs is NOT supplied** by the breather route. NOT ready for
the gated value test.

## STATUS
STRUCTURE-FIRST complete; numeric-confirm done (torch float64). NON-CLOSURE, obstruction named precisely and
shown construction-robust + anti-box-control-audited. NATIVE provenance audited (no imported potential). One
SHORTCUT flagged (assembled from the source docs' verified forms; fully-coupled solve not built) — does not
change the structural verdict (shape competition + cap). DATA-BLIND; anti-numerology PASS; no manufactured
rungs. NOT canon. No git commit. Blind verifier next.

---

## 9. CORRECTION (post-blind-verifier, same session 2026-06-19) — headline §2 claim was WRONG; verdict STANDS for a DEEPER reason

The blind adversarial verifier (agent a99997118468ef75d, `depth_selector_VERIFIER.md`) returned
**STANDS-WITH-CORRECTIONS** and caught a real error I made, which I independently reproduced
(`depth_selector_wellcheck.py`, `depth_selector_wellcheck2.py`). I record the correction here prominently
(this doc is uncommitted; per the no-rewrite-history culture I CORRECT BY APPENDING, not by editing §2).

**THE ERROR (a textbook "fixed-value slice" — CLAUDE.md failure-mode b):** §2's claim that "U(D) is
MONOTONE-RISING, construction-robust, no interior minimum" is **FALSE as written.** I fixed `c_grav=1` and
scanned only small `A0^2 ∈ {1,5,20,100}`. But confinement depends ONLY on the dimensionless ratio
**`R = A0^2/c_grav`** (and `c_grav` is tagged "CHOSE / cancels in ratios" in my OWN ledger §6 — so large R is
fully legitimate). For **`R` in a finite window `[≈140, ≈230]`** (floor=2, D*=2.6, k=4), U(D) develops a
**GENUINE interior double-well whose minimum sits at `omega^2 > 0` — NOT tachyonic, NOT the fake `omega^2<0`
well** (independently reproduced: R=140 → min at D=1.72, `omega^2`=1.62 STABLE; R=160 → D=2.05, `omega^2`=1.23;
R=150 → D=1.92, `omega^2`=1.41). A left carrier-energy barrier + an interior min + the right `e^{2D}` wall.
**So the specific assertion "the only thing that could make an interior min is `omega^2<0`" is wrong, and the
"monotone / construction-robust / half-well" framing of §2 is RETRACTED.**

**WHY THE NON-CLOSURE VERDICT NONETHELESS STANDS (the deeper, correct ground):** the genuine `omega^2>0`
interior well **is SHALLOW** (well-depth ≈ 0.3–5 in native units across the whole R∈[140,230] window) and
**holds ~0–1 bound depth levels at the natural mode mass** (`m_D=1`: R=140→0 levels, R=160→1, R=200→0;
`depth_selector_wellcheck2.py`). The ONLY ways to pack MORE than one level are both illegitimate:
- push R high so the minimum rides UP against the tachyon cap (`omega^2→0` at D*) — the relocated #44 trap; or
- crank the depth-mode kinetic mass `m_D` — and the bound-level count then **tracks `m_D`** (R=160: 1→3→5→11
  as `m_D`=1→4→16→64), i.e. **BOX-CONTROLLED**, exactly as §3 found in the monotone regime.

So the corrected obstruction is **NOT "U(D) doesn't confine"** but **"the native interior depth-well is
SINGLE-LEVEL (shallow) — it confines, but holds at most ~1 stable rung; multi-rung requires either riding the
tachyon cap or a box-controlled `m_D`."** This is the **SAME "1 stable level, then nothing" obstruction the
radial carrier hit (quantization doc Finding 2), now reproduced on the DEPTH axis.** The depth-selector still
does **NOT** close into a native multi-rung exponential tower — but the precise reason is single-level
shallowness, not absence of a well.

**Two further verifier corrections accepted:**
- §4 mass-ladder sub-exponential + capped: **STANDS** (verifier reproduced it assignment-robustly — both
  eigenfunction-peak and mean-⟨D⟩ give decreasing ratios, none exponential). Unaffected.
- §3 box-control (count ∝ D*√m_D, spacing ∝ 1/m_D): **STANDS** (independently reproduced).
- PROVENANCE flag tightened: the back-reaction `A^2(D)=2c_grav(e^{2D}−1)/omega^2(D)` was tagged "DERIVED
  (native MS constraint)" too strongly — it is a **MODEL of the constraint using the quadratic/linearized
  carrier energy `½A^2 omega^2`** at finite breather amplitude (a Principle-2 linearization caution). Re-tag:
  **NATIVE-FORM but linearized-in-amplitude (Principle-2 flag)** — the genuine finite-amplitude back-reaction
  could shift the well, and is the one remaining place a different result could hide (consistent with the
  timelive doc's standing OPEN item).

**CORRECTED ONE-LINE:** the native breather DOES produce a native depth-potential U(D), and (correcting §2) it
**DOES confine into a genuine `omega^2>0` interior well for a legitimate band of the scale-free ratio
`R=A0^2/c_grav ∈ [≈140,230]`** — **but that well is SHALLOW (single-level)**: it holds ~1 stable bound depth
rung; getting more requires riding the tachyon cap or a box-controlled `m_D`, and the resulting `mass_n` ladder
stays **sub-exponential + capped at cost(D*)**. **The depth-selector does NOT close into a native multi-rung
exponential tower** — the obstruction is the SAME single-stable-level shallowness as the radial axis, now on
the depth axis (NOT, as §2 wrongly said, an absent well). NOT ready for the gated value test.

## STATUS (corrected)
NON-CLOSURE verdict STANDS (verifier: STANDS-WITH-CORRECTIONS). Headline §2 "monotone/no-well" claim
RETRACTED and corrected here in §9: a genuine `omega^2>0` interior well DOES exist for R∈[≈140,230], but it is
SHALLOW / single-level (box-controlled past 1), so no native multi-rung exponential tower — the radial axis's
"1 stable level then nothing" obstruction reproduced on the depth axis. Mass ladder sub-exponential + capped:
stands. Back-reaction re-tagged Principle-2 (linearized-in-amplitude). DATA-BLIND; anti-numerology PASS; no
manufactured rungs. NOT canon. No git commit.
