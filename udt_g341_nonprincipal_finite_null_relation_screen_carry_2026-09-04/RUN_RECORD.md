# G341 run record

Date: 2026-09-04

## Frame

- question: classify the full nonprincipal finite directed-null relation on the exact G340
  Taub--Kasner spacetime;
- route: metric-led;
- dynamics: exact null geodesics and Levi-Civita transport;
- device: CPU; GPU unnecessary;
- dependencies: Python standard library only;
- physics inputs: only the frozen supplied metric, normal observers, endpoint/lattice query data,
  and prior typed G269/G298 relation definitions;
- outputs: three JSON evidence files plus this report package.

## Executions

1. `python3 -B -S derive_nonprincipal_relation.py`
   - result: `8992/8992`;
   - seed: `341001`;
   - coverage: 420 mixed local/rank/screen cases, 72 endpoint inverse cases, 120 principal-boundary
     cases, 96 mixed zero-shift cases, and 16 compact-lattice branch sets.
2. `python3 -B -S verify_nonprincipal_independent.py`
   - result: `4400/4400`;
   - seed: `341919`;
   - coverage: 320 direct metric cases, 44 slope-first inverse cases, and 144 direct Christoffel/RK
     transport cases;
   - no production import or result read.
3. `python3 -B -S run_catch_proofs.py`
   - result: `16/16` hostile mutations caught by the baseline validator.
4. `python3 -B -S verify_package.py`
   - result: `20/20` aggregate gates;
   - all three outcome scripts replayed with `UDT_NO_WRITE=1` and changed no package bytes.
5. `python3 verify_current_scientific_premises.py`
   - result: pass for the 323-row registry through G340 and the compacted startup surface.
6. `python3 -m pytest tests/`
   - first run exposed only pre-existing startup-surface growth;
   - redundant G313--G340 chronology was compacted without changing claims or guards;
   - final result: `220 passed, 1 expected xfail`.

No observation, fit, field equation, action, source, matter model, light-transfer law, physical
route population, absolute scale, or `X_max` was introduced. No long process remains running.
