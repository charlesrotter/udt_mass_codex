# Exact derivation — staged `JR_CERT_NATIVE` program

Date: 2026-08-01

Base: `686336343878e8a9e39a4b72df08d23754243631`

Outcome: `NO_NATIVE_PROBLEM_DERIVED_DOWNSTREAM_STAGES_BLOCKED`

This is a bounded derivation and source theorem over the preregistered 586-path universe. It does
not assert that no future UDT equation or boundary law exists.

## 1. Stage 1 asks for selection, not reconstruction

The required object is an operation

```text
E_native: U_full -> Y
```

whose domain owns the complete founded scalar/coframe content, whose zero set is a proper realized
subset of the admitted configurations, and whose native provenance does not depend on importing or
conditionally adopting an action, source, carrier, pairing, or boundary.

The distinction is decisive. A metric determines its Levi-Civita connection. That fact does not
determine which metric is physically realized.

### Exact arbitrary-profile control

To make that logical distinction executable, use the bounded control family

```text
g_phi = diag(-exp(-2 phi(x)), exp(+2 phi(x)), 1, 1).
```

This is not proposed as the complete UDT coframe. It is a subfamily carrying the founded inverse
clock/ruler action. Its determinant is exactly `-1` for every smooth finite `phi`.

With

```text
theta0 = exp(-phi) dt,
theta1 = exp(+phi) dx,
```

the first structure calculation is

```text
d theta0 = exp(-phi) phi' theta0 wedge theta1,
d theta1 = 0,
omega01 = -exp(-phi) phi' theta0.
```

Therefore

```text
d theta0 + omega01 wedge theta1 = 0
```

identically for arbitrary `phi`. The curvature is not forced to vanish:

```text
Omega01 = exp(-2 phi)(phi''-2 phi'^2) theta0 wedge theta1.
```

Thus the structure relation reconstructs a connection and curvature from each supplied profile; it
does not select the profile.

The independent coordinate calculation gives all `64/64` metric-compatibility components and all
`64/64` torsion components equal to zero for arbitrary `phi`. The scalar curvature is

```text
R = 2 exp(-2 phi)(phi''-2 phi'^2).
```

For `phi=a x`, `R=-4 a^2 exp(-2 a x)`, so distinct nonzero-curvature geometries pass exactly the
same compatibility and torsion tests.

The contracted Bianchi divergence also gives

```text
nabla_mu G^mu_nu = (0,0,0,0)
```

for arbitrary `phi(x)`. This establishes that it has zero independent field-selection rank in this
control. It may become a compatibility condition after a native sourced equation is derived; it is
not that equation.

`ALGEBRA_RESULT.json` contains the exact Christoffels, Einstein tensor, Cartan coefficients, seal
family, and variation identities.

## 2. All eight equation routes

`EQUATION_ROUTE_ADJUDICATION.tsv` applies one gate to every preregistered route.

1. Cartan structure relations reconstruct connection and curvature for each admitted coframe.
2. Levi-Civita compatibility selects one connection per metric, not one realized metric.
3. Differential/Bianchi relations are identities and carry no independent selection rank here.
4. Reciprocity and coframe composition derive exact kinematics, but registered complete response
   retains screen, mixing, path, completion, and on-shell choices.
5. Finite-cell smoothness, holonomy, and gluing remove some configurations but leave multiple
   smooth complete families and do not supply a whole interior/global response operation.
6. Bootstrap supplies the exact two-arrow type

   ```text
   A(X,O)=0,
   O-R[X]=0,
   ```

   but neither complete map, its domain, derivative, native pairing, nor a common fixed point.
7. `C^2`/Bach remains unique-conditional and EH/carrier routes remain conditional. No present
   premise turns them into an unconditional complete UDT law.
8. The repository-wide joint-selector census and the current joint-realization census contain no
   other registered complete native on-shell operation.

Zero of eight routes passes Stage 1. This is not a universal no-go: higher-jet, nonlocal,
set-valued, and future whole-solution operations remain outside the theorem.

## 3. Stage 2 cannot be inferred from a seal value

A matching boundary operation must be the differentiable boundary/corner/completion domain of the
same `E_native`. The current record contains exact boundary objects, but not that operation.

### Seal-family control

Near a mirrored static seal, the odd family

```text
phi_a(x)=a x
```

has

```text
phi_a(0)=0,
partial_n phi_a(0)=a,
R(0)=-4a^2.
```

The registered trace/parity datum therefore admits arbitrary normal slope and distinct curvature.
It neither supplies the other field data nor selects a realized profile.

### Boundary dependence on the missing operator

Two pure mathematical variation controls show why a wall value cannot be promoted before the
operator is known. They are not candidate UDT actions.

For a two-derivative control,

```text
delta integral (phi')^2/2 dx
  = integral (-phi'') delta_phi dx + [phi' delta_phi].
```

For a four-derivative control,

```text
delta integral (phi'')^2/2 dx
  = integral phi'''' delta_phi dx
    + [phi'' delta_phi' - phi''' delta_phi].
```

Fixing `delta_phi=0` closes the displayed second-order flux but leaves the `phi'' delta_phi'` term
in the fourth-order control. Hence the correct differentiable boundary data depend on the native
operator and variation domain. This is exactly why conditional EH, Bach, and carrier boundaries
cannot be spliced into one native boundary law.

All six boundary routes fail:

- static seal parity fixes only the scoped `phi` trace;
- regular caps, seams, mirrors, quotients, horizons, and interval ends form a catalogue rather than
  a selected differentiable completion;
- conditional actions have different operator orders and boundary primitives;
- bootstrap requires boundary/global shape variation but supplies no map or derivative;
- the conditional carrier and numerical exterior do not derive a physical metric boundary; and
- raw wall flux, horizon regularity, parity, and gluing data do not jointly supply one matching
  primitive, generator, normalization, reference, or time-live law.

Because Stage 1 failed, Stage 2 is also blocked as a *construction of the matching boundary*. Its
six candidate routes were nevertheless independently adjudicated so the failure is not merely an
automatic consequence of Stage 1.

## 4. Stages 3 and 4 stop mechanically

The preregistered launch rule is

```text
solve_allowed = stage1_pass and stage2_pass.
```

Both inputs are false. `CATCH_PROOFS.tsv` exercises all four truth assignments and confirms that
only `(true,true)` permits a solve. The primary verifier separately rejects an unauthorized launch
or certificate promotion.

Accordingly:

- no ODE/PDE or live solve was launched;
- no field was filtered for a desired shape;
- no conditional action, carrier, boundary, or topology was adopted; and
- no `JR_CERT_NATIVE` instance was assembled.

The schema itself remains exact:

```text
JR_CERT_NATIVE = (
    Pi_native=(E_native,B_native,P_compatible),
    one common u,
    static/time/angular restriction proofs,
    nonzero time-live and angular-live proofs,
    E_native[u]=0,
    B_native[u]=0,
    one-premise-stack proof
).
```

What is missing is the schema's content, beginning with `E_native`.

## 5. Bounded theorem

Within the exact 586-path preregistered source universe:

```text
NO_NATIVE_PROBLEM_DERIVED_DOWNSTREAM_STAGES_BLOCKED.
```

The strongest constructive lead remains the bootstrap two-arrow architecture, because it has the
right whole-system type. It is not yet a law: deriving either arrow by inventing an objective,
density equality, action, source, or pairing would violate the premise gate.
