# ESR1 exposed mathematical review

Actual separate context `/root/esr_math`, inherited model, 2026-10-03.
Verdict: VERIFIED-WITH-CAVEATS for INITIAL_CANDIDATE.md SHA-256
9828c44c3b89d6b9f6f9f83f98e69a127dfc551e2d65a5c48587cd3b4fb2f59c.
This is a mathematical proof review, not final integration attestation or
scientific adoption. Candidate/source freeze hashes were independently matched.

The candidate was first read after SOURCE_FIRST_SEAL and its explicit count
correction were saved and their hashes sent to the parent. Parent reports
receiving brief concordances before candidate freeze; my full proof/code/results
were still unread by the parent then. Fresh context, independently written
argument/code, shared model and shared SymPy are separate independence axes.
No different-model, human or formal-assistant review is claimed.

## Attempted breaks and survivors

1. An arbitrary Q need not equal ECS1's rational function. The candidate avoids
   presupposing that identity: a nonzero electric eigenvalue fixes only the two
   required derivatives, which then remove every quartic defect. I independently
   obtained Q'(1)=3,Q''(1)=14 by direct p/q Taylor matching before exposure.
2. A Lorentzian curvature operator need not be diagonalisable. The candidate
   diagonalizes only E_U on the Euclidean U-perp, where self-adjointness supplies
   the ordinary spectral theorem. A nonzero full tensor with every E_U zero is
   excluded by a separately stated polynomial/polarization argument.
3. A T=0 direction might leave transverse W despite vanishing sixth coefficient.
   The candidate never divides by that T. Its common-Q Taylor remainder is
   o(L^4) for all preparations, and both physical n directions force V=0. The
   all-U boost/polarization step determines the entire tensor, including W.
4. All Jacobi operators being scalar might constrain Ricci alone. The candidate
   proves equality of their scalars by a determinant-one timelike-plane boost,
   then polarizes full sectional contractions. The Bianchi step gives the full
   tensor, not only its trace. My independent 36-by-21 exact tensor system at
   seven rational frames has rank20/nullity1 and rejects a product tensor;
   that finite anchor corroborates, but does not replace, the displayed proof.
5. Smooth Q could differ on an unobserved side. The candidate explicitly retains
   that freedom and the flat branch Q(1)=1 with no derivative constraint. Its
   local geometry conclusion does not imply global topology or completeness.
6. The branch range might need to be uniform under boosts. Every limiting
   argument is at a fixed finite frame, so no such hidden uniformity is used.
7. The local sufficiency could use an inverse/past outgoing root. The candidate
   explicitly selects a~2L and excludes the a=0 root. I checked the signed
   construction and endpoint derivatives directly below.

No substantive defect or source-strengthening repair was found. The source-first
proof and exposed candidate follow the same elementary argument; this is honest
concordance, not evidence of different proof strategies. The source-first exact
check had 19 passing assertions, two families, Python3.10.12/SymPy1.13.1, 0.209s,
44784 KiB max RSS, captured with 2 GiB address space and no wall/CPU timeout.
The original source-first seal's typed status incorrectly said23; its separate
correction preserves the original seal and points to the actual19-entry output.

## Independent signed sufficiency audit

For nonzero kappa use an ambient inner product with orthogonal O,U,N satisfying
<O,O>=1/kappa, <U,U>=-1, <N,N>=1. The ambient signature is (-++) for kappa>0
and (--+) for kappa<0; the quadric <X,X>=1/kappa has Lorentzian tangent metric.
Write C=C_{-kappa}, S=S_{-kappa}, c=C_kappa(L), d=S_kappa(L). Then

    A(s)=C(s)O+S(s)U,
    B(0)=cO+dN,
    B(b)=C(b)(cO+dN)+S(b)U.

The preparation curve lies in span(O,N); the constant ambient vector U is
tangent and parallel along it. The two timelike curves have unit proper
velocities by C^2-kappa S^2=1. A short pair is null separated precisely when
its ambient chord is null: the corresponding line remains on the quadric and
is an intrinsic null geodesic. Hence the incidence is

    kappa<A(s),B(b)>-1=c C(s)C(b)-kappa S(s)S(b)-1=0.

At first reception C(b)=1/c and h=S(b), so p=1/c. Put z=kappa h^2=1/c^2-1.
The nonzero later solution has C(a)=(1+z)/(1-z), S(a)=2h/(1-z), with a~2L.
Direct differentiation at(a,b) gives

    F_s=kappa h,
    F_b=-kappa h/[c(1-z)],
    q=-F_b/F_s=c/(2c^2-1).

These denominators are nonzero for every sufficiently small fixed-frame L>0
and nonzero kappa. The displayed ambient argument fails at kappa=0 by division
by kappa, correctly handled separately by the candidate's original flat null
incidence. IEC1's normal-Jacobi construction supplies local equivalence of the
constant-tensor geometry and this model; no global classification is needed.

## Remaining gates and scope limits

The parent reported an initial short-script structural SymPy equality failure,
preserved with its receipt, and an in-scope exact-difference implementation
repair. I have not read or passed that check at this proof-review stage; its
actual final bytes/receipt remain a separate final review target. No new
reviewer script is needed: the allowed independent short check is already
complete and source-first.

I did not rerun IEC1's free-word expansion, full original-incidence suite or
full406 verifier. IEC1's reviewed quartic/hand-audit sources remain the admitted
dependencies, with their existing limits. The parent owns closure premise and
maintenance checks. Native geometry selection, FC adoption, variable curvature,
response attribution, sign/scale, X_max and canon are outside the theorem.
Final maintained-file/source-map review is still pending.
