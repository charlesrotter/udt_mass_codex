# OB1 — one stationary loop, retained metric information, and unused phase tests

Conditional candidate, UNPROMOTED; fresh review pending. WORK_ORDER.md and
FRAME_AND_DISCOVERY.md own scope, pre-computation exposure and restrictions. G405's accepted
ER1 argument/review is the source for the marked records, with G166 native assembly OPEN and
G176 completed reciprocity WORKING. Standard Sagnac/optics and elementary phasor algebra are
credited methods. The following supplied metrics are configurations, not selected native UDT
solutions. No Einstein equation, native Maxwell law, optical identification of chi, or physical
meaning for conditional c_eff is added.

## 1. Exact supplied geometry and one two-path setup

Use a smooth stationary metric on a neighborhood of a compact oriented closed spatial loop C:

    g = -N(x)^2 [dx0 + beta_i(x) dx^i]^2 + gamma_ij(x) dx^i dx^j,
    x0=c_E t, N>0, gamma SPD, U=N^-1 partial_x0.

All coordinates x0,x^i have length units in this convention; beta_i,N,gamma_ij are dimensionless.
The time coordinate need not extend globally beyond this neighborhood. Supply one single-valued
stationary chart covering C, an emitter/detector at a point D on C following U, the loop marking,
and gamma-N^2 beta beta^T SPD along C. This last sufficient restriction ensures positive coordinate
traversal in both directions; it is not a necessary general Sagnac theorem or native requirement.
The detector's proper time is d tau_D=N_D dx0/c_E, with N_D=N(D).

The two paths are C and its reverse, in the same stationary apparatus. An ideal null tangent obeys

    dx0 = -beta_i dx^i + (1/N) sqrt(gamma_ij dx^i dx^j).             (1)

The positive root is fixed by future orientation N(dx0+beta dx)>0. The square-root term is even
under path reversal, so the coordinate transit difference and proper detector delay are

    X_+ - X_- = -2 integral_C beta,
    D_g := T_+ - T_- = -2 N_D/c_E integral_C beta.                 (2)

Here X are coordinate lengths and T=N_D X/c_E are delays expressed on the detector clock.
This is an exact algebraic identity for the ideal prescribed null-path class. It does not prove
that an arbitrary curved C is a free null geodesic or a Maxwell boundary solution. The supplied
optical guide/reflection model must implement the same reciprocal path, coherent propagation and
phase transfer below. In a reciprocal medium, equality of local opposite-direction speeds gives
the analogous transit cancellation, but a pulse/group transit identity alone does NOT establish
a phase-delay law in a dispersive guide. This candidate makes no such extension.

Ruggiero–Tartaglia1411.0135v2 SecII, especially Eq11, supplies the standard same-path/equal-local-
speed precedent. In our convention g0i/g00=beta_i. We derive the proper factor directly from
g00=-N^2, namely sqrt(-g00)=N; the retrieved text of its Eq12 displays sqrt(g00), so it is not
copied as a sign authority. No other conclusions from that paper are imported.

Time relabeling x0'=x0+f(x) gives beta'=beta-df and leaves (2) invariant for single-valued f.
Positive constant time-coordinate rescaling x0'=a x0 gives N'=N/a,beta'=a beta and again leaves
N_D integral beta invariant. The physical source clock and loop must be carried. An arbitrary
new observer or new physical loop is a different query. Stokes' theorem can replace the line
integral by integral d beta only if C bounds an oriented surface in the regular chart/domain.
No simply connected topology, global exactness or curvature interpretation follows automatically.

## 2. Join to the retained reciprocal records, and its limits

G405's actual constant-direction surfaces F_(a,v)(x0,sigma)=(x0,a+sigma v) have

    h00=-N^2, h0sigma=-N^2 beta(v),
    hsigma_sigma=gamma(v,v)-N^2 beta(v)^2,
    det h=-N^2 gamma(v,v)<0.

Only after this full pullback, G176's working normalization gives

    T_v=N, m_v=N sqrt(gamma(v,v)), B_v=beta(v)/m_v,
    Phi_v=-log N, chi_v=tanh(Phi_v), beta(v)=m_v B_v.               (3)

