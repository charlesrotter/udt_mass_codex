# Global Functional-Degree-of-Freedom and Constraint-Rank Audit — Preregistration

Date: 2026-07-26

Base: `bb5949a5a2bce59a10e5f8227ceeef8615f3d8af`

Mode: metric-led, CPU-only, source-bounded. No action, carrier, density law, branch preference,
empirical fit, PDE/time-live solve, GPU work, canonization, or repository reorganization.

## Whole question

Across the complete registered local metric/coframe inventory, seven off-shell realization branches,
and twelve global completion classes, determine exactly what is already fixed, what is gauge or a
derived readout, and what remains free. Decide whether the remaining closure problem is:

1. one missing functional relation;
2. several independent bulk or boundary relations; or
3. a still-unselected response law plus global completion data.

This audit counts **configuration freedom and constraint rank**. It does not count propagating
physical polarizations, because no complete native UDT action, constraint propagation system, or
initial-value problem has been derived.

## Bounded universe

The exact objects are frozen in `UNKNOWN_UNIVERSE.tsv`, `CONSTRAINT_UNIVERSE.tsv`,
`COMPLETION_UNIVERSE.tsv`, and `SOURCE_SCOPE.tsv`. The audit includes:

- a generic regular four-dimensional Lorentz metric, represented either by ten symmetric metric
  components or by a sixteen-component coframe with local-Lorentz presentation gauge;
- signed `phi` in every registered relationship to the metric: derived readout, independent scalar,
  reciprocal coframe character, supplied projector, hard constraint/multiplier, two-stage bridge,
  and independent-connection branch;
- the supplied `2+2` base/screen/shifts chart only as a complete regular local coordinate chart, not
  as an intrinsically selected split;
- boundary traces, normal jets, moving/glued/capped completions, topology, connection, holonomy,
  physical representative, and scale as separately typed data;
- the metric-native toric connection and curvature only as downstream objects when their toric
  premises are supplied; and
- all twelve registered completion classes, including singular, nonorientable, rank-changing,
  nonintegrable, and conditional reciprocal-toric alternatives.

No finite audit can count arbitrary global four-manifolds or all smooth function spaces. “Complete”
means every declared object, constraint, local realization branch, and registered completion class
is represented, while uncounted global moduli remain explicitly uncounted.

## Counting language

The result is a typed signature rather than a single scalar:

- `F4[n]`: `n` arbitrary scalar functions of four coordinates;
- `F3[n]`: `n` arbitrary scalar functions on a three-dimensional boundary/interface;
- `F1[n]`: `n` arbitrary one-dimensional profiles;
- `C[n]`: `n` continuous constants/moduli;
- `Z[...]`: discrete, integral, combinatorial, or topological choices;
- `G4[n]`: `n` local gauge functions of four coordinates;
- `U[...]`: functional/global data whose dimension is not supplied and may not be invented;
- `O[...]`: downstream object not evaluable before missing parent data exist.

Counts from different dimensions or kinds may not be added into one number. A branch may have an
exact local count and an uncounted global completion simultaneously.

## Rank rules

The frozen `RANK_RULES.tsv` governs every result. In particular:

- `10 F4` metric components minus `4 G4` coordinate presentation functions gives a generic local
  metric configuration quotient signature of `6 F4`; this is not a propagating-mode count;
- equivalently, `16 F4` coframe components minus `6 G4` local-Lorentz and `4 G4` coordinate
  presentation functions gives the same `6 F4` metric signature;
- an independent scalar `phi` adds `1 F4`; a metric-derived `phi` adds none but requires the missing
  derivation map;
- regular signature and positivity are open inequalities and have rank zero;
- no local conformal function is removed unconditionally. The strong local-CSN quotient is audited
  only as a challenged conditional branch; a constant common rescaling removes at most one global
  modulus;
- abstract reciprocal weights reduce from two positive channels to one relative character, but
  impose zero rank on the spacetime metric until a physical soldering/slot map is derived;
