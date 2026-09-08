# BI2 independent pre-candidate reconstruction

Conditional reconstruction; not a promoted result. This predates BI2 candidate
exposure. REVIEW_SCOPE.md discloses the incidental pre-seal campaign-log summary
of whiteboard advice; a strictly blind no-advice pass is not claimed.

## 1. Actual development requires the complete initial pair

Use G315's negative-K convention, dot(gamma)=-2K, and its original constraints.
For the fixed Berger metric gamma=A(sigma1²+sigma2²)+C sigma3², A,C>0 and A!=C,
BI1's reviewed complete left-invariant class has K13=K23=0 in the initial
orthonormal frame, arbitrary symmetric horizontal block, and its Hamiltonian
quadric. This is a provisional reviewed dependency with its entire review,
including the two author-harness false passes detected independently. No
assumption of pure trace, horizontal isotropy, nonzero root, nonzero horizontal
mean or a sign of Lambda is made. Each complete datum fixes its constant Lambda.

A rotation about X3 is an initial Berger isometry and diagonalizes every real
symmetric horizontal K block. This is one initial frame/data equivalence,
including the repeated-eigenvalue case, not a time-dependent gauge restriction
or removal of shear. In that frame write gamma(0)=diag(A,A,C) and
K(0)=diag(A k1,A k2,C k3) in the fixed invariant Xi frame.

The complete pair is invariant under all left SU2 translations and under the
three determinant-one diagonal sign changes diag(1,-1,-1), diag(-1,1,-1),
diag(-1,-1,1). These preserve [Xi,Xj]=2 epsilon_ijk Xk and integrate to global
SU2 automorphisms. They preserve K as well as gamma, even when k1!=k2. Continuous
right axial symmetry need not preserve K. Using that symmetry without checking
K would be the wrong uniqueness application.

Now apply the explicitly imported GENERAL smooth Einstein-Cauchy existence,
geometric uniqueness and isometry-extension method, conditionally as in G330.
Hypotheses: smooth compact boundary-free S3, positive smooth gamma, smooth
symmetric K, all four original constraints, constant Lambda; no source or
boundary. All hold in this declared class. G321's torus application does not
prove this general theorem. Extend each data isometry with the same chosen
future normal; normal exponential flow commutes with these extensions.
Compactness and regularity provide a common small Gaussian slab. Thus left
invariance and the finite sign-change symmetries hold on its actual slices.
They force, in the SAME fixed initial frame,

    gamma(t)=x(t) sigma1²+y(t) sigma2²+z(t) sigma3², x,y,z>0.

This uses uniqueness of actual developments, not a zero-jet argument or an
assertion that the auxiliary BI1 linear metric path solves the equation. The
same symmetries force K(t) diagonal. Equivalently the original ADM equations
close on the diagonal class; that algebra is an interface check, not the
existence/uniqueness proof. Gaussian marking is essential to statements that
this line/projector is fixed in time.

## 2. Full triaxial Ricci spectrum and the original branch

Independent Koszul curvature on the fixed bracket frame gives the endomorphism

    rho1=2[x²-(y-z)²]/(xyz),
    rho2=2[y²-(z-x)²]/(xyz),
    rho3=2[z²-(x-y)²]/(xyz).

The original Berger vertical branch is rho3 with line span(X3). Its two gaps are

    rho3-rho1=4(z-x)(z+x-y)/(xyz),
    rho3-rho2=4(z-y)(z+y-x)/(xyz).

At x=y=A,z=C both equal 4(C-A)/A², nonzero. Smoothness therefore gives, for EACH
complete finite datum, an epsilon>0 with both gaps nonzero and metric positive.
There is no uniform epsilon over unbounded K and no claimed global extension.
The branch remains isolated on any connected regular Gaussian interval on
which BOTH gaps stay nonzero. The horizontal eigenvalues may coincide or
split; exactly one simple eigenvalue is not a requirement. At a triaxial slice
there can be three simple lines. This construction continues the original
branch using initial marking; it does not arbitrarily select a new simple line
from the later metric or claim a history-free selector of a distinguished one.

In these fixed coordinates its metric-orthogonal projector is exactly
diag(0,0,1), hence both image and full projector persist. A basis-independent
spectral expression for the selected branch is

    P3=(B-rho1 I)(B-rho2 I)/[(rho3-rho1)(rho3-rho2)],

