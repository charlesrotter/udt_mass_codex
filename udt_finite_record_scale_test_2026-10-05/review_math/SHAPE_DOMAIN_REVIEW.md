# Source-first refinement: dimensionless admission and translated windows

Parent disclosed this refinement after SOURCE_FIRST.md, before a FRI1 parent
candidate was opened. The original length-box calculation remains preserved
as exploratory review history; the following is the reviewed stronger target.

Let mu=mH in [.005,.01], A=aH in [.05,.1], E in [1,10],
y=1/(HR) in [0,1/50000], B=Hb in [0,1/10000], and principal B_*=0.
Then w=Omega/H has 2<=w<9, h>=.4, f(a)>=.59. These are dimensionless
admission priors, not a known ruler or empirically inferred onset condition.
For z in [y,1/A], set s=sqrt(1+B^2(1-z^2+2mu z^3)). Crude bounds are
.999<s<1.001. The incidence equation is the dimensionless version of
SOURCE_FIRST.md. Its derivative is (1-wB)I with
I>=Imin=(10-1/50000)/1.001^3, and 1-wB>=.9991.
The root bracket at B=1/10000 beats the worst right-hand tail 9/50000.
Thus a unique smooth principal root exists on the entire closed y interval.

Write W=sqrt(1+(E^2-1)y^2+2mu y^3), D=Ey+W,
alpha_hat=1/D+WB^2/(1+s), j=WD B^2/(1+s). At reception,

    B'=[B/s+w alpha_hat/(W(1-wB))]/I,
    W<=1.00000002, W'<=.002, D<=1.00020002,
    alpha_hat<=1.000000006, B'<1, |s'|<.000101.

Primes are y derivatives along the actual root. The decomposition
alpha_hat=(1+j)/D gives |j'|<.000101 and therefore

    |(log F)'| <= w|B'|/(1-wB)+D'/D+|j'| <20,
    |K_length/H-1| <= 2e-8+(1+2e-8)*20/50000
                       =.000400020008 <1/2000.

This bound is a proof with exact inequalities; incidence samples are only
implementation checks. The rational script independently validates the
conservative inequalities. No parent implementation is imported.

Let Y=log Z-log nu_e, q bound |(log nu_e)'| in calibrated receiver length
time, and eta=1/2000. Equal-width translated means
M(t)=w_window^(-1) integral_(t-w_window/2)^(t+w_window/2)Y(s)ds obey
H(1-eta)-q <= M'(t) <= H(1+eta)+q, provided the entire support hull is
admitted. This uses differentiation of the translated integral, or Fubini;
it is not an approximation replacing an average by its midpoint. No extra
window term belongs in this particular interval theorem. This differs from
the arbitrary positive frequency-averaging protocol discussed initially.

For nominal center gap T, each true-center error <=sigma, per-reading
log error <=epsilon, and D the measured second-minus-first Y difference,
the robust inequalities are

    H(1-eta) (T-2sigma)-q(T+2sigma) <= D+2epsilon,
    H(1+eta) (T+2sigma)+q(T+2sigma) >= D-2epsilon.

Sharper standard endpoints, when H(1-eta)-q>=0 over the interval under
consideration, are

    H >= ((D-2epsilon)/(T+2sigma)-q)/(1+eta),
    H <= ((D+2epsilon)/(T-2sigma)+q)/(1-eta).

In fact those endpoints follow without assuming positive M' by first dividing
the per-true-gap inequality; however when D-2epsilon or D+2epsilon is negative,
the extremizing gap changes. A universally safe result must branch on those
signs or use the robust nondivided inequalities above. For the intended long
positive-drop synthetic record both numerators are positive. Require T>2sigma.
Intersect with H>0. If the lower endpoint is nonpositive there is no finite
upper bound on 1/H from this interval argument.

The protocol supplies logarithmic frequency-window readings; it does not derive
the material source, photon count, cycle resolution, angular centroid or
instrument. The source drift and angular reference remain substantive admitted
information. The phase endpoint/cadence limitations from TSI1 remain open.

No final verdict on parent numerical results is claimed here.
