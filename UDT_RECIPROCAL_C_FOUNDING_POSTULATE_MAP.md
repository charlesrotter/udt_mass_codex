# Reciprocal-c founding postulate — derivation MAP

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Origin | Charles Rotter: “c is a reciprocal identity of time and length—not a one-way speed” |
| Mode | Analytic derivation and circularity audit; DATA-BLIND |
| Repository | `grok` at `64af120`; unrelated dirt preserved |
| Adoption | User-proposed foundational postulate; mathematical reach not pre-accepted |
| GPU | Not used or requested |

## 0. Question

Determine whether the following user-originated postulate, together with the UDT Reciprocity
Principle, genuinely sits upstream of positional dilation:

> **Reciprocal-c Identity.** The universal constant $c$ is the reversible identity between temporal
> and spatial measure. Its two directions,
> $L=cT$ and $T=L/c$, are equally fundamental and are respected by every positional comparison.

Test whether this derives, rather than assumes,

$$
ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2,
$$

and then determine whether it selects a dynamical action or the scale $X$.

## 1. Formalizations frozen before calculation

Let the dimension-matched radial coframe pair be

$$
q=\begin{pmatrix}c\,dt\\dr\end{pmatrix}.
$$

A continuous positional comparison at additive depth $\Delta$ acts diagonally:

$$
P(\Delta)=\operatorname{diag}(u(\Delta),v(\Delta)),
\qquad u,v>0.
$$

The two meanings below must not be conflated.

### F1 — conversion-map covariance only

Treat $c:\mathcal T\to\mathcal L$ as an isomorphism and require the positional maps to commute with
it. In one dimension this gives equal representations on time and length.

### F2 — reciprocal duality

Treat the two directions $c$ and $c^{-1}$ as a dual pair, and interpret the UDT Reciprocity
Principle as requiring positional transformations to act contragrediently on the two sides. The
dimensionless evaluation pairing is preserved.

In the coframe basis this pairing may be represented by

$$
K=\begin{pmatrix}0&1\\1&0\end{pmatrix},
$$

and Reciprocity requires

$$
P(\Delta)^T K P(\Delta)=K.
$$

This is an operational time-length duality statement, not yet a metric equation.

## 2. Other declared premises

### P1 — positional relativity

Only relative depth matters; comparisons compose and reverse:

$$
P(\Delta_1+\Delta_2)=P(\Delta_1)P(\Delta_2),
\qquad
P(-\Delta)=P(\Delta)^{-1}.
$$

Assume continuity or measurability sufficient to exclude pathological Cauchy solutions.

### P2 — nontriviality

At least one positional comparison is not the identity. This is to be tagged as empirical or as a
separate founding premise; it must not be derived from group composition.

### P3 — local metric readout

Use the local Lorentzian interval in the dimension-matched physical coframe,

$$
ds^2=-(q'^0)^2+(q'^1)^2+r^2d\Omega^2,
\qquad q'=Pq,
$$

with spherical areal $r$. This is declared SR-continuity/local metric structure. The reciprocal-c
postulate by itself supplies a time-length conversion and null structure, not the quadratic
Lorentzian signature or angular sector.

## 3. Predeclared gates

### G1 — circularity

PASS only if the derivation states exactly where $v=u^{-1}$ enters. If it is simply the formal
meaning assigned to Reciprocity, tag it as postulated structural content rather than a theorem of
$c$ alone.

### G2 — competing formalization

Compute F1. If F1 gives $v=u$, record that reciprocal-c identity alone does not force the UDT
metric.

### G3 — metric derivation

Under F2 plus P1–P3, solve for $u,v$ and recover the reciprocal exponential metric up to sign and
normalization of $\phi$.

### G4 — nontrivial branch

Check whether $u=v=1$ remains a solution.

### G5 — independent consequences

Derive the positional group, determinant, volume form, generator, reversal invariant, and tangent
norm without importing field equations.

### G6 — action selection

Test whether the premises select $F(Y)=Y$ over nonlinear $F(Y)$. One valid counteraction defeats
uniqueness.

### G7 — role of $X$

Determine whether $X$ occurs in the local postulates or follows from their equations. Distinguish a
local action parameter, solution integration constant, and global boundary datum.

## 4. Required outputs

1. Exact implication of F1.
2. Exact implication of F2.
3. Continuous representation theorem and metric.
4. Complete assumption ledger.
5. Action counterfamily or action selector.
6. Explicit verdict on whether $X$ must be postulated now.
7. Symbolic verifier and cold workstation dispatch.

## 5. Stop rules

- Do not claim that the arithmetic existence of $1/c$ alone derives reciprocal dilation.
- Do not call the metric derived from only two premises if local metric readout, continuity, or
  nontriviality is also required.
- Do not import GR field equations or an EH action as UDT derivations.
- Do not infer matter emergence or an $S^2$ carrier from the kinematic group.
- Do not postulate $X$ merely because the local kinematic derivation does not contain it.
- Do not alter `LIVE.md` or `CANON.md` or bank the result without independent verification and the
  owner's explicit verdict.

