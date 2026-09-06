# Stage A — frozen source-first adversarial reconstruction

Date: 2026-09-06. Reviewer context: /root/curvature_phase_adversarial_review, a fresh separate context.
Runtime model: UNKNOWN (no reliable exact runtime model identifier exposed). Different-model
independence: UNTESTED. No candidate proof, code, output, or prior candidate review was read before
this freeze. The candidate WORK_ORDER.md supplied the exact recipe/question, not a result.

This is an independent mathematical reconstruction, not acceptance, adoption, or canon. The proof
below was developed from the admitted source definitions and the work order. The coordinate code
was independently authored and imports no repository or candidate module. Exact arithmetic checks
support the argument; they are not a replacement for it.

## Orientation, scope and sources

Read-only HEAD was verified as b304c89f567b9bc301239b631d7a84c91485767d on grok. Git status
showed unrelated untracked work and the candidate directory; only metadata was inspected and no
protected payload was opened. The pinned read-only dispatch overrides checkout/fetch/pull during
the parent's work. Remote freshness is not independently verified. No repository or Git writes
were made. Scratch is /tmp/udt-curvature-review-qassiP only.

Read AGENTS.md, current LIVE/HANDOFF blocks, CURRENT_RESEARCH_PROGRAM.md,
CURRENT_SCIENTIFIC_PREMISES.md, CLAUDE.md method/trigger/repo-discipline sections, INDEX.md,
MEMORY.md, CROSS_MODEL_VERIFY.md and the no-shortcuts, completeness-map and
verifier-before-record skills. The 335-row premise verifier is delegated to the parent by the
explicit dispatch and was NOT independently repeated here. No registry row or accepted grade is
changed. Current source audit reports supersede older pending headers.

Admitted science: G313's supplied constant-real-A local plane-wave family; G351's owner-provisional
source-free labelwise measure premise; G352's owner-provisional clock-rate readout and explicitly
chosen continuous phase-independent product realization. The exact quadratic Weyl recipe is a
CHOSEN mathematical construction, not an admitted physical law. Time orientation is supplied,
with partial_v future. Coordinate volume orientation is chosen for components. A and its signs
are free-and-explored inside this bounded supplied family. No physical value, source, support,
history, preferred observer, field equation, or scale is selected.

The claim covers every real constant A != 0 and separately A=0, local smooth regular patches,
exact geometry in four dimensions. No approximation, GPU, mesh, boundary problem, A(u), global
completion, perturbation census, or physical realization is included. At most one CPU check at a
time, 60-second child timeout, under 512 MiB target; hard parent deadline 20:08:22 UTC.

Pinned accepted-source SHA256 values:

| Source | SHA256 |
|---|---|
| G313/AUDIT_REPORT.md | b7df75cee891ed23dcf4796aba0a3d25e101ee89e4c1add95c8ef842987e418e |
| G313/EXACT_DERIVATION.md | 7bf8dd3b081ff0d37ee23c8ea462abc451f9f4a3510283ea5e9ef87dd042b6bf |
| G351/AUDIT_REPORT.md | 9fe05975201708714983e03ca592f75bd40ccb16ea4079b7e4a33c9dfe4b48c1 |
| G351/EXACT_DERIVATION.md | 37bd938dc488c305e43c3e1b414e1b40e489bf7fa23dd6453ce3118c953ea317 |
| G352/AUDIT_REPORT.md | 4f1925a1d11d00d55bea6bf3858cbedf2878e63c8e4e14e5a22211b4e03d9f8f |
| G352/EXACT_DERIVATION.md | 70aac9b85acb797cba41caa8dad9d567174b8031e853de8189a074e929e51b0d |
| candidate/WORK_ORDER.md | c89f7e5d9cedbc4460bb1060c5776a4aaa9105860fbee57dd9fd8011bde360ca |

Full source directories are exactly those named in the dispatch: G313 is
udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01; G351 is
udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05; G352 is
udt_g352_clock_rate_carried_measure_readout_2026-09-05. Scientific inputs are these accepted
sources, not the previous UNPROMOTED current representation.

## Independent full-tensor argument

Write l=du, e_1=dx, e_2=dy and Q_i=l wedge e_i. The inverse metric has
g^{uv}=g^{vu}=-1, g^{vv}=-A(x^2-y^2), g^{xx}=g^{yy}=1, g^{uu}=0, determinant -1.
All Gamma^u_ab vanish. The work-order curvature convention gives

    W = -A Q_1 tensor Q_1 + A Q_2 tensor Q_2.

Indeed R_uxux=-A and R_uyuy=A with only the curvature symmetries supplying other nonzero
components, and the Ricci trace is zero. The coordinate reconstruction independently evaluates
all 256 lower-index curvature and Weyl components from g and its derivatives.

For epsilon_uvxy=+1, the FIRST-pair Hodge dual obeys star Q_1=-Q_2 and star Q_2=Q_1, hence

    star W = A Q_2 tensor Q_1 + A Q_1 tensor Q_2.

