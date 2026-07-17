# DISPATCH — independent verification of the WR-L solution-space closure lead

## Mission

Independently verify or falsify the action-independent WR-L endpoint/operator derivation, then
adversarially test whether its inverse minimum functional has any forced UDT-native provenance.

Do not bank a conclusion, edit `LIVE.md` or `CANON.md`, start F/G, or merge the macro and particle
lanes.  One evidence-only commit is permitted only after every generated source, raw output, and
machine-readable result is present.

## Repository synchronization

Do not trust a hash in this dispatch.  Begin with:

```bash
git checkout grok
git fetch origin
git pull --ff-only origin grok
git status --short --branch
git log -8 --oneline
```

Preserve all unrelated dirty files.

## Read order and arm isolation

### Arm A — cold re-derivation

Give Arm A only:

1. `UDT_WRL_SOLUTION_SPACE_CLOSURE_MAP.md`
2. `UDT_METHOD_MUSIC.md`
3. `UDT_DOTTED_LINE.md`
4. `UDT_ELEGANCE_UNCOVER.md`
5. `SIMPLE_METRIC_MACRO.md`
6. `simple_metric_L_wall_regularity_closure_results.md`
7. `simple_metric_WR_L_center_recenter_exclusion_results.md`
8. `simple_metric_WR_L_center_nogo_atlas_results.md`
9. `simple_metric_angular_on_L_multipole_results.md`

Do not give Arm A the derivation results, verifier code, or this dispatch's expected numerical
constants beyond those already frozen in the MAP.

### Arm B — adversarial audit

Arm B may read everything, including:

- `UDT_WRL_SOLUTION_SPACE_CLOSURE_DERIVATION_RESULTS.md`
- `verify_udt_wrl_solution_space_closure.py`
- `verify_udt_wrl_solution_space_closure_out.txt`
- the current action/boundary derivation files;
- all historical negative registries needed to detect a repeated failed operator.

Arm B must look for hidden GR equations, variation-space changes, endpoint-term loss, spectrum
overclaims, and inverse-variational nonuniqueness.

## Binding UDT rules

- The metric is the theory.
- Use no GR field equation as a UDT derivation.  Standard geometry may be used as readout or tensor
  algebra only.
- Use no EH premise, carrier, Standard Model mechanism, quantum rule, fluid, fit, cutoff, effective
  correction, or invented coupling.
- Keep `DERIVED`, `CHOSE`, `WORKING`, `OPEN`, `CONDITIONAL`, `POSIT`, and `OBSERVED` distinct.
- Retain the full nonlinear metric.
- A coordinate horizon is not a curvature boundary without proof.
- A raw geometric flux is not a mass charge without a derived generator and normalization.
- An on-shell inverse functional is not a native action without off-shell provenance.

## Phase V1 — exact independent checks

For

\[
A=1-r/X,
\qquad N=\sqrt A,
\]

recompute from scratch:

1. proper radius, optical radius, static-patch volume, and the proper-coordinate profile (r(s));
2. (R), ({}^{(3)}R), the Kretschmann scalar, their center/wall limits, and the three integrated
   curvature quantities reported in the result;
3. a regular ingoing-null coordinate chart and the existence or nonexistence of null and timelike
   crossing curves at (r=X);
4. the exact identity
   \[
   D^2N=-\frac{N}{Xr}=-\frac{{}^{(3)}R}{4}N=-\frac R6N;
   \]
5. the raw spherical flux (Phi_N(r)), its wall value, and whether it is radius-independent;
6. the (A^p) flux threshold at (p=1/2);
7. the general solution of
   \[
   r^2A''+rA'-A+1=0;
   \]
