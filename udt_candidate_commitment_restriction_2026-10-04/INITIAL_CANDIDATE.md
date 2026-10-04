# CPR1 initial restriction audit and conditional limit

This tests CGE1 against existing commitments. Its Einstein equation remains
conditional; no new physical law, response, observer population or completion
is adopted. Sources/WORK_ORDER own the status and scope. The conclusion is a
conditional parameter/domain restriction for a specified realization, not yet
a native UDT selection. Parent discovery preceded the freeze. Matching reviewer
messages exposed their independent limit formulas; the universal limiting
product in section3 was first highlighted to the parent by the math reviewer.

## 1. Fixed source and received-clock experiment

Keep CGE1's f=1-2m/r-Lambda r²/3, m>0, c_E=1 (proper time in length units).
A circular emitter has areal radius a, h=1-3m/a>0, f(a)>0,
Omega²=m/a³-Lambda/3>0, u_e=(partial_t+Omega partial_phi)/sqrt(h).
Omega>0 fixes orientation; no conclusion requires privileging that orientation.
The receiver has one fixed finite Killing energy E>0 and is outward radial,
v=sqrt(E²-f)>0. The angular parameter b of each actual connecting outward ray
is allowed to vary with emission; s=sqrt(1-fb²/r²)>0. Source regularity requires
|b|<a/sqrt(f(a)). Let beta=Omega a/sqrt(f(a))<1; this follows from
f(a)-a²Omega²=h>0. All finite-domain claims retain these inequalities.

In the static region f>0, E-vs can be rationalized:

    A=(E-vs)/f=(1+v²b²/r²)/(E+vs),
    Z=(1-Omega b)/(sqrt(h) A).                        (1)

There v<E and s<=1, so A>=1/(2E), and therefore

    0<Z<=2E(1+beta)/sqrt(h).                         (2)

This is uniform over the admitted outgoing incidences at fixed a,m,Lambda,E;
it is not a bound uniform in unbounded observer boosts or a source approaching
h=0. Neither going to a static chart horizon nor increasing its presentation
phi supplies the owner's divergent received-clock target within this class.
The finite CGE1 results survive; the static patch cannot itself furnish this
particular asymptotic realization. This does not exclude the metric's continuation.

## 2. Same metric through the outer coordinate horizon

Use outgoing u=t-integral dr/f where the static chart is valid. The continued
metric is

    g=-f du²-2 du dr+r²dOmega².                     (3)

Its radial determinant is -1 and its coefficients are smooth for r>0, including
f=0. Ric=Lambda g survives in this same conditional mathematical extension;
no wall, seam or new source is inserted. Its physical/global UDT admission is
not established by this coordinate continuation.

The actual receiver and affine ray become

    u_o^u=1/(E+v), u_o^r=v,
    k^u=b²/[r²(1+s)], k^r=s, k^phi=b/r².           (4)

Their norms are -1 and0. The regular positive receiver frequency is

    A=1/(E+v)+v b²/[r²(1+s)].                      (5)

Together with omega_e=(1-Omega b)/sqrt(h), this gives (1) without subtracting
nearly equal terms at f=0. At an outer horizon v=E,s=1,
A=1/(2E)+E b²/(2r_h²)>0: the horizon crossing itself has finite Z.

Define on a regular outward branch

    U(R,b)=integral_a^R b² dr/[r²s(1+s)],
    P(R,b)=integral_a^R b dr/(r²s),
    u_o(R)=u_0+integral_R0^R dr/[v(E+v)].

For the same fixed circular emitter phi=phi_0+Omega t_e, t_e=u_e after a constant
origin choice, actual incidences satisfy

    t_e+U(R,b)=u_o(R), phi_0+Omega t_e+P(R,b)=0.     (6)

Both unknowns must vary. U_b=b I, P_b=I, I=integral_a^R dr/(r²s³)>0.
The Jacobian in (t_e,b) is I(1-Omega b)>0. Differentiation along the actual
branch yields

    dt_e/dR=A/[v(1-Omega b)], d tau_o/dR=1/v,
    d tau_o/d tau_e=(1-Omega b)/(sqrt(h)A)=Z.        (7)

Thus the time map, frequency and causality all refer to the same regular clocks
and null signals, including outside the static chart. A radial b=0 formula
cannot be differentiated while artificially freezing b for an orbiting source.

## 3. What positive Lambda can realize

Let Lambda>0, H=sqrt(Lambda/3), and require an escaping receiver: v²>0 for
all r>=R0 and R->infinity. E>=1 suffices for m>0, but is not necessary.
Assume a regular limiting solution (t_*,b_*) of (6) at R=infinity, with
|b_*|<a/sqrt(f(a)). Set S_*=sqrt(1+H²b_*²). Source, receiver and ray constants
remain fixed; b varies as required by incidence, not to fit a target curve.

The integrals U_infinity,P_infinity and u_infinity converge. With x=1/R,
their tails and derivatives are smooth near x=0; the nonzero limiting Jacobian
gives a genuine local incidence branch b=b_*+O(1/R), t_e=t_*+O(1/R).
The leading behaviors are

    v~HR, s~S_*, A~S_*/(HR),
    Z/R -> H(1-Omega b_*)/[sqrt(h) S_*],
    R(t_*-t_e) -> S_*/[H²(1-Omega b_*)],
    Z (tau_e,*-tau_e) -> 1/H.                     (8)

The last product follows by multiplying the preceding two limits and using
tau_e=sqrt(h)t_e. Restoring seconds changes its right side to1/(c_E H).
Receiver proper time diverges logarithmically: d tau_o/dR~1/(HR). Every finite
R is a regular finite reception; the limiting received interval is unreachable
at finite receiver proper time. There is no abnormal intrinsic local clock.

