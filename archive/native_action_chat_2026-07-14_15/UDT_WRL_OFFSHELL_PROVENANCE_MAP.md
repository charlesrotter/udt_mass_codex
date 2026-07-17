# WR-L off-shell action provenance — MAP

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic DERIVE + adversarial inverse-variational audit |
| Repository | `grok` at `64af120`; pre-existing dirty work preserved |
| Parent result | `UDT_WRL_SOLUTION_SPACE_CLOSURE_DERIVATION_RESULTS.md` |
| Driver | DISCLOSED NON-COLD; the WR-L ODE and inverse functional are known |
| Preliminary work | A scratch multiplier/counteraction calculation preceded this file; no coldness claimed |
| GPU | Not used or requested |
| Banking | Forbidden pending fresh independent verification |

## 0. Question

The parent audit found

\[
F[A]\equiv r^2A''+rA'-A+1=0
\]

and the inverse functional

\[
\mathcal I_0[A]
=\frac12\int dr\left[r(A')^2+\frac{(A-1)^2}{r}\right].
\]

This audit asks:

\[
\boxed{
\text{Is }\mathcal I_0\text{ forced by UDT off shell, unique in a stated class, or only one of
many actions sharing WR-L?}
}
\]

## 1. Frozen premises

| Item | Status |
|---|---|
| Positional dilation | FOUNDING UDT postulate |
| Reciprocity / reciprocal metric slot | FOUNDING/working metric structure as currently recorded |
| Residual re-centering | Premise used in WR-L selector |
| (A=e^{-2\phi}), (A(0)=1) | Residual definition and seat normalization |
| (A=1-r/X) | DERIVED under residual re-centering plus wall regularity |
| (X) | WORKING POSIT; independent-vs-derived OPEN |
| EH, GR equations, (S^2), observed mass | Not used |

The on-shell residual transformation is

\[
(T_RA)(s)=A_R(s)=\frac{A(R+s)}{A(R)}.
\]

No assumption is made that this is already an off-shell action symmetry.  That claim is tested.

## 2. Classes to distinguish

### Q — narrow quadratic radial class

\[
L_Q
=\frac12p(r)(A')^2+s(r)(A-1)A'
+\frac12q(r)(A-1)^2,
\]

with first derivatives only.  Classify up to a nonzero overall constant and displayed total
derivatives.

### L — general local first-derivative radial class

\[
L=L(r,A,A'),
\]

with no fitted data and no hard cutoff.  Explicit local scale-free counteractions are admissible as
logical countermodels even if they are not proposed as physics.

### G — geometric parent class

Local covariant or explicitly UDT-foliated functionals whose independent fields, reciprocal
constraint, boundary primitive, and variation order are stated.  Holding a metric component fixed
that reciprocity makes dependent is not a valid one-field derivation.

## 3. Required derivations

1. Compute (F_s[T_RA]) exactly and determine whether the ODE is off-shell covariant.
2. Determine which stationary branches are closed under (T_R).
3. Transform (mathcal I_0) off shell and test action/quasi-action invariance.
4. Prove or refute uniqueness in class Q.
5. Construct at least one inequivalent member of class L sharing the WR-L extremal; check its Euler
   equation and Hessian multiplier exactly.
6. Test global depth scaling (A\mapsto kA) before and after seat gauge fixing.
7. Re-audit the fixed-spatial-metric curvature-lapse parent under reciprocal reduced variation.
8. Identify the minimum extra premise needed to treat any surviving functional as native.

## 4. Predeclared verdicts

### UNIQUE-NATIVE

Allowed only if one functional is forced in class G with its boundary primitive and no inequivalent
allowed class-L counteraction survives the same premises.

### CONDITIONAL-UNIQUE

Use if (mathcal I_0) is unique only after a named restriction such as class Q.  The restriction must
not be relabeled a UDT theorem.

### NONUNIQUE / INVERSE LEAD

Use if explicit inequivalent local counteractions share WR-L or if off-shell re-centering does not
select the action.

### INCONSISTENT

Use only if the proposed functional fails even to have WR-L as an extremal under its own declared
variation.

## 5. Stop rules

- Do not add an action axiom to rescue uniqueness.
- Do not infer dynamics from an on-shell identity alone.
- Do not hide a field-dependent multiplier or extra stationary branches.
- Do not quotient inequivalent actions merely because they share one solution.
- Do not promote a gauge-fixed seat functional to a global shift-invariant action without deriving
  the reference/seat variable and its variation.
- Stop before numerics unless the analytic audit produces a determined nonlinear boundary problem.

## 6. Deliverables

- `UDT_WRL_OFFSHELL_PROVENANCE_DERIVATION_RESULTS.md`
- `verify_udt_wrl_offshell_provenance.py`
- `verify_udt_wrl_offshell_provenance_out.txt`

