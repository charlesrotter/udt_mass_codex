# C08 exact modular Gröbner refinement

Date: 2026-08-03
Branch: `grok`
Base before this preregistration: `9a7b6704b23716060cbd1d486f2aae2669d473d8`

## Trigger and disclosed information

The registered all-zero-coefficient case is the exact bivariate ideal

```text
I0=<A_12,B_12,A_13,B_13,A_23,B_23> in QQ[z,y].
```

Direct rational `slimgb(I0)` was stopped with Charles's authorization after 23,675 seconds. It had
returned no basis, used 47,295,612 KiB RSS at the final snapshot, and incurred no major page
faults. Its stdout also disclosed that Singular had failed to load `p_Procs_FieldIndep.so` and was
therefore running its slower fallback polynomial kernel. This is a resource and implementation
diagnosis only. It gives no information about the dimension, roots, or basis of `I0`.

The already disclosed construction proves each frozen C08 normalized curvature equation has the
form `A_i(y,z)x+B_i(y,z)`. The diagnostic six-antipodal-cluster reconnaissance remains disclosed
and non-certifying. Neither that count nor any expected factor, root, or physical interpretation may
control this refinement.

## Whole bounded question

Determine whether exact modular reconstruction can return and certify a rational Gröbner basis of
the unchanged ideal `I0`. This run covers only the exceptional `A_1=A_2=A_3=0` case required by the
registered case-complete linear-elimination split. It does not classify the three `A_i!=0` charts.

This is a metric-led algebraic classification of one frozen stationary/off-shell C08 tile. It is
not a field-equation solve, action test, source model, branch selector, or physics calculation.

## Frozen input and method

Before production, Git must freeze the six exact `A_i,B_i` polynomial files, their construction
record, the construction script, this preregistration, and both resource-return records. The
production driver must reproduce the registered SHA-256 values and prove that its emitted Singular
input contains those six polynomials unchanged.

The sole production method is:

```text
ring r=0,(z,y),dp;
ideal I=A_12,B_12,A_13,B_13,A_23,B_23;
ideal G=modStd(I,1);
```

`modStd(I,1)` is the exactness-one route in Singular `modstd.lib`: modular prime computations and
rational reconstruction are followed by exact input reduction and exact `verifyGB`. A
probability-only `modStd(I,0)` result is forbidden as a certificate. The returned basis must also
pass an explicit `system("verifyGB",G)` and exact reduction of all six original generators.

The optimized `p_Procs_FieldIndep.so` module must be preloaded. A warning-free smoke test on an
unrelated toy ideal must pass before the production input is opened. This is a Category-A
implementation correction; it does not change the ideal.

### Pre-production smoke-gate correction

No C08 production run had launched when the first toy smoke exposed two implementation facts. The
parallel modular library communicates between local worker processes, so the run must permit
localhost worker sockets. Its prime-field children also request `p_Procs_FieldGeneral.so`,
`p_Procs_FieldQ.so`, and `p_Procs_FieldZp.so` in addition to `p_Procs_FieldIndep.so`. The final gate
therefore preloads all four shipped optimized polynomial modules and launches Singular with local
worker communication enabled.

The first toy script also demonstrated that Singular can continue after an internal task error and
print a later success marker. The final smoke gate must consequently require all of: no internal
error text, no missing-library warning, `verifyGB=1`, zero exact input-reduction failures, and the
terminal pass marker. The failed restricted-sandbox toy run did not open the C08 production input
and carries no algebraic outcome.

The algebraic choices are solver choices, not physics premises:

- `QQ` coefficients: `pinned-by-THEORY`, inherited exact polynomial domain;
- variables/order `(z,y),dp`: `CHOSE_SOLVER_TECHNIQUE`, sparse degree-compatible computation;
- four process slots: `CHOSE_RESOURCE_CONTROL`;
- exactness one and final exact verification: `pinned-by-CERTIFICATION_CONTRACT`;
- no boundary condition, carrier, action, source, scale, density, or physical filter enters.

## Resource and stop contract

Run only one research computation. Launch Singular with `--cpus=4 --threads=1 --flint-threads=1`.
The supervising driver records the complete descendant process tree once per minute.

Terminate the process tree and return `OPEN_RESOURCE_BOUNDED_EXACT_ATTEMPT` if any occurs:

1. wall time reaches 86,400 seconds without a returned verified basis;
2. aggregate descendant RSS reaches 96 GiB;
3. host available memory falls to 24 GiB or less;
4. host swap use reaches 8 GiB;
5. the optimized polynomial-kernel smoke test fails;
6. Singular exits nonzero, emits an error, or exact final verification fails.

No resource stop is a zero-set result. A user-authorized earlier stop receives the same OPEN grade.
No automatic retry, changed order, changed ideal, looser exactness, or larger resource envelope is
authorized by this preregistration.

## Certification and maximum conclusion

A returned basis is only a machine artifact until independently reconstructed and adversarially
reviewed. Before any mathematical verdict, record the exact command, versions, environment,
input/output hashes, process log, peak resources, basis hash, dimension, verification markers, and
all six exact reductions. The remaining nonzero-A charts still require their registered saturation
and complete real-root isolation.

Maximum conclusion from this attempt alone: an exact certified Gröbner basis and algebraic
dimension for the frozen C08 all-zero-coefficient ideal, or an honestly OPEN resource return. It
cannot select C08 or imply a carrier, charge, action, source, boundary, dynamics, bootstrap law,
mass, matter, or physical universe.
