# Preregistration — time-live depth cocycle probe (Probe 1)

Date: 2026-08-05
Branch: grok
Author: driver (Opus), reins handed by Charles 2026-08-05
Mode: MAP + FROZEN CONTRACT. No derivation is run in this document. DERIVE is gated behind
this preregistration per the binding method.

## 0. Origin and intent (owner, verbatim intent)

Charles's hypothesis (2026-08-05): the unselected angular-modulation parameter `a` in the
complete-pair depth family may be a function of going time-live — the freedom might exist
only because the derivation was performed on a stationary (time-frozen) branch. Intent is
to **find more structure and constraints**, not to resolve mass emergence. This probe was
chosen first over the E=mc² parallel by a dependency argument: both act on the same
depth/energy cocycle, but the E=mc² parallel needs the cocycle's off-stationary structure,
which this probe produces; the reverse dependence does not hold.

## 1. What is banked (the object we start from — cited, not re-derived)

From `udt_complete_pair_phi_orchestra_audit_2026-08-05/` (EXACT_DERIVATION.md, AUDIT_REPORT.md):

- The complete comparison arrow `A:(V_p,g_p)->(V_q,g_q)` has a frame-covariant strain
  `C_A = A^dagger A`, `A^dagger = g_p^-1 A^T g_q`. Under independent endpoint Lorentz
  changes `A -> L_q A L_p^-1`, `C_A -> L_p C_A L_p^-1`: conjugacy data (char. poly,
  eigenvalues + causal labels, trace invariants) are endpoint-frame invariant. **This
  object does NOT require stationarity.**
- On the regular Lorentzian stratum with one distinguished timelike eigenline,
  `delta_t(A) = -(1/2) log(lambda_timelike)` is frame-invariant and reduces on the pure
  reciprocal subgroup to the founded signed depth `delta = phi`. Reversal gives
  `lambda_t^-1`, so `delta_t` composes/reverses as a real groupoid 1-cocycle. **Also does
  NOT require stationarity.**
- The one-parameter family `delta_a(p,q) = log[N(p)/N(q)] + a log[R(q)/R(p)]` DOES require
  stationarity: it was obtained on a conditional stationary integrable 2+2 branch after
  SUPPLYING (i) an intrinsic Killing line (defines `N`, the Killing norm), (ii) a screen
  split, (iii) a fixed endpoint screen identification, (iv) the R-to-screen-area
  convention. Every member composes/reverses exactly; the active premises do not select
  `a`.

CRUX LOCATED: the `a`-freedom lives inside the stationary DECOMPOSITION (`N`-term vs
`R`-term), not inside the frame-covariant depth extractor `delta_t` itself. Dropping
stationarity removes the object (`N` = Killing norm) that defines the first term.

## 2. The frozen question

On a time-live (non-stationary) comparison — where no timelike Killing vector is supplied,
so `N` is not defined as a Killing norm and the comparison arrow `A` carries genuine time
evolution between `p` and `q` — recompute the cocycle structure of `delta_t(A)` and ask:

**(Q1)** Does a one-parameter (or larger/smaller) angular-modulation freedom analogous to
`a` survive, once the stationary Killing-line supply is removed and replaced by a time-live
compatible construction of the same depth extractor?

**(Q2)** Does the time-live cocycle-consistency requirement — exact composition/reversal
PLUS single-valuedness (or quantized holonomy) around genuine time-direction loops — CUT
that freedom (to a point, a discrete set, or empty), leave it intact, or render the `N`/`R`
split (hence `a` itself) ill-defined so the question must be reframed?

## 3. Supplied-vs-derived ledger (each tagged; the anti-smuggle gate)

- SUPPLIED / CHOSE: the registered reciprocal-lock metric class and the frame-covariant
  strain machinery (banked, cited). The choice to work on a time-live branch of the same
  registered configuration architecture. Any screen split / endpoint identification that
  must be re-supplied off-stationary is tagged CHOSE and its necessity is itself a result.
