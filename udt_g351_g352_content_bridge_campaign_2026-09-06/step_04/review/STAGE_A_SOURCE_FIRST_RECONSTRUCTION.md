# Step 4 source-first reconstruction, sealed before author disclosure

Reviewer /root/content_campaign_step04_review, 2026-09-06. Fresh separate
context; exact runtime model UNKNOWN; different-model axis UNTESTED. This
stage saw definitions, work order, startup/method sources and reviewed Step
1-3 dependencies, including their verdicts. It saw no new Step 4 author
argument, code, result or verdict. This is an independent reconstruction of
the stated mathematical question, not yet a direct candidate verdict.

Initial HEAD was 6a3755bb2b059a30c004ee3c246dd36043f5c8aa on grok, with
unrelated untracked work present. The dispatch forbids checkout/fetch/pull
and repository mutation. Only fresh /tmp scratch was written. Remote freshness
is unverified by this review. The user-supplied AGENTS text was available from
startup; disk AGENTS was additionally read fully before this seal. The bounded
status/method chain was read, and orientation preceded computation. The full
premise audit was not repeated per dispatch; inherited actual pass records
are distinguished from this reviewer's checks in STAGE_A_PLAN.md.

## Exact source seam

G351 EXACT_DERIVATION sections 2-3 requires a supplied standard finite
nonnegative countably additive label measure unchanged along source-free
cuts; it supplies neither the measure nor populated labels. Its regular
density is s/J. G352 EXACT_DERIVATION sections 1-2 requires a supplied
dimensionless phase with nonzero future-raised null gradient, positive fixed
spacing Delta, and the explicit continuous product (|dTheta|/Delta) tensor mu
with ONE phase-independent transverse measure. It then gives
Gamma=(omega/Delta)s/J. The product choice is not derived from G351 or the
metric. Section 4 admits common positive affine phase/spacing gauge, not
arbitrary nonlinear reparameterization at fixed spacing. Its full exact
registry row and current audit keep physical realization/identity open.

The reviewed UNPROMOTED Step 3 supplies, conditionally on its chosen
curvature/first-dual recipe and smooth local harmonic Brinkmann arena,

    g=-2du dv+dx^2+dy^2+H(u,x,y)du^2, Hxx+Hyy=0,
    N=Hxx^2+Hxy^2>0, b=N^(1/4), beta=-b du,
    C0=b partial_v, alpha=db/b, q=(b_x^2+b_y^2)/b^2.

On q>0, D=qC0 has quotient measure w|du|dxdy, w=qb>0. Conservation
div D=partial_v w=0 leaves arbitrary u-dependence in w. A different aligned
phase k=dTheta=-kappa(u)du is permitted mathematical input, with kappa>0;
it is not another normalized root of the same fixed B except where kappa=b.
No physical action, source, observer, length or content law is supplied by
this reconstruction. Prior review is a conditional dependency, not promotion.

## Positive fixed-label factorization theorem

Let I be an interval, V a connected transverse open patch, and w>0 smooth
on I x V. Use its fixed product labels. For fixed Delta>0 the following are
equivalent, subject to finiteness on the retained label query:

1. w|du|dz=(kappa(u)|du|/Delta) tensor mu for some smooth kappa>0 and one
   phase-independent nonnegative measure mu;
2. w(u,z)=A(u)f(z) with smooth positive A,f;
3. for all points in the domain, w(u,z)w(u0,z0)=w(u,z0)w(u0,z);
4. d_z(partial_u log w)=0 throughout I x V.

For (1), integrate equality over a nonempty compact subinterval of I.
Because its integral of kappa is finite and positive, mu is absolutely
continuous with density s proportional to the integral of w over that
subinterval. This is positive and smooth locally in z. Fubini gives
w=kappa s/Delta almost everywhere; smoothness then gives equality everywhere.
Thus allowing singular mu cannot evade factorization of a smooth positive
w on this product. This argument avoids taking a conditional density on one
measure-zero phase slice. Conversely (2) gives kappa=A and s=Delta f after
consistent phase units, with Theta=-integral kappa du+constant. Product
measurability and countable additivity follow from the smooth positive density.

