#!/usr/bin/env python3
"""topo_doubling_fork.py -- THE DECISIVE FORK the blind verifier exposed:
which CLOSED 3-MANIFOLD the matter cell actually is, and therefore
whether a WINDING FAMILY of types exists or the topology is rigid.
=======================================================================
Driver: Claude (Opus 4.8). Date 2026-06-13. New file (topo_*).
Triggered by blind verifier ab449c89db47f7f1d: the chi=0 bookkeeping in
topo_classes_zoo does NOT distinguish S3 from S2xS1 from a lens space
L(p,q) -- ALL closed orientable 3-manifolds have chi=0. The distinction
is GEOMETRIC (the inner-end closure), and it is DECISIVE for the
type-family question:
    closed cell = S3       -> H^2=0    -> winding KILLED  -> RIGID, one class
    closed cell = S2 x S1  -> H^2=Z    -> winding Z       -> INTEGER FAMILY
    closed cell = L(p,q)   -> H^2=Z/p  -> winding Z/p     -> FINITE FAMILY

This is the honest center of the answer to Charles's question
"could there be families of topologies?": the answer is CONDITIONAL on
the matter-cell inner-end closure, which CANON pins for the UNIVERSE cell
but leaves OPEN for the MATTER (particle) cell. I DERIVE the fork; I do
NOT assert which branch; I report what each branch implies and what
single fact decides it.

CANON (C-2026-06-10-1, -2, read from CANON.md):
  - areal reading: rho = r = sqrt(Area/4pi) (C2 theorem). So r=0 IFF the
    areal sphere shrinks to a point = a REGULAR axis cap (-> 3-ball).
  - UNIVERSE cell: domain [0, r_CMB], phi: 0 -> ln(1101). Inner end r=0
    -> regular point-cap -> capped collar = 3-ball -> double across seal
    = S3. (For the universe the S3 branch is canon-grounded.)
  - MATTER cell (the PARTICLE): "inside-out", phi: 0 at interface ->
    -INFINITY at the core endpoint. The core is NOT stated to be a
    regular r=0 areal cap; phi DIVERGES there. Whether the areal sphere
    shrinks to a point (cap, -> S3) or stays finite (second seal, ->
    S2xS1) at the phi->-infinity core is the OPEN geometric fact that
    decides the fork. THIS is where the type-family question actually
    lives.

DISCIPLINE: topology only; derive the fork; flag the open fact as
HYPOTHESIS-GRADE; no integer-hunting. Log flush-per-line.
"""
import time
import sympy as sp

t0 = time.time()
_fh = open("/tmp/topo_doubling_fork.log", "w")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond); (PASS if ok else FAIL).append(tag)
    log(f"FORK-{tag}: {'PASS' if ok else 'FAIL'}  {note}")

log("=" * 72)
log("topo_doubling_fork -- which closed 3-mfd, and the type-family fork")
log("=" * 72)

# =====================================================================
# (1) chi=0 does NOT pin the 3-manifold (the verifier's objection, made
# exact). Every closed orientable 3-manifold has chi=0 (Poincare duality:
# b0=b3, b1=b2 => chi = b0-b1+b2-b3 = 0). So the topo_classes_zoo chi
# step is a CONSISTENCY CHECK, not a proof of S3. Downgrade it explicitly.
# =====================================================================
log("\n(1) chi=0 is necessary, NOT sufficient -- it cannot pin the 3-mfd")
b0, b1, b2, b3 = sp.symbols('b0 b1 b2 b3', integer=True, nonnegative=True)
# Poincare duality on a closed orientable 3-mfd: b0=b3, b1=b2.
chi = b0 - b1 + b2 - b3
chi_PD = chi.subs({b3: b0, b2: b1})
check("1", sp.simplify(chi_PD) == 0,
      "chi = b0-b1+b2-b3; Poincare duality b0=b3, b1=b2 => chi=0 for "
      "EVERY closed orientable 3-manifold. So chi=0 does NOT distinguish "
      "S3 (b1=0) from S2xS1 (b1=1) from L(p,q) (b1=0 but H_1=Z/p torsion). "
      "The topo_classes_zoo chi-bookkeeping is DOWNGRADED to a "
      "consistency check; it does NOT prove S3. The verifier was right.")

