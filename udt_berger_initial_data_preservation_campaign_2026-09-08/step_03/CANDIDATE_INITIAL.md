# BI3 initial conditional candidate — UNREVIEWED, UNPROMOTED

## 1. Precise statement and scope

Fix any real analytic nonround Berger metric gamma on S3 with a,c>0,a!=c,
any point o and real h!=0. Set R=8/a²-2c²/a⁴ and fix Lambda=R/2+3h².
For every real epsilon there is an open neighborhood U of o and a real
analytic symmetric K_epsilon on U satisfying ALL original G315 vacuum
constraints at this SAME gamma,Lambda. At o,

    K_epsilon=h gamma,    D K_epsilon=0,
    Y(o)=(epsilon/Delta)e2,    Delta=4(c²-a²)/a⁴.                   (1)

Here Y is BI1's full initial normal-flow Ricci-line velocity, not a spatial
flow vector or physical worldline. For epsilon!=0 it is nonzero. The data
are ACTUAL analytic fields on a neighborhood, not just a compatible formal
jet. U may depend on the data/epsilon; no global S3 extension or uniform
lifetime/norm estimate is claimed. Analyticity and h!=0 are sufficient method/
construction restrictions here, not proved necessary or imposed physical laws.

Inputs are accepted G315/G330/G337 plus reviewed BI1 and its ENTIRE review,
including independent full-tensor verification and two author-harness false
passes. BI2 is NOT a dependency. G310/G312 remain owner-provisional. A standard
analytic CK theorem is imported as mathematical method, not a carrier, coupling,
source, action or selected data law. The paused optional source model is unused.

## 2. Exact original nonlinear constraint reduction

Use the analytic invariant initial orthonormal frame e_i, with
[e1,e2]=q e3,[e2,e3]=p e1,[e3,e1]=p e2, p=2/c,q=2c/a².
Seek a declared subfamily of smooth K, with only two entries prescribed:

    K=[[m,0,r],[0,m,w],[r,w,z]],
    z=(E-m²+r²+w²)/(2m), E=Lambda-R/2=3h², m!=0.                 (2)

Horizontal isotropy and K12=0 in this fixed invariant frame are a chosen local
construction restriction, not a claim that every lawful K has that form.
The mixed entries are free to vary spatially. The Hamiltonian holds identically
because m²+2mz-r²-w²=E, which is exactly half its quadratic part.

Let F=m+z=(m²+E+r²+w²)/(2m). Direct Koszul divergence, including the connection
terms of the noncommuting frame, gives the complete momentum system

    e3 m=(e1 r+e2 w)/2,
    e3 r=e1 F+(p-q)w,
    e3 w=e2 F+(q-p)r.                                          (3)

Indeed the original residuals are

    M1=-e1(m+z)+e3 r+(q-p)w,
    M2=-e2(m+z)+e3 w+(p-q)r,
    M3=e1 r+e2 w-2e3 m.

Equations (2)--(3) solve the full original constraints, not their linearization.
No spatially varying Lambda, omitted connection or new evolution equation is
introduced. The variable used to solve (3) below is a SPATIAL coordinate.

## 3. Actual analytic realization

Choose an analytic two-surface through o whose tangent plane AT o is spanned
by e1,e2, with local coordinates (u,v) so those coordinate tangents agree there.
Flow it by the analytic nonzero vector e3 to obtain coordinates (u,v,s),
e3=partial_s. This does not assert integrability of the horizontal distribution:
e1,e2 are tangent to the two-surface only AT the chosen point, not everywhere.
Write

    eA=a_A^b partial_b+b_A partial_s, A,b=1,2,
    a_A^b(o)=delta_A^b, b_A(o)=0.

For unknown U=(m,r,w), move all partial_s U terms of (3) to the left. The
coefficient matrix is

    A=[[1,-b1/2,-b2/2],
       [-b1 F_m,1-b1 F_r,-b1 F_w],
       [-b2 F_m,-b2 F_r,1-b2 F_w]].                            (4)

The remaining right side uses only U, tangential derivatives partial_u U,
partial_v U and analytic coefficients. At o, A=I. On m!=0, F is analytic;
therefore A^{-1} and the right side are analytic on a sufficiently small
neighborhood of the initial values where det A!=0. This is an actual
noncharacteristic normal system partial_s U=G(u,v,s,U,partial_u U,partial_v U).

Supply analytic data on s=0:

    m(u,v,0)=h, r(u,v,0)=0, w(u,v,0)=epsilon u²/2.               (5)

The standard local analytic Cauchy--Kovalevskaya theorem applies to (4)--(5).
It supplies a convergent analytic solution after shrinking about o. The
normal-form theorem, recursion and convergence proof are sourced in Leon
Simon's Stanford Lectures on PDE, Lecture3 pp21--26; see METHOD_SOURCE.md.
No finite check is substituted for that mathematical-method hypothesis.

