# G351 first blind adversarial response

Date: 2026-09-05
Context: fresh internal agent, read-only, no internet, no protected paths
Verdict: `REPAIR_G351_BOUNDED_CARRIED_MEASURE_CONSERVATION`

## Load-bearing finding

The intended exponent result is correct only for an existing nonzero absolutely continuous
density, not for every finite nonnegative conserved measure as the first draft stated.

On regular cuts define pulled-back area measures `alpha_i=J_i dlambda`. If `mu << alpha_i`, then
the Radon--Nikodym chain rule gives

```text
n_j=A_ji^-1 n_i
```

almost everywhere. The ratio form is valid only where `n_i>0`. For a nonzero component of declared
observer weight `w`, conservation throughout G350's independent positive abstract domain forces
`a=w` and `q=-1`; `w=p` remains a freely declared representation type.

The counterexample is label space `[0,1]`, regular `J_i=1`, `J_j=2`, and conserved
`mu=delta_(1/2)`. It is finite, nonnegative, and additive but has no density relative to either
area measure. Thus `q` is undefined for its singular part. Zero measure also constrains no exponent.

## Other findings

- The caustic, multiplicity, source/population, identity, sewing, reversal, observer covariance,
  ownership, and physical-ceiling statements were otherwise correctly scoped.
- Arbitrary real frequency powers need an explicit fixed dimensional reference.
- Initial arithmetic implementations sampled only densities and did not catch the singular
  counterexample; their evidence language needed narrowing and stronger probes.
- The pre-R1 evidence records had a 26/27 chronological reporting inconsistency.
- The review builder included contextual files not declared in `SOURCE_SCOPE.tsv`.

## Required repair

Narrow the theorem to the nonzero absolutely continuous regular-density component, retain the full
finite measure as the weak caustic-safe object, add atomic and zero-measure attacks, use
division-free equality, make the frequency reference explicit, reconcile evidence counts, and make
the sealed review source set match the registered source set.

The response made no edits and selected no light law, source, history, scale, or canon.
