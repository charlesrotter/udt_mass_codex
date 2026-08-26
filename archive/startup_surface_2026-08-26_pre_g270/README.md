# G267-era startup surface archive index

This directory indexes the startup surface displaced by the G268--G270 refresh on 2026-08-26.
It is historical evidence, not current authority. Follow root `AGENTS.md`; root `LIVE.md` wins.

## Why this state was archived

At starting commit `87b8e666`, the active startup documents ended at G267 and told the next session
to test whether the provisional `(sech(delta),tanh(delta))` state was more than a bounded
reparameterization. G268 answered that question, G269 derived an independent metric null-transport
readout, and G270 separated intrinsic completed-pair normalization from ambient transported-screen
mismatch. Keeping the G267 question on the active surface would now restart closed work.

The root README also called the August 12 observational package “current work.” That package remains
valid bounded evidence, but it is not the current relational-geometry frontier.

## Exact recovery

The exact displaced files remain immutable in Git and can be read without reconstructing them:

```bash
git show 87b8e666:AGENTS.md
git show 87b8e666:LIVE.md
git show 87b8e666:HANDOFF.md
git show 87b8e666:CURRENT_RESEARCH_PROGRAM.md
git show 87b8e666:CURRENT_SCIENTIFIC_PREMISES.md
git show 87b8e666:CURRENT_SCIENTIFIC_PREMISES.tsv
git show 87b8e666:INDEX.md
git show 87b8e666:MEMORY.md
git show 87b8e666:README.md
git show 87b8e666:verify_current_scientific_premises.py
git show 87b8e666:tests/test_startup_surface.py
```

## Pre-refresh SHA-256 ledger

| Path | SHA-256 |
|---|---|
| `AGENTS.md` | `8f8b0b37e3b8dba8f54aa3e81349cb68e81cba33e76352098f7870f6cdfb4e78` |
| `LIVE.md` | `21f4054adb79eab770d7ffcbe596eaac3d34833f215a393f4133108c261ce449` |
| `HANDOFF.md` | `64c58c4d1c78508b31759b424f6c6a607549d7727e3c64cdea1ce798b87b6b31` |
| `CURRENT_RESEARCH_PROGRAM.md` | `54db912e6e732bec9f83e4dc8c83148e4e66c6505099b0d7cb04e2fd5ff33c32` |
| `CURRENT_SCIENTIFIC_PREMISES.md` | `41cb63726d44d5b55a35830be5ca32626f9eff6f5dc16a7dbb6fe10aa3c42454` |
| `CURRENT_SCIENTIFIC_PREMISES.tsv` | `ff547bb6108fd4dfba9b27f4a2fcba8e16d884ffd43dc712f9f2d487ceff1509` |
| `INDEX.md` | `0736bf5c167cf5a4a9aaab4d946cf149748ba02b837ab90b25c670fbe10e1e5a` |
| `MEMORY.md` | `cc8abb8e5324fc3fa2cb815a116d26494ff43d19014116773d273ca552885f64` |
| `README.md` | `938e7342ba7525541514126dc9c20bcd252369b70111234533a3a2a5b18410e5` |
| `verify_current_scientific_premises.py` | `b32b19501403ac9a08f8befe6ea1d59645cc06e58e0e75e0da3f18d9bd4199d1` |
| `tests/test_startup_surface.py` | `cfb1c89854d28c904e4cc5eb331cdf900695c3fbf6182f91f973460104c8defa` |

No scientific evidence was moved or regraded by this archive operation.