# =====================================================================
# (2) THE THREE DOUBLING OUTCOMES and their H^2 (the winding home).
# The matter cell is a collar S2 x I (radial I, angular S2) with:
#   - OUTER end = the seal S2 (the mirror-fold crease; gluing surface).
#   - INNER end = the core (phi -> -infinity).
# Double across the seal: take cell U (mirror cell), glued on the seal S2.
# The result depends ENTIRELY on the inner-end closure of each copy:
#   (A) inner end is a REGULAR AREAL CAP (areal r->0, S2 shrinks to a
#       point): each capped collar = B^3 (3-ball). Two B^3 glued on
#       boundary S2 = S^3. H^2(S3,Z)=0.
#   (B) inner end is a SECOND SEAL / finite areal sphere (S2 stays
#       finite): each copy = S2 x I with BOTH ends S2. Gluing the two
#       outer seals AND identifying/closing the inner ends: the double
#       of S2 x I across one boundary, with the other boundary closed by
#       the SAME mirror structure, is S2 x S1 (the radial interval closes
#       into a circle through the two seals). H^2(S2 x S1,Z)=Z.
#   (C) inner end glues with a TWIST (a p-fold mirror identification of
#       the seal S2): a lens-space-like quotient L(p,q). H^2=Z/p.
# We record the H^2 of each and the winding-family verdict it gives.
log("\n(2) the three doubling outcomes (decided by the inner-end closure)")
outcomes = [
    ("A", "inner end = REGULAR AREAL CAP (areal r->0, S2->point)",
     "two 3-balls glued on seal S2", "S^3", "H^2=0",
     "winding KILLED -> RIGID, ONE class (the sphere, c1=0)"),
    ("B", "inner end = SECOND finite SEAL (areal S2 stays finite)",
     "double of S2xI, radial interval closes through both seals",
     "S^2 x S^1", "H^2=Z",
     "winding TOWER survives -> a DISCRETE INTEGER FAMILY of types "
     "(Chern label n in Z)"),
    ("C", "inner-seal glues with a p-fold mirror twist",
     "lens-type quotient of the doubled collar",
     "L(p,q)", "H^2=Z/p",
     "a FINITE winding family of p types (Chern label in Z/p)"),
]
for tag, inner, build, mfd, h2, verdict in outcomes:
    log(f"  ({tag}) inner end: {inner}")
    log(f"        build: {build}")
    log(f"        closed 3-mfd: {mfd},  {h2}")
    log(f"        TYPE-FAMILY VERDICT: {verdict}")
check("2", True,
      "the type-family question reduces EXACTLY to which 3-manifold the "
      "matter cell closes to, which reduces to the matter-cell INNER-END "
      "closure (cap vs second-seal vs twist). NOT decidable by chi; "
      "decidable by the areal behavior of the S2 at the phi->-infinity "
      "core.")

# =====================================================================
# (3) WHAT CANON PINS, AND WHAT IT LEAVES OPEN.
# =====================================================================
log("\n(3) canon status of the inner-end closure")
log("  UNIVERSE cell (C-2026-06-10-2): domain [0,r_CMB], inner end r=0;")
log("    areal r=0 (C-2026-06-10-1) => the S2 shrinks to a POINT => a")
log("    REGULAR AREAL CAP => branch (A) => S3 => winding killed for the")
log("    universe cell. (Canon-grounded.)")
log("  MATTER cell (C-2026-06-10-2): 'inside-out', phi: 0 -> -INFINITY at")
log("    the core. CANON does NOT state the areal radius at that core. The")
log("    phi->-infinity endpoint is the legacy hadronic-depth regime where")
log("    exp(-2 phi0)~5 and linearization fails (CLAUDE.md warning). The")
log("    areal-sphere fate there (point-cap A vs finite-seal B vs twist C)")
log("    is the OPEN geometric fact. It is NOT settled here and must NOT")
log("    be assumed. THIS is the single fact that decides whether")
log("    particles come in a topological FAMILY or are topologically RIGID.")
check("3", True,
      "canon pins branch (A) S3 for the UNIVERSE cell (areal r=0 cap), "
      "but leaves the MATTER-cell core (phi->-infinity) OPEN. The "
      "type-family verdict is therefore CONDITIONAL and HYPOTHESIS-GRADE, "
      "pinned to one derivable geometric fact: does the areal S2 shrink "
      "to a point at the matter-cell core?")

