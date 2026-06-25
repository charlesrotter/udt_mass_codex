# B1 — Mass as the Dilation COST of the Charge (algebraic read-off)

**Mode:** ALGEBRAIC DERIVE (exact symbolic) **+ IMPORT-PROVENANCE AUDIT.**
TRACK B / STEP B1 of ALGEBRAIC_MATTER_PATH_PLAN.md.
**Agent:** claude-opus-4-8[1m]. **Date:** 2026-06-19.
**Status:** NOT canon. Working algebraic-derive + audit record. Append-only.
**Script:** `B1_mass_charge_identities.py` (sympy-exact; all identities below
reproduced machine-exact, no grid / box / cutoff / numeric PDE as instrument).
**DATA-BLIND:** no lepton wall numbers (contract 26fc757) and no empirical
mass/ratio loaded anywhere in this work — verified by inspection of the script.

---

## 0. The question (restated)

Express the MASS of a charge-N cell as an EXACT closed-form algebraic
functional of the topological (area-form) CHARGE — "the dilation cost of the
charge" — symbolically. If `mass = f(N)` exactly, the mass is DISCRETE because
N is. CORE: assembling **only AUDITED-NATIVE pieces**, is the Misner–Sharp mass
an exact function of the topological charge N (via Q=2p_F, the native
transgression, the area form), with no numerically-fitted input?

**Headline answer:** the **charge ladder closes natively and exactly** (N→q→η);
the **Misner–Sharp mass closed form is exact and native**; but the **BRIDGE from
the charge to a dimensionful mass does NOT close on N alone.** B1 closes
**PARTIALLY** — the *charge label* `Q = q = 1 − 2/N` is an exact discrete
functional of N (clean, native), but the *dimensionful MS mass* carries a free
overall scale and the corpus's own additivity-over-depth result is REFUTED. The
obstruction is NAMED below. No closed form `mass(N)` was manufactured by fitting
or by leaning on an import — and one tempting "closure" (the η/2-per-e-fold
ladder) is shown to be a scoped, leading-order-only object, not an exact law.

---

## 1. PROVENANCE AUDIT TABLE (the non-negotiable guardrail A)

Each object used: **NATIVE** (provably from the UDT metric / area form /
dilation — derivation shown) vs **IMPORT** (borrowed SM/QCD/topology template)
vs **UNAUDITED**. Citations are file:line from the corpus dig.

