VERIFIED_WITH_CAVEATS

1. Required repairs: [verify_package.py](/intake/udt_g304_global_cell_constant_sector_discriminator_2026-08-30/verify_package.py:13) and [verify_package.py](/intake/udt_g304_global_cell_constant_sector_discriminator_2026-08-30/verify_package.py:83) resolve source hashes against `HERE.parent`, but [SOURCE_MANIFEST.tsv](/intake/udt_g304_global_cell_constant_sector_discriminator_2026-08-30/SOURCE_MANIFEST.tsv:2) stores paths relative to `/intake/frozen_sources`; as shipped, the registered replay fails with `AssertionError: founding.md`. [COMMANDS.md](/intake/udt_g304_global_cell_constant_sector_discriminator_2026-08-30/COMMANDS.md:8) also cites `verify_current_scientific_premises.py`, which is absent from the intake. I reran only the available standard-library checks; I did not rerun the SymPy production derivation.

2. Independent reproduction: from `ds^2=-f dt^2+dr^2/f+r^2 dΩ^2` I get
`R_tt = f(f''/2 + f'/r)`,
`R_rr = -(f''/2 + f'/r)/f`,
`R_θθ = 1-f-rf'`,
`R_φφ = sin^2θ R_θθ`,
`R = -f'' - 4f'/r + 2(1-f)/r^2`.
Trace-free equality `R_tt/g_tt = R_θθ/g_θθ` gives `r^2 f'' - 2f + 2 = 0`, so `f(r)=1+b/r-(R0/12)r^2`, and then `R_ab=(R0/4)g_ab`, `R=R0`. The invariants are `R_ab R^ab = R0^2/4`, `R_abcd R^abcd = R0^2/6 + 12 b^2/r^6`, `C_abcd C^abcd = 12 b^2/r^6`; smooth-center regularity therefore forces `b=0`.

3. Exact root/domain/invariant census reproduced: for `R0>0`, `P(r)=r+b-(R0/12)r^3` has one positive root for `b>=0`, two for `-4/(3√R0)<b<0`, one double root at `b=-4/(3√R0)` with `r*=2/√R0`, and none below that. For `R0=0`, roots are none for `b>=0` and one inner root for `b<0`; for `R0<0`, monotonicity gives none for `b>=0` and one inner root for `b<0`. On the smooth-center branch `b=0`: `R0>0` gives `X=√(12/R0)`, a simple zero at `r=X`, finite proper reach `πX/2`, infinite optical reach, finite curvature, `phi→+∞`, `chi→1`; `R0=0` gives no outer zero and both reaches infinite; `R0<0` gives `L=√(-12/R0)`, no outer zero, infinite proper reach, finite optical reach `πL/2`, `phi→-∞`, `chi→-1`.

4. Maximum honest conclusion: no scientific weakening is needed beyond the packet’s own boundary. G17’s exact active wording at [CURRENT_SCIENTIFIC_PREMISES.tsv](/intake/frozen_sources/CURRENT_SCIENTIFIC_PREMISES.tsv:148), read with the binding precision in [CANON.md](/intake/frozen_sources/CANON.md:462), legitimately functions only as a bounded static-chart horizon discriminator here; it is not a hard boundary, not an arbitrary accelerated-observer horizon, not a maximal-extension theorem, and not an all-frame physical relation ceiling. Founded/W1/W5/W6/G235/G294 do not supply a missed nonidentity sign cut, and WR-L stays separate because `r^2 f''-2f+2 = 2r/X` for `f=1-r/X`.

5. `X_EMERGES` is acceptably bounded only as “an algebraic static-patch radius arising after `R0>0` is selected”; it must not be read as physical `X_max`, and the packet mostly respects that guard. Banking grade is `repaired`, not external-verification: I reran `verify_global_cell_discriminator_independent.py` with `55` assertions passed, `run_catch_proofs.py` with `10/10` caught, and independently confirmed `14/14` source hashes under the intended `/frozen_sources` base plus the `8` domain rows, but the shipped replay surface is not clean until the verifier-path bug and the missing-command reference are fixed.