8. the Euler equation, square completion, lower bound, and (X)-independence of
   \[
   \mathcal I[A]=\frac12\int_0^X\left[r(A')^2+\frac{(A-1)^2}{r}\right]dr;
   \]
9. the reciprocal reduced variation of
   \[
   \mathcal J[N;\gamma]
   =\frac12\int[(DN)^2-{}^{(3)}RN^2/4]dV,
   \qquad \gamma_{rr}=N^{-2};
   \]
10. the spacetime scalar radial operator, tortoise potential, static multipole endpoint identity,
    lapse-mode norms, and the distinct spatial Laplace-Beltrami operator;
11. the homothetic (x=r/X, \tau=ct/X) scaling and absence or presence of a native mass variable.

Use an independently written CAS script.  Record exact expressions before floating evaluation.

## Phase V2 — adversarial provenance test

The strongest lead is the inverse functional (mathcal I[A]).  Try to kill it before promoting it.

### P1 — inverse-variational nonuniqueness

Find explicit inequivalent local functionals, if they exist, that have WR-L as an extremal or have
the same ODE.  Quotient only by a fully displayed nonzero overall constant and a displayed total
derivative.  If field-dependent integrating multipliers or different off-shell equations survive,
report them as counterexamples to uniqueness.

### P2 — off-shell residual re-centering

Derive the transformation of (mathcal I[A]) under

\[
A_R(s)=\frac{A(R+s)}{A(R)}.
\]

Test the full off-shell functional, not only the WR-L solution.  An on-shell form-invariance is not
enough.

### P3 — geometric parent

Search for a local covariant or explicitly UDT-foliated functional whose declared independent
fields and consistent variation reduce to the WR-L ODE.  Do not hold (gamma) fixed if reciprocity
makes it a function of (N).  State every extra field, derivative-order, boundary, and foliation
premise.  Failure to find a parent is an honest negative, not permission to use (mathcal I) as law.

### P4 — endpoint ontology

Determine whether the metric itself makes (X) invariantly unreachable or only unreachable in the
static (t) chart.  If a regular causal crossing exists, identify the minimum additional axiom
needed to make (X) a terminal universal distance.

### P5 — spectral rigor

Check the endpoint classification of both scalar operators.  Report separately:

- static zero modes;
- time-live essential/point spectrum under each stated center domain;
- spatial-slice self-adjoint extensions;
- what changes under causal continuation, terminal boundary, and reflection/gluing.

Do not call a discrete spectrum metric-derived if a Robin parameter or reflecting wall was chosen.

## Predeclared verdict rules

### Algebra pass

PASS only if both arms reproduce every decisive formula or document a corrected formula that leaves
the logical verdict unchanged.  Any sign, endpoint, or norm discrepancy must be resolved explicitly.

### Native-action promotion

Do **not** promote unless:

1. one off-shell functional class is forced by named UDT premises;
2. its independent fields and variation domain are fixed;
3. the WR-L ODE follows without inverse fitting;
4. the boundary primitive and charge normalization are fixed;
5. no inequivalent allowed counterfunctional survives.

If any item fails, retain **PROVISIONAL ANALYTIC LEAD / ACTION OPEN**.

### Compactness/matter promotion

Do **not** claim a native mass, compactness, or matter carrier unless those objects occur in the
derived operator and normalization.  A finite lapse flux or normalizable lapse zero mode alone is
insufficient.

## Required artifacts

Create a dated evidence directory containing:

1. Arm A derivation, CAS source, raw output, and compact JSON;
2. Arm B adversarial report, counterexample sources, raw output, and compact JSON;
3. exact environment and repository manifest with SHA-256 hashes;
4. a consistency checker comparing every duplicated formula;
5. a final evidence report with one row per Phase V1/V2 item and explicit gate booleans.

The final console report must include:

- checker verdict;
- algebra pass/fail;
- native-action promotion gate pass/fail;
- causal-unattainability verdict;
- compactness/matter promotion gate pass/fail;
- all discrepancies;
- `git status --short --branch` and `git log -5 --oneline`.

No GPU run is requested.  Stop after the evidence package and await Charles's verdict.
