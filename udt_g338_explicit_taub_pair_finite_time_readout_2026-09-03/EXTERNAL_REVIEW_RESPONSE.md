# External Review Response — G338

## Scope and seal authentication

I treated `/intake` as sealed read-only evidence and did not inspect or use any repository content outside it. I copied only `/intake/g338` into the writable replay directory `/work/g338_external_review.IWopf3` before running any checks there.

Seal results:

1. `REVIEW_MANIFEST.sha256` matches `REVIEW_MANIFEST.tsv` exactly: `b485c8a553eb225cf9a3e4a0803753073059d29d21329871f34ae2008433b92f`.
2. `REVIEW_SCOPE.json` is listed in the manifest with the recorded size `541` and SHA-256 `575b921c1217ea1a638fa63719b3f8e0d497b9bb97e1f0e28944bacb7939bc2e`; the payload matches.
3. The scope count is consistent: `/intake` contains `39` files total, which equals `36` manifest payloads plus `REVIEW_MANIFEST.tsv`, `REVIEW_MANIFEST.sha256`, and no extras.
4. Every one of the `36` manifest payload entries matched both recorded byte count and recorded SHA-256.
5. The source stamps recorded in `g338/SOURCE_SCOPE.tsv` matched the sealed source files inside `/intake/sources` during intake authentication.

## Findings

1. Severity `none`: no repair-required mathematical defect was found in the bounded G338 claim.
The source metric from G324 is
`g = -dT^2 + C_X^2 T^(-2/3) dX^2 + C_perp^2 T^(4/3) (dy^2 + dz^2)` on `T > 0`, with Kasner exponents `(-1/3, 2/3, 2/3)`. These satisfy `sum p_i = sum p_i^2 = 1`, so the displayed Kasner form is Ricci-flat in the bounded imported sense used by G323/G324.

Take the `T0`-orthonormal spatial basis
`E_X = (T0^(1/3)/C_X) ∂X`, `E_Y = (1/(C_perp T0^(2/3))) ∂y`, and, by transverse rotational symmetry, choose the initial unit direction
`e(T0) = sqrt(rho) E_X + sqrt(1-rho) E_Y`, `rho in [0,1]`.
Under the declared commuting-translation-field carry, the coordinate coefficients stay fixed, so at `u = T/T0`
`|e(T)|^2 = rho u^(-2/3) + (1-rho) u^(4/3) =: G(u,rho)`.
This reconstructs the claimed `G` directly from the source metric and the declared normalization.

In the carried `2 x 2` pair plane, the metric in the basis `(∂T, e(T))` is `diag(-1, G)`. For finite rapidity `z`, let
`B = [[cosh z, sinh z], [sinh z, cosh z]]`.
Then the full pullback is
`h = B^T diag(-1, G) B`, hence
`h00 = -cosh^2 z + G sinh^2 z`,
`h01 = (G-1) sinh z cosh z`,
`h11 = -sinh^2 z + G cosh^2 z`.
Because `det B = cosh^2 z - sinh^2 z = 1`,
`det h = det(diag(-1,G)) = -G`.
So the off-diagonal term is load-bearing and the determinant claim is correct.

Writing `Delta = cosh^2 z - G sinh^2 z = -h00`, the regular pair stratum is exactly `Delta > 0`. Using the unchanged G176/W1 kernel on the completed pair,
`T_pair = sqrt(Delta)`,
`L_sigma^2 = h11 - h01^2 / h00 = G / Delta`,
`m = T_pair L_sigma = sqrt(G)`,
`L_s = 1 / sqrt(Delta)`,
`beta = h01 / h00 = -(G-1) sinh z cosh z / Delta`,
`beta_s = beta / sqrt(G)`,
`Phi = -1/2 log Delta`,
`chi = tanh Phi = (1-Delta)/(1+Delta)`.
These formulas are internally consistent and match the bounded W1 theorem from G176.

At zero boost `z = 0`, `Delta = 1`, `h = diag(-1, G)`, `beta = 0`, `Phi = 0`, `chi = 0`, while `m = sqrt(G)` still varies with `u` and `rho`. The terminal scalar is therefore blind at zero boost, but the full completed-pair ruler-density channel is not. That statement is correct and not overstated.

The initial jets are also correct:
`G_u(1) = (4 - 6 rho)/3`,
`G_uu(1) = (4 + 6 rho)/9`,
`d(sqrt G)/dT |_(T0) = (2 - 3 rho)/(3 T0)`.
Thus the unique first-order silent direction is `rho = 2/3`. For that direction,
`d^2(sqrt G)/dT^2 |_(T0) = 4/(9 T0^2) > 0`.
With `y = u^(2/3)`,
`G - 1 = (y-1)^2 (y+2) / (3 y)`.
Hence the silent direction turns on exactly for every finite `u != 1` on both sides, not just in a truncated Taylor sense.

