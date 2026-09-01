# External Adversarial Review of G315

Date: 2026-09-01
Reviewer mode: fresh zero-context adversarial scientific review
Evidence scope: sealed intake only at `/intake`

## 1. Intake authentication

I authenticated the sealed top-level review files before reading package payloads.

- `REVIEW_MANIFEST.sha256` verifies `REVIEW_MANIFEST.tsv` with SHA-256
  `0fb22f759047334bbe56d323faf026df4a8c2aa5e958d8ce47dce4dcb3c17495`.
- Every manifest payload hash matched the value listed in `REVIEW_MANIFEST.tsv`.
- Every manifest payload byte count matched the value listed in `REVIEW_MANIFEST.tsv`.

That includes `REVIEW_SCOPE.json`, all 22 `package/*` payloads, and all 12 `sources/*` payloads.
I did not inspect anything outside `/intake` except a writable replay copy under `/work` and the
report I am writing here.

## 2. Instruction compliance

I read `/intake/package/EXTERNAL_REVIEW_REQUEST.md` and followed its constraints.

- I did not edit any evidence file under `/intake`.
- I did not browse, search, download, install packages, or use networked Python.
- I did not access any repository or protected package.
- I did not select a data set, history, `Lambda`, topology, scale, physical `X_max`, action,
  source, matter law, observation, or bootstrap rule.
- I treated PDE existence and propagation results only as conditional mathematical methods.

## 3. Registered replay

I copied `/intake/package` to `/work/g315_review_20260901_141254` and ran exactly the four
registered commands there:

```text
python3 -S derive_data_interface.py
python3 -S verify_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
```

Observed replay results:

- production PASS: 72 exact assertions; 15 interface rows
- independent PASS: 89 exact assertions
- hostile checks PASS: 17/17 caught
- package verification PASS

I also compared the regenerated output artifacts against the sealed package copies. The following
files were byte-identical to the sealed intake versions:

- `DERIVATION_RESULT.json`
- `INDEPENDENT_VERIFICATION.json`
- `CATCH_PROOF_RESULT.json`
- `PACKAGE_VERIFICATION_RESULT.json`
- `DATA_INTERFACE_ATLAS.tsv`

## 4. Independent scientific rederivation

### 4.1 Active equation and bounded scope

Within the bounded G312/G313 arena, the active equation under review is

\[
R_{ab}=\Lambda g_{ab}, \qquad d\Lambda=0
\]

on each connected regular region. The package consistently presents this as a bounded conditional
vacuum equation, not as a unique-universe selector.

### 4.2 Spacelike constraints

With signature `(-,+,+,+)` and convention

\[
K_{ij}= -\frac12 \mathcal L_n \gamma_{ij},
\]

the Gauss equation and the `nn` Einstein projection give

\[
{}^{(3)}R + K^2 - K_{ij}K^{ij} = 2\Lambda.
\]

The Codazzi equation and `ni` projection give

\[
D_j(K^{ij}-\gamma^{ij}K)=0.
\]

So the package's Hamiltonian and momentum constraints are correct for the stated convention.

### 4.3 Trace and trace-free split

Writing

\[
K_{ij}=A_{ij}+\frac13\tau \gamma_{ij}, \qquad A^i{}_i=0, \qquad \tau=K,
\]

one gets

\[
K_{ij}K^{ij}=A_{ij}A^{ij}+\frac13\tau^2,
\]

hence

\[
{}^{(3)}R+\frac23\tau^2-A_{ij}A^{ij}=2\Lambda.
\]

Also

\[
K^{ij}-\gamma^{ij}K = A^{ij}-\frac23\tau\gamma^{ij},
\]

so

\[
D_jA^{ij}-\frac23 D^i\tau=0.
\]

This is only a decomposition of the constraint surface. It does not make arbitrary seed data
lawful. The package states that boundary correctly.

### 4.4 Evolution equation and `-\Lambda \gamma_{ij}` sign attack

For the stated convention, the metric evolution law

\[
(\partial_t-\mathcal L_\beta)\gamma_{ij}=-2NK_{ij}
\]

is consistent, and the `K_{ij}` evolution law

\[
(\partial_t-\mathcal L_\beta)K_{ij}
=-D_iD_jN + N\left({}^{(3)}R_{ij}+K K_{ij}-2K_i{}^kK_{kj}-\Lambda\gamma_{ij}\right)
\]

has the correct `-\Lambda\gamma_{ij}` sign.

Flat positive slicing control:

- take `N=1`, `beta=0`, `R^(3)_{ij}=0`, `K_{ij}=-H\gamma_{ij}`, `Lambda=3H^2`
- then `K=-3H` and `K_i{}^kK_{kj}=H^2\gamma_{ij}`
- RHS becomes `(3H^2-2H^2-3H^2)\gamma_{ij}=-2H^2\gamma_{ij}`
- LHS is `\partial_tK_{ij}=-2H^2\gamma_{ij}`

Round positive bounce control:

- at the bounce, `K_{ij}=0`, `N=1`, `beta=0`
- the spatial slice is round with `{}^{(3)}R_{ij}=2X^{-2}\gamma_{ij}` and `Lambda=3X^{-2}`
- RHS becomes `(2X^{-2}-3X^{-2})\gamma_{ij}=-X^{-2}\gamma_{ij}`
- LHS is the bounce value of `\partial_tK_{ij}=-X^{-2}\gamma_{ij}`

Both controls fail if the sign is flipped to `+\Lambda\gamma_{ij}`. The package's sign is correct.

### 4.5 Generic local count

The package's `12-4-4=4` statement is acceptable only as a generic local phase-space count:

- `\gamma_{ij}` and `K_{ij}` contribute 12 hypersurface functions
- 1 Hamiltonian plus 3 momentum constraints remove 4
- 4 coordinate freedoms remove 4 gauge functions
- 4 physical phase-space functions remain

That means two local configuration modes plus their initial rates. It does not mean four
configuration modes, and it is not a global moduli theorem. The package states those caveats
explicitly and correctly.

### 4.6 Gauge versus physical data

The package correctly keeps lapse, shift, coordinates, null parametrization, and null-normal
normalization as gauge presentation choices rather than UDT-selected physical initial data.
I found no in-scope place where these were promoted to physical data.

### 4.7 Characteristic/null interface

For a twist-free affinely parametrized null generator `\ell` with

\[
\chi_{AB}=\frac12\mathcal L_\ell q_{AB}, \qquad
\theta=q^{AB}\chi_{AB}, \qquad
\sigma_{AB}=\chi_{AB}-\frac12\theta q_{AB},
\]

the Raychaudhuri equation gives

\[
\mathcal L_\ell \theta
= -\frac12\theta^2 - \sigma_{AB}\sigma^{AB} - R_{ab}\ell^a\ell^b.
\]

Under `R_{ab}=\Lambda g_{ab}` and `g(\ell,\ell)=0`,

\[
R_{ab}\ell^a\ell^b = \Lambda g_{ab}\ell^a\ell^b = 0.
\]

So the same-null equation reduces to

\[
\mathcal L_\ell \theta = -\frac12\theta^2 - \sigma_{AB}\sigma^{AB}.
\]

This is the correct bounded statement. `\Lambda` cancels only because it drops out directly from
the `\ell\ell` Ricci projection. That does not imply Weyl or shear independence; the shear term
remains explicit.

For cross-normalized null normals `g(\ell,k)=-1`,

\[
R_{ab}\ell^a k^b = \Lambda g_{ab}\ell^a k^b = -\Lambda.
\]

The package states this correctly. It also keeps the characteristic-data claim bounded:
compatible screen/shear data and corner data may be supplied, while expansion and related
connection quantities obey a transport hierarchy. It does not promote one null sheet to a complete
formalism-independent data set.

### 4.8 Constraint propagation and PDE scope

The package keeps Bianchi-based constraint propagation and local Cauchy/characteristic existence in
the right logical place: conditional mathematical methods for lawful regular data. It repeatedly
disclaims any global completeness, caustic-free completion, singular-boundary theorem, or new UDT
postulate. That matches the review request.

### 4.9 Reciprocal kernel provenance

I found no evidence that G315 adds an independent evolution residual, profile, metric
modification, angular rule, observational transfer, or physical scale. The package consistently
places the reciprocal/pair evaluator downstream of a supplied metric development and supplied germ.

## 5. Provenance and scope audit

The sealed provenance chain is coherent within `/intake`.

- `SOURCE_SCOPE.tsv` cites only bounded predecessor materials relevant to G310, G312, G313, and
  G314, plus `LIVE.md` and `CURRENT_SCIENTIFIC_PREMISES.tsv`.
- `PREMISE_LEDGER.tsv` correctly records Universal Reciprocity/DDR and the G312 premises as
  owner-adopted provisional premises rather than derived or canonized laws.
- `STATUS_LEDGER.tsv` correctly keeps G315's outputs bounded: lawful data interface, conditional
  propagation, no global selector, no scale calibration, no metric/kernel/interface change.
- The protected packages named in `LIVE.md` are not present in `SOURCE_SCOPE.tsv`.

One boundary should be stated carefully: because the instructions forbid repository access, the
claimed preregistration commit ancestry can only be assessed as attested by sealed package records,
not independently reconstructed from VCS state here. That is a provenance limit of the allowed
review scope, not an in-scope scientific refutation.

## 6. Findings

I found no equation-sign defect, counting defect, characteristic-scope defect, downstream-kernel
defect, or in-scope provenance violation sufficient to overturn the bounded landing.

The package does the key things the request demanded:

- it derives the correct ADM constraints and the correct `-\Lambda\gamma_{ij}` evolution sign
- it distinguishes lawful constrained data from arbitrary seeds
- it reports the local `12-4-4=4` count in the correct phase-space sense
- it keeps lapse/shift and null parametrization as gauge
- it derives same-null `\Lambda` cancellation only from `Ric(\ell,\ell)=0`
- it keeps characteristic completeness and PDE theorems conditional and local
- it leaves the reciprocal kernel downstream and unchanged

## 7. Verdict

G315_ACCEPTED__CONDITIONAL_DATA_INTERFACE_UPHELD