The factor 1/2 is essential because the antisymmetric pair is summed in both orders. Reversing
volume orientation negates star W, which leaves its quadratic contribution unchanged. Reversing
the curvature convention negates both W and star W and also leaves B unchanged.

For all indices a,b and i,j in {1,2}, direct contraction gives

    g^{ef} (Q_i)_ae (Q_j)_bf = delta_ij l_a l_b.

The omitted terms vanish by g^{-1}(l,l)=0 and g^{-1}(l,e_i)=0. Applying this identity to BOTH
metric contractions in the exact recipe yields the sum of squared entries of diag(-A,A), namely
2A^2, from W and the same 2A^2 from its dual. Therefore the full tensor identity is

    B = 4 A^2 du tensor du tensor du tensor du.

This is an analytic identity for every constant real A, not an inference from B_uuuu alone.
The independent coordinate calculation agrees on all 256 components.

For A != 0 set q=(4A^2)^(1/4)=sqrt(2)*sqrt(abs(A))>0. If a real covector b has b^tensor4=B,
the components B_iiii=0 for i=v,x,y force b_i=0, while b_u^4=4A^2 forces b_u=+q or -q.
Raising du gives -partial_v. The supplied time orientation therefore chooses uniquely

    beta = -q du,       C=beta#=q partial_v.

This real nonzero future-raised root is null and unique FOR THIS RECIPE and time orientation.
It is parallel since q is constant and all Gamma^u_ab vanish. Thus d beta=0 and div C=0.
Locally, Theta=-q u+Theta_0 is a primitive, unique up to an additive constant on a connected
patch. This supplies a local geometric phase; it does not declare that phase physically occupied.

At A=0, the full tensor B=0; a real fourth root must be the zero covector. Therefore this recipe
has no nonzero phase gradient there. This does not prohibit supplied null phases in flat geometry
or rule out other constructions.

## Quotient measure and G352 comparison, derived directly

Let vol=du wedge dv wedge dx wedge dy. Then

    j = i_C vol = -q du wedge dx wedge dy = dTheta wedge dx wedge dy.

The form is horizontal for C, and Cartan's identity gives L_C j=0 because d j=0 and i_C j=0.
Thus in a local flow box it descends to the three-dimensional space of C-orbits, coordinatized by
(u,x,y). Its absolute density defines the nonnegative locally finite Borel measure

    dXi_geo = q |du| |dx dy| = |dTheta| tensor dA_screen.

A finite amount requires a retained measurable region of finite measure; geometry has not chosen
one. On any constant-u screen cut v=f(x,y), tangent vectors are partial_x+f_x partial_v and
partial_y+f_y partial_v. Their full metric Gram matrix is identically the 2x2 identity for
arbitrary f_x,f_y, so ordinary sheet area is |dx dy|, including nonconstant cuts. This is not a
claim that arbitrary cross-phase spacelike surfaces have that area.

On a chosen product patch and the displayed transverse identification, choose any common
dimensionless spacing Delta>0 and set

    dmu_geo = Delta dA_screen.

Then EXACTLY

    dXi_geo = (|dTheta|/Delta) tensor dmu_geo.

That realizes G352's mathematical product form locally. The product region, finite transverse
support, spacing, and cross-phase label identification remain query choices. The area density is
phase-independent in this trivialization. Flow conservation occurs along C, which stays inside
each phase sheet: C(Theta)=0. It cannot by itself identify labels across different phases.

There is also explicit geometric evidence against calling the displayed identification canonical.
For any b with b''=A b, the local transformation

    u'=u, x'=x+b(u), y'=y,
    v'=v+b'(u)x+(1/2)b'(u)b(u)

preserves the metric, beta, C and orientation. Taking b(u_0)=0 and b'(u_0) nonzero fixes quotient
labels on phase u_0 while shifting their coordinates at other phases. The supplied geometry thus
does not single out the identity-in-(x,y) cross-phase correspondence. This standard differential-
geometric calculation adds no physical equation: b is only an isometry parameter satisfying the
displayed directly checkable metric-preservation condition.

For any supplied future unit timelike U, omega=-beta(U)>0. Since C=beta#, its scalar local flux
readout is -g(C,U)=omega. To obtain this directly from j, choose an orthonormal observer screen
E_1,E_2 perpendicular to U and the null direction; write C=omega(U+n), with n unit spatial and
orthogonal to E_i. Then |j(U,E_1,E_2)|=omega. This is amount per observer proper time per metric
screen area in the local swept-screen construction.

Here n_geo=dmu_geo/dA_screen=Delta, so G352's comparison formula yields

    Gamma_geo=(omega/Delta)n_geo=omega=-g(C,U).

No prior candidate current-representation identity was used. For the selected congruence, ordinary
constant-phase screen-cut area is preserved along its generators; the physically populated
G351 measure and G352 meaning are still not adopted from this calculation. One cannot claim that
this single geometry realizes the full abstract independent (R,A_area) domain used to prove
G350/G352 weight uniqueness.

## Four different scaling operations

