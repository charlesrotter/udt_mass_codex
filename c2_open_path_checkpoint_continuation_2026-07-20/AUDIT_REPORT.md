# C2 open-path checkpoint continuation audit

## Result first

The exact 22 order-four paths left open by the parent failed-basin audit were restarted from their
saved coefficients, continuation parameter, and tangent. All 22 returned within the registered
global budget:

- 7 reached the reduced equation at `lambda = 0`;
- 1 of those is the round gauge-fixed orbit and passes the higher-order/doubled-grid projection;
- 6 are nonzero reduced-basis stationary points, but all 6 fail both the higher-order projection and
  the direct full Bach-tensor gate by large margins, so they are truncation artifacts rather than
  promoted metric solutions;
- 11 remain time-limited, 2 reached the coefficient-norm safety wall, and 2 reached the absolute
  lambda safety wall;
- no registered closed-loop witness was observed.

The cumulative bounded search therefore has 177 certified round endpoints among the original 198
registered starts. Fifteen continuation paths remain open. Zero nonround full-Bach endpoint has been
observed. This is not a uniqueness theorem.

## Frame and premises

- `CONDITIONAL`: four-dimensional metric-only C2/Bach bulk dynamics, conditional on variation before
  physical scale selection.
- `CONDITIONAL_CANDIDATE_PREMISE`: the smooth-cap reciprocal-toric metric family and finite polynomial
  tile used by the parent search.
- `NUMERICAL_CONTROL`: the artificial homotopy `H(q,lambda)=F(q)-lambda F(q0)`. Its lambda is neither
  UDT depth nor physical time.
- `OPEN_NOT_TESTED`: unrestricted metric functions, physical boundary completion, nontoric topology,
  time-live dynamics, source, carrier, scale, and backreaction.

The registered controls were unchanged: CPU float64; exact Hessian refresh at least every two
accepted points; step range 0.002 to 0.10; 500 additional points, arclength 20, coefficient norm 5,
absolute lambda 5, and 900 seconds per path; endpoint raw residual 1e-9; higher projection 1e-7;
round norm 1e-6; full Bach promotion 1e-6.

## Exact observations

The raw return contains all 22 identities, 3,919 accepted states, one rejected corrector record, full
coefficient vectors, tangents, actions, residuals, and stopping data. Maximum saved/replayed homotopy
residual was `9.990852589680799e-10`. Maximum restart residual was
`8.846683385854703e-10`.

The surviving round endpoint has coefficient norm `1.4192160598672403e-12`, raw reduced residual
`1.8671079793799925e-10`, and higher-order residual `1.8692780302206613e-10`.

The six apparent nonround endpoints have reduced coefficient norms from about 0.758 to 4.503 and raw
reduced residuals below 1e-9. Their higher-order residuals instead range from
`1.3935095306339191` to `32.647766140492074`; their 64-node full Bach component maxima range from
`5.072513337501108` to `1316.2550636617357`, against a `1e-6` gate. They are therefore recorded as
`REDUCED_TRUNCATION_ARTIFACT_FULL_BACH_FAIL`, not as UDT branches.

## Independent verification

The verifier independently:

1. matched the exact 22 identities and restart states to parent SHA-256
   `1a8da008545be0a65d9f25899219a9334e4afd0692d5ef1bb7b67b95a817b2e8`;
2. replayed all 3,919 saved homotopy states with zero logged/recomputed residual difference;
3. recomputed all twelve 32/64-node full-Bach artifact profiles with zero logged difference;
4. checked three reduced-action gradients by centered finite differences, maximum scaled error
   `8.179778700419816e-09`;
5. passed 14 fail-closed mutation catches.

The first verifier invocation completed the expensive science groups but failed its own
`open_promoted_rejected` catch because it trusted the stored top-level status count without
recounting path rows. The verifier was corrected to recount both statuses and endpoint classes, and
the complete expensive replay was run again successfully. This correction history is preserved.

Package grade: `VERIFIED-WITH-CAVEATS`. There was no fresh external-model review, the physical
boundary remains open, and finite-tile evidence cannot establish global uniqueness.

## Does the nonround stable Hopfion help?

Yes, as a lead, with three meanings of *round* kept separate:

1. The banked Hopfion's spatial energy/configuration is full three-dimensional, toroidal, twisted,
   and nonround.
2. Its fixed round `S2` target remains a `POSIT`/conditional carrier premise; UDT has not derived that
   target, its section, its action, or its boundary completion.
3. Its spacetime/background metric was fixed rather than solved with carrier backreaction.

Thus a round base metric can coexist with a nonround topological texture. The new continuation makes
it less promising to obtain that texture merely by enlarging the same scalar metric coefficient
ansatz: six apparently convincing nonround reduced points fail the full tensor equation.

The sharper zoom-out lead is to ask whether the UDT metric's angular/null-direction geometry carries
a nontrivial section, connection, framing, or holonomy over an otherwise round base. That structure
could be the geometric place where linked Hopf topology lives. This is a targeted hypothesis, not a
derived carrier and not authority to import the existing round `S2` matter action.

## Four banking gates

1. Preregistered: **yes**.
2. Full space or bounded scope justified: **bounded exact 22-path universe; yes within registered
   path/time/arclength/safety limits; unrestricted space remains open**.
3. Independently verified on the load-bearing premise: **yes for saved states, action gradients, and
   full Bach rejection; no fresh external-model review**.
4. Every premise audited: **yes for this computation; physical boundary, complete action, native
   carrier/source, and global uniqueness explicitly remain open**.

Maximum conclusion: `EXTENDED_22_PATH_CONDITIONAL_C2_HOMOTOPY_CHARACTERIZED`; cumulative
`177_OF_198_CERTIFIED_ROUND`; six reduced artifacts rejected; fifteen paths remain bounded-open; no
full-Bach nonround endpoint observed; uniqueness and the native angular/topological bridge remain
open.
