# Causal specialist peer critique of the kernel initial note

2026-09-28. Author/reviewer context `/root/cgw_causal`. This is the assigned
specialist cross-check, not the parent's later fresh adversarial review.
Runtime model identity and different-model independence are not attested.
I read the candidate and its checker before the new checks below; no blind-
method claim. My own source-led causal note was sealed before kernel exposure.

Target independently hashed at intake and after checks:
`kernel/INITIAL_NOTE.md`, SHA256
`3a50ac98902b6323f24c7bd68e406d3a93945c58a8713f1cfef8625bf53bc9b0`.
My original note remains
`04ab83d23ee6f695dc1a6cd80c773163129a45703e0cf29b47a0d78160fcb75b`.
Neither seal was edited. Parent reports the sole full406-row audit passed in
408.48s; I did not duplicate it or treat it as proof of these arguments.

**Peer verdict:** the local normal form, full shifted pair typing, conformal
clock/screen weights and all-direction first-order sign restriction survive
this critique at their declared conditional scopes. No load-bearing defect
requiring a repair to the sealed initial argument was found. One epoch/sign
qualification should be kept explicit in the synthesis; it is already fixed
correctly by the initial note's actual emission/arrival events.

## Findings, survivors and smallest precision steps

| Attack | Finding and strongest survivor | Smallest precision step |
|---|---|---|
| Is K1 only a convenient ansatz? | Starting from xi=fU and L_xi g=2psi g, g(xi,xi)=-f² forces xi(log f)=psi. Therefore f^-2g has unit timelike Killing xi. A local flowbox then yields exactly the stationary A,h form. Conversely that form yields the aligned conformal Killing field. It is a local representation of the G402 class, not a selected metric. | None. Preserve the fixed U, all-local-directions and local-domain quantifiers. |
| Does K1 silently require zero twist? | No. The spatial h is the positive rest/quotient form even if dt slices are not the rest spaces. A need not be closed. Direct non-diagonal metric-jet checks below have nonzero twist, zero shear and alpha=dlnf. | None. Keep A and h supplied; do not suppress A during synthesis. |
| Does a global potential imply a global time chart? | No, and the initial note explicitly says otherwise. Exact alpha gives a global scalar f, but a real flow coordinate t also needs suitable global orbit/section structure. Local flowbox reasoning is sufficient for K1. | No repair. Do not shorten “local normal form” to “global metric classification.” |
| Is G176's m=f²ell or shift beta_s wrong? | They follow from the full pulled-back metric, det(h_sigma)=-f^4ell² and m=sqrt(-det). At the calibrated coframe level T=f, L_s=1/f, beta_s=beta/(f²ell). The actual beta remains in the pullback; it cancels only in the determinant. Source G176 matches. | None. Its WORKING grade and supplied worldsheet must remain visible. |
| Is time-dependent ds=m d sigma an illicit coordinate change? | It would be, but the note expressly retains the coframe/slice interpretation and warns about the temporal cross term. My actual-coordinate calculation below confirms why carrying the original comparison clock is essential. | No repair. If a later explicit coordinate is used, carry K as well as the metric; do not reselect fixed-new-coordinate observers. |
| Are conformal Jacobi weights missing a source factor? | For the angular-to-physical-screen map, angles at A are conformally unchanged and physical length at B gains f(B), so D_g=f(B)D_bar is right. A source factor belongs to a differently normalized affine phase block, not this stated map. Consequently the area ratio is R². | Keep the words “source-angle map” and corresponding physical endpoint frames. Do not apply this formula unchanged to an arbitrary B phase block. |
| Can identical clocks still have different beams? | Yes. The ultrastatic flat versus R×S² control has U parallel and constant frequency while the meridional screen tide includes the sphere curvature. The supplied radii L and sin(L) solve the original Jacobi equations on a regular preconjugate branch. Neither metric is being declared a native Einstein history. | Respect the regular chart/branch and supplied curvature-scale limits. |
| Is K2's sign statement stronger than its average? | No. B=H+a.n+sigma(n,n) is continuous on the compact unit sphere and has mean H. Nonnegative B with B>0 somewhere gives a positive-measure positive neighborhood, hence H>0. H=0 with B>=0 forces B identically0; its odd dipole and even trace-free quadrupole then force a=sigma=0. | None. This concerns one supplied U and the leading local coefficient, not arbitrary observer changes or finite rays. |
| Does the quadratic control show redshift at a common receiving epoch0? | No. It correctly fixes EMISSION at0, so reception is at L and R=exp(kappa L²). For a common RECEPTION epoch0, emission is -L and R=exp(-kappa L²), a blueshift. This does not refute the stated example because its endpoints are explicit. | In the synthesis add or retain “emission at the zero-expansion epoch.” Avoid the shorter phrase “redshift observed at the zero-expansion epoch.” |
| Are composition, reversal and drift conflated? | The correctly carried clock-map derivative composes at t+L1. Reusing emission epoch t drops 2kappaL1L2. A later future-return ray is explicitly distinguished from reversal of the same segment. B's endpoint-along-ray derivative is also explicitly distinguished from temporal redshift drift. | None. Keep the event labels. |
| Is arbitrary f being admitted inside G374/G375? | No. The last section explicitly reinstates the fixed Einstein base, Hessian equation, fixed-target and positivity restrictions, and the G312 admission gap. The broad K1 examples are controls outside that narrower class when appropriate. | None. Both metrics' Einstein antecedents remain conditional; the normal form supplies no membership route. |

