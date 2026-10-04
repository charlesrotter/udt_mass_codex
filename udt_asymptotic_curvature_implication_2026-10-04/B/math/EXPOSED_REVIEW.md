# ACI1 exposed mathematical review

Verdict: VERIFIED-WITH-CAVEATS for the fixed candidate and supplement as
conditional mathematics. No required scientific repair identified. The requested
native physical implication remains UNCLOSED: comparison-family admission and
positional attribution are OPEN. No sibling argument was read. This review binds
the actual inputs recorded in EXPOSED_INPUT_PINS.json, including all three control
captures and the exact normalizer repair history.

## Candidate and exposure

Actual INITIAL_CANDIDATE SHA256:
aa57035504c19a42586d8266d863d7973d543b884872b6fd636d61e9f80e4859.
This file was guarded against protected paths, hashed, then read after this
reviewer's SOURCE_FIRST_SEAL. EXPOSED_INPUT_PINS.json records it and the exact
CCW sources newly inspected. SOURCE_FIRST_ARGUMENT and its seal remain fixed.

I am /root/aci_math, the same actual separate context that produced B/math's
source-first reconstruction; inherited Codex/GPT-6-family model. This exposed
review is not a new fresh context and not independent of that reconstruction.
No different-model claim is made. Old source verdicts and proofs were exposed.
The pre-seal route message reached the parent before the parent file freeze;
that departure is explicit in both the candidate and this reviewer's EXPOSURE.
The parent is not claimed to have an independent pre-review frozen derivation.
My own reconstruction preceded parent/sibling candidate exposure. Neither a
checksum nor the ordering of file timestamps repairs the disclosed exposure.

## 1. Transport proof checked directly

With F(0,t)=gamma and F(1,t)=beta, P_0=P_gamma, P_1=P_beta, so
H_1=P_gamma^{-1}P_beta agrees with the candidate's endpoint H. For a fixed
initial vector W=P_s(t)w, nabla_t W=0 and commuting the parameter derivatives
under the stated R convention gives

    nabla_t nabla_s W = R(F_t,F_s)W.

The fixed initial endpoint/vector removes the initial variation. Pullback to
p and integration yield the candidate's A_s=P_s(1)^{-1}partial_s P_s(1), with
R(F_t,F_s) in that order. There is no omitted final endpoint term because the
endpoint q is also fixed. H_s'=H_s A_s follows by direct differentiation.
Every pulled-back R(F_t,F_s)U lies in u-perp. This supplies the SAME positive
inner-product space for the integral's triangle inequality. Left multiplication
by H_s preserves the hyperboloid norm, so |d_s(H_su)|=|A_su|. Integrating this
speed gives rho(u,Hu)<=C. The relative-clock triangle split has the correct
orientation and yields |log Z|<=B+C without assuming commuting boosts.

Piecewise sweeps are valid as stated when "matching differentiable pieces"
means a finite piecewise C2 parameter subdivision with continuous transported
vectors and compatible s derivatives at seams; internal variation terms then
cancel. Arbitrary discontinuous or nonsmooth seams would not be covered. The
candidate already requires matching differentiable pieces, so this is an
explicit reading of the existing domain, not a new physical restriction.

## 2. Acceleration and area norm

For beta=c followed by the receiver worldline, pulling v(tau) back along that
worldline gives derivative equal to pulled-back proper acceleration. The
hyperboloid length bound gives B<=rho0+integral|a|. Source acceleration is absent
because c starts at the ACTUAL emission p and uses its ACTUAL u. A comparison
using a source preparation at an earlier event would need the corresponding
source-history term, as supplied in my source-first generalization. This is
not a defect in the candidate's narrower preparation statement.

