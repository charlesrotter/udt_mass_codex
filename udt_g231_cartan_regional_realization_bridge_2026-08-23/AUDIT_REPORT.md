# G231 audit report — Cartan regional realization bridge

Date: 2026-08-23

## Primary landing

```text
CARTAN_REGIONAL_BRIDGE__BARE_R_NOT_CLOSED__CLASSIFYING_DERIVATIVE_DATA_REQUIRED
```

G227, G228, and G230 are not an endless collection of unrelated local restrictions. They are the
first successive exterior-closure conditions of the torsion-free Cartan system on the
orthonormal-frame bundle. G229 is the distinct point-jet metric-realization bridge between those
closure stages.

## What was derived

On the ten-dimensional local orthonormal-frame bundle, the four solder forms and six Lorentz
connection forms obey the torsion-free Cartan equations. Exact `d^2=0` closure yields:

| Stage | Raw arena | Exact restriction | Compatible arena |
|---|---:|---:|---:|
| curvature two-form | 36 | algebraic Bianchi rank 16 | 20 |
| first curvature derivative | 80 | differential Bianchi rank 20 | 60 |
| ordered second derivative | 320 | differentiated Bianchi plus Ricci rank 194 | 126 |

The final 126 agrees exactly with G230's independent metric-fourth-jet quotient. A constant-
curvature control closes at every frozen stage with zero horizontal derivative and zero vertical
action. A non-space-form algebraic-curvature witness has a nonzero quadratic Ricci-commutator term.
Its canonical Lorentz action is nontrivial, so principal-frame equivariance cannot be deleted from
the moving-frame problem.

## The decisive type correction

Three inputs that had been verbally blurred are not equivalent:

```text
bare moving-frame R
  -> incomplete

R relative to an already supplied coframe
  -> evaluative; the metric is already present

R plus compatible horizontal derivative and vertical frame law
  -> genuine Cartan realization problem
```

This removes a false fork. The regional bridge is neither “curvature values magically determine a
metric” nor “supply the metric and reconstruct it.” It is an integration problem for a fully typed
classifying law.

## Standard existence boundary

For a finite-dimensional classifying manifold with smooth anchor/structure functions, regularity,
and full `SO(1,3)`-equivariant `G`-structure-algebroid identities, standard theory provides
conditional local `G`-realizations. The construction may yield an effective orbifold under locally
free action; an ordinary Lorentz manifold needs a free principal action/trivial isotropy.

For infinite PDE-type data, G231 cites only the analytic formally-integrable **coframe** realization
theorem. That theorem does not generally construct the principal `SO(1,3)` bundle, so Lorentz
descent remains open. G231 does not claim generic smooth or global existence.

The relevant standard references are:

- Fernandes--Struchiner, *The Classifying Lie Algebroid of a Geometric Structure I: Classes of
  Coframes*, arXiv:1103.5850;
- Fernandes--Struchiner, *The Classifying Lie Algebroid of a Geometric Structure II: G-structures
  with connection*, arXiv:2107.01193;
- Fernandes--Smilde, *Relative algebroids and Cartan realization problems*, arXiv:2503.19233,
  especially the analytic formally-integrable realization boundary.
- Fernandes--Struchiner, *The Global Solutions to Cartan's Realization Problem*, arXiv:1907.13614,
  for the finite `G`-realization dictionary, integrability, and local-solution theorem.

These are mathematical existence tools, not UDT physical premises.

## Why this advances the history bridge

The local curvature jets now have one common home: a coframe/connection/curvature exterior system.
This is closer to an actual neighborhood than another isolated fifth-jet census and explains why
the earlier dimensions interlocked.

But the Cartan system is a player, not the composer. It integrates compatible supplied values; it
does not choose the curvature profile, observer population, or physical metric history. The next
scientific joint is now the source of the classifying derivative law or the proof that the primary
metric already supplies one on a declared family.

## Evidence

- preregistration committed and pushed at `a5cd16a9` before outcome;
- exact SymPy/DomainMatrix exterior-symbol construction;
- independent standard-library symmetric-bivector construction and two-prime ranks;
- independent exact rational nonlinear sign witness;
- constant-curvature and vertical-frame controls;
- seventeen substantive hostile mutations caught;
- theorem category, regularity, and local/global boundaries explicitly audited.

## Maximum conclusion

`DERIVED_CONDITIONAL`: G231 proves the correct regional realization architecture and exact agreement
of its first prolongations with G227--G230. It does not supply curvature values, derive a
classifying law, prove unconditional smooth or global realization, populate observer relations,
select transport, derive dynamics, action, source, matter, bootstrap, boundary, `X_max`, transfer,
observation, mass, signalling, or a physical/global history.
