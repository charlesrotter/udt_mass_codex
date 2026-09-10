# Construction partner freeze — supplied completed records and actual immersions

Status: mathematical CANDIDATE, UNPROMOTED, fresh review pending. Frozen before the
confirmation subprocess; the algebra below was explored by hand after reading sources.
Date: 2026-09-10. Baseline `grok` at `2d9f607fd0ff085aaaa93219028f6abb6d537091`.
Parent reports same-session mandatory startup, actual365 PASS, fetch/pull; this partner
attributes those checks and independently checked branch, HEAD and visible status.
Parent method-only edits and original protected/untracked state are outside this task.
Runtime model/version UNATTESTED. This is the one construction partner, no subdelegation.

## Question and source ownership

Roadmap exact-metric/kernel stages 1–2 plus simultaneous-realization stage 3. Within the
authorized smooth local metric/observer class, which supplied completed pair records
recover the metric and its first coordinate jet, once lapse, spatial shape and stationarity
are no longer fixed? This is an exact conditional representation/data statement, not
novel metric tomography, physical acquisition, native field-law selection, or a complete
minimality theorem. Parent handles the rotation formula and coupled witness.

G176 owns working completed-pair normalization, conditional on the provisional working
clarification, not canon. G179 owns the full rank-two pullback, m=sqrt(-det h), retained
normalized shift, and Phi=-log T on each regular germ. G180 owns the smooth positive
density and tape integration along one supplied connected one-dimensional family.
G182 separates intrinsic Gram/metric data from supplied full immersion/coframe carry.
G216 identifies T=dτ/dt for the supplied common comparison-clock tangent, and forbids
silently replacing it by unit U while retaining a nonzero endpoint Phi.
Their exact registry rows and on-disk audit reports control grades. G179/G180/G216
exact derivations were read; no source scientific code was read or imported.

## Frozen class, choices and omissions

On a supplied smooth coordinate neighborhood (t,x1,x2,x3), use

    g = -N(t,x)^2 (dt + β_i(t,x) dx^i)^2 + γ_ij(t,x) dx^i dx^j,
    N > 0, γ positive definite, U = N^-1 ∂t.

Signature (-+++), dimension 3+1, smoothness/regularity and the common comparison-clock
marking are supplied choices admitted by the work order (pinned-by-HABIT means declared
chart/class convention, not a physical law). N, β and γ are free-and-explored profiles,
subject only to the displayed class conditions. The split is a convenient exact chart
for the stated observer congruence, not a selected physical coordinate system.
c_E=1 is dimensional calibration only; no scale value is inferred. No boundary/initial
problem, field equation, action, matter, topology, physical instruments or populations.

For each constant nonzero spatial direction v and supplied base label a, use the ACTUAL
pair surface F_{a,v}(t,σ)=(t,a+σv), restricted inside the chart. Its columns are
J_v=(∂t,v^i∂i), which commute and have rank two. The direction set is
D={e1,e2,e3,e1+e2,e1+e3,e2+e3}; linear dependence and common basepoint identification
are supplied coordinate facts. These are mathematical probes, not claimed physical access.

The record map retains common labels/calibration plus the positive germ density m_v and
the G179 normalized germ shift B_v, as well as T (or its absolute calibrated Phi):

    T=N, m_v=N sqrt(γ(v,v)), B_v=β(v)/m_v, Phi=-log T.

The density m_v is retained RELATIVE TO THE SUPPLIED AUXILIARY DIRECTION/CLOCK marking;
it is not reconstructible from one normalized 2x2 pair metric. Relative endpoint depths
alone do not supply absolute T. First jets mean derivatives with respect to the original
common (t,x) chart, including transverse directions; they are not just along-pair derivatives.

## Frozen reconstruction map and compatibility checks

Set q_v=(m_v/T)^2 and b_v=m_v B_v. Then

    N=T,
    β_i=b_ei,
    γ_ii=q_ei,
    γ_ij=(q_(ei+ej)-q_ei-q_ej)/2  (i<j).

With common positive T, positive m_v, smooth matching of common labels, the sum-direction
shift conditions b_(ei+ej)=b_ei+b_ej and recovered γ positive definite are sufficient
for the displayed local metric to reproduce all six supplied record functions. Every
pair surface above then coexists in that ONE smooth metric. This is a conditional
sufficiency statement for this finite chart-marked recipe; no arbitrary record family
or full inverse theorem is claimed. For first-jet data the equalities are differentiated
in the same common chart. The reconstructed metric first jet follows by product and
quotient rules. No second metric jet or curvature reconstruction follows from first jets.

## Frozen rejection controls and their exact intended defects

1. Delete m: g_λ=-dt²+λ²δ_ij dx^i dx^j with β=0 gives the same T=1,B_v=0 for
   every direction but different metric components, m_v and rest inverse metric.
2. Delete mixed directions: γ=I and γ with γ12=γ21=1/3 retain all three axial
   q_ei while the cross component differs. Both γ are positive definite.
3. Assume six directional positivities imply SPD: γ=[[1,2,0],[2,1,0],[0,0,1]]
   has positive q on D yet γ(e1-e2,e1-e2)=-2. These pairwise-regular arrays do
   not belong to the admitted observer-rest class.
4. Ignore sum-direction shift coherence: change b_(e1+e2) alone. No common linear
   one-form β reproduces the three corresponding values under the fixed labels.
5. Replace coordinate ∂t by normalized U without changing data: for N=exp(x1),
   [U,∂1]=N^-1∂1(log N) ∂t≠0 and T for U is 1, not N. A germ at one event may
   have those columns, but that exact pair of fields is not a coordinate basis.
6. Treat ds=m(t,σ)dσ as a full 2D coordinate differential with unchanged clock:
   m=exp(t), s=exp(t)σ gives ds=exp(t)dσ+s dt; the normalized fields do not
   commute. Fixed-t leaf tape exists, but at fixed s the time tangent changes.

## Resources, verification and maximum claim

CPU only; no GPU/grid, no floating-point approximation or tolerance. One fresh standalone
SymPy exact construction script, no prior author scientific imports. It checks abstract
six-direction algebra, one jointly time/spatially varying SPD example, differential
reconstruction, immersion rank/commutation, and all six rejection controls. Algebraic
confirmation supplements the explicit proof, and is construction regression, not an
independent review. Preserve script, versions, commands, stdout, stderr, exit code and
source hashes. Each scientific subprocess timeout 120 seconds; partner target by
23:15 UTC, full campaign return 00:48:30 UTC. On mismatch preserve the diagnostic,
identify the defective step and repair only within the frozen class. No commits or
edits outside this package's whiteboard directory.

## Pre-check clarification from parent, 2026-09-10

Parent independently agreed that the pointwise/leafwise distinction is central. Before
running confirmation, add this explicit control: the actual metric
g=-dt²+exp(2t)dx²+dy²+dz² and actual v=e1 surface have T=1,m=exp(t),B=0.
For s=exp(t)σ the genuine transformed pair metric is -dt²+(ds-s dt)².
Its determinant is still -1, but its fixed-s clock factor is sqrt(1-s²),
regular as a G179 clock only on |s|<1. It is a changed clock congruence, not
new physical behavior or a correction to the original completed scalar. Check
this by an explicit coordinate Jacobian and compare original- versus fixed-s
clock columns. This supplement precedes all confirmation output.
