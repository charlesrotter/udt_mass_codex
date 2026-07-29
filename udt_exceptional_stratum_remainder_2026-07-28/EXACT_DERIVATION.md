# Exact derivation — exceptional-stratum remainder (gate d)

Date: 2026-07-28. Branch: `grok`. Contract: `PREREGISTRATION.md` in this package
(frozen targets T-d1..T-d4, falsifiers F-d1..F-d3, maximum conclusion — a fired
falsifier is first-class). Machine record: `derive_stratum_remainder.py` →
`DERIVATION_RESULT.json` / `DERIVATION_STDOUT.txt` (44 checks, all zero-residual
sympy passes, exit 0, deterministic). Check names in `[brackets]` refer to the JSON.

Parents (only imports permitted):

- **P-OWN** = `udt_higher_isometry_plane_ownership_audit_2026-07-28/EXACT_DERIVATION.md`
  (family §1, orbit Gram G3 §2, full response D3 §3, double-plane witness §6,
  two-free-lines/primitivity §7).
- **P-SEL** = `udt_alpha_plane_selector_theorem_2026-07-28/EXACT_DERIVATION.md`
  (certificate C, stratum derivation `{alpha = 0, S := b u + f² = c}`, conventions §0).
- **P-CAP** = `udt_cap_gluing_selector_2026-07-28/AUDIT_REPORT.md` (BANKED, commit
  `5291b63`) — **cited for SCOPE only, never assumed in a derivation here**: complete
  two-cap exceptional members have `c = 1` exactly; cap cycles `v∓ = (V ± Y)/2`.
- **G01/G02** = `CURRENT_SCIENTIFIC_PREMISES.tsv` rows G01 (founded `phi` = additive
  log depth of the reciprocal pair, DERIVED) and G02 (`phi ↦ diag(e^{−phi}, e^{+phi})`
  pair action, DERIVED), sourced to
  `udt_founded_phi_complete_coframe_extension_audit_2026-07-25/`.

## 0. Setting and premise ledger

Registered family (P-OWN §1, CHOSE-inherited): `g = −u(c_E dt + alpha A)² + u⁻¹A² + q_B`
on `R × S³`, `u = e^{−2 phi}`; `V` the registered vertical circle (`A(V) = 1`), `Y` the
second commuting compact Killing generator, `f = A(Y)`, `H = Y − f V`, `b = q_B(H,H) > 0`
on principal orbits; `X` transverse. This package works on the **exceptional stratum**
`{alpha = 0, S := b u + f² = c constant}` (DERIVED — P-SEL theorem, blind-verified).
Verified from the family first `[P0_G3_det_parent, P0_GKV_alpha0, P0_GKY_alpha0_stratum]`:

```text
G_KV = diag(−c_E² u, 1/u),      G_KY = diag(−c_E² u, c/u)      (alpha = 0, on-stratum)
```

| Premise | Tag |
|---|---|
| Family + registration | CHOSE — inherited P06/P07/P14-class |
| Stratum `{alpha = 0, S = c}` | DERIVED (P-SEL, blind-verified) |
| Clock generator = K (as a LINE) | DERIVED-inherited, CONDITIONAL (P-OWN §5 family-wide only) |
| Primitivity of V, Y (no free rescaling; sign only) | DERIVED-inherited (P-OWN §7) |
| `c = 1` forced for COMPLETE two-cap members | CITED (P-CAP, banked) — used for scope statements only |
| Cohomogeneity-one normal form; isometry-extension-to-completion | Category-A standard mathematics (soundness-checked in-run where expressible) |

No certificate leg is ADOPTED anywhere below (adoption = Charles). No physics.

## 1. T-d1 — area-value provenance: the exact chain and the grade

The candidate extended leg is: **"det G_P = −c_E² exactly"** (a VALUE, not merely
constancy). Its provenance decomposes into three links, each adjudicated separately.