## Independent hand checks

The conformal Killing proof needs no field equation. In a local flowbox of
nonvanishing timelike xi, the rescaled metric gbar=f^-2g satisfies both
L_xi gbar=0 and gbar(xi,xi)=-1. Writing its components as
gbar=-(dt+A)^2+h identifies h as the positive metric on the quotient by xi.
This proves the normal form without assuming hypersurface orthogonality or
that the flow parameter is global.

The first-order sign argument uses angular polynomial uniqueness, not a
finite sky sample. The odd part is a.n. Once it vanishes, a trace-free
quadratic form constant on the sphere must vanish: diagonalize it, compare
the eigenvector directions, then use zero trace. K2's isotropy and H=0
corollaries follow. The note's six-axis symbolic average check is a valid
degree-two moment anchor, not an independent full-sky empirical measurement.

For the G415 background, the actual source metric has N proportional to
t^-1/4 and b_y=b_z=sqrt(t) at epsilon0. Proper-time logarithmic derivatives
therefore give H_xi=-1/(4Nt), H_y=H_z=1/(2Nt), and nonzero shear. Its axial
endpoint formula cannot establish an all-direction potential for this U.
The existing G415 source retains that longitudinal limitation.

## Actual additional checks

Read the candidate, CHECK_CONTRACT, SOURCE_PINS, CHECK_RESULT and its complete
check_kernel.py. Read the load-bearing G176 normalization derivation, G402
candidate/repair, G348 screen derivation, G374 candidate/review/banking and
G312 current authority; these overlap my initial source intake. Independently
read G415's metric and longitudinal clock sections for the axial claim.
I did not rerun the kernel script because it writes beside itself and refuses
to overwrite its sealed evidence. Its saved result and empty stderr were read.

The new check contract is PEER_KERNEL_CHECK_FREEZE.md. A separate short metric-
jet contraction implementation in peer_kernel_check.py imports no kernel code.
Its supplied non-diagonal test metric is

    f=1+t+xy, A=z dx+x dy,
    h=(1+x²)dx²+(1+y²)dy²+(1+z²)dz²,
    g=f²[-(dt+A)²+h], U=f^-1 partial_t.

At two exact rational events with f>0, original metric derivatives gave
sigma=0 and alpha=dlnf exactly; U was unit and H=f_t/f². The twist norms
were respectively 1 and 6481377/11669480, so the check did not silently set
twist to zero. This supports a genuinely shifted and spatially varying K1
example beyond the kernel author's purely conformal-flat original-metric test.

For a time-dependent G176 tape, take f=exp(t), m=f² and S=m sigma. Then
dS=m d sigma+2S dt. The true new metric has

    g_tt=-f²+4S²/f², g_tS=-2S/f², g_SS=f^-2.

The carried original comparison clock is K=partial_t+2S partial_S, and
g(K,K)=-f² exactly. Holding the new coordinate S fixed would choose a
different clock; the coframe nonclosure coefficient is 2exp(2t). This validates
the note's distinction rather than exposing a hidden substitution.

Finally, the exact quadratic comparison log R=kappa[t_o²-(t_o-L)²] gave
+kappa L² for emission0 and -kappa L² for reception0. This is the retained
event-label qualification above.

All14 named exact checks passed. Captured peer_kernel_01 stdout/stderr/JSON
report exit0, 0.227s, 45,340KiB maximum RSS, Python3.10.12/SymPy1.13.1,
under a one-thread/512MiB/60s cap; stderr is empty. This implementation is
distinct for the new pointwise contractions but was written AFTER candidate
and checker exposure; it is not fresh blind review. Original author algebra
checks were inspected, not misrepresented as independently replayed.

## Omissions and resulting ceiling

No global flowbox theorem, global positive-domain completion, full G375
classification proof, G415 nonzero-amplitude development, physical query
acquisition, empirical local precision or new UDT response-class membership
was independently established here. No instrument/source/light/flux law was
added. Finite symbolic checks support the hand arguments and explicit
witnesses; they do not prove their entire mathematical source packages.

The strongest survivor is a conditional normal form plus the invariant local
directional sign restriction, with correctly typed full pair and screen
readouts. This advances identification of admissible specifications, but does
not select the physical conformal factor, stationary optical geometry,
observer family, or asymptotic completion. The required fresh campaign review
and any synthesis repairs remain the parent's separate stage.
