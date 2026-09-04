# External Review Response

## Scope and authentication

I treated this as a sealed-evidence, zero-context review. I inspected only `/intake`, copied the full tree to `/work/g345_review_copy`, and ran checks only from that writable copy.

- `REVIEW_MANIFEST.sha256` matches `REVIEW_MANIFEST.tsv` exactly:
  `8686ac1a7285313d3418099c331915acddd43d3cddecc729bdadbf8d7193a554`.
- `REVIEW_SCOPE.json` matches the manifest entry exactly:
  `7eaac32355b0772ca835621f11c6fbec8adab138f36a26d7301be2c50a805cae`.
- The sealed tree contains 31 files total: 29 payload files plus `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`, matching `payload_count_excluding_manifest_and_detached_seal: 29`.
- Every manifest-listed payload hash and byte count matched exactly in `/intake` and in the `/work` copy.

## Findings by severity

### Low

1. `g345/derive_screen_scalar.py:460-461` and `g345/verify_screen_scalar_independent.py:316-317` use documentary compact-label assertions (`tuple(labels) == labels`) rather than executable per-lift dynamics. This is a vacuous check as written. It does not undercut the bounded claim because G345 does not compute lift aggregation at all and nowhere sums or selects lifts, but the executable evidence for the "retained separately" clause is weaker than the surrounding mathematical evidence.

2. `g345/derive_screen_scalar.py:495` and `g345/verify_screen_scalar_independent.py:289` record ordering-coverage tautologies (`index % 6 in range(6)`), and `g345/derive_screen_scalar.py:524` records a literal `True` for `principal_no_affine_reference_scale`. These named assertions add no evidentiary force. The underlying loops still do exercise all six permutations and compare principal formulas while varying `nu` and `t_reference`, so this is a verifier-quality issue, not a scientific defect.

3. `g345/verify_package.py:139-149` includes brittle text-token guards, including the line-wrap-sensitive literal `It is not yet\nbrightness` and the inert anti-token `not yet\n+brightness`. Those checks are integrity sentries, not analytic verification. They do not change the target, but they should not be mistaken for mathematical evidence.

I found no high-, medium-, or blocking low-severity defect.

## Adversarial mathematical review

1. Common-affine cancellation is correct. From G344, `K_10 = B_10^{-T}` and under common affine rescaling `B -> B/a`, hence `K -> aK` and `Delta -> a^2 Delta` (`sources/.../g344.../EXACT_DERIVATION.md:247-254`). From G340/G343 the endpoint frequencies satisfy `omega_i -> a omega_i` (`sources/.../g340.../EXACT_DERIVATION.md:96-113`, `sources/.../g343.../EXACT_DERIVATION.md:271-279`). Therefore `Khat_10 = K_10 / sqrt(omega_1 omega_0)` is exactly affine-invariant, and in two screen dimensions `det Khat = det K / (omega_1 omega_0)`, so `Dhat_10 = Delta_10 / (omega_1 omega_0)` in orthonormal screens.

2. The determinant-exponent classification is correct in the frozen monomial class `Delta omega_0^a omega_1^b`. Affine invariance gives `2 + a + b = 0`. Reversal symmetry gives `a = b`. Hence uniquely `a = b = -1`. The report is also explicit that this is only a restricted classification and does not choose a unique observable or arbitrary function of the scalar (`g345/EXACT_DERIVATION.md:55-71`).

3. The `GL(2)` scalarization is correct with the passive coordinate convention stated. If `x_i' = R_i x_i` and canonical covectors transform as `p_i' = R_i^{-T} p_i`, then
   `B_10' = R_1 B_10 R_0^T`,
   `K_10' = (B_10')^{-T} = R_1^{-T} K_10 R_0^{-1}`,
   and
   `q_i' = R_i^{-T} q_i R_i^{-1}`.
   Thus
   `det K' = det K / (det R_1 det R_0)` and
   `det q_i' = det q_i / (det R_i)^2`.
   Hence
   `sqrt(det q_1' det q_0') = sqrt(det q_1 det q_0) / abs(det R_1 det R_0)`,
   so `abs(det K)/(omega_1 omega_0 sqrt(det q_1 det q_0))` is exactly invariant, while the oriented determinant retains the expected orientation sign. I independently spot-checked this with a scratch numeric `GL(2)` calculation and obtained zero relative discrepancy.

4. Reversal is typed correctly. In one common affine gauge, G343/G344 give `B_01 = -B_10^T`, so `K_01 = -K_10^T`, hence `Khat_01 = -Khat_10^T` and `Dhat_01 = Dhat_10`. Under separately unit-frequency endpoint normalization, G343 gives `B_01^[1] = -alpha_01 [B_10^[0]]^T` with `alpha_01 = omega_1 / omega_0` (`sources/.../g343.../EXACT_DERIVATION.md:301-316`). Therefore `Delta_reverse^[1] = Delta_forward^[0] / alpha_01^2`, and dividing by the reverse endpoint frequency product `1/alpha_01` reproduces the same normalized scalar.

