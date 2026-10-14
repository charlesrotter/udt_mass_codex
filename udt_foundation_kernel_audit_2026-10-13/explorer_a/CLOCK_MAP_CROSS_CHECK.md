# FKA1 — later explorer cross-check of the clock-map and tape probes

Verdict: **CONFIRMED within the stated conditional representation and positive-
slope domains**, including the radar/tape separation. No substantive algebraic
defect found. Two scope details must remain explicit: use common compact query
windows for finite-family statements, and require finite strictly positive
derivatives for the general clock-map cocycle. Mere increasingness does not
alone guarantee the latter.

This is a later separate-context argument check by `/root/fka_explorer_a`,
not a fresh FKA reviewer. I previously constructed the explorer A candidates,
read their permitted historical comparison chain, and received Charles's
current postulate clarification. I did not originate these new controls. Their
author is the fidelity-review context, whose own author check is not independent
certification. I read the two specified target probes and their freezes, but
no sibling mathematics review or checking code. No numerical or symbolic worker
was launched. The calculations below start from the displayed metric, curves,
incidence equations and integral; existing pass counts play no role.

## Snapshot and exact reviewed sources

Independently checked branch `grok`, HEAD
`67246b3528c8fbc363b98c1d06794517e8109f65`. Parent integration currently has
tracked edits in CURRENT_RESEARCH_PROGRAM, HANDOFF, INDEX, LIVE, MEMORY,
UDT_DEVELOPMENT and UDT_RESEARCH_ROADMAP; these are not called a clean tree.
I opened none of their new contents for this check and changed none of them.
Unrelated/protected untracked work remains untouched. Earlier explorer editions
remain preserved. Parent startup and premise-audit attribution remain as recorded
in this campaign; no fresh top-level startup claim is made.

- `review/fidelity/CLOCK_MAP_REALIZATION.md`:
  `9cef9602e0f30512ed3fa4fbc7860f69c8366e3fdbfbaacd3152ed81cf90be2b`.
- `review/fidelity/RADAR_TAPE_PROBE.md`:
  `8db36c6191b2ef74d905da9ac7b9a6a4cebd766e149ed6a5b275e36f6f4721f8`.

Both target hashes match their supplied freezes. Hashes establish source
correspondence, not scientific truth or independence.

## 1. Original metric, clocks, causal direction and exchange

Write `s=Z+Z^-1`, `Z>1`, and

`P=u²-suv+v²`, `H=P²/ell⁴`, `C=Z exp(2εH)`,
`g=-C du dv+dx_perp²+dz_perp²`, `ell>0`, `ε∈R` finite.

The coordinates u,v and ell have length units, making H,C dimensionless. The
cross-term convention is `g_uv=-C/2`. Thus the radial inverse has
`g^uv=-2/C`, and with `t=(u+v)/2`,

`g^-1(dt,dt)=2(-2/C)(1/2)(1/2)=-1/C<0`.

The smooth positive C defines a Lorentz metric on the full positive u,v quadrant
(and its flat transverse product). No completeness or asymptotic uniform bound
is inferred. For each finite query, its segments are compact subsets of that
quadrant. A compact family of queries needs one patch containing all of its
segments and, when used, the returns and exchange images. This makes precise
the finite-patch wording in the first frozen probe; the parent has specified the
full-quadrant presentation for the combined supplement.

Choose future by `dt>0`. For radial curves increasing u with v fixed, or
increasing v with u fixed, this is future null. More generally a nonzero causal
tangent obeys `C u'v'≥|x_perp'|²+|z_perp'|²`; its future component has
nonnegative u',v', so t increases. A global real temporal function excludes
causal loops in this domain, not just on the displayed two-clock experiment.

The curves are `A(a)=(a,a/Z)` and `B(b)=(b/Z,b)`, transverse positions zero.
On each, P=0, hence `H=0`, `H_i=2PP_i/ell⁴=0`, `C=Z`, and `C_i=0`.
Their norms are independently

`g(A',A')=-C/Z=-1`, `g(B',B')=-C/Z=-1`.

Computing from the inverse metric leaves exactly

`Γ^u_uu=C_u/C`, `Γ^v_vv=C_v/C`

in the u,v block; all mixed entries and transverse Christoffels vanish. Both
symbols vanish along both clock curves. The coordinate tangents are constant,
so `∇_{A'}A'=∇_{B'}B'=0`. Parameters a,b are ordinary unit proper time in
the common length-time units, not coordinate clocks with hidden accelerations.