**Link (a) — the u-cancellation is the G02 unit-determinant pair action: DERIVED.**
With `u = e^{−2 phi}` the clock leg of the plane carries weight `e^{−2 phi}` and the
ruler leg `e^{+2 phi}`; their product is 1, so `det G_KV = −c_E²` with identically zero
`phi`-derivative `[Td1_pair_unit_det_phi_independence]`. The CONSTANCY of the plane
area is exactly the founded pair's unit-determinant action realized in the family.
(This is the already-banked leg (i); nothing new is claimed for it.)

**Link (b) — the compact-generator normalization: DERIVED.** P-OWN §7's primitivity
fixes `V` and `Y` up to SIGN only (the lattice normalization is the torus group
structure itself — there is **no hidden 2π dial**: primitivity is scale-free). A sign
flip is the congruence `diag(1,−1)`, which leaves the Gram (and det) unchanged
`[Td1_sign_irrelevance]`. So the compact slot contributes NO free rescaling to the value.

**Link (c) — the clock normalization: NOT derived; registration residue.** The clock
result (P-OWN §5, conditional) fixes a LINE, not a vector: no derived structure pins
the scale of `K` (equivalently the placement of `c_E`; the noncompact factor has no
lattice to make a scale canonical). Under `K → lam K` BOTH plane dets scale by `lam²`
`[Td1_K_rescaling_scales_dets]`. The ABSOLUTE value `−c_E²` therefore rides the
registered clock constant.

**Grade (honest adjudication): DERIVED-WITHIN-REGISTRATION**, with a fully DERIVED
clock-free core:

```text
det G_KY / det G_KV = c = g(Y,Y) / g(V,V)          [Td1_ratio_clock_free, Td1_norm_ratio_form]
```

— invariant under `K`-rescaling, `c_E`-free (at `alpha = 0` the plane dets factor as
`g(K,K)·g(W,W)`, so the ratio is the free-circle NORM ratio: no clock enters at all),
and rescaling-free in the compact slot by link (b). The absolute-value form
"`det G_P = −c_E²`" is legitimate ONLY within the registered presentation: it is not a
naked CHOSE (no NEW dial beyond the inherited registration; `c_E` is fixed per member
by the registration this whole program conditions on), but it is **the first
certificate leg that load-bears on `c_E`** — the banked certificate C never did (P-SEL
§8: `c_E` cancels from all three legs). This must travel with any use of the leg.

**Presentation-relativity of the label (derived, sharpens the honesty).** The same
metric can be re-presented with `Y` as the vertical circle; the relabel map, computed
purely from Gram data `[Td1_relabel_map]`, is

```text
u → u/c,   c_E² → c·c_E²,   f → f/c,   b → b/c,   S → 1/c ,
```

so the labeled value of `c` is presentation-relative (`c ↔ 1/c`) while the UNORDERED
det pair `{−c_E², −c_E² c}` and the statement `c ≠ 1` are presentation-free. At `c = 1`
the relabel fixes every presentation scalar `[Td1_relabel_c1_fixed_point]` — the two
presentations of a `c = 1` member carry IDENTICAL profile data `(u, f, b, c_E)`.

