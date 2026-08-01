# A3 correction layer — blind-verifier required amendments

Date: 2026-08-01. Status: **IMPLEMENTED, DERIVATION-SIDE SELF-AUDITED, AND SAME-VERIFIER
CLOSED-PASS**. This is an append-only overlay on the original return and blind verifier record.
It does not modify the frozen preregistration, rehearsal, round-one verifier prefix, or round-one
independent checker/results. The verifier appended exactly one structured closure section.

## Scope and immutable records

The only scientific conclusion retained is the verifier's maximum conditional conclusion: fixed
domain/presentation integers survive, but no solution-dependent native integer or mass/modulus cut
is derived on either certified massive carrier; the carrier-to-two-cap-`S3` joins remain OPEN. No
physics conclusion follows.

Immutable SHA-256 checks:

- `PREREGISTRATION.md`: `fbd16a3d33ae5c2b71c9940fb3c2f07b700997a891b5dd44f861a05df97e2fa7`
- `VERIFIER_REPORT.md` immutable round-one prefix:
  `8756e582303d79311113e110e0fd59010f8e181a94e1ab4902ee4be64a3f4980`
- `VERIFIER_INDEPENDENT_CHECK.py`: `ff151fa8750e0bd6a2e7995468e03f209c9d5581c037b50cd2b28bf5f9fb6466`
- `VERIFIER_INDEPENDENT_RESULTS.json`: `3eaf1e3b59d8625dc6e209c3d4df8ca94e5289e0832af7466389da5876d6fed6`

## AM-1 — F-B3 full per-row scope enforcement

`ANGULAR_A3_LEDGER.tsv` now has 15 explicit fields. In addition to the original content, each row
names both branch axes, the linear-time branch, its stage-specific mode layer, jet/bigrade layer,
absent-`theta` status, and seat-specific kill/provenance lineage. The generator refuses an unknown
seat. `F_B3_full_stamp_coverage` compares every generated field to the registered exact value; a
nonempty generic stamp is insufficient.

The branch semantics are explicit: each row is one spatial-reading branch and aggregates the two
named lock readings only because the banked A1/T2 result says angular content is a spectator and
the verdict is identical on both. Neither reading is selected.

## AM-2 — omitted discrete presentation/character seats

Every alpha cell × spatial-reading pair now has seven seats rather than three:

1. native real fields;
2. `T2` character modes;
3. large `zeta` chart shear;
4. compact-fiber connection holonomy;
5. conditional angular mirrors `Z2xZ2`;
6. lawful-stratum `m` involution `Z2`;
7. `h` reparametrization orientation/degree.

Exact checks show the two mirror matrices square to identity and commute; the banked general
flip-and-shear `m -> (-m_y,m_z-2g_yz*m_y/g_yy)` squares to identity; and the two affine circle-map
representatives have degrees `+1` and `-1`. These are conditional character or presentation
components. They are not solution windings and contain no mass/modulus symbol. Under the projected
spatial reading the `m` content is slack pairing, not an independent pointwise character cut.

## AM-3 — compact-fiber connection holonomy

For `A=dz+f dy` on the torus stratum,

    H_y = exp((2*pi*i/P_z) integral_y f dy),
    H_y(mode zero) = exp(2*pi*i*f0*P_y/P_z).

The large shear changes `f0` by `nP_z/P_y`, multiplying `H_y` by `exp(2*pi*i*n)=1`. Values at
`f0=0`, `P_z/(4P_y)`, and `P_z/(2P_y)` are exactly `1`, `i`, and `-1`, so the seat is continuous
and not forced trivial. If the `y`-average of `f` is a globally real periodic lift in `z`, its
holonomy angle returns exactly and the winding is zero. Nonzero winding requires
`Delta fbar=wP_z/P_y`, i.e. separately owned transition/completion monodromy. No such monodromy is
adopted here.

## AM-4 — independent C1a recovery

The old tuplewise copy comparison was removed. The generator now contains a separate frozen
cycle × family recovery construction: four families crossed with three common cycle templates,
then four cyclic-completion rows and four J11 rows. It compares all six fields of every recovered
row with the bank and writes `C1_MODE_ZERO_PERIOD_RECOVERY.tsv`. Result: **120/120 field
comparisons PASS** across **20/20 rows**.

## Staged rerun and self-audit

- Alpha: **18/18** = 14 substantive + 4 guard; 84 rows.
- Beta cumulative: **35/35** = 27 substantive + 8 guard; 112 rows.
- Gamma cumulative: **57/57** = 37 substantive + 20 guard; 126 rows.
- Exact SymPy only; one CPU; no floats, numerical solvers, array backend, randomness, GPU, or
  background process.
- `python3 verify_current_scientific_premises.py`: **PASS** (18 premise guards, 9 startup
  controls, 754 candidate dispositions). Controlling registry rows: G08 keeps the complete 4D
  angular/mixing extension open; G09 keeps the `S2` carrier a posit; G13 keeps `U(1)` selection,
  source, current, and charge open; G18 keeps mirror closure working/bridge-only rather than
  derived bedrock.
- Two full gamma replays exited 0 and were byte-identical for all 13 derivation-generated
  ledger/JSON/transcript/recovery artifacts; their direct stdout streams were also identical.
- Executed catch-proofs reject a mutated lock-reading stamp, an unknown cell, an unknown
  seat/lineage, a mutated independently coded C1 field, and a forced-trivial holonomy claim.
- Repository tests: **70 passed, 1 xfailed** (the documented `test_no_habit_pins` xfail), no
  unexpected failure.
- `DERIVATION_MANIFEST.sha256` covers derivation-owned artifacts only. It intentionally excludes
  the frozen preregistration/rehearsal and all verifier-owned artifacts, preventing this correction
  from silently re-authoring the verifier record.

Same-verifier closure replay: **30/30 PASS**, including a catch-proof that a one-byte mutation of
the immutable round-one report prefix is rejected. Current verifier-owned hashes are recorded in
the closure section of `VERIFIER_REPORT.md` and its machine result.

Four gates after this correction: preregistered **YES**; full frozen smooth scope **YES**;
independently verified **YES, CLOSED-PASS after amendments**; premises **YES, derivation-side and
adversarially audited**. Status is **VERIFIED-WITH-CAVEATS**, not canon and not physics.
