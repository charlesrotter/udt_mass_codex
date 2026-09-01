# External Review Response

## Scope and authentication

I reviewed only `/intake`, as instructed. I authenticated `REVIEW_MANIFEST.sha256` against
`REVIEW_MANIFEST.tsv`, then authenticated `REVIEW_SCOPE.json` and every manifest-listed payload in
the sealed intake by byte count and SHA-256. The manifest hash matched exactly, and all 31
manifest-listed payloads matched their recorded sizes and digests.

This establishes seal integrity for the supplied package. It does not, by itself, prove the
historical Git ancestry claims mentioned inside the prose, because repository access was forbidden.
That is a provenance limit of the sealed-review protocol, not a scientific defect in the bounded
claim.

## Replay of registered commands

I copied `/intake/package` into a fresh writable directory under `/work` and ran the four
registered commands:

1. `python3 -S derive_lawful_data_construction.py`
2. `python3 -S verify_independent.py`
3. `python3 -S run_catch_proofs.py`
4. `python3 -S verify_package.py`

All four completed successfully. Reported outputs were:

- production assertions: `66`
- independent assertions: `139`
- hostile mutations caught: `16/16`
- package verification: `PASS_PRE_EXTERNAL_REVIEW`

The regenerated files `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`,
`CATCH_PROOF_RESULT.json`, `PACKAGE_VERIFICATION_RESULT.json`, and
`DATA_CONSTRUCTION_ATLAS.tsv` were byte-identical to the sealed versions in `/intake/package`.

## Independent adversarial assessment

### 1. Conformal powers and transformed constraints

Starting from the sealed G315 spacelike constraints

`R^(3) + (2/3) tau^2 - A_ij A^ij = 2 Lambda`

and

`D_j A^ij - (2/3) D^i tau = 0`,

the three-dimensional conformal bookkeeping in the package is correct:

- `gamma_ij = psi^4 gbar_ij`
- `gamma^ij = psi^-4 gbar^ij`
- `A^ij = psi^-10 Abar^ij`
- `A_ij = psi^-2 Abar_ij`
- `A_ij A^ij = psi^-12 |Abar|^2`
- `R^(3) = psi^-5 (-8 Deltabar psi + Rbar psi)`
- `D_j A^ij = psi^-10 Dbar_j Abar^ij` for tracefree `A`
- `D^i tau = psi^-4 Dbar^i tau`

These imply exactly the displayed Lichnerowicz equation

`-8 Deltabar psi + Rbar psi - |Abar_TT + Lbar W|^2 psi^-7 + ((2/3) tau^2 - 2 Lambda) psi^5 = 0`

and vector equation

`Dbar_j (Lbar W)^ij = (2/3) psi^6 Dbar^i tau`.

I find no algebraic sign or power defect in `-8`, the negative TT norm, the coefficient
`(2/3)tau^2 - 2Lambda`, or the powers `-7`, `5`, and `6`.

### 2. CMC status, kernel obstruction, and bounded solvability

The package keeps CMC decoupling as a diagnostic mathematical subcase, not as a UDT premise. That
is the correct scope discipline here.

For the compact boundaryless vector problem, the integration-by-parts identity

`int X_i (Dbar_j (Lbar W)^ij) = -(1/2) int (Lbar X)_ij (Lbar W)^ij`

correctly exposes the conformal-Killing kernel, the orthogonality condition on the source, and the
nonuniqueness of `W` modulo kernel elements while leaving `Lbar W` unchanged. The package does not
inflate this into a global parameterization or full solvability theorem.

The constant-coefficient controls also survive adversarial checking:

- with `Rbar = 0`, `|Abar|^2 = a^2 > 0`, `C = (2/3)tau^2 - 2Lambda > 0`, one gets
  `psi^12 = a^2 / C`;
- with the same nonzero `a^2` and `C <= 0`, the integrated scalar equation has no positive
  solution on a compact boundaryless slice;
- with `Abar = 0`, constant `Rbar = R0`, constant `C`, constant solutions require
  `psi^4 = -R0 / C > 0`;
- with `Rbar = 0`, `Abar = 0`, `C = 0`, every positive constant `psi` solves, exhibiting an
  unfixed homothety rather than a selected physical scale.

These are legitimate bounded witnesses. They do not amount to a global Yamabe/non-CMC/boundary
classification, and the package does not claim that they do.

### 3. Physical-constraint sign check and G315 witness reconstruction

The four G315 witnesses were not merely recycled through the conformal residual. Using the
physical Hamiltonian constraint directly:

- round positive bounce: `6 + 0 - 0 = 2*3`
- flat positive slicing: `0 + (2/3)*9 - 0 = 2*3`
- positive product time-symmetric: `6 + 0 - 0 = 2*3`
- Berger-`S3`: `(7/2) + (2/3)*(15/4) - 0 = 2*3`

The signs are therefore consistent at the physical-constraint level, including the positive
`Lambda` controls and the absence of an erroneous TT contribution in these witnesses.

### 4. Null-corner boost laws and scope discipline

With `g(ell,k) = -1` and boost `ell -> e^f ell`, `k -> e^-f k`, the package correctly assigns:

- weight `+1` to `theta_(ell)` and `sigma^(ell)`
- weight `-1` to `theta_(k)` and `sigma^(k)`
- weight `0` to the cross-products and to `Ric(ell,k)`

Using the stated sign convention

`omega_A = - k_b q_A^c nabla_c ell^b`,

the transformation `omega_A -> omega_A + D_A f` is correct, so the curl is boost invariant. Since
`Ric_ab = Lambda g_ab`, the mixed projection gives `Ric(ell,k) = -Lambda`, also boost invariant.

The package is also disciplined about interpretation: cross-normalization is not promoted to a
physical scale, and one null sheet is not called a complete characteristic data set.

### 5. Seed/solved/gauge/output typing and provenance

The seed/solved/gauge/output ledger is scientifically well-typed:

- conformal metric, TT tensor, mean curvature, connected `Lambda`, topology, and boundary data are
  supplied inputs;
- `psi` and `W` are solved variables, if solvable;
- `gamma_ij` and `K_ij` become lawful data only after the constraints are solved;
- lapse and shift remain evolution gauge;
- no physical history, population, scale, topology, source, matter/mass law, observation, action,
  or physical `X_max` is selected.

I found no sealed evidence of protected-package use, repository mining, observational calibration,
or smuggled extra premises. The listed provenance sources stay within the sealed G310/G312/G313/G315
chain plus the current authority files.

## Findings

I do not find an algebraic, geometric, solvability, scope, or provenance defect that overturns the
bounded landing. The package supports one conformal construction of a lawful subset of G315 data,
with real existence and obstruction gates, conformal-Killing degeneracy, and bounded null-corner
gauge statements, while explicitly refusing a physical selector or a full global theorem.

The only caveat is protocol-level provenance: sealed files can authenticate the recorded intake,
but not independently reconstruct historical Git timing/ancestry without repository access. That
limitation does not refute the scientific landing stated here.

G316_ACCEPTED__LAWFUL_CONSTRUCTION_AND_BOUNDS_UPHELD
