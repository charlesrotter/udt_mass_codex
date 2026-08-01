# A3 blind adversarial verifier report

Date: 2026-08-01. Verifier verdict: **PASS-WITH-REQUIRED-AMENDMENTS**.
Scope source: `PREREGISTRATION.md` read first. I did not read `LIVE.md` or `HANDOFF.md` and
received no desired outcome. Verification used the uncommitted package in the `grok` worktree.
The mandatory fetch/pull could not update `.git/FETCH_HEAD` because this environment mounted it
read-only and denied escalation; local HEAD was `c54bfc2`.

## Operational record

- Ran `derive_angular_A3.py --stage gamma` twice, each as one bounded process pinned to CPU 0,
  with numerical-library thread counts fixed to one. Both exited 0.
- The two direct stdout streams were byte-identical; each equaled `DERIVATION_STDOUT.txt`.
  All 12 generated stdout/JSON/ledger artifacts had identical SHA-256 values across both runs.
- AST recount: 48 unique checks = 31 SUBSTANTIVE + 17 GUARD. Independent stage recount:
  alpha 12 = 8+4; cumulative beta 29 = 21+8; gamma 48 = 31+17.
- Independent purity audit found no floats, numerical solvers, numerical arrays, GPU imports,
  randomness, or background execution in the derivation.
- A throwaway in-package mutant changed C1a's expected period-row count from 20 to 19. The mutant
  printed the named guard failure and exited 1. Mutation artifacts were removed, and all landed
  derivation artifacts remained byte-identical to the pre-probe hashes.
- Preserved independent implementation: `VERIFIER_INDEPENDENT_CHECK.py`; machine findings:
  `VERIFIER_INDEPENDENT_RESULTS.json`.

## Independent result by internal stage

### Alpha — torus

The periodic-character and real-target conclusions survive. Exact torus characters carry
`(n,m) in Z^2`, but the amplitude homotopy contracts every real-valued mode. Positive factors
and SPD metric blocks are convex targets, so the same conclusion is independent of mode or jet
order. These integers are decomposition labels, not solution winding.

The large fiber shear is genuine presentation data. In a cap basis it is
`S_n=[[1,0],[n,1]]`; it fixes one cap line and preserves the other only at `n=0`. For each banked
unimodular cap basis `U`, I independently checked that `U S_n U^-1` is integral. Thus the torus
mapping-class seat is real, while its nonzero unipotent class cannot extend over both S3 caps.

One TB3-2 seat is missing from the landed census: for `A=dz+f dy` on a T2 stratum,
`H_y=exp(2*pi*i*f0*P_y/P_z)` is a native compact-fiber holonomy. It is invariant under the large
shear shift `f0 -> f0+n P_z/P_y` and ranges continuously in `U(1)`. No banked rule sets `H_y=1`,
and a globally real-lifted `f` gives zero winding of this holonomy around another registered
cycle; nonzero monodromy requires a separately stamped transition/completion class. Therefore
this missed seat does not produce quantization here, but it must be adjudicated explicitly.

### Beta — full S3

My parser recomputed all 104 cap rows: both slopes are primitive, every recorded determinant is
reproduced, and `|det|=1` in all 104 cases. The generic unimodular-basis argument above closes the
whole registered two-cap class, rather than only the finite representatives.

Independent exact integration gives Chern `-1`, transition winding `-1`, canonical normalized
Hopf representative `-1`, and base Euler number `2` in the landed orientation convention. These
are fixed bundle/base data. Nonzero Chern class blocks a global Hopf phase. A smooth global
connection perturbation changes curvature by an exact form, so it does not change Chern class.
An orthogonal coframe map, including a large framing class, leaves the metric exactly unchanged.

The completion stamp is correct: the bank identifies only the unimodular two-cap class as the
registered S3 completion; the same-closer/crease class is package-introduced, unregistered, and
outside that arena. No fixed S3 integer was transferred to either massive carrier.

### Gamma — fine detail

The no-cutoff conclusion survives for smooth regular fields because it is target-topological,
not a finite mode scan: real/affine section spaces contract linearly; positive and SPD sections
contract convexly; connection spaces within a fixed bundle are affine. Higher modes, higher jets,
and nodes cannot change those homotopy classes. Singular/distributional fields and exotic
non-Hopf completions remain correctly open.

The landed “complete” census nevertheless omits banked discrete presentation/character layers:
the conditional angular-mirror `Z2 x Z2`, the stratum m-involution `Z2`, and the orientation/degree
content of the `h` reparametrization slack. They do not quantize mass data, but TB3-1/TB3-2 must
list and classify them before claiming an exact complete discrete census.

