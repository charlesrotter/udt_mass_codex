# External review response — G319

## Primary finding

I found no scientific defect that overturns the bounded G319 landing as stated in the sealed
request. The package supports the ratio-free `B!=0` regular-stratum classification, retains
`B=0` as a compatibility/gluing stratum rather than deleting it, and preserves G318 exactly as an
ansatz-scoped embedded subfamily. The package does **not** establish a global `B=0` crossing
classification or a full non-CMC census, but it does not claim either.

## 1. Authentication and scope compliance

I authenticated `REVIEW_MANIFEST.tsv` against `REVIEW_MANIFEST.sha256`, then authenticated every
manifest-listed payload by independent byte count and SHA-256. All 33 listed payloads matched.

I inspected only `/intake`, except for copying `/intake/package` into a writable ephemeral working
directory under `/work` for replay. I did not edit sealed evidence files. I did not use web
browsing, downloads, package installation, or nonlocal network access.

The sealed scope guards are internally consistent:

- [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json) forbids promotion to physical topology, scale,
  history, observation, source, matter/mass law, `X_max`, or a full UDT canon.
- [SOURCE_SCOPE.tsv](/intake/package/SOURCE_SCOPE.tsv) confines provenance to the sealed source
  records needed for G315-G318 ancestry and excludes the protected packages named in
  [verify_package.py](/intake/package/verify_package.py).
- [STATUS_LEDGER.tsv](/intake/package/STATUS_LEDGER.tsv) and
  [COMPLETENESS_MAP.md](/intake/package/COMPLETENESS_MAP.md) mark the global `B=0` crossing
  classification as open rather than silently solved.

## 2. Registered replay and artifact comparison

I copied the sealed package into `/work/g319_review.LxMxsb` and ran exactly the four registered
commands from [REPLAY_COMMANDS.txt](/intake/package/REPLAY_COMMANDS.txt):