For an explicit existence witness, choose u_infinity=0 and the emitter phase
phi_0=0, so t_*=b_*=0. This fixes a relative time/phase preparation, not a UDT
population prescription. The limiting Jacobian is1/a>0. Nearby preparations
also admit regular limiting roots by the implicit-function theorem; no
uniqueness across arbitrary images or all preparations is asserted.

Writing d(R)=integral_R^infinity dr/[v(E+v)], the witness satisfies

    P(R,b)-Omega U(R,b)=Omega d(R),
    t_e=-d(R)-U(R,b).

This is an actual fixed-history orbiting-clock example; b(R) is generally
nonzero at finite R. It is not one of the four original CGE1 numerical queries
and does not retrospectively change their initial events or calibration.

For Lambda=0 the outward exterior has f>0 for r>=a>3m, so (2) excludes
divergent Z at fixed finite E, including escaping E>=1 receivers. For Lambda<0,
f increases without bound and every fixed finite E outward receiver reaches a
finite turning radius; it cannot escape to R=infinity. Its outward static branch
also obeys (2). Hence **this fixed-source/fixed-finite-energy outgoing realization
of unbounded slowing requires Lambda>0**. Positive Lambda alone does not guarantee
escape or a regular connecting branch; those hypotheses remain indispensable.

Crucial physical boundary: (8) is a late-emission reception-horizon limit for
one pair of fixed histories. Areal R is not automatically observer-pair proper
separation or a finite X_max. The current owner asymptotic requirement does not
by itself identify its intended separation family with this experiment. Thus
Lambda>0 is a conditional candidate restriction, not an unconditional selection
by all UDT commitments. A horizon redshift is not automatically an additional
effect beyond physically matched GR, nor does it remove a cosmological expansion
interpretation merely by using a static chart.

## 4. Recovery can give a bound once its observable and tolerance are stated

Use the circular emitter's proper angular rate nu=Omega/sqrt(h), with the
rotational angle normalized to period2pi. Compare the Lambda and zero-Lambda
members at the same areal radius a and same m, matching these geometric data.
m can be distinguished geometrically by the Weyl invariant below; identifying
it with a physical source mass remains separate. This is an explicit comparison,
not equality of coordinate time scales across arbitrary metrics.

    (nu_Lambda²-nu_0²)/nu_0²=-Lambda a³/(3m).       (9)

If the stated tested-regime requirement for this squared proper orbital rate
is a supplied relative tolerance0<epsilon<1, then

    |Lambda|<=3m epsilon/a³.                       (10)

Combined with the particular divergent-clock realization above this gives
0<Lambda<=3m epsilon/a³, still subject to its other branch/orbit conditions.
No measured epsilon, physical mass scale or empirical exclusion is supplied
here. (10) is not a bound on every solar experiment, the received maser slope,
the whole GR filter or the positional contribution in every protocol.

## 5. Angular cancellation and DDR do not silently close the selection

On the positive-f primary domain G201/G260's native amplitude formulas give

    A_parallel=(r²f''-rf')/2=-3m/r,
    A_perp=1-f+rf'/2=+3m/r.                        (11)

Their trace cancels for every Lambda. This is an application of the existing
classification, not a new theorem or selection equation. It does not mean
the individual modes, finite optical map or Weyl curvature vanish. Their
positive-f native scope is not automatically extended beyond the chart. The
current sources supply no universal combined-response score or global departure
law that would make (11) a whole-UDT exclusion. In particular, (8) cannot be
relabeled as a demonstrated angular loud regime.

DDR acts on its specified response, not on every tensor one could build. In
R10's separately conditional class E_response=c1 Ric+c2 Rg the present family
gives E_response=(c1+4c2)Lambda g, so DDR supplies no further m/Lambda selection
within that class. CGE1 with m>0 is not a space form, however, so R9FST's
all-natural-response invariance argument cannot be imported here.

An explicitly UNADOPTED mathematical diagnostic makes this distinction concrete.
The curvature scalar I=C_abcd C^abcd=48m²/r^6 has I'=-288m²/r^7. The symmetric
metric-natural finite-jet tensor T_ab=(nabla_a I)(nabla_b I) is local and smooth
on the exterior but lies outside R10's order/weight class. With static orthonormal
U,N, T(U,U)=0 and T(N,N)=f(I')²>0, hence its contraction with R9's reciprocal
shape direction is2f(I')², not zero. This is not a proposed physical response
or UDT countermodel. It refutes only the claim that locality/naturality alone
make every such response automatically obey DDR on this nonhomogeneous family.
No principal/causal/recovery status is assigned to this diagnostic tensor.

## 6. Return to the actual commitments

Ordinary local clocks, metric causal signals and circumstance-dependent
observer universality are compatible with the constructed domain; they do not
alone add a parameter equation here. Reciprocity's completed-pair readout still
needs supplied physical comparison data. Strong local CSN is challenged, not
a selector; measured c_E/G_obs do not supply Lambda or X_max. The owner does
not require equal numerical outcomes for all observers in different circumstances.

The asymptotic and tested-regime commitments provide usable **conditional tests**:
the static patch fails the stated divergent-clock realization, the escaping
extension selects a positive sign for that realization, and a declared proper-
orbital tolerance imposes (10). Their physical attachment to UDT's additional
separation effect remains OPEN. No whole-postulate insufficiency, new-premise
necessity, native field-law admission or observation confirmation follows.
The next issue is that attachment, not another fit of a free redshift curve.
