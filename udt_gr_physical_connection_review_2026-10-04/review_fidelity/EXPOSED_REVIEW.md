# GRL1 exposed fidelity and physical-connection review

Verdict: **VERIFIED-WITH-CAVEATS**, scoped to INITIAL_SYNTHESIS.md SHA-256
`c22dba85f79bb91334cad3f89ead99e0d1974f0aeebbe123f80c96efd5d56260`,
its two analytic tests and its bounded literature/physical-return interpretation.
No blocking scientific defect found. This is not final-integration review,
source regrading, physical adoption or a full reproof of the cited literature.

Actual reviewer context `/root/grl_fidelity`; inherited runtime, exact model
revision unexposed. The source-first stage was sealed before reading the current
candidate/researcher arguments. The parent confirmed its candidate freeze before
any source-first findings were transmitted. I subsequently read the candidate,
TEST_PLAN, all three researcher REPORT.md and SOURCES.json files. No sibling
review was read. Historical verdict exposure remains recorded in EXPOSURE.json.
No scientific program, fit or numerical production was run; checks below are
analytic. Bookkeeping/read/download commands are not scientific computations.

## T1: the conclusion and its physical ceiling survive

I checked the null-cone algebra: in a g0-orthonormal basis, comparing null
directions (1,n) and (1,-n) kills the mixed coefficients; the constant quadratic
form on the unit spatial sphere forces g_ij=-g_00 delta_ij. Signature fixes a
positive smooth conformal factor. The stated connection difference then follows
by substituting exp(2f)g0 into metric compatibility, or directly into the
Christoffel formula.

For every timelike v, projective path agreement gives grad0 f parallel to v.
Two nonparallel timelike directions suffice pointwise to kill that gradient;
the candidate's stronger all-direction antecedent supplies them. Connectedness
makes f constant. Matched endpoint proper intervals acquire the same factor,
so their ratio stays fixed. A shared calibration is needed only to identify
the absolute metric factor, not the clock-ratio consequence.

The proposed conformal control was independently recomputed. The normalized
coordinate-rest velocity exp(-H eta)partial_eta has zero g-acceleration because
its derivative cancels Gamma^eta_eta eta=H. Null incidence gives eta_o=eta_e+L
and the actual ratio exp(HL). For v=partial_eta+b partial_x, connection
difference components are H(1+b²),2Hb; parallelism would require b²=1 when
b is nonzero, excluding the stated timelike range. Thus the control really
defeats replacing all free-fall directions by one congruence.

The physical non-closure is correctly narrowed. W4 ties its own readouts to
one metric; it does not require equality to every readout of a chosen GR
reference. The owner's approximate/tested-regime recovery is not global exact
agreement. T1 neither refutes the intended extra effect nor proves a new
postulate necessary. It is an operational comparison guard, overlapping old
inverse/matching work while sharpening the exact data sufficient for this lemma.

## T2: independent derivation of the local coefficient and average

The key distinction is following one source history while varying reception
time, then taking a family of sources to coincidence. Re-preparing at each tick
would compute another derivative. A merely pointwise O(r²) remainder would not
suffice, but the fixed smooth geodesic congruence and regular short branch permit
the differentiable local expansion used here.

An independent way to verify the coefficient uses the congruence Riccati
identity. In the parallel observer frame, let X be a neighboring Jacobi
separation and V=B X to first order. Geodesic variation gives

    D_U² X = -T X,                 dot B + B² = -T.

For X=rn, set s=n.Bn. Then dot r=r s and dot n=P_n Bn. Differentiating the
leading actual shift r s gives

    (1/r) d(r s)/dt
      = s² + (P_n Bn).Bn + n.B(P_n Bn) + n.dot B n
      = |Bn|²-s²+n.(dot B+B²)n
      = |P_n Bn|²-T(n,n).

This retains the antisymmetric part W; assuming B symmetric would unnecessarily
exclude vorticity. It verifies the candidate without importing the disputed
published quadrupole, an Einstein equation or an energy condition.

For the remainder issue, label neighboring geodesics by epsilon times smooth
initial spatial data. On a sufficiently small fixed observer-time interval,
their positions have X(t,epsilon)=epsilon J(t)+O_C1(epsilon²), with J bounded
away from zero after choosing a nonzero initial direction. Their velocities
are O(epsilon). Fermi metric corrections are O(|X|²), and the scaled null
incidence problem has the ordinary transverse flat limit. Smooth geodesic/
incidence dependence therefore gives the received ratio

    Z(t,epsilon)=1+n(t).V(t)+O_C1(epsilon²).

This supplies the needed differentiated remainder locally. Compactness of the
direction sphere permits a common sufficiently small tube for the exact
spherical average. No finite-distance tolerance, universal convergence radius
or survey extrapolation follows. The candidate already states those limits.

