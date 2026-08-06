# Adversarial Review 1 — hunt for a missed lock-specific invariant (anti-FALSE-NEGATIVE)

Date 2026-08-06. Branch grok. Reviewer: blind adversarial (Opus), zero probe-code imported.
Independent sympy 1.13.1 engine (`scratchpad/adv_*.py`: Christoffel→Riemann→Ricci→frame from
scratch; verified against nothing in the probe dir). Target contract: `MAP_AND_PROBE1.md` (frozen);
LEAD under review: `DERIVATION_NOTES.md` (class TL-INVARIANT-GENERIC).

Mandate: attack the NEGATIVE. Try HARD to find a lock-specific invariant of
`ds^2=-e^{-2phi}c^2dt^2+e^{2phi}(dx^2+dy^2+dz^2)` (lock: A=-B and C=B, phi(t,x)) that the probe
missed. Rules: a hit must be (a) coordinate-invariant/measurable (not F-GAUGE, not a probe direction),
(b) genuinely absent for independent g_tt,g_xx.

## What I recomputed independently (all EXACT, transcribed)
Full anisotropic diagonal metric `diag(-e^{2A}c^2,e^{2B},e^{2C},e^{2C})`, A,B,C(t,x). Orthonormal-frame
Ricci {R00,R11,R22,R01}, sectional curvatures {R_0101,R_0202,R_1212,R_2323,R_0212,R_0112},
Einstein eigenvalues {rho=G00,p_x=G11,p_T=G22,G01}, Ricci scalar. Specialized to LOCK and to two other
one-function families to separate reciprocity from mere DOF reduction.

## Hunt results (each reviewer sub-question)

**#1 ON-lock distinguished combination (does something become special ON-lock, not just vanish off-lock).**
- Constant-coefficient LINEAR relations among the 10 curvature invariants: LOCK has exactly **5**
  (adv_relations.py). GENERAL independent A,B,C has exactly the **same 5** (adv_step2.py). All 5 are
  the UNIVERSAL Ricci-from-sectional-curvature identities (e.g. R00=R_0101+2R_0202), true for any
  metric. The lock adds ZERO extra linear invariant relation.
- Pointwise dimension count: after the 5 universal relations, 5 independent invariants remain; they are
  functions of 6 independent jet numbers (phi_x,phi_t,phi_xx,phi_tt,phi_tx,E=e^phi). 5<6 ⇒ NO algebraic
  relation at all (linear or nonlinear) is forced pointwise. No distinguished combination goes special.
- Einstein EOS (rho,p_x,p_T are true invariant eigenvalues): NO reciprocity-specific relation
  (adv_eos.py). Red herring caught: "halflock" (A=-B, C=0) gives rho=p_x=0 identically — but that is the
  UNIVERSAL vanishing of the 2D Einstein tensor for any M^2×flat-R^2 product, NOT reciprocity (a
  conformal 2D block ×flat gives the same). Confirms the engine; not a hit.

**#2 Nonlocal / holonomy.** The boost curvature R^0_1=dω^0_1 is a diffeo-COVARIANT 2-form (= the (t,x)
sectional curvature). Its loop holonomy is therefore preserved by any diffeomorphism — including the
lock-breaking reparam below — so it is NOT lock-special. It is ordinary spacetime curvature, nonzero
already STATICALLY (matches the probe's honest residual); smooth, no period lattice, no topological
quantization. The integrated depth-stretch V(A)/V(B) = Z·L reciprocity is coordinate-dependent (see #4).

**#3 Transverse sector.** R^0_2-type mixing (R_0212=-(phi_t phi_x+phi_tx)/c under lock) has the same
generic form as any anisotropic metric. Conformal-flatness (Weyl) tracks the CONFORMAL family A=B=C
(manifestly e^{2phi}η, Weyl=0), NOT the reciprocal lock (Weyl≠0) — so Weyl does not fingerprint
reciprocity. The transverse tie C=B is broken by the same reparam below while invariants are preserved.

**#4 Causal/reciprocal signature.** c_eff=c·e^{-2phi} is a COORDINATE light speed (coordinate-dependent).
Z·L=1 holds iff A+B=const; but L=e^{B_b-B_a} is NOT invariant under x→f(x) (g_xx→g_xx/f'^2). So Z·L=1 is
a statement in the reciprocal GAUGE = F-GAUGE. Killed directly by the reparam demonstration.

## DECISIVE unifying reason (sharper than the probe's DOF argument)
The reciprocal lock g_tt·g_xx=-c^2 (and the transverse tie C=B) is a COORDINATE/GAUGE condition:
a spatial reparametrization x=h(X) sends B→B+ln h', leaving A,C untouched, so A+B=ln h'≠0 and
g_tt·g_xx=-c^2 h'^2≠-c^2 — the lock is BROKEN — while the metric is the SAME spacetime, so every local
curvature invariant is unchanged. Verified exactly+numerically (adv_reparam2.py): with
phi=(1/3)log(1+t^2+x^2), h=x+x^3, the Ricci scalar is bit-identical for lock and broken-lock at every
sampled point (diff=0.0e+00), while g_tt·g_xx/(-c^2)=(3x^2+1)^2.
⇒ No local curvature invariant, and no diffeo-covariant nonlocal holonomy, can detect the lock. Any
object that IS lock-special must be coordinate-dependent (F-GAUGE) or rest on the copresence/preferred-
frame posit (CHOSE, Q2b), NOT on the metric. This is WHY the hunt fails, not merely that it did.

## VERDICT: F-GENERIC-CONFIRMED (with strengthened reason)
No lock-specific invariant exists at the free-kinematic bare-metric level. The probe's TL-INVARIANT-
GENERIC class stands; its Q3 conclusion is correct and, in fact, under-stated: it is not just that the
invariants "survive relaxing the lock," it is that the lock is a gauge condition invisible to
invariants by construction. All four reviewer hunts (pointwise, nonlocal, transverse, causal) fail for
the same reason.

## NARROW boundary (honest scope, not a rescue)
Confirmed ONLY for invariants of the BARE metric, free-kinematic (no source, no law) — the probe's own
scope, F-LAWCLAIM held. It does NOT speak to N4 (Machian/source-level) content: a matter action or
field equation that references phi non-generically could carry lock content, because the lock is a
statement about the metric FORM that a phi-coupled SOURCE can see even though vacuum curvature cannot.
That is exactly the probe's deferred residual and the correct next gate — not a local-invariant hunt.

STRONGEST SINGLE POINT: the lock is broken by a coordinate change that preserves every curvature
invariant (verified diff=0), so lock-specificity cannot live in any bare-metric invariant, local or
nonlocal-holonomic. No FALSE-NEGATIVE found.
