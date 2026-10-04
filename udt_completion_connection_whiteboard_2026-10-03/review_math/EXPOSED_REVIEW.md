# CCW1 exposed mathematical and fidelity review

Verdict: **VERIFIED-WITH-CAVEATS for the frozen conditional synthesis**.
No required mathematical repair found. This verdict accepts its bounded
connections, local existence witness and adverse controls; it does not adopt
RG, supply native physical attribution, or authorize recommendation B's execution.
Final integration/version attestation remains separate.

## Version, context and exposure

Reviewer `/root/ccw_review`, actual fresh context with inherited Codex GPT-6
model; no different-model, human specialist, proof assistant or independent-code
claim. SOURCE_FIRST.md and SOURCE_FIRST_SEAL.json preserve the prior unexposed
stage, sources and independently derived clock/curvature connection.

I read and independently hashed INITIAL_SYNTHESIS.md:
`1b300a65b544cbf63dacfb5a8a449cd4d638694ef62a25bb7bf38271888dea69`.
CANDIDATE_FREEZE.json is
`e60420c800ebbbd571255bf3296dce1405880866e04e9fd0146a7fa79d87c540`.
The actual candidate, CHECK_PLAN and check_controls.py bytes match that freeze.
I subsequently read all three contributor reports, the check plan/code, actual
saved stdout/stderr/receipt, exact CPW SUCCESSOR_SCOPE and FCL WORK_ORDER,
CROSS_MODEL_VERIFY, and central R9FST's conditional response scope. These are
exposed checks, not retroactively claimed blind findings. Source/control hashes
and exposure are preserved in EXPOSED_REVIEW_SEAL.json.

Parent startup/full406/normal/57-test evidence remains attributed, not rerun.
The first candidate-freeze metadata attempt's schema KeyError is disclosed;
the successful freeze binds the actual candidate/code. Checksums establish
correspondence, not independent chronology. No protected payload was inspected.
Only review_math files are written. No scientific program was run by me.

## 1. Curvature, signs and the invariant scale

Using f=-log x in the conformal connection, the derivative and quadratic
terms cancel the dx tensor dx contribution to Ricci in four dimensions.
Independent contraction gives exactly

    Ric[g]=Ric[b]+2x^-1 Hess_b x
             +(x^-1 Box_b x-3x^-2 q)b,
    R[g]=x^2 R[b]+6x Box_b x-12q.

The synthesis's convention and signs agree with its positive homogeneous
curvature control. C3 nondegenerate extension bounds the terms multiplied by x
or x^2 in the scalar expression. It does not make coordinate Ricci components
bounded; no such assertion is made. With the candidate's notation
kappa=-q(p)>0, the scalar limit is12kappa, and N_*=1/sqrt(kappa).
Regular positive conformal gauge weights cancel exactly at x=0. This is a
boundary invariant, with no reason here that it be constant across endpoints.

I recomputed every nonzero entry of the saved nonuniform-lapse Ricci control by
a different calculation from the parent's direct physical Christoffel loop.
For b=-N(y)^2 dx^2+d y^2+d z^2+d w^2, N=1+y^2,

    Ric[b]_xx=N N'', Ric[b]_yy=-N''/N,
    Hess_b(x)_xy=-N'/N, Box_b x=0, q=-1/N^2.

The resulting physical entries are

    Ric[g]_xx=2N-3/x^2,
    Ric[g]_xy=-4y/(xN),
    Ric[g]_yy=-2/N+3/(x^2 N^2),
    Ric[g]_zz=Ric[g]_ww=3/(x^2 N^2).

All other entries vanish except symmetric xy. These equal the saved direct
entries. Their contraction gives R=12/N^2-4x^2/N. At the negative-control
point x=1/2,y=1/3, omitting the leading term leaves residual243/25, so the
reported omission is detected. This independent hand calculation shares the
derived conformal identity, but not the parent's Christoffel implementation.

## 2. Actual emitter-gap residue and scalar readout