The original common comparison clock is partial_x0, not unit U. The loop is an externally
supplied optical query through a common geometry; it is NOT a path inserted upstream of the
native scalar kernel. Values of the three axial marked full records on the entire loop, with
their original densities, recover beta_i=m_i B_i and N_D, hence (2). G405's six-direction
coherence/SPD conditions provide one sufficient common smooth metric realization; they are
not replaced by unrelated pair samples. Full fields on C, common labels and loop embedding are
supplied, not three isolated observations. Actual acquisition, arbitrary-network/gluing and
native physical pair population remain OPEN. No claim of minimal observational data is made.

One controlled witness within the same setup is

    N=1, gamma=dx^2+dy^2+dz^2, beta=kappa(x dy-y dx)/2,
    C(theta)=(R cos theta,R sin theta,0), 0<=theta<=2pi,
    R>0, |kappa|R/2<1, D_g=-2pi kappa R^2/c_E.                   (4)

Take a slightly larger neighborhood still satisfying the strict inequality. The coordinate
slice eigenvalues are1,1,1-kappa^2(x^2+y^2)/4. Direct roots along the oriented circle give
X_+=2pi R-pi kappa R^2 and X_-=2pi R+pi kappa R^2, both positive. Every marked directional
Phi_v and chi_v is zero for every kappa, yet delay changes with kappa. Thus these scalar outputs
alone do not determine the loop delay in this admitted supplied class. Full shift records do
distinguish it. This is a specific information-omission witness, not scalar-kernel failure or
the assertion that all normalized pair metrics agree. Fixing measured c_E selects neither
kappa (inverse length) nor R (length). Their appearance exposes the still-supplied shape/scale.

One loop gives one weighted circulation, not beta(x), spacetime curvature, a rotation source,
topology, metric uniqueness or a UDT-specific prediction. Exact gradients added to beta are
invisible; more general changes can also have zero integral on this particular C.

## 3. Imported phase transfer at one common detection event

Supply a coherent monochromatic source E_in(tau) proportional to exp(i omega tau), with omega
the detector/source PROPER angular frequency. For each direction assume an ideal stationary
delay transfer E_±(tau)=a_± exp(i[omega(tau-T_±)+b_±]), with nonzero coherent amplitudes and
relative phase accessible through a calibrated quadrature measurement. This transfer is a
conventional ideal optical input. Merely observing intensity proportional to cos phase would
not by itself give the signed unit phasor assumed here. Beam splitting, guide/mirror boundaries,
polarization, losses/visibility, quadrature sign and electronics need their own transfer audit.

Define comparator phase as arg E_- minus arg E_+. At the SAME reception event, subtraction gives

    Z(omega)=exp(i[omega D_g+b]), b=b_- - b_+.                     (5)

This compares different emission times reaching one receiver; it is not accumulation of k dx
along a null ray. Reversing comparator ordering conjugates Z and reverses all reported signs.
omega=2pi nu if ordinary frequency nu is used. The metric determines (2) only under the supplied
optical identification. Dolan1806.08617 describes the high-frequency vacuum wave approximation;
it neither supplies this finite guide nor derives electromagnetism from UDT. A real implementation
requires wavelength/geometry/boundary regimes and controlled approximation errors. No such bound
or qualified device is claimed. Equation(5) is exact for the declared ideal transfer model.

## 4. A concrete three-frequency protocol with two honest uses

Keep the SAME loop/geometry/source clock stationary over the sequence. Register in advance
omega_j=omega0+j d_omega, j=0,1,2, with d_omega>0 and all omega_j>0. These are supplied probe
frequencies, not theory-selected scales. Assume one frequency-independent residual phase b,
or independently correct a known frequency response and bound the remaining departures.
Do not infer constancy from the target readings. Use calibrated signed unit phasors Z_j.

**Use A: independently supplied geometry prediction.** If D_g is supplied from geometry/records
obtained independently of these target optical data, fit b using Z0 only. There remain genuine
unused predictions at j=1,2:

    Z_j/Z0 = exp(i j d_omega D_g).                                (6)

These constrain the JOINT supplied-geometry/optical-transfer/calibration model. A change in loop
circulation producing delay deltaD is invisible on these integer-spaced probes iff
d_omega deltaD is an integer multiple of2pi. A calibration from the same optical data cannot
be presented as an independent geometrical input. There is currently no certified acquisition
route for the G405 records in this study, so Use A is a conditional contract, not a ready test.

**Use B: no independent delay prediction.** Treat D as a free effective delay and use Z0,Z1 for
the two scalar phase parameters. Then the unique unused wrapped prediction at the third probe is

    Z2=Z1^2/Z0, equivalently W:=Z2 Z0/Z1^2=1.                     (7)

