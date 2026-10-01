# FPC1 mathematical derivation before parent-candidate exposure

This fixed evidence record follows SOURCE_FIRST.md. It remains a conditional candidate pending adversarial review, not a maintained scientific summary or a native UDT result. No parent FPC1 candidate or peer record has been read at this freeze. Closest prior work is PSW1's quadratic prepared-clock calculation and G212's conditional space-form control. Same inherited model and same installed SymPy as the parent are not different-model independence.

## One supplied nonflat Ricci-flat control

Use g=-dt²+sum_i t^(2p_i)(dx^i)², p=(-1/3,2/3,2/3), central clock A=(t,0), preparation event t=1. All lengths/times are in c_E=1 units; L>0 is proper length along the initial spacetime spacelike geodesic, never the coordinate displacement. The metric is a supplied free-and-explored comparison. The axis planes are totally geodesic by the spatial translations/reflections and diagonal form. In axis i write its exponent r (to distinguish it from the outgoing arrival derivative p_arr).

The spacelike preparation obeys t^(2r)x'=1, t''=-r t^(-2r-1), initial t=1,t'=0,x=0,x'=1. Its orthogonal future unit normal is V=(t^(-r),t' t^(-r)). This vector is parallel: in two dimensions the unit normal of a unit affinely geodesic spacelike tangent is parallel; substitution in both transport equations confirms it. Thus this is exactly PSW1's preparation, not synchronous comoving preparation. With T=t(L), X=x(L), the released timelike receiver has conserved spatial momentum C=T^r t'(L). Series at preparation are

    T = 1-r L²/2-r²(2r+1)L⁴/24+O(L⁶),
    X = L+r² L³/3+O(L⁵),
    C = -r L+r²(r-1)L³/6+O(L⁵).

Timelike normalization and momentum conservation give gamma(t)=sqrt(1+C²/t^(2r)), w(t)=C/t^r, and dx/dt=C/[t^(2r)gamma(t)]. Let eta'(t)=t^(-r). At fixed prepared receiver, the emission time u and outgoing reception tb satisfy

    eta(tb)-eta(u)=X+integral_T^tb C/[t^(2r)gamma(t)] dt.

For emission u=1 and the actual immediate null return, eta(ta)=2eta(tb)-eta(1). These equations directly fix the nearby future branches. They imply, by implicit differentiation at fixed preparation and by the endpoint frequency contractions,

    p_arr = (tb/u)^r /(gamma_b-w_b),
    q_arr = (ta/tb)^r (gamma_b+w_b).

In particular at u=1,

    log p_arr = r log(tb)+asinh(C/tb^r),
    log q_arr = r log(ta/tb)+asinh(C/tb^r).

The return is a separate future branch, not 1/p_arr. Differentiating while re-preparing T,X,C with u would be a different experiment.

The exact finite symbolic recurrence in check_kasner_higher.py solves the preparation ODE, then each implicit incidence equation coefficient by coefficient. It does not insert a desired clock series. The output is:

| Axis exponent r | log p_arr through L⁴ | log q_arr through L⁴ |
|---|---|---|
| -1/3 | 2L²/9-4L³/27+22L⁴/243 | 2L²/3-28L³/27+50L⁴/27 |
| 2/3 (each of two axes) | -L²/9+2L³/27-43L⁴/486 | -L²/3+14L³/27-5L⁴/6 |

Hence the three principal-axis means are

    mean_i log p_arr = -7 L⁴/243+O(L⁵),
    mean_i log q_arr =  5 L⁴/81+O(L⁵).

The L² and L³ means both cancel. Reflection x^i -> -x^i is an isometry fixing A and the preparation frame except for the reflected axis, so the corresponding negative-axis experiment has the same answer at the same positive L. Thus a six-axis mean agrees with this triad mean. One must not replace L by a signed length in the future-flight series: odd powers describe positive flight duration and do not change sign under spatial reflection. This calculation does not establish a spherical average beyond L².

The nonflat Ricci-flat conditions are checked by sum r_i=sum r_i²=1; Ric_tt is proportional to sum r_i(r_i-1), Ric_ii to r_i(sum r_j-1). Tidal eigenvalues r_i(1-r_i) are nonzero. The actual nonlinear equations are analytic near t=1; at L=0 the selected one-sided outgoing and return incidence equations have nonzero derivative in arrival time. Analytic ODE/implicit-function dependence supplies O(L⁵) remainders for these local chosen branches. Consequently the stated nonzero leading fourth-order means have their indicated signs for sufficiently small positive L. No explicit finite-L error constant or certified numerical threshold is supplied.

