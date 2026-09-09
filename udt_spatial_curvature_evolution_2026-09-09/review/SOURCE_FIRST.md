# Source-first reconstruction — SCURV review

Reviewer `/root/scurv_review`, actual fresh separate context, 2026-09-09.
Exact model UNKNOWN; different-model independence UNTESTED. Pinned HEAD
`a4da1bae512aa291d26d57b1a54c5a53770302b2`, branch grok, independently checked.
Parent owns synchronization. Unrelated untracked work is preserved. The
reviewer independently ran full365 and reproduced its existing G325
`replay_exact:DERIVATION_RESULT.json` failure; this is not repaired or waived.
This stage is UNPROMOTED mathematical review, not banking or acceptance.

Before writing this note or code I read AGENTS; bounded LIVE/HANDOFF current
blocks; current program/premise summary and exact G303/G310/G312/G315 rows;
required CLAUDE sections; no-shortcuts, completeness-map, solution-space and
verifier protocols; CROSS_MODEL_VERIFY; compact INDEX/MEMORY; work order;
G303/G310/G312/G315 reports and adoption records; LE1 complete candidate and
195-line direct review; NR2 complete initial candidate, reviewed result and
242-line adversarial review. NR2 tangent necessity/classification is not an
input to the present witness. Its exact constraint construction and conditional
analytic development interface are reused at their UNPROMOTED scope.

No SCURV author candidate, code, output or proof has been opened. The work
question and dependencies were known. At the end of this stage the parent
disclosed that its construction uses a different NR2 metric-profile datum;
no formula, calculation or proof for that datum was supplied. Thus this is
source-first, not hypothesis-blind. No author function supplies this check.

## General diagnostic calculation

Signature (-+++), R^a_bcd=partial_c Gamma^a_db-partial_d Gamma^a_cb plus
the corresponding quadratic connection terms. Choose supplied future unit
normal n, local Gaussian time and a Fermi transported orthonormal spatial
frame, eps_123=+1. K=-gamma_t/2. Let D be the spatial Levi-Civita derivative
and curl S_ij=eps_(i^kl D_k S_j)l. My magnetic convention is explicitly

    E_ij=C_i0j0, B_ij=(1/2)eps_i^kl C_kl0j=+curl K_ij,
    Q=E+iB.

The alternative C_klj0 gives -B and conjugates Q and A. My Q represents one
choice of the full complex self-dual Weyl operator; it is not electric-only.
For W=projected nabla_n Q, I2=tr Q² !=0 and I3=tr Q³, the product/quotient
rule gives the exact instantaneous criterion

    n(A)=36 I3 [I3 tr(QW)-I2 tr(Q²W)]/I2^4.                 (SF1)

It vanishes for W=alpha Q+[Omega,Q]. Multiplication and frame similarity
therefore do not change A. This is a sufficient form, not a converse:
I3=0 forces n(A)=0 for every W at that event, and A is no complete invariant
of arbitrary metrics. Zero instantaneous derivative is not finite-time
preservation. Flat/type-N I2=0 points are outside this diagnostic's domain.

Expanding vacuum differential Bianchi in the chosen Gaussian/Fermi frame,
using constant Lambda and K=-D n, gives

    W=i curl Q+2 tau Q-3 (KQ)_(sym,TF), tau=tr K.           (SF2)

Here (KQ)_(sym,TF)=(KQ+QK)/2-tr(KQ)I/3. The 2 tau Q part
drops out of SF1; spatial curl and trace-free kinematic terms can contribute
or cancel. The split depends on the supplied congruence; the directional
derivative of the scalar along that specified geometric n is invariant.
No independent freely chosen E/B fields are inferred to be realizable.

As a primary mathematical sign/convention cross-check, I opened Maartens
and Bassett, arXiv:gr-qc/9704059v3, definitions and equations (2),(29),(31),
(34),(35), https://arxiv.org/pdf/gr-qc/9704059. Setting acceleration and
vorticity to zero, substituting theta=-tau and sigma=-K+tau I/3, and taking
their H=-B yields SF2. This is my convention translation and application to
the admitted constant-Lambda equation. No physical interpretation or source
law from that paper is imported. An initial HTML request returned cache miss;
the primary PDF text was accessible. The general theorem is not machine-proved.

