# ERC1 fixed initial construction — conditional response comparison

Exploratory algebra precedes numerical execution. Parent knew the standard
metric-f(R) trace behavior and GCA1 before constructing this candidate; these
are not blind discoveries or new UDT equations. Initial construction is fixed
for later adversarial review. Conventions: signature(-+++), standard metric
Ricci with positive scalar for de Sitter, c_E=1. alpha is a constant L² parameter.

## 1. Scalar modulation control

Let F=1+2alpha R and E_A=F G. On any smooth domain where F is nowhere zero,
TF(E_A)=F[Ric-(R/4)g]=0 iff Ric=(R/4)g. Contracted Bianchi implies dR=0
on a connected region. Thus a variable formula for F does not produce new
solutions of the regular shape equation. This is the same scalar-rescaling
limitation already discussed in central R17, now used as a control.

The conclusion does not include F=0 open strata. For alpha!=0, metrics of
constant scalar R=-1/(2alpha) make E_A=0 without imposing Einstein shape. Isolated
zeros and smooth transitions are not classified here. This degeneracy is not
scientific evidence for admitting such a response. div E_A=G(dF,.) generally
does not vanish off shell; conservation is not imposed on A to manufacture rejection.

## 2. Derivative response and exact trace

Retain GCA1's UNADOPTED E_B=G+alpha Q, with

    Q=2R Ric-(R²/2)g+2(g Box R-Hess R).
    TF(E_B)=F[Ric-(R/4)g]-2alpha[Hess R-(Box R/4)g].

The Hessian term cannot be discarded as a rescaling. With compactly supported
metric variations this is the known R+alpha R² Euler response, up to overall
normalization. Its divergence vanishes identically: the two Ric(dR,.) terms
from differentiating2R Ric and commuting Hessian divergence cancel. Its trace
is -R+6alpha Box R. No matter source or independent physical scalar is specified.

DDR gives E_B=lambda g. The response's own identity gives d lambda=0. Define
Lambda=-lambda; then E_B+Lambda g=0, with Lambda a free integration datum,
not an imposed E_B=0 or selected cosmological value. For alpha!=0,

    Box(R-4Lambda) - (R-4Lambda)/(6alpha)=0.

This is an exact metric-curvature equation, not a second propagation mechanism.
Around Minkowski/Lambda=0 the scalar linear mode has squared inverse length
1/(6alpha). Positive alpha gives oscillatory homogeneous linear curvature;
negative alpha gives an exponentially growing homogeneous linear mode. These
are linear-sector statements, not nonlinear/global stability or causal well-posedness.
alpha=0 returns Einstein shape. Every Einstein metric Ric=Lambda g has Q=0
and remains a B solution; B alone does not select positive Lambda, its magnitude,
initial data or the desired positional asymptote. F=0 is not generically cancelled.

## 3. Weak nonuniform exterior: two potentials and actual clocks

Write the first-order metric as

    g=-(1+2epsilon Psi)dt²+(1-2epsilon Phi)delta_ij dx^i dx^j,
    R_geometry=epsilon R1+O(epsilon²).

The time-potential is Psi and the spatial-potential is Phi. For alpha>0, let
m²=1/(6alpha), on a compact exterior annulus r>0,

    R1=A exp(-m r)/r,
    U=-mu/r,
    Psi=U-alpha R1, Phi=U+alpha R1.

A and mu are free exterior amplitudes, not derived matter parameters. The decaying
branch is a supplied boundary choice; the growing radial solution is not proved
absent in general. It is not a cosmological cutoff or preferred universal center.
The original static linear curvatures are

    Ric00=Delta Psi, Ricij=partial_i partial_j(Phi-Psi)+delta_ij Delta Phi,
    R1=4Delta Phi-2Delta Psi.

Delta U=0 and Delta R1=m² R1 give G00=R1/3; the00 derivative correction is
-2alpha Delta R1=-R1/3. The spatial Einstein term is2alpha Hess R1-R1 delta/3,
cancelled by2alpha(delta Delta R1-Hess R1). Hence every linearized component
of E_B vanishes. Radial and transverse derivatives/tides need not agree.

