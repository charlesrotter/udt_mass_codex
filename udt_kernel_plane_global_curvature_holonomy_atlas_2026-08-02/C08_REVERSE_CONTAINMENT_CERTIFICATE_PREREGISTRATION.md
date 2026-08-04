# C08 exact reverse-containment certificate preregistration

Date: 2026-08-03
Branch: `grok`
Base before this preregistration: `6270240a2edc05eef373aaa89f00f31c09952160`

## Trigger and disclosed information

The frozen all-zero-coefficient C08 ideal is

```text
I=<A_12,B_12,A_13,B_13,A_23,B_23> in QQ[z,y].
```

The exactness-one modular production route returned a nine-polynomial rational object `G`. A
separate implementation established all 36 Buchberger reductions for `G`, zero reductions of the
six input generators by `G`, and a 124-element standard-monomial staircase. A direct exact
`lift(I,G)` did not return before its registered 1,800-second bound. Consequently only
`I subset <G>` is independently established; `<G> subset I` and ideal equality remain OPEN.

Inspection of the installed `modstd.lib` source after that return disclosed that exact modular
standard bases accept modules as well as ideals. No transformation coefficient, factor, root, or
physical classification has been inspected. This preregistration fixes a coefficient-tagged module
method before any C08 tagged-module computation.

## Whole bounded question

Can exact modular module algebra return explicit rational coefficients `C_ij(z,y)` satisfying

```text
G_j = sum_i C_ij I_i,  j=1,...,9,
```

with all nine identities independently expanded to exact zero?

This is a solver-certificate question for the frozen all-zero branch only. It does not isolate real
roots, count physical configurations, solve the three nonzero-A charts, or test any action, source,
carrier, boundary, scale, density, bootstrap, matter, mass, or dynamics.

## Frozen algebra and tagged-module method

Let `e_0,...,e_6` be a free-module basis over `QQ[z,y]`, and construct the six columns

```text
v_i = I_i e_0 + e_i,  i=1,...,6.
```

The production driver may use only an ordering in which the `e_0` component controls the projected
polynomial Gröbner calculation. That ordering must first pass an unrelated toy example proving all
of the following:

1. the nonzero `e_0` projections form the toy ideal's exact Gröbner basis;
2. each projected polynomial equals the original toy generators multiplied by its returned tag
   coordinates;
3. a low-degree lift from the projected basis to the independently supplied toy target reconstructs
   an exact coefficient certificate; and
4. changing one certificate coefficient makes exact verification fail.

After the toy gate, compute only

```text
module M=...v_1,...,v_6...;
module H=modStd(M,1);
```

using the same warning-free optimized exact modular implementation already frozen for C08. Extract
the nonzero `e_0` projections `P` and their six tag coordinates `T`. Every extracted column must
first satisfy `P=I*T` by exact expansion. Only then may `lift(P,G)` be attempted; this lift is between
the returned low-degree projected basis and the frozen nine-polynomial object, not between the six
large original generators and `G`. If it returns `G=P*L`, form `C=T*L` and save all entries.

No coefficient may be guessed, interpolated from numerical values, fitted, truncated, or inferred
from the desired result. A probability-only modular basis is forbidden.

## Premise ledger

- six rational input generators: `pinned-by-THEORY`, frozen C08 algebra;
- nine returned rational polynomials: `pinned-by-OBSERVED_MACHINE_RETURN`, not yet ideal equality;
- `QQ[z,y]` and variable order `(z,y)`: `pinned-by-FROZEN_ALGEBRA`;
- tagged free-module construction: `CHOSE_CERTIFICATE_METHOD`;
- component ordering: `CHOSE_SOLVER_TECHNIQUE`, admissible only after the preregistered toy gate;
- `modStd(M,1)`: `pinned-by-CERTIFICATION_CONTRACT`;
- four workers and resource bounds: `CHOSE_RESOURCE_CONTROL`;
- no physical value, sign, chart beyond the frozen all-zero chart, boundary, source, carrier, action,
  density, or desired root enters.

## Resource and stop contract

Use CPU only and one research process tree. The supervisor must launch at most four Singular workers
with one thread each and record descendant RSS, available memory, swap, wall time, exact command,
versions, and complete stdout/stderr. Stop and return OPEN if any occurs:

1. 7,200 seconds wall time;
2. 64 GiB aggregate descendant RSS;
3. host available memory at or below 32 GiB;
4. 8 GiB swap use;
5. failed toy gate, missing optimized kernel, internal Singular error, or nonzero exit;
6. missing projected basis, failed exact tag identity, failed low-degree lift, or failed exact
   production certificate identity.

No automatic retry, alternate component order, larger resource envelope, direct rational standard
basis, changed generator set, or real-root work is authorized.

## Independent verification and catch-proofs

A separate verifier must parse the six input polynomials, nine frozen returned polynomials, and the
saved certificate without importing production functions. It must use its own sparse exact-rational
polynomial arithmetic to expand every `G_j-sum_i C_ij I_i`. All nine must be identically zero.

It must also reject, in exercised catch-proofs:

- one changed rational coefficient;
- a dropped certificate row or column;
- a permuted input-generator identity;
- a certificate paired with any changed input or returned-basis hash; and
- a merely numerical or modular-zero comparison offered in place of exact rational equality.

Fresh adversarial review remains a separate gate and may not be represented by the production or
independent local verifier.

## Maximum conclusion

If and only if the production identities and independent exact expansions all pass, this attempt may
establish `<G> subset I`. Combined with the already independently established `I subset <G>`, it may
establish exact ideal equality for the frozen C08 all-zero-coefficient branch, pending fresh cold
review under the repository's load-bearing standard.

It cannot establish any real root, physical admissibility, global C08 classification, branch
selection, charge, carrier, action, source, boundary, bootstrap law, mass, matter, or dynamics.
