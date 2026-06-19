# Mass-as-COST Ladder — the FREQUENCY-VS-COST split test

**Mode:** STRUCTURE-FIRST, DATA-BLIND. Combines two banked results to test whether
the mass ladder is exponential when mass = dilation COST (B1) rather than ℏω.
**Agent:** claude-opus-4-8[1m]. **Date:** 2026-06-19. **Status:** NOT canon. Append-only
working record. No git commit.
**Scripts:** `mass_cost_ladder.py` (exact sympy cost functional + the split derivation +
numeric exp-vs-power form test + intrinsic-vs-box + rung count),
`mass_cost_robustness.py` (4-profile robustness of the cost exponential + depth-selector audit).
**DATA-BLIND:** no lepton/mass/ratio/wall numbers loaded anywhere (contract 26fc757;
verified by inspection). Comparison to lepton wall numbers NOT done (the later gated test).
**Anti-numerology:** no rational/integer promoted to evidence; we test FORM (exp vs power),
not values. The fit exponents (e^{~2D}, D^{~3.7}) are SHAPE diagnostics, not banked numbers.
**Anti-manufacture:** the exponential is DERIVED analytically (sympy) from the exact MS cost
functional, NOT fitted into existence; the numeric fit only corroborates the analytic form.

---

## 0. The two banked results combined