j_U is positive definite and restricts to g on U-perp. L_U is a well-defined
linear map on bivectors by curvature antisymmetry. The operator-norm estimate
C<=integral K_U |T wedge S|_j follows pointwise without a factor ambiguity when
the domain norm is the standard j-induced exterior norm, as stated. Parametrized
area must count multiplicity; the candidate says so. Rank-zero/one pieces make
the bivector zero. Null nonzero bivectors need not vanish in this positive norm.
The proof therefore imports no positive Ad-invariant Lorentz-group norm.

C, K_U and area depend on transported U and on path/sweep choice. They are
coordinate/frame invariant for those data, not observer-independent local
curvature invariants. A separate derivation of a uniform bound on them must not
assume the desired bound on the endpoint rapidity; otherwise the application
would be circular. The candidate does not supply or silently assume that bound.

## 3. Initial analytic controls recomputed without a scientific program

Flat inertial receiver: t_o=(s+L)/(1-v), tau_o=t_o/gamma_v, so
Z=1/[gamma_v(1-v)]. For v=tanh rho0>0 this equals exp rho0.
The stated exact saturation follows; the control implicitly chooses the
receding signed-v branch when naming rho0 as a nonnegative rapidity.

Flat acceleration: t-x=(1-exp(-a tau))/a-L=s, hence
exp(-a tau)=1-a(s+L), Z=exp(a tau), and log Z=a tau.
The future reception domain includes tau>=0 and a positive logarithm argument.
The candidate expressly says to use its future reception domain. A fixed
pointwise a does not control growing accumulated acceleration.

For a=exp(Ht), b=exp(Hy), the nonzero original-coordinate connection entries are

    Gamma^t_xx=H a^2, Gamma^x_tx=Gamma^x_xt=H,
    Gamma^y_zz=-H b^2, Gamma^z_yz=Gamma^z_zy=H.

They give

    Ric_tt=-H^2, Ric_xx=H^2 a^2,
    Ric_yy=-H^2, Ric_zz=-H^2 b^2,
    R=0, Ric_ab Ric^ab=4H^4, R_abcd R^abcd=8H^4.

This is an independent analytic connection/curvature reconstruction, not a rerun
of the parent's code or a reuse of its output. Future null x motion
obeys dx/dt=exp(-Ht). Integrating and differentiating the actual clock incidence
gives the parent formula Z=1/(1-HL) at source s=0.

Along the t=0 preparation, the frame connection is H dx times the boost
generator. Parallel transport sends the source vector to rapidity -HL relative
to the comoving receiver, so the nonnegative mismatch is rho0=HL. Along the
null ray that boost parameter is -Ht_o. On the finite planar triangle, the
curvature generator sends every unit timelike U in the plane to a spatial unit
vector multiplied by H^2 times the signed Lorentz area density. Consequently

    C=integral_0^t_o H^2 exp(Ht)
        [L-(1-exp(-Ht))/H]dt
     =Ht_o-HL=log Z-rho0.

The area and C are nonnegative on 0<HL<1. The plane is totally geodesic for
this product CONTROL, while the main proof does not impose that restriction.
As HL->1, uniform preparation holds, every finite comparison is regular,
curvature scalars stay fixed and C grows through the longer surface/history.
No singular finite reception event is inferred.

## 4. RG statement checked at its actual source

Read CCW1 INITIAL_SYNTHESIS section1 and REVIEWED_RESULT directly and pinned
both. Its RG requires C3 g=x^-2 b with a regular nondegenerate b and nonzero
timelike dx at the spacelike endpoint. The source's contracted identity is

    R[g]=x^2 R[b]+6x Box_b x-12 b^-1(dx,dx)
         ->12 kappa>0.

That positive limiting scalar is necessary for precisely this endpoint class.
The candidate's R identically zero control cannot have such an RG endpoint
along the queried tail (indeed any proposed endpoint would face the same scalar
obstruction). This does not exclude less regular, null, degenerate or other
completion types, supply a topology or prove native UDT admission. The
candidate's statement retains the correct ceiling. Divergent redshift alone
therefore does not establish RG.

## 5. Quantifiers and physical ceiling

