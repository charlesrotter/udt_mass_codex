# NTB1 initial candidate — full beam evaluator and transverse nonfocusing

UNPROMOTED; direct review PENDING. Source snapshot: SOURCE_PINS.json.
Parent analytic exploration preceded numerical outcomes. The invariant scalar ODE
and positive auxiliary-system argument below were developed before receiving the
reviewer's first message, but not hash-sealed then. The reviewer independently
reported the same pure-y scalar ODE and a finite no-root diagnostic before this
candidate freeze. These timing/exposure distinctions preclude claiming a blind
parent freeze. No parent numerical result was read before this file was written.

## 1. Scope and exact full-sky evaluator

Use the entire G394 metric as written in G415's INITIAL_CANDIDATE.md (1):
g=N²(-dt²+dxi²)+b_y²dy²+b_z²dz², b_y²=t exp(P), b_z²=t exp(-P),
P=epsilon F(t)cos(k xi), k=3/4, N=exp(lambda/4)t^-1/4,
F''+F'/t+k²F=0, F(1)=0,F'(1)=3/2; full source lambda retained.
G394 owns the exact conditional Ric=0 geometry; current G312 is FILTER ONLY.
No native equation, preferred observer, physical beam or full pair assembly follows.

The source is t=1, unit frequency, chosen unit sky s, supplied areal observer
n=N^-1 partial_t, source xi_e. Compare at equal marked reception t. All quantities
below are infinitesimal variations about the FULL nonlinear metric and ray.
N_e=3/4, b_y(e)=b_z(e)=1. Set L=diag(N,b_y,b_z), p_e=L_e s,
A=diag(1,N²/b_y²,N²/b_z²). The positive-time reduced null Hamiltonian is

    h=sqrt(p^T A p), x'=h_p, p'=-h_x, omega=h/N.               (1)

Let M be its six-dimensional canonical first variation, M(1)=I, and let E_e
be an oriented orthonormal pair perpendicular to s in source spatial orthonormal
components. With K=M_xp, the target separation columns at fixed t are

    X=L_o K L_e E_e,  s_o=L_o^-1 p_o/omega_o,
    D=E_o^T X,   A_forward=|det D|, R=1/omega_o.              (2)

Here E_o is any orthonormal pair perpendicular to s_o. Fixed-t endpoint variation
differs from fixed-affine endpoint variation by a multiple of the central null
tangent. Quotient projection removes that multiple. In fact p_o dot delta x=0:
the source-fixed null Jacobi variation has g(k,J)=0, which is preserved, and
adjusting its endpoint parameter adds a null multiple. Thus (2) is the intrinsic
G348 quotient map in observer screen representatives, not an unprojected coordinate
area. Source-frequency normalization and both screen dimensions are essential.

For explicit implementation, Q=A p, S_x=p^T A_x p, S_xx=p^T A_xx p,
where x-derivatives mean xi derivatives. The Hessian blocks are

    h_pp=A/h-Q Q^T/h³,
    h_xp=(A_x p/h-Q S_x/(2h³)) in row xi, other rows zero,
    h_xx=S_xx/(2h)-S_x²/(4h³) in slot xi,xi only,
    M'=[[h_px,h_pp],[-h_xx,-h_xp]] M.                       (3)

The field derivatives retain lambda_x and lambda_xx. These are exact first
variations, not a truncated metric or a finite angular bundle. Smoothness on each
finite positive-time slab provides the finite flow and its derivative along each
regular ray. Rank loss of (2) is the G348 conjugate-endpoint criterion; coordinate
wrapping/cut ties and finite-wavefront overlap are different questions.

## 2. Reciprocity and observer choices: reused G348

Same-segment reversal, common affine normalization and arbitrary finite timelike
endpoint-observer changes obey G348 (13)--(24). In particular

    A_forward/A_reverse=R²                                   (4)

where both areas are nonzero; at a conjugate endpoint both vanish and the quotient
of zeros is not used. Multiplying source/target frequencies by positive Doppler
factors d_e,d_o multiplies directional areas by d_e²,d_o² respectively and R by
d_e/d_o. A passive representation change leaves the same physical query unchanged;
physically changing an observer changes its sky/frequency readout, not the underlying
quotient rank. No finite observer change creates or removes conjugacy. A later
causal return is not the mathematical inverse segment. This is already source-owned
general geometry, not a new derivation of Universal Reciprocity/DDR or proof of full
native UDT membership.

## 3. Exact transverse symmetry-plane extension

Take xi_e=m pi/k (m integer), mu=0, arbitrary transverse direction
(p_y,p_z)=(cos psi,sin psi). Reflection makes xi(t)=xi_e,p_xi=0 an exact
ray for every finite amplitude. Absorb cos(k xi_e)=(-1)^m into e=+/-epsilon.
On the ray P=e F, define

    M_t=p_y² exp(-P)+p_z² exp(P)>0,
    r=(p_z² exp(P)-p_y² exp(-P))/M_t,
    w=e t F', q=w²/4+r w/2, b=log N-log(t)/2+log(M_t)/2.

