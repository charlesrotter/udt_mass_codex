# External Adversarial Review Response: G320

Date: 2026-09-01
Reviewer mode: fresh zero-context, sealed-intake only, bounded read-only review

## 1. Scope compliance

I inspected only `/intake` and did not access any repository, protected package, or unsealed
observation. I did not browse, search, download, install packages, or make network-capable calls.
I did not edit any evidence file. I copied `/intake/package` into a fresh writable directory under
`/work` solely to rerun the four registered commands.

## 2. Authentication of the sealed intake

I authenticated the detached seal first.

- `sha256sum -c /intake/REVIEW_MANIFEST.sha256` returned `REVIEW_MANIFEST.tsv: OK`.

I then authenticated every manifest payload against both recorded byte count and recorded SHA-256.

- Manifest payload rows checked: `32`
- Size mismatches: `0`
- Hash mismatches: `0`

That covers `REVIEW_SCOPE.json`, all `package/*` payloads, and all `sources/*` payloads listed in
`REVIEW_MANIFEST.tsv`.

## 3. Replay of the registered commands

I copied `/intake/package` to `/work/g320_review_yvUVBj` and reran exactly:

```text
python3 derive_physical_quotient.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

All four commands passed. The regenerated artifacts matched the sealed package byte-for-byte.

- `DERIVATION_RESULT.json`: identical
- `INDEPENDENT_VERIFICATION.json`: identical
- `CATCH_PROOF_RESULT.json`: identical
- `PACKAGE_VERIFICATION_RESULT.json`: identical
- `INVARIANT_ATLAS.tsv`: identical

The regenerated hashes exactly matched the manifest hashes.

## 4. Independent rederivation of the load-bearing geometry claim

I did not accept the package’s curvature separator on faith. I rederived it.

For the three-dimensional conformal metric

\[
\gamma_{ij}=\psi^4\delta_{ij},\qquad \psi=\psi(x)>0,
\]

the standard `n=3` conformal scalar-curvature transformation with flat seed gives

\[
{}^{(3)}R=-8\psi^{-5}\Delta\psi=-8\psi^{-5}\psi''.
\]

The volume form is

\[
d\mu_\gamma=\psi^6\,dx\,dy\,dz.
\]

Therefore

\[
\int {}^{(3)}R\,d\mu_\gamma
=-8\int \psi\psi''\,d^3x
=8\int (\psi')^2\,d^3x
\]

on the periodic torus, by integration by parts with vanishing boundary term. This is exact. The
sign, the conformal power `-5`, and the volume power `6` are all correct; the hostile mutations
that flip any of them are genuinely fatal.

Under a constant homothety `\gamma \mapsto \ell^2\gamma`, scalar curvature scales as `\ell^{-2}`
and volume form as `\ell^3`, so `\int R\,d\mu` scales as `\ell` while `Vol^{1/3}` also scales as
`\ell`. Hence

\[
Q_R=\frac{\int {}^{(3)}R\,d\mu_\gamma}{\operatorname{Vol}(\gamma)^{1/3}}
\]

is homothety-neutral and spatial-diffeomorphism invariant. If two reconstructed physical metrics
are spatially diffeomorphic, they must have the same `Q_R`.

## 5. Independent check of the mode family and coefficients

For the registered family

\[
\psi_n(x)=p+a\cos(nx),\qquad p=\frac32,\qquad a=\frac15,
\]

positivity is immediate because `p>|a|`.

The volume density is `\psi_n^6`. Averaging over one `2\pi` period uses

\[
\langle \cos^2\rangle=\frac12,\qquad
\langle \cos^4\rangle=\frac38,\qquad
\langle \cos^6\rangle=\frac5{16},
\]

so

\[
\langle \psi_n^6\rangle
=p^6+\frac{15}{2}p^4a^2+\frac{45}{8}p^2a^4+\frac5{16}a^6
=\frac{2585929}{200000},
\]

independent of `n`. The coefficient pattern in the package is correct.

Also

\[
\psi_n'=-an\sin(nx),
\qquad
\int (\psi_n')^2\,d^3x=(2\pi)^2\pi a^2 n^2,
\]

so

\[
Q_R[\psi_n]=n^2Q_R[\psi_1].
\]

I independently recomputed the numerical values with my own ad hoc quadrature script, using
sample counts not used by the package. The results matched the sealed atlas:

- common volume `3207.20120198444...`
- `Q_R(1)=2.69123022947259...`
- `Q_R(2)=10.76492091789047...`
- `Q_R(3)=24.22107206525346...`
- `Q_R(4)=43.05968367156167...`

These satisfy the exact `1:4:9:16` law to numerical precision.

This is enough to exclude spatial-diffeomorphism equivalence between different modes. The
inequivalence argument does not depend on raw arrays, phase choices, or a preferred coordinate.

## 6. Lawful-data reconstruction check

I also rederived the regular-stratum reconstruction logic from the sealed G319 source.

With

\[
AB=F[\psi],\qquad B'=3H(A-B),\qquad H=\psi'/\psi,
\]

one gets

\[
(B^2)'=6H(F-B^2),
\]

and hence

\[
(\psi^6B^2)'=6\psi^5\psi'F.
\]

For the registered `d=0`, `\Lambda=0` slice, this integrates to

\[
J_0=\psi^6B^2-36(\psi')^2,
\qquad
B^2=\psi^{-6}\bigl(36(\psi')^2+J_0\bigr).
\]

The coefficient `36` is correct. The package’s first-integral algebra is coherent.

For the specific diagnostic choice `J_0=100`, the stronger sign-control quantity is

\[
Z+\psi^6F=36(\psi')^2+100+12\psi\psi'',
\]

and the package’s crude lower bound

\[
100-12an^2(p+a)
\]

is correct. For `n=1,2,3,4` it gives `95.92, 83.68, 63.28, 34.72`, all positive. So the chosen
regular branch is indeed lawful for both signs on the finite replay set.

I independently reconstructed `A`, `B`, `\tau`, `\lambda`, and the diagonal `K`, then checked the
direct Hamiltonian residual, direct momentum residual, branch sign, and `J_0` constancy with my
own script. I reproduced the sealed values up to roundoff:

- maximum Hamiltonian residual: about `4.4e-15`
- maximum momentum residual: about `2.2e-15`
- maximum `J_0` drift: about `7.1e-14`
- minimum signed `\tau` stayed positive on both branches for all replayed modes

So G320 is not merely exhibiting intrinsic trial metrics. It is replaying lawful reconstructed
initial data in the bounded G319 slice.

## 7. Quotient controls and false-equivalence attacks

The phase/reflection controls are sound and not overclaimed.

- Phase shifts and reflections are spatial diffeomorphisms of the marked torus.
- `Q_R`, volume, and the stated weighted contractions must therefore agree.
- The package tests several explicit representatives as a regression guard.
- The proof of inequivalence does not depend on those finite phase samples; it depends on the
  invariant itself.

The conformal-seed covariance control is also sound within its stated scope.

- If `\widehat{\bar\gamma}=\vartheta^4\bar\gamma`, `\widehat\psi=\psi/\vartheta`, and
  `\widehat{\bar A}^{ij}=\vartheta^{-10}\bar A^{ij}`, then the reconstructed physical metric and
  physical trace-free tensor are unchanged.
- With unchanged `\tau`, the full reconstructed `K` is unchanged.
- The package checks this with nonconstant positive `\vartheta`, and the independent verifier uses
  a different `\vartheta`.

I found no false equivalence being smuggled in through raw seed comparisons, phase changes, or the
auxiliary conformal representation.

## 8. Production versus independent implementation separation

The separation is real, though not absolute.

- `verify_independent.py` does not import `derive_physical_quotient.py`.
- It does not read `DERIVATION_RESULT.json`.
- It rebuilds Christoffels, Ricci, and momentum divergence by explicit index loops.
- It uses different `p`, amplitude, modes, sample count, `J_0`, and seed rewrite.

That is a meaningful implementation-distinct cross-check of the load-bearing geometry and
constraint replay.

The boundary of that independence is also clear: the independent verifier still accepts the same
bounded G319 mathematical framework and reconstruction formulas. It is not an independent proof of
the upstream G319 theorem. But G320 does not pretend otherwise; it uses G319 as an explicit sealed
premise, and the package does not overstate this point.

## 9. Scope, provenance, and overclaim audit

The package stays inside the declared bounds.

- It does not claim a complete quotient of all G319 profiles.
- It does not select physical topology, population, scale, sources, matter, mass, observations, or
  physical `X_max`.
- It does not change the metric or reciprocal kernel.
- It does not promote the diagnostic one-coordinate torus slice into full UDT.

The source-scope file lists only the bounded prerequisite materials, and the protected package
identifiers named in `verify_package.py` are absent from the sealed source scope. I found no sealed
evidence of provenance laundering or unauthorized dependency import.

## 10. Adversarial conclusion

I attacked the curvature coefficient, the conformal powers, the volume weight, the homothety
normalization, the `n^2` scaling, the branch-sign argument, the lawful reconstruction claim, the
phase/reflection quotient controls, the conformal-seed covariance control, the implementation
separation claim, the bounded-scope guardrails, and the provenance envelope.

No scientific defect survived those attacks inside the sealed scope.

What is proved is exactly the bounded claim and no more: within the externally accepted G319
regular slice, the registered positive periodic family contains genuinely inequivalent physical
initial geometries after quotienting the declared representation freedoms. The proof is carried by
the exact invariant `Q_R`, not by raw coordinates, not by finite array comparison, and not by an
implicit choice of physical scale or history.

G320_ACCEPTED__GENUINE_INITIAL_GEOMETRY_FREEDOM_UPHELD
