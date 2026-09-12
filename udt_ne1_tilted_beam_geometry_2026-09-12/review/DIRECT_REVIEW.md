# NTB1 direct adversarial review

2026-09-12. Reviewer `/root/ntb1_beam_review`, actual separate context.
Verdict: **VERIFIED-WITH-CAVEATS**, conditional candidate only, UNPROMOTED.
Entire INITIAL_CANDIDATE.md equations 1–13 at SHA256
9932e4a2557144873cd7e23b4147948cc18a559605b920e5109deb4954ea6015
survives this review. No required scientific repair or narrowing was found.
Final packaging fidelity and actual allocation closure are recorded separately.

## Argument audit

**Exact evaluator and normalization.** From the original null Hamiltonian,
h=sqrt(p^T A p), h_p=Ap/h and h_x=(p^T A_x p)/(2h). Differentiating gives all
three Hessian blocks of (3), with canonical ordering (x,p). In particular the
minus signs in the lower blocks and the lambda_xixi contribution are necessary.
The initial fixed-frequency sky derivative is delta p=L_e E_e delta theta;
replacing L_e by I changes the longitudinal normalization by4/3 and fails the
independent check. Multiplication by L_o converts spatial coordinate separation
to the target orthonormal frame. Null Jacobi orthogonality makes p_o.delta x=0;
changing the endpoint parameter adds only a multiple of k. Thus target projection
in (2) is the same intrinsic quotient class, and both screen columns are retained.

Finite-time regularity is legitimate: the supplied metric and inverse are smooth
and uniformly bounded on each compact positive-t slab. The reduced Hamiltonian is
positive and homogeneous in every nonzero p, with |p'|<=C|p| and bounded spatial
coordinate speed there. Gronwall bounds prevent finite-time blowup or collapse of
|p| to zero, so the ray/variational flow continues across every such slab. This
argument does not establish affine completeness or anything at t=0. Neither
coordinate winding nor cut-locus ties are the Jacobi rank-loss criterion.

**Invariant mixed transverse rays.** Reflection at xi=m pi/k makes P_xi and
lambda_xi vanish, so p_xi=0 and xi=constant are preserved for every transverse
mixture. With r=M_P/M, direct differentiation gives r_P=1-r^2 and |r|<=1,
including r=+/-1 at the pure axes. The Bessel equation gives w'=-e k^2 tF.
Consequently

    q'=(w+r)w'/2+(1-r^2)w^2/(2t),
    q'-t b_xixi=(1-r^2)w^2/(2t).

Substituting this identity into the independently checked scalar geodesic
variation yields exactly the candidate's Y system. All its coefficients are
regular at finite positive t; Z initially increases and Y(1)=1. On the putative
first interval with Z>=0, Y'>=0 and the integrating-factor solution for Z has a
strictly positive integrand. A first return to zero is impossible. This proves
Z>0 for all t>1 on this explicitly invariant family, not from sampled signs.

For the second screen direction, put v=(-p_z,p_y) with |v|=1. The Hessian of
N sqrt(M/t) in the transverse plane is N vv^T/(sqrt(t)M^(3/2)), because the
diagonal transverse inverse factors have determinant1. At the target,
|L_o v|=sqrt(tM). This independently checks every source/endpoint factor in (8).
The two columns occupy the xi and transverse planes respectively, so their
orthogonality is exact and each positive width rules out nonvertex conjugacy.
No sign-based determinant argument is being substituted for these two modes.

**Pure transverse axes and asymptotics.** For r^2=1, Y=1. Dividing its equation
by t gives Z'+(b_t-1/t)Z=1/t and integrating factor exp(b)/t. This yields (10)
without an omitted source factor. At zero amplitude it gives
Z=(4/7)(t^(7/4)-1), hence the precise D_xi0 in (11); the other integral gives
D_perp0=3sqrt(t)(t^(1/4)-1). Both are positive for t>1.

For fixed epsilon!=0, the source-owned uniform Bessel estimates imply
exp(b)=Theta(exp(beta t)t^(-3/4)). The positive integral in (10) is therefore
Theta(exp(beta t)t^(-11/4)), giving Z=Theta(t^-1). Equation (8) similarly gives
D_perp=Theta(exp(beta t)t^-1/4). Every exponent in (12) follows. The background
area grows only polynomially, so it does not affect the limiting logarithmic
contrast rate 2beta. The statement D_xi/D_perp=Theta(1/t) implies a ratio tending
to zero while both physical widths diverge; coordinate Z tending to zero is not
a conjugate endpoint. Bounded oscillatory factors do not imply a prefactor limit
or monotonicity. Constants need not remain bounded as epsilon approaches zero.

