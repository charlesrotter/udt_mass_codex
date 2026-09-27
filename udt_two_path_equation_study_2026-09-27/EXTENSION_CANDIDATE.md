# Extension path: quadratic-curvature response under DDR

Source-exposed candidate; actual checks/review state is recorded in CLOSEOUT.md.
This is an explicitly CHOSEN, UNADOPTED counterfactual. No native UDT law or
physical source is asserted. The starting c postulate is fixed; c_E is only
measured clock/ruler calibration. The point of this example is to test a changed
metric response while retaining the shared reciprocal geometry, not to add a
second signal speed or fit a desired redshift profile.

## A. Chosen response and premise changes

Let L(R)=R+alpha R^2, F=dL/dR=1+2alpha R in four dimensions. Alpha is a real
constant with dimensions length^2, free-and-explored. Use smooth Lorentzian
Levi-Civita geometry and compactly supported variations on an open patch; no
physical boundary term or selected universe boundary is introduced.

The metric variational response is

    E_ab = F Ric_ab - (L/2)g_ab + (g_ab box - nabla_a nabla_b)F.       (E1)

For this path only, CHOOSE E as the physical symmetric response on which the
existing all-pair DDR condition acts. This identification is the unsupported
native join made explicit as a counterfactual hypothesis. We do not impose
unrestricted action stationarity E=0. The field condition is

    TF(E)=0.                                                        (E2)

Applying the registered DDR condition to this chosen fourth-order response is
part of the unadopted counterfactual. Neither DDR nor Local Metric Sufficiency
admits this response architecture or establishes physical population of all
diagnostic pair planes.

Equivalently, with S_ab=Ric_ab-(R/4)g_ab, the full covariant candidate equation is

    (1+2alpha R)S_ab
       -2alpha[nabla_a nabla_b R-(box R/4)g_ab]=0.                 (E2a)

The f(R) template is established external mathematics; no novel-theory claim
is made. What is being tested here is its explicitly chosen response under DDR
and the complete reciprocal primary geometry.

Compared with the full conditional G301 class, this choice permits fourth metric
derivatives and a supplied dimensionful coefficient. Its operator no longer has
the exact curvature-weight-one property at fixed alpha. It retains metric-only
locality, symmetric tensor type and coordinate covariance. Local Metric Sufficiency
does not by itself forbid finite fourth-jet response. None of these permissions
establishes that UDT owns the choice, that it is unique, or that its extra
dynamical content is acceptable. No independent scalar field is assumed as a
fundamental object, but higher derivative curvature dynamics are present.

E1 is standard metric f(R) mathematics used as an external template. The local
variation identity delta R=Ric_ab delta g^ab+(g_ab box-nabla_a nabla_b)delta g^ab,
with two integrations by parts, gives E1. Contracted Bianchi and the scalar-gradient
commutator give nabla^a E_ab=0 identically. This is a property of the chosen
response, not a separately derived UDT conservation law. Consequently E2 implies

    E_ab=C g_ab,   C constant on a connected regular region,
    -R+6alpha box R=4C.                                             (E3)

C is an unfixed trace integration datum, not zero by default and not a selected
physical scale. Omitting it would discard solutions allowed by DDR. For fixed
smooth metric data E_alpha tends to G as alpha tends to zero; E2 then becomes
TF(Ric)=0, the existing conditional Einstein branch. This is an operator check,
not uniform convergence of all alpha-dependent solution families.

## B. Exact primary static reciprocal branch

Retain the full primary areal metric

    ds^2=-f(r)(dx0)^2+dr^2/f(r)+r^2 dOmega^2,  x0=c_E t,

