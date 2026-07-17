# Workstation dispatch — cold verification of the deeper positional postulate candidate

## Scope

Independently audit the reverse derivation in:

- `UDT_DEEP_POSITIONAL_RELATIVITY_POSTULATE_MAP.md`
- `UDT_DEEP_POSITIONAL_RELATIVITY_POSTULATE_DERIVATION_RESULTS.md`
- `verify_udt_deep_positional_relativity.py`
- `verify_udt_deep_positional_relativity_out.txt`

Do not adopt a postulate, alter `LIVE.md` or `CANON.md`, begin F/G, or import GR field equations.
This dispatch asks whether the candidate is logically valid and genuinely deeper than restating the
metric.

## Candidate under test

> Observational positions are related by reversible, composable transformations. A positional
> transformation may redistribute temporal and radial calibration, but it preserves their local
> oriented spacetime measure.

## Required independent checks

### 1. Composition theorem

Starting without the supplied algebra, determine whether continuous positive factors satisfying

$$
T(x+y)=T(x)T(y),
\qquad
R(x+y)=R(x)R(y)
$$

must be exponentials. State all regularity assumptions and identify pathological alternatives if
continuity/measurability is omitted.

### 2. Measure implication

Audit whether preservation of the oriented radial spacetime measure really gives $TR=1$ and hence
opposite exponents. Separate:

- tetrad/coframe determinant;
- metric determinant;
- equality to an operational reference volume form;
- coordinate gauge.

### 3. Gauge adversary

Start from

$$
ds^2=-C(r)c^2dt^2+D(r)dr^2+r^2d\Omega^2.
$$

Determine exactly which coordinate transformations remain after areal $r$ and a reference clock
normalization are fixed. Decide whether $CD=1$ is then physical, gauge, or partly conventional.
Try to defeat the claim.

### 4. Independent consequences

Recompute from scratch:

$$
S(\phi)=\operatorname{diag}(e^{-\phi},e^{\phi}),
\qquad
\frac12\operatorname{Tr}(S^{-1}dS)^2=d\phi^2,
$$

the trace of $\delta g$, $\delta\sqrt{-g}$, and—only as a conditional metric-coupling
readout—the stress combination selected by $T^{\mu\nu}\delta g_{\mu\nu}$.

Audit signs and conventions. Do not promote the conditional stress readout to native UDT physics.

### 5. Counterexample search

Find explicit alternatives that obey positional composition, reversal, and measure preservation
but differ in:

- radial profile $A(r)$;
- action $F(Y)$;
- full time-live or nonspherical extension.

One valid counterexample defeats any uniqueness claim.

### 6. Candidate comparison

Evaluate independently whether:

1. positional relativity alone;
2. invariant local $c$ alone;
3. reciprocal dilation as a direct postulate;
4. positional relativity plus causal-measure preservation;

forces the reciprocal metric. Rank each as DERIVED, INSUFFICIENT, RESTATEMENT, or VIABLE CANDIDATE.

### 7. Nontrivial-branch gate

Check the claim that the candidate also permits $T=R=1$. Determine the smallest additional
empirical or logical premise that selects nonzero positional dilation without assuming the desired
WR-L profile.

## Required report

Return:

1. PASS/FAIL for every numbered check;
2. corrected equations for every failure;
3. a list of hidden assumptions;
4. the strongest explicit counterexample found;
5. one of these final verdicts:
   - **REJECTED**;
   - **VIABLE KINEMATIC CANDIDATE, NOT DYNAMICS**;
   - **FORCES RECIPROCAL METRIC UNDER STATED PREMISES**;
   - **STRONGER RESULT**, with exact proof;
6. a separate statement of whether a unique native action follows.

Raw scripts and raw output must be retained. Stop after the verification report; do not bank a
physics conclusion without the owner's verdict.