5. Stationary composition is correct and naive multiplicativity is correctly rejected. From G344,
   `H_1 = B_21^{-1} B_20 B_10^{-1}` and
   `Delta_20 = Delta_21 Delta_10 / |det H_1|` (`sources/.../g344.../EXACT_DERIVATION.md:198-223`).
   Since `H_1` carries affine weight one, the normalized joined scalar is
   `hhat_1 = |det H_1| / (omega_1^2 det q_1)`.
   Substituting into the normalized determinant formula yields
   `Dhat_20 = Dhat_21 Dhat_10 / hhat_1`.
   The production replay explicitly exercises all six nonidentity endpoint orderings, and the derivation correctly notes that independently normalized segment charts must first be converted into one common typed chart before sewing.

6. The reference-free mixed-direction formula is correct. Using G343's common-affine expressions
   `B_parallel = h_1 h_0 (T_1 T_0)^(-1/3) J_parallel / gamma`,
   `B_Z = (T_1 T_0)^(2/3) J_Z / gamma`,
   and
   `omega_i = gamma T_i^(-2/3) h_i`,
   with `h_i = sqrt(T_i^2 + lambda^2)`,
   gives
   `Delta = gamma^2 / (h_1 h_0 T_1^(1/3) T_0^(1/3) |J_parallel J_Z|)`.
   Dividing by `omega_1 omega_0 = gamma^2 h_1 h_0 / (T_1 T_0)^(2/3)` yields exactly
   `Dhat_10 = (T_0 T_1)^(1/3) / (((T_0^2 + lambda^2)(T_1^2 + lambda^2)) |J_parallel J_Z|)`,
   so both `gamma` and the marked event cancel. The longitudinal and transverse principal limits agree with the stated closed forms, and the coincidence limit `Dhat |T_1 - T_0|^2 -> 1` follows from the leading local expansions of the two integrals. I independently checked these numerically in a scratch script with max relative discrepancies around `1e-13` to `1e-15`, and coincidence error around `3e-11`.

7. The scalar-status language stays within the declared bookkeeping invariances. The package repeatedly states that dependence on the supplied spacetime, supplied normal observers, supplied endpoints, supplied ray direction, and supplied compact path label remains, and that "scalar" does not mean universally observer-independent (`g345/EXACT_DERIVATION.md:294-297,314-321`). Compact lifts are kept separate; no sum, weighting, interference rule, or preferred lift is derived.

8. The preserved chronology does not change the scientific target. The first repair changed only an over-strong monotonicity diagnostic on two already-converged coincidence samples; it did not change the preregistered coincidence formula, tolerance, candidate law, or bounded domain (`g345/PREREGISTRATION_EXECUTION_NOTE.md:8-31`). The aggregate-verifier repair fixed an impossible self-hash wording gate by moving the commit-hash requirement to later immutable records (`g345/PREREGISTRATION_EXECUTION_NOTE.md:33-38`). That changed verifier wording, not the scientific claim. I reproduced the registered no-write aggregate replay in `/work/g345_review_copy/g345`; it passed `17/17`. I also reran the three underlying scripts directly and reproduced sealed results exactly: production `9824/9824`, implementation-distinct direct-`T` Simpson `4360/4360`, and hostile `17/17`.

9. I found no silent promotion of this quantity into electromagnetic transfer, flux, luminosity, probability, amplitude, observational distance, a path or observer population, a generic spacetime theorem, stability, matter/mass, physical scale, `X_max`, or canon. On the contrary, those interpretations are repeatedly excluded in the preregistration, exact derivation, audit report, premise ledger, and status ledger.

## Sufficiency for the bounded grade

Yes. The core derivation closes exactly from the sealed G340/G343/G344 inputs, the declared bookkeeping invariances are handled with the correct inverse/transpose structure, reversal and typed sewing are correct, the mixed-direction formula and both principal limits close, and the repair chronology did not move the target. The replay evidence is strong enough for the bounded claim.

Residual caveat: some verifier assertions are documentary or tautological rather than substantive, especially for compact-label retention and a few coverage labels. Those are real quality nits, but they do not rise to a scientific finding against the bounded G345 result because the mathematical claim itself is per-labelled-ray, non-aggregating, and the load-bearing algebraic and numerical checks were independently reproduced.

ACCEPT_G345_BOUNDED_OBSERVER_CALIBRATED_SCREEN_SCALAR
