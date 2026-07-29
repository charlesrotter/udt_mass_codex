# Exact derivation — cap gluing of the plane-selector certificate

Date: 2026-07-28. Branch: `grok`. Contract: `PREREGISTRATION.md` in this package
(T-c1..T-c4, falsifiers F-c1..F-c3, maximum conclusion). Machine record:
`derive_cap_gluing.py` → `DERIVATION_RESULT.json` / `DERIVATION_STDOUT.txt`
(72 checks, all zero-residual sympy passes, exit 0). Check names below in
`[brackets]` refer to that JSON.

Parents (only imports permitted):

- P-OWN = `udt_higher_isometry_plane_ownership_audit_2026-07-28/EXACT_DERIVATION.md`
  (family §1, Gram `G3` §2, full response §3, witness §6, two-free-lines/cap-lattice §7,
  `FREE_CIRCLE_CLASSES.tsv`).
- P-SEL = `udt_alpha_plane_selector_theorem_2026-07-28/EXACT_DERIVATION.md`
  (certificate quantities `det G_KY = -c_E^2 (b u + f^2)`, off-eigenline term
  `-alpha c_E df u^2/(b u + f^2)`, `tr D_KY = X(b u + f^2)/(b u + f^2)`; conventions §0;
  exceptional stratum §6).

## 0. Setting and what "regular cap" means (registered vs derived)

Inherited family (CHOSE, P-OWN §1 / P-SEL §0): `g = -u(c_E dt + alpha A)^2 + u^{-1} A^2 + q_B`
on `R x S3`, `u = e^{-2 phi} > 0`, `A` the registered smooth Hopf connection with `A(V) = 1`,
`V` vertical, `q_B` basic and positive on horizontal vectors, `Y` the second commuting compact
Killing generator, `f = A(Y)`, `H = Y - f V`, `b = q_B(H,H)`, `alpha, c_E` constants.

REGISTERED toric structure used here (each tag "chose or derived?" made explicit):

| Input | Tag |
|---|---|
| Two-cap toric completion of `S3`; primitive cap cycles `(v_-, v_+)` a unimodular basis of the `2 pi`-periodic torus lattice | REGISTERED — P-OWN §7 ("as required for the smooth two-cap S3 completion") |
| `{V, Y}` = the two free circle lines `v_- ± v_+` (up to overall signs) | DERIVED-inherited — P-OWN §7 + P-SEL premise row (topology supplies exactly two); which one is `V` = registration of the Hopf bundle |
| `A` smooth on the completed manifold, `A(V) = 1`; the torus acts smoothly on the completion; `g` smooth | REGISTERED — family presentation |
| "Regular cap" = the closing primitive cap cycle degenerates smoothly, `2 pi` period, no conical defect | REGISTERED — the meaning of regularity (P-OWN §6 "no cone defect"); this is the standard smooth-completion condition |
| Smooth rotation-invariant functions on the transverse disc are smooth functions of `rho^2` (rho = transverse geodesic distance); a closing circle of period `2 pi` needs `g(w,w) = rho^2 (1 + O(rho^2))` | STANDARD MATH, Category-A borrow (GR-corpus axis/bolt regularity; Whitney/Schwarz invariant-function fact). Changes nothing physical; machine-controlled below `[Tc2_evenness_negative_control, Tc1_gww_leading]` |

