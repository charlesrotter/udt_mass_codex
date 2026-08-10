# Audit report — R17 stationary connection subloci and ownership

Date: 2026-08-10

## Result

Inside the supplied smooth regular stationary R17/W01 family on `R x S3`, the complete projected
normal connection has now been classified into its flat, base-descended, and holonomy classes.

The exact global result is:

```text
curvature horizontal through the pair fibers  iff  phi is constant.
```

For a constant profile, write `x=exp(2phi)>a` and

```text
B_lambda(x)=2-x^(1-lambda)+a^2 x^(-(1+lambda)).
```

Then:

- complete flatness is exactly `B_lambda(x)=0`;
- an abstract parallel quotient over `S2` exists exactly when `B_lambda(x)` is an integer;
- descent as the inherited Hopf tangent bundle would require `B_lambda(x)=2`, which gives `x=a`,
  the excluded slice-degeneracy boundary for nonzero twist;
- complete holonomy on simply connected `R x S3` is trivial on the flat roots and full `SO(2)`
  everywhere else. No proper nontrivial reduced-holonomy class exists.

At `a=1/64`, flat regular root counts across `lambda=(-2,-1,0,1/2,1,2)` are

```text
(1,1,1,1,0,2).
```

All actual C01--C06 `F_GENERIC` witnesses are nonconstant. They are therefore nonhorizontal,
nonflat, nondescended, and have full `SO(2)` complete holonomy. This coarse classification does not
erase their different curvature components or the already banked special roles of
`lambda=-1,0,1`.

## Ownership ruling after external correction

No owner is shown by the manifest-backed current authority and included core R17/W01 sources for
any special locus above. The current registry explicitly leaves that selection open, and every
included R17/W01 source package treats the configurations as off shell.

The package's tracked-repository literal census remains useful supporting local evidence, but it
was generated as an audit output and was not one of the 16 frozen upstream sources in the sealed
external-review manifest. The original repo-wide wording is therefore withdrawn rather than
promoted beyond the independently reviewed fence.

The `R x S3` completion is load-bearing for compactness and for the holonomy dichotomy. It
classifies the options; it does not choose one.

## Evidence gates

1. **Preregistered:** yes, commit `d2ca6c7c` before derivation.
2. **Full or bounded:** full for smooth stationary profiles in all six supplied regular twisted
   `lambda` strata on `R x S3`, plus the two registered controls; time-live, null, rank-changing,
   and other branches excluded.
3. **Independently verified:** production SymPy derivation plus independent standard-library
   calculus and bisection, 16/16 checks; package verifier 26/26; 12/12 mutations rejected. Fresh
   external gpt-5.4 review independently reproduced the algebra and root census and returned
   `VERIFIED_WITH_CORRECTIONS`; its ownership-scope correction is incorporated above.
4. **Premises audited:** yes. The coframe and connection are supplied conditional R17 geometry;
   no equation, action, source, matter law, bootstrap, or physical path is inferred.

## Maximum conclusion

```text
STATIONARY_SPECIAL_SUBLOCUS_CLASSIFIED__GLOBAL_HORIZONTALITY_FORCES_CONSTANT_PHI__
FLAT_AND_ABSTRACT_DESCENT_LOCUS_EXPLICIT__NO_REGULAR_CANONICAL_HOPF_TANGENT_DESCENT__
COMPLETE_HOLONOMY_TRIVIAL_OR_SO2__MANIFEST_BACKED_R17_SOURCES_SELECT_NONE
```

This is a kinematic classification, not canon and not physical branch selection.