1. Passive positive null-coordinate change u'=a u, v'=v/a, a>0: A'=A/a^2 and q'=q/a.
   beta=-q' du', C=q' partial_v', B_u'u'u'u'=4A^2/a^4. The geometric tensors, measure and
   scalar observer readout are unchanged; only their components change. Volume has unit Jacobian.

2. G352 affine phase/spacing gauge at FIXED g,C,j,mu: Theta'=b Theta+c, Delta'=b Delta,
   b>0. Then k'=dTheta'=b beta and omega'=b omega, while omega'/Delta'=omega/Delta.
   The fixed current is C=(1/b)(k')#, not (k')#. The new k' is not the fixed recipe's root
   unless b=1. The fixed quotient form is (1/b)dTheta' wedge dA_screen; mu remains fixed.
   Imposing C=(k')# as well would change the current and would not be this gauge operation.

3. Constant metric homothety g_s=s^2 g, s>0 on the same coordinate manifold: the connection is
   unchanged, W_lower and starW_lower scale by s^2, and the two inverse metrics supply s^-4.
   Thus B_s=B and beta_s=beta. C_s=s^-2 C, vol_s=s^4 vol, j_s=s^2 j and Xi_geo,s=s^2 Xi_geo.
   Screen area and mu_geo (fixed Delta) scale by s^2. Unit observer U_s=s^-1 U gives
   omega_s=Gamma_s=s^-1 omega. This is not a passive coordinate transformation or phase gauge.

4. Multiplying the WHOLE chosen recipe by r>0 at fixed metric gives B_r=rB,
   beta_r=r^(1/4)beta, C_r=r^(1/4)C, j_r=r^(1/4)j and Theta_r=r^(1/4)Theta+constant.
   For fixed spacing, mu_geo remains Delta dA, while the phase factor and Gamma scale by r^(1/4).
   If spacing is also scaled by r^(1/4), equality to this changed j requires mu_geo to scale too;
   this is not fixed-current gauge invariance. r=0 loses the nonzero root; r<0 admits no real
   fourth root for A!=0. Recipe normalization is a mathematical choice, not uniquely selected
   physical content.

With coordinates carrying length and g components dimensionless, A has units L^-2, q has L^-1,
Theta and Delta are dimensionless, Xi_geo and mu_geo have units L^2, and Gamma_geo has units
L^-1. The homothety calculation gives the coordinate-independent version of this distinction.
Thus the construction supplies a geometric amount with area scaling, not a dimensionless physical
count. A dimensionless populated count would require an additional amount-per-count/area
identification or normalization. No absolute scale is introduced or selected here.

## Actual checks and limitations

Executed exactly:

    timeout 60s /usr/bin/time -v python3 -B /tmp/udt-curvature-review-qassiP/stage_a_tensor.py > /tmp/udt-curvature-review-qassiP/stage_a_tensor.stdout 2> /tmp/udt-curvature-review-qassiP/stage_a_tensor.stderr

Actual child exit 0; Python 3.10.12, SymPy 1.13.1. Recorded start
2026-09-06T18:48:54.743567+00:00, finish 18:49:00.603139+00:00; /usr/bin/time wall 6.01 seconds,
max RSS 48,396 KiB. Separate stdout/stderr retained. No failed run or omitted failure is present.

Exact computations cover the complete coordinate curvature/Weyl/dual/B tensors, Ricci flatness,
both quadratic contributions (2A^2 each), all-component A=0 control, null root/current, parallel
du, zero exterior derivative and divergence, arbitrary nonconstant fixed-phase screen cuts,
contraction 3-form, positive null coordinate covariance and proof-orientation reversal.
The deliberately wrong dual with omitted half-factor gives 10A^2 instead of 4A^2.
The nonclosed/nonconserved control beta_bad=-q(1+v)du gives (d beta_bad)_uv=q and div C_bad=q,
so the differential routines demonstrably detect nonzero quantities.

The analytic bivector contraction supplies the full metric-inverse argument; the present executable
has not yet run a deliberate Euclidean-inverse mutant. Homothety, general observer flux, coefficient
scaling, root uniqueness and cross-phase noncanonicity are analytic checks here, not advertised as
separate executable tests. The code takes q>0 for differential/root identities; q^4=4A^2 and real
root uniqueness are proved above for both A signs. No finite examples stand in for the universal
constant-A proof. No full source-package replay, repository purity suite, premise verifier,
different-model audit, human specialist audit, external timestamp authentication or remote check
was performed. Backup completeness and pre-reboot unsaved-state disposition remain UNVERIFIED;
ScratchDisk was unused.

## Stage A finding and return

The exact recipe succeeds locally for every nonzero real constant A with the tensor, unique
future-raised root, closed phase, divergence-free current, quotient geometric measure and bounded
G352 mathematical comparison stated above. It fails to provide a nonzero root at A=0. The
normalization/support/cross-phase/physical-count boundaries are essential, not optional wording.
This is not a verdict on unseen candidate bytes. Stage A is now frozen; await Stage B disclosure
before reading the candidate proof/code/results and issuing a direct adversarial verdict.
