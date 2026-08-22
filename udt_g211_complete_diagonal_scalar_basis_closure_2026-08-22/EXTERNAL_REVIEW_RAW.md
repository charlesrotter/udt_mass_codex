**Primary Grade**

`VERIFIED_WITH_CAVEATS`

**Exact Findings**

1. No refuting defect was found in the local rank-two closure claim. The supplied-split uniqueness of `ell` and `sigma`, the exact basis change `(Omega,q)=(ell,sigma-ell)`, the lapse-only line `(Omega,q)=(ell,-ell)`, and the `V/W` inverse coefficients are coherent in the derivation and in the symbolic replay. See [G211 EXACT_DERIVATION.md](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/EXACT_DERIVATION.md:18) and [derive_diagonal_scalar_basis.py](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/derive_diagonal_scalar_basis.py:25).

2. The ADM determinant, inverse, Lorentz signature, temporal `dt`, fixed cone center, and width law `exp(-q)` check out under arbitrary positive supplied `H` and supplied shift `b`. See [G211 EXACT_DERIVATION.md](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/EXACT_DERIVATION.md:126) and [derive_diagonal_scalar_basis.py](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/derive_diagonal_scalar_basis.py:44).

3. The intake keeps the crucial conditional boundary intact: `Omega` cancels from cones, but arbitrary `q` is not thereby proved globally hyperbolic. Cauchy transfer is stated only from a supplied relative metric `g_q`, which is the correct reading. The null-affine law `d lambda_g = exp(2 Omega) d lambda_q` and the all-null weighted-integral criterion are consistent with the inherited G206 conformal theorem, but they remain analytic theorems rather than universally mechanized script conclusions. See [G211 EXACT_DERIVATION.md](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/EXACT_DERIVATION.md:191), [G206 EXACT_DERIVATION.md](/tmp/udt_g211_review_efn8o_7v/udt_g206_g205_conformal_timelive_nonspherical_robustness_2026-08-21/EXACT_DERIVATION.md:29), and [verify_core_package.py](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/verify_core_package.py:83).

4. The four G205 controls support exactly the bounded separation claimed and no more. In particular, the compensated case certifies outgoing radial affine restoration with unchanged relative cone data, but not full null completeness. That caveat is explicit and correctly preserved. See [G211 EXACT_DERIVATION.md](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/EXACT_DERIVATION.md:235), [run_radial_controls.py](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/run_radial_controls.py:16), and [G210 EXACT_DERIVATION.md](/tmp/udt_g211_review_efn8o_7v/udt_g210_g205_spatial_volume_robustness_2026-08-21/EXACT_DERIVATION.md:208).

5. The completed-pair pullback is consistent with the inherited G179 theorem: `Phi=-Omega-(1/2)log[...]`, generic spatially bearing clocks hear both modes, and Eulerian-normal / unshifted-static strata are `q`-blind but not `Omega`-blind. See [G211 EXACT_DERIVATION.md](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/EXACT_DERIVATION.md:252) and [G179 EXACT_DERIVATION.md](/tmp/udt_g211_review_efn8o_7v/udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/EXACT_DERIVATION.md:37).

6. Integrity and replay checks passed. `REVIEW_SCOPE.json` matched the required SHA-256 `553151874b32f4411ac184eae7d3c8d035b8230e9b87f5d46e3c94c0aea7dbc5`; all 34 registered payload hashes matched; the registered no-write replay passed byte-stably and reproduced 29 production assertions, 280,003 independent assertions over 10,000 exact cases, 4 radial profiles at 120 digits, and 31 hostile catches. See [verify_core_package.py](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/verify_core_package.py:42).

**Strongest Retained Theorem**

After a supplied calibrated `1+3` split with positive reference lapse and positive spatial reference, the complete local diagonal scalar sector is exactly two-dimensional: `(ell,sigma)` and `(Omega,q)` are equivalent rank-two coordinates, lapse-only deformation is not a third tile, causal cones depend only on `q`, while null affine reach and completed-pair depth hear `Omega`. See [G211 EXACT_DERIVATION.md](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/EXACT_DERIVATION.md:18).

**Strongest Caveat Or Failure**

The result stops at a conditional local basis theorem plus bounded G205 witnesses. It does not prove arbitrary-`q` global hyperbolicity, unrestricted live null completeness, or any physical/history/`X_max` selection, and the finite scripts do not mechanize the universal quantifiers behind the global causal-transfer and all-null affine criteria. See [G211 EXACT_DERIVATION.md](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/EXACT_DERIVATION.md:298) and [run_radial_controls.py](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/run_radial_controls.py:54).

**Replay Status**

`PASS`. Registered command executed read-only: `PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/verify_core_package.py`.

**Bounded Repairs**

None required for the sealed claim set.

Optional documentation-only cleanup: align the local variable names in [derive_diagonal_scalar_basis.py](/tmp/udt_g211_review_efn8o_7v/udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/derive_diagonal_scalar_basis.py:133) with the paper’s `v_i`/`w_i` notation to remove avoidable verifier-script ambiguity.