The same invariant ray has omega=sqrt(M/t) by nullness and p_xi=0; the background
clock ratio is sqrt(t), hence R/R0=M^-1/2 tends to1 as P tends to0. This directly
checks (13) without treating NCR1's UNPROMOTED status as accepted authority. The
credit to NCR1 for the previously reviewed formula is appropriate. General mixed
transverse beam exponents and generic oblique nonconjugacy remain unclaimed.

**Reversal and observers.** The candidate uses G348's theorem within its supplied
smooth-metric/regular-geodesic domain. Common positive affine rescaling cancels
from source-normalized area. At fixed ray, changing the target observer adds a
null multiple to a screen representative, an isometry of the quotient; changing
the source observer rescales its angular differential by the source Doppler
factor. Thus the source-factor-squared law and unchanged rank are correct.
Same-unoriented-segment reversal is the adjoint Jacobi relation, not a later
causal return. The area-ratio formula is explicitly restricted away from zero
areas, avoiding a hidden 0/0 assertion. No preferred physical areal frame follows.

## Independent quantitative checks

Source-first notes and outcomes were sealed before candidate exposure. They used
original Christoffels and full perturbed geodesics with three great-circle
offset sizes; parent uses analytic reduced-Hamiltonian first variations. Both
share the admitted metric and NumPy/SciPy, not ray/variation code or trajectories.

The eight signed-amplitude invariant scalar integrations through t80 found no
nonvertex zero. That result is finite support only; the cooperative argument
above supplies the all-time invariant-ray proof. Eleven original-geodesic cases
covered both longitudinal signs, y/z and mixed directions, both axes, invariant
pure-transverse controls and epsilon0. Max finest-versus-Richardson normalized
derivative difference7.8761e-7; max central null residual5.5401e-14. Axial
positive quadratures, invariant scalar widths and background momentum-quadrature
controls passed. The saved physical3x2 derivative matrices, not only determinants,
were then compared with the parent evaluator at the same cases:

| Quantity | Maximum normalized/absolute difference |
|---|---:|
| Full physical screen matrix, source-basis rotation included |1.7685158e-11|
| Source-normalized area |1.7969547e-11|
| Clock frequency |7.6050277e-15|
| Endpoint spatial coordinates |3.9079850e-14|

All were below frozen2e-5 screen/area and2e-8 frequency/endpoint controls. These
are floating-point agreements, not interval certification. Two actual adverse
variants were executed with separate preserved stdout/stderr/receipts:
omitting source L_e failed the matrix check at0.1596851, and dropping spatial
Hessian blocks failed at0.00935586. Both exited1. The source-normalization
mutation changes the compared matrix only; its printed unmodified parent area
is not a claim to have tested that mutated area independently.

I inspected parent discovery output:58 cases,232 saved receptions, no nonpositive
sampled signed area, maximum scaled orthogonality2.2095e-12, maximum absolute
symplectic residual3.5726e-9 and maximum scaled residual7.1299e-12. Scaled residuals
alone would be a weak certificate if matrices became large; the independent
screen/trajectory checks above supply a different route. Finite discovery cannot
exclude crossings between samples or at later times, and no such inference is
made. Its code/source hash matched the parent freeze.

## Fidelity, provenance and omissions

G394 remains supplied conditional Ric=0 geometry; current G312 remains FILTER
ONLY with native response membership unclosed. G415 owns axial positive maps and
axial limits. G348 owns the generic quotient/reciprocity/observer theorem. NCR1
is a reviewed conditional UNPROMOTED prior, with its clock formula independently
visible here. New content is the full NE1 evaluator, invariant mixed-transverse
nonconjugacy and pure-transverse area/shape asymptotics. No equation, physical
selection, observer preference, light/flux/distance law or full pair assembly is
adopted, and no registry or canonical status is changed by this verdict.

Reviewer checked the actual parent current398 capture receipt and complete short
stdout: started21:56:03.377016UTC,404.0895995s,exit0,no timeout,398-row/G415 PASS.
This is attributed parent execution, not a separately rerun premise verifier.
Underlying G394/G415/G348/NCR1 verification suites were not broadly replayed;
their source hashes matched pinned versions and their load-bearing equations
were audited above. No claim of independent empirical evidence follows.

Fresh context and independent implementation/argument are established. Runtime
model/version is UNATTESTED; different-model/library, human-specialist, formal
proof and interval certification remain UNTESTED. Candidate parent exposure to
the reviewer's initial scalar finding before its freeze is explicitly retained.
Hashes establish byte correspondence, not externally signed timing or truth.
No reviewer subagents, capacity retry, sync/switch, staging or protected-payload
read occurred. General capacity and backup/pre-reboot completeness stay UNVERIFIED.
