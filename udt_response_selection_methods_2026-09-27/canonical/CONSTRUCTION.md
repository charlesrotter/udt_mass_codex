# Conditional canonical closure — initial construction

State: INITIAL CANDIDATE, not independently reviewed or adopted. Author context:
`/root/closure_construct`, Codex/GPT-6 runtime; exact underlying model identifier
not exposed. Date: 2026-09-27. Baseline independently observed:
`grok`, `df71211c11fde4b123d1e71e2028cc571719ea68`.
Parent startup/synchronization/full-premise evidence is attributed to the parent;
this worker inspected branch, HEAD, status, method files and scoped sources.
Existing untracked/protected payloads were not opened or modified.

## Question, frame and coverage

For ALL smooth positive spatial 3-metrics and symmetric weight-one momentum
densities on an open patch, and ALL smooth compactly supported scalar lapses and
vector shifts, which constant real coefficients give the specified strong
Lorentzian hypersurface-deformation bracket? This is a CHOSEN, template-led
conditional canonical test. All six metric and momentum components are retained.
The canonical cotangent phase space, Poisson form, local quadratic momentum
ansatz, two-spatial-derivative potential, and closure target are method
hypotheses, not consequences of metric-only UDT, DDR or Local Metric Sufficiency.
A, B, C, D are free-and-explored; chart, signature and bracket signs are declared
conventions. No numerical physical value is pinned. The native positional-dilation
interpretation is unchanged: no independent primitive speed is introduced;
`c_E` remains calibration. Coordinate lapse is not identified with physical dilation.

Compact support licenses integration by parts; it supplies no physical boundary.
No physical approximation, grid, GPU, fitted target, new field or production
solver is used. The controls are exact symbolic CPU calculations, each capped at
120 seconds. Worker ceiling: 40 minutes. Stop at this frozen conditional result
and requested same-premise review; no commit or scientific promotion by this worker.
The class is not claimed exhaustive among metric theories, local responses or
phase spaces. Extra-constraint dynamics and nonlinear well-posedness are omitted.

## Conventions and functional derivatives

Write `s=sqrt(det h)`, `p=h_ij pi^ij`, `Q=A pi^ij pi_ij+B p^2`.
Indices on pi are moved with h. The connection is Levi-Civita, and curvature has
`R_ij=partial_k Gamma^k_ij-partial_j Gamma^k_ik+Gamma^k_kl Gamma^l_ij-Gamma^k_jl Gamma^l_ik`.
For symmetric canonical variables,

```text
{F,G}=integral (delta F/delta h_ij delta G/delta pi^ij
              -delta F/delta pi^ij delta G/delta h_ij) d^3x,
{h_ij(x),pi^kl(y)}=delta_(i^k delta_j)^l delta^3(x-y).
H[N]=integral N [Q/s+s(C R+D)] d^3x,
D[v]=integral pi^ij Lie_v h_ij d^3x
    =-2 integral v_j nabla_i pi^ij d^3x.
```

The weight-one derivatives must be kept:
`nabla_i pi^ij=partial_i pi^ij+Gamma^j_ik pi^ik`, after density cancellation,
and `nabla_i p=partial_i p-Gamma^k_ki p=s partial_i(p/s)`.
Thus the trace-gradient obstruction below is a gradient of `p/s`, not `partial_i p`.
All repeated symmetric-index sums here run over the full 3 by 3 tensor; in
independent off-diagonal coordinates the derivative is twice the tensor entry.

The complete derivatives are

```text
delta H[N]/delta pi^ij = (2N/s)(A pi_ij+B p h_ij),

delta H[N]/delta h_ij = (N/s)[2A pi^i_k pi^jk+2B p pi^ij-(1/2)h^ij Q]
  +s C[N((1/2)R h^ij-R^ij)+nabla^i nabla^j N-h^ij Delta N]
  +(1/2)s D N h^ij,

delta D[v]/delta pi^ij = Lie_v h_ij,
delta D[v]/delta h_ij = -Lie_v pi^ij.
```

Here `Lie_v pi^ij=v^k partial_k pi^ij-pi^kj partial_k v^i
-pi^ik partial_k v^j+pi^ij partial_k v^k` includes the density term.
The curvature variation follows from
`delta R=-R^ij delta h_ij+nabla^i nabla^j delta h_ij-Delta(h^ij delta h_ij)`;
two integrations by parts move derivatives onto N. No discarded physical surface
term or finite-cell assumption is present.

The shift generator gives `{h,D[v]}=Lie_v h`, `{pi,D[v]}=Lie_v pi`, and hence

```text
{D[v],D[u]}=D[[v,u]],       [v,u]^i=v^j partial_j u^i-u^j partial_j v^i,
{D[v],H[N]}=H[Lie_v N].
```

For example `{H[N],D[v]}=integral N Lie_v(H-density)
=-integral (Lie_v N)(H-density)`; this fixes the mixed-bracket sign.

## Full lapse bracket, with integration by parts

