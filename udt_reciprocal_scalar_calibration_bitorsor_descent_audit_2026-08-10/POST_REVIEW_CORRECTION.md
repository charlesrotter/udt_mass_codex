# Post-review correction

Date: 2026-08-10

External verdict: `ACCEPT_SCOPED_DESCENT_AND_OPEN_CALIBRATION_OWNER`.

The isolated reviewer reproduced the load-bearing descent and required two corrections before
banking:

1. The terminal determinant identity now carries its exact source-calibration factor. For source
   flag Gram matrix `s` and terminal pair metric `h`,

   ```text
   (-det h)/h_00^2 = Q * |det s|/|s_00|^2.
   ```

   Equality with `Q` therefore requires the declared normalized source calibration
   `|det s|=|s_00|^2`. The normalized audit witness satisfies it. A separate unnormalized witness
   has factor `9/4` and rejects silent omission.

2. The generated atlas string
   `NO_ISOMETRIC_ALIGNMENT_HAS_ZERO_LOG_DENSITIES` was an inverted English label. It is corrected
   to `NO_ISOMETRIC_ALIGNMENT_HAS_NONZERO_LOG_DENSITIES`, matching the exact result
   `rho_1=rho_2=Q=1` and `delta_RF=0` for every admitted isometric alignment.

Neither correction changes the primary scoped landing. They make its conditional calibration and
zero-generation boundary explicit.
