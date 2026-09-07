# RC3 Stage A sealed source-first reconstruction

Reviewer /root/restrictiveness_rc3_review, 2026-09-07 UTC; fresh context YES,
exact runtime model UNKNOWN, other-model/human/formal review UNTESTED.
The question, prescribed experiment, old scientific arguments/reviews and
current authority were exposed. No new RC3 candidate argument, scientific
code, output or verdict was opened, and no parent method hint about a new
candidate was received before this report. This is not ansatz-blind review.
The RC2 source's late-hint exposure limitation remains controlling and was
read in its complete direct report, record and EXPOSURE_CORRECTION.md.

## Independent reconstruction

Use g=-2du dv+dx^2+dy^2+Hdu^2 and V=partial_v future. Direct inverse-metric
connection differentiation gives Ric_uu=-(Hxx+Hyy)/2, all other Ricci zero,
and all nabla V slots zero. The proposed harmonic combinations therefore
give ACTUAL Ricci-flat local developments, not arbitrary curvature values.
The general metric is Lorentzian by its null-coordinate block and positive
transverse metric; determinant -1 alone would not prove the signature.

The independently assembled Q_abcd=g(R(partial_a,partial_b)partial_c,partial_d)
and FIRST dual, after the explicitly admitted harmonic restriction, give
the complete 256-component old quadratic B=(Hxx^2+Hxy^2)du^4. A root of this
nonzero tensor has only a u component; its future sign uniquely gives
beta=-N^(1/4)du. This uses the complete tensor and fixed old coefficient.

Let P=Re(z^3+z^4), Q=Im(z^3+z^4), z=x+iy. Cauchy-Riemann identities give
Qxx=-Pxy and Qxy=Pxx. Consequently for H=cos(theta(u))P+sin(theta(u))Q,

    (Hxx,Hxy)=(cos(theta)Pxx-sin(theta)Pxy,
                cos(theta)Pxy+sin(theta)Pxx),
    N0=36(x^2+y^2)(4x^2+4x+4y^2+1).

Thus N, the full B and beta are independent of the arbitrary smooth angle
function. Full recurrence follows from Gamma^u_ab=0:
nabla beta=(d log b) tensor beta, b=N0^(1/4). The inverse-metric norm is

    q0=(16x^2+8x+16y^2+1)
        /[4(x^2+y^2)(4x^2+4x+4y^2+1)],
    D=w0 V, w0=q0 b.

Every component of alpha, q0, C0 and D is angle-independent on the fixed
registration. At x=1,y=0, N0=324, b=3sqrt(2), q0=25/36,
w0=25sqrt(2)/12. This supplies an open positive neighborhood, not a theorem
from one sample: continuity permits a compact interior patch avoiding all
zeros. On a sufficiently small such patch sqrt(P^2+Q^2)<3, so H+4>1 for
EVERY angle value. The regular spacelike graph therefore exists uniformly
with respect to the angle values, without constraining theta's derivatives.
Individual smooth functions have bounded derivatives on a retained compact
u interval; no uniform derivative/stability bound over all functions follows.

On v+2u=0, the full independently induced data are

    gamma=diag(L,1,1), L=H+4,
    n=(partial_u+(H+2)partial_v)/sqrt(L),
    K=[[Hu,Hx,Hy],[Hx,0,0],[Hy,0,0]]/(2sqrt(L)).

An independent INTRINSIC three-dimensional connection/Ricci/divergence
calculation yields the ORIGINAL Hamiltonian -(Hxx+Hyy)/L and momentum
((Hxx+Hyy)/(2sqrt(L)),0,0). Their vanishing follows from harmonicity.
G361's f=L^-1/2,Y=-(partial_u-2partial_v)/L satisfy V=f n+Y; nabla V=0
supplies both full seed equations with the stated minus-Weingarten sign.
The metric and complete data change with theta and its derivatives. At the
anchor H=2cos(theta), Hu=-2sin(theta)theta'; hence Kuu carries derivative
freedom at a generic angle. A single u-null cut would omit this information.

## Fixed product and separately varied phase