All pieces without derivatives of the smearing cancel between the two orders.
The potential-potential bracket is zero and the kinetic-kinetic bracket is
ultralocal and zero after antisymmetrization. The surviving cross terms are

```text
{H[N],H[M]} = 2C integral {
 A pi^ij (M nabla_i nabla_j N-N nabla_i nabla_j M)
 -(A+2B)p (M Delta N-N Delta M)} d^3x.                  (1)
```

Set `w_j=N partial_j M-M partial_j N`, `w^i=h^ij w_j`, and
`T^ij=A pi^ij-(A+2B)p h^ij`. The gradient-product part of
`nabla_i w_j` is antisymmetric, so its contraction with symmetric T vanishes.
One more integration by parts gives the exact identity

```text
{H[N],H[M]} = 2C integral w_j[A nabla_i pi^ij-(A+2B)nabla^j p] d^3x
             = -AC D[w]-2C(A+2B) integral w^i nabla_i p d^3x.       (2)
```

D, the constant potential coefficient, drops out. Equation (2) is a full
phase-space identity; no Hamiltonian/momentum constraint, symmetry or equation
of motion was imposed in deriving it.

## Necessity, sufficiency and degeneracies

The DECLARED normalized Lorentzian target, for signature `(-+++)` with the above
Poisson and shift conventions, is `{H[N],H[M]}=D[w]` as an identity on phase
space. At a flat metric, two local momentum jets establish independent vectors:

* `pi=diag(x,-x,0)` gives `nabla_i pi^ij=(1,0,0)` and `nabla^j p=0`.
* `pi=diag(0,0,x)` gives `nabla_i pi^ij=0` and `nabla^j p=(1,0,0)`.

Coordinate permutations cover all three directions. More generally the exact
linear map from 18 symmetric momentum first jets to these six vector entries
has rank six; the check below reconstructs it. Smearings detect each coefficient:
locally choose `M=x N` for a smooth nonzero bump N, obtaining `w_x=N^2`.
Thus equality for every h, pi, N, M requires and is sufficient for

```text
AC = -1,       A+2B = 0,
equivalently A != 0, C=-1/A, B=-A/2, D arbitrary.           (3)
```

No coefficient was divided away before this necessity argument. A and C are
nonzero as a consequence of the normalized target. Changing bracket/curvature
conventions changes written signs together; it does not create a measured speed.
For a target `k D[w]` with a prescribed nonzero k the relations are instead
`AC=-k`, `B=-A/2`. A positive k can be brought to the displayed normalization by
a real constant rescaling of H; a negative k cannot be made positive this way.
That normalization is not a derivation of a physical calibration constant.

All degenerate branches are retained:

| Coefficients | Exact lapse bracket / limitation |
|---|---|
| C=0, arbitrary A,B,D | zero, an ultralocal algebra, not the normalized Lorentzian target |
| A=B=0, arbitrary C,D | zero, a momentum-independent potential, not that target |
| C!=0, A=0, B!=0 | `-4BC integral w^i nabla_i p`; obstructed without extra constraints |
| C!=0, A!=0, B=-A/2 | `-AC D[w]`; normalized target only when AC=-1 |
| C!=0, A+2B!=0 | trace-gradient obstruction; no closure on the original constraints |

These cases overlap consistently; the first two are exactly the cases in which
`{H,H}` vanishes STRONGLY for all fields. The kinetic Hessian is degenerate if
`A=0` (five traceless directions) or `A+3B=0` (trace direction). Neither is
compatible with (3). At (3), `Q=A pi_TF^ij pi_TF_ij-(A/6)p^2`:
the relative kinetic signature follows inside the selected ansatz, but the
overall sign of A, its magnitude and D are not selected or empirically fixed.
No positive-energy or stability theorem follows from this signature.

## Weak closure is different, and the obstruction survives H=D=0

For the ORIGINAL constraints H=0 and `nabla_i pi^ij=0`, first-class closure
(the lapse bracket vanishes on their entire constraint surface) occurs precisely
when `C(A+2B)=0`. Sufficiency follows from (2), including every ultralocal case.
This is algebraic closure, not a claim that every degenerate choice has a
nonempty regular constraint surface: for example A=B=C=0, D!=0 gives no H=0
positive-metric data. Its weak equalities are vacuous while its strong algebra
is still Abelian.
Here is a local constrained counterexample proving necessity when this product
is nonzero; it is a witness, not a symmetry reduction of the derivation.

Take `h=dx^2+f(x)^2 dy^2+dz^2`, `pi^zz=f(x) q(x)`, all other pi components zero.
Then `s=f`, `p=f q`, `nabla_i pi^ij=0`, `R=-2 f''/f` and

```text
H-density/f = (A+B)q^2 -2C f''/f+D.
```

