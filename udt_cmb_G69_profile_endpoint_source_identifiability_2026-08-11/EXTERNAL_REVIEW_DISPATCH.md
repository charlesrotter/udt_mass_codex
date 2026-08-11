# Cold adversarial review dispatch — G69 CMB identifiability atlas

You are receiving a sealed read-only intake. Do not edit files, continue the research, import
outside repository knowledge as affirmative UDT physics, or inspect anything outside the intake.

## Claimed bounded result

The package reconstructs `21 x 15 = 315` intermediate observer-sky Jacobi maps from already saved
G68 trajectories. It reports:

1. all `15/15` preregistered three-channel sensitivity matrices for
   `(endpoint, lapse, mixing amplitude) -> (area, anisotropy, azimuthal carry)` are numerically full
   rank under the frozen threshold, though condition numbers are large;
2. for every invertible `D`, unrestricted positive-definite source covariance obeys the exact
   compensation identity

   ```text
   C_obs = D C_src D^T,
   C_src = D^-1 C_obs D^-T;
   ```

3. therefore the geometric instrument distinguishes the controls locally, while a sky covariance
   cannot select the geometry until source/state or independent channel ownership is restricted.

The package explicitly does not claim that scalar TT reads all three channels or that the full CMB
data set is globally non-identifying.

## Required review

1. Reproduce every manifest hash before interpretation.
2. Type-check the saved-state reconstruction `D_AB=E_A g J_B` and independently inspect the cell,
   sensitivity, and covariance atlases.
3. Audit whether the PCHIP/CubicSpline agreement is a legitimate interpolation check and whether it
   is honestly distinguished from independent path integration.
4. Recompute the finite-difference matrices and rank classifications. Challenge the midpoint,
   normalization, threshold, conditioning, and use of azimuthal carry.
5. Prove or refute the source-covariance congruence theorem, including positive definiteness and
   singular-map qualifications.
6. Determine exactly which observation classes the theorem does and does not address. In
   particular, challenge any silent jump from a local `2 x 2` screen covariance to full TT/TE/EE/BB
   spectra or a physical source population.
7. Audit the observational-anchor policy. Decide whether a few future coefficients can be fitted
   without violating the exact compensation freedom, and state the necessary ownership conditions.
8. Search for omitted profile, endpoint, source, sign, branch, or query freedom that invalidates the
   bounded conclusion.
9. Run or independently replace the exact algebra and package checks. Do not accept same-code
   agreement as independent evidence.

## Required landing

Return exactly one primary landing:

- `VERIFIED_AS_BOUNDED`;
- `VERIFIED_WITH_CAVEATS`;
- `CORRECTABLE_DEFECT`;
- `RANK_CLAIM_NOT_SUPPORTED`;
- `SOURCE_DEGENERACY_CLAIM_NOT_SUPPORTED`;
- `TYPE_OR_SCOPE_FAILURE`.

Separate `DERIVED`, `OBSERVED`, `CHOSE_CONTROL`, `CONDITIONAL`, and `OPEN`. Give exact corrections,
if any, and runnable algebra for every load-bearing challenge. Do not derive a physical CMB profile,
source, endpoint, spectrum, action, bootstrap law, `X_max` value, or signalling rule.
