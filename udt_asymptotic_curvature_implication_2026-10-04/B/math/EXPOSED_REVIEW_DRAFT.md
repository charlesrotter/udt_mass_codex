# ACI1 exposed mathematical review — provisional pending frozen controls

This is a work-in-progress review, not the final verdict. The parent requested
that the scientific verdict wait for the frozen parent CPU control and the
supplemental cosh-product analytic control. No sibling argument was read.

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
of the parent's forthcoming code or a reuse of its output. Future null x motion
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

## Pending checks before final verdict

Inspect the parent's frozen control script, output, exact invocation/resource
capture and supplement, then bind the final review to their actual hashes.
No reviewer scientific CPU slot has run; analytic checks above used no numeric
sampling. No sibling argument, protected payload or external source was read.
No central file was edited. No empirical, human, different-model, formal-proof,
source-wide reproof or new premise-audit claim is made.
