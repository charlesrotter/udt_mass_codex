# Native boundary-generator and scale-selection audit

Date: 2026-07-19

Base: `ad9e9bd5c27e4bfe40defcc225f81f2806a1c9f9`

Compute: CPU-only exact algebra and repository-evidence audit; no GPU

## Result first

The WR-L wall lapse flux is an exact finite **metric curvature budget**, but it is not yet a native
conserved charge or total mass.

For

```text
A(r)=1-r/X,
N(r)=sqrt(A),
0<r<X,
```

the independent calculation gives

```text
Phi_N(r) = -2*pi*r^2/X,
Phi_N(X) = -2*pi*X,
d Phi_N/dr = -4*pi*r/X != 0.
```

The nonzero radial derivative is decisive. The raw flux is not surface-independent through the
WR-L interior, so it cannot be called a vacuum Gauss charge merely because its wall value is finite.
Instead, the metric satisfies the exact clock-curvature relation

```text
D^2 N = -N/(X*r) = -R4*N/6 = -R3*N/4.
```

Consequently,

```text
Phi_N(X) = integral D^2N dV
         = -(1/6) integral N R4 dV
         = -(1/4) integral N R3 dV
         = -2*pi*X.
```

This is the strongest new lead: the metric itself already ties accumulated clock dilation to a
finite boundary quantity. What remains missing is the native off-shell law that says what this
curvature budget counts, whether it is conserved in the full time-live universe, and how it is
normalized into physical mass.

## Why the flux is not yet mass

Turning a metric flux into a physical charge requires more than multiplying by `c_E^2/G_obs`.
The current foundation does not yet supply:

- a complete native action or equivalent variational law;
- the off-shell fields and variation domain;
- a differentiable boundary/corner primitive;
- a physical symmetry generator and its normalization;
- reference subtraction, orientation, and sign convention;
- integrability of the generator in solution space;
- a native source ledger identifying all mass sectors;
- the global domain and the equality `X=X_max`; or
- time-live conservation.

The ambiguity is exact, not philosophical. Multiplying an action by a nonzero constant leaves its
stationary solutions unchanged but rescales its canonical momenta and charges. Adding an exact
radial derivative leaves the bulk Euler equation unchanged while shifting boundary momentum; a
different exact derivative shifts the movable-endpoint Hamiltonian. The archived Arm-C and
finite-cell scripts reproduce these statements independently. Therefore the metric and bulk
equations alone cannot fix a boundary charge normalization.

Observed `G_obs` can calibrate the normalization after UDT selects an action, generator, and
ordinary-regime matching rule. It cannot choose those structures by itself.

## Scale-selection result

Suppose, only conditionally, that a future action turns the wall flux into

```text
M_flux = gamma c_E^2 X/G_obs,
```

where `gamma` is a native dimensionless normalization. Pairing this with the dimensional global
relation

```text
X = alpha G_obs M_flux/c_E^2
```

does not determine `X`. The two-equation coefficient matrix has determinant

```text
1-alpha*gamma.
```

- If `alpha*gamma=1`, the equations are the same homogeneous relation and every positive common
  scale remains possible.
- If `alpha*gamma!=1`, the homogeneous pair has only the zero solution.

Thus a flux-derived mass linear in `X` can fix compactness, but not absolute size. This is the exact
homothety obstruction anticipated by the preceding boundary audit.

There is also no monomial combination of `c_E` and `G_obs` alone with dimensions of length. Their
combination `c_E^2/G_obs` has dimensions mass per length. This does not invalidate the owner
hypothesis; it specifies what the proper native mass structure must add.

## How the owner hypothesis can still close

The joint determination of `M_tot` and `X_max` remains `WORKING_COHERENT` if the complete native
matter/boundary/bootstrap system supplies at least one independent scale-breaking datum. Examples
of the required mathematical role—not proposed mechanisms—are:

1. a native total-mass functional `M_UDT[X,state]` that is not homogeneous of degree one in `X`;
2. a boundary transversality/eigenvalue equation not invariant under common rescaling; or
3. a natively derived physical density center `rho_star`.

For illustration only, the conditional WR-L volume and flux mass give

```text
V = 64*pi*X^3/15,
rho = 15*gamma*c_E^2/(64*pi*G_obs*X^2).
```

If UDT independently derived a physical `rho_star`, this equation would select

```text
X = sqrt(15*gamma*c_E^2/(64*pi*G_obs*rho_star)).
```

But current bootstrap supplies only the working requirement of a narrow fractional density window.
It does not supply the center, width, mass functional, or physical density normalization. Inserting
`rho_star` would therefore be circular today.

## CSN and bootstrap ruling

Common-Scale Neutrality says an absolute local scale is not primitive and must emerge from global
closure, boundary data, matter formation, or their combination. It does not provide the emergence
equation.

The current bootstrap principle acts as on-shell global admissibility: complete matter-bearing
solutions must occupy a narrow density window. It is not yet an off-shell functional, charge law,
or scale eigenvalue equation. Neither principle may be promoted into the missing equation merely
because it says the scale must emerge.

## Candidate-source and provenance audit

The immutable-base census contains 476 sources: 27 load-bearing, 79 context-only, 41 duplicate or
audit records, 40 pre-July negative controls, and 289 excluded with reason. All 27 load-bearing
sources are individually classified in `SOURCE_ADJUDICATION.tsv`.

Pre-July sources provide no affirmative UDT physics. Archived post-July sources are used only at
their explicit conditional grade or as rerunnable algebra. Current authority comes from the
premise-reset/boundary overlays and the frozen final A/B/C adjudication.

## Verification

- new exact derivation: 25/25 checks pass;
- independent verifier: eight gate groups and 12 exercised catch-proofs pass;
- archived WR-L solution-space replay: 55/55;
- archived finite-cell boundary replay: 23/23;
- frozen Arm-C boundary replay: 5/5.

The independent implementation uses the dimensionless coordinate `y=r/X`, independently proves
the flux gradient and closure-rank determinant, and proves that no monomial of `c_E,G_obs` has
length dimensions.

The preregistered fresh-context external-model review is not transmitted without separate explicit
disclosure authorization. This package is therefore `VERIFIED-WITH-CAVEATS`, not `SETTLED`.

## Four evidence gates

1. **Preregistered:** yes, commit `049bacd` before source inspection or outcome calculation.
2. **Full space or bounded scope justified:** yes for the static WR-L flux/action-normalization and
   homogeneous scale-rank question; no claim about all time-live or matter-bearing solutions.
3. **Independently verified:** yes by a separate coordinate/scaling implementation and archived
   algebra replays; fresh-context model review remains authorization-gated.
4. **Every premise audited:** yes within this bounded question; action, source, carrier, global
   domain, physical density center, and time-live conservation remain explicitly absent.

## Maximum conclusion

Bank as `VERIFIED-WITH-CAVEATS`:

> `RAW_METRIC_CURVATURE_BUDGET_DERIVED; CONSERVED_CHARGE, NATIVE MASS, AND ABSOLUTE SCALE OPEN.`

The exact clock-curvature identity is a promising candidate seam, not yet a universal UDT field
equation. The next bounded scientific question is whether Reciprocity, CSN, finite-cell structure,
and bootstrap force that identity—or a covariant generalization—across the admissible complete
metric family. That follow-on is not launched here.

No numerical `X_max`, total mass, action, source, carrier, physical density, cosmology,
canonization, GPU work, or repository reorganization is claimed.
