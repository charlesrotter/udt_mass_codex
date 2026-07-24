# CSN–`dphi` transport-selector audit

Date: 2026-07-23

Base: `bc802bb0ec3b612f841963cc471440fc88741bbf`

Preregistration commit: `42edf80`

Mode: metric-led, CPU-only exact differential geometry

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

The earlier fork—“either find a conformally natural connection or wait
for bootstrap to select a metric representative”—was too coarse. A real
pre-scale local connection is already available wherever `dphi` is
nonnull.

Let

```text
alpha = dphi,
s = g^{-1}(alpha,alpha).
```

On any connected region with `s != 0`, define

```text
h0 = |s| g.
```

Under arbitrary positive Common-Scale rescaling,

```text
g -> exp(2 sigma) g,
s -> exp(-2 sigma) s,
```

so `h0` is exactly unchanged. It also makes `dphi` unit:

```text
h0^{-1}(dphi,dphi)=sign(s).
```

Therefore `LC(h0)` is a genuine CSN-invariant local affine connection.
In a representative `g` it is the Weyl connection with

```text
A0=(1/2)d log|s|,
A0 -> A0-dsigma.
```

This is a substantive positive result. Bootstrap is **not** needed merely
to make a local pre-scale comparison connection exist.

It is not yet a unique physical law. The same registered data admit the
exact family

```text
h_f = exp(2 f(phi)) h0,
A_f = A0 + f'(phi)dphi,
```

for arbitrary smooth `f`. Every member is CSN invariant as a construction
from `([g],phi)`. The nontrivial family

```text
f_lambda(phi)=lambda phi^2
```

is even under reciprocal reversal and obeys `f_lambda(0)=0` at the static
seal, yet different `lambda` give inequivalent affine connections. The
current foundation does not contain a rule selecting `f=0`.

The split-preservation result is equally sharp:

- a torsion-free Weyl connection preserves the normalized `dphi` line
  exactly when the orthogonal three-screen is umbilical—its change along
  `dphi` is pure common expansion/contraction with zero trace-free shear;
- that connection is unique if it exists;
- a generic shearing screen fails the exact system with coefficient rank
  four and augmented rank five in both timelike and spacelike cases;
- a metric-compatible projected/Kato connection preserving the line and
  induced `3+3` reduction always exists on a smooth nonnull region, but
  it is generically torsionful; and
- even after choosing the minimal projected connection, an arbitrary
  screen-Lorentz/rotation-valued one-form can be added. This leaves three
  components per tangent direction, twelve at a point in four
  dimensions.

At null `dphi`, `h0` degenerates and `A0` is undefined. At `dphi=0`,
there is no line and `h0` vanishes. The normal conformal tractor
connection remains a canonical rank-six representation connection, but
it is not a tangent connection or a selected tangent section.

The honest ruling is:

```text
LOCAL_CSN_INVARIANT_CONNECTION_AVAILABLE_ON_NONNULL_DPHI
TORSION_FREE_SPLIT_PRESERVATION_UNIQUE_IFF_UMBILIC
PROJECTED_SPLIT_TRANSPORT_AVAILABLE_BUT_TORSIONFUL_AND_NONUNIQUE
PHYSICAL_CONNECTION_AND_NULL_ZERO_GLOBAL_EXTENSION_OPEN
```

## Lay interpretation

CSN says that changing every local ruler and clock by the same factor
does not change pre-scale physics. The size of the `phi` gradient changes
in exactly the opposite way. Multiplying the metric by that gradient
size therefore cancels the arbitrary recalibration.

It is like discovering a built-in, scale-free graph paper: wherever
`phi` is genuinely changing and is not lightlike, the graph paper can be
normalized so that one unit of `phi` is one unit along its own direction.
That graph paper supplies a perfectly good rule for comparing directions
from point to point.

But the metric has not yet said that this is **the** physical graph
paper. Other graph papers can be multiplied by a positive function of
`phi` and still obey CSN, reciprocal reversal, and the seal. Nor does the
most direct connection always keep the `phi` direction cleanly separated
from the other three directions.

