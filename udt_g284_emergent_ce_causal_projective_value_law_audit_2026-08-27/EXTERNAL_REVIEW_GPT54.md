# G284 Fresh External Adversarial Review

Primary verdict: `ACCEPT-WITH-REPAIRS`

Bounded scientific landing survives unchanged: `YES`

Accepted bounded landing:

```text
EMERGENT_CE_CAUSAL_PROJECTIVE_NETWORK_RECONSTRUCTS_BUT_DOES_NOT_SELECT_TIDAL_HISTORY
```

## 1. Packaging and seal audit

I verified the detached manifest seal at `/intake/REVIEW_MANIFEST.sha256` against
`/intake/REVIEW_MANIFEST.tsv`. The SHA-256 matched exactly. The manifest contains 37 payload rows,
and all 37 recorded byte counts and SHA-256 payload hashes matched the sealed intake contents. The
outer intake tree contains 39 files total. A full tree walk found no symlinks.

Result: `PASS`

## 2. Registered-command replay in ephemeral copy

Replay root: `/work/g284_replay_1787865379`

I ran the five registered commands from
[COMMANDS.md](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/COMMANDS.md:1).

1. `python3 .../verify_preregistration.py`
Exit code: `0`
Type: saved-artifact/source-seal checking
Observed result: `PASS: G284 preregistration; sources=15 premises=16`

2. `python3 .../derive_causal_projective.py`
Exit code: `1`
Type: recomputation
Observed result: `ModuleNotFoundError: No module named 'sympy'`

3. `python3 .../verify_independent.py`
Exit code: `0`
Type: recomputation
Observed result: independent exact/numerical verification passed; 512 exact cases, 7,168 exact
assertions, 64 network cases, maximum symplectic residual `5.11e-15`, maximum composition residual
`7.23e-13`, maximum reversal residual `1.04e-14`

4. `python3 .../run_catch_proofs.py`
Exit code: `0`
Type: recomputation
Observed result: 9/9 in-memory claim-schema catches passed

5. `python3 .../verify_package.py`
Exit code: `0`
Type: saved-artifact checking
Observed result: internal package check passed as a consistency check over sealed JSON and text
artifacts

Replay conclusion: 4/5 registered commands exited successfully in this environment. The only failed
registered replay was the symbolic derivation, and it failed before recomputation because the
runtime dependency `sympy` was unavailable.

## 3. Scientific audit

### Coordinate conversion and central invariants

The coordinate change

\[
u=(c_E t-z)/\sqrt{2},\qquad v=(c_E t+z)/\sqrt{2}
\]

is correct. On the central ray `x=y=0`, the family

\[
g_T=-2\,du\,dv+dx^2+dy^2-x^iT_{ij}(u)x^j\,du^2
\]

reduces exactly to

\[
-c_E^2 dt^2+dz^2+dx^2+dy^2,
\]

so the central longitudinal null slopes are `dz/dt=+/-c_E`. Because `g_uu=-x^iT_{ij}x^j` is
quadratic in `(x,y)`, the central metric and all first derivatives of the metric are independent of
`T`; therefore the central connection also vanishes there. The central frequency quantity
`-g(U,k)=1/sqrt(2)` with `U=(∂u+∂v)/sqrt(2)` and `k=∂u` is `T`-independent, so the bounded central
claims `r=1`, `delta=0`, `chi=0`, and `M=1` are consistent.

Result: `PASS`

### Neighboring-null construction and signs

For the chosen neighboring null branch `k_T=∂u+a_T∂v`, nullness gives

\[
0=g(k_T,k_T)=-Q_T-2a_T,
\qquad
a_T=-Q_T/2=-x^iT_{ij}x^j/2.
\]

Differentiating twice in the transverse coordinates yields

\[
\partial_i\partial_j a_T=-T_{ij},
\qquad
T_{ij}=-\partial_i\partial_j a_T.
\]

This matches the same `T_{ij}` that appears in the Jacobi equation `D''+T(u)D=0`. In this
Brinkmann gauge one also has `Gamma^i_{uu}=T_{ij}x^j`, hence
`R^i_{u j u}|_{x=y=0}=T_{ij}` and equivalently `R_{uiuj}=T_{ij}` in the sign convention used in
[EXACT_DERIVATION.md](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/EXACT_DERIVATION.md:57).

I found no missing factor, sign flip, or omitted derivative in the scoped derivation. The only
caveat is one of interpretation: `a_null` is a coordinate coefficient in the chosen adapted gauge,
so the Hessian formula should be read as a bounded gauge-fixed reconstruction statement, not as a
new coordinate-free observable by itself.

