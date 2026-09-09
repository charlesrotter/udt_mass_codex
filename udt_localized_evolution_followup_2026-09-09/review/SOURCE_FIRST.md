# LE1 source-first adversarial assessment

Reviewer `/root/le1_review`, actual separate context, 2026-09-09 about 18:41 UTC.
Pinned repository HEAD: `2fbd422a8271de56296ad2efa4a1037887e20c91`, branch `grok`.
This note is frozen BEFORE reading any LE1 author candidate, author code or
author output. The research question and work order were supplied. The prior
LG2 proof and its original and repaired review verdicts were exposed because
they are controlling dependencies. This is source-first reconstruction of a
new local consequence, not blind review of the direction or of LG2.

Exact reviewer model is UNKNOWN; different-model independence UNTESTED.
Implementation: new metric/Christoffel/Riemann tensor code, no author function
or result imports. Argument: independently reconstructed from the pinned sources.
Its finite algebra does not independently prove general PDE theorems.

## Premises and dependency scope

G310/G312 and the later owner-adoption records give the OWNER-PROVISIONAL
bounded vacuum arena, not canon. Bianchi completes it to Ric(g)=Lambda g on a
connected smooth region. G303/G315 require the FULL Hamiltonian and momentum
constraints and condition smooth local development, causal domain dependence,
and geometric uniqueness on standard imported hyperbolic methods. G321 is used
only to retain that method/application distinction. G324 supplies the fixed
Ricci-flat Taub comparison. Agreement with its initial tensors on an open
exterior fixes the connected comparison Lambda to zero.

LG2 remains REVIEWED UNPROMOTED and is effective only as CANDIDATE.md plus
REPAIR.md. In particular its projected-deformation map is the covector
J_i=-2M_i, with the prescribed fixed-base pairing, not a varying raised map.
Its smallness, smooth weighted inverse/regularity hypotheses, diagonal
reflection-invariant prescribed interior, nested embedded balls, supplied
T0>0 and fixed compact quotient all remain. No actual completed transition
tensor field was furnished. A raw cutoff is not a lawful datum. The new
conditional assertion must quantify over ACTUAL smooth full-constraint
completions, not the nonlawful interpolation.

The full365 verifier was independently run and failed at the existing G325
`replay_exact:DERIVATION_RESULT.json` gate. Later gates were not reached. I did
not repair it. This blocks promotion/full-integration claims, not this bounded
unpromoted review. Protected and unrelated payloads were not inspected.

## Independent analytical result

Let B be the open exact-interior ball with radius r_-, and fix one allowed
nonzero u. Write the source Kasner data as p_i=-T0 k_i. Then

    g_K=-dT^2 + sum_i (T/T0)^(2p_i) (dx^i)^2,
    sum p_i=sum p_i^2=1,  T>0.

