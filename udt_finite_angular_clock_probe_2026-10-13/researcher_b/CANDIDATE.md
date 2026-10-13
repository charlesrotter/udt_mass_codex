# FAC1 B — independent finite clock reconstruction and recovery screen

Status: contributor candidate for fresh review. Supplied-metric mathematics and
numerical evidence only; AMS/RUS remain UNADOPTED. The central development is
owned by the coordinator. No UDT metric, scale, source, positional attribution,
registry grade or canon is selected here.

## What changed

An original-coordinate finite integration, completed before exposure to A's
symbolic coefficients, found **positive spherical means in both independent
first-signal directions** for the chosen Ricci-flat Kasner laboratory. FPC1's
negative principal-axis outgoing mean is therefore not a guide to this sphere.
After exposure, the independent numerical values corroborate A's coefficient
4/1215 at their numerical scope; A's analytic argument owns the exact expansion.

Actual re-preparation in the parent's smooth conformal controls then gives either
small-L mean sign while the metrics recover Kasner smoothly. At one finite
preparation the two means even have opposite signs while their combined mean is
positive. Thus the combined statistic considered in B's initial proposal would
hide reverse speeding. This is a concrete reason to retain both actual records.

## Independent numerical construction

INITIAL_APPROACH and NUMERICAL_FREEZE precede the first scientific run. The
original implementation and all three first captures (vacuum baseline/fine and
flat control) precede receipt of A's coefficients. Subsequent exposure and
redirection are recorded in EXPOSURE_AND_NEXT_PROBE. No sibling code or derivation
was used to implement the original solver.

For the diagonal homogeneous supplied metric

    g=-N(t)^2 dt^2+sum_i a_i(t)^2 (dx^i)^2,

spatial translations give constant momenta. The spacelike exponential curve and
parallel transport of U are integrated in the original coordinates, with all
three spatial components retained in the equations. They supply the actual B0,
velocity and free-receiver momenta P. A null ray has constant spatial momenta q
and W=sqrt(sum q_i^2/a_i^2). Its coordinate tangent is

    dx^i/dt=N q_i/(a_i^2 W).

The outgoing solve matches this null displacement to the independently evolved
receiver displacement. The reverse solve starts at B0 and meets A. It is not an
immediate echo from the outgoing reception. The actual endpoint frequency is

    omega=W gamma-sum_i q_i P_i/a_i^2,
    gamma=sqrt(1+sum_i P_i^2/a_i^2).

For A, P=0. Ratios are omega_emit/omega_receive. The normalization of q cancels.
The resulting p derivatives hold the actual worldlines fixed.

These are the original geodesic equations, not a fitted clock curve. For example
W W'=-sum_i (a_i'/a_i)q_i^2/a_i^2 makes the t-component null geodesic equation
vanish after substituting k^t=W/N; the spatial equations cancel against the
two connection terms. The timelike momentum representation analogously satisfies
normalization and geodesicity. The separate spacelike/transport ODE residuals,
endpoint incidence and normalization checks remain essential.

Kasner exponents are (-1/3,2/3,2/3), with A at t=1. Axial rotations and spatial
reflections are isometries preserving the entire experiment. They justify the
exact angular reduction n=(mu,sqrt(1-mu^2),0) and mean integral_0^1 dmu, rather
than replacing the sphere by principal axes. The same original preparation solid
angle is used for both senses; it is not the receiver sky.

## Vacuum evidence and its scope

Fine runs use float64, DOP853 rtol4e-14/atol4e-16, angular Gauss order48 and
time quadrature order64. Baseline uses angular24/time32 and looser ODE tolerances.
Saved JSON retains every direction, root, initial state and residual.

| L | M_plus | M_minus |
|---|---:|---:|
| .08 | 1.3529550203e-7 | 1.1658590679e-7 |
| .06 | 4.2822697071e-8 | 3.8229171762e-8 |
| .04 | 8.4558220869e-9 | 7.8293222055e-9 |
| .03 | 2.6742089516e-9 | 2.5228466080e-9 |
| .02 | 5.2787098318e-10 | 5.0757335687e-10 |

The maximum baseline/fine mean discrepancy is6.68e-16. Flat exponent controls
give zero means. Published FPC1 outgoing axis expansions leave remainders
consistent with their O(L^5) scope. After exposure, A's full angular forward
expansion agrees with the independent numerical data with bounded observed
remainder/L^5 over the tested range. This is numerical corroboration, not an
interval enclosure, proof of an exact coefficient or generic Ricci-flat theorem.

The bounded continuation L=.2,.4,.6,.8 also yields both positive means in saved
fine records. It did not change the sign decision, so no larger range was
searched. That supplementary run has original residual checks but no angular
refinement or general analytic finite-branch certificate. It establishes neither
monotonicity nor all-range positivity and is not needed for the local proof.

## Actual-clock recovery controls

The parent proposed f_epsilon=epsilon(t-1)^2/2 and
g_epsilon=exp(2f_epsilon)g_Kasner before this branch was executed. B implemented
that exposed proposal as N=exp(f), a_i=exp(f)t^r_i and re-integrated the complete
preparation for each epsilon. Keeping coordinate clocks from vacuum would have
been a different experiment. No such shortcut was used.

