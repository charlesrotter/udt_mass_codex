# NCB1 direct adversarial review

Verdict: **VERIFIED-WITH-CAVEATS**, conditional and UNPROMOTED. No mathematical
defect, scientific repair or required narrowing was found in the exact scope
of INITIAL_CANDIDATE equations (1)–(14). Fidelity review of the final result,
lay brief and navigation is still a separate pending stage at this writing.

Reviewer: `/root/ncb1_clock_beam_review`, actual fresh separate context,
2026-09-12. Reviewed initial candidate SHA-256:
`8f58d15f3e24bf8878fca2af5c24c95cb7c68dec49bfb2fa175fbe945b54879f`.
The current G312 GR FILTER ONLY overlay controls G394's historical
equation-ownership wording. Supplied Ric=0 geometry is not a native UDT
response law derived or adopted here. G394's exact metric remains a source;
the new result evaluates declared metric readouts on it.

## What was attacked and why it survives

1. **Clock sign and spatial lapse.** Reconstructing the conformal-base
   geodesic gives k=C N^-2(1,s,0,0), omega=C/N and the proper clock slope
   N_o/N_e. Independently, the fixed-label incidence equation gives
   dt_o/dt_e=1 and the same proper-time slope. Thus no time-only lapse
   assumption is smuggled into the spatially varying NE1 metric. The exact
   identity D_s lambda=t(D_s P)^2 gives candidate (5); analyticity and uniform
   decay justify strictness for every finite nonzero epsilon and nonempty
   leg. The candidate correctly does not infer R>1 on every finite leg.

2. **Both screen directions and fixed-affine differentiation.** The original
   connection makes E_y,E_z parallel vectors on the central ray. Conserved
   transverse momenta have source variation delta p_i=b_i(e) delta theta_i.
   Initial longitudinal tangent changes only quadratically with transverse
   angle, and the base geodesic equations have no linear transverse-momentum
   term. The candidate therefore has the correct fixed-affine two-dimensional
   map, including its source factors. Dropping a source width would pass the
   homogeneous Jacobi equation but fail its unit vertex slope; the actual
   mutation test catches precisely that defect.

3. **Original metric curvature.** The source-first script independently built
   the diagonal metric's Christoffels and R(E_i,k)k before candidate exposure.
   It obtained both individual candidate tides, vanishing cross entry, and
   trace cancellation after the NE1 null constraint. The tide was not
   invented by differentiating the proposed Jacobi solution. Its sign agrees
   with G348's convention. Positivity of the quadratures rules out conjugate
   endpoints on these longitudinal future legs for all finite amplitudes;
   it supplies no global cut-locus or other-direction conclusion.

4. **Reversal and affine units.** On the same reverse segment, the reception
   source normalization replaces N_e by N_o, so each reverse screen width is
   R^-1 times the forward width and the area ratio is R^2. This is G348
   reciprocity reused. The candidate explicitly distinguishes mathematical
   reversal from a later causal return. Its arbitrary-C scaling is correct.

5. **Long-reception estimates.** For fixed nonzero epsilon, G394's uniform
   bounded remainder in lambda supplies upper and lower positive bounds
   N^2/b_i^2=Theta(exp(alpha t)t^-3/2). On a sufficiently late interval,
   split the integral at t/2 for an upper bound, and retain its last fixed
   positive-length subinterval for a lower bound. This proves the claimed
   integral order and logarithmic clock/area rates without assuming a
   constant prefactor or reading a limit from a plot. The epsilon=0 control
   is exactly G342 under T=t^(3/4). Constants are allowed to depend on fixed
   nonzero amplitude; exchanging the small-amplitude and late-time limits
   is explicitly excluded.

6. **Shape factor.** Divergence of both positive weighted integrals and
   uniform P->0 force I_y/I_z->1. The endpoint factor tends to exp(P_e),
   hence unity only at the declared t_e=1 initial event (or another source
   with P_e=0). Candidate (12) and its general-source qualification are
   correct. Width-ratio circularization neither proves zero instantaneous
   shear nor background area recovery.

7. **Late emission on a fixed marked path.** Directly integrating
   t(D_sP)^2 using the leading Bessel phase gives precisely (13). The
   remainder is uniform on each fixed-length interval at fixed amplitude.
   Since |sin x|<x for x>0, the lower exponent in (14) is strictly positive.
   Continuous emission time reaches both phase extrema; the stated liminf,
   limsup and special sin(2kd)=0 constant limit follow. This is bounded
   clock persistence, distinct from the exponential long-reception result.
   No fixed proper baseline or proper duration is held constant.