| # | Object | Exact form | Provenance verdict | Evidence / derivation |
|---|--------|-----------|--------------------|-----------------------|
| 1 | Area-form charge `ω_H1` | `ω_H1 = ε_ijk n_i dn_j∧dn_k = sinθ dθ∧dφ`, `∫ω_H1=4π` | **NATIVE** | S² area 2-form of the metric's OWN ℓ=1 carrier `n`; deg-1 generator of `H²(S²,ℤ)`. Same object that sources B=1/A (CANON C-2026-06-14-1). h1_types:31-37 |
| 2 | Topological invariant | degree ∈ `π₂(S²)=ℤ` (= 1 for hedgehog); **Hopf charge = 0** | **NATIVE** | degree of the shell map, integer read-off, no grid. crux1_statistics_topology:49-52,71,81 |
| 3 | `N=3` | two locks: `C(N,3)=1` (ε-singlet) **and** `C(N²,2)=4N² ⇒ N²−1=8 ⇒ N=3` | **NATIVE, NOT color** | a *dimensional* lock on the ℓ=1 operator algebra (`8=3⊕5` only at ℓ=1), NOT a winding number. su(3) **KINEMATICS** = metric-given (selection rule); su(3) **DYNAMICS** (color force/confinement/running α_s) = NOT metric-given, explicitly excluded. h1_types:161-162; UDT_REBUILD:73-76. **N=3 is the area form's geometric three-ness, NOT QCD color** (HANDOFF_ARCHIVE:202). Verified exact in script [1]. |
| 4 | `q = 1 − 2/N = 1/3` | collar slope `d ln f = −q d ln r` | **NATIVE, NOT quark charge** | the dilation SLOPE of the metric near the seal, the public charge of the transgression Θ; explicitly *not* fractional quark charge. h1_types:163; global_spin_structure:202-205. Verified [2]. |
| 5 | `η = q/6 = 1/18` | seal action density | **NATIVE (derived from q), one N-specific flag** | η=q/6 is arithmetic from q. ALSO written η=`2/dim Λ²End(H1)=2/36`; the two formulas agree **only at N=3** (script [2]: `eta_dim==q/6` general-N → **False**). So η=1/18 is native, but the "2/dim" route is an N-specific coincidence with the q/6 route — record, do not double-bank. legacy_hadron:169; w8_catalog:265 |
| 6 | Transgression `Θ=(ln f)·ω_H1`, `Ξ=dΘ=−q(dr/r)∧ω_H1` | EXACT form; `∫Ξ=4π(ln f)_seal =: D` | **NATIVE, metric's OWN forms** | Θ is the metric dilaton `ln f` wedged with the metric's own area form — NOT an imported Chern–Simons/WZW class. EXACT ⇒ zero bulk Euler–Lagrange ⇒ by Stokes its *entire* content is the seal boundary value. native_stabilizer:188-201,324; topo:16-18; theta_bc_provenance:113-116 |
| 7 | Misner–Sharp mass `m(r)=(c²r/2G)(1−e^{−2φ})` | integrated `G^t_t` constraint | **NATIVE-to-metric (GR-form, see audit note)** | reduced weld form `m(y,u)=(y/2)(1−f)`, `f=e^{−2φ}`. Verified exact [4]; seal limit `f→0 ⇒ m=y/2` (trapping saturation) exact. udt_canonical:1401-1403; macro_sector_fork:33; mass_audit:50-55. **AUDIT NOTE (Principle 7):** this is the standard MS quasi-local mass = integral of the standard Einstein `G^t_t`. It is metric-geometric and the macro stack validates it on data, but it is the GR-FORM mass. Per the new charter Principle 7, whether UDT's *native* field equations assign this same `m` (vs the GR-inherited form smuggling GR back in) is **NOT re-audited here** — flagged as an inherited-form dependency. |
| 8 | Public charge `Q = 2 p_F`, `p_F = γ/2` | `Q = γ` | **NATIVE (weld-jet theorem) — but reduced-class scoped** | `p_F` = interface monopole momentum = the MS mass the exterior sees; exact weld theorem `m(weld)=0`, `d_y m=`jet, `d²_y m=0` **WITHIN THE REDUCED SOURCE-FREE CLASS** (VMA amendment: physical H1-sourced tail has `m_yy(1+)=s=1/9`). mass_audit:18-30; ensembles:36-40. **SCOPED:** the two-sided jet theorem is reduced-class. |
| 9 | Charge–driving lock `γ = q` | at mirror-matched monopole driving | **NATIVE but MONOPOLE-SECTOR ONLY** | "γ = q (forced, MONOPOLE SECTOR ONLY, by finite-action welding to the cosmic tail; **the ℓ=1 drive needs exterior angular structure beyond the bare tail** — VMA caveat)". mass_audit:34-36. **This is the load-bearing bridge and it is NOT general.** |
| 10 | η/2-per-e-fold mass ladder `Δp_F ∝ exp(−(η/2)d)` | `Q_eff·g^d`, `g=3e^{−1/36}` | **IMPORT/UNAUDITED for the EXACT law — banked only leading-order** | `q²/4 = η/2 = 1/36` is a **selector echo**: `q²/4=(q/6)/2 iff q=1/3`, both repo-derived ⇒ **ZERO new evidential weight** (verified [3]). The depth `d=2L` is a "reading-grade" count, **no junction-condition derives it** (dpf_verifier:23-28,155,170). Additivity over depth is **REFUTED** (mass_audit:58-62). **Do NOT use as an exact mass(N).** |
| 11 | Index theorem | AS/APS | **IMPORT — scope-mismatch HALT** | standard index theorems require closed Riemannian / APS BC; UDT is Lorentzian + Neumann ⇒ inapplicable; native version NOT derived. udt_canonical:5912; udt_validated:29491. **For B2: not available as native.** |
| 12 | Junction condition / transfer ladder | recursion `r=C·g^d` | **UNAUDITED / hypothesis-grade** | full junction-condition PDE closure OPEN; transfer ladder is empirical-shaped, not metric-closed. dpf_verifier:155,170; particles_types:71. **For B2: not yet native.** |