At o, m=h!=0. Shrink U so m stays nonzero and (2) is analytic. Every momentum
residual vanishes on U by (3), and the Hamiltonian vanishes on U by (2).
Thus there is no remaining 'formal jets might not integrate' gap for this
LOCAL analytic construction. This says nothing about solving global S3 data,
joining to a specified exterior, or smooth nonanalytic-data well-posedness.

## 4. Exact two-jet of the realized data

Let T=K_epsilon-h gamma. At o, T=0. From (5), all tangential first derivatives
of U vanish. At the base values (h,0,0), F=2h, F_m=-1, F_r=F_w=0 and the
zeroth-order source in (3) vanishes. Since A(o)=I, all normal first derivatives
also vanish. Hence D T=0, independent of coordinate/frame connection choices.

Differentiate (3) once at o. Derivatives of its frame/normal-matrix coefficients
multiply first derivatives of U, which vanish; derivatives of the zeroth-order
source also vanish. With subscripts denoting coordinate derivatives at o,

    m_3j=(r_1j+w_2j)/2, r_3j=-m_1j, w_3j=-m_2j.               (6)

Tangential second derivatives from (5) have only w_11=epsilon nonzero.
For j=1,2, (6) forces all mixed normal second derivatives to zero; then j=3
forces all double-normal second derivatives to zero. Formula (2) gives zero
second derivative of z-h: its terms linear in second derivatives involve only
m, and its r,w dependence is quadratic with vanishing first derivatives at o.

Consequently the ONLY nonzero components of the covariant second derivative
of T at o are

    (D_1 D_1 T)_23=(D_1 D_1 T)_32=epsilon.                    (7)

This coordinate-to-covariant statement is exact: all connection and frame-
derivative corrections multiply T or D T, both zero at o. Also
[e_i,e_j] applied to the component difference vanishes at o because its first
derivatives vanish, so the displayed second-jet ordering is consistent.
These statements describe the convergent solution just established, not an
arbitrarily painted tensor jet on a nonintegrable horizontal plane.

## 5. Full first-normal line consequence

The uncommuted Ricci-variation operator is linear in K for fixed gamma. For
K0=h gamma it vanishes identically, since D K0=0. Substituting (7) in the
FULL operator gives

    Ric3-dot(K_epsilon)-Ric3-dot(K0)
       =epsilon(e2-flat tensor e3-flat+e3-flat tensor e2-flat) at o.   (8)

The two mixed-divergence second terms and Hessian of the trace are zero for
this jet; the covariant Laplacian term contributes (8). These cancellations
follow from (7), not from commuting derivatives or dropping curvature terms.

At o, K_epsilon=K0=h gamma, so the inverse-metric derivative is the SAME
diagonal 2hB in both data and contributes no mixed term. BI1 therefore gives

    P-dot(o)=epsilon/Delta [e2 tensor e3-flat+e3 tensor e2-flat],
    Pi V-dot(o)=Y(o)=epsilon e2/Delta.                            (9)

Here V denotes the unit Ricci-line representative, not the CK unknown U.
The unit representative's parallel normalization term h e3 is not drift.
Equation (9) proves (1); neither K(o) nor its first spatial jet suffices to
decide first-normal line preservation. The complete spatial data were always
legitimate supplied input. No additional physical law is needed for this
bounded mathematical departure.

Conditional on the same standard LOCAL smooth Einstein-Cauchy method with
its original constraints, these analytic data have a local development near
o; use a smaller open-patch domain of dependence, not a claim of compact
global extension. Its normally compared Ricci branch has derivative (9).
For epsilon!=0 differentiability gives actual fixed-line departure at the
marked point for every sufficiently small nonzero normal time. This does not
establish a change of closed-orbit structure, global fibration or topology.

## 6. Interpretation, countercontrols and ceiling

The construction supplies a family of exact local data, not a new recipe
adopted as physical content. It defeats the LOCAL assertion that the vacuum
constraints on a Berger background alone force the homogeneous no-drift
property. It does not defeat BI1's homogeneous theorem or prove a global
compact-S3 counterexample. A nonzero principal symbol alone would be weaker;
the analytically realized original constraints are the load-bearing bridge.

epsilon=0 has the constant pure-trace solution and zero drift. Either sign
of h is retained with the same Lambda; either sign of epsilon reverses the
drift. h=0 is outside this parametrization, not ruled out physically. Round
a=c removes the simple Ricci line and is outside (9), not an inadmissible
UDT geometry. No general stability, norm-controlled persistence, global
constraints/gluing, particle, old-carrier action, physical size/scale or canon.

Discovery: parent first noticed that the local momentum system is first-order
in the three unfixed entries after algebraic Hamiltonian elimination. A
transverse two-jet suggested drift; the flow-box noncharacteristic argument
and exact two-jet recursion were then supplied to establish realization.
No BI3 whiteboard or reviewer argument/code/results was read before this
initial author construction; BI1 reviewed reconstruction was used openly.
