# GL2 — conditional regular normalized Einstein limit

Initial candidate, 2026-09-10. CONDITIONAL, UNPROMOTED, not yet reviewed.
Question recorded in CAMPAIGN_LOG before this candidate. The argument was
explored analytically before freeze; no numerical search or observed dataset
selected it. GL1 is a reviewed UNPROMOTED dependency with ALL its caveats.
Current filter-only authority, not superseded strong W3, controls this result.

## Statement and exact hypotheses

Let U be a connected smooth four-dimensional domain with a supplied common
marking. On U let g_epsilon be smooth Lorentz metrics, 0<epsilon<=epsilon0,
and set h_epsilon=epsilon^2 g_epsilon. The parameter and marking describe a
comparison family; no physical value, cosmic normalization or operator length
is selected. F and reporting units are held fixed throughout the family.
This is a family of geometries, not a change of units hiding an F retuning.

Use exactly GL1's fixed finite-order m, ambient finite-curvature-jet extension,
full unoriented Lorentz equivariance, Frechet differentiability at zero, and
trace-free response T=PF. Its curvature-linear term is a S, where
S=Ric-(R/4)g. Assume a!=0 for this implication; UDT has not selected a or
excluded a=0. The actual geometric jets, not arbitrary formal slots, are
evaluated by the same F at every event. No external position dependence or
preferred vector is added. Coefficients of different dimensions, if present,
remain conditional parts of the fixed response, not UDT-supplied scales.

Assume h_epsilon -> h0 in C^r_loc on U, r=max(m+2,3), with h0 nondegenerate
Lorentzian. These are sufficient convergence/regularity hypotheses, not a
necessary-condition classification. In particular no assertion is made that
UDT, DDR, small curvature or local metric sufficiency provides this family,
its convergence, its derivative bounds or its nondegenerate limit. Supplied
pullbacks by identifications may be included before defining g_epsilon; their
regular convergence is part of the hypothesis, not an available gauge theorem.

Finally assume exact all-pair DDR for this specified symmetric response:

    T(J(g_epsilon)) = 0.

Alternatively allow its component norm on every compact patch to be at most
rho_K(epsilon) epsilon^2, with rho_K->0 in the controlled frames below.
This alternative is a mathematical approximate balance, not an admitted
replacement for exact DDR. No development equation or source is selected.

Conclusion: the limiting metric is Einstein,

    Ric(h0) = Lambda h0,

with one constant Lambda on connected U, not selected in value or sign.
This is a NECESSITY result for an assumed regular convergent balanced family,
not existence, a converse, convergence of arbitrary developments, stability,
physical GR recovery or an empirical prediction.

## Proof: actual metric jets and normalized shape

Fix a relatively compact sufficiently small coordinate patch. Nondegeneracy
and C^r convergence allow an h0-orthonormal frame to be continued to
h_epsilon-orthonormal frames u_epsilon with uniformly controlled coefficients
and derivatives through r. One construction keeps a locally timelike vector,
normalizes it, projects a spatial basis, and uses positive-definite Gram--Schmidt
on its orthogonal complement. Shrinking the patch preserves all denominators.
Finitely many such patches cover each compact set. These are reporting frames,
not additional physical observers. The norms are positive component norms;
no uniformity over unbounded Lorentz boosts is claimed.

For constant rescaling g_epsilon=epsilon^-2 h_epsilon, the connections agree.
The all-lowered curvature and its j-th covariant derivatives obey, as coordinate
tensors,

    nabla^j Rm(g_epsilon) = epsilon^-2 nabla^j Rm(h_epsilon).

The g_epsilon-orthonormal frame is e_epsilon=epsilon u_epsilon. There are
4+j covariant slots, so in these frames

    J_j(g_epsilon) = epsilon^(j+2) J_j(h_epsilon), 0<=j<=m.

C^r_loc convergence and uniform invertibility bound the h_epsilon jets on each
compact patch. Thus there are fixed M_j,K with
||J_j(g_epsilon)||<=M_j,K epsilon^(j+2); the actual jets enter F's near-zero
domain for sufficiently small epsilon. The formal ambient extension remains
a response-class assumption, while these inputs themselves are realizable.

Coordinate Ricci tensors agree under constant rescaling; scalar curvatures
scale by epsilon^2 and S(g_epsilon)=S(h_epsilon) as coordinate tensors. In
the corresponding orthonormal frames,

    S(g_epsilon)[e,e] = epsilon^2 S(h_epsilon)[u,u].

Apply GL1 with its fixed a, modulus omega, M_K and D_K. Exact balance gives

    ||S(h_epsilon)|| <=
      [D_K epsilon^2 + M_K omega(M_K epsilon^2)] / |a| -> 0.

