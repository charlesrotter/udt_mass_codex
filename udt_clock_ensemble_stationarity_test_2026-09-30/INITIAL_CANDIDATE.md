# CES1 conditional nonstationarity of the prepared clock ensemble

Initial candidate, not adopted physics. The preparation was frozen in
PREPARATION_FREEZE.json before this explicit calculation. The proposed L1 law,
counting measure and exact Minkowski-stationarity benchmark are supplied choices.
In particular, exact global Minkowski stationarity is not synonymous with local
SR recovery. The founding UDT interpretation and existing grades are unchanged.

## Claim and fixed inputs

For every product probability measure and positive rapidity interval specified
in PREPARATION.md, there is an admissible compact reciprocal variation at the
Minkowski metric for which

    δC = 2 B0 <η> > 0,
    C[g;p,U,μ] = (1/2) ∫ (log Z[g,Q_g(q)])² dμ(q).

Here B0=∫_a^b b0(r)dr>0 and the average uses the fixed normalized rapidity
density. The shorthand C[g] suppresses laboratory and preparation data. They
are neither a native population nor an automatically metric-local selection.
This refutes stationarity against every compact reciprocal strain for this
specified family. It is not an all-ensemble theorem or a UDT/SR refutation.

## Actual preparation and endpoint terms

Use the frozen physically specified initial separation, direction and rapidity,
emitter proper emission time s, and ordinary freely falling clocks. The test
metric is exactly flat on a neighborhood of the entire preparation slice and
both relevant clock histories. Therefore the spacelike preparation geodesic,
its parallel transport, the initial timelike tangents and the subsequent clock
worldlines are exactly unchanged, by uniqueness of the geodesic initial-value
problem. This holds on the finite histories containing all arrivals, uniformly
for small strain. Proper rates on those worldlines are also unchanged. These
terms vanish by support, not by freezing coordinate meaning artificially.

At the baseline write v=tanh η, receiver r=L+vt, and proper receiver time
τ=t sqrt(1-v²). Its coordinate and proper arrival times are respectively T(s)
and A(s)=sqrt(1-v²)T(s). Although the worldline is unchanged, the arrival event
moves. This term cannot be omitted. The label measure dμ is fixed; all metric
dependence of physical queries belongs to Q_g. No spacetime pushforward with
an omitted Jacobian is substituted for the specified integral.

## Null interception calculation

For the outgoing radial null curve of the exact frozen metric,

    dt/dr = exp(2 ε f(t,r)),    t(0;s)=s.

In the shell the baseline curve has t=s+r and χ=1. If u=∂ε t|0 then

    ∂r u=2(s+r)b0(r),    u(0;s)=0.

Put B1=∫_a^b r b0(r)dr. Outside the shell,

    tε(r;s)=s+r+2ε(s B0+B1)+O(ε²).

The interception radius is Rε=L+v Tε, so the baseline and variations are

    T0=(s+L)/(1-v),       R0=(L+v s)/(1-v)>L>b,
    δT=2(s B0+B1)/(1-v),
    A0=e^η(s+L),         δA=2e^η(s B0+B1).

The receiver is receding, η>0, and sqrt(1-v²)/(1-v)=e^η. Differentiating
the proper arrival map with respect to the emission proper time gives

    Z0=A0'=e^η,          δZ=2e^η B0,
    D0=log Z0=η,         δD=δZ/Z0=2B0.

Consequently δC=∫D0 δD dμ=2B0<η> ≥ 2B0 η_->0. The arbitrary normalized
s/L/direction weights integrate to one. No selected numerical weight or fitted
profile makes the sign. The squared contrast includes ordinary Doppler shifts;
the specified strain changes that contrast in the same sign for this ensemble.
Changing the metric, not an abnormal local clock mechanism, changes the arrival.

## FCV1 cross-check with physical clock labels

Parameterize both clocks by proper time, so their lapse factors are one. Let
λ run from0 to1 along the baseline ray; k=R0(1,n) and
u_receiver=(cosh η,sinh η n). For h=2f(dt²+dr²),

    ω_receiver=−g(k,u_receiver)=R0 e^(−η),
    I[h]=(1/2)∫_0^1 h(k,k)dλ=2R0(s B0+B1).

FCV1 gives V=δA=I/ω_receiver=2e^η(s B0+B1), since the fixed-label worldline
and proper-rate variations actually vanish. Its tick-contrast response is
V'/A0'=2B0. Differentiation carries the s dependence of R0 in both I and ω;
dropping the denominator derivative would be erroneous. This is a second route
through the existing full-variation formula, not a separate physical premise.

## Admissibility and differentiation

b0 and χ are smooth compact controls. The shell avoids the coordinate origin,
so the metric and h extend smoothly in Cartesian coordinates. The metric is
Lorentzian, t is temporal, and h=fH has exactly the existing reciprocal factor
two and zero metric trace. Its finite t-r determinant is −1. The laboratory
center is supplied query data; no universal center or physical wall is asserted.

The compact label set has 1-v≥1-tanh η_+>0. Smooth dependence of the radial
ODE and the transverse receiver intersection gives a uniformly regular branch
for sufficiently small |ε|. The plateau contains an open neighborhood of every
baseline crossing; compactness supplies a common small strain interval that
keeps crossings inside it. Smooth parameter dependence also holds after one
s derivative, giving a uniform O(ε²) remainder for Z. Positivity of Z persists.
All resulting derivatives are bounded on the compact set, justifying their
interchange with the finite label integral. The exact first variation, not a
finite-strain numerical approximation, owns the conclusion.

## Solver-first diagnostic and limits

The original null equation, interception with a moving receiver, proper clock
normalization, preparation and worldline support, fixed label measure, compact
reciprocal strain and regular branch have all been carried explicitly. The
perturbed metric is an off-shell variation, not an asserted physical solution.
Restricting variations to already stationary solutions would change the test.
The positive derivative suffices without assuming that a full smooth volume
response tensor exists. If such a tensor and the proposed all-pair stationarity
were present, this derivative would have to vanish.

The benchmark fails. Stop this candidate before claiming smooth response,
finite-jet locality, dynamical stability or empirical GR recovery. Ordinary
local clocks and metric SR behavior remain intact; exact global stationarity
of this supplied functional is a stronger, unadopted demand. Other ensembles,
different physically justified population rules or response identifications
are not excluded. No weight adjustment, GR subtraction or replacement law is
offered as a repair. The physical stationarity identification and native
ensemble selection remain open. This result narrows a proposed connection;
it neither closes the native positional-prediction join nor proves that the
founding postulates are insufficient.

Evidence: PREPARATION.md owns the frozen experiment and controls; the reviewed
FCV1 full-variation result and central R6/R9 own the conditional interfaces.
The producer's symbolic checks validate algebra, not physical adoption, and
fresh separate-context review is required before banking this candidate.
