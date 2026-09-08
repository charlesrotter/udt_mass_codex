# Independent source-first BI3 construction

This argument is derived before BI3 author proof/code/results exposure. It
uses accepted G315/G330/G337 and provisional reviewed BI1 with all limits.
Discovery is mathematical and targeted; the witness data below were selected
to answer the stated existence question, not inferred to be typical.

## Exact nonlinear spatial construction

Use the analytic invariant orthonormal Berger frame and write

    K=[[x,u,v],[u,y,w],[v,w,z]], p=2/c, q=2c/a^2,
    E=Lambda-R/2=3h^2, h!=0.

Koszul gives Gamma12^3=q/2, Gamma21^3=-q/2, Gamma13^2=-q/2,
Gamma23^1=q/2, Gamma31^2=p-q/2, Gamma32^1=q/2-p.
The full four constraints, not their linearization, are

    xy+(x+y)z-u^2-v^2-w^2=E,
    -e1(y+z)+e2(u)+e3(v)+(q-p)w=0,
    e1(u)-e2(x+z)+e3(w)+(p-q)v=0,
    e1(v)+e2(w)-e3(x+y)=0.

In the open set x+y!=0 the scalar constraint is solved EXACTLY by

    z=F(x,y,u,v,w)=(E-xy+u^2+v^2+w^2)/(x+y).

Prescribe the analytic free functions y=h and u=0 on the whole patch. The
unknowns are U=(x,v,w). Choose any point o and an analytic spatial coordinate
chart (r,t,s), centered at o, whose differentials there are the coframe dual
to (e1,e2,e3). Such a chart exists by an invertible linear change of an
analytic chart. Write e_i=A_i^r partial_r+A_i^t partial_t+n_i partial_s.
At o, A_i^alpha=delta_i^alpha and (n1,n2,n3)=(0,0,1).
The frame is NOT a commuting coordinate frame on a neighborhood. In particular
the horizontal distribution is not claimed tangent to every s-level surface.

After substitution the exact three momenta have normal matrix

    M = [[-n1 F_x,       n3-n1 F_v, -n1 F_w],
         [-n2(1+F_x),   -n2 F_v,    n3-n2 F_w],
         [-n3,          n1,          n2]]

against partial_s(x,v,w). All other terms are analytic functions of
(r,t,s,U,partial_r U,partial_t U), including the noncommuting-frame connection
terms (q-p)w and (p-q)v. At U=(h,0,0), F=h and
F_x=-1,F_v=F_w=0. At o, det M=-1. Thus M is invertible in an open neighborhood
of the initial state and point. The nonlinear equations are an analytic
first-order normal-form system partial_s U=G(r,t,s,U,partial_r U,partial_t U).

On the analytic surface s=0 supply

    x=h, v=epsilon*t^2/2, w=0,   epsilon any real nonzero constant.

At o, x+y=2h!=0 and det M=-1. Shrink the analytic initial surface around o so
both nonvanishing conditions persist. The analytic normal-form CK theorem
therefore gives an actual convergent local real-analytic solution U, hence K.
The algebraic substitution and all three reduced equations are equivalent
to the ORIGINAL constraints throughout its open patch at the SAME constant
E=3h^2 and Lambda. No omitted constraint requires a separate propagation
argument. CK uniqueness is only for this chosen reduction/free data/surface;
it is not uniqueness of all constraint solutions or of physical initial data.

The method invoked is standard local analytic normal-form existence, as in
Leon Simon, Lectures on PDE, Lecture 3, pp21--26,
https://math.stanford.edu/~lms/lecs-on-pde.pdf. Its role is convergence/existence
once analyticity and noncharacteristic normal form are established here. It
is an explicitly imported mathematical method, not an added physical premise.

## Jet of the actual solution

The exact baseline y=x=z=h,u=v=w=0 solves this same system. Set L=K-h gamma.
The boundary values have L(o)=0 and zero tangential first derivatives. The
invertible normal system then gives partial_s L(o)=0 as well. Consequently
L(o)=0 and DL(o)=0; the two data sets have the same K and first derivatives
in a coordinate-invariant sense, not only constant-looking frame components.