For each comparison inequality(5) holds for EVERY existing admissible sweep.
If preparations are uniformly bounded and log Z->infinity, each such C is
bounded below by log Z minus that common allowance. Hence every sequence of
admissible sweeps diverges, and the infimum over a nonempty permitted set does
too. Empty sweep sets are a domain failure. A large value on one inefficient
sweep does not establish a large shift or large minimal budget. Smooth compact
sweeps give finite quantities per comparison; uniformity across a noncompact
family is an additional hypothesis. Actual null-branch regularity and endpoint
incidence are still required for the clock formula.

The candidate clearly preserves R7's directional obstruction to any converse.
It selects no curvature sign. Its genuine mathematical increment is a finite
transport comparison bound, beyond the previous supplied endpoint-rapidity or
single-ray K descriptions and infinitesimal PSW expansion. It remains ordinary
conditional geometry. A physical UDT comparison family with the required
kinematic and sweep admission is not derived. Therefore the final account must
say this is a necessary test for a specified realization, not completion of
the requested native geometry selector.

My sealed source-first flat Milne-cylinder winding control also shows why the
sweep cannot be dropped: actual free-clock rays have Z=exp(mL), curvature zero
and preparation/acceleration zero, but different winding from the reference
path. The parent's explicit homotopy hypothesis already prevents this defect;
including the control is optional, not a required extension of the work order.

## 6. Supplemental cosh product independently checked

CONTROL_SUPPLEMENT SHA256:
f5b9072b51ba243a690af5904fdbd77573fa6efda2f65561a5ea5cd12a46f4c2.
The supplement explicitly attributes its initial cosh control idea to the
fidelity context. I did not read that sibling source note; this review therefore
has exposure to its attributed idea through the supplement, not a claim that
the idea is independent of the review process.

For a=cosh(Ht), the original-coordinate formulas generalize to
Gamma^t_xx=a a', Gamma^x_tx=a'/a and Ric_tt=-a''/a,
Ric_xx=a a''. Since a''=H^2 a, its Lorentz2 curvature is again H^2; the unchanged
spatial factor has curvature -H^2. The scalar and two quadratic contractions
are exactly the same as for the exponential product. At t=0, a=1 and a'=0.
Every connection coefficient entering the x-preparation geodesic and transport
of partial_t vanishes there, so proper preparation length L, rho0=0 and free
comoving clocks are correct.

Integrating dx/dt=1/a gives x_gamma(t)=atan(sinh(Ht))/H. Differentiating the
ACTUAL nearby-emission incidence integral on the fixed worldlines yields
Z=a(t_o)/a(s), hence at s=0

    t_o=asinh(tan(HL))/H,
    Z=cosh(Ht_o)=sec(HL),  0<HL<pi/2.

