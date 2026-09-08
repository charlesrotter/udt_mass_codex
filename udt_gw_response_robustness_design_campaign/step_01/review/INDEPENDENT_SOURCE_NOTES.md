# Independent source and analytic notes before target exposure

2026-09-08 00:33 UTC. Follows immutable SOURCE_FIRST_SEAL. No RD1 parent
candidate/proof/code/output has been opened. These are reviewer reconstructions
and finite anchors, not a verdict on the target or an instrument certificate.

## Full-operator null and stability

For bounded A0:U->Y between Hilbert spaces, a bounded N:Y->Z with NA0=0
annihilates closure(range(A0)). Such a nonzero scalar functional exists iff
that closed range is a proper subspace (orthogonal projection supplies it).
Its size and number are properties of the full map, not the count of names
assigned to infinitely many input and output degrees of freedom.

A pointwise measurable F:B->C^(3x2) with rank2 a.e. and a measurable unit null
q(f) gives the multiplication null q(f)^dagger on L2(B)^3; its norm is1.
Stable recovery of both waveforms holds when essinf sigma_min(F)>0.
For F(f)=[[1,0],[0,f],[0,0]], f in(0,1), rank2 holds everywhere in domain.
Let h_a(f)=(0,a^(-1/2)1_(0,a)(f)); its norm is1, while ||F h_a||=a/sqrt(3)
tends to zero. Thus no positive uniform recovery constant follows from a.e.
rank. A compact band and continuous full rank at every point WOULD give
a positive minimum; neither compactness nor positivity may be omitted.

For y=(A0+E)h+e, bounded ||E||<=epsilon and ||A0h||>=gamma||h|| imply
||y||+||e|| >= (gamma-epsilon)||h||. When gamma>epsilon this proves the
sealed data-dependent amplitude inequality under the null hypothesis.
The projection r=Ny follows by applying N and the triangle inequality.
These are norm proofs, not conclusions extrapolated from80 finite checks.

If N has a nominal defect NA0, it belongs in the same leakage operator.
A known image-preserving E=A0K has zero null leakage, whether K is a common
scalar or a more general waveform-domain transformation. An unknown error
component whose image is not annihilated by N leaks proportionally to h.
For a nonzero NE choose h0 with NEh0!=0; h=Mh0 gives unbounded mathematical
leakage as M increases. A qualitative weak-wave regime does not itself supply
a useful numerical H at a stated strain sensitivity. This scaling separator
does not assert arbitrarily large physical weak perturbations.

Possible data-dependent upstream cleaning need not be a fixed linear E.
The abstract theorem applies only after that relation is supplied/justified;
alternatively an admitted uniform bound on the nonlinear residual over the
waveform class can be propagated directly. No processing linearity is
derived from metric geometry.

## Source correspondence

T2100313v3 calibration README was read in full from
/tmp/udt-complementary-wave-sources-C72KZ2/calibration_README.txt,
SHAfb4650601da797badc8bf9e068f798788842667a5bc27ae035ae5ffd0d311d7e.
It specifies true/model complex response estimates, hourly discrete LIGO
records, one Virgo O2 run file, medians and pointwise +/-1sigma boundaries.
It does not provide a hard full-band/full-time uncertainty set or complete
joint covariance. If r=R_true/R_model and released data use R_model,
the signal ratio released/true is1/r. If |r-1|<=rho<1 then
|1/r-1|<=rho/(1-rho). That latter hypothesis is a conditional bound, not
a reinterpretation of the marginal table as deterministic evidence.

Cached noise-subtraction text, arXiv1809.05348v2:
 /tmp/udt-gw170817-fixed-window-xshnIR/noise_subtraction.txt,
SHAab7cab0c255f4fd8a30d462fb0277e44d21bbbaf66dda45a1e7ae9a155ace750.
Read sections2 and4 including sensor safety, injections, finite calibration
lines, transient gating and narrow spurious-correlation caveats. Transfer
coefficients are estimated from witness/strain cross spectra in windows.
These documented finite checks support intended use but do not constitute a
uniform error theorem for every admitted arbitrary waveform or its upstream
processing. No previous strain arrays or raw supports were opened.