The exact chain rule ds/dx=(1/Z)(dtau/dx)=-NB/gamma has the correct sign.
The supplied finite interior emission limit justifies integrating from0 to x;
continuity gives epsilon/x->N_*B_*. Thus epsilon Z->N_* without any
derivative-of-remainder assumption. FCL's finite additive logarithmic remainder
then supplies both the finite positive exponential amplitude and log-rate limit.
The elementary conversion log(epsilon)=log(x)+log(N_*B_*)+o(1) is sufficient.

The tanh identity gives 1+chi_clock=2/(1+Z^2); with
Z exp(-sqrt(kappa)tau)->A, equation(4)'s limit is2/A^2. The sign is correct:
divergent received slowing gives Phi_clock->-infinity and chi_clock->-1.
This is the already typed matched clock leg, not the full projective relation.
The source-first stage independently obtained these facts with a differently
named positive square-root scale; the candidate's kappa is its square.

For the saved actual comoving clocks, s=-log(1+x),tau=-log x,
direct derivative division yields Z=(1+x)/x. Since log(1+x)/x->1,
(-s)Z->1 and log Z/tau->1. These are genuine proper-clock quantities.
Neither this control nor the general result proves a finite-data asymptote,
global last-emission horizon, distance relation, or d(log Z)/dtau limit.

## 3. Local signal construction and finite differentiability

The explicit C3 Lorentz extension assumption resolves the possible one-sided
extension gap. In that extension the geodesic spray is C2, so its local flow,
exponential map and local inverse have C2 endpoint dependence. The local world
function has at least the needed C2 regularity. A convex normal neighborhood
provides unique local segments; it is not a statement about global caustics.

For affine span1 on the short future null segment, the endpoint variation is
d sigma=-b(kbar_e,d e)+b(kbar_o,d q). Consequently

    F_s=-b(kbar_e,u_e)=E_*>0,
    F_x=b(kbar_o,-N_* n_p)=N_*B0>0,
    s'(0)=-N_*B0/E_*<0.

The implicit-function theorem therefore applies. FCL's receiver endpoint
estimate supplies r'(0)=-N_*n_p. The x coordinate is temporal in a small collar;
the chosen future segments between interior emissions and late receptions stay
on the physical side. The construction does not require a physical exterior.

Normalization is exact: with k=x^2 kbar and physical unit emitter u_e,
-g(k_e,u_e)=-b(kbar_e,u_e). No extra x_e is missing; it is already contained
in the physical emitter tangent. Dividing the whole ray by E preserves a
finite nonzero limiting tangent, with B_*=B0/E_*.

**Regularity precision retained at integration:** C2 ray variation is needed
at regular interior receptions for R6. The receiver is only proved C1 at x=0;
continuous endpoint tangents and the displayed first derivative suffice for
the endpoint limit. No C2 extension of r(x), nor of the emitter-parametrized
restricted family at the boundary, has been proved or is needed. The candidate
distinguishes these roles and does not claim that extra differentiability.

Quantifier checked: one may choose an emitter on p's local past null cone for
each already supplied receiver endpoint. This does not establish access from
an independently prescribed remote source, existence of the receiver, a preferred
population, or an echo. In the stated unavailable-source control, future direct
incidence would give x_o=x_e-2<0 for x_e in[0.9,1.1]; no hidden caustic issue
is needed for that failure. No required repair to the local lemma found.

## 4. Stronger same-tail beta2 obstruction

For Omega=z^2,z=1-h eta, the geometric identity gives
R=12(2hz)^2-6z^2(2h^2)=36h^2z^2->0. Any RG representation making that SAME
physical tail converge to a stated spacelike regular endpoint would instead
force a strictly positive scalar limit. Scalar invariance makes this a genuine
same-tail obstruction beyond regular positive gauge changes.

It is not a classification of all ends/extensions and does not rule out null,
degenerate or less regular completions. The historical FCW proof remains intact;
the new bounded obstruction has its own proof and scope. The explicit proper-
time integrals epsilon=integral_0^r (v+d)^(-beta)dv/h give exactly the displayed
beta1 and beta2 formulas. Both have divergent Z, while only beta1 has the stated
finite clock-gap residue. These are supplied controls, not complete UDT models.