```text
python3 derive_ratio_free_family.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

Observed replay outputs:

- `derive_ratio_free_family.py`: `87586` assertions, `324` exact zero-stratum instances, `8`
  periodic witnesses.
- `verify_independent.py`: `35059` assertions, `6` independent periodic variable-ratio
  instances, maximum direct residual `6.661338147750939e-15`.
- `run_catch_proofs.py`: `69/69` hostile mutations caught.
- `verify_package.py`: aggregate `PASS_PENDING_EXTERNAL_REVIEW`.

I then compared regenerated artifacts against the sealed package by exact bytes and SHA-256. The
replayed copies of [DERIVATION_RESULT.json](/intake/package/DERIVATION_RESULT.json),
[INDEPENDENT_VERIFICATION.json](/intake/package/INDEPENDENT_VERIFICATION.json),
[CATCH_PROOF_RESULT.json](/intake/package/CATCH_PROOF_RESULT.json),
[PACKAGE_VERIFICATION_RESULT.json](/intake/package/PACKAGE_VERIFICATION_RESULT.json), and
[PROFILE_ATLAS.tsv](/intake/package/PROFILE_ATLAS.tsv) were exact matches.

This matters: the sealed outputs are reproducible, not hand-curated after the fact.

## 3. Independent derivation of the ratio-free constraints

Starting from the registered conformal constraints stated in
[EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md) and inherited from
[G316](/intake/sources/udt_g316_lawful_constraint_data_construction_2026-09-01/EXACT_DERIVATION.md),

\[
v'=\psi^6\tau',
\]

\[
-8\psi''-\left(\frac23 v^2+2d^2\right)\psi^{-7}
+\left(\frac23\tau^2-2\Lambda\right)\psi^5=0,
\]

define

\[
\lambda=v\psi^{-6},\qquad A=\tau+\lambda,\qquad B=\tau-\lambda,\qquad H=\psi'/\psi.
\]

Then

\[
\lambda'=\tau'-6H\lambda,
\]

so

\[
B'=\tau'-\lambda'=6H\lambda=3H(A-B).
\]

This is the vector reduction, with no division by `B`.

For the scalar equation, multiply by `3 psi^-5 / 2`:

\[
\tau^2-v^2\psi^{-12}=12\psi''\psi^{-5}+3d^2\psi^{-12}+3\Lambda.
\]

Since `lambda^2=v^2 psi^-12` and `AB=tau^2-lambda^2`,

\[
AB=F[\psi],\qquad F[\psi]=12\psi''\psi^{-5}+3d^2\psi^{-12}+3\Lambda.
\]

That reproduces the claimed ratio-free `A/B` system exactly.

## 4. Independent derivation of the conserved `J0`

From

\[
B'=3H(A-B),\qquad AB=F,
\]

one gets

\[
(B^2)'=2BB'=6H(AB-B^2)=6H(F-B^2).
\]

Hence

\[
(\psi^6B^2)'=6\psi^5\psi'B^2+\psi^6(B^2)'
=6\psi^5\psi'F.
\]

Substituting `F` gives

\[
(\psi^6B^2)'=
72\psi'\psi''+18d^2\psi^{-7}\psi'+18\Lambda\psi^5\psi'.
\]

Therefore

\[
J_0=\psi^6B^2-36(\psi')^2+3d^2\psi^{-6}-3\Lambda\psi^6
\]

has zero derivative. This derivation is global on the connected coordinate circle and does not
divide by `B`, so the first integral survives across `B=0` as an identity even though the regular
square-root reconstruction does not.

## 5. Regular-stratum reconstruction and compact positivity

On any connected component where `B` is nowhere zero,

\[
B^2=\psi^{-6}Z,\qquad
Z=36(\psi')^2-3d^2\psi^{-6}+3\Lambda\psi^6+J_0,
\]

so one may choose a fixed sign `epsilon` and write

\[
B=\epsilon\psi^{-3}\sqrt{Z},\qquad A=F/B.
\]

Then

\[
\tau=\frac{A+B}{2}=\frac{B^2+F}{2B}.
\]

The sign of `tau` is therefore **not** controlled by `Z>0` alone. The package correctly treats
`B^2+F>0` as a second load-bearing positivity condition. This point is scientifically important;
without it, the sign-definite `tau` claim would be wrong.

For a fixed smooth positive periodic `psi` on a compact circle, the smooth functions

\[
G=36(\psi')^2-3d^2\psi^{-6}+3\Lambda\psi^6,\qquad -G,\qquad -G-\psi^6F
\]

are bounded. Choosing

\[
J_0>\sup_x\max\{-G(x),-G(x)-\psi(x)^6F(x)\}
\]

forces both `Z>0` and `Z+psi^6 F>0`, hence both `B^2>0` and `B^2+F>0`. Then `epsilon=+1`
produces `tau>0`, while `epsilon=-1` produces `tau<0`.

This compactness argument is sufficient for the stated bounded theorem: within the registered
slice, every smooth positive periodic `psi` admits regular sign-definite reconstructed constraint
data after choosing sufficiently large free `J0`.

## 6. Direct physical Hamiltonian and momentum constraints

Using the conformal weight from [G316](/intake/sources/udt_g316_lawful_constraint_data_construction_2026-09-01/EXACT_DERIVATION.md),
the mixed physical trace-free part is

\[
A^i{}_j=\psi^{-6}\operatorname{diag}\left(\frac23 v,-\frac13 v+d,-\frac13 v-d\right)
=\operatorname{diag}\left(\frac23\lambda,-\frac13\lambda+q,-\frac13\lambda-q\right),
\]

with `q=d psi^-6`. Therefore

\[
K^x{}_x=\frac{\tau+2\lambda}{3},\qquad
K^y{}_y=\frac{\tau-\lambda}{3}+q,\qquad
K^z{}_z=\frac{\tau-\lambda}{3}-q.
\]

These are the claimed mixed eigenvalues.

For the Hamiltonian constraint, with `R^(3)=-8 psi^-5 psi''`,

\[
\sum_i (K^i{}_i)^2
=\frac13(\tau+2\lambda)^2
+2\left[\left(\frac{\tau-\lambda}{3}\right)^2+q^2\right]
=\frac13\tau^2+\frac23\lambda^2+2q^2.
\]

Hence

\[
R^{(3)}+\tau^2-K_{ij}K^{ij}-2\Lambda
=-8\psi^{-5}\psi''+\frac23(\tau^2-\lambda^2)-2d^2\psi^{-12}-2\Lambda.
\]

Using `AB=tau^2-lambda^2=12 psi'' psi^-5+3 d^2 psi^-12+3 Lambda`, the right side vanishes
exactly.

For the momentum constraint, the only nontrivial component is the `x` component in this
one-coordinate diagonal frame. Directly,

\[
0=\nabla_j(K^{xj}-\gamma^{xj}\tau)
=K^x{}_{x}{}' - \tau' + 6H K^x{}_x - 2H\tau
=\frac23(\lambda'-\tau'+6H\lambda),
\]

which vanishes exactly because `lambda'=\tau'-6H lambda`.

So the physical direct replay agrees with the reconstructed conformal solution, and the package’s
direct-constraint claim is correct.

## 7. `B=0` compatibility, smoothness, and crossing limits

I attacked the weakest branch point directly.

At `B=0`, the scalar factorization `AB=F` forces `F=0`. The vector equation remains

\[
B'=3HA.
\]

So a zero of `B` need not be stationary; it can cross with nonzero derivative if `H A != 0`.
That part of the package is correct and materially important.

The regular reconstruction

\[
B=\epsilon\psi^{-3}\sqrt{Z}
\]

cannot itself classify all crossings because smooth gluing through `Z=0` depends on vanishing
order and compatibility of `A=F/B`. The package does **not** prove a global crossing theorem, and
its exact zero-stratum rows are best read as compatibility witnesses, not a full parameterization.
That is an open edge, but not a defect against the bounded claim set because the package explicitly
keeps this stratum open.

## 8. Periodic mean subtraction and TT/longitudinal descent

The descent

\[
\alpha=\frac23\langle v\rangle,\qquad
w'=\frac12(v-\langle v\rangle)
\]

is correct in this registered frame.

The factor `2/3` is forced by the diagonal TT seed normalization, and the mean subtraction is
load-bearing: without it, `w'` would generally fail the periodic zero-mean condition and periodic
`w` would not exist. The hostile catch suite explicitly tests this failure mode, and the algebra
checks out.