This derivative computation is an independent analytic check of the clock map;
it does not simply equate two definitions in the program. For the triangle,

    integral_0^t_o a''(t)[L-x_gamma(t)]dt
      =[a'(t)(L-x_gamma(t))]_0^t_o
          +integral_0^t_o a'(t)/a(t)dt
      =log cosh(Ht_o).

The first boundary term is zero at both ends, and the integrand is nonnegative.
In this Lorentz2 product plane R(T,S)U is its scalar boost coefficient times
the spatial unit orthogonal to U; therefore this is the theorem's C, not an
unrelated scalar contraction. C=log Z saturates the finite bound with zero
initial mismatch and zero acceleration. The conclusion is regular accumulated
curvature over an increasingly long triangle, not pointwise curvature blowup,
a finite-time endpoint, native admission or an empirical additional effect.
The scalar-zero RG exclusion remains at CCW's exact endpoint-class scope.

## 7. Parent code, preserved failures and actual captures

Read the original check_controls.py and both normalization wrappers, rather
than inferring their content from a pass receipt. The original program computes
Christoffels, curvature, Ricci and contractions from the supplied diagonal4D
metric, and checks the explicit tangent k=(1/a,1/a^2,0,0) against the original
null/affine-geodesic equations. Its curvature index order matches the candidate
convention. The diagonal inverse-metric contractions are appropriate for these
metrics; they would not be a general non-diagonal tensor routine.

The script also checks the derivative of a proposed triangle-integral primitive.
This is a useful independent residual for that primitive. Some other named
assertions, especially sharp_integrated_bound after defining C by the same
formula and arrival_vs_frequency after defining Z=a(T)/a(0), are algebraic
consistency checks, not independent scientific proofs. The general theorem is
supported by the analytic argument and review, not by a count of51 assertions.
The direct arrival derivative and boundary integral were checked analytically
above. No independent second scientific implementation was run by this reviewer.

Original execution failed at cosh.scalar_zero with numerator
sinh(2v)tanh(v)-cosh(2v)+1. For real v, cosh(v)>0,
sinh(2v)tanh(v)=2sinh(v)^2 and cosh(2v)-1=2sinh(v)^2, so this is exactly zero.
The first repair changed only normalization to hyperbolic expansion/exponential
rewrite, then failed at the positive perfect square

    sqrt(exp(4HT)+2exp(2HT)+1)=exp(2HT)+1.

The identity is valid because the radicand is (exp(2HT)+1)^2 and its base is
strictly positive for real H,T. The final wrapper first retains ordinary
simplify, then uses the same exact rewrite plus deep factorization only for
unresolved expressions. Inspection confirms fixed original-script SHA checks,
exact-one replacement guards, no force-branch rule, no numeric tolerance, no
change to metrics, curvature equations, ray data or expected quantities, and
continued exact-zero assertions. Two failed executions and one successful
execution are preserved; this is one bounded normalization-repair round with
multiple execution attempts, not a claim that only one process was run.

Actual final capture reports returncode0, 1.9364315860439092 seconds,
2,147,483,648-byte address-space ceiling, maxrss55344KiB, and no wall/CPU timeout.
Its stdout reports EXACT_CONTROLS_PASS,51 checks,2 metric families,
Python3.10.12/SymPy1.13.1; stderr is empty. The previous two captures report
returncode1 and preserve the actual exception expressions. I independently
recomputed stdout/stderr hashes against each capture, verified all frozen
source hashes against the read files, and checked51 unique named assertions in
EXACT_CONTROLS.json. CONTROL_ARTIFACT_CHECK.json records those BYTE/METADATA
checks. No reviewer scientific CPU control was used. The receipts do not record
the launching BLAS-thread environment, so this reviewer does not independently
attest that environment setting; this does not affect the analytic validity
or change the explicitly recorded2GiB/no-timeout settings.

## 8. Final decision and remaining scope

Accept the fixed initial candidate plus fixed supplement as a reviewed
conditional finite Lorentz4 transport estimate and exact supplied controls.
No substantive unresolved mathematical objection or required scientific repair
was found within this scope. The finite surface bound is a real strengthening
of the available estimate on supplied comparisons, while the attempted native
physical assignment remains unclosed. Headline those two facts separately.

The necessary condition concerns EVERY admitted sweep when such sweeps exist;
its budget is transported-frame/sweep-dependent. It gives no scalar-curvature
bound, pointwise singularity requirement, sign, direction, global source access,
topology, actual population, metric dynamics, X_max realization or universal
UDT selector. Large budget alone does not imply redshift. The control metrics
are off-equation supplied examples, not native-admitted alternatives.

No central file was edited by this reviewer. No sibling report, protected
payload or external source was read. No empirical, human, different-model,
formal-proof, source-wide reproof or new premise-audit claim is made. Parent
closure owns required regressions, full406, source/descendant bindings and final
integration review. This report itself does not approve later unseen central
bytes or scientific promotion. The original source-first argument, provisional
exposed draft, procedural exposure defect and failed control history remain
preserved.