Approximate balance adds rho_K(epsilon)/|a|. The estimate is locally uniform.
If GL1's OPTIONAL C1,1 response hypothesis holds, the exact-balance estimate
is O(epsilon^2), with constants depending on the fixed response and compact
patch. No power rate is inferred from bare differentiability, and no rate
for h_epsilon-h0 itself is obtained by this argument.

C^2 metric convergence implies curvature continuity, so S(h0)=0. The limit
is at least C^3, hence the contracted Bianchi identity applies classically:

    div Ric(h0) = (1/2)dR(h0),
    Ric(h0) = (R(h0)/4) h0  =>  (1/4)dR(h0)=(1/2)dR(h0).

Thus dR(h0)=0, and connectedness gives Lambda=R(h0)/4 constant. We apply
Bianchi to the exact limiting identity, not to a small C0 residual. No bound
on the derivative of that residual has been silently assumed.

## What this constrains, and what remains free

Absolute flattening alone is weak: for any fixed smooth h with bounded jets,
g_epsilon=epsilon^-2 h has component curvature tending to zero. GL2 constrains
the retained normalized shape h0 for balanced families with a!=0. Its content
is not the observation that every such g_epsilon becomes weakly curved.

The hypotheses are not empty: flat g_epsilon=epsilon^-2 eta has all jets zero,
and T(0)=0 for every GL1 response. This does not establish a NONFLAT balanced
family for an arbitrary response, let alone construct a lawful evolution.
Einstein limits need not be Ricci-flat or maximally symmetric. Lambda, Weyl
curvature and admissible geometric initial/query data are not uniquely fixed.
The theorem gives no source law, content identification, dimensional scale,
geodesic/instrument prescription or physical coupling.

## Two hypothesis diagnostics, not additional new laws

1. Nonzero linear coefficient matters. Reuse the reviewed UNPROMOTED ND1
   scalar-flat control, without promoting it or claiming new nonselection:

       h=-f dt^2+f^-1 dr^2+r^2 dOmega^2,
       f=1+d/r^2, d!=0, on a connected positive-radius f>0 domain.

   Its mixed Ricci eigenvalues are (-d/r^4,-d/r^4,d/r^4,d/r^4).
   The OPTIONAL Q=TF(Ric_ac Ric_b^c) response has Q=0 but S!=0; a=0.
   For g_epsilon=epsilon^-2 h, Q remains exactly zero and h_epsilon=h is
   a regular non-Einstein normalized limit. This is not a counterexample to
   GL2 or to UDT, because it lacks a!=0 and Q has not been adopted physically.
   It prevents silently treating that gate as dispensable.

2. Small curvature does not itself provide slow variation. On a fixed regular
   angular patch and 1/2<=r<=3/2 let, for integer n>=2,

       f_n=1+n^-6 cos(n(r-1)),
       k_n=-f_n dt^2+f_n^-1 dr^2+r^2 dOmega^2.

   f_n>=63/64, so these are actual smooth Lorentz metrics; k_n tends to the
   flat spherical metric in C^4. Full spherical curvature components are
   controlled by f_n''/2, f_n'/(2r), (1-f_n)/r^2: curvature is O(n^-4).
   Scalar curvature is R=-f''-4f'/r+2(1-f)/r^2. At r=1,

       R=n^-4-2n^-6,
       R'=4n^-4+4n^-6,
       R''=-n^-2-6n^-4-12n^-6,
       (nabla^2 R)(e_r,e_r)=(1+n^-6) R'', e_r=sqrt(f_n) partial_r.

   The last magnitude divided by R grows as n^2, although both go to zero.
   Since nabla^2 R is a contraction of nabla^2 Rm, this is incompatible with
   GL1's j=2 hierarchy for epsilon=n^-2: J0=O(epsilon^2), but this Hessian
   component is order epsilon, not O(epsilon^4). All jets through order2
   still tend to zero. This diagnostic does NOT assert DDR balance for k_n,
   does not refute GL2 (whose h_epsilon normalization is nondegenerate),
   and does not imply departure from GR or physical instability. It isolates
   a logical gap in inferring a derivative hierarchy just from smallness.

The two diagnostics are scope controls for this step, not a third substantive
campaign step, an alternative UDT law, or new compatibility/example campaigns.

## Verification plan and maximum claim

Author small symbolic check: recompute complete spherical Ricci from the metric,
including angular derivatives, constant-rescaling identities, diagnostic jets
and ND1 control; preserve code, exact output, versions and narrow negative
controls. Such finite/symbolic checks do not prove the general limit theorem.
Fresh reviewer reconstructs the transfer source-first, then attacks proof,
regularity, quantifiers, fixed-map assumption and checks independently.
No actual dynamical solution, PDE theorem, observation or empirical GR tolerance
is computed. New result remains conditional and UNPROMOTED even if verified.
