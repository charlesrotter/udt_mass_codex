# C08 modular transformation-certificate preregistration

Date: 2026-08-03
Branch: `grok`
Base before this preregistration: `f11d8fce`

## Trigger and prior method boundary

The frozen exactness-one modular return produced a nine-polynomial object `G`. Independent exact
checks establish that `G` is a Gröbner basis of `<G>`, that all six generators of the frozen C08
all-zero ideal `I` reduce to zero by `G`, and that `R/<G>` has rational vector-space dimension 124.
The still-missing direction is `<G> subset I`.

The separately preregistered tagged-module method opened no C08 tagged-module input. Its exactness-one
toy exposed an installed ideal-only final-test dispatch; its `(dp,C)` placements failed the projection
gate; and its first `(C,dp)` toy was algebraically vacuous because the chosen toy generators were
already a Gröbner basis. That method is stopped rather than retuned further.

Inspection of the installed `modular.lib` and `liftstd` interfaces discloses a distinct route:
`modular` can rationally reconstruct a matrix, while finite-field `liftstd(I,T)` can return a basis
and its generator-transformation matrix. No C08 transformation coefficient has been computed or
inspected before this preregistration.

## Whole bounded question

Can a modular transformation computation return exact rational matrices satisfying

```text
G_j = sum_i I_i T_ij,  i=1,...,6, j=1,...,9,
```

and can a separately implemented sparse exact-rational verifier expand all nine residuals to zero?

This covers only the frozen C08 all-zero-coefficient ideal in `QQ[z,y]`. It cannot classify real
roots, the three nonzero-A charts, C09/C10, or any physical structure.

## Fixed method

Define a pure Singular procedure `stdWithTransform(I)` which, in its current basering, performs

```text
matrix T;
ideal H=liftstd(I,T);
```

and returns one polynomial matrix `W` with the normalized basis `H` in row one and the six
transformation rows of `T` below it. Thus column `j` is `(H_j,T_1j,...,T_6j)`.

Use `modular("stdWithTransform",list(I),...)` to compute finite-field transformations, discard
unlucky primes by the size and leading-monomial sequence of row one, combine matrices by Chinese
remaindering, and reconstruct rational coefficients by Farey reconstruction.

Every candidate remains untrusted until the final exact rational test verifies all of:

1. row one has nine nonzero polynomials and `system("verifyGB",H)=1`;
2. all six frozen input generators reduce exactly to zero by `H`;
3. every entry of `matrix(I)*T-matrix(H)` is exactly zero;
4. `H` and the frozen returned `G` are identical after the registered reduced-basis normalization,
   or a separately saved low-degree basis-change matrix `L` satisfies `G=H*L` exactly;
5. the composed certificate satisfies `matrix(I)*T*L-matrix(G)=0` exactly when `L` is required.

The finite-field modular outputs and prime tests are coefficient-search and reconstruction machinery.
The certificate is the final exact rational polynomial identity, not agreement at sampled primes.

## Nontrivial toy gate

Before any C08 transformation input is opened, the exact implementation must pass the unrelated
fixed toy

```text
ring r=0,(x,y),dp;
ideal I=x^2+y, x*y+1;
```

whose leading monomials are not relatively prime. The gate must return a transformed basis, verify
`I*T=H` exactly, verify the basis exactly, reduce both toy inputs to zero, and show that changing one
nonzero transformation coefficient makes the exact matrix identity fail. Internal errors, missing
optimized kernels, a zero/vacuous matrix, or a probability-only comparison fail the gate.

## Premise ledger

- six input polynomials and nine frozen returned polynomials: `pinned-by-FROZEN_ALGEBRA`;
- `QQ[z,y]`, `(z,y)`, and `dp`: `pinned-by-FROZEN_ALGEBRA`;
- per-prime `liftstd` transformation: `CHOSE_CERTIFICATE_METHOD`;
- matrix-valued modular reconstruction: `CHOSE_CERTIFICATE_METHOD`;
- exact rational identity as the only membership gate: `pinned-by-CERTIFICATION_CONTRACT`;
- four worker processes, one thread each: `CHOSE_RESOURCE_CONTROL`;
- no root, sign, physical-domain, action, carrier, source, boundary, scale, density, or desired
  configuration enters.

## Resource and stop contract

Use CPU only and one supervised research process tree. Stop and return OPEN on any of:

1. 7,200 seconds wall time;
2. 64 GiB aggregate descendant RSS;
3. host available memory at or below 32 GiB;
4. 8 GiB swap use;
5. failed nontrivial toy, failed source/hash gate, internal error, or nonzero exit;
6. unstable matrix dimensions or leading-monomial order across retained primes;
7. failed exact basis, transformation, basis-change, or final certificate identity.

No automatic retry, alternate monomial order, changed ideal, larger envelope, root isolation, or
fallback algebra engine is authorized.

## Independent verification and catch-proofs

A separate Python verifier must not import the production driver. It must parse all six inputs, all
nine frozen returned polynomials, and all 54 certificate entries independently. Using its own sparse
dictionary representation with exact rational coefficients, it must compute every convolution and
sum in `G_j-sum_i I_i C_ij`; every residual dictionary must be empty.

It must exercise and reject:

- changing one nonzero numerator by one;
- dropping or duplicating a certificate row or column;
- permuting two input identities without permuting the certificate;
- any input, basis, or certificate hash mismatch; and
- modular-zero or numerical agreement offered instead of exact rational equality.

Fresh adversarial review remains separate and absent unless explicitly authorized.

## Maximum conclusion

If production and independent exact identities pass, this attempt may establish `<G> subset I`.
Together with the already independently established `I subset <G>`, it may establish exact ideal
equality for the frozen C08 all-zero branch, pending fresh cold review under the repository standard.

It cannot establish real roots, physical admissibility, the complete C08 zero set, branch selection,
charge, carrier, action, source, boundary, bootstrap, matter, mass, or dynamics.
