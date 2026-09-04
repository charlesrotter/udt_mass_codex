# External Review Response

## Scope and authentication

I treated `/intake` as sealed read-only evidence and did not edit it. Before any executable replay, I copied the complete intake to `/work/g346_intake_copy`.

Authentication results:

- `/intake` contains 31 files total: 29 declared payloads plus `REVIEW_MANIFEST.tsv` and its detached seal `REVIEW_MANIFEST.sha256`.
- `REVIEW_MANIFEST.sha256` matches the exact bytes of `REVIEW_MANIFEST.tsv`.
- The 29 payload paths declared in `REVIEW_MANIFEST.tsv` match the actual payload set exactly.
- Every declared payload hash and byte count matches the sealed file bytes.
- `REVIEW_SCOPE.json` is internally consistent with the observed payload count and bounded task statement.
- The sealed Git proof records preregistration commit `9a037558dce6a4f86ffd5135ece0342ec1620c0b` for the frozen preregistration bundle.

## Replay and evidentiary status

I ran the registered no-write replay in `/work/g346_intake_copy/g346` exactly as banked:

- `python3 -S derive_directional_angular_area.py`: `PASS`, `11204/11204`
- `python3 -S verify_directional_angular_area_independent.py`: `PASS`, `4251/4251`
- `python3 -S run_catch_proofs.py`: `PASS`, `20/20`
- `python3 -S verify_package.py`: `PASS`, `19/19`

These replays reproduced the banked outputs exactly.

I did not treat text-token or documentary checks as mathematical proof. In particular, some guards are only integrity scaffolding rather than substantive derivations, including the unconditional `True` records in [derive_directional_angular_area.py](/intake/g346/derive_directional_angular_area.py:558), the string-based promotion checks in [run_catch_proofs.py](/intake/g346/run_catch_proofs.py:123), and the token-presence checks in [verify_package.py](/intake/g346/verify_package.py:110).

## Independent mathematical review

No blocking mathematical defect was found in the bounded G346 claim.

1. The `p = omega q theta` map is correctly typed and does not require imported optics.
At fixed observer frequency, a null tangent decomposes locally as `k = omega (n + s)` with `s` unit spatial direction in the observer rest space. A sky variation tangent `theta` to the local unit sky satisfies `g(s,theta)=0`, so the induced screen covector is `p = g(delta k, .)|screen = omega q theta`. This is exactly the covector/vector distinction stated in [EXACT_DERIVATION.md](/intake/g346/EXACT_DERIVATION.md:31). The word `celestial` is only the tangent geometry of the observer’s local sky sphere; I found no hidden detector, radiative transfer, or optical reciprocity import.

2. The metric solid-angle and screen-area forms are local metric area forms, not borrowed observational laws.
Given endpoint screen metric `q_i`, the sky tangent area form is `dOmega_i = sqrt(det q_i) d^2 theta_i` and the screen area form is `dA_i = sqrt(det q_i) d^2 x_i`, as stated in [EXACT_DERIVATION.md](/intake/g346/EXACT_DERIVATION.md:44). This is consistent with the G342 source-sky normalization [sources/udt_g342_full_null_jacobi_beam_area_2026-09-04/EXACT_DERIVATION.md](/intake/sources/udt_g342_full_null_jacobi_beam_area_2026-09-04/EXACT_DERIVATION.md:89) and G345’s use of metric screen forms as induced area structures rather than detector measures [sources/udt_g345_observer_calibrated_screen_scalar_2026-09-04/EXACT_DERIVATION.md](/intake/sources/udt_g345_observer_calibrated_screen_scalar_2026-09-04/EXACT_DERIVATION.md:111).

3. Both directional Jacobians and all frequency powers are correct.
From `x_1 = B_10 p_0 = B_10 omega_0 q_0 theta_0`, one gets
`det(dx_1/dtheta_0) = det(B_10) omega_0^2 det(q_0)`, hence
`A_{1<-0} = omega_0^2 |det B_10| sqrt(det q_1 det q_0)`.
The reverse formula uses `omega_1^2` analogously. There is no missing or extra frequency factor. This matches [EXACT_DERIVATION.md](/intake/g346/EXACT_DERIVATION.md:58).

4. The arbitrary `GL(2)` typing is correct outside orthonormal frames.
For passive endpoint coordinate changes, `x' = R x`, `theta' = R theta`, `p' = R^{-T} p`, `q' = R^{-T} q R^{-1}`, and `B' = R_1 B R_0^T` are the correct transformations, and they make `p = omega q theta` covariant exactly as shown in [EXACT_DERIVATION.md](/intake/g346/EXACT_DERIVATION.md:95). This also resolves the possible confusion with G344’s orthonormal-frame `O(2)` specialization [sources/udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md](/intake/sources/udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md:170): outside orthonormal frames, the G345/G346 `R^{-T}` covector typing is the correct one.