Everything else below is DERIVED in this run. No cap-extended response `D_P` is claimed
anywhere: `D_P` is undefined at `b = 0`; only LIMITS of the scalar certificate quantities
(and of the matrices' entries as functions on the principal region) are computed.

## 1. T-c1 — regular-cap conditions

**1.1 Which circle can close.** A cap is the fixed-point core of the closing circle
subgroup; its Killing generator `w` vanishes on the core (a Killing field vanishes at
fixed points of its flow — triviality). Write `w = x V + y Y` in the free-line basis.
Since `A` is a smooth one-form on the completion, `A(w) = x + y f -> A(0) = 0` at the core.

- **`V` never closes (DERIVED).** `w = ±V` means `(x, y) = (±1, 0)` and then
  `A(w) = ±1`, a nonzero constant — it cannot tend to 0 `[Tc1_V_never_closes]`. This
  answers the preregistration's case (i): the "registered line V closes" branch is
  IMPOSSIBLE inside the family, from `A(V) = 1` + smoothness alone.
- **`Y` never closes in the registered completion.** `Y` is a free line (P-OWN §7 /
  P-SEL candidate-set premise); a free circle has no fixed points. (Hypothetical
  non-registered completions closing `Y` are recorded in §3 only.) This answers case (ii).
- **What actually closes (DERIVED).** The cap cycles are `v_-` and `v_+` themselves.
  Solving the lattice relations for every sign labeling of `V = ±(v_- + v_+)`,
  `Y = ±(v_- - v_+)`: each cap cycle has coordinates `|x| = |y| = 1/2` in `(V, Y)`,
  i.e. the closers are `(V ± Y)/2` `[Tc1_cap_cycle_coords]`. In the witness these are
  `∂_xi2` (closing at `eta = 0`) and `∂_xi1` (closing at `eta = pi/2`).

**1.2 The moment at the cap (DERIVED — the preregistration's candidate, confirmed with
its exact mechanism).** With `y != 0`, `A(w) -> 0` forces

```text
f -> f_cap = -x/y        [Tc1_fcap_formula]
```

and in the registered completion `f_cap = ±1` exactly, with OPPOSITE signs at the two
caps (`+1` at one, `-1` at the other, up to the global sign of `Y`)
`[Tc1_fcap_registered, Tc1_fcap_opposite]`. Witness control: `f = cos 2 eta -> +1, -1`
`[W_fcap_eta0, W_fcap_etapi2]`. So "`f -> ±1` = primitive closing" is DERIVED, not
assumed — and the mechanism is sharper than the candidate: `f_cap` is the lattice ratio
`-x/y` of the closing cycle, and `±1` is exactly the registered free-line structure.

**1.3 `b -> 0` at every cap (DERIVED).** From the parent Gram `G3` (P-OWN §2),

```text
g(w,w) = Q (x + y f)^2 + y^2 b,       Q = u^{-1} - alpha^2 u     [Tc1_gww_formula]
```

and at the cap moment value `f = -x/y` the identity `H = w/y` holds exactly
`[Tc1_H_is_w_over_y]`, so in the limit `y^2 b / g(w,w) -> 1` `[Tc1_b_gww_ratio]`: `b`
vanishes exactly as fast as the closing norm, for EVERY admissible `alpha` and screen.
(Wording per verifier: the ratio statement is the exact limit form; `b = g(w,w)/y^2` holds
at the cap moment value as a limit identity.) The parent's "at a toric cap `b` can vanish"
is upgraded: at a regular cap `b` MUST vanish.

**1.3b `u0` bounded and positive (DERIVED — verifier-required discharge, 2026-07-28).**
`u -> u0 in (0, infinity)` at a regular cap is FORCED by registered premises, not assumed:
`g` is smooth on the completion and `K` is non-vanishing there, so `g(K,K) = -c_E^2 u`
is finite, giving `u0 < infinity`; and `V` limits to the surviving (non-vanishing) cap-cycle
generator, so `g(V,V) = Q = 1/u - alpha^2 u` is finite, which at `u -> 0` would diverge —
giving `u0 > 0`. (Previously carried as a positive-symbol assumption; re-tagged DERIVED.
This discharge is load-bearing for §1.3's `b -> 0` and for T-c3.)

**1.4 Rates (DERIVED, cap series model).** Let `rho` be transverse geodesic distance
from the core. The `-> 0` limit statements below are scoped to transverse directions `X`
extending boundedly/smoothly across the cap (any smooth completion direction qualifies;
verifier probe: a non-smooth `X = (1/rho) d_rho` shifts `chi`'s limit — T-c3 itself involves
no `X`). The invariant scalars `u, f, b` extend to smooth torus-invariant
functions on the completion, hence are smooth EVEN functions of `rho` (§0 standard-math
row; negative control: an odd jet breaks `C^1` across the core, jump `= 2 f1`
`[Tc2_evenness_negative_control]`). Writing `u = u0 + u2 rho^2 + ...`,
`f = f_cap + f2 rho^2 + ...`, `b = b2 rho^2 + ...`:

- `g(w,w) = y^2 b2 rho^2 + O(rho^4)` — the `Q (x+yf)^2` term is `O(rho^4)`
  `[Tc1_gww_leading]`; the `2 pi`/no-cone condition `g(w,w) = rho^2 (1 + O(rho^2))` forces
  **`b2 = 1/y^2`**, i.e. registered `b = 4 rho^2 (1 + O(rho^2))` `[Tc1_b_rate]`.
- **`chi -> 0` at every regular cap** (`u` even): `chi = -(u2/u0) rho + O(rho^3)`
  `[Tc1_chi_zero, Tc1_chi_rate]`. Regular caps are depth-critical points.
- **`df -> 0` at every regular cap** (`f` even), at the specific rate
  `df = 2 f2 rho + O(rho^3) = O(sqrt(b))`:
  `df^2/b -> 4 f2^2/b2 = 4 f2^2 y^2` (unit rate) `[Tc2_df_zero, Tc1_df_rate_general,
  Tc1_df_rate_unit]`. Witness: `df^2/b -> 4` with `f2 = -2, y = -1/2, u0 = 1`
  `[W_df_rate]`; non-witness NW1: `df^2/b -> 81/25` at both caps `[NW1_df_rate]`.
- `db -> 0` (`b` even) `[Tc1_db_zero]`; cross-terms `g(w,K)` and `g(w,w')` (surviving
  cycle) vanish like `O(rho^2)` — consistency of the smooth completion
  `[Tc1_cross_K_formula, Tc1_cross_orbit_formula]`.

Observation (recorded, not load-bearing): by the parent Cartan identity `df = -i_Y F`
(P-OWN §3), the coefficient `f2` is the cap value of the base curvature density;
nondegenerate `F` up to the cap makes `f2 != 0`, so `O(sqrt(b))` is then the sharp rate,
not just an upper bound.

## 2. T-c2 — cap limit atlas of the certificate quantities

The three P-SEL formulas were recomputed INDEPENDENTLY from the Gram matrix inside this
run before taking limits (F-c3 guard) `[Tc2_det_recompute, Tc2_off_recompute,
Tc2_trace_recompute]`. Limits at a regular cap (general `x, y`, then registered):

| Quantity | Cap limit | Rate of approach |
|---|---|---|
| `det G_KY = -c_E^2 (b u + f^2)` | `-c_E^2 f_cap^2 = -c_E^2 x^2/y^2`; registered `= -c_E^2` — EQUAL to `det G_KV` | `O(rho^2)` `[Tc2_detGKY_limit_general, Tc2_detGKY_limit_registered]` |
| off-term `-alpha c_E df u^2/(b u + f^2)` | `0` | `-2 alpha c_E f2 u0^2 (y^2/x^2) rho + O(rho^3)`, i.e. `O(sqrt(b))` `[Tc2_off_limit, Tc2_off_rate]` |
| `tr D_KY = X(b u + f^2)/(b u + f^2)` | `0` | `O(rho)` `[Tc2_trace_limit]` |
| full `D_KY` (entrywise) | `0` matrix | `[Tc2_DKY_limit]` |
| `D_KV = [[-2 chi, -4 alpha chi/c_E], [0, 2 chi]]` | `0` matrix (`chi -> 0` forced) | `O(rho)` `[Tc2_DKV_limit]` |

**Answer to the frozen T-c2 question: `df -> 0` at caps is FORCED by regularity**
(evenness of the smooth invariant scalar `f` across the core), NOT witness-specific.
The witness merely instantiates it; NW1 (`alpha = 7/10`, off-stratum, non-witness
profiles) shows the same limits at both caps `[NW1_*]`.

## 3. T-c3 — the exceptional-stratum feedback (exact)

`S = b u + f^2 -> 0 · u0 + f_cap^2 = f_cap^2` at every regular cap
`[Tc3_S_limit_general]` (uses §1.3 `b -> 0` and §1.3b `u -> u0 in (0, infinity)`, the
latter DERIVED per the verifier-required discharge). Hence:

> **Theorem (cap value of the exceptional constant).** Let a member of the registered
> family lie on the exceptional stratum (`alpha = 0`, `b u + f^2 == c` on the connected
> principal region) and possess at least one regular cap. Then `c = f_cap^2` exactly
> (`S` is continuous up to the cap and constant on the dense principal region)
> `[Tc3_c_forced_series]`. In the registered two-cap completion — where the closing
> cycles are `(V ± Y)/2` and `f_cap = ±1` — BOTH caps and BOTH possible closing cap
> cycles give the same value `[Tc3_both_caps_both_lines]`:
>
> **`c = 1` exactly. Complete two-cap exceptional-stratum members have `c = 1`.**

**Corollary.** On complete two-cap exceptional members, `|det G_KY| = c_E^2 = |det G_KV|`:
the two certificate-silent planes carry the SAME constant reciprocal area. The P-SEL
witness (`b u + f^2 = 1`, `[W_on_stratum]` reproduced here) is not a coincidence of the
witness — the value `1` is forced by completeness. This decides the (d)-gate's
area-VALUE question for complete members; per the contract, no assumption travels from
here to (d) beyond this exact statement.

**Second lock (recorded).** `S == c` also kills the `O(rho^2)` jet of `S`:
`f2 = -b2 u0/(2 f_cap)` `[Tc3_stratum_rate_lock]` — with witness numbers
(`b2 = 4, u0 = 1, f_cap = +1`) this gives `f2 = -2`, exactly the jet of `cos 2 eta`
`[Tc3_rate_lock_witness_value]`. On complete exceptional members the moment's cap jet is
slaved to the depth's cap value.

**Instance + failure controls (non-witness).** NW2 (`alpha = 0`,
`f = cos 2 eta (1 + (1/20) sin^2 2 eta)`, `u = 1 + (3/10) sin^2 2 eta + (1/5) sin^2 eta`,
`b = (1 - f^2)/u`, transverse coefficient `v = (9/10) cos^2 eta + (3/4) sin^2 eta`
derived in-run from the unit-rate condition) is a complete two-cap exceptional member,
provably not of the witness form, with `c = 1` `[NW2_*]`. Forcing `c = 6/5` on the same
profiles leaves `b -> 1/5 != 0` at the cap — the circle does not close, no two-cap
completion exists; forcing `c = 4/5` makes `b < 0` near the caps — inadmissible
(`q_B` positive) `[NW3_c_gt1_fails, NW3_c_lt1_fails]`.

**General toric record (scope honesty).** For an arbitrary (non-registered) toric
completion the theorem reads `c = x^2/y^2`; a hypothetical completion closing the second
circle itself (`w = ±Y`) would force `c = 0` — but such a `Y` is not a free line and
falls outside the registered candidate set `[Tc1_Y_closing_record, Tc3_general_record]`.

## 4. T-c4 — continuity atlas

- **No certificate leg is singular or discontinuous at a regular cap.** All three legs'
  quantities extend continuously (§2 table): `det -> -c_E^2`, off-term `-> 0`,
  `tr -> 0`, and both restricted responses `D_KV, D_KY -> 0` entrywise. Nothing
  obstructs stating the selector theorem on the completed manifold minus caps; the cap
  boundary values are finite and matched between the two planes.
- **Degeneracy type at the cap.** Since `chi -> 0` is FORCED (regular caps are
  depth-critical), the founded rate pair `(-2 chi, +2 chi) -> (0, 0)`: at the cap the
  certificate's rate NORMALIZATION degenerates exactly as at interior `chi = 0` points,
  which the selector theorem's quantifier discipline already covers (P-SEL §6). The cap
  adds no new degeneracy class — it lands on an existing one.
- **The scope stamp was doing real work — for the FULL response.** The full
  three-direction trace `tr D3 = db/b` (P-OWN §3) DIVERGES like `2/rho` at a regular cap
  `[Tc4_D3_trace_diverges]` — the rank drop is real. That divergent object is NOT a
  certificate quantity; the restricted-plane certificate is exactly the part that
  survives the cap limit `[Tc4_certificate_continuous]`.

**Scope verdict:** the principal-orbit scope stamp of the selector theorem is RETAINED,
now with this atlas as its boundary annotation — and TIGHTENED on the exceptional
stratum: for complete two-cap members the stratum constant is pinned to `c = 1` (§3).

## 5. Falsifier review

- **F-c1** (regularity conditions underivable from the parents' recorded structure):
  does not fire. All conditions were derived from the registered structure plus one
  standard Category-A math fact (§0 table), machine-controlled. One preregistration
  FRAMING presupposition is corrected, not papered: the T-c1 dichotomy "closing circle =
  (i) V, (ii) Y" is empty — V closing is impossible (derived) and Y closing contradicts
  the registered free-line candidate set; the actual closers are the cap cycles
  `(V ± Y)/2`.
- **F-c2** (a certificate quantity divergent at a regular cap contaminating the
  classification): does not fire — every certificate quantity extends continuously
  (§2, §4). The only divergent object found, `tr D3 = db/b`, is not a certificate leg
  and is recorded as the reason the FULL-response operation genuinely needs the
  principal-orbit restriction.
- **F-c3** (algebra error): does not fire — 72/72 zero-residual checks; the three P-SEL
  certificate formulas were independently recomputed from the Gram matrix in this run
  before any limit was taken; witness (symbolic `eps`, symbolic `alpha`) and two
  non-witness exact-rational families agree with the series model at every point of
  contact (`df^2/b`, `f2` lock, `c = 1`).

## 6. LIMITS (honest scope)

1. **The family is CHOSE** (registered block-screen stationary descended constant-alpha
   Hopf control); every statement is scoped to it and to its registered two-cap toric
   completion (unimodular cap basis, `{V, Y}` the two free lines).
2. **No cap-extended response is claimed.** `D_P` is undefined at `b = 0`; everything
   here is a LIMIT of quantities defined on the principal region. The `-> 0` limits of
   `D_KV, D_KY` are limits of their entries, not a definition of a response AT the cap.
3. **"Regular cap" is the registered smooth-completion condition** (`2 pi` period, no
   cone); conical or otherwise singular caps are outside scope. The evenness/axis
   machinery is standard borrowed technique (Category A), soundness-checked by the
   negative control and three profile families, not a physical mechanism.
4. **Series truncation is not an approximation of results**: every limit computed
   depends only on the finite jet orders displayed; the `O(rho^4)` truncation is exact
   for those limits (no linearization enters any banked claim).
5. **T-c3's `c = 1` requires completeness** (two regular caps — one regular cap already
   suffices for `c = f_cap^2`; the registered structure makes it `1`). Non-complete
   exceptional members (principal region not capped regularly) keep a free `c`. The
   P-SEL "exceptional stratum remainder OPEN" limit is NARROWED, not closed: on complete
   members the stratum has `c = 1` and both planes carry equal area; whether some other
   selector exists there remains OPEN.
6. **The selector theorem's other limits travel unchanged** (clock = K conditional;
   certificate-relative R09; constant-depth degeneration; family CHOSE).
7. **No physics.** No physical branch, alpha value, action, source, carrier, density
   law, dynamics, or mass emergence enters or is constrained. `f2 != 0` via nondegenerate
   `F` is a recorded observation, not load-bearing.
