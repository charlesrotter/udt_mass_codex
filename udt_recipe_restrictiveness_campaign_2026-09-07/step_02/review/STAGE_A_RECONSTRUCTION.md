# RC2 independent source-first reconstruction

Frozen before opening new RC2 candidate/proof/code/results. The reviewed RC1
argument and full direct report were permitted inputs; their tangent-only
claim is not assumed to be an exact vacuum family. Exact model UNKNOWN;
fresh context YES, independently implemented calculations YES, other-model/
human/formal review UNTESTED. Shared SymPy/tensor methods and the unchanged
resource wrapper are disclosed; no author scientific code was imported.

## Admitted equation, recipe and exact completion

The examined original equation is Ric(g)=0 within the owner-provisional
G312/G313 Einstein arena. The sector is chosen for this question, not selected
by UDT. G355/G358/G361 specify Q_abcd=g(R(a,b)c,d), the FIRST-pair Hodge dual,
and B_abcd=g^ef g^hi(W_aech W_bfdi+starW_aech starW_bfdi).
In vacuum W=Q. Full B=beta^4 for a nonzero real future-raised null beta and
full ambient nabla beta=alpha tensor beta are separate recipe requirements.
G361--G363 keep restricted data and chosen product assumptions; nothing here
identifies physical content, an instrument, a population, a scale or canon.

Independently constructed the coordinate metric

    g=-2du dv+dx^2+dy^2+Hdu^2+2 epsilon x^2du dy,
    H=x^3-3xy^2-2 epsilon v y+c epsilon^2x^4.

Its connection matrices give the exact full Ricci tensor

    Ric=-2 epsilon^2 x^2(3c-2)du^2, scalar R=0.

Thus c=2/3 supplies an ACTUAL local Ricci-flat family, including finite
epsilon. The O(epsilon^2) correction leaves RC1's complete first variation
unchanged. The old c=0 family remains off-equation and is not reclassified.
The metric determinant is -1; completing the transverse square leaves a
2D block of determinant -1, so the signature is Lorentzian everywhere.

On t=v+2u=0, use tangent columns X=(partial_u-2partial_v,partial_x,partial_y).
The complete data, before any claimed constraints, are

    S=H+4-epsilon^2 x^4,
    gamma=X^T g X,
    n=-g^-1(dt)/sqrt(S),
    K_ij=-X_i^a X_j^b(2 Gamma^u_ab+Gamma^v_ab)/sqrt(S).

At p=(0,0,1,0),epsilon=0, S=5. Continuity supplies one smaller regular open
graph neighborhood and sufficiently small real epsilon with S>0. All inverse,
cross, lapse/shift and normal terms are retained. The source-first metric
code verifies det(gamma)=S, normal unit norm and all orthogonality components.
The intrinsic checker constructs its OWN three-dimensional connection,
curvature, K contractions and momentum divergence from gamma/K: the original
Hamiltonian and all momentum residuals vanish as exact open-patch expressions.
No ambient Ricci projection is reused in those intrinsic residuals.

At p, independently computed ALL256 B slots with the full metric contractions
and first dual. Two relevant entries and one rank-one necessary minor are

    B_uuuu=4(25 epsilon^4+51 epsilon^2+27)/3,
    B_uxux=2 epsilon^2, B_uuux=0,
    B_uuuu B_uxux-B_uuux^2
      =8 epsilon^2(25 epsilon^4+51 epsilon^2+27)/3.

This is strictly positive for every nonzero real epsilon. EVERY covector
fourth power must make this minor zero, so no real covector root exists at p
for any such epsilon, independent of a proposed null direction or extractor.
All baseline slots recover36 du^4. This is an exact lawful departure from the
chosen algebraic recipe, not a failure of the original metric equation.
One event suffices to refute a neighborhood root; it is not a finite-sampling
argument for genericity, codimension or classification of all solutions.

## Full-root algebra and local recurrence integrability

