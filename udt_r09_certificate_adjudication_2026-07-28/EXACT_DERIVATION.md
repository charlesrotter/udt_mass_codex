# Exact derivation — R09 certificate adjudication (C_restricted vs C_full)

Date: 2026-07-28. Branch: `grok`. Contract: `PREREGISTRATION.md` in this package
(targets T-b1..T-b4, falsifiers F-b1/F-b2, maximum conclusion). Machine record:
`derive_r09_adjudication.py` → `DERIVATION_RESULT.json` / `DERIVATION_STDOUT.txt`
(73 checks, all zero-residual sympy passes plus exact-rational numeric spot checks,
exit 0). Check names below in `[brackets]` refer to that JSON.

Parents (only imports permitted):

- P-OWN = `udt_higher_isometry_plane_ownership_audit_2026-07-28/EXACT_DERIVATION.md`
  (family §1, Gram `G3` §2, response `D3` + quoted entries §3, Cartan §3, witness §6).
- P-SEL = `udt_alpha_plane_selector_theorem_2026-07-28/EXACT_DERIVATION.md` +
  `derive_alpha_plane_selector.py` (the banked certificate C_restricted, conventions,
  derivative rules, T4 Cartan theorem, T6 area record, selector branches (b)/(c)).

## 0. Setting and premise ledger (inherited; tags restated)

`g = -u(c_E dt + alpha A)^2 + u^{-1} A^2 + q_B` on `R x S3`, `u = e^{-2 phi} > 0`;
`A` the registered Hopf connection (`A(V) = 1`), `K` the stationary generator, `V` the
registered vertical circle, `Y` the second commuting compact Killing generator;
`f = A(Y)`, `H = Y - f V`, `b = q_B(H,H) > 0` on principal orbits; `X` transverse;
`chi = X(phi)`, `X(u) = -2 chi u`, `X(f) = df`, `X(b) = db`; `alpha`, `c_E`
constants annihilated by `X`.

