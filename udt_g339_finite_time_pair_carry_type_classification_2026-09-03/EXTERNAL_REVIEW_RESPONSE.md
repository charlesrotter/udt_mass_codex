# External Review Response

## Scope and authentication

I treated `/intake` as sealed read-only evidence, copied only `/intake/g339` into `/work/g339_review/g339` for execution, and ran no networked or package-installing steps. The intake scope requires exactly that bounded mode of work: [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:1).

Authentication passed cleanly.

1. The detached seal for the manifest matched: `sha256(REVIEW_MANIFEST.tsv)=f7715b15bd5bb082681f7d2f6f7e92256170f7c9ded2eb1d78b6ffe3e1458539`, agreeing with [REVIEW_MANIFEST.sha256](/intake/REVIEW_MANIFEST.sha256:1).
2. The manifest listed 32 payload files, matching the scope declaration `payload_count_excluding_manifest_and_detached_seal = 32`: [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:11), [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:1).
3. The actual `/intake` file set had 34 files total, with the only unlisted files being `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`, which is consistent with the declaration.
4. Every listed payload hash verified `OK` against the sealed bytes in [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:2).

## Findings by severity

1. High: no repair-grade mathematical defect was found in the bounded G339 classification.
The core distinction is stated correctly in [EXACT_DERIVATION.md](/work/g339_review/g339/EXACT_DERIVATION.md:20). From
`gamma = diag(a_X^2, a_perp^2, a_perp^2)` with `a_X ~ T^(-1/3)` and `a_perp ~ T^(2/3)`, one gets
`H = (1/2) gamma^(-1) L_n gamma = diag(a'_X/a_X, a'_perp/a_perp, a'_perp/a_perp) = (1/(3T)) diag(-1,2,2)`,
so `tr H = 1/T`, `tr(H^2)=1/T^2`, and `det H = -4/(27 T^3)`, with dimensionless ratios `1` and `-4/27` as claimed in [EXACT_DERIVATION.md](/work/g339_review/g339/EXACT_DERIVATION.md:41). Those are properties of the supplied normal congruence, not of any chosen carry.

2. High: the transport identity and its signs are correct, and the report keeps the geometric term separate from the carry term.
For any spatial extension `V`,
`(L_n g)(V,V)=n[g(V,V)]-g([n,V],V)-g(V,[n,V])`,
hence
`(1/2) n[g(V,V)] = (1/2) (L_n g)(V,V) + g([n,V],V)`,
with the bracket term entering with a plus sign after solving for the raw derivative. That matches [EXACT_DERIVATION.md](/work/g339_review/g339/EXACT_DERIVATION.md:60). This is the key step that prevents confusion between metric deformation and basis transport.

3. High: the full declared `lambda` family is internally correct, and G339 distinguishes infinitesimal observer separation from a carried local ruler.
With `J_lambda^i(T)=J_0^i[a_i(T0)/a_i(T)]^lambda`, one has
`[n,J_lambda]^i = dJ_lambda^i/dT = -lambda (a'_i/a_i) J_lambda^i = -lambda H_i J_lambda^i`
and
`nabla_n J_lambda^i = dJ_lambda^i/dT + Gamma^i_{Ti} J_lambda^i = (1-lambda) H_i J_lambda^i`,
so [EXACT_DERIVATION.md](/work/g339_review/g339/EXACT_DERIVATION.md:86) is correct. `lambda=0` is the commuting connecting field for infinitesimally neighboring fixed-label normal observers; `lambda=1` is a parallel local ruler along one observer and is not the same relational object. The report does not conflate those two.

4. High: the finite-boost pair pullback, determinant, W1 regular stratum, interval classes, and `rho=2/3` silent-direction factorization check out.
Using `e0 = c n + s J`, `e1 = s n + c J` with `g(J,J)=G_lambda`, the pullback is
`h00=-c^2+G_lambda s^2`, `h01=(G_lambda-1) s c`, `h11=-s^2+G_lambda c^2`, and
`det h = -G_lambda (c^2-s^2)^2 = -G_lambda`, matching [EXACT_DERIVATION.md](/work/g339_review/g339/EXACT_DERIVATION.md:123). On `Delta_lambda = c^2-G_lambda s^2 > 0`, `L_sigma^2 = G_lambda/Delta_lambda`, so `m=sqrt(G_lambda)` and the stated W1 outputs follow. For `0 <= lambda < 1`, `rho=1` gives `u > tanh(|z|)^[3/(1-lambda)]`, `rho=0` gives `u < coth(|z|)^[3/(2(1-lambda))]`, and mixed `0<rho<1` gives two clock-null crossings around `u=1`. At `rho=2/3`, `G_lambda-1 = (y-1)^2(y+2)/(3y)` with `y=u^[2(1-lambda)/3]`, so first-order silence is exact at `u=1` but not persistently silent for `lambda<1`. This matches [EXACT_DERIVATION.md](/work/g339_review/g339/EXACT_DERIVATION.md:168).

5. High: G339 correctly distinguishes clock-null pair boundaries from spacetime or pair-plane degeneracy.
At `Delta_lambda=0`, the carried clock vector becomes null, but `det h = -G_lambda < 0` remains Lorentzian as long as `G_lambda>0`, so the pair plane is not degenerating. Since these crossings occur at finite positive `T`, they are not the Taub/Kasner curvature singularity at `T=0`. That separation is stated correctly in [EXACT_DERIVATION.md](/work/g339_review/g339/EXACT_DERIVATION.md:159) and is consistent with the inherited finite-positive-`T` regularity from [udt_g338.../EXACT_DERIVATION.md](/intake/sources/udt_g338_explicit_taub_pair_finite_time_readout_2026-09-03/EXACT_DERIVATION.md:217).

