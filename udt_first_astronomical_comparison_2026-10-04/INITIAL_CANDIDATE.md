# ACP1 initial candidate — CGCG 074-064 as an actual metric comparison

Mathematical construction, conditional and unreviewed at this freeze. This is
one concrete **comparison**, not a selected astronomical metric or a fit. All
published outcomes are exposed. It develops R6/R7/R13 and OEV1; it does not
adopt the source disk model as UDT or import an expansion/field equation.

## 1. Actual object, data and candidate contract

Choose CGCG 074-064 because MCP XI publishes its disk/readout equations,
individual-spot schema and likelihood, already audited by OEV1. The target is
the disk as observed from Earth. No hypothetical pair of parallel-prepared free
clocks or initial proper separation is substituted for those source histories.

A candidate comparison package supplies one smooth time-oriented Lorentz metric
g on the relevant source/observer/ray neighborhoods; regular future timelike
maser histories gamma_j; a receiver history gamma_o and its astrometric tetrad;
actual smooth null incidence branches; source transition/cadence histories;
the source/reference/epoch calibration; and a declared statistical model.
The same g supplies the clocks, connection, rays, frequency ratios and angular
map. These are legitimate conditional query inputs. Their native selection or
realization is a separate open question. An imported Kepler/Schwarzschild source
prescription has to be realized consistently with that g, not added after an
incompatible metric calculation.

For each identified emitting feature and reception epoch, solve the actual
source-to-receiver incidence, holding the histories fixed when varying emission
time. Supply the feature association and reference epoch; a catalog channel is
not by itself a persistent identified emitter. The published finite-width,
time-averaged and fitted records need the same reduction operation applied to
the candidate's ideal history. No instantaneous prediction is silently compared
with a fitted two-year slope.

The spot data schema is (type,v_opt,x,sigma_x,y,sigma_y,a_opt,sigma_a,flag).
Flux and its uncertainty help source selection but no flux/luminosity law is
needed for the comparison here. The velocity is an optical barycentric channel
coordinate; it is not a physical velocity magnitude. Acceleration flag 1 denotes
a measured spectral slope; flag 0 is a model result and is excluded from the
acceleration measurement likelihood. No full raw-spectrum reanalysis is claimed.

## 2. Spectral and arrival prediction from the same geometry

Use c_E=1 in geometric unit-clock formulas; restore its observed clock/ruler
calibration in the reported optical-velocity units. For future affine k,

    omega_i = -g(k_i,u_i) > 0,
    Z_j = omega_e/omega_o = d tau_o/d tau_e.

R6 establishes this on a regular family. A constant positive affine rescaling
changes both omegas equally and leaves Z unchanged. Emission/receiver histories
and branch are part of the observable, not nuisances selected by the kernel.

Supply the conventional spectral readout alpha_j(tau_e)=nu_e/nu_ref>0. Then

    nu_o = nu_e/Z_j,
    v_opt,j = c_E (Z_j/alpha_j - 1).                       (1)

This identifies a stable line or supplied varying source cadence with the R6
clock record. It is a conditional source/detector bridge, not a derived UDT
theory of light, water molecules, energy or line formation. Ordinary local
physics does not make the astronomical source history known without observation.

Receiver-frame changes must be applied to the endpoint clock/direction and
calibration together. At the same event replacing u_o by v_o with
F=omega(v_o)/omega(u_o)>0 gives Z_new=Z_old/F. The associated infinitesimal
solid angle changes by F^-2 and D_A changes by F (R13/G348). A source-reported
optical barycentric-to-CMB offset is that source's reduction convention, not a
native preferred observer or a universal scalar correction for every ray.

Differentiation of (1) on the actual correspondence gives

    d v_opt/d tau_o
      = c_E [(dZ/d tau_e)/(alpha Z) - (d alpha/d tau_e)/alpha^2].       (2)

For a stable line alpha=1 this is c_E d(log Z)/d tau_e. It is not a local
four-acceleration or automatically the Newtonian source acceleration. A monitored
finite-window slope must use the candidate's actual reduction/time coordinates.
Unmodeled line evolution can imitate a geometric spectral drift.

## 3. A useful cancellation; no additional slowdown factor

If a separately justified matched comparison lets Z=Z0 Q_j, with Q_j expressed
on the same emitter-time parameter, (2) gives exactly for a stable line

    a_opt = c_E [d(log Z0)/d tau_e + d(log Q_j)/d tau_e].               (3)

If Z0 is constant on that window, a_opt=c_E Q'_j/Q_j. A fixed external redshift
factor cancels between the optical-velocity scale and the received-time scale.
It does not disappear from the spectral offset or the arrival intervals.
This is algebraic composition of the same clock correspondence, not deletion
of source motion or an assumption that a physical geometry splits into effects.
If Z0 varies, its logarithmic derivative remains. Distinct rays need not share
Z0; defining Q=Z/Z0 as an identity gives no new physical predictive factorization.

MCP XI A15 already multiplies source Doppler, Schwarzschild and systemic factors;
A16 uses optical v=c_E z. Its A6/A7 projected disk acceleration is a conventional
source model. An extra standalone factor 1/(1+z0) cannot be appended to that
pipeline merely because clocks are dilated. Full consistency still requires its
source approximation, proper/coordinate-time convention and finite estimator;
(3) is not an exact validation of every source approximation in MCP XI.

## 4. Angular prediction needs a map, not only an area

In the reception tetrad the direction toward the source is

    n_sky^a = -g(k_o,E_a)/omega_o,  a=1,2,3.

It is opposite to future propagation. Predict the calibrated sky chart and
relative spot/reference positions using the actual ray endpoints. This exact
procedure makes no small-disk approximation and includes any branch/parity
information present in the supplied metric.