For static endpoint proper clocks at r_e,r_o, the supplied weak metric itself
gives p=sqrt[(1+2epsilon Psi_o)/(1+2epsilon Psi_e)], q=1/p on an immediate
return. log p=epsilon(Psi_o-Psi_e)+O(epsilon²), with the scalar contribution
-epsilon alpha(R1_o-R1_e). Both future legs are not forced to redshift. Radial
coordinate null timing obeys dt/dr=1-epsilon(Psi+Phi)+O(epsilon²); the scalar
term cancels at first order in this coordinate expression, not in proper-clock
endpoint observations.

This is a solution of the exact FIRST-VARIATION equations, not an exact nonlinear
exterior solution. On a fixed compact annulus and bounded sufficiently small
epsilon, the metric and its finite derivatives are smooth and nondegenerate;
Taylor's theorem gives uniform O(epsilon²) original-equation residual, since the
zero and first coefficients vanish. No bound against an unknown exact nonlinear
solution or empirical solar-system test is inferred. The clock Taylor error in
the supplied weak metric has its own directly checkable bound/convergence.

## 4. Evolving regular slice and its constraint

Take the declared spatially flat homogeneous/isotropic metric
g=-dt²+a(t)²delta_ij dx^i dx^j, H=a'/a, R=6(H'+2H²), P=R'. This is a
restricted diagnostic, not a native cosmology or complete solution search.
For alpha!=0 the equations give the smooth first-order system

    H'=R/6-2H²,
    R'=P,
    P'=-3HP-(R-4Lambda)/(6alpha),
    a'=aH, eta'=1/a.

The original00 constraint is

    C=3F H²-alpha R²/2+6alpha H P-Lambda=0.

Direct differentiation yields C'=-4HC. Thus C initially zero remains zero;
the trace and geometric definition then supply the full spatial equation as well.
The polynomial H/R/P system gives ordinary local ODE existence for supplied
finite data; a remains positive locally. The claim is confined to this slice,
not well-posedness of the unrestricted fourth-order field system.

R is tracked as a numerical variable but must agree with curvature independently
reconstructed from H. Original00/spatial tensor residuals must be evaluated
from saved metric data and numerical derivatives, rather than only the RHS used
to evolve. Constraint preservation and solver success alone are insufficient.

## 5. A locally flat preparation need not freeze the finite records

With Lambda=0 and initial H=R=0 but P=P0!=0, C=0. The resulting local solution
has H'=0, H''=P0/6 and

    a(t)=1+P0 t³/36+O(t^5).

Its full curvature vanishes at t=0, while higher derivatives need not. At that
event the comoving clocks are also initially parallel-prepared because H=0.
With initial proper separation L and first emission at t=0, define arrival and
echo by eta(t_b)=L and eta(t_a)=2L. The actual tick ratios are

    p=a(t_b)/a(0), q=a(t_a)/a(t_b),
    log p=(P0/36)L³+O(L^5),
    log q=7(P0/36)L³+O(L^5).

This realizes the leading cubic feature of PCC1's supplied control within this
conditional governing equation. The complete scale factor is solved from the
equation rather than chosen to make this clock curve. P0 is still free curvature-
derivative initial data. The construction does not select its sign or identify
the effect as UDT positional physics. It does not contradict the zero quadratic
coefficient or the conditional1:3 quadratic relation (both quadratic terms vanish).

For every other evolving case the comoving clocks are supplied and are not
silently PSW1 parallel-prepared. Positive/negative shifts depend on geometry and
data; a time-reversed/contracting control must not be discarded for its appearance.

## 6. Physical limits

The two unsupported response identifications are displayed, not derived from the
kernel. B is a known metric-f(R) extension and GCA1 prior, not a new UDT law.
Its regular evolving tests can establish conditional dynamics and readout only.
No source coupling, physical alpha/Lambda, native response identity, distinct
positional attribution, observed GR pass, global X_max or complete nonlinear
stability/causality result follows. Free lawful initial data are not themselves
proof of a missing law. Neither limited candidate failure nor nonselection here
proves full UDT underdetermined or in need of a new postulate.