## C-1 and massive-carrier attack

My own parser found 20 distinct six-field period-gate rows and exactly the six expected T3
branch-(a) completion rows, each with `no new cycle (B1a)` and `static verdicts VERBATIM`. The
mathematical mode-zero recovery is consistent. The executable C1a guard is too weak, however:
`angular_zero_pullback` is constructed as a tuplewise copy of `period_tuples` and compared to its
source, so content recovery is tautological and only the row count can fail. A generated
mode-zero snapshot/digest must be compared field-by-field to the bank.

Both named massive carriers are present under both spatial readings. Their source banks do not
certify a join to the registered two-cap S3 completion or a nonzero angular-live on-shell
solution. The fixed Chern/Hopf/Euler numbers and the presentation integers contain no `E0`,
`ell`, `k_mod`, `k10`, `C`, or response modulus, and no cited law couples them. Thus all such
data remain uncut. The two cyclic masslessness confinements in the period ledger also remain.

## Required amendments and maximum conclusion

1. Replace the F-B3 nonempty-cell guard with enforcement of every frozen per-row stamp: cell,
   both branch axes, mode layer, jet bigrade, and kill-scope/provenance lineage.
2. Add the omitted banked mirror/m-involution/h-slack discrete seats to TB3-1/TB3-2 and all
   headline “complete/exact list” prose.
3. Add the compact-fiber `U(1)` connection-holonomy seat, state its continuous status, and prove
   the registered real lift gives no variable integer absent a nontrivial transition class.
4. Harden C1a to compare an independently generated mode-zero projection with every banked row;
   the present copy-equals-source assertion is not content recovery.

Subject to those amendments, the landed core survives: fixed domain/presentation integers exist,
but no solution-dependent native integer or mass/modulus cut is derived on either certified
massive carrier; their two-cap-S3 coexistence remains OPEN. No physics conclusion follows.

## Same-verifier closure — 2026-08-01

**Verdict: CLOSED-PASS.** The four required amendments were re-audited in generated emissions,
not accepted from correction prose.

- The immutable round-one prefix remains byte-exact at SHA-256 `8756e582...f4980`; exactly one
  structured same-verifier closure section follows it. A one-byte prefix mutation is rejected.
- Two bounded CPU-0 gamma reruns exited 0. Direct stdout SHA-256 was identically
  `a103d324f8eda40315b301e892cb25dd93ddb91a358ddd2686dd844dbfbc3a69`; all 13 generated
  stdout/JSON/ledger/recovery artifacts were byte-identical.
- Independent AST recount is 57 unique checks = 37 SUBSTANTIVE + 20 GUARD. Stage banks are
  alpha 18/18, cumulative beta 35/35, cumulative gamma 57/57. Purity passed.
- F-B3 closes: the actual ledger has 15 fields and 126 rows = 84 alpha + 28 beta + 14 gamma;
  all 126 rows match the exact branch/mode/jet/theta/lineage stack. A throwaway emitted-mode-layer
  mutation triggered `F_B3_full_stamp_coverage: FAIL` and exit 1.
- The actual alpha ledger contains 12 rows each for mirror `Z2xZ2`, the general flip-and-shear
  `m` involution `Z2`, and `h` degree/orientation, with the projected/coordinate distinction exact.
- The actual alpha ledger contains 12 compact-fiber holonomy rows. Independent algebra confirms
  shear invariance, values `1,i,-1`, and zero winding for a globally periodic real lift; nonzero
  winding still requires separately owned transition monodromy.
- Independent source parsing reproduced every emitted C1 digest: 20 rows x 6 fields = 120/120.
  A throwaway mutation of one independently coded C1 field triggered the named C1a failure and
  exit 1.
- The 104 cap pairs, Chern/Hopf/Euler data, both massive-carrier scope rows, and completion bank
  were rechecked. Neither carrier inherits the two-cap S3 class; `E0`, `ell`, `k_mod`, `k10`,
  `C`, and response moduli remain uncut; angular-live on-shell coexistence remains OPEN.

Preserved closure implementation: `VERIFIER_CLOSURE_CHECK.py`; machine result:
`VERIFIER_CLOSURE_RESULTS.json` (**30/30 independent closure checks, zero failed**).

The correction closes the verifier's four amendments. Maximum result remains premise-scoped:
fixed domain/presentation integers and continuous holonomy exist, but no solution-dependent native
integer or mass/modulus quantization is derived on either certified massive carrier. No physics or
canon claim follows.
