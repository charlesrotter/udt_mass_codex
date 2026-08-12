# Preregistration — pair-terminal reachability atlas

Date: 2026-08-12

Mode: `MAP -> DERIVE`, metric-led, exact zero-order algebra

Status: **PREREGISTERED BEFORE DERIVATION**

## Whole question

Fix one regular A-calibrated Lorentzian base pair metric. Release the complete pointwise Gram
contribution over the entire positive-semidefinite `2 x 2` cone. Determine exactly:

1. the signature of every completed pair form;
2. the complete A-calibrated terminal image in `(T,L,beta)` and `(kappa,phi,beta)`;
3. every rank-zero, rank-one, rank-two, Lorentzian, degenerate, and positive stratum;
4. a constructive inverse from every admitted terminal state to a Gram matrix; and
5. the factorization fiber of a fixed Gram matrix, without identifying ambient mixing and
   immersion slope.

The calculation asks what the already derived local orchestra can play. It does not ask which
state resembles a particle, cosmology, SNe, CMB, or `X_max`.

## Exact bounded regime

The fixed base is

```text
h0=-T0^2(dy0+beta0 dy1)^2+L0^2(dy1)^2,
T0>0,
L0>0,
beta0 real.
```

The released contribution is every

```text
P=C^T q C >= 0,
```

where `q` is the positive screen metric in one supplied regular local complete-coframe split.
An algebraic shear removes `beta0` from `h0`; congruence preserves the complete PSD cone. The
result must be transformed back to the original A calibration before terminal variables are
reported.

The full signature atlas retains every `P>=0`. The terminal atlas is restricted to the declared
A-calibrated stratum `h00<0`; nonterminal Lorentzian, degenerate, and positive forms are
characterized rather than discarded.

## Premise ledger

- `DERIVED`: `h=h0+P`, with `P` ranging over the full `PSD(2)` cone, from the pair-first theorem.
- `DERIVED CONDITIONAL`: terminal `(T,L,beta,kappa,phi)` from an A-calibrated Lorentzian pair form.
- `OBSERVED`: `c_E` is the clock/ruler calibration anchor; it selects neither `P` nor a relation.
- `CHOSE FOR COORDINATES`: one fixed base triple `(T0,L0,beta0)` remains symbolic.
- `FREE-AND-EXPLORED`: all three independent entries of `P`, including ranks zero, one, and two.
- `OPEN/INACTIVE`: physical history, query, immersion, branch, derivative jets, action, source,
  matter, bootstrap, `X_max`, SNe, CMB, and dynamics.

No numerical physical value, boundary condition, source, carrier, action, or observational target
enters this calculation.

## Preregistered candidate statements

The derivation will test, not assume, the following statements.

1. In a base-shift-removed covector frame,

   ```text
   h0=diag(-t,l),  t=T0^2>0, l=L0^2>0,
   P=[[p,m],[m,n]],  p>=0, n>=0, m^2<=p n.
   ```

2. Full signature is classified solely by

   ```text
   det(h)=(p-t)(l+n)-m^2.
   ```

3. The A-calibrated terminal image has a necessary-and-sufficient inequality in the target
   variables `(T,L,beta)` and admits an exact inverse construction of `P`.

4. Rank of `P` corresponds exactly to base, equality-boundary, and strict-interior terminal
   strata.

5. The image in terminal coordinates may be nonlinear; it will not be called a cone unless that
   property is proved.

6. No pointwise reachability statement selects a physical Gram history, branch, or global
   observer-relation family.

## Falsification and certification contract

The primary landing is allowed only if all of the following hold:

1. a symbolic derivation proves necessity and sufficiency, not merely sampled consistency;
2. an explicit inverse reconstructs a PSD Gram matrix for every target satisfying the proposed
   inequalities;
3. an independent stdlib exact-rational implementation, sharing no production code or output,
   checks direct matrix addition, signature, terminal extraction, inverse reconstruction, and rank
   on at least 250 preregistered rational cases spanning every retained stratum;
4. boundary controls include `P=0`, both pure rank-one axes, mixed rank one, positive-definite
   rank two, A-clock-null limits, Lorentzian forms outside the A-calibrated chart, degenerate forms,
   and positive forms;
5. pair-basis congruence and screen-frame invariance are checked exactly;
6. hostile controls demonstrate that reversed inequalities, omitted cross terms, and rank-boundary
   misclassification are caught; and
7. an adversarial semantic review confirms that no local signal speed, `X_max`, dynamics, or
   physical selector was inferred.

If any necessity, sufficiency, reconstruction, or independent check fails, the result must land as
`PARTIAL_OR_REFUTED_REACHABILITY_MAP`, with the failing stratum retained.

## Maximum allowed conclusion

At most:

```text
EXACT_ZERO_ORDER_REACHABILITY_CLASSIFICATION_FOR_ALL_PSD_GRAM_ADDITIONS_TO_ONE_FIXED_SYMBOLIC_
A_CALIBRATED_BASE_PAIR_METRIC__NO_DERIVATIVE_GLOBAL_OR_PHYSICAL_SELECTION_CONCLUSION.
```

## Completeness map

Covered: one complete pointwise `2 x 2` Gram image, all its ranks, all completed signatures, and
the entire regular A-calibrated terminal chart.

Dropped: variation over spacetime, second and higher jets, time-live evolution, topology, branch
gluing, global calibration carry, path holonomy, action terms, field equations, sources, matter,
stability, and physical regimes. Any of those may further restrict which pointwise states coexist
in a physical solution.

