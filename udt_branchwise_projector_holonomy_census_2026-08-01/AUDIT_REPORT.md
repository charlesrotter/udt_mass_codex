# Branchwise intrinsic-projector and reduced-holonomy census — audit report

Date: 2026-08-01  
Frozen base: `156b8a57d2e4ce65a588e5f7c2d82d0bd1f88334`  
Preregistration commit: `b390d75`  
Grade: **VERIFIED-WITH-CAVEATS; COMPLETE FROZEN-REGISTRY CENSUS; FRESH EXTERNAL SEMANTIC REVIEW OPEN**

## Result first

The branch census found a genuine positive geometric joint in one complete registered
**off-shell configuration family**.

In each of the six frozen twisted-`S3` configurations C01--C06, the complete metric intrinsically
recovers:

- a global timelike clock line;
- a twist-selected global spacelike ruler line;
- the sign-independent rank-one ruler projector `P_n` in the positive rank-three bundle
  orthogonal to the clock; and
- its unique rank-two screen complement.

The new exact calculation then finds nonzero **relative projector curvature** at the registered
north event in all six configurations:

```text
C01  lambda=-2     634/625
C02  lambda=-1     2509/2500
C03  lambda=0      1
C04  lambda=1/2    10009/10000
C05  lambda=1      2509/2500
C06  lambda=2      634/625
```

A separate standard-library `Fraction` implementation reconstructs the Cartan connection and every
fraction exactly without importing SymPy or production functions.

This closes one antecedent of the prior conditional response theorem: on these named complete
configurations, the metric supplies the rank-one reduction rather than requiring it to be inserted.
The projector has nontrivial path/loop geometry, so the previous `L2` path-strain and `L4` relative-
area identities are nonvacuous there.

The maximum new conclusion is:

```text
DERIVED_CONDITIONAL_ON_NAMED_REGISTERED_COMPLETE_OFFSHELL_CONFIGURATION:
INTRINSIC_GLOBAL_RULER_PROJECTOR_AND_NONZERO_RELATIVE_PROJECTOR_CURVATURE_SOMEWHERE.
```

It is **not** an on-shell branch, a universal projector principle, carrier emergence, action
selection, stability, or matter.

## Why ambient full holonomy does not erase the result

Two different claims must remain separate.

1. The metric reconstructs `P_n` at every point of the complete configuration and supplies the
   projected metric connection on its positive rank-three bundle.
2. Ambient Levi-Civita transport does not preserve the full reciprocal grading.

Both are true. The frozen twisted configurations retain full sampled `so(1,3)` holonomy and the
exact nonparallel component

```text
(nabla_E0 X_lambda)^0_1=-3/25
```

for every tested `lambda`. Thus the full lift stays path-labelled rather than endpoint-only. The
new relative term is precisely the curvature associated with the changing projector; it is not
ambient curvature relabeled and it is not reduced ambient holonomy.

The `lambda=+1`, constant-depth, twist-free round product is the complementary control: its
clock-versus-all-space projector is parallel under spatial `so(3)`, hence `DP=0` and the relative
response vanishes. It has no nontrivial depth or twist-selected ruler.

## Complete census rather than a positive-result filter

The discovery universe was fixed before content inspection:

- 11,456 tracked frozen-base paths;
- 11,150 text-eligible paths;
- 239 tracked package audit reports; and
- 297 top-level groups.

The broad preregistered content scan produced 4,461 literal hit paths across 280 groups. A mention
was never equated with a branch. Every hit, report, and group has exactly one disposition:

- 239/239 report dispositions;
- 280/280 group dispositions; and
- 4,461/4,461 path dispositions, including all 283 mixed root hits individually.

Thirty-seven source packages reached source-level six-gate review. Their content was consolidated
into eighteen nonduplicative object/branch cases in `BRANCH_OBJECT_GATE_LEDGER.tsv`. The retained
outcomes include:

- the positive complete twisted family and its rank-two complement;
- the parallel zero-response product control;
- a complete unique-clock-only control;
- local nonnull-`dphi` projectors and null/zero failure strata;
- local spectral projectors with operator and eigenvalue degeneracies;
- toric shortest lines that become an unordered set at ties;
- unselected seal involutions;
- the celestial null-direction fiber without a section;
- a supplied reciprocal plane that is conditional rather than metric-selected;
- full-holonomy and isotropy no-projector controls;
- larger-isometry plane ambiguity; and
- eleven structural completion types that lack complete `(g,phi)` witnesses.

No branch was removed because it failed to resemble a particle, Hopf map, or desired action.

## The six gates

For C01--C06, the ruler projector and complement have the following exact grade:

| Gate | Ruling |
|---|---|
| intrinsic definition | pass, conditional on the named complete metric configuration |
| rank and uniqueness | pass for an unoriented rank-one ruler line and its unique rank-two complement |
| smooth local continuation | pass globally on the smooth frozen `R x S3` configurations |
| transport/holonomy | projected covariant connection passes; ambient parallel preservation fails |
| global descent | pass on the global Maurer--Cartan `S3` configuration |
| relative curvature | nonzero at P00 in all six configurations |

This split ruling is deliberate. “Covariant intrinsic field” is not rounded up to “parallel
holonomy reduction.”

## Relation to carrier and action

The positive projector is a line in the metric-derived positive rank-three clock complement. It is
not identified with:

- the conditional celestial `S2` fiber;
- a selected `S2` section;
- the posited fixed round particle carrier; or
- a physical species.

The previous exact path/loop theorem may now be evaluated on this projector family, but it still
does not prove that UDT integrates those responses as `L2+L4`, selects their relative coefficient,
or uses the result as matter. Selecting C01--C06 because they make that action available would be
circular and is forbidden by the preregistration.

## Parent replay caveat

The three direct parent holonomy/reduction verifiers pass. The twisted intrinsic-pair production
derivation and its independent full-Riemann/Torch reconstruction also pass. Its monolithic July 27
verifier now stops at a historical source-manifest guard because it pinned an older
`CURRENT_SCIENTIFIC_PREMISES.tsv` (`c05647...`) while the frozen census base contains the later
premise registry (`69342e...`). No frozen parent file was rewritten. This audit therefore replays
all 1,270 admitted source files by their frozen Git blobs and hashes, which passes, and records the
current-path guard failure rather than concealing it.

## Evidence

- exact SymPy 1.13.1 derivation: 32/32 checks;
- independent no-SymPy `Fraction` replay: 26 checks and six exact fraction matches;
- branch/object verifier: 19/19 exercised mutation catches;
- 1,270/1,270 frozen six-gate source blobs hash-replay;
- six frozen native-action manifests: 127 members / 133 package paths;
- current premise verifier: 18 guards, 9 startup controls, 754 dispositions;
- navigation: 1,114 current artifact paths and 101 frontier targets resolve; and
- repository tests: `70 passed, 1 xfailed`.

## Four banking gates

1. **Preregistered:** yes, at `b390d75`, before outcome classification or new projector-curvature
   calculation.
2. **Full or bounded scope:** complete for the frozen registered source/discovery universe and the
   eighteen consolidated object families. It is not all smooth Lorentzian metrics, future
   higher-jet/nonlocal selectors, or an on-shell solution space.
3. **Independently verified:** yes for the load-bearing exact algebra and frozen-source identities.
   A fresh external semantic reviewer has not been authorized for this new package, so the grade
   remains `VERIFIED-WITH-CAVEATS` rather than settled.
4. **Every premise audited:** yes in `PREMISE_LEDGER.tsv`, `OUTCOME_PREMISE_AUDIT.tsv`, the
   branch/object ledger, and the negative/control rows.

## Next gate

After an authorized fresh adversarial review, the justified metric-led next test is a deformation-
neighborhood persistence map around all C01--C06 centers: release the registered screen and profile
degrees of freedom without an action, and determine where intrinsic uniqueness, global descent,
and nonzero relative curvature persist or cross degeneracy walls. Only after that map should an
independently stated on-shell/bootstrap admissibility rule be tested against the survivors.

No GPU work, carrier/action adoption, physics labeling, canonization, or repository reorganization
was performed.