The determinant and raising map give the positive quotient density
Xi=w0 |du| dxdy and full initial flux wf dVol_gamma=w0 |du| dxdy.
This is computed from the actual D before defining a matching measure.
Choose once Theta=-kappa0 u, kappa0>0, fixed Cartesian labels and Delta>0,
with baseline mu=(Delta/kappa0)w0 dxdy on a compact regular label patch.
It is positive finite, independent of theta and phase. The full future phase
covector is -kappa0 du, not the nonclosed recipe root. Its complete initial
normal value follows from the metric; no extra normal field is chosen.
The same fixed product matches every angle function on the common local
patch. This is a fixed product inverse-data freedom statement, not another
amplitude normalization example or physical counting law.

For a separately supplied aligned phase with dTheta_tilde=-kappa(u)du,
kappa>0, keeping Delta, labels and THIS mu fixed gives the exact density
residual w0(kappa/kappa0-1). Thus compatibility throughout a connected
product region requires kappa=kappa0 pointwise. The phase may differ only
by an additive constant (with corresponding coordinate-domain bookkeeping);
if its absolute initial value is also fixed, that constant vanishes.
A nonconstant or unequal constant normalization cannot be rescued without
changing another supplied input. Common phase/spacing scaling is a different
allowed gauge only if spacing is also changed, which this comparison excludes.
There is no requirement for theory to uniquely select these ordinary inputs.

## What the additional ideal query can distinguish

Let Knull=partial_u+(H/2)partial_v. Direct full contractions give
g(Knull,Knull)=g(V,V)=0, g(V,Knull)=-1; ex,ey are orthonormal and orthogonal
to both. Knull is future with the given future V. The ideal tide is

    T_ij=Q(e_i,Knull,Knull,e_j)=-H_ij/2,
    T at x=1,y=0 = -9[[cos(theta),sin(theta)],
                       [sin(theta),-cos(theta)]].

This differs under angle variation in the supplied registered frame even
though its trace and eigenvalues are unchanged. The query uses the SAME
metric-dependent null-normalization rule; Knull's coordinate v component
is recomputed from each metric. It does not hold an incompatible coordinate
vector fixed while claiming the same normalization. Here -g(V,Knull)=1 is
the supplied null-pair calibration. If one instead wants G358's timelike
normalization exactly, U=(V+Knull)/sqrt(2) is unit future and
-g(U,Knull)=1/sqrt(2); using sqrt(2)Knull produces -g(U,k)=1 and doubles T.
These are stated affine normalizations, not apparatus identification.

Different registered tides rule out equivalence preserving that complete
registration. They do not classify spacetime metrics under ALL isometries.
A screen rotation can change component displays; it also changes this fixed
registration. Arbitrary theta(u) represents functional freedom in registered
data; neither that fact nor mixed cubic/quartic degrees alone proves a global
isometry quotient theorem. No such classification is needed for this bounded
inverse-data result.

## Checks, exposure, limitations

source_first.py was written independently and imports only SymPy/stdlib,
not parent scientific code. It constructs all connection/curvature/full B
slots and intrinsic constraint expressions. The exact run passed 15 named
groups, exit0, 0.940324151 seconds, max RSS50308KiB, empty stderr; Python
3.10.12/SymPy1.13.1. Counted elementary phase/product rearrangements do not
provide independent evidence for product existence; the explicit positive
measure equality and source measure theorem supply that argument. Every
quantity is exact symbolic algebra without floating tolerance. The analytic
rotation, local-domain and measure arguments own their stated quantifiers.

The unchanged shared capture was completely read before use. One child ran,
512 MiB address space, 60-second CPU/wall, python3 -B, absolute new prefix.
Exact argv/cwd/timestamps/streams/runtime metadata are preserved. No failure
or repair occurred in this independent Stage A calculation.

The parent's STARTUP_PREMISE_AUDIT.json was directly read: exit0, 346-row
audit, 399.077024916 seconds,105792KiB, empty stderr. I did not repeat the
full audit, synchronization or broad historical suites. A read-only diff
found no baseline change in the controlling old authority/scientific-source
paths. No independent remote-freshness claim is made.

No candidate verdict is issued yet. Outstanding direct review will check
the actual candidate proof, frozen source/output correspondence, saved
load-bearing quantities, guards and actual defect mutations. General PDE
existence, genericity, nonlinear stability, root-only/nonzero-Lambda breadth,
global isometry/holonomy/caustic issues, physical instruments/content, sources,
population, scale and canon are not tested or derived here. No new scientific
dependency or accepted grade is changed. Writes are confined to this review.