P and hence C are symmetric under u↔v. That swap preserves g, preserves t,
and sends A(a) to B(a). It is a genuine time-orientation-preserving exchange
isometry. It proves symmetry of this pair preparation, not an all-observer law.

## 2. Both future correspondences and independent affine-frequency check

From A(a), the outgoing u=a line reaches B when `b/Z=a`, giving `b=Za`.
Its v coordinate grows from `a/Z` to `Za`. From B(b), the outgoing v=b line
reaches A when `a/Z=b`, giving `a=Zb`, with increasing u. Both are strictly
future on the positive domain.

For the first line, the geodesic equation is

`v''+(C_v/C)(v')²=0`, hence `C v'=κ>0`.

On each compact segment, C is smooth, positive and finite, so integrating
`dλ/dv=C/κ` supplies a regular increasing affine parameter with finite span.
For the return, `C u'=κ>0` is the analogous affine equation. A transverse
geodesic has constant transverse affine slope; equal zero transverse endpoint
positions force that slope to vanish. The two radial null branches cannot switch
along a nonzero affinely parametrized geodesic. The other radial branch from
A(a) meets B in the past, so it is not a second future direct reception.

An additional direct contraction checks the clock ratio independently of
reading it back from the event equations. On the A-to-B ray,

`K=(0,κ/C)`, `U_A=(1,1/Z)`, `U_B=(1/Z,1)`,
`-g(K,U_A)=κ/2`, `-g(K,U_B)=κ/(2Z)`.

Their ratio is Z. On the B-to-A ray, `K=(κ/C,0)` exchanges the two contractions
and gives emitter/receiver ratio Z again. This is an exact check of the
conditional geometric representation; it adds no photon or independent physical
propagation ontology to Charles's postulate.

Both stipulated maps and their finite intervals are therefore exact for all
finite ε. The immediate composed return is `a↦Z²a`, not `a↦a`, and its apparent
delay is `(Z²-1)a`. Clock origins/alignment are the stated common choices.
These results do not promise unchanged spacelike separation, transported
relative velocity, tides, screens or experiments with other clocks.

## 3. Curvature checks real metric freedom

With the curvature convention `R(X,Y)=[∇_X,∇_Y]-∇_[X,Y]`, the Christoffels above
give `Ric_uu=Ric_vv=0` and

`Ric_uv=-∂_u∂_v log C`.

Contracting both symmetric off-diagonal entries therefore gives

`R=(4/C)∂_u∂_v log C=(8ε/C)H_uv`.

The flat transverse product adds no scalar curvature. At `Z=2`, `u=v=ell`,
direct polynomial differentiation gives

`P=-ell²/2`, `P_u=P_v=-ell/2`, `P_uv=-5/2`,
`H_uv=2(P_uP_v+P P_uv)/ell⁴=3/ell²`,
`R=12ε exp(-ε/2)/ell²`.

As an independent general check, at `u=v=ell` and arbitrary Z>1,

`H=(s-2)²`, `H_uv=4(s-2)(s-1)/ell²`,
`R=32ε(s-2)(s-1) exp[-2ε(s-2)²]/(Z ell²)`.

Since s>2, every nonzero finite ε has nonzero curvature there. ε=0 is flat.
Choose a query patch containing this point when using this local separator.
Thus at least a flat and a nonflat metric are non-isometric despite the
unchanged specified clock records. This does not establish that all nonzero
ε members are pairwise non-isometric, and the probe does not require that claim.

## 4. Actual-map cocycle and kernel scope

For increasing C1 clock maps with finite `f'(a)>0` and `g'(f(a))>0`, the chain
rule gives `Z_gf(a)=Z_g(f(a))Z_f(a)`. Consequently

`Φ_gf(a)=Φ_g(f(a))+Φ_f(a)`, `Φ_f=-log Z_f`,
`D_gf(a)=D_g(f(a))D_f(a)`, `D_f=diag(Z_f,Z_f^-1)`.

Taking `χ_f=(1-Z_f²)/(1+Z_f²)` proves

`χ_gf=[χ_g(f(a))+χ_f(a)]/[1+χ_g(f(a))χ_f(a)]`.

If x,y denote the two positive slopes, the denominator is explicitly
`2(1+x²y²)/[(1+x²)(1+y²)]>0`, so there is no concealed singularity on this
domain. The inverse map has inverse slope at the matched argument, while the
independently prescribed future map need not be that inverse.

The wording “differentiable increasing” alone is not sufficient for finite
logarithmic depth: for example `f(a)=2+(a-1)³` near a=1 is strictly increasing
but has zero derivative there. The source also invokes positive slopes; the
combined result should carry that hypothesis explicitly. This is a scope
precision, not a defect in the displayed proof on its positive-slope domain.