At an arbitrary event, choose an oriented orthonormal frame with future
L=e0+e3 along beta-sharp, so beta=b(-e0-flat-coordinate+e3-flat-coordinate)
has components b(-1,0,0,1), b>0. Use G358's COMPLETE vacuum Weyl representation,

    E=[[a,d,e],[d,b,f],[e,f,-a-b]],
    M=[[m,p,q],[p,n,r],[q,r,-m-n]].

Here the temporary matrix coordinate b is unrelated to root scale. Direct
independent FIRST-dual contraction gives the following exact sum of squares:

    B0000+B0003 =
      (a+b)^2+(a+p)^2+(b-p)^2
      +(d-m)^2+(d+n)^2+(m+n)^2
      +(e+r)^2+e^2+r^2+(f-q)^2+f^2+q^2.

A full fourth power along b_root(-1,0,0,1) makes the left side zero. REAL
sum-of-squares vanishing therefore forces

    b=-a, p=-a, m=d, n=-d, e=f=q=r=0.

No indefinite cancellation, restricted tensor subspace or dropped component
is allowed. Substitution in the FULL source Weyl representation gives
Q_ab0d+Q_ab3d=0 for every a,b,d. Thus R(X,Y)beta-sharp=0 for all X,Y.
Conversely the retained two-parameter class has full B=4(a^2+d^2)L-flat^4;
its zero member is excluded by the nonzero-root hypothesis. Exact symbolic
checks verify the entire64-component annihilation and256-component identity.
The saturation quadratic's separately computed Gram eigenvalues are
3(multiplicity6),1(multiplicity2),0(multiplicity2), consistent with the displayed
analytic squares and their two-dimensional kernel. The squares, not an
eigenvalue count or an assertion count, own the arbitrary-event quantifier.

Now assume FULL smooth recurrence of this SAME beta on a Ricci-flat
neighborhood. For a covector, curvature commutation gives

    (nabla_X nabla_Y-nabla_Y nabla_X-nabla_[X,Y]) beta
       =-beta composed with R(X,Y)=dalpha(X,Y) beta.

Metric skew-adjointness and the preceding algebraic annihilation make the
left side zero. Since beta is nonzero, dalpha=0. After shrinking to a
contractible coordinate ball, the ordinary local closed-one-form integration
gives alpha=dF (for example the radial integral formula, differentiated using
dalpha=0). Hence

    ell_flat=exp(-F) beta, nabla ell_flat=0.

This is a nonzero future parallel local representative with a positive
rescaling. The auxiliary representative may be multiplied by a positive
constant; beta itself remains the fixed normalized fourth root. It need not
be parallel or closed before that rescaling. Recurrence alpha is unique for
nonzero beta. Smoothness/contractible shrinking are essential; no global
parallel representative or topology conclusion follows.

Root alone gives curvature annihilation but does not supply recurrence or
the differential implication above. Recurrence of another null line does
not supply annihilation of THAT line from the root argument. No general
classification of every root-only metric is claimed. In an already ACTUAL
development this proves local necessity of a parallel representative for
the full recurrent-root recipe domain. Its restriction to any small spacelike
patch satisfies the G361 full seed equations. This does not remove G362's
separate conditional wave-method hypothesis for constructing a parallel
extension from initial data, nor give a general initial-data/PDE theorem.

## Evidence and retained diagnostic

Runs use Python3.10.12/SymPy1.13.1, exact expressions, no tolerance, one child
at a time under512MiB/60s. The initial intrinsic comparison failed because
SymPy factor left momentum zeros as unevaluated0*sqrt(3), exposed by a second
preserved run. Exact final simplification corrects only the structural zero
comparison; all geometric formulas remain unchanged. Initial code, stdout/
stderr and the frozen diagnostic plan survive. This is a reviewer diagnostic,
not an author science repair. No candidate has been inspected at this seal.

Parent STARTUP_PREMISE_AUDIT.json was read directly:346-row audit exit0,
399.0770249160123seconds,105792KiB maxRSS, empty stderr. I do not claim to
have repeated the full audit or verified remote freshness. No old production
suite, GPU/PDE solve, generic stability, phase/product development, empirical,
human/different-model/formal verification or protected/archive/disk operation
was performed. Review writes remain confined to this directory.
