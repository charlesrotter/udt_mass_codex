**Findings**

1. `ACCEPT_WITH_REPAIRS`: the preregistered certification contract was not fully met in machine-readable form. `PREREGISTRATION.md` requires an explicit `E/I/C/W` ledger with citations, but `ATTACHMENT_OWNERSHIP.tsv` has no separate `I` column and no per-leg citations, and `derive_attachment_ownership.py` hardcodes the negative `I/C` outcomes by class after a small set of phrase checks rather than recording candidate-by-candidate cited evidence.

2. The preregistered “run the current 233-row premise verifier before banking” step is not externally reproducible from the sealed intake. It is demanded in `PREREGISTRATION.md` and listed in `COMMANDS.md`, but `verify_current_scientific_premises.py` is not in the 35-file intake, so an external sealed-intake reviewer can only rely on the saved result, not rerun that gate.

**Adjudication**

`ACCEPT_WITH_REPAIRS`

The scientific landing survives on the sealed evidence. I verified all 34 scoped payload hashes, ran the three registered no-write replays with `PYTHONDONTWRITEBYTECODE=1`, and ran the package verifier; all passed. Reported bounded checks also held: 18 candidates, 7 direct-attachment classes, 3 matter/instrument composites, 0 native owners, 22/22 hostile catches, 0 observational values used, 0 fitted coefficients.

No source in the 12-source universe owns all four legs for any candidate. The intake consistently supports:

- evaluator ownership plus typed supplied objects,
- but not realized same-object physical attachment,
- and not an independently calibrated absolute datum.

The strongest evidence-bounded landing that survives is:

current UDT owns the evaluators and supplied geometric object types; no registered class owns an independent same-object absolute datum capable of breaking the G249 homothety; metric self-evaluation/internal cross-channel closure is circular or scale-cancelling; the seven direct classes require one supplied operational attachment; the three mass/density/energy composites require an additional matter/instrument law; no anchor value, history, branch population, fit, or observational outcome was selected.

So: no bounded scientific refutation found, but the result should not be banked as fully certified until the intake includes the preregistered cited `E/I/C/W` ledger and the rerunnable premise-verifier gate.