If the transverse geometry only swells or shrinks uniformly, one unique
torsion-free split-preserving connection exists. If the transverse
geometry shears—one direction stretching while another contracts—no
torsion-free Weyl connection can preserve the split. We can always
construct a split-following geometric connection, but it generally
acquires torsion and retains internal rotation freedom.

So the new result removes one blocker but exposes the remaining one more
precisely:

> UDT already has local scale-free transport candidates. What it still
> lacks is the rule saying which candidate is physical and how it crosses
> lightlike or zero-gradient regions to close a whole finite cell.

## Why `h0` is intrinsic on a nonnull stratum

Write `epsilon=sign(s)`. The vector

```text
n = sharp_h0(dphi)
```

obeys

```text
h0(n,n)=epsilon,
n-flat_h0=dphi.
```

Because `dphi` is exact, its Hessian is symmetric. Because the norm of
`n` is constant,

```text
n^a nabla_a n_b
= n^a nabla_b n_a
= (1/2)nabla_b[n^a n_a]
= 0.
```

Thus the normalized `dphi` congruence is automatically geodesic in
`h0`. This is a geometric identity, not an equation of motion.

Since

```text
h0=exp(2 omega)g,
omega=(1/2)log|s|,
```

the exact conformal connection formula gives

```text
LC(h0)=LC(g)+C(A0),
A0=domega=(1/2)d log|s|.
```

The shift `A0 -> A0-dsigma` cancels the Levi-Civita shift under
`g -> exp(2sigma)g`, leaving one affine connection.

This metric is relational and scale-free. It does not produce an
absolute meter, second, `X_max`, `G`, mass, or physical CSN
representative.

## Why conformal naturality does not select one connection

`phi` is CSN-neutral. Therefore any positive function of `phi` may
multiply `h0` without spoiling input-representative invariance:

```text
h_f=exp(2f(phi))h0.
```

Its connection differs by

```text
LC(h_f)-LC(h0)=C(f'(phi)dphi).
```

The controller finds ten nonzero connection-difference components for
the exact timelike `f=phi^2` witness and ten between the `lambda=1` and
`lambda=2` witnesses. The independent rational implementation reproduces
the count.

The current ontology audit explicitly rules that additive `phi` shifts
are not a derived CSN gauge. Reciprocal reversal and the static seal do
not eliminate the family because every even `f` with `f(0)=0` survives.
A new naturality/minimality premise could choose `f=0`, but none is
registered.

This counterfamily is sufficient to defeat unrestricted uniqueness. It
is not claimed to exhaust all higher-jet natural connections.

## Exact torsion-free line-preservation theorem

Use `h0`, its unit vector `n`, and the orthogonal projector `Q`. Let

```text
K(X)=Q nabla_X n
```

for screen vectors `X`. Exactness of `dphi` makes the associated
second-fundamental form symmetric, and the unit-gradient identity makes
the line acceleration vanish.

Every torsion-free Weyl connection relative to `h0` has the form

```text
D_X Y
= nabla_X Y
  + B(X)Y+B(Y)X-h0(X,Y)B-sharp.
```

The screen part of `D_X n=0 mod n` gives

```text
K(X)+B(n)X=0
```

for screen `X`. The `X=n` equation gives `B_perp=0`. Therefore a solution
exists exactly when

```text
K = (H/3) I_screen,
H=trace(K),
```

and then

```text
B(n)=-H/3
```

fixes the complete one-form uniquely.

The exact diagonal shear witness `K=diag(1,-1,0)` has coefficient rank
four and augmented rank five for both causal signs. It is not repaired by
choosing a different Weyl one-form. Current UDT supplies no complete
on-shell branch proving that this trace-free shear vanishes everywhere.

## Split-preserving transport without torsion freedom

Let `P` project onto the unit `dphi` line and `Q=1-P`. For
`nabla=LC(h0)`, define

