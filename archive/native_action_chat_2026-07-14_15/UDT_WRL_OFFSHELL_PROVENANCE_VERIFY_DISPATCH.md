# DISPATCH — blind verification of WR-L off-shell nonuniqueness

## Mission

Independently verify or falsify the claimed local action counterfamily for the WR-L equation.  This
is analytic CPU work.  Do not run GPU numerics, edit `LIVE.md`/`CANON.md`, or bank a native action.

## Synchronize first

```bash
git checkout grok
git fetch origin
git pull --ff-only origin grok
git status --short --branch
git log -8 --oneline
```

Preserve unrelated dirt.

## Cold arm

Give the cold verifier only:

1. `UDT_WRL_OFFSHELL_PROVENANCE_MAP.md`
2. `UDT_METHOD_MUSIC.md`
3. `UDT_DOTTED_LINE.md`
4. `SIMPLE_METRIC_MACRO.md`
5. `simple_metric_L_wall_regularity_closure_results.md`
6. `UDT_WRL_SOLUTION_SPACE_CLOSURE_DERIVATION_RESULTS.md`

Do not provide the off-shell results, verifier script, or output until its derivation is frozen.

## Adversarial arm

The adversary may then read:

- `UDT_WRL_OFFSHELL_PROVENANCE_DERIVATION_RESULTS.md`
- `verify_udt_wrl_offshell_provenance.py`
- `verify_udt_wrl_offshell_provenance_out.txt`
- all current action/boundary audits and negative registries.

## Required checks

1. Recompute the exact off-shell transformation of
   \[
   F[A]=r^2A''+rA'-A+1
   \]
   under (A_R(s)=A(R+s)/A(R)).
2. Check closure of (A=1+ar+b/r) and identify exactly which branch is re-centering closed.
3. Recompute the fixed-endpoint perturbation test proving that (mathcal I_0) is only on-shell
   re-centering invariant.
4. Classify
   \[
   L_Q=\tfrac12p(B')^2+\sigma BB'+\tfrac12qB^2
   \]
   up to overall scale and a displayed value-only total derivative.
5. Independently derive the Euler expression and velocity Hessian of
   \[
   L_6=
   \frac{r^5(B')^6}{480}
   -\frac{r^3B^2(B')^4}{96}
   +\frac{rB^4(B')^2}{32}
   +\frac{B^6}{96r}.
   \]
6. For (L_\lambda=L_0+\lambda L_6, \lambda>0), prove or refute
   \[
   E[L_\lambda]
   =r\left[1+\frac\lambda{16}(B^2-r^2B'^2)^2\right]
   \left(B''+\frac{B'}r-\frac{B}{r^2}\right).
   \]
7. Check whether the multiplier is strictly nonzero, whether extra stationary branches exist, and
   whether (L_\lambda) is equivalent to (L_0) by normalization or total derivative.
8. Recompute the WR-L action values and wall momenta:
   \[
   I_0=\frac12,
   \quad I_6=\frac1{180},
   \quad p_0(X)=-1,
   \quad p_6(X)=-\frac1{30}.
   \]
9. Test the reference-residual completion (A/A_0) and determine whether depth scaling removes the
   counterfamily.
10. Recheck the fixed-spatial-metric curvature-lapse functional under reciprocal one-field
    variation.

Use independently written symbolic code and preserve raw output.

## Verdict gates

- **NONUNIQUENESS PASS:** only if an independently verified, strictly nondegenerate
  (L_{\lambda\ne0}) has the identical bulk solution set and a different boundary momentum.
- **QUADRATIC CONDITIONAL UNIQUENESS PASS:** only if the quadratic classification is exhaustive
  inside its explicitly named class.
- **NATIVE ACTION PASS:** forbidden unless a separate UDT premise independently forces the
  quadratic class, measure, reference variable, boundary primitive, and normalization.
- Any discrepancy in signs, multipliers, endpoint terms, or equivalence classes must be resolved
  before a conclusion.

## Required return

Commit only an evidence package containing independent source, raw output, compact JSON, artifact
hashes, and a consistency checker.  The console summary must report all three gates above,
discrepancies, `git status --short --branch`, and `git log -5 --oneline`.  Stop afterward; no
physics conclusion or numerics.