(2) implies (3)-(4). Equation (3), for fixed basepoint (u0,z0), directly
constructs A(u)=w(u,z0) and f(z)=w(u0,z)/w(u0,z0). For (4), connectedness
of V makes partial_u log w independent of z; integrate along the interval I
to obtain log w=F(u)+G(z). Exponentiation proves (2). A disconnected V
would need a common phase factor across its components; the pointwise
derivative condition alone would not impose that. Positivity prevents zero
support ambiguities. These are analytic implications, not a finite grid claim.

The smooth local theorem alone does not prove global finite total mass.
Restricting V to a supplied compact query patch whose closure lies in the
regular region makes s bounded and integrable. Bounded phase intervals with
compact closure likewise give finite Xi. Singular boundaries and global
completions are outside this claim. A phase-dependent relabelling can change
the product question; a fixed invertible relabelling preserves separability
because its Jacobian is independent of u.

If two factorizations of the same w have kappa_1,kappa_2 and spacings
Delta_1,Delta_2, positivity yields kappa_2=c kappa_1 for one c>0 and
s_2=(Delta_2/(c Delta_1))s_1. Phase origins are arbitrary. The common affine
gauge Theta_2=c Theta_1+d, Delta_2=c Delta_1 holds mu fixed. Scaling phase
at fixed spacing instead changes mu inversely; changing spacing at fixed
phase changes mu proportionately. Those are different product inputs for
the same Xi, not the G352 fixed-mu gauge. An arbitrary nonlinear phase
change cannot preserve this fixed-label product with constant spacing and
the same w unless its derivative is constant over the retained interval.

## Stationary cubic existence and full readout

For H=x^3-3xy^2 in supplied length units, let r=sqrt(x^2+y^2)>0. Direct
differentiation gives N=36r^2 and

    b=sqrt(6) sqrt(r), q=1/(4r^2), w=(sqrt(6)/4)r^(-3/2).

This positive w is independent of u and factors exactly. Choose a constant
kappa>0 and Theta=-kappa u+constant; then

    dmu=(Delta/kappa)w dxdy.

Every constant positive kappa is possible, with the stated compensating
normalization. Necessity forces constant kappa for this stationary w and
nonzero mu on fixed labels. The construction changes the phase normalization
from beta=-sqrt(6)sqrt(r)du, which is not closed. It does not erase the
original root's transverse variation or make D-flat a phase gradient.

For a full arbitrary unit observer, choose a>0 and arbitrary real p,t, and

    U=(a,(1+p^2+t^2+H a^2)/(2a),p,t).

Then g(U,U)=-1 and g(U,partial_v)=-a<0 fixes the chosen future cone.
The full covector k=(-kappa,0,0,0) raises to K=(0,kappa,0,0), is null,
and omega=-k(U)=kappa a>0. A fixed-phase graph cut v=F(x,y) has tangent
columns (0,Fx,1,0) and (0,Fy,0,1), so its full Gram matrix is identity.
Adding the required multiples of K to make those columns U-orthogonal
preserves that Gram matrix. No transverse-velocity or H term was dropped
from the normalization calculation. Thus J=1 in these labels, and

    Gamma=(kappa a/Delta)(Delta w/kappa)=a w=-g(U,D).

Under another regular fixed transverse chart, both s and J acquire the same
absolute Jacobian, giving the same rate. This realizes the original
geometric-current readout for all finite future observers in this local
query. It does not generate an observer, worldline interception, source or
population. Along each fixed (u,x,y) generator, w and the label measure stay
constant in v; D is conserved independently of the cross-phase criterion.

An exact finite example chooses kappa=sqrt(6), Delta=2 and the annular
sector 1<=r<=4, 0<=angle<=1. In polar labels dmu=(1/2)r^(-1/2)dr dangle,
whose total is 1. These are supplied query edges away from r=0, not a
physical boundary or selected scale. At (x,y)=(1,0), a=1/2, the readout is
sqrt(6)/8. At (4,0), a=3/2, it is 3sqrt(6)/64. These different transverse
labels are point witnesses, not an endpoint transfer-ratio comparison.