## 9. Exact G318 embedding

Restore the G318 ansatz

\[
\tau=C\psi^n,\qquad \lambda=\frac{n}{n+6}\tau,\qquad n\ne -6.
\]

Then

\[
A=\frac{2(n+3)}{n+6}\tau,\qquad
B=\frac6{n+6}\tau,
\]

so

\[
AB=\frac{12(n+3)}{(n+6)^2}C^2\psi^{2n}.
\]

Equating this with `F` yields

\[
-8\psi''
+\frac{8(n+3)}{(n+6)^2}C^2\psi^{2n+5}
-2d^2\psi^{-7}
-2\Lambda\psi^5=0,
\]

which is exactly the G318 scalar ODE recorded in
[G318](/intake/sources/udt_g318_nonconstant_psi_noncmc_branch_classification_2026-09-01/EXACT_DERIVATION.md).

Thus G318 is neither erased nor promoted. It survives exactly as a strict embedded subfamily, and
its `n<=-3` obstruction remains ansatz-scoped rather than universal. I found no evidence that G319
overwrites or weakens the sealed G318 theorem.

## 10. Independence, circularity, and provenance

The production derivation and independent verifier are not identical code paths.

- [derive_ratio_free_family.py](/intake/package/derive_ratio_free_family.py) performs the main
  algebraic reduction and periodic witness generation.
- [verify_independent.py](/intake/package/verify_independent.py) rebuilds Christoffels, Ricci, and
  momentum divergence by explicit index loops and does not import production code or read
  production outputs.
- [run_catch_proofs.py](/intake/package/run_catch_proofs.py) rejects the high-risk coefficient,
  sign, conformal-power, mean-subtraction, `B=0`, and scope/provenance mutations named in the
  preregistration.

The independent verifier is supporting evidence, not the primary proof: it constructs jets using
the reduced equations and then checks direct physical residuals. That would be too weak if the
package lacked a clean symbolic derivation, but here the symbolic derivation is short, explicit,
and correct. I do not find scientific circularity sufficient to overturn the package.

## 11. Verdict basis

The sealed package establishes, within its declared flat marked-`T^3`, positive periodic `psi`,
sign-definite `tau`, diagonal-TT, one-coordinate diagnostic slice, that:

1. removing G318’s constant-ratio ansatz reduces the exact constraints to `B'=3H(A-B)` and
   `AB=F[psi]`;
2. these equations carry the stated conserved `J0` without dividing by `B`;
3. on each nowhere-zero `B` component, every smooth positive periodic `psi` admits regular
   sign-definite reconstructed constraint data for sufficiently large free `J0`;
4. the direct physical Hamiltonian and momentum constraints agree with that reconstruction;
5. `B=0` is retained as a compatibility/gluing stratum requiring `F=0`, not deleted;
6. G318’s power family, obstruction, and periodic tidal family survive exactly as ansatz-scoped
   embedded results;
7. no physical initial data, history, topology, population, scale, source, matter/mass law,
   observation, or physical `X_max` is selected.

Residual limitation: the package does not solve the global `B=0` crossing classification. That is
an openly declared boundary, not a hidden defect.

G319_ACCEPTED__RATIO_FREE_REGULAR_QUADRATURE_AND_ANSATZ_SCOPE_UPHELD