The capture completed48 finite exact assertions in4.659s at61,200KiB maximum RSS with2GiB address cap and no CPU/wall timeout. It checks preparation norm and transport, outgoing/return incidence, old quadratic limits, Ricci-flat exponent identities, and exactly vanishing readouts for axis exponents0 and1 as flat consistency controls. Python3.10.12, SymPy1.13.1. The two distinct exponent values are components of one Kasner geometry; they are not two supplied nonflat controls. These checks are exact formal algebra plus the analytic remainder argument, not independent numerical ray integration or a generic curvature-jet classification. Script, freeze, stdout, stderr and TPS1 capture receipt are preserved. No failed scientific run preceded this output.

## Finite space-form endpoint calculation

Let k=H²>0 and l=HL. In ambient signature(-,+,+), use the standard de Sitter radius1/H surface and the totally geodesic radial plane. Dimensionless embedding curves are

    H A(s)=(sinh(Hs),0,cosh(Hs)),
    H B(b)=(sinh(Hb),sin(l)cosh(Hb),cos(l)cosh(Hb)).

These have proper parameters s,b, and B0 lies at proper spatial geodesic distance L on t=0. Its initial U=(1,0,0) is ambient constant along that spatial geodesic, so its tangential covariant derivative vanishes: the preparation is parallel. Their second ambient derivatives are normal to the hyperboloid, giving geodesics. A radial future-null chord satisfies

    cos(l)cosh(Hs)cosh(Hb)-sinh(Hs)sinh(Hb)=1.

Chronology selects the outgoing root. At s=0 and 0<l<pi/2,

    Hb0=artanh(sin l),  p_arr=sec l.

At that relay the actual future arrival a on A obeys cosh(Ha)-tan(l)sinh(Ha)=1. The root a=0 is the prior emission; the future second root is

    Ha0=2artanh(tan l), q_arr=cos l/cos(2l), 0<l<pi/4.

At l=pi/4 the return time diverges. For pi/4<=l<pi/2 there is still a finite outgoing relay but no finite immediate future return to this A. The stronger round-trip restriction must not be erased by the broader outgoing branch. As l->pi/2 from below outgoing b0 and p_arr diverge, but this is outside the return sector. Small-L logs are kL²/2+O(L⁴) and3kL²/2+O(L⁴), matching PSW1 because T(n,n)=-k. All directions in the simply connected local space form are equivalent under isotropy; this is a property of this supplied control, not an inference from UDT's absence of a preferred observer.

For k=-H²<0, a standard universal-cover anti-de Sitter radial plane with ambient signature(-,-,+) has dimensionless curves

    H A(s)=(cos(Hs),sin(Hs),0),
    H B(b)=(cosh(l)cos(Hb),sin(Hb),sinh(l)cos(Hb)).

Use the first chronological branch before crossings/refocusing; no periodic time identification is adopted. The same norm, geodesic and parallel-preparation arguments apply. Null incidence is cosh(l)cos(Hs)cos(Hb)+sin(Hs)sin(Hb)=1. At s=0, for every finite l>0 on that first branch,

    Hb0=arctan(sinh l), p_arr=sech l,
    Ha0=2arctan(tanh l), q_arr=cosh l/cosh(2l).

Both derivatives are positive and less than1, so the supplied opposite-sign control blueshifts both legs. Both emission0 flight times lie before pi/(2H), and every finite L has a regular first outgoing/return. As L->infinity both arrival times approach pi/(2H), with both derivatives tending to zero; that infinite-separation limit is not an attained finite regular experiment. The flat limit is b0=L,a0=2L,p_arr=q_arr=1. At finite l, the subsequent crossings or reflected AdS boundary paths are not covered.

These standard homogeneous-geometry controls supply no preferred universal center: choosing A defines a laboratory, and isometries map it to another admissible laboratory. Their k,L and branches remain supplied. They do not derive k, select its sign, identify a physical curvature scale or X_max, prove the full UDT postulates admit them, or show an additional positional effect beyond an operationally matched comparison. G212 is explicit prior conditional space-form work. The present useful comparison is its finite PSW1-prepared actual clock map and distinct future-return boundary, not a new space-form theorem.

## Strongest survivor and seam

Ric=0 cancellation of PSW1's leading triad mean does not force every finite principal-axis mean to vanish: this one supplied analytic Kasner geometry has nonzero fourth-order means. Its outgoing and return means have opposite signs, and individual directions already have both signs. It supplies no all-direction or spherical positivity theorem.

The positive-curvature supplied space form has nonlinear slowing on both actual legs in its return sector, and distinct outgoing/return limiting boundaries. Ordinary local proper clocks and unit local null speed remain intact. It is a conditional geometric compatibility example, not a physical adoption or a discriminating UDT prediction. The physical seam remains the owner assignment of a particular net/matched finite comparison to positional dilation, followed by any physical selection of k and scale. An evaluator or covariance principle does not supply those assignments.