Proof: exponents cancel because omega2+omega0-2omega1=0 and1+1-2=0. Conversely every Z0,Z1 of
unit modulus has some (D,b) representation: choose any argument of Z1/Z0 for d_omega D and set
b from Z0. Different choices D'=D+2pi k/d_omega,b'=b-omega0*2pi k/d_omega, k integer, give ALL
the same integer-j readings. Thus D is identifiable only modulo2pi/d_omega, although Z2 is
unambiguously predicted. A prior independent interval of width strictly less than2pi/d_omega
can give at most one alias, conditional on consistency. No phase unwrapping is presumed.

For a comparison extra phase a j^2, W=exp(i2a); a=pi/4 is detected noiselessly, whereas a=pi
is invisible despite being non-affine as a real function. Arbitrary frequency-dependent offsets
b_j can fit every triple, destroying this test entirely. A frequency-linear extra delay d_inst
is also invisible to(7): only D_g+d_inst is inferred. Therefore a passing(7) alone constrains the
shared affine-frequency transfer/stationarity model; it supplies no independent metric value
and cannot distinguish UDT from conventional optics or other geometries producing that delay.
G407 motivates the calibration-versus-testing distinction, but this wrapped proof is separate.

## 5. Error support and empirical gates

Let actual frequency be omega_j+eta_j, |eta_j|<=v_j, and remaining phase error e_j satisfy
|e_j|<=u_j, with external bounds in rad/s and radians respectively. These e_j must include
all uncorrected guide/boundary/wave/phase-meter/clock and stationarity errors relevant to(5).
A constant b may be absorbed; a frequency-dependent unbounded bias may not. With fixed actual
delay D and an independent |D|<=D_max, the wrapped circular distance d_c(z,1)=|Arg z| obeys

    d_c(W,1) <= B := min(pi, u2+2u1+u0+D_max(v2+2v1+v0)).         (8)

The untruncated expression follows by the real triangle inequality before reduction modulo2pi;
the circle diameter supplies pi. Correlations need not be assumed absent. No probability law
or significance follows. Without a finite delay bound or controlled exact frequency spacing,
frequency errors cannot simply be assigned a delay-independent tolerance. B=pi is vacuous.
Training readings' errors enter the same expression and are not ignored.

For Use A, let the independent predicted delay be D0 with |D-D0|<=u_D and form
V_j=(Z_j/Z0)exp(-i j d_omega D0). Then

    d_c(V_j,1) <= min(pi, u_j+u0+j d_omega u_D
                         +(abs(D0)+u_D)(v_j+v0)), j=1,2.         (9)

Uncontrolled d_inst must either enter this independently justified delay uncertainty or the
phase errors; otherwise Use A is not eligible. A specified wrapped departure larger than twice
the untruncated null bound guarantees rejection under the same error bound for the alternative,
by the circle triangle inequality. Merely nonzero ideal response is not attainable sensitivity.
No numeric u,v,u_D, device sensitivity, experimental data, fit or empirical rejection is supplied.

Before any physical trial freeze geometry/provenance, guide/phase model, signed quadrature
readout, three frequencies/clock calibration, target-independent nuisance corrections, finite
error or covariance support, raw-data separation and exposure. Keep confirmation probes unused
and do not retune b/error law after them. An actual response/dataset eligibility dossier is the
next practical gate; this study neither opens target data nor dispatches that work.

## 6. Return and remaining science

The proposed bridge is useful at a precise conditional scope: the retained metric/record shift
can supply a loop phase prediction, scalar depth alone cannot, and one fixed phase experiment
has a clearly identified unused test and equally explicit calibration blind spaces. Most of
the optical identity is established conventional physics. The UDT contribution here is the
careful source/record join and its information boundary, not invention of the Sagnac effect.
Without independent geometric prediction and certified optical errors, the three-frequency
contrast is an interface-consistency test and no native UDT empirical constraint has been won.
It still identifies what extra evidence would make the bridge more informative.

No entire-universe completion is required for this conditional contract. Native metric assembly,
physical query selection, derivation/identification of light and matter, selected shape/scale,
G312 response-class membership and the broader nonlinear roadmap remain separate open work.
TI1/G413 and TI2/G414 keep their banked scopes; TI3 remains reviewed UNPROMOTED. This candidate
adds no accepted dependency or canon. Exact algebra, adverse controls, independent review and
final disposition are recorded separately; passing checks alone do not establish hypotheses.