---

## 2. What CLOSES natively and exactly (clean pieces)

Verified machine-exact in `B1_mass_charge_identities.py`:

**(a) The charge ladder is an exact, discrete functional of N (CLEAN, native).**
```
N = 3            (forced by C(N,3)=1 AND C(N²,2)=4N²; script [1])
q   = 1 − 2/N    = 1/3      (collar dilation slope; script [2])
η   = q/6        = 1/18
s   = q²         = 1/9
```
All three are exact functions of the integer N. Because N is a cohomology
degree (an integer with no continuum), **q, η, s are automatically DISCRETE.**
This is the B0 template working exactly — the read-off charge ladder is clean.

**(b) The Misner–Sharp "dilation cost" closed form is exact and native-to-metric.**
```
m(r) = (c²r / 2G)(1 − e^{−2φ(r)})        (script [4], exact)
```
This *is* literally a "dilation cost": `e^{−2φ}` is the metric's dilation factor
and `(1 − e^{−2φ})` is its **deficit from unity** — the cost of the dilation —
times the geometric radius `r` over `2G/c²`. The seal limit is exact and clean:
`φ→+∞ (f→0) ⇒ m → r/2` (in c=G=1), saturating the trapping bound — the seal is
exactly where the mass aspect reaches its own horizon radius (mass_audit:54-55).

**(c) The transgression is the exact native bridge bulk→boundary.**
`Θ=(ln f)·ω_H1` is EXACT, so by Stokes **all** its content is the single seal
number `D = 4π(ln f)_seal`. This is the genuinely native algebraic bridge from a
bulk topological object (the area form) to a boundary/seal quantity — built from
the metric's own dilaton `ln f` and own area form `ω_H1`, NOT an imported
Chern–Simons class. **This is the right shape for a charge→mass bridge.**

**(d) The charge LABEL Q is an exact discrete functional of N.**
```
Q = 2 p_F = γ ,   and at monopole driving  γ = q = 1 − 2/N      (script [5])
⇒ Q(N) = 1 − 2/N ,   Q(3) = 1/3      (DISCRETE because N is an integer)
```

---

## 3. Where B1 does NOT close — the NAMED obstruction(s)

The plan poses B1 as "mass = exact functional of the charge." The **charge**
side closes (§2). The **mass** side does **not** close on N alone. Three named
obstructions, each from the corpus's own verified record (not invented here):

**OBSTRUCTION O1 — the free dimensionful scale (the mass is not pure-N).**
The MS mass `m=(c²r/2G)(1−e^{−2φ(r)})` requires a *radius* `r` and the *full
profile* `φ(r)`, not just N. The charge ladder fixes only the **SLOPE** of the
dilation near the seal (`d ln f = −q d ln r`), i.e. `φ(r) ≈ (q/2)ln(r/r₀)`. The
**additive constant of φ** and the **seal radius r₀** are NOT fixed by N. The
script makes this explicit (block [6]):
```
collar profile  f=(r/r₀)^{−q},  φ=(q/2)ln(r/r₀)
⇒ m_collar = (c²/2G) · r^{1−q}(r^q − r₀^q)     — still carries r, r₀, c²/G.
```
So `m` is **dimensionful and scale-dependent**; N fixes its *exponent structure*
(`q=1/3`) but not its *normalisation*. A pure `mass(N)` would need that scale
fixed natively. CANON C-2026-06-18-1 + the dynamic-scale synthesis say the scale
is set by the universe's MS mass M (cosmic-only — it does **not** bridge to the
particle scale). **A legitimate single absolute anchor would have to come from
that cosmic scale or m_e; it is NOT supplied by the area-form charge.** This is
the same "scale-autonomy" open question CANON C-2026-06-10-2 named.

