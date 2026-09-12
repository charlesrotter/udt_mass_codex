# NCR1 direct scientific review

Verdict: **VERIFIED-WITH-CAVEATS**, conditional and UNPROMOTED, for the entire
frozen INITIAL_CANDIDATE.md equations(1)-(14) and the explicitly credited
SOURCE_FIRST_ADDENDUM.md equations(A1)-(A3). No scientific defect, required
narrowing or source-preserving repair was found. Parent computation/final
documentation fidelity is a separately recorded remaining review stage;
this verdict does not claim that pending publication or audit checks passed.

Reviewer `/root/ncr1_directional_review` is an actual fresh separate context.
Runtime model/version is UNATTESTED. Direct intake authenticates all eight
entries of CANDIDATE_FREEZE.json. Initial candidate SHA256
`bb8559afcd073cd969719dca645e678b60e9f0ef3098e04d44b203712a68089a`;
addendum SHA256
`dda7843029c4c3bd75315ed7ee74dba3de380b49a8f0a3a656e89b19c836e18e`.
Current G312 FILTER ONLY and exact G394/G415/G220 source limits control.

## Load-bearing argument attacked

1. **Initial comparison and background.** At t=1 the spatial metric and
   normalized frame agree for all amplitudes: N=3/4 and P=0. Conserved
   p_y,p_z equal the transverse sky components and p_xi=(3/4)mu. Solving
   the full null Hamiltonian for future p_t gives the exact frequency.
   In the zero-amplitude metric the longitudinal term in omega_0^2 is
   mu^2 sqrt(t), and the transverse term is rho^2/t. Candidate(5) keeps
   both, so there is no replacement of the same-sky background by its
   axial special case. Receivers are reached at the same marked t and
   can have different labels. A regular-branch G220 clock interpretation
   is not confused with a universal fixed-sky family clock experiment.

2. **Nonaxial Hamiltonian reduction.** Source-first reconstruction from the
   admitted metric independently obtained conserved transverse momenta,
   xi'=p_xi/h, p_xi'=-B^2 b_xi/h, and eta'=-b_xi-v b_t. Total h'=partial_t h
   along its Hamiltonian flow gives precisely candidate(3). Spatial lapse
   gradients, both transverse axes and mixed momenta remain in b_xi. The
   sign of v may change. rho=0 is separated before atanh is used. On every
   finite slab the bounded coefficients and |xi'|<=1 prevent finite-t
   rapidity blowup; the omitted transverse positions also extend there
   because their Hamiltonian slopes are finite on that same slab. No
   affine completeness or off-axis conjugacy assertion follows.

3. **Coefficient asymptotics.** Direct expansion of the actual source
   constraints gives lambda_t/4=beta[1-cos U cos V]+O(1/t) and
   lambda_xi/4=beta sin U sin V+O(1/t). The remaining b terms are
   -3/(4t) and bounded momentum weights multiplying P_t/P_xi, hence
   O(t^-1/2), uniform in xi, mixture and nonzero momentum magnitude.
   beta=epsilon^2 sigma/4>0 only after fixing epsilon!=0. This checks the
   signs and factors in(8); it does not average away the oscillations.

4. **Bounded excursions, with explicit constants.** At v>=7/8,
   -(b_t+b_xi)+(1-v)b_t is bounded above by
   -beta[1-cos(U+V)]+145 beta/512, which is less than the stated
   -beta[1-cos(U+V)]+beta/3. Over L=2pi/k the phase derivative lies in
   [15k/4,4k], so its phase advance exceeds two full periods. Changing
   variables and retaining two periods gives integral(1-cosPhi)dt>=pi/k.
   Thus the net rapidity increment is <=-beta pi/(3k). The negative
   side follows with -eta and U-V. The global late derivative bound
   |eta'|<4beta controls incomplete intervals; each complete interval
   entirely outside the threshold decreases the excursion magnitude.
   This proves(11). No assumption of a converging direction or constant
   frequency prefactor enters the proof.

5. **Fixed-direction growth order.** For fixed rho>0, bounded eta and
   M/rho^2->1 imply omega=Theta(t^-1/2). If additionally mu!=0,
   omega_0=Theta(t^1/4), giving C=Theta(t^3/4). Two-sided Theta bounds
   imply both logarithmic limits in(13). Uniformity holds on compact
   bands away from rho=0 and mu=0. At rho=0 the previously accepted
   exponential rate remains. At mu=0 the order is only Theta(1), with
   the exact xi=0 control recovering one for every transverse mixture.
   The changing sign of F in that control forbids importing the axial
   all-finite-leg sign theorem off axis.

