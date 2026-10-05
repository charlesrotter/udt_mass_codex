# FRI1 source-first mathematics review

Reviewer: fresh separate Codex context `/root/fri_math`, inherited GPT-6 family;
no claim of a different model. Parent startup is attributed, not independently
repeated. I independently read AGENTS.md, work order, the required CLAUDE.md
sections, triggered no-shortcuts/completeness-map/verifier-before-record skills,
central R8CPR/R16TSI and the CPR1/TSI1 candidate sources. Actual local branch was
`grok`, HEAD `37c0864880b1c336247a403b84d1eba1896995ce`; no tracked dirt was shown
at entry. Protected/unrelated names were visible only through git status.
The new package was untracked. Parent reports synchronized origin and startup
premise checks; I do not claim to have independently fetched or run that audit.

Exposure: parent disclosed the proposed late uniform bound, parameter box and
factor-two histories at dispatch. No FRI1 candidate implementation, outputs or
candidate argument had been opened when this note was written. The argument
below is independent algebra from owned sources, not blind to that lead.

## Scope and source-first findings

All statements are conditional on supplied CPR1 geometry, principal preparation,
outgoing incidence and calibrated receiver time. Parameters and experimental
protocol are free-and-explored synthetic controls. No native/empirical admission,
source law, mass interface, physical X_max or additional matched-GR effect follows.

Put Q(y)=H^2-y^2+2my^3, s(y,b)=sqrt(1+b^2 Q(y)), and
V(y)=sqrt(H^2+(E^2-1)y^2+2my^3). Principal incidence is the unique small positive
root of

    G(b,x)=integral_x^(1/a) [b/s-Omega b^2/(s(1+s))]dy
           -Omega integral_0^x [1/(V(Ey+V))]dy = 0.

Its derivative is G_b=(1-Omega b)I, I=integral_x^(1/a)dy/s^3. Differentiating
the actual angular incidence and emitter arrival equations gives

    b' = [b/s(x,b)+Omega alpha/(V(1-Omega b))]/I,
    alpha=1/(Ex+V)+Vb^2/(1+s(x,b)).

These are consistent with CPR1. In particular, freezing b=0 at finite x would
be an incorrect orbiting-source derivative.

For m in [1,2], a in [10,20], H in [1/400,1/200], E in [1,10],
0<=x<=1e-7, the source conditions hold uniformly: h>=.4, f(a)>=.59,
Omega^2>=.0001 and Omega<.045. On 0<=b<=.02 and y<=1/a<=.1,
.9999<s<1.000001, I>.04999 and 1-Omega b>=.9991.
G(0,x)<=0 while G(.02,x)>0: the positive integral is >.0009995 and
Omega*d(x)<=.00072. Strict G_b>0 proves a unique admissible root throughout
this entire compact rectangle, not merely an infinitesimal IFT branch.

A rational-arithmetic bound check will validate the following conservative
constants, independently of sampled incidences: V<=.005000001, V'<=.004,
alpha<=400.000002, b'<=145000. At reception |s'|<.074. Write
alpha=(1+j)/D with D=Ex+V and j=VD b^2/(1+s). Then

    |(log alpha)'| <= D'/D+|j'|,
    |j'| <= (V'D+VD')b^2/(1+s)
            +VD[2b|b'|/(1+s)+b^2|s'|/(1+s)^2].

This gives |F'/F|<10600 for F=(1-Omega b)/(sqrt(h)alpha).
Also V/H-1<=8e-8, so

    |K_length/H-1| <= 8e-8+(1+8e-8)*10600*1e-7 < .0011.

The bound proves an interval only for histories admitted to this very late
principal class. It cannot diagnose that admission from finite noisy data.

## Records, window, time and source objections to check

If y=log(nu_o)=constant+d-log Z and |d'|<=rho in receiver length time, then
|y'|<=H(1+eta)+rho. A positive normalized average of nu_o over a support within
w of a reported center differs in its logarithm from y(center) by at most
[H(1+eta)+rho]w. The same statement for a log-frequency average is immediate;
an arithmetic average of frequency must use positivity and bounding between
the extremal frequencies. These are distinct protocols that must be named.

For a pair of centers separated by T, log-frequency errors <=epsilon, uncertain
centers <=delta and support half-width w, the observed log drop D obeys

    |D-H T| <= eta H T + rho T
              +2 epsilon+2[H(1+eta)+rho](w+delta).

An equivalent formulation using the true elapsed time must put the uncertainty
in the denominator explicitly. One must not count a nominal calibrated time
as exact while only bounding frequency error. With eta<1 and T>2(w+delta),
this rearranges to a finite positive H interval when its numerator allows it.
Receiver-time source drift is extra record admission. A bound in emitter
proper time is different and requires division by Z.

Fixed emitter cadence still gives only finitely many available pulses before
the finite emission endpoint. A finite window cannot be called a measured
frequency without separately supplying phase/cycle-resolution assumptions;
the synthetic protocol may explicitly supply frequency observations, but then
it remains conditional. Positive windows and finite cadence do not themselves
produce a physical source interface.

Two homothetic histories compared at fixed calibrated times are not exactly
degenerate, but finite error boxes can overlap after matching their initial
normalizations. A coordinatewise midpoint of two allowed finite records is a
constructive common data record if each half-difference is within the declared
error. Such a witness proves compatibility, not exact identifiability failure
for perfect finite records. With unconstrained source drift, timing alone can
be matched exactly by choosing allowed frequency histories; adding a bound
rho restricts this freedom and is substantive prior information.

Angular error must be specified as absolute angle or logarithmic/relative
angle. The leading principal angle tends to zero, so an absolute angular
noise floor is not a fixed relative-noise bound. Cadence, angular reference,
source centroid and sign/unwrapping must remain stated. A fixed finite
ambiguity witness does not establish ambiguity for every duration or precision.

This is a source-first analysis, not a final verdict on the evolving package.
