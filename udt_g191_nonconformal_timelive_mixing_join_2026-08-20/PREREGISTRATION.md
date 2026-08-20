# G191 preregistration — nonconformal time-live mixing join

Date: 2026-08-20

## Whole question and bounded regime

Does the externally accepted G190 completed-pair frequency/screen evaluator remain one coherent
metric initial-value problem when the supplied complete metric is simultaneously time-live,
nonconformally flat, and mixing-active?

The bounded arena is one analytic regular neighborhood with coordinates
`(eta,z,x,y)`, constants `H>0`, `mu>0`, and complete coframe

\[
\begin{aligned}
a(\eta)&=e^{H\eta},\\
\theta^0&=a\,d\eta,\\
\theta^1&=a\,dz,\\
\theta^2&=a\left[dx+\frac{\mu}{\sqrt2}(x+y)(d\eta+dz)\right],\\
\theta^3&=a\left[dy+\frac{\mu}{\sqrt2}(x+y)(d\eta+dz)\right],\\
g&=-(\theta^0)^2+(\theta^1)^2+(\theta^2)^2+(\theta^3)^2.
\end{aligned}
\]

The completed pair surface is supplied as

\[
F(\tau,\sigma)=(\eta=\tau,z=\sigma,x=0,y=0).
\]

The source vertex is the origin. The `+z` ruler orientation chooses the outgoing null germ. The
declared branch is `eta>=0` on its maximal regular analytic interval. No endpoint population or
later observer intersection is selected.

## Metric-led versus template-led

This is metric-led. Connection, curvature, affine propagation, frequency, and the full matrix
Jacobi response must be recomputed from the displayed coframe metric. G188 and G190 are regression
limits only; their output formulas may not be pasted into the joint result.

## Premise and choice ledger

| Item | Status | Role |
|---|---|---|
| `c_E` | `OBSERVED`, set to one in dimensionless control units | clock/ruler calibration only |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` | acts after the full pullback |
| displayed complete coframe | `CHOSE_MATHEMATICAL_CONTROL` | one analytic supplied history, not cosmology |
| `H>0`, `mu>0` | `free-and-explored` symbolic control parameters | no observational value or fit |
| pair surface and `+z` ruler orientation | `CHOSE_QUERY` | fixes local completed pair and outgoing germ |
| affine parameter | `DERIVED_CONDITIONAL` | normalized by the completed source clock |
| endpoint frequency | `DERIVED_CONDITIONAL` | contraction with the supplied pair clock carry |
| screen/Jacobi map | `DERIVED_CONDITIONAL` | G188 metric evaluator on the same branch |
| transparent transfer, source luminosity | `OMITTED` | no flux or SNe prediction in G191 |
| P1, static `phi(R)`, `R(Z)`, G116 coefficients | `OMITTED` | forbidden construction inputs |
| `X_max` | `OMITTED` | possible later global consequence only |

## Omitted sectors and limits

The test omits physical history/query population, later endpoint intersection, negative-eta and
global extensions, cut loci outside the analytic chart, spherical topology, emission, radiative
transfer, flux, source standardization, observations, action, dynamics, matter, mass, bootstrap,
signalling, and any numerical `X_max`.

The control retains the full rank-two screen. It may not be diagonalized and then reported as if
the original endpoint screen had no cross-response.

## Preregistered derivation and certification gates

1. Reconstruct `g=E^T eta_4 E`; prove invertibility and Lorentzian signature on the declared domain.
2. Pull back `g` to `F`; reconstruct the completed orthonormal `U,N` and the two null germs.
3. Derive the selected affine central ray and its affine-parameter relation from the Christoffel
   symbols, not from the conformal special case.
4. Derive endpoint frequency and the differential contraction law on the same branch.
5. Construct a parallel orthonormal screen and recompute the full self-adjoint tidal matrix from
   Riemann curvature.
6. Require both controls: `mu -> 0` reproduces G190's time-live scalar screen, while `H -> 0`
   reproduces the G188 mixing tide after accounting for the declared affine normalization.
7. Solve or certify the full vertex-normalized matrix Jacobi IVP. Off-diagonal response must remain
   live for `mu != 0`; setting it to zero is a red result.
8. Classify frequency monotonicity, determinant zeros/caustics, and whether `d_A(Z)` descends on the
   declared branch. Do not force single-valued descent if any turn or caustic occurs.
9. Independently replay random positive `(H,mu)` cases without importing production code or reading
   its output. Compare exact formulas with a separate numerical ODE integration and register raw
   residuals.
10. Catch at least: static substitution, mixing deletion, scalarization, curvature-sign reversal,
    frequency-sign reversal, nonaffine propagation, forced `d_A(Z)`, P1/G116/G189 input, `X_max`,
    native-transfer promotion, and physical-history promotion.

Certification requires exact symbolic residuals where available, raw numerical errors below
preregistered `2e-9` on the bounded independent sample, all hostile catches, the current premise
verifier, full repository tests, and `git diff --check`.

## Falsification contract

The proposed joined control fails if any of the following occurs:

- the displayed coframe is singular or the pair pullback is not regular Lorentzian;
- the completed outgoing germ is not null and source-normalized;
- the claimed central ray is not affine geodesic;
- the differential frequency identity fails;
- the screen is not parallel/orthonormal or the tidal operator is not self-adjoint;
- either `mu -> 0` or `H -> 0` regression fails;
- nonzero mixing produces no cross-response in the fixed source screen;
- the exact and independent ODE solutions exceed the registered tolerance.

## Maximum conclusion

At most G191 may establish that one exact nonconformally-flat, time-live, mixing-active complete
metric control produces frequency and full angular response through the single G190 initial-value
problem, and classify its regular parametric branch. It cannot identify the physical UDT history,
predict SNe, derive light transfer, choose observer populations, or establish global completion.
