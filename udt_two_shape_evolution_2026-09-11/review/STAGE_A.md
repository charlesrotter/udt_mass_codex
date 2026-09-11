# TI2 independent ADM rate — sealed before author TI2 science exposure

This note and its seal own the independent route. INDEPENDENT_FRAME.md owns authority,
choices, exposure and resource controls. The accepted TI1 full argument and review were read;
no author TI2 implementation/results/candidate/record draft have been opened. Runtime
model/version is UNATTESTED. Different context and implementation are actual; different-model,
independent-library general proof and formal/human-specialist review are not established.

## Derivation retaining the full geometric derivatives

Use the supplied conventions and all TI1 data. Write d=p^2+r^2, k=(d-s^2)/(2s),
tau=k+2s and W=p r_X-r p_X. The vacuum Gauss/Codazzi relations in these conventions are

    E=Ric3+tau K-K gamma^-1 K,
    B_ij=epsilon_i^{ab} D_a K_bj,  P=16 E_ij B_kl gamma^ik gamma^jl.

At the initial flat slice gamma_T=-2K, (gamma^-1)_T=2K,
K_T=tau K-2K^2, and tau_T=tr(K_T)+2tr(K^2)=tau^2 by the constraint.
The full flat Ricci variation gives

    Ric3_T,ij = Delta K_ij + partial_i partial_j tau
                -partial_a partial_i K_aj -partial_a partial_j K_ai
              = diag-block(0,-H_XX).

Thus E_T=Ric3_T+2tau^2 K-4tau K^2+2K^3. The curl derivative includes

    (epsilon_i^{ab})_T=(tau delta_im-2K_im)epsilon_m^{ab},
    (Gamma^a_bj)_T=-(partial_b K_aj+partial_j K_ab-partial_a K_bj),
    B_T,ij=(tau delta_im-2K_im)B_mj
           +epsilon_i^{ab}(partial_a K_T,bj-Gamma_T^c_aj K_bc).

The other connection term vanishes by symmetry in the antisymmetrized a,b indices;
it is not omitted by assuming the connection derivative vanishes. Both inverse-metric
factors in P contribute, giving

    U(P)/16 = E_T:B + E:B_T + 4(KE):B.

The last term vanishes IDENTICALLY for this special datum: the transverse KE block is
a scalar multiple of I and the transverse B block is tracefree, while B_XX=0. This
identity is a consequence after differentiation, not authority to freeze inverse metrics.

Exact general-symbol output, with p,r and their first two X derivatives arbitrary, is

    P = -16W(d-s^2)/s,
    U(P) = -8W(5d^2+6ds^2-11s^4)/s^2
           -32(p_XX r_X-p_X r_XX).

For the supplied harmonic profiles p_XX=-p,r_XX=-r and W=-A B sin(theta), hence

    U(P) = 8 A B sin(theta) [5d^2+6ds^2-11s^4-4s^2]/s^2,
    L = [5d^2+6ds^2-11s^4-4s^2]/[2s(d-s^2)],
    L0(s) = (11s^2+4)/(2s),
    S = U(P)-L0(s)P
      = 8 A B sin(theta) d[5d-5s^2-4]/s^2.

Under A=epsilon a,B=epsilon b at fixed s, d=epsilon^2 h(X), W=-epsilon^2 ab sin(theta).
For ab sin(theta)!=0 and small nonzero epsilon, L is well-defined and L0 is independent
of a,b,theta,X. It depends on s and the supplied unit spatial harmonic/normalization.
This is a scalar initial-rate reference, not an exact reference spacetime.

In the safe box d<1/8,s^2>1/4. Nonaligned profiles cannot have p=r=0 at a common X, so d>0.
Therefore S has sign opposite AB sin(theta), hence opposite P, and is nonzero everywhere
on the initial slice. L-L0<0. This states faster initial logarithmic decrease of |P|
relative to this marked reference; it establishes no energy transfer or general coupling.

