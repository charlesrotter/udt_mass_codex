# Audit report — rebuilt reciprocal-kernel release candidate

## Result

The rebuilt kernel is internally coherent. G87, G89, G90, and G92 now join without adding a new
mechanism or double-counting angular mixing:

```text
(B,Q,S,Y,Z) -> h -> phi_pair -> c_eff/c_E.
```

Ambient endpoint transitions and terminal pair transitions each compose and reverse exactly on a
matched middle state, but remain correctly type-distinct. Every complete channel affects the
terminal depth at a generic point. The recovered `mu_lock` belongs to the ambient transition and is
not appended after the terminal readout.

## SNe readiness

The kernel is ready for a **conditional geometry-level SNe query**: a supplied complete metric and
observer/null-screen realization can return both redshift and Jacobi angular distance. It is not
ready for an unconditional/full SNe validation because neither the physical complete history nor a
native flux/source law is owned.

The previous SNe result remains a useful observed compatibility anchor, but it was a retyping of a
frozen scalar profile, not a replay of this rebuilt kernel. G79 proves the stronger same-geometry
redshift-plus-angular-distance calculation for one chosen control, not for a selected universe.

## Evidence

- primary exact symbolic harness: 16/16 checks;
- implementation-independent standard-library route on the same three witnesses: 12/12 checks;
- exact terminal character and ambient composition; terminal matrix residuals `1e-90` and `3e-90`;
- five nonzero exact `delta h` and `delta phi_pair` channel sensitivities;
- nine hostile interface/semantic mutations caught;
- source-level SNe interface ledger completed without fitting.

## Four gates

1. Preregistered: **PASS**.
2. Full or bounded: **PASS for the declared local/interface scope**; physical histories, global
   branches, singular strata, and flux/source physics are excluded.
3. Independently verified: **PASS WITH CAVEATS**; a fresh sealed reviewer rebuilt the rational
   algebra in memory. The packaged no-import route reuses the primary witness states.
4. Premises audited: **PASS**; evaluator, ambient arrow, terminal arrow, redshift, Jacobi area, flux,
   and physical ownership are separately stamped.

## Grade

`EXTERNALLY_VERIFIED_WITH_CAVEATS__NO_FIT_GEOMETRY_REPLAY_JUSTIFIED`. This is not canon and not a
cosmological validation.

## Next justified rung

Preregister one no-fit complete SNe geometry replay:

1. choose a declared complete metric/history family without using SNe outcomes;
2. use one typed observer/null-screen query over its endpoint range;
3. compute `z` and `d_A` from the same geometry;
4. compare the resulting relation with the frozen P1 anchor only afterward;
5. keep the flux/source law explicitly conditional unless separately derived.
