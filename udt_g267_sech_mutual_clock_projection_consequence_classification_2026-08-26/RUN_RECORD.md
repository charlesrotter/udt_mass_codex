# G267 run record

Date: 2026-08-26
Branch: `grok`
Preregistration commit: `13132a6f`

## Commands

```text
python3 derive_sech_projection.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

## Result

```text
production exact checks       37
independent state cases       49
independent pair cases        192
independent assertions        1067
mutation catches              8
selected alternative          C
history rejections            0
```

No observation, fit, source, action, profile, `X_max`, protected package, ODE/PDE, or GPU process
was used. No long process is running.

## Fresh external review

Sealed GPT-5.4 review returned `ACCEPT_NO_REPAIRS`. The reviewer reproduced the registered no-write
package replay and retained alternative C. The sealed review could not independently inspect the
referenced Git commit chronology outside its intake; repository commit `13132a6f` remains that
chronology proof.
