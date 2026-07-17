# Reverse-engineering the deeper UDT postulate — MAP

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | MAP / analytic reverse derivation; DATA-BLIND |
| Repository | grok at 64af120; unrelated dirt preserved |
| Driver | DISCLOSED NON-COLD; the reciprocal metric and action no-go results are known |
| User direction | Seek a logical SR/GR-like principle beneath positional dilation |
| Adoption authority | No candidate is adopted; owner verdict and independent verification required |
| GPU | Not used or requested |

## 0. Question

Work backward from

$$
ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2
$$

and identify the smallest lay-language principle that:

1. does not merely repeat “clocks and rods dilate reciprocally”;
2. independently forces the exponential reciprocal form;
3. resembles the epistemic structure of SR/GR principles;
4. has consequences beyond the one metric formula;
5. does not pretend to derive dynamics if it supplies only kinematics.

## 1. Candidate census frozen before formal derivation

### C1 — positional relativity only

No observational position is privileged; comparisons depend only on relative positional depth,
compose, and reverse.

### C2 — invariant light speed only

Every local observer measures the same $c$.

### C3 — reciprocal clock/ruler statement

Any loss of clock rate is exactly balanced by radial ruler dilation.

### C4 — invariant causal measure

Changes of observational position are reversible, composable relativity transformations that may
redistribute temporal and radial calibration but preserve the local oriented radial spacetime
measure. In the spherical areal sector this also preserves the metric four-volume.

Lay version:

> Position may redistribute how much interval is read as time and how much as radial distance, but
> it cannot create or destroy their combined local spacetime capacity.

### C5 — invariant-distortion dynamics

Physical histories extremize a quadratic invariant strain of those measure-preserving positional
transformations.

C5 is listed separately because an extremization rule is stronger than a kinematic invariance.

## 2. Formal test frame

Use a positive diagonal adapted radial metric

$$
ds^2=-T(\Delta)^2c^2dt^2+R(\Delta)^2dr^2+r^2d\Omega^2,
$$

where $\Delta$ is additive relative positional depth and $T(0)=R(0)=1$.

Test:

$$
T(\Delta_1+\Delta_2)=T(\Delta_1)T(\Delta_2),
$$

$$
R(\Delta_1+\Delta_2)=R(\Delta_1)R(\Delta_2),
$$

with continuity/regularity and reversible comparisons.

For C4, impose the geometric volume-form statement in the adapted areal sector:

$$
T(\Delta)R(\Delta)=1.
$$

## 3. Predeclared gates

### G1 — metric forcing

PASS only if a candidate forces both exponential composition and reciprocal exponents, up to a
conventional normalization of depth.

### G2 — non-restatement

PASS only if the candidate can be stated operationally without naming the desired metric
coefficients.

### G3 — coordinate/gauge audit

Determine whether $TR=1$ is:

- an invariant relation to a declared reference volume form;
- a residual coordinate gauge;
- or a physical restriction only after areal radius and clock normalization are fixed.

Do not call a coordinate determinant by itself a physical conservation law.

### G4 — independent consequences

Require at least two consequences beyond rewriting the metric, such as:

- fixed metric volume form;
- traceless allowed reciprocal variations;
- a definite source combination under constrained variation;
- an invariant group current/norm;
- a falsifiable failure mode when transverse or time-live sectors are added.

### G5 — dynamics

Test whether C4 selects a unique action. One allowed nonlinear invariant action defeats that claim.
C5 must not be smuggled into C4.

### G6 — global reach

Determine whether the candidate derives the universal scale $X$ or the WR-L profile
$A=1-r/X$. Kinematic reciprocity alone is not allowed to claim the wall selector.

## 4. Required exact derivations

1. Solve the continuous composition equations for $T$ and $R$.
2. Apply C4 and recover the reciprocal metric.
3. Compute the radial determinant and four-volume form.
4. Express the infinitesimal transformation as a determinant-one matrix and compute its invariant
   quadratic trace norm.
5. Compute the tangent metric variation and its trace.
6. Derive the source selected by reciprocal tangent variation in a generic diagonal stress tensor.
7. Exhibit nonlinear invariant action counterfamilies if dynamics remains unselected.
8. Test C1–C5 against G1–G6 and rank them.

## 5. Stop rules

- Do not infer C4 merely because the metric already has $TR=1$; record it as a reverse-engineered
  candidate until independent consequences and alternatives are tested.
- Do not import Lorentz transformations, GR field equations, or unimodular dynamics as UDT
  derivations.
- Do not infer matter emergence, $S^2$, mass, $X$, or WR-L wall behavior from local volume
  preservation alone.
- Do not call the invariant trace norm an action without an extremization premise.
- No postulate is adopted in this artifact.

## 6. Deliverables

- UDT_DEEP_POSITIONAL_RELATIVITY_POSTULATE_DERIVATION_RESULTS.md
- verify_udt_deep_positional_relativity.py
- verify_udt_deep_positional_relativity_out.txt
- UDT_DEEP_POSITIONAL_RELATIVITY_POSTULATE_VERIFY_DISPATCH.md

