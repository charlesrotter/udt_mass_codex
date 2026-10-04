# GRL1 mathematical exposed review

Verdict: **VERIFIED-WITH-CAVEATS** for the two conditional mathematical results
and bounded physical-implication audit in INITIAL_SYNTHESIS.md, SHA256
`c22dba85f79bb91334cad3f89ead99e0d1974f0aeebbe123f80c96efd5d56260`.
Two local precision repairs are requested below. Neither changes the core
rigidity theorem or drift coefficient; neither establishes a native physical
assignment. Final integration is not yet reviewed.

Reviewer `/root/grl_math`, 2026-10-04. Fresh context relative to the parent;
same inherited model family, exact revision unexposed; not a different-model
or human review. SOURCE_FIRST_SEAL.json fixed the reconstruction before any
candidate content or lane reports were read. Parent candidate-freeze announcement
preceded this seal but supplied only its path/hash; this is recorded in EXPOSURE.
After sealing I read the frozen candidate, TEST_PLAN and all three lane REPORTs
and source ledgers. Their additional literature claims are exposed, not silently
counted as my own primary-paper inspections. My five primary papers and original
inspection limits remain recorded in the source-first file. No sibling review
has been read. No scientific CPU or GPU calculation was run; checks below are
independent hand derivations rather than a rerun of shared code.

## T1: reconstructed proof and exact controls

Take a g0-orthonormal basis and write a symmetric bilinear form g as blocks
`(a,b^T;b,D)`. Cone equality says `a+2 b.n+n^T D n=0` for every unit n.
Opposite n force b=0; evaluating basis directions and their pairwise sums
forces D=-a I. The common sign convention yields g=lambda g0, lambda>0.
Smooth metrics give smooth lambda and f=(1/2)log lambda. This proves the
pointwise conformal step without using an operational reconstruction theorem.

The Koszul formula gives

    C(v,v)=2 df(v)v-g0(v,v) grad0 f.

A common unparameterized geodesic has C(v,v) parallel to v. A timelike v has
nonzero g0(v,v), so grad0 f is parallel to v. Two nonparallel timelike
directions suffice to make it zero. With all timelike directions available,
this holds at every point; connectedness makes f constant. Constant scaling
does not change the connection or null correspondence and scales both actual
proper intervals equally, so their received ratio is unchanged. One actual
absolute proper-time calibration fixes the remaining positive constant, but
this is not needed to obtain equal received ratios.

For the candidate's `g=exp(2H eta)eta`, f=H eta and
`grad0 f=-H partial_eta`. Coordinate-rest curves have acceleration parallel
to their tangent before proper normalization, and are unparameterized
geodesics. The normalized vector is exp(-H eta)partial_eta. A tilted vector
`v=partial_eta+b partial_x` gives

    C(v,v)=H(1+b^2)partial_eta+2Hb partial_x.

For 0<|b|<1 it is not proportional to v: proportionality from the x component
would require time coefficient2H rather than H(1+b²). For rest clocks the
null incidence eta_o=eta_e+L and d tau=exp(H eta)d eta give exactly
`Z=exp(HL)` versus1 in the flat comparator. This is a correct counterexample
to replacing rich timelike path data by one congruence; it is not an admitted
UDT countermodel or a parallel-prepared comparison between the two metrics.

**Objection M1 — necessity wording.** The heading “The all-direction clause is
essential” is too strong if read as asserting mathematical necessity of every
direction. The proof above shows that two nonparallel timelike common tangents
at every point already suffice after cone matching. The survivor is the stated
all-direction sufficient theorem and the failure of a single congruence.
Smallest repair: label it “One common congruence is insufficient” and explicitly
describe all-direction agreement as a sufficient rich-data assumption. No
larger reconstruction theorem or minimal-data classification is requested.

The physical conclusion is appropriately bounded. Neither W4 nor an empirical
GR filter supplies this exact complete reference agreement. Failure to infer
it from the inspected sources is not a proof that the full UDT postulates are
insufficient. The extra received ratio cannot be bolted onto identical complete
metric/protocol data, but the result does not locate or quantify a permissible
physical deviation.

## T2: independent local derivation, including the differentiated remainder

Use Fermi coordinates (t,X) of the observer's geodesic; t is its proper time.
For a smooth geodesic congruence agreeing with that observer at X=0, the
coordinate velocity field has

    V(t,X)=B(t)X+O(|X|²),
    A(t,X)=-T(t)X+O(|X|²).

The second relation follows directly from the geodesic equation:
Gamma^i_00=T_ij X^j+O(|X|²), while terms containing a spatial velocity are
O(|X|²) because V=O(|X|). The coordinate/proper-time normalization differs
from1 only at quadratic order. No zero-shear, zero-vorticity or Einstein
equation is used.

Here is an explicit way to control differentiation. Label nearby fixed source
curves by their initial displacement epsilon n. On a sufficiently short compact
observer-time interval their positions have smooth dependence

    X(t,epsilon,n)=epsilon A(t)n+O_C1(epsilon²),
    A(t0)=I, A'(t0)=B(t0), A''(t0)=-T(t0).

Shrink the interval so |A(t)n| is bounded below uniformly on the unit sphere.
Set t_e=t-epsilon s in the source-observer null world-function equation and
divide by epsilon². Its smooth limiting equation is
`[-s²+|A(t)n|²]/2=0`. The positive root is simple: its s derivative is
`-|A(t)n|`, bounded away from zero. The implicit-function theorem therefore
gives a smooth scaled retarded incidence in t,epsilon,n. Taylor expansion is
uniformly C1 in reception time, not only a pointwise O(epsilon²) statement.
The smooth metric frequency contractions, normalized by the same nonzero
leading null scale, give

    z=n_X.V+O_C1(epsilon²),