When differentiating momenta once at o, coefficient-derivative and connection
terms multiply L or its first derivatives and vanish after baseline
subtraction. Algebraic Hamiltonian differentiation gives z_ab=-x_ab because
y,u are constant and the lower L jet vanishes. With indices 1=r,2=t,3=s,
the differentiated system reduces to

    v_3b=-x_1b, w_3b=0, x_3b=v_1b+w_2b,   b=1,2,3.

The prescribed tangential Hessians have only v_22=epsilon. Solving the above
mixed and then double-normal derivatives shows that every other second
derivative of L vanishes. These are the derivatives of the actual CK solution,
not a separate unproved formal jet. Noncommuting e_a e_b adds a commutator
times the vanishing first derivative of L, so it changes no second-jet value
at o. It must not be ignored for higher derivatives or away from this point.

The naive polynomial retaining only this second jet is NOT an exact solution:
with x=y=z=h, v=epsilon*t^2/2 its scalar residual is -epsilon^2*t^4/2 in the
full G315 Hamiltonian. Even replacing z by its algebraic solution alone does
not establish momentum away from o. Analytic CK supplies the higher-order
corrections to all unknowns required by every equation.

## Full first-normal drift

G315 fixes dot(gamma)=-2K. For K0=h gamma, the spatial metric initially varies
by a spatially constant homothety, so dot(Ric3)_ij=0 as a covariant tensor.
The variation operator is linear in K. For L(o)=DL(o)=0, every curvature,
connection and first-derivative correction to its second-derivative part
vanishes at o. This is a proved specialization of the FULL G337 operator:

    S_ij=-D^k D_i L_kj-D^k D_j L_ki+D^k D_k L_ij+D_i D_j tr L.

With only (D2 L)_22,13=(D2 L)_22,31=epsilon nonzero,

    S=[[0,0,epsilon],[0,0,0],[epsilon,0,0]].

This is also obtained directly by differentiating the connection variation
and its Ricci contraction in spatial normal coordinates: L and DL vanish,
so no connection correction is suppressed without justification. A separate
full covariant implementation keeps all connection slots and verifies this.

The inverse metric term is still present: dot(B)=S+2K^sharp B at o. Here K is
hI, so it contributes only the diagonal 2h B; the mixed block remains S_hv.
With Delta=q(q-p)=4(c^2-a^2)/a^4!=0, reviewed BI1 yields

    Y=(epsilon/Delta)e1 !=0,
    dot(P)=(epsilon/Delta)(e1 tensor theta3+e3 tensor theta1).

Thus actual local analytic lawful K can match the pure-trace control through
first spatial order at a point but have different first-normal image-line
and full-projector drift there. This holds for each positive nonround Berger
geometry and every h!=0 with the stated SAME Lambda, on a possibly smaller
patch depending on the supplied parameters. No uniform existence radius is
claimed and h=0 is not covered by this reduction.

Conditional on the already admitted local smooth Einstein-Cauchy method,
restrict to a smaller relatively compact spatial patch and its local domain
of dependence. The simple Ricci eigengap stays open near the marked event
for a short time. Under Gaussian normal comparison the nonzero derivative
gives actual local line departure, via its nonzero linear term in time. The
spatial CK coordinate s is NOT this physical normal time. No global compact
extension, closed-orbit assertion, topology change, stability, genericity,
matter/particle interpretation or physical scale follows.

## Evidence and independence

The source-first executable reconstructs the momentum connection, checks
Hamiltonian elimination and the normal matrix, computes the complete
covariant variation, and compares a direct connection-variation contraction.
It imports no BI3 author or BI1 code. It shares SymPy, declared sources and
the standard variation method; different implementation does not imply a
different reviewer/model. The exact checks support algebra, not CK convergence
or universal quantifiers, which are supplied by the explicit argument above.