For a specified regular infinitesimal source cut and central ray, let B_eo be
the observer-to-source position-from-momentum Jacobi block in orthonormal
quotient screens. With a compatible sky-angle orientation, the differential
map is J=omega_o B_eo (an overall sign can be absorbed by the stated screen
orientation). The geometric angular-area distance is

    D_A^2 = |det J| = omega_o^2 |det B_eo|.                         (4)

Under k->a k, B->B/a, so J and D_A are invariant. This is angular-area geometry,
not a luminosity or physical-content law. The source disk projection must use
the corresponding source cut/screen and source metric lengths.

One scalar D supplies the full linear sky-to-source length map, up to an
orthogonal orientation/parity, only if

    J^T J = D^2 I.                                                 (5)

This is the similarity condition, stronger than |det J|=D^2. For example J1=D I
and J2=D diag(2,1/2) have the same area distance but send a given angular offset
to different physical disk positions. This linear-algebra example is not a
claim that two such maps are selected native UDT geometries. It proves that a
determinant alone does not identify the required matrix data.

MCP XI converts angular disk radius r into rD and fits orientation/warping in
Euclidean source geometry. Transplanting its scalar D posterior into a general
metric therefore requires the published scalar-map approximation or a source
refit using the actual map. A shear can also be degenerate with source disk
parameters; a determinant comparison cannot resolve that by assertion.

For an actual smooth inverse angular map rho(theta) on a convex regular patch,
if ||D^2 rho||<=M, the first-order error is at most M||delta theta||^2/2.
The relevant source cut, absence of branch switches and that bound must be
established for a candidate. A small observed angular disk by itself does not
bound M near focusing. No uncontrolled finite-patch equality is used here.

## 5. Concrete statistical comparison

The primary comparison is a joint forward prediction of the published spot
positions, spectral-channel coordinates and measured spectral slopes. Let
X_j,Y_j,V_j,A_j be the candidate histories after the declared observation
reduction. As an explicitly imported baseline, MCP XI B17–B24 specifies

    -2 log L = sum_j [(x_j-X_j)^2/s_xj^2 + log(2 pi s_xj^2)
                    +(y_j-Y_j)^2/s_yj^2 + log(2 pi s_yj^2)
                    +(v_j-V_j)^2/s_vj^2 + log(2 pi s_vj^2)]
             + sum_{flag_j=1} [(a_j-A_j)^2/s_aj^2 + log(2 pi s_aj^2)],       (6)

where s_xj^2=sigma_xj^2+sigma_x^2, similarly y,a, and s_vj is the fitted
systemic or high-velocity error floor. Variances must be positive. The separate
terms/conditional independence, features and error floors belong to this source
likelihood. They are not inferred from six marginal galaxy summaries and are
not a general covariance theorem. Its priors/sensitivity analysis would have
to accompany any posterior use. We do not choose floors or fit a posterior here.

A raw-data or summary likelihood is an alternative use of the same data, not
two independent tests. The source's fitted D and z0 cannot be multiplied into
(6) as new independent observations. Reconstructing a likelihood from posterior
samples also requires the original priors and sampling/normalization information.

## 6. The actual CGCG summary restriction, at its retained scope

For the source-compatible scalar-map reduction, MCP XIII Table 1 gives D=87.6
Mpc with marginal interval [80.4,95.5], and optical CMB v0=7172.2 +/-1.9 km/s.
With the observed convention c_E=299792.458 km/s, this is Z0=1+v0/c_E.
The same actual g/query must predict its source-reduced Z0 and (4), with the
conventional source nuisance treatment retained. It is not enough to append
Z0(D) as a separate profile to a kernel evaluation.

Under the matched R6 clock-leg identification, Phi_clock=-log Z0 and
chi_clock=tanh(Phi_clock). These conditional numbers are neither the entire
native phi_pair assignment nor a recession speed. The CMB reduction and source
systemic inference must be matched before applying this clock interpretation.
In the omega_o=1 affine convention, the area constraint is |det B_eo|=D_A^2.
It constrains one supplied null comparison's angular area, not an initial proper
separation, X_max, endpoint wall, or an independent physical scale law.

Each published interval is marginal. Evaluating whether an assigned prediction
lies within either interval is descriptive only; it is not a simultaneous
confidence region, likelihood ratio, model rejection threshold or confirmation.
The 263.3 km/s conversion from MCP XI gives its barycentric center 6908.9;
its asymmetric/error/systematic details cannot be replaced by MCP XIII's rounded
summary. The two summaries are not independent measurements.

## 7. What this constructs and what remains open

The comparison is now an explicit observer/source/null forward map, its local
angular reduction, a source-owned conditional likelihood and one actual
astronomical endpoint restriction. Its principal additions to OEV1 are the
full-map requirement and the correct optical-slope time conversion. No candidate
metric has been fitted, ruled out or accepted as native. This is not a claim
that the already-open native field equation is newly missing.

An actual native or explicitly conditional candidate still has to provide a
metric and consistent source histories that predict these records. If source
disk/observer/calibration assumptions are altered, its published D posterior
is not automatically portable. Source-reduced summaries can be used only at
their matching scope; the full forward map supplies the route for a refit.
This narrows the required physical connection without proving that all current
UDT commitments are insufficient or that a new physical postulate is needed.

## 8. Exclusions and evidence ownership

No chosen redshift-distance curve, FLRW/Einstein evolution, H0/flow subtraction,
new force/coupling, homogeneous universe, preferred observer, source luminosity,
universal onset, physical X_max or native light/matter model is supplied.
No protected/parked data is opened. Source PDFs and the MCP model remain fixed.
The initial candidate precedes finite numerical checking and exposed review;
source-first reviewer suggestions are disclosed separately. Fixed arithmetic
and matrix controls test the construction's formulas, not a UDT universe.