| Premise | Tag |
|---|---|
| Family + registration (constant alpha, stationary, descended, Hopf bundle) | CHOSE — inherited; every conclusion scoped to it |
| Candidate planes: span(K, mV + nY), real (m,n) != (0,0) | DERIVED-inherited (preregistration; superset of P-OWN §7's two free lines) |
| `G3`, `D3 = G3^{-1} X(G3)`, derivative rules | DERIVED — P-OWN §2/§3, reproduced independently here (F-b2 gate, §1 below) |
| C_restricted = the selector certificate (constant area, K-eigenline, rates ±2chi of the RESTRICTED response `D_P = G_P^{-1} X(G_P)`) | DERIVED-inherited (P-SEL, banked); its selection map is IMPORTED from P-SEL T5, not re-derived |
| C_full = D3-invariance of the plane (+ optional founded-rates leg on `D3|_P`) | DERIVED-inherited (P-OWN §3's R02 invariance usage); both variants tested per contract |
| `{df != 0}` nonempty open on admissible members | DERIVED-inherited — P-SEL §5 (T4, Cartan), banked form; its pointwise strengthening is used ONLY where flagged (§3 cap corollary) |
| Principal orbits only (`b > 0`) | THEORY — P-OWN §1 (`D3` undefined at caps) |
| Clock = K | CONDITIONAL — inherited from P-SEL (fixed-profile clock cancellations OPEN) |

## 1. F-b2 gate — the parent's `D3` reproduced exactly

Independent implementation of `G3` and `X`, then `D3 = G3^{-1} X(G3)`, reproduces
every parent-quoted entry with zero residual `[P00–P08]`: `det G3 = -b c_E^2`;
`tr D3 = db/b`; the full characteristic polynomial of P-OWN §3; the obstructions
`p(-2chi) = -4 alpha^2 df^2 u chi / b` and `p(+2chi) = -4 df^2 chi/(b u)`; the
leakage entries (Y-components of `D3(K)`, `D3(V)`)

```text
D3[Y,K] = -alpha c_E df u / b,      D3[Y,V] = -df (alpha^2 u^2 - 1)/(b u);
```

the `df = 0` factorization `(lam + 2chi)(lam - 2chi)(lam - db/b)`; and the parent
machine record's full matrix (`expected_D` of the P-OWN script, check A04 there).
**F-b2 does NOT fire.** The contract's stop condition is not met; the derivation
proceeds.

## 2. Invariance formulation (stated precisely, frozen before use)

A Killing vector `z0 K + z1 V + z2 Y` is the column `(z0, z1, z2)^T`; `D3` acts on
columns from the left. For `P = span(K, W)`, `W = m V + n Y`, define the membership
functional

```text
L(v) = n v_V - m v_Y ;        v in P  iff  L(v) = 0 .
```

**P is `D3`-invariant at a point iff `I1 := L(D3 K) = 0` and `I2 := L(D3 W) = 0`
there; P is `D3`-invariant on a region iff both hold at every point.** For
`(m,n) = (1,0)` these are exactly (minus) the parent R02 conditions — the
Y-components of `D3(K)` and `D3(V)` — gated `[C03]`. Exact closed forms
(`z := m + n f`) `[C01, C02]`:

```text
I1 = alpha c_E df u z / b
I2 = [ alpha^2 df u^2 z^2 + u n z (2 b chi - db) + df (n^2 b u - z^2) ] / (b u).
```

C_full without the optional leg = region-wide `D3`-invariance. C_full WITH the leg
additionally demands that the spectrum of `D3` restricted to `P` be exactly the
founded pair `(-2 chi, +2 chi)` at every point.

## 3. T-b1 — complete stratified enumeration of `D3`-invariant planes

Strata are jet-level: `(alpha = 0 / != 0) x (df = 0 / != 0)` pointwise, `db` free
(unconstrained; a fixed value of `db` is flagged separately as a fixed-member locus).
`u, b > 0`, `c_E > 0`, and `f, chi` free throughout.

- **Stratum A (`alpha != 0`, `df != 0`): EMPTY — even pointwise.** `I1 = 0` forces
  `z = 0` at the point; substituting `m = -n f` gives `I2 = df n^2` exactly `[SA1]`,
  nonzero unless `n = 0`; but `z = 0` with `n = 0` gives `m = 0`, excluded. **No
  candidate plane is `D3`-invariant at ANY single point of this stratum.**
- **Stratum B (`alpha != 0`, `df = 0`):** `I1 = 0` identically `[SB1]` and
  `I2 = n z (2 chi - db/b)` `[SB2]`. With `db` (and `f`) free, `n z != 0` cannot hold
  identically, so `n = 0`: **span(K,V) is the UNIQUE invariant plane**, with founded
  restricted rates `(-2chi, +2chi)` `[SB3]`. Pointwise exceptional loci (recorded, not
  planes-of-the-stratum): at `z = 0` the plane `span(K, H)` is invariant with second
  rate `db/b` `[SB6]`; at `db = 2 b chi`, `D3` becomes `(-2chi) ⊕ 2chi·I_2` up to the
  K-row `[SB4]` and **EVERY candidate plane is invariant with founded rates** `[SB5]`.
- **Stratum C (`alpha = 0`, `df != 0`): EMPTY with `db` free.** `I1 == 0` identically
  `[SC1]`; the `db`-coefficient of `I2` is `-n z / b` `[SC2]`, so an identity in `db`
  needs `n z = 0`; `n = 0` gives `I2 = -m^2 df/(b u) != 0` `[SC3]` and `z = 0` gives
  `I2 = df n^2 != 0` `[SA1]`. **Fixed-member locus (the door T-b2 walks through):**
  at a point whose OWN `db` equals

  ```text
  db = 2 b chi + df (n^2 b u - z^2) / (u n z),     n z != 0,
  ```

  the plane IS invariant `[SC4]`, `K` is an exact eigenvector with rate `-2 chi`
  `[SC5]`, and the second restricted rate is exactly

  ```text
  mu = 2 chi + n df / z      [SC6, SC7]
  ```

  — off the founded pair at every `df != 0` point (`n != 0, z != 0` are forced by
  invariance there).
- **Stratum D (`alpha = 0`, `df = 0`):** identical factorization to stratum B
  (`alpha` enters `I2` only through the `df`-term): **span(K,V) uniquely** with `db`
  free; same pointwise exceptional loci `z = 0` / `db = 2 b chi`.

## 4. T-b2 — the adjudication

C_restricted's selection map is imported from P-SEL T5: it crowns span(K,V) always at
`alpha != 0`, and at `alpha = 0` iff `b u + f^2` is nonconstant (`X(b u + f^2) != 0`
somewhere); on `{alpha = 0, b u + f^2 constant}` it is silent.

### 4.1 C_full WITH the founded-rates leg: **NO-CONFLICT**

**C_full-with-rates is EMPTY on every admissible member** — a fortiori wherever
C_restricted selects. Proof: `{df != 0}` is nonempty open (P-SEL T4, banked form).
Let `P` satisfy C_full region-wide and take any point with `df != 0`. If
`alpha != 0`: impossible — stratum A is empty pointwise (§3). If `alpha = 0`:
invariance at the point forces `n != 0`, `z != 0` and the `db`-locus, whereupon the
restricted spectrum is `(-2 chi, 2 chi + n df/z)` with `n df / z != 0` — the rates
leg fails at that point, hence region-wide. This is the preregistered NO-CONFLICT
outcome in its strong form: *the full criterion is empty where the founded
certificate selects (indeed everywhere), so no crowning conflict is possible in this
family.* (Adding a K-eigenline leg to C_full would only shrink it further; the
verdict is robust to that strengthening.)

### 4.2 C_full WITHOUT the founded-rates leg: **CONFLICT — falsifier F-b1 FIRES**

Admissibility here = a member of the registered family on its connected
principal-orbit region (the parents' evaluation domain and this contract's premise
"principal orbits only"). Exact witness:

```text
alpha = 0;  Hopf chart;  V = d_xi1 + d_xi2,  Y = d_xi1 - d_xi2,  f = cos(2 eta);
u = 2 + f  (smooth, in [1,3], nonconstant depth);
b u = 6 + f - f^2 = (3 - f)(2 + f) > 0  on the whole principal region  [W00];
q_B torus-invariant positive with q_B(H,H) = b;  X = d/d eta;  eta in (0, pi/2).
```

- **`P = span(K, 2V + Y)` is `D3`-invariant at EVERY principal point** `[W01]`
  (zero-residual in `eta`), as is `span(K, -3V + Y)` `[W02]`; the COMPLETE
  invariant-plane list on this member is `(m + 3n)(m - 2n) = 0`: exactly these two,
  since `I2 · b u = -df (m + 3n)(m - 2n)` here `[W03]`. Neither is span(K,V);
  span(K,V), span(K,Y), span(K,V+Y) all fail C_full on this member `[W04]`.
- **C_restricted crowns span(K,V) within P-SEL's two-candidate set {V,Y}:**
  `b u + f^2 = 6 + f` is nonconstant (`X(b u + f^2) = df != 0` on the region) `[W05]`,
  so P-SEL branch (c) selects span(K,V) uniquely AMONG {span(K,V), span(K,Y)} — the only
  uniqueness P-SEL T5 proves (its T6 general-(m,n) row is record-only). Directly: span(K,V)
  keeps `det = -c_E^2` constant `[W09]`, while `P` FAILS C_restricted's area leg:
  `X(det G(K, 2V+Y)) = -5 c_E^2 df != 0` `[W06–W08]` (native recomputation agreeing with
  P-SEL T6). CORRECTION (blind verifier, 2026-07-28 — see CORRECTION_LAYER.md): over THIS
  package's own general-(m,n) candidate premise, uniqueness FAILS on this member —
  **span(K, V−2Y)** also passes all three C_restricted legs (`det = -25 c_E^2` constant,
  diagonal response, rates exactly `(-2chi, +2chi)`). The CONFLICT verdict is unaffected and
  strengthened: the C_restricted satisfier set {span(K,V), span(K,V−2Y)} and the C_full
  satisfier set {span(K,2V+Y), span(K,−3V+Y)} are DISJOINT.
- **The two criteria crown DIFFERENT planes on this member.** The restricted rates on
  `P` are `(-2 chi, 2 chi + df/(2 + f))` `[W10]` — at `alpha = 0`, `K` is an exact
  `D3` eigenvector, so even `C_full + K-eigenline` still conflicts; **the entire
  adjudication hinges on the founded-rates leg alone.**

Numeric spot checks: 5 exact-rational admissible points per jet stratum
`[N_A_*, N_B_*, N_C_*, N_D_*]` and 6 exact `eta` points on the witness `[N_W_*]`
— all symbolic verdicts confirmed exactly (no floating point).

### 4.3 Record — cap-closure corollary (conditional)

If admissibility is strengthened to complete two-cap `S3` members, then `b -> 0` at
BOTH caps (the base projection of `Y` vanishes at the poles), and — conditional on
`df != 0` throughout the principal region (P-SEL T4's recorded pointwise
strengthening; unconditional for the standard toric presentation `f = cos 2 eta`) —
region-wide invariance at `alpha = 0` integrates to `b u = z (Ct - f/n)` (the full
solution family of the first-order linear invariance ODE `[K01, K02]`). Two-cap
closure then factors as `(m+n)(Ct - 1/n) = 0` and `(m-n)(Ct + 1/n) = 0` `[K03]`:
for `m != ±n` the two demands contradict `[K06]`; the only closing branches are
`(m,n) ∝ (1,1)` and `(1,-1)`, BOTH giving `b u = 1 - f^2` `[K04, K05]`, hence
`b u + f^2 = 1` CONSTANT `[K07]` — the member lies ON the selector's exceptional
stratum, where C_restricted is silent. **Under this strict reading NO-CONFLICT is
restored even without the rates leg.** The parent's own §6 witness realizes it:
`span(K, V+Y)` and `span(K, V-Y)` — the two coordinate-circle planes `2 d_xi1`,
`2 d_xi2` — are `D3`-invariant on it `[K08–K10]`. (Record; the preregistered T-b2
verdict is the principal-orbit one of §4.2.)

## 5. T-b3 — crowning agreement on the `df = 0` strata

On `df = 0` (where P-OWN says span(K,V) IS `D3`-invariant):

- `alpha != 0`, `db != 2 b chi`: **AGREE** — C_full crowns span(K,V) uniquely with
  founded rates (§3 stratum B); C_restricted always selects at `alpha != 0`.
- `alpha = 0`, `db != 2 b chi`: **AGREE** — at `df = 0`,
  `X(b u + f^2) = u (db - 2 b chi) != 0`, so C_restricted selects; C_full crowns
  span(K,V) uniquely.
- `alpha = 0`, `db = 2 b chi` (exactly the exceptional condition
  `X(b u + f^2) = 0` at `df = 0`): **AGREEMENT-IN-SILENCE** — C_restricted is silent
  and C_full is non-selective (every plane invariant with founded rates, `[SB4/SB5]`).
- `alpha != 0`, `db = 2 b chi`: a FORMAL pointwise disagreement (C_full
  non-selective, all planes founded-invariant; C_restricted selects span(K,V)) —
  unrealizable region-wide on admissible members, since `{df != 0}` is nonempty open
  (P-SEL T4) and C_full is a region-wide requirement; under T4's pointwise
  strengthening the `df = 0` strata contain no admissible-member points at all.

## 6. T-b4 — rate spectra of `D3` restricted to each invariant plane (record only)

| Plane | Locus | Restricted spectrum | Founded? |
|---|---|---|---|
| span(K,V) | `df = 0` (any alpha) | `(-2chi, +2chi)` | YES |
| every span(K,W) | `df = 0, db = 2 b chi` (any alpha) | `(-2chi, +2chi)` | YES (degenerate locus) |
| span(K,H) (`z = 0`, pointwise) | `df = 0` | `(-2chi, db/b)` | only if `db = 2 b chi` |
| span(K, mV+nY), `n z != 0`, `db`-locus | `alpha = 0, df != 0` | `(-2chi, 2chi + n df/z)` | NO |
| witness `P = span(K, 2V+Y)` | witness member | `(-2chi, 2chi + df/(2+f))` | NO |
| parent-witness span(K, V±Y) | `b u = 1 - f^2, alpha = 0` | `(-2chi, 2chi + df/(f±1))` | NO |

No claim is frozen from this table (per contract).

## 7. Verdict (within the preregistered ceiling)

Criteria-compatibility classification on the registered family, principal orbits,
clock = K conditional:

> **C_full WITH the founded-rates leg: NO-CONFLICT** — it is empty on every
> admissible member; the R09 caveat is downgraded, for this variant, to "the full
> criterion is empty where the founded certificate selects — no crowning conflict is
> possible in this family."
>
> **C_full WITHOUT the founded-rates leg: CONFLICT — F-b1 FIRES** (first-class
> outcome, banked with equal standing): an exact principal-orbit witness exists on
> which C_full crowns span(K, 2V+Y) (and span(K, -3V+Y)) while C_restricted crowns
> span(K,V). The disagreement risk named in the selector theorem's LIMITS #3 is
> REAL for invariance-only full-response ownership, and is neutralized exactly by
> the founded-rates leg (and, under strict two-cap admissibility, by cap closure —
> §4.3 record).

This does NOT decide which criterion is "the" ownership definition — that remains a
foundational call for Charles.

## 8. LIMITS (honest scope)

1. **The family itself is CHOSE** (registered constant-alpha stationary descended
   Hopf control). Nothing here says the family is preferred.
2. **Clock = K is CONDITIONAL** (inherited from P-SEL; fixed-profile clock
   cancellations OPEN).
3. **Principal orbits only; caps excluded.** `D3` is undefined where `b -> 0`. The
   CONFLICT verdict of §4.2 is scoped to principal-orbit-region admissibility (the
   parents' evaluation domain and this contract's premise); §4.3 records that strict
   two-cap completeness dissolves it, so the T-b2 outcome is
   ADMISSIBILITY-READING-DEPENDENT at the leg-free variant — both readings are
   stated, neither is adopted as "the" reading.
4. **No criterion is adopted as THE ownership definition.** This package classifies
   compatibility only; C_restricted's selection map is imported from P-SEL, not
   re-derived.
5. **The cap corollary (§4.3) is conditional** on `df != 0` throughout the principal
   region (T4's recorded pointwise strengthening, or the standard toric
   presentation); under only the banked "nonempty open" form, constants of
   integration need not propagate across hypothetical interior `df = 0` sets.
6. **`db`-free vs fixed-member readings are both reported in T-b1** (the
   preregistration's "db free" enumeration is the headline; the fixed-member locus
   is what T-b2's witness realizes — stated separately, no conflation).
7. **Constant-depth members** (`chi == 0`): the certificates degenerate (P-SEL
   LIMITS #6); all identities here still hold trivially; the witness has
   nonconstant depth by construction.
8. **No physics.** No physical branch, alpha value, action, source, carrier,
   density law, dynamics, or mass emergence is selected or constrained.