6. High: the rotating, parallel/Fermi, and principal-axis accelerated controls are signed correctly, and quiet local frames are not misread as zero curvature.
For geodesic `n`, Fermi-Walker along `n` equals parallel transport, so the `lambda=1` endpoint is exactly the nonrotating local-ruler control. For orthonormal rotating carry with `nabla_n V = Omega V`, `Omega^T=-Omega`, one gets `[n,V]=Omega V - H V`; then `g(Omega V,V)=0` and the raw norm change cancels despite nonzero `H`, as in [EXACT_DERIVATION.md](/work/g339_review/g339/EXACT_DERIVATION.md:195). For principal `e_i`, with constant rapidity `U = c n + s e_i`, `S = s n + c e_i`, the formulas `nabla_U U = H_i s S` and `nabla_U S = H_i s U` are correct, so `S` is Fermi-Walker transported along the accelerated worldline while the local Gram matrix stays `diag(-1,1)`: [EXACT_DERIVATION.md](/work/g339_review/g339/EXACT_DERIVATION.md:212). This is local-frame quietness, not flatness and not vanishing of `H`.

7. Medium: the `GL(2)` whitening statement is mathematically correct and, within the bounded report, not overstated.
Any Lorentzian `2x2` form can be whitened pointwise to `diag(-1,1)` by an invertible basis change, so no nonconstant scalar of the raw pair-component matrix alone is invariant under arbitrary smooth pair-frame congruence. G339 explicitly does not infer from this that metric deformation disappears; instead it says the typed pair plus its declared carry recovers `L_n g` via transport subtraction: [EXACT_DERIVATION.md](/work/g339_review/g339/EXACT_DERIVATION.md:241). That is the correct conclusion.

8. Low: the sealed package has one packaging completeness limitation, but it does not invalidate the bounded mathematics.
[SOURCE_SCOPE.tsv](/work/g339_review/g339/SOURCE_SCOPE.tsv:1) includes a preregistered hash for `LIVE.md`, but that file is not present in the sealed intake payload set [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:2). Because of that, the aggregate verifier falls back to the weaker sealed-mode check `sealed_source_absence_is_explicit` instead of replaying every `SOURCE_SCOPE.tsv` hash from local files: [verify_package.py](/work/g339_review/g339/verify_package.py:112). This is a provenance-packaging limitation, not a failure in the bounded carry classification itself.

9. Low: the independent verifier is implementation-distinct, but it is not premise-distinct.
It does not import production code or read production results, which is good: [verify_carry_type_independent.py](/work/g339_review/g339/verify_carry_type_independent.py:78). But it still accepts the declared `lambda` carry ansatz and the same spacetime as inputs, then reconstructs consequences directly from the 4D metric. That is sufficient for this bounded tile, but it is not evidence for generic accelerated congruences, arbitrary screen-mixing, or finite-separation observer populations.

## Completeness audit

The package remains bounded exactly where it says it is bounded: [COMPLETENESS_MAP.md](/work/g339_review/g339/COMPLETENESS_MAP.md:5), [STATUS_LEDGER.tsv](/work/g339_review/g339/STATUS_LEDGER.tsv:1).

Untested or still open:

1. Generic accelerated congruences beyond the three principal-axis Fermi controls.
2. Full nonprincipal screen/mixing sectors, null pair germs, caustics, and rank-changing pair planes.
3. Finite observer separation between distinct worldlines as opposed to infinitesimal connecting fields and local two-plane data.
4. Any physical observer population, occupancy, topology selection, stability statement, or matter/source/action completion.
5. Any claim that the metric physically selects one carry, one congruence, one scale, or one `X_max`.

These are genuine completeness limits, not contradictions in the bounded result.

## Replay results

I ran the registered aggregate replay from the writable copy using the exact no-write command path documented in [COMMANDS.md](/work/g339_review/g339/COMMANDS.md:1):

`UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_package.py`

Result:

1. Aggregate verifier passed `15/15`.
2. Production exact checks passed `2182/2182`.
3. Independent direct-4D reconstruction passed `16155/16155`.
4. Hostile mutation catches passed `12/12`.
5. Replay changed no bytes in the copied package.

I found no circular import of production code into the independent route, no network/package dependence, and no evidence that the main bounded conclusion is vacuous. The strongest caution is narrower: the aggregate verifier contains several string/packaging checks, and in sealed mode it cannot replay the missing `LIVE.md` source hash. That does not overturn the mathematical result.

## Strongest bounded landing

The strongest defensible bounded conclusion is:

1. On this one exact Taub/Kasner spacetime with the supplied geodesic normal congruence, G339 correctly separates infinitesimal fixed-label observer separation from parallel/Fermi local-ruler transport.
2. Raw pair components, W1 readouts, and clock-null boundaries depend on the declared carry and clock/ruler calibration.
3. The carry-corrected metric deformation of the supplied normal congruence is recoverable from the typed pair-plus-carry state and has the carry-independent eigenvalue pattern `(-1,2,2)/(3T)`.
4. Neither quiet local frames nor pointwise `GL(2)` whitening remove the underlying metric deformation.
5. No physical carry, observer population, or occupancy statement is selected by this tile.

No repair requests are required for the bounded carry-type classification as stated.

ACCEPT_G339_BOUNDED_CARRY_TYPE_CLASSIFICATION