## Independent globally lawful witness

On a supplied compact split translation quotient choose unit spatial scale,
T0=1 and an axial coordinate of period 2pi. These are free supplied choices,
not UDT-selected values. Transverse translation periods remain freely supplied.
For q=e cos x take analytic periodic data

    gamma=I,
    K=diag(1/3-3q²/4, -2/3-q, -2/3+q), Lambda=0.         (SF3)

These are the NR2 flat chart member f=w=r=0, p=cos x, c=Lambda=0.
Since R3=0 and the sum of pairwise K eigenvalue products is exactly zero,
H=(tr K)²-tr K²=0 pointwise. The axial momentum equals
-partial_x(K22+K33)=0 and the two transverse momenta vanish. Positivity,
periodicity and analyticity are explicit. Thus NR2's checked analytic
Gaussian reduction, compact gluing and full Bianchi propagation supply actual
local analytic vacuum developments. This is conditional use of that method,
not an inference from a finite list of metric jets or a new global existence
claim. No tangent classification is re-proved or promoted.

At x=0 one has B=0 but -curl B=diag(0,e,-e). The full coordinate-metric
third-jet reconstruction in source_first_tensor.py, obtained from the admitted
ADM equation rather than SF2, gives

    Q=E=tau K-K²,
    W=2 tau E+diag(0,e,-e),
    n(A)=2592 e²(e-2)(e+2)/(3e²+4)^4.                     (SF4)

The last simplified expression is used only where the ORIGINAL I2 is nonzero;
in particular e=+-2/3 gives flat curvature and is excluded despite removable
factors in a rational expression. At the chosen e=1/6,

    E=diag(-5/12,5/32,25/96), B=0,
    I2=1225/4608, I3=-625/12288,
    A=20449/117649, n(A)=-5930496/5764801 !=0.

K E is pure trace here, so all nonzero diagnostic change at this event comes
from the spatial contribution; the local term is only common multiplication.
This is one lawful witness of local normal variation, not genericity or
long-time behavior. It is not the unknown LG2 collar evolution.

The same independent metric construction also checked x=pi/2, where B23=B32=1/6
is nonzero. It gives I2=13/54, I3=-25/243, A=-7803/2197 and n(A)=-856800/28561.
This second event belongs to the same datum and checks extraction with nonzero
magnetic curvature. The diagnostic need not lie in [0,1] for general full Q.

## Actual checks and limits

The reviewer wrote an independent finite 4D tensor-jet engine. It constructs
all Christoffels, their first derivatives, first-kind Riemann and its normal
derivative, then contracts all Ricci components and their normal derivatives.
Both vanish exactly at both tested events. It separately extracts E/B and
their normal derivatives from the full rank-four curvature, including all
Fermi basis derivative slots. SF4 is compared against those metric results.
Symbolic pointwise Hamiltonian and momentum identities check SF3 globally.

The single captured run passed without failure in 0.676 seconds, 49408 KiB
child RSS, Python 3.10.12/SymPy 1.13.1. Its wrapper imposes 512 MiB address
space and 60-second CPU/wall limits; all library thread variables were 1.
Exact command, time, output and empty stderr are preserved. This is exact
arithmetic checking of an independently derived finite metric jet and written
analytic argument, not proof of general PDE existence or a convergence study.
No GPU, raw fields, protected payloads, archive, observations or new premise.

Preserving controls survive: Kasner common Weyl multiplication leaves A
constant; e=0 in SF3 recovers the homogeneous Taub datum. No implication from
spatial variation alone to diagnostic change or from diagnostic stationarity
to absence of geometric change is made. Full-Weyl invariance, I2-domain and
I3 blind spot must be retained in the direct review. Different-model,
independent-library, specialist-human and formal-proof review remain untested.
