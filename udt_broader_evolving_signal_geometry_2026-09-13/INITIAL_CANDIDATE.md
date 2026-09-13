# BE1 — finite-mode evolving geometry and linked signal maps

INITIAL CONDITIONAL CANDIDATE, UNREVIEWED, UNPROMOTED. Mathematical exploration
and source/implementation mapping preceded this written candidate; no broader
numerical or fresh-reviewer outcome has been exposed. This extends a supplied
conditional family, not native dynamics or a new general Gowdy theorem.

## 1. Full finite-mode completion

Take WORK_ORDER's positive-time polarized metric, supplied torus/areal marking,
L,c_E>0 and distinct fixed positive integer modes n_1<...<n_m, k_j=3n_j/4,
finite real a_j,phi_j. For t>0 put theta_j=k_j xi+phi_j and

 F_j=A_j J0(k_j t)+B_j Y0(k_j t),
 A_j=-(3pi/4)Y0(k_j), B_j=(3pi/4)J0(k_j),
 P=sum_j a_j F_j cos(theta_j), lambda0=4log(3/4),
 L_j=t²(F_j'²+k_j² F_j²)/2+tF_jF_j'/2-9/8,
 C_ij^+=t(k_j F_i'F_j+k_i F_j'F_i)/(k_i+k_j),
 C_ij^-=t(k_j F_i'F_j-k_i F_j'F_i)/(k_j-k_i),
 lambda=lambda0+sum_j a_j²[L_j+tF_jF_j' cos(2theta_j)/2]
        +sum_{i<j} a_i a_j[C_ij^+ cos(theta_i+theta_j)
                          +C_ij^- cos(theta_j-theta_i)].             (1)

Distinct k_j make all denominators nonzero. Equal-frequency phases would first
need combination into one real sine/cosine amplitude; they are not fed into(1).
Zero-amplitude members and the empty sum are allowed as controls. These finite
real functions are analytic at every positive t and periodic in xi.

The Bessel Wronskian gives F_j(1)=0,F_j'(1)=3/2 and
F_j''+F_j'/t+k_j²F_j=0. Hence P_tt+P_t/t-P_xixi=0. Direct differentiation gives

 L_j'=t(F_j'²+k_j²F_j²)/2,
 (tF_jF_j'/2)'=t(F_j'²-k_j²F_j²)/2,
 (C_ij^+)'=t(F_i'F_j'-k_i k_j F_i F_j),
 (C_ij^-)'=t(F_i'F_j'+k_i k_j F_i F_j).                (2)

Product-to-sum identities establish lambda_t=t(P_t²+P_xi²).
Differentiating(1) in xi establishes lambda_xi=2tP_tP_xi, including every mixed
term. At t=1, all spatial terms vanish and lambda=lambda0. The finite periodic
primitive proves zero period integral; no nonperiodic drift or seam is imposed.
The full original-metric Ricci reduction in G394 candidate(3)-(4), read under
current G312 FILTER ONLY authority, then sets EVERY Ricci component to zero.
This is an explicit conditional metric development, not only mode equations,
formal jets or a linearized lapse. Dropping mixed terms generally violates it.

Set Q(X)=sum a_j cos(n_j X+phi_j), xi=4X/3. At t=1 the physical initial spatial
metric is L²I and, with K=-(1/2)L_n gamma, its mixed extrinsic tensor is

 K^i_j=L^-1 diag(1/3-3Q²/4,-2/3-Q,-2/3+Q).           (3)

The full Hamiltonian constraint cancels pointwise; flat-slice momentum reduces
to the derivative of Kyy+Kzz=-4/(3L), hence vanishes for these periodic Q.
Equation(1) matches the complete supplied pair, including the quadratic KXX.
Initial metric-value equality across profiles is not equality of all data.

N=exp(lambda/4)t^-1/4>0 and t exp(+/-P)>0 give a smooth Lorentzian metric
on(0,infinity)xT3. On each compact positive-t slab, coordinate causal speeds
are bounded and space is compact. An inextendible causal curve with an interior
finite t endpoint would converge spatially and extend through a regular point,
a contradiction. Thus the t slices are Cauchy for this explicit development.
No t=0 extension, maximality, geodesic completeness, uniqueness or stability
claim is needed. This reuses G394's clarified argument at the new finite-mode scope.

## 2. A fading profile still need not restore the marked geometry

For each fixed mode, G394's real-positive-argument Bessel asymptotics give
F_j,F_j'=O(t^-1/2), L_j=sigma_j t+O(1),

 sigma_j=k_j(A_j²+B_j²)/pi>0,
 S=sum a_j² sigma_j,
 P=O(t^-1/2), lambda-lambda0=S t+O(1),                 (4)

uniformly in xi for this FIXED finite mode/amplitude/phase list. Each mixed
term is bounded because it is a fixed coefficient times tF_i'F_j or tF_j'F_i.
Thus S>0 whenever at least one a_j is nonzero. Under the SAME marked orbit-area
comparison as G394, Z_geom/Z_geom0=exp[-(lambda-lambda0)/2] and
H_rho/H_rho0=exp[-(lambda-lambda0)/4] tend to zero. Here Z_geom is the squared
area-gradient norm, NOT the signal frequency ratio used below. This extends
G394's cumulative lapse/marked-rate result. It does not establish its special
alternating tidal-extremum subsequence for arbitrary mode mixtures.

Constants depend on the fixed list; no infinite-mode, uniform-frequency,
small-amplitude/infinite-time, generic-data or physical-time instability claim.
This marked asymptotic comparison is distinct from finite repeated signals at
fixed receiver labels. No asymptotic claim for those finite arrival schedules
is inferred from(4), and no conditional c_eff becomes a local signal speed.

## 3. Joint records: inherited identities, enlarged geometry

Prescribe WORK_ORDER's fixed source/receiver worldlines, covering lift, actual
source proper reading s=sigma_A(t_e), sigma_i(t)=integral_1^t N(u,xi_i)du.
Ideal test signals follow full future null geodesics with local skies and
proper-clock tags, neglecting backreaction. These are conditional rules.
Let ell=diag(N,sqrt(t)e^(P/2),sqrt(t)e^(-P/2)),
A=diag(1,N²e^-P/t,N²e^P/t), h=sqrt(p^T A p),
x'=h_p,p'=-h_x, p_e=ell_e s_e with |s_e|=1.
Use the full canonical variation M and quotient screens E_e,E_o as in G421.

The earlier identities depend on these geometric hypotheses, not on one mode:

 D=E_o^T ell_o M_xp ell_e E_e,
 J_end=[M_xp ell_e E_e | v_o], det J_end=det D/t_o,
 Z_sig=u'(s)=omega_e/omega_o=1/omega_o>0,
 Delta u=integral_s0^s1 Z_sig(s) ds,
 A_forward=Z_sig² A_reverse on the SAME segment.        (5)

For the determinant identity use ell_o v_o=N_o s_o and det ell_o=N_o t_o.
Nonzero determinant gives LOCAL endpoint regularity, not global reach/uniqueness
or generic no-conjugacy. Duration requires a regular whole-event branch; a
positive interval is needed for its mean/normalized-error reading. Area ratios
need nonzero reverse area; the division-free relation has the inherited rank-loss
scope. A reverse Jacobi calculation is not a later causal return. These are
applications of G348/G421/G423/G417, not newly discovered general geometry.

Changing emission time retains the G421 vector
w_e=(0,ell'_e s_e)-V_e and the full current lower endpoint. For arbitrary P here,

 (log ell)'=(-1/(4t)+t(P_t²+P_xi²)/4,
             1/(2t)+P_t/2,1/(2t)-P_t/2).              (6)

Equations(5)-(6) must use actual source time/rulers and full mixed lapse. Fixed-
emission spatially varying frozen controls are separate supplied metrics, not
one alternative evolving clock history or asserted Ricci-flat developments.
Dimensionless records and joint L/c_E protocol scaling retain G423's scope.

## 4. A special symmetry may disappear without a focusing conclusion

NTB1's invariant transverse-plane proof needs its reflection-plane hypothesis.
For the numerical P profile, inspect xi=0 and a pure-y launch at t=1 (a separate
symmetry diagnostic, not the main emitter). Write q=P_t(1,0), r=P_txi(1,0).
Here q=9/16 and r=-(27/80)sin(pi/3), so q!=1 and r!=0. Initially P_xi=a_xi=0,
but for a=log N,

 partial_t(2a_xi-P_xi)|_(1,0)=(q-1)r !=0.              (7)

If xi were constant with p_xi=0, the pure-y Hamiltonian would require
partial_xi A_y=A_y(2a_xi-P_xi)=0 throughout the path. Equation(7) contradicts
that for sufficiently small positive times. Thus this old plane is not invariant
for the mixed-phase datum. This does NOT prove a conjugate point, focusing,
instability or failure of every invariant plane. NTB's proof cannot be imported
without its hypotheses; the actual broader beam question remains scoped.

## 5. Initial calibration leaves a concrete next question

At the known initial epoch/source axes/phase let Q_A=sum a_j cos(theta_j(xi_A)).
The independently supplied ideal metric rates satisfy

 H_y+H_z=4c_E/(3L), H_y-H_z=2(c_E/L)Q_A.               (8)

Thus these readings calibrate L and Q_A, not each amplitude of a multi-mode
profile. This is the exact extension of G423's calibration, not an acquisition
theorem, native scale selection or a new generic nonselection theorem. With
known two-mode phases, one linear amplitude direction remains after Q_A is fixed.
The useful NEXT question is whether a further unused signal record distinguishes
that particular direction. It is reserved for authorized StageC, not preclaimed
here. Unknown phases, extra modes and nonregular branches retain extra freedom.

The predeclared finite checks illustrate actual full-profile joint maps, tighter
agreement, original endpoint/constraint residuals, source-time and reverse-beam
relations. They do not prove asymptotics, interval bounds or generic coverage.
Candidate construction precedes outcomes; any later repair or failed procedure
must remain visible. Maximum disposition: reviewed conditional BE1, UNPROMOTED.