6. **Uniform cone lower bound.** The early coefficient bound is uniform
   in xi, mixture and nonzero rho. Combining it with the late excursion
   estimate gives |eta(t)|<=|eta(1)|+K_epsilon. The inequality
   cosh(x+K)<=exp(K)cosh(x) for x,K>=0 and
   rho cosh(eta(1))=1 therefore remove the apparent axis singularity
   from sqrt(t)omega. The original Hamiltonian is smooth near either
   axial initial momentum at every fixed finite t, so continuity extends
   the SAME upper-frequency constant through rho=0. The exact background
   then gives(A2)/(A3) uniformly on closed cones |mu|>=c_*>0. This does
   not supply an upper polynomial bound through the axis, a numerical
   onset time, or uniformity as epsilon tends to zero. The stronger
   uniform bound originated in the reviewer's source-first argument;
   the parent's addendum is a credited adaptation, not independently
   rediscovered by two contexts.

7. **Necessary angular narrowing.** Nullness and the transverse Killing
   momenta alone give omega>=rho exp(-|P|/2)/sqrt(t), so(6) is exact at
   every finite t. Algebraically solving this upper bound under
   C>=q C_ax gives(7), with a positive-denominator qualification. Since
   the axial contrast is Theta(exp(beta t)) and P is bounded, the stated
   O(t^3/4 exp(-beta t)) necessary width follows. Sufficiency, exact
   transition width and a joint angle/time asymptotic are expressly
   unproved. This bound cannot be misread as saying all contrast has
   vanishing angular reach; the closed-cone lower bound says otherwise.

These attacks found no defect. The strongest survivor is the entire
conditional directional classification plus the credited uniform cone
lower bound. No scientific repair is prescribed. The argument remains
specific to the supplied exact polarized NE1 family, marking, source
slice/frame and areal observers, with regular-branch clock interpretation.

## Actual independent checks and exposure

The source-first argument/check contract was sealed21:05:47UTC before
NCR1 parent candidate/code/output exposure. The parent reports completing
its initial argument21:05:51 before receiving reviewer findings; its formal
hash seal21:06:51 explicitly discloses that it followed the scientific
message. This review treats those as the actual recorded chronology, not
an externally signed timing proof. The complete parent chain including the
credited addition was frozen21:09:33 before direct reviewer exposure.

The reviewer implemented original diagonal-metric first derivatives and
Christoffels, then integrated all spatial positions/slopes and log(k^t).
A separate scalar implementation integrated the independently reconstructed
rapidity equations. Eight frozen cases plus a tighter worst-case repeat
passed: maximum relative frequency discrepancy2.05089056848351e-09,
scaled xi discrepancy6.658218014696276e-11, original null residual
4.1063056050023684e-09 and Killing-momentum error2.0269985689935766e-10.
The tighter worst-case frequency discrepancy was2.1608048683674497e-11.
Both actual hostile variants exited1 at the unchanged frequency assertion,
with defects18.56080902598741 and0.6527979120269158. Exact outputs,
versions, commands, resource captures and hashes are retained in review/.

These checks preceded direct exposure and are reused after checking that
their hypotheses/readout match the complete candidate. There is no need to
rerun unchanged finite cases merely because the analytic proof was opened.
They cover both signs, each transverse axis, mixed tilts, negative and
finite amplitude1.2, zero amplitude, a small finite tilt and invariant
equatorial controls. They are finite float64/SciPy support, not asymptotic
proofs or interval certificates. Source derivative constraints remain a
shared admitted input; the metric's Ricci construction was not re-proved.

| Independence axis | Actual record |
|---|---|
| Context | One fresh separate reviewer context; parent startup attributed |
| Model | Runtime model/version UNATTESTED; different-model axis UNTESTED |
| Argument | Source-first metric reconstruction before parent proof/code/output; direct attack after sealed invitation |
| Uniform addition | Reviewer-origin argument, followed by credited parent adaptation and direct constant/quantifier check |
| Implementation | Original-connection and reduced equations independently assembled without new parent code imports |
| Library/premises | SciPy and exact source geometry shared; neither different-library nor premise independence claimed |
| Other axes | Human specialist, formal proof and interval certification UNTESTED |

No beam/Jacobi, generic equatorial limiting classification, conjugacy/cut
census, fixed-label boundary-value reception, late-emission fixed-path
extension, full pair-kernel assembly, physical light/redshift/cosmology,
native response-law selection, source/action/carrier/scale or canon is
reviewed or promoted. Source full computations and full398 were not rerun
by this reviewer; the parent owns the current audit. No protected payload,
root/scientific source or Git state was modified by this review.
