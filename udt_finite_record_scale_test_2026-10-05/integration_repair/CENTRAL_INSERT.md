<a id="r16fri"></a>

#### Finite records: a bounded scale estimate and an explicit ambiguity — FRI1

R16TSI's infinite-time limit is no longer the only conditional calibration
route. FRI1 proves a finite error enclosure and constructs finite timing AND
angular records compatible with two scales differing by factor2. Which result
is useful depends on the admitted class, uncertainty and coverage. Neither is
an astronomical measurement or native selection of the metric.

Use ordinary calibrated receiver length ell=c_E tau_seconds. Keep the inherited
principal b_*=0 histories and define mu=mH, A=aH, y=1/(HR), B=Hb,
w=Omega/H=sqrt(mu/A³-1). A here is source-radius notation, not frequency.
The explicitly supplied, scale-invariant conditional domain is

    mu in[.005,.01], A in[.05,.1], E in[1,10], 0<y<=.00002.

H>0 remains free. These are free-and-explored shape/tail conditions, not an
inferred source ruler or native prior. The entire support hull of the records,
including gaps, must lie in this domain. The data do not establish that tail
membership. h>=.4, f(a)>=.59 and2<=w<9 keep the source regular.

The actual incidence equation is P-w Uhat=w dhat, where

    s(z,B)=sqrt(1+B²-B²z²+2mu B²z³),
    P=int_y^(1/A) B/s dz, Uhat=int_y^(1/A) B²/[s(1+s)] dz,
    W=sqrt(1+(E²-1)y²+2mu y³),
    dhat=int_0^y dz/[W(z)(Ez+W(z))], I=int_y^(1/A) dz/s³.

On0<=B<=.0001, .999<=s<=1.001 and dhat<=y. The incidence derivative
(1-wB)I exceeds J0=(1-.0009)(10-.00002)/1.001³. The incidence left-hand side atB=.0001
exceeds the target9y, so there is a unique root in this interval, B<=9y/J0.
This proves a uniform small-B branch; it is not uniqueness among all images.

Let D=Ey+W, alpha=1/D+WB²/(1+s), j=WD B²/(1+s),
F=(1-wB)/(sqrt(h)alpha), so Z=F/y. Differentiating the actual incidence gives
B'=[B/s+w alpha/(W(1-wB))]/I. The stated box yields B'<1,
W<=1.00000002, W'<.002, D'<=10.002, alpha<=1.000000006 and
|j'|<.000101, including actual B' contributions. Since alpha=(1+j)/D,
|(log F)'|<20. Therefore

    |(dlog Z/dell)/H-1| < .000400020008 < eta=.0005.       (FRI1-1)

The continuum argument and exact rational inequalities own this bound, not
a grid of samples. Original-equation numerical checks support its application.
The declared radial frame also gives a conservative |dtheta/dell|<H/20000;
a sharper special-shape bound H/290000 is used for the factor2 witness.

Records are finite equal-width translated window means. Timing measures the
mean of Y=log Z-log(nu_e/nu_ref), where nu_e is evaluated at the actual
emission map and nu_ref is a constant. Impose the explicit receiver-length
source-drift bound |dlog nu_e/dell_o|<=q. An emitter-time bound would need
the1/Z conversion. Stable-source or labeled proper-clock records allow q=0.
Each reported mean has deterministic error epsilon_z; the analogous angle
record is an arithmetic mean of signed theta, not mean log-angle. The angular
frame is fixed. These error/readout conditions are supplied interfaces, not
derived instruments, material clocks, source visibility or Gaussian likelihoods.

The derivative of a translated mean is the mean of the derivative, so the
same interval H(1-eta)-q<=Ybar'<=H(1+eta)+q applies to finite windows.
No extra finite-width bias appears in this specific equal-window protocol.
Let the reported centers differ by T>2sigma, with each true-center error at
most sigma. Let d be the reported mean difference and Tminus=T-2sigma,
Tplus=T+2sigma. Define the sign-safe rate interval

    rlo=min((d-2epsilon_z)/Tminus,(d-2epsilon_z)/Tplus),
    rhi=max((d+2epsilon_z)/Tminus,(d+2epsilon_z)/Tplus).

Every admitted history consistent with these records has

    H in [max(0,(rlo-q)/(1+eta)),(rhi+q)/(1-eta)] intersect(0,infinity). (FRI1-2)

This permits the full supplied shape/motion range. It is a conservative enclosure,
not a guarantee that every enclosed value is realizable or all other parameters
are identified. Arbitrary source drift, frame rotation or unknown window width
falls outside its hypotheses. c_E converts seconds to length units; G supplies
no independent constraint without its open physical mass/density interface.

The explicit ambiguity uses m1,a10,H.005,E1,R(0)=20000000 and its factor2
homothety m2,a20,H.0025,E1,R(0)=40000000. They have identical initial Z and
theta but are evaluated at the SAME calibrated times. A small backward-support
bound keeps all windows inside the admitted tail. Use five centers from0 to1.6,
window width.1, log-mean error.003, angular error5e-8rad, each timestamp error
.001T. Take each reported value to be the midpoint of the two center values;
constant sources and zero realized timestamp error are allowed members.
Uniform derivative bounds prove both actual window means fall inside the same
error bands. The proof includes each mean's displacement from its center value;
it does not substitute instantaneous records for finite means.

The result is substantive: two distinct H, hence two lengths1/H differing by2,
are compatible even with both channels and a stable source. They are not exactly
equal noiseless timed curves. It disproves universal recovery at this finite
coverage/uncertainty, not all finite recovery or UDT itself.

For the longer fixed interval T=200 with the same widths/readout errors,
timestamp error.2 and allowed source drift q=.000005, synthetic base records
give H in[.0049725836,.0050676842] for the supplied H=.005. Repeating withE10
gives[.0049722999,.0050673991]. The widths are about1.902% of the input H;
these are total deterministic interval widths, not one-sigma error bars.
Both exclude.0025. The paired long angular records also separate beyond their
declared errors, but no all-parameter angular inverse theorem is claimed.
All numerical units, schedules and errors were frozen controls; none is an
observed Hubble rate or a measured instrument capability.

The [initial argument](udt_finite_record_scale_test_2026-10-05/INITIAL_CANDIDATE.md),
[work record](udt_finite_record_scale_test_2026-10-05/WORK_RECORD.md) and
[descendant review](udt_finite_record_scale_test_2026-10-05/DESCENDANT_REVIEW.md)
preserve the exact bounds, actual finite records, review exposure and limits.
Finite conditional inversion is now established for the stated domain and
interfaces; real tail/source/error admission and native geometry selection
remain open. Matched GR gives the same records. The [return brief](udt_finite_record_scale_test_2026-10-05/DECISION_BRIEF.md)
proposes checking those physical interfaces before claiming empirical scale.
