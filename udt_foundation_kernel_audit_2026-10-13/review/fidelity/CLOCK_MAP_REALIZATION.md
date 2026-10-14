# FKA1 fidelity-review probe — start with the clock maps

Status: exact analytic control frozen during direct review, before sibling
review exposure. It addresses a concrete omitted reverse-direction test in the
initial joint candidate. It is not a native UDT solution, a theorem about all
founding premises, adoption of a physical equation or a scientific grade change.

Reviewer `/root/fka_review_fidelity`; inherited model, separate review context.
The construction originated here after source-first, owner-correction and
target-candidate exposure. The parent received its proposed equations before
this freeze and authorized completing this in-scope probe. No sibling review,
code or numerical result was read. No numerical worker was used. All equations
below are derived directly from the displayed metric and clock curves.

## 1. Question and choices

Can a specified bilateral slowing relation be represented by one causal metric,
starting from the clock records rather than imposing a separate photon-travel
cause? Does that supplied relation and its calibration uniquely determine the
metric in this bounded realization class?

Supply the two maps, in common proper-time units,

    b = f_AB(a) = Z a,        a = f_BA(b) = Z b,
    Z > 1,                   a,b > 0.

Z, the common origins, the positive-time domain, the two-clock preparation,
the smooth metric realization below and the null encoding of the event relation
are all **free-and-explored control choices**, not consequences of the owner
postulate. Time is expressed in length units using calibrated c_E; no measured
cosmic scale or new physical law is introduced. The question is conditional
compatibility and inverse reconstruction for these maps, not selection of Z.

The reverse map is a different future observation: the return on A is
`a -> Z^2 a`, not the inverse of the first map. Both interval ratios are Z,
so both corresponding cadences are slower by 1/Z. The maps specify finite
intervals exactly because Z is constant.

## 2. A family of single-metric realizations

Let u,v have length units; let ell>0 be a control unit/length and epsilon any
finite real dimensionless parameter. Define

    P(u,v) = (v-u/Z)(v-Zu),
    H(u,v) = P(u,v)^2 / ell^4,
    C_epsilon(u,v) = Z exp(2 epsilon H(u,v)),
    g_epsilon = -C_epsilon du dv + dx_perp^2 + dz_perp^2.

The symmetric components are `g_uv=g_vu=-C_epsilon/2`. Work on a finite open
patch of u,v>0 containing the required clock/ray segments; every finite
epsilon gives a smooth Lorentz metric. C_epsilon>0 and the u,v determinant is
`-C_epsilon^2/4<0`. With `t=(u+v)/2`,

    g_epsilon^{-1}(dt,dt) = -1/C_epsilon < 0.

Thus this patch admits a time function; increasing u and/or v is future. There
is no causal loop hidden in the two slowing maps.

Choose the two curves, with transverse coordinates zero,

    A(a) = (a,a/Z),          B(b) = (b/Z,b).

P vanishes along both. Because H is its square, both H and its first derivatives
vanish there. Consequently C=Z and dC=0 on the two clock curves. Direct metric
contraction gives

    g(A',A') = -Z(1)(1/Z) = -1,
    g(B',B') = -Z(1/Z)(1) = -1.

a and b therefore are ordinary proper-clock parameters in every family member.
For this product metric the only u,v Christoffel symbols are

    Gamma^u_uu = partial_u log C,
    Gamma^v_vv = partial_v log C.

They vanish on A and B. The displayed coordinate tangents are constant, so both
clocks are geodesic in every member; their proper acceleration is unchanged.
No altered intrinsic clock rate or hidden acceleration correction is used.

The polynomial `P=u^2-(Z+1/Z)uv+v^2` is symmetric under u↔v. Therefore the
map (u,v)↔(v,u) is an isometry of every g_epsilon and exchanges A(a) with B(a).
Neither of these two clocks is privileged by the chosen metric. This symmetry
does not establish a universal observer-population theorem.

## 3. The geometry realizes the supplied correspondence

The radial null directions have either du=0 or dv=0. Starting from A(a), the
curve with u=a reaches B at b=Za; v increases from a/Z to Za. Starting from
B(b), the curve with v=b reaches A at a=Zb; u increases from b/Z to Zb. Both
segments are future for Z>1 and a,b>0. These are precisely the stipulated maps.

