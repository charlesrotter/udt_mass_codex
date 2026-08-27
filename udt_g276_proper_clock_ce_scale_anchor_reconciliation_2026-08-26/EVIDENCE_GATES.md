# G276 evidence gates

| Gate | Result | Evidence |
|---|---|---|
| preregistered before outcomes | PASS | commit `e5fddc76` pushed before implementation |
| exact homothety weight | PASS | `derive_proper_clock_scale.py` |
| unique positive scale recovery | PASS | exact solve plus 20,000 rational cases |
| second-anchor consistency | PASS | 20,000 consistent and 20,000 inconsistent controls |
| independence / same-object enforcement | PASS | 40,000 rejected circular or mismatched records |
| `c_E` unit audit | PASS | `c_E` alone fails; `c_E tau_*` has length units |
| scale-blind state controls | PASS | `M`, `chi`, and same-weight ratios invariant |
| independent implementation | PASS | no production import or output read |
| hostile mutations | PASS | 6 implementation + 2 typed-scope catches |
| no-write replay | PASS | three registered scripts plus package verifier |
| premise audit | PASS | 259-row authority verified before banking |
| external adversarial review | ACCEPT WITH REPAIRS | science retained; one unit-control repair requested |
| R1 physical unit relabelling | PASS | fixed `C_bar`; independent length/time numeric units; 20,000 cases |
| repair-only external follow-up | ACCEPTED | bounded landing unchanged; no remaining R1 defect |

Current grade: `EXTERNALLY_REVIEWED_REPAIR_ACCEPTED__BOUNDED_LANDING_UNCHANGED`.
