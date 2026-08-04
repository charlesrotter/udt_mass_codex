# C08 finite-field dimension certificate preregistration

Date: 2026-08-04
Branch: `grok`
Base before preregistration: `1bea9bc4`

## Trigger and disclosed boundary

For the frozen C08 all-zero-coefficient ideal

```text
I=<A_12,B_12,A_13,B_13,A_23,B_23> in QQ[z,y],
```

the exact rational nine-polynomial object `G` independently passes all 36 Buchberger reductions,
all six input reductions, and has a 124-element standard-monomial staircase. Thus
`I subset <G>` is established. Direct rational lift and modular rational-transformation routes did
not return the reverse certificate within their registered 1,800-, 7,200-, and 14,400-second
bounds. Exact reverse containment and ideal equality remain OPEN.

No finite-field C08 basis, transformation, dimension, or selected prime has been tested for this
new route before this preregistration.

## Whole bounded question

Can one exactly certified finite-field fiber prove an upper bound

```text
dim_Q QQ[z,y]/I <= 124,
```

which, combined with the already established quotient lower bound 124 induced by
`I subset <G>`, forces exact rational ideal equality `I=<G>`?

This is a certificate-led algebra audit of one frozen exceptional chart. It does not solve or
filter the metric's real solution space.

## Fixed integral model and prime

Use the six unchanged integer polynomials exactly as stored in the committed
`C08_MODULAR_ALL_ZERO_INPUT.sing`. Their generated ideal after extension to `QQ` is `I`.

Use exactly

```text
p=32003
```

after deterministic trial-division confirmation that it is prime. This is a
`CHOSE_SOLVER_TECHNIQUE` value, fixed before outcome. If it is composite, Singular rejects it, any
input becomes structurally invalid, or the finite-field attempt fails, return OPEN. Do not search
for a lucky prime and do not retry another prime.

## Exact finite-field certificate

In `Fp[z,y]` with variables `(z,y)` and `dp`, compute

```text
matrix T;
ideal H=liftstd(Ip,T);
```

and require all of:

1. `system("verifyGB",H)=1`;
2. every generator of `Ip` reduces exactly to zero by `H` after the verified standard-basis tag;
3. every entry of `matrix(Ip)*T-matrix(H)` is exactly zero in `Fp[z,y]`;
4. changing one nonzero entry of `T` makes that identity fail;
5. `H` is zero-dimensional and its leading-monomial staircase is finite;
6. the complete finite-field quotient dimension is exactly 124;
7. the full basis and transformation matrix are preserved for an independent parser.

A matching dimension without the transformation identity is not evidence that `H` belongs to
`Ip` and fails closed.

## Dimension argument to verify independently

For each total-degree cutoff `D`, form the integer Macaulay map from the multiples of the six
integer generators into the polynomial space of degree at most `D`. Reduction modulo `p` cannot
increase matrix rank:

```text
rank_Q(M_D) >= rank_Fp(M_D mod p).
```

Therefore every filtered quotient dimension satisfies

```text
h_Q(D) <= h_Fp(D).
```

If the certified finite-field quotient has total dimension 124, then `h_Fp(D)<=124` for every
`D`, so `dim_Q QQ[z,y]/I<=124`, even without assuming characteristic-zero zero-dimensionality.

The exact rational basis `G` independently gives a 124-dimensional quotient and the established
containment `I subset <G>` gives a surjection

```text
QQ[z,y]/I -> QQ[z,y]/<G>.
```

Hence the rational quotient has dimension at least 124. Matching upper and lower bounds make the
surjection an isomorphism and force `I=<G>`.

The independent verifier must reconstruct the finite-field identities and staircase without
importing production code, then separately replay the rational `G` Buchberger, input-reduction,
and 124-staircase gates. It must exercise mutations of `T`, `H`, one input coefficient, the prime,
and the claimed quotient count.

## Premise ledger

- six integer inputs: `pinned-by-FROZEN_ALGEBRA`;
- nine rational target polynomials and their one-way containment: `pinned-by-VERIFIED_PRIOR_RETURN`;
- ring variables `(z,y)` and `dp`: `pinned-by-FROZEN_ALGEBRA`;
- `p=32003`: `CHOSE_SOLVER_TECHNIQUE`, no physical meaning;
- `liftstd` and filtered-rank comparison: `CHOSE_CERTIFICATE_METHOD`;
- quotient target 124: `pinned-by-VERIFIED_PRIOR_RETURN`, used as an equality gate rather than fitted;
- no real sign, root, chart beyond all-zero, action, source, carrier, boundary, density, scale,
  bootstrap, mass, matter, or dynamical premise enters.

## Resource and stop contract

Use CPU only, one Singular process, and one thread. Stop and return OPEN on any of:

1. 3,600 seconds wall time;
2. 32 GiB aggregate descendant RSS;
3. host available memory at or below 64 GiB;
4. 4 GiB swap use;
5. failed source/hash/toy/prime gate, internal error, or nonzero process exit;
6. failed exact basis, transformation, mutation, dimension, or independent-replay gate;
7. output exceeding 2 GiB.

No automatic retry, second prime, rational reconstruction, changed monomial order, changed input,
larger envelope, real-root work, or fallback engine is authorized.

## Completeness and maximum conclusion

This covers only the all-`A_i=B_i=0` exceptional component inside C08's registered stationary,
off-shell projective zero-set split. It drops all three nonzero-`A_i` charts, exact real isolation,
C04/C09/C10 completion, arbitrary profiles, time dependence, field equations, action, source,
boundary, stability, and physical interpretation.

If production and independent exact checks pass, this attempt may establish rational ideal equality
for the frozen C08 all-zero branch, pending fresh cold adversarial review. If any gate fails, the
status remains OPEN. It cannot establish the real zero set, complete C08, select a branch, or support
charge, carrier, action, source, bootstrap, matter, mass, or dynamics.