1. **QUANTIZATION** (quantized_carrier_structure_results.md): postulate A on the native
   time-live carrier gives a genuine INTRINSIC discrete bound well (box-control BROKEN,
   first on the program; +1/2 = native area-form Maslov spin-1/2). BUT the eigen-FREQUENCY
   binding is POWER-LAW in depth (~D^{3.5–4.9}), NOT exponential, because V_eff is built
   from LOG-DERIVATIVES of the depth profile (s = 2v0', linear in D) — the exponential
   e^{φ} is differentiated away. AND the radial-overtone tower is SHALLOW (~1 stable level,
   then tachyon past D* ~ 2.4–3.4).
2. **B1** (B1_mass_dilation_cost_results.md): the mass is the dilation COST,
   `m(r) = (c²r/2G)(1 − e^{−2φ})`, an EXACT native functional, exponential in depth
   (1 − e^{−2φ} grows exponentially as φ deepens). The mass was NEVER the eigenfrequency.

**Hypothesis tested:** the discrete LADDER comes from quantization, but the MASS of each
quantized state is its dilation COST (B1), not ℏω — so the exponential hierarchy may live
in mass-as-COST (undifferentiated e^{φ}) while the frequency stays power-law (differentiated).

---

## 1. The exact mass-as-COST functional (B1, restated symbolically)

With the native dilation profile `φ(r) = v0(r) = −D f(r)` (depth D; deep negative core
→ 0 exterior; `f` a native-like core shape), B1's Misner–Sharp dilation cost is, EXACTLY
(`mass_cost_ladder.py` Part 1, sympy):

```
m(r) = (c²r / 2G) · ( 1 − e^{−2φ(r)} ) = (c²r / 2G) · ( 1 − e^{ +2 D f(r) } )
```

`e^{−2φ}` is the metric's dilation factor; `(1 − e^{−2φ})` is its **deficit from unity**
= the cost of the dilation. Because φ is NEGATIVE in the core, `e^{−2φ} = e^{+2Df}` grows
**exponentially as the depth D increases.** This is the exact native functional, not a model.

Two scalar "cost of the state at depth D" measures (both reported, neither chosen to favor
the hypothesis): the **core amplitude** `|1 − e^{+2D}|` (r→0, leading `~e^{2D}` deep), and
the **integrated cost weight** `∫|1 − e^{−2φ}| dr`. Both are exponential in D (Part 4, §4).

---

## 2. WHY cost restores the exponential that frequency lost (the re-derivation)

The single structural point, derived exactly (`mass_cost_ladder.py` Part 1b, sympy):

- The dilation **amplitude** is `e^{φ} = e^{−Df}` — the depth D sits **in the exponent**.
- The eigen-**FREQUENCY** sees φ only through the Liouville potential
  `V_L = ½s′ − ¼s²`, `s = 2v0′`. Forming `s = 2(−D f)′ = −2D f′` **differentiates** the
  profile: the D that was in the exponent comes **down as a multiplicative polynomial
  coefficient** (linear in `½s′`, quadratic in `−¼s²`). The binding scale that sets ω²
  is therefore `~D²` (a POWER), and the surviving `e^{−Df}` is a fixed *shape*, not a
  depth-amplitude. **Differentiation converts "D in the exponent" into "D as a polynomial
  coefficient" → POWER-LAW in depth.**
- The **COST** sees φ through `e^{−2φ} = e^{+2Df}` **directly — no derivative.** The depth
  D **stays in the exponent → EXPONENTIAL in depth.**

So the frequency route and the cost route differ by exactly one derivative, and that one
derivative is what demotes the exponential to a power law. **Mass-as-cost restores the
exponential that mass-as-frequency differentiated away — confirmed analytically (sympy),
not fitted.** This is the precise content of the "frequency-vs-cost split."

---

## 3. Numerical corroboration (exp vs power), DATA-BLIND, profile-robust

For a depth scan D ∈ [0.6, 3.4] (no spacing chosen; D treated as a continuous parameter),
fit each quantity to exp-in-D vs power-in-D; smaller log-residual wins
(`mass_cost_ladder.py` Part 4):

| quantity | verdict |
|---|---|
| FREQUENCY binding `(V_inf − E_0)` | **POWER-LAW** `~D^{3.73}` (exp-resid 4.6e-1 ≫ pow-resid 2.5e-1) |
| COST core amplitude `|1 − e^{−2φ}|` | **EXPONENTIAL** `~e^{2.09 D}` (exp-resid 5.9e-2 ≪ pow-resid 3.6e-1) |
| COST integrated weight `∫|·|dr` | **EXPONENTIAL** `~e^{1.83 D}` (exp-resid 4.3e-2 ≪ pow-resid 3.2e-1) |

**Profile-robust** across all four native-like cores the quantization doc used
(`mass_cost_robustness.py` A): cost core amplitude is EXP `e^{2.06–2.09 D}` for
gaussian/lorentzian/expcore/sech²; integrated weight EXP `e^{1.56–1.83 D}`. The split is
structural, not a profile artifact — same four profiles, **frequency = power, cost = exp.**
(The exponents are SHAPE diagnostics; no value is banked.)

---

## 4. The structure of mass_n as COST (the deliverable form)

GIVEN any increasing sequence of depths `{D_n}` (the spacing left OPEN — see §6), the
cost-mass has this structure (`mass_cost_ladder.py` Part 3):

```
|m_n|  ~  e^{2 D_n}        (leading, deep core; vs frequency route m_n² = l(l+1) − D_n^k)
m_n / m_0  ~  e^{2 (D_n − D_0)}
```

| property | verdict |
|---|---|
| **EXPONENTIAL in the depth index?** | **YES** — analytic `e^{2D}` (core) / `e^{~1.8D}` (integrated), profile-robust. The cost genuinely restores the exponential (§2–§3). |
| **RATIOS scale-free?** | **YES** — `c²/2G, r_core, a` ALL cancel in `m_n/m_0 ~ e^{2(D_n−D_0)}`; only the dimensionless depth DIFFERENCE survives. |
| **INTRINSIC (not box)?** | **YES** — the cost is exactly R-independent for BOTH measures (Part 5): core amplitude is r-local; integrated weight saturates (`f→0` exterior). The exponential lives in a **box-free** quantity (unlike the frequency continuum). |
| **multi-rung?** | **NOT ESTABLISHED** — see the named obstruction §6. The cost functional itself imposes no rung limit, but the discrete depth ladder is not yet selected, and the carrier-stability cap D* still bounds the deepest admissible rung. |

So on three of the four desiderata — **exponential, scale-free, intrinsic** — mass-as-cost
**passes cleanly** where mass-as-frequency failed the first. The fourth — a genuine
multi-rung family — is where the obstruction sits.

---

## 5. The ladder axis (what indexes the family) — honest answer

- **radial n:** SHALLOW (1 stable level, then tachyon; quantization doc Finding 2). **NOT** the axis.
- **angular l:** the **CHARGE** axis (N=3, q=1/3, already banked). Charge diversity, **NOT** a
  same-charge generation family. **NOT** the generation axis.
- **depth D:** the state's location in the dilation well — **the candidate**, and the only one
  on which the cost-mass is exponential + scale-free + intrinsic.

So the natural ladder axis for the cost-mass family is **DEPTH D_n** (one charge-1 object at a
sequence of depths), with `mass_n = cost(D_n) ~ e^{2D_n}`. **BUT** where the discrete depths
come from is the load-bearing open question (§6) — it is NOT assumed.

---

## 6. HONEST OBSTRUCTION CHECK — the named wall

**Does mass-as-cost-of-quantized-states give a clean DISCRETE, SCALE-FREE, EXPONENTIAL
ladder? — PARTIAL. The exponential + scale-free + intrinsic are RESTORED and CLEAN; the
DISCRETE multi-rung LADDER is NOT yet closed natively. One precisely-named obstruction.**

**What the split DID buy (genuine, not narrated):** the cost route fixes the two specific
failures the frequency route hit — it is **EXPONENTIAL** in depth (vs power-law), **SCALE-FREE**
in ratios (prefactors cancel), and **INTRINSIC / box-free** (vs the box-discretized continuum).
The hypothesis's core claim — "the exponential lives in mass-as-COST because cost is the
undifferentiated e^{φ} amplitude while frequency is its log-derivative" — is **CONFIRMED
analytically and corroborated numerically, profile-robust.** This is a real, clean advance:
the exponential hierarchy is now sitting in a native, exact, box-free functional.

**The named OBSTRUCTION (the depth-selector gap) — `mass_cost_robustness.py` (B):**
mass_n = cost(D_n) needs a SEQUENCE of discrete depths {D_n}. **Postulate A does NOT supply
it.** Postulate A, as scoped (ℏ + spin-½ + statistics) and as applied in the quantization doc,
is **radial Bohr–Sommerfeld over r**, which quantizes the **radial node n at FIXED depth D**
(candidate C1) — the WRONG variable. It indexes n (≈1 stable rung, then tachyon), not D. The
candidates that WOULD discretize the depth are:
- **C2 — depth/breather Bohr–Sommerfeld** `∮ p_D dD = (n+½)ℏ`: quantizes the well DEPTH as a
  collective coordinate. This is the right shape and is *legal* under postulate A, but it needs
  the **nonlinear breather back-reaction `ω(A)` / an effective depth-potential `U(D)`** with a
  confining shape — which is **UNBUILT** (flagged UNAUDITED / not-yet-native in both source docs).
  `U(D)` must be DERIVED from the coupled time-live solve, not posited (posit = smuggled mechanism).
- **C4 — closed-time / non-stationary selector** (#57): a periodic-time condition could
  discretize the depth temporally. **UNBUILT / UNAUDITED.**
- **C5 — imposing a spacing {D_n} by hand** (even/log): **IMPORT / smuggled value — FORBIDDEN,
  NOT done.** Any specific spacing would be a fit, and the wall numbers are gated besides.

**Second, scope-limited obstruction (the tachyon cap is NOT lifted by cost):** the cost
relabels the mass of a state that already exists; it does **not** relax the carrier-stability
requirement `ω² = E > 0`. If the rungs are RADIAL levels at fixed D, still ~1 stable (cap
unchanged). If the rungs are at different depths D_n, each D_n must independently host a STABLE
(`ω²>0`) carrier, so **D* still bounds the deepest admissible rung.** The cost functional itself
imposes no rung limit, but carrier stability (depth < D*) does — so the rung count is gated by
BOTH the missing depth-selector AND the D* cap (`mass_cost_ladder.py` Part 6).

**NET READ:** the frequency-vs-cost split is **REAL and the right move** — it relocates the
exponential hierarchy from the (differentiated, power-law, box-discretized) eigenfrequency to
the (undifferentiated, exponential, scale-free, intrinsic) dilation cost, exactly as the
hypothesis predicted, and this is profile-robust and exact. **But it is NOT yet a clean
multi-rung ladder ready for the gated value test**, because the thing that makes it a *family*
— the DISCRETE DEPTHS {D_n} — is not selected by postulate A (radial), and the two candidates
that could select it (the breather depth-potential U(D); the closed-time condition) are UNBUILT.
**The exponential is restored; the rungs are not yet handed out.** No false convergence claimed:
this is one informative tile — the split works on FORM, the ladder still needs a native
depth-selector.

---

## 7. PREMISE LEDGER (native / postulate-A / chosen)

| Item | tag | note |
|---|---|---|
| MS dilation cost `m=(c²r/2G)(1−e^{−2φ})` | **exact-from-corpus, NATIVE-to-metric (GR-FORM flag, Principle 7)** | B1 §1; native field-eq assignment of this m not re-audited (B1's inherited-form caveat carries over) |
| `φ = v0 = −D f(r)`, deep core → 0 exterior | **CHOSE (generic native-like)** | *** SHORTCUT: modeled profile, not the pointwise coupled v0; tested 4 profiles — exp verdict robust *** |
| `e^{−2φ} = e^{+2Df}` exponential in D (cost) | **DERIVED-here exact (sympy)** | the load-bearing "undifferentiated amplitude" fact |
| `V_L = ½s′ − ¼s²`, `s=2v0′` power-law in D (frequency) | **DERIVED-here exact (sympy)** | the "differentiated → polynomial" fact; matches quantization doc |
| `m_n ~ e^{2D_n}`, `m_n/m_0 ~ e^{2(D_n−D_0)}` | **DERIVED (form), depths NOT chosen** | structure only; {D_n} spacing left OPEN |
| depth sequence {D_n} (the rungs) | **UNAUDITED / NOT-YET-NATIVE** | needs C2 breather U(D) or C4 closed-time; FORBIDDEN to choose by hand (C5) |
| tachyon cap D* bounds deepest rung | **derived (carrier stability), profile-robust** | `ω²>0` required; cost does not lift it |
| core width `a`=1, `r_core`=0.02, grid h | **CHOSE (unit/numeric; cancel in ratios)** | scale-free; R-independence verified |
| any specific exponent (e^{2D}, D^{3.7}) | **SHAPE diagnostic, NOT banked** | no value promoted to evidence; data-blind |

---

## 8. ONE-LINE SUMMARY

The frequency-vs-cost split is REAL and clean: mass-as-COST `m=(c²r/2G)(1−e^{−2φ})` is
**EXPONENTIAL in depth** (`~e^{2D}`, profile-robust, sympy-exact), **SCALE-FREE in ratios**
(`m_n/m_0~e^{2(D_n−D_0)}`, all prefactors cancel), and **INTRINSIC / box-free** — restoring
exactly the exponential the eigen-FREQUENCY route differentiated away (frequency sees `v0′`,
power-law `~D^{3.7}`; cost sees `e^{−2φ}`, undifferentiated). **BUT** the discrete multi-rung
LADDER is NOT yet closed: postulate A (radial Bohr–Sommerfeld) quantizes the radial node n
(≈1 stable rung, then tachyon), NOT the DEPTH; the depth-selector that would hand out {D_n}
(a breather depth-potential `U(D)`, or a closed-time condition) is UNBUILT, and choosing a
spacing by hand is forbidden. **The exponential hierarchy now lives in a native exact box-free
cost functional (the right home) — but it is NOT yet ready for the gated value test, because
the native DEPTH-SELECTOR for the rungs is the precisely-named open obstruction.**

## STATUS
STRUCTURE-FIRST complete. Split CONFIRMED analytically (sympy-exact) + numerically (exp-vs-power
form test) + profile-robust (4 cores). Cost = exponential + scale-free + intrinsic (3/4 desiderata
clean). Obstruction NAMED and precise: the discrete depth-ladder {D_n} is not selected by
postulate A (radial); needs the UNBUILT breather depth-potential U(D) (C2) or closed-time (C4);
hand-spacing forbidden (C5). Tachyon cap D* still bounds deepest rung (cost does not lift it).
DATA-BLIND; anti-numerology PASS; no manufactured exponential (derived, not fitted). One SHORTCUT
flagged (modeled profile; coupled breather not built) — does not change the structural verdict.
NOT canon. No git commit. Blind verifier next.
