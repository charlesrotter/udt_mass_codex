# G197 startup-surface audit

## Initial defects

The pre-repair startup surface was scientifically recoverable but increasingly distracting:

- the 181-row registry was described by one test as 180 rows;
- `LIVE.md`, `HANDOFF.md`, the program, premises guide, and index exceeded their readability budgets;
- repeated G129--G196 chronologies obscured the dependency spine;
- `B,Q,S=0` could falsely imply that all coframe blocks vanish;
- G190's local `d_A(Z)` descent was described too broadly across turns/caustics;
- observational and active relational-frontier entries were mixed in `INDEX.md`.

## Repairs

- Compressed the live surface to the G166--G196 dependency spine and G197 gate.
- Corrected the bounded coframe wording to metric-fixed `B,Q`, with `S=0`.
- Stated that `d_A(Z)` descends only on monotone, noncaustic pieces.
- Made G176's non-derived working status and the `phi_control`/`Phi` distinction prominent.
- Made G190--G196's chosen-family, supplied-germ, standard-evaluator, and evidence ceilings explicit.
- Split the active relational frontier from observational interfaces in `INDEX.md`.
- Replaced duplicate token-census guards with semantic current-spine guards.
- Updated the startup test to 181 exact registry rows and expanded its chronology range.
- Preserved the exact pre-repair surface through git commit `8462797d`; the archive pointer is
  `archive/startup_surface_2026-08-21_pre_g197/README.md`.

## Mechanical result before dress rehearsal

- premise verifier: PASS, 181 rows;
- startup tests: 38/38 PASS;
- startup files: within registered line, word, and maximum-line budgets;
- `git diff --check`: PASS;
- protected local payloads: untouched and unstaged.

Zero-context rehearsals are recorded separately after the final G197 landing is routed into the
startup surface.
