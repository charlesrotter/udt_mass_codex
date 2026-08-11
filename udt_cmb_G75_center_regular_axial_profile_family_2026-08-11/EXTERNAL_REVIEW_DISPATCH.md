# Cold external review — G75 center-regular axial profile family

You are a fresh adversarial mathematical reviewer. You may inspect only the sealed intake defined
by `REVIEW_MANIFEST.tsv`. Do not edit files, continue the research, infer a physical CMB profile,
or inspect anything outside the intake.

## Starting point

The supplied stationary axial control metric is

```text
ds^2 = -A(x)c_E^2 dt^2 + R^2 dx^2/A(x)
       + R^2 x^2(dtheta^2 + sin^2(theta)dpsi^2)
       + 2 R c_E h(x) sin^2(theta) dt dpsi,
A(x)=1+a x^2, h(x)=x^2 q(x^2), 0<=x=r/R<=1.
```

`c_E` is an observed clock/ruler calibration. `R>0` is symbolic. This is a complete 4D metric only
inside the declared stationary axial envelope; it is neither the generic ten-function coframe nor a
physical cosmology.

Put `s=x^2`. G75 preregisters every primitive integer coefficient ray

```text
p(s)=c0+c1*s+c2*s^2,
ci in {-2,-1,0,1,2},
gcd(nonzero |ci|)=1,
first nonzero coefficient >0.
```

It claims there are 49 rays. For each, it normalizes by

```text
M=max_[0,1]|p|, q=epsilon*p/M,
epsilon in {1/20,1/5,1/2,1},
a in {-1/4,0,1/4},
```

and adds three `q=0` controls, for 591 profiles. Negative `q` is represented analytically by the
axial reflection `psi -> -psi` and is not claimed to be physically selected away.

G74, included only as parent evidence, found a `3/6/12` whole-sky split in a different frozen family;
the twelve blocked rows were not `C2` at the center. G75 claims to be a new center-regular family,
not a repair of those rows.

## Required review

1. Verify every sealed hash before interpreting the package. Note that the G75 source manifest
   froze the then-current premise registry at base `ac01381b`; `POST_BANK_NAVIGATION.md` explains why
   the separately transmitted current registry now has a different, later hash.
2. Reconstruct the primitive coefficient rays from the definition. Confirm or refute 49 unique rays
   and 591 unique profiles without trusting the production generator.
3. Derive the exact Cartesian-center form of the lapse, radial spatial block, and axial cross term.
   Decide whether every frozen profile is genuinely smooth at `r=0`; distinguish coordinate from
   metric degeneracy.
4. Derive the full metric signature on `0<=x<=1`, including the time-angle Schur complement, polar
   axes, center limit, all three lapse controls, and all four amplitudes.
5. Independently recompute each shape's exact normalization, center onset, endpoint-zero order,
   interior roots and multiplicities, extrema, sign changes, behavior class, and stratum code.
   Report exact census totals and any mismatch row by row.
6. Test the claimed reflection equivalence. State precisely what is chart-derived, what is metric-
   isometric, and what remains physically unselected.
7. Audit the production, independent replay, package verifier, hash verifier, repository gates, and
   catch proofs for circularity, shared-code false independence, loose checks, or mutations that do
   not exercise the load-bearing claim.
8. Audit scope and premise language. In particular, reject any promotion from the frozen quadratic
   atlas to all smooth profiles, from the stationary axial envelope to the generic complete metric,
   or from mathematical strata to physical CMB regimes.
9. Supply runnable exact algebra or a clean independent script for all finite claims. Give precise
   hypotheses for the center and signature derivations.

## Required return

Return exactly one primary landing from the preregistered list, then:

- a concise premise/type ledger;
- exact reconstructed counts;
- center-regularity and signature adjudication;
- row-level corrections, if any;
- independence/catch-proof assessment;
- scope and maximum justified conclusion;
- SHA-256 of your raw response and any runnable verifier you create.

Do not derive a sky response, fit peaks, activate a source ensemble, select `R` or `X_max`, invoke
bootstrap, derive an action or matter source, or inspect the protected stopped native-on-shell draft.
