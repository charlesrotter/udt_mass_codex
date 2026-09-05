# G352 preregistration — clock-rate carried-measure readout

Date: 2026-09-05
Parent: G351 externally accepted bounded carried-measure conservation result

## Owner instruction interpreted

After the bounded candidate premise was stated exactly, Charles replied:

> adopt provisionally and proceed.

G352 records that as authorization to use the statement in `ADOPTION_RECORD.md` as an
`OWNER_ADOPTED_PROVISIONAL_PREMISE`. It is not derived, canonical, a theory of light, or permission
to select one `p` for every possible carried quantity.

## Exact question

Let `Theta` be a supplied monotone dimensionless phase/event coordinate on one supplied labelled
future-null family, with future-null covector `k_a=grad_a(Theta)`. Let successive crossings be
separated by one supplied constant `DeltaTheta>0`. A finite observer `u_i` measures

```text
omega_i=-u_i^a k_a=dTheta/dtau_i>0.
```

Let `mu` be G351's source-free conserved finite nonnegative countably additive transverse label
measure. On a regular cut let `n_i=dmu_ac/dArea_i=s/J_i`. Under the adopted readout premise define

```text
Gamma_i=(omega_i/DeltaTheta) n_i.
```

Does this specific readout force

```text
Gamma_j/Gamma_i=R_ji A_ji^-1,
```

and hence `p=1`, without selecting the weight of any other observable?

## Claims to test

1. Proper-time differentiation of the supplied phase gives crossing rate
   `dN/dtau=omega/DeltaTheta`.
2. Combining that rate with G351's regular density gives
   `Gamma_i=(omega_i/DeltaTheta)s/J_i`.
3. The regular nonzero transfer is exactly `R A^-1`, so this readout has G350 weights
   `(p,q)=(1,-1)`.
4. Within G350's full independent positive character domain, matching the adopted readout forces
   the frequency exponent to one and the area exponent to minus one.
5. Identity, algebraic reversal, and exact three-cut sewing hold.
6. Independent finite endpoint-observer changes give observer weight one and do not choose a
   preferred observer.
7. A common positive phase reparameterization `Theta->a Theta` and
   `DeltaTheta->a DeltaTheta` leaves the rate and transfer unchanged.
8. On a rank-loss cut, the frequency-weighted pushforward
   `nu_i(B)=integral_(X_i^-1(B)) (omega_i/DeltaTheta) dmu` remains a finite measure when the weight
   is integrable, while its ordinary area density may diverge or fail to exist.
9. Zero measure remains zero, and no phase sequence, source content, or population is generated.
10. `p=0` remains the observer-neutral G351 density; other readout weights remain open. G352 does
    not select a universal `p`.

## Coverage contract

The production program will use only standard-library exact rational arithmetic and must cover:

- positive rational `omega`, `J`, `s`, and `DeltaTheta` values over at least 2,000 three-cut cases;
- identity, reversal, every three-cut ordering, and sewing;
- independent endpoint observer factors;
- common phase-coordinate rescalings;
- zero and nonzero supplied measures;
- at least 100 shrinking-Jacobian rank-loss sequences with finite integrated rate measure and
  unbounded regular density;
- independent coefficient witnesses distinguishing `(1,-1)` from neighboring integer and rational
  character weights.

An implementation-distinct verifier may not import production code or read its result. It will use
a separate exact grid and solve the two log-character coefficient conditions independently. Check
counts are regression evidence, not the analytic proof.

All programs must support `python3 -B -S` and `UDT_NO_WRITE=1`. No long solve or GPU is authorized.

## Hostile mutations

The catch proof must reject at least:

1. clock-rate frequency weight different from one;
2. area weight different from minus one;
3. omission of `DeltaTheta` phase-normalization cancellation;
4. a preferred endpoint observer;
5. `p=1` promoted to a universal weight for all carried quantities;
6. zero source generating nonzero content;
7. finite ordinary density required at every caustic;
8. geometric image-union replacing the label-measure pushforward;
9. the G352 premise relabelled `DERIVED`;
10. light, photon, energy, brightness, flux, luminosity, detector, distance, history, scale,
    `X_max`, matter, mass, or canon selected.

## Acceptance and falsification

Accept only if the analytic chain is valid in the declared scope, both exact implementations agree,
all hostile mutations are caught, phase normalization and observer covariance close, caustics are
handled measure-wise without a finite-density claim, premise provenance is explicit, and a fresh
adversarial verifier finds no broader promotion.

Falsify or narrow if `p=1` requires any undeclared energy/light premise, common phase rescaling
changes the readout, observer covariance fails, the rate measure is claimed finite without the
integrability condition, or the conclusion suppresses other legitimate readout types.

## Maximum conclusion

At most: conditional on Charles's owner-adopted provisional clock-rate readout premise and a
supplied causal phase/event sequence, G352 derives `T_clock=R A^-1`, fixing `(p,q)=(1,-1)` only for
that readout. G351's `p=0` observer-neutral density and other possible observer-weighted readouts
remain distinct and open.

No phase source, nonzero content, label population, emission, absorption, detector, cross-label
physics, light, photon, energy, brightness, flux, luminosity, distance, history, occupancy, matter,
mass, scale, `X_max`, or canon may follow.
