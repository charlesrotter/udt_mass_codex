# Exact derivation — fixed-metric reciprocal-plane selector (constant-alpha family)

Date: 2026-07-28. Branch: `review/external-perspective-2026-07-28`. Contract:
`PREREGISTRATION.md` in this package (targets T1–T6, falsifiers F-A..F-D, maximum
conclusion). Machine record: `derive_alpha_plane_selector.py` →
`DERIVATION_RESULT.json` / `DERIVATION_STDOUT.txt` (37 checks, all zero-residual
sympy passes, exit 0). Check names below in `[brackets]` refer to that JSON.

Parents (only imports permitted):

- P-OWN = `udt_higher_isometry_plane_ownership_audit_2026-07-28/EXACT_DERIVATION.md`
  (family §1, Gram G3 §2, response and Cartan identity §3, every-plane determinant §4,
  witness §6, two-free-lines theorem §7).
- P-KV = `udt_killing_plane_strata_transition_audit_2026-07-28/EXACT_DERIVATION.md`
  (the (K,V) response eigenstructure §3; constant-depth exceptional stratum §5).

## 0. Setting and premise ledger (inherited; tags restated)

`g = -u(c_E dt + alpha A)^2 + u^{-1} A^2 + q_B` on `R x S3`, `u = e^{-2 phi} > 0`;
`A` the registered Hopf connection with curvature `F = dA` nondegenerate on the base;
`K` the stationary generator (`A(K) = 0`, `q_B(K,.) = 0`); `V` the registered vertical
circle (`A(V) = 1`, `q_B(V,.) = 0`); `Y` the second commuting compact Killing generator;
`f = A(Y)`, `H = Y - f V`, `b = q_B(H,H) > 0` on principal orbits; `X` any direction
transverse to the three-dimensional isometry orbits; `chi = X(phi)`, `X(u) = -2 chi u`,
`X(f) = df`, `X(b) = db`; `alpha`, `c_E` constants (`X` annihilates them).

| Premise | Tag |
|---|---|
| Family + registration (block-screen, stationary, descended, constant alpha, Hopf bundle) | CHOSE — inherited; every conclusion scoped to it |
| Candidate ruler set = the two free circle lines {V, Y} | DERIVED — P-OWN §7 (topology supplies exactly two) |
| Clock generator = K | DERIVED-inherited, CONDITIONAL — P-OWN §5 is family-wide only; fixed-profile clock cancellations remain OPEN there; this theorem conditions on clock = K throughout |
| Certificate C(P), P = span(K,W): (i) `|det G_P|` constant on the connected principal-orbit region; (ii) K an eigenvector of `D_P = G_P^{-1} X(G_P)` at every point; (iii) eigenvalue pair exactly `(-2 chi, +2 chi)` | DERIVED-inherited from P-KV §3; CERTIFICATE-RELATIVE (R09 caveat travels; see §8) |
| `df` not identically 0 for the second line | DERIVED in-run — §5 below (T4), hypotheses (H1)–(H5) stated exactly |
| Principal orbits only (`b > 0`); caps excluded | THEORY — P-OWN §1: `b` vanishes at caps, the response is undefined there; cap gluing OPEN, not claimed |

Conventions (frozen before computing, per the T2 caution): a Killing vector
`Z = z0 K + z1 W` is the column `(z0, z1)^T` in the ordered basis `(K, W)`; `G_P` is the
restricted Gram matrix in that basis; `D_P = G_P^{-1} X(G_P)` acts on columns from the
left. `K = (1,0)^T`, so `D_P(K)` is column 0 of `D_P` and **K is an eigenvector of `D_P`
iff the entry `D_P[1,0]` (row 1 = W-component of the image of K) vanishes**, the
eigenvalue then being `D_P[0,0]`.

## 1. T1 — the registered plane passes universally

With `Q = u^{-1} - alpha^2 u`,

```text
G_KV = [ -c_E^2 u        -alpha c_E u ]
       [ -alpha c_E u     Q           ],       det G_KV = -c_E^2   exactly.
```

`[T1_det_GKV]`. Exact differentiation and inversion give

```text
D_KV = [ -2 chi     -4 alpha chi / c_E ]
       [   0              +2 chi       ],
```