G176 conditionally turns the matched target tangent `Z U_target` into `T=Z`,
`Φ=-log Z`, `χ=(1-Z²)/(1+Z²)`. Both directions have χ=-3/5 for Z=2. Their
common scalar does not imply that the complete pair metric, ruler density or
every physical comparison is the same across ε. Normalization ambiguity at a
fixed completed input is not reopened.

## 5. Independent radar/tape calculation

The explicit timing convention gives

`D_rad=(Z²-1)a/2`, `t_rad=(Z²+1)a/2`.

These follow from the stipulated return record and remain fixed across ε.
Restoring time units multiplies the radius by c_E; they are not a new
independent physical light-speed or spacelike-ruler postulate.

Set

`S(a)=∫[a/Z,Za] C(a,v)dv>0`,
`∫[a/Z,V(a,λ)] C(a,v)dv=λS(a)`, `F(a,λ)=(a,V(a,λ))`.

The positive integrand and implicit differentiation give a unique smooth V,
`V_λ=S/C`, `K=(0,S/C)`, `J=(1,V_a)`. The equation `C K^v=S(a)` verifies
affine geodesicity from the original connection. Contraction, without using
G176, gives

`h00=-C V_a`, `h01=-S/2`, `h11=0`, `det h=-S²/4`.

At ε=0, `V=a[(1-λ)/Z+λZ]`, hence
`-h00=1+λ(Z²-1)≥1`. On each compact positive a-window, smooth dependence on
ε and compactness of `[a0,a1]×[0,1]` yield an ε_*>0 with `-h00>0` for all
`|ε|<ε_*`. Negative determinant is automatic, but it does not alone establish
the clock-leg inequality for arbitrary larger ε. The source correctly restricts
the whole-ribbon G176 conclusion to the established small-parameter window.

The endpoint equations `V(a,0)=a/Z` and `V(a,1)=Za` give `T_e=1`, `T_o=Z`
exactly for all ε; they are not approximate consequences of the continuity bound.
The completed density is `m=S(a)/2`, constant in λ. With `T²=C V_a`, the
retained shift is `β=m/T²`, and completion gives `β_completed=1/T²`.
Thus the one-family completed tape is

`L_completed=S(a)/2=(1/2)∫[a/Z,Za] C(a,v)dv`.

At ε=0 it equals D_rad. Inside the segment, P<0 and H>0. Therefore `C>Z`
for ε>0 and `C<Z` for ε<0 in the interior, with strict positive integration
length. The stated strict tape/radar inequalities follow without quadrature.

One extra exact integral independently checks the infinitesimal result. Put
`Δ=(Z-Z^-1)a`, `w=v-a/Z`; then `P=w(w-Δ)` and

`∂_ε L_completed|₀=Z/ell⁴ ∫[0,Δ] w²(w-Δ)²dw`
`                    = Z Δ⁵/(30 ell⁴)>0`.

For Z=2 this is `81 a⁵/(160 ell⁴)`, with the required length units. This
derivative is supplementary; the finite inequalities are exact sign statements.

The family restriction matters. Generally
`d(m(a)dλ)=m'(a)da∧dλ`; already at ε=0,
`m'=(Z²-1)/2>0`. Thus the completed ruler density is not a global exact
spacetime coordinate at unchanged clock tangent. A coordinate `s=m(a)λ` has
`ds=m dλ+λm' da`. The probe integrates only along fixed-a families and is
sound at that scope. The tape is neither null proper length (zero) nor
automatically radar distance or a prepared spacelike ruler.

## 6. Decision and limits

The two probes jointly establish a bounded positive representation and inverse-
reconstruction result: specified bilateral slowing maps, ordinary free clocks,
alignment, exchange symmetry and a timing convention coexist in flat and
curved metrics; on an explicitly regular null ribbon their G176 tapes differ
while the endpoint kernels and timing records agree. If equality of that tape
with that radar convention were separately imposed, it would exclude nonzero
small ε in this family. The probes do not impose or attribute that equality.

This is compatible with the current owner-first physical framing: the clock
records are supplied first, and the null construction is their conditional
geometric representation. It does not derive the records from all UDT premises,
justify a unique ruler interpretation, establish a native solution, introduce
an independent photon cause, or prove new physics necessary. Remaining UDT
commitments or additional records could distinguish the metrics. Repeated
numerical sampling would not strengthen the exact conclusion proved here.
