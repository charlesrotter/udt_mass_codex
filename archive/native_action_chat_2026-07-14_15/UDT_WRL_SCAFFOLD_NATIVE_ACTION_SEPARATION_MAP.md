# WR-L scaffold versus native action — inverse-variational MAP

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Trigger | Charles Rotter: “Perhaps WR-L is a non-native scaffold.” |
| Mode | Analytic inverse-variational audit; DATA-BLIND |
| Repository | `grok` at `64af120`; unrelated dirt preserved |
| Prior status retained | WR-L is DERIVED under residual re-centering plus wall regularity, canon `C-2026-07-09-1` |
| Prohibited inference | Failure of one action class does not erase the banked geometric derivation or prove that no native action exists |
| GPU | Not used or requested |

## 0. Hypothesis under test

Separate three roles that were previously at risk of being conflated:

1. **Foundational kinematics:** Reciprocal-c Identity plus UDT Reciprocity gives the reciprocal
   metric family.
2. **WR-L scaffold:** residual re-centering plus wall regularity selects
   $A(r)=1-r/X$ inside that family.
3. **Native dynamics:** an off-shell action must independently make a physical profile stationary.

Test whether WR-L can be stationary in the broad local first-gradient reciprocal-current class. A
failure would support, but not prove, the scaffold interpretation.

## 1. Action class frozen before CAS verification

Use the full reciprocal physical metric

$$
ds^2=-A(r)c^2dt^2+A(r)^{-1}dr^2+r^2d\Omega^2,
\qquad
A=e^{-2\phi}>0.
$$

The determinant is independent of $\phi$. For a static radial reciprocal-group field,

$$
Y=\frac12\operatorname{Tr}(J_\mu J^\mu)
=g^{rr}(\phi')^2
=e^{-2\phi}(\phi')^2.
$$

Audit the entire class

$$
I_F=\mathcal N\int dr\,r^2F(Y),
$$

where:

- $F$ is universal and has no explicit $r$, desired profile, or boundary insertion;
- $F$ is at least $C^2$ on the range sampled by a regular solution;
- the physical metric is used in $Y$;
- no linearization is made;
- normalization $\mathcal N$ is irrelevant to stationarity.

This class includes the canonical quadratic group action but is not claimed to exhaust all possible
native UDT actions.

## 2. Predeclared gates

### G1 — full nonlinear variation

Vary $\phi$ before inserting WR-L. Account for the $\phi$ dependence in both $g^{rr}$ and $Y$.
Reject any fixed-background or linearized shortcut.

### G2 — inverse equation

Insert only after variation

$$
A_{\rm WR-L}=1-\frac rX,
\qquad
\phi_{\rm WR-L}=-\frac12\ln A_{\rm WR-L},
$$

and solve exactly for $p(Y)=F'(Y)$ along the complete interior range $0<r<X$.

### G3 — center regularity

At $r=0$, WR-L has

$$
Y_0=\frac{1}{4X^2}.
$$

Require a nontrivial native $F$ to be differentiable there. A divergent $F'$ fails this action
class's regularity gate even if a weighted on-shell integral happens to remain finite.

### G4 — $X$ universality

Determine whether one $F$, independent of the solution label $X$, can support more than one WR-L
scale. If supporting WR-L forces $X$ into $F$, then $X$ is an action parameter rather than an
integration constant in this class.

### G5 — honest scope

List all remaining escape routes, including:

- explicit $\phi$ potentials;
- curvature or higher-derivative metric invariants;
- additional native fields or carrier coupling;
- nonlocal/global functionals;
- boundary-selected rather than Euler-stationary scaffolds.

Do not invent or prefer an escape route without an independent UDT derivation.

### G6 — status discipline

Allowed verdicts:

- **WR-L NATIVE IN THE TESTED CLASS**;
- **WR-L REQUIRES A SINGULAR OR X-INSERTED MEMBER OF THE TESTED CLASS**;
- **TESTED CLASS EXCLUDES REGULAR NATIVE WR-L; SCAFFOLD LEAD STRENGTHENED**.

No result here may demote canon `C-2026-07-09-1`; that canon records a conditional geometric
derivation, not an off-shell action theorem.

## 3. Required exact calculations

1. Derive the arbitrary-$F$ Euler expression.
2. Compute $Y_{\rm WR-L}(r)$ and its range.
3. Convert the Euler equation into a first-order ODE for $p(Y)=F'(Y)$.
4. Solve the ODE exactly.
5. Audit $Y\to Y_0^+$ and $Y\to\infty$.
6. Test whether one nontrivial $F$ supports distinct $X$ values.
7. Recover the prior quadratic failure as the special case $F'(Y)=\text{constant}$.

## 4. Stop rules

- Do not infer “WR-L is not UDT.”
- Do not infer “no UDT action exists.”
- Do not add a potential, cutoff, fitted coefficient, or hard physical regulator to repair WR-L.
- Do not treat an integrable singular on-shell density as a regular off-shell variational law.
- Do not alter `LIVE.md` or `CANON.md` or begin F/G.