The complete regular-interval classification is correct:
for `z = 0`, every `u > 0` is regular;
for finite `z != 0`, regularity is `G < coth^2 |z|`.
If `rho = 1`, then `G = u^(-2/3)` and regularity is `u > tanh^3 |z|`.
If `rho = 0`, then `G = u^(4/3)` and regularity is `u < coth^(3/2) |z|`.
If `0 < rho < 1`, then `G(y) = rho/y + (1-rho) y^2` has a unique minimum at
`y_* = (rho / (2(1-rho)))^(1/3)`, equivalently
`u_* = sqrt(rho / (2(1-rho)))`,
while `G(1,rho) = 1 < coth^2 |z|`.
Therefore there are exactly two pair-null boundaries `u_- < 1 < u_+` and one regular interval `(u_-, u_+)`.

No pair-germ boundary was improperly promotable to an ambient singularity or horizon on the sealed evidence. `Delta = 0` means only that the declared carried clock becomes null in the chosen pair plane. The ambient spacetime singularity in G324 is at `T -> 0`, whereas every finite positive-`T` pair boundary has finite ambient curvature
`K = 64 / (27 T^4)`.

Premise and scope stamps were handled correctly in the package text I checked. The statuses stay bounded as follows:
`Universal_Reciprocity_DDR` and `quiet_GR_response` remain `OWNER_ADOPTED_PROVISIONAL_POSTULATE`;
`G176_completed_pair_Dual_Reciprocity` remains `WORKING_FOUNDATIONAL_CLARIFICATION`;
`Taub_Kasner_metric` remains `DERIVED_CONDITIONAL_G323_G324`;
`compact_T3_quotient` remains `CHOSE_BOUNDED_DIAGNOSTIC_FAMILY`;
`pair_carry` remains `CHOSE_DECLARED_QUERY`;
`pair_regular_stratum` remains `DERIVED_DOMAIN`;
`observation_scale_Xmax` and `stability_occupancy` remain open.
I found no sealed wording that canonized the provisional dynamics, selected the carry, selected a physical topology or occupancy, or fixed a scale or `X_max`.

2. Severity `low`: the registered code replay does not independently mechanize the source-metric-to-`G(u,rho)` bridge.
The replayed scripts strongly test the pullback algebra, W1 normalization, interval structure, hostile mutations, and bounded wording. But the production script treats Kasner powers and representative `G` values as inputs, and the independent verifier also starts from the closed-form `G(u,rho)` rather than rebuilding it from the metric coefficients and the `T0` unit-direction normalization. This is a hardening gap in the automation, not a defect in the bounded mathematics, because the bridge is short and I independently rederived it above from the sealed source metric.

Repair request: none required for the present verdict.
Optional hardening: add one dependency-free replay check that reconstructs `G` from the metric coefficients, the `T0` orthonormal basis, and the declared fixed translation-field coefficients.

3. Severity `low`: the aggregate verifier in the package-only `/work` replay cannot itself reauthenticate the sealed upstream source hashes.
`verify_package.py` degrades to `sealed_source_absence_is_explicit` when only the copied `g338` package is present. That behavior is honest, and it did not hide a failure here because I separately authenticated `g338/SOURCE_SCOPE.tsv` against the sealed `/intake/sources` files before replay.

Repair request: none required for the present verdict.
Optional hardening: allow the aggregate verifier to accept an explicit sealed-intake root for source-hash checking while keeping repository access disabled.

## Replay results

Replay was run only in `/work/g338_external_review.IWopf3` with dependency-free `python3 -S` commands.

1. `derive_explicit_taub_pair_readout.py`: passed `169/169`.
2. `verify_explicit_taub_pair_readout_independent.py`: passed `16/16`.
3. `run_catch_proofs.py`: passed `9/9`.
4. `verify_package.py`: passed `12/12`, including no-write aggregate replay and no byte changes during the no-write rerun.

I found no evidence of circular import dependence between production and independent scripts. The stronger statement I can defend is narrower: the independent verifier is implementation-distinct for the pullback/W1 algebra and numerical interval checks, but it is not independently deriving `G` from the source metric inside code.

The numeric tolerances are not loose relative to the tested formulas. The independent sweep used 500 deterministic random cases, achieved determinant error below `2e-11`, W1 error below `3e-10`, and exercised more than 100 regular cases. Analytic coverage in the sealed derivation, not sampling alone, is what closes arbitrary finite `z` and full-direction coverage.

## Strongest defensible landing

On the exact G323/G324 Taub/Kasner spacetime, and only under the explicitly declared commuting-translation-field carry, the unchanged G176/W1 completed-pair kernel does produce the G338 formulas and the bounded finite-time classification:
the full `2 x 2` pullback with shift is correct, `det(h) = -G` exactly, the regular stratum is `Delta > 0`, zero-boost terminal blindness coexists with nontrivial ruler-density evolution, the unique initially silent direction is `rho = 2/3`, and that direction turns on exactly at finite time on both sides.

Nothing in the sealed evidence upgrades this to a physical history selector, a universal carry theorem, a topology selector, a stability theorem, a matter/source claim, an observational scale, or an `X_max` statement.

ACCEPT_G338_BOUNDED_FINITE_TIME_PAIR_READOUT
