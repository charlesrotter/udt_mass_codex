# Reciprocal-transport naturality selector audit

## Result

The registered UDT premises do **not** select a unique physical affine
connection on the smooth nonnull-`dphi` region.

The honest status is:

```text
physical transport selector: OPEN_SELECTOR
```

The parent candidate

```text
h0 = |g^{-1}(dphi,dphi)| g
Gamma0 = LC(h0)
```

remains an exact, local, CSN-invariant geometric construction. This
audit did not demote it. It determined that the existing source
authority does not distinguish it from exact alternatives.

## The decisive counterfamily

For every smooth function `f`,

```text
h_f = exp(2 f(phi)) h0
Gamma_f = LC(h_f)
A_f = A0 + f'(phi) dphi.
```

Because `phi` has CSN weight zero, every member is CSN invariant.
Strict invariance under reciprocal reversal requires

```text
f'(-phi) = -f'(phi),
```

so `f` may be any even function up to an irrelevant constant. In
particular,

```text
f(phi) = lambda phi^2
```

survives.

At the canonized static seal, `phi=0` while the normal derivative is
free. The even counterfamily has `f'(0)=0`, so every member agrees with
`Gamma0` at the seal. Exact component algebra nevertheless gives a
nonzero connection difference in the bulk. Reversal plus seal
therefore does not select the connection.

## What composition does—and does not—do

The registered composition rule derives the additive comparison group:

```text
S(phi1) S(phi2) = S(phi1 + phi2).
```

It does not derive a local field gauge symmetry

```text
phi(x) -> phi(x) + a,
```

and the current ontology ledger explicitly leaves the map between group
depth, observer comparison, and the local signed field open.

If local-shift invariance is added, exact algebra forces `f` to be
affine. If strict affine-connection invariance under reversal is then
also added, the affine slope vanishes and `Gamma_f=Gamma0`. This is a
real theorem, but only within the declared `Gamma_f` family and only
under those two extra assumptions:

```text
Gamma0: UNIQUE_CONDITIONAL
```

It does not remove independently supplied split-stabilizer connection
data.

Likewise, demanding that the extra factor `f` itself be a regular
additive character makes `f` affine. No registered UDT rule says that
an arbitrary CSN-invariant conformal factor must be a second copy of
the positional comparison character, so that restriction cannot be
used as present authority.

## The three data levels are not equivalent

### Full signed `phi`

Contains enough information to write the infinite even counterfamily.
Reversal and seal do not remove it.

### Exact `dphi`

If explicit dependence on `phi` is forbidden, the residual family is

```text
A_lambda = A0 + lambda dphi.
```

Reciprocal reversal maps `lambda` to `-lambda`. Treating that as
covariance leaves the family intact; demanding strict orientation
blindness selects `lambda=0`. Current UDT authority supplies the signed
reciprocal roles but not this strict connection-invariance rule.

### Oriented or unoriented projector

The projector loses too much information to determine `A0`. Under

```text
phibar = F(phi),     F'(phi)=exp(kappa phi)>0,
```

the line and projector are unchanged, but

```text
A0bar = A0 + kappa dphi.
```

Thus the same projector supports distinct connections. By contrast, a
constant linear group-coordinate rescaling changes `dphi` by a constant
factor and leaves `A0` unchanged. The additive group normalization
matters; the projector alone does not retain it.

## Source-authority audit

The current repository supplies:

- CSN;
- additive relative composition;
- reciprocal group reversal;
- the static `phi=0` seal.

It does not presently supply:

- local additive shifts as a gauge of `phi(x)`;
- a complete action of reciprocal reversal on the affine connection;
- torsion freedom as a native law;
- zero split-stabilizer addition as a native minimality law;
- a bootstrap local connection operator; or
- a seal equation selecting bulk transport.

No appeal to simplicity, familiar Levi-Civita mechanics, GR/SR
observer theory, the carrier, or a desired Hopf result was admitted.

## Verification

- Exact SymPy controller: all 16 registered checks passed.
- Independent stdlib/Fraction implementation: 9/9 exact checks, 12/12
  catches, and 5/5 cross-result agreement checks passed.
- The independent implementation does not import the controller.
- Both exact timelike/spacelike parent transport results remain
  unchanged; this audit did not rerun or alter their fixed evidence.

The final repository gates, manifests, tests, and dirty-checkout
metadata are recorded in `REPOSITORY_GATES.json`.

## Four evidence gates

1. **Preregistered:** yes, commit `59bc92f`, before the outcome scripts
   ran.
2. **Full or bounded scope justified:** bounded and explicit—local,
   smooth, nonnull `dphi`; all registered transformation meanings were
   source-audited.
3. **Independently verified:** yes for the load-bearing algebra, using a
   separate stdlib/Fraction implementation; no fresh independent model
   family was used.
4. **Every premise audited:** yes within the declared source set and
   scope.

Accordingly the counterfamily and conditional theorem are
`VERIFIED-WITH-CAVEATS`; no complete global or physical connection
theorem is claimed.

## Scientific consequence

Further attempts to select transport merely by adding familiar
connection properties would be premise invention. The connection seam
is now sharply localized:

> UDT still lacks a typed native law stating which `phi` data define
> physical transport and how reciprocal reversal acts on that
> transport.

This is a clean stopping point for connection drilling.