where X,V,n_X are simultaneous reception-time Fermi data of that fixed source.
Retardation changes the leading radial velocity only at quadratic order. The
Fermi lapse corrections are also quadratic. Thus at t0, with r=|X|,

    dot z=n_X.A+(|V|²-(n_X.V)²)/r+O(r²)
         =r[-T(n,n)+|P_n Bn|²]+O(r²).

This supplies the claimed C1 control in a fixed smooth congruence and regular
short branch. It does not supply a finite-size error constant, bounds uniform
over arbitrary metrics/congruences, survey convergence, or a global source
population. Smoothness and a common local tube are doing real work here.
At only one event setting a=0 would be insufficient; the candidate correctly
assumes geodesic worldlines in the neighborhood.

For the sphere average, write S=H I+sigma and B=S+W. Direct moments give

    <|Bn|²>=tr(B^T B)/3=H²+sigma²/3+W²/3,
    <(n.Bn)²>=[(tr S)²+2 tr(S²)]/15=H²+2sigma²/15.

Their difference is sigma²/5+W²/3. Since tr T=Ric(U,U), the corrected
monopole is exactly `M=-Ric(U,U)/3` at the limiting coefficient level.
This is a uniform mathematical sphere average; a triad or finite sky sample
does not automatically compute it. Division by H(n) is justified only where
H(n)!=0; the r formulation remains usable in zero-leading-redshift directions.

## T2 adverse control recomputed from incidence

In the supplied flat congruence X(t,q)=q+tBq, B=diag(2h,h,h), choose an emission
event at (-r_E,r_E n_E), received at the origin at t_o=0. Its fixed source label
is q=(I-r_E B)^(-1)r_E n_E and v=Bq. With hr_E<1/8,
`||v||<=2hr_E/(1-2hr_E)<1/3`; all required inverse matrices and null branches
are regular. The sources are straight timelike curves, and the central observer
is inertial. Differentiating t_o=t_e+|q+t_e v| for that same fixed q gives

    dt_e/dt_o=1/(1+n_E.v),
    dot n_E=P_n_E v/[r_E(1+n_E.v)],
    Z=gamma_v(1+n_E.v),
    dot Z=gamma_v |P_n_E v|²/[r_E(1+n_E.v)].

Here v and gamma_v are constants when differentiating, rather than being
reselected at every tick. Expanding v=r_E Bn_E+O(r_E²) gives
`J=h² n_1²(1-n_1²)`. Independently, <n_1²>=1/3 and <n_1^4>=1/5, so
`<J>=2h²/15`. The congruence has sigma²=2h²/3 and W=0; M=0=Ric(U,U).
The raw-positive-sign inference is therefore genuinely defeated by a direct
arrival-map calculation, not by substituting a target curvature formula.

**Objection M2 — emission and reception separation labels.** The candidate
defines r,n as simultaneous reception-time Fermi separation/direction, then
uses the same labels for retarded emission position in this exact control.
They differ at finite r. The displayed exact control is correct in emission
labels. At reception X(0,q)=q, so

    r_F=|q|=r_E+O(r_E²),
    n_F=q/|q|=n_E+O(r_E).

Consequently the limiting J and sphere average survive. Smallest repair: use
r_E,n_E in the exact control and record this conversion before identifying
its limit with T2. There is no need to change the theorem or compute a finite
correction series.

The common-time versus received-clock check also passes independently:
for Y:x=0 and X:x=L+vt, `t_r=(t_e+L)/(1-v)` and
`Z=sqrt(1-v²)/(1-v)`. The v=±3/5 examples have equal common-time rate4/5
but actual ratios2 and1/2. This blocks a protocol substitution; it is not a
claim that the literature's corrected measurement scheme is invalid.

## Source fidelity, prior overlap and limits

The source-first ultrastatic line×curved-surface calculation independently
supports quarantining the external v1 quadrupole. T2's local Fermi/Jacobi
argument and scalar sphere average do not depend on that printed coefficient.
No general repair or verdict for the whole external paper is required for this
candidate. In particular, avoid promoting the review's source-adversarial
control into an adopted new GRL1 connection.

The synthesis preserves the distinctions established in D1, W4, R6/R7,
PSW/J1, NCI, ECS, ACI and R13/R14. Clock/tidal reconstruction can test independent
records but does not identify DDR's symmetric response or exclude other
response channels. A positive corrected M would imply negative Ric(U,U) for
this experiment; the current owner statements do not require that M. A global
asymptotic slowing family is not a reception-time derivative at one event.
Luminosity/flux uses need their own physical readout assumptions. No action,
Einstein source equation, observer population or local X_max input is supplied.

I reviewed the three lane reports as synthesis inputs, not as ten independent
paper re-proofs. The five papers outside my directly assigned primary set remain
lane-attributed. No full current-premise verifier, historical numerical replay,
all20 compass-coefficient audit, all higher-order drift check, observation or
formal machine proof was performed by this reviewer. Parent startup/full406
attribution remains distinct from my substantive mathematical checks.

Both precision repairs are source-preserving and same-premise. Once incorporated,
the conditional mathematical candidate can retain VERIFIED-WITH-CAVEATS with
the explicit operational/error/adoption limits above. The result is review of
this bounded candidate, not canonical acceptance or proof of empirical truth.
