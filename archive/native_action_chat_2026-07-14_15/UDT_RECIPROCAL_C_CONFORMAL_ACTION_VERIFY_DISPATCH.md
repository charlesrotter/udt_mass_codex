# Workstation dispatch — cold audit of the Reciprocal-c conformal-action branch

## Scope and attribution

Charles Rotter proposed the Reciprocal-c Identity: $c$ and $c^{-1}$ are coequal time-length
conversion directions. The supplied derivation asks whether the common scale left undetermined by
that identity can supply an action selector.

Audit only:

- `UDT_RECIPROCAL_C_CONFORMAL_ACTION_MAP.md`
- `UDT_RECIPROCAL_C_CONFORMAL_ACTION_DERIVATION_RESULTS.md`
- `verify_udt_reciprocal_c_conformal_action.py`
- `verify_udt_reciprocal_c_conformal_action_out.txt`

Do not alter `LIVE.md` or `CANON.md`, adopt common-scale neutrality, bank an action, start F/G, or
import conformal-gravity phenomenology.

## 1. Foundational circularity audit

Independently decompose

$$
\operatorname{diag}(u,v)=\Omega\operatorname{diag}(e^{-\phi},e^\phi).
$$

Determine exactly what follows from:

1. the reversible $c/c^{-1}$ identity;
2. UDT Reciprocity;
3. the additional assertion that common local scale is representational.

Give the strongest argument that common-scale neutrality is upstream and the strongest objection
that it is an added conformal postulate. Do not merge these judgments.

## 2. Invariant-basis reconstruction

Without trusting the supplied basis, classify the local parity-even metric scalars through
curvature-quadratic order in four dimensions. Audit:

$$
E_4=Riem^2-4Ric^2+R^2,
$$

$$
C^2=Riem^2-2Ric^2+\frac13R^2.
$$

Verify local conformal weights, topology/boundary equivalences, and the claim that $C^2$ is the
unique non-topological bulk density within the named minimal basis. List every premise needed to
exclude higher-derivative conformal invariants.

## 3. Reciprocal curvature algebra

From the metric

$$
ds^2=-A(r)c^2dt^2+A(r)^{-1}dr^2+r^2d\Omega^2,
$$

recompute Christoffels, Riemann, Ricci, $R$, $Ric^2$, $Riem^2$, $E_4$, and $C^2$. In particular audit

$$
C^2=\frac{[r^2A''-2rA'+2(A-1)]^2}{3r^4}.
$$

Check algebra, signs, coordinate assumptions, and the $r=0$ domain separately.

## 4. Variation audit

Compute the higher-derivative Euler operators for the reduced $R^2$, $Ric^2$, Euler, and $C^2$
densities. Confirm that $R^2$ and $Ric^2$ are independent and that the $C^2$ equation reduces to

$$
rA''''+4A'''=0.
$$

State all boundary data required by the fourth-order variation.

## 5. Full-tensor gate

Do not accept reduced variation as certification. Independently construct

$$
B_{\mu\nu}
=\left(\nabla^\rho\nabla^\sigma+\frac12R^{\rho\sigma}\right)
C_{\mu\rho\nu\sigma}
$$

or an algebraically equivalent full unrestricted-metric Euler tensor.

For

$$
A=a_0+a_1r+\frac{a_{-1}}r+a_2r^2,
$$

audit the claimed full constraint

$$
a_0^2-3a_1a_{-1}=1.
$$

Retain raw tensor code and output.

## 6. WR-L post-test

Only after sections 1–5, insert

$$
A=1-r/X.
$$

Check independently:

1. every Bach component;
2. $C^2$;
3. $R$;
4. whether $X$ occurs in the action or only in the solution;
5. whether the action admits, selects, or assigns zero density to WR-L.

## 7. Dynamics adversary

Assess without importing outside phenomenology:

- fourth-order initial/boundary data;
- additional time-live modes;
- finite-cell boundary functional;
- action normalization and energy sign;
- whether conformal gauge can coexist with physical clocks, matter, and mass;
- whether $C^2=0$ makes WR-L a scaffold rather than a dynamically selected vacuum.

No defect may be repaired by inserting $X$, a carrier, a cutoff, or an effective term.

## 8. Required verdict

Return:

1. PASS/FAIL for sections 1–7;
2. corrected equations for every failure;
3. raw CAS scripts and output;
4. one foundational verdict:
   - **COMMON-SCALE NEUTRALITY DERIVED**;
   - **VIABLE ADDITIONAL POSTULATE**;
   - **UNJUSTIFIED / INCOMPATIBLE**;
5. one action verdict:
   - **UNIQUE WITHIN STATED MINIMAL BASIS**;
   - **NONUNIQUE EVEN WITHIN BASIS**;
   - **FULL-TENSOR FAILURE**;
6. one WR-L verdict:
   - **NOT A SOLUTION**;
   - **ADMITTED BUT NOT SELECTED**;
   - **UNIQUELY SELECTED**;
7. separate judgments on whether the native-action and scaffold interpretations are mutually
   exclusive.

Stop after reporting. No frontier/canon change without Charles's explicit verdict.