```text
K_X=(nabla_X P)P-(nabla_X P)Q,
D_X=nabla_X-K_X.
```

The exact projector identities give

```text
[K_X,P]=nabla_X P,
D P=0,
K_X is h0-skew,
D h0=0.
```

The induced connection on two-forms preserves the line-screen
three-plane and its complementary three-plane. This is the tangent-bundle
version of the previously banked Kato transport identity.

Its torsion is

```text
T^D(X,Y)=-K_XY+K_YX.
```

For unit-gradient data, screen-screen torsion cancels, while
`T^D(n,X)=K(X)` for screen `X`. It is therefore nonzero whenever the
screen changes along the `dphi` direction. The preregistered generic
exact witnesses contain fourteen nonzero tensor components in both
causal signatures.

Nor is `D` unique. Any one-form `S` with values in the screen orthogonal
algebra satisfies

```text
S_X^T h0+h0 S_X=0,
[S_X,P]=0,
```

so `D+S` remains metric-compatible and split-preserving. The exact
kernel has dimension three for each tangent direction, hence twelve
pointwise connection components in four dimensions.

Choosing `S=0` is a mathematically simple projected connection. Simplicity
alone is not current UDT authority.

## Causal and global limits

The construction is valid separately on connected timelike and spacelike
nonnull regions. It does not turn the spacelike `3+3` into an observer
boost/rotation split.

At `s=0`,

```text
det(h0)=|s|^4 det(g)=0,
```

and `A0=(1/2)dlog|s|` is undefined. At `dphi=0`, the same metric
degeneracy accompanies the loss of the intrinsic line. Any causal-type
change crosses one of these strata.

This is an obstruction to extending **this construction** smoothly. It
is not a theorem that no future UDT interface law can exist. The current
finite-cell atlas supplies twelve completion types but zero complete
on-shell `(g,phi)` branches, so no global continuation or branch
selection follows here.

## Consequence for bootstrap

Bootstrap is no longer required merely to create local pre-scale
comparison geometry. The normalized-gradient construction already does
that.

Bootstrap—or another separately derived UDT selector—would still have to
do at least one of the following before the connection becomes physical:

1. select the `h0`/`A0` prescription over the `h_f` and stabilizer
   families;
2. force the umbilical condition if torsion-free split preservation is
   required;
3. provide a null/zero interface law;
4. select a complete finite-cell `(g,phi)` solution and its global
   holonomy; or
5. explain why geometric connection transport is the physical
   propagation law.

The registered bootstrap currently supplies none of those operators.

## Verification and correction note

The SymPy controller passes `38/38` exact checks. The independent
standard-library `Fraction` implementation imports no production code
and passes `25/25` reconstruction checks plus `12/12` exercised
fail-closed mutations.

The independent run initially caught one controller reporting bug: the
controller counted nonzero slices of the torsion array and reported four,
while the independent implementation counted fourteen individual
components. The controller was corrected and both implementations now
return fourteen. No identity, rank, or scientific ruling changed.

## Four evidence gates

1. **Preregistered:** yes; commit `42edf80` precedes exact evaluation.
2. **Full space or bounded scope:** complete local torsion-free Weyl
   existence system and complete local metric-compatible
   split-preserving affine freedom on smooth nonnull strata; explicit
   null/zero guards. Higher-jet natural connections and global on-shell
   finite-cell solutions are not claimed.
3. **Independent verification:** yes; separate standard-library rational
   algebra with no production import, including exercised mutations.
   No fresh external-model adversary was authorized, so the grade remains
   `VERIFIED-WITH-CAVEATS`.
4. **Premises audited:** yes; configuration ownership, causal type,
   torsion, connection class, reciprocal reversal, seal, tractor type,
   bootstrap, and all downstream physics limits are explicit.

## Stop line

No connection is adopted as physical. No action, field equation, source,
carrier, Hopf section, boundary functional, finite-cell branch, physical
time law, scale, density, `X_max`, mass, GPU work, canonization, or
repository reorganization follows from this audit.
