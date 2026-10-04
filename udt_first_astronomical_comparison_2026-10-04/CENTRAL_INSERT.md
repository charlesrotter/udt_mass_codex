<a id="r8acp"></a>

#### First astronomical comparison — ACP1

Charles authorized construction and audit of OEV1's first astronomical
comparison. **CGCG 074-064 now has an explicit conditional metric-to-data
comparison. No astronomical metric has been selected, fitted or validated.**
The source was chosen because MCP XI exposes its spot schema, source equations
and likelihood, not because its measurements match a UDT curve. Published
outcomes are exposed. The [contract](udt_first_astronomical_comparison_2026-10-04/COMPARISON_CONTRACT.json)
and [premise ledger](udt_first_astronomical_comparison_2026-10-04/PREMISE_LEDGER.tsv)
state the actual objects and open inputs.

**One geometry must predict the records together.** Supply one regular
time-oriented Lorentz metric, actual maser/receiver proper-clock histories,
receiver tetrad, regular null incidences, source cadence and calibration,
feature association and observation-window reduction. The same metric supplies
the connection, endpoint frequencies and sky map. Source histories are query
data; a conventional disk prescription must be consistently realized or justified
as a controlled approximation in that geometry. A separate fitted Z(D) profile
cannot substitute for these predictions.

For each actual maser signal, R6 gives Z=omega_e/omega_o=d tau_o/d tau_e.
With a supplied spectral readout alpha=nu_e/nu_ref, the optical channel and
its receiver-time derivative obey

    v_opt=c_E (Z/alpha-1),
    d v_opt/d tau_o=c_E [Z'/(alpha Z)-alpha'/alpha^2],

where primes are emitter proper-time derivatives. Stable alpha=1 gives
c_E d(log Z)/d tau_e. This is a received spectral slope, not automatically
a local proper acceleration. MCP XI fits finite monitoring windows (nine
consecutive epochs with its selection/binning procedure); a pointwise derivative
does not replay that estimator. A candidate must predict the reduced records
using the relevant feature, epoch and channel information.

If a justified matched factorization has Z=Z0 Q, stable source cadence gives
c_E[(log Z0)'+(log Q)']. For constant Z0 only, this is c_E Q'/Q: the common
factor cancels between optical-velocity scaling and reception-time scaling.
It remains in the spectral offset and received intervals. A varying Z0 retains
its derivative, and different spot rays need not share it. The identity
Q=Z/Z0 by itself creates no physical decomposition. MCP XI already multiplies
source Doppler, gravitational and systemic factors before defining optical
v=c_E z; adding a standalone 1/(1+z0) slowdown would require a new justification.
This observation does not certify every Newtonian/source-time approximation in
that published model or establish a defect in unavailable code.

**The angular constraint is a full map.** In the reception tetrad,
n_sky^a=-g(k_o,E_a)/omega_o, opposite future propagation. Actual incidence and
the calibrated sky chart give the finite spot positions. For a regular
infinitesimal source cut, fix G348's reverse block B_eo using the same future
affine k and fixed orthonormal quotient-screen bases. Then

    J=-omega_o B_eo,       D_A^2=|det J|=omega_o^2 |det B_eo|.

A screen-basis change must also transform the source coordinates. Positive
affine rescaling leaves J and D_A unchanged. Changing the physical receiver
with frequency multiplier F changes Z to Z/F and D_A to F D_A; frame labels
and astrometric calibration cannot be mixed silently.

The scalar D reproduces all linear source lengths up to orthogonal orientation
only if J^T J=D^2 I. Equal area is weaker: D I and D diag(2,1/2) have equal
determinants but different spot maps. MCP XI's angular-radius conversion rD
therefore carries a source-compatible scalar-map approximation; its D posterior
is not automatically portable to arbitrary sheared geometries. A general
candidate needs the full map or a justified source refit. For a smooth inverse
angular map with Hessian norm bounded by M on a convex regular patch, the linear
remainder is at most M|delta theta|^2/2. The small apparent disk size alone does
not bound M or exclude focusing/branch changes.

**The source likelihood remains conditional.** MCP XI supplies spot positions,
optical barycentric channel values and monitored spectral slopes. Its B17–B24
likelihood uses the squared residual and Gaussian normalization for each
declared positive variance: positional/acceleration measurement variances plus
error floors, and separate systemic/high-velocity spectral floors. Only
acceleration flag 1 contributes as a measurement; flag 0 is modeled. This
factorization is an imported statistical comparison, not a theorem of source
independence. Priors and floor sensitivity matter for posterior use. Full
spot-level data and its fitted summaries are alternative uses of the same
observations, not independent likelihood factors.

The complete machine-readable spot table and full estimator metadata were not
retrieved within the bounded attempts. No full source replay or fit was done.
The printed six-row illustration is not the complete dataset. A source count
narrative inconsistency is recorded without treating it as proof that the
published distance is wrong or inventing missing rows.

**A concrete summary restriction survives.** Under the published compatible
source/scalar-map reduction, the CGCG row has D=87.6 Mpc with printed marginal
statistical interval [80.4,95.5] and optical CMB v0=7172.2 +/-1.9 km/s. The
observed unit conversion yields Z_summary=1.0239238840. With omega_o=1 the
conditional area median is 7673.76 Mpc^2 and the transformed marginal endpoints
are [6464.16,9120.25]. MCP XI separately reports model-choice systematics
1.5 Mpc and 1.7 km/s; they remain separate and are not folded into a fabricated
joint or total confidence interval. XI/XIII reuse the same underlying source.

The transformed parameters Phi_summary=-log Z_summary=-0.0236421919 and
chi_summary=tanh(Phi_summary)=-0.0236377879 are initially source-summary labels.
Their identification with an actual R6 clock leg additionally requires a
regular reference clock/history, null branch and source-reduction realization.
The fitted systemic parameter does not supply an emitting clock at the SMBH
center. No full native phi_pair assignment, recession velocity, initial proper
separation, physical scale or X_max follows from these transformations.
Each printed interval remains marginal; membership is descriptive, not a joint
confidence test or model rejection rule.

This construction adds two usable restrictions to OEV1: the actual angular map
must be checked before importing a scalar distance, and the spectral slope must
use the same clock correspondence as the frequency. R6/R7/R13 provide the
geometric derivation; the disk/transition/calibration/statistics remain supplied
source hypotheses. Native geometry selection is still open. A subsequent test
needs a candidate metric with consistent source histories and the actual data
reduction, rather than another independent response profile.

The [initial candidate](udt_first_astronomical_comparison_2026-10-04/INITIAL_CANDIDATE.md)
and controlling [precision repair](udt_first_astronomical_comparison_2026-10-04/REPAIR.md)
retain sign, reference-clock, estimator and uncertainty corrections. Exact
symbolic and distinct high-precision checks support the bounded identities and
summary arithmetic; they are not an empirical test. The initial checker’s output
write failure is preserved and repaired. Two actual fresh reviewer contexts
own source-first, exposed and final scoped review; no human/different-model,
native metric admission, full-corpus reproof or observational confirmation is
claimed. R18 owns the current return and next action.
