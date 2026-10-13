# Kerr magnetic-curvature lead — source and check freeze

This continuation is separate from the immutable initial CANDIDATE/MANIFEST.
After that freeze, the coordinator supplied A's independent plane-wave result
and proposed a tentative vacuum quartic form (4 E^2-3 B^2)/360. Its generality
is UNPROVED here; two fitted controls cannot establish it. The coordinator also
proposed a Kerr principal-frame event with E=0 as a discriminator. This is
exposed parent-origin lead generation, not B's independent invention.

## Primary sources inspected

1. Bahram Mashhoon, *Critical Tidal Currents in General Relativity*,
   [arXiv:2007.12023v3](https://arxiv.org/pdf/2007.12023v3), Appendix C,
   equations C3--C8, PDF pages21--22. The canonical Kerr Petrov frame has
   diagonal electric and magnetic matrices with eigenvalue proportions(-2,1,1),
   determined by M/(r+i a cos(theta))^3. No tidal-motion equation from that paper
   is imported into FAC1. The published version has A43--A45 instead.
   The [2021 correction](https://www.mdpi.com/2218-1997/7/2/39) lists changes to
   earlier tidal-motion formulas; the inspected Appendix C component formulas
   are retained in the revised arXiv version.
2. Lode Wylleman, L. Filipe O. Costa and Jose Natario,
   *Poynting vector, super-Poynting vector, and principal observers in
   electromagnetism and general relativity*,
   [arXiv:2007.15384v2](https://arxiv.org/html/2007.15384v2), section6.2,
   equations147,155,159--161. These identify the Kerr-Newman coframe, type-D
   eigenvalues and the Carter timelike vector. Use the zero-charge Kerr
   specialization only. Their static-laboratory intermediary is not substituted
   for the Carter observer at/inside the stationary limit.

Sources were browsed directly. General observer arguments or matter/energy
interpretations from those papers are not UDT premises. The exact checks below
differentiate the metric independently of the quoted Weyl eigenvalue formula.

## Question and frozen checks

For the original Kerr metric in coordinates(t,r,y=cos(theta),phi), derive all
first/second metric derivatives, Christoffel products and covariant Riemann
components exactly at each test point. Transform the bivector curvature to the
orthonormal Carter frame. Check g(U,U)=-1, full Ricci=0, electric/magnetic
symmetry and traces, and compare their squared norms with the source formulas.
Use R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y]; test the electric sign against a
Schwarzschild radial tide. Magnetic orientation may reverse its sign but not
the squared norm.

Supplied free-and-explored points (all M=1):

- Schwarzschild sign/control: a=0,r=3,y=3/5.
- Parent extremal lead: a=1,r=sqrt(3/2),y=1/sqrt(2).
- B nonextremal control: a=sqrt(15)/4,r=3/2,y=2/sqrt(5), with
  r_plus=5/4,Sigma=3,Delta=3/16. E=0 is predicted. The point has gtt=0 but
  is regular and outside the horizon; Carter U remains timelike.
- Same nonextremal geometry at r=31/20, same y: strictly outside both horizon
  and stationary limit, testing magnetic dominance away from those surfaces.

The Carter vector specifies only the initial U for FAC1. The actual clock A
must then follow the unique geodesic with that tangent; it is not held on the
Carter orbit. Pointwise curvature E(U),B(U) uses that initial U. A general
quartic clock law would still need proof that its derivative/curvature terms
are exactly those claimed for this free preparation.

One exact SymPy check, TPS1 capture,2GiB,one thread,no timeout; coordinator CPU
slot approved. Preserve any failure before repair. No Kerr ray integration,
general vacuum-clock theorem, empirical Kerr claim, native admission or UDT
refutation is authorized by success of this algebraic control. Strong-field
Kerr compatibility is distinct from tested-regime SR/GR recovery.
