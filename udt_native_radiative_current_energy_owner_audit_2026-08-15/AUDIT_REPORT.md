# Audit report — native radiative current and energy ownership

Date: 2026-08-15

## Result

The metric owns two substantial pieces of mathematical machinery on supplied regular branches:

1. a Maxwell-shaped response complex after a four-dimensional oriented Abelian reduction is
   supplied or conditionally derived;
2. canonical null Hamiltonian flow and phase-volume preservation.

Neither machinery supplies a physical radiative population. The exact ownership result is

```text
GEOMETRIC_RESPONSE_AND_PHASESPACE_TRANSPORT_ONLY
__PHYSICAL_TRANSFER_OPEN
__ONE_CARRIER_COVECTOR_PREMISE_GIVES_EPSILON_EQUALS_ONE_OVER_Z
__CLOSED_CARRIER_MEASURE_STILL_NEEDED_FOR_ETA_EQUALS_ONE
```

## Load-bearing equations

For a conditional Abelian connection `mathcal A`,

```text
mathcal F=d mathcal A,
d mathcal F=0,
mathcal J=d(*mathcal F),
d mathcal J=0.
```

The first and last equations are identities. The source-free equation `d(*mathcal F)=0` is not.
The exact counterexample `mathcal A=t^2 dx` has

```text
mathcal F=2t dt wedge dx,
d(*mathcal F)=-2 dt wedge dy wedge dz != 0.
```

Canonical Hamiltonian flow has zero phase-volume divergence, but an arbitrary distribution is not
transported: the flat witness `f=x^0` gives `X_H f=-p_0`.

If a physical carried covector is supplied as `p=C k_flat` on the same null query, then

```text
E_u=-p(u),
epsilon=E_o/E_s=omega_o/omega_s=1/Z.
```

The constant `C` cancels. The physical identification does not.

## What changed

The open G94 transfer product is now split more sharply:

- `epsilon=1/Z` needs only one carrier-covector/energy-readout premise; no `hbar` is needed for the
  ratio.
- `eta=1` needs a physically identified closed null-carrier measure and zero side flux, or an
  equivalent wave-action/distribution evolution law.
- A full Maxwell action would be sufficient machinery on a selected branch, but it is not currently
  derived and is more than the narrow SNe propagation closure requires.

## Candidate-space result

Thirteen candidate homes were retained and typed in `CANDIDATE_OWNER_ATLAS.tsv`. They include the
reciprocal pure-gradient connection, full Cartan curvature, four-dimensional screen connection,
pair-normal connection, toric/Hopf connection, Hodge response, null phase-space flow, physical
covector energy, quadratic stress, Killing/Bianchi currents, and the missing closed carrier form.

No candidate was filtered because it failed to resemble electromagnetism. The complete orchestra
enters conditional screen curvature through ambient curvature and off-diagonal/extrinsic connection
blocks; it still does not select the physical reduction or cargo.

## Evidence

- SymPy exterior-calculus, gauge, response, Hamiltonian-divergence, and energy-ratio derivation;
- independent standard-library exact-Fraction polynomial exterior algebra with no SymPy or primary
  implementation import;
- explicit nonzero-response and nontransport catch witnesses;
- current-authority source census and 13-candidate ownership atlas.

## Scope

This is a local regular-branch ownership result. It excludes physical history selection, caustics,
multiple images, absorption/scattering, detector response, global bundle completion, source
luminosity, action, matter, mass, bootstrap, and `X_max`.

## Four gates

1. Preregistered: **PASS** before derivation and candidate classification.
2. Full or bounded: **PASS for the declared local candidate-home and transfer-ownership question**;
   global/singular propagation and every future law remain open.
3. Independently verified: **PASS WITH CAVEATS** by an implementation-distinct exact-Fraction route
   and a fresh sealed external reconstruction. `verify_package.py` is consistency-only, not an
   independent derivation.
4. Premises audited: **PASS**; split, connection, action, source, carrier, measure, energy,
   boundary, and history are separately typed.

## Grade

```text
VERIFIED_WITH_CAVEATS
__GEOMETRIC_RESPONSE_AND_PHASESPACE_TRANSPORT_ONLY
__PHYSICAL_TRANSFER_OPEN
__EPSILON_ONE_OVER_Z_ONLY_AFTER_ONE_CARRIER_COVECTOR_IDENTIFICATION
```

External adjudication: `EXTERNAL_REVIEW_ADJUDICATION.md`.
