# RT2 independent source-first requirements and argument seal

Reviewer /root/rt2_product_review, fresh separate context,2026-09-08 UTC.
Pinned grok b85a14cc920c24f5c8554c4a4eaa727e4bdead0f. Runtime model UNKNOWN;
different-model/human review UNTESTED. This document is written before ANY
new RT2 author proof, code, output, outline or verdict exposure. The question
and its three fixed/varied data cases were known from the approved work order
and RT2_PLANNED_QUESTION.md. Entire original SM1 and reviewed RT1 proofs and
reviews, G351/G352 exact derivations/reports, and G367 banking scope were read.

The parent owns already performed synchronization/full352 audit; this pinned
review does not duplicate them. Protected/unrelated untracked paths inspected
by names only; no source mutation. Writes confined to this review directory.

## Independent question and governing data

Within RT1's nonzero null rank-one OPTIONAL comparison S=beta*n*dphi^2,
beta fixed nonzero, n positive, phase exact/future-null and j conserved, ask
which transformations remain G352 products at stated fixed inputs. These
nonzero-S comparison metrics are NOT admitted G312 vacuum histories and do
not adopt a source law or physical counting. Use sufficiently small connected
smooth four-dimensional product/flow boxes, regular positive screen J and
finite smooth positive label measures. Singular/zero/global cases excluded.

Reference coordinates (r,phi,y), ell=grad(phi)=partial_r, are supplied.
G367 gives sigma=J*n independent of r, with possible dependence on phi,y.
The ENTIRE reviewed RT1 proof supplies all exact decompositions at fixed
metric,beta: phi'=F(phi)+c, a=F'>0, n'=n/a^2, j'=j/a. Fixed observer U
gives -g(U,j')=-g(U,j)/a. These are comparison DATA variations, not the
G352 simultaneous Theta/Delta gauge (which leaves dphi fixed).

## Independent derivation at fixed labels

At the same event/cut/labels, increasing F leaves phase sheets and intrinsic
screen area unchanged: J'=J. Affine ray coordinate r'=r/a restores
grad(phi')=partial_r'. Consequently the product coefficient is sigma/a^2.
Any extra factor from changing the three-dimensional quotient phase volume
must not be confused with the two-dimensional label density.

For prescribed positive s0(y), product matching is precisely
sigma(phi,y)=a(phi)^2*s0(y). Necessity: sigma/s0 must be independent of y.
Sufficiency: on that positive smooth domain set a=sqrt(sigma/s0), integrate
F locally. At fixed s0, a is unique; the phase origin remains free unless
supplied. If normalized phase was fixed from the beginning, a=1 and the
condition is sigma=s0 throughout the box. Current is then fixed by the
FULL supplied inputs, not by metric alone.

If s is free but phase-independent at the same labels, existence is equivalent
locally to positive separability sigma=A(phi)*B(y). On a connected coordinate
product box it is equivalently d_y(partial_phi log sigma)=0. To prove
sufficiency, the mixed condition makes partial_phi log sigma depend only on
phi; integrate and subtract to obtain log sigma=alpha(phi)+b(y). All splits
then have a=c*sqrt(A), s=B/c^2, c>0, plus phase origin. The remaining constant
changes j; it is supplied measure/phase data, not admitted gauge. This is a
local characterization, not a finite-test-based completeness assertion.

## Independent derivation with explicitly changed label identification

Let z=Y(phi,y), independent of r and locally invertible with positive
D=det(D_y Y). This now permits a different cross-phase identification.
At the same event the screen density becomes J_z=J/D. Keeping the current
for a fixed a requires the full transformed coefficient

    sigma_z = sigma/(a^2 D).

To obtain chosen fixed s0(z), one requires D*s0(Y)=sigma/a^2. Locally this
can ALWAYS be done for positive smooth sigma and any supplied a>0, with
s0=1, by z2=y2 and

    z1 = integral_{y1_base}^{y1} sigma(phi,t,y2)/a(phi)^2 dt.

The transverse determinant is sigma/a^2>0, and the full map
(r,phi,y)->(r/a,F(phi),Y(phi,y)) is locally invertible. Restrict to a common
small product box in the NEW coordinates; positive bounded density on a
relatively compact finite box gives finite measure. The images of the entire
old label domain need not coincide at every phase. This is NOT a global
fixed-boundary mass-normalization theorem.

This construction changes supplied cross-phase label/product data. It must
not be described as an admitted phase-independent passive product gauge, or
as proving that an ORIGINALLY prescribed product was already satisfied.
A passive coordinate rewrite preserves j only when the FULL quotient measure
is transformed. Taking a=1 and changing identification can display the same
current as a product; taking different a gives genuinely different full
currents/readouts, while full S remains fixed. Thus product existence with
unprescribed label identification does not select a metric-only current.

## Frozen independent diagnostic design

One CPU child, existing capture helper, OPENBLAS/OMP/MKL threads1,512MiB
address space and60s CPU/wall, no GPU/install/network/data. Exact symbolic
metric and Jacobian checks, not convergence or numerical certification.
Metric choices below are free-and-explored diagnostic members; beta=1 is a
declared optional comparison parameter, not a physical constant.

Recompute connection and full Ricci directly from components of
g=2du dr+dx^2+dy^2+H du^2. Check full Ricci/scalar, not only intended Ric_uu.
Choose H=-(2+u)*(3*x^2+x^4/6): expected sigma=(2+u)*(3+x^2), which separates.
Choose H=-2*x^2-u*x^3/3: expected sigma=2+u*x, positive on |u|,|x|<1/4,
which has mixed log derivative2/(2+u*x)^2 and cannot match ANY fixed-label
phase-independent product by the RT1 F freedom.

For the latter choose a=1+u^2 and z1=(2*x+u*x^2/2)/a^2,z2=y. Check actual
Jacobian, FULL metric transformation, positive screen determinant, current
components, full S equality and observer scalar invariance. Use
U=-partial_u+(H+1)*partial_r/2: directly verify unit norm and future sign,
then compare Gamma and Gamma/a. On |u|<1/4 the old x endpoints +/-1/4 map
past +/-1/4, so a common |z1|<1/4 patch is available after shrinking other
coordinates. No observer physical interpretation is added.

Actual rejected substitutes: wrong density exponent, missing label Jacobian,
unchanged-current/readout assertion, fixed-label factorization of2+u*x,
unchanged given measure with nontrivial phase scaling, and treating the
positive Jacobian as a global fixed-domain mass map. Last global issue may
be checked analytically; no artificial machine assertion is needed.

Source-first arguments and finite implementation independence are separate.
Standard Ricci formula/SymPy overlap does not make a different-premise or
algorithmically unrelated review. Author replay after exposure is regression.
Seal hash and first-run records will be sent before direct target intake.
