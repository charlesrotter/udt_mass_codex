# Operational probe freeze — COC1 B

Exposure: parent reported that A independently selected the same scalar projector
after INITIAL_PROPOSAL was saved. A now owns physical attribution and Bianchi;
B owns operational affine calibration. Before this cross-exposure I had begun
deriving a radar-cut alternative. No A derivation has been read.

The affine optical statistic is vulnerable to a cubic distance relabeling:
if s=lambda+b(n)lambda^3+O(lambda^4), the area/s^2 coefficient shifts by -2b.
Therefore local first-order calibration s/lambda->1 is inadequate. First test
will derive and check how actual two-way proper timing fixes the cubic cut.

**RC1 — proposed geometric protocol, not a physical field law.** A freely
falling source emits at p=gamma(0), and the return is received at q=gamma(2l).
The immediate-relay events comprise the small smooth cut
S_l=boundary I+(p) intersect boundary I-(q). l is half the actual proper
round-trip interval, in c_E=1 length units. Measure proper screen area on that
cut and source angular directions. Auxiliary rulers/relays are declared ideal
measurement data under W4, not a naturally selected observer population.

Target formulas to audit, with e(n)=g(R(n,U)U,n), k=U+n:

    lambda=l+e(n)l^3/3+O(l^4),
    (dA_l/dOmega)/l^2=1+[2e(n)/3-Ric(k,k)/6]l^2+O(l^3),
    Ric(k,k)=4e(n)-6a(n),
    Area(S_l)=4pi l^2[1-Scal*l^2/18+O(l^3)].

a(n) denotes the measured leading normalized radar-area coefficient. e(n)
comes independently from the already established PSW1 preparation if full
null focusing is wanted. Total area alone should recover Scal without that
extra preparation. The leading observer-independent scalar is not automatically
an additional positional contribution or a sign law. This probe tests access.

Domain/quantifier: smooth Lorentz4 with geodesic central clock, sufficiently
small causally convex normal neighborhood and unique regular outgoing/return
branches, compact source sky, fixed U. No caustic, finite cosmological inference,
global completeness, optical brightness/flux or Einstein equation assumption.
Errors: local smooth-jet O(l^3) after normalization; no numerical certified
finite-size constant. Fixed proper-time calibration is pinned by protocol; U,
metric and scale tend-to-zero sequence are free-and-explored. Central free fall
is an explicit preparation, not a universal assignment.

Nearest primary result found after deriving target: Gibbons–Solodukhin,
arXiv hep-th/0703098v3, section3 equation29 gives
A=pi tau^2[1-Scal*tau^2/72+...], tau=2l. This agrees with the target. It is
standard borrowed metric geometry, no novelty claim. Wang1904.01034v2 distinguishes
Alexandrov, geodesic-ball and affine-lightcone constructions, warning that their
coefficients differ. Source notes and exact access scope will accompany the return.

Finite exact CPU check planned: use SymPy only, under TPS1 capture.py, to derive
scalar curvature directly from several original smooth metrics and independently
expand their exact radar-cut areas; compare formulas. Include de Sitter and
ultrastatic constant-spatial-curvature controls, an accelerated Minkowski clock
showing why free fall cannot silently be dropped, generic symmetric Ricci
algebra, and the cubic reparameterization ambiguity. These are finite exact
controls, not proof for arbitrary geometry or independent-context verification.
One worker at a time,2GiB virtual memory,one BLAS thread,no wall/CPU killing
timeout,no GPU/install. Preserve all captures and failures.
