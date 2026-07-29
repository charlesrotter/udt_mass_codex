# CORRECTION LAYER — gate (d) stratum remainder (append-only)

Date: 2026-07-28. Source: blind adversarial verifier (required documentation amendment),
applied before banking. No computation in the package was wrong; the theorem, the c=1 ⇔
swap-isometry dichotomy, and the "middle class EMPTY" synthesis all STAND. The amendment
closes a proof-RECORD gap in the necessity argument.

## C1 (required) — the unstated constant-combination lemma

§4(A) claimed necessity "topology-only; no assumption on the isometry algebra," but the step
"`Φ_*` maps the Killing lattice to itself" holds automatically only when the torus is
conjugation-stable; in a strictly larger isometry group it needs a lemma. The verifier
DERIVED the missing lemma and machine-checked it (4/4 stages; script preserved in-package as
`VERIFIER_LEMMA_B1.py` + `VERIFIER_LEMMA_B1_STDOUT.txt`, re-run exit 0): any Killing field
pointwise tangent to `span(K,Y)` on an `alpha=0` stratum member is a constant combination
`aK + bY` (pointwise separation closes all derivative terms incl. the `f = ±c` corners;
constant-depth escapees closed by torus single-valuedness). §4(A) is amended in place
(visible in git) to state the lemma and route the proof through it. The verifier's first
pointwise-jet probe FAILED by design — the lemma is not a pointwise linear-algebra fact —
which is exactly why it must be stated rather than waved at.

## C2 (required) — "lattice injectivity" → freeness

§4(A) said injectivity forces `Φ_*Y = ±V`; injectivity alone does not (`εV + nY` is
injectivity-compatible for any n). The operative fact is the two-free-lines FREENESS theorem:
`|ε+n| = |ε−n| = 1` forces `n = 0`. Wording corrected in place.

## C3 (required) — one-directional inequivalence scope note

The contrapositive "isometrically inequivalent at c ≠ 1" is fully proven in the two-sided
plane-swap reading. The one-directional strengthening is proven whenever `sup u < ∞` or
`inf u > 0`; the residual corner (principal-orbit-only members with strictly larger isometry
algebra and depth range all of `(0,∞)`) is OPEN and carried as a scope note. No conclusion in
the package rides it: selection at `c ≠ 1` uses the pointwise norm ratio, not the
inequivalence claim. JSON field `T_d4.necessity` carries this reading (generated JSON not
hand-edited).