also valid when rho1=rho2 and separated from rho3. The simpler G330 two-value
linear expression must not be used after horizontal splitting. Extra gap
zeros z+x=y or z+y=x are possible with all metric coefficients positive;
checking z!=x,z!=y alone is insufficient. If a gap closes, the symmetry line
may still exist but this isolated Ricci-branch argument stops.

## 3. Closed spatial leaves and normalized integral

The integral curves of the fixed left-invariant X3 are g exp(s X3). In the
declared SU2 normalization they are free circle orbits of period 2pi. Their
length on each homogeneous slice is 2pi sqrt(z). Unit representative and dual
are V=+/-X3/sqrt(z), alpha=+/-sqrt(z) sigma3. Period/fibre-length normalization
gives eta=+/-sigma3. With G330's orientation and volume convention,

    d sigma3=-2 sigma1 wedge sigma2,
    integral sigma1 wedge sigma2 wedge sigma3=2pi²,
    (1/(4pi²)) integral eta wedge d eta=-1, magnitude 1.

Line reversal leaves the integral unchanged; ambient orientation reverses its
sign. This calculation needs neither x=y nor a descended horizontal metric.
The free circle action and quotient S2 survive; original-branch identity is
certified only while its gap is open. The integral here is the declared
metric-length-normalized Hopf quantity, not an energetic stability measure,
independent fixed-target carrier degree or a chosen physical length.

## 4. Direct Riemannian quotient is a separate iff statement

The unaveraged horizontal metric is the semidefinite tensor

    q=gamma-gamma(V,.) tensor gamma(V,.)=x sigma1²+y sigma2².

It annihilates X3. For the principal circle quotient pi:S3->S2 it equals
pi* h for a unique base Riemannian metric h exactly when it is invariant along
the circle action (basicness); positivity on the horizontal spaces then makes
pi a Riemannian submersion. The horizontal distribution ker(sigma3) is invariant
even in the triaxial case, but its metric need not be invariant.

Cartan's formula and the fixed brackets give

    L_X3 sigma1=2 sigma2, L_X3 sigma2=-2 sigma1, L_X3 sigma3=0,
    L_X3 q=2(x-y)(sigma1 tensor sigma2+sigma2 tensor sigma1).

Consequently direct descent on a given diagonal slice is equivalent to x=y.
This is not a claim that the topological quotient ceases to exist or that no
other quotient metric could be defined by averaging or extra data.

At t=0 descent holds for every K because the initial geometry is Berger.
Descent on an open actual-time interval containing 0 holds iff the initial
horizontal K block is scalar: K11=K22 and K12=0 in the initial orthonormal
frame, equivalently BI1 d=s=0. Sufficiency: the complete data then also have
continuous axial symmetry, which extends by the same imported method, forcing
x=y locally. Necessity: in the initial diagonalizing frame

    d/dt (x-y)|0=-2A(k1-k2).

If k1!=k2 this derivative is nonzero; differentiability gives x(t)!=y(t)
for all sufficiently small nonzero t. Equality on an interval would force
k1=k2. In the original frame a symmetric 2x2 block has equal eigenvalues iff
it is scalar, giving d=s=0. Zero shear is necessary for DIRECT DESCENT on such
an interval, but it is not necessary for line, projector, closed-fibre or
normalized-integral persistence. Pure trace is stronger than horizontal
isotropy: k3 is unrestricted subject to the original Hamiltonian constraint.

The lawful BI1 witness A=1,C=9/4, Lambda=3 and orthonormal K eigenvalues
(1,2,-1/4) gives dot(x-y)=2. Its original branch and closed fibres persist
locally but direct descent immediately fails at nonzero small times. This is
a derivative-based departure proof for descent AFTER actual development has
been justified; it is not numerical integration or a zero-jet persistence
claim. Shear norm in the unrotated horizontal block is sqrt(d²+s²), so a K12
entry is retained by this test rather than deleted by diagonalization.

## Limits and evidence type

Only conditional mathematics in the supplied homogeneous Gaussian class is
claimed. No uniform/global time, smooth inhomogeneous census, arbitrary
foliation-invariant persistence statement, continuation through spectral
degeneracy, selected future universe, physical stability, common fixed carrier
target, action, mass, scale or canon. Imported Cauchy theory is not re-proved.
Exact curvature and Lie/ADM calculations test the algebra; their finite
fixtures do not certify the general method or replace the arguments above.