upper-triangular: `K = (1,0)^T` is an eigenvector with eigenvalue `-2 chi`, the trace is
`0`, the second eigenvalue is `+2 chi`, all for symbolic `alpha`
`[T1_K_eigenvector, T1_K_rate, T1_trace_zero, T1_second_rate]`; the off-diagonal entry
reproduces P-KV §3 verbatim `[T1_offdiag_parent_D1]`. Since `det G_KV` is the constant
`-c_E^2`, **span(K,V) satisfies all three certificate legs for every member of the family
and every constant `alpha`** — pointwise polynomial identities in the free symbols, no
genericity needed.

## 2. T2 — second plane, K-eigenline leg

```text
G_KY = [ -c_E^2 u          -alpha c_E u f  ]
       [ -alpha c_E u f     Q f^2 + b      ],     det G_KY = -c_E^2 (b u + f^2)
```

`[T2_det_GKY]`. Write `S = b u + f^2` (so `S > 0` on principal orbits, since `u, b > 0`
`[T2_denominator_positive]`). Exact computation of `D_KY = G_KY^{-1} X(G_KY)` gives

```text
(D_KY)[1,0] = -alpha c_E df u^2 / (b u + f^2)
```

`[T2_off_entry_formula, T2_off_cleared]` — the exact off-eigenline component frozen in
the preregistration, in the stated convention. Because `u > 0`, `S > 0`, `c_E != 0`:

> **K is an eigenvector of `D_KY` at a point iff `alpha * df = 0` there.**

(For comparison, the FULL three-direction response of P-OWN §3 has Y-component of
`D3(K)` equal to `-alpha c_E df u / b` — a different denominator: the restricted-plane
response is not the projection of the full response. This is P-OWN's "two different
metric operations" distinction, and is why the present certificate is certificate-relative;
see §8.)

## 3. T3 — second plane, area leg

```text
X(b u + f^2) = db u - 2 chi u b + 2 f df          [T3_XS_formula]
tr D_KY      = X(b u + f^2) / (b u + f^2)
             = X(log|det G_KY|)                    [T3_trace_is_dlogdet, T3_jacobi]
X(det G_KY)  = -c_E^2 X(b u + f^2)                 [T3_Xdet]
```

Hence on the connected principal-orbit region:

> **`|det G_KY|` is constant iff `X(b u + f^2) = 0` identically.**

## 4. The `alpha = 0` sub-case (both legs collapse onto ONE condition)

At `alpha = 0`, `G_KY = diag(-c_E^2 u, f^2/u + b)` and `D_KY` is exactly diagonal
`[T5a0_diagonal]`: the K-eigenline leg passes trivially with eigenvalue `-2 chi`
`[T5a0_K_rate]`. The second eigenvalue is

```text
lambda_2 = X( ln( f^2/u + b ) )                    [T5a0_second_rate_log]
```

and, since `f^2/u + b = (b u + f^2)/u` exactly `[T5a0_E_identity]`,

```text
lambda_2 = X( ln(b u + f^2) ) + 2 chi              [T5a0_rate_decomposition]
lambda_2 - 2 chi = X(b u + f^2) / (b u + f^2)      [T5a0_founded_iff]
```

> **Coincidence, noted explicitly:** at `alpha = 0` the rate leg (`lambda_2 = +2 chi`)
> and the area leg (`|det|` constant) are governed by the SAME exceptional condition
> `X(b u + f^2) = 0`. The certificate's two nontrivial legs do not cut two strata; they
> cut one.

## 5. T4 — the Cartan argument: `df` cannot vanish identically (prose deliverable)

**Exact hypotheses.**

- (H1) The family presentation of §0 (CHOSE-inherited): `A` a one-form on `S3` with
  `A(K) = 0`, `A(V) = 1`, `V` vertical, `q_B` basic and positive on horizontal vectors.
- (H2) `Y` is a Killing field of `g`, tangent to `S3` (so `Y(t) = 0`), commuting with
  `K` and `V` — P-OWN §1 ("arbitrary commuting compact Killing generator").
