# Reciprocal-transport naturality selector audit — preregistration

Date: 2026-07-23  
Mode: metric-led, CPU-only, data-blind algebra and source-authority audit  
Base: `efa2fd60a5e5c0566394baa87a30506ec9563ce5`

## Whole question

On a smooth region where

```text
alpha = dphi
s = g^{-1}(alpha, alpha) != 0,
```

the parent audit derived the CSN-invariant representative

```text
h0 = |s| g
A0 = (1/2) d log |s|
Gamma0 = LC(h0) = Weyl(g,A0).
```

It also exhibited the exact CSN-invariant family

```text
hf = exp(2 f(phi)) h0
Af = A0 + f'(phi) dphi
Gammaf = LC(hf).
```

The bounded question is:

> Do the already registered reciprocal character, composition,
> reversal, static seal, CSN, finite-cell, or bootstrap statements
> select `Gamma0` (or the projected split-preserving connection) as
> physical transport, without importing simplicity, minimality, an
> action, a carrier, or GR/SR observer mechanics?

## Frame

- Whole frame: the complete currently registered source authority
  listed in `SOURCE_MANIFEST.tsv`.
- Bounded mathematical region: smooth nonnull `dphi`.
- Metric-led: no desired particle, Hopf charge, action, boundary
  polarization, or empirical target enters the test.
- Hopfion evidence is out of scope and will not be inspected or used.
- Null and zero-`dphi` loci remain outside this local construction and
  must remain explicitly open.

## Configuration classes

The audit keeps these meanings separate:

1. full signed scalar `phi`;
2. exact one-form `dphi`;
3. oriented normalized line determined by `dphi`;
4. unoriented line/projector determined by `dphi`;
5. reciprocal group element/current;
6. an independently supplied affine connection.

It will not identify them merely because they coincide in one adapted
chart.

## Preregistered transformation tests

### T1 — CSN

Apply `g -> Omega^2 g` with `phi` fixed and verify the transformation
of `s`, `h0`, `A0`, and every `Gammaf`.

### T2 — reciprocal reversal

Apply `phi -> -phi`, `dphi -> -dphi`. Distinguish:

- covariance of the formula;
- invariance of the resulting affine connection; and
- exchange of the reciprocal clock/ruler roles.

Solve the exact condition on `f` for strict connection invariance. Do
not assume that strict invariance is already a physical postulate.

### T3 — static seal

At the canonized static seal `phi=0` with normal derivative free, test
whether reversal-compatible counterfamilies coincide with `Gamma0`
there while remaining distinct in the bulk.

### T4 — composition versus local shift

Separate the derived comparison law

```text
S(phi1) S(phi2) = S(phi1 + phi2)
```

from the unproved local field gauge law

```text
phi(x) -> phi(x) + a.
```

Compute what local-shift invariance would imply only as a
`CONDITIONAL` theorem. It may not be used as current UDT authority.

### T5 — derivative-only and orientation-blind subclasses

Classify the residual family if transport is restricted to depend on
`dphi` but not `phi`, and then if it is additionally required to be
blind to `dphi -> -dphi`. The second restriction must be source-audited,
not inserted as taste.

### T6 — projector-only naturality

Use an exact monotone field reparameterization

```text
phibar = F(phi),  F'(phi)>0
```

which preserves the line/projector. Determine whether the projector
alone determines `A0` or a unique connection.

### T7 — reciprocal-group normalization

Compare arbitrary monotone reparameterizations with the much smaller
set preserving the additive one-parameter group. Test whether the
chosen sign/unit of `phi` supplies physical selection or only a
coordinate convention.

### T8 — torsion-free versus projected transport

Audit whether torsion freedom or zero stabilizer addition is registered
UDT authority. Reuse the parent's exact algebra only as parent evidence;
do not call a zero addition selected merely because it is short.

### T9 — bootstrap and finite-cell authority

Test source authority for an actual local connection/variation law. A
global selection requirement or static value parity is not to be
promoted to an unrecorded local equation.

## Exact witnesses and catches

The controller and an independent implementation must exercise:

1. an even nonconstant family, including `f=lambda*phi^2`, surviving
   strict reversal and the static seal;
2. a derivative-only family `A_lambda=A0+lambda*dphi`;
3. the conditional intersection of local-shift invariance and strict
   reversal;
4. a nonlinear monotone reparameterization preserving the projector
   but changing `A0`;
5. a linear group-coordinate rescaling leaving `A0` unchanged;
6. rejection of a false local-shift authority;
7. rejection of a false claim that seal matching fixes the bulk;
8. rejection of a false claim that projector data alone fixes `A0`;
9. rejection of a false promotion of torsion freedom or zero
   stabilizer addition to a native law;
10. rejection of any physical-transport, action, carrier, Hopfion, or
    time-evolution conclusion.

## Certification and conclusion ceiling

Required before banking:

- exact symbolic controller;
- independent exact implementation not importing controller code;
- exercised catch-proofs;
- source hashes unchanged;
- repository tests at their current baseline;
- frozen-package and current-path gates replayed through the existing
  parent gate verifier;
- dirty-checkout metadata unchanged and contents unread.

Possible maximum conclusions:

- `SELECTED_WITHIN_EXACT_REGISTERED_CLASS`, only if every surviving
  counterfamily is excluded by an explicitly cited current UDT rule;
- `UNIQUE_CONDITIONAL`, if uniqueness requires clearly identified
  additional transformation/naturality assumptions;
- `OPEN_SELECTOR`, if an exact counterfamily survives the complete
  registered source authority.

No result may select an action, carrier, source, boundary charge,
physical time evolution, or Hopf structure. No canonization is
authorized.