For the angular calculation, write S=H I+sigma. Direct sphere contractions give

    <|Bn|²>=H²+(sigma²+W²)/3,
    <(n.Bn)²>=< (n.Sn)² >=H²+2sigma²/15.

Subtracting gives sigma²/5+W²/3. Together with <T(n,n)>=Ric(U,U)/3 this yields
the candidate's M exactly. Where H(n)=n.Bn is nonzero, z/r tends to H(n), so
dot z/z tends to J(n)/H(n). The restriction is genuine; at H(n)=0 that quotient
may fail although the r-coordinate limit is well defined. Averaging Hs rather
than multiplying separate averages is correctly specified.

## Exact adverse control and protocol check

For one fixed Minkowski source label q, v=Bq is constant and
t_o=t_e+|q+t_e v|. Put R=|q+t_e v| and N=(q+t_e v)/R. Direct differentiation
gives dt_o/dt_e=1+N.v, dN/dt_o=P_N v/[R(1+N.v)]. Since d tau_e=dt_e/gamma_v,

    Z=gamma_v(1+N.v),
    dot Z=gamma_v |P_N v|²/[R(1+N.v)].

At t_o=0, q=(I-RB)^(-1)R N, so v=R B N+O(R²). For B=diag(2h,h,h),
|P_N BN|²=h² N1²(1-N1²); its average is h²(1/3-1/5)=2h²/15.
The shear has norm squared2h²/3, hence sigma²/5 removes precisely that mean.
Ric=0 is immediate from the original flat metric, not manufactured from M.
The stated bound hR<1/8 implies |v|<=2hR/(1-2hR)<1/3, and the required
inverse exists. Each derivative holds its actual q fixed even though different
q are chosen for different members of the limiting family.

Minor notation precision for integration: the exact control's R,N are retarded
emission separation/direction, whereas the general theorem starts with
simultaneous Fermi r,n. Here q=R N+R²BN+O(R³), so

    r=|q|=R+O(R²),          n=N+O(R),

with differentiable remainders under the fixed-history derivative. Thus the
limiting J and its spherical average agree. The current candidate explicitly
defines the control through its emission event, so this is not a false finite
identity or blocking error. Smallest clarity improvement: state this handoff
in the review response/integration, without editing frozen initial evidence.

The separate v=+/-3/5 source/receiver chain-rule example recomputes to ordinary
same-coordinate quotient4/5 and actual received Z=2 or1/2. It supports the
protocol warning. The inspected extended-compass paper expressly discusses
time-transfer modeling; the synthesis correctly avoids claiming its inverse
formulas are disproved by this example.

## Physical meaning, duplication and literature scope

The candidate keeps the additional positional requirement intact while refusing
to assign it by fiat to M, J or measured Ricci. A far-separation limiting family
is not a local temporal drift-sign premise. Ordinary proper clocks and W4
also do not supply that sign. PSW/J1 already separates clock curvature from
positional attribution; T2 is a different-preparation diagnostic. The claim
that no tested bridge closed the physical assignment is properly source-bound,
not a statement that no native connection can exist. There is no hidden demand
that a law choose one universe or eliminate legitimate initial/query data.

The three source ledgers count3+3+4 substantive primary papers. The explicitly
discarded mistaken identifier is separate metadata exposure; even counting it
gives11, within the12-paper cap. All papers opened in this reviewer context
were already in that allocation. The ledgers disclose missing paper byte pins,
failed screenshot/download access and partial section reconstruction. I can
verify the actual documents and my own access; their access-history claims are
attributed records, not independently observed researcher execution.

After source-first sealing I additionally inspected Avalos1611.10198v2 §IV's
proper-time equivalence and §V's reunion/integrability argument, the complete
operative definition/time-transfer passage in Neumann2006.09716v2 §II, and
2010.06534v2 §2 equations12–16. They support the retained distinctions: a
clock-definition premise matters to the Weyl statement; no second clock effect
does not mean equal accumulated elapsed times; luminosity distance introduces
photon and energy-flux identifications beyond an angular screen. These were
not pre-seal reads and are not claimed as full-paper audits.

I also directly checked2406.06167v1 §VII against its displayed(26) and §IX.
The stated spatial-Ricci sign tension is visible. Quarantining that quadrupole
while independently deriving the monopole is appropriate. I do not adjudicate
the external paper's full calculation or declare any existing UDT source wrong.
The other three allocated papers were not independently opened by this reviewer;
their bounded literature summaries remain attributed to researcher source
inspection, with omissions preserved.

No necessity for extra physics, selected population, field law, scale, global
completion, empirical detection or successor campaign is inferred. The closest
survivor is a conditional rigidity guard plus corrected local diagnostic, with
both physical antecedents still explicit. Native selection remains unclosed in
these tests. Final central integration, graph/descendant disposition, required
maintenance/full406 receipts and banking remain for their separate actual review.