- (H3) `F = dA` is nondegenerate on the Hopf base — P-OWN §3 ("On the nontrivial Hopf
  base, `F` is a nondegenerate area form") and the preregistration's setting line.
- (H4) Principal orbit: `b = q_B(H,H) > 0`, `H = Y - f V` — P-OWN §1. Equivalently the
  base projection `H^` of `Y` is nonzero there. (H4 encodes "Y not proportional to V"
  pointwise: at a principal point `Y` and `V` span a 2-plane.)
- (H5) `X` is transverse to the three-dimensional isometry orbits (P-KV §3 / P-OWN §3);
  the family is cohomogeneity-one, so the base of the Hopf bundle is two-dimensional
  and the transverse direction is one-dimensional.

**Step 1 — `Y(u) = 0` (derived).** From (H1), `g(K,K) = -c_E^2 u`. `Y` Killing with
`[Y,K] = 0` gives `Y(g(K,K)) = 0`, hence `Y(u) = 0`.

**Step 2 — `L_Y A = 0` (derived, both alpha cases).** From (H1),
`g(K,.) = -u c_E (c_E dt + alpha A)` as a one-form. `Y` Killing and `[Y,K] = 0` give
`L_Y( g(K,.) ) = 0`; with `L_Y dt = d(Y(t)) = 0` (H2) and Step 1, this yields
`alpha c_E u L_Y A = 0`, i.e. **`L_Y A = 0` whenever `alpha != 0`.** For `alpha = 0`,
use the V-row instead: `g(V,.) = u^{-1} A` (H1, `alpha = 0`), and `L_Y(g(V,.)) = 0`
with Step 1 gives `u^{-1} L_Y A = 0`, i.e. `L_Y A = 0`. (For general constant `alpha`
the V-row gives `(u^{-1} - alpha^2 u) L_Y A = 0`, conclusive wherever `Q != 0`; the two
rows together cover every constant-`alpha` member everywhere.) So bundle preservation is
NOT an extra pin here — it is forced by the registered isometries. This grounds P-OWN
§3's "bundle-preserving extra circle" hypothesis inside the family.

**Step 3 — Cartan (P-OWN §3, verbatim).** `0 = L_Y A = i_Y dA + d(i_Y A) = i_Y F + d f`,
hence the one-form identity `d f = -i_Y F`.

**Step 4 — nonvanishing.** `F` is basic, so `i_V F = 0` and `i_Y F = i_H F = F(H^, .)`
on the base. By (H4) `H^ != 0` at every principal point. The base is two-dimensional
(H5); the projection `X^` of `X` has a component transverse to `H^` — otherwise
`X` would lie in `span(K, V, H) =` the orbit tangent, contradicting (H5). By (H3),
`F` is a nondegenerate area form, so `d f(X) = -F(H^, X^) != 0`. Finally `f = A(Y)` is
orbit-invariant (`K(f) = 0` as `f` is time-independent; `V(f) = (L_V A)(Y) + A([V,Y]) = 0`
by the registered `V`-invariance of `A`; `Y(f) = (L_Y A)(Y) = 0` by Step 2), so `d f` is
supported on the transverse direction and `df = X(f) != 0`.

**Conclusion (T4, banked as frozen):** under (H1)–(H5), `df` cannot vanish identically
on the principal-orbit region; the set `{df != 0}` is a nonempty open set.
**Observed strengthening (same hypotheses, recorded but not load-bearing beyond T4):**
the argument is pointwise — `df != 0` at EVERY principal point. Witness control agrees:
there `df = -2 sin(2 eta)` `[W_df_convention]` vanishes only at `eta = 0, pi/2`, which
are exactly the caps (`b = 0`), outside the principal region.

**Grounding audit:** every hypothesis is grounded in the parents or the registration;
none had to be pinned ad hoc, so the ledger row "TO BE DERIVED in-run" closes DERIVED
and no gap is reported.

## 6. T5 — the selector classification theorem

**Theorem (fixed metric; principal orbits; clock = K; certificate C; family of §0).**
Fix one metric of the registered family and work on its connected principal-orbit
region. Then:

- **(a)** span(K,V) satisfies C — identically, for every member and every constant
  `alpha` (§1; pointwise identities).
- **(b) `alpha != 0`:** span(K,Y) violates leg (ii) at every point where `df != 0` (§2);
  by T4 (§5) that set is nonempty and open (indeed, all principal points under
  (H1)–(H5)). A single violating point defeats C, which is a region-wide certificate.
  **Hence C selects span(K,V) uniquely.**
- **(c) `alpha = 0`:** leg (ii) holds identically for span(K,Y) (§4). Legs (i) and
  (iii) each hold iff `X(b u + f^2) = 0` identically (§3, §4 — the same condition).
  **Hence: if `b u + f^2` is nonconstant, C selects span(K,V) uniquely; if
  `b u + f^2` is constant, BOTH planes satisfy C and the certificate is silent.**
- **(d) Exceptional stratum, exactly:** `{ alpha = 0 and b u + f^2 constant }`
  (equivalently `alpha*df == 0` identically and `b u + f^2` constant: by T4 `df` is not
  identically zero, so `alpha*df == 0` identically forces `alpha = 0`).

Quantifier discipline: leg (i) is a region statement (constancy on the connected
principal region; jet criterion `X(det) = 0` at every point); legs (ii)–(iii) are
required at every point; failure claims in (b), (c) are pointwise and therefore also
region failures. Points with `chi = 0` (depth extrema) degenerate the rate NORMALIZATION
but violate nothing: all identities above are polynomial/rational identities in the jet
symbols, and the global-eigenline extension of P-KV §3 applies. Machine assembly of the
two branches: `[T5_branch_alpha_nonzero, T5_branch_alpha_zero]`.

**Witness control (frozen in T5).** The P-OWN §6 witness (`alpha = 0`,
`f = cos 2 eta`, `u = 1 + eps (1 - f^2)`, `b = (1 - f^2)/u`, `X = d/d eta`) satisfies

```text
b u + f^2 = 1   exactly                      [W_on_stratum]
```

— it lies ON the exceptional stratum — and BOTH planes pass the full three-leg
certificate there, by direct `d/d eta` computation independent of the jet formalism
`[W_KV_full_certificate, W_KY_full_certificate]`, with the jet-formalism matrices
agreeing exactly `[W_formalism_consistency]`. At the witness's exchange-symmetric points
an isometry swaps the two lines (P-OWN §6), so selection is PROVABLY impossible there.
Between "certificate silent" and "provably impossible" on the REST of the stratum:
OPEN, not claimed.

**Stratum cross-check (parent §6 identity, corrected generalization).** On the stratum
`X(b u + f^2) = 0` with symbolic `alpha`:

```text
det D_KY + 4 chi^2 = alpha^2 u^2 df^2 / (b u + f^2)     [parent6_identity_general_stratum]
```

which reduces to P-OWN §6's stated `det D_KY + 4 chi^2 = alpha^2 u^2 df^2` exactly on
its witness where `b u + f^2 = 1` `[parent6_identity_on_witness]`. Honesty note: a first
version of this AUXILIARY control asserted the parent's witness form on the whole
stratum and failed; hand re-derivation produced the `1/(b u + f^2)` factor above and
both corrected statements pass. The failure was in this package's own mis-generalized
auxiliary target — not in any preregistered T1–T6 formula and not in the parent — so
falsifier F-C does not fire; the incident is recorded in the script header comment and
here. Physical content of the identity, unchanged: for `alpha*df != 0` the rates leave
the founded pair even where the area stays constant — turning on twist breaks the
degeneracy of the exceptional stratum, consistent with branch (b).

## 7. T6 — record only: constant-area leg for a general candidate line

For `W = m V + n Y` (`m, n` constants), exactly

```text
det G(K, W) = -c_E^2 [ (m + n f)^2 + n^2 b u ]              [T6_det_formula]
X(det G(K, W)) = -c_E^2 [ 2 m n df + n^2 X(b u + f^2) ]     [T6_Xdet_record]
```

(the first agrees with P-OWN §4's `det G(T,Z)` at `T = K` `[T6_parent4_crosscheck]`;
`alpha` drops out of both). Recorded vanishing structure of `X(det)`: it vanishes iff
`n = 0` (the registered plane, always) or `n != 0` with `2 m df + n X(b u + f^2) = 0`
pointwise; on the `X(b u + f^2) = 0` stratum the condition is `m n df = 0`. **No claim
is made beyond this record** (in particular no eigenline/rate analysis for general `W`).

## 8. Falsifier review and certificate well-definedness (F-D)

- **F-A** (a fixed metric with `alpha*df != 0` somewhere on which both planes pass):
  does not fire — §2 proves span(K,Y) fails leg (ii) at any such point.
- **F-B** (a generic `alpha = 0` metric on which span(K,Y) passes, or an
  exceptional-stratum metric on which C is not silent): does not fire — §3–§4 give the
  exact iff; the witness confirms silence on the stratum.
- **F-C** (algebra error in T1–T3): did not fire — 37/37 zero-residual checks; the one
  auxiliary-control mis-statement (outside T1–T6) is documented in §6 and was corrected
  against a hand re-derivation, not massaged.
- **F-D** (presentation dependence): does not fire. The certificate depends only on
  `(g, K, the line W, X)`: under an in-plane constant basis change fixing `K`
  (`W -> sigma K + lam W`, `lam != 0`), `det` scales by the constant `lam^2` (constancy
  invariant) and `D -> S^{-1} D S` (eigenvalues invariant; `D'[1,0] = D[1,0]/lam`, so
  the K-eigenline condition is invariant) `[FD_basis_det, FD_basis_similarity,
  FD_offentry_scaling]`. Under `X -> c X` all of `(chi, df, db)` scale by `c` and
  `D -> c D`, so legs (ii)–(iii) are X-normalization covariant `[FD_X_rescaling]`;
  adding orbit components to `X` changes nothing because every Gram entry is
  orbit-invariant. `c_E` enters only through `c_E^2` in dets and cancels from `D`'s
  eigenstructure conditions.

Numeric spot checks: 7 random admissible jet points (4 with `alpha*df != 0`: T2 formula
confirmed to `<1e-12`, K-eigenline of span(K,Y) numerically broken; 3 with `alpha = 0`,
`X(b u + f^2) != 0`: K-eigenline holds, area nonconstant, second rate off `+2 chi`) —
all symbolic verdicts confirmed `[NUMERIC_spot_checks]`, seed 20260728 in the script.

## 9. Conclusion (within the preregistered ceiling)

Inside the registered constant-alpha family, on principal orbits, CONDITIONAL on
clock = K, and relative to the inherited founded-pair certificate C:

> **The fixed-metric two-candidate selection question is CLOSED.** C selects the
> registered plane span(K,V) uniquely for every fixed metric with `alpha != 0`, and for
> every `alpha = 0` metric with `b u + f^2` nonconstant. The exceptional stratum is
> exactly `{ alpha = 0, b u + f^2 constant }`, on which both planes satisfy C and the
> certificate is silent; the parent's double-plane witness lies on it, and at its
> exchange-symmetric points selection is provably impossible.

This closes P-OWN §4/§9's `GENERIC_FIXED_METRIC_SELECTION_OPEN` for the
topology-supplied two-candidate set `{V, Y}`, in the certificate-relative sense, and
replaces "generic" by an exact characterization.

## 10. LIMITS (honest scope)

1. **The family itself is CHOSE** (registered block-screen stationary descended
   constant-alpha Hopf control). Nothing here says the family is preferred.
2. **Clock = K is CONDITIONAL.** The parent clock scan is family-robustness only
   (P-OWN §5); fixed-profile clock cancellations are OPEN there. If a fixed profile
   admitted another founded clock line, the selector question would have to be re-posed.
3. **Certificate-relative (R09).** C is the restricted-plane scan (P-OWN §3's operation
   2). The full three-direction response D3 does not keep span(K,V) invariant where
   `df != 0` (P-OWN §3), so a full-response-invariance criterion DISAGREES with C
   exactly where C's selection is strongest. This theorem ranks planes by C, not by
   full-response invariance, and does not adjudicate between the two criteria.
4. **Principal orbits only; caps excluded.** `D` is undefined where `b -> 0`; cap
   gluing/regularity is OPEN and nothing here extends through caps.
5. **Exceptional stratum remainder OPEN.** On `{alpha = 0, b u + f^2 const}` the
   certificate is silent everywhere; impossibility of ANY metric selection is proven
   only at the witness's exchange-symmetric points (parent isometry). Whether the rest
   of the stratum admits some other selector is OPEN and not claimed.
6. **Constant-depth members** (`phi` constant, `chi == 0`): `X(G_KV) = 0`, the
   certificate degenerates (P-KV §5's stratum) and the selector has no content; the
   algebraic identities above still hold trivially.
7. **T4's pointwise strengthening** (`df != 0` at every principal point) is an
   observation under (H1)–(H5); the banked claim is the frozen "not identically zero".
8. **T6 is a record**, not a theorem about general candidate planes.
9. **No physics.** No physical branch, alpha value, action, source, carrier, density
   law, dynamics, or mass emergence is selected or constrained. Constant `c_E != 0` and
   the derivative rules for `X` are the family's registered presentation; `dchi` was
   declared for completeness and is nowhere load-bearing.
