# Running-Rate Absorbability — BLIND ADVERSARIAL VERIFIER pass

Agent: general-purpose (verifier, driver-delegated) | Date: 2026-06-18
MODE: **blind adversarial verifier** — independent sympy derivation done BEFORE
reading constructor scripts/doc. Goal was to REFUTE the absorbability claim and
vindicate Charles. Tools: my own from-scratch sympy (`/tmp/verif_*.py`), then
cross-read of `udt_field_equation_running_rate_results.md` +
`running_rate_*.py`. NOT canon. Do NOT git commit (per instructions).

Claim under test (constructor verdict (iii), load-bearing):
> The running coupling `kappa(phi)=kappa0 e^{8phi}` on the SOURCE is ABSORBABLE.
> Define `T~=e^{8phi}T`; then `G=kappa0 T~` is ordinary GR with constant coupling,
> and `nabla^mu T~=0` exactly. So running-rate ALONE is not a physical departure
> from GR; the only non-absorbable fingerprint is the matter exponent `a`.
> Verdict DEPENDS-on-a, NOT physical.

---

## VERDICT: **CONFIRMED** (with one sharpening, below)

The absorbability claim survives a hard adversarial pass. I built the geometry,
the abstract divergence identity, and the chart-level conservation check from
scratch and could NOT construct any invariant that distinguishes "bare-T physical"
from "T~ physical." The running coupling, taken alone, genuinely relabels back to
GR. The physical departure lives entirely in the matter-coupling exponent `a`.

I attacked it four ways; all four failed to refute.

---

## ATTACK 1 — the divergence identity (independent re-derivation)

Pure Leibniz + metric-compatibility, for an **arbitrary symmetric T_munu**:
```
nabla^mu(e^{8phi} T_munu) = e^{8phi}[ nabla^mu T_munu + 8 (partial^mu phi) T_munu ]
=> nabla^mu T~ = 0  <=>  nabla^mu T_munu = -8 (partial^mu phi) T_munu.
```
This is an algebraic identity. It is **NOT** restricted to perfect fluids,
isotropy, or staticity — I checked the structure abstractly; the product rule
does not care about the form of T. So the constructor's "general T" claim holds.

**Deeper point (the one that makes refutation hopeless):** Bianchi gives
`nabla^mu G_munu = 0` IDENTICALLY (geometry). The moment you write the standard
`G_munu` on the left and set `G = kappa0 T~`, the object `T~ := G/kappa0` is
conserved **by construction** — a tautology of Bianchi, for ANY source. So the
"is T~ conserved?" question can never come back negative within this frame. The
absorption's conservation half is forced, not lucky. CONFIRMED, and it is
robust to non-perfect-fluid / anisotropic / time-dependent T.

Chart spot-check (my own sympy, static diagonal `T^a_b=diag(-rho,p_r,p_t,p_t)`):
substituting the UDT on-shell relation `nabla_a T^a_r = -8 phi' p_r` into
`nabla_a(e^{8phi}T)^a_r` gives **exactly 0**. Reproduces constructor Task 3.

---

## ATTACK 2 — the interpretation crux (the real make-or-break)

I tried hardest here, because this is where a departure could hide. Result: I
could not build a distinguishing invariant. Reasoning:

- Curvature invariants (R, R_munu R^munu, Kretschmann) are functionals of the
  metric `g` ONLY. Both readings use the SAME `g`. They are identically equal.
  My sympy R = `2(-2r^2 phi'^2 + r^2 phi'' + 4r phi' + e^{2phi} - 1)e^{-2phi}/r^2`
  carries no trace of "8" and no trace of which T is called physical.
- Geodesics / null cones / tidal (geodesic-deviation) observables depend on `g`
  and its connection ONLY. A Cassini probe, a redshifted photon, a tidal
  measurement — none can tell reading A from reading B. The "8" never enters a
  test-particle observable.
- The ONLY physical fact that differs between the readings is the equation of
  motion of the SOURCE MATTER ITSELF: reading A's bare-T is non-conserved
  (`nabla^mu T = -8 partial^mu phi T`, a 5th-force-like exchange); reading B's
  T~ is conserved. Whether THAT is observable requires independently knowing
  "what stress-energy a real detector couples to" — which is precisely the
  matter-ruler-vs-metric-ruler exponent `a`. So the entire physical content of
  a possible departure is funneled into `a`. I confirm the constructor's
  dimensionless-ratio argument: `lambda_C/(proper ruler) ~ e^{(a-1)phi}` carries
  `a`, not `8`. **No invariant with "8" in it exists.**