**Consequence (verified).** For `c ≠ 1` stratum members the extended certificate is
not silent: `span(K,V)` has `det = −c_E²`, `span(K,Y)` has `det = −c_E²·c`
`[Td1_det_GKV_value, Td1_det_GKY_value]` — the planes are objectively DISTINGUISHED by
the derived clock-free core (and, by §4's necessity, even isometrically inequivalent);
NAMING which one is the founded plane uses the registered `c_E` (within-registration).
**Scope (P-CAP, cited):** complete two-cap members have `c = 1` exactly, so the
`c ≠ 1` selectable class contains only NON-COMPLETE / principal-orbit-only members.
Auxiliary exact fact: the cap cycles satisfy `g(v−, v+) = (1 − c)/(4u)` — they are
`g`-orthogonal exactly at `c = 1` `[Td1_cap_cycle_inner_product]`.

## 2. T-d2 — all-orders identity at c = 1 (theorem; F-d1 does not fire)

**What "identical" means, precisely.** The basis correspondence is
`(K, V) ↔ (K, Y)`: `K` is shared (same clock vector on both sides — any common choice
on the clock line; the statement is `K`-scale covariant), and `V ↦ Y`, each the
primitive generator of its free-circle class (P-OWN §7), defined up to a sign that
leaves the Gram invariant. The claim is entrywise equality of the restricted Gram
matrices **under this correspondence, at every principal point, together with all
transverse jets**.

**Theorem.** At `alpha = 0`, `c = 1` (where `b = (1 − f²)/u` is forced — the identity
`S = 1 ⇔ b = (1−f²)/u` is checked `[Td2_b_forced_at_c1]`):

```text
G_KY = diag(−c_E² u, f²/u + b) = diag(−c_E² u, 1/u) = G_KV
```

as matrix FUNCTIONS on the region — the same function of `u` alone. Hence every
`X`-jet of every entry agrees identically (verified symbolically with arbitrary
profile functions `u(s), f(s)` through order 5 `[Td2_gram_and_jets_identical]`; the
equality of the undifferenced entries is an identity in `(u, f)`, so ALL orders agree
— the order-5 machine check is a soundness control, not the proof), and the restricted
responses coincide: `D_KV = D_KY` identically `[Td2_response_identical]`.

**Corollary.** Any certificate whose inputs are the plane-restricted Gram and its
`X`-jets — of ANY finite order, including the banked C — evaluates identically on the
two planes at `c = 1`. **No plane-restricted certificate at any order distinguishes.**

**Hidden-asymmetry hunt in the correspondence** (all dissolved): (i) `K` shared —
no asymmetry; (ii) both compact generators primitive — no scale asymmetry (link (b));
(iii) signs — Gram-invariant; (iv) both off-diagonal entries vanish at `alpha = 0`
(`g(K,V) = g(K,Y) = 0` `[Td2_no_offdiagonal_asymmetry]`) — no cross-term asymmetry;
(v) the restricted certificate consumes nothing beyond the Gram jet, by its definition
(P-SEL §0). **F-d1 does NOT fire.**

## 3. T-d3 — ambient inventory at c = 1 (tagged; nothing promoted)

Relabel map (§1) = the effect of exchanging which line is "the fiber"; a quantity
distinguishes the planes AS UNORDERED OBJECTS only if it is NOT symmetric under it.
Exact inventory (general `c` first, then `c = 1`); all Gram-level formulas
machine-verified:

| Ambient quantity (exact) | Relabel behavior | Certificate-grade? | Discriminates (unordered) at c = 1? |
|---|---|---|---|
| `g(V,Y) = f/u` `[Td3_gVY_value]` | invariant pair scalar | yes | **No** (symmetric) |
| norm ratio `g(Y,Y)/g(V,V) = c` `[Td3_gYY_stratum]` | `c → 1/c` | yes | **No** (= 1); at `c ≠ 1`: YES (T-d1 core) |
| complement norms `g(H,H) = b` vs `g(H̃,H̃) = b/c` `[Td3_H_norm, Td3_Htilde_norm]` | swap | yes | **No** (equal at c = 1) |
| `g(H,H̃) = −f b/c` `[Td3_H_Htilde_pairing]` | invariant pair scalar | yes | **No** |
| mixed D3 entries: `(D3)_{V→Y} = c f′/(c−f²)`, `(D3)_{Y→V} = f′/(c−f²)` `[Td3_D3_mixing_entries]`; ratio `= c` `[Td3_D3_mixing_ratio_is_c]`, difference `= (c−1)f′/(c−f²)` `[Td3_D3_mixing_difference]` | swap (ratio `c → 1/c`) | yes | **No** (entries EQUAL at c = 1) |
| orientation pairing (Hopf vs anti-Hopf Euler sign; sign of `vol(K,X,V,Y)`; `F`-holonomy sign) | sign flip | **NO** — requires a CHOSE orientation; a metric does not orient; not a function of `(g, K, line, X)` | only relative to a chosen orientation |
| cap data `V = v− + v+` vs `Y = v− − v+` (complete members) | relative cap-cycle sign flip | **NO** — each cap cycle canonical only up to sign; the relative sign is orientation-class data | No |

**Master fact (proved, stronger than the item-by-item table).** Let `P` be the linear
swap (`K` fixed, `V ↔ Y`). At `c = 1` the ENTIRE ambient orbit Gram is `P`-invariant —
`Pᵀ G3 P = G3` identically in the free profiles, and likewise every `X`-jet of `G3`
and the full response `D3` `[Td3_P_invariance_G3_c1, Td3_P_invariance_G3_jets_c1,
Td3_P_invariance_D3_c1]`. For general `c` the `P`-defect of `G3` is exactly
`diag(0, (c−1)/u, (1−c)/u)` — supported ONLY on the norm gap `[Td3_P_defect_is_norm_gap]`:
the norm ratio is not just one discriminator among many, it is the ONLY one at the
level of orbit Gram data. And by §4 the swap is realized by an actual **isometry** at
`c = 1`, so no metric-native quantity of ANY construction (not only those listed)
distinguishes the planes there. Per the preregistration, **nothing is promoted to a
selector**; at `c = 1` there is nothing to promote — the inventory is CLOSED EMPTY of
metric-native discriminators; the only differing data are orientation-relative signs,
which fail certificate-grade.

## 4. T-d4 — exchange-isometry characterization (classification)

**Theorem.** Within the registered family, on the stratum `{alpha = 0, S = c}`:

> **A plane-swapping isometry exists ⇔ c = 1.**

**(A) Necessity (AMENDED per blind verifier, 2026-07-28 — see CORRECTION_LAYER.md).**
Let `Φ` be an isometry with `Φ_*(span(K,V)) = span(K,Y)` and `Φ_*(span(K,Y)) = span(K,V)`
(the two-sided plane-swap reading; see the scope note below). The step "`Φ_*` maps the
Killing lattice to itself" needs, and has, a LEMMA the original text left unstated
(verifier-derived, machine-checked 4/4 — preserved as `VERIFIER_LEMMA_B1.py`):

> **Lemma (constant-combination).** Any Killing field pointwise tangent to `span(K,Y)`
> on an `alpha = 0` stratum member is a CONSTANT combination `aK + bY`. (The Killing
> component equations force all derivatives of `a, b` to zero pointwise, including the
> `f = ±c` corner cases; constant-depth members, which escape the separation step, are
> closed by torus single-valuedness.)

With the lemma: the conjugated generator of the V-circle is a Killing field tangent to
the image plane, hence `aK + bY` with constants; compactness (the `t`-flow is unbounded
on `R × S3`) forces `a = 0`, and primitivity forces `b = ±1` — so `Φ_*V = ±Y` with no
assumption on the ambient isometry algebra. The two-free-lines FREENESS theorem
(P-OWN §7 — freeness, not mere lattice injectivity: in the cap-cycle basis
`εV + nY = (ε+n)v− + (ε−n)v+` is free iff `|ε+n| = |ε−n| = 1`, forcing `n = 0`) gives
`Φ_*Y = ±V` for the two-sided swap. Isometry matching of the circle norms across the
induced orbit-space map `σ`:

```text
c/u(σ(s)) = 1/u(s)   and   1/u(σ(s)) = c/u(s)
⇒  u∘σ = u  and  c² = 1  ⇒  c = 1        [Td4_necessity_algebra, Td4_necessity_solve]
```

(Contrapositive and its exact scope: at `c ≠ 1` no TWO-SIDED plane-swapping isometry
exists, and the pointwise norm ratio `c` distinguishes the planes absolutely —
selection at `c ≠ 1` rides that pointwise ratio and is untouched by the following
corner. SCOPE NOTE (verifier point 3): the stronger ONE-DIRECTIONAL claim ("no isometry
maps plane 1 onto plane 2 at all") is proven whenever `sup u < ∞` or `inf u > 0`
(via `u∘Φ = c·u`); the unproven corner is principal-orbit-only members with strictly
larger isometry algebra AND depth range all of `(0, ∞)`. No conclusion in this package
rides that corner.)

**(B) Sufficiency — constructive, for EVERY c = 1 profile; no symmetry needed.** On
the principal region take adapted coordinates `(t, s, φ−, φ+)`: `v∓ = (V ± Y)/2` the
unimodular cap-cycle lattice basis (P-OWN §7 / P-CAP), `s` the orbit-orthogonal
transversal (Category-A cohomogeneity-one normal form; at `alpha = 0` there are no
`dt` cross terms — family identities `g(K,V) = g(K,Y) = 0`, `g(K, spatial) = 0`). The
normal form reproduces the family `G3` exactly `[Td4_normal_form_consistency]`. The
map

```text
J : (t, s, φ−, φ+) ↦ (t, s, φ−, −φ+)     (the lattice map V ↔ Y, K fixed)
```

is well-defined on the torus (`diag(1,−1) ∈ GL(2,Z)` in the cap-cycle basis) and
satisfies `Jᵀ g J = g` **identically at `c = 1` for arbitrary profiles
`u(s), f(s), n(s)`** `[Td4_sufficiency_congruence_c1]`; the ONLY congruence defect for
general `c` is `−2 g(v−,v+) = −(1−c)/(2u)` `[Td4_congruence_defect_generic]` — the
entire obstruction is the cap-cycle inner product, zero iff `c = 1`. `J` swaps the
planes (`J V = Y`, `J Y = V`, `J K = K`) and has `det J = −1`
`[Td4_J_swaps_planes]`. It fixes both cap-closing cycle lines (`J v− = v−`,
`J v+ = −v+` `[Td4_J_cap_cycles]`) — **cap-fixing** — and extends to the metric
completion of complete members (an isometry of the dense principal region of the
spatial Riemannian factor extends to its completion; Category-A standard; the caps are
the completion points, P-CAP).

**(C) Orientation class (exact).** Among the four lattice swaps `V → s₁Y, Y → s₂V`,
Gram invariance at `c = 1` holds exactly for `s₁s₂ = +1`, i.e. `det = −1`
`[Td4_swap_orientation_class]`: wherever `f ≠ 0`, **every plane-swapping isometry is
orientation-reversing** — coherent with §3: the orientation pairing is precisely the
datum a swap must (and does) reverse.

**(D) Witness and asymmetric control.** The P-OWN §6 witness is on-stratum (`S = 1`
exactly) and even under `η → π/2 − η` `[Td4_witness_on_stratum,
Td4_witness_even_profile]`; the general construction covers it — **evenness is
sufficient-not-necessary**. The preregistered NON-symmetric `c = 1` control
`u = 1 + (3/10)sin²2η + (1/10)sin²2η·cosη`, `f = cos2η`, `b = (1−f²)/u`: on-stratum
exactly; genuinely asymmetric (`u(π/2−η) − u(η) ≈ −0.0275, −0.0200` at `η = π/6, π/5`
— the reflection is NOT an isometry of this member) `[Td4_control_on_stratum,
Td4_control_asymmetric]`; its plane-restricted data and all jets are identical (T-d2
instantiated) `[Td4_control_plane_data_identical]`; its ambient candidates do NOT
differ (`g(V,V) = g(Y,Y)`, equal D3 mixing entries, `g(v−,v+) = 0`, while the pair
scalar `g(V,Y) = f/u ≠ 0`) `[Td4_control_ambient_symmetric]`; and the swap isometry
exists for it despite the asymmetry `[Td4_control_swap_isometry]`.

**(E) Cap-swapping subclass and the anticipated curvature obstructions.** Isometries
that additionally exchange the two caps require `u∘σ = u` with `σ` the orbit-interval
reflection — i.e. reflection-symmetric profiles; the control excludes them while still
admitting the cap-fixing swap. The preregistration's anticipated
curvature/Ricci-invariant obstructions for asymmetric profiles apply exactly to this
orbit-space-moving subclass and DISSOLVE for the main question: a `σ = id` swap always
exists at `c = 1`, and all `T²`-invariant scalars match trivially at the same point.

**OPEN remainder (recorded, not forced):** the structure of the FULL swap-isometry
group (beyond existence) is not classified; members whose isometry algebra strictly
exceeds the registered `R × T²` are covered by (A) (topology-only) and (B)
(constructive) for the existence question, but their extra isometries are not
classified (P-OWN §8 territory).

## 5. Stratum sub-classification (assembled; within the preregistered ceiling)

- **`c ≠ 1`** (necessarily NON-complete / principal-orbit-only — P-CAP, cited): the
  planes are isometrically INEQUIVALENT (§4A) and distinguished by the clock-free
  norm/det ratio (§1, DERIVED); naming `span(K,V)` via the VALUE leg is
  DERIVED-WITHIN-REGISTRATION. **Area-value-selectable.**
- **`c = 1`** (all complete members, and any principal-only member with `S = 1`):
  a plane-swapping isometry exists for EVERY profile (§4B) — **selection is PROVABLY
  IMPOSSIBLE**, not merely certificate-silent.
- **The "certificate-silent-but-possibly-selectable" middle class is EMPTY on the
  stratum.** The preregistration's category (iii) closes: its inventory (§3) contains
  no metric-native discriminator, and the swap isometry forecloses every future one at
  `c = 1`. The parent theorem's LIMIT #5 (silence vs impossibility OPEN outside the
  witness's symmetric points) is now resolved: silent = impossible, on the whole
  `c = 1` stratum.

No new certificate leg is ADOPTED; the extended value/ratio leg is RECORDED for
Charles's adjudication.

## 6. Falsifier review

- **F-d1** (a jet distinguishes at `c = 1`): **does not fire** — §2 proves all-orders
  identity; the asymmetric control confirms it pointwise.
- **F-d2** (T-d1 provenance fails; leg CHOSE and unusable): **does not fire in the
  frozen sense** — the leg has a DERIVED clock-free core (the ratio/norm comparison)
  that breaks `c ≠ 1` silence unconditionally; honesty outcome: the frozen
  ABSOLUTE-value form is downgraded to DERIVED-WITHIN-REGISTRATION (`c_E`
  load-bearing, first leg to do so; presentation-relativity of the label `c ↔ 1/c`
  recorded). The downgrade is stated wherever the leg is used.
- **F-d3** (algebra error, independent implementation): **not fired at this stage** —
  44/44 zero-residual gates, deterministic rerun byte-identical; the independent
  adversarial implementation belongs to the blind verifier pass before banking.

## 7. LIMITS (honest scope)

1. **The family itself is CHOSE** (registered P06/P07/P14-class); every conclusion is
   scoped to it. Nothing says the family is preferred.
2. **Clock = K is CONDITIONAL** (P-OWN §5 family-wide only); T-d1's grade additionally
   flags that the VALUE leg load-bears on the registered clock scale `c_E`, which no
   parent derives.
3. **No leg is ADOPTED** — the extended value/ratio leg and the sub-classification are
   RECORDED; adoption is Charles's call. No canonization.
4. **Principal orbits** for all response/jet statements; cap statements are limit/
   completion statements via P-CAP (cited) and the Category-A extension argument.
5. **Category-A borrowings** (cohomogeneity-one normal form with orbit-orthogonal
   transversal; unimodular lattice coordinates; isometry-extension-to-completion) are
   solving technique, machine-checked where expressible (`[Td4_normal_form_consistency]`
   ties the normal form back to the family `G3` exactly); they import no physics.
6. **T-d4's OPEN remainder** is §4E's group-structure question only; existence ⇔ `c = 1`
   is closed within the stated scope.
7. **No physics.** No branch, no alpha value, no action, source, carrier, density law,
   dynamics, or mass emergence. Constant-depth members degenerate the certificate as
   in P-SEL LIMIT #6; the swap results hold there trivially.
