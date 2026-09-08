# SM1 initial direct adversarial review

Verdict: VERIFIED-WITH-CAVEATS at the exact local conditional mathematical
scope below. No load-bearing mathematical defect or required scientific
repair was found. This is the initial grouped verdict; zero of the permitted
one grouped same-premise repair/re-review cycles has been used. No scientific
promotion or physical identification is conferred.

Reviewer: `/root/sm1_current_review`, separate author/reviewer contexts.
Date: 2026-09-08 UTC. Baseline verified grok
cc71a324a61bf2711a4b52c8ebee8a8e4d9b8269. Runtime model UNKNOWN;
different-model and human-specialist axes UNTESTED.

## Candidate and exposure pins

Reviewed initial candidate SHA256:
b9c883ebb807ea2aea6b6bc7487d407cc218a04c0c8852426ffa899a99dd7e8d
for ../CANDIDATE_INITIAL.md.

Author script SHA256:
0c1a18d8995559e1b8d1bfea6655da3f8a9df17025ea52d91701fc98591dbe66
for ../check_current.py. Author saved stdout SHA256:
5d4c46098b1fbc7ea866bea36703eebc06cfbe3b99fd657ac84e041b55772769.
All three were independently hashed and matched the dispatch before review.

Source-first requirements seal SHA256:
5374e928b503657e01c299e6f7948b020985826e1b1f512b70b0f4039c24e1e3.
That file and the first independent checker were written before candidate,
author code, output or verdict exposure. The independent run began at
01:42:12UTC; exact candidate pins arrived afterward. Only seal completion
and absence of a decisive source blocker were communicated to the author
before the candidate freeze; the reconstructed proof was withheld.

The direct stage then read the full candidate, author script/output, source
ledger and STARTUP_AUDIT.md. G349 was added at this stage because the
candidate explicitly cites its graph-cut result. No prior SM1 verdict existed.
Historical banked-source review summaries were known; they are not treated
as independent review of this new candidate.

## Accepted mathematical scope and independent reconstruction

For every supplied smooth local product flow box satisfying the candidate's
nonzero future null exact phase, constant positive spacing, regular rank-two
screen and smooth AC finite label-measure hypotheses, the chosen G352
phase-independent product determines a unique spacetime current. Its
conservation and observer contraction follow from the supplied data and
metric geometry. They do not constitute a metric source equation.

The dimensional bridge is explicit: the tube is an open four-dimensional
region; the ray quotient has three coordinates (normalized phase, two
labels). A single null phase sheet or transverse cut would not supply this
open-region object. Because ell(phi)=0 while ell and dphi are nonzero, the
restriction of dphi to any local section transverse to ell is nonzero.
Complete phi to three coordinates on that section, and transport the other
two by the flow. This proves the local adapted chart needed by the
candidate without deriving phase or a global tube from the metric.

Exactness and nullness give nabla_ell ell=0. Coordinate pairing with
ell-flat=dphi gives g_rr=0, g_rA=0, g_rphi=1. The coordinate screen vectors
have independent classes in ell-perp/span(ell), so the quotient metric q
is positive definite. Expansion of the four-dimensional determinant along
the r row gives det(g)=-det(q), independently of H and A_A. Thus metric
volume and cut sheet area have the same coefficient J in the declared
coordinate ordering. A graph-cut tangent differs by a multiple of ell;
its Gram form is unchanged. This is the local geometric argument, not an
unwarranted use of G349's larger finite-map claims.

Independently, on the ray quotient consider the oriented product three-form
eta=s(y)dphi wedge dy1 wedge dy2 and pull it back to the tube. Contraction
with the nonzero metric four-volume identifies a unique vector. The kernel
of eta is exactly the ray direction where s>0. Contracting explicitly fixes
the coefficient j=(s/J)ell and its future sign. Both the coordinate formula
and Cartan's identity d(i_j epsilon)=(div j)epsilon give conservation. The
candidate retains the zero-density case without deriving a ratio from zero.

For each future unit timelike observer U, metric contraction gives
-g(U,j)=(s/J)(-U(Theta))/Delta, exactly G352's admitted continuous local
readout. Quotient-screen representative changes preserve its area. Equality
for all future unit timelike U determines the covector because those U span
an open cone after positive rescaling. This uniqueness is at fixed supplied
data; a single observer readout does not suffice.

The converse is also correct on a product flow box with connected r fibres:
div(f ell)=0 iff partial_r(Jf)=0, leaving Jf=S(phi,y). Choosing the G352
fixed phase-independent product further restricts S to s(y). Positivity,
smoothness and finite chosen-patch measure remain inherited conditions;
the converse for arbitrary signed f alone does not give a positive measure.
The candidate's flat f=2+sin(phi) is a strictly positive conserved counterexample
to conservation implying fixed product, on every open phase interval.

## Gauge and orientation audit