**OBSTRUCTION O2 — the charge↔mass bridge `γ = q` is MONOPOLE-SECTOR ONLY.**
The one relation that ties the dimensionful jet (`p_F`, hence `m`) to the
topological charge is `γ = q`, and it is **forced only in the monopole sector**:
"the ℓ=1 drive needs exterior angular structure beyond the bare tail" (VMA
caveat, mass_audit:34-36). So `Q = 1−2/N` is an honest *charge-label*
identity, but it does **not** propagate to "the dimensionful MS mass is `q`."
The weld theorem that makes `p_F` two-sided-clean is itself **reduced-class**
(O8 in the table; physical H1-sourced tail has `m_yy=1/9≠0`). The bridge is
scoped, not general.

**OBSTRUCTION O3 — additivity over depth is REFUTED (no charge-sum mass).**
A discrete-catalog mass formula of the form "stack the per-rung charge cost
`exp(−(η/2)d)`" would need the bulk action to ADD over depth. The corpus's own
audit **refutes** this for every bulk object: "no plateau; the last e-fold
carries ~64%; `A_tot` diverges ~`ε^{−1.3}`; **log-mass is NOT a bulk
functional**" (mass_audit:58-62). The MS mass `p_F` *does* converge at threshold
(`ε⁰`), but as a **weld-jet functional, not a charge sum**. And the η/2-per-e-fold
ladder that looks like a closed mass law is (i) a **selector echo** carrying zero
new weight (`q²/4=η/2` iff `q=1/3`, both derived — script [3]), and (ii) "banked
leading-order-only," with the depth `d=2L` a reading-grade count **no
junction-condition derives** (dpf_verifier:23-28). **It is not an exact law and
must not be presented as `mass(N)`.**

---

## 4. Is the mass DISCRETE? And the single scale?

- The **charge** (`N, q, η, s, Q`) is **DISCRETE** natively — integer cohomology
  degree, no continuum (clean).
- The **dimensionful mass** is **NOT shown discrete from the charge.** Its
  exponent structure is fixed by `q`, but its scale is a free dimensionful
  normalisation (O1) and the charge↔mass bridge is scoped (O2). There is no
  native charge-sum that would make a *spectrum* of masses (O3).
- **The single overall scale is NOT supplied by B1.** The only legitimate
  absolute anchor in the corpus is cosmic (the universe's MS mass M, CANON
  C-2026-06-18-1 / dynamic-scale synthesis), which is flagged as cosmic-only and
  does **not** bridge to particle scale. So B1 cannot identify "the one scale";
  it inherits the standing **scale-autonomy** open question. (This is consistent
  with the no-presumed-quantum-sector reframe: a *discrete spectrum* of masses,
  if it exists, is expected to come from a standing-wave / eigenvalue condition,
  NOT from the static charge cost — exactly the B2 territory the plan reserves.)

---

## 5. Premise ledger (chose / derived / exact-from-corpus — every non-exact step flagged)

| Premise | Tag | Note |
|---------|-----|------|
| `ω_H1`, `∫=4π`, degree∈ℤ | **exact-from-corpus, NATIVE** | metric's own S² area form |
| `N=3` (two locks) | **exact-from-corpus, NATIVE** | re-verified exact in script; not color |
| `q=1−2/N`, `η=q/6`, `s=q²` | **exact-from-corpus, NATIVE** | re-verified exact |
| `η=2/dim Λ²End` route | **derived, N-SPECIFIC FLAG** | agrees with q/6 *only* at N=3 (script) — do not double-bank |
| MS mass `m=(c²r/2G)(1−e^{−2φ})` | **exact-from-corpus; GR-FORM flag (Principle 7)** | integrated standard `G^t_t`; native field-eq assignment NOT re-audited here |
| `Q=2p_F`, `p_F=γ/2` | **derived, REDUCED-CLASS scoped** | weld-jet theorem two-sided only in reduced source-free class |
| `γ=q` bridge | **derived, MONOPOLE-SECTOR-ONLY** | ℓ=1 drive needs structure beyond bare tail — **the load-bearing gap** |
| collar profile `f=(r/r₀)^{−q}` | **derived (slope), scale CHOSEN-FREE** | additive const of φ + seal radius r₀ NOT fixed by N (O1) |
| η/2-per-e-fold mass ladder | **NOT banked as exact** | selector echo + reading-grade depth + additivity refuted (O3) |
| any specific number used as evidence | **none** | no rational was promoted to evidence; see §6 |

