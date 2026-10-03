# IEC1 initial candidate — finite echo invariants in a locally symmetric geometry

UNREVIEWED candidate at freeze, not physical adoption. The parent formal result
was saved before reviewer coefficients arrived. Subsequently both fresh source-
first reviewers independently supplied tilted ultrastatic controls with matching
quartic behavior. Their proofs/results have not yet been opened by the parent.
No general invariant statement is inferred solely from examples.

## Geometry and protocol

Supply a Lorentz4 metric with ∇Riemann=0 in a neighborhood of the preparation and
both short null legs. R(X,Y)=[∇X,∇Y]−∇[X,Y], signature(-+++). At o choose
future unit U and spatial unit n⊥U. A(s)=exp_o(sU), B(0)=exp_o(Ln), and B's
initial U is parallel transported along that preparation geodesic. B(b) is its
unit free worldline. Nearby emissions vary on these fixed prepared clocks.

Let F(s,b,L) be their squared geodesic interval on the local normal branch.
First reception solves F(0,b,L)=0 with b~L and p=-F_s/F_b. Actual later return
solves F(a,b,L)=0 with a~2L and q=-F_b/F_s there. In a general symmetric metric
there need not be FCW1's future-clock exchange reflection; q=f'(f(0)) is not
assumed. Near L=0 both ratios are positive and p<sqrt2. Define
D=log q-log[p/(2-p²)]. Scalar FC remains UNADOPTED; D is a diagnostic only.

## Candidate universal coefficients

All tensors below are evaluated at o. Set

 C=R(n,U), A=CU, B=Cn, T=g(A,n),
 V=A-Tn, W=B-TU,
 aa=g(A,A), ab=g(A,B), bb=g(B,B).

V,W lie in the positive-definite perpendicular complement of span(U,n).
Thus aa=T²+|V|², ab=<V,W>, bb=-T²+|W|². Define curvature contractions
Kij=R(V_i,Z_i,V_j,Z_j)=g(R(V_i,Z_i)V_j,Z_j), with pair list
0=(A,U),1=(A,n),2=(B,U),3=(B,n).
The locally symmetric curvature derivation identity gives R(A,n)=R(B,U), so
indices1 and2 have identical contractions. No arbitrary algebraic R tensor is
silently assumed to be realizable by a locally symmetric metric.

The candidate formula is

 D(L)=d4 L⁴+d6 L⁶+O(L⁸),
 d4=2aa+ab-2T²=2|V|²+<V,W>,
 d6=[120K00+108K01-120K03+90K11-27K13
       +60T³+120T aa-236T ab-60T bb]/180.

In particular, if n is an electric-tidal eigenvector (V=0), then

 D(L)=(T|W|²/3)L⁶+O(L⁸).

This is a general conditional extension of FCW1's one-family coefficient if
review confirms the proof. Generic V≠0 can produce a quartic term of either
sign; d4=0 alone does not imply V=W=0 or a totally geodesic sheet. No observer-
universal scalar law, sign/scale, geometry admission or rigidity theorem follows.

## Geometric derivation method

Local symmetry gives the symmetric-pair description h+p, p≅T_oM, with
[X,Y]=-R(X,Y) for X,Y∈p and [H,X]=HX. The local transvection exp(Ln)
has differential equal to parallel transport along exp_o(λn); it carries A(b)
to the prepared B(b). Therefore relative position is represented by
G=exp(-sU)exp(Ln)exp(bU). If σ is the symmetric involution, the local radial
vector Z of G.o satisfies exp(2Z)=G σ(G)^-1, giving

 Z=1/2 log[exp(-sU)exp(Ln)exp(2bU)exp(Ln)exp(-sU)],
 F=g(Z,Z).

This is a local metric-geodesic identity; no Killing-form normalization or global
Cartan decomposition is imposed. Flat central directions are allowed. Sources
for the mathematical symmetric-space method are being pinned in REFERENCES;
the local argument must apply to indefinite signature, not import a Riemannian
global classification. Jacobi fields under ∇R=0 have constant coefficients in
parallel frames: the local exponential-chart metric is analytic, reflection is
an isometry, and transvections realize the stated transport. Algebraic bracket
and metric identities require only the local symmetric connection.

Write s=Lx,b=Ly and expand the displayed product/log through degree7. The
palindrome makes Z odd: Z=LZ1+L³Z3+L⁵Z5+L⁷Z7+O(L⁹), with

 Z1=n+(y-x)U,
 Z3=[(x²-2xy-2y²)A-(2x+y)B]/6.

The saved exact rational noncommutative computation gives Z5,Z7 as nested
curvature expressions. Its left-nested word representation uses A or B as the
first degree3 vector, with every two further letters (z,w) meaning −R(vector,z)w.
The original associative log and that bracket reconstruction need exact replay
before acceptance; the finite list is retained rather than silently fitting
invariants to examples.

F/L²=F2+F4 L²+F6 L⁴+F8 L⁶+O(L⁸), where
F2=1-(y-x)²,
F4=-T(x²+xy+y²)/3,

 F6=-[4aa x⁴-16aa x³y-36aa x²y²-16aa xy³+4aa y⁴
       -16ab x³-12ab x²y+12ab xy²+16ab y³
       +4bb x²+7bb xy+4bb y²]/180.

F8 and full arrival/ratio coefficients are in UNIVERSAL_FORMAL_RESULT.json.
Solve successively y=1+y2L²+y4L⁴+y6L⁶ for first reception and
x=2+x2L²+x4L⁴+x6L⁶ for return, then differentiate the original F, not a
fitted arrival relation. The saved D_raw reduces to d4,d6 using index1=2.
Independent verification must examine the pairings/signs and true return root,
not just compare final symbolic strings.

## Local remainder and scope

The local group logarithm and exponential are analytic near identity. F/L²
extends analytically in (x,y,L²). At first (x,y)=(0,1), F2_y=-2; at return
(x,y)=(2,1), F2_x=-2. The analytic implicit function theorem gives the two
future roots and their emission derivatives. This justifies the even Taylor
remainder for each fixed geometry/frame; it gives no uniform boost range,
finite-distance error constant, caustic/global classification or physical law.
The signature-independent local symmetric-space identification is load-bearing;
if it cannot be justified, narrow to an explicit symmetric-pair metric class.

For V=0, A=Tn, ab=0, aa=T², bb=-T²+|W|²,
K00=-T³,K01=K11=K13=0,K03=T³-T|W|². Substitution proves the stated corollary.
W measures the other failure of the clock plane's curvature closure. T=0 or W=0
can make the sixth-order coefficient vanish without a global classification.
Any stronger conclusion requires its own argument and is outside this candidate.

## Check and admission gates

The first formal construction ran22.75s/83044KiB with exact rational algebra,
one BLAS thread,2GiB virtual limit, no timeout. It is construction, not independent
verification. Parent next checks must reconstruct the associative log and test
original metric/geodesic controls, including a non-product symmetric plane-wave
if feasible. Both reviewers sealed independent tilted ultrastatic counterexamples
before seeing this candidate; their exact source-first results belong to them.
The proposed formula is not accepted merely because it matches those examples.
Native UDT equation, physical geometry, additional positional attribution, FC/RG
adoption and X_max remain unchanged/open. The selected work does not investigate
FCW1's second completion lead. Stop after reviewed conditional return and banking.