- definitions, Bianchi/exterior-calculus identities, projectors, curvatures, holonomies, and readouts
  derived from a metric/coframe are not additional independent fields and are not counted twice;
- finite-cell ontology, `c`, `G`, and bootstrap wording impose no point-local functional rank unless
  an explicit sourced equation is present; and
- a boundary trace condition may remove boundary trace data without removing a bulk function.

## Premise ledger

| premise | stamp | use |
|---|---|---|
| complete regular 4D Lorentz metric/coframe arena | `REGISTERED / CONDITIONAL ARENA` | local configuration census |
| ten-amplitude regular chart | `DERIVED CHART COMPLETENESS WITH SUPPLIED 2+2 SPLIT` | exact local rank control |
| signed `phi` semantics | `DERIVED / REGISTERED` | branch-aware scalar census |
| observer-frame Reciprocity and reciprocal character | `FOUNDATIONAL / DERIVED ABSTRACTLY` | internal comparison rank only until soldered |
| finite-cell structure and static seal | `FOUNDATIONAL / STATIC-BRANCH CONDITIONAL` | domain and boundary rank only |
| measured `c` and `G` | `OBSERVED ANCHORS` | dimensional calibration, not a local equation |
| strong local CSN | `CHALLENGED_OPEN` | separate conditional sensitivity row only |
| constant common rescaling | `WORKING PRESENTATION POSSIBILITY` | at most one global modulus |
| physical representative, `X_max`, mass, density, bootstrap closure | `OPEN` | recorded as unevaluable outputs |
| toric angular split and integral circle character | `CONDITIONAL` | downstream connection/Maxwell cross-check only |
| `S2` carrier, matter action/source, EH or `C2` action | `POSIT / CONDITIONAL / OPEN` | excluded from rank reduction |
| GR/Maxwell field equations | `REFERENCE ONLY` | no UDT constraint rank |

## Falsification and certification contract

The audit fails closed if any of the following occurs:

1. a frozen source hash changes;
2. any of the seven realization branches or twelve completion classes is omitted or duplicated;
3. unlike function spaces, constants, discrete choices, and gauge freedoms are collapsed into one
   integer;
4. configuration quotient freedom is called propagating physical degrees of freedom;
5. a regularity inequality is counted as an equation;
6. strong local CSN is subtracted unconditionally;
7. abstract Reciprocity is counted as a metric constraint before soldering;
8. finite-cell ontology, `c`, `G`, or bootstrap prose is counted as a local field equation;
9. a boundary trace condition is counted as removing a bulk scalar function;
10. a metric-derived projector, connection, curvature, holonomy, or readout is double-counted as an
    independent field;
11. `F=dS` and the identity `dF=0` are counted as two dynamical constraints;
12. a supplied `U(1)`/Maxwell action, current, or charge is imported as native UDT rank;
13. the conditional `FC12` two-profile ansatz is promoted to the generic metric family;
14. an uncounted global modulus is assigned an invented finite dimension;
15. one completion is preferred by smoothness, familiarity, particle resemblance, or desired
    physics;
16. a rank statement lacks its field inventory, constraint source, domain, and independence status;
17. an algebraic rank is promoted to a complete global solution count; or
18. a same-code replay is presented as independent verification.

Every forbidden promotion must have an exercised catch-proof. The load-bearing local ranks and
branch census must be recomputed by a structurally independent implementation. A fresh adversarial
review must inspect source lineage, double counting, conditional quotients, boundary-versus-bulk
typing, and the final conclusion.

## Maximum allowed conclusion

At most:

`REGISTERED_CONFIGURATION_FREEDOM_AND_CONSTRAINT_RANK_CHARACTERIZED`.

The audit may identify a smallest missing interface only if every surviving freedom is traced to it.
It may not claim an action, equation of motion, propagating mode count, selected completion, matter
emergence, bootstrap closure, mass law, physical scale, or canon.