The subscript on M_t distinguishes this scalar from canonical matrix M.
Direct field differentiation gives

    b_t=(q-3/4)/t,
    b_xixi=(w+r)w'/(2t),
    w'=-e k²tF, r'=(1-r²)w/t.                              (5)

For the source-sky variation toward xi, let Z=delta xi, Z(1)=0,Z'(1)=1.
The exact reduced ray equation gives

    Z''+b_t Z'+b_xixi Z=0.                                 (6)

Set Y=tZ'+(q-7/4)Z. Equations (5)--(6) are equivalent to

    Z'=Y/t-(q-7/4)Z/t,
    Y'=(1-r²)w² Z/(2t),  Z(1)=0,Y(1)=1.                   (7)

On every finite interval these coefficients are regular, and both off-diagonal
coefficients are nonnegative (1/t strictly positive). Integrating-factor positivity
or the first-zero argument gives Z(t)>0 and Y(t)>=1 for every t>1. Specifically,
while Z>=0, Y is nondecreasing; the first equation with Y>=1 has a strictly positive
integral solution and cannot return to zero. The initial positive slope starts the
argument. Hence the longitudinal screen width is D_xi=N_o Z>0.

The independent source-sky variation within the transverse plane has
v=(-p_z,p_y). At xi=xi_e it does not perturb the xi ray. The transverse Hamiltonian
Hessian is N/(t² W^(3/2)) vv^T, W=M_t/t. Consequently the other width is

    D_perp=sqrt(t M_t) integral_1^t N(u)/(sqrt(u) M_u^(3/2)) du >0.   (8)

The two screen directions are orthogonal and decouple by reflection. Thus

    A_forward=D_xi D_perp>0 for all t>1, all finite epsilon,
    every psi, and every reflection-plane source xi_e=m pi/k.       (9)

This is an exact nonconjugacy theorem for these invariant transverse rays,
including mixed y/z directions. It is neither an open angular neighborhood of
nonconjugacy for unbounded times nor a theorem for arbitrary source phases/tilts.
At fixed finite endpoints continuity does give a sufficiently small neighborhood
with nonzero determinant, but supplies no common neighborhood for t->infinity.

## 4. Pure transverse axes: clock quietness does not force area quietness

For p_y p_z=0, r=+/-1 and Y=1 exactly. Therefore

    Z=t exp(-b(t)) integral_1^t exp(b(u))/u² du.             (10)

At epsilon=0, equations (8),(10) recover

    D_xi0=(3/7)(t^(3/2)-t^(-1/4)),
    D_perp0=3(t^(3/4)-t^(1/2)).                            (11)

Fix nonzero finite epsilon. G394 owns P=O(t^-1/2) uniformly in xi and
lambda-lambda0=epsilon² sigma t+O(1), sigma>0. Let beta=epsilon² sigma/4.
Then N=Theta(exp(beta t)t^-1/4), exp(b)=Theta(exp(beta t)t^-3/4).
Positive exponential-tail integration in (8),(10) gives

    Z=Theta(1/t),
    D_xi=Theta(exp(beta t)t^-5/4),
    D_perp=Theta(exp(beta t)t^-1/4),
    D_xi/D_perp=Theta(1/t),
    A_forward=Theta(exp(2 beta t)t^-3/2),
    log(A_forward/A_forward0)/t -> 2 beta.                 (12)

These are two-sided orders and a logarithmic rate, not constant prefactor limits.
Constants depend on fixed amplitude; no uniform epsilon->0/time limit is asserted.
Each width ultimately grows in order, but monotonicity is not proved; their ratio
tends to zero while neither width vanishes. Thus increasing ellipticity is not
conjugacy. At the same time omega=sqrt(M_t/t), R0=sqrt(t), so

    R/R0=M_t^-1/2 ->1.                                    (13)

The clock contrast limit is reused from NCR1's conditional invariant-ray formula,
also directly visible from (1). The new join is a nontrivial area/shape contrast
along those same rays. G415's axial area rate is 4 beta and width ratio tends to1
for the supplied source; (12) has rate2 beta and anisotropic shape. No asymptotic
exponent for mixed transverse directions or generic oblique beams is asserted.

## 5. Maximum conclusion

Exact full-ray variational evaluator and explicit invariant transverse nonconjugacy;
pure transverse axial-direction area/shape asymptotics at fixed supplied source and
marked reception. All comparisons retain areal observers and source/marking choices.
This reveals conditional geometric information missed by clocks alone. It does not
select light, flux, distance, sources, a universe, native response, full kernel assembly,
an absolute scale, a physical preferred frame or canon. General tilted focusing remains
to be investigated; finite diagnostics must retain their separate evidence grade.