These points were reconstructed in SOURCE_FIRST_RECONSTRUCTION.md and sealed
at 17:23:31 UTC before the direct-review invitation. The work order's route
names and question were exposed, so this was source-first reconstruction,
not wholly uninformed mathematical discovery. The parent had independently
frozen its candidate at 17:22:07 UTC; no reviewer formulas were sent before
that freeze. Hashes are documentary correspondence, not signed chronology.

## Actual independent and regression checks

The captured source-first exact SymPy run passed all 40 listed coverage
predicates for the original metric connection/curvature, both signs,
parallel screens, null-constraint tide trace, and integral Jacobi identity.
Structural zeros and normalization identities are not 40 independent proofs.

After candidate exposure, a new implementation integrated the complete
eight-dimensional position/tangent null-geodesic equations from independently
assembled metric first-derivative arrays and Christoffels. Perturbed source
sky angles {0.002,0.001,0.0005} were tested in both screen directions on six
frozen cases, including t_e<1, both signs, negative amplitude and epsilon=1.2.
This finite-difference route is different from integrating the proposed
scalar Jacobi ODE. It uses accepted G394 first-derivative constraints and the
same SciPy technology; it does not independently reprove G394's full Ricci
result. The maximum finest screen-map scaled error was
`5.009068049238301e-08`; coarse-to-fine error reduction ranged from
`15.994788320040206` to `16.000062499721622`, consistent with the frozen
second-order angle difference. The maximum direct null residual was
`6.24743717966032e-16`, and central endpoint error
`9.9322259818389e-13`. Independently taking ratios of short proper-time
integrals at fixed endpoint worldlines gave maximum clock error
`2.2141399824704422e-11`. All passed the frozen thresholds; no samples,
tolerances or formulas were repaired after these outcomes.

The reviewer also actually reran both parent scripts. Their stdout replayed
byte-for-byte: 39 symbolic predicates and 64 finite cases. The largest
author mixed-scaled width error was `2.3961519034498936e-12`; the frozen
tighter worst-case repeat gave `2.520250304520591e-13`; no warnings occurred.
These replays are same-code regression, not independent derivation.

All three parent hostile variants were independently rerun and exited 1
under the same baseline assertions. Their rejected defects were:

| Mutation | Rejecting assertion | Nonzero defect |
|---|---|---|
| Drop source width | vertex_unit_affine_slope | (1-be)/be |
| Invert clock | clock_frequency_and_correspondence | Ne/No-No/Ne |
| Suppress lapse response in tangent | affine_geodesic_-1_0 | C^2[4t(a_t-a_x)+1]/2 |

The first failure illustrates why a Jacobi-equation-only check is inadequate;
the source normalization is an independently required initial condition.
The lapse mutation is rejected by the actual original connection, rather
than by a text token or a mutation-name guard. No missing gate was converted
to a scientific conclusion. Execution/capture records preserve commands,
stdout/stderr, limits and environment versions. Seven of eight allowed
reviewer scientific runs have been used; no full397 run was started by this
reviewer. The parent handles the current premise audit.

## Independence and residual limits

| Axis | Actual record |
|---|---|
| Context | Fresh separate reviewer context; parent startup attributed |
| Model | Runtime model/version UNATTESTED; different-model axis UNTESTED |
| Implementation | Independently written source-first metric curvature and direct-stage full geodesics; parent code replays separately labeled regression |
| Argument | Source-first reconstruction before NCB1 proof/code/output exposure, then direct attack |
| Library | SymPy/SciPy technology shared; different-library claim not made |
| Premises | Same supplied G394 geometry and G220/G348 definitions; not premise-independent |
| Other review | Human specialist/formal proof/interval certification UNTESTED |

No required scientific repair exists to prescribe. The strongest survivor is
the entire bounded candidate (1)–(14) as exact conditional metric geometry
and its stated analytic limits. Maintain UNPROMOTED status and all supplied
metric/marking/observer/path restrictions. Do not turn this into physical
light, observational distance, a full dynamic pair plane, event/path
population, adopted Einstein dynamics, generic persistence/stability, or a
fixed-size apparatus prediction. No physical c_E scale or X_max input was
introduced. G394/G342/G348/G220 retain credit for their existing results;
the local reuse review is not a whole-repository novelty theorem.

The earlier source packages' full computations, generic Gowdy theory,
nonaxial rays, finite beams and alternative observers were not re-reviewed
or recomputed. Finite floating agreement is numerical support, not a proof
at infinity or interval certification. No protected payload or unrelated
dirty file was read or modified. This reviewer writes only new review files
and makes no Git mutation or scientific promotion.
