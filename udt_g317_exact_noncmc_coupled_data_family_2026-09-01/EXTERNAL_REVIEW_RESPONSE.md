# External Review Response — G317

I reviewed only the sealed intake at `/intake`, copied the package to a writable ephemeral directory under `/work`, and reran the four registered `python3 -S` commands there. I did not inspect any repository, protected package, or non-intake material, and I did not edit sealed evidence files.

## 1. Authentication and scope

`REVIEW_MANIFEST.sha256` matches `REVIEW_MANIFEST.tsv`, and every manifest-listed payload matched both the sealed byte count and sealed SHA-256. The replayed outputs in `/work` matched the sealed package outputs byte-for-byte for:

- `DERIVATION_RESULT.json`
- `INDEPENDENT_VERIFICATION.json`
- `CATCH_PROOF_RESULT.json`
- `PACKAGE_VERIFICATION_RESULT.json`
- `NONCMC_FAMILY_ATLAS.tsv`

The sealed scope file and source-scope ledger are consistent with the stated boundary: bounded review of the constant-`psi`, flat marked-`T3`, diagonal-TT, one-coordinate non-CMC ansatz only; no topology, `Lambda`, scale, source, matter/mass, observation, or history selection; no promotion into a global UDT theorem; no protected-package use.

## 2. Registered command replay

In `/work/g317_review_0mSYWS` I ran:

```text
python3 -S derive_exact_noncmc_family.py
python3 -S verify_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
```

All four passed. Reported counts reproduced exactly:

- production assertions: `1637`
- independent assertions: `1191`
- hostile catches: `29/29`
- family instances: `48`
- atlas rows: `14`

## 3. Independent derivation audit

### 3.1 Vector equation

With flat seed metric `\bar\gamma_{ij}=\delta_{ij}` and `W=w(x)\partial_x`,