Official LALDetectors_gitlab.h cache SHA
82ac49e8042d4eab0f890e63e3599ae227967aee16c76cd5f6b6b729c8798684
was inspected at H1/L1/V1 arm/vertex constants. These are supplied published
geometry decimals, not exact2017 calibration or metrology.

Official source files newly fetched by parent were inspected ONLY as primary
response definitions, before candidate exposure:
 /tmp/udt-gw-response-docs-L3JgrF/DetResponse.c,
SHA2e1d5db56170607e655a866165905b5867d537200e90dceb77c81f8832259a40;
 /tmp/udt-gw-response-docs-L3JgrF/LALSimulation.c,
SHAa10f73a39029b86d4de7c46c11ad269b0ee17a9499dce52b9b42a0bbeb1cb619.
Read DetResponse lines178–330 and relevant LALSimulation response/interpolation/
segment routines. The arm function comment says beta=pi*f*L/c, but the
actual caller supplies beta=f*L/c and the function forms x=pi*beta.
Caller plus normalized sinc fixes the implementation convention; no extra
factor pi is inserted. This is a source-comment inconsistency, not a claim
that the deployed instrument has a calibration error. Mean-arm approximation,
static segment response, finite interpolation and rotation-update qualifications
remain. Present source code is not proof of the2017 release transfer.

## Independent arm integral and checks

Put x=pi*f*L/c and mu=k.u in[-1,1]. The source expression is
T=1/2 [exp(ix(1-mu))*sinc(x(1+mu))
       + exp(-ix(1+mu))*sinc(x(1-mu))],
with sinc(z)=sin(z)/z continued at0.
Writing each sinc as one half the integral of exp(iz s), s in[-1,1],
expresses T as the equally weighted mean of unit complex factors exp(i x V),
where V is uniform on each of [-2mu,2] and [-2,-2mu], with degenerate
endpoints interpreted by the continuous limit. Hence |T|<=1, |V|<=2,
E V=-mu and E V^2=(4/3)(1+mu^2). The Taylor remainder
|exp(iv)-1-iv|<=v^2/2 yields
|T-1| <= min(2,2|x|,|x mu|+(2/3)x^2(1+mu^2)).
These statements follow from the integral and have all-real-x quantifiers,
not from sampled frequencies. At mu=0, T=sinc(2x) exactly. This derives a
bound for the supplied arm response expression only, not complete detector
calibration or full time-varying/finite-window response.

independent_arm_integral.py independently evaluates the integral by Simpson
quadrature at128/256 subintervals and compares25 declared(x,mu) points.
Maximum256-point error1.12422e-9; finite quadrature tolerance1e-7 (no claimed
uniform numerical certificate). Direct analytic source-expression limit/
magnitude/bound checks pass at those points. At500Hz,L4000m,mu0.6 the correct
source value is0.9996017789704585-0.01257256622271169i. Wrong extra-pi input
changes it by0.027086425630295428, resolving the convention distinctly.

independent_definitions.py uses separately authored Fraction and scalar
complex code.80 finite stable-recovery cases pass; minimum amplitude-bound
slack0.0134566861, maximum projected-error-bound ratio0.947559727.
A varying response followed by common averaging gives exact incorrect null
[0,-1/2], while the correctly ordered pointwise null is zero. A kept Fourier
input bin of zero acquires output magnitude1 from an unretained input
amplitude8 after a window. Same covariance diagonals(1,1) permit contrast
variances0 and4. Three marginals with exact2/3 coverage can have simultaneous
coverage0. Invalid zero assertions were actually executed and caught.
These are finite method counterexamples, not mutations of unseen producer code.

Run records: independent_definitions_run and independent_arm_run, both exit0,
empty stderr/no timeout, Python3.10.12. Durations0.023715578s and0.023101556s;
maxRSS15168KiB and15320KiB;512MiB AS/60s CPU/wall via inspected common utility.
Explicit OPENBLAS/OMP/MKL single-thread environment was set in actual invocations.
No overlapping child, GPU, install, observed sample or source theorem-suite run.
Hashes of code/stdout are preserved in this directory and eventual manifest.

