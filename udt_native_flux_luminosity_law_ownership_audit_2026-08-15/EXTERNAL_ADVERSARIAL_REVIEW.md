**Landing**

`VERIFIED_WITH_CAVEATS__Z3_GEOMETRIC_CLOCK_FACTOR__TRANSFER_PRODUCT_OPEN`

**Load-Bearing Algebra**

1. The Wronskian step survives. In a parallel orthonormal screen basis, the symmetric optical tidal matrix gives `W' = 0`; endpoint normalization plus affine reversal yields `D_r = Z O_o D_f^T O_s`, so `|det D_r| = Z^2 |det D_f|` and therefore `d_G = Z d_A`. The sign and screen-gauge issues are absorbed by the orthogonal overlaps and the absolute determinant, and `d_A` and `d_G` stay distinct types throughout.

2. The clock factor is owned only as a clock/frequency ratio. From the query readout, `d tau_o/d tau_s = Z`, hence `d tau_s/d tau_o = 1/Z`; that is identical to the frequency ratio, not to the energy ratio.

3. The flux bookkeeping also survives. With `L_Omega = dE_s/(d tau_s dOmega_s)`, `dA_o = d_G^2 dOmega_s`, survival `eta`, and per-carried-unit energy ratio `epsilon`, the exact factorization is `F_o = L_Omega eta epsilon (d tau_s/d tau_o)/d_G^2 = L_Omega eta epsilon/(Z^3 d_A^2)`. An independent inline `python3` reconstruction returned `det_factor=Z**2`, `flux=LO*eps*eta/(Z**3*dA**2)`, `dL2=Z**3*dA**2/(eps*eta)`, and `wronskian_zero=True`.

4. The open arrow is real. The intake marks radiative survival and energy conversion as unowned, so neither `eta=1` nor `epsilon=1/Z` follows from the metric/query alone.

**Objections And Repairs**

- The nonuniqueness argument works, but the largest justified class is bigger than the displayed power laws. From composition and reversal alone, any positive multiplicative character on `R_{>0}` is admissible; `Z^-p` and `Z^-q` are the continuous/local subclass. That is a wording repair, not a theorem-breaking flaw.
- The old Maxwell/photon closure cannot overrule the current registry. The source census explicitly demotes that historical claim and says it cannot control against current G13/G16/G21 precedence.

**Maximum Justified Conclusion**

The intake supports a regular single-branch propagation theorem only: geometry plus the typed query conditionally own `d_G = Z d_A` and the extra clock factor, hence the `1/(Z^3 d_A^2)` prefactor, but they do not derive the transfer product `eta epsilon`, the historical `d_L = Z^2 d_A` closure, or any SNe/global/material/action claim.

