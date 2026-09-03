# External Adversarial Review of Sealed G333 Intake

## Scope and evidence handling

I inspected only `/intake`, used `/work` for writable replay, and did not edit sealed evidence.

Authentication result:

- `REVIEW_MANIFEST.sha256` matches `sha256(REVIEW_MANIFEST.tsv)`:
  `0e494ee3fe884b63c57975ec6d2ceb9b0a70a58d6330956dbc4dd2db16e4065c`.
- `REVIEW_SCOPE.json` matches the top-level manifest entry:
  `11dc73862c3569c3c645091ba3f9ae006472b214248584bf816b5a76b3a6a07a`, 798 bytes.
- `python3 -S /intake/package/verify_review_intake.py /intake` passed: `G333 intake PASS: 36 payloads`.

Writable replay result in `/work/g333_review_copy`:

- `derive_initial_pair_response.py`: `6882` checks, `360` cases.
- `verify_initial_pair_response_independent.py`: `146` checks, `PASS`.
- `run_catch_proofs.py`: `9` mutations caught, `PASS`.
- `verify_package.py`: `83` aggregate gates, `PASS`.
- Replayed JSON outputs were byte-identical to the registered sealed outputs.

## Mathematical audit

### 1. G315 sign

With the sealed sign convention
`K_{ij}=-(1/2)L_n gamma_{ij}`,
raising one index gives
`K^i{}_j=-(1/2) gamma^{ik} L_n gamma_{kj}`.
Hence
`H^i{}_j := (1/2) gamma^{ik} L_n gamma_{kj} = -K^i{}_j`.
The claimed conclusion `H=-K^sharp` is correct. I found no sign flip.

### 2. Re-derivation from the G332 tensor

Write
`a=(C-b)/2`,
`eta=gamma(xi,.)`,
`P=xi tensor eta`.
Because `gamma(xi,xi)=1`, `P^2=P` and `P` is the rank-one orthogonal projector onto `span{xi}`.

From sealed G332:
`K = a gamma + b eta tensor eta`,
so
`K^sharp = a I + b P`,
and therefore
`H = -a I - b P`.

This yields:

- horizontal eigenvalue on `xi^perp`:
  `H_h = -a = (b-C)/2`;
- vertical eigenvalue along `xi`:
  `H_v = -a-b = -(C+b)/2`;
- difference:
  `H_v-H_h = -b`;
- trace:
  `tr(H)=2H_h+H_v=(b-3C)/2`;
- mean:
  `bar(H)=tr(H)/3=-C/2+b/6`;
- trace-free eigenvalues:
  `(b/3,b/3,-2b/3)`;
- trace-free squared norm:
  `2(b/3)^2+(-2b/3)^2 = 2b^2/3`.

For any unit spatial direction `v`, with `mu=gamma(v,xi)^2 in [0,1]`,
`P(v,v)=mu`, so
`H(v,v) = (b-C)/2 - b mu`.
This is the correct all-direction formula.

### 3. Both G332 branches and the Hamiltonian identity

The eigenvalues of `K` are
`k_h=(C-b)/2` with multiplicity 2 and
`k_v=(C+b)/2`.
Thus
`tau=tr(K)=(3C-b)/2`
and
`|K|^2 = 2 k_h^2 + k_v^2 = (3C^2-2Cb+3b^2)/4`.

Therefore
`tau^2-|K|^2 = (3C^2-2Cb-b^2)/2`,
so the Hamiltonian residual is
`R + tau^2 - |K|^2 = R + (3C^2-2Cb-b^2)/2`.
Using the sealed G332 branch relation
`(b+C)^2 = 2(R+2C^2-2Lambda)`,
equivalently
`b^2+2Cb+4Lambda-2R-3C^2=0`,
this reduces exactly to `2Lambda`.

This uses only `(b+C)^2`, so both square-root signs satisfy the identity. No branch-dependent sign defect appears.

### 4. Gaussian normal pair germ and transport condition

For the bounded normal-spatial pair germ, `h11 = gamma(v,v)`. Differentiating along `n` gives
`n(h11) = (L_n gamma)(v,v) + 2 gamma(L_n v, v)`.
Hence the claimed equality
`n(h11)=L_n gamma(v,v)`
is valid only when the extension of `v` is chosen so that `L_n v=0` at the evaluation point, equivalently `[n,v]=0` there.

Under that stated transport condition, together with the unit-slice normalization `gamma(v,v)=1`,
`n(h11)= (L_n gamma)(v,v) = 2 H(v,v)`.
Also in Gaussian normal form `h00=-1`, so `n(h00)=0`, and for
`Phi = -(1/2) log(-h00)`,
`n(Phi)=0`.

I do not find an error here, but the transport condition is load-bearing and must remain explicit.

### 5. Complete pullback versus terminal scalar

For this germ class, the scoped conclusion is valid:

- `n(Phi)=0` for every tested direction;
- `n(h11)=2H(v,v)` varies with `mu` whenever `b != 0`.

So the complete pair pullback contains first-jet information that the terminal scalar `Phi` does not.

An attempted generalization beyond this bounded germ would fail. For oblique, shifted, accelerated, null, or screen-mixed pair germs, `h00`, `h01`, and `h11` can carry different first-jet content, and `n(Phi)` need not vanish. The sealed package mostly respects that boundary and should keep doing so.

### 6. Hidden dependence and no-promotion boundary

I found no hidden dependence on orbit closure, Hopf topology, fibre period normalization, action, source, mass model, observational fit, scale selection, or `X_max` in the actual G333 derivation. The response formulas depend only on the local datum already present in G332: `gamma`, `K`, `xi`, `n`, `v`, `C`, `Lambda`, and the retained branch.

Global compactness and the unit-Killing hypothesis are used upstream in G332 to produce the admissible family on the strict-radicand stratum. They are not smuggled into G333 as orbit-period or Hopf-input data.

The sealed boundary is also mathematically appropriate: this is a first normal jet statement only. It does not prove stability, persistence, topology selection, occupancy, global history, matter, mass, scale, observation, or canon.

## Requested repairs

1. State explicitly, wherever `H(v,v)` is used, that this means the bilinear contraction `gamma(Hv,v) = (1/2)L_n gamma(v,v)`, not an unqualified endomorphism evaluation.
Scientific landing changed: no.

2. Promote the transport hypothesis to theorem-level text: `n(h11)=L_n gamma(v,v)=2H(v,v)` requires the chosen extension of `v` to satisfy `[n,v]=0` or `L_n v=0` at the evaluation point; otherwise extra terms appear.
Scientific landing changed: no.

3. Tighten the implementation-independence wording: the production derivation carries the analytic all-`mu` proof, while the independent verifier gives an implementation-distinct rotated-matrix and finite-difference confirmation on representative directions rather than a second continuum symbolic proof.
Scientific landing changed: no.

4. State plainly that the detached manifest seal establishes internal payload integrity and replay consistency, not third-party authorship or provenance beyond the sealed intake itself.
Scientific landing changed: no.

## Verdict

No refuting mathematical defect was found in the bounded claim as stated. The algebra, branch handling, projector decomposition, trace-free norm, all-direction response, Gaussian pair-germ jet, scoped pullback-versus-terminal-scalar comparison, and no-promotion boundary all survive adversarial review within the sealed premises.

ACCEPT_WITH_REPAIRS__G333_BOUNDED_FIRST_RESPONSE_RETAINED

