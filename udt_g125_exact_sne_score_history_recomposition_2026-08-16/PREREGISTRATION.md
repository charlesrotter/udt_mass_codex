# G125 preregistration — exact SNe score/history recomposition

Date: 2026-08-16

## Whole bounded question

Combine, without refitting, G120's conditional outgoing SNe radius-frequency curve with G124's
exact finite-radius live junction. Determine:

1. whether the G117/G120 SNe numerical curve changes;
2. what exact combination of terminal depth, screen expansion, and endpoint-clock relation the
   curve constrains;
3. whether any individual component or complete physical history is selected.

This is a conditional interface recomposition, not a fit, profile search, history solve, or native
radiative-transfer derivation.

## Supplied and typed inputs

- `OBSERVED/CONDITIONAL`: processed catalog frequency coordinate `Z>1` and the frozen P1 curve.
- `IMPORTED_CONDITIONAL`: G120 transparent-transfer bridge `eta=1`, `epsilon=1/Z`.
- `DERIVED_CONDITIONALLY`: G119 `d_A=R` on the regular central-spherical point-observer query.
- `DERIVED_CONDITIONALLY`: G124
  `zeta=phi_pair-kappa_pair+chi_s`, `zeta=log Z`, and
  `kappa_pair=-log|K(R)|/2` on the same correctly matched query class.
- `OPEN`: physical complete history, query ownership, endpoint/source-clock ownership, native
  transfer, branch population, global completion, and `X_max`.

No Lambda-CDM distance, new coefficient, optimizer, raw-data replay, or observational outcome is
permitted.

## Preregistered exact candidates

1. `NUMERICAL_INTERFACE_INVARIANT__TOTAL_SCORE_ONLY_IDENTIFIED`: G120 remains exactly unchanged
   because it is already written in operational `Z` and `R`; G124 retypes it as one exact total-score
   constraint without selecting `phi`, `kappa`, or `chi` separately.
2. `INCONSISTENT_QUERY_OR_TRANSFER_TYPING`: the combined equations contradict G120 on their common
   declared domain.
3. `COMPONENT_OR_HISTORY_SELECTION`: the joined equations uniquely determine at least one terminal
   component or the full history without an additional premise.

## Exact tests

- symbolically invert `R(Z)=R_inf(1-Z^(-2/n))` on `Z>1`;
- derive `zeta(R)` and verify substitution both ways;
- combine with G124 to derive the score constraint and affine-rate family;
- prove the explicit family of decompositions retains functional freedom;
- verify `d_L=Z^2 R` is algebraically unchanged;
- check center and formal-limit behavior without promoting the limit to `X_max`;
- independently replay all load-bearing identities without importing production code.

## Certification and stop rule

The result is bankable only if exact production and independent checks pass, the source hashes are
frozen, and a fresh adversarial review confirms the type boundaries. If candidate 1 lands, stop:
do not rerun either SNe likelihood and do not launch a history solve. A numerical replay would be a
loop because the predicted `d_L(Z)` has not changed.

Maximum conclusion: an exact conditional retyping of the frozen SNe interface and its remaining
functional freedom. No physical-history, native-light, `X_max`, CMB/BAO, action, bootstrap, matter,
mass, or signalling conclusion.
