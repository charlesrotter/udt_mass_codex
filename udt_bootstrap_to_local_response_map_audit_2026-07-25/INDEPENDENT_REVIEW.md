# Fresh adversarial review

## Frozen verdict

`VERIFIED-WITH-CAVEATS`: no preregistered candidate supplies a complete native
bootstrap-to-local response map. The corrected two-arrow conditional skeleton
and the minimum missing object survive adversarial reconstruction.

## Independent derivation

The reviewer first reconstructed the problem without reading the production
results. The owner tuning hypothesis requires

```text
A(X,O)=0,
O-R[X]=0,
```

not only an observable residual `B(O[X])=0`. Its extended differential is

```text
lambda(D_X A delta X + D_O A delta O)
  + mu(delta O-D R_X delta X).
```

After `delta O=D R_X delta X`, the local branch term is
`lambda(D_X A+D_O A D R_X)delta X`. Local sensitivity additionally needs
branch regularity or invertibility modulo gauge. Neither complete arrow,
regularity condition, nor native dual pairing is supplied.

The reviewer agreed that:

- a density window is on-shell admissibility, not an interior response;
- `delta rho=(delta M-rho delta V)/V` and local bulk volume is trace-only;
- the density projection needs native trace-free mass response to affect the
  trace-free angular channel;
- this does not rule out energy, curvature, boundary, or other closure
  components;
- fixed-point language does not select a map or linearization;
- owner “optimization” means mutual tuning, while scalar extremization is a
  stronger open implementation;
- the calibrated-metric and conformal-class ontology branches cannot be
  silently spliced.

## Challenges that changed the package

The first production formula omitted the direct local branch arrow. It was
replaced by the complete coupled closure above. The reviewer also caught and
caused correction of:

- `R01 G7`, reduced from `PASS` to `CONDITIONAL` because density depends on the
  unresolved metric ontology;
- `R05 G7`, changed from `INCOMPATIBLE` to `CONDITIONAL` because representative
  selection is branch-dependent rather than universally incompatible;
- a vacuous independent shear check and a hard-coded fixed-point slope check;
- an abstract free-coefficient demonstration for non-density angular response.

For the last item, the final package adds a concrete mathematical curvature
candidate. The bulk variation of `integral sqrt(h) R` against
`H=diag(1,-1,0)` in a Ricci eigenframe is `-r1+r2`, with a separate boundary
flux. This establishes availability, not native UDT selection. A corresponding
energy calculation remains unavailable because native total energy is absent.

## Final replay

After correction, the pinned SymPy 1.14 production replay, independent
stdlib/Fraction checks, source identities, semantic mutation catches, and
repository gates all pass. The remaining caveat is scientific rather than
procedural: the audit derives the required *type* of the tuning loop, not its
physical arrows or closure law.