## 5. The adverse receiver-population control is genuinely geodesic

I checked the geodesic with P CONSTANT, before substituting any population label.
For g=x^-2 eta, gamma=sqrt(1+P^2x^2), u=(-x gamma,Px^2,0,0),
the x acceleration terms are x+2P^2x^3 and -x-2P^2x^3; the y terms are
-2Px^2gamma and +2Px^2gamma. They cancel, and g(u,u)=-1. The ray
k=x^2(-1,1,0,0) is independently null and affine by the same direct check.

Only then put P_a=(1-a^-2)/2 at event q_a=(a,1-a). One has
P_a a=(a-a^-1)/2 and gamma_a=(a+a^-1)/2, so
omega_o=a(gamma_a-P_a a)=1. Source normalization at (1,0) is1.
The three saved cases give P=-3/2,-15/2,-63/2 and gamma=5/4,17/8,65/16;
all independently give received frequency1.

Integrating dy/dx=-Px/sqrt(1+P^2x^2) gives the contributor's finite-position
formula and bounded initial positions tending to2. Every fixed P worldline has
a finite endpoint and T->(-1,0,0,0). The initial boosts are unbounded across
the family, exactly the missing uniform preparation bound.

Independent actual-map differentiation, with x_e=x+y(x), gives
Z=x_e/[x(gamma-Px)] and evaluates to1 at each q_a. Thus this is not an
arbitrary tangent or accelerated-curve counterexample. It defeats only the
unrestricted exchange of individual and population limits. Common compact
collar bounds and bounded initial momentum make FCL's displayed estimate
uniform; bounded positive normalized ray data are also required to control B.
No distance law follows until the actual incidence and operational preparation
are derived. Candidate B keeps that work as a proposal.

## 6. Meaning, attribution and preserved source scopes

No Ricci response identification, Einstein equation, new light law, distance
definition, preferred center or X_max assignment enters these computations.
R9FST is retained within its existing local natural symmetric-response sector;
the synthesis does not extend it to all native constraints. Its historical
proof was not independently replayed here.

Matched identical metric/query data give D_pos=0 by the existing observable
definition. Matching two emitter gaps is an additional experimental hypothesis;
under that hypothesis their residue ratio gives the stated limiting logarithmic
contrast. Equal residues can still permit different interior records. Neither
a pass of the necessary RG diagnostic nor a nonzero matched contrast alone
establishes a native positional contribution. Inverse-map reciprocity still
does not identify two different future routes.

The scientific survivor is substantial and conditional: an invariant clock/
curvature relation, an arranged local regular emitter family, a stronger bounded
beta2 obstruction, and a concrete free-receiver quantifier control. Admission
and attribution remain open joins. Nothing proves complete-postulate insufficiency.

## Evidence, omissions and repair disposition

Actual parent capture: PASS, four families/seven cases,0.5244726039236411s,
returncode0,2GiB address-space limit,48,588KiB reported max RSS, no wall/CPU
timeout; Python3.10.12/SymPy1.13.1. Saved stdout/stderr hashes match the receipt;
stderr is empty. I inspected the code and actual quantities, and independently
recomputed the load-bearing analytic identities and all three rational receiver
cases. I did not rerun the parent's code or spend the optional reviewer program.
Finite controls do not prove the generic argument by sampling.

Omitted: full registry/normal/maintenance replay at this review stage, all old
source numerical controls, global continuation/caustics, all-conformal-extension
classification, receiver existence, native RG admission, physical reference
selection, finite observational error certification, different-model/human/formal
review, and final integration bytes not yet frozen. The parent owns closure checks.

Required defects/repairs: none. Nonblocking precision: retain the interior-versus-
boundary regularity distinction above in the central text and keep every open
admission/attribution join visible. If a later integration asserts a C2 boundary
family, a fixed-emission distance law, native attribution, or RG adoption, this
verdict does not cover that strengthening and it requires repair/re-review.