At t=1, f=df=0. The standard conformal Ricci formula gives
Ric_epsilon(U,U)=-3epsilon; the parent's proof owns the detailed exact argument.
PSW/FAC1 then give both means epsilon L^2/2+O(L^3) for each fixed epsilon.
Consequently either local mean sign is compatible with smooth metric recovery.
This is not adoption of a physical conformal field or a new source equation.

Selected refined actual records:

| epsilon | L | M_plus | M_minus |
|---:|---:|---:|---:|
| -1e-4 | .02 | -1.9516271904e-8 | -1.9536473989e-8 |
| -1e-4 | .08 | -1.8747860461e-7 | -2.0615906804e-7 |
| -1e-4 | .16 | 8.4953234374e-7 | 3.2237607115e-7 |
| -1e-5 | .02 | -1.4765433515e-9 | -1.4968314244e-9 |
| -1e-5 | .04 | 4.2073426068e-10 | -2.0560257550e-10 |
| -1e-5 | .08 | 1.0301809130e-7 | 8.4311409272e-8 |

Both positive epsilon values give positive recorded means at every frozen L.
The negative grids were repeated at baseline settings; the largest change is
2.36e-15. Every displayed negative/positive value is more than50 times its
refinement discrepancy. At epsilon=-1e-5,L=.04 the combined mean is+1.07566e-10,
despite the negative reverse mean. These are separated numerical signs, not
rigorously enclosed values. Exact formulas and the parent smooth-dependence
argument own any analytic asymptotic claim.

The useful two-parameter implication is conditional on smooth uniform local
remainders. With c=4/1215, smooth dependence and A's vacuum expansion give

    M_±(epsilon,L)=epsilon L^2/2+c L^4+O(|epsilon|L^3+L^5).

For epsilon=-delta and L=s sqrt(delta), the scaled mean tends to
-s^2/2+c s^4 for each fixed positive s. Thus negative near-onset means and positive
larger means can coexist with recovery to a positive-mean vacuum control, with
the crossover approaching zero. This strengthens the original proposal's warning
about noncommuting small-L and recovery limits. It does not refute continuity at
fixed finite L, which holds. It also does not support the initially anticipated
negative-GR-control no-go: this inspected GR control has positive means.

## Direct observable check

ARRIVAL_CHECK_FREEZE preceded a second numerical arrangement. Holding the same
worldlines fixed, it re-solves null incidence at perturbed emission times and
integrates the actual endpoint proper times. Twenty-four comparisons cover both
first directions, three generic angles, vacuum and one deformed case, and two
finite-difference steps. The arrival derivatives agree with endpoint-frequency
ratios to1.12e-12; incidence residuals are below1.18e-16. This checks the physical
definition and reverse timing. It shares the preparation code and libraries and
is not a wholly independent implementation or a mean-error certificate.

## Physical decision

The supplied Ricci-flat control demonstrates that finite positive averaged
received slowing need not be an additional UDT effect. It defeats the inference
from zero leading Ricci mean to no finite spherical mean. Positivity at this
one laboratory does not make AMS automatic for every vacuum geometry, observer,
directional record or finite separation.

Conversely, if AMS were physically justified on a stated small-L regime, it
would be a nontrivial conditional restriction: the negative-epsilon controls
violate it despite arbitrarily smooth recovery to this vacuum comparator.
No inspected source turns that conditional restriction into an accepted UDT law.
The role of averaging is still a proposed operational summary, not cause
isolation. The distant-onset positional requirement is untouched.

RUS, which would infer a uniform small-L sign merely from positive-GR recovery,
fails on this explicit metric family. AMS itself is neither derived nor generally
refuted. A result that only reconstructs these supplied clocks cannot select the
physical geometry. Further work needs a specified new decision, such as whether
the quartic sign is general for a justified vacuum/preparation class; no arbitrary
metric survey follows from the present four finite continuation points.

## Evidence and omissions

All B scientific executions used the existing TPS1 capture, one thread,2GiB
virtual-memory limit and no killing timeout. Before final summary capture the
twelve receipts total4.515seconds wall time, with max RSS81616KiB; the summary
adds0.032seconds. The capture does not record separate CPU seconds. All return
codes were zero; no failed numerical run or hidden repair occurred. The existing
20 CPU-minute shared allowance was not approached. No GPU, field evolution,
external data, installation, protected work or untracked payload was used.

Not established here: independent symbolic coefficient proof, rigorous numerical
enclosures, generic vacuum positivity, all-frame behavior, an observational
threshold, selected physical scale, native metric admission or full-postulate
sufficiency/insufficiency. Initial and exposed stages are preserved distinctly.
Fresh same-model review is still required by FAC1. Checksums establish artifact
correspondence, not truth, model independence or physical adoption.

Exact prior sources inspected before implementation: FPC1 REVIEWED_RESULT and
math/DERIVATION; PRT1 REVIEWED_RESULT; CPW1 REVIEWED_RESULT and geometry/SOURCE_FIRST;
central D1/R6--R8/R18, PSW/COC/PEA scopes and the positional owner statements.
The maintained argument and source grades remain owned by those sources and the
coordinator's integration, not by this contributor record.
