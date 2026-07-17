# DISPATCH — blind verification of the quadratic dilation-cost derivation

## Mission

Independently verify whether existing UDT premises derive:

1. an invariant quadratic infinitesimal norm on dilation-depth space;
2. an exact quadratic local field action;
3. the specific WR-L inverse functional.

This is analytic CPU work. Do not run GPU numerics, edit LIVE.md/CANON.md, or adopt a new postulate.

## Synchronize

    git checkout grok
    git fetch origin
    git pull --ff-only origin grok
    git status --short --branch
    git log -8 --oneline

Preserve unrelated dirt.

## Cold arm packet

Give the cold arm only:

1. UDT_QUADRATIC_DILATION_COST_DERIVATION_MAP.md
2. UDT_METHOD_MUSIC.md
3. UDT_DOTTED_LINE.md
4. UDT_ELEGANT_FRAME.md
5. SIMPLE_METRIC_MACRO.md
6. UDT_FOUNDING_TO_DYNAMICS_MAP.md
7. UDT_MUTUAL_DILATION_RESISTANCE_MAP.md
8. UDT_WRL_OFFSHELL_PROVENANCE_MAP.md

Do not provide the quadratic-cost results, verifier source, or output until its independent
derivation is frozen.

## Adversarial arm packet

The adversary may then read:

- UDT_QUADRATIC_DILATION_COST_DERIVATION_RESULTS.md
- verify_udt_quadratic_dilation_cost.py
- verify_udt_quadratic_dilation_cost_out.txt
- UDT_MUTUAL_DILATION_RESISTANCE_DERIVATION_RESULTS.md
- UDT_WRL_OFFSHELL_PROVENANCE_DERIVATION_RESULTS.md
- all current action and variation-domain audits.

## Required independent checks

1. From additive depth and reciprocity, classify invariant one-dimensional Riemannian state metrics.
2. Transform the result exactly among $\phi$, $A=e^{-2\phi}$, and $B=1-A$.
3. Prove or refute
   $$
   \cosh\Delta\phi-1
   =\frac12[2\sinh(\Delta\phi/2)]^2.
   $$
4. Classify smooth reciprocal costs $F(\cosh\Delta\phi)$ through fourth order and provide an allowed
   cost with no quadratic term.
5. Independently derive the symmetric-kernel zero-range limit and its first nonzero error.
6. Test uniformity of that limit on WR-L as $r\to X$.
7. Exhibit or reject nonlinear local covariant actions $F(Y)$ obeying the same existing symmetries.
8. Prove the orthogonal-additivity selector theorem and audit whether orthogonal additivity is
   already a recorded UDT premise.
9. Compare the invariant depth norm directly with the flat-$B$ kinetic term in the WR-L inverse
   functional.
10. Recompute the WR-L residuals of the shift-clean radial depth action and reciprocal-reduced
    scalar kinetic action.
11. Check whether the prior $L_\lambda$ counterfamily has the same linearized equation on WR-L.

Use independently written symbolic code and preserve raw output.

## Verdict gates

- **TANGENT-NORM PASS:** the invariant state metric is uniquely $Z\,d\phi^2$ inside a clearly stated
  Riemannian class.
- **FULL-QUADRATIC-ACTION PASS:** allowed only if all nonlinear $F(Y)$ counteractions are excluded by
  an already-recorded UDT principle.
- **WR-L-ACTION PASS:** allowed only if the derived norm also supplies the radial measure,
  $(A-1)^2/r$ term, variation domain, and boundary generator.
- **NEW-PRINCIPLE REQUIRED:** if exact orthogonal additivity or equivalent input is necessary but not
  already present.

Do not collapse these four gates into one conclusion.

## Required return

Create an evidence-only package containing independent source, raw output, compact JSON, SHA-256
manifest, and a consistency checker. Report every gate, every discrepancy, git status, and the last
five commits. Stop afterward; no new physics principle and no numerics.