Result: `PASS`

### Nonselection inference and active premises

Within the stated witness class of a sufficiently small causally convex tube and finite
path-labelled transport, I found no active frozen premise that rejects an arbitrary smooth
symmetric `T`. The reasons are coherent and source-bounded:

- local causal convexity is a standard local smooth-Lorentz fact and does not select `T`;
- the Hamiltonian Jacobi generator `A_T=[[0,I],[-T,0]]` is symplectic for every symmetric `T`, so
  reversal and composition remain available for arbitrary `T`;
- G274 explicitly preserves path-labelled frame carry rather than replacing it with endpoint-only
  or path-independent composition;
- G280 explicitly separates W5 projective state from Jacobi area;
- [PREMISE_LEDGER.tsv](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/PREMISE_LEDGER.tsv:15)
  and
  [PREREGISTRATION.md](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/PREREGISTRATION.md:77)
  keep endpoint-only laws, path independence, zero holonomy, all-germ isotropy, and curvature
  residuals out of the tested conjunction.

So the nonselection conclusion is supported on the bounded witness arena. It is not a global no-go
theorem.

Result: `PASS`

### Homothety separator and G276 boundary

The positive homothety argument is sound. Replacing `g_T` by `lambda^2 g_T` preserves null cones
and the Levi-Civita connection, and it leaves the dimensionless central/projective quantities
unchanged. This does not attach an absolute scale. G276 remains controlling: fixed `c_E` plus the
causal/projective network still requires an independent proper-clock datum to determine one scale.

Result: `PASS`

### Scope discipline

The scoped witness is local and bounded, not global. The current prose mostly respects that limit.
[AUDIT_REPORT.md](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/AUDIT_REPORT.md:68)
and
[EXACT_DERIVATION.md](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/EXACT_DERIVATION.md:106)
explicitly preserve the bounded scope. I found no scoped scientific overstatement that would force
rejection.

Result: `PASS`

### Missing mathematical type

The narrowing to “a nonidentity relationship between longitudinal reciprocal/projective variation
and transverse second cone variation” is defensible only as a type-level provisional inference. The
intake handles that correctly: [STATUS_LEDGER.tsv](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/STATUS_LEDGER.tsv:9)
marks it `PROVISIONAL_INFERENCE`, and
[EXACT_DERIVATION.md](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/EXACT_DERIVATION.md:135)
states that G284 derives the mathematical type but not a formula. That is acceptable.

Result: `PASS`

### Scope exclusions

I found no promotion of infinite bare `c` into observable signalling and no use of a field
equation, action, source, matter model, observation, fit, transfer law, operational distance,
absolute scale, history selection, population, or `X_max`. This exclusion is consistent across the
frozen preregistration, premise ledger, and audit report.

Result: `PASS`

## 4. Defects

### Defect 1

Class: `packaging`

The registered symbolic derivation command is not self-contained in the replay environment because
the intake declares no dependency mechanism, yet
[derive_causal_projective.py](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/derive_causal_projective.py:8)
imports `sympy`. The command is registered as a plain `python3` invocation in
[COMMANDS.md](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/COMMANDS.md:7),
but the package contains no requirements file, installer, or runtime note. In this review
environment that command exits `1` before any symbolic recomputation.

Repair required: declare and ship the runtime dependency path needed for the registered replay, or
replace the command with a dependency-free verifier.

### Defect 2

Class: `evidential`

[verify_package.py](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_package.py:40)
passes by reading the saved `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`, and
`CATCH_PROOF_RESULT.json` artifacts, then checking their contents
([verify_package.py](/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_package.py:92)).
It does not rerun the registered recomputation commands. As a result, the package can report a
passing internal verification even when the official derivation replay fails in the same
environment. That is an evidence-robustness gap, not a scientific contradiction.

Repair required: either make `verify_package.py` explicitly a sealed-artifact integrity checker and
stop presenting it as replay evidence, or extend it to fail when the registered recomputations
cannot actually be rerun in the declared environment.

## 5. Final decision

Scientific classification:

- `scientific defects`: none found within the bounded witness and frozen source universe
- `evidential defects`: one
- `packaging defects`: one
- `wording defects`: none requiring repair

Primary verdict: `ACCEPT-WITH-REPAIRS`

Why: the bounded mathematical landing is supported. The coordinate conversion, central invariants,
neighboring-null Hessian reconstruction, nonselection argument, homothety separator, and scope
discipline all hold as stated on the fixed local arbitrary-`T` witness. The package still needs
repair before banking because one registered recomputation command is not replayable in the current
environment and the package verifier can pass without proving full rerun reproducibility.
