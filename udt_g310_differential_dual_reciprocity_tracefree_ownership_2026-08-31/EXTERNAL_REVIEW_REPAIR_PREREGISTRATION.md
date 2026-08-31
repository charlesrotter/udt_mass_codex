# G310 external-review repair preregistration

Date: 2026-08-31
State: frozen before repair implementation or repaired outcomes
Scientific question: unchanged
Scientific landing: unchanged and not yet externally accepted

## Frozen external findings

The external reviewer returned `G310_REPAIRABLE_DEFECTS` and identified exactly two defects.

### R1 — full reciprocal-tangent normalization

The derivation defines

\[
H(u,n)=2\left(u^\flat\!\otimes u^\flat+n^\flat\!\otimes n^\flat\right),
\]

but both executable certificates use `H/2`. This leaves span, rank, annihilator, and the scientific
landing unchanged, but it does not certify the exact displayed tangent.

Repair contract:

- production must use the exact seed `diag(2,2,0,0)`;
- the independent `pair_tangent` must return the exact factor-two tangent;
- all dependent expected cross terms and hostile wrong-sign tangents must use the same
  normalization;
- saved machine-readable outcomes must be regenerated from the repaired live builders;
- rank must remain nine, annihilator nullity one, and the conditional residual unchanged.

### R2 — actual independent annihilator reconstruction

The separate verifier constructs nine independent tangent directions but then hardcodes the
annihilator equations and a metric multiple. That supports the answer but does not independently
reconstruct it.

Repair contract:

- build the Lorentz-pairing rows from the separately constructed nine-direction basis;
- independently row-reduce those rows and compute their nullspace;
- prove exact rank nine, nullity one, and proportionality of the returned basis to `g_ab`;
- verify the component equations from the computed null vector rather than supplying them as the
  proof;
- do not import the production rank, nullspace, orbit, or pairing helpers.

## Evidence-language closure

After R1 and R2 pass, update result reports and ledgers only to record external repair acceptance or
pending follow-up accurately. Do not strengthen the bounded claim, call DDR founded or adopted,
fix the common scalar datum, select a history, or change G301's conditional type.

## Registered repair checks

Run under `python3 -S`:

```bash
python3 -S derive_ddr_tracefree.py
python3 -S verify_ddr_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
```

Then run the current premise verifier and complete repository regression. A fresh sealed repair-only
follow-up must replay the repaired package before the external gate closes.

## Maximum conclusion

At most: the two review defects are repaired and the original bounded conditional theorem is
externally accepted without scientific change. The repair cannot derive or adopt DDR, select the
G301 arena from the founding chain, or choose a curvature value, history, scale, or `X_max`.