- MUST BE DERIVED (not imported): what replaces the Killing norm `N` when no Killing vector
  exists; whether the depth extractor `delta_t` still decomposes into a depth-term and an
  angular-term; the exact freedom (if any) in that decomposition; the time-loop holonomy of
  `delta_t` and whether consistency constrains the freedom.
- FORBIDDEN (Principle 7): importing the ADM/GR lapse-shift split, or the SR/GR energy-
  momentum four-vector, as the definition of the time-live comparison. The strain `C_A` is
  already native and frame-covariant; the construction must ride it, not a GR foliation.
  (Time-live posing hazards are the same ones the July T1 work flagged; hyperbolic/
  well-posedness ANALYSIS is allowed as technique, GR FORM-import is not.)

## 4. Outcome classes (all first-class; pre-committed)

- **OT-COLLAPSE** — time-live consistency cuts the `a`-analog to a point or a discrete set.
  This is Charles's hypothesis confirmed and the strongest structural result. It would mean
  the angular-modulation weight is FIXED by time-live consistency (a new constraint the
  stationary branch could not see).
- **OT-SURVIVE** — the `a`-analog persists as a genuine free family time-live. The freedom
  is not a stationarity artifact; selecting it needs something else (the angular-live route,
  a deeper principle, or an observational anchor). A clean null, equally first-class.
- **OT-REFRAME** — the `N`/`R` split does not survive; `a` is not the right variable
  time-live; the time-live depth cocycle has a different structure whose freedom (if any)
  must be re-characterized. First-class; possibly the most informative.
- **OT-MIXED** — different branches/strata give different answers; report per stratum.

## 5. Named temptation and falsifiers (hypothesis discipline)

- F-STEER (primary): Charles WANTS OT-COLLAPSE. That is the owner-pleasing direction. Any
  step selected or phrased to make time-live "fix `a`" fires this. The verifier attacks
  OT-COLLAPSE hardest; OT-SURVIVE and OT-REFRAME must be given equal derivational care.
- F-IMPORT: any GR/ADM foliation or SR four-vector smuggled as the native construction
  (Principle 7). Fires -> leg void.
- F-STATIONARY-RESIDUE: any residual use of a Killing norm / stationarity after it was
  declared dropped. Fires -> leg void.
- F-SCOPE: every claim carries its branch/stratum/regularity/supplied-structure stamps; a
  time-live result on one integrable branch is not the general theorem.
- F-SYMBOLIC: exact algebra; failures recorded as-is.

## 6. Method and verification gate

1. This preregistration committed first (frozen contract).
2. Derivation (next step, exact-symbolic where possible; a bounded explicit time-live
   comparison arrow with genuine evolution between endpoints, riding the banked `C_A`
   machinery): recompute `delta_t`, test the decomposition, compute the time-loop holonomy.
3. **VERIFICATION — cold/different-method required, not same-session.** The 2026-08-01 P4
   cold review is the controlling lesson: a same-session verifier passed a load-bearing
   error (the K4/U(1) identification) that a genuinely independent, different-method review
   caught. Therefore any result of this probe is UNBANKED until it survives a verifier that
   imports none of this probe's or the orchestra's producer code and recomputes the depth
   extractor and holonomy by a different route. Same-session checks are labeled regression/
   parser checks only.
4. AUDIT_REPORT + scope stamps before any bank; LIVE.md pointer only on a banked result.

## 7. Ceiling (pre-committed)

The strongest bankable statement is "on [branch/stratum], the time-live depth cocycle's
angular-modulation freedom is [collapsed to X / free / ill-posed] by [derivation], with
[holonomy/consistency] as the operative constraint" — scoped to the branch, no general
theorem claimed from one branch, no mass claim, no law selected, no physics. This probe
seeks STRUCTURE AND CONSTRAINTS on the cocycle, per Charles's intent, not closure.