The coordinates, orientation T increasing, T0, p_i and ball marking are
supplied mathematical choices; they are not physical scale or history
selection. Every actual smooth constraint-compatible completion agrees with
these full initial tensors on B. Conditional geometric uniqueness therefore
identifies its development locally with g_K in the core domain of dependence.
For each such completion and each compact B' strictly inside B there exists a
positive local time interval with this identification. The interval may depend
on the datum, the selected development and B'. The logically safe quantifier is

    for every actual completion D, for every B' compactly contained in B,
    there exists epsilon(D,B')>0 with the stated local isometry.

No source here supplies a common global lifespan for all arbitrary
completions. Symmetry of an arbitrary completion is unnecessary for this
consequence: equality of both core initial tensors, regularity, all
constraints and the same sector are what uniqueness uses. LG2's symmetry is
a sufficient construction hypothesis for its supplied family.

In the Kasner orthonormal frame direct curvature calculation gives B_Weyl=0
and Q=E+iB_Weyl diagonal with eigenvalues

    e_i=p_i(1-p_i)/T^2=-p_j p_k/T^2.

Here Q represents the Weyl operator on complex self-dual bivectors, up to a
common conventional factor/sign. Changes of orthonormal observer/frame act
by similarity on that operator. Thus its characteristic coefficients are
spacetime invariants. Merely taking tr(E^2) for an arbitrary observer in an
arbitrary spacetime would NOT have justified this invariant claim.

Put P=p1*p2*p3. The Kasner sum and square identities imply sum_{i<j}p_i*p_j=0.
Consequently

    I2=tr Q^2=-2P/T^4,
    I3=tr Q^3=-3P^2/T^6,
    K=R_abcd R^abcd=8 I2=-16P/T^4.

In the supplied near-Taub interval, P<0, so K>0 and dK/dT=-4K/T<0.
For the trace-free cubic characteristic polynomial,

    Disc(Q)=I2^3/2-3 I3^2=product_{i<j}(e_i-e_j)^2.

A convenient openly chosen mathematical shape query is

    A=2 Disc(Q)/I2^3=1-6 I3^2/I2^3=1+27P/4.

It is dimensionless and unchanged by the common curvature factor; its
denominator is nonzero in this core. Taub has P=-4/27 and A=0 everywhere.
For LG2's u-family the exact independent reduction gives

    P=-4(1-3u^2)^2/[27(1+u^2)^3],
    A=u^2(u^2-3)^2/(1+u^2)^3 > 0 for 0<|u|<1/10,
    K=64(1-3u^2)^2/[27(1+u^2)^3 T^4].

Thus A is positive and constant throughout every justified exact-core
development region even while K strictly falls. This is an invariant
discriminator against EVERY Taub event, independent of coordinate
identification or reslicing. It is not a complete metric classifier or a
physical content density. A=0 in a general spacetime is not an iff criterion
for Taub; algebraic-speciality degeneracies remain outside this test.

If one elects the supplied equal-T comparison, K_core/K_Taub=1-A is constant,
and K_Taub-K_core=(64/27) A T^-4. That comparison illustrates why an absolute
difference can decrease without loss of the normalized distinction. It uses
the supplied common-time marking; the A discriminator itself does not.

## Causal bound and adverse scope test

For future T>=T0 a causal curve of g_K satisfies

    sum_i (T/T0)^(2p_i) (dx^i/dT)^2 <= 1.

With p_min=min p_i, this implies Euclidean |dx/dT| <= (T/T0)^(-p_min).
Therefore its displacement back to T0 is at most

    L(T)=T0[(T/T0)^(1-p_min)-1]/(1-p_min).

It follows that |x|+L(T)<r_- is a sufficient Kasner inner region of the core's
future domain of dependence. Transfer only the portion justified by the
actual local isometry/development. For a compact core of initial coordinate
radius rho<r_-, a sufficient causal time limit is

    T<T0[1+(1-p_min)(r_- -rho)/T0]^(1/(1-p_min)),

again intersected with the justified local existence region. This is an
inner bound, not the complete anisotropic wavefront for arbitrary x.
The bound loses its content at finite time for any finite initial margin;
that is loss of this guarantee, not proof that the geometry erases, radiation
arrives, or a singularity forms. Extending the homogeneous formula to T=infinity
does not establish its validity in the localized completion.

Strongest surviving conclusion: every actual permitted smooth completion has
a local causally protected exact-core germ with decreasing positive absolute
curvature and a persistent nonzero dimensionless contrast from Taub. The
claim that decreasing absolute curvature by itself proves erasure is not
supported and fails already in this local invariant sense. This does not
refute eventual erasure or prove later survival for the whole completion.

## Independent recomputation and failure history

source_first_check.py was written before LE1 candidate exposure. It starts
from a separately parameterized rational Kasner metric with
p=(-q,1+q,q(1+q))/(1+q+q^2), reconstructs all Christoffel symbols, all Riemann
components, Ricci and the full Kretschmann contraction, and computes the
characteristic-polynomial discriminant of E. It also reconstructs the actual
source u-family directly. For q=6/5 it gives A=18496/753571, whereas A(q=1)=0.
The interval result follows from the factored formula, not this sample.

The initial run failed an exact-zero assertion because SymPy had left equal
positive-time exponents in different rational forms. source_first_failure_probe
preserves the actual expression, including correct q=1 values. The first
normalization continuation also failed; power_normalization_probe confirms
that deep power simplification and denesting both reduce the residual to zero.
RECHECK_REPAIR.patch preserves the one-line continuation-code change. Its
pre-repair SHA256 was
6d63aa022df81af3f0e7c26d580942ed7808aee5ac115f036ac83c9f8985957b.
The original check source and both failing stdout/stderr/captures remain.
These were reviewer implementation/normalization failures, not silently
discarded scientific counterexamples or repairs to the unseen author result.

The final source_first_recheck_pass run exited 0 at 18:38:52 UTC, duration
2.91 seconds, maximum RSS 50960 KiB, Python 3.10.12, SymPy 1.13.1. All checks
used the existing run_capture.py with absolute output paths, 512 MiB address
space and 60 second CPU/wall limits, OMP/OPENBLAS/MKL threads set to one.
Each capture JSON contains its exact argv, cwd, start, status and resource
limits. The final calculation independently yields Ricci=0, B_Weyl=0,
K=8I2, the discriminant identity and the invariant/curvature-time formulas.

Not re-proved or replayed: the general smooth hyperbolic theorem, general
constraint-deformation/weighted regularity theorems, all upstream package
tests or source reviews, actual collar PDE data, global evolution, numerical
convergence, genericity/stability, physical interpretation, human specialist
review or different-model review. No GPU, external messages, premise/grade,
canon or manuscript changes. SOURCE_MANIFEST.tsv pins the load-bearing
repository sources and exact work order. Startup/current method reads were
also performed. No public paper was needed for this conditional consequence;
the imported methods retain their already-reviewed source limitations.

Ready to receive the frozen LE1 candidate for direct adversarial review.