\[
\bar D_k W^k = w', \qquad
(\bar L W)^{ij}
= \operatorname{diag}\!\left(\frac43 w',-\frac23 w',-\frac23 w'\right).
\]

Only the `x`-component of the divergence survives:

\[
\bar D_j (\bar L W)^{xj} = \partial_x\!\left(\frac43 w'\right)=\frac43 w''.
\]

The G316 momentum equation with constant `\psi=p` becomes

\[
\frac43 w'' = \frac23 p^6 \tau'
\quad\Longrightarrow\quad
2w''=p^6\tau'.
\]

Integrating once,

\[
w'=\frac{p^6}{2}\tau + c.
\]

Periodicity of `w` forces zero mean of `w'`, hence

\[
0=\langle w' \rangle = \frac{p^6}{2}\mu + c,
\qquad
\mu=\frac1{2\pi}\int_0^{2\pi}\tau(x)\,dx,
\]

so

\[
w'=\frac{p^6}{2}(\tau-\mu).
\]

That mean subtraction is necessary. Omitting it gives a nonzero mean for `w'` unless `\mu=0`, so periodic `w` generally fails.

### 3.2 Scalar residual and exact classification

Write

\[
\beta=-\frac\alpha2+d,\qquad \gamma=-\frac\alpha2-d.
\]

Using `w'=(p^6/2)(\tau-\mu)`, the total conformal trace-free tensor is

\[
\bar A_{TT}+\bar L W
= \operatorname{diag}\!\left(
\alpha+\frac23 p^6(\tau-\mu),
\beta-\frac13 p^6(\tau-\mu),
\gamma-\frac13 p^6(\tau-\mu)
\right).
\]

Its squared norm expands to

\[
|\bar A_{TT}+\bar L W|^2
= \frac32\alpha^2 + 2d^2 + 2\alpha p^6(\tau-\mu) + \frac23 p^{12}(\tau-\mu)^2.
\]

Since `\bar R=0` and `p` is constant, the scalar equation divided by `p^5` reduces to

\[
\mathcal F(x)=
\left(\frac43\mu-2\alpha p^{-6}\right)\tau
-\frac23\mu^2 + 2\alpha p^{-6}\mu
-\left(\alpha^2+\beta^2+\gamma^2\right)p^{-12}
-2\Lambda.
\]

This matches the sealed formula. Because `\tau(x)` is assumed nonconstant, pointwise vanishing requires the `\tau` coefficient to vanish:

\[
\alpha=\frac23 p^6\mu.
\]

Substituting that value cancels the mean terms and leaves

\[
0=-2d^2p^{-12}-2\Lambda,
\qquad
\Lambda=-d^2p^{-12}.
\]

Defining `q=dp^{-6}` gives `\Lambda=-q^2`. Inside this ansatz that condition is both necessary and sufficient. I found no coefficient, conformal-power, or sign error in this reduction.

### 3.3 Negative sign boundary

The negative relation is ansatz-specific. It comes from the exact flat, constant-`psi`, diagonal-TT, one-coordinate reduction above and from no broader theorem. The sealed package repeatedly keeps that boundary explicit and does not validly support promotion to a global sign law.

## 4. Direct physical reconstruction

Using `A^i{}_j = p^{-6}(\bar A_{TT}+\bar L W)^i{}_j`, the classified total tensor gives

\[
A^i{}_j = \operatorname{diag}\!\left(\frac23\tau,\ q-\frac13\tau,\ -q-\frac13\tau\right).
\]

Adding `(1/3)\tau\delta^i{}_j` yields

\[
\gamma_{ij}=p^4\delta_{ij},
\qquad
K^i{}_j=\operatorname{diag}(\tau,q,-q).
\]

This reconstruction is correct.

For the Hamiltonian constraint, `{}^{(3)}R=0` because `\gamma` is flat and constant, while

\[
K=\tau,\qquad K_{ij}K^{ij}=\tau^2+2q^2.
\]

Hence

\[
{}^{(3)}R+K^2-K_{ij}K^{ij} = -2q^2 = 2\Lambda
\]

iff `\Lambda=-q^2`, matching the classified relation.

For the momentum constraint,

\[
K^{ij}-\gamma^{ij}K = p^{-4}\operatorname{diag}(0,q-\tau,-q-\tau).
\]

Its only nonzero entries are `yy` and `zz`, but those depend only on `x`, so their divergences differentiate in `y` and `z` and vanish. The `xx` entry is identically zero. Therefore

\[
D_j(K^{ij}-\gamma^{ij}K)=0.
\]

This is a genuine direct check, not a circular reuse of the conformal residual.

## 5. Genuine non-CMC coupling

The family is genuinely non-CMC and coupled. If `\tau` is nonconstant, then `\tau'` is nonzero somewhere, so the vector source `(2/3)p^6\bar D^i\tau` is active somewhere. Also `w'=(p^6/2)(\tau-\mu)` cannot vanish identically unless `\tau\equiv\mu`, contrary to the nonconstant hypothesis. So the longitudinal correction is genuinely activated by registered nonconstant profiles.

## 6. Weyl/tide audit

Using

\[
E^i{}_j = {}^{(3)}R^i{}_j + K K^i{}_j - K^i{}_k K^k{}_j - \frac23\Lambda\delta^i{}_j
\]

with `{}^{(3)}R^i{}_j=0`, `K^i{}_j=\operatorname{diag}(\tau,q,-q)`, and `\Lambda=-q^2`, I rederived

\[
E^i{}_j
= \operatorname{diag}\!\left(
\frac23 q^2,\ \tau q-\frac13 q^2,\ -\tau q-\frac13 q^2
\right).
\]

The `-2\Lambda/3` term is necessary: omitting it destroys trace-freeness.

For the magnetic Weyl part, with flat constant `\gamma` and diagonal `K`, the only nonzero spatial derivative of `K` is `D_xK_{xx}`. In the curl expression every surviving term would require a repeated `x` inside the Levi-Civita tensor, so the magnetic part vanishes on the initial slice.

Consequences:

- `q=0` gives `\Lambda=0` and `E=B=0`, so this is a zero-initial-tide branch.
- `q\neq0` gives `E^x{}_x=2q^2/3\neq0`, so this is a nonzero invariant electric-tide branch.

That split is correct.

## 7. Local flatness caveat

The package does not overclaim here. The `q=0` branch is presented only as conditionally locally flat, contingent on the already-caveated local uniqueness theorem. I found no uncaveated global completion claim and no valid basis in the sealed evidence for one.

## 8. `q` sign symmetry

Under the marked `y \leftrightarrow z` axis relabelling,

\[
\operatorname{diag}(\tau,q,-q)\mapsto \operatorname{diag}(\tau,-q,q),
\]

so `q` and `-q` are interchanged. The same swap interchanges the last two electric-Weyl eigenvalues. The sign of `q` is therefore not selected inside this symmetric diagnostic family.

## 9. Completeness within the declared ansatz

Within the declared ansatz, the classification is complete in the advertised sense:

- arbitrary smooth periodic nonconstant `\tau(x)` remains free;
- `p>0` remains free;
- `q\in\mathbb R` remains free;
- the translation/conformal-Killing kernel in `w` remains visible;
- both `q=0` and `q\neq0` branches remain visible.

The package does not validly establish anything beyond that bounded sector, but it does not claim to.

## 10. Scope, provenance, and smuggling audit

I found no sealed evidence that:

- changes the metric, reciprocal kernel, angular cancellation, or observational interface;
- imports source/action/matter/mass/observation inputs;
- selects a topology, scale, physical `X_max`, source, or history;
- promotes the torus, constant `\psi`, diagonal TT seed, one-coordinate profile, `q`, or `\Lambda` relation into a UDT premise;
- uses protected packages named in the sealed `LIVE.md` protection list.

The source-scope ledger is consistent with the bounded dependency story: G317 rests on G315 constraints, G316 conformal construction, the current premise registry, and adoption records already inside the sealed intake.

## 11. Defects found

No algebraic, geometric, completeness-within-scope, or provenance defect in the sealed evidence refutes the bounded landing.

One review-limit caveat remains: because repository access was prohibited by the sealed protocol, I could authenticate the included preregistration and evidence-gate records but could not independently reconstruct Git ancestry beyond the sealed intake itself. That limits provenance depth, not the bounded scientific derivation.

## 12. Conclusion

The sealed package supports the bounded claim exactly as stated and only within the stated ansatz. The core load-bearing items all survive adversarial rederivation: vector equation, mean subtraction, scalar residual, necessity/sufficiency of `\alpha=(2/3)p^6\mu` and `\Lambda=-q^2`, direct physical reconstruction, genuine non-CMC coupling, Weyl zero-tide/tidal split, `q\leftrightarrow -q` axis symmetry, and explicit nonpromotion of bounded choices into a global theorem or physical selection.

G317_ACCEPTED__EXACT_NONCMC_INTERLOCK_AND_TIDE_SPLIT_UPHELD