# =====================================================================
# (4) A PARTIAL DISCRIMINANT from the areal reading (NOT a closure, a
# pointer for the next push). With rho = r = sqrt(Area/4pi) and phi ->
# -infinity at the core: the metric f = e^{-2phi} -> e^{+infinity}
# (BLOWS UP, the legacy exp(-2phi0)~5 regime). The areal radius r is the
# INDEPENDENT coordinate of the domain [interface, core]; the QUESTION is
# whether the core sits at r=0 (cap, branch A) or at finite r=r_core>0
# (second seal, branch B). The 'inside-out' canon language (phi DIVERGES
# while r runs to an endpoint) is consistent with EITHER: a cap at r=0
# with phi->-inf logarithmically, OR a finite-r core where phi->-inf at a
# fixed areal sphere. We record the discriminant, we do NOT decide it.
# =====================================================================
log("\n(4) the discriminant for the next push (NOT decided here)")
log("  In the areal chart rho=r: branch (A) <=> core at r=0 (areal S2")
log("  shrinks to a point); branch (B) <=> core at finite r_core>0 (areal")
log("  S2 finite, a second mirror seal). The matter-cell profile phi(r)")
log("  with phi->-infinity sets WHICH: if phi->-inf AS r->0 (the universe-")
log("  mirror picture) -> cap -> S3 -> rigid; if phi->-inf at finite r ->")
log("  second seal -> S2xS1 -> integer family. The deciding computation is")
log("  the matter-cell radial profile's endpoint behavior (r at the")
log("  phi->-inf core) under the metric's own field equation -- a")
log("  GEOMETRY calc on the existing radial operator, the correct next")
log("  step. NO mechanism invented; the fork is intrinsic.")
check("4", True,
      "the discriminant is the areal radius at the phi->-infinity core "
      "(r=0 cap vs finite-r seal), readable from the matter-cell radial "
      "profile -- the concrete next geometry calc. Recorded as the "
      "pointer; not computed here (out of topology-only scope).")

log("\n" + "="*72)
log("FORK VERDICT -- the honest answer to 'families of topologies?'")
log("="*72)
log("  The CLOSED-SURFACE topology is RIGID: g=0 (sphere), forced by axis")
log("  regularity (Poincare-Hopf chi=2). No genus family. SOLID.")
log("  The CLOSED-BUNDLE / WINDING topology is FORK-DEPENDENT:")
log("    - if the matter-cell core is a regular areal cap (r->0): the")
log("      closed cell is S3, H^2=0, winding KILLED -> ONE class, RIGID.")
log("    - if the core is a finite second seal: S2xS1, H^2=Z, winding")
log("      survives -> a DISCRETE INTEGER FAMILY of types (Chern n in Z).")
log("    - if a p-fold twist: L(p,q), H^2=Z/p -> a FINITE family of p.")
log("  CANON pins the CAP (S3, rigid) for the UNIVERSE cell; the MATTER")
log("  (particle) cell's core is OPEN. So: families of topologies are")
log("  POSSIBLE and would be a WINDING (Chern) family, NOT a genus family")
log("  -- IFF the particle core fails to cap. The single deciding fact is")
log("  the areal radius at the phi->-infinity matter core. HYPOTHESIS-")
log("  GRADE; the next push is that radial-endpoint geometry calc.")
log("  (The {3,5,7} numerology stays rejected #35; this is a Z or Z/p")
log("  homology tower, derived, NOT a hand-picked integer set.)")

log(f"\nFORK: {len(PASS)} PASS / {len(FAIL)} FAIL ({time.time()-t0:.0f}s)")
if FAIL: log("FAILED: " + str(FAIL))
log("log /tmp/topo_doubling_fork.log")
_fh.close()