5. Common-affine invariance, marked-event covariance, common-gauge reversal, and separately unit-frequency reversal all close exactly.
G343 gives `B -> a^{-1} B` under common affine rescaling and leaves the marked-event converted propagator invariant [sources/udt_g343_bilocal_screen_phase_space_propagator_2026-09-04/EXACT_DERIVATION.md](/intake/sources/udt_g343_bilocal_screen_phase_space_propagator_2026-09-04/EXACT_DERIVATION.md:247). Combining this with `omega -> a omega` leaves each directional Jacobian invariant. In one common affine gauge, `B_01 = -B_10^T`, so `A_{1<-0}/A_{0<-1} = (omega_0/omega_1)^2`. In separately endpoint-unit gauges, G343’s typed reset `B_{01}^{[1]} = -alpha_{01} [B_{10}^{[0]}]^T` forces `A_{0<-1}^{[1]} = alpha_{01}^2 A_{1<-0}^{[0]}` [EXACT_DERIVATION.md](/intake/g346/EXACT_DERIVATION.md:146).

6. Inverse G345 is exactly the geometric mean, not merely a special-case resemblance.
G345’s scalar is
`Dhat_10 = 1 / (|det B_10| omega_1 omega_0 sqrt(det q_1 det q_0))`
[sources/udt_g345_observer_calibrated_screen_scalar_2026-09-04/EXACT_DERIVATION.md](/intake/sources/udt_g345_observer_calibrated_screen_scalar_2026-09-04/EXACT_DERIVATION.md:97). Multiplying the two G346 directional Jacobians and taking the square root gives exactly `1 / Dhat_10`, with no remaining frame, affine, or endpoint-order ambiguity [EXACT_DERIVATION.md](/intake/g346/EXACT_DERIVATION.md:191).

7. Stationary sewing is typed correctly for all endpoint orderings, and bare multiplication is false.
From G344,
`H_1 = B_21^{-1} B_20 B_10^{-1}` and
`|det B_20| = |det H_1| |det B_21| |det B_10|`
[sources/udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md](/intake/sources/udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md:198). Dividing by the middle-endpoint clock/metric factor gives
`hhat_1 = |det H_1| / (omega_1^2 det q_1)` and therefore
`A_{2<-0} = hhat_1 A_{2<-1} A_{1<-0}`. The outer-identity case remains singular exactly where the type-I chart should fail, not as a hidden interior defect [EXACT_DERIVATION.md](/intake/g346/EXACT_DERIVATION.md:233).

8. Mixed direction, both principal limits, coincidence, and analytic positivity are all consistent with the source chain.
G343 and G344 prove each scalar `B` channel has the sign of `T_1 - T_0`, so `det B > 0` for every noncoincident positive endpoint pair [sources/udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md](/intake/sources/udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md:39). G345’s reference-free formulas give the mixed result, and G346’s principal formulas follow exactly from the `lambda = 0` and `lambda -> infinity` limits [EXACT_DERIVATION.md](/intake/g346/EXACT_DERIVATION.md:278). Coincidence behaves as `|epsilon|^2`, consistent with `B = epsilon I + O(epsilon^3)` and with the type-I boundary singularity rather than an interior caustic [sources/udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md](/intake/sources/udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md:310).

9. Compact labels remain separate, and the scientific target did not drift into forbidden claims.
The derivation keeps each compact lift `L` separate [EXACT_DERIVATION.md](/intake/g346/EXACT_DERIVATION.md:358). I found no derivation of finite-beam evolution, transfer, brightness, flux, luminosity, probability, selected distance, route/population selection, matter/mass, scale, `X_max`, or canon. The result stays an infinitesimal metric angular-area identity on one supplied spacetime/observer/ray family.

## Scratch reconstruction

Using a fresh standalone `python3 -S` script with direct Simpson quadrature and no intake imports, I tested one mixed-direction sample at `t0=1.19`, `t1=2.41`, `t2=3.77`, `lambda=0.83`, `gamma=1.27`, plus arbitrary endpoint `GL(2)` frames. It produced:

- `A_{1<-0} = 1.377241763884338`
- `A_{0<-1} = 1.658991556186616`
- reversal residual `8.88e-16`
- geometric-mean residual `6.66e-16`
- stationary-sewing residual `8.88e-16`
- `GL(2)`-moved forward/sewing residuals `4.44e-16` and `8.88e-16`

This independent spot reconstruction agrees with the sealed derivation’s load-bearing identities.

## Self-reference repair

The aggregate self-reference repair did not change the scientific target. The issue was only that a preregistration file cannot contain the hash of the future commit created by committing that file. The repair moved that check to later documentary evidence and left formulas, alternatives, tolerances, outcomes, and the maximum conclusion unchanged, as stated in [PREREGISTRATION_EXECUTION_NOTE.md](/intake/g346/PREREGISTRATION_EXECUTION_NOTE.md:13). I agree with that classification.

## Verdict

The bounded G346 result survives adversarial review on the sealed intake. The mathematical content is a local infinitesimal causal-geometry statement built from the supplied metric screen forms, observer frequencies, bilocal Jacobi block, endpoint density, and typed stationary elimination. The package’s text/document guards are weaker than the mathematics, but they do not expose a scientific failure.

ACCEPT_G346_BOUNDED_DIRECTIONAL_ANGULAR_AREA_RECIPROCITY