On the same-tangent analytic c(epsilon)=O(epsilon^2) family with s0=-2/3,

    P=(32/3)epsilon^2 ab sin(theta)+O(epsilon^4),
    U(P)=-(640/9)epsilon^2 ab sin(theta)+O(epsilon^4),
    S=-112epsilon^4 ab sin(theta)h(X)+O(epsilon^6).

The last remainder follows from the exact S formula, bounded s away from zero and compact
X. Odd higher coefficients of analytic c are allowed; c=O(epsilon^2) still gives the
stated O(epsilon^6) remainder. For a reference fixed instead at s0, U(P)-L0(s0)P includes
[L0(s)-L0(s0)]P. Since L0'(s0)=1, c=c2 epsilon^2+... adds
(32/3)c2 ab sin(theta)epsilon^4. Completion independence of the matched-s coefficient
must not be misreported as independence under an original-background reference.

Zero/one/aligned controls have P=U(P)=S=0. Their local evolved P=0 follows from the
complete-data reflection argument already accepted in TI1, not just this first derivative.
Opposite phase reverses the oriented diagnostic when profiles are transformed consistently;
an arbitrary theta change also changes d(X), so it need not be a simple pointwise sign flip.
The permitted outside-safe-box p=s cosX,r=s sinX datum has d=s^2,W=s^2:
P=0 but U(P)=32s^2. It is an initial cancellation, not persistent zero or a universal theorem.

## Derivative/time/record and realization assessment

The accepted full TI1 joint analytic CK/Bianchi argument supplies actual local Ric=0
developments. All these jets are equation-required derivatives of those solutions.
For fixed data, analyticity gives P(T0+t,X)=P0+t U(P)0+O(t^2), uniformly in compact X
on a sufficiently small datum-dependent slab. A mathematical comparison with
P0 exp(L0(s)t) has linear coefficient S; it is not a fabricated reference solution.
No finite trajectory, prescribed uniform lifetime, global Gaussian coordinates or stability.

Six actual commonly marked density functions reconstruct gamma by q_v=m_v^2 and
polarization. A general direct derivative of curvature uses a metric three-jet and hence
record derivatives up to third order. In this flat initial slice ADM expression the
necessary data can be supplied by K,K_X,K_XX, i.e. q_T,q_TX,q_TXX together with the
known initial gamma and conditional equation. The harmonic prior K_XX relation allows
the displayed scalar formula to be evaluated using the lower-order supplied coefficients;
that is a model-assisted recipe, not a general lower-order or minimal-information theorem.
Whole smooth fields already include their derivatives. Identical normalized H fields do
not identify full time-live tapes or native history/pair populations; original clocks remain
marked geometric normals and G166/G176 boundaries remain unchanged.

## Actual execution and preserved diagnostic

independent_adm_rate.py imports no author TI2 code. SymPy1.13.1/Python3.10.12; exact
arithmetic, one thread,2GiB/180s. The first capture adm_rate exited1 at an overly strong
reviewer control expectation: it required omitting inverse contraction to change this
special scalar, but the included term cancels exactly. All preceding symbolic tensor and
constraint checks passed. Original script INITIAL_independent_adm_rate.py and failed
stdout/stderr/receipt are preserved. Repair only stopped requiring every omission control
to be nonzero; it did not change any tensor or scalar expression.

adm_rate_repaired: exit0, empty stderr/no timeout,0.611230741s,maxRSS46600KiB. The exact
safe-family rational anchor p=1/8,r=1/12,p_X=-1/10,r_X=1/7,s=-2/3 gives
P=-297/1120,U(P)=1576553/860160,L0=-20/3,S=55913/860160. The accepted TI1 review already
exhibits its actual harmonic realization with A^2=41/1600,B^2=193/7056 inside the safe box.
Omitting the B-connection, B-volume or Ricci spatial variation gives respective nonzero
anchor errors -35739/57344,-77319/286720,-88/105. Finite checks do not prove generality;
the symbolic identities and the stated analytic hypotheses own the quantifiers.

Next stage: compare the frozen author candidate to this sealed route; independently check
all equation/three-jet/record/time claims and narrowed geometric interpretation. This
provisional survivor remains UNPROMOTED and has not yet received whole-candidate review.
