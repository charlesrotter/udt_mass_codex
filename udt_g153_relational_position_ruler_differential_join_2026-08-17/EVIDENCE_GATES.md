# G153 evidence gates

Date: 2026-08-17

| gate | status | evidence |
|---|---|---|
| preregistered | PASS | commit `18060cba` contains only preregistration and source manifest |
| source ownership | PASS | G137 leaves proper length open; G147 calls `rho n` a conditional non-displacement lift |
| finite/tangent type separation | PASS | G135 common-scale witness preserves `rho` while changing `L` |
| exact coframe decomposition | PASS | coordinate and orthonormal-frame calculations agree symbolically |
| live shift and time dependence | PASS | `beta`, `partial_tau phi`, and `partial_sigma phi` retained |
| open `X_max` realization | PASS | generic product-rule terms retained; fixed `X_max` is labelled conditional |
| reciprocal derivative | PASS | direct `chi(T,L)` derivative equals `sech(phi)^2 dphi` in both coordinates |
| common-scale covariance | PASS | response coefficients scale inversely to coframes; `d rho` is unchanged |
| independent replay | PASS | separate exact `Fraction` implementation and nonvacuous finite difference |
| optional-unit-ruler guard | PASS | explicitly additional and not adopted |
| physical promotion guard | PASS | proper length, history, `X_max` value, and completion remain open |

Fresh adversarial status: the initial concurrent snapshot returned `REPAIR_REQUIRED`; after the
open-`X_max` repair and artifact refresh, a fresh reread returned `FOLLOWUP_PASS` with no blocker.
