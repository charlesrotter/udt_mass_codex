# Adversarial Review 2 — object faithfulness, residual honesty, steer/scope

Reviewer: independent adversarial pass (Opus, zero-credit). Date 2026-08-06. Branch grok.
Target: `MAP_AND_PROBE1.md` + `DERIVATION_NOTES.md` (Probe 1, landed TL-INVARIANT-GENERIC).
Context read: static null (`udt_ceff_crux_test_probe_2026-08-06`), retraction
(`udt_timelive_depth_cocycle_probe_2026-08-05`).

ALGEBRA INDEPENDENTLY REPRODUCED (sympy, coordinate Christoffel->Riemann->frame, NOT Cartan):
- general-diagonal frame sectional curvature R_{0101} matches the probe's general R^0_1 formula;
- lock specialization matches `{c^2(2phi_x^2-phi_xx) - e^{4phi}(2phi_t^2+phi_tt)}e^{-2phi}/c^2` EXACTLY (diff=0).
- static reduction (phi_t=0) is nonzero -> delta_t holonomy non-exact ALREADY static: confirmed.
The Q3 result (timelike-leg curvature survives independent A,B; theta, gamma un-collapse generic) is
arithmetically correct. The defect, if any, is object/scope — not the algebra.

## 1. OBJECT FAITHFULNESS — the probe collapsed the nonlocal object to a LOCAL scalar.

The MAP posed copresence nonlocally: N2 = finite between-points ratio V(A)/V(B); N3 = loop HOLONOMY;
N4 = Machian. Charles's copresence = "interconnectedness," a relation between DISTANT points.

What Probe 1 actually extracted as its "nonlocal invariant" is **R^0_1 = the frame sectional
curvature** — a POINTWISE scalar evaluated at one event — plus **gamma = cosh w**, a local scalar at
the probe point. Both are exactly what a pointwise-invariant scan handles. The probe reached them by
taking the DIFFERENTIAL of the depth 1-form (d omega^0_1 = R^0_1) and reading "R^0_1 != 0 =>
delta_t non-exact." That differential step DISCARDS the finite/global content of N2 (the finite ratio
between two SPECIFIC points) and keeps only the local density. N3's "loop holonomy" was likewise
identified with its curvature density R^0_1. On a simply-connected R^{1,1} patch this identification is
complete (Stokes: ∮omega = ∫∫R^0_1) — but that is precisely the LOCAL COLLAPSE. So "F-GENERIC at the
local level" is a verdict on the pointwise curvature, NOT on the between-points relation. It does not
settle the nonlocal question; it evades it, structurally repeating the static probe's error one level
up (static rigged u to the KV; here u is rigged to the coordinate-t normal, forcing twist=0 and a
trivially-integrable foliation — the N1 obstruction is killed by the ansatz, not tested).

## 2. RESIDUAL HONESTY — "must go to matter/N4 or the law" is PREMATURE; it conflates
"not in local kinematics" with "not in matter-free physics."

There is a matter-free, nonlocal, TOPOLOGICAL object between the tested-local and the deferred-matter-N4
that the probe skipped: **the depth-boost holonomy ∮ omega^0_1 around a NONCONTRACTIBLE time cycle**
(the abelian boost period). The boost connection is abelian (single 2D boost), so around a CONTRACTIBLE
loop the holonomy = ∫∫R^0_1 (what the probe computed). Around a noncontractible cycle — a compact/cyclic
time with WINDING — ∮ omega^0_1 is an INDEPENDENT period, NOT equal to any area-integral of R^0_1, an
Aharonov-Bohm/flat-connection-type invariant that survives even where local curvature is small. It:
- needs NO matter source (pure geometry + topology) — so the residual's hand-off to N4/matter is wrong;
- is genuinely nonlocal (a copresence relation carried around a closed time-loop — "a point with itself
  around time"), faithful to "interconnectedness";
- is LIVE in the project's OWN banked frame: the T-lane certifies massive carriers with time-winding
  n_t (MEMORY 2026-07-31); compact-time cycles are not exotic here, they are on the desk;
- carries the lock structure: the dt-component of omega^0_1 is c e^{A-B}A_x -> under the lock
  c e^{-2phi}(-phi_x), i.e. the reciprocal combination A-B=-2phi. Whether its PERIOD is UDT-specific is
  unresolved BECAUSE IT WAS NOT COMPUTED — that is the point.

Second (weaker) untested matter-free object: N2 as the FINITE two-point ratio V(A)/V(B) itself, as a
pair-invariant, rather than its local generator. Under the reciprocal lock the time-leg and space-leg
finite stretches are constrained (A=-B), a between-legs relation the single-leg delta_t curvature cannot
see. (Caveat, stated against my own point: g_tt g_xx = -c^2 is a spatial-recoordinatization gauge
statement; its content requires holding the physically-preferred UDT chart, which copresence itself is
supposed to select — a circularity that must be handled, not a clean win. The time-holonomy is the
cleaner untested object.)

So the residual is not FORCED. "Free-kinematic level exhausted" is true only for CONTRACTIBLE, LOCAL
objects on R^{1,1}. A matter-free topological rung remains and is cheaper than N4.

## 3. STEER / SCOPE.

- Reverse-steer (over-deflation) on the TESTED objects: NO. The Q3 deflation of R^0_1, theta, gamma is
  honest and correct (I reproduced it); flagging delta_t non-exact-already-static is a genuine anti-steer
  move that surrenders the easy time-live "prize." That part is clean, not under-credited.
- Over-deflation in the RESIDUAL/SCOPE: YES, mild. The scope stamp "time-live reciprocal-lock,
  free-kinematic" silently ALSO assumes (i) contractible R^{1,1} topology and (ii) copresence = the
  coordinate-t normal (twist-free). Those two hidden premises are exactly what annihilate the nonlocal
  object. They belong in the stamp. Generalizing the LOCAL null to "the matter-free level is exhausted"
  is the over-reach.
- Push to N4/matter: legitimate as a deep TARGET, illegitimate as the ONLY next step — it defers a null
  past a cheaper matter-free test (the winding holonomy). Testing matter before topology is the wrong
  order and risks parking a null indefinitely behind a matter source that then gets blamed.

## VERDICT: OBJECT-TOO-LOCAL.
The local test was fair FOR contractible/local objects and its GENERIC finding is honest; but the
nonlocal object Charles named was reduced to a pointwise curvature scalar, and a matter-free nonlocal
invariant was left untested: the depth-boost holonomy ∮omega^0_1 around a noncontractible time-winding
cycle (independent of ∫∫R^0_1 off contractible patches; needs no matter; connects to the banked n_t
sector). The residual's jump to N4/matter is therefore premature. Recommend: before invoking matter,
compact the time direction (the project's own n_t topology) and compute the boost-holonomy PERIOD and
its Q3 lock-relaxation behavior. Do NOT bank TL-INVARIANT-GENERIC as "free-kinematic exhausted."