The phase AND spacing change Theta->aTheta+b, Delta->aDelta leaves dphi and
ell unchanged. Translation changes phi only by a constant. Therefore j and
Gamma are invariant at fixed mu. A phase-only scaling at fixed spacing
changes the current; a rescaling of mu changes the current; neither is the
admitted gauge. Ray-origin shifts preserve ell and the quotient screen.

The orientation sentence is sound when interpreted as consistent use of
the fixed geometric orientation, or simultaneous reversal of both oriented
representatives. It must not mean flipping eta while holding epsilon fixed.
Equivalently the orientation-free ratio of positive densities s/J directly
gives the future vector. No orientation choice selects physical content.

For preservation of the stated product class, passive label gauge means a
fixed relabeling y'=F(y), independent of phase. Both positive densities
transform by the same absolute Jacobian. A phase-dependent relabeling can
still represent the same underlying current if the FULL quotient measure
is transformed, but generally makes the represented label density depend
on phase. The candidate's warning against obtaining a product by changing
labels after the fact is essential. This interpretation is a retained scope
caveat, not an additional symmetry or a required scientific repair.

## Independent checks, replays and false-pass scrutiny

The independent script independent_current_check.py imports no author code
and reads no author result. SHA256:
dcdab556ed89028af74aefdc988a4870b6d2fe4d1a3ed7ed2caa87b28bb210bd.
It computes the general determinant directly, then constructs the FULL
Levi-Civita connection of an outgoing spherical Minkowski tube. It contracts
that connection to obtain divergence, instead of using the author's volume-
density derivative. The example choice overlaps the author example, but
was fixed before exposure and the divergence implementation is distinct.
This is implementation independence for this diagnostic, not a different
physical premise or an independent empirical confirmation.

Saved independent result:16/16 exact diagnostic assertions, exit0,
0.4529381820029812seconds, maximum child RSS48524KiB, empty stderr.
Python3.10.12; SymPy1.13.1. Load-bearing values recomputed independently:

- det(g)=q12^2-q11*q22 for arbitrary other adapted metric blocks;
- outgoing generator expansion2/r and current covariant divergence0;
- a timelike observer with both radial and angular components has norm-1;
  direct readout and observer-screen Gram area equal the candidate formulas;
- multiplying by2+theta^2 leaves divergence0 but makes the fixed-product
  derivative25/2 at the recorded exact point;
- omitting inverse area produces divergence5/6 at that point;
- phase-only scaling by2 changes the current coefficient by5/36;
  doubling the supplied measure produces the same nonzero change.

The last controls test actual nonzero residuals. They are not tautological
checks that a declared mutation label occurs in text. Symbolic identities
and exact evaluations are finite diagnostics, not proof of the general
quantifier. No convergence or numerical-certification claim is made.

The author script was read and replayed unchanged under the same capture
limits:14/14 assertions, exit0,0.24425932700978592seconds, maximum child
RSS47176KiB, empty stderr. Its stdout is byte-identical to the author's
saved stdout. This is shared-code regression only. The author's symbolic
non-equality mutation guards establish nonidentity, not failure at every
parameter value; trivial gauge values remain expected. The observer-span
determinant is a finite anchor; the open-cone argument supplies uniqueness.
No vacuous check was found to carry a scientific conclusion.

Both commands used the inspected existing
udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py
(SHA2568ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef),
with explicit OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1,
512MiB address-space and60s CPU/wall limits. Exact commands, times and
resource records are in the two capture JSON files and EXECUTION_RECORD.md.
No numerical children ran concurrently in this reviewer context.

## Source grades, checks omitted and residual limits

The parent full349 audit completed exit0/PASS before exact registry queries.
The reviewer inspected its preserved receipt, not a second independent
full349 execution: STARTUP_AUDIT.md SHA256
d665a3ba872c4d06bd49d78dbb7af63bea07358cc4939693e107f125f84dd9c5.
Receipt limitations are explicit: combined terminal streams and approximate
launch/elapsed time. Registry SHA256:
ccd1fd2752a5884dfa2864fc9f3904f9dcc7e22557f6d4057e92ec2c54caf81f.
Exact G312/G313/G315/G348/G349/G351/G352/G353--G356 rows were queried only
after that audit. G351/G352 remain conditional on owner-provisional premises
and the CHOSEN product; G353--G356 are banked conditional mathematics with
caveats. No scientific grade or original source was changed.

Original G348/G349 production counts, prior campaign scripts, general PDE
theorems, singular/caustic measure extensions, global topology, metric source
coupling, observational identification and human-specialist review were not
replayed or established. The accepted scope uses only the regular local
geometry reconstructed above. Protected payloads were neither read nor
hashed. No network, samples, fitting, source-law adoption or solve occurred.

The strongest surviving result is the full initial candidate's bounded
local correspondence. Its useful downstream input is a conserved null
current with specified normalization dependence and observer weight, at
fixed supplied data. It supplies no independent equation connecting that
current to metric evolution. SM2 may use this as a REVIEWED CONDITIONAL
input within the approved work order; it is not an accepted-grade source.