on a connected open interval r>0 with smooth f>0. Spherical symmetry and staticity
are a restricted test sector; no conclusion below covers arbitrary dynamic or
nonspherical UDT. All angular curvature is retained. Source geometry gives

    R=-f''-4f'/r-2(f-1)/r^2,
    (Hess R)^t_t=f'R'/2,
    (Hess R)^r_r=f R''+f'R'/2,
    (Hess R)^theta_theta=(Hess R)^az_az=f R'/r,
    box R=f R''+(f'+2f/r)R'.                                       (E4)

The time/radial Ricci entries agree in this metric. Thus

    E^r_r-E^t_t=-2alpha f R''.                                     (E5)

For alpha!=0, E2 forces R''=0 everywhere in this regular interval. Write
R=u r+v, where u,v are constants. Integrating the displayed definition of R
gives the COMPLETE local f family under this necessary condition:

    f=1+p/r+q/r^2-v r^2/12-u r^3/20.                              (E6)

p,q are integration constants; no matter, charge or particle meaning is assigned.
Substitution into the trace equation E3 yields, after multiplication by r^2,

    -(3/2)alpha u^2 r^4 +(-u-2alpha u v)r^3
      +(-v-4C)r^2+12alpha u r+6alpha u p=0.                       (E7)

This polynomial must vanish on an open interval, not at sampled radii. The
linear coefficient and alpha!=0 force u=0; then v=-4C. The full remaining
tensor equation reduces to

    (1+2alpha v) q=0.                                             (E8)

The exact local classification therefore has TWO strata:

1. **Nondegenerate, 1+2alpha v!=0:** q=0 and
   f=1+p/r-v r^2/12, Ric=(v/4)g. There is no new static reciprocal vacuum
   solution family relative to the conditional Einstein class in this sector.
   The entire response law has not thereby been proved equivalent to GR.
   "Nondegenerate" here means only this scalar coefficient is nonzero, not
   that the full differential system has been certified nondegenerate or stable.
2. **Degenerate, 1+2alpha v=0:** v=-1/(2alpha), C=1/(8alpha), and
   f=1+p/r+q/r^2+r^2/(24alpha), with q free and positivity imposed only on the
   chosen interval. These are exact local solutions of E2. For q!=0 they are
   non-Einstein; they must not be removed by division by F or mislabeled as a
   source/charge. No global regularity, physical viability or stability is proved.

The alpha=0 case is handled separately and gives only the Einstein family in
this static sector. At fixed finite alpha, the two strata exhaust this stated
smooth positive static ansatz because E5--E8 are necessary and direct substitution
verifies sufficiency. The exceptional curvature diverges as alpha approaches zero,
so that branch has no bounded-curvature zero-alpha limit. This is not an
exhaustive classification of the full
counterfactual theory or of UDT. In particular no horizon or center is included
by the r>0,f>0 proof; no boundary condition is silently chosen.

## C. Why the exceptional branch needs separate interpretation

At the exceptional constant scalar curvature R0=-1/(2alpha), the coefficient F of
Ricci vanishes. This is algebraic degeneracy of the chosen response, not grounds
to reject an exact admitted counterfactual solution by appearance.

For a fixed integration datum C and a perturbation h about such a background,
linearizing E-Cg gives

    delta(E_ab-Cg_ab)
       =2alpha[delta R Ric_ab+(g_ab box-nabla_a nabla_b)delta R].    (E9)

Thus directions with delta R=0 receive no first-order restoring condition from
that linearized residual. This establishes a precise loss of linearized response,
not nonlinear instability, a ghost theorem, well-posedness failure, or physical
admission. The non-Einstein branch is retained as a degenerate survivor with that
limitation. Selecting it as UDT physics would require additional justification.

For any constant-R solution background at fixed C, the trace linearization is

    (6alpha box_background-1)delta R=0.                           (E10)

If the connected integration datum varies, the right side is instead 4 delta C.

For alpha!=0 its scalar principal cone is that of the background metric. This
checks one linearized scalar equation only. It does not certify causal propagation,
energy sign, stability or well-posedness of the full fourth-order system. A formal
scalar equation also does not by itself prove that every scalar solution lifts
to a full metric perturbation. No particle or physical mass is identified.

## D. Discovery history, test plan and stop

The parent explored E5--E10 algebraically before freezing this initial candidate.
It is not an outcome-blind preregistration. Exact checks reconstruct the
full geometric tensor and Hessian, verify the trace/divergence, both strata,
nonzero-q exceptional witness, failure of nondegenerate nonzero-q, alpha=0,
and linear-response cancellation (52 checks PASS, 2.525 seconds, Python 3.10.12 /
SymPy 1.13.1). A separate source-first worker received the
hypothesis and domain but not this proof or its expected strata.

The model is a transparent test case, not a preferred theory derived from the
c postulate. Its generic static return to Einstein and exceptional degeneracy
must be reported together. Do not add another curvature term to rescue it here.
The outcome does not settle time-dependent/nonspherical sectors or other extensions.

External primary derivation: A. Guarnizo, L. Castañeda and J. M. Tejeiro,
*Boundary Term in Metric f(R) Gravity: Field Equations in the Metric Formalism*,
arXiv:1002.0617v4, equations (3.8), (3.14), (3.25).
https://arxiv.org/html/1002.0617v4
Consulted by the separate reviewer before candidate exposure, and by the parent
during direct review on 2026-09-27. Compactly supported variations supply our
local boundary prescription. The source supplies the variational identity, not
UDT adoption; DDR insertion and the classification require the arguments above.
Earlier parent exposure: Sotiriou and Faraoni, arXiv:0805.1726, equations (6)--(8),
is a review, not the primary derivation. This provenance correction is recorded
without rewriting the initial candidate.