---

## 6. Numerology guardrail (B) + DATA-BLIND status

- **DATA-BLIND: PASS.** No lepton wall numbers (contract 26fc757) or any
  empirical mass/ratio appear in `B1_mass_charge_identities.py` or this doc.
- **No bare integer/rational was promoted to evidence.** The rationals here
  (`1/3, 1/18, 1/9, 1/36`) are all *re-derivations* of banked area-form
  quantities, used only to verify the algebra closes/agrees, not as new finds.
- **TEST-B-relevant flag recorded:** `η=2/dim Λ²End(H1)` and `η=q/6` coincide
  **only at N=3** (general-N: not equal — script [2]). This is exactly the kind
  of N-specific small-rational coincidence the null-test polices; it is RECORDED
  as a coincidence, **not banked as an independent lock.** The `q²/4=η/2=1/36`
  "triple" is a **double** (selector echo, zero new weight — mass_audit:38-43).
- No new rational identity is claimed as evidence here, so no TEST-B classifier
  run is required to bank a result — the deliverable is a **non-closure with a
  named obstruction**, which is import/numerology-clean by construction.

---

## 7. Honest read — does B1 close algebraically on NATIVE pieces?

**PARTIAL closure. Clean as far as it goes; does not reach `mass(N)`.**

- **CLEAN & native:** the charge ladder (`N→q→η→s`), the MS dilation-cost closed
  form, the exact transgression bridge bulk→seal, and the charge *label*
  `Q=2p_F=γ=q=1−2/N`. All exact, all from the metric's own area form/dilaton,
  all DISCRETE because N is. The B0 read-off template extends cleanly to the
  *charge* of the mass object and to the *form* of the dilation cost.

- **DOES NOT close to a dimensionful `mass(N)`**, blocked by three named,
  corpus-verified obstructions: **O1** a free dimensionful scale (N fixes the
  exponent `q`, not the normalisation — the standing scale-autonomy gap);
  **O2** the charge↔mass bridge `γ=q` is monopole-sector-only (the ℓ=1/angular
  drive beyond the bare tail is UNDERIVED — this is the load-bearing gap, and it
  is exactly Charles's standing φ–angular suspect); **O3** additivity over depth
  is REFUTED, so there is no native charge-sum to build a mass *spectrum*, and
  the η/2-per-e-fold ladder that mimics one is a scoped, leading-order,
  selector-echo object, **not** an exact law.

- **Import status:** the mass relation is **NOT import-contaminated** in the
  algebraic-sand sense — it does not secretly rest on a Chern–Simons/WZW/index
  template (those are absent or scope-halted, table #10-12). The honest result is
  a **native non-closure**: the pieces are native, but they don't assemble into a
  pure `mass(N)`. The **one inherited-form caveat** is Principle-7-shaped (the MS
  mass is the GR-form `G^t_t` integral; whether UDT's *native* field equations
  assign the same mass is not re-audited here — flagged, not resolved).

- **Where the prize lives (for B2, not done here):** a *discrete mass spectrum*
  is not produced by the static charge cost. It would have to come from fixing
  O1's scale (cosmic anchor or m_e) AND deriving O2's ℓ=1/angular bridge — i.e.
  the φ–angular coupling — most naturally as a standing-wave / eigenvalue
  condition (no-presumed-quantum-sector), which is precisely the
  transfer-ladder/junction territory B2 reserves and which is **UNAUDITED /
  not-yet-native** today (table #11-12). **No false convergence is claimed:**
  B1 banks a clean charge-side read-off and a precisely-located mass-side wall.

---

## 8. One-line summary

`Q = 1 − 2/N` is an exact, native, discrete functional of the area-form charge;
the Misner–Sharp **dilation cost** `m=(c²r/2G)(1−e^{−2φ})` is an exact native
form — but the two do **not** assemble into a pure dimensionful `mass(N)`,
blocked by a free overall scale (O1), a monopole-only charge↔mass bridge (O2,
the φ–angular gap), and a refuted additivity-over-depth (O3). **B1 closes on the
CHARGE, not on the dimensionful MASS — a clean, native, non-closure with the
obstruction named.**