Choose `q=x`. For ANY real A,B,D and nonzero C, solve the regular linear ODE
`f''=[((A+B)x^2+D)/(2C)] f`, with `f(0)=1`, `f'(0)=0`.
Smooth local existence and continuity give f>0 on a smaller open interval.
Both original constraints hold there exactly, but `nabla_x p=f`.
For nonzero smooth compactly supported N in this patch and `M=x N`, (2) is
`-2C(A+2B) integral f N^2 d^3x`, which is nonzero. This defeats weak closure
for every remaining coefficient set, including kinetic degeneracies, regardless
of D. The symbolic control recomputes its curvature and density derivatives.

Demanding only `{H,H} approximately D[w]` ON H=D=0 cannot determine the
normalization or signature: its right-hand side already vanishes, so all
first-class cases above pass that weak equality. It is not the strong target.
Imposing an ADDITIONAL constraint `partial_i(p/s)=0` removes the anomaly even
for other B, as does restricting to its stronger p=0 subcase. This is an extra
phase-space restriction, not implied by the original constraints as the witness
shows. Its preservation and brackets with H may constrain lapses or generate
further conditions; none was calculated here, so no full first-class extension
or refoliation theorem is claimed for this repair. Restricting lapse pairs also
weakens the target and is outside the stipulated all-smearings quantifier.

## Conditional action comparison and the DDR trace sector

This paragraph adds the CANONICAL ACTION as an explicit mathematical comparison,
not a native UDT premise. At (3), let
`I=integral dt (integral pi^ij dot h_ij-H[N]-D[v])`, with N>0 on a chosen local
time-orientation branch for this action comparison,
and `K_ij=(dot h_ij-Lie_v h_ij)/(2N)`. The momentum equation gives
`pi^ij=(s/A)(K^ij-K h^ij)`. The Legendre transform is

```text
L = (N s/A)[K_ij K^ij-K^2+R-A D].
```

For the additionally reconstructed spacetime metric
`g=-N^2 dt^2+h_ij(dx^i+v^i dt)(dx^j+v^j dt)`, Gauss-Codazzi identifies this
with `(1/A) sqrt(-g)(R^(4)-2 Lambda)`, up to local divergence terms, with
`Lambda=A D/2`. Compactly supported variations eliminate such terms; no global
boundary functional is selected. Unrestricted variation (including N and v)
then gives `G_ab+Lambda g_ab=0`, a fixed-Lambda sector for each fixed A,D.
The converse local Legendre map is regular at (3); this statement does not
assert global foliation, development existence, stability or physical adoption.

That field equation differs from DDR's trace-free condition. For example for
the comparison response `E_ab=(1/A)G_ab+(D/2)g_ab`, DDR imposes `TF(E)=0`,
so on a connected regular region `Ric=Lambda_eff g` with freely integrated
constant Lambda_eff. If `E=lambda g`, Bianchi makes lambda constant and
`Lambda_eff=A D/2-A lambda`. The unrestricted canonical action fixes lambda=0.
One represents a chosen DDR constant-trace sector by choosing the CONSTANT
canonical coefficient `D_eff=D-2 lambda=2 Lambda_eff/A`; the family of such
canonical theories covers those sectors. No variable D, new scalar field or
equivalence of full off-shell formulations is asserted.

In particular, full original G301 gates give a curvature-linear response with
`F(0)=0` and exact weight-one homogeneity, excluding a bare order-zero metric
term. The canonical D term belongs only to this expressly broader work-order
test class. For a G301 response proportional to G without a metric term, DDR
still retains all constant-curvature trace sectors; the canonical D=0 action
would retain only Lambda=0. Therefore neither the closure calculation nor the
action comparison closes UDT response-class membership or selects its scalar
datum, action normalization, or cosmological coefficient.

## Exposure, checks and evidence ceiling

Question/ansatz and source ownership were read before candidate construction.
No parent proof, coefficient result, check code, reviewer output or protected
payload was read before this freeze. The author knows standard canonical-GR
mathematics; this is not an outcome-blind mathematical discovery. Primary ADM
reference was inspected as method provenance during construction; it contains
the familiar specialization. The result above was calculated from free A,B,C,D,
not inferred from that specialization. Parent's later scope message requested
care with the DDR trace sector and G301's excluded order-zero term; no proof
or coefficient values were supplied.

`check_canonical.py` uses exact symbolic differentiation of the six independent
metric/momentum coordinates at a non-diagonal positive rational metric; direct
polynomial integration of the pre-integration-by-parts lapse bracket; an
18-column jet-rank calculation; and direct Christoffel/Ricci/density calculations
for the constrained witness. The polynomial cube control uses lapses whose
values/first derivatives vanish at its faces; it is an exact integration-by-parts
control, not an assertion that these polynomials are globally smooth compact
bumps. The universal result is the analytic argument above. Mutated sign,
trace coefficient, density derivative and off-diagonal normalization are each
tested against their independent controls. No floating-point tolerance is used.
Author-written controls are independent routes within this context, not a fresh
review or a proof of native premises. Actual commands, stdout/stderr, versions,
checks and source hashes accompany the initial manifest.