The paths are null geodesics after affine reparameterization. For example, on
u=constant the v equation is

    v'' + (partial_v log C)(v')^2 = 0,
    equivalently C v' = constant.

C>0 supplies a regular increasing affine parameter on every compact segment.
The reverse path has the analogous equation. The transverse geodesic equations
are linear; zero transverse endpoint separation forces zero transverse slope
on the chosen direct branch. No photon field or independent speed law appears.

Here “null” specifies a geometric representation of the clock/event relation.
It is a conditional construction compatible with the clarified single-geometry
ordering; it is not a proof that the owner postulate uniquely requires this
representation, nor a second physical delay added to the postulated effect.

For all epsilon the entire displayed records agree:

    f_AB(a)=Za,   f_BA(b)=Zb,   Z_AB=Z_BA=Z,
    echo(a)=Z^2 a,            echo(a)-a=(Z^2-1)a.

This includes offsets/alignment as fixed here, finite intervals, geodesic clock
preparation and the exchange isometry. It does not claim agreement of arbitrary
other clocks, curvature measurements, screens or an independently prepared
spacelike ruler. Those would be additional records.

## 4. The metric freedom is real curvature, not just chart freedom

The displayed Christoffel symbols give

    Ric_uv = -partial_u partial_v log C,
    R = (4/C) partial_u partial_v log C
      = (8 epsilon/C) partial_u partial_v H.

The flat transverse product leaves this scalar curvature unchanged. For an
explicit interior check set Z=2 and evaluate at u=v=ell. Then

    P=-ell^2/2,
    P_u=P_v=-ell/2,            P_uv=-5/2,
    H=1/4,
    H_uv=2(P_u P_v + P P_uv)/ell^4 = 3/ell^2,
    C=2 exp(epsilon/2),
    R=12 epsilon exp(-epsilon/2)/ell^2.

At epsilon=0 the metric is flat. At every nonzero finite epsilon it has nonzero
curvature at this point. Thus the same two proper-clock records and geodesic
preparations occur in at least two non-isometric metrics in this declared class.
This is not the stronger claim that arbitrary conformal changes preserve every
proper-clock experiment or satisfy all UDT premises.

## 5. Relation to the reciprocal kernel and actual composition

Using a source-clock label on the opposite target gives the tangent Z U_target.
Any regular companion and the adopted G176 completion give, as in the candidate,

    T=Z,  Phi_clock=-log Z,
    chi_clock=(1-Z^2)/(1+Z^2).

Both directions have this same negative Phi_clock. For Z=2 their scalar is
-3/5, for every epsilon. Thus a matched kernel and full clock records can remain
the same while other metric information differs. The family does not supply a
physical ruler identification or re-open normalization ambiguity at a fixed
completed query.

More generally, without any null representation, two differentiable increasing
clock maps f and g obey the exact pointwise cocycle

    Z_(g composed f)(a) = Z_g(f(a)) Z_f(a),
    Phi_(g composed f)(a) = Phi_g(f(a)) + Phi_f(a),
    D_(g composed f)(a) = D_g(f(a)) D_f(a),
    D_f(a) = diag(Z_f(a),1/Z_f(a)).

The scalar contrasts therefore obey

    chi_(g composed f)(a)
      = [chi_g(f(a))+chi_f(a)]/[1+chi_g(f(a))chi_f(a)].

This follows from the derivative chain rule and the specified G176/readout
representation; the positive slopes ensure finite |chi|<1 and a positive
denominator. The inverse of f has reciprocal slope at f(a). A separately
chosen physical return g need not be that inverse. The intermediate argument
f(a) is essential. This is composition on actual labelled maps, not proof of a
universal endpoint potential, spatial depth law or a physical time/length slot
identification from mutual slowing alone.

## 6. Conclusion ceiling and return significance

The reverse-direction probe succeeds: there is a conditional single-metric
realization of these specified bilateral slowing maps, including ordinary free
clocks, causal ordering and observer exchange symmetry. It also proves a bounded
nonuniqueness statement for inverse reconstruction from precisely these records.

It does not derive these maps from the UDT postulate, match an independent
distance-to-depth law, satisfy a selected field equation, recover all tested GR
regimes, choose a geometry/sign/scale, establish all-observer mutual slowing,
or realize X_max. “All founding premises are satisfied” and “the full postulates
are insufficient” are both outside this proof. The free ell and epsilon are
control parameters, not fitted or adopted physics.

This answers one concrete continuation that the initial candidate had not
explicitly attempted. It supports a return only with a precise distinction:
conditional geometric realization is possible, while the physically selected
correspondence and its native interpretation remain unestablished. Further
sampling of this family would add no mathematical conclusion. A next useful
argument would have to bring an existing admitted relation that discriminates
these records/metrics, or a source that actually supplies the time/length or
physical ruler identification. Such an argument remains open; this probe does
not prove that a new physical premise is necessary.