I specifically looked for an energy-condition / rest-frame obstruction to
calling T~ "physical." There is none structural: `T~ = e^{8phi} T` is a positive
scalar (e^{8phi}>0) times T, so it preserves the sign structure / energy
conditions / rest frame of T. T~ is a perfectly legitimate stress tensor. So
the relabel is not blocked by any tensor-legitimacy argument.

---

## ATTACK 3 — is the "8" / e^{kphi} form escapable?

No, and this strengthens the verdict. For ANY constant k, `kappa0 e^{kphi}` on
the source with standard G on the left absorbs identically (`T~=e^{kphi}T`,
conserved by Bianchi). The value 8 is irrelevant to absorbability. So **a scalar
multiplier f(phi) on T, with standard G on the left, is NEVER a standalone
physical departure**, whatever the exponent. A departure would require a
NON-scalar coupling (a tensor `K_munu^{ab}T_ab` not reducible to f(phi)T) — but
that is NOT the e^{8phi}-on-T frame under test. Within the stated frame,
absorbability is forced for every exponent.

---

## ATTACK 4 — was GR smuggled by standard G on the left? (Principle-7 probe)

YES, in the precise sense the constructor's own premise ledger (P2) already
confesses — and this is the honest residual, not a refutation of the
absorbability claim:

- Putting the STANDARD Einstein tensor on the left makes vacuum=Ricci-flat=
  Schwarzschild BY FIAT, and predetermines both Cassini-safety AND the
  absorbability of any scalar source coupling. "Empty=GR" is here by
  CONSTRUCTION, not derived — exactly the Principle-7 SCAR.
- But this does NOT rescue the running-rate law as a physical departure; it does
  the opposite. The smuggle is what MAKES the absorption work. The constructor
  flags this honestly (ledger P2 "PRIMARY GR-LEAK", overall read).
- The alternative packaging "rate in the geometry" (f(phi)R / Brans-Dicke) gives
  vacuum != Schwarzschild and is the Cassini-dead γ=9 route. So neither clean
  scalar packaging yields a live standalone gravitational departure. A genuinely
  native left-hand-side law (non-scalar, Cassini-safe, non-relabelable) is not
  excluded in general but is unbuilt and is NOT this claim.

So the "smuggle" criticism is valid AND already on the record; it reinforces
rather than refutes verdict (iii).

---

## SHARPENING (the one nuance I add to the constructor)

The constructor calls the verdict "DEPENDS-on-a." I sharpen the LOGIC of why it
can never be otherwise within this frame: **once standard G is on the left,
Bianchi makes G/kappa0 a conserved tensor identically, so ANY source-side scalar
running is absorbable as a theorem — not a contingent fact to be re-checked per
T.** The constructor's per-chart check (correct, reproduced) is therefore
confirmatory of a structural inevitability, not the source of the result. This
makes the verdict STRONGER (frame-level), and makes clear the only escape routes
are (1) the matter exponent `a` (matter sector) or (2) abandoning standard G on
the left for a genuinely native, non-scalar, Cassini-safe curvature law
(gravity sector) — exactly the two open targets the constructor named.

---

## DISCREPANCIES WITH CONSTRUCTOR

None of substance. Every load-bearing identity reproduced independently:
- Einstein tensor components (G^t_t=G^r_r, G^th_th=G^ph_ph): MATCH.
- `Box_g phi + G^th_th = 0` exactly: MATCH (my independent sympy).
- `nabla_a(e^{8phi}T)^a_r = 0` on-shell: MATCH (my independent sympy).
- Dimensionless ratio carries `a`, not `8`: MATCH (analysis).
The doc's HONEST OVERALL READ and PREMISE LEDGER are accurate and appropriately
self-incriminating about P2. I found no rubber-stamping and no hidden import.

---

## BOTTOM LINE

CONFIRMED. The running coupling `kappa(phi)=e^{8phi}` on the source, with
standard G on the left, is genuinely absorbable: it relabels back to ordinary GR
with a conserved `T~`, by a Bianchi tautology, for arbitrary T. No
coordinate-invariant, no curvature ratio, no geodesic/tidal observable
distinguishes the two readings — I tried and failed to build one. The departure
from Einstein does NOT live in the running rate; it lives ONLY in the matter
mass-dilation exponent `a` (or in an as-yet-unbuilt non-scalar native LHS law).
Charles's physical conviction is NOT vindicated by THIS packaging — the
running-COUPLING reformulation cannot, by itself, carry the departure. It
relocates the entire question onto the standing `a` crux.

Recommend (echoing constructor): PONDER with Charles whether the honest target is
the matter `a` (matter sector) or a truly native, non-scalar left-hand-side law
(gravity sector). This push shows the scalar-running-coupling packaging is not a
third way — it is GR wearing a different label.