Restoring H=(x^3-3xy^2)/L^3 merely records the supplied metric/example
normalization: b has inverse-length units, q inverse-area, w inverse-volume,
s inverse-area for dimensionless phase/spacing and kappa inverse-length.
Both mu and Xi are dimensionless geometric amounts, while Gamma has
inverse proper-length times inverse-area units in the metric convention.
This makes them dimensionally count-compatible, not literal atomic counts.

For constant homothety g->h^2g at fixed covector phase/root and coordinates,
q->h^-2 q, C0->h^-2 C0, D->h^-4 D, volume->h^4 volume. Hence i_D vol,
Xi and the factorized mu remain invariant. U->U/h, omega->omega/h and
area->h^2 area give Gamma->h^-3 Gamma, matching -g(U,D). It would be
incorrect to scale the original normalized-coordinate formula qb alone and
call that the quotient measure after homothety; the inverse metric and
volume factors must both be included.

## Explicit conserved phase-varying failure

Take H=Re(z^3+u z^4)=x^3-3xy^2+u(x^4-6x^2y^2+y^4). Each slice is
harmonic. Put r2=x^2+y^2,

    F=1+4ux+4u^2 r2, G=1+8ux+16u^2 r2.

Independent differentiation from H gives

    N=36r2 F, q=G/(4r2 F),
    w=(sqrt(6)/4)G/(r2 F)^(3/4).

On a product neighborhood of u=0 and any compact transverse patch away
from r2=0, F,G stay positive after restricting I. Thus the same smooth,
nonzero, positive current/measure domain applies. At u=0,

    partial_u log w=5x,
    partial_x partial_u log w=5.

The fixed-label factorization criterion fails on every such open patch.
D is still conserved because its coefficient is independent of v. This
is an actual counterexample to replacing product compatibility by current
conservation, and to asserting that every positive harmonic-wave amount
admits an aligned-phase product on these fixed labels.

An independent exact four-point discriminator, using w^4 to eliminate
positive fourth roots, gives a nonzero rank-one minor 3734393/150994944
at u in {0,1/4}, x in {1,2}, y=0. Positivity makes fourth powers faithful
for this rejection. The differential argument bears the open-domain
quantifier. Failure is limited to this current, labels and aligned phases;
it is not a no-go for all cross-phase identifications, phase families,
metric classes or G352 realizations.

## Checks, limits and pending direct review

The independent code imports no new author module and read no new author
output. It differentiates the metric/profile inputs, uses full 4x4 metric
and 4-component covector/observer checks, and exact positive/rational
factorization witnesses. It passed 33 guard groups, rc0, Python 3.10.12,
SymPy 1.13.1, 0.602912 s and maximum RSS 50,820 KiB under enforced 512 MiB
and 60-second limits. stdout/stderr and exact command metadata are preserved.
No unexpected mathematical or implementation failure occurred in this stage.
Those counts organize checks; they are not 33 independent proofs. Finite
arithmetic alone does not prove the factorization theorem or physical content.

Not repeated: full prior curvature tensor derivation, historical packages,
prior proof reviews, whole 335-row premise verifier, repository-wide tests,
observational archives, global completion, caustics, atomic crossing models,
nonaligned phases or variable label-identification constructions. The Step 3
tensor/recipe result is inherited with its reviewed UNPROMOTED conditional
scope. Current accepted source hashes and work-order/dependency hashes are
recorded; hashes establish correspondence, not truth or trusted chronology.

The strongest independently reconstructed survivor is a local positive
factorization/data theorem, a finite dimensionless geometric realization
on the stationary cubic branch using a DIFFERENT supplied phase, and a
bounded conserved-current counterexample on a phase-varying branch. None
identifies physical content, selects phase/spacing/support/labels/recipe,
adopts a count law, changes accepted grades or canon, or removes the
G351/G352 owner-provisional premise stamps. Direct author review is pending.
