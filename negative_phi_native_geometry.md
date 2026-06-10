# negative_phi_native_geometry.md

> STATUS: working note, not canonical. Purpose: start the particle-sector rebuild from the native
> negative-phi geometry alone. No Form-T, no Dirac equation, no SM labels, no fitted floor. Spinors are
> allowed only later as a diagnostic probe, not as the thing to be explained.

## 0. The clean variable

Start from the UDT metric

```math
ds^2 = -e^{-2\phi(r)}dt^2 + e^{2\phi(r)}dr^2 + r^2d\Omega^2.
```

Use

```math
f(r) = e^{-2\phi(r)}.
```

Then

```math
ds^2 = -f(r)dt^2 + f(r)^{-1}dr^2 + r^2d\Omega^2.
```

The matter-side/inside-out region is simply

```math
\phi < 0 \quad \Longleftrightarrow \quad f > 1.
```

The endpoint

```math
\phi \to -\infty
```

is

```math
f \to +\infty.
```

This is the first discipline shift: do not ask what a Dirac mode does in the cavity. Ask what a
static spherical metric with `f > 1` does before any probe field is imported.

## 1. Immediate metric facts

For a stationary observer at fixed `r`,

```math
d\tau = \sqrt{f}\,dt = e^{-\phi}dt.
```

So negative phi stretches local proper time relative to coordinate time.

For radial distance,

```math
d\ell = {dr \over \sqrt{f}} = e^\phi dr.
```

So negative phi compresses proper radial distance.

The angular area is unchanged:

```math
A(r) = 4\pi r^2.
```

The angular sector therefore remains native and phi-blind at the kinematic level. Negative phi changes
the radial/time weights, not the round two-sphere representation algebra.

The determinant is also phi-independent:

```math
\sqrt{-g} = r^2\sin\theta.
```

This is load-bearing: phi can become large without changing the four-volume density. The action weights
enter through inverse metric factors, not through a changing `sqrt(-g)`.

## 2. Curvature bookkeeping

For

```math
ds^2 = -fdt^2 + f^{-1}dr^2 + r^2d\Omega^2,
```

the mixed Einstein components are

```math
G^t{}_t = G^r{}_r = {r f' + f - 1 \over r^2},
```

```math
G^\theta{}_\theta = G^\varphi{}_\varphi = {f'' \over 2} + {f' \over r}.
```

The Ricci scalar is

```math
R = -f'' - {4f' \over r} - {2(f-1) \over r^2}.
```

The vacuum equation is

```math
f'' + {2f' \over r} = 0,
```

equivalent to

```math
\phi'' + {2\phi' \over r} - 2(\phi')^2 = 0.
```

Its asymptotically flat negative-phi branch is

```math
f(r) = 1 + {a \over r}, \qquad a > 0,
```

or

```math
\phi(r) = -{1\over2}\ln\left(1 + {a\over r}\right).
```

This reaches `phi -> -infinity` at `r -> 0`. It is the negative-mass Schwarzschild branch:

```math
f = 1 - {2M\over r}, \qquad M = -a/2.
```

The Kretschmann scalar for the vacuum branch is

```math
K = {12a^2 \over r^6}.
```

So the deep negative-phi endpoint is not itself a particle. It is a curvature-singular core.

## 3. Native geodesic reading

For a test body with conserved coordinate energy `E` and angular momentum `L`,

```math
\dot r^2 = E^2 - f\left(1 + {L^2\over r^2}\right)
```

for timelike geodesics, and

```math
\dot r^2 = E^2 - f{L^2\over r^2}
```

for null geodesics.

Since the negative-phi region has `f > 1`, and the vacuum core has `f -> infinity`, the core is not a
simple attractive geodesic well. Massive finite-energy probes and nonradial null probes encounter an
exclusion barrier; strictly radial null rays are the special case. The phrase "energy well" should
therefore be used carefully: natively, negative phi first creates a redshift/radial-compression/singular
boundary structure, not automatically a particle trap.

This is a useful correction. If particle structure appears, it must come from the operator/boundary/angle
problem built on this geometry, not from geodesic attraction alone.

## 4. The first native field operator

Before spinors, the clean scalar wave operator is

```math
\Box \Psi =
-{1\over f}\partial_t^2\Psi
+ {1\over r^2}\partial_r\left(r^2 f\,\partial_r\Psi\right)
+ {1\over r^2}\Delta_{S^2}\Psi.
```

For

```math
\Psi = e^{-i\omega t}R_\ell(r)Y_{\ell m}(\theta,\varphi),
```

the radial Sturm-Liouville problem is

```math
-\left(r^2 f R_\ell'\right)' + \ell(\ell+1)R_\ell
= \omega^2 {r^2\over f} R_\ell.
```

This is the first import-free spectrum problem. It uses only:

- the metric,
- the negative-phi profile through `f`,
- the round-sphere angular eigenvalue `ell(ell+1)`.

No spinor structure is present.

Native interpretation:

- `p(r)=r^2 f(r)` is the radial stiffness.
- `w(r)=r^2/f(r)` is the time-frequency weight.
- As `f -> infinity`, gradients become expensive and the frequency weight collapses.
- The deep core tends to behave like a boundary/suppressed-support region.

This is the first place to test whether negative phi plus angular modulation creates discrete structure
without importing the Dirac operator.

## 5. Angular sector: what survives and what does not

Survives natively:

- The round `S^2` angular spectrum `ell(ell+1)`.
- The `2ell+1` multiplicity.
- The operator algebra on the `ell=1` space.
- The `ell=1` traceless operator algebra structure `8 = 3 + 5`.
- The unique antisymmetric three-index singlet for a three-dimensional angular space.

Does not follow yet:

- spin-1/2,
- fermion statistics,
- a Dirac equation,
- a color force,
- a mass hierarchy,
- an identification of angular labels with SM particles.

So the angular sector is still the quantum-number/modulation axis, but not yet the particle sector by
itself.

## 6. First honest result

The native negative-phi geometry gives:

1. a matter-side branch `f > 1`,
2. proper-time stretching,
3. radial proper-distance compression,
4. unchanged angular two-sphere kinematics,
5. negative Misner-Sharp mass `m_MS = r(1-f)/2 < 0`,
6. a singular endpoint for the vacuum branch,
7. a natural boundary-like suppression region for massive/nonradial finite-energy probes,
8. an import-free scalar/angular Sturm-Liouville problem.

It does not yet give:

1. spinors,
2. particle identities,
3. observed masses,
4. a hierarchy.

This is not a failure. It is the clean starting point. The old spinor picture may have been a useful
shadow of the real geometry, but the next derivation must not assume that shadow is the object.

## 7. Next calculation

The next calculation should solve the native scalar/angular Sturm-Liouville problem on a family of
negative-phi profiles:

```math
f(r) = 1 + {a\over r}
```

as the vacuum control, and then on smooth regulated profiles where the singular endpoint is replaced by a
finite negative-phi core.

Questions:

1. Does the scalar/angular operator produce a discrete spectrum without a hard wall?
2. Which boundary condition is selected by finite action or finite norm at `phi -> -infinity`?
3. Does `ell=1` behave qualitatively differently from `ell=0` and `ell=2`?
4. Is there a natural three-channel structure before spinors enter?
5. Does the spectrum remain scale-free, or does the negative-phi endpoint introduce a native scale?

Only after these are answered should the spinor probe be reintroduced, and then only as a diagnostic
comparison against the native scalar/angular result.

## 8. First scalar/angular box test

Implemented in `native_scalar_spectrum.py`.

Equation tested:

```math
-\left(r^2 f R_\ell'\right)' + \ell(\ell+1)R_\ell
= \omega^2 {r^2\over f} R_\ell.
```

Profiles:

```math
f_\mathrm{vac}(r)=1+{2\over r},
```

and a smooth regulated control

```math
f_\mathrm{reg}(r)=1+{2\over \sqrt{r^2+\rho^2}}, \qquad \rho=0.25.
```

Boundary conditions:

- inner: natural zero flux, `p R' = 0`;
- outer: finite-box Dirichlet control, `R(Rmax)=0`.

Result:

```text
vacuum, ell=0:
Rmax= 40  omega1=0.085786  omega1*Rmax=3.43144
Rmax= 80  omega1=0.041103  omega1*Rmax=3.28821
Rmax=160  omega1=0.020093  omega1*Rmax=3.21484

vacuum, ell=1:
Rmax= 40  omega1=0.119723  omega1*Rmax=4.78890
Rmax= 80  omega1=0.058014  omega1*Rmax=4.64111
Rmax=160  omega1=0.028540  omega1*Rmax=4.56634

vacuum, ell=2:
Rmax= 40  omega1=0.152076  omega1*Rmax=6.08303
Rmax= 80  omega1=0.074031  omega1*Rmax=5.92249
Rmax=160  omega1=0.036510  omega1*Rmax=5.84159
```

The regulated profile gives the same numbers at the shown precision. Therefore the low eigenvalues
collapse approximately as

```math
\omega_1 \sim {constant\over R_\mathrm{max}}.
```

First verdict:

The native scalar/angular operator on the asymptotically flat negative-phi vacuum branch does not by
itself create a genuine discrete particle spectrum. The finite outer box creates the discreteness. The
negative-phi core changes the inner boundary behavior, but it does not supply an absolute mass scale or a
standalone scalar particle ladder.

This is an honest negative and should be preserved. It narrows the path:

1. scalar/angular alone is not the particle sector;
2. the angular sector remains real modulation/selection structure;
3. the missing ingredient must be a native boundary, source, topology, nonlinear self-consistency, or a
   later probe sector;
4. the old spinor result may still be a useful diagnostic shadow, but cannot be re-imported as the
   foundation.

## 9. Topology of the negative-phi endpoint

For the vacuum negative-phi branch,

```math
f(r)=1+{a\over r},
```

the endpoint `r=0` is curvature-singular and removed from the regular manifold. A spatial slice therefore
has the topology

```math
(0,\infty)\times S^2,
```

equivalent to punctured three-space. This has a nontrivial two-sphere surrounding the removed endpoint.

Native consequence:

- the angular two-sphere is not just a local representation space;
- it is also the linking surface around the singular negative-phi core;
- radial flux sectors can be defined by integrals over that `S^2`.

For a closed two-form flux,

```math
F = q\sin\theta\,d\theta\wedge d\varphi,
```

the sphere integral is

```math
\int_{S^2}F = 4\pi q.
```

This is the first native route to charge-like sector labels: not from spinors, but from the punctured
negative-phi geometry plus the surviving angular sphere.

Caveat:

Topology gives a sector label, not yet a finite-energy particle or a mass. Integer quantization requires
extra structure, such as a compact U(1) bundle / charged matter consistency condition. The geometry alone
gives the puncture and the linking `S^2`; it does not yet give the charge unit.

## 10. Flux-energy test

Implemented in `native_flux_topology.py`.

For the UDT metric in `f` form,

```math
ds^2=-fdt^2+f^{-1}dr^2+r^2d\Omega^2,
```

the static Maxwell energy weight is

```math
N\sqrt{\gamma}=r^2\sin\theta.
```

The phi-dependence cancels. Radial electric or magnetic flux therefore has the classical radial scaling

```math
E_\mathrm{flux}\propto q^2\int_\epsilon^{R}{dr\over r^2}
= q^2\left({1\over\epsilon}-{1\over R}\right).
```

Numerical cutoff check:

```text
cutoff=1.00000  energy_scale= 0.9
cutoff=0.50000  energy_scale= 1.9
cutoff=0.25000  energy_scale= 3.9
cutoff=0.12500  energy_scale= 7.9
cutoff=0.06250  energy_scale=15.9
cutoff=0.03125  energy_scale=31.9
```

Second verdict:

The negative-phi puncture can support flux-sector topology, but the native metric does not regularize
classical radial U(1) flux energy. The divergence is the ordinary `1/epsilon` Coulomb/monopole divergence,
and it is phi-blind.

This creates a sharp tension:

1. singular puncture retained -> nontrivial `S^2` flux sectors, but divergent classical flux energy;
2. regular core imposed -> possible finite energy, but the puncture topology can disappear;
3. therefore the next native task is not "add charge"; it is to find whether UDT supplies a self-consistent
   core/boundary condition that preserves a quantized sector while removing the divergence.

This is the first serious candidate shape of the particle-sector problem:

```text
negative-phi core + angular S^2 linking + finite-energy boundary condition
```

not

```text
negative-phi well + imported spinor spectrum.
```

## 11. Radial flux back-reaction control

The native abelian sector can be included without importing a color force. For a radial electric or
magnetic flux, the compatible `B=1/A` sourced metric has the Reissner-Nordstrom-like form

```math
f(r)=1+{a\over r}+{q^2\over r^2}.
```

Equivalently,

```math
\phi(r)=-{1\over2}\ln\left(1+{a\over r}+{q^2\over r^2}\right).
```

The Einstein component is

```math
G^t{}_t=G^r{}_r=-{q^2\over r^4},
```

matching radial Maxwell stress up to conventions. This is native in the limited sense that the metric can
carry the abelian flux sector while preserving `G^t{}_t=G^r{}_r`.

But this does not regularize the core. Instead, as `r -> 0`,

```math
f(r)\sim {q^2\over r^2},
```

and the Misner-Sharp mass becomes

```math
m_\mathrm{MS}={r\over2}(1-f)
=-{a\over2}-{q^2\over2r}\to-\infty.
```

So the flux back-reaction strengthens the negative-phi singular endpoint; it does not resolve it.

The scalar/angular spectrum test was repeated with this charged profile using `native_scalar_spectrum.py`.
Representative low modes:

```text
charged, ell=0:
Rmax= 40  omega1=0.085983  omega1*Rmax=3.43932
Rmax= 80  omega1=0.041128  omega1*Rmax=3.29022
Rmax=160  omega1=0.020095  omega1*Rmax=3.21522

charged, ell=1:
Rmax= 40  omega1=0.119899  omega1*Rmax=4.79596
Rmax= 80  omega1=0.058034  omega1*Rmax=4.64272
Rmax=160  omega1=0.028541  omega1*Rmax=4.56652

charged, ell=2:
Rmax= 40  omega1=0.152233  omega1*Rmax=6.08932
Rmax= 80  omega1=0.074047  omega1*Rmax=5.92378
Rmax=160  omega1=0.036510  omega1*Rmax=5.84162
```

Third verdict:

Radial abelian flux is a real native sector label and a real back-reaction source, but it still does not
generate a scalar/angular mass ladder. The spectrum remains box-controlled. The singularity is not healed;
the source makes the core more singular.

Narrowed frontier:

```text
Find a finite-energy core/boundary mechanism that is neither a hard wall nor a Dirac import.
```

Candidate native places to look next:

1. finite-action boundary terms at the negative-phi endpoint;
2. nonlinear phi self-consistency with localized non-abelian-free angular stress;
3. topology plus a regularized core that preserves a boundary `S^2`;
4. an index/spin-structure route on the punctured spatial slice.

## 12. Monopole angular diagnostic

Implemented in `native_monopole_angular.py`.

If the punctured negative-phi endpoint carries a compact U(1) monopole sector with integer flux `n`, a
charged scalar on the linking `S^2` uses monopole harmonics rather than ordinary spherical harmonics:

```math
j={|n|\over2}+k,\qquad k=0,1,2,\ldots
```

with angular eigenvalues

```math
\lambda_j=j(j+1)-\left({n\over2}\right)^2
```

and degeneracy

```math
2j+1.
```

Small flux ladders:

```text
n=0:
  j=0,1,2,3        degeneracy=1,3,5,7

n=1:
  j=1/2,3/2,...    degeneracy=2,4,6,8

n=2:
  j=1,2,3,...      degeneracy=3,5,7,9

n=3:
  j=3/2,5/2,...    degeneracy=4,6,8,10
```

This is the first genuinely interesting topology/angular bridge:

- `n=1` gives a lowest doublet and half-integer angular labels;
- `n=2` gives a lowest triplet, matching the ordinary `ell=1` multiplicity but with shifted eigenvalue;
- odd flux sectors create spinor-like angular ladders for otherwise scalar probes.

But the caveat is load-bearing:

The metric puncture alone does not select `n=1`, does not quantize the charge unit, and does not derive
fermion statistics. The half-integer appears only after adding a compact U(1) flux sector and a charged
probe. So this route does not derive spin-1/2 from bare negative phi. It relocates the spin input into a
topological flux input.

Fourth verdict:

The topological route is promising as a classification mechanism, not yet as a derivation. It can explain
how the negative-phi endpoint plus angular sector could organize doublets/triplets without Form-T, but it
cannot yet claim those sectors are native particles.

Next narrowed question:

```text
Does UDT force a minimal flux sector at the negative-phi core, or is flux an additional input?
```

If flux is forced, the particle-sector rebuild has a real native route. If flux is optional, then the
monopole ladder is a useful diagnostic but not a derivation.

## 13. Minimal-flux audit

Corpus check:

- `UDT_REBUILD.md` keeps the static abelian Coulomb interaction as real metric-given dynamics:

```math
A_t = c_0 + {Q\over r}.
```

- In that clean statement, `Q` is a continuous source/integration constant. The metric cancellation gives
  the Coulomb equation; it does not by itself quantize `Q`.
- The old `udt_canonical_geometry.md` contains a stronger U(1) story, but it runs through the canonical
  Dirac action / local phase invariance / Form-T radial reduction chain. That is exactly the layer now
  under quarantine for this native rebuild.

Therefore:

```text
minimal flux is NOT currently forced by negative-phi geometry alone.
```

This downgrades the monopole route:

- **Useful:** it shows how a punctured negative-phi core plus angular `S^2` could organize doublets,
  triplets, and shifted angular ladders.
- **Not derived:** it requires a compact U(1) flux sector, a flux integer, and a charged probe.

Fifth verdict:

The native rebuild has not yet derived spin, charge quantization, or particle identity. It has produced a
cleaner map of the problem:

```text
negative phi supplies the singular/punctured geometric stage;
S^2 supplies angular representation structure;
abelian flux supplies possible topological sector labels;
none of those alone supplies finite masses or forced spin-1/2.
```

The next non-import move is now precise:

```text
Audit finite-action boundary conditions at the negative-phi endpoint.
```

If finite action selects a nontrivial boundary condition or residual boundary degree of freedom on the
linking `S^2`, that could be the first native particle-sector mechanism. If finite action only selects
trivial regularity, then the particle sector requires an additional postulate/probe beyond bare geometry.

## 14. Finite-action endpoint scaling

Implemented in `native_endpoint_scaling.py`.

Let the negative-phi endpoint scale as

```math
f=e^{-2\phi}\sim c r^{-p}.
```

Then

```math
\phi' \sim {p\over2r}.
```

For the C1-like dilation action density used in the rebuild,

```math
S_\phi \sim \int dr\, r^2 e^{-2\phi}g^{rr}(\phi')^2,
```

and since `g^{rr}=f`,

```math
r^2 e^{-2\phi}g^{rr}(\phi')^2
\sim r^2 f^2(\phi')^2
\sim r^{-2p}.
```

Therefore

```math
\int_0 r^{-2p}dr
```

is finite only when

```math
p < {1\over2}.
```

Controls:

```text
p=0.25  finite
p=0.50  logarithmically divergent
p=1.00  divergent as 1/epsilon      vacuum negative-phi branch
p=2.00  divergent as 1/epsilon^3    charged radial-flux branch
```

Sixth verdict:

The raw singular endpoint is not just a curvature singularity; under the C1 dilation action it is also an
infinite-action endpoint for the known vacuum and charged branches. A native particle cannot simply be
identified with the unsoftened `phi -> -infinity` core.

This makes Charles's "band / ensemble" framing sharper rather than weaker:

The particle sector is unlikely to be one solo mechanism. The current solo tests identify the instruments:

- negative phi supplies the inside-out geometric stage and radial/time weighting;
- the angular `S^2` supplies representation structure and modulation;
- the puncture supplies possible topological sector labels;
- abelian flux supplies a real metric-compatible interaction/back-reaction;
- finite action supplies a hard constraint on which cores are admissible.

The composition to test is therefore:

```text
negative phi + angular S^2 + topology/flux + finite-action endpoint softening
```

The target is not a deep singular well. The target is a self-consistent softened endpoint or boundary layer
that preserves enough `S^2`/flux structure to classify states while avoiding the infinite-action singular
core.

## 15. Softened endpoint and minimal ensemble probe

Implemented in:

- `native_softened_endpoint.py`
- `native_ensemble_probe.py`

Use the softened family

```math
f(r)=1+\left({a\over r}\right)^p.
```

For `p>0`, this still has

```math
\phi\to-\infty
```

at the endpoint. But finite C1 action requires

```math
p<1/2.
```

This family is not vacuum except at `p=1`:

```math
f''+{2f'\over r}\sim p(p-1)r^{-p-2}.
```

The metric source bookkeeping gives

```math
G^t{}_t=G^r{}_r\sim (1-p)r^{-p-2},
```

and

```math
R\sim -(p-1)(p-2)r^{-p-2}.
```

So a finite-action softened endpoint still requires a non-vacuum, singular source near the core. It is
not supplied by the known vacuum branch, and it is not the radial Maxwell branch.

Scalar/angular spectrum on softened endpoints:

```text
p=0.25, ell=0:
Rmax= 40  omega1=0.114282  omega1*Rmax=4.57129
Rmax= 80  omega1=0.054302  omega1*Rmax=4.34420
Rmax=160  omega1=0.025957  omega1*Rmax=4.15308

p=0.49, ell=0:
Rmax= 40  omega1=0.095490  omega1*Rmax=3.81961
Rmax= 80  omega1=0.045316  omega1*Rmax=3.62529
Rmax=160  omega1=0.021789  omega1*Rmax=3.48627
```

Then combine two instruments:

1. softened negative-phi radial geometry with `p<1/2`;
2. ordinary or monopole angular sectors on `S^2`.

Representative minimal-ensemble results:

```text
p=0.25, monopole n=1 lowest sector:
Rmax= 40  omega1=0.127636  omega1*Rmax=5.10544
Rmax= 80  omega1=0.060936  omega1*Rmax=4.87491
Rmax=160  omega1=0.029255  omega1*Rmax=4.68073

p=0.49, monopole n=2 lowest sector:
Rmax= 40  omega1=0.117313  omega1*Rmax=4.69250
Rmax= 80  omega1=0.056138  omega1*Rmax=4.49102
Rmax=160  omega1=0.027168  omega1*Rmax=4.34683
```

Seventh verdict:

The linear native ensemble

```text
softened negative phi + angular S^2 + monopole/topological angular shift
```

still does not make a standalone scalar particle ladder. It changes angular labels, degeneracies, and
mode constants, but the low modes remain controlled by the outer box.

This is not a rejection of the band/composition idea. It says the current instruments, when treated
linearly, are still missing a rhythm section: a finite-size/self-consistent boundary layer, nonlinear
source equation, or collective condition that localizes the composition without imposing a hard wall.

Narrowed next target:

```text
Find the native source/boundary layer that produces p<1/2 softening while preserving the S^2/topological
sector, then test the full ensemble on that self-consistent background.
```

## 16. Angular-source softening lead

Implemented in `native_angular_source_softening.py`.

The C1 vacuum equation is

```math
\phi''+{2\phi'\over r}-2(\phi')^2=0.
```

For a softened endpoint

```math
f=e^{-2\phi}\sim r^{-p},
```

we have

```math
\phi\sim -{p\over2}\ln r,
```

so

```math
\phi''+{2\phi'\over r}-2(\phi')^2
= {p(1-p)\over 2r^2}.
```

This is important because angular gradients naturally scale as

```math
{1\over r^2}.
```

So the ensemble route has a concrete mathematical shape:

```math
{p(1-p)\over2} = s_\mathrm{ang},
```

where `s_ang` is an effective angular/source strength.

If

```math
s_\mathrm{ang}=\eta\lambda,
```

with angular eigenvalue or monopole-harmonic value `lambda`, then

```math
p_\pm={1\over2}\left(1\pm\sqrt{1-8\eta\lambda}\right).
```

The finite-action branch is

```math
p_-= {1\over2}\left(1-\sqrt{1-8\eta\lambda}\right) < {1\over2}.
```

Representative map:

```text
eta=0.03:
  monopole n=1 lowest lambda=0.5  -> p_soft=0.03096
  monopole n=2 lowest lambda=1.0  -> p_soft=0.06411
  ordinary ell=1 lambda=2.0       -> p_soft=0.13944

eta=0.06:
  monopole n=1 lowest lambda=0.5  -> p_soft=0.06411
  monopole n=2 lowest lambda=1.0  -> p_soft=0.13944
  ordinary ell=1 lambda=2.0       -> p_soft=0.40000
```

This is the first positive ensemble mechanism candidate:

```text
angular S^2 stress can supply the exact 1/r^2 source shape needed to soften the negative-phi endpoint.
```

But the coefficient is not yet derived. This is where a small postulate may be legitimate.

## 17. Minimal-postulate ledger

The rebuild should not pretend everything is postulate-free if one or two simple inputs are actually doing
the work. The honest standard is:

```text
few postulates, named explicitly, each with a clear job and no hidden SM import.
```

Candidate postulates now visible:

### Candidate P1: finite-action endpoint admissibility

Physical negative-phi cores are not allowed to be raw infinite-action singular branches. A particle-sector
core must satisfy finite C1 action and preserve the linking `S^2` as a boundary/topological surface.

Status:

- mostly native, because it follows from taking the C1 action seriously;
- may need to be stated as an admissibility principle.

What it buys:

- rejects the raw vacuum `p=1` core as a particle;
- rejects the charged radial-flux `p=2` core as a particle;
- forces endpoint softening `p<1/2`.

### Candidate P2: compact angular/flux sector at the endpoint

The negative-phi core carries a compact angular/topological sector on the linking `S^2`, with an integer
flux or winding label.

Status:

- not yet derived from the metric alone;
- plausible as a simple topological input;
- dangerous if it smuggles in charge quantization or spin without being named.

What it buys:

- gives sector labels;
- gives monopole angular ladders;
- can produce doublets/triplets at the angular level;
- supplies a natural place for an angular `1/r^2` source.

### Candidate P3: angular-source coupling

Angular sector stress sources the phi equation with strength

```math
s_\mathrm{ang}=\eta\lambda.
```

Status:

- the `1/r^2` shape is native to angular gradients;
- the coefficient `eta` is not yet derived.

What it buys:

- produces finite-action softened negative-phi endpoints;
- ties endpoint depth profile to angular/topological labels;
- creates the first real composition mechanism:

```text
phi endpoint shape depends on angular sector.
```

Current judgment:

P1 is close to native. P2 and/or P3 may be acceptable as the one or two simple postulates if no derivation
is found. They are much cleaner than importing Form-T: they are geometric/topological/source rules, not a
full particle equation.

## 18. Localized angular-source core solve

Implemented in:

- `native_core_solver.py`
- `native_core_spectrum.py`

Use the candidate ensemble source equation

```math
\phi''+{2\phi'\over r}-2(\phi')^2={s\,W(r)\over r^2},
```

where `W(r)` is a core-localized angular source window. In

```math
x=\ln r,
```

the equation becomes

```math
f_{xx}+f_x+2sW(x)f=0.
```

This is useful because:

- inside the core, `W≈1`, so `f~r^{-p}` with `p(1-p)/2=s`;
- outside the core, `W≈0`, so `f=A+B/r`;
- after normalization, the exterior is

```math
f\to 1+{a\over r}.
```

Thus the localized angular source produces a finite-action softened core that matches to an ordinary UDT
negative-mass exterior tail.

Representative solve with `eta=0.03`, `s=eta*lambda`:

```text
monopole n=1, lambda=0.5:
  p_soft=0.03095842  a_tail=0.049219982  action_scale=0.00056618

monopole n=2, lambda=1:
  p_soft=0.06411011  a_tail=0.10335351  action_scale=0.00266656

ordinary ell=1, lambda=2:
  p_soft=0.13944487  a_tail=0.23276698  action_scale=0.01604143
```

The exterior tail and action scale are stable as the inner cutoff moves inward. The endpoint value of
`phi` keeps deepening, as it should for `phi -> -infinity`, while the exterior data remain fixed.

This is the first constructive ensemble result:

```text
localized angular stress can soften the negative-phi endpoint into a finite-action core and match it to a
UDT exterior.
```

But the scalar spectrum on this constructive background remains box-controlled:

```text
eta=0.03, monopole n=1:
Rmax= 40  omega1=0.091365  omega1*Rmax=3.65461
Rmax= 80  omega1=0.045639  omega1*Rmax=3.65109
Rmax=160  omega1=0.022808  omega1*Rmax=3.64930

eta=0.03, monopole n=2:
Rmax= 40  omega1=0.100057  omega1*Rmax=4.00229
Rmax= 80  omega1=0.049935  omega1*Rmax=3.99482
Rmax=160  omega1=0.024944  omega1*Rmax=3.99103

eta=0.03, ordinary ell=1:
Rmax= 40  omega1=0.113123  omega1*Rmax=4.52492
Rmax= 80  omega1=0.056346  omega1*Rmax=4.50770
Rmax=160  omega1=0.028119  omega1*Rmax=4.49898
```

Eighth verdict:

The localized angular-source ensemble solves the core-admissibility problem but not the particle-locality
problem. It gives a finite-action negative-phi core with angular/topological labels, but the linear scalar
probe still sees an asymptotically flat continuum. Discreteness appears only when an outer scale/boundary is
imposed.

This clarifies the remaining missing instrument:

```text
finite-action core + angular/topological labels is not enough;
the particle sector also needs a localization/gap/outer-boundary mechanism.
```

Candidate ways this could enter, in increasing order of cost:

1. a native `phi=0` interface condition that makes each matter core a finite cell;
2. a nonlinear self-trapped collective mode rather than a linear scalar probe;
3. a small explicit probe postulate, such as spin-1/2/Dirac, but now on the softened native core rather than
   on the old Form-T scaffold;
4. an additional dimensionful scale/anchor if no native cell size emerges.

## 19. Finite phi-zero interface audit

Implemented in `native_interface_audit.py`.

The localized angular-source core naturally matches outside the source to

```math
f(r)=1+{a\over r}.
```

Since

```math
\phi=-{1\over2}\ln f,
```

`phi=0` means `f=1`. A smooth finite-radius match to exactly flat exterior requires both

```math
f(R)=1,\qquad f_x(R)=0.
```

In the exterior form this is equivalent to

```math
a=0.
```

Scan result:

```text
width=0.25, eta=0.03:
  monopole n=1 source=0.015  a_tail=0.0352922
  monopole n=2 source=0.030  a_tail=0.0752293
  ell=1       source=0.060  a_tail=0.175548

width=0.50, eta=0.03:
  monopole n=1 source=0.015  a_tail=0.0492200
  monopole n=2 source=0.030  a_tail=0.103354
  ell=1       source=0.060  a_tail=0.232767

width=1.00, eta=0.03:
  monopole n=1 source=0.015  a_tail=0.243131
  monopole n=2 source=0.030  a_tail=0.493282
  ell=1       source=0.060  a_tail=1.02142
```

Across positive source strengths and widths, `a_tail>0`. It tends to zero only as the source turns off.

Ninth verdict:

A finite `phi=0` matter-cell boundary is not produced for free by the localized angular-source core. The
core wants to carry an exterior negative-mass tail. To make a finite cell, UDT needs either:

1. a boundary layer/shell at the `phi=0` interface;
2. an opposing source contribution that cancels the exterior tail;
3. a nonlinear global condition that sets `a_tail=0`;
4. or acceptance that the matter-side object has a long-range negative-mass tail and the spectrum is not
   cell-discrete.

This is the cleanest place for a simple postulate if Charles allows one:

```text
Matter Cell Postulate:
A particle-sector core is a finite-action negative-phi endpoint with compact angular/topological source,
matched at a phi=0 interface by a boundary layer whose net exterior monopole tail vanishes.
```

This single postulate would combine the previously separate P1/P2/P3/P4 roles:

- finite action,
- compact endpoint angular sector,
- angular-source softening,
- finite `phi=0` cell closure.

What remains derived after that postulate:

- allowed endpoint powers `p<1/2`;
- angular dependence of endpoint softening through `lambda`;
- doublet/triplet angular sector structure if compact flux is included;
- discrete finite-cell spectra once the cell size/boundary condition is specified.

What would still not be derived:

- the numerical coupling `eta`;
- the cell radius or absolute scale, unless the zero-tail condition fixes it;
- spin statistics;
- observed mass hierarchy.

## 20. Matter-cell spectrum under the postulate

Implemented in `native_cell_spectrum.py`.

Assume the candidate Matter Cell Postulate operationally:

1. solve the localized angular-source core inside a finite cell;
2. normalize the boundary to

```math
f(R_\mathrm{cell})=1 \quad\Longleftrightarrow\quad \phi(R_\mathrm{cell})=0;
```

3. do not model the boundary layer yet;
4. compute the scalar/angular finite-cell spectrum.

Set

```math
R_\mathrm{cell}=1
```

so all frequencies are dimensionless `omega*R_cell`.

Representative result with `eta=0.03`, source centered at `x_core=-2.5`, width `0.5`:

```text
monopole n=1, lambda=0.5, degeneracy=2:
  p=0.0309584, phi_inner=-0.284530
  Dirichlet omega*R = 3.65752, 6.84802, 10.0235, 13.1955
  flux      omega*R = 1.13314, 5.05625,  8.3171, 11.5253

monopole n=2, lambda=1, degeneracy=3:
  p=0.0641101, phi_inner=-0.589473
  Dirichlet omega*R = 4.00707, 7.24021, 10.4486, 13.6516
  flux      omega*R = 1.54289, 5.43846,  8.7302, 11.9683

ordinary ell=1, lambda=2, degeneracy=3:
  p=0.139445, phi_inner=-1.28354
  Dirichlet omega*R = 4.53241, 7.84459, 11.1199, 14.3880
  flux      omega*R = 2.08975, 6.01677,  9.3734, 12.6751
```

Tenth verdict:

Once the finite cell is postulated, the ensemble produces clean discrete dimensionless spectra. However,
the boundary condition changes the ground mode substantially. Therefore the finite-cell spectrum is not yet
a prediction. The boundary layer is load-bearing.

What this accomplishes:

- gives a concrete non-Dirac particle-sector scaffold;
- ties core depth to angular/source sector;
- preserves doublet/triplet labels through topology/angular structure;
- produces dimensionless finite-cell spectra.

What remains open:

- derive the boundary layer and its spectral boundary condition;
- derive or postulate `eta`;
- derive or anchor `R_cell`;
- determine whether the physical particle sector uses scalar collective modes, a spinor probe on this
  native core, or another field/operator.

Current best rebuild frame:

```text
UDT native geometry gets us to:
finite-action negative-phi matter cell + angular/topological sector labels + dimensionless spectra.

It does not yet get us to:
spin statistics, absolute masses, or the observed hierarchy.
```

## 21. Electron anchor discipline

The electron mass can remain the single dimensionful anchor.

This is not a retreat. It is the clean scale convention already allowed in the rebuild:

```text
dimensionless geometry first; one measured mass fixes the unit.
```

For the finite-cell spectra, the conversion is

```math
M_i = m_e{\omega_i\over\omega_e},
```

where `omega_e` is the dimensionless mode chosen as the electron anchor.

Implemented in `native_cell_spectrum.py` with:

```text
--electron-sector monopole1 --electron-bc flux
```

Using `eta=0.03`, `x_core=-2.5`, width `0.5`, and anchoring the lowest monopole-`n=1`
flux-boundary mode to

```math
m_e=0.51099895\ \mathrm{MeV},
```

gives

```text
omega_e = 1.1331374
scale = 0.45095939 MeV per dimensionless omega
```

Anchored masses from that same run:

```text
monopole1 flux:
  0.510999, 2.28017, 3.75065, 5.19743 MeV

monopole2 flux:
  0.695779, 2.45252, 3.93695, 5.39721 MeV

ell1 flux:
  0.942392, 2.71332, 4.22702, 5.71595 MeV
```

Verdict:

The electron anchor converts the finite-cell dimensionless spectra into masses, but the current scalar-cell
ensemble remains compressed and MeV-scale. It does not reproduce the observed hierarchy. That is acceptable
at this stage: the anchor supplies units, not the hierarchy.

Updated status:

- **Allowed input:** one dimensionful scale, `m_e`.
- **Still open:** which dimensionless mode is the electron; the boundary condition; the coupling `eta`; the
  hierarchy mechanism.
- **Do not claim:** these anchored scalar-cell masses are predictions.

This makes the postulate budget clearer:

```text
P1/Pcell: matter-cell admissibility and phi=0 boundary layer.
P2/P3: compact angular/flux sector and angular-source coupling, unless derived.
F: electron mass anchor.
```

That is a small, explicit input set. The next work should try to reduce P2/P3 or derive the boundary layer;
the electron anchor can stay.

## 22. Boundary-layer audit

Implemented in:

- `native_boundary_scan.py`
- `native_shell_stress.py`

The finite cell currently hides its `phi=0` boundary layer. Make that explicit.

At the cell boundary,

```math
f(R)=1.
```

Exterior flat closure requires

```math
f_\mathrm{out}=1,\qquad f_{x,\mathrm{out}}=0.
```

The interior softened core generally has

```math
f_{x,\mathrm{in}}<0.
```

Therefore the boundary layer must supply the jump

```math
\Delta f_x=f_{x,\mathrm{out}}-f_{x,\mathrm{in}}=-f_{x,\mathrm{in}}.
```

For the current reference cell (`eta=0.03`, `x_core=-2.5`, width `0.5`):

```text
monopole n=1:
  f_x(in)=-0.00382390  jump=0.00382390

monopole n=2:
  f_x(in)=-0.00801399  jump=0.00801399

ordinary ell=1:
  f_x(in)=-0.01795973  jump=0.01795973
```

In an idealized thin-shell bookkeeping at `R_cell=1`, with `f_in=f_out=1`, the angular extrinsic curvature
is continuous, so the shell has zero surface energy in this simplified junction model. The derivative jump
appears as a tangential pressure/tension load:

```math
\sigma_\mathrm{shell}=0,
```

```math
P_\mathrm{shell}\sim {\Delta f_x\over16\pi}.
```

Numerically:

```text
monopole n=1: P_shell=0.0000761
monopole n=2: P_shell=0.0001594
ordinary ell=1: P_shell=0.0003573
```

This is not yet a derivation of the shell. It turns the boundary-layer postulate into a concrete target:

```text
derive a phi=0 surface stress whose pressure cancels the interior derivative tail while preserving f=1.
```

## 23. Boundary-condition sensitivity

The spectral boundary condition can be parameterized as

```math
p(R)R'(R)+\beta R(R)=0.
```

Here `beta=0` is natural zero-flux. Large `beta` approaches Dirichlet.

Reference Robin scan:

```text
monopole n=1:
  beta=0       omega=1.13310, 5.05608, 8.31676   ratios=1, 4.4622, 7.3398
  beta=1000    omega=1.76703, 5.18224, 8.39288   ratios=1, 2.9327, 4.7497
  beta=100000  omega=3.60078, 6.74191, 9.86870   ratios=1, 1.8723, 2.7407

monopole n=2:
  beta=0       omega=1.54283, 5.43827, 8.72985   ratios=1, 3.5249, 5.6583
  beta=1000    omega=2.08243, 5.55807, 8.80335   ratios=1, 2.6690, 4.2274
  beta=100000  omega=3.94459, 7.12731, 10.2862   ratios=1, 1.8069, 2.6077

ordinary ell=1:
  beta=0       omega=2.08967, 6.01656, 9.37305   ratios=1, 2.8792, 4.4854
  beta=1000    omega=2.54841, 6.12882, 9.44330   ratios=1, 2.4050, 3.7056
  beta=100000  omega=4.46097, 7.72056, 10.9443   ratios=1, 1.7307, 2.4534
```

Eleventh verdict:

The boundary condition is load-bearing. It changes not just the absolute ground mode but also the low
ratios. Therefore the `phi=0` boundary layer cannot be treated as a harmless technicality. It is part of
the particle-sector mechanism.

Updated minimal postulate shape:

```text
Matter Cell Postulate:
A particle-sector core is a finite-action negative-phi endpoint with compact angular/topological source,
closed at a phi=0 surface by a boundary layer whose stress cancels the exterior monopole tail and whose
dynamics fixes the spectral boundary condition.
```

This is now specific enough to attack. The next frontier is to derive that boundary layer from the UDT
action or admit it as a named postulate.

Small-jump check:

If the Robin coefficient is of the same dimensionless order as the geometric derivative jump, then the
spectrum is effectively the natural flux spectrum:

```text
monopole n=1 jump≈0.003824:
  beta=0        omega=1.13310, 5.05608, 8.31676
  beta=0.0038   omega=1.13310, 5.05608, 8.31676

monopole n=2 jump≈0.008014:
  beta=0        omega=1.54283, 5.43827, 8.72985
  beta=0.0080   omega=1.54284, 5.43827, 8.72985

ordinary ell=1 jump≈0.017960:
  beta=0        omega=2.08967, 6.01656, 9.37305
  beta=0.0180   omega=2.08968, 6.01656, 9.37306
```

So a Dirichlet-like wall cannot be smuggled in as "the thin shell" unless the shell has a large stiffness
not explained by the geometric jump. The conservative default for the matter-cell spectrum is therefore
the flux/natural boundary condition until a stronger boundary-layer dynamics is derived.

## 24. Angular-sector staging

Implemented in `native_angular_staging.py`.

Answer to the staging question:

```text
No, do not bring in the full angular sector yet.
```

The matter-cell scaffold is not ready for all angular instruments. Bring in only the components whose
inputs are already present and whose status survived the re-audit without importing spinors or SM labels.

### Include now

1. **Round `S^2` eigenvalues**

```math
\lambda_\ell=\ell(\ell+1).
```

Status: native metric kinematics.

Use: scalar/angular cell spectra and angular source strength.

2. **Multiplicity**

```math
2\ell+1.
```

Status: native metric kinematics.

Use: degeneracy and angular-sector bookkeeping.

3. **Monopole harmonics, only under explicit compact-flux postulate P2**

```math
j={|n|\over2}+k,\qquad
\lambda=j(j+1)-\left({n\over2}\right)^2.
```

Status: candidate compact endpoint/flux sector, not bare metric.

Use: doublet/triplet angular sector labels.

4. **`ell=1` operator algebra**

The traceless operators on the `ell=1` three-dimensional angular space give

```math
8=3+5.
```

Status: derived angular kinematics.

Use now only as representation bookkeeping. Do not call it a color force.

5. **`epsilon_abc` singlet**

The totally antisymmetric triple has count

```math
\dim\Lambda^3 V={N(N-1)(N-2)\over6}.
```

So:

```text
N=1 -> 0
N=2 -> 0
N=3 -> 1  unique epsilon case
N=4 -> 4
N=5 -> 10
```

Status: derived angular kinematics.

Use: selection/observability rule for three `ell=1` sectors.

### Defer

1. **Rank-2 `Y_2` coupling matrix**

Status: matrix structure is solid, but the origin and magnitude as metric back-reaction are open.

Reason to defer: it would add a strong angular coupling before the matter-cell boundary layer and
angular-source coefficient `eta` are pinned. That would create too many adjustable levers.

2. **Parity blocks**

Status: tied to full spinor angular structure.

Reason to defer: it depends on the spinor/Form-T layer we are currently avoiding.

3. **`kappa` channel ladder**

Status: Dirac/spinor-dependent.

Reason to defer: not native to the current scalar/topological matter-cell scaffold.

4. **Color force / confinement dynamics**

Status: not metric-given.

Reason to defer: the rebuild explicitly says there is no metric-given color force.

5. **SM charge/flavor/mass labels**

Status: labels/fits.

Reason to defer: not part of native geometry assembly.

Twelfth verdict:

The angular sector should enter in layers:

```text
Layer A: S^2 eigenvalues + multiplicities.
Layer B: compact-flux/monopole angular sectors, if P2 is admitted.
Layer C: ell=1 su(3) kinematic bookkeeping + epsilon singlet selection.
Layer D: rank-2/parity/kappa structure only after boundary-layer dynamics is pinned, and probably only if
         a spinor probe is explicitly reintroduced.
```

So the current build is not missing the whole angular sector by accident. It is intentionally using only
Layers A and B, and now it can safely add Layer C as a selection rule. Layer D is premature.

## 25. Layer-C selection rule added

Implemented in `native_selection_rules.py`.

This adds only the safe angular selection rule:

```text
unique epsilon selection exists only for a three-dimensional angular sector.
```

It does not add binding, confinement, a color force, rank-2 dynamics, or SM labels.

Results:

```text
ordinary ell=0:
  dimension=1, Lambda^3 count=0

monopole n=1 lowest:
  dimension=2, Lambda^3 count=0

monopole n=2 lowest:
  dimension=3, Lambda^3 count=1  unique epsilon eligible

ordinary ell=1:
  dimension=3, Lambda^3 count=1  unique epsilon eligible

ordinary ell=2:
  dimension=5, Lambda^3 count=10 not unique
```

Implication for the current matter-cell scaffold:

- the lowest monopole `n=1` sector is a doublet candidate, useful for electron-like anchoring if P2 is
  admitted, but it is not an epsilon-triplet sector;
- monopole `n=2` and ordinary `ell=1` are the triplet sectors eligible for the unique antisymmetric
  selection rule;
- epsilon selection is an observability/projection rule, not a binding mechanism.

Thirteenth verdict:

Layer C can be included now, but only as kinematic selection. It should not be used to claim confinement
or mass generation. The next calculation should ask whether the Matter Cell Postulate plus Layer-C
selection changes ensemble counting or allowed composite states, not whether it creates a force.

## 26. Composite counting under Layer C

Implemented in `native_composite_counting.py`.

This is kinematic bookkeeping only:

```text
No binding, no confinement, no mass rule.
```

Reference single-cell sectors from the `eta=0.03`, flux-boundary finite-cell run:

```text
M1 = monopole n=1 lowest, dimension 2, omega=1.13314
M2 = monopole n=2 lowest, dimension 3, omega=1.54289
E1 = ordinary ell=1,      dimension 3, omega=2.08975
```

Epsilon eligibility:

```text
M1+M1+M1: epsilon_count=0
M2+M2+M2: epsilon_count=1
E1+E1+E1: epsilon_count=1
```

Mixed triplets are not selected by this minimal epsilon rule.

With the electron anchor using `M1` as the electron placeholder:

```text
scale = 0.45095835 MeV per omega
```

Naive same-sector sums are:

```text
M1+M1+M1: 1.53300 MeV, not epsilon-selected
M2+M2+M2: 2.08734 MeV, epsilon-selected
E1+E1+E1: 2.82717 MeV, epsilon-selected
```

Fourteenth verdict:

Layer-C selection gives clean allowed/forbidden composite bookkeeping, but it does not create binding or
mass hierarchy. The electron-anchored naive sums remain MeV-scale and compressed.

This is useful because it prevents a false upgrade:

```text
epsilon selection = observability/composite eligibility, not confinement and not mass emergence.
```

The next missing instrument is therefore not more kinematic angular algebra. It is a dynamical or
collective contribution that can change energy scales/ratios after the allowed sectors are selected.

## 27. Energy-scale ledger

Implemented in `native_energy_ledger.py`.

Question:

```text
What can break the compressed 1/R finite-cell spectrum after the electron anchor?
```

Current ledger:

```text
linear cell eigenfrequency:
  scaling: 1/R
  hierarchy potential: low

angular-source core action:
  scaling: dimensionless/R? normalization open
  hierarchy potential: medium

phi=0 shell pressure:
  scaling: surface term, normalization open
  hierarchy potential: medium

abelian Coulomb:
  scaling: alpha/R
  hierarchy potential: low-medium unless running/charge structure enters

epsilon selection:
  scaling: no energy
  hierarchy potential: none

rank-2 angular coupling:
  deferred; magnitude unknown

spinor/probe zero-point:
  deferred; could matter but imports spin structure

running/quantum collective effects:
  open; highest hierarchy potential
```

Fifteenth verdict:

Adding more kinematic angular algebra will not solve the hierarchy. The next native energy work should be:

1. derive the normalization of the angular-source core action;
2. derive the normalization/dynamics of the `phi=0` shell;
3. only then assemble Coulomb and Layer-C selection;
4. defer rank-2/spinor machinery until the native cell energy ledger is exhausted.

This keeps the band/composition picture, but avoids adding instruments that are only labels.

## 28. Core/shell energy normalization audit

Implemented in `native_energy_normalization.py`.

This compares, on the same finite-cell profiles:

1. the lowest linear flux-boundary eigenfrequency `omega1`;
2. the C1-like core action scale

```math
S_\mathrm{core}\sim\int {f_x^2\over4} r\,dx;
```

3. the idealized shell load

```math
P_\mathrm{shell}\sim{\Delta f_x\over16\pi}.
```

The absolute normalization of core/shell energy is not derived here. This is a size audit.

Reference `eta=0.03`, electron anchor on `monopole1`:

```text
monopole1:
  omega1=1.133098 -> 0.510999 MeV
  core_action=0.0000423 = 0.0000373 of omega1
  shell_pressure=0.0000761 = 0.0000671 of omega1

monopole2:
  omega1=1.542831 -> 0.695778 MeV
  core_action=0.0001985 = 0.0001287 of omega1
  shell_pressure=0.0001594 = 0.0001033 of omega1

ell1:
  omega1=2.089675 -> 0.942391 MeV
  core_action=0.0011849 = 0.0005670 of omega1
  shell_pressure=0.0003573 = 0.0001710 of omega1
```

Near the admissibility edge, `eta=0.062`:

```text
ell1:
  p=0.455279
  omega1=2.115089 -> 0.952546 MeV
  core_action=0.105556 = 0.049906 of omega1
  shell_pressure=0.001408 = 0.000666 of omega1
```

Sixteenth verdict:

With natural unit normalization, the classical core-action and shell-load terms are too small to generate
the observed hierarchy. The core action can become non-negligible near the finite-action edge, but it still
does not create orders of magnitude. The shell load is smaller.

Therefore the hierarchy is not in:

```text
linear cell spectrum + unit-normalized classical core action + unit-normalized shell load.
```

Remaining live possibilities:

1. a large derived normalization for the core/shell sector;
2. nonlinear amplification or collective self-trapping;
3. quantum/running effects;
4. reintroducing a small explicit probe postulate, such as spin-1/2, but on the native matter cell rather
   than the old Form-T scaffold.

## 29. Scale-covariance audit

Implemented in `native_scale_covariance.py`.

If a matter cell of radius `R` is obtained by scaling the dimensionless `R=1` solution, the classical
terms tested so far have the form

```math
E_i(R)={c_i\over R}.
```

The electron anchor fixes one such coefficient:

```math
m_e={c_e\over R_e}.
```

If every sector shares the same `R`, changing `R` rescales all classical energies together. It cannot
produce a hierarchy.

Reference coefficients:

```text
M1_flux  = 1.13314
M2_flux  = 1.54289
E1_flux  = 2.08975
M1_core  = 0.0000423
M2_core  = 0.0001985
E1_core  = 0.0011849
M1_shell = 0.0000761
M2_shell = 0.0001594
E1_shell = 0.0003573
```

With the electron anchor on `M1_flux`, changing the common cell radius gives:

```text
R=0.5: M1=1.022 MeV, M2=1.392 MeV, E1=1.885 MeV
R=1.0: M1=0.511 MeV, M2=0.696 MeV, E1=0.942 MeV
R=2.0: M1=0.255 MeV, M2=0.348 MeV, E1=0.471 MeV
```

Ratios do not change.

Seventeenth verdict:

The current classical matter-cell scaffold is scale-covariant. The electron anchor can set the unit, but
it cannot create the hierarchy. To get a hierarchy from this route, UDT needs one of:

1. sector-dependent cell radii derived from a native condition;
2. large derived coefficients in the core/shell sector;
3. nonlinear/collective amplification;
4. quantum/running effects;
5. a reintroduced probe postulate with new spectral structure.

This matches the earlier rebuild conclusion: classical geometry gives structure and a scale carrier, not
the full hierarchy by itself.

## 30. Classical parameter sensitivity

Implemented in `native_parameter_scan.py`.

Scan:

```text
eta     = 0.005, 0.01, 0.03, 0.05, 0.06
x_core  = -4, -2.5, -1, 0
width   = 0.25, 0.5, 1.0
```

Observable:

```text
flux-boundary ground-mode ratios relative to M1.
```

Result:

```text
M2/M1:
  min = 1.3602247
  max = 1.3775399

E1/M1:
  min = 1.838773
  max = 1.9374711
```

The most favorable points differ only at the order-one / few-percent level:

```text
M2/M1 min:
  eta=0.005, x_core=-4, width=0.25

M2/M1 max:
  eta=0.06, x_core=0, width=0.25

E1/M1 min:
  eta=0.005, x_core=-4, width=0.25

E1/M1 max:
  eta=0.06, x_core=0, width=0.25
```

Eighteenth verdict:

The continuous classical cell-shape parameters do not generate a hierarchy. They shift the low spectrum by
order-one factors and mostly preserve the compressed structure.

This rules out a tempting loophole:

```text
The hierarchy is not hidden in eta/x_core/width tuning of the classical finite cell.
```

Remaining live hierarchy mechanisms are now sharply narrowed:

1. a new derived large coefficient;
2. sector-dependent cell radii from a nontrivial native condition;
3. nonlinear/collective self-trapping;
4. quantum/running effects;
5. a small explicit spin/probe postulate.

## 31. Required sector-dependent radii

Implemented in `native_required_radii.py`.

If the electron anchor is fixed by coefficient `c_e`, and another mode has coefficient `c_i`, then a target
mass ratio requires

```math
{R_i\over R_e}={c_i/c_e\over M_i/M_e}.
```

Using the reference flux-boundary coefficients:

```text
M1_1 = 1.13314  electron anchor
M2_1 = 1.54289
E1_1 = 2.08975
```

Muon-like ratio:

```text
M2_1 assignment: R_i/R_e = 0.006585  (R_e/R_i = 151.9)
E1_1 assignment: R_i/R_e = 0.008919  (R_e/R_i = 112.1)
```

Tau-like ratio:

```text
M2_1 assignment: R_i/R_e = 0.000392  (R_e/R_i = 2553.7)
E1_1 assignment: R_i/R_e = 0.000530  (R_e/R_i = 1885.4)
```

Using higher radial modes helps only by factors of a few, not orders of magnitude.

Nineteenth verdict:

A sector-dependent radius rule could mathematically carry the hierarchy, but the required radius ratios are
large:

```text
muon-like: 10^2 smaller cell scale
tau-like: 10^3 smaller cell scale
```

Therefore this is not a free rescue. UDT would need a native quantization/running/collective rule that
generates those radii. Hand-assigning them would be equivalent to fitting the hierarchy.

## 32. Running/log-scale requirement

Implemented in `native_running_requirements.py`.

If hierarchy is carried by sector-dependent radii, define

```math
\Delta_i=\ln{R_e\over R_i}
=\ln\left({M_i/M_e\over c_i/c_e}\right).
```

Then the required radius hierarchy becomes a logarithmic gap.

Muon-like assignments:

```text
M2_1: Delta=5.02293
E1_1: Delta=4.71955
M1_2: Delta=3.83597
```

Tau-like assignments:

```text
M2_1: Delta=7.84530
E1_1: Delta=7.54192
M1_3: Delta=6.16065
```

Twentieth verdict:

The classical cell does not generate these gaps, but the required logarithmic separations are not absurd:

```text
muon-like: Delta roughly 3-5
tau-like:  Delta roughly 6-8
```

This makes a true running/collective mechanism the best remaining hierarchy lead. The task is now specific:

```text
derive a UDT-native flow or collective condition that produces sector-dependent log scales Delta(lambda, n, ...).
```

Without that, the electron anchor plus finite cells remains a compressed scale-covariant spectrum.

## 33. Missing angular piece audit

Implemented in:

- `native_boundary_ratio_limits.py`
- `native_angular_operator_catalog.py`

Question:

```text
Could the angular sector be missing a hierarchy-generating piece?
```

Answer:

```text
Possibly, but not as ordinary angular kinematics.
```

### Boundary stiffness test

Hypothesis:

```text
the missing angular piece is a sector-dependent Robin stiffness beta(lambda)
at the phi=0 boundary.
```

Scan positive `beta` from natural flux to very stiff/Dirichlet-like behavior.

With the same `beta` applied to the compared sectors:

```text
M2/M1 range: 1.09549 to 1.36160
E1/M1 range: 1.23893 to 1.84421
```

Even under the generous test where the target sector gets arbitrary positive `beta` while the electron
placeholder stays at natural flux:

```text
M2/M1 max: 3.53352
E1/M1 max: 3.99674
```

Verdict:

```text
boundary stiffness beta(lambda) alone cannot create lepton-like hierarchy.
```

### Higher angular operator test

Ordinary angular operators grow polynomially:

```math
\lambda_\ell=\ell(\ell+1).
```

Vector/tensor variants shift this by order-one constants:

```math
\ell(\ell+1)-1,\qquad \ell(\ell+1)-2.
```

To get a mass ratio directly from

```math
\sqrt{\ell(\ell+1)}
```

would require:

```text
muon-like ratio: ell ≈ 207
tau-like ratio:  ell ≈ 3477
```

No current native angular rule selects such huge `ell`, and introducing one by hand would be a fit.

Twenty-first verdict:

The missing angular piece, if real, is not likely to be:

1. ordinary higher-`ell` kinematics;
2. scalar/vector/tensor harmonic eigenvalue shifts;
3. a simple Robin boundary stiffness `beta(lambda)`;
4. epsilon selection alone.

The only angular-sector possibilities still worth pursuing are dynamical:

1. an angular determinant / Casimir / quantum boundary effect;
2. a spin^c / index mechanism tied to compact flux;
3. a rank-2 angular back-reaction operator with derived magnitude;
4. angular-sector running that generates log scales `Delta(lambda)`.

So yes, the angular sector may be missing a piece, but it must be an angular **dynamics/quantum/index**
piece, not more classical angular bookkeeping.

## 34. Angular determinant diagnostic

Implemented in `native_angular_determinant.py`.

Candidate:

```text
an angular quantum determinant / Casimir-like boundary term generates running or log-scale gaps.
```

Diagnostic sum:

```math
\log\det_L=\sum_{\mathrm{levels}\le L} d_i\log(\lambda_i+\mu^2).
```

With `mu2=1`, increasing cutoff gives:

```text
cutoff   n2-n1 determinant difference
5        23.0806
10       54.3688
20       129.5059
40       306.1603
80       713.5541
160      1637.8686
```

These raw determinant differences do not stabilize. They are cutoff/renormalization dependent.

Twenty-second verdict:

Angular determinants are a plausible place for running/log-scale behavior, but not a prediction until UDT
supplies a native subtraction or renormalization rule. This is the right *type* of missing angular piece,
but not yet a derived mechanism.

What would be needed:

```text
1. define the angular operator whose determinant belongs on the phi=0 boundary;
2. define the UDT-native subtraction/reference sector;
3. show the finite remainder or RG flow produces Delta ~ 3-8;
4. verify it does not re-import SM/QFT structure under another name.

## 35. Native angular physics vs SM analogs

Important correction:

The angular sector should not be judged only by whether it matches Standard Model analogs. Much of the old
angular work was framed through SM-like labels because those were the available comparison targets. But the
metric's angular sector may contain native physics with no current Standard Model counterpart.

So the rebuild needs two tracks:

```text
Track A: SM-analog audit
  Which angular structures correspond to familiar labels such as charge/color/flavor/spin?

Track B: Native angular physics
  Which angular structures are real consequences of the metric even if they do not map to known labels?
```

The current matter-cell work belongs mostly to Track B.

Track-B candidates already visible:

1. **Endpoint angular source**

Angular gradients naturally supply a `1/r^2` source that can soften the negative-phi endpoint. This is not
an SM analog. It is native geometry.

2. **Phi-zero boundary dynamics**

The angular sector may determine the boundary layer at the matter-cell interface. This need not correspond
to any known force.

3. **Angular determinant / boundary RG**

The angular spectrum may generate running/log-scale behavior through a native determinant. This is not
automatically QFT as currently modeled; it could be a UDT boundary effect.

4. **Triplet/singlet observability**

The epsilon selection rule may be a native observability condition, not QCD confinement.

5. **Monopole/spin-c endpoint structure**

If compact endpoint flux is admitted or derived, angular doublets/triplets may be native endpoint sectors,
not necessarily electron/quark labels.

Revised discipline:

```text
Do not discard angular structures merely because their old SM label failed.
Do discard SM labels when the native structure does not require them.
```

Twenty-third verdict:

The missing angular piece may be real native UDT physics, not a missing Standard Model imitation. The next
angular work should search for native angular invariants and boundary/RG rules first, then only later ask
whether any of them resemble known particle sectors.

## 36. Native angular invariant catalog and admissibility cap

Implemented in:

- `native_angular_invariants.py`
- `native_angular_admissibility.py`

The angular-source softening equation gives

```math
{p(1-p)\over2}=\eta\lambda.
```

Real softened branches require

```math
\eta\lambda\le {1\over8}.
```

Finite action requires the strict version:

```math
\eta\lambda< {1\over8}.
```

Therefore the angular sector has a native admissibility cap:

```math
\lambda < {1\over8\eta}.
```

This is not an SM analog. It is a UDT-native angular selection rule from endpoint admissibility.

Reference `eta=0.03`:

```text
lambda_cap = 4.1667

ordinary:
  ell=0 allowed
  ell=1 allowed, lambda=2, p=0.139445
  ell=2 excluded, lambda=6

monopole lowest sectors:
  n=1 allowed, lambda=0.5, p=0.030958
  n=2 allowed, lambda=1.0, p=0.064110
  n=3 allowed, lambda=1.5, p=0.100000
  n=4 allowed, lambda=2.0, p=0.139445
  n=8 allowed, lambda=4.0, p=0.400000
```

Near the special value

```math
\eta={1\over16}=0.0625,
```

the cap is

```math
\lambda_\mathrm{cap}=2.
```

This puts ordinary `ell=1` (`lambda=2`) exactly at the logarithmic edge `p=1/2`. Just below this value,
ordinary `ell=1` is the highest finite-action ordinary spherical sector; ordinary `ell=2` is excluded.

Example:

```text
eta=0.0624:
  lambda_cap=2.00321
  ell=1 allowed with p=0.48
  ell=2 excluded
```

Twenty-fourth verdict:

This is the first native angular reason for `ell=1` specialness in the matter-cell rebuild. It is not
derived fully until `eta` is derived, but the structure is real:

```text
finite-action endpoint admissibility can cap the angular sector at ell=1.
```

This may be a missing angular piece that was hidden by earlier SM-analog framing.

Open target:

```text
derive eta, or derive why eta sits near 1/16.
```

If UDT derives `eta≈1/16` from the angular/source/boundary action, then the `ell=1` sector becomes native
instead of imposed.

## 37. Eta candidate: the angular bridge value `1/18`

There is a nearby candidate that is cleaner than the critical edge:

```math
\eta={1\over18}.
```

This value already appears in the old angular bridge bookkeeping as `B_1=1/18`, so it is worth testing as
a candidate, not promoting.

For

```math
\eta={1\over18},
```

the angular cap is

```math
\lambda_\mathrm{cap}={1\over8\eta}={18\over8}=2.25.
```

Therefore:

```text
ordinary ell=1: lambda=2 allowed
ordinary ell=2: lambda=6 excluded
```

For the `ell=1` source,

```math
s=\eta\lambda={1\over18}\cdot2={1\over9},
```

and

```math
{p(1-p)\over2}={1\over9}
```

gives

```math
p={1\over3}.
```

This is structurally attractive:

```text
eta=1/18 selects ell=1 as the highest ordinary finite-action sector and gives p=1/3.
```

Finite-cell spectrum at `eta=1/18`, flux boundary, electron anchored on `monopole n=1`:

```text
monopole n=1:
  omega = 1.13433, 5.07316, 8.35485, 11.5862
  anchored = 0.510999, 2.28539, 3.76375, 5.21944 MeV

monopole n=2:
  omega = 1.54635, 5.47618, 8.81321, 12.1018
  anchored = 0.696612, 2.46695, 3.97024, 5.45171 MeV

ordinary ell=1:
  omega = 2.10394, 6.14146, 9.64140, 13.1020
  anchored = 0.947796, 2.76665, 4.34332, 5.90227 MeV
```

Twenty-fifth verdict:

`eta=1/18` is a serious candidate for the native angular-source coupling because it:

1. is already an angular bridge number in the corpus;
2. selects ordinary `ell=1` without admitting `ell=2`;
3. gives a clean endpoint exponent `p=1/3`.

But it does not solve the hierarchy. It improves the native angular admissibility story, not the mass
ratio problem.

Open target:

```text
derive eta=1/18 from the angular-source/boundary action, or reject it as numerology.
```

## 38. Eta candidate audit

Implemented in `native_eta_candidate_audit.py`.

The candidate

```math
\eta={1\over18}
```

can be written as

```math
\eta={1\over2N^2},\qquad N=2\ell+1=3.
```

Candidate comparison:

```text
eta = 1/(2N^2), N=3:
  eta=0.0555556
  lambda_cap=2.25
  ell1 allowed, p=1/3
  ell2 excluded

eta = 1/(8N), N=3:
  eta=0.0416667
  lambda_cap=3
  ell1 allowed, p=0.2113
  ell2 excluded

eta = 1/(2pi^2):
  eta=0.0506606
  lambda_cap=2.4674
  ell1 allowed, p=0.2824
  ell2 excluded

eta = 1/16:
  eta=0.0625
  lambda_cap=2
  ell1 at p=1/2 edge, not finite-action interior
  ell2 excluded
```

The `1/(2N^2)` form is attractive because it uses the same `N=3` angular-space dimension that already
appears in the `ell=1` representation structure.

Twenty-sixth verdict:

`eta=1/18` is now the best concrete candidate for the angular-source coupling, but it is not derived.

The exact derivation target is:

```text
show that angular source averaging on the ell=1 three-dimensional space produces eta = 1/(2N^2).
```

If that derivation succeeds, then UDT has a native angular reason for:

```text
ell=1 admissibility,
ell=2 exclusion,
p=1/3 endpoint softening,
and the first non-SM angular physics piece in the matter-cell rebuild.
```

If it fails, `1/18` remains a numerically attractive but noncanonical candidate.

## 39. Eta derivation attempt and generalization check

Implemented in:

- `native_eta_derivation_attempt.py`
- `native_eta_generalization.py`

### Angular averaging attempt

For `ell=1`, the angular dimension is

```math
N=2\ell+1=3.
```

Simple angular averages give:

```text
1/N      = 1/3
1/N^2    = 1/9
1/(2N^2) = 1/18
```

The target `1/18` is hit only if two ingredients are both justified:

```text
two independent triplet averages -> 1/N^2
quadratic action normalization   -> 1/2
```

The angular average alone gives `1/N` or `1/N^2`, not the extra `1/2`.

Audit verdict:

```text
eta=1/18 is algebraically natural, but not derived until the source-action
factorization is derived.
```

### Generalization check

If one instead defines a per-sector rule

```math
\eta_\ell={1\over2(2\ell+1)^2},
```

then

```math
s_\ell=\eta_\ell\ell(\ell+1)
={\ell(\ell+1)\over2(2\ell+1)^2}.
```

This stays below `1/8` for all finite `ell` and approaches the edge from below:

```text
ell=1: p=1/3
ell=2: p=0.4
ell=3: p=0.428571
ell=4: p=0.444444
...
ell -> infinity: p -> 1/2
```

So `eta_l=1/(2N_l^2)` is not an `ell=1` selector. It is a universal near-critical
normalization.

Twenty-seventh verdict:

To make `ell=1` special, `eta=1/18` must be a **global coupling fixed by the `N=3` angular sector**, not a
normalization recomputed separately for every `ell`.

That is a stronger and more precise target:

```text
derive why the endpoint angular-source coupling is fixed by the ell=1 triplet dimension N=3.
```

If UDT cannot derive that, then `eta=1/18` is still an attractive candidate but not a native selection law.

## 40. Epsilon route to global `N=3`

Implemented in `native_eta_epsilon_route.py`.

Hypothesis:

```text
The unique antisymmetric triplet fixes the global angular-source dimension N=3.
```

Combinatorics:

```math
\dim\Lambda^3 V={N(N-1)(N-2)\over6}.
```

Values:

```text
N=1 -> 0
N=2 -> 0
N=3 -> 1  unique
N=4 -> 4
N=5 -> 10
N=6 -> 20
```

If that unique `N=3` sector fixes the global source normalization,

```math
\eta={1\over2N^2}={1\over18}.
```

Then:

```text
ordinary ell=1:
  lambda=2, source=1/9, p=1/3, allowed

ordinary ell=2:
  lambda=6, source=1/3, no real softened endpoint, excluded
```

Twenty-eighth verdict:

This gives a coherent minimal-postulate route:

```text
Unique Epsilon Source Postulate:
The endpoint angular-source coupling is normalized by the unique N=3 antisymmetric
angular sector, eta=1/(2N^2)=1/18.
```

What is derived:

- `N=3` is the unique dimension with exactly one antisymmetric triple;
- `eta=1/18` follows algebraically if the source normalization is `1/(2N^2)`;
- `ell=1` is admitted and `ell=2` excluded by finite-action endpoint admissibility;
- `p=1/3` follows for the `ell=1` endpoint.

What is not yet derived:

- why the unique epsilon sector fixes the global angular-source coupling;
- why the source normalization is exactly `1/(2N^2)` rather than, for example, `1/N^2`;
- how the boundary/source action implements the rule.

This is a legitimate small-postulate candidate. It is much narrower than importing Form-T or Standard
Model color: it uses only angular topology/combinatorics plus the quadratic-action factor.

## 41. Working-postulate frame adopted for exploration

Implemented in `native_postulate_frame.py`.

For downstream exploration, assume provisionally:

```text
Pcell:
  finite-action negative-phi matter cell closes at phi=0 via a boundary layer.

Pepsilon:
  the unique N=3 epsilon sector fixes the global angular-source normalization
  eta=1/(2N^2)=1/18.

Pflux:
  compact endpoint flux sectors may exist. This remains optional.

F:
  electron mass is the single dimensionful anchor.
```

Discipline:

```text
Use these to explore consequences.
Do not relabel postulate consequences as derived.
Try to eliminate or derive each postulate later.
```

## 42. Consequences with `eta=1/18`

With

```math
\eta={1\over18},
```

the angular admissibility cap is

```math
\lambda<2.25.
```

Allowed ordinary sectors:

```text
ell=0
ell=1
```

Excluded:

```text
ell >= 2
```

Allowed lowest monopole sectors:

```text
n=0,1,2,3,4
```

Endpoint exponents:

```text
monopole n=1: p=0.0590414
monopole n=2: p=0.127322
ordinary ell=1: p=1/3
```

Flux-boundary finite-cell spectra, electron anchored on `monopole n=1`:

```text
monopole n=1:
  omega = 1.13433, 5.07316, 8.35485, 11.5862, 14.8021
  MeV   = 0.510999, 2.28539, 3.76375, 5.21944, 6.66814

monopole n=2:
  omega = 1.54635, 5.47618, 8.81321, 12.1018, 15.3766
  MeV   = 0.696612, 2.46695, 3.97024, 5.45171, 6.92697

ordinary ell=1:
  omega = 2.10394, 6.14146, 9.64140, 13.1020, 16.5557
  MeV   = 0.947796, 2.76665, 4.34332, 5.90227, 7.45810
```

Core/shell energy normalization remains small:

```text
monopole n=1:
  core_action / omega1 = 0.000146
  shell_pressure / omega1 = 0.000129

monopole n=2:
  core_action / omega1 = 0.000614
  shell_pressure / omega1 = 0.000210

ordinary ell=1:
  core_action / omega1 = 0.007970
  shell_pressure / omega1 = 0.000449
```

Layer-C same-sector epsilon composites under this fixed frame:

```text
M1+M1+M1:
  not epsilon-selected; naive sum = 1.533 MeV

M2+M2+M2:
  epsilon-selected; naive sum = 2.090 MeV

E1+E1+E1:
  epsilon-selected; naive sum = 2.843 MeV
```

Twenty-ninth verdict:

The `N=3 -> eta=1/18` working postulate makes the angular sector cleaner:

```text
ell=1 is native-admissible;
ell=2 is excluded;
the ell=1 endpoint has p=1/3;
epsilon triplet selection is available for dimension-3 sectors.
```

But the mass spectrum is still compressed. This postulate improves angular admissibility, not hierarchy.

The next necessary mechanism remains:

```text
a native running/collective rule producing log scale gaps Delta ~ 3-8,
or a justified reintroduction of a spin/probe sector on the native matter cell.
```

## 43. Radius-flow stabilization cannot be common-coefficient only

Implemented in `native_radius_flow_model.py`.

The generic stabilized matter-cell energy was tested as

```math
E(R)=A/R+B R^q.
```

The stationary radius is

```math
R_*=(A/(Bq))^{1/(q+1)}.
```

If `B` is common across sectors, then

```math
R_i/R_e=(A_i/A_e)^{1/(q+1)}.
```

Since the eta=`1/18` angular coefficients are only order-one separated, common `B` produces only
order-one radius shifts:

```text
q=1:
  M2 radius ratio = 1.1676
  E1 radius ratio = 1.3619

q=2:
  M2 radius ratio = 1.1088
  E1 radius ratio = 1.2287

q=3:
  M2 radius ratio = 1.0805
  E1 radius ratio = 1.1670
```

To force muon-like or tau-like ratios through this model, the stabilizing coefficient would need to
vary by large amounts:

```text
muon-like target:
  required B_i/B_e ~ 10^4-10^9 depending on q

tau-like target:
  required B_i/B_e ~ 10^7-10^14 depending on q
```

Thirtieth verdict:

```text
A simple common stabilization term cannot make the hierarchy.
```

This does not rule out a missing native term. It narrows the target:

```text
the missing term must be sector-dependent, running, discrete, or non-power-law.
```

## 44. Epsilon cascade as a native log-scale candidate

Implemented in `native_epsilon_cascade.py`.

The best next hypothesis is not another ordinary angular eigenvalue. It is a native log-scale rule:

```math
M_i/m_e=(A_i/A_e)\gamma^n.
```

Here:

```text
A_i/A_e = finite-cell angular prefactor;
gamma = native radius-contraction factor;
n = discrete cascade depth.
```

With fixed `gamma=3`, the nearest integer cascade hits are:

```text
muon-like target 206.768:
  M1, n=5 -> 243        (+17.5%)

tau-like target 3477.15:
  M2, n=7 -> 2981       (-14.3%)
  E1, n=7 -> 4056       (+16.7%)
```

Allowing a common `gamma` near 3 gives a much sharper diagnostic fit:

```text
gamma = 2.92451
  muon-like: M1, n=5 -> 213.9   log error +0.0340
  tau-like: E1, n=7 -> 3394     log error -0.0243
```

This is not a derivation. The sector assignment and the cascade depths were selected after the fact.
But it is the first probe where the missing hierarchy appears in the right size range without importing
Form-T or Standard Model mass formulas.

Thirty-first verdict:

```text
The likely missing piece is a native angular/negative-phi scale cascade.
```

The cascade should be treated as a provisional postulate candidate:

```text
Pcascade:
  the N=3 epsilon sector does not only fix eta;
  it also permits discrete log-radius contractions with gamma approximately 3.
```

Required derivations before canonization:

```text
derive gamma from the negative-phi/angular action;
derive allowed cascade depths n;
derive sector assignment rules;
derive residual correction away from exact gamma=3;
show why the electron sector is n=0 or otherwise fixed as the anchor.
```

Important caveat:

```text
This mechanism need not correspond to anything in current physics models.
It may be a native UDT angular-sector effect that only looks like particle generations after anchoring.
```

## 45. Native candidates for the cascade multiplier

Implemented in `native_gamma_candidates.py`.

With `eta=1/18`, the ordinary `ell=1` endpoint satisfies

```math
p(1-p)/2=\eta\lambda,\quad \lambda=2,
```

so

```math
p=1/3.
```

This means `3` now appears in two independent native ways:

```text
epsilon dimension:
  N = 3

ordinary ell=1 endpoint:
  1/p = 3
```

The fitted cascade factor from the muon-like/tau-like diagnostic was

```text
gamma_fit = 2.92451.
```

Simple native candidates:

```text
N                              -> 3.00000
1/p                            -> 3.00000
N * exp(-eta/2)                -> 2.91781
N * (1 - eta/2)                -> 2.91667
N - eta                        -> 2.94444
```

The most interesting is

```math
\gamma = N e^{-\eta/2}.
```

Reason:

```text
it uses only N=3, eta=1/18, and the same half-factor already present in the quadratic action.
```

Using this native-looking correction with the tentative depth assignment

```text
muon-like: M1 sector, n=5
tau-like: E1 sector, n=7
```

gives:

```text
muon-like ratio:
  predicted 211.49 vs target 206.77  (+2.28%)

tau-like ratio:
  predicted 3339.63 vs target 3477.15 (-3.96%)
```

Thirty-second verdict:

```text
gamma itself has a plausible native origin;
the depth rule does not yet.
```

The strongest provisional hierarchy frame is now:

```text
Pepsilon:
  N=3 fixes eta=1/(2N^2)=1/18.

Pgamma:
  the cascade multiplier is gamma=N exp(-eta/2), or a nearby derived correction.

Pdepth:
  allowed non-electron stable depths include n=5 and n=7.
```

Only `Pepsilon` and `Pgamma` currently have native structural clues. `Pdepth` is still just a
working ansatz.

## 46. Depth-rule audit

Implemented in `native_depth_rule_audit.py`.

Using

```math
\gamma=N e^{-\eta/2},
```

and testing simple `N=3` depth expressions, the best low-complexity assignment was:

```text
muon-like:
  sector M1
  n = 2N - 1 = 5
  predicted ratio 211.49
  log error +0.0226

tau-like:
  sector E1
  n = 2N + 1 = 7
  predicted ratio 3339.63
  log error -0.0404
```

This pattern is compact:

```text
electron-like: n=0 anchor
muon-like:     n=2N-1
tau-like:      n=2N+1
```

with the two non-electron depths bracketing `2N`.

Thirty-third verdict:

```text
n=2N-1 and n=2N+1 is the best current depth ansatz,
but it is not yet a native rule.
```

The missing derivation should not be forced into Standard Model language. The target is a UDT-native
selection principle, possibly from:

```text
negative-phi endpoint closure count;
epsilon-sector orientation count;
boundary-layer winding;
admissible finite-action cascade termination;
an angular determinant or index effect not present in current physics models.
```

## 47. Boundary-count candidate for cascade depth

Implemented in `native_boundary_depth_model.py`.

A more native-looking way to state the successful depths is:

```math
n(d)=N+2(d-1).
```

Interpretation:

```text
N:
  epsilon-sector dimension.

2:
  the two radial ends of a finite negative-phi matter cell
  (endpoint/core side and phi=0 closure side).

d-1:
  angular degrees after removing the common scalar mode.
```

For `N=3`:

```text
d=2 -> n=3+2(1)=5
d=3 -> n=3+2(2)=7
```

This recovers the useful depth pattern without reading off the lepton targets:

```text
M1 doublet:
  d=2
  n=5
  ratio=211.48891
  mass=108.07061 MeV

E1 triplet:
  d=3
  n=7
  ratio=3339.6274
  mass=1706.5461 MeV
```

The target values used only for comparison are:

```text
muon-like ratio: 206.768
tau-like ratio: 3477.15
```

Thirty-fourth verdict:

```text
The depth ansatz can now be stated as a native count.
It is still not derived from the action.
```

## 48. Sector-selection audit: why not M2?

Implemented in `native_sector_selection_audit.py`.

The boundary-count rule assigns `n=7` to any triplet. That creates a necessary audit:

```text
M2:
  compact-flux triplet
  d=3
  n=7

E1:
  ordinary ell=1 triplet
  d=3
  n=7
```

Native invariants:

```text
M1:
  flux=1
  dimension=2
  lambda=0.5
  p=0.059041448
  primitive_flux=yes
  endpoint p=1/N=no

M2:
  flux=2
  dimension=3
  lambda=1
  p=0.127322
  primitive_flux=no
  endpoint p=1/N=no
  epsilon unique=yes

E1:
  flux=0
  dimension=3
  lambda=2
  p=1/3
  primitive_flux=yes
  endpoint p=1/N=yes
  epsilon unique=yes
```

Two native-looking filters exclude `M2`:

```text
Fprimitive:
  elementary stable branches use only zero flux or minimal compact flux.

Fendpoint:
  the stable triplet cascade requires p=1/N.
```

Both keep:

```text
M1
E1
```

and reject:

```text
M2
```

Thirty-fifth verdict:

```text
The current strongest elementary-branch ansatz is M1 at d=2 and E1 at d=3.
M2 is not discarded because it is inconvenient; it fails two native filters.
```

But:

```text
Fprimitive is not derived.
Fendpoint is not derived.
```

They are now the next derivation targets.

## 49. Primitive-flux stability pressure

Implemented in `native_flux_primitivity_audit.py`.

The earlier flux-energy test gave

```math
E_\mathrm{flux}(n)\propto n^2\left({1\over\epsilon}-{1\over R}\right).
```

Therefore:

```text
n=1:
  E_n / E_1 = 1
  E_n / (n E_1) = 1

n=2:
  E_n / E_1 = 4
  E_n / (n E_1) = 2

n=3:
  E_n / E_1 = 9
  E_n / (n E_1) = 3
```

So a compact-flux `n=2` cell is superadditive relative to two primitive `n=1` cells:

```math
E_2 - 2E_1 = 2E_1.
```

Thirty-sixth verdict:

```text
Fprimitive is no longer just a taste preference.
Native radial flux energy makes n>1 compact flux costly as an elementary branch.
```

This does not prove that `M2` cannot exist. It says:

```text
M2 is representation-eligible;
M2 is not favored as an elementary stable compact-flux branch
unless a derived binding term overcomes the n^2 flux cost.
```

This strengthens the current elementary-branch selection:

```text
M1:
  primitive compact-flux doublet, allowed as anchor/cascade branch.

E1:
  zero-flux ordinary triplet, allowed as p=1/N endpoint-cascade branch.

M2:
  nonprimitive compact-flux triplet, demoted to diagnostic/composite candidate.
```

## 50. Endpoint-resonance selection

Implemented in `native_endpoint_resonance_audit.py`.

The endpoint softening equation is

```math
{p(1-p)\over2}=\eta\lambda.
```

With the working epsilon normalization

```math
\eta={1\over2N^2},
```

the endpoint-resonance condition

```math
p={1\over N}
```

requires

```math
\lambda=N-1.
```

For `N=3`:

```text
eta = 1/18
p = 1/3
lambda = 2
```

Sector check:

```text
O0:
  lambda=0
  p=0
  resonance=no

M1:
  lambda=0.5
  p=0.059041448
  resonance=no

M2:
  lambda=1
  p=0.127322
  resonance=no

E1:
  lambda=2
  p=1/3
  resonance=yes

O2:
  lambda=6
  no real finite-action branch under eta=1/18
```

Thirty-seventh verdict:

```text
If p=1/N is the triplet endpoint-resonance rule,
then eta=1/(2N^2) selects ordinary ell=1 automatically.
```

This gives a native reason for the depth-7 branch to use `E1` rather than `M2`:

```text
M2 is epsilon-eligible but not endpoint-resonant.
E1 is epsilon-eligible and endpoint-resonant.
```

The remaining postulate has narrowed:

```text
Before:
  choose E1 over M2.

Now:
  derive or justify p=1/N as the stable triplet cascade endpoint condition.
```

## 51. Endpoint self-similarity route to `p=1/3`

Implemented in `native_endpoint_self_similarity.py`.

For

```math
f=e^{-2\phi}\sim r^{-p},
```

the C1 action density scales as

```math
r^{-2p}.
```

The finite near-endpoint action remainder below cutoff `epsilon` therefore scales as

```math
S(0,\epsilon)\sim \epsilon^{1-2p}.
```

A possible native endpoint closure condition is:

```text
the finite-action remainder scales with the same power as the endpoint profile.
```

That is:

```math
1-2p=p.
```

So:

```math
p={1\over3}.
```

With

```math
\eta={1\over18},
```

the angular source equation gives

```math
{p(1-p)\over2}=\eta\lambda
\quad\Rightarrow\quad
\lambda=2.
```

Thus the self-similar endpoint condition selects the same sector as the epsilon resonance:

```text
p=1/3
lambda=2
ordinary ell=1
```

Comparison:

```text
M1:
  p=0.059041448
  action-remainder exponent / profile exponent = 14.9373

M2:
  p=0.127322004
  action-remainder exponent / profile exponent = 5.8541

E1:
  p=1/3
  action-remainder exponent / profile exponent = 1
```

Thirty-eighth verdict:

```text
Fendpoint has a native closure candidate:
the stable triplet endpoint is the self-similar finite-action endpoint.
```

This is not yet a theorem from the variational problem, but it is stronger than a free sector choice:

```text
self-similar finite-action closure -> p=1/3 -> lambda=2 -> E1.
```

## 52. Current native mass-ladder candidate

Implemented in `native_mass_ladder_candidate.py`.

This is not canonized. It is the current compact working chain:

```text
Pepsilon:
  N=3
  eta=1/(2N^2)=1/18

Pgamma:
  gamma=N exp(-eta/2)=2.91781343135

Pdepth:
  n(d)=N+2(d-1)

Pselect:
  M1 primitive compact-flux doublet;
  E1 self-similar ordinary ell=1 triplet.

F:
  electron mass anchor.
```

Branch predictions:

```text
electron anchor:
  sector=M1
  dimension=2
  depth=0
  predicted mass=0.51099895 MeV

muon-like:
  sector=M1
  dimension=2
  depth=5
  predicted ratio=211.4889084
  predicted mass=108.0706101 MeV
  diagnostic target=105.6583755 MeV
  fractional error=+2.2831%

tau-like:
  sector=E1
  dimension=3
  depth=7
  predicted ratio=3339.627442
  predicted mass=1706.546116 MeV
  diagnostic target=1776.86 MeV
  fractional error=-3.9572%
```

Thirty-ninth verdict:

```text
The hierarchy is no longer absent from the native rebuild.
It appears if the negative-phi cell has an epsilon/log-scale cascade.
```

But the status remains:

```text
Pepsilon: structural postulate with strong native clues.
Pgamma: native-looking correction, not yet variationally derived.
Pdepth: boundary-count ansatz, not yet variationally derived.
Pselect: strengthened by flux primitivity and endpoint self-similarity, not yet final.
F: accepted electron anchor.
```

The next mathematical target is therefore:

```text
derive the cascade multiplier and boundary-depth count from the finite-cell action/boundary layer.
```

## 53. Gamma correction audit

Implemented in `native_gamma_correction_audit.py`.

Write the cascade multiplier as

```math
\gamma=N e^{-c\eta}.
```

For the current fixed branch assignments:

```text
muon-like:
  M1, n=5

tau-like:
  E1, n=7
```

the target-implied corrections are:

```text
muon-like:
  gamma=2.90466989975
  c=0.58126566

tau-like:
  gamma=2.93469211457
  c=0.39617536

joint least-squares:
  gamma=2.92451492531
  c=0.45870587
```

Simple native-looking choices:

```text
c=0:
  gamma=3
  muon error=+17.523%
  tau error=+16.657%

c=1/3:
  gamma=2.944955687
  muon error=+7.130%
  tau error=+2.474%

c=1/2:
  gamma=2.917813431
  muon error=+2.283%
  tau error=-3.957%

c=2/3:
  gamma=2.890921333
  muon error=-2.344%
  tau error=-9.985%
```

Fortieth verdict:

```text
c=1/2 is the best simple native half-factor among the tested choices.
The exact diagnostic fit would use c≈0.459, so Pgamma remains ansatz-bearing.
```

This is the current discipline:

```text
Use gamma=N exp(-eta/2) as the simplest native correction.
Do not call it derived until the boundary/action calculation produces the half-factor.
```

## 54. Boundary-transfer audit

Implemented in `native_boundary_transfer_audit.py`.

The current cascade can be written as a boundary-transfer rule:

```math
\gamma = N e^{-c\eta},
```

with depth

```math
n(d)=N+B(d-1).
```

Interpretation:

```text
N:
  epsilon transfer multiplicity.

c:
  boundary action penalty coefficient.

B:
  number of finite-cell closure boundaries contributing non-scalar angular degrees.
```

For the current ansatz:

```text
c=1/2
B=2
```

Depth sensitivity at `c=1/2`:

```text
B=0:
  n2=3
  n3=3
  muon-like mass=12.6938 MeV
  tau-like mass=23.5444 MeV

B=1:
  n2=4
  n3=5
  muon-like mass=37.0382 MeV
  tau-like mass=200.4486 MeV

B=2:
  n2=5
  n3=7
  muon-like mass=108.0706 MeV
  tau-like mass=1706.5461 MeV

B=3:
  n2=6
  n3=9
  muon-like mass=315.3299 MeV
  tau-like mass=14528.9111 MeV
```

So `B=2` is load-bearing. It cannot be treated as harmless bookkeeping.

Gamma sensitivity at `B=2`:

```text
c=0:
  gamma=3
  muon error=+17.523%
  tau error=+16.657%

c=1/3:
  gamma=2.9449557
  muon error=+7.130%
  tau error=+2.474%

c=1/2:
  gamma=2.9178134
  muon error=+2.283%
  tau error=-3.957%

c=2/3:
  gamma=2.8909213
  muon error=-2.344%
  tau error=-9.985%
```

Forty-first verdict:

```text
The current hierarchy candidate requires three boundary-transfer claims:
1. N acts as transfer multiplicity, not only static degeneracy.
2. the two finite-cell boundaries both count, giving B=2.
3. each transfer carries a half-eta penalty, c=1/2.
```

The first two are native-looking. The third is the least secure:

```text
c=1/2 must come from a quadratic boundary action,
a determinant measure,
or another native cell-closure calculation.
```

The classical shell-stress magnitude does not derive it by itself.

## 55. Gamma-origin audit

Implemented in `native_gamma_origin_audit.py`.

The working per-step correction exponent is

```math
\eta/2 = 0.0277777778.
```

Raw classical closure loads at `eta=1/18`:

```text
M1:
  shell pressure = 0.0001465535
  shell / (eta/2) = 0.005276
  core action = 0.0001659681
  core / (eta/2) = 0.005975

M2:
  shell pressure = 0.0003245816
  shell / (eta/2) = 0.011685
  core action = 0.0009488416
  core / (eta/2) = 0.034158

E1:
  shell pressure = 0.0009437632
  shell / (eta/2) = 0.033976
  core action = 0.0167668973
  core / (eta/2) = 0.603608
```

Forty-second verdict:

```text
The raw shell pressure does not derive eta/2.
The raw core action does not derive eta/2.
```

Therefore:

```text
gamma=N exp(-eta/2) cannot currently be read off from the classical shell/core load.
```

The half-factor must come from something normalized at the transfer level:

```text
quadratic boundary action;
Gaussian/determinant measure;
epsilon-sector transfer normalization;
or another native cell-closure mechanism not yet modeled.
```

## 56. Universal gamma audit

Implemented in `native_universal_gamma_audit.py`.

The working model uses a universal step multiplier:

```math
\gamma=N e^{-\eta/2}.
```

A tempting alternative is a raw sector-source penalty:

```math
\gamma_i=N e^{-\eta\lambda_i/2}.
```

But this makes the correction too sector-dependent:

```text
universal eta:
  muon-like error=+2.283%
  tau-like error=-3.957%

lambda-dependent source:
  muon-like error=+9.638%
  tau-like error=-20.929%

p-dependent source:
  muon-like error=+16.563%
  tau-like error=+9.336%
```

Forty-third verdict:

```text
The gamma correction should be global if the current branch assignment is kept.
It should not be the raw angular source eta*lambda.
```

This narrows the target:

```text
derive gamma from global epsilon/boundary transfer,
not from sector-local angular stress.
```

## 57. Minimal epsilon transfer-matrix model

Implemented in `native_transfer_matrix_model.py`.

The current gamma ansatz can be written as the trace of a simple transfer matrix:

```math
T=e^{-s\eta} I_N.
```

Then:

```math
\gamma=\mathrm{tr}(T)=N e^{-s\eta}.
```

The working choice is:

```text
N=3
eta=1/18
s=1/2
```

so:

```math
\gamma=3e^{-\eta/2}=2.91781343135.
```

Transfer split comparison:

```text
s=0:
  gamma=3

s=1/4:
  gamma=2.95862135023

s=1/2:
  gamma=2.91781343135

s=1:
  gamma=2.83787840672
```

Forty-fourth verdict:

```text
The gamma ansatz has a compact transfer-matrix form:
T = exp(-eta/2) I_N.
```

But the derivation is still missing. The finite-cell boundary calculation must show:

```text
1. the transfer space is exactly N-dimensional;
2. the leading transfer matrix is proportional to the identity;
3. the universal exponent split is s=1/2.
```

This is a clearer target than "find the missing hierarchy mechanism."

## 58. Partial-depth audit

Implemented in `native_partial_depth_audit.py`.

If every power of `gamma` were a stable particle branch, the model would predict extra light states.

For `M1`:

```text
n=0:
  mass=0.510999 MeV
  allowed anchor

n=1:
  mass=1.491 MeV
  must be forbidden/transient

n=2:
  mass=4.35046 MeV
  must be forbidden/transient

n=3:
  mass=12.6938 MeV
  must be forbidden/transient

n=4:
  mass=37.0382 MeV
  must be forbidden/transient

n=5:
  mass=108.071 MeV
  allowed closure
```

For `E1`:

```text
n=0:
  mass=0.947797 MeV
  must be forbidden/transient

n=3:
  mass=23.5444 MeV
  must be forbidden/transient

n=5:
  mass=200.449 MeV
  must be forbidden/transient

n=7:
  mass=1706.55 MeV
  allowed closure
```

Forty-fifth verdict:

```text
Pdepth cannot be a free excitation ladder.
It must be an admissibility or closure rule.
```

Therefore the boundary-depth derivation must show:

```text
partial cascades are not closed finite-action matter cells;
only n=0, n=2N-1, and n=2N+1 are stable elementary closures under the current branch rules.
```

Otherwise the model predicts extra low-mass states immediately.

## 59. Closure-constraint count

Implemented in `native_closure_constraint_count.py`.

The depth rule can be restated as a closure-constraint count:

```math
n_\mathrm{close}(d)=N+2(d-1).
```

Interpretation:

```text
N:
  epsilon orientation constraints.

d-1:
  non-scalar angular constraints at the core-side boundary.

d-1:
  non-scalar angular constraints at the phi=0 boundary.
```

For `N=3`:

```text
d=1:
  epsilon constraints=3
  core non-scalar constraints=0
  outer non-scalar constraints=0
  total closure depth=3
  caveat: formal scalar count only; no non-scalar matter-cell branch

d=2:
  epsilon constraints=3
  core non-scalar constraints=1
  outer non-scalar constraints=1
  total closure depth=5

d=3:
  epsilon constraints=3
  core non-scalar constraints=2
  outer non-scalar constraints=2
  total closure depth=7

d=5:
  epsilon constraints=3
  core non-scalar constraints=4
  outer non-scalar constraints=4
  total closure depth=11
```

Forty-sixth verdict:

```text
The depth rule has a plausible closure-count form.
Partial depths are unclosed cells under this count.
```

What remains open:

```text
why each closure constraint maps to one gamma transfer;
why the scalar d=1 formal count is not an elementary matter branch;
whether d=5 is excluded entirely by finite-action endpoint admissibility or becomes a higher non-elementary sector.
```

The finite-action cap already excludes ordinary `ell=2` at `eta=1/18`, so the `d=5` ordinary sector is not an
elementary finite-action endpoint in the current frame.

## 60. Transfer multiplicity audit

Implemented in `native_transfer_multiplicity_audit.py`.

The working cascade uses one factor of `N` per closure transfer:

```math
\gamma=N e^{-\eta/2}.
```

But if the core-side and `phi=0` boundary epsilon labels were independently summed, the multiplicity would be
`N^2`, not `N`.

Comparison:

```text
single channel:
  gamma=0.972604477116
  muon-like error=-99.579%
  tau-like error=-99.956%

trace/diagonal N:
  gamma=2.91781343135
  muon-like error=+2.283%
  tau-like error=-3.957%

independent pair N^2:
  gamma=8.75344029405
  muon-like error=+24754.781%
  tau-like error=+209945.606%

epsilon triples choose(N,3):
  gamma=0.972604477116
  muon-like error=-99.579%
  tau-like error=-99.956%
```

Forty-seventh verdict:

```text
The current hierarchy requires trace/diagonal N multiplicity.
Independent core/outer epsilon sums overcount by N per transfer.
```

So the boundary rule must be:

```text
epsilon orientation is transported/closed diagonally across the finite cell.
```

This is another derivation target.

## 61. Quadratic unit-transfer route to `eta/2`

Implemented in `native_quadratic_unit_transfer.py`.

A precise conditional route to the half-factor is:

```math
S_\mathrm{step}={\eta\over2}\|v\|^2.
```

For an elementary unit transfer:

```math
\|v\|^2=1,
```

so:

```math
S_\mathrm{step}=\eta/2.
```

Summing over the `N` diagonal transferred orientations gives:

```math
\gamma=\sum_{i=1}^N e^{-S_\mathrm{step}}
=N e^{-\eta/2}.
```

Norm sensitivity:

```text
norm^2=0.25:
  gamma=2.97923883747

norm^2=0.5:
  gamma=2.95862135023

norm^2=1:
  gamma=2.91781343135

norm^2=2:
  gamma=2.83787840672

norm^2=3:
  gamma=2.76013324389
```

Forty-eighth verdict:

```text
eta/2 follows if the boundary action is quadratic
and the elementary closure move has unit norm.
```

The missing derivation is now specific:

```text
derive the unit-norm closure move in the epsilon boundary space.
```

## 62. Transfer-norm fit

Implemented in `native_transfer_norm_fit.py`.

Write:

```math
\gamma=N e^{-(\eta/2)\rho}.
```

Then the target-implied effective norms are:

```text
muon-like:
  gamma=2.90466989975
  rho=1.1625313

tau-like:
  gamma=2.93469211457
  rho=0.79235072

joint:
  gamma=2.92451492531
  rho=0.91741173

unit rho:
  gamma=2.91781343135
  rho=1
```

Forty-ninth verdict:

```text
rho=1 is close but not target-exact.
The exact joint fit would use rho≈0.917.
```

Therefore:

```text
keep rho=1 only as a structural unit-transfer ansatz;
do not tune rho unless a native boundary calculation produces the value.
```

## 63. Formal scalar-branch audit

Implemented in `native_scalar_branch_audit.py`.

The closure count gives:

```math
n(d=1)=N=3.
```

If this were allowed as an elementary matter branch, then:

```text
gamma=2.91781343135
formal scalar mass=12.693827 MeV
```

This creates an extra-state problem unless `d=1` is excluded or reclassified.

Native exclusion candidates:

```text
d=1 has no non-scalar angular boundary constraints;
d=1 has no unique epsilon triplet selection;
d=1 is a scalar cell/background mode, not an elementary matter branch;
the clean dilaton/scalar sector is gapless continuum in the canonical rebuild.
```

Fiftieth verdict:

```text
The closure-depth rule must be paired with a matter-branch admissibility rule:
elementary matter cells require non-scalar angular boundary data.
```

Otherwise the cascade predicts a low scalar-like state.

## 64. Candidate dependency ledger

Implemented in `native_candidate_dependency_ledger.py`.

Current load-bearing dependencies:

```text
Pepsilon:
  claim: eta=1/(2N^2), N=3
  support: unique epsilon sector and quadratic half-factor clue
  gap: endpoint-source normalization is still postulated

Ptransfer-space:
  claim: N-dimensional diagonal transfer
  support: needed to get N rather than N^2 or 1
  gap: must be derived from boundary matching/orientation closure

Pgamma:
  claim: gamma=N exp(-eta/2)
  support: conditional on quadratic unit transfer
  gap: raw shell/core loads do not derive it

Pdepth:
  claim: n_close(d)=N+2(d-1)
  support: closure-count candidate
  gap: must derive why each constraint maps to one gamma transfer

Pselect-M1:
  claim: primitive compact-flux doublet
  support: n=1 flux avoids superadditive flux cost
  gap: compact flux itself remains optional/postulated

Pselect-E1:
  claim: ordinary ell=1 triplet
  support: self-similar endpoint p=1/3 selects lambda=2
  gap: p=1/3 closure principle still not variational theorem

Pexclude-scalar:
  claim: d=1 is not elementary matter
  support: no non-scalar boundary data; scalar sector gapless
  gap: must be formalized as admissibility rule

F:
  claim: electron mass anchor
  support: accepted dimensionful input
  gap: not derived by UDT geometry
```

Fifty-first verdict:

```text
The candidate is compact, but not derived.
The next proof targets are Ptransfer-space, Pgamma, and Pdepth.
```

This is the current strongest native reading:

```text
negative-phi finite cell
+ epsilon/angle boundary transfer
+ primitive compact flux anchor
+ self-similar ell=1 endpoint branch
+ electron mass anchor
```

It remains a working model, not canon.

## 65. Orchestra ablation audit

Implemented in `native_orchestra_ablation.py`.

The current candidate is compositional. Removing one load-bearing piece at a time gives:

```text
full candidate:
  gamma=2.917813431
  n_mu=5
  n_tau=7
  tau angular coefficient=1.8547927
  muon-like error=+2.283%
  tau-like error=-3.957%

remove eta/2 penalty:
  gamma=3
  muon-like error=+17.523%
  tau-like error=+16.657%

remove N transfer:
  gamma=exp(-eta/2)
  muon-like error=-99.579%
  tau-like error=-99.956%

wrong multiplicity:
  gamma=N^2 exp(-eta/2)
  muon-like error=+24754.781%
  tau-like error=+209945.606%

one-boundary depth:
  n_mu=4
  n_tau=5
  muon-like error=-64.945%
  tau-like error=-88.719%

three-boundary depth:
  n_mu=6
  n_tau=9
  muon-like error=+198.443%
  tau-like error=+717.673%

remove E1 angular coefficient:
  tau-like error=-48.219%

ordinary no cascade:
  muon-like error=-99.516%
  tau-like error=-99.947%
```

Fifty-second verdict:

```text
No single component carries the hierarchy by itself.
The useful result appears only from the combined transfer/depth/selection structure.
```

This supports the "instruments in a band" interpretation:

```text
negative phi supplies the finite-cell endpoint problem;
angular sector supplies dimensions and lambda;
epsilon supplies N=3 and diagonal transfer;
boundary closure supplies depth count;
finite action/self-similarity selects E1;
flux primitivity selects M1 as anchor branch;
electron anchor supplies the one dimensionful scale.
```

## 66. Residual budget audit

Implemented in `native_residual_budget_audit.py`.

After the full candidate, the remaining logarithmic corrections are:

```text
muon-like:
  log(target/pred)=-0.0225737940
  = -0.406328 eta

tau-like:
  log(target/pred)=+0.0403762488
  = +0.726772 eta
```

Native small quantities for comparison:

```text
eta/2:                     +0.0277777778
eta/3:                     +0.0185185185
eta^2:                     +0.0030864198
E1 core action:            +0.0167668973
E1 shell pressure:         +0.0009437632
M1 core action:            +0.0001659681
M1 shell pressure:         +0.0001465535
eta * MS(ordinary-M1):     -0.0094932988
-eta * MS(ordinary-M1):    +0.0094932988
eta * MS(M2-M1):           +0.0691344321
```

Fifty-third verdict:

```text
The residuals have opposite signs.
A single common correction cannot fix both.
```

So the residual is probably:

```text
branch-specific native effects;
or a better derivation of gamma/depth;
or evidence that the current branch assignment is only approximate.
```

It should not be treated as a free fitting budget.

## 67. Residual-combination warning

Implemented in `native_residual_combo_warning.py`.

Searching signed combinations of up to three native-looking small quantities shows that numerical residual fits
are easy to manufacture.

Examples:

```text
muon residual target:
  -0.0225737940

near match:
  -eta/3 - eta^2 - E1_shell
  value=-0.0225487015

tau residual target:
  +0.0403762488

near match:
  +eta/2 + eta^2 - eta*MS(ordinary-M1)
  value=+0.0403574963
```

Fifty-fourth verdict:

```text
Many small combinations can imitate the residuals.
Residual matching is not evidence without an independent derivation.
```

Discipline:

```text
Allow combinations of disparate native pieces.
Do not allow post-hoc residual patching.
```

## 68. Epsilon transfer-form audit

Implemented in `native_transfer_form_audit.py`.

The working cascade requires

```math
\mathrm{tr}(T)=N e^{-\eta/2}.
```

Several plausible transfer forms were compared:

```text
damped identity:
  T = exp(-eta/2) I_N
  trace = 2.91781343135
  matches target

mismatch penalty:
  T_ij = exp[-eta ||e_i-e_j||^2 / 2]
  trace = 3
  total sum = 8.67575681344

independent boundary penalty:
  each core/outer pair has unit cost
  trace = 2.83787840672
  total sum = 8.51363522016

projector average:
  trace = 1
```

Fifty-fifth verdict:

```text
The working gamma requires a damped diagonal identity transfer.
It is not produced by a generic mismatch penalty or independent boundary sum.
```

The boundary interpretation is therefore specific:

```text
same epsilon orientation transported across the cell;
universal cost per transported orientation;
trace over the transported orientation space.
```

## 69. Boundary constraint-rank model

Implemented in `native_boundary_rank_model.py`.

The closure-depth count can be represented as the rank of an independent constraint set:

```text
N epsilon orientation constraints;
d-1 core-side non-scalar angular constraints;
d-1 phi=0-side non-scalar angular constraints.
```

For `N=3`:

```text
d=1:
  rank=3
  caveat: formal scalar count only

d=2:
  rank=5

d=3:
  rank=7

d=5:
  rank=11
```

Fifty-sixth verdict:

```text
The depth count is the rank of the assumed independent closure-constraint set.
```

The derivation target is now:

```text
show that the finite-cell boundary variational problem supplies this exact independent constraint set.
```

## 70. Constraint-count failure modes

Implemented in `native_constraint_failure_modes.py`.

If the two boundaries are not independent, the successful depths collapse.

For `N=3`:

```text
d=2:
  independent two-boundary count: 5
  identified boundary constraints: 4
  no epsilon constraints: 2
  extra cross constraints: 6

d=3:
  independent two-boundary count: 7
  identified boundary constraints: 5
  no epsilon constraints: 4
  extra cross constraints: 9
```

Fifty-seventh verdict:

```text
The 5/7 depth pattern requires independent core and phi=0 non-scalar boundary constraints.
```

This creates a precise but delicate structure:

```text
epsilon orientation transfer must be diagonal;
angular boundary constraints must remain two-boundary independent.
```

So the two boundary roles are different:

```text
epsilon:
  transported as one diagonal orientation across the cell.

non-scalar angular closure:
  constrained separately at both finite-cell boundaries.
```

## 71. Hard/soft transfer split

Implemented in `native_hard_soft_transfer_audit.py`.

The desired transfer is:

```math
T_{ij}=e^{-\eta/2}\delta_{ij}.
```

This separates into two ingredients:

```text
hard rule:
  epsilon orientation is conserved, so i=j.

soft rule:
  each transported unit orientation carries action eta/2.
```

Comparison:

```text
hard diagonal + soft unit cost:
  trace=2.91781343135
  offdiag_sum=0

hard diagonal only:
  trace=3
  offdiag_sum=0

soft mismatch only:
  trace=3
  offdiag_sum=5.67575681344

soft independent pair:
  trace=2.83787840672
  offdiag_sum=5.67575681344
```

Fifty-eighth verdict:

```text
The working transfer requires both pieces:
hard diagonal selection and soft unit action cost.
```

This is a combination mechanism, not a single term.

## 72. Boundary action block model

Implemented in `native_boundary_action_blocks.py`.

The required structure is block-like:

```text
epsilon block:
  hard diagonal transport;
  soft unit cost eta/2.

angular block:
  independent non-scalar constraints at the core boundary and phi=0 boundary.
```

For `N=3`:

```text
epsilon block:
  transfer trace=2.91781343135
  offdiag_sum=0

d=2:
  angular constraint rank=2
  total closure count=N+rank=5

d=3:
  angular constraint rank=4
  total closure count=N+rank=7
```

Fifty-ninth verdict:

```text
The desired epsilon and angular roles are compatible if they live in distinct boundary-action blocks.
```

This is the strongest structural target so far:

```text
derive a block boundary action with diagonal epsilon transport and independent angular endpoint constraints.
```

## 73. Boundary-variation skeleton

Implemented in `native_boundary_variation_skeleton.py`.

Ordinary finite-interval variation naturally gives independent endpoint terms:

```math
\delta S_\mathrm{boundary}
=P_\mathrm{core}\delta a_\mathrm{core}
+P_\mathrm{outer}\delta a_\mathrm{outer}.
```

For `d-1` non-scalar angular modes, this gives:

```text
2(d-1)
```

endpoint variation terms.

For `N=3`:

```text
d=2:
  angular endpoint terms=2
  diagonal epsilon transport labels=3
  closure count=5

d=3:
  angular endpoint terms=4
  diagonal epsilon transport labels=3
  closure count=7
```

Sixtieth verdict:

```text
Pdepth has a variational skeleton:
two independent finite-cell endpoints naturally produce 2(d-1) angular boundary conditions.
```

But:

```text
Ptransfer-space still needs a topological/holonomy derivation for diagonal epsilon transport.
```

## 74. Epsilon holonomy audit

Implemented in `native_epsilon_holonomy_audit.py`.

If epsilon orientation acquires holonomy `U` across the finite cell:

```math
T=e^{-\eta/2}U.
```

Then:

```math
\gamma=e^{-\eta/2}\mathrm{tr}(U).
```

Cases:

```text
identity:
  tr(U)=3
  gamma=2.91781343135

swap two orientations:
  tr(U)=1
  gamma=0.972604477116

3-cycle permutation:
  tr(U)=0
  gamma=0

small rotation theta=eta:
  tr(U)=2.996914374
  gamma=2.91481233768

rotation theta=pi/3:
  tr(U)=2
  gamma=1.94520895423
```

Sixty-first verdict:

```text
The leading model requires trivial epsilon holonomy with tr(U)=N.
```

Nontrivial holonomy is possible as a native correction only if derived. It cannot be casually added.

## 75. Holonomy residual-limit audit

Implemented in `native_holonomy_residual_limits.py`.

If residuals are assigned only to holonomy, required traces are:

```text
muon-like:
  tr(U)=2.98648625218
  allowed by trace bound yes

tau-like:
  tr(U)=3.01735410808
  allowed by trace bound no
```

Sixty-second verdict:

```text
Norm-preserving holonomy can reduce the muon-like branch,
but it cannot raise the tau-like branch above identity holonomy.
```

Therefore:

```text
residuals require more than a common holonomy correction.
```

## 76. Scalar exclusion from endpoint softening

Implemented in `native_scalar_exclusion_derivation.py`.

The formal scalar depth problem from Section 63 can be removed natively.

For the scalar ordinary sector:

```text
d=1
lambda=0
```

The endpoint equation is:

```math
{p(1-p)\over2}=\eta\lambda.
```

So for `lambda=0`:

```text
p=0
```

That is not a negative-phi finite-action matter endpoint.

Sector comparison at `eta=1/18`:

```text
O0:
  lambda=0
  p=0
  negative_phi_endpoint=no

M1:
  lambda=0.5
  p=0.059041448
  negative_phi_endpoint=yes

M2:
  lambda=1
  p=0.127322004
  negative_phi_endpoint=yes

E1:
  lambda=2
  p=1/3
  negative_phi_endpoint=yes

O2:
  lambda=6
  no real finite-action branch
```

Sixty-third verdict:

```text
The d=1 scalar formal closure count is not an elementary matter branch,
because lambda=0 gives p=0 and no negative-phi endpoint.
```

This is stronger than an exclusion by preference.

## 77. Elementary branch filter

Implemented in `native_elementary_branch_filter.py`.

Combining the current native filters:

```text
nontrivial negative-phi endpoint;
finite-action softened branch;
primitive compact flux if compact flux is used;
endpoint resonance p=1/N for the ordinary triplet cascade;
scalar d=1 exclusion by p=0.
```

The result is:

```text
O0:
  excluded
  reason: p=0; no negative-phi matter endpoint

M1:
  elementary anchor candidate
  reasons:
    primitive compact-flux doublet
    nontrivial finite-action endpoint

M2:
  diagnostic/non-elementary
  reasons:
    nonprimitive compact flux
    triplet but not p=1/N endpoint

E1:
  elementary cascade candidate
  reasons:
    zero-flux ordinary triplet
    unique epsilon eligible
    endpoint resonance p=1/N

O2:
  excluded
  reason: no real finite-action softened endpoint
```

Sixty-fourth verdict:

```text
The current elementary branches are M1 anchor and E1 cascade.
O0 and O2 are excluded natively.
M2 remains diagnostic/non-elementary unless a new binding term stabilizes nonprimitive flux.
```

## 78. Block boundary-action variation

Implemented in `native_block_action_variation.py`.

The toy boundary action is:

```math
S_b=S_\epsilon+S_\mathrm{angular}.
```

Epsilon block:

```text
hard condition:
  epsilon_outer = epsilon_core

unit action:
  S_step = eta/2

count:
  N transported labels in the trace
```

Angular block:

```math
\sum_a P_{c,a}\delta A_{c,a}
+\sum_a P_{o,a}\delta A_{o,a}.
```

For `d=2`:

```text
epsilon labels=3
angular endpoint terms=2
closure count=5
```

For `d=3`:

```text
epsilon labels=3
angular endpoint terms=4
closure count=7
```

Sixty-fifth verdict:

```text
The toy boundary variation gives the desired count only if epsilon is discrete/transported.
Treating epsilon as two ordinary endpoint variables would change the model.
```

The active derivation gap is therefore:

```text
derive epsilon as a transported discrete boundary label of the negative-phi cell.
```

## 79. Epsilon volume-form transport audit

Implemented in `native_epsilon_volume_transport.py`.

For a three-dimensional angular boundary space `V`, epsilon is naturally the volume form in:

```math
\Lambda^3 V.
```

A boundary frame map

```math
A:V_\mathrm{core}\to V_\mathrm{outer}
```

transports the volume form by:

```math
\det(A).
```

But the current mass-ladder transfer uses:

```math
\mathrm{tr}(A).
```

Cases:

```text
identity:
  tr(A)=3
  det(A)=1
  penalty*tr(A)=2.91781343135
  penalty*det(A)=0.972604477116

rotation theta=pi/3:
  tr(A)=2
  det(A)=1
  penalty*tr(A)=1.94520895423
  penalty*det(A)=0.972604477116

volume-preserving anisotropic:
  tr(A)=3.5
  det(A)=1
  penalty*tr(A)=3.40411566991
  penalty*det(A)=0.972604477116
```

Sixty-sixth verdict:

```text
Epsilon volume-form preservation gives det(A)=1, not tr(A)=N.
Volume-form transport alone is insufficient.
```

This exposes a category gap:

```text
unique epsilon singlet != transported basis-label trace.
```

## 80. Epsilon basis-label transport audit

Implemented in `native_epsilon_basis_transport.py`.

To get:

```math
\gamma=N e^{-\eta/2},
```

the model needs:

```math
\sum_i \langle e_i^\mathrm{outer}|e_i^\mathrm{core}\rangle=N.
```

That is identity overlap of transported basis labels.

Cases:

```text
identity orthonormal frame:
  det=1
  trace_overlap=3
  gamma_trace=2.91781343135

permuted frame:
  det=-1
  trace_overlap=1
  gamma_trace=0.972604477116

rotated frame pi/3:
  det=1
  trace_overlap=2
  gamma_trace=1.94520895423

non-orthonormal volume-preserving:
  det=1
  trace_overlap=3.5
  gamma_trace=3.40411566991
```

Sixty-seventh verdict:

```text
The current gamma requires identity overlap of transported basis labels.
Epsilon volume preservation alone does not fix this overlap.
```

Required additional structure:

```text
a boundary metric/orthonormal frame rule.
```

## 81. Minimal orthonormal-frame postulate candidate

Implemented in `native_orthonormal_frame_postulate.py`.

The smallest current postulate that closes the epsilon-transfer gap is:

```text
Pframe:
  a closed finite negative-phi matter cell transports an oriented orthonormal angular frame
  between the core-side boundary and the phi=0 boundary.
```

Consequences:

```text
epsilon volume form is preserved;
transported basis-label overlap is identity;
transfer multiplicity is tr(I_N)=N;
hard diagonal epsilon transfer is justified at leading order.
```

Sixty-eighth verdict:

```text
Pframe is a small postulate candidate.
It is much narrower than importing Form-T or a Dirac operator,
but it is still a postulate until derived from boundary geometry.
```

Current hierarchy of assumptions:

```text
Pepsilon:
  N=3 and eta=1/(2N^2).

Pframe:
  oriented orthonormal angular frame transport.

Punit:
  unit transferred frame label carries quadratic action eta/2.

Pdepth:
  independent angular endpoint constraints give n_close(d)=N+2(d-1).
```

## 82. Ordinary angular frame transport from the metric

Implemented in `native_angular_frame_transport.py`.

The UDT angular block is:

```math
g_\Omega=r^2 d\Omega^2.
```

After rescaling by radius, every finite-radius boundary has the same unit-sphere angular metric:

```math
d\Omega^2.
```

Therefore ordinary `S^2` angular modes have a canonical radial identification across the finite cell.

Numerical overlap check:

```text
ell=0:
  dimension=1
  trace overlap=1
  max |overlap-I|=1.110e-16

ell=1:
  dimension=3
  trace overlap=3
  max |overlap-I|=3.331e-16

ell=2:
  dimension=5
  trace overlap=5
  max |overlap-I|=1.533e-16
```

Sixty-ninth verdict:

```text
Ordinary S2 angular frames have canonical identity overlap across radius.
This derives the ordinary-sector part of Pframe from phi-blind angular geometry.
```

This is important for the `E1` branch:

```text
E1 ordinary triplet basis transport is metric-native.
```

## 83. Compact-flux frame-transport audit

Implemented in `native_monopole_frame_transport_audit.py`.

Ordinary angular sector:

```text
depends only on the unit S2 metric;
identity radial transport follows from r^2 dOmega^2.
```

Compact-flux monopole sector:

```text
depends on the unit S2 metric plus a U(1) bundle/connection;
identity radial transport additionally requires fixed flux integer and fixed gauge patching/parallel transport.
```

Seventieth verdict:

```text
Pframe is partially derived for ordinary sectors.
The compact-flux M1 anchor still depends on Pflux/Pbundle.
```

So the branch status is now:

```text
E1:
  ordinary angular frame transport is metric-derived.

M1:
  primitive compact-flux selection is native-looking,
  but its bundle transport is still an assumption unless compact flux is derived.
```

## 84. Updated dependency ledger

Implemented in `native_updated_dependency_ledger.py`.

After the frame-transport audit:

```text
Pframe-ordinary:
  claim: ordinary S2 angular frame transports identically across radius
  support: derived from g_ang=r^2 dOmega^2 after unit-sphere rescaling
  gap: applies to E1; not automatically to compact-flux sectors

Pbundle-M1:
  claim: primitive compact-flux anchor has fixed bundle transport across cell
  support: needed for M1 identity frame/anchor branch
  gap: still postulated unless compact flux sector is derived

Ptransfer:
  claim: epsilon transfer is diagonal with trace N
  support: ordinary basis overlap supports trace N for E1
  gap: needs relation between epsilon labels and transported orthonormal basis

Punit:
  claim: unit transferred label has action eta/2
  support: quadratic unit-transfer route
  gap: unit norm and boundary action not yet derived

Pdepth:
  claim: n_close(d)=N+2(d-1)
  support: finite interval gives independent angular endpoint variations
  gap: constraint-to-transfer mapping not yet derived
```

Seventy-first verdict:

```text
Pframe has been reduced:
ordinary E1 frame transport is metric-derived;
compact-flux M1 still carries Pbundle/Pflux.
```

The next most exposed assumption is no longer all of `Pframe`. It is:

```text
derive compact flux/bundle transport for M1,
or find a zero-flux/non-compact-flux anchor alternative.
```

## 85. Anchor alternative audit

Implemented in `native_anchor_alternative_audit.py`.

The current electron anchor is `M1`, the primitive compact-flux doublet. Since `M1` still carries `Pflux/Pbundle`,
we tested whether a zero-flux ordinary anchor can replace it.

Results:

```text
current M1 anchor:
  anchor=M1
  muon-like mass=108.07061 MeV
  muon-like error=+2.283%
  tau-like mass=1706.5461 MeV
  tau-like error=-3.957%

E1 zero-flux anchor, same sectors:
  muon-like mass=58.265599 MeV
  muon-like error=-44.855%
  tau-like mass=920.07375 MeV
  tau-like error=-48.219%

E1 zero-flux anchor, E1 cascades:
  muon-like mass=108.07061 MeV
  muon-like error=+2.283%
  tau-like mass=920.07375 MeV
  tau-like error=-48.219%

M2 compact triplet anchor:
  muon-like mass=79.275277 MeV
  muon-like error=-24.970%
  tau-like mass=1251.8382 MeV
  tau-like error=-29.548%
```

Seventy-second verdict:

```text
The M1 compact-flux anchor is load-bearing.
A zero-flux E1 anchor does not preserve the current lepton-like hierarchy.
```

Therefore the next hard problem is:

```text
derive or explicitly postulate the primitive compact-flux/bundle sector for M1.
```

This is now the most exposed assumption in the candidate chain.

## 86. Compact bundle topology audit

Implemented in `native_bundle_topology_audit.py`.

The finite negative-phi matter-cell collar has topology:

```math
S^2\times I.
```

For compact `U(1)` line bundles:

```math
H^2(S^2\times I,\mathbb{Z})=\mathbb{Z}.
```

Consequences if a compact `U(1)` bundle is admitted:

```text
integer Chern number n labels the bundle;
n is the same on core-side and phi=0 boundary spheres;
radial transport of the flux label is topological;
primitive nonzero sector is |n|=1.
```

Not derived by topology alone:

```text
the bundle must be nontrivial;
compact U(1) is mandatory;
a charged probe/matter field must live in the bundle.
```

Seventy-third verdict:

```text
Pbundle transport is derived conditional on admitting a compact U(1) bundle.
The remaining postulate is primitive nontrivial compact bundle occupancy.
```

## 87. Primitive compact-bundle selection audit

Implemented in `native_primitive_bundle_selection.py`.

Assume compact `U(1)` line bundles on `S^2 x I` are admitted.

Then:

```text
n=0:
  trivial/background
  lowest degeneracy=1

n=1:
  primitive nontrivial sector
  lowest degeneracy=2
  lambda=0.5
  flux energy ratio=1
  elementary primitive candidate

n=2:
  nonprimitive
  lowest degeneracy=3
  lambda=1
  flux energy ratio=4
  diagnostic/non-elementary

n=3:
  nonprimitive
  lowest degeneracy=4
  lambda=1.5
  flux energy ratio=9
```

Seventy-fourth verdict:

```text
If a nontrivial compact bundle is admitted, |n|=1 is the unique primitive sector.
This selects the M1 doublet without selecting higher flux as elementary.
```

## 88. Compact-flux postulate minimization

Implemented in `native_flux_postulate_minimization.py`.

Old broad `Pflux` included:

```text
compact endpoint flux sectors may exist;
flux labels transport across the cell;
primitive n=1 is the electron anchor.
```

Reduced status:

```text
transport:
  derived if compact U(1) bundle exists on S2 x I.

integer label:
  Chern number n in H^2(S2 x I, Z)=Z.

primitive selection:
  |n|=1 is unique nontrivial primitive sector.

higher n:
  nonprimitive and flux-energy superadditive.
```

Remaining minimal postulate:

```text
Pbundle0:
  elementary negative-phi matter cells may occupy the primitive nontrivial compact U(1)
  line-bundle sector on the linking S2.
```

Seventy-fifth verdict:

```text
Pflux is reduced to Pbundle0.
Pbundle0 is still not derived from the metric alone.
```

## 89. Reduced-postulate ladder

Implemented in `native_reduced_postulate_ladder.py`.

With:

```text
Pbundle0:
  primitive compact bundle may be occupied.

Pframe-ordinary:
  ordinary E1 frame transport is metric-derived.

Pepsilon/Punit:
  eta=1/(2N^2), unit transfer action eta/2.

Pdepth:
  closure constraints map to gamma transfers.
```

the branch reading is:

```text
electron:
  M1 primitive compact bundle |n|=1, anchored.

muon-like:
  M1 primitive compact bundle, closure depth 5.

tau-like:
  E1 ordinary triplet, closure depth 7.
```

Predictions remain:

```text
muon-like:
  mass=108.07061 MeV
  error=+2.283%

tau-like:
  mass=1706.5461 MeV
  error=-3.957%
```

Seventy-sixth verdict:

```text
The compact-flux burden has narrowed.
The candidate no longer needs arbitrary flux transport; it needs Pbundle0.
```

Current remaining postulates:

```text
Pbundle0:
  primitive nontrivial compact U(1) bundle occupancy.

Pepsilon/Punit:
  eta normalization and unit transfer action.

Pdepth:
  closure constraints map to gamma transfers.

F:
  electron mass anchor.
```

## 90. Transfer observable audit

Implemented in `native_transfer_observable_audit.py`.

For a boundary transfer matrix `T`, possible scalar reductions are not equivalent:

```text
trace(T)
largest eigenvalue
determinant(T)
spectral radius
total sum
```

For the damped identity:

```text
T = exp(-eta/2) I_N

trace              = 2.91781343135
largest eigenvalue = 0.972604477116
spectral radius    = 0.972604477116
determinant        = 0.920044414629
total_sum          = 2.91781343135
```

For a uniform rank-one projector:

```text
trace              = 0.972604477116
largest eigenvalue = 0.972604477116
total_sum          = 2.91781343135
```

Seventy-seventh verdict:

```text
The current gamma is trace(damped identity), not an eigenvalue or determinant.
```

So the physical interpretation must be:

```text
all N diagonal transported labels contribute additively.
```

This is a partition/trace statement, not a dominant-channel statement.

## 91. Partition-trace interpretation

Implemented in `native_partition_trace_interpretation.py`.

If the boundary transfer is a one-step partition trace:

```math
Z_\mathrm{step}=\mathrm{Tr}\,e^{-S_\mathrm{step}},
```

and there are `N` degenerate transported labels with:

```math
S_i=\eta/2,
```

then:

```math
Z_\mathrm{step}=N e^{-\eta/2}.
```

This is exactly:

```math
\gamma=N e^{-\eta/2}.
```

Equivalently:

```math
\log\gamma=\log N-\eta/2.
```

Seventy-eighth verdict:

```text
The gamma rule has a clean boundary free-action interpretation:
entropy/counting term log N minus unit action penalty eta/2.
```

Still open:

```text
derive that the finite-cell boundary closure uses a partition trace over transported labels.
```

## 92. Boundary free-action ledger

Implemented in `native_boundary_free_action.py`.

Define:

```math
\Delta=\log N-\eta/2.
```

For `N=3`, `eta=1/18`:

```text
Delta = 1.07083451089.
```

Branch logs:

```text
electron:
  sector=M1
  depth=0
  total log ratio=0
  ratio=1

muon-like:
  sector=M1
  depth=5
  boundary log contribution=5.35417255445
  total log ratio=5.35417255445
  ratio=211.488908378

tau-like:
  sector=E1
  depth=7
  log angular coeff=0.617772959097
  boundary log contribution=7.49584157623
  total log ratio=8.11361453533
  ratio=3339.62744164
```

Seventy-ninth verdict:

```text
The ladder is additive in boundary free action.
Deriving Delta=log N-eta/2 may be easier than deriving gamma directly.
```

This is the cleanest current target:

```text
per closure constraint:
  + log N from transported-label degeneracy;
  - eta/2 from quadratic unit boundary action.
```

## 93. Constraint-type free-action audit

Implemented in `native_constraint_type_free_action.py`.

The previous ledger assumed every closure unit contributes:

```math
\Delta=\log N-\eta/2.
```

But closure count contains different-looking pieces:

```text
N epsilon transport labels;
2(d-1) angular endpoint constraints.
```

If only epsilon constraints carry `log N`, the ladder collapses:

```text
all closure units carry log N - eta/2:
  muon-like error=+2.283%
  tau-like error=-3.957%

only epsilon constraints carry log N:
  muon-like error=-88.635%
  tau-like error=-98.814%

all constraints action-only, no log N:
  muon-like error=-99.579%
  tau-like error=-99.956%
```

Eightieth verdict:

```text
The hierarchy requires angular endpoint constraints to be mediated by the same N-way transfer.
```

This is a new load-bearing requirement:

```text
not only epsilon constraints,
but every independent closure constraint must carry the transported-label trace.
```

## 94. Epsilon-mediated constraint model

Implemented in `native_epsilon_mediated_constraints.py`.

The needed rule is:

```text
each closure constraint is solved by choosing one of N transported epsilon frame labels;
each choice carries the same unit action eta/2.
```

Then one closure constraint has:

```math
Z_\mathrm{unit}=\sum_{i=1}^N e^{-\eta/2}=N e^{-\eta/2}.
```

For `d=2`:

```text
independent closure constraints=5
total log contribution=5.35417255445
```

For `d=3`:

```text
independent closure constraints=7
total log contribution=7.49584157623
```

Eighty-first verdict:

```text
This explains how angular constraints could inherit log N,
but it must be derived: angular closure must be epsilon-mediated.
```

This may be the real core of `Pdepth`.

## 95. Constraint entropy count

Implemented in `native_constraint_entropy_count.py`.

If each independent closure constraint has `N` transported-label choices, the number of closure configurations is:

```math
N^{n_\mathrm{close}}.
```

For `N=3`:

```text
d=1:
  closure constraints=3
  N^constraints=27
  caveat: scalar/background, not matter branch

d=2:
  closure constraints=5
  N^constraints=243

d=3:
  closure constraints=7
  N^constraints=2187

d=5:
  closure constraints=11
  N^constraints=177147
```

Eighty-second verdict:

```text
The hierarchy-scale growth is primarily an entropy/counting effect,
damped by the unit boundary action.
```

This is promising but risky:

```text
promising:
  it naturally creates large ratios from small native counts.

risky:
  it requires independent epsilon-mediated closure choices.
```

The next derivation target is therefore:

```text
derive epsilon-mediated angular closure from the finite-cell boundary action.
```

## 96. Epsilon choice-correlation audit

Implemented in `native_epsilon_choice_correlation.py`.

The current hierarchy assumes:

```text
each independent closure constraint has its own N-way epsilon-mediated choice.
```

If choices are globally shared, the entropy collapses:

```text
independent epsilon choice per constraint:
  muon-like error=+2.283%
  tau-like error=-3.957%

one global epsilon choice shared by all constraints:
  muon-like error=-98.737%
  tau-like error=-99.868%

one epsilon choice per closure block:
  muon-like error=-88.635%
  tau-like error=-98.814%
```

Eighty-third verdict:

```text
The hierarchy requires independent or effectively independent epsilon choices per closure constraint.
```

This is a strong requirement and a possible overcounting risk.

## 97. Constraint tensor model

Implemented in `native_constraint_tensor_model.py`.

A local bookkeeping model:

```text
index a:
  independent closure constraint.

index i:
  transported epsilon/frame label.
```

For each constraint:

```math
W_a=\sum_{i=1}^N e^{-\eta/2}.
```

For `d=2`:

```text
closure constraints=5
local weight=2.91781343135
total weight=211.488908378
```

For `d=3`:

```text
closure constraints=7
local weight=2.91781343135
total weight=1800.53941904
```

Eighty-fourth verdict:

```text
The tensor-index model reproduces the entropy only if each closure constraint has an independent epsilon/frame index.
```

Derivation target:

```text
show that the boundary equations factorize into independent local constraint tensors W_a.
```

## 98. Constraint independence audit

Implemented in `native_constraint_independence_audit.py`.

For `d=2`, `constraints=5`:

```text
independent i per constraint:
  weight=211.488908378
  log=5.35417255445

shared i across all constraints:
  weight=2.6109741775
  log=0.959723399779

no entropy:
  weight=0.870324725833
  log=-0.138888888889
```

For `d=3`, `constraints=7`:

```text
independent i per constraint:
  weight=1800.53941904
  log=7.49584157623

shared i across all constraints:
  weight=2.46987574628
  log=0.904167844224

no entropy:
  weight=0.823291915426
  log=-0.194444444444
```

Eighty-fifth verdict:

```text
Independent epsilon/frame index per constraint is the load-bearing entropy assumption.
Shared-index alternatives are too small by powers of N.
```

This is now the most important unresolved mathematical question:

```text
Are the finite-cell closure constraints genuinely independent local choices,
or are they correlated by one global transported frame?
```

If independent:

```text
the hierarchy mechanism has a plausible native entropy source.
```

If globally correlated:

```text
the hierarchy collapses.
```

## 99. Constraint factor-graph audit

Implemented in `native_constraint_factor_graph.py`.

Model:

```text
nodes:
  closure constraints.

node label:
  epsilon/frame index i in {1,...,N}.

equality edge:
  two closure constraints must share the same epsilon/frame index.
```

If the graph has `C` connected components:

```math
\#\mathrm{choices}=N^C.
```

For `N=3`:

```text
constraints=5:
  independent nodes:             components=5, count=243
  one global equality component: components=1, count=3
  three approximate blocks:      components=3, count=27
  two approximate blocks:        components=2, count=9

constraints=7:
  independent nodes:             components=7, count=2187
  one global equality component: components=1, count=3
  three approximate blocks:      components=3, count=27
  two approximate blocks:        components=2, count=9
```

Eighty-sixth verdict:

```text
The mass-ladder entropy requires the factor graph to be disconnected at the individual constraint level.
```

Even partial correlation into a few blocks collapses the entropy.

## 100. Angular constraint orthogonality audit

Implemented in `native_angular_constraint_orthogonality.py`.

Ordinary spherical harmonic boundary modes are orthogonal:

```text
ell=1:
  dimension=3
  max offdiag=9.189e-17
  max diag error=3.331e-16

ell=2:
  dimension=5
  max offdiag=1.533e-16
  max diag error=8.446e-19
```

Eighty-seventh verdict:

```text
Ordinary angular boundary modes are orthogonal at leading order.
This supports factorized angular constraints.
```

But:

```text
orthogonality supports independence of angular factors;
it does not by itself derive epsilon mediation.
```

Current refined target:

```text
derive a boundary action whose angular constraint factors are orthogonal
and whose individual factors are each mediated by an independent epsilon/frame label.
```

## 102. Soft correlation strength audit

Implemented in `native_correlation_strength_audit.py`.

Hard equality edges are not the only possible correlation. A soft chain coupling can bias neighboring closure
labels without fully identifying them:

```math
w=\exp(\kappa)
```

when adjacent labels are equal.

The corrected diagnostic uses Shannon effective state count, not raw partition sum.

For `N=3`, `constraints=5`:

```text
kappa=0:
  entropy_count=243
  effective_components=5

kappa=0.5:
  entropy_count=215.378
  effective_components=4.8902

kappa=1:
  entropy_count=148.402
  effective_components=4.5511

kappa=2:
  entropy_count=42.9872
  effective_components=3.4233

kappa=5:
  entropy_count=4.12923
  effective_components=1.2908
```

For `constraints=7`:

```text
kappa=0:
  entropy_count=2187
  effective_components=7

kappa=0.5:
  entropy_count=1824.91
  effective_components=6.8352

kappa=1:
  entropy_count=1043.75
  effective_components=6.3267

kappa=2:
  entropy_count=162.723
  effective_components=4.6350

kappa=5:
  entropy_count=4.84443
  effective_components=1.4362
```

Eighty-ninth verdict:

```text
Soft correlations reduce entropy continuously.
Hard equality is the limiting collapse to one component.
```

This softens the binary question:

```text
not all correlations kill the mechanism;
but strong correlations do.
```

## 103. Entropy-correlation residual audit

Implemented in `native_entropy_correlation_residual.py`.

Correlations reduce effective entropy relative to full independence. That can lower a branch mass, but cannot
raise a branch above the independent-entropy prediction.

Using the same correlation strength for both branches:

```text
kappa=0:
  muon-like error=+2.283%
  tau-like error=-3.957%

kappa=0.25:
  muon-like error=-0.657%
  tau-like error=-8.068%

kappa=0.5:
  muon-like error=-9.344%
  tau-like error=-19.859%

kappa=1:
  muon-like error=-37.535%
  tau-like error=-54.163%
```

Ninetieth verdict:

```text
Entropy correlations can reduce the muon-like branch.
They cannot raise the tau-like branch above the independent-entropy prediction.
```

Therefore:

```text
correlation corrections are not a universal residual fix.
tau-like residual still needs a positive branch-specific effect,
or a better derivation of the base transfer/depth rule.
```

## 104. Zoom-out native mechanism scorecard

Implemented in `native_mechanism_scorecard.py`.

This is a deliberate anti-myopia audit.

```text
classical finite-cell spectrum:
  hierarchy power: O(1) ratios only
  selection power: finite-cell modes
  failure mode: compressed spectrum
  status: use as coefficients, not hierarchy source

common radius-flow stabilization:
  hierarchy power: too weak with common coefficients
  failure mode: requires huge sector-dependent B
  status: revisit only if B derives from native running

endpoint admissibility/self-similarity:
  hierarchy power: sector selection, not full hierarchy
  selection power: strong
    p=0 excludes scalar
    p=1/3 selects E1
    ell=2 excluded
  remaining gap: eta/source normalization

compact bundle/topology:
  hierarchy power: selects M1 anchor, not full hierarchy
  selection power: strong conditional
    |n|=1 primitive if compact bundle admitted
  remaining gap: Pbundle0

angular determinant/RG:
  hierarchy power: possible log-scale corrections
  failure mode: scheme dependence and easy residual fitting
  status: correction candidate, not main mechanism yet

boundary closure entropy:
  hierarchy power: strong
    N^5 and N^7 scale
  selection power: strong if constraints are epsilon-mediated
  failure mode: overcounting if choices are globally correlated
  next test: derive factorized epsilon-mediated boundary constraints
```

Ninety-first verdict:

```text
Current best hierarchy source:
  boundary closure entropy.

Current best selection sources:
  endpoint admissibility/self-similarity;
  compact topology/bundle primitivity.

Current correction candidate:
  angular determinant/RG.
```

This keeps two tracks open:

```text
Track A:
  derive/test boundary closure entropy.

Track B:
  keep determinant/RG, scale-flow, and topology alternatives visible in case entropy is a shadow of a deeper rule.
```

## 105. Orchestra residual separation audit

Implemented in `native_orchestra_residual_separation.py`.

The baseline residuals have opposite signs:

```text
muon-like:
  baseline=108.07061 MeV
  log_need=-0.0225737940

tau-like:
  baseline=1706.5461 MeV
  log_need=+0.0403762488
```

This means the residual cannot be one common correction.

M1 damping instrument:

```text
kappa needed to place muon-like target:
  0.22050888

effective entropy components:
  4.9794524

corrected muon-like mass:
  105.65838 MeV
```

E1 positive-boost budget:

```text
required tau boost:
  +0.0403762488
  = +0.726772 eta

native scale comparisons:
  eta/2                    = +0.0277777778
  eta/3                    = +0.0185185185
  eta^2                    = +0.0030864198
  E1 core action           = +0.0167668973
  -eta*MS(ordinary-M1)     = +0.0094932988
  eta*MS(M2-M1)            = +0.0691344321
```

Ninety-second verdict:

```text
M1 residual can be explained by small branch-local entropy correlation.
E1 still needs a separate positive native effect.
```

This supports the orchestra framing:

```text
different branches may receive different native corrections from different instruments.
```

It also preserves discipline:

```text
do not patch the tau residual by choosing a convenient combination.
derive the E1-positive instrument first.
```

## 106. Native orchestra interaction matrix

Implemented in `native_orchestra_interaction_matrix.py`.

Current instrument roles:

```text
negative-phi finite cell:
  role: creates endpoint/boundary problem.
  M1: finite-action endpoint stage.
  E1: finite-action endpoint stage.
  status: native metric behavior.

ordinary S2 angular frame:
  role: metric-derived identity transport.
  M1: not enough for compact bundle alone.
  E1: directly supports E1 frame transport.
  status: derived for ordinary sectors.

compact U(1) bundle:
  role: primitive nontrivial anchor sector.
  M1: selects M1 if Pbundle0 admitted.
  E1: not used.
  status: minimal postulate Pbundle0.

endpoint admissibility:
  role: sector selection through p(lambda).
  M1: allows M1 finite endpoint.
  E1: selects E1 via p=1/N.
  status: partly derived; eta still postulated.

boundary closure entropy:
  role: large hierarchy scale.
  M1: depth 5 if epsilon-mediated independent constraints.
  E1: depth 7 if epsilon-mediated independent constraints.
  status: leading hierarchy candidate.

constraint correlations:
  role: branch damping.
  M1: can lower M1/muon-like branch.
  E1: would lower E1/tau-like branch, undesirable.
  status: possible M1 residual instrument only.

angular determinant/RG:
  role: small log correction candidate.
  M1: scheme-dependent; not assigned.
  E1: possible positive E1 correction if derived.
  status: open; high overfit risk.

electron anchor:
  role: sets absolute scale.
  M1: anchors M1 ground branch.
  E1: sets E1 masses by ratios.
  status: accepted input F.
```

Ninety-third verdict:

```text
M1 and E1 are not the same instrument played louder.
Selection, scale, damping, and residual correction are distributed across different native pieces.
```

The next zoomed-out target is:

```text
derive the E1-positive instrument without disturbing the M1 damping/anchor structure.
```

## 107. Metric discovery ledger

Implemented in `native_metric_discovery_ledger.py`.

This is an anti-invention audit.  The question is not "what mechanism can we add?"
but:

```text
what does the metric already force,
what follows only if a small postulate is admitted,
and what is still just a working ladder ansatz?
```

Current metric-forced pieces:

```text
negative phi sheet:
  phi<0 gives f=e^{-2phi}>1 and creates the endpoint/cell problem.

round S2 angular block:
  g_theta_theta=r^2 and g_phi_phi=r^2 sin^2 theta are phi-blind.

abelian Coulomb sector:
  sqrt(-g) g^rr g^tt cancels phi, giving a real flat-form Coulomb dynamic.
```

Metric-forced under the C1 action:

```text
finite-action endpoint bound:
  for f ~ r^-p, finite radial action requires p < 1/2.
```

Conditional metric consequences:

```text
angular source softening:
  an s/r^2 angular source gives p(1-p)/2=s,
  but s=eta lambda is not yet derived.

compact U(1) line bundle:
  if admitted on S2 x I, integer flux sectors follow topologically,
  and primitive |n|=1 is selected.
```

Working postulate pressure points:

```text
Pbundle0:
  a primitive compact U(1) bundle may be occupied by elementary cells.

Pepsilon:
  eta=1/18 from the N=3 epsilon normalization.

Pclosure:
  independent epsilon-mediated boundary constraints contribute log N - eta/2.
```

Open hidden-metric candidate:

```text
angular determinant/RG finite part:
  possible branch-dependent correction,
  but high scheme-dependence and high residual-fitting risk.
```

Ninety-fourth verdict:

```text
The main hierarchy candidate still depends on live postulates.
The main native facts are endpoint formation, phi-blind S2 structure,
finite-action filtering, topology if compact flux is admitted,
and the real abelian Coulomb sector.
```

Therefore the next metric-first target is:

```text
derive the phi=0 boundary variation and constraint graph before assigning
any more branch corrections.
```

## 108. Hidden metric audit

Implemented in `native_hidden_metric_audit.py`.

The reminder that the metric may contain pieces not yet uncovered changes the search
order.  The next pass should inspect native structures we have not fully used:

```text
phi=0 interface:
  induced metric, extrinsic curvature, boundary variation.
  possible missing piece: eta or closure count.

punctured endpoint topology:
  linking S2 and collar S2 x I.
  possible missing piece: a metric obstruction requiring nonzero compact flux.

angular measure and Laplacian:
  degeneracy, determinant, heat-kernel finite part.
  possible missing piece: E1-positive branch correction.

radial proper distance:
  dl=e^phi dr and redshifted radial measure.
  possible missing piece: a scale-flow invariant that changes depth count.

Maxwell cancellation:
  real phi-blind Coulomb dynamics.
  possible missing piece: branch-selective boundary energy through existing labels.

self-adjoint endpoint data:
  admissible boundary form without importing Dirac Form T.
  possible missing piece: allowed endpoint channels.

nonlinear angular back-reaction:
  multiple angular instruments feeding phi together.
  possible missing piece: true orchestra interaction, not a solo correction.
```

Guardrail:

```text
Do not use the mu/tau residuals to choose these pieces.
First derive their sign, branch support, and normalization target-blind.
Only then compare to the residual budget.
```

Ninety-fifth verdict:

```text
The most promising uncovered metric location is the boundary/interface,
not another mass-fit term.
```

The next concrete calculation should be:

```text
derive the C1 action boundary variation for a finite negative-phi cell
with round-S2 angular data, then ask whether the resulting boundary form
contains:

  1. an eta-like unit action,
  2. an independent constraint count,
  3. a branch-selective Coulomb or determinant term,
  4. a native reason for primitive compact flux.
```

## 109. C1 boundary variation and phi=0 interface geometry

Implemented in:

```text
native_boundary_variation_c1.py
native_phi0_interface_geometry.py
```

Write:

```text
f = e^{-2 phi}

ds^2 = -f dt^2 + f^-1 dr^2 + r^2 dOmega^2
```

For the static radial C1 action:

```text
sqrt(-g) e^{-2phi} g^rr phi'^2
  = r^2 e^{-4phi} phi'^2
  = (1/4) r^2 f'^2
```

So the bare radial C1 action is simply a Dirichlet energy for `f`.

The boundary flux is:

```text
Pi_f proportional to r^2 f'
```

For an endpoint:

```text
f ~ r^-p
```

the action remainder scales as:

```text
epsilon^(1-2p)
```

Therefore:

```text
finite C1 action:
  p < 1/2

self-similar endpoint/action scaling:
  1 - 2p = p
  p = 1/3
```

This confirms:

```text
bare radial C1 gives finite-action filtering and p=1/3 visibility.
bare radial C1 does not by itself contain eta, N, or closure count.
```

Now inspect the actual `phi=0` interface.

For a timelike shell `r=R` with `f(R)=1`:

```text
K^t_t = f'/2
K^theta_theta = K^phi_phi = 1/R
K = f'/2 + 2/R
```

For an inner endpoint matched to the collar:

```text
f = (R/r)^p
f'(R) = -p/R

K_inner = (2 - p/2)/R
K_flat_outer = 2/R

Delta K = K_outer - K_inner = p/(2R)
```

At the self-similar finite endpoint:

```text
p = 1/3

Delta K * R = 1/6
```

Now the important metric-native diagnostic:

```text
three transported frame directions:
  (Delta K * R) / 3 = 1/18

half of the frame share:
  (Delta K * R) / 6 = 1/36 = eta/2
```

Ninety-sixth verdict:

```text
eta=1/18 is no longer only a numerological epsilon postulate.
It appears as the equal frame-share of the phi=0 extrinsic-curvature jump
for the p=1/3 self-similar endpoint.
```

But the discipline line is:

```text
The metric has produced the eta-sized quantity.
It has not yet proved the equal-share rule or the Boltzmann damping exp(-eta/2).
```

This is a substantial improvement in status:

```text
before:
  eta=1/18 was a working normalization postulate.

after:
  eta=1/18 is a native interface-geometry candidate,
  pending derivation of frame-sharing from the boundary variation.
```

The next target is therefore sharper:

```text
derive whether the boundary/interface action decomposes into three equal
transported-frame channels.

If yes:
  eta = 1/18 becomes metric-derived from:
    p=1/3 self-similarity
    phi=0 extrinsic curvature jump
    three-frame angular transport

If no:
  eta remains a postulate even though the same number appears naturally.
```

## 110. Interface frame-share audit

Implemented in `native_interface_frame_share_audit.py`.

The previous section found a real native scalar:

```text
p = 1/3
Delta K * R = 1/6
```

However, the stronger claim needs a correction.

The mixed extrinsic-curvature jump on the `phi=0` shell is tensorial:

```text
Delta K^a_b = diag(p/(2R), 0, 0)

directions:
  (t, theta, phi)
```

That means:

```text
Delta K = p/(2R)
```

but the jump is not equally distributed over the shell directions.  The two
angular curvature components do not jump in this simple matched model.

For the self-similar endpoint:

```text
p = 1/3

tensor jump:
  diag(1/6, 0, 0)

trace:
  1/6

equal trace share over three labels:
  1/18
```

Ninety-seventh verdict:

```text
The metric derives the interface scalar 1/6.
It does not, from the extrinsic-curvature tensor alone, derive eta=1/18.
```

So the status is:

```text
eta=1/18 is upgraded from arbitrary normalization
to a native scalar-projection candidate:

  eta = (self-similar interface jump) / (three transported labels)
      = (1/6) / 3
      = 1/18

but the projection onto three transported labels is still the unresolved step.
```

This is not a setback.  It sharpens the search:

```text
Do not ask whether extrinsic curvature itself is isotropic.
It is not.

Ask whether the scalar boundary action projects the interface jump onto the
epsilon/oriented-frame basis, where N=3 is already native to the angular sector.
```

If that projection is derived, the chain becomes:

```text
finite-action C1 endpoint
  -> self-similarity p=1/3
  -> phi=0 scalar interface jump 1/6
  -> epsilon-frame projection over N=3
  -> eta=1/18
  -> unit damping eta/2 if the boundary transfer uses half-action weight
```

Remaining open links:

```text
1. scalar-interface projection onto epsilon frame,
2. half-action weighting in the transfer trace,
3. independent boundary-constraint count.
```

## 111. Scalar projection route to eta

Implemented in `native_scalar_projection_eta.py`.

The corrected interface result is:

```text
B = Delta K * R = p/2
```

For the self-similar endpoint:

```text
p = 1/3
B = 1/6
```

The extrinsic-curvature tensor does not divide this equally over shell tangent
directions.  But `B` itself is a scalar boundary quantity.  If the scalar
boundary term acts on the transported `N`-label angular/epsilon space and carries
no label index, then label symmetry forces:

```text
B -> B I_N
```

The normalized per-label action is then:

```text
eta = Tr(B I_N) / N^2
    = B/N
```

For the native self-similar/three-label case:

```text
p = 1/3
N = 3
B = 1/6

eta = B/N
    = (1/6)/3
    = 1/18

eta/2 = 1/36
```

This recovers the transfer factor:

```text
gamma = N exp(-eta/2)
      = 3 exp(-1/36)
```

Ninety-eighth verdict:

```text
eta=1/18 can be recast as a scalar boundary projection:

  self-similar interface jump / transported label count.
```

This does not require isotropic extrinsic curvature.

It does require:

```text
Pproject:
  the scalar phi=0 boundary jump acts as an identity operator on the
  transported N=3 frame/epsilon label space.
```

That is a smaller and more metric-aligned assumption than the older form:

```text
Pepsilon:
  set eta=1/18.
```

Updated status:

```text
derived/native:
  p=1/3 from endpoint/action self-similarity
  B=p/2=1/6 from phi=0 interface geometry
  N=3 transported label space from angular/epsilon structure

conditional:
  eta=B/N=1/18 if the scalar boundary action projects as B I_N

still open:
  half-action transfer weight
  independent closure count
  why the scalar projection is occupied by each boundary constraint
```

This is a better kind of progress:

```text
we did not choose eta to fit masses;
we found the metric pieces that would generate eta if the boundary scalar
couples democratically to the native three-label frame.
```

## 113. Projection normalization audit

Implemented in `native_projection_normalization_audit.py`.

The scalar projection route needs one more precision step.

Given:

```text
p = 1/3
B = Delta K * R = p/2 = 1/6
N = 3
```

label symmetry alone says only:

```text
S_label = alpha I_N
```

It does not by itself determine `alpha`.

There are two different lifts:

```text
per-channel scalar lift:
  S_label = B I_N
  Tr(S_label) = N B
  eta candidate = B = 1/6

trace-preserving total-action lift:
  S_label = (B/N) I_N
  Tr(S_label) = B
  eta candidate = B/N = 1/18
```

Therefore:

```text
identity form:
  follows from scalar label-blindness.

eta = B/N:
  follows only if the scalar boundary action is a single total boundary
  budget whose trace is preserved when lifted into the N-label space.
```

This is plausible because the metric interface scalar is integrated once over
the boundary, not once per transported label.

But it is still a named conditional rule:

```text
Ptrace:
  lifting the scalar phi=0 boundary action into the transported N-label
  space preserves the total scalar action:

    Tr(S_label) = B

  hence:

    S_label = (B/N) I_N
```

Hundredth verdict:

```text
The eta route is now sharper:

  p=1/3
  B=1/6
  Ptrace
  N=3
  eta=B/N=1/18

The remaining assumption is not "choose eta";
it is "the boundary scalar lifts trace-preservingly into the label space."
```

This is a smaller, testable geometric statement.

## 112. Half-action transfer audit

Implemented in `native_half_action_transfer_audit.py`.

Given the scalar projection candidate:

```text
N = 3
eta = 1/18
```

the transfer trace has the form:

```text
gamma = Tr exp(-w eta I_N)
      = N exp(-w eta)
```

Candidate weights:

```text
full action:
  w = 1
  gamma = 2.83787840672

half action:
  w = 1/2
  gamma = 2.91781343135

quarter action:
  w = 1/4
  gamma = 2.95862135023
```

The current ladder used:

```text
w = 1/2
gamma = N exp(-eta/2)
```

Native interpretation:

```text
half-action weighting is natural for a symmetric interface-to-interface
transfer, where a boundary scalar unit is shared between the two sides
of a finite cell.
```

But the metric has not forced it yet.

Ninety-ninth verdict:

```text
eta has a plausible scalar-boundary projection route.
The factor eta/2 remains a transfer rule awaiting derivation from a
two-boundary cell variational problem.
```

Updated dependency chain:

```text
stronger:
  p=1/3
  B=p/2=1/6
  eta=B/N=1/18 if scalar boundary projection acts on N=3 label space

weaker:
  w=1/2 in exp(-w eta)
  independent closure depth counts
```

Next target:

```text
derive the finite-cell transfer as a two-interface problem:

  left phi=0 collar
  negative-phi interior
  right/outer closure collar

and check whether the boundary scalar enters as:

  S_step = eta/2

or instead:

  S_step = eta
```

## 114. Boundary constraint-origin audit

Implemented in `native_boundary_constraint_origin_audit.py`.

The depth rule can also be restated in the metric-discovery frame.

Candidate:

```text
n_close(d) = N_frame + 2(d - 1)
```

Metric-native ingredients:

```text
N_frame:
  transported oriented frame / epsilon closure count.

d - 1:
  non-scalar sector-shape data after removing the common scalar mode.

2:
  the two finite-cell boundaries:
    core-side boundary
    phi=0 boundary
```

For `N_frame=3`:

```text
O0:
  d=1
  n_close=3+0+0=3
  caveat: formal scalar count only; no non-scalar negative-phi matter endpoint.

M1:
  d=2
  n_close=3+1+1=5

E1:
  d=3
  n_close=3+2+2=7

M2:
  d=5
  n_close=3+4+4=11
  caveat: nonprimitive or nonresonant under current branch filter.
```

Hundred-first verdict:

```text
The useful depths 5 and 7 can be stated as boundary data counts:

  frame closure
  plus non-scalar shape closure at two cell boundaries.
```

This is better than assigning depths from mass targets.

But the open links are still significant:

```text
1. why every closure constraint is epsilon-mediated;
2. why the frame-orientation count is N_frame=3 for every surviving branch;
3. why the core-side and phi=0 shape constraints are independent;
4. why each accepted constraint contributes the same transfer trace gamma.
```

Updated orchestra status:

```text
eta:
  now has a boundary scalar / trace-preserving projection route.

depth:
  now has a boundary constraint-count route.

gamma:
  still requires both eta and the half-action transfer rule.

mass ladder:
  still conditional, but the conditional pieces are becoming geometric
  questions rather than loose knobs.
```

## 115. Two-boundary independence audit

Implemented in `native_two_boundary_independence_audit.py`.

The `2(d-1)` part of the closure count has a native variational reason.

For a local finite-cell shape action:

```text
S_shape = integral L(q_a, q'_a) dr
```

the variation contains:

```text
[ Pi_a delta q_a ]_core^phi0

= Pi_a(phi0) delta q_a(phi0)
  - Pi_a(core) delta q_a(core)
```

Unless another metric condition ties the endpoint variations:

```text
delta q_a(core)
delta q_a(phi0)
```

are independent boundary data.

Therefore each non-scalar shape mode contributes:

```text
1 core-side closure constraint
1 phi=0-side closure constraint
```

For a branch of dimension `d`, after removing the common scalar mode:

```text
non-scalar modes = d - 1
two-boundary shape constraints = 2(d - 1)
```

This gives:

```text
M1:
  d=2
  two-boundary shape constraints=2

E1:
  d=3
  two-boundary shape constraints=4
```

Hundred-second verdict:

```text
The factor 2 in N + 2(d-1) is variationally natural for local finite-cell
shape data.
```

This does not yet prove:

```text
epsilon mediation,
shared gamma weight,
or the universal N=3 frame-closure count.
```

But it does improve the depth rule:

```text
before:
  5 and 7 were useful closure numbers.

after:
  5 and 7 are:

    N_frame=3
    plus local two-boundary non-scalar shape closure.
```

Remaining failure mode:

```text
If a future metric boundary condition ties the two endpoint variations,
the count collapses from 2(d-1) to d-1 and the current ladder fails.
```

## 116. Frame-count origin audit

Implemented in `native_frame_count_origin_audit.py`.

The `N_frame=3` term also needs a clean status.

For the round two-sphere:

```text
dim H_ell = 2 ell + 1
```

Therefore:

```text
ell=0:
  dimension=1
  scalar/common mode

ell=1:
  dimension=3
  lowest non-scalar angular space
  unique three-index epsilon available

ell=2:
  dimension=5
  no unique three-index epsilon of the same type
```

Metric-native facts:

```text
the angular block is the round S2;
the lowest non-scalar harmonic space has dimension 3;
the oriented three-label space carries epsilon_abc.
```

Conditional universal-use step:

```text
both M1 compact/primitive branches and E1 ordinary branches close through
the same phi=0 scalar/interface angular frame.
```

If true:

```text
every surviving branch inherits N_frame=3.
```

If false:

```text
M1 and E1 could carry different frame counts,
and the shared gamma/depth structure would not be universal.
```

Hundred-third verdict:

```text
N_frame=3 is metric-native for the lowest non-scalar S2 angular space.
Its universal use across surviving branches remains a boundary-closure
condition, not a completed derivation.
```

Updated depth-chain status:

```text
N_frame=3:
  native S2 fact, universal-use conditional.

2(d-1):
  variationally natural from independent endpoint shape data.

n_close = N_frame + 2(d-1):
  good boundary-count candidate, still awaiting epsilon mediation and
  transfer-weight derivation.
```

## 117. Epsilon mediation status

Implemented in `native_epsilon_mediation_status.py`.

The closure count only becomes a mass hierarchy if the constraints are
epsilon/frame mediated.

Constraint classes:

```text
frame orientation closure:
  count = N_frame
  epsilon status = direct
  reason = the constraint is defined on the transported oriented N=3 frame.

core-side non-scalar shape closure:
  count = d - 1
  epsilon status = conditional
  reason = shape data must be projected onto the same transported H1/epsilon frame.

phi=0-side non-scalar shape closure:
  count = d - 1
  epsilon status = conditional
  reason = the phi=0 interface has both the scalar boundary jump and S2 frame available.
```

For surviving branches:

```text
M1:
  3 direct frame constraints
  2 conditional shape constraints

E1:
  3 direct frame constraints
  4 conditional shape constraints
```

Hundred-fourth verdict:

```text
epsilon mediation is solid for the frame-closure part.
epsilon mediation is still conditional for the 2(d-1) shape-closure part.
```

Failure mode:

```text
If non-scalar shape modes close by scalar amplitude matching only,
they contribute no N entropy and the hierarchy collapses.
```

Survival condition:

```text
non-scalar shape closure must be measured in the transported H1 frame,
not merely in scalar amplitude.
```

This is now the main depth-rule target:

```text
derive the boundary shape form and check whether its natural basis is:

  scalar amplitude basis:
    no epsilon entropy from shape constraints;

  transported H1 frame basis:
    shape constraints are epsilon-mediated and the 5/7 count survives.
```

## 118. Shape-basis projection audit

Implemented in `native_shape_basis_projection_audit.py`.

A `d`-component branch has:

```text
1 common amplitude mode
d - 1 relative shape modes
```

For shape closure to be epsilon-mediated, the relative modes must be represented
as boundary data in the transported `N=3` frame space.

Branch status:

```text
E1:
  d=3
  relative shape modes=2
  frame dimension N=3
  embedding status=direct

M1:
  d=2
  relative shape modes=1
  frame dimension N=3
  embedding status=conditional

M2:
  d=5
  relative shape modes=4
  frame dimension N=3
  embedding status=fails elementary frame embedding
```

Hundred-fifth verdict:

```text
E1 shape closure is naturally frame-mediated.
M1 shape closure is frame-mediated only if the compact primitive doublet
closes through the common phi=0 H1 frame.
M2 fails elementary N=3 frame embedding, matching its demotion.
```

This is the orchestra picture in a more exact form:

```text
E1:
  ordinary angular frame is enough to carry the branch shape data.

M1:
  compact topology selects the primitive doublet,
  but the doublet must still meet the ordinary phi=0 frame to receive
  the shared boundary transfer.
```

So the M1 branch is not a topology solo.
It is a topology/interface/angular-frame chord.

Remaining M1-specific open link:

```text
derive the map from primitive compact U(1) doublet data to the common
phi=0 transported H1 frame.
```

## 119. M1 Hopf-to-H1 bridge

Implemented in `native_hopf_m1_h1_bridge.py`.

The primitive compact U(1) doublet has a native projective map to the ordinary
two-sphere.

Let:

```text
z = (z1, z2) in C2
z†z = 1
z ~ exp(i alpha) z
```

Then:

```text
normalized doublet / compact phase = CP1 = S2
```

The phase-invariant bilinears are:

```text
X = 2 Re(z1* z2)
Y = 2 Im(z1* z2)
Z = |z1|^2 - |z2|^2
```

They satisfy:

```text
X^2 + Y^2 + Z^2 = 1
```

and give the ordinary `S2` coordinate vector:

```text
(X,Y,Z) = (sin theta cos phi, sin theta sin phi, cos theta)
```

This is not a Dirac/Form-T import.  It is the standard projective geometry of a
compact U(1) doublet.

Hundred-sixth verdict:

```text
The primitive compact M1 doublet has a native map into the common ell=1/H1
angular frame:

  compact doublet
  -> quotient by compact phase
  -> CP1
  -> S2 coordinate vector
  -> H1 frame data
```

So the M1 branch can be an orchestra chord:

```text
compact topology:
  selects the primitive doublet.

projective/Hopf map:
  turns the doublet's phase-invariant shape into S2/H1 data.

phi=0 interface:
  supplies the shared scalar boundary jump and transfer frame.
```

Remaining condition:

```text
the boundary action must use these projective bilinears as the M1 shape-closure
variables.
```

## 120. Projective dimension filter

Implemented in `native_projective_dimension_filter.py`.

For compact U(1) flux `n`, the lowest compact sector has:

```text
d = |n| + 1
```

After quotienting the common compact phase:

```text
projective space = CP^(d-1)
real dimension = 2(d-1)
```

The common interface frame is:

```text
S2
real dimension = 2
```

Therefore:

```text
n=0:
  d=1
  projective dimension=0
  trivial compact sector

|n|=1:
  d=2
  CP1 real dimension=2
  CP1 = S2
  unique primitive compact sector matching the interface

|n|>1:
  d>2
  CP^(d-1) real dimension > 2
  projective space larger than the elementary S2 interface
```

Hundred-seventh verdict:

```text
The primitive compact sector |n|=1 is uniquely able to meet the elementary
S2/H1 interface without extra projection data.
```

This strengthens M1 selection:

```text
before:
  |n|=1 was primitive and energetically elementary if compact flux is admitted.

after:
  |n|=1 is also the unique compact projective sector whose shape space is S2,
  matching the ordinary phi=0 interface frame.
```

This also sharpens M2 demotion:

```text
higher compact sectors are not just nonprimitive;
their projective shape spaces are too large for the elementary H1 interface.
```

## 121. Symmetric boundary-transfer audit

Implemented in `native_symmetric_boundary_transfer.py`.

The remaining factor in:

```text
gamma = N exp(-eta/2)
```

is the half-action weight.

A local interval transfer has:

```text
left boundary side
right boundary side
```

For composable transfer kernels, a shared internal boundary should contribute
one boundary action after gluing, not two.

Therefore the symmetric assignment is:

```text
each boundary side carries B/2
two adjacent sides at a glued boundary give B
```

Applied to the projected boundary action:

```text
B_label = eta
single transfer side = eta/2
```

so:

```text
T = exp(-(eta/2) I_N)
gamma = Tr(T)
      = N exp(-eta/2)
```

Hundred-eighth verdict:

```text
eta/2 is natural for a composable symmetric boundary-transfer kernel.
The full eta is recovered only after two boundary sides are glued.
```

This upgrades the transfer factor from:

```text
chosen damping:
  exp(-eta/2)
```

to:

```text
conditional boundary-kernel consequence:
  a one-sided transfer carries half the boundary action to avoid double counting.
```

Remaining condition:

```text
each closure constraint must be represented by such a composable boundary kernel.
```

Updated gamma chain:

```text
p=1/3
  -> phi=0 scalar interface jump B=1/6
  -> trace-preserving lift to N=3 label space gives eta=B/N=1/18
  -> symmetric boundary-transfer side gives eta/2
  -> gamma=N exp(-eta/2)
```

Remaining weak link in the hierarchy:

```text
not gamma;
now mainly the closure-constraint graph:

  which constraints exist,
  which are epsilon/frame mediated,
  and which are independent.
```

## 122. Revised dependency ledger

Implemented in `native_revised_dependency_ledger.py`.

The status of the main inputs has shifted.

```text
eta=1/18
  old:
    Pepsilon normalization postulate.
  new:
    conditional scalar-boundary projection:
      p=1/3
      B=1/6
      eta=B/N
  remaining gap:
    derive trace-preserving lift Tr(S_label)=B.

gamma=N exp(-eta/2)
  old:
    native-looking transfer ansatz.
  new:
    conditional trace of symmetric one-sided boundary kernel.
  remaining gap:
    show each closure constraint is represented by the kernel.

M1 to H1 frame mediation
  old:
    conditional compact branch frame assumption.
  new:
    Hopf/projective bridge CP1=S2 for primitive compact doublet.
  remaining gap:
    show boundary action uses phase-invariant bilinears.

M1 primitive selection
  old:
    primitive nonzero compact flux if Pbundle0 admitted.
  new:
    primitive flux plus unique projective S2 interface match.
  remaining gap:
    derive why nontrivial compact bundle is occupied.

2(d-1) shape count
  old:
    boundary-count ansatz.
  new:
    variationally natural independent endpoint shape data.
  remaining gap:
    check no metric condition ties the two endpoints.

N_frame=3
  old:
    epsilon/angular postulate pressure.
  new:
    metric-native lowest non-scalar S2 frame.
  remaining gap:
    derive universal use by all surviving branch closures.

closure independence
  old:
    factorized entropy assumption.
  new:
    still the main unresolved hierarchy condition.
  remaining gap:
    derive factor graph and rule out equality correlations.

electron anchor
  old/new:
    accepted dimensionful input F.
```

Hundred-ninth verdict:

```text
The largest remaining live assumption is no longer eta or gamma directly.
It is the boundary closure factor graph:

  which constraints exist,
  whether they use the common frame kernel,
  and whether they are independent physical boundary choices.
```

This is exactly where the orchestra frame matters:

```text
the hierarchy appears only if endpoint geometry, interface geometry,
ordinary angular frame, compact projective topology, and transfer composition
all participate in the same boundary graph.
```

## 123. Frame gauge / physical audit

Implemented in `native_frame_gauge_audit.py`.

The frame count only contributes to hierarchy if the frame labels are physical
boundary-sector data, not removable gauge coordinates.

Diagnostic scenarios:

```text
physical boundary sectors:
  frame and shape constraints are physical boundary nodes.

one global frame gauge:
  one common frame label is gauge and divided out.

shape nodes only:
  frame labels are pure gauge; only shape endpoints count.

frame nodes only:
  shape closure is scalar amplitude only.
```

Hundred-tenth verdict:

```text
The hierarchy depends strongly on treating transported frame labels as
boundary observables measured by the interface kernel.
```

If the frame is only gauge:

```text
the current closure entropy is overcounted.
```

If shape closure is scalar-amplitude only:

```text
the ladder collapses.
```

Therefore the needed derivation is:

```text
show that the phi=0 boundary/interface kernel measures the transported
H1/projective frame label as an observable sector variable.
```

## 124. S2 isotropic projection audit

Implemented in `native_s2_isotropic_projection.py`.

This is the strongest version so far of the trace-preserving lift.

Let `n_a` be the unit coordinate vector on the round metric two-sphere:

```text
n = (sin theta cos phi, sin theta sin phi, cos theta)
```

The normalized second moment is:

```text
<n_a n_b> = integral n_a n_b dOmega / integral dOmega
          = delta_ab / 3
```

This is not a chosen label split.  It is the isotropic projection forced by the
round `S2` metric.

Apply the scalar interface budget:

```text
p = 1/3
B = Delta K * R = p/2 = 1/6
```

Then:

```text
B <n_a n_b>
  = (1/6)(delta_ab/3)
  = (1/18) delta_ab
```

So:

```text
eta = 1/18
```

Hundred-eleventh verdict:

```text
The round S2 metric supplies the trace-preserving equal split through:

  <n_a n_b> = delta_ab/3.
```

Therefore the eta chain is now:

```text
endpoint/action self-similarity:
  p = 1/3

phi=0 interface geometry:
  B = p/2 = 1/6

round S2 isotropic projection:
  <n_a n_b> = delta_ab/3

projected boundary action:
  B <n_a n_b> = (1/18) delta_ab

eta:
  1/18
```

Remaining condition:

```text
the closure observable must be the H1/projective unit vector n_a,
not an anisotropic selected component.
```

This substantially improves the status of `Ptrace`:

```text
before:
  trace-preserving lift was a plausible projection rule.

after:
  trace-preserving lift is the isotropic second moment of the round S2 metric,
  if the boundary closure variable is n_a.
```

## 125. Current eta/gamma chain

Implemented in `native_eta_gamma_chain_current.py`.

Current chain:

```text
metric-derived or metric-forced:

  endpoint self-similarity:
    p = 1/3

  phi=0 interface scalar:
    B = p/2 = 1/6

  round S2 isotropic projection:
    <n_a n_b> = delta_ab/3

  eta:
    eta = B/3 = 1/18
```

Composable transfer:

```text
one-sided boundary action:
  eta/2 = 1/36

transfer trace:
  gamma = N exp(-eta/2)
        = 3 exp(-1/36)
        = 2.91781343135
```

Remaining required conditions:

```text
1. The boundary closure observable is the H1/projective unit vector n_a.

2. Closure constraints are represented by symmetric composable boundary kernels.

3. Closure nodes are physical and independent in the factor graph.
```

Hundred-twelfth verdict:

```text
eta is now metric-derived under condition 1.
gamma is transfer-derived under conditions 1 and 2.
the hierarchy still depends on condition 3.
```

This is the cleanest current status of the mass-side rebuild:

```text
the metric has supplied the numerical unit;
the transfer formalism has supplied the half-weight;
the unresolved part is the closure graph.
```

## 126. H1 kernel physicality audit

Implemented in `native_h1_kernel_physicality_audit.py`.

There is a possible overcount:

```text
are H1 frame labels physical boundary data,
or are they only a removable global S2 rotation?
```

Represent boundary H1 data as:

```text
q_a
```

The isotropic metric projection gives:

```text
S = eta q_a q_a
K_ab = eta delta_ab
```

Under a global S2 rotation:

```text
q -> R q
K -> R^T K R
```

For:

```text
K = eta I_3
```

the kernel is unchanged up to basis conjugation.  Its rank and trace are
invariant.

Therefore:

```text
ordinary rotational symmetry:
  changes basis inside H1;
  preserves the three-dimensional transfer rank.

singlet-only/gauge projection:
  removes H1 entirely;
  collapses the non-scalar boundary sector.
```

Hundred-thirteenth verdict:

```text
Treating the H1 rank as physical is consistent if non-scalar boundary
shapes are allowed as sector data.
```

The hierarchy fails only under the stronger condition:

```text
elementary closure requires S2-rotation singlets at each boundary constraint.
```

That stronger condition would also erase the non-scalar M1/E1 branch structure.

So the current working stance is:

```text
H1 rotations are symmetries producing degenerate boundary modes,
not gauge redundancies to divide out.
```

Remaining independence question:

```text
not whether H1 has rank 3;
it does.

the question is whether distinct closure constraints carry independent H1
kernels or are tied by equality/matching edges in the boundary graph.
```

## 127. Constraint granularity audit

Implemented in:

```text
native_constraint_granularity_audit.py
native_rank_one_constraint_kernel.py
native_scalar_closure_equation_inventory.py
```

There is a deeper possible overcount.

An H1 block has rank 3.  But one full H1 block contributes one trace:

```text
Tr exp(-K/2)
```

The current ladder instead uses:

```text
gamma^k
```

for `k` scalar closure equations.  That requires the boundary action to factor
at the scalar-equation level.

For one scalar closure equation measured in H1:

```text
P_i = |i><i|
i = 1..N

Z_1 = sum_i exp(-eta/2)
    = N exp(-eta/2)
    = gamma
```

For `k` independent scalar closure equations:

```text
Z_k = gamma^k
```

But for one correlated H1 block:

```text
Z_block = gamma
```

Hundred-fourteenth verdict:

```text
H1 rank by itself gives one trace.
The current depth rule requires independent rank-one H1 projector constraints.
```

Named scalar closure-equation inventory:

```text
M1:
  transported frame component closure = 3
  core-side relative shape closure    = 1
  phi0-side relative shape closure    = 1
  total = 5

E1:
  transported frame component closure = 3
  core-side relative shape closure    = 2
  phi0-side relative shape closure    = 2
  total = 7
```

This inventory is useful, but it is not the final proof.

Remaining metric task:

```text
show that these named scalar equations are independent rank-one H1/projective
kernel constraints, not components of one correlated global block.
```

## 128. Current native orchestra graph

Implemented in `native_orchestra_graph_current.py`.

This section is a deliberate zoom-out.

The strongest current pattern is not a solo mechanism.  It is a coupled
boundary graph.

Native instruments:

```text
negative_phi_endpoint:
  metric/action native.
  creates finite-action endpoint arena and p=1/3 self-similarity.

phi0_interface:
  metric native.
  supplies scalar boundary jump B=p/2.

round_S2_H1:
  metric native.
  supplies N=3 lowest non-scalar frame and isotropic projection.

compact_U1_primitive:
  conditional topology.
  selects primitive M1 doublet if nontrivial compact bundle is occupied.

Hopf_projective_bridge:
  topology/geometry native once compact doublet exists.
  maps primitive compact doublet modulo phase to CP1=S2/H1 data.

symmetric_transfer_kernel:
  composition native.
  assigns eta/2 to one side of a composable boundary transfer.

two_boundary_variation:
  local action native.
  makes core-side and phi0-side shape boundary data independent unless tied.

closure_factor_graph:
  open.
  decides whether closure nodes are independent physical kernel factors.
```

Key couplings:

```text
negative_phi_endpoint -> phi0_interface:
  p=1/3 gives B=1/6.

phi0_interface -> round_S2_H1:
  B <n_a n_b> = (1/18) delta_ab.

round_S2_H1 -> symmetric_transfer_kernel:
  gamma = 3 exp(-1/36), if closure constraints are composable kernels.

compact_U1_primitive -> Hopf_projective_bridge:
  primitive doublet / U(1) phase = CP1=S2.

Hopf_projective_bridge -> round_S2_H1:
  M1 compact shape can be read as H1/projective boundary data.

two_boundary_variation -> closure_factor_graph:
  provides two endpoint shape data sets.
```

Hundred-fifteenth verdict:

```text
The mass-side structure now looks like a native boundary orchestra:

  endpoint self-similarity supplies p,
  interface geometry supplies B,
  S2 isotropy supplies eta,
  transfer composition supplies eta/2,
  compact projective topology lets M1 play in the same H1 frame,
  two-boundary variation supplies shape closure locations.
```

The open question is not "which solo mechanism makes mass?"

It is:

```text
do these native instruments form independent physical closure nodes,
or do they collapse into a correlated/global boundary block?
```

## 129. Orchestra locality / independence audit

Implemented in `native_orchestra_locality_independence.py`.

The graph should not be assumed independent merely because independence gives
the desired hierarchy.

But equality edges are also not automatic if closure nodes live on distinct
boundary locations or distinct variational variables.

Current M1 nodes:

```text
frame_x:
  location = collar transport
  variable = H1/projective frame component x

frame_y:
  location = collar transport
  variable = H1/projective frame component y

frame_z:
  location = collar transport
  variable = H1/projective frame component z

core_shape:
  location = core-side boundary
  variable = M1 relative shape via CP1

phi0_shape:
  location = phi0 boundary
  variable = M1 relative shape via CP1
```

Current E1 nodes:

```text
frame_x, frame_y, frame_z:
  location = collar transport
  variable = H1 frame components

core_shape_1, core_shape_2:
  location = core-side boundary
  variable = E1 relative shape modes

phi0_shape_1, phi0_shape_2:
  location = phi0 boundary
  variable = E1 relative shape modes
```

Native supports for factorization:

```text
core-side and phi0-side variables:
  appear as separate endpoint variations in a local radial action.

H1 frame components:
  orthogonal under the round S2 measure.

M1 compact shape:
  reaches H1 through phase-invariant CP1 bilinears.

interface scalar kernel:
  isotropic, so it imposes no preferred equality edge between components.
```

Collapse risks:

```text
a global matching condition could tie core and phi0 shape variables;
a singlet-only closure rule could project out non-scalar H1 data;
a single-block transfer could replace tensor-product node traces.
```

Hundred-sixteenth verdict:

```text
The orchestra graph has native locality reasons to remain factorized,
but independence is still a structural hypothesis until the full boundary
variation is written in these variables.
```

This is the right balance:

```text
not just fitting:
  independent nodes correspond to distinct metric/topological/interface
  objects.

not yet derived:
  we have not written the full boundary action proving no equality edges.
```

## 130. Observation / mechanism separation

Implemented in `native_observation_mechanism_separation.py`.

This is a methodological guardrail:

```text
UDT can match observed quantities without using the same mechanisms
as the Standard Model.
```

This already matters in the macro sector.  It may also matter in the particle
sector.

Allowed uses of observations:

```text
electron mass:
  allowed as the single dimensionful anchor F.

muon/tau masses:
  allowed as diagnostic comparisons after target-blind structure is derived.

QED/Coulomb:
  allowed only where the metric itself supplies phi-blind abelian dynamics.

SU(3)/color language:
  allowed as translation language for S2/H1/epsilon kinematics.

generation language:
  allowed as a diagnostic label for ladder branches.
```

Forbidden uses:

```text
do not infer the SM electron mass mechanism from the electron anchor;
do not choose closure counts from mu/tau masses;
do not re-import Dirac/Form-T spinor mechanics;
do not import non-abelian color force or confinement dynamics;
do not assume SM generation ontology.
```

Native substitutes:

```text
electron anchor:
  sets scale after native ratios are computed.

mu/tau observations:
  test residual signs and branch-specific predictions.

spinor/Dirac analogs:
  replaced by negative-phi endpoint data, H1 frame data,
  and compact projective data.

SM color analogs:
  replaced by round-S2 kinematics, epsilon projection,
  and metric-derived closure rules only.

generations:
  replaced by finite-cell closure depths and branch filters.
```

Hundred-seventeenth verdict:

```text
Observed agreement is an output test, not a mechanism license.
```

The active rule is:

```text
Use observations to anchor and falsify.
Use the metric/orchestra to build.
```

## 131. Three-rule search protocol

Implemented in `native_three_rule_search_protocol.py`.

The working search rules are now:

```text
1. Uncover what the metric is already doing.

2. Preserve the orchestra:
   test coupled instruments, not only isolated solos.

3. Use observations to anchor/test,
   but do not import the observed sector's standard mechanism.
```

Candidate priorities under this protocol:

```text
H1/projective boundary observable n_a:
  metric-native content:
    round S2 coordinate vector and CP1 Hopf image.
  orchestra role:
    connects interface scalar, E1 ordinary frame, and M1 compact doublet.
  import/fitting risk:
    low.
  next action:
    derive boundary action in n_a variables.

closure factor graph:
  metric-native content:
    local endpoint variations plus H1 orthogonality.
  orchestra role:
    decides whether instruments remain independent nodes.
  import/fitting risk:
    medium.
  next action:
    derive graph from boundary variation before mass comparison.

Coulomb phi-blind sector:
  metric-native content:
    Maxwell cancellation in UDT metric.
  orchestra role:
    possible branch-selective interface energy.
  import/fitting risk:
    medium.
  next action:
    couple only verified abelian boundary energy to the graph.

angular determinant finite part:
  metric-native content:
    round S2 Laplacian and measure.
  orchestra role:
    possible branch correction after base graph.
  import/fitting risk:
    high.
  next action:
    use only target-blind subtraction-invariant signs.

nontrivial compact bundle occupation:
  metric-native content:
    topology supports transport if admitted.
  orchestra role:
    enables M1 primitive branch and Hopf bridge.
  import/fitting risk:
    medium.
  next action:
    search for interface obstruction requiring nonzero compact flux.
```

Hundred-eighteenth verdict:

```text
The next best calculation is the boundary action in H1/projective n_a variables.
```

Reason:

```text
it tests the metric-native eta projection,
the M1/E1 orchestra bridge,
and the closure graph,
without borrowing Standard Model machinery or fitting observed masses.
```

## 132. H1/projective boundary-action skeleton

Implemented in `native_h1_boundary_action_skeleton.py`.

The minimal native boundary action in the `H1/projective` observable should use
only terms currently supported by the metric.

Boundary observable:

```text
n_a n_a = 1
```

Status:

```text
metric/projective native:
  ordinary S2 coordinate vector for E1;
  CP1/S2 Hopf image for primitive compact M1.
```

Round-S2 projection:

```text
<n_a n_b> = delta_ab / 3
```

Interface scalar coupling:

```text
B <n_a n_b>

B = p/2
```

At the self-similar endpoint:

```text
p = 1/3
B = 1/6

B <n_a n_b> = (1/18) delta_ab
```

One-sided transfer split:

```text
S_side = eta / 2
```

Status:

```text
composition native for symmetric transfer kernels;
prevents double-counting under gluing.
```

Conditional shape closure projectors:

```text
P_i = |i><i|
```

Status:

```text
conditional;
requires distinct scalar closure equations.
```

Explicitly not native yet:

```text
anisotropic branch potential:
  V_ab n_a n_b, with V not proportional to delta_ab.
```

Guardrail:

```text
do not introduce anisotropic terms to fit mu/tau residuals.
```

Hundred-nineteenth verdict:

```text
The minimal native n_a boundary action is isotropic.
It can supply eta and gamma-side weights.
It does not by itself supply branch-specific residual corrections.
```

Therefore:

```text
the remaining hierarchy question is how many distinct shape/projector
closure equations the metric boundary variation actually creates.
```

## 133. M1 projective-count tension

Implemented in `native_m1_projective_count_tension.py`.

There is a possible overcount in the M1 orchestra bridge.

The primitive compact doublet gives:

```text
compact doublet / U(1) phase = CP1 = S2
```

But:

```text
CP1 has two real projective directions.
```

The current M1 depth count uses:

```text
d = 2
d - 1 = 1
```

shape equation per boundary.

Three possible counts:

```text
component-relative count:
  M1 shape per boundary = 1
  E1 shape per boundary = 2
  M1 depth = 5
  E1 depth = 7

projective-real count:
  M1 shape per boundary = 2
  E1 shape per boundary = 2
  M1 depth = 7
  E1 depth = 7

shared-projective count:
  M1 shape per boundary = 1
  E1 shape per boundary = 2
  M1 depth = 5
  E1 depth = 7
```

The only way to keep the current M1/E1 separation while using the Hopf bridge is:

```text
M1 CP1 orientation is not an extra pair of shape equations.
It is the way M1 enters the existing common H1 frame closure nodes.
```

Then the remaining M1-specific shape equation is:

```text
one primitive compact/radial relative closure scalar per boundary.
```

Hundred-twentieth verdict:

```text
Do not double-count the M1 Hopf sphere.
```

It can supply the bridge into the shared H1 frame, but if it is also counted as
two additional M1 shape degrees, M1 and E1 collapse to the same depth.

This is now a key boundary-action test:

```text
does the M1 projective orientation appear only in the common H1 frame closure,
with one residual primitive compact/radial shape scalar at each boundary?

or does it appear as two independent shape equations at each boundary?
```

## 134. Orchestra node-merge audit

Implemented in `native_orchestra_node_merge_audit.py`.

The orchestra metaphor needs a graph rule:

```text
couplings can merge nodes, not only add nodes.
```

This matters for M1.

Scenario A:

```text
M1 shared Hopf-frame graph:
  frame nodes = 3
  core shape nodes = 1
  phi0 shape nodes = 1
  total = 5

Interpretation:
  Hopf/CP1 orientation is the bridge into the existing H1 frame nodes.
  Only one primitive compact/radial shape scalar is added at each boundary.
```

Scenario B:

```text
M1 double-counted Hopf graph:
  frame nodes = 3
  core shape nodes = 2
  phi0 shape nodes = 2
  total = 7

Interpretation:
  CP1 projective directions are counted as extra M1 shape nodes in addition
  to the common H1 frame nodes.
```

Scenario C:

```text
E1 ordinary H1 graph:
  frame nodes = 3
  core shape nodes = 2
  phi0 shape nodes = 2
  total = 7

Interpretation:
  E1 relative shape modes are directly ordinary H1 shape modes at both
  boundaries.
```

Hundred-twenty-first verdict:

```text
Orchestra coupling is not simple addition.
Some instruments identify variables and prevent overcounting.
```

For the current M1 depth route:

```text
Hopf orientation must merge with the common H1 frame nodes,
not create separate CP1 shape nodes.
```

This is not arbitrary bookkeeping.  It follows the role of the Hopf map:

```text
Hopf/CP1 is the bridge into H1,
not an additional instrument playing an independent H1 melody.
```

Updated orchestra graph language:

```text
endpoint/interface:
  creates scalar boundary budget.

S2/H1:
  projects and weights the common frame nodes.

compact Hopf bridge:
  lets M1 share those frame nodes.

boundary variation:
  adds branch-specific shape nodes.

node merge rule:
  prevents shared bridge variables from being counted twice.
```

## 135. Orchestra node-role taxonomy

Implemented in `native_orchestra_node_role_taxonomy.py`.

The safe orchestra rule is:

```text
typed composition, not additive stacking.
```

Not every instrument adds a node.

Current role taxonomy:

```text
negative-phi endpoint:
  role = node condition
  effect = admits or excludes endpoint branches
  example = finite action and p=1/3 self-similarity

phi0 interface:
  role = weight source
  effect = supplies scalar budget B=p/2
  example = B=1/6 for p=1/3

round S2/H1:
  role = projector and rank source
  effect = turns scalar budget into eta delta_ab and rank-3 traces
  example = <n_a n_b>=delta_ab/3

symmetric transfer:
  role = edge weight
  effect = assigns one-sided eta/2 to composable boundary kernels
  example = gamma=3 exp(-1/36)

two-boundary variation:
  role = node creator
  effect = creates core-side and phi0-side shape closure opportunities
  example = 2(d-1) local shape data

compact U1 primitive:
  role = branch selector
  effect = admits M1 primitive doublet if nontrivial compact bundle occupied
  example = |n|=1

Hopf/CP1 bridge:
  role = node merger / bridge
  effect = identifies M1 compact orientation with common H1 frame nodes
  example = CP1=S2

observed masses:
  role = diagnostic only
  effect = tests output after graph is built
  example = electron anchor and mu/tau residual checks
```

Hundred-twenty-second verdict:

```text
A proposed instrument must state whether it:

  creates nodes,
  weights nodes,
  selects branches,
  bridges variables,
  merges nodes,
  or only diagnoses output.
```

This prevents two common errors:

```text
under-counting:
  treating all coupled instruments as one block.

over-counting:
  adding every coupled instrument as a new independent node.
```

## 136. Current typed branch graph

Implemented in `native_typed_branch_graph_current.py`.

Typed graph rule:

```text
selectors and bridges do not automatically add nodes.
```

### M1

Selectors:

```text
nontrivial primitive compact U1 sector |n|=1;
projective dimension CP1=S2 matches the elementary interface.
```

Bridge / merger:

```text
Hopf/CP1 maps compact orientation into the common H1 frame;
node-merge rule prevents double-counting CP1 as extra M1 shape nodes.
```

Closure nodes:

```text
shared frame nodes = 3
branch shape nodes per boundary = 1
boundary count = 2

shape nodes = 2
total closure nodes = 5
```

Remaining gap:

```text
requires Pbundle0 or a future metric reason for nontrivial compact occupation.
```

### E1

Selectors:

```text
ordinary H1 triplet;
p=1/3 endpoint resonance.
```

Bridge:

```text
ordinary H1 shape data directly uses the common frame.
```

Closure nodes:

```text
shared frame nodes = 3
branch shape nodes per boundary = 2
boundary count = 2

shape nodes = 4
total closure nodes = 7
```

Remaining gap:

```text
none at the current elementary-interface level.
```

Hundred-twenty-third verdict:

```text
M1 and E1 can differ in depth without assigning different eta/gamma.
```

The difference is in branch-shape node creation after typed composition:

```text
M1:
  3 shared frame + 2 shape = 5

E1:
  3 shared frame + 4 shape = 7
```

This is a genuine orchestra form:

```text
selectors, bridges, projectors, weights, mergers, and node creators
play different roles.
```

The current hierarchy claim should be stated as:

```text
if the typed boundary graph is physical and factorized,
then the native metric transfer unit gamma applies 5 times to M1
and 7 times to E1.
```

## 137. Typed graph mass diagnostic

Implemented in `native_typed_graph_mass_diagnostic.py`.

This is explicitly a diagnostic comparison, not a construction rule.

Metric/orchestra chain:

```text
p = 1/3
B = p/2 = 1/6
eta = B/3 = 1/18
gamma = 3 exp(-eta/2) = 2.91781343135
```

Observation use:

```text
electron mass:
  anchors the scale.

mu/tau masses:
  diagnostic only.

branch coefficients:
  current finite-cell diagnostics, not Standard Model imports.
```

M1 / mu-like branch:

```text
sector:
  M1

typed closure nodes:
  5

graph status:
  3 shared H1 frame nodes
  + 2 primitive compact/radial shape nodes

predicted mass:
  108.07061 MeV

diagnostic target:
  105.6583755 MeV

fractional error:
  +2.2831%
```

E1 / tau-like branch:

```text
sector:
  E1

typed closure nodes:
  7

graph status:
  3 shared H1 frame nodes
  + 4 ordinary H1 shape nodes

coefficient ratio:
  1.85479273951

predicted mass:
  1706.54612 MeV

diagnostic target:
  1776.86 MeV

fractional error:
  -3.9572%
```

Hundred-twenty-fourth verdict:

```text
The typed graph reproduces the previous compact ladder structure,
but with cleaner dependency language.
```

Remaining open items:

```text
1. prove graph factorization / no hidden equality edges;
2. derive or justify nontrivial compact bundle occupation;
3. derive branch coefficient normalization;
4. only then revisit residual corrections.
```

Do not use the few-percent agreement as a mechanism license.

Use it only as:

```text
a reason to keep investigating the metric-native orchestra graph.
```

## 138. Linearization / approximation risk audit

Implemented in `native_linearization_risk_audit.py`.

The current typed graph may be the correct skeleton but still miss nonlinear
metric behavior.

Possible approximation risks:

```text
endpoint power law:
  current:
    f ~ r^-p near the endpoint.
  nonlinear target:
    solve the full nonlinear f equation with angular/interface boundary data.
  risk:
    asymptotics may miss finite-cell matching constants.

interface scalar jump:
  current:
    B = Delta K R = p/2.
  nonlinear target:
    use full extrinsic curvature of matched finite cell.
  risk:
    finite-radius matching can alter the effective boundary scalar.

S2 isotropic projection:
  current:
    <n_a n_b> = delta_ab/3.
  nonlinear target:
    integrate the actual boundary distribution of n_a induced by the cell.
  risk:
    the distribution may be anisotropic even though the metric measure is isotropic.

rank-one closure projectors:
  current:
    independent P_i traces.
  nonlinear target:
    full coupled boundary kernel on products of H1/projective variables.
  risk:
    independent traces may become correlated by nonlinear constraints.

Hopf bridge:
  current:
    CP1=S2 maps compact doublet to H1 direction.
  nonlinear target:
    boundary action in z†sigma_a z variables with correct measure.
  risk:
    CP1/Fubini-Study measure may contribute nontrivial weights.

symmetric transfer:
  current:
    one side carries eta/2.
  nonlinear target:
    exact transfer composition including gluing measure.
  risk:
    determinant/Jacobian factors may modify gamma.

branch coefficients:
  current:
    finite-cell coefficient ratios reused from current ladder.
  nonlinear target:
    derive coefficients from the same typed graph.
  risk:
    few-percent residuals may live in coefficient normalization.
```

Hundred-twenty-fifth verdict:

```text
Do not interpret the few-percent residuals as missing mechanisms yet.
They may be artifacts of linearized boundary kernels, asymptotic endpoint
forms, or simplified measures.
```

Updated next step:

```text
replace skeleton pieces with nonlinear metric calculations before adding
residual corrections.
```

## 139. Finite-cell interface slope audit

Implemented in:

```text
native_finite_cell_interface_slope_audit.py
native_endpoint_vs_collar_exponent_audit.py
```

The eta chain used:

```text
B = Delta K R = p/2
```

But this assumes the endpoint exponent also controls the `phi=0` collar slope.

For a finite-cell profile:

```text
f(x) = x^-p h(x)
x = r/R
f(1) = 1
```

the collar slope is:

```text
f'(1) = -p + h'(1)
```

and the interface scalar is:

```text
B = -f'(1)/2
  = (p - h'(1))/2
```

Therefore:

```text
B = p/2
```

only if:

```text
h'(1) = 0
```

Equivalently, define:

```text
p_core:
  endpoint exponent from f ~ r^-p_core.

q_phi0:
  collar slope q_phi0 = -R f'(R)/f(R).
```

The interface scalar uses:

```text
B = q_phi0 / 2
eta = q_phi0 / 6
```

not `p_core` directly.

For eta:

```text
eta = 1/18
```

we need:

```text
q_phi0 = 1/3
```

Hundred-twenty-sixth verdict:

```text
p_core=1/3 does not by itself derive eta=1/18.
The eta chain requires q_phi0=1/3 at the interface collar.
```

A globally self-similar cell has:

```text
p_core = q_phi0 = 1/3
```

but a nonlinear finite cell could have:

```text
p_core != q_phi0
```

This is a major nonlinear target:

```text
derive whether the native finite-cell boundary problem enforces
p_core = q_phi0,
or whether the collar slope receives nonlinear shape corrections.
```

## 140. Log-slope flow audit

Implemented in `native_log_slope_flow_audit.py`.

Define the local logarithmic slope:

```text
q(r) = - d ln f / d ln r
```

For a pure power:

```text
f ~ r^-p
q = p
```

But for a nonlinear finite cell:

```text
q_core may differ from q_phi0.
```

The interface scalar depends on the collar value:

```text
B = q_phi0 / 2
eta = q_phi0 / 6
```

Therefore:

```text
eta = 1/18
```

requires:

```text
q_phi0 = 1/3
```

not merely:

```text
p_core = 1/3.
```

Hundred-twenty-seventh verdict:

```text
The nonlinear question is whether q=1/3 is a finite-cell flow fixed point
that survives from core to phi0 collar.
```

If yes:

```text
eta=1/18 remains metric-native.
```

If no:

```text
eta must be replaced by q_phi0/6,
and the compact ladder shifts before residual corrections are considered.
```

Next real calculation:

```text
derive the q-flow equation from the full negative-phi/angular boundary action.
```

## 141. Minimal q-flow candidate

Implemented in `native_minimal_q_flow_candidate.py`.

The endpoint/source relation:

```text
q(1-q)/2 = s
```

can be represented by the minimal autonomous candidate:

```text
dq/dtau = beta(q)
        = q^2 - q + 2s
```

This is not yet the derived flow.  It is only the simplest beta function whose
fixed points reproduce the angular-source relation.

For:

```text
s = 1/9
```

the fixed points are:

```text
q = 1/3
q = 2/3
```

Interpretation:

```text
q = 1/3:
  finite-action self-similar branch.

q = 2/3:
  companion non-finite-action branch under the p<1/2 filter.
```

Hundred-twenty-eighth verdict:

```text
The angular-source fixed-point relation naturally contains q=1/3.
```

But:

```text
stability and collar inheritance cannot be decided without the correctly
oriented q-flow from the full boundary action.
```

Therefore:

```text
q=1/3 is a promising nonlinear fixed-point target,
not yet a completed finite-cell derivation.
```

## 142. q-collar residual sensitivity

Implemented in `native_q_collar_residual_sensitivity.py`.

This is diagnostic only.

If the collar slope is:

```text
q_phi0 = q
```

then:

```text
eta = q/6
gamma(q) = 3 exp(-q/12)
```

Baseline:

```text
q = 1/3
gamma = 2.91781343135
```

M1 / mu-like branch:

```text
baseline mass:
  108.07061 MeV

target:
  105.6583755 MeV

required q:
  0.387510439043

delta q:
  +0.0541771057096
```

E1 / tau-like branch:

```text
baseline mass:
  1706.54612 MeV

target:
  1776.86 MeV

required q:
  0.264116906769

delta q:
  -0.0692164265639
```

Hundred-twenty-ninth verdict:

```text
A single common nonlinear collar slope cannot fix both residuals.
```

The signs are opposite:

```text
mu-like:
  wants larger q to lower its mass.

tau-like:
  wants smaller q to raise its mass.
```

Therefore:

```text
if the residuals are nonlinear effects,
they must be branch-specific or enter through branch coefficients/measures,
not through one universal q shift.
```

This reinforces the orchestra frame:

```text
the shared metric unit can be universal,
while residual corrections may arise from branch-specific nonlinear
measure, topology, or coefficient effects.
```

## 143. Derived q-flow from angular-source equation

Implemented in `native_derived_q_flow.py`.

The earlier minimal q-flow candidate can be derived from the constant-source
radial equation:

```text
f'' + 2 f'/r + 2s f/r^2 = 0
```

Use:

```text
t = ln r
q = - d ln f / d ln r
```

Then:

```text
f_tt + f_t + 2s f = 0
```

and the exact local slope flow is:

```text
dq/dt = q^2 - q + 2s
```

Fixed points obey:

```text
q(1-q)/2 = s
```

For:

```text
s = 1/9
```

the fixed slopes are:

```text
q = 1/3
q = 2/3
```

Their outward stability for increasing `r`:

```text
q = 1/3:
  beta' = -1/3
  outward-attractive

q = 2/3:
  beta' = +1/3
  outward-repulsive
```

Hundred-thirtieth verdict:

```text
For constant s=1/9, q=1/3 is the outward-attractive finite-action fixed point.
```

This strengthens the eta route:

```text
if the cell boundary layer is governed by the same H1 source through the
phi=0 collar, then q_phi0=1/3 is not a pure-power assumption.
It is the stable finite-action slope.
```

Remaining nonlinear risk:

```text
s may run with radius or branch data.
```

If so:

```text
q_phi0 follows a forced flow,
and eta becomes branch-sensitive through q_phi0/6.
```

## 144. Distributed approximation-correction map

Implemented in `native_distributed_approximation_corrections.py`.

Approximation corrections can affect multiple orchestra instruments.  They
should be classified before residuals are interpreted as physics.

Current correction channels:

```text
collar log-slope q_phi0:
  affects:
    M1 through gamma(q)^5;
    E1 through gamma(q)^7.
  status:
    common q cannot fix opposite residual signs.
  next:
    derive q-flow for M1 and E1 boundary data separately.

S2 boundary distribution:
  affects:
    M1 through Hopf/projective image distribution;
    E1 through ordinary H1 distribution.
  status:
    branch-specific if induced distributions differ.
  next:
    derive induced n_a distribution before using <n_a n_b>=delta/3.

CP1/Fubini-Study measure:
  affects:
    M1 directly.
  status:
    exact geometry known, action coupling open.
  next:
    compare Hopf bilinear measure to round S2 measure.

ordinary H1 shape measure:
  affects:
    E1 directly;
    M1 only through shared frame after Hopf merge.
  status:
    open boundary measure.
  next:
    derive E1 relative-shape measure after removing common amplitude mode.

transfer gluing determinant:
  affects:
    both branches if every kernel glues.
  status:
    common unless determinant depends on branch dimension or node type.
  next:
    derive kernel composition including normalization determinant.

node granularity/correlation:
  affects:
    both branches through effective node count.
  status:
    usually lowers entropy; cannot raise tau-like mass by itself.
  next:
    write boundary variation and identify equality edges.

branch coefficient normalization:
  affects:
    M1/E1 differently.
  status:
    not yet derived in typed graph.
  next:
    recompute coefficients from nonlinear typed boundary action.
```

Hundred-thirtieth verdict:

```text
Common corrections are useful for validating the skeleton,
but cannot explain opposite-sign residuals by themselves.
```

Most promising nonlinear places after the graph is written:

```text
branch-specific measures;
branch coefficient normalization;
possibly branch-specific q-flow / boundary layers.
```

Do not add residual terms until these native correction channels are derived or
ruled out.

## 145. CP1 / Hopf measure audit

Implemented in `native_cp1_measure_hopf_audit.py`.

The M1 bridge uses:

```text
primitive compact doublet / U(1) phase = CP1 = S2
```

The possible approximation risk was:

```text
CP1/Fubini-Study measure may not match the round S2 measure used in
<n_a n_b> = delta_ab/3.
```

In CP1 polar coordinates:

```text
z = tan(chi/2) exp(i phi)
```

the Fubini-Study area density is proportional to:

```text
sin(chi) dchi dphi
```

Under the Hopf/projective map:

```text
n = (sin chi cos phi, sin chi sin phi, cos chi)
```

the second moment is:

```text
<n_a n_b>_CP1 = delta_ab / 3
```

Hundred-thirty-first verdict:

```text
The CP1 Fubini-Study measure pushes forward to the round S2 measure.
```

Therefore:

```text
the primitive M1 Hopf bridge does not introduce hidden anisotropy at the
level of bare projective geometry.
```

Any M1-specific correction must come from:

```text
the boundary action;
compact-bundle occupation weight;
nonlinear q-flow;
or branch coefficient normalization,
```

not from CP1 measure alone.

## 146. E1 relative-shape measure audit

Implemented in `native_e1_relative_shape_measure_audit.py`.

For an ordinary three-component H1 branch, remove the common amplitude mode:

```text
c = (1,1,1)/sqrt(3)
```

The remaining relative-shape space is the two-dimensional plane orthogonal to
`c`.

An orthonormal basis in that plane has:

```text
Gram matrix = I
```

For a uniform relative angle in that plane:

```text
<u_i u_j> = delta_ij / 2
```

Hundred-thirty-second verdict:

```text
E1 relative shape after removing common amplitude is a clean isotropic
two-dimensional plane.
```

This supports:

```text
two E1 shape nodes per boundary.
```

But it does not supply:

```text
branch-specific residual corrections.
```

Therefore E1-specific corrections, if present, must come from:

```text
boundary action weighting;
nonlinear q-flow;
gluing/determinant factors;
or coefficient normalization,
```

not from bare relative-shape measure anisotropy.

## 147. Measure audit summary

Implemented in `native_measure_audit_summary.py`.

Bare geometry measures now have two checks:

```text
M1:
  space:
    CP1/Fubini-Study via Hopf.
  result:
    pushes forward to round S2.
  second moment:
    <n_a n_b> = delta_ab/3.
  implication:
    no bare compact-projective anisotropy.

E1:
  space:
    relative-shape plane after removing common amplitude.
  result:
    isotropic two-dimensional plane.
  second moment:
    <u_i u_j> = delta_ij/2.
  implication:
    no bare ordinary relative-shape anisotropy.
```

Hundred-thirty-third verdict:

```text
Bare geometry measures are clean on both M1 and E1 sides.
```

This strengthens:

```text
the shared isotropic skeleton.
```

It weakens:

```text
simple measure-anisotropy explanations of the few-percent residuals.
```

Remaining likely nonlinear correction channels:

```text
nonlinear boundary action weights;
gluing / Jacobian determinants;
branch coefficient normalization;
branch-specific q-flow / boundary layers.
```

## 148. Transfer gluing determinant audit

Implemented in `native_transfer_gluing_determinant_audit.py`.

Symmetric transfer gives:

```text
exp(-eta/2)
```

per one-sided node.

But a physical gluing measure may also contribute:

```text
determinant / Jacobian factors.
```

Schematic finite-dimensional Gaussian normalization:

```text
integral exp(-1/2 x^T A x) dx ~ (det A)^(-1/2)
```

At:

```text
eta = 1/18
```

unnormalized determinant factors can be large:

```text
rank-one Gaussian:
  eta^(-1/2) ~ 4.2426

rank-three Gaussian:
  eta^(-3/2) ~ 76.3675
```

Hundred-thirty-fourth verdict:

```text
gluing determinants are dangerous.
```

If kernels are normalized transfer operators:

```text
determinant factors cancel by convention;
gamma remains unchanged.
```

If the physical boundary path integral includes unnormalized Gaussian measures:

```text
determinant factors can dominate the ladder,
not merely correct it by a few percent.
```

Therefore:

```text
do not use determinant corrections until the exact boundary transfer
normalization is derived.
```

This moves determinant/RG ideas lower in priority for residuals unless a
canonical cancellation or finite normalized determinant is found.

## 149. Branch coefficient dependency audit

Implemented in `native_branch_coefficient_dependency_audit.py`.

The current few-percent residuals may live in coefficient normalization, not in
`eta`, `gamma`, or a new physical mechanism.

Current coefficient risks:

```text
cell normalization:
  M1:
    sets anchored compact branch amplitude.
  E1:
    sets E1/M1 coefficient ratio.
  status:
    open in typed graph.
  risk:
    old coefficient ratio may carry legacy approximation choices.
  required:
    normalize finite-cell action in n_a/projective variables.

shape-mode volume:
  M1:
    one compact/radial shape scalar per boundary.
  E1:
    two ordinary relative-shape scalars per boundary.
  status:
    node counts clarified; weight normalization open.
  risk:
    different shape volumes can move M1 and E1 in opposite directions.
  required:
    derive boundary measure per shape node after node-merge rules.

compact occupation weight:
  M1:
    direct selector/weight.
  E1:
    none.
  status:
    Pbundle0 still open.
  risk:
    can look like an M1 residual correction if fitted.
  required:
    find metric/interface reason for nontrivial primitive compact occupation.

ordinary endpoint resonance normalization:
  M1:
    indirect shared frame only.
  E1:
    direct selector/weight.
  status:
    p=1/3 resonance strong; normalization open.
  risk:
    can look like an E1 boost if fitted.
  required:
    derive E1 finite-cell normalization from endpoint resonance and H1 shape action.
```

Hundred-thirty-fifth verdict:

```text
The old M1/E1 coefficient ratio is provisional.
```

Coefficients must be recomputed after:

```text
typed graph;
Hopf merge;
q-flow;
transfer normalization.
```

This is currently the most plausible place for opposite-sign branch movement
without inventing a new mechanism.

## 150. q-flow source-running audit

Implemented in `native_q_flow_source_running.py`.

With the derived flow:

```text
dq/dt = q^2 - q + 2s(t)
```

a branch-specific effective source can shift the collar slope:

```text
q_phi0
```

without changing the basic fixed-point skeleton.

Baseline:

```text
s0 = 1/9
q0 = 1/3
```

Sample source-running effects:

```text
constant delta s = +0.005:
  q_phi0 = 0.360547271552
  delta q = +0.0272139382188

constant delta s = -0.005:
  q_phi0 = 0.30850833126
  delta q = -0.0248250020731

collar bump delta s = +0.02:
  q_phi0 = 0.370510077974
  delta q = +0.0371767446407

collar bump delta s = -0.02:
  q_phi0 = 0.298026064781
  delta q = -0.0353072685523
```

Diagnostic source values corresponding to residual-required collar slopes:

```text
M1 / mu-like:
  q_req = 0.387510439043
  fixed-source s_req = 0.118673049338
  delta s = +0.00756193822674

E1 / tau-like:
  q_req = 0.264116906769
  fixed-source s_req = 0.0971795831639
  delta s = -0.0139315279472
```

Hundred-thirty-sixth verdict:

```text
branch-specific effective source s(t) can shift q_phi0 with either sign.
```

Important locality result:

```text
collar-local source changes have stronger direct leverage on q_phi0 than
core-local bumps of the same size after outward attraction.
```

Discipline line:

```text
do not choose s(t) from observed masses.
derive s(t) from branch boundary data.
```

This gives the nonlinear search a sharper target:

```text
derive the branch-specific angular/interface source profile near the phi=0 collar.
```

## 151. Branch-specific source-sign requirements

Implemented in `native_branch_source_sign_requirements.py`.

This is diagnostic only.

Translate residual-required collar slopes into effective fixed-source shifts
using:

```text
s = q(1-q)/2
```

Baseline:

```text
s0 = 1/9
eta = 1/18
```

M1 / mu-like:

```text
q_required = 0.387510439043
s_required = 0.118673049338
delta_s = +0.00756193822674
delta_s / eta = +0.136114888081

sign needed:
  positive
```

Possible native interpretation:

```text
primitive compact boundary data could add positive collar source.
```

E1 / tau-like:

```text
q_required = 0.264116906769
s_required = 0.0971795831639
delta_s = -0.0139315279472
delta_s / eta = -0.25076750305

sign needed:
  negative
```

Possible native interpretation:

```text
ordinary relative-shape normalization could reduce effective collar source.
```

Hundred-thirty-seventh verdict:

```text
M1 wants a positive effective collar-source shift.
E1 wants a negative effective collar-source shift.
```

This sign split is compatible with an orchestra picture where:

```text
compact topology;
ordinary H1 shape weighting;
and interface source flow
```

affect the collar differently.

But:

```text
this is not a derivation.
the source profile must come from the nonlinear boundary action.
```

## 152. Source-sign physics filter

Implemented in `native_source_sign_physics_filter.py`.

The branch-specific source idea must respect native sign constraints.

Positive-definite source terms:

```text
positive angular-gradient energy;
positive compact U1 flux energy.
```

These can:

```text
raise q_phi0.
```

Therefore they are compatible with:

```text
M1 / mu-like:
  wants positive delta q / positive delta s.
```

But they are not compatible with:

```text
E1 / tau-like:
  wants negative delta q / negative delta s.
```

Possible sign-filtered roles:

```text
positive compact U1 flux energy:
  natural M1-positive source candidate if Pbundle0 is occupied.

node correlation entropy:
  possible M1 damping only;
  wrong direction for tau-like branch.

branch coefficient normalization:
  can move M1 and E1 in opposite directions without requiring negative
  angular energy.

subtraction / normalization of shape source:
  possible E1 q-lowering route only if derived as an effective baseline
  subtraction, not as negative physical energy.
```

Hundred-thirty-eighth verdict:

```text
Positive-definite angular/source physics can help the M1-required shift,
but not the E1-required shift.
```

Therefore:

```text
E1 / tau-like residual should first be sought in:

  coefficient normalization,
  normalized/subtracted boundary source definition,
  gluing normalization,
  or another branch-specific boundary effect,

not ordinary positive angular energy.
```

## 153. Unidentified metric-spawned mechanism second look

Implemented in `native_unidentified_mechanism_second_look.py`.

As the typed orchestra frame tightens, old negative results should be revisited.
They may only rule out older solo variables, not coupled metric mechanisms.

The second-look rule:

```text
do not import new forces;
revisit native metric structures that may act as mechanisms only in the
coupled orchestra.
```

Current candidates:

```text
phi0 boundary layer:
  sector:
    phi/interface.
  native content:
    finite cell matching, extrinsic curvature jump, tail cancellation.
  possible role:
    sets q_phi0;
    cancels exterior negative-mass tail;
    creates physical closure nodes.
  next probe:
    derive boundary layer source required for a_tail=0 and q_phi0=1/3.

angular-source running:
  sector:
    angular/phi coupling.
  native content:
    angular gradients supply 1/r^2 source shape;
    q-flow obeys dq/dt=q^2-q+2s(t).
  possible role:
    branch-specific collar source shifts and nonlinear endpoint softening.
  next probe:
    derive s(t) for M1 Hopf/projective and E1 ordinary H1 boundary data.

tail cancellation / global closure:
  sector:
    phi/global.
  native content:
    localized positive angular source creates exterior negative-mass tail
    unless canceled.
  possible role:
    global finite-cell quantization or closure condition.
  next probe:
    express a_tail as a boundary functional of typed nodes.

abelian Coulomb boundary energy:
  sector:
    phi-blind force.
  native content:
    Maxwell cancellation gives exact Coulomb form in the UDT metric.
  possible role:
    branch-selective interface energy or compact occupation pressure.
  next probe:
    compute finite-cell Coulomb boundary energy under primitive compact/topological closure.

compact bundle occupation obstruction:
  sector:
    topology/angular.
  native content:
    S2 x I supports integer line-bundle sectors;
    |n|=1 gives CP1=S2 bridge.
  possible role:
    forces or favors M1 primitive branch.
  next probe:
    search for boundary regularity/phase patching obstruction that excludes
    trivial-only closure.

angular determinant with fixed normalization:
  sector:
    angular measure.
  native content:
    round S2 Laplacian and finite-dimensional H1/shape kernels.
  possible role:
    finite normalized coefficient correction after graph is fixed.
  next probe:
    derive normalized determinant ratios from typed kernels, target-blind.

phi stiffness / matter-side C:
  sector:
    phi dynamics.
  native content:
    C1 action stiffness not fixed by macro gravity normalization.
  possible role:
    nonlinear back-reaction strength or finite-cell coefficient normalization.
  next probe:
    track whether C cancels in ratios or enters branch coefficient normalization.
```

Hundred-thirty-ninth verdict:

```text
The best hidden-mechanism candidates are not new SM-like forces.
They are boundary/interface/global-closure effects generated by the
phi-angular-topology orchestra.
```

Priority:

```text
1. phi0 boundary layer;
2. angular-source running;
3. global tail cancellation;
4. only then residual comparison.
```

## 154. phi0 boundary-layer requirements

Implemented in `native_phi0_boundary_layer_requirements.py`.

A finite matter cell needs two distinct boundary jobs:

```text
1. cancel the exterior negative-mass tail:
   a_tail -> 0

2. set or preserve the collar slope:
   q_phi0
```

At:

```text
R = 1
f(R) = 1
```

the inner collar slope is:

```text
f'_inside = -q
```

Flat exterior requires:

```text
f'_outside = 0
```

so the slope jump to flat is:

```text
q
```

and:

```text
Delta K R = q/2
eta = q/6
```

Hundred-fortieth verdict:

```text
tail cancellation and collar-slope setting are separate jobs.
```

Therefore:

```text
a boundary layer that only cancels a_tail need not preserve q=1/3;
a boundary layer that preserves q=1/3 need not cancel a_tail.
```

The hidden mechanism, if present, must couple both conditions:

```text
a_tail = 0
q_phi0 controlled by H1/interface data
```

This reframes the phi0 layer:

```text
not a hard wall;
not an arbitrary cutoff;
but a coupled matching object tying global tail cancellation to local
H1/interface slope.
```

## 155. Tail / slope relation audit

Implemented in `native_tail_slope_relation_audit.py`.

For the exterior vacuum branch near `R=1`:

```text
f_out = 1 + a/r
```

the exterior logarithmic slope is:

```text
q_out = -R f'_out / f_out
      = a/(R+a)
```

So:

```text
flat exterior:
  a = 0
  q_out = 0
```

But the eta route needs:

```text
interior q_phi0 = 1/3
```

Hundred-forty-first verdict:

```text
nonzero eta and zero exterior tail require a genuine interface layer.
```

Smooth matching to a flat exterior would impose:

```text
q_phi0 -> 0
eta -> 0
```

Therefore the phi0 boundary layer is not optional in the current rebuild.

It must supply:

```text
slope jump:
  q_inside != q_outside

tail cancellation:
  a_tail,outside = 0

boundary scalar:
  Delta K R = q_inside/2
```

This upgrades the phi0 layer from:

```text
convenient finite-cell closure
```

to:

```text
necessary carrier of the eta-producing interface jump.
```

## 156. phi0 shell-stress signature

Implemented in `native_phi0_shell_stress_signature.py`.

For flat exterior and inner collar slope:

```text
f'_inside(R) = -q/R
```

the extrinsic-curvature jump at `R=1` is:

```text
[K^a_b] = diag(q/2, 0, 0)
```

in shell directions:

```text
(t, theta, phi)
```

The trace is:

```text
[K] = q/2
```

The trace-reversed bracket that appears in the shell stress is:

```text
[K^a_b] - delta^a_b [K]
  = (0, -q/2, -q/2)
```

For the self-similar eta collar:

```text
q = 1/3

[K^a_b] - delta^a_b [K]
  = (0, -1/6, -1/6)
```

Hundred-forty-second verdict:

```text
The eta-producing interface jump has an angular/tension-like shell signature.
```

It is:

```text
not a radial Coulomb tail;
not smooth vacuum matching;
not an arbitrary hard wall.
```

It is compatible with:

```text
an H1/angular boundary layer on the S2 interface.
```

This is an important second-look result:

```text
the metric itself points the missing phi0 mechanism toward angular/interface
stress.
```

## 157. Interface stress-source catalog

Implemented in `native_interface_stress_source_catalog.py`.

The target metric jump has shell-direction pattern:

```text
(t, theta, phi):

[K^a_b] - delta^a_b[K]
  = (0, -q/2, -q/2)
```

This matters because not every angular-looking source has this signature.

Candidate source signatures:

```text
ordinary surface tension / domain wall:
  pattern:
    nonzero time component and nonzero angular components.
  match:
    poor, unless derived as a special UDT boundary term.

static angular gradient field on shell:
  pattern:
    energy density plus angular stresses, generally anisotropic.
  match:
    partial; would need averaging/subtraction.

round-S2 curvature / boundary functional:
  pattern:
    zero or topological time component, isotropic angular component.
  match:
    best structural match.

trace-subtracted H1 boundary kernel:
  pattern:
    zero time component, isotropic angular component.
  match:
    good if kernel is a constraint stress rather than material energy.

radial Coulomb / Maxwell tail:
  pattern:
    radial/electric stress pattern.
  match:
    poor for the phi0 angular shell target.
```

Hundred-forty-third verdict:

```text
The phi0 layer looks more like a metric boundary/corner constraint
or trace-subtracted angular interface kernel than ordinary shell matter.
```

Therefore:

```text
do not model the missing interface as a generic material wall force.
derive it from the boundary variational principle.
```

This preserves the second-look lesson:

```text
the metric may spawn a mechanism here,
but it may not look like a familiar force.
```

## 158. Boundary functional stress audit

Implemented in `native_boundary_functional_stress_audit.py`.

Target:

```text
angular-only phi0 interface stress with no time component.
```

Candidate boundary functionals:

```text
area term on timelike shell:
  variation:
    proportional to full induced metric h_ab.
  match:
    poor; includes time component.
  risk:
    imports wall-like mechanism.

S2 area term only:
  variation:
    angular metric variation only.
  match:
    good angular pattern.
  risk:
    must explain why time direction is excluded.

Gibbons-Hawking-York / extrinsic curvature term:
  variation:
    cancels normal derivative variations and yields Brown-York-like stress.
  match:
    promising but needs exact UDT/C1 analogue.
  risk:
    may cancel rather than create the jump if used with smooth matching.

corner / joint term at phi0 collar:
  variation:
    localized where radial cell and S2 boundary meet.
  match:
    strong candidate for angular-only interface action.
  risk:
    must derive UDT joint term, not borrow GR blindly.

intrinsic S2 curvature integral:
  variation:
    topological in 2D for fixed topology.
  match:
    weak for local stress; useful for topology/selection.

H1 trace constraint action:
  variation:
    trace-subtracted angular projector stress.
  match:
    good if derived from constraint variation.
  risk:
    conditional until derived.
```

Hundred-forty-fourth verdict:

```text
Full shell tension is the wrong shape.
Pure S2 topology is probably too inert.
```

Best second-look targets:

```text
1. UDT/C1 boundary or joint term at phi0;
2. S2-only interface action;
3. derived H1 trace-constraint action.
```

These are:

```text
metric boundary mechanisms,
not conventional forces.
```

## 159. C1 phi0 boundary conjugate

Implemented in `native_c1_phi0_boundary_conjugate.py`.

The C1 radial density in:

```text
f = e^{-2phi}
```

is:

```text
L = (1/4) r^2 f'^2
```

Its variation gives the boundary term:

```text
Pi_f delta f
```

with:

```text
Pi_f = (1/2) r^2 f'
```

At the `phi0` collar:

```text
R = 1
f = 1
f' = -q
```

so:

```text
Pi_f = -q/2
```

For the self-similar eta collar:

```text
q = 1/3
Pi_f = -1/6
```

To make the finite-cell variational problem well-posed with free boundary
variation, a boundary functional must satisfy:

```text
dS_boundary/df = -Pi_f = q/2
```

Hundred-forty-fifth verdict:

```text
nonzero q means the C1 action carries nonzero canonical boundary momentum.
```

Therefore the `phi0` mechanism may be:

```text
the conjugate boundary functional that cancels the C1 boundary momentum
and makes the constrained phi0 endpoint physical.
```

This is a strong native candidate because:

```text
its derivative scale is q/2,
the same scale as the extrinsic-curvature jump.
```

So the missing layer may not be a force at all.

It may be:

```text
a metric variational boundary mechanism.
```

## 160. Boundary momentum H1 projection

Implemented in `native_boundary_momentum_h1_projection.py`.

The C1 boundary conjugate scale at `phi0` is:

```text
-Pi_f = q/2
```

The round S2/H1 projection is:

```text
<n_a n_b> = delta_ab / 3
```

Therefore the projected unit is:

```text
eta(q) = (q/2) / 3
       = q/6
```

and the one-sided transfer weight is:

```text
eta(q)/2 = q/12
```

For the self-similar collar:

```text
q = 1/3

-Pi_f = 1/6
eta = 1/18
eta/2 = 1/36
```

Hundred-forty-sixth verdict:

```text
eta can be interpreted as the H1 projection of the C1 boundary canonical
momentum at phi0.
```

This unifies:

```text
extrinsic jump view:
  Delta K R = q/2

action variation view:
  -Pi_f = q/2

H1 projection:
  eta = q/6

symmetric transfer:
  eta/2 = q/12
```

Current best hidden-mechanism chain:

```text
C1 boundary momentum
  -> phi0 conjugate boundary functional
  -> S2/H1 isotropic projection
  -> eta
  -> one-sided transfer
```

This is a metric variational boundary mechanism, not a conventional force.

## 161. No-approximation reset for the boundary functional

Implemented in `native_exact_c1_boundary_identities.py`.

The previous toy Hessian modeling path is discarded.  The next stage should use
only:

```text
exact metric identities;
exact variational identities;
or explicitly open derivation gaps.
```

Exact C1 identity:

```text
f = exp(-2 phi)

sqrt(-g) e^(-2phi) g^rr phi'^2
  = r^2 e^(-4phi) phi'^2
  = (1/4) r^2 f'^2
```

Exact boundary variation:

```text
delta S_C1 boundary
  = [(1/2) r^2 f' delta f]_boundary

Pi_f = (1/2) r^2 f'
```

At the `phi0` collar:

```text
R = 1
f = 1
f' = -q

Pi_f = -q/2
dS_boundary/df = -Pi_f = q/2
```

For the exact self-similar value:

```text
q = 1/3

Pi_f = -1/6
-Pi_f = 1/6
H1/S2 projection = (1/6)/3 = 1/18
one-sided transfer = 1/36
```

Exact shell jump identity for flat exterior:

```text
[K^a_b] = diag(q/2, 0, 0)
[K] = q/2

[K^a_b] - delta^a_b[K]
  = (0, -q/2, -q/2)
```

Hundred-forty-seventh verdict:

```text
The boundary momentum / shell-jump / H1-projection chain is exact for the
stated metric ansatz and collar data.
```

Remaining open items are not to be approximated:

```text
derive the phi0 boundary functional;
derive the typed closure kernel from that functional;
derive branch coefficients from that same exact structure.
```

## 162. Boundary functional two-condition audit

Implemented in `native_boundary_functional_two_conditions.py`.

A real `phi0` mechanism must handle two conditions:

```text
1. value / global condition:
   exterior tail a_tail = 0

2. derivative / local condition:
   boundary momentum Pi_f = -q/2
```

Simple closures fail:

```text
Dirichlet wall f=1:
  fixes f at phi0;
  does not dynamically cancel Pi_f;
  cancels tail only if flat exterior is imposed.

Neumann smooth flat match:
  sets Pi_f=0;
  can cancel tail;
  kills q and therefore eta.
```

The needed object is:

```text
conjugate phi0 boundary functional.
```

It must do both:

```text
value condition:
  encode exterior flat/tail cancellation.

derivative condition:
  dS_boundary/df = q/2,
  canceling the C1 boundary momentum.
```

Hundred-forty-seventh verdict:

```text
Dirichlet and smooth Neumann closures each do only half the job.
```

The orchestra form is:

```text
global closure functional of typed nodes:
  value:
    a_tail[nodes] = 0

  derivative:
    variation gives node-level momentum constraints

  H1 projection:
    q/2 -> eta
```

This is the cleanest current statement of the missing mechanism:

```text
a two-condition metric boundary functional at phi0.
```

## 163. Typed nodes as boundary-functional variables

Implemented in `native_typed_nodes_boundary_functional.py`.

The typed closure graph can be reinterpreted as the variable set of the `phi0`
two-condition boundary functional.

Node classes:

```text
shared H1 frame nodes:
  M1 count = 3
  E1 count = 3

  value role:
    orient closure so a_tail functional can vanish in H1-projected sectors.

  derivative role:
    project C1 boundary momentum q/2 into eta=q/6.

core-side shape nodes:
  M1 count = 1
  E1 count = 2

  value role:
    encode how endpoint/source data contribute to a_tail.

  derivative role:
    supply variation of a_tail with respect to core-side shape.

phi0-side shape nodes:
  M1 count = 1
  E1 count = 2

  value role:
    encode collar/source data needed for a_tail=0.

  derivative role:
    supply variation of boundary functional with respect to collar shape.
```

Totals:

```text
M1:
  3 + 1 + 1 = 5

E1:
  3 + 2 + 2 = 7
```

Hundred-forty-eighth verdict:

```text
The typed closure graph is no longer just bookkeeping.
It is a candidate coordinate system for the phi0 boundary functional.
```

In this frame:

```text
a_tail = 0:
  value equation.

q/2 projection:
  derivative / momentum equation.

factorization:
  claim about the Hessian or transfer kernel of the boundary functional
  in typed node variables.
```

Next derivation target:

```text
derive the phi0 boundary functional in these variables and compute whether
its kernel factorizes into rank-one H1/projective closure nodes.
```

## 164. Exact radial C1 Hamilton-Jacobi / tail relation

Implemented in `native_exact_radial_hj_tail_relation.py`.

For source-free radial C1 in:

```text
f = e^{-2phi}
```

the action is:

```text
S = (1/4) integral r^2 f'^2 dr
```

The Euler-Lagrange equation is:

```text
(r^2 f')' = 0
```

with exact solution:

```text
f(r) = A + B/r
```

The canonical boundary momentum is:

```text
Pi_f = (1/2) r^2 f'
     = -B/2
```

Therefore:

```text
B = -2 Pi_f
```

At a collar `R` with:

```text
f(R) = 1
q = -R f'(R)/f(R)
```

we have:

```text
f'(R) = -q/R
B = q R
Pi_f = -q R/2
```

For:

```text
R = 1
q = 1/3
```

the exact chain is:

```text
B = 1/3
Pi_f = -1/6
H1 projection (-Pi_f)/3 = 1/18
```

Hundred-forty-ninth verdict:

```text
In source-free C1 radial evolution, the vacuum-tail coefficient and the
boundary momentum are the same integration constant.
```

Therefore:

```text
q != 0
and
a_out = 0
```

cannot be joined by a smooth source-free continuation.

No-approximation conclusion:

```text
the phi0 interface layer is required if eta is nonzero and the exterior is flat.
```

## 165. Exact interface momentum jump

Implemented in `native_exact_interface_momentum_jump.py`.

The C1 canonical momentum is:

```text
Pi_f = (1/2) r^2 f'
```

At `phi0`:

```text
R = 1
f = 1
```

with inner collar:

```text
f'_inside = -q
```

and flat exterior:

```text
f'_outside = 0
```

we get:

```text
Pi_inner = -q/2
Pi_outer = 0
```

Therefore the exact canonical momentum jump is:

```text
Delta Pi = Pi_outer - Pi_inner
         = q/2
```

For:

```text
q = 1/3
```

this gives:

```text
Delta Pi = 1/6
H1-projected Delta Pi = 1/18
one-sided transfer = 1/36
```

Hundred-fiftieth verdict:

```text
The phi0 interface mechanism is exactly a C1 canonical momentum-jump carrier.
```

This is now the exact target:

```text
derive the H1/S2 boundary functional whose variation carries
Delta Pi = q/2.
```

## 166. phi0 boundary functional exact requirements

Implemented in `native_phi0_boundary_functional_requirements.py`.

These are requirements, not an approximate model.

A candidate `phi0` boundary functional must satisfy or explicitly replace:

```text
value closure:
  exact condition:
    a_tail,outside = 0
  reason:
    finite matter cell must not leave exterior negative-mass tail.
  failure:
    object has long-range negative-mass tail, not a closed particle cell.

momentum jump:
  exact condition:
    Delta Pi_f = Pi_outer - Pi_inner = q/2
  reason:
    nonzero eta with flat exterior requires C1 boundary momentum jump.
  failure:
    smooth flat matching forces q=0 and eta=0.

H1 projection:
  exact condition:
    Delta Pi_f <n_a n_b> = (q/6) delta_ab
  reason:
    round S2/H1 projection turns scalar boundary momentum into eta.
  failure:
    no derived eta transfer unit.

self-similar fixed collar:
  exact condition:
    q = 1/3 for the base finite-action H1 source.
  reason:
    gives eta=1/18 and follows from constant-source q-flow if s=1/9.
  failure:
    eta becomes q/6 and branch/source running must be derived.

typed node variables:
  exact condition:
    functional variables are shared H1 frame nodes plus branch shape nodes.
  reason:
    connects closure graph to variational structure.
  failure:
    depth count remains bookkeeping.

factorized kernel:
  exact condition:
    kernel factorization must be derived exactly, not assumed.
  reason:
    gamma^k requires independent rank-one H1/projective closure factors.
  failure:
    node entropy collapses or becomes coefficient/determinant problem.
```

Hundred-fifty-first verdict:

```text
A candidate phi0 boundary functional is not acceptable unless it satisfies
these exact conditions or explicitly replaces one with a derived alternative.
```

This is the current no-approximation checklist for the hidden metric mechanism.

## 167. Exact exterior Hamilton-Jacobi no-go

Implemented in `native_exact_exterior_hj_no_go.py`.

Consider the source-free exterior C1 problem:

```text
S_ext = (1/4) integral_R^infty r^2 f'^2 dr
```

with:

```text
f(R) = F
f(infinity) = 1
```

The exact solution is:

```text
f(r) = 1 + B/r
B = R(F - 1)
```

The exact on-shell action is:

```text
S_ext(F;R) = B^2/(4R)
           = R(F - 1)^2/4
```

Its boundary derivative is:

```text
dS_ext/dF = R(F - 1)/2
          = B/2
```

The exterior canonical momentum at `R` is:

```text
Pi_out = (1/2) R^2 f'(R)
       = -B/2
```

so:

```text
dS_ext/dF = -Pi_out
```

For flat exterior:

```text
F = 1
B = 0
S_ext = 0
dS_ext/dF = 0
```

But the self-similar inner collar needs:

```text
q = 1/3
-Pi_inner = q/2 = 1/6
```

Hundred-fifty-second verdict:

```text
The flat exterior Hamilton-Jacobi functional cannot cancel a nonzero inner
C1 boundary momentum.
```

Therefore:

```text
the eta-producing phi0 momentum jump is not hidden in smooth exterior closure.
```

It requires:

```text
an additional interface functional,
or an exactly derived replacement for flat exterior closure.
```

## 168. Exact distributional interface source

Implemented in `native_exact_distributional_interface_source.py`.

The C1 radial field equation in `f` can be written:

```text
(r^2 f')' = J(r)
```

Integrate across a thin `phi0` interface at `R`:

```text
[r^2 f']_out-in = integral J(r) dr
```

In canonical momentum:

```text
Pi_f = (1/2) r^2 f'
```

so:

```text
Delta Pi_f = Pi_out - Pi_in
           = (1/2) integral J(r) dr
```

For flat exterior and inner:

```text
f'_inside = -q/R
```

at `R=1`:

```text
Pi_in = -q/2
Pi_out = 0
Delta Pi_f = q/2
integral J dr = q
```

For the self-similar collar:

```text
q = 1/3

Delta Pi_f = 1/6
interface source integral = 1/3
H1-projected Delta Pi_f = 1/18
```

Hundred-fifty-third verdict:

```text
Any phi0 boundary functional that creates the eta-producing jump is equivalent,
in the radial C1 equation, to a distributional interface source with integrated
strength q.
```

Important:

```text
the H1/S2 projection acts on Delta Pi_f = q/2,
not directly on J = q.
```

Exact target for a candidate mechanism:

```text
produce integrated interface source q
and carry canonical momentum jump q/2
with the angular shell signature already derived.
```

## 169. Exact boundary functional accept/reject audit

Implemented in `native_exact_boundary_functional_accept_reject.py`.

A candidate `phi0` functional must supply:

```text
dS/df = q/2
```

or an exact derived replacement.

Candidate status:

```text
pure intrinsic S2 curvature integral:
  depends on f:
    no, for fixed round S2 topology/radius.
  supplies dS/df:
    no.
  exact status:
    reject as local momentum-jump source;
    useful only for topology/selection.

pure S2 area at fixed R:
  depends on f:
    no if R and angular metric are fixed independently of f.
  supplies dS/df:
    no.
  exact status:
    reject unless exact f-coupling is derived.

timelike shell area/tension:
  depends on f:
    yes through induced time metric sqrt(f).
  supplies dS/df:
    yes.
  exact status:
    wrong stress signature unless trace-subtracted or specially derived.

C1 conjugate boundary functional:
  depends on f:
    yes by definition.
  supplies dS/df:
    yes, must give q/2 at f=1.
  supplies tail value:
    yes if value condition encodes a_tail=0.
  exact status:
    acceptable target, not yet derived.

H1 trace-projected conjugate functional:
  depends on f:
    yes through C1 boundary momentum and H1 projection.
  supplies dS/df:
    projected derivative eta=q/6.
  supplies tail value:
    possible if tied to typed closure nodes.
  exact status:
    best exact target, still to derive.
```

Hundred-fifty-fourth verdict:

```text
Pure S2 topology or fixed-area terms cannot carry the C1 momentum jump unless
an exact f-coupling is derived.
```

The remaining target is:

```text
C1 conjugate / H1 trace-projected boundary functional.
```

Not:

```text
generic geometric area term;
generic material wall;
pure angular topology alone.
```

## 170. Exact local phi0 boundary form

Implemented in `native_exact_local_boundary_form.py`.

Let:

```text
F = f(phi0)
```

A differentiable boundary functional:

```text
S_b(F, nodes)
```

that cancels the C1 inner momentum must satisfy, at:

```text
F = 1
```

the exact first-variation condition:

```text
dS_b/dF = q/2
```

Therefore:

```text
delta S_b = (q/2) delta F
```

at the collar.

Equivalently, every acceptable boundary functional has local form:

```text
S_b(F, nodes)
  = S_b(1, nodes)
    + (q/2)(F - 1)
    + terms with zero first F-derivative at F=1.
```

For:

```text
q = 1/3
```

this gives:

```text
dS_b/dF = 1/6
H1-projected derivative = 1/18
```

If the `H1/projective` unit vector carries the boundary observable:

```text
delta S_b,ab = (q/2) n_a n_b delta F
```

and exact round-S2 averaging gives:

```text
<delta S_b,ab> = (q/6) delta_ab delta F
```

Hundred-fifty-fifth verdict:

```text
The local momentum-carrying part of the phi0 functional is fixed by its
first derivative.
```

But this does not determine:

```text
S_b(1, nodes)
```

which is where:

```text
a_tail = 0
```

must enter.

No-approximation conclusion:

```text
local momentum closure and global tail closure are exactly distinct pieces
of the phi0 boundary functional.
```

## 171. Exact scale-normalized boundary momentum

Implemented in `native_exact_scale_normalized_boundary_momentum.py`.

At a collar of radius `R` with:

```text
f(R) = 1
q = -R f'(R)/f(R)
```

we have:

```text
f'(R) = -q/R
```

The C1 boundary momentum is:

```text
Pi_f = (1/2) R^2 f'(R)
     = -q R/2
```

So raw `Pi_f` is scale-covariant.

The dimensionless collar momentum is:

```text
pi_hat = -Pi_f/R
       = q/2
```

The H1 projection uses this dimensionless quantity:

```text
eta(q) = pi_hat/3
       = q/6
```

For:

```text
q = 1/3
```

the exact dimensionless chain is:

```text
pi_hat = 1/6
eta = 1/18
one-sided transfer = 1/36
```

Hundred-fifty-sixth verdict:

```text
Setting R=1 is a dimensionless cell normalization.
```

The invariant transfer unit is built from:

```text
-Pi_f/R = q/2
```

not the raw scale-covariant `Pi_f`.

This preserves:

```text
scale covariance of the mass-ratio ladder.
```

## 172. Exact C1 variational options at phi0

Implemented in `native_exact_c1_variational_options.py`.

The bare C1 action has exact variation:

```text
delta S_C1 = bulk term + [Pi_f delta f]_boundary
Pi_f = (1/2) r^2 f'
```

At the `phi0` collar with:

```text
R = 1
f = 1
f' = -q
```

we have:

```text
Pi_f = -q/2
```

Existing C1 variational choices:

```text
Dirichlet boundary:
  delta f = 0 at phi0.
  nonzero Pi_f is allowed.
  But f=1 is imposed as a boundary condition, not derived.

Natural/free boundary:
  delta f is free at phi0.
  stationarity requires Pi_f = 0.
  Therefore q = 0.

Added boundary functional:
  stationarity requires Pi_f + dS_b/df = 0.
  nonzero q is possible if dS_b/df = q/2.
  But S_b is not present in bare C1 unless derived elsewhere.
```

For:

```text
q = 1/3
```

the requirement is:

```text
Pi_f = -1/6
dS_b/df = 1/6
```

Hundred-fifty-seventh verdict:

```text
Bare C1 alone gives either imposed Dirichlet phi0 data with nonzero momentum,
or natural Neumann data with q=0.
```

It does not derive:

```text
nonzero-q phi0 closure with flat exterior.
```

Therefore:

```text
the phi0 boundary functional remains an open requirement unless found in
another already-native metric/interface term.
```

## 173. Exact Maxwell / phi0 mismatch audit

Implemented in `native_exact_maxwell_phi0_mismatch.py`.

Purpose:

```text
prevent the real abelian force from being mistaken for the eta-producing
phi0 boundary mechanism.
```

Static radial Maxwell/Coulomb:

```text
exact metric fact:
  sqrt(-g) g^rr g^tt is phi-independent,
  giving the flat Coulomb equation.

can supply Delta Pi_f:
  not as a localized phi0 shell unless a surface charge layer is added.

stress signature:
  bulk radial electric/magnetic stress,
  not angular-only trace-reversed shell.

verdict:
  real metric-given force,
  wrong carrier for eta-producing phi0 jump.
```

Surface charge sheet at `phi0`:

```text
exact metric fact:
  would create Maxwell field discontinuity by Gauss law.

can supply Delta Pi_f:
  only if coupled to f boundary momentum by an additional rule.

verdict:
  added charged shell, not currently native.
```

H1 angular/interface boundary:

```text
exact metric fact:
  round S2 projection and C1 boundary momentum share the phi0 collar.

can supply Delta Pi_f:
  target remains q/2.

stress signature:
  angular/interface trace-reversed signature.
```

Hundred-fifty-eighth verdict:

```text
Maxwell/Coulomb remains a real metric-given sector,
but it does not automatically supply the C1 phi0 momentum jump.
```

Therefore:

```text
treat Maxwell as a possible later orchestra instrument,
not the derived boundary mechanism.
```

## 174. GR metric-corpus second look

Implemented in `native_gr_metric_corpus_second_look.py`.

The UDT metric is close enough in form to GR metric geometry that the GR
mathematical corpus is a valuable atlas.

But the guardrail is strict:

```text
Use GR boundary and metric mathematics as a map.
Do not import Einstein matter-sourcing as the mechanism.
```

Relevant GR-derived tools:

```text
Israel junction conditions:
  already useful.
  Exact thin-interface bookkeeping for jumps in extrinsic curvature.
  UDT use: metric jump algebra only, not Einstein matter sourcing.

ADM / Schwarzschild tail mass:
  already useful.
  The 1/r tail coefficient is a conserved radial integration constant.
  UDT use: tail/momentum diagnostic, not ordinary sourced mass.

Gibbons-Hawking-York boundary term:
  promising target.
  A metric variational principle generally needs boundary completion.
  UDT test: find the native boundary completion, if any.

Brown-York quasilocal stress:
  promising target.
  Organizes boundary energy, pressure, and momentum on finite S2 collars.
  UDT test: derive quasilocal quantities from C1/angular terms, not from EH import.

Corner / joint terms:
  high-priority target.
  Codimension-2 terms appear where boundary pieces meet.
  UDT test: phi0 may be a collar joint where radial negative-phi data
  meets angular S2 data.

Gauss-Codazzi constraints:
  promising target.
  Relate intrinsic S2 curvature, extrinsic curvature, and boundary constraints.
  UDT test: search for a missing angular scalar/constraint.

Mixed Robin boundary conditions:
  already useful.
  Classifies nonzero phi0 slope as a conjugate boundary condition.
  UDT test: classification is not derivation.

Covariant phase space / edge modes:
  promising target.
  Boundary degrees of freedom can appear when metric/gauge symmetries meet a boundary.
  UDT test: H1 nodes may be edge variables only if their symplectic role is derived.

Horizon and trapped-surface mechanics:
  mostly diagnostic.
  phi0 has f=1, not a horizon.

Domain walls / branes:
  import risk.
  Thin-shell language is useful, but wall dynamics are not native unless derived.

Linearized perturbation theory:
  diagnostic only.
  It can guide brainstorming, but not final conclusions.
```

Hundred-fifty-ninth verdict:

```text
The GR corpus points most strongly toward boundary mathematics,
not toward a new bulk force.
```

The best search targets are:

```text
1. variational completion,
2. quasilocal boundary momentum,
3. junction stress,
4. corner/joint terms,
5. possible edge modes.
```

This fits the current exact result:

```text
Bare C1 has the right boundary momentum variable,
but not yet the native boundary functional that fixes it.
```

So the GR-corpus pass sharpens the open problem:

```text
Find the UDT-native phi0 boundary/joint/edge term, if it exists.
```

## 175. GR atlas: Robin / joint audit for phi0

Implemented in `native_gr_robin_joint_audit.py`.

The exact C1 boundary variation is:

```text
delta S_C1 = bulk + [Pi_f delta f]
Pi_f = (1/2) R^2 f'(R)
```

At phi0:

```text
f(R) = 1
q = -R f'(R)/f(R)
Pi_f = -q R/2
```

The scale-normalized conjugate is:

```text
-Pi_f/R = q/2
```

Robin/mixed-boundary classification says:

```text
nonzero q with free delta f requires a boundary functional B.
```

Stationarity gives:

```text
Pi_f + partial B/partial f = 0
```

Therefore:

```text
partial B/partial f = q R/2
```

For the current H1 target:

```text
q = 1/3
-Pi_f/R = 1/6
eta = (q/2)/3 = 1/18
one-sided transfer = 1/36
```

The GR atlas suggests a sharper native target:

```text
A phi0 joint/edge term would be localized at the collar where
the radial negative-phi region and angular S2 data meet.
```

It must:

```text
1. supply partial B/partial f = q R/2,
2. preserve flat exterior a_tail,outside = 0,
3. project through the H1/S2 factor exactly as eta = q/6,
4. derive q or the source fixing q, not assume it,
5. avoid importing Einstein-Hilbert, wall, or brane dynamics.
```

Hundred-sixtieth verdict:

```text
Robin language identifies the exact missing mathematical role.
```

It does not derive:

```text
B
q
the typed H1 variables
the kernel factorization
```

The strongest next search is therefore:

```text
look for a native UDT joint/edge term whose variation supplies
the phi0 boundary momentum.
```

## 176. GR curvature diagnostic for a phi0 slope jump

Implemented in `native_gr_curvature_phi0_distribution.py`.

For the metric form:

```text
ds^2 = -f dt^2 + f^-1 dr^2 + r^2 dOmega^2
```

the exact GR curvature identities are:

```text
G^t_t = G^r_r = (r f' + f - 1)/r^2
G^theta_theta = G^phi_phi = f''/2 + f'/r
R = -f'' - 4 f'/r + 2(1-f)/r^2
```

These are used here as metric curvature identities, not as Einstein
matter-source equations.

At a phi0 collar:

```text
f(R) = 1
f'_in = -q/R
f'_out = 0
Delta f' = f'_out - f'_in = q/R
```

Therefore the derivative discontinuity gives:

```text
f'' contains (q/R) delta(r-R)
```

So the singular curvature pieces are:

```text
R_singular contains -(q/R) delta(r-R)
G^theta_theta_singular contains (q/(2R)) delta(r-R)
```

The exact C1 interface source is:

```text
(r^2 f')' = J
integral J dr = R^2 Delta f' = q R
Delta Pi_f = (1/2) integral J dr = q R/2
```

Now compare the curvature measure:

```text
integral r^2 R_singular dr = -q R
```

Thus:

```text
|integral r^2 R_singular dr| = |integral J dr| = q R
```

and:

```text
Delta Pi_f = q R/2
```

For:

```text
q = 1/3
```

this gives:

```text
integral J dr = R/3
Delta Pi_f = R/6
Delta Pi_f/R = 1/6
eta = 1/18
```

Hundred-sixty-first verdict:

```text
GR curvature math points to the phi0 slope jump itself as an exact
distributional boundary object.
```

This does not derive:

```text
the boundary action
the preferred value q = 1/3
the H1 typed variables
```

But it changes the target from:

```text
invent a mechanism that creates the jump
```

to:

```text
check whether the UDT metric/action already assigns a native joint or
curvature weight to the slope jump.
```

This is currently the best GR-corpus clue.

## 177. Einstein-Hilbert total-boundary diagnostic

Implemented in `native_eh_total_boundary_diagnostic.py`.

For:

```text
ds^2 = -f dt^2 + f^-1 dr^2 + r^2 dOmega^2
```

we have:

```text
sqrt(-g) = r^2 sin(theta)
R = -f'' - 4 f'/r + 2(1-f)/r^2
```

Suppressing angular/time factors, the radial Einstein-Hilbert density is:

```text
L_EH = r^2 R
     = -r^2 f'' - 4 r f' + 2(1-f)
```

This is exactly:

```text
L_EH = d/dr [2 r (1-f) - r^2 f']
```

So in the restricted UDT metric sector:

```text
the GR scalar-curvature action is boundary-only.
```

At phi0:

```text
f(R) = 1
B_EH(phi0) = -R^2 f'(R)
            = q R
```

Compare the C1 conjugate:

```text
Pi_f = (1/2) R^2 f'(R)
-2 Pi_f = -R^2 f'(R) = q R
```

For flat exterior:

```text
Delta Pi_f = q R/2
```

For:

```text
q = 1/3
```

this gives:

```text
B_EH(phi0) = R/3
-Pi_f = R/6
-Pi_f/R = 1/6
eta = 1/18
```

Hundred-sixty-second verdict:

```text
In this metric sector, GR's scalar-curvature action identifies the same
collar quantity as C1:

B_EH = -2 Pi_f.
```

This is a strong mathematical clue because:

```text
1. the action collapses to the boundary,
2. the boundary quantity is exactly the phi0 slope jump quantity,
3. the scale behavior is q R, matching the C1 interface source integral,
4. the C1 transfer uses the half-conjugate Pi_f.
```

But it is not yet a derivation, because:

```text
UDT cannot simply import the Einstein-Hilbert action as the mass mechanism.
```

The refined native question is:

```text
Did the UDT reduction discard or quarantine a native curvature/joint boundary
term that should participate in the phi0 closure?
```

This is the most concrete fruit from the GR-corpus second look so far.

## 178. GHY / Dirichlet cancellation audit

Implemented in `native_ghy_dirichlet_cancellation_audit.py`.

The previous section used the raw Einstein-Hilbert scalar-curvature
primitive:

```text
B_EH = 2R(1-f) - R^2 f'
```

That raw primitive sees the phi0 slope.

But standard GR does not use the raw scalar-curvature action as a
well-posed Dirichlet metric variational principle. It adds the
Gibbons-Hawking-York boundary term.

For the timelike `r=R` boundary:

```text
n^r = sqrt(f)
K = 2 sqrt(f)/R + f'/(2 sqrt(f))
sqrt(|h|) = sqrt(f) R^2 sin(theta)
```

Suppressing angular/time factors:

```text
sqrt(|h|) K = 2 R f + (R^2 f')/2
2 sqrt(|h|) K = 4 R f + R^2 f'
```

Therefore the Dirichlet-completed boundary combination is:

```text
B_EH + 2 sqrt(|h|)K
  = [2R(1-f) - R^2 f'] + [4Rf + R^2 f']
  = 2R(1+f)
```

At phi0:

```text
f = 1
B_EH + 2K term = 4R
flat reference value = 4R
subtracted value = 0
```

Hundred-sixty-third verdict:

```text
The raw EH total derivative sees the phi0 slope.
Standard Dirichlet EH+GHY completion cancels that slope dependence.
```

So:

```text
ordinary GR Dirichlet boundary completion at f=1 does not derive eta.
```

This is not a failure of the GR-corpus pass. It is a useful narrowing:

```text
the eta-producing boundary momentum, if native, must behave like a
mixed/Neumann/joint/edge contribution, not like standard Dirichlet
EH+GHY quasilocal energy.
```

## 179. Brown-York phi0 boundary-stress audit

Implemented in `native_brown_york_phi0_stress_audit.py`.

The Dirichlet-completed action value cancels the raw `f'` dependence at
`f=1`, but the boundary stress is a variation with respect to the induced
boundary metric. That is a different diagnostic.

For the timelike `r=R` boundary:

```text
K^t_t = f'/(2 sqrt(f))
K^theta_theta = K^phi_phi = sqrt(f)/R
K = f'/(2 sqrt(f)) + 2 sqrt(f)/R
```

Trace-reversed boundary curvature:

```text
K^a_b - K delta^a_b
```

has components:

```text
t component       = -2 sqrt(f)/R
angular component = -f'/(2 sqrt(f)) - sqrt(f)/R
```

Flat reference subtraction gives the Brown-York-type stress structure:

```text
tau^t_t proportional to 2(1 - sqrt(f))/R
tau^A_A proportional to -f'/(2 sqrt(f)) + (1 - sqrt(f))/R
```

At phi0:

```text
f = 1
f' = -q/R
```

therefore:

```text
tau^t_t = 0
tau^A_A proportional to q/(2R)
```

The dimensionless angular boundary-stress unit is:

```text
R tau^A_A -> q/2
```

For:

```text
q = 1/3
```

this gives:

```text
R tau^A_A -> 1/6
H1/S2 projected eta = (q/2)/3 = 1/18
```

Hundred-sixty-fourth verdict:

```text
Brown-York stress separates boundary value from boundary variation.
```

At `f=1`, the subtracted quasilocal energy vanishes, but the angular
boundary stress can remain nonzero:

```text
tau^A_A ~ q/(2R)
```

This matches the already found phi0 shell signature:

```text
angular-only stress
dimensionless unit q/2
H1/S2 projection eta = q/6
```

Guardrail:

```text
This is still a GR boundary-stress map, not a UDT derivation.
```

But it is a stronger clue than the raw EH action value:

```text
the native UDT target may be an angular boundary stress / edge stress,
not a boundary energy.
```

## 180. phi0 boundary candidate scorecard

Implemented in `native_phi0_boundary_candidate_scorecard.py`.

Current exact candidate status:

```text
C1 boundary momentum:
  q/2 unit:
    yes, -Pi_f/R = q/2.
  flat exterior:
    yes if paired with an interface source.
  angular form:
    needs H1/S2 projection added or derived.
  derives q:
    no.
  verdict:
    native conjugate variable; missing boundary functional.

Israel shell jump:
  q/2 unit:
    yes, trace-reversed angular jump has magnitude q/2.
  flat exterior:
    yes by construction.
  angular form:
    yes, angular-only at phi0.
  derives q:
    no.
  verdict:
    exact interface bookkeeping; not a native source by itself.

Raw EH curvature primitive:
  q/2 unit:
    sees qR, equal to -2 Pi_f.
  flat exterior:
    diagnostic only.
  angular form:
    distributional curvature includes angular delta stress.
  derives q:
    no.
  verdict:
    strong atlas clue; import risk as action.

Standard EH+GHY Dirichlet boundary action:
  q/2 unit:
    no, f' cancels at f=1 after completion/reference subtraction.
  flat exterior:
    yes.
  angular form:
    no eta-producing slope dependence in action value.
  derives q:
    no.
  verdict:
    rejected as eta mechanism.

Brown-York angular boundary stress:
  q/2 unit:
    yes, R tau^A_A -> q/2 at f=1.
  flat exterior:
    yes, energy vanishes at f=1.
  angular form:
    yes, zero energy and nonzero angular stress.
  derives q:
    no.
  verdict:
    best GR boundary-stress map; still not UDT derivation.

Maxwell/Coulomb sector:
  q/2 unit:
    no native coupling to Pi_f.
  flat exterior:
    not as phi0 shell without added charge layer.
  angular form:
    no, radial electromagnetic stress.
  derives q:
    no.
  verdict:
    real orchestra instrument, wrong boundary mechanism.
```

Hundred-sixty-fifth verdict:

```text
The q/2 angular boundary unit is now overdetermined by exact metric diagnostics.
```

It appears in:

```text
1. C1 boundary momentum,
2. Israel shell trace-reversed angular jump,
3. Brown-York angular boundary stress.
```

Therefore the missing derivation is no longer:

```text
how to get q/2 once q is given.
```

The missing derivation is:

```text
1. why native phi0 closure selects q = 1/3,
2. why the H1/S2 edge variables are the correct projection space,
3. why the projection factor is dynamically active rather than only kinematic.
```

This is progress because it moves `eta = 1/18` from a free numerical
guess toward a two-part exact target:

```text
q = 1/3        from native phi0 closure
1/3 projection from native angular/edge averaging
```

## 181. Positional-dilation guardrail for GR math

Implemented in `native_positional_dilation_gr_guardrail.py`.

Correction / caveat:

```text
UDT is not ordinary GR.
```

The positional-dilation term and the C1 action modify how GR mathematical
objects may be interpreted.

Therefore:

```text
GR math is an atlas.
UDT dynamics must be re-derived in the positional-dilation frame.
```

Classification:

```text
connection / curvature identities:
  usable exactly.
  They follow from the metric tensor itself, independent of field equations.

extrinsic curvature and shell-jump algebra:
  usable exactly as geometry.
  They follow from how hypersurfaces embed in the metric.

Einstein equations as source equations:
  not imported.
  UDT treats the metric as definitional positional dilation, not matter-sourced GR.

Einstein-Hilbert action as dynamics:
  not imported.
  UDT uses the C1 positional-dilation scalar action for phi dynamics.

GHY / Brown-York boundary objects:
  atlas only until native derivation.
  They identify boundary variables, but UDT may assign different action weights.

ADM mass / quasilocal energy:
  diagnostic only.
  UDT tail constants are scale/momentum diagnostics, not ordinary GR sourced mass.

horizon thermodynamics:
  not applicable at phi0.
  phi0 has f=1 and is not a horizon.

energy conditions / domain-wall dynamics:
  import risk.
  They assume GR matter-source interpretation rather than UDT positional dilation.
```

Hundred-sixty-sixth verdict:

```text
A GR result may be used directly only if it is a tensor/geometric identity
of the metric.
```

If it depends on:

```text
Einstein-Hilbert dynamics
Einstein source equations
GR boundary normalization
ordinary GR mass interpretation
```

then it becomes:

```text
a candidate map that must be re-derived from UDT's C1/angular action.
```

This modifies the previous GR-corpus result:

```text
Brown-York angular stress is not a UDT derivation.
```

Its correct status is:

```text
best current GR boundary-stress map to the native UDT target.
```

The native target remains:

```text
derive q = 1/3 and the q/2 angular boundary unit from the
positional-dilation C1/angular variational structure.
```

## 182. C1 bulk stress vs phi0 boundary unit

Implemented in `native_c1_bulk_stress_vs_boundary_unit.py`.

Now apply the positional-dilation guardrail directly.

The C1 scalar Lagrangian form, suppressing the overall coupling, is:

```text
L = -1/2 e^{-2phi} (partial phi)^2
f = e^{-2phi}
phi' = -f'/(2f)
```

For a static radial field:

```text
e^{-2phi} g^rr phi'^2 = f * f * phi'^2 = f'^2/4
```

The mixed C1 bulk stress components are:

```text
T^t_t = -f'^2/8
T^r_r = +f'^2/8
T^theta_theta = T^phi_phi = -f'^2/8
```

At phi0:

```text
f = 1
f' = -q/R
```

so:

```text
T^theta_theta = -q^2/(8R^2)
```

Compare the boundary unit:

```text
C1 boundary momentum:
  -Pi_f/R = q/2

Brown-York atlas angular unit:
  R tau^A_A -> q/2
```

For:

```text
q = 1/3
```

we get:

```text
C1 angular bulk-stress magnitude = 1/(72 R^2)
boundary unit = 1/6
```

Hundred-sixty-seventh verdict:

```text
The C1 bulk stress is quadratic in q.
The eta-producing boundary unit is linear in q.
```

Therefore:

```text
ordinary C1 bulk stress is not the missing eta mechanism.
```

The linear native object remains:

```text
C1 boundary momentum / edge stress.
```

This is the positional-dilation correction to the GR boundary-stress clue:

```text
GR points to the right kind of object, but UDT must derive it as a
C1/angular boundary variation, not as bulk scalar stress.
```

## 183. Spatial curvature fraction at phi0

Implemented in `native_spatial_curvature_fraction_q.py`.

Now use only the positional-dilation metric geometry, not GR dynamics.

On a static spatial slice:

```text
dl^2 = f^-1 dr^2 + r^2 dOmega^2
```

the exact 3D scalar curvature is:

```text
R3 = 2(1 - f - r f')/r^2
```

The intrinsic scalar curvature of the round S2 collar is:

```text
R2 = 2/r^2
```

At phi0:

```text
f(R) = 1
f'(R) = -q/R
```

therefore:

```text
R3(phi0) = 2q/R^2
R2(phi0) = 2/R^2
```

So:

```text
R3(phi0) / R2(phi0) = q
```

For:

```text
q = 1/3
```

this becomes:

```text
R3 = R2/3
```

Hundred-sixty-eighth verdict:

```text
q is not merely a slope parameter.
```

At the phi0 collar:

```text
q is exactly the fraction of the round-S2 intrinsic curvature that appears
as spatial-slice scalar curvature.
```

This does not yet derive:

```text
q = 1/3
```

But it changes the target into a clean geometric question:

```text
why would native phi0 closure select the one-third curvature fraction?
```

This is especially relevant because the angular projection already contains:

```text
<n_a n_b> = delta_ab/3
```

So the same one-third now appears in two exact metric-native places:

```text
1. isotropic H1/S2 angular projection,
2. phi0 spatial-curvature fraction if q = 1/3.
```

That is not yet a derivation, but it is a better target than a numerical ansatz.

## 184. phi0 sectional-curvature audit

Implemented in `native_phi0_sectional_curvature_audit.py`.

The spatial metric can be written with proper radial distance `rho`:

```text
dl^2 = d rho^2 + r(rho)^2 dOmega^2
d rho = dr/sqrt(f)
dr/d rho = sqrt(f)
```

The exact sectional curvatures are:

```text
K_radial-angular = -f'/(2r)
K_tangent-sphere = (1-f)/r^2
```

and:

```text
R3 = 4 K_radial-angular + 2 K_tangent-sphere
   = 2(1-f-rf')/r^2
```

At phi0:

```text
f(R) = 1
f'(R) = -q/R
```

so:

```text
K_radial-angular = q/(2R^2)
K_tangent-sphere = 0
R3 = 2q/R^2
```

The intrinsic S2 collar curvature is:

```text
K_S2 = 1/R^2
R2 = 2/R^2
```

Therefore:

```text
K_radial-angular / K_S2 = q/2
R3 / R2 = q
```

For:

```text
q = 1/3
```

this gives:

```text
K_radial-angular / K_S2 = 1/6
R3 / R2 = 1/3
```

Hundred-sixty-ninth verdict:

```text
q = 1/3 is not ordinary isotropic 3D curvature.
```

At phi0:

```text
the ambient tangential sectional curvature is zero.
```

The q data lives in:

```text
the two radial-angular sectional planes.
```

The eta source unit:

```text
q/2
```

is exactly:

```text
each radial-angular sectional curvature divided by the intrinsic S2 curvature.
```

This is a sharper native geometric interpretation:

```text
eta starts from the radial-angular curvature fraction, then applies the
H1/S2 isotropic projection.
```

## 185. Angular embedding-curvature piece

Implemented in `native_angular_embedding_curvature_piece.py`.

This addresses the question:

```text
could the angular sector be missing a piece?
```

The answer suggested by the exact metric geometry is:

```text
yes, but not as a new internal angular force.
```

The missing piece is likely:

```text
the embedding / radial evolution of the S2 collar.
```

For the S2 collar embedded in the spatial slice:

```text
s^A_B = sqrt(f)/R delta^A_B
k = 2 sqrt(f)/R
det(shape) = f/R^2
```

The ambient tangential sectional curvature is:

```text
K_tangent = (1-f)/R^2
```

The Gauss equation gives:

```text
K_intrinsic(S2) = K_tangent + det(shape)
                = (1-f)/R^2 + f/R^2
                = 1/R^2
```

So:

```text
the intrinsic round-S2 angular algebra is phi-blind exactly.
```

But the radial evolution of the shape operator is:

```text
n(s) = sqrt(f) d/dR [sqrt(f)/R]
     = f'/(2R) - f/R^2
```

and the Riccati relation gives:

```text
K_radial-angular = -n(s) - s^2
                 = -f'/(2R)
```

At phi0:

```text
f = 1
f' = -q/R
s = 1/R, same as flat
n(s) = -(1 + q/2)/R^2
K_radial-angular = q/(2R^2)
```

Hundred-seventieth verdict:

```text
The intrinsic angular sector is preserved and phi-blind.
```

But:

```text
the radial evolution of the angular embedding is phi-sensitive.
```

This explains why earlier angular-sector work could preserve most
functions and still miss a mass-emergence piece:

```text
it was looking mostly at intrinsic S2 algebra,
while q/2 lives in the radial-angular embedding curvature.
```

This keeps the orchestra frame:

```text
radial phi slope modulates the angular collar through embedding curvature.
```

It does not replace the angular sector. It supplies an interface instrument:

```text
intrinsic S2 representation algebra
+ radial-angular embedding curvature
+ C1 boundary momentum
```

## 186. Minimal curvature-share closure candidate

Implemented in `native_minimal_curvature_share_closure.py`.

This is the first clean `q = 1/3` candidate after the GR/positional-dilation
guardrail.

It is deliberately classified as:

```text
minimal native closure postulate
```

not as:

```text
derivation.
```

Native phi0 quantities:

```text
K_S2 = 1/R^2
K_radial-angular = q/(2R^2)
```

The two radial-angular planes sum to:

```text
2 K_radial-angular = q/R^2 = q K_S2
```

The H1/S2 isotropic share is:

```text
<n_a n_b> = delta_ab/3
```

so one isotropic frame share of the S2 curvature is:

```text
K_S2/3
```

Minimal closure condition:

```text
total radial-angular curvature share = one H1 isotropic share
```

That is:

```text
q K_S2 = K_S2/3
```

Therefore:

```text
q = 1/3
```

Consequences:

```text
per radial-angular plane:
  q/2 = 1/6

H1/S2 projected eta:
  (q/2)/3 = 1/18

one-sided transfer:
  eta/2 = 1/36
```

Hundred-seventy-first verdict:

```text
This is not a final derivation.
```

But it is a high-quality candidate postulate because:

```text
1. it uses only native metric quantities,
2. it uses the exact H1/S2 one-third projection,
3. it explains why the number 3 enters q rather than being fitted afterward,
4. it keeps the angular sector phi-blind intrinsically,
5. it puts mass emergence at the radial-angular edge/embedding layer.
```

Its current status is:

```text
P_phi0 candidate:
  at the phi0 closure, the summed radial-angular curvature share equals
  one isotropic H1/S2 angular share.
```

The next test is:

```text
derive or reject this closure from the C1/angular boundary variation.
```

## 187. One-third convergence audit

Implemented in `native_one_third_convergence_audit.py`.

The number `1/3` is now appearing through three native-looking routes.

Route 1:

```text
endpoint action/profile self-similarity
```

Equation:

```text
1 - 2p = p
```

Result:

```text
p = 1/3
```

Status:

```text
native closure principle candidate.
```

Open gap:

```text
does not prove the finite phi0 collar slope q equals endpoint exponent p.
```

Route 2:

```text
constant H1 angular-source q-flow
```

Equation:

```text
dq/dt = q^2 - q + 2s
s = 1/9
```

Result:

```text
q* = 1/3 outward-attractive
q* = 2/3 companion branch
```

Status:

```text
exact if the collar source is constant s = 1/9.
```

Open gap:

```text
derive s = 1/9 and show it remains the collar source.
```

Route 3:

```text
phi0 curvature-share closure
```

Equation:

```text
q K_S2 = K_S2/3
```

Result:

```text
q = 1/3
```

Status:

```text
minimal native boundary postulate candidate.
```

Open gap:

```text
derive the one-share allocation from C1/angular boundary variation.
```

Common downstream chain if:

```text
q = 1/3
```

is:

```text
radial-angular sectional ratio:
  q/2 = 1/6

H1/S2 projected eta:
  q/6 = 1/18

one-sided transfer:
  q/12 = 1/36
```

Hundred-seventy-second verdict:

```text
The repeated 1/3 is not yet a theorem.
```

It is:

```text
a convergence of native closure candidates.
```

The next decisive task is to prove or disprove whether:

```text
endpoint self-similarity,
H1 source strength,
curvature-share closure
```

are the same boundary condition expressed in three coordinate languages.

## 188. One-third equivalence triangle

Implemented in `native_one_third_equivalence_triangle.py`.

Definitions:

```text
p = endpoint profile exponent for f ~ r^-p
q = collar log-slope, q = -d ln f / d ln r
s = constant H1 source in q-flow
```

The bridge assumption to test is:

```text
q_phi0 = p
```

This holds for:

```text
a globally self-similar power-law collar.
```

It is not guaranteed for:

```text
a finite cell with a nontrivial boundary layer.
```

Endpoint self-similarity gives:

```text
1 - 2p = p
```

so:

```text
p = 1/3
```

If:

```text
q_phi0 = p
```

then:

```text
q = 1/3
R3/R2 = q = 1/3
```

The fixed-source q-flow condition is:

```text
s = q(1-q)/2
```

so for:

```text
q = 1/3
```

we get:

```text
s = 1/9
```

The downstream transfer is:

```text
q/2 = 1/6
eta = q/6 = 1/18
eta/2 = q/12 = 1/36
```

Hundred-seventy-third verdict:

```text
The three one-third routes are algebraically the same if q_phi0 = p.
```

Therefore the decisive native question is:

```text
does the phi0 boundary layer preserve the self-similar log-slope?
```

If yes:

```text
q = 1/3 follows from endpoint self-similarity.
```

If no:

```text
q is determined by the boundary layer/source running instead.
```

This reduces the apparent proliferation of mechanisms. The orchestra may be
playing one motif through three instruments:

```text
endpoint scaling,
angular-source q-flow,
radial-angular curvature share.
```

## 189. Collar slope renormalization audit

Implemented in `native_collar_slope_renormalization_audit.py`.

To isolate the remaining gap, write a finite-cell interior as:

```text
f(r) = (R/r)^p h(r)
```

with:

```text
h(R) = 1
```

The collar log-slope is:

```text
q_phi0 = -d ln f / d ln r at R
       = p - d ln h / d ln r at R
```

Define the boundary-layer renormalization:

```text
delta_h = -d ln h / d ln r at R
```

Then:

```text
q_phi0 = p + delta_h
```

Therefore:

```text
q_phi0 = p only if delta_h = 0.
```

For endpoint self-similarity:

```text
p = 1/3
```

we have:

```text
q_phi0 = 1/3 + delta_h
eta = q_phi0/6 = 1/18 + delta_h/6
```

The flat exterior condition is:

```text
f_out = 1
f'_out = 0
```

This does not force:

```text
delta_h = 0
```

It only tells us:

```text
the interface jump equals the inner q_phi0.
```

Hundred-seventy-fourth verdict:

```text
The endpoint p=1/3 route derives q=1/3 only if the phi0 boundary layer
does not renormalize the log-slope.
```

The next native test is whether C1/angular closure enforces:

```text
delta_h = 0
```

or instead predicts:

```text
branch-dependent delta_h.
```

This is where the orchestra can enter without inventing a separate mechanism:

```text
different instruments may contribute through delta_h.
```

## 190. Revised phi0 edge variable set

Implemented in `native_revised_phi0_edge_variables.py`.

The candidate boundary functional should no longer be described only as:

```text
angular sector
```

or:

```text
phi boundary layer.
```

The exact native variables now visible at the phi0 edge are:

```text
f:
  meaning:
    metric value at the phi0 collar.
  phi0 value:
    f = 1.
  role:
    sets the zero-phi interface.

Pi_f:
  meaning:
    C1 conjugate boundary momentum.
  phi0 value:
    Pi_f = -qR/2.
  role:
    native linear boundary object.

K_S2:
  meaning:
    intrinsic round-S2 sectional curvature.
  phi0 value:
    K_S2 = 1/R^2.
  role:
    phi-blind angular representation arena.

s^A_B:
  meaning:
    shape operator of the S2 collar in the spatial slice.
  phi0 value:
    s^A_B = (1/R) delta^A_B.
  role:
    embedding value; same as flat at phi0.

n(s):
  meaning:
    normal/radial evolution of the shape operator.
  phi0 value:
    n(s) = -(1 + q/2)/R^2.
  role:
    embedding evolution; carries q.

K_rad:
  meaning:
    radial-angular sectional curvature.
  phi0 value:
    K_rad = q/(2R^2).
  role:
    linear curvature-share object; equals eta source unit before H1 projection.

n_a:
  meaning:
    unit H1/S2 direction observable.
  phi0 value:
    <n_a n_b> = delta_ab/3.
  role:
    isotropic projection from edge curvature to eta.
```

Hundred-seventy-fifth verdict:

```text
The next boundary-functional search should use these native edge variables
before introducing any new mechanism.
```

In orchestra language:

```text
phi provides Pi_f and q,
angular geometry provides K_S2 and n_a,
the interface provides s^A_B, n(s), and K_rad.
```

This is the cleanest current map of the native ensemble at phi0.

## 191. Edge-embedding hypothesis falsification criteria

Implemented in `native_edge_hypothesis_falsification_criteria.py`.

The edge-embedding hypothesis is useful only if it stays falsifiable.

Criteria:

```text
native-variable closure:
  requirement:
    uses f, Pi_f, K_S2, shape data, K_rad, and H1/S2 projection only.
  failure mode:
    requires an imported force, EH dynamics, SM label, or fitted mass ratio.

linear boundary unit:
  requirement:
    produces the linear edge unit -Pi_f/R = K_rad/K_S2 = q/2.
  failure mode:
    uses ordinary C1 bulk stress, which is quadratic in q.

flat exterior:
  requirement:
    keeps f_out = 1 and f'_out = 0 outside phi0.
  failure mode:
    leaks an exterior 1/r tail or requires exterior mass charge.

slope selection:
  requirement:
    derives or explicitly postulates q_phi0 = 1/3.
  failure mode:
    assumes q without naming the closure input.

slope-renormalization audit:
  requirement:
    accounts for q_phi0 = p + delta_h.
  failure mode:
    silently identifies endpoint p with collar q.

angular projection:
  requirement:
    uses the exact H1/S2 projection <n_a n_b> = delta_ab/3.
  failure mode:
    adds an angular coefficient or degeneracy by hand.

scale covariance:
  requirement:
    depends on dimensionless units such as -Pi_f/R and K_rad/K_S2.
  failure mode:
    introduces a dimensionful scale other than the later electron anchor.
```

Hundred-seventy-sixth verdict:

```text
Treat the edge-embedding hypothesis as a candidate only while it passes
these tests.
```

If it fails one:

```text
downgrade it immediately.
```

## 192. Curvature-share closure as Neumann boundary data

Implemented in `native_curvature_share_as_neumann_data.py`.

At phi0:

```text
K_rad = q/(2R^2)
K_S2 = 1/R^2
Pi_f = -qR/2
```

Therefore:

```text
K_rad / K_S2 = q/2
-Pi_f / R = q/2
```

The minimal curvature-share closure:

```text
K_rad / K_S2 = 1/6
```

is exactly equivalent to:

```text
-Pi_f/R = 1/6
Pi_f = -R/6
```

Thus:

```text
q = 1/3
eta = q/6 = 1/18
one-sided transfer = q/12 = 1/36
```

Hundred-seventy-seventh verdict:

```text
The curvature-share closure is Neumann/edge momentum data for the C1
radial action.
```

It is not:

```text
ordinary C1 bulk stress
```

and it is not:

```text
a potential B(f) alone.
```

If accepted as a postulate, the smallest honest form is:

```text
P_phi0:
  the phi0 edge fixes the dimensionless C1 momentum -Pi_f/R to one
  radial-angular curvature share, 1/6.
```

To upgrade it from postulate to derivation:

```text
the boundary variation must produce this Neumann value.
```

## 193. Constant H1 source mode-filter audit

Implemented in `native_constant_h1_source_mode_filter.py`.

The constant-source radial equation is:

```text
f'' + 2 f'/r + 2s f/r^2 = 0
```

For a power branch:

```text
f ~ r^-q
```

the source relation is:

```text
s = q(1-q)/2
```

For:

```text
s = 1/9
```

the two branches are:

```text
q = 1/3
q = 2/3
```

The general local solution is:

```text
f(r) = A r^(-1/3) + B r^(-2/3)
```

The C1 finite-action condition near the endpoint is:

```text
f ~ r^-p is finite-action only if p < 1/2.
```

Therefore:

```text
p = 1/3  finite-action
p = 2/3  not finite-action
```

So finite C1 action sets:

```text
B = 0
```

leaving:

```text
f(r) = A r^(-1/3)
```

and therefore:

```text
q(r) = -d ln f/d ln r = 1/3
```

at every radius in the constant-source collar.

Thus:

```text
delta_h = 0
```

At phi0:

```text
q_phi0 = 1/3
-Pi_f/R = q/2 = 1/6
eta = q/6 = 1/18
```

Hundred-seventy-eighth verdict:

```text
If the phi0 collar is governed by the constant H1 source s = 1/9,
finite C1 action removes the 2/3 companion branch and enforces
q_phi0 = p = 1/3.
```

This is the strongest no-renormalization result so far.

The remaining open derivation is now narrowed to:

```text
why the native H1 edge source is s = 1/9.
```

## 194. H1 source one-ninth origin audit

Implemented in `native_h1_source_one_ninth_origin_audit.py`.

The constant-source route now reduces the problem to:

```text
s = 1/9
```

But this must not be derived by loose numerology.

Candidate origins:

```text
single isotropic S2 second moment <n_i^2>:
  value:
    1/3.
  verdict:
    too large; gives 1/3, not 1/9.

single-component S2 fourth moment <n_i^4>:
  value:
    1/5.
  verdict:
    wrong value; do not replace by (1/3)^2 unless two factors are independent.

two independent isotropic H1/S2 second-moment projections:
  value:
    1/9.
  verdict:
    correct value if the source genuinely factorizes into two independent
    projections.

curvature-share 1/3 times H1/S2 projection 1/3:
  value:
    1/9.
  verdict:
    correct value if curvature-share closure is already established.

fixed-point backsolve from q=1/3:
  value:
    1/9.
  verdict:
    algebraically true but circular as a derivation of s.
```

Hundred-seventy-ninth verdict:

```text
s = 1/9 is not derived by saying "one third appears twice."
```

It requires an exact two-factor structure:

```text
independent projection x independent projection
```

or:

```text
established curvature-share x independent H1/S2 projection.
```

Otherwise:

```text
s = 1/9 remains a postulate or circular backsolve.
```

This is the next anti-fitting guardrail.

## 195. Source coefficient as S2 curvature fraction

Implemented in `native_source_as_s2_curvature_fraction.py`.

The angular-source radial equation is:

```text
f'' + 2 f'/r + 2s f/r^2 = 0
```

The round S2 scalar curvature is:

```text
R2 = 2/r^2
```

Therefore the source term is:

```text
(2s/r^2) f = s R2 f
```

So:

```text
s is exactly the fraction of intrinsic S2 scalar curvature coupled
into the radial f equation.
```

For:

```text
s = 1/9
```

the source is:

```text
(1/9) R2 f
```

Projection checks:

```text
one isotropic S2/H1 share:
  R2/3 -> s = 1/3

two independent one-third shares:
  R2/9 -> s = 1/9
```

Hundred-eightieth verdict:

```text
The open derivation is not an arbitrary source constant.
```

It is specifically:

```text
does the native phi0 edge couple one ninth of the S2 scalar curvature
into the radial f equation?
```

This sharpens the `s = 1/9` problem into an angular-curvature coupling
problem.

## 196. Two-factor source-structure audit

Implemented in `native_two_factor_source_structure_audit.py`.

Allowed and rejected structures for:

```text
s = 1/9
```

are:

```text
same-axis fourth moment:
  value:
    1/5.
  status:
    rejected for s = 1/9.
  condition:
    this is <n_i^4>, not <n_i^2>^2.

single H1/S2 projection:
  value:
    1/3.
  status:
    rejected for s = 1/9.
  condition:
    one projection gives s = 1/3.

independent input/output H1 projections:
  value:
    1/9.
  status:
    viable target.
  condition:
    requires two independently normalized edge projections.

curvature-share times H1 projection:
  value:
    1/9.
  status:
    viable only after curvature-share closure.
  condition:
    requires q = 1/3 from an independent closure, otherwise circular.

rank-one normalized kernel trace:
  value:
    1/9.
  status:
    viable target.
  condition:
    requires an exact separable kernel with two trace-normalized H1 legs.
```

Hundred-eighty-first verdict:

```text
The strongest non-circular path is an exact edge kernel with two
independently normalized H1/S2 projection legs.
```

Without that kernel:

```text
s = 1/9 remains the minimal phi0 postulate, not a derivation.
```

This gives the next concrete work target:

```text
search the native edge variables for a separable H1/S2 boundary kernel.
```

## 197. phi0 edge-embedding resolution candidate

Implemented in `native_phi0_resolution_candidate.py`.

Instead of treating the current work as an endless derivation chase, state the
candidate resolution cleanly.

Minimal optional postulate:

```text
P_phi0:
  the phi0 edge fixes the dimensionless C1 boundary momentum to one
  radial-angular curvature share.
```

Equivalent forms:

```text
-Pi_f/R = 1/6
K_rad/K_S2 = 1/6
q/2 = 1/6
q = 1/3
```

Exact consequences:

```text
q = 1/3
s = q(1-q)/2 = 1/9
eta = q/6 = 1/18
one-sided transfer = eta/2 = 1/36
```

Interpretation:

```text
mass emergence starts as a phi/angular edge condition.
```

The instruments are:

```text
C1 boundary momentum,
radial-angular embedding curvature,
H1/S2 projection.
```

What this resolves:

```text
1. why intrinsic angular algebra survives,
2. where q/2 lives geometrically,
3. why eta = 1/18 follows from one small closure,
4. why ordinary C1 bulk stress is not the eta mechanism,
5. why Maxwell/Coulomb is a real later instrument but not this boundary closure.
```

What this does not resolve:

```text
1. derivation of P_phi0 from a boundary kernel,
2. cascade depth rule,
3. gamma transfer normalization beyond eta,
4. branch coefficient ratios.
```

Hundred-eighty-second verdict:

```text
This is a concrete resolution candidate for the ponder hypothesis.
```

It is not:

```text
a completed derivation of the full mass ladder.
```

The honest status is:

```text
P_phi0 can be banked as a minimal native postulate,
or pursued as a derivation from a separable H1/S2 edge kernel.
```

## 198. Minimal postulate budget

Implemented in `native_minimal_postulate_budget.py`.

If the work banks `P_phi0`, the postulate budget is:

```text
P0 metric:
  status:
    foundation.
  note:
    positional-dilation metric; already UDT foundation.

P_phi0:
  status:
    candidate minimal mass-emergence postulate.
  note:
    at phi0, -Pi_f/R = 1/6, equivalently K_rad/K_S2 = 1/6.

electron anchor:
  status:
    allowed dimensionful anchor.
  note:
    sets the absolute mass scale only.

H1/S2 projection:
  status:
    derived geometry.
  note:
    <n_a n_b> = delta_ab/3.

finite C1 action branch filter:
  status:
    derived filter.
  note:
    rejects q = 2/3 branch under constant s = 1/9.

gamma = N exp(-eta/2):
  status:
    still candidate transfer rule.
  note:
    compact diagnostic but transfer normalization not fully derived.

depth rule:
  status:
    still ansatz-bearing.
  note:
    typed edge/cascade depth not fully derived.

branch coefficient ratios:
  status:
    still diagnostic.
  note:
    not upgraded by P_phi0 alone.
```

Hundred-eighty-third verdict:

```text
P_phi0 would be one small new postulate on top of P0 and the electron anchor.
```

It resolves:

```text
q
s
eta
```

if accepted.

It does not by itself canonize:

```text
the full mass ladder.
```

That separation is important because it prevents the edge closure from
silently laundering later ansatz pieces into derived status.

## 199. P_phi0 criteria scorecard

Implemented in `native_p_phi0_criteria_scorecard.py`.

Check `P_phi0` against the falsification criteria.

```text
native-variable closure:
  status:
    passes.
  reason:
    uses Pi_f, K_rad, K_S2, and H1/S2 projection only.

linear boundary unit:
  status:
    passes.
  reason:
    postulates -Pi_f/R = K_rad/K_S2 = 1/6.

flat exterior:
  status:
    passes if treated as interface Neumann data.
  reason:
    flat exterior has Pi_out = 0; the jump is localized at phi0.

slope selection:
  status:
    passes as postulate, not derivation.
  reason:
    selects q = 1/3 explicitly rather than hiding it.

slope-renormalization audit:
  status:
    passes under constant s = 1/9 plus finite-action filter.
  reason:
    finite action removes q = 2/3 branch, leaving delta_h = 0.

angular projection:
  status:
    passes.
  reason:
    eta uses exact <n_a n_b> = delta_ab/3.

scale covariance:
  status:
    passes.
  reason:
    closure uses dimensionless -Pi_f/R and K_rad/K_S2.

non-circular s = 1/9 derivation:
  status:
    open.
  reason:
    requires a native two-factor edge kernel or remains part of P_phi0.
```

Hundred-eighty-fourth verdict:

```text
P_phi0 is internally clean as a minimal closure postulate.
```

It is not yet:

```text
internally derived.
```

because:

```text
the non-circular two-factor source kernel remains open.
```

This is a good stopping point for the ponder hypothesis:

```text
the metric appears to be doing edge-embedding closure.
```

The only unresolved choice is:

```text
derive the edge kernel,
or bank P_phi0 as the minimal new postulate.
```

## 200. phi0 decision point

Implemented in `native_phi0_decision_point.py`.

There are now two legitimate next branches.

Branch 1:

```text
derive-kernel branch
```

Action:

```text
search for an exact separable H1/S2 edge kernel producing s = 1/9.
```

Claim allowed:

```text
P_phi0 can be upgraded from postulate to derived boundary condition if found.
```

Claim not allowed:

```text
do not assume factorization before the kernel exists.
```

Branch 2:

```text
bank-postulate branch
```

Action:

```text
declare P_phi0 as a minimal native postulate.
```

Claim allowed:

```text
q, s, and eta are consequences of P_phi0 plus derived H1/S2 projection.
```

Claim not allowed:

```text
do not call the phi0 closure derived;
do not canonize the full ladder.
```

Hundred-eighty-fifth verdict:

```text
The ponder hypothesis has a concrete candidate resolution.
```

The honest fork is:

```text
derive P_phi0 now,
or bank it as a minimal postulate while building the rest of the orchestra
around it.
```

This prevents endless derivation drift because the unresolved item is no
longer vague:

```text
find the edge kernel, or explicitly postulate the edge closure.
```

## 201. Banked P_phi0 working chain

Implemented in `native_banked_p_phi0_chain.py`.

Working choice:

```text
Bank P_phi0 as a minimal native edge postulate.
```

The postulate is:

```text
P_phi0:
  -Pi_f/R = 1/6
```

equivalently:

```text
K_rad/K_S2 = 1/6
```

Exact consequences of `P_phi0` plus the H1/S2 projection:

```text
q = 1/3
s = q(1-q)/2 = 1/9
eta = q/6 = 1/18
one-sided transfer exponent = eta/2 = 1/36
```

Transfer diagnostic:

```text
gamma = 3 exp(-eta/2) = 2.91781343135...
```

Status ledger:

```text
P_phi0:
  banked minimal postulate.

H1/S2 projection:
  derived geometry.

finite-action branch filter:
  derived once s = 1/9 is present.

gamma transfer form:
  diagnostic / candidate.

typed depth rule:
  diagnostic / candidate.

branch coefficients:
  diagnostic / candidate.
```

Hundred-eighty-sixth verdict:

```text
Banking P_phi0 resolves the eta foundation without pretending to derive
the full transfer ladder.
```

## 202. Banked P_phi0 mass diagnostic

Implemented in `native_banked_p_phi0_mass_diagnostic.py`.

With banked `P_phi0`:

```text
q = 1/3
eta = 1/18
```

The following remain diagnostic:

```text
gamma = 3 exp(-eta/2)
typed node depths
branch coefficient ratio
```

Using the existing diagnostic typed branches:

```text
M1/mu-like:
  typed_nodes = 5
  coefficient ratio = 1
  predicted mass = 108.07061 MeV
  target = 105.65838 MeV
  fractional error = +2.2831%

E1/tau-like:
  typed_nodes = 7
  coefficient ratio = 1.85479...
  predicted mass = 1706.54612 MeV
  target = 1776.86 MeV
  fractional error = -3.9572%
```

Hundred-eighty-seventh verdict:

```text
P_phi0 improves the foundation of eta.
```

It does not by itself validate:

```text
gamma,
depths,
coefficients.
```

So the current mass diagnostic remains:

```text
promising but not canonized.
```

## 203. Post-P_phi0 orchestra map

Implemented in `native_post_p_phi0_orchestra_map.py`.

After banking `P_phi0`, do not spend the next pass re-deriving `eta`.

The current orchestra is:

```text
P_phi0 edge closure:
  role:
    fixes -Pi_f/R = 1/6, hence q = 1/3 and eta = 1/18.
  status:
    banked minimal postulate.
  next test:
    optional search for exact H1/S2 edge kernel.

H1/S2 projection:
  role:
    projects q/2 to eta = q/6 via <n_a n_b> = delta_ab/3.
  status:
    derived geometry.
  next test:
    none for eta; only check independence in transfer graph.

finite C1 action filter:
  role:
    rejects q = 2/3 branch once s = 1/9 is present.
  status:
    derived filter.
  next test:
    ensure no branch-specific source running reintroduces delta_h.

transfer multiplier gamma:
  role:
    converts eta into per-node multiplicative ladder gamma = 3 exp(-eta/2).
  status:
    candidate transfer rule.
  next test:
    derive channel multiplicity and one-sided exponential from boundary action.

typed node depth:
  role:
    assigns M1 depth 5 and E1 depth 7 in current diagnostic.
  status:
    candidate graph rule.
  next test:
    derive node independence and prevent double counting shared H1 frame nodes.

branch coefficients:
  role:
    supply M1/E1 finite-cell coefficient ratio.
  status:
    diagnostic coefficient data.
  next test:
    derive from native edge spectrum or remove from predictive chain.

electron anchor:
  role:
    sets absolute mass scale.
  status:
    allowed single dimensionful anchor.
  next test:
    none; keep it as scale only.
```

Hundred-eighty-eighth verdict:

```text
With P_phi0 banked, the next load-bearing work is transfer gamma,
typed node depth, and branch coefficients.
```

## 204. Transfer postulate candidate audit

Implemented in `native_transfer_postulate_candidate.py`.

Given banked `P_phi0`:

```text
eta = 1/18
```

Candidate transfer rule:

```text
P_transfer:
  each independent edge node contributes
  gamma = N exp(-eta/2)
```

with:

```text
N = 3
```

from H1/S2 channel multiplicity.

For:

```text
eta = 1/18
```

we get:

```text
eta/2 = 1/36
gamma = 3 exp(-1/36) = 2.91781343135...
```

What must be derived to upgrade `P_transfer`:

```text
1. N = 3 acts as multiplicity in the transfer, not only representation count.
2. eta/2 is the correct one-sided boundary action per independent node.
3. node contributions multiply rather than add.
4. typed nodes are independent after shared H1 frame merging.
```

Hundred-eighty-ninth verdict:

```text
P_transfer is a second possible compact postulate.
```

But:

```text
it is not resolved by P_phi0.
```

Keep the two postulates separate:

```text
P_phi0 resolves eta.
P_transfer supplies the ladder multiplier.
```

## 205. Two-postulate working model

Implemented in `native_two_postulate_working_model.py`.

If the work allows two simple postulates, the clean working model is:

```text
P_phi0:
  status:
    banked minimal postulate.
  output:
    -Pi_f/R = 1/6 -> q = 1/3 -> eta = 1/18.

P_transfer:
  status:
    candidate second postulate.
  output:
    gamma = 3 exp(-eta/2).
```

Together they give:

```text
eta = 1/18
gamma = 2.91781343135...
```

The derived geometric piece remains:

```text
H1/S2 projection:
  <n_a n_b> = delta_ab/3.
```

The pieces not solved by the two-postulate model are:

```text
typed depths:
  M1 = 5
  E1 = 7
  status: diagnostic.

branch coefficients:
  status: diagnostic.
```

Hundred-ninetieth verdict:

```text
With P_phi0 and P_transfer banked, the ladder multiplier is fixed.
```

But:

```text
mass predictions are not derived until typed depths and branch coefficients
are independently fixed or explicitly postulated.
```

## 206. Typed depth next audit

Implemented in `native_typed_depth_next_audit.py`.

After `P_phi0` and `P_transfer`, typed depth is the next major
load-bearing piece.

Current claims:

```text
M1 / mu-like:
  current depth:
    5.
  current count:
    3 shared H1 frame nodes + 2 primitive compact/radial shape nodes.
  risk:
    primitive compact nodes may be bridge variables rather than independent
    transfer nodes.
  required derivation:
    show which compact/radial variables produce independent transfer factors.

E1 / tau-like:
  current depth:
    7.
  current count:
    3 shared H1 frame nodes + 4 ordinary H1 shape nodes.
  risk:
    ordinary H1 shape nodes may double-count frame or boundary variables.
  required derivation:
    derive four independent E1 edge-shape transfer nodes.
```

Hundred-ninety-first verdict:

```text
Typed depth must be derived as independent edge-transfer nodes,
not tuned from observed mu/tau masses.
```

This becomes the next non-eta target.

## 207. H1 components vs transfer nodes audit

Implemented in `native_h1_components_vs_nodes_audit.py`.

The exact H1/S2 geometry provides several related but distinct numbers:

```text
H1 component count:
  exact value:
    3.
  meaning:
    three ambient components n_a.
  transfer status:
    may support channel multiplicity if a transfer rule is postulated or
    derived.

unit constraint:
  exact value:
    n_a n_a = 1.
  meaning:
    one exact constraint on the three components.
  transfer status:
    prevents reading component count as unconstrained degrees of freedom.

S2 manifold dimension:
  exact value:
    2.
  meaning:
    the unit vector n_a lives on S2.
  transfer status:
    geometric degree count, not automatically transfer-node count.

isotropic second moment:
  exact value:
    <n_a n_b> = delta_ab/3.
  meaning:
    projection identity over the round S2.
  transfer status:
    derived projection factor for eta.

projector trace:
  exact value:
    tr(delta_ab/3) = 1.
  meaning:
    the normalized projector sums to one total share.
  transfer status:
    does not by itself create three independent transfer nodes.
```

Hundred-ninety-second verdict:

```text
The exact H1/S2 geometry derives a 1/3 projection and a three-component
channel arena.
```

It does not by itself derive:

```text
three independent transfer depth nodes.
```

Therefore:

```text
3-as-multiplicity and 3-as-depth must be treated separately.
```

## 208. phi0 edge invariant rank audit

Implemented in `native_edge_invariant_rank_audit.py`.

Now audit what the spherical phi0 edge itself contains.

```text
intrinsic S2 metric:
  phi0 form:
    gamma_AB = R^2 omega_AB.
  independent shape:
    isotropic; no traceless angular part.
  consequence:
    preserves phi-blind round-S2 representation arena.

S2 shape operator:
  phi0 form:
    s^A_B = (1/R) delta^A_B.
  independent shape:
    isotropic; same value as flat at f = 1.
  consequence:
    does not create branch depth by itself.

normal derivative of shape:
  phi0 form:
    n(s)^A_B = -(1+q/2) delta^A_B / R^2.
  independent shape:
    isotropic scalar q correction.
  consequence:
    carries edge momentum but no traceless angular split.

radial-angular sectional curvature:
  phi0 form:
    K_rad = q/(2R^2).
  independent shape:
    single scalar shared by both radial-angular planes.
  consequence:
    supplies eta source unit q/2 before projection.

C1 boundary momentum:
  phi0 form:
    Pi_f = -qR/2.
  independent shape:
    single scalar conjugate momentum.
  consequence:
    native Neumann edge datum.
```

Hundred-ninety-third verdict:

```text
The spherical phi0 edge supplies scalar/isotropic invariants plus the H1/S2
orientation arena.
```

It does not by itself contain:

```text
native 5- or 7-node typed depth.
```

Those counts require:

```text
an additional edge graph or bundle structure beyond the scalar spherical
metric edge.
```

This does not reject the orchestra. It prevents overclaiming:

```text
P_phi0 resolves eta, but not typed depth.
```

## 209. Exact bundle/measure status

Implemented in `native_exact_bundle_measure_status.py`.

Earlier bundle probes used numerical sampling only as diagnostics. They are
not used as stated results here. The exact replacements are:

```text
CP1 / Hopf bridge:
  exact statement:
    normalized C2 modulo common U(1) phase is CP1, and CP1 is S2.
  depth consequence:
    Hopf bilinears merge into the common H1/S2 frame; they do not add a
    second orientation frame.
  status:
    exact topology/geometry.

CP1 measure pushforward:
  exact statement:
    Fubini-Study measure on CP1 pushes to the round S2 measure.
  depth consequence:
    bare M1 projective geometry has no anisotropic extra weighting.
  status:
    exact standard CP1/S2 measure fact.

H1/S2 second moment:
  exact statement:
    <n_a n_b> = delta_ab/3.
  depth consequence:
    gives eta projection; does not create three unconstrained depth nodes.
  status:
    exact round-S2 integral.

E1 relative-shape plane:
  exact statement:
    R3 decomposes into common line span(1,1,1) plus a two-dimensional
    orthogonal relative plane.
  depth consequence:
    supports two relative-shape coordinates per boundary if those boundaries
    are independent.
  status:
    exact linear algebra.

relative-plane second moment:
  exact statement:
    uniform unit circle in the relative plane has <u_i u_j> = delta_ij/2
    in an orthonormal basis.
  depth consequence:
    isotropic within relative shape; no branch correction by itself.
  status:
    exact circle integral.
```

Hundred-ninety-fourth verdict:

```text
These are exact geometry/linear-algebra facts.
```

They replace:

```text
numerical measure probes
```

as inputs to the current chain.

## 210. Exact typed-depth status

Implemented in `native_typed_depth_status_exact.py`.

The exact geometry supports the ingredients of the current typed-depth
candidate, but not the transfer-node independence.

```text
M1 / compact primitive:
  exact native support:
    CP1/Hopf data maps exactly into the common H1/S2 frame;
    a primitive compact/radial scalar may appear at each boundary.
  candidate count:
    3 H1 channel slots + 1 core shape + 1 phi0 shape = 5.
  open assumption:
    H1 channel slots and the two boundary shape scalars are independent
    transfer nodes.
  verdict:
    candidate P_depth_M1, not derived from scalar edge rank alone.

E1 / ordinary H1:
  exact native support:
    after removing common amplitude, ordinary H1 relative shape is an exact
    two-dimensional plane.
  candidate count:
    3 H1 channel slots + 2 core relative shapes + 2 phi0 relative shapes = 7.
  open assumption:
    core and phi0 relative-shape coordinates are independent transfer nodes.
  verdict:
    candidate P_depth_E1, not derived from scalar edge rank alone.
```

Hundred-ninety-fifth verdict:

```text
The exact geometry supports the ingredients of 5 and 7,
but not the transfer-node independence.
```

Therefore, if used:

```text
typed depth must be a separate P_depth postulate or derived from an
edge graph.
```

This is compatible with the orchestra metaphor:

```text
P_phi0 supplies the edge unit,
P_transfer supplies the per-node multiplier,
P_depth supplies which native edge/bundle variables actually play.
```

## 211. Postulate pressure audit

Implemented in `native_postulate_pressure_audit.py`.

There is now a clear postulate budget pressure.

```text
one-postulate edge model:
  banked items:
    P_phi0.
  resolved:
    q, s, eta.
  remains diagnostic:
    gamma, typed depth, branch coefficients, full masses.
  verdict:
    cleanest native mass-emergence foundation; not a full ladder.

two-postulate multiplier model:
  banked items:
    P_phi0 + P_transfer.
  resolved:
    q, s, eta, gamma.
  remains diagnostic:
    typed depth, branch coefficients, full masses.
  verdict:
    still compact; useful working model but not a full derivation.

three-postulate ladder model:
  banked items:
    P_phi0 + P_transfer + P_depth.
  resolved:
    q, s, eta, gamma, typed depth.
  remains diagnostic:
    branch coefficients and coefficient normalization.
  verdict:
    postulate-heavy; should not be called minimal unless P_depth is derived.
```

Hundred-ninety-sixth verdict:

```text
The cleanest current stopping point is P_phi0,
or at most P_phi0 + P_transfer.
```

Do not bank:

```text
P_depth
```

unless:

```text
1. the project explicitly accepts a third postulate, or
2. P_depth is derived from an edge graph.
```

This honors the reminder:

```text
uncover what the metric is doing; do not create mechanisms.
```

Typed depth remains:

```text
diagnostic, not canonical.
```

## 212. Exact transfer identity conditions

Implemented in `native_exact_transfer_identity_conditions.py`.

Given banked `P_phi0`:

```text
eta = 1/18
```

There is an exact conditional identity:

```text
If an edge transfer node has:
  1. three exactly degenerate H1/S2 channel states, and
  2. scalar one-sided action eta/2 on each state,

then:
  gamma = Tr_H1 exp(-eta/2 I_3)
        = 3 exp(-eta/2).
```

For:

```text
eta = 1/18
```

this is:

```text
eta/2 = 1/36
gamma = 3 exp(-1/36)
```

What is exact here:

```text
the trace identity,
the no-double-counting half-boundary bookkeeping if the transfer kernel is
one side of a glued boundary.
```

What is not exact from `P_phi0` alone:

```text
existence of the transfer kernel,
threefold degeneracy as transfer multiplicity,
scalar action eta/2 on all three channels,
multiplication over independent typed nodes.
```

Hundred-ninety-seventh verdict:

```text
P_transfer is an exact conditional identity, not a derived UDT result.
```

To derive it:

```text
the metric must supply the three-channel scalar one-sided edge kernel.
```

## 213. Transfer identity failure modes

Implemented in `native_transfer_identity_failure_modes.py`.

Failure modes for:

```text
gamma = 3 exp(-eta/2)
```

are:

```text
nondegenerate channel actions:
  consequence:
    gamma becomes sum_i exp(-a_i), not 3 exp(-eta/2).
  verdict:
    P_transfer rejected unless a_i are all eta/2.

single normalized projector instead of channel trace:
  consequence:
    trace weight is one normalized share, not multiplicity three.
  verdict:
    3 factor rejected.

full boundary action per side:
  consequence:
    single-step exponent is eta, not eta/2.
  verdict:
    half-factor rejected unless gluing/no-double-counting applies.

correlated typed nodes:
  consequence:
    node weights do not multiply independently.
  verdict:
    depth exponent rejected or reduced.

branch-dependent edge actions:
  consequence:
    one universal gamma fails.
  verdict:
    use branch-specific transfer or reject ladder.
```

Hundred-ninety-eighth verdict:

```text
The transfer rule is fragile.
```

It should be used only if these exact failure modes are ruled out by:

```text
metric edge structure,
```

not by:

```text
observation matching.
```

## 214. H1 edge-kernel eigenvalue audit

Implemented in `native_h1_edge_kernel_eigenvalue_audit.py`.

Use:

```text
eta = 1/18
```

The exact H1 kernel possibilities are different.

Candidate A:

```text
scalar identity action
A = (eta/2) I_3
eigenvalues: eta/2, eta/2, eta/2
trace exp(-A) = 3 exp(-eta/2)
status: gives P_transfer exactly.
```

Candidate B:

```text
rank-one direction action
A = (eta/2) n n^T
eigenvalues: eta/2, 0, 0
trace exp(-A) = exp(-eta/2) + 2
status: not P_transfer.
```

Candidate C:

```text
normalized isotropic projector
<n_a n_b> = delta_ab/3
A = (eta/2)(I_3/3)
eigenvalues: eta/6, eta/6, eta/6
trace exp(-A) = 3 exp(-eta/6)
status: not P_transfer.
```

Candidate D:

```text
scalar after projection, then channel trace
projection produces scalar eta
independent transfer postulate assigns eta/2 to each of 3 channels
trace exp(-A) = 3 exp(-eta/2)
status: P_transfer, but requires a separate channel-trace rule.
```

Hundred-ninety-ninth verdict:

```text
The exact H1/S2 projection alone does not derive P_transfer.
```

P_transfer requires:

```text
the metric edge to turn the projected scalar eta into an equal
one-sided action on three channel states.
```

This is stricter than:

```text
there are three H1 components.
```

So:

```text
P_transfer remains a separate postulate unless the scalar identity kernel
is found natively.
```

## 215. Scalar identity kernel search

Implemented in `native_scalar_identity_kernel_search.py`.

Search current native edge variables for the kernel required by:

```text
P_transfer:
  A = (eta/2) I_3
```

Results:

```text
C1 boundary momentum:
  native object:
    Pi_f = -qR/2.
  kernel supplied:
    scalar edge momentum, no H1 channel matrix.
  verdict:
    does not supply I_3 transfer kernel.

radial-angular curvature:
  native object:
    K_rad/K_S2 = q/2.
  kernel supplied:
    scalar curvature ratio, no H1 channel matrix.
  verdict:
    does not supply I_3 transfer kernel.

H1/S2 projection:
  native object:
    <n_a n_b> = delta_ab/3.
  kernel supplied:
    normalized identity I_3/3.
  verdict:
    supplies eta projection, not eta/2 I_3 action.

round S2 intrinsic metric:
  native object:
    gamma_AB = R^2 omega_AB.
  kernel supplied:
    2D tangent metric on S2.
  verdict:
    not a 3D H1 channel identity.

S2 shape operator:
  native object:
    s^A_B = (1/R) delta^A_B.
  kernel supplied:
    2D tangent identity on embedded S2.
  verdict:
    not a 3D H1 channel identity.

CP1/Hopf bridge:
  native object:
    CP1 -> S2 via phase-invariant bilinears.
  kernel supplied:
    maps compact data into existing H1/S2 orientation.
  verdict:
    does not add an independent I_3 transfer kernel.

E1 relative-shape plane:
  native object:
    two-dimensional plane orthogonal to common amplitude.
  kernel supplied:
    2D relative-shape identity if a shape action exists.
  verdict:
    not the universal 3D scalar H1 transfer kernel.
```

Two-hundredth verdict:

```text
No current native edge variable supplies the required eta/2 I_3 transfer
action.
```

The known metric pieces supply:

```text
scalars,
tangent identities,
or the normalized H1/S2 projector I_3/3.
```

Therefore:

```text
P_transfer remains a separate postulate unless a new native edge kernel is
uncovered.
```

This is a meaningful negative result:

```text
P_phi0 appears native/minimal;
P_transfer is not yet uncovered from the metric.
```

## 216. Edge quantum composition laws

Implemented in `native_edge_quantum_composition_laws.py`.

If `P_phi0` is banked:

```text
eta = 1/18
```

This gives an edge quantum. It does not by itself give a ladder.

Possible exact composition laws:

```text
independent action addition:
  exact rule:
    S_total = sum_i S_i.
  consequence:
    weights multiply: exp(-S_total)=prod_i exp(-S_i).
  status:
    exact if edge quanta are independent action terms.

glued boundary half-action:
  exact rule:
    two half-boundaries glue to one full boundary action.
  consequence:
    one side carries eta/2; glued internal boundary carries eta.
  status:
    exact bookkeeping if the object is a composable boundary kernel.

shared variable merge:
  exact rule:
    two nominal nodes constrained to the same edge variable count once.
  consequence:
    depth is reduced; multiplication overcounts.
  status:
    exact constraint-counting warning.

correlated edge block:
  exact rule:
    edge variables form one coupled block rather than product factors.
  consequence:
    trace/eigenvalues of full block replace gamma^n.
  status:
    exact alternative if metric supplies a coupled kernel.

channel trace:
  exact rule:
    Tr exp(-a I_N) = N exp(-a).
  consequence:
    factor N appears only for an actual N-channel identity kernel.
  status:
    exact but conditional.

normalized projection:
  exact rule:
    <n_a n_b> = delta_ab/3.
  consequence:
    gives projection factor 1/3; does not by itself give multiplicity 3.
  status:
    exact projection, not transfer multiplication.
```

Two-hundred-first verdict:

```text
The metric has exposed an edge quantum.
```

A mass ladder requires:

```text
an exact composition law for multiple edge quanta.
```

The allowed composition laws are:

```text
action addition,
boundary gluing,
variable merging,
coupled-block tracing,
channel tracing.
```

They are not interchangeable.

Therefore:

```text
do not force gamma as the composition law unless the edge kernel supplies it.
```

## 217. Edge quantum current status

Implemented in `native_edge_quantum_current_status.py`.

Current status:

```text
edge quantum eta:
  status:
    resolved if P_phi0 is banked.
  reason:
    P_phi0 plus exact H1/S2 projection gives eta = 1/18.

edge quantum existence:
  status:
    strong native candidate.
  reason:
    same unit appears as C1 momentum, radial-angular curvature share,
    and phi0 edge datum.

composition law:
  status:
    open.
  reason:
    current metric edge has not supplied an independent scalar I3 transfer kernel.

ladder multiplier gamma:
  status:
    conditional/postulate.
  reason:
    requires channel trace over eta/2 I3.

typed depth:
  status:
    diagnostic.
  reason:
    exact geometry supports ingredients but not transfer-node independence.

mass hierarchy:
  status:
    not resolved.
  reason:
    requires composition law plus typed depth and coefficients.
```

Two-hundred-second verdict:

```text
The metric appears to be doing edge closure first.
```

The hierarchy, if native, should be searched for as:

```text
an exact composition law of edge quanta,
```

not forced as:

```text
a transfer multiplier.
```

## 218. Composition candidate support

Implemented in `native_composition_candidate_support.py`.

Classify composition candidates by what the metric currently supports.

```text
single phi0 edge quantum:
  metric support:
    C1 momentum, radial-angular curvature, H1/S2 projection.
  missing piece:
    derivation of P_phi0 if not banked.
  current verdict:
    strong native candidate.

two-sided boundary gluing:
  metric support:
    boundary variations naturally have sides; glued boundaries add actions.
  missing piece:
    actual edge kernel whose side action is eta/2.
  current verdict:
    plausible composition framework, not yet a UDT result.

channel trace over H1:
  metric support:
    three H1 components and round-S2 projection geometry.
  missing piece:
    scalar identity action eta/2 I3.
  current verdict:
    conditional only.

node product over typed graph:
  metric support:
    exact CP1/Hopf bridge and exact E1 relative-shape plane.
  missing piece:
    independence of graph nodes as action terms.
  current verdict:
    diagnostic only.

coupled edge block:
  metric support:
    orchestra frame and shared variables suggest correlations are possible.
  missing piece:
    explicit native coupled kernel and its spectrum.
  current verdict:
    open alternative; may replace gamma^n.

branch-specific source running:
  metric support:
    q-flow allows s(t) or branch data to affect q.
  missing piece:
    native exact running law.
  current verdict:
    open; would modify eta rather than preserve universal gamma.
```

Two-hundred-third verdict:

```text
The only strongly supported object is the single phi0 edge quantum.
```

All multi-edge composition laws remain open until:

```text
a native edge kernel
```

or:

```text
a native coupled block
```

is found.

This redirects the search:

```text
do not ask which composition law fits;
ask which composition law the metric actually provides.
```

## 219. Boundary topology composition audit

Implemented in `native_boundary_topology_composition_audit.py`.

Topology constrains composition.

```text
single negative-phi cell with regularized/excised core:
  spatial form:
    [core, phi0] x S2.
  boundary components:
    core-side S2 plus phi0 S2.
  composition consequence:
    at most two radial boundary components before adding bundle variables.

single negative-phi cell with singular endpoint not treated as boundary:
  spatial form:
    (0, phi0] x S2 with singular endpoint.
  boundary components:
    phi0 S2 only.
  composition consequence:
    only one explicit radial edge quantum.

two cells glued at a shared boundary:
  spatial form:
    [a,b] x S2 union [b,c] x S2.
  boundary components:
    shared b boundary is internal after gluing.
  composition consequence:
    shared variables merge; boundary action should not be double-counted.

disconnected cells:
  spatial form:
    disjoint union of intervals x S2.
  boundary components:
    boundary components add over disconnected pieces.
  composition consequence:
    actions can add if cells are independent.
```

Two-hundred-fourth verdict:

```text
A single spherical metric cell does not provide arbitrary radial
transfer-node depth.
```

Repeated nodes require:

```text
disconnected cells,
independent boundary/bundle variables,
or an explicit edge graph.
```

So if the typed depths:

```text
5 and 7
```

survive, they must come from:

```text
bundle/edge variables living on the boundary,
```

not from:

```text
multiple radial copies.
```

## 220. C1 gluing composition audit

Implemented in `native_c1_gluing_composition_audit.py`.

C1 gluing gives exact constraints:

```text
smooth gluing:
  exact condition:
    f and f' match across the interface.
  action consequence:
    no interface source; C1 bulk actions add over intervals.
  verdict:
    no new edge quantum at the glued interface.

continuous f with slope jump:
  exact condition:
    f matches, Delta f' != 0.
  action consequence:
    interface source J with Delta Pi_f = (1/2)R^2 Delta f'.
  verdict:
    one localized edge datum, not two independent nodes.

flat exterior with inner q:
  exact condition:
    f = 1, f'_out = 0, f'_in = -q/R.
  action consequence:
    Delta Pi_f = qR/2; P_phi0 fixes q = 1/3 if banked.
  verdict:
    single phi0 edge quantum.

two nominal nodes sharing one edge variable:
  exact condition:
    same f, Pi_f, or H1/S2 direction variable.
  action consequence:
    constraint identifies variables.
  verdict:
    nodes merge; product counting overcounts.
```

Two-hundred-fifth verdict:

```text
C1 gluing supplies additive bulk action and localized interface momentum
jumps.
```

It does not by itself:

```text
turn one phi0 edge quantum into a multiplicative ladder.
```

This reinforces:

```text
the ladder, if native, must come from a boundary/bundle composition law,
not ordinary radial gluing alone.
```

## 221. C1 edge phase-space audit

Implemented in `native_c1_edge_phase_space_audit.py`.

If a ladder composition law is native, there should be actual edge degrees
of freedom with an action or symplectic pairing.

Audit:

```text
bare C1 boundary variation:
  condition:
    delta S_C1 has edge term Pi_f delta f.
  phase-space consequence:
    the scalar edge canonical data are (f, Pi_f).
  verdict:
    one radial scalar canonical pair before boundary conditions.

phi0 value condition:
  condition:
    f = 1 at the phi0 boundary.
  phase-space consequence:
    Dirichlet value removes delta f at the boundary.
  verdict:
    no free f variation if imposed.

P_phi0 momentum condition:
  condition:
    -Pi_f/R = 1/6.
  phase-space consequence:
    Neumann momentum is fixed.
  verdict:
    fixes the remaining scalar edge momentum.

H1/S2 orientation:
  condition:
    n_a n_a = 1 and <n_a n_b> = delta_ab/3.
  phase-space consequence:
    kinematic orientation arena, but no C1 conjugate momentum.
  verdict:
    not a dynamical edge phase space from C1 alone.

shape / embedding data:
  condition:
    s^A_B and n(s)^A_B are isotropic at phi0.
  phase-space consequence:
    carry q as scalar embedding data, no independent traceless modes.
  verdict:
    not enough for multi-node dynamics.
```

Two-hundred-sixth verdict:

```text
Scalar C1 gives one edge canonical pair (f, Pi_f).
```

At phi0:

```text
f = 1
P_phi0 fixes Pi_f
```

so that scalar pair is fixed.

H1/S2 supplies:

```text
kinematic orientation,
```

but C1 alone does not supply:

```text
an angular edge phase space or node graph.
```

## 222. Edge bundle-action requirement

Implemented in `native_edge_bundle_action_requirement.py`.

To get a native ladder, the metric must supply more than the scalar phi0
edge quantum.

Requirements:

```text
angular edge variables:
  exact need:
    boundary variables such as n_a or relative-shape coordinates must
    appear in an action.
  current status:
    present as geometry/labels, not yet as edge dynamics.

conjugate structure:
  exact need:
    edge variables need a symplectic pairing or quadratic action kernel.
  current status:
    not supplied by scalar C1.

kernel spectrum:
  exact need:
    the edge action must have exact eigenvalues that define the composition law.
  current status:
    unknown; no native kernel found.

node independence:
  exact need:
    multiple variables must factor as independent action terms.
  current status:
    not established; shared variables may merge.

channel trace:
  exact need:
    factor 3 requires an actual three-channel identity kernel.
  current status:
    not supplied by normalized H1/S2 projection alone.
```

Two-hundred-seventh verdict:

```text
The missing ladder object is a boundary/bundle action for angular or
relative-shape edge variables.
```

That object has not been uncovered.

This keeps the frame clean:

```text
P_phi0 = native edge quantum candidate.
composition law = still missing boundary/bundle dynamics.
```

## 223. S2 ell=1 identity-kernel audit

Implemented in `native_s2_l1_identity_kernel_audit.py`.

The normalized H1/S2 projector:

```text
<n_a n_b> = delta_ab/3
```

does not supply the required transfer kernel:

```text
I_3.
```

But the round S2 Laplacian has an exact identity structure on each
angular eigenspace:

```text
Delta_S2 Y_lm = -l(l+1)Y_lm/R^2.
```

For:

```text
l = 1
```

the eigenspace has dimension:

```text
2l + 1 = 3
```

and:

```text
-R^2 Delta_S2 |_{l=1} = 2 I_3.
```

Two-hundred-eighth verdict:

```text
The round S2 l=1 Laplacian supplies a native three-dimensional identity
structure.
```

This is a better candidate for the `I_3` part of `P_transfer` than:

```text
the normalized second-moment projector I_3/3.
```

But it still does not derive:

```text
the eta/2 coefficient,
the exponential transfer rule,
or node independence.
```

The refined missing object is:

```text
a boundary action coupling the phi0 edge quantum eta to the l=1
angular identity kernel.
```

## 224. Angular action candidate audit

Implemented in `native_angular_action_candidate_audit.py`.

Audit native angular action candidates:

```text
S2 Laplacian restricted to l=1:
  exact metric fact:
    -R^2 Delta_S2 = 2 I_3 on l=1.
  can supply I3:
    yes.
  can supply action weight:
    no; needs coupling to eta or a boundary action.
  verdict:
    best native angular kernel candidate.

S2 Killing algebra:
  exact metric fact:
    round S2 has three SO(3) Killing generators.
  can supply I3:
    gives a three-generator algebra, not an action kernel by itself.
  can supply action weight:
    no.
  verdict:
    supports channel arena, not transfer weight.

Gauss-Bonnet integral:
  exact metric fact:
    integral_S2 R2 dA = 8 pi, fixed by topology.
  can supply I3:
    no.
  can supply action weight:
    topological constant; no local transfer eigenvalues.
  verdict:
    not P_transfer.

S2 tangent metric:
  exact metric fact:
    gamma_AB = R^2 omega_AB.
  can supply I3:
    no; tangent space is two-dimensional.
  can supply action weight:
    no.
  verdict:
    intrinsic geometry, not H1 channel kernel.

normalized H1/S2 second moment:
  exact metric fact:
    <n_a n_b> = delta_ab/3.
  can supply I3:
    supplies I_3/3, not I_3.
  can supply action weight:
    supplies projection factor for eta.
  verdict:
    eta projection, not transfer kernel.
```

Two-hundred-ninth verdict:

```text
The metric does contain a native I_3 structure:
the l=1 Laplacian eigenspace.
```

What remains missing is:

```text
the boundary action that couples the phi0 edge quantum eta to that
l=1 identity kernel.
```

This is a real improvement over the previous negative result:

```text
I_3 is native to the angular metric,
but the eta/2 transfer action is not yet derived.
```

## 225. Normalized ell=1 transfer-kernel candidate

Implemented in `native_l1_normalized_transfer_kernel.py`.

The round S2 Laplacian gives:

```text
-R^2 Delta_S2 |_{ell=1} = 2 I_3
```

Normalize by the `ell=1` eigenvalue:

```text
L_1 = (-R^2 Delta_S2)/2 restricted to ell=1
L_1 = I_3
```

Given banked `P_phi0`:

```text
eta = 1/18
```

the candidate side action is:

```text
A_side = (eta/2) L_1
       = (eta/2) I_3
```

Equivalently:

```text
A_side = (eta/4)(-R^2 Delta_S2)|_{ell=1}
eta/4 = 1/72
```

Then:

```text
Tr exp(-A_side) = 3 exp(-eta/2)
```

Two-hundred-tenth verdict:

```text
The I_3 channel identity is native to the metric angular Laplacian.
```

What remains postulated or to derive is:

```text
1. the side-action coupling A_side = (eta/2)L_1,
2. why the transfer uses the normalized ell=1 kernel,
3. why independent edge nodes multiply.
```

So the refined `P_transfer` is:

```text
P_transfer:
  the one-sided phi0 edge action eta/2 couples to the normalized
  ell=1 angular Laplacian kernel.
```

This is smaller and more native than:

```text
postulate a bare 3 exp(-eta/2).
```

## 226. Transfer status after Laplacian audit

Implemented in `native_transfer_status_after_laplacian.py`.

Updated status:

```text
I_3 channel identity:
  previous status:
    not found in scalar edge variables.
  updated status:
    found in round S2 ell=1 Laplacian eigenspace.

eta scalar:
  previous status:
    resolved by P_phi0 if banked.
  updated status:
    unchanged.

eta/2 side action:
  previous status:
    candidate P_transfer condition.
  updated status:
    still needs boundary-gluing/action derivation.

exponential trace:
  previous status:
    exact conditional identity.
  updated status:
    unchanged.

node independence:
  previous status:
    open.
  updated status:
    unchanged; not supplied by Laplacian degeneracy.
```

Two-hundred-eleventh verdict:

```text
P_transfer is less unsupported than before.
```

The `I_3` part is:

```text
native to the angular metric.
```

The remaining non-derived pieces are:

```text
boundary action coupling eta/2 to the normalized ell=1 kernel,
independent composition over nodes.
```

## 227. Lowest nontrivial angular sector audit

Implemented in `native_lowest_nontrivial_angular_sector_audit.py`.

The angular sector hierarchy of the round S2 metric is exact:

```text
ell = 0:
  dimension:
    1.
  -R^2 Delta eigenvalue:
    0.
  metric role:
    constant scalar on S2.
  transfer relevance:
    no angular identity variation; no nonzero angular Laplacian kernel.

ell = 1:
  dimension:
    3.
  -R^2 Delta eigenvalue:
    2.
  metric role:
    lowest nonconstant angular sector; coordinate-vector/H1 arena.
  transfer relevance:
    first native angular identity kernel with I3 after normalization.

ell = 2:
  dimension:
    5.
  -R^2 Delta eigenvalue:
    6.
  metric role:
    quadrupolar/traceless-shape sector.
  transfer relevance:
    higher angular shape response, not minimal edge identity.
```

Two-hundred-twelfth verdict:

```text
ell = 1 is selected as the lowest nonconstant angular identity sector
of the round S2 metric.
```

This is:

```text
a metric fact,
```

not:

```text
a Standard Model import.
```

It explains why the first transfer-kernel candidate should use:

```text
the normalized ell=1 Laplacian
```

if any angular kernel is used.

## 228. phi0-to-ell=1 coupling hypothesis

Implemented in `native_phi0_l1_coupling_hypothesis.py`.

The compact native coupling hypothesis is:

```text
the phi0 edge quantum acts on the lowest nonconstant angular identity
sector through the normalized ell=1 Laplacian kernel.
```

Pieces:

```text
edge scalar:
  exact piece:
    P_phi0 supplies eta = 1/18 if banked.
  open piece:
    derivation of P_phi0 if not banked.

angular kernel:
  exact piece:
    L1 = (-R^2 Delta_S2)/2 restricted to ell=1 equals I3.
  open piece:
    none for I3 identity.

coupling:
  exact piece:
    A_side = (eta/2)L1 would give the transfer kernel.
  open piece:
    why the edge scalar couples as eta/2 to L1.

trace:
  exact piece:
    Tr exp[-(eta/2)I3] = 3 exp(-eta/2).
  open piece:
    why trace over channels is the physical composition operation.
```

Two-hundred-thirteenth verdict:

```text
This is a compact native coupling hypothesis, not a derivation.
```

It is the current best in-between target:

```text
not broad pondering,
not ladder fitting,
but exact scrutiny of phi0 edge action on ell=1.
```

## 229. eta/2 boundary-condition audit

Implemented in `native_eta_half_boundary_condition_audit.py`.

The side-action half:

```text
eta/2
```

has exact sources only under specific conditions.

```text
two-sided boundary kernel:
  exact rule:
    full boundary action eta is split as eta/2 on each side.
  applies if:
    the phi0-to-ell=1 coupling is a composable boundary kernel.
  verdict:
    valid source of eta/2 if boundary-kernel structure is present.

interface jump alone:
  exact rule:
    Delta Pi_f gives q/2 and eta after projection.
  applies if:
    only C1 momentum jump is considered.
  verdict:
    does not by itself split eta into eta/2.

single exterior boundary:
  exact rule:
    one boundary component has one edge datum.
  applies if:
    phi0 is treated as only an outer boundary, not a glued interface.
  verdict:
    no automatic half-factor.

trace square-root convention:
  exact rule:
    assign exp(-eta/2) so two sides multiply to exp(-eta).
  applies if:
    there is a symmetric transfer amplitude whose square gives boundary weight.
  verdict:
    valid only if amplitude/kernel interpretation is native.
```

Two-hundred-fourteenth verdict:

```text
eta/2 is exact for a two-sided composable boundary kernel or native
symmetric transfer amplitude.
```

It is not derived by:

```text
the edge quantum alone.
```

The missing condition is:

```text
kernel/amplitude structure at phi0.
```

So the current refined bridge is:

```text
P_phi0 supplies eta,
ell=1 Laplacian supplies I3,
boundary-kernel structure would supply eta/2.
```

## 230. phi0-to-ell=1 boundary kernel candidates

Implemented in `native_phi0_l1_boundary_kernel_candidates.py`.

Native boundary-kernel candidates:

```text
C1 scalar boundary kernel:
  form:
    B_phi0(f, Pi_f) or fixed -Pi_f/R.
  native parts:
    C1 boundary momentum and P_phi0.
  supplies bridge:
    no angular L1 operator.
  verdict:
    supplies eta, not transfer kernel.

angular Laplacian kernel:
  form:
    L1 = (-R^2 Delta_S2)/2 on ell=1.
  native parts:
    round S2 metric.
  supplies bridge:
    supplies I3, no eta coefficient.
  verdict:
    supplies channel identity, not edge action.

separable product kernel:
  form:
    A_side = (eta/2) L1.
  native parts:
    P_phi0 edge scalar times normalized ell=1 Laplacian.
  supplies bridge:
    yes, if side-action coupling is native.
  verdict:
    best current bridge candidate; coupling still not derived.

rank-one direction kernel:
  form:
    A = (eta/2) n n^T.
  native parts:
    H1/S2 unit direction.
  supplies bridge:
    no; eigenvalues are eta/2, 0, 0.
  verdict:
    wrong trace for P_transfer.

projected normalized kernel:
  form:
    A = (eta/2)(I3/3).
  native parts:
    H1/S2 second moment.
  supplies bridge:
    no; gives 3 exp(-eta/6).
  verdict:
    eta projection, not transfer.

ell=0 scalar kernel:
  form:
    L0 = 0 or constant mode.
  native parts:
    round S2 scalar sector.
  supplies bridge:
    no nonzero angular identity action.
  verdict:
    not mass-edge angular identity.
```

Two-hundred-fifteenth verdict:

```text
The only candidate with the right bridge is the separable product
A_side = (eta/2)L1.
```

It is native in parts:

```text
eta from P_phi0,
L1 from the round S2 metric.
```

But:

```text
the coupling that forms the product is still the missing object.
```

## 231. Coupled kernel exact requirements

Implemented in `native_coupled_kernel_exact_requirements.py`.

Exact requirements for the coupled kernel:

```text
scalar edge quantum:
  exact requirement:
    eta must be fixed by phi0 edge data.
  current status:
    available if P_phi0 is banked.

angular identity kernel:
  exact requirement:
    L1 = (-R^2 Delta_S2)/2 must equal I3 on ell=1.
  current status:
    derived metric fact.

separable coupling:
  exact requirement:
    edge action must factor as scalar eta/2 times L1.
  current status:
    not derived.

boundary-sidedness:
  exact requirement:
    eta must split into eta/2 per side by gluing or amplitude structure.
  current status:
    not derived for phi0-to-L1 coupling.

channel trace:
  exact requirement:
    physical composition must trace over ell=1 channels.
  current status:
    not derived.

composition over nodes:
  exact requirement:
    multiple kernels must be independent or have known coupled spectrum.
  current status:
    not derived.
```

Two-hundred-sixteenth verdict:

```text
The metric now supplies the scalar and angular factors.
```

The missing native object is:

```text
the separable boundary coupling and its composition rule.
```

This is the tightest current formulation of the bridge problem.

## 232. Boundary tensor-product structure

Implemented in `native_boundary_tensor_product_structure.py`.

The product form:

```text
A_side = (eta/2)L1
```

has a native structural interpretation.

Boundary factor spaces:

```text
radial/edge scalar factor:
  factor space:
    one-dimensional scalar edge data at phi0.
  native operator:
    multiplication by eta or eta/2 if a side kernel exists.
  role:
    sets edge action scale.

angular ell=1 factor:
  factor space:
    H_ell=1(S2), dimension 3.
  native operator:
    L1 = (-R^2 Delta_S2)/2 = I3.
  role:
    sets lowest nonconstant angular identity kernel.
```

The boundary tensor product is:

```text
edge scalar space tensor H_ell=1(S2)
```

with operator form:

```text
scalar_edge_action tensor L1.
```

If:

```text
scalar_edge_action = eta/2
```

then:

```text
A_side = (eta/2)L1.
```

Two-hundred-seventeenth verdict:

```text
The product form is structurally native to a boundary field/operator:
radial edge scalars multiply angular boundary operators.
```

What remains missing is the derivation that:

```text
1. the scalar side action is eta/2,
2. this tensor product is the physical transfer kernel.
```

This means the coupling is no longer arbitrary in form:

```text
it is the natural tensor product of phi0 scalar edge data with the
lowest nonconstant angular operator.
```

## 233. Angular invariant bridge between phi spaces

Implemented in `native_angular_invariant_bridge_phi_spaces.py`.

This incorporates the earlier working intuition:

```text
negative-phi matter space must remain accessible through a positive-phi /
scalar-background side, and the bridge is the angular spectrum invariant
under r* changes.
```

Exact bridge facts:

```text
angular metric:
  exact statement:
    g_AB = r^2 omega_AB on both phi signs.
  relevance:
    intrinsic S2 geometry is the shared interface arena.

angular Laplacian scaling:
  exact statement:
    Delta_S2 = r^-2 Delta_unit.
  relevance:
    normalized operator -r^2 Delta_S2 is independent of r*.

angular eigenvalues:
  exact statement:
    -r^2 Delta_S2 Y_lm = l(l+1) Y_lm.
  relevance:
    angular spectrum is invariant under scale changes and phi sign.

ell=1 bridge:
  exact statement:
    L1 = (-r^2 Delta_S2)/2 equals I3 on ell=1.
  relevance:
    lowest nonconstant angular identity sector is common to both sides.

phi0 interface:
  exact statement:
    f = 1 at phi0 while angular operator remains the same across the interface.
  relevance:
    negative-phi edge can couple to exterior/scalar background through
    angular invariants.
```

Two-hundred-eighteenth verdict:

```text
The angular spectrum is the natural bridge between negative-phi matter
space and the positive-phi/scalar background.
```

Reason:

```text
the normalized angular operators are invariant under r* and phi sign.
```

This helps the current bridge problem because:

```text
L1 = I3 is not only native to the angular metric;
it is also the common operator seen from both sides of phi0.
```

## 234. Two-sided phi bridge interpretation

Implemented in `native_two_sided_phi_bridge_interpretation.py`.

The two sides are:

```text
negative-phi side:
  role:
    matter-side radial closure / edge momentum.
  shared object:
    phi0 S2 angular spectrum.
  consequence:
    supplies the edge scalar eta through P_phi0 if banked.

positive-phi / scalar-background side:
  role:
    accessibility/exterior continuation arena.
  shared object:
    same normalized angular spectrum.
  consequence:
    provides the other side of the angular bridge.

phi0 bridge:
  role:
    interface where both sides share f = 1 and the same S2 operator.
  shared object:
    L1 = I3 on ell=1.
  consequence:
    makes a two-sided angular boundary-kernel interpretation plausible.
```

Two-hundred-nineteenth verdict:

```text
This gives a native reason to revisit the eta/2 half-factor.
```

If phi0 is a bridge between:

```text
negative-phi matter closure
```

and:

```text
positive-phi/scalar accessibility,
```

then:

```text
the edge quantum may be naturally two-sided.
```

This is still:

```text
an interpretation,
```

until:

```text
the boundary action is derived.
```

But it is useful because it ties the half-factor question to the same
invariant angular bridge that already produced:

```text
L1 = I3.
```

## 235. phi-sign mirror bridge audit

Implemented in `native_phi_sign_mirror_bridge_audit.py`.

The two-sided bridge has native metric support.

```text
inside-out phi mirror:
  exact statement:
    phi -> -phi swaps the positive-phi and negative-phi radial/time weights.
  consequence:
    matter-side and gravity/scalar-side sectors are related by the same
    metric form.

angular invariance under phi mirror:
  exact statement:
    g_AB = r^2 omega_AB is unchanged by phi -> -phi.
  consequence:
    the intrinsic angular spectrum is common to both sides.

phi0 fixed surface:
  exact statement:
    at phi = 0, f = e^(-2phi) = 1.
  consequence:
    both phi signs meet at the same angular geometry and flat radial value.

normalized angular operator:
  exact statement:
    -r^2 Delta_S2 has eigenvalues l(l+1), independent of phi.
  consequence:
    angular modes can carry information across the phi-sign interface.

ell=1 identity bridge:
  exact statement:
    L1 = (-r^2 Delta_S2)/2 = I3 on ell=1.
  consequence:
    the lowest nonconstant angular identity sector is shared by both phi sides.
```

Two-hundred-twentieth verdict:

```text
The two-sided bridge is native at the level of metric geometry.
```

Reason:

```text
phi changes radial/time weights,
while the normalized angular spectrum remains the common invariant across
both phi signs.
```

## 236. Two-sided half-action status

Implemented in `native_two_sided_half_action_status.py`.

Status of the half-action idea:

```text
two-sided phi bridge:
  support:
    phi -> -phi mirror plus phi-blind angular operator.
  limit:
    does not by itself define an action split.
  status:
    native geometric bridge.

shared ell=1 kernel:
  support:
    L1 = I3 on both sides of phi0.
  limit:
    does not decide transfer direction or trace operation.
  status:
    derived metric fact.

eta/2 per side:
  support:
    natural if the full edge action eta is shared by two bridge sides.
  limit:
    requires a boundary action or amplitude structure.
  status:
    plausible coupling rule, not derived.

gamma trace:
  support:
    exact if A_side = (eta/2)L1 and physical operation is channel trace.
  limit:
    trace/composition interpretation remains open.
  status:
    conditional identity.
```

Two-hundred-twenty-first verdict:

```text
The two-sided phi bridge makes eta/2 plausible and native-looking,
but does not prove it.
```

The exact upgrade still requires:

```text
a boundary action or amplitude whose two sides compose to eta.
```

This keeps the intuition useful without overclaiming it.

## 237. GR boundary-kernel atlas

Implemented in `native_gr_boundary_kernel_atlas.py`.

The relevant GR/math corpus is not ordinary Einstein sourcing. The sharper
atlas is boundary-kernel theory:

```text
heat kernel / spectral semigroup:
  GR/math role:
    uses exp(-t operator) and exact semigroup composition
    K(t1)K(t2)=K(t1+t2).
  UDT relevance:
    directly matches a boundary operator L1 and exponential transfer structure.
  status:
    highest-priority atlas object.

Dirichlet-to-Neumann map:
  GR/math role:
    maps boundary values to normal derivatives for elliptic boundary problems.
  UDT relevance:
    P_phi0 is exactly a boundary momentum/normal-derivative condition at f=1.
  status:
    promising atlas object.

Calderon projector / Cauchy data space:
  GR/math role:
    splits allowable boundary Cauchy data and supports gluing formulas.
  UDT relevance:
    could formalize two-sided phi bridge as a boundary data split.
  status:
    promising but not derived.

BFK determinant gluing:
  GR/math role:
    factorizes determinants of operators on glued manifolds using boundary
    operators.
  UDT relevance:
    may explain composition of boundary spectra without inventing a force.
  status:
    caution: determinant factors can overdominate.

Hamilton-Jacobi boundary functional:
  GR/math role:
    on-shell action as a functional of boundary data; momenta are boundary
    derivatives.
  UDT relevance:
    C1 Pi_f is already an HJ-type boundary derivative.
  status:
    already partially used.

corner / joint terms:
  GR/math role:
    codimension-2 terms where boundary pieces meet.
  UDT relevance:
    phi0 is a radial/angular edge where scalar and angular data meet.
  status:
    promising but not yet enough.

covariant phase space edge modes:
  GR/math role:
    boundary degrees of freedom required by gauge/gravity symplectic structure.
  UDT relevance:
    could supply angular edge dynamics missing from scalar C1.
  status:
    open atlas object.
```

Two-hundred-twenty-second verdict:

```text
The most direct GR-math pointer is spectral boundary-kernel theory:
heat kernels, Dirichlet-to-Neumann maps, and gluing projectors.
```

These are:

```text
maps,
```

not:

```text
imported mechanisms.
```

UDT still has to supply:

```text
the actual phi0 boundary operator and action time.
```

## 238. ell=1 heat-kernel semigroup audit

Implemented in `native_l1_heat_kernel_semigroup.py`.

Metric angular fact:

```text
L1 = (-R^2 Delta_S2)/2 |_{ell=1} = I3
```

Define the spectral boundary kernel:

```text
U(t) = exp(-t L1)
```

Since:

```text
L1 = I3
```

we have:

```text
U(t) = exp(-t) I3
Tr U(t) = 3 exp(-t)
```

Exact semigroup law:

```text
U(t1) U(t2) = U(t1+t2)
```

For a two-sided split of the edge quantum:

```text
eta = 1/18
side time = eta/2 = 1/36
U(eta/2) U(eta/2) = U(eta)
```

One-side trace:

```text
Tr U(eta/2) = 3 exp(-eta/2)
```

Full glued trace:

```text
Tr U(eta) = 3 exp(-eta)
```

Two-hundred-twenty-third verdict:

```text
Spectral kernel math supplies the exponential, the trace, and the
two-sided composition law once L1 and the time parameter are given.
```

Remaining UDT condition:

```text
Identify the phi0 edge action time with eta,
or side time with eta/2.
```

This is the closest GR/math object so far to the missing transfer structure.

## 239. Dirichlet-to-Neumann / Calderon phi0 audit

Implemented in `native_dtn_calderon_phi0_audit.py`.

Boundary data translation:

```text
Dirichlet data:
  mathematical role:
    boundary value of a field.
  phi0 translation:
    f = 1 at phi0.
  verdict:
    present exactly.

Neumann data:
  mathematical role:
    normal derivative / conjugate boundary momentum.
  phi0 translation:
    Pi_f = -R/6 if P_phi0 is banked.
  verdict:
    present as P_phi0.

Dirichlet-to-Neumann map:
  mathematical role:
    operator mapping boundary values to normal derivatives.
  phi0 translation:
    would derive Pi_f from f and angular edge data.
  verdict:
    missing native map.

Calderon projector:
  mathematical role:
    projector onto boundary data that extend to a valid bulk solution.
  phi0 translation:
    would select admissible two-sided phi bridge Cauchy data.
  verdict:
    promising atlas object, not yet constructed.

two-sided Cauchy data:
  mathematical role:
    boundary data from both sides of an interface.
  phi0 translation:
    negative-phi side plus positive-phi/scalar side sharing angular spectrum.
  verdict:
    matches the current bridge picture.
```

Two-hundred-twenty-fourth verdict:

```text
GR/PDE boundary math points to the missing object as a native
Dirichlet-to-Neumann or Calderon-type map for the phi0 bridge.
```

Such a map would upgrade:

```text
P_phi0
```

from:

```text
postulate
```

to:

```text
boundary selection.
```

## 240. ell=1 Poisson semigroup / DtN audit

Implemented in `native_l1_poisson_semigroup_dtn.py`.

The heat-kernel idea has a sharper GR/PDE cousin: the Poisson
semigroup and Dirichlet-to-Neumann map.

Exact product-collar boundary model:

```text
P = -d_x^2 + L
x >= 0 is normal distance from the boundary
```

For boundary data:

```text
u(0) = u0
```

the decaying extension is:

```text
u(x) = exp(-x sqrt(L)) u0
```

The Dirichlet-to-Neumann map is:

```text
-u'(0) = sqrt(L) u0
```

For the normalized `ell=1` angular operator:

```text
L = L1 = I3
sqrt(L1) = I3
```

therefore:

```text
u(x) = exp(-x) u0
Tr exp(-x sqrt(L1)) = 3 exp(-x)
```

If the phi0 side-length/action parameter is:

```text
x = eta/2 = 1/36
```

then:

```text
one-side trace = 3 exp(-eta/2)
```

Two-hundred-twenty-fifth verdict:

```text
This is exact for the product-collar operator -d_x^2 + L1.
```

UDT must still show:

```text
1. the two-sided phi0 bridge is governed by this product-collar Poisson kernel,
2. the side parameter x equals eta/2.
```

This is a better GR-math pointer than the ordinary heat kernel because:

```text
it is explicitly a boundary-extension / Dirichlet-to-Neumann object.
```

## 241. Boundary-normal operator caveat

Implemented in `native_boundary_normal_operator_caveat.py`.

The Poisson semigroup result must not be overclaimed.

Exact layers:

```text
collar coordinates:
  exact statement:
    near a smooth boundary, a metric can be written as d rho^2 + h_rho.
  implication:
    there is an exact normal/tangential split of variables.

product collar:
  exact statement:
    h_rho = h_0 throughout the collar.
  implication:
    Poisson kernel exp(-rho sqrt(L_h0)) is exact.

non-product collar:
  exact statement:
    h_rho varies with rho.
  implication:
    extrinsic-curvature and h_rho variation terms modify the exact kernel.

phi0 boundary value:
  exact statement:
    at phi0, f = 1 and h_0 = R^2 omega.
  implication:
    the boundary angular operator L1 is exact at the interface.

UDT missing step:
  exact statement:
    the exact bridge kernel has not been derived from the full phi0 collar.
  implication:
    do not treat the product-collar Poisson kernel as a conclusion yet.
```

Two-hundred-twenty-sixth verdict:

```text
The product-collar Poisson semigroup is the right atlas object.
```

But UDT must derive:

```text
that the phi0 bridge reduces to that exact boundary-normal kernel.
```

Otherwise:

```text
curvature/collar variation may change the composition law.
```

## 243. Positional-dilation boundary-operator refactor

Implemented in `native_positional_dilation_boundary_operator_refactor.py`.

This is the key caution for importing GR/PDE boundary kernels.

The UDT spatial metric is:

```text
dl^2 = f^-1 dr^2 + r^2 dOmega^2
```

So normal distance is:

```text
d rho = dr/sqrt(f)
```

and:

```text
dr/d rho = sqrt(f)
```

Thus the collar is:

```text
d rho^2 + r(rho)^2 dOmega^2
```

not automatically:

```text
d rho^2 + R^2 dOmega^2.
```

The exact spatial Laplacian is:

```text
Delta u = u_rhorho + 2(r_rho/r)u_rho + r^-2 Delta_S2 u
```

For an angular mode:

```text
u = a(rho)Y_lm
```

the harmonic-extension equation becomes:

```text
-a'' - 2(r'/r)a' + l(l+1)a/r^2 = 0
```

Using the Liouville transform:

```text
v = r a
```

gives:

```text
-v'' + [r''/r + l(l+1)/r^2]v = 0
```

The UDT radial acceleration is:

```text
r'' = d^2r/d rho^2 = f'/2
```

So the exact normal operator gains:

```text
r''/r = f'/(2r)
```

Two-hundred-twenty-eighth verdict:

```text
The GR product-collar Poisson kernel must be refactored through UDT proper
radial distance.
```

The exact normal operator gains:

```text
the warping/extrinsic term r''/r = f'/(2r).
```

## 244. phi0 DtN potential shift

Implemented in `native_phi0_dtn_potential_shift.py`.

After the Liouville transform:

```text
H_l = -d_rho^2 + V_l
V_l = r''/r + l(l+1)/r^2
```

With UDT positional dilation:

```text
r'' = f'/2
```

At phi0:

```text
f = 1
f' = -q/R
r''/r = -q/(2R^2)
```

Therefore:

```text
V_l(phi0) = [l(l+1) - q/2]/R^2
```

If `P_phi0` is banked:

```text
q = 1/3
```

so:

```text
V_l(phi0) = [l(l+1) - 1/6]/R^2
```

For:

```text
l = 1
```

this gives:

```text
V_1(phi0) = (11/6)/R^2
```

Compare the product normalized angular kernel:

```text
L1 = I3
```

Two-hundred-twenty-ninth verdict:

```text
Positional dilation shifts the boundary-normal DtN operator.
```

The naive product kernel:

```text
L1 = I3
```

is exact as:

```text
a boundary angular operator,
```

but not as:

```text
the full bulk DtN normal operator through the warped collar.
```

## 245. Refactored kernel implications

Implemented in `native_refactored_kernel_implications.py`.

Implications:

```text
angular bridge survives:
  statement:
    normalized -r^2 Delta_S2 still gives L1 = I3 on the boundary.
  status:
    exact.

bulk DtN kernel changes:
  statement:
    warped normal operator includes r''/r = f'/(2r).
  status:
    exact.

eta may be the correction source:
  statement:
    the shift term is controlled by q, hence by P_phi0 if banked.
  status:
    promising interpretation, not derivation.

simple gamma is not automatic:
  statement:
    3 exp(-eta/2) follows only from the abstract boundary L1 kernel or
    an exact reduction.
  status:
    conditional.

refactored GR target:
  statement:
    derive the phi0 Calderon/DtN map for the warped UDT collar and compare
    its ell=1 boundary spectrum.
  status:
    next exact target.
```

Two-hundred-thirtieth verdict:

```text
Positional dilation does not erase the angular bridge,
but it changes the normal boundary operator.
```

The next exact work is not:

```text
generic GR heat kernels.
```

It is:

```text
the UDT-refactored DtN/Calderon map.
```

## 242. Warped collar operator obstruction

Implemented in `native_warped_collar_operator_obstruction.py`.

The product Poisson kernel is the right atlas object, but ordinary scalar
propagation through a spherical collar is not automatically product.

Cases:

```text
product cylinder:
  exact operator:
    -d_x^2 + L with L independent of x.
  consequence:
    Poisson kernel is exactly exp(-x sqrt(L)).
  verdict:
    gives exact semigroup transfer.

spherical warped collar:
  exact operator:
    -a'' - 2(r'/r)a' + l(l+1)a/r^2 for each Y_lm mode.
  consequence:
    radial first-derivative and r-dependent angular term appear.
  verdict:
    not the product-cylinder operator.

phi0 boundary value:
  exact operator:
    at phi0, f = 1 and boundary angular operator L1 = I3.
  consequence:
    boundary operator is exact at the interface.
  verdict:
    does not make the whole collar product.

abstract boundary action:
  exact operator:
    A_side = (eta/2)L1 defined directly on boundary data.
  consequence:
    no bulk propagation through a warped collar is assumed.
  verdict:
    viable if derived as a boundary action.
```

Two-hundred-twenty-seventh verdict:

```text
Ordinary scalar propagation through a spherical collar is not exactly the
product Poisson semigroup.
```

Therefore the semigroup remains viable only as:

```text
1. an abstract boundary action/kernel,
```

or:

```text
2. an exact UDT variable change reducing the bridge to product form.
```

This prevents an overclaim:

```text
GR/PDE semigroup math points to the right class of object,
but the UDT bridge kernel still has to be derived.
```

## 246. Frozen phi0 DtN symbol diagnostic

Implemented in `native_frozen_phi0_dtn_symbol.py`.

From the positional-dilation refactor, the Liouville normal operator is:

```text
H_l = -d_rho^2 + V_l
```

with:

```text
V_l(phi0) = [l(l+1) - q/2]/R^2
```

The frozen-coefficient DtN eigenvalue at phi0 is therefore:

```text
lambda_l^frozen = sqrt(V_l)
                 = sqrt(l(l+1)-q/2)/R
```

The product-cylinder comparison is:

```text
lambda_l^product = sqrt(l(l+1))/R
```

For banked `P_phi0`:

```text
q = 1/3
```

and:

```text
l = 1
```

we get:

```text
shifted V coefficient = 11/6
product V coefficient = 2
squared DtN ratio = 11/12
DtN ratio = sqrt(11/12)
```

Two-hundred-thirty-first verdict:

```text
The frozen local DtN symbol is shifted by positional dilation.
```

Therefore:

```text
the simple product kernel is not the local bulk DtN symbol
```

unless:

```text
1. an abstract boundary action is the correct object,
```

or:

```text
2. an exact UDT reduction removes the warping contribution.
```

This is a diagnostic, not a replacement transfer rule.

## 247. DtN kernel path split

Implemented in `native_dtn_kernel_path_split.py`.

There are now distinct kernel paths:

```text
abstract boundary action path:
  kernel:
    A_side = (eta/2)L1 on boundary data.
  exact status:
    valid if UDT boundary action is defined directly on phi0 angular data.
  consequence:
    gives 3 exp(-eta/2) without using bulk collar propagation.

product-collar Poisson path:
  kernel:
    exp(-x sqrt(L1)).
  exact status:
    exact only for product normal operator -d_x^2 + L1.
  consequence:
    gives 3 exp(-x) with x = eta/2 if side time is eta/2.

UDT warped DtN path:
  kernel:
    DtN of -d_rho^2 + [r''/r + l(l+1)/r^2].
  exact status:
    the correct bulk-collar path after positional-dilation refactor.
  consequence:
    generically differs from product kernel; must be solved or characterized.

Calderon boundary-selection path:
  kernel:
    projector onto two-sided admissible Cauchy data.
  exact status:
    promising GR/PDE atlas object; not constructed for UDT phi0.
  consequence:
    could derive P_phi0 and/or side split if found.
```

Two-hundred-thirty-second verdict:

```text
The simple gamma path is an abstract boundary-action or product-collar path.
```

The literal UDT bulk DtN path is:

```text
warped
```

and must be solved separately.

This is where positional dilation materially changes the GR/PDE import.

## 248. Self-similar warped DtN solution

Implemented in `native_self_similar_warped_dtn_solution.py`.

Now solve the UDT-refactored warped collar exactly for a self-similar
interior.

Use:

```text
y = r/R
f = y^(-q)
```

The harmonic angular-mode equation is:

```text
a_yy + (2 - q/2) a_y/y - l(l+1)y^(q-2)a = 0
```

Set:

```text
beta = q/2
x = sqrt(l(l+1)) y^beta / beta
c = 2/q
m = (1-c)/2 = (1-2/q)/2
nu = |m|
```

Then the exact solution is:

```text
a(y) = x^m [A I_nu(x) + B K_nu(x)]
```

For:

```text
0 < q < 1/2
```

finite endpoint behavior selects:

```text
B = 0
```

so:

```text
a_finite(y) = x^m I_nu(x)
```

The exact boundary logarithmic derivative at `y = 1` is:

```text
d ln a / d ln y = beta [m + x I_nu'(x)/I_nu(x)] at x=x0
x0 = sqrt(l(l+1))/beta = 2 sqrt(l(l+1))/q
```

For the finite branch with:

```text
nu = -m
```

this simplifies exactly to:

```text
d ln a / d ln y = beta x0 I_{nu+1}(x0)/I_nu(x0)
```

Two-hundred-thirty-third verdict:

```text
The self-similar UDT warped collar has an exact DtN expression.
```

But it is:

```text
a Bessel-ratio boundary map,
```

not:

```text
the product-cylinder value sqrt(L).
```

## 249. ell=1 self-similar DtN exact formula

Implemented in `native_l1_self_similar_dtn_exact_formula.py`.

For banked `P_phi0`:

```text
q = 1/3
beta = q/2 = 1/6
```

For:

```text
l = 1
```

we have:

```text
l(l+1) = 2
x0 = sqrt(2)/beta = 6 sqrt(2)
m = (1 - 2/q)/2 = -5/2
nu = 5/2
```

Finite endpoint branch:

```text
a(y) = x^(-5/2) I_{5/2}(x)
x = 6 sqrt(2)y^(1/6)
```

Exact dimensionless boundary derivative:

```text
D_1 = d ln a / d ln y |_{y=1}
    = sqrt(2) I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2))
```

Product-cylinder DtN comparison:

```text
D_product = sqrt(2)
```

Exact ratio:

```text
D_1 / D_product = I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2))
```

Two-hundred-thirty-fourth verdict:

```text
The exact self-similar UDT warped DtN map does not collapse algebraically
to the product value unless this Bessel ratio equals 1.
```

Therefore:

```text
do not replace the warped DtN map by sqrt(2) or L1 without a separate
boundary-action argument.
```

This is a strict positional-dilation correction to the GR product-kernel
intuition.

## 250. Half-integer Bessel closed form for warped ell=1 DtN

Implemented in `native_l1_dtn_half_integer_closed_form.py`.

For banked `P_phi0` and `ell = 1`:

```text
q = 1/3
beta = 1/6
x = 6 sqrt(2)
```

The half-integer modified Bessel functions can be written exactly as:

```text
I_{5/2}(x) = A [sinh(x) - 3 cosh(x)/x + 3 sinh(x)/x^2]
I_{7/2}(x) = A [cosh(x) - 6 sinh(x)/x
                  + 15 cosh(x)/x^2 - 15 sinh(x)/x^3]
```

where the shared prefactor `A` cancels in the ratio.

Therefore:

```text
I_{7/2}(x) / I_{5/2}(x)
= [cosh(x) - 6 sinh(x)/x + 15 cosh(x)/x^2 - 15 sinh(x)/x^3]
  / [sinh(x) - 3 cosh(x)/x + 3 sinh(x)/x^2]
```

with:

```text
x = 6 sqrt(2)
```

So the exact warped `ell = 1` DtN derivative is:

```text
D_1 = sqrt(2)
      [cosh(x) - 6 sinh(x)/x + 15 cosh(x)/x^2 - 15 sinh(x)/x^3]
      / [sinh(x) - 3 cosh(x)/x + 3 sinh(x)/x^2]
```

with `x = 6 sqrt(2)`.

Two-hundred-thirty-fifth verdict:

```text
The positional-dilation warped DtN correction is not special-function fog.
For the banked ell=1 case it is an exact hyperbolic rational expression.
```

It still does not reduce to the product-cylinder value without an additional
identity:

```text
I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2)) = 1.
```

That identity is not native to the expression above.

Therefore:

```text
literal UDT warped bulk propagation does not by itself justify replacing
the boundary map by L1 = I3.
```

The cleaner path for the simple transfer candidate remains:

```text
derive an abstract phi0 boundary action whose ell=1 operator is L1 = I3,
```

or else accept that the actual positional-dilation bulk DtN operator supplies
a different exact member of the orchestra.

## 251. Warped DtN preserves the ell=1 identity triplet

Implemented in `native_warped_dtn_identity_preservation.py`.

The exact self-similar warped collar changed the product-cylinder DtN
eigenvalue.

It did not change this angular fact:

```text
dim H_{ell=1}(S2) = 2ell + 1 = 3.
```

Because the background remains spherically symmetric, the DtN map is still
diagonal by angular momentum sector. Therefore on the `ell = 1` subspace it
must be proportional to the identity:

```text
K_warped|_{ell=1} = D_1 I3.
```

For banked `P_phi0`:

```text
D_1 = sqrt(2) B
B = I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2)).
```

So:

```text
K_warped|_{ell=1} = sqrt(2) B I3.
```

The product-cylinder comparison is:

```text
K_product|_{ell=1} = sqrt(2) I3.
```

Therefore the exact positional-dilation dressing relative to the product
kernel is:

```text
K_warped K_product^{-1}|_{ell=1} = B I3.
```

where:

```text
B = I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2)).
```

Two-hundred-thirty-sixth verdict:

```text
The warped collar does not erase the angular identity bridge.
It dresses the ell=1 triplet by an exact scalar factor.
```

This is an orchestra-compatible result:

```text
angular sector supplies the invariant I3 triplet,
positional-dilation radial warping supplies an exact scalar dressing,
phi0 boundary momentum supplies the candidate eta scale.
```

No single one of those pieces should be mistaken for the whole mechanism.

## 252. Transfer operator fork: intrinsic boundary versus warped DtN

Implemented in `native_transfer_operator_fork.py`.

At this point there are two exact native `ell = 1` identity structures.

Intrinsic boundary angular operator:

```text
L1|_{ell=1} = I3.
```

Warped bulk DtN operator:

```text
K_warped|_{ell=1} = sqrt(2) B I3
B = I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2)).
```

Relative to the product-cylinder DtN comparison:

```text
K_product|_{ell=1} = sqrt(2) I3,
```

the warped dressing is:

```text
K_warped K_product^{-1}|_{ell=1} = B I3.
```

Therefore the transfer candidate has a clean fork.

If the native transfer action is intrinsic-boundary angular:

```text
A_side = (eta/2) I3
Tr exp(-A_side) = 3 exp(-eta/2).
```

If the native transfer action uses the warped DtN dressing:

```text
A_side = (eta/2) B I3
Tr exp(-A_side) = 3 exp(-eta B/2).
```

Two-hundred-thirty-seventh verdict:

```text
Both branches preserve the native angular triplet.
The unresolved issue is which native operator enters the phi0 transfer action.
```

This is a concrete anti-fitting constraint:

```text
do not choose between 3 exp(-eta/2) and 3 exp(-eta B/2) by observational
convenience.
```

Choose only by deriving which boundary operator the metric supplies at the
`phi = 0` interface.

## 253. Variational test for which operator is selected

Implemented in `native_operator_selection_variational_test.py`.

The fork in Section 252 can be sharpened by asking where the boundary
quadratic form comes from.

For the spatial collar metric:

```text
dl^2 = d rho^2 + r(rho)^2 dOmega^2,
```

consider a scalar Dirichlet energy probe:

```text
E[u] = (1/2) int |grad u|^2 dV.
```

For an angular mode:

```text
u(rho, Omega) = a(rho) Y_lm(Omega),
```

with normalized angular basis, the radial energy is:

```text
E_l[a] = (1/2) int [r^2 a'^2 + l(l+1) a^2] d rho.
```

The Euler-Lagrange equation is:

```text
(r^2 a')' = l(l+1) a.
```

On shell:

```text
r^2 a'^2 + l(l+1) a^2 = (r^2 a a')'.
```

Therefore:

```text
E_l,on-shell = (1/2) [r^2 a a']_boundary.
```

That is the Dirichlet-to-Neumann boundary form.

So:

```text
bulk harmonic elimination selects the DtN operator.
```

For the banked `P_phi0`, `ell = 1`, self-similar UDT collar:

```text
K_DtN|_{ell=1} = sqrt(2) B I3
B = I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2)).
```

Two-hundred-thirty-eighth verdict:

```text
If the phi0 transfer action is the on-shell eliminated bulk collar energy,
the native operator is the warped DtN kernel, not the intrinsic L1 kernel.
```

The simple intrinsic branch:

```text
A_side = (eta/2) I3
```

remains viable only if the metric supplies an interface-local boundary action
at `phi = 0`, rather than the transfer action being the ordinary on-shell
bulk-collar Dirichlet form.

This is useful because it turns the next search into a concrete question:

```text
Does the phi0 interface have its own native boundary action, or does the
transfer form arise by eliminating the negative-phi collar bulk?
```

## 254. phi0 boundary value/derivative split

Implemented in `native_phi0_boundary_value_derivative_split.py`.

Let:

```text
F = f(phi0)
```

and let `a` denote angular boundary data.

The most general local expansion of a `phi0` boundary functional near
`F = 1` is:

```text
S_b(F,a) = S_0[a] + S_1[a](F - 1) + O((F - 1)^2).
```

The C1 momentum closure fixes only the first derivative:

```text
S_1[a] = q/2.
```

After the H1/S2 projection:

```text
<S_1,ab> = (q/6) delta_ab.
```

For banked `P_phi0`:

```text
q = 1/3
q/2 = 1/6
eta = q/6 = 1/18.
```

But a transfer exponential depends on the angular quadratic operator contained
in the boundary value:

```text
S_0[a],
```

not merely on:

```text
dS_b/dF at F=1.
```

Therefore:

```text
S_0[a] = (eta/2) <a, I3 a>
```

would give:

```text
Tr exp[-(eta/2)I3] = 3 exp(-eta/2),
```

while:

```text
S_0[a] = (eta B/2) <a, I3 a>
```

would give:

```text
Tr exp[-(eta B/2)I3] = 3 exp(-eta B/2).
```

Two-hundred-thirty-ninth verdict:

```text
The scalar phi0 momentum scale eta is fixed once q is fixed.
The angular transfer operator is not fixed by that scalar derivative alone.
```

This prevents a false derivation:

```text
q = 1/3 -> eta = 1/18
```

does not by itself imply:

```text
A_side = (eta/2) I3.
```

The missing object is specifically:

```text
the angular operator in S_0[a], the value part of the phi0 boundary action.
```

## 255. Intrinsic phi0 S0 operator classification

Implemented in `native_phi0_intrinsic_s0_operator_classification.py`.

If the missing `S_0[a]` is genuinely interface-local, then it should be built
from the intrinsic angular geometry at `phi0`:

```text
h_AB = R^2 omega_AB.
```

A local rotationally invariant quadratic form with up to two angular
derivatives has the exact form:

```text
S_0[a] = (1/2) alpha <a,a>
       + (1/2) beta <a, -R^2 Delta_S2 a>.
```

On a spherical harmonic sector:

```text
-R^2 Delta_S2 -> ell(ell+1),
```

so the `S_0` eigenvalue is:

```text
lambda_ell = alpha + beta ell(ell+1).
```

If the interface action is required to be blind to the constant angular mode,
then:

```text
lambda_0 = alpha = 0.
```

Then:

```text
S_0[a] = (1/2) beta <a, -R^2 Delta_S2 a>.
```

For `ell = 1`:

```text
-R^2 Delta_S2 = 2 I3.
```

The normalized intrinsic operator is:

```text
L1 = (-R^2 Delta_S2)/2,
```

and:

```text
L1|_{ell=1} = I3.
```

Two-hundred-fortieth verdict:

```text
Intrinsic phi0 locality plus rotational invariance restricts S0 to a small
operator family.
```

Adding constant-mode blindness selects the angular Laplacian branch:

```text
S_0 proportional to -R^2 Delta_S2.
```

But it still does not fix the coefficient:

```text
beta.
```

Therefore the intrinsic branch is now cleaner:

```text
metric S2 geometry can select L1 = I3 on ell=1,
but the eta/2 coupling coefficient still needs a native bridge to the scalar
phi0 momentum scale.
```

## 256. eta-L1 coefficient factor ledger

Implemented in `native_eta_l1_coefficient_factor_ledger.py`.

The desired intrinsic transfer operator is:

```text
A_side = (eta/2) L1.
```

Since:

```text
L1 = (-R^2 Delta_S2)/2,
```

this is equivalently:

```text
A_side = (eta/4)(-R^2 Delta_S2)|_{ell=1}.
```

For banked `P_phi0`:

```text
q = 1/3.
```

The exact coefficient ledger is:

```text
C1 boundary momentum unit:       q/2   = 1/6
H1/S2 isotropic projection:      q/6   = eta = 1/18
one-sided interface split:       q/12  = eta/2 = 1/36
L1 normalization factor:         q/24  = eta/4 = 1/72
```

Thus:

```text
A_side = (eta/2)L1
       = (q/12)L1
       = (q/24)(-R^2 Delta_S2)|_{ell=1}.
```

Two-hundred-forty-first verdict:

```text
The simple transfer coefficient has a coherent exact factor ledger:
boundary momentum x isotropic projection x side split x L1 normalization.
```

But this is not yet a derivation.

The unresolved native-action steps are:

```text
1. why the phi0 scalar momentum scale couples to S0[a],
2. why the glued interface assigns half the full action to one side,
3. why the intrinsic constant-blind angular operator is the transfer operator.
```

This is the current cleanest orchestra statement:

```text
q/2 supplies the radial scalar edge unit,
1/3 supplies the H1/S2 isotropic channel share,
1/2 supplies one-sided gluing bookkeeping,
1/2 supplies L1 normalization from ell=1 angular eigenvalue 2.
```

## 257. Simple gamma derivation gate

Implemented in `native_simple_gamma_derivation_gate.py`.

The simple transfer candidate can now be written as a gated derivation rather
than a fit.

Gate ledger:

```text
phi0 scalar edge unit:
    status: banked as P_phi0; exact consequences follow
    consequence: q=1/3, q/2=1/6, eta=q/6=1/18

H1/S2 isotropic projection:
    status: derived from round S2 second moment
    consequence: <n_a n_b>=delta_ab/3

ell=1 angular identity:
    status: derived from intrinsic S2 Laplacian
    consequence: L1=(-R^2 Delta_S2)/2=I3 on ell=1

constant-mode blindness:
    status: physically motivated selector; not yet forced
    consequence: removes alpha<a,a> and leaves Laplacian branch

scalar-to-angular S0 coupling:
    status: open
    consequence: needed to form A_full=eta L1 or A_side=(eta/2)L1

one-sided composable split:
    status: conditional gluing identity
    consequence: side kernel carries half of full shared boundary action

trace over ell=1 triplet:
    status: conditional transfer interpretation
    consequence: Tr exp[-(eta/2)I3]=3 exp(-eta/2)
```

Two-hundred-forty-second verdict:

```text
The simple gamma path is no longer a loose fit.
It is a precise gated derivation with one central missing gate.
```

That central missing gate is:

```text
scalar-to-angular S0 coupling at phi0.
```

In orchestra language:

```text
we have several instruments with exact parts,
but the score that makes them play the same boundary action is still missing.
```

This is also the main anti-myopia result:

```text
do not collapse radial momentum, angular triplet, side split, and transfer
trace into one mechanism.
```

## 258. Shell stress as S0 coupling audit

Implemented in `native_shell_stress_s0_coupling_audit.py`.

The exact metric jump at `phi0` gives an angular-only shell signature.

For flat exterior and inner:

```text
f'_in = -q/R,
```

the extrinsic curvature jump is:

```text
[K^a_b] = diag(q/2R, 0, 0)
```

in the `(t, theta, phi)` directions, with:

```text
[K] = q/2R.
```

Therefore:

```text
[K^a_b] - delta^a_b[K] = (0, -q/2R, -q/2R).
```

This is an angular-only isotropic interface stress signature.

For banked `P_phi0`:

```text
q = 1/3
q/2 = 1/6
eta = (q/2)/3 = 1/18.
```

This supports:

```text
radial slope momentum couples to angular surface geometry at phi0.
```

But it does not yet supply:

```text
the constant-blind Laplacian operator L1.
```

Reason:

```text
isotropic angular stress couples first to angular metric/area variation,
while L1 requires a shape-gradient or nonconstant-mode boundary action.
```

Two-hundred-forty-third verdict:

```text
The shell stress partially closes the scalar-to-angular coupling gate.
It supplies the angular surface scale q/2, but not yet the L1 operator.
```

This is important because it prevents a tempting overclaim:

```text
angular-only shell stress -> eta
```

is supported, while:

```text
angular-only shell stress -> eta L1
```

still needs an additional shape/nonconstant-mode argument.

## 259. H1-restricted operator equivalence

Implemented in `native_h1_restricted_operator_equivalence.py`.

The previous section exposed a possible overclaim:

```text
angular-only shell stress -> eta L1
```

is not established on the full sphere.

But the transfer trace has usually been taken over the `ell = 1` triplet, not
over the full angular Hilbert space.

Let:

```text
P_H1
```

be the projector onto the `ell = 1` triplet.

Then two different full-`S2` operators become identical after restriction:

```text
P_H1 I P_H1 = I3
```

and:

```text
P_H1 [(-R^2 Delta_S2)/2] P_H1 = I3.
```

Therefore, on the already-selected `H1` transfer space:

```text
isotropic angular surface stress
```

and:

```text
normalized L1
```

both act as:

```text
I3.
```

Two-hundred-forty-fourth verdict:

```text
The trace over H1 cannot distinguish an intrinsic identity kernel from
normalized L1.
```

This changes the missing-gate diagnosis.

The shell stress may not need to generate the full Laplacian operator. It may
only need to supply an isotropic angular coupling after the transfer space has
already been restricted to `H1`.

Then:

```text
A_side = (eta/2) I3
```

can be read as:

```text
isotropic angular phi0 stress restricted to the ell=1 bridge space.
```

The unresolved question becomes:

```text
why is the transfer space exactly H1?
```

rather than:

```text
why does the shell stress generate the full angular Laplacian?
```

## 260. H1 transfer-space selector status

Implemented in `native_h1_transfer_space_selector_status.py`.

The current `H1` selector can be stated without Standard Model analogy.

Metric filters:

```text
phi-sign/angular invariance:
    result: normalized angular spectrum is shared across phi<0, phi=0,
            and exterior phi>0
    status: derived metric fact

constant-mode rejection:
    result: ell=0 is scalar/background, not an angular bridge with nonzero
            operator
    status: selector assumption unless tied to accessibility/shape constraint

lowest nonconstant sector:
    result: ell=1 is the first nonconstant angular eigenspace
    status: derived once ell=0 is rejected

triplet multiplicity:
    result: dim H1 = 2ell+1 = 3
    status: derived angular spectrum fact

identity action on selected space:
    result: isotropic stress and normalized L1 both restrict to I3 on H1
    status: derived restricted-operator fact
```

Two-hundred-forty-fifth verdict:

```text
H1 is strongly native if the constant mode is excluded.
```

The remaining selector burden is:

```text
justify ell=0 rejection as a metric/accessibility condition,
not as a desired particle-sector outcome.
```

This fits the older bridge intuition:

```text
negative phi matter space is accessible from positive/scalar background
through angular structures invariant under r* and phi sign.
```

In that frame:

```text
ell=0 is shared scalar background,
ell=1 is the first nonconstant angular bridge.
```

## 261. ell=0 exclusion from exact endpoint equation

Implemented in `native_ell0_exclusion_exact_endpoint.py`.

The `ell = 0` rejection can be strengthened without particle analogy.

The endpoint source equation is:

```text
p(1 - p)/2 = eta lambda.
```

For the constant angular sector:

```text
ell = 0
lambda = ell(ell+1) = 0.
```

Therefore:

```text
p(1 - p)/2 = 0.
```

So:

```text
p = 0
```

or:

```text
p = 1.
```

The finite-action endpoint filter rejects:

```text
p = 1,
```

because the finite C1 endpoint branch requires:

```text
p < 1/2.
```

The remaining finite branch is:

```text
p = 0.
```

Two-hundred-forty-sixth verdict:

```text
ell=0 carries no angular source and gives the trivial finite branch.
```

Thus:

```text
ell=0 is background/scalar collar data,
not a negative-phi matter endpoint.
```

The first finite nonconstant angular bridge is therefore:

```text
ell=1.
```

This is the cleanest current metric-native argument for the `H1` transfer-space
selector:

```text
ell=0 -> no finite negative-phi angular endpoint,
ell=1 -> first nonconstant phi-invariant angular bridge,
dim H1 = 3,
I or L1 restricted to H1 = I3.
```

## 262. Post-ponder transfer chain status

Implemented in `native_post_ponder_transfer_chain_status.py`.

The serious-ponder pass upgrades the simple transfer path.

Current chain:

```text
P_phi0 gives q=1/3:
    status: banked minimal postulate

C1 boundary momentum gives q/2:
    status: exact once q is fixed

phi0 shell signature is angular-only:
    status: metric-derived jump fact

H1/S2 projection gives eta=q/6:
    status: derived round-S2 average

ell=0 gives p=0 finite branch:
    status: exact endpoint exclusion

ell=1 is first finite nonconstant angular bridge:
    status: derived after ell=0 exclusion

dim H1=3:
    status: derived angular spectrum fact

isotropic stress restricted to H1 is I3:
    status: derived restricted-operator fact

one side carries eta/2:
    status: conditional composable gluing rule

trace gives 3 exp(-eta/2):
    status: exact if side-action interpretation holds
```

Two-hundred-forty-seventh verdict:

```text
The H1 selector is now mostly metric-native.
```

The earlier missing gate:

```text
scalar-to-angular S0 coupling
```

has split into two clearer pieces:

```text
1. angular-only shell stress supplies the angular scalar scale,
2. exact ell=0 exclusion selects H1 as the first finite nonconstant bridge.
```

The remaining unresolved items are now:

```text
1. derive or bank P_phi0,
2. prove the transfer kernel is a one-sided composable boundary action,
3. prove the physical operation is the H1 trace.
```

This is not yet a full derivation, but it is much less fitting-like than before:

```text
the number 3 is not inserted;
it appears as dim H1 after ell=0 is removed by the endpoint equation.
```

## 263. Half-action from symmetric gluing

Implemented in `native_half_action_from_symmetric_gluing.py`.

The one-sided factor can be derived conditionally from exact gluing
bookkeeping.

Let the full shared `phi0` edge action be:

```text
B = eta.
```

Let a one-sided transfer kernel carry side weight:

```text
w.
```

Composable gluing requires a shared internal boundary to contribute one full
boundary action, not two:

```text
w_left + w_right = B.
```

If the interface is symmetric under side exchange:

```text
w_left = w_right = w.
```

Therefore:

```text
2w = B
```

and:

```text
w = B/2 = eta/2.
```

For banked `P_phi0`:

```text
eta = 1/18
eta/2 = 1/36.
```

Two-hundred-forty-eighth verdict:

```text
eta/2 is exact if the transfer kernel is one side of a symmetric composable
phi0 boundary action.
```

This upgrades the earlier status:

```text
one side carries eta/2
```

from a convenient convention to a conditional theorem.

The remaining burden is:

```text
prove that the physical transfer object is a one-sided composable phi0
boundary kernel.
```

## 264. Half-split symmetry scope audit

Implemented in `native_half_split_symmetry_scope_audit.py`.

The exact half split follows from:

```text
w_left + w_right = B
w_left = w_right
therefore w_left = w_right = B/2.
```

But the symmetry assumption has a scope.

Where side symmetry is native:

```text
intrinsic phi0 angular geometry,
h_AB = R^2 omega_AB,
normalized angular spectrum common to both phi signs.
```

Where side symmetry is not automatic:

```text
literal radial/bulk DtN through the collar,
flat exterior has q_out = 0,
negative-phi interior has q_in != 0.
```

Therefore:

```text
intrinsic interface-local action can justify the half split if the two sides
share one angular boundary action.
```

But:

```text
bulk DtN propagation cannot use the half split unless its two one-sided
kernels are proven symmetric or deliberately normalized.
```

Two-hundred-forty-ninth verdict:

```text
eta/2 is exact for a symmetric interface-local boundary action.
It is not automatically exact for an asymmetric radial bulk-DtN bridge.
```

This reinforces the path split:

```text
simple gamma -> intrinsic interface-local H1 action,
warped gamma -> literal positional-dilation bulk DtN action.
```

## 265. H1 trace operation audit

Implemented in `native_h1_trace_operation_audit.py`.

Let:

```text
a = eta/2.
```

For banked `P_phi0`:

```text
a = 1/36.
```

On `H1`:

```text
A_side = a I3.
```

There are several exact operations one could apply.

Single prepared channel:

```text
<m|exp(-a I3)|m> = exp(-a).
```

This requires an external channel label or prepared direction.

Unlabelled channel sum:

```text
Tr_H1 exp(-a I3) = 3 exp(-a).
```

This is valid if all `H1` channels are accessible and no channel is selected.

Normalized channel average:

```text
(1/3) Tr_H1 exp(-a I3) = exp(-a).
```

This is valid if the transfer is averaged rather than counted.

Gaussian determinant:

```text
det exp(-a I3) = exp(-3a).
```

This is a different object, relevant only for a determinant or path-integral
measure.

Two-hundred-fiftieth verdict:

```text
The factor 3 comes from trace/counting over unlabelled H1 channels.
```

It is not produced by:

```text
a single channel,
a normalized average,
or a Gaussian determinant.
```

Therefore the physical trace rule remains a gate:

```text
the metric must justify counting all accessible H1 bridge channels rather
than selecting, averaging, or determinant-weighting them.
```

## 266. Trace versus average physical role

Implemented in `native_trace_vs_average_physical_role.py`.

The operation on `H1` depends on what the transfer multiplier represents.

Boundary-state count:

```text
Tr_H1 exp(-A)
```

Interpretation:

```text
sum over accessible unlabelled bridge channels.
```

Native fit:

```text
natural for a partition/measure multiplier.
```

Prepared-channel amplitude:

```text
<m|exp(-A)|m>.
```

Interpretation:

```text
one selected H1 channel.
```

Native fit:

```text
requires a preferred angular label not supplied by round phi0 geometry.
```

Ignorance average:

```text
(1/3) Tr_H1 exp(-A).
```

Interpretation:

```text
normalized probability over an unknown channel.
```

Native fit:

```text
requires probability normalization external to the boundary action.
```

Gaussian field integral:

```text
det(A)^(-1/2)
```

or a related determinant.

Interpretation:

```text
continuous boundary-field measure.
```

Native fit:

```text
requires a specified path-integral measure and normalization.
```

Two-hundred-fifty-first verdict:

```text
The trace is the correct operation only if the phi0 transfer multiplier is
a boundary-state count or partition weight.
```

It is not correct if the quantity is:

```text
a normalized transition probability for an unknown prepared channel.
```

For the mass-emergence ladder use case, the trace branch is plausible because
the multiplier has been treated as:

```text
a degeneracy/availability factor in the boundary composition,
```

not:

```text
a normalized probability for a single prepared angular state.
```

But this remains a physical-role gate, not a bare algebraic identity.

## 267. Upgraded transfer conditional theorem

Implemented in `native_upgraded_transfer_conditional_theorem.py`.

The simple transfer multiplier can now be stated as a clean conditional theorem.

Assumptions:

```text
A1. P_phi0 fixes q = 1/3.
A2. The phi0 shell action is intrinsic/interface-local on H1.
A3. The interface is symmetric and composable, so one side carries eta/2.
A4. The multiplier counts unlabelled H1 boundary states.
```

Exact consequences:

```text
eta = q/6 = 1/18
a = eta/2 = 1/36
ell=0 gives only the trivial finite branch p=0
ell=1 is the first finite nonconstant angular bridge
dim H1 = 3
A_side|H1 = a I3
```

Therefore:

```text
gamma = Tr_H1 exp(-A_side)
      = Tr_H1 exp(-a I3)
      = 3 exp(-a)
      = 3 exp(-1/36).
```

Two-hundred-fifty-second verdict:

```text
Under these assumptions, gamma = 3 exp(-1/36) is exact.
```

The assumptions are now explicit gates:

```text
P_phi0,
intrinsic/interface-local H1 action,
symmetric composable side split,
boundary-state counting.
```

They are not hidden fitting choices.

This is the current best form of the simple transfer path.

## 268. Simple versus warped branch discriminator

Implemented in `native_simple_vs_warped_branch_discriminator.py`.

The current fork has an exact discriminator.

Simple intrinsic-interface branch:

```text
gamma_simple = 3 exp(-eta/2).
```

With banked `P_phi0`:

```text
gamma_simple = 3 exp(-1/36).
```

Dependence:

```text
eta and H1 only.
```

Self-similar warped bulk-DtN branch:

```text
gamma_warped = 3 exp(-eta B/2),
```

where:

```text
B = I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2)).
```

With banked `P_phi0`:

```text
gamma_warped = 3 exp(-B/36).
```

Dependence:

```text
eta, H1, and radial collar DtN dressing.
```

Two-hundred-fifty-third verdict:

```text
The branch discriminator is profile dependence.
```

If transfer is intrinsic to the `phi0` interface:

```text
it is insensitive to the radial collar profile after q/eta are fixed.
```

If transfer is bulk-DtN propagation:

```text
it remembers the negative-phi collar through the DtN map.
```

Therefore the next mathematical test is not numerical closeness. It is:

```text
does the metric's transfer object live locally at phi0,
or does it propagate through the negative-phi collar?
```

## 269. Transfer locality evidence

Implemented in `native_transfer_locality_evidence.py`.

Current native objects do not all point in the same direction.

C1 momentum jump:

```text
support: Delta Pi_f is localized at phi0 when exterior is flat.
branch pressure: intrinsic/interface-local.
caveat: fixes eta scale, not the transfer operation by itself.
```

Distributional curvature jump:

```text
support: f'' contains a delta term at the slope discontinuity.
branch pressure: intrinsic/interface-local.
caveat: GR curvature is atlas math, not imported dynamics.
```

Angular-only shell signature:

```text
support: trace-reversed stress has zero time part and isotropic angular parts.
branch pressure: intrinsic/interface-local H1 coupling.
caveat: requires H1 selector and state-count interpretation.
```

Warped DtN map:

```text
support: on-shell harmonic elimination through the negative-phi collar.
branch pressure: bulk/profile-sensitive.
caveat: correct only if transfer is bulk propagation.
```

Two-hundred-fifty-fourth verdict:

```text
The eta-producing native objects currently point to an interface-local shell.
```

The warped DtN branch remains necessary if and only if:

```text
the transfer operation is identified with bulk harmonic propagation through
the collar.
```

This leans the current mass-emergence transfer chain toward:

```text
intrinsic phi0 shell + H1 bridge + boundary-state count,
```

not because it fits better numerically, but because the known eta carrier is
localized at the interface.

## 270. P_phi0 from H1 self-consistency

Implemented in `native_p_phi0_from_h1_self_consistency.py`.

The upgraded `H1` selector gives a possible route to `P_phi0`.

Endpoint equation:

```text
p(1 - p)/2 = eta lambda.
```

For the `H1` bridge:

```text
ell = 1
lambda = ell(ell + 1) = 2.
```

The H1/S2 projected collar scale is:

```text
eta = q/6.
```

If the edge is self-similar so that the endpoint exponent equals the `phi0`
collar slope:

```text
p = q,
```

then:

```text
q(1 - q)/2 = (q/6) * 2.
```

So:

```text
q(1 - q)/2 = q/3.
```

The solutions are:

```text
q = 0
```

or:

```text
q = 1/3.
```

The first solution:

```text
q = 0
```

is the trivial scalar/background branch.

The first nontrivial `H1` self-consistent branch is:

```text
q = 1/3.
```

Consequently:

```text
eta = q/6 = 1/18.
```

Two-hundred-fifty-fifth verdict:

```text
P_phi0 is derived if p=q self-similar edge closure is derived.
```

Otherwise this remains:

```text
a conditional derivation of P_phi0,
not a replacement for the banked postulate.
```

This is promising because it uses the same pieces already uncovered:

```text
ell=0 exclusion,
H1 as first finite nonconstant bridge,
H1/S2 eta projection,
self-similar edge preservation.
```

## 271. p=q gate status

Implemented in `native_p_equals_q_gate_status.py`.

Write the finite-cell interior as:

```text
f(r) = (R/r)^p h(r)
h(R) = 1.
```

Then the `phi0` collar slope is:

```text
q_phi0 = -d ln f / d ln r |R
       = p - d ln h / d ln r |R.
```

Define:

```text
delta_h = -d ln h / d ln r |R.
```

Then:

```text
q_phi0 = p + delta_h.
```

So:

```text
p = q_phi0
```

if and only if:

```text
delta_h = 0.
```

The earlier constant H1 source filter supports this in the self-consistent
case.

If:

```text
s = 1/9,
```

then the radial power branches are:

```text
q = 1/3
q = 2/3.
```

Finite C1 action rejects:

```text
q = 2/3.
```

The remaining branch:

```text
q = 1/3
```

has the same slope at every radius, so:

```text
delta_h = 0.
```

Two-hundred-fifty-sixth verdict:

```text
p=q is supported if the H1 source is constant through the collar.
```

The open gate is now:

```text
does the native phi0 boundary layer enforce delta_h=0,
or does it allow source running?
```

This is narrower than postulating:

```text
q = 1/3.
```

We can instead seek:

```text
constant H1 source / no collar renormalization.
```

## 272. Reduced gate budget after H1

Implemented in `native_reduced_gate_budget_after_h1.py`.

The current work reduces several earlier postulates into sharper gates.

```text
q=1/3 / P_phi0:
    old status: banked minimal postulate
    new status: conditional theorem from H1 self-consistency if p=q

p=q:
    old status: part of self-similar assumption
    new status: equivalent to delta_h=0; supported by constant H1 source
                plus finite action

H1 selector:
    old status: plausible lowest nonconstant angular sector
    new status: strengthened by exact ell=0 trivial-branch exclusion

eta/2 side action:
    old status: plausible half-boundary convention
    new status: conditional theorem from symmetric composable gluing

factor 3:
    old status: channel multiplicity candidate
    new status: dim H1 after ell=0 exclusion, if physical role is
                boundary-state count
```

Two-hundred-fifty-seventh verdict:

```text
The postulate load has decreased.
```

The remaining irreducible gates are:

```text
1. no collar source running: delta_h=0,
2. intrinsic/interface-local transfer action,
3. boundary-state counting rather than averaging.
```

The first gate would upgrade:

```text
P_phi0
```

from a banked postulate to a derived consequence of:

```text
H1 self-consistency.
```

The second and third gates decide whether:

```text
gamma = 3 exp(-1/36)
```

is the correct transfer multiplier or merely one branch among alternatives.

## 273. Orchestra ponder gate scan

Implemented in `native_orchestra_ponder_gate_scan.py`.

An orchestra-based scan is appropriate now because the work has narrowed to
three precise gates:

```text
1. no collar source running: delta_h=0,
2. intrinsic/interface-local transfer action,
3. boundary-state counting rather than averaging.
```

The scan should not search for a new force-like mechanism. It should ask which
native metric instruments can address those gates.

Current priority map:

```text
phi0 boundary variation:
    native object:
        C1 boundary momentum, induced S2 metric, extrinsic-curvature jump
    gates addressed:
        delta_h=0; interface-local transfer; possibly boundary-state count
    promise:
        highest: all current gates touch this object
    risk:
        can become an imposed boundary action if not derived from variation
    next probe:
        write the local phi0 variation in variables (F, q, n_a, H1 data)
        and identify value/action terms

collar source-running law:
    native object:
        q-flow dq/dt=q^2-q+2s(t) and H1 angular source
    gates addressed:
        delta_h=0
    promise:
        high: directly decides whether P_phi0 is derived
    risk:
        approximating s(t) would reintroduce linearization drift
    next probe:
        derive whether H1 shell source is constant along the collar or
        distributional at phi0

Calderon/interface Cauchy data:
    native object:
        boundary map relating field value and normal derivative at phi0
    gates addressed:
        interface-local transfer versus bulk-DtN branch
    promise:
        high: exact branch discriminator
    risk:
        ordinary PDE probe may not be the physical mass-transfer action
    next probe:
        construct the UDT phi0 Cauchy-data space and ask whether it is local
        or collar-memory bearing

H1 boundary-state measure:
    native object:
        round S2 H1 triplet, isotropic shell stress, transported angular frame
    gates addressed:
        boundary-state counting rather than averaging
    promise:
        medium-high: decides trace versus average
    risk:
        easy to confuse degeneracy count with normalized probability
    next probe:
        classify the boundary object as state-count, transition amplitude,
        average, or determinant

compact/Hopf bridge:
    native object:
        primitive U1 line bundle and CP1 -> S2/H1 map
    gates addressed:
        later branch/node independence; not primary current gates
    promise:
        medium: important for M1 participation in the same H1 frame
    risk:
        can overcount if Hopf data merely reuses existing H1 variables
    next probe:
        only revisit after phi0/H1 transfer kernel is fixed

Coulomb phi-blind sector:
    native object:
        Maxwell cancellation in UDT metric
    gates addressed:
        later residual/branch shifts; not primary current gates
    promise:
        medium-low for current theorem, higher for corrections
    risk:
        tempting to import force analogs
    next probe:
        defer until transfer kernel and q/eta chain are settled

angular determinant/RG finite part:
    native object:
        regulated S2/H1 operator determinants
    gates addressed:
        possibly later coefficient corrections, not current gates
    promise:
        low now
    risk:
        high scheme/fitting risk
    next probe:
        defer unless a fixed subtraction rule is derived from boundary action
```

Two-hundred-fifty-eighth verdict:

```text
The orchestra scan says the current bottleneck is still the phi0 boundary
variation, not a new mechanism.
```

The most promising unknown metric mechanism is:

```text
an interface-local phi0 boundary action/variation that simultaneously
controls q-flow, H1 coupling, and state counting.
```

This could look like several instruments only after decomposition:

```text
radial momentum jump,
angular shell stress,
H1 bridge,
side-symmetric gluing,
state-count measure.
```

But they may all be shadows of one native boundary variational object.

## 274. phi0 variation variable ledger

Implemented in `native_phi0_variation_variable_ledger.py`.

Use the local `phi0` variables:

```text
F = f(phi0)
q = -R f'(R)/F
n_a = H1/projective unit direction on S2
P_H1 = projector onto the ell=1 triplet.
```

The C1 boundary momentum is:

```text
Pi_F = (1/2) R^2 f'(R).
```

At:

```text
F = 1,
```

the scale-normalized inward momentum is:

```text
-Pi_F/R = q/2.
```

A local boundary functional near `F = 1` has the expansion:

```text
S_b(F,n) = S_0[n] + S_1[n](F - 1) + O((F - 1)^2).
```

Momentum closure fixes:

```text
S_1 = q/2.
```

With H1 direction resolution:

```text
S_1,ab = (q/2) n_a n_b.
```

Round-S2 averaging gives:

```text
<S_1,ab> = (q/6) delta_ab.
```

For:

```text
q = 1/3,
```

this gives:

```text
q/2 = 1/6
q/6 = 1/18.
```

Two-hundred-fifty-ninth verdict:

```text
The local F-variation fixes the scalar edge momentum scale and its H1/S2
isotropic projection.
```

It does not fix:

```text
S_0[n], the value/action term,
whether q is forced to 1/3,
whether delta_h=0,
whether the transfer operation is a trace, average, or determinant.
```

So the phi0 boundary variation must have more structure than the first
`F`-derivative if it is to close all three remaining gates.

## 275. Minimal phi0 boundary object requirements

Implemented in `native_minimal_phi0_boundary_object_requirements.py`.

A full `phi0` boundary object that closes the current gates must supply five
things.

1. Momentum closure:

```text
dS_b/dF |F=1 = q/2.
```

2. Full H1 value action:

```text
S_0|H1 = eta I3 = (q/6) I3.
```

3. One-sided composable transfer:

```text
A_side|H1 = (eta/2) I3 = (q/12) I3.
```

4. H1 state-count operation:

```text
gamma = Tr_H1 exp(-A_side).
```

5. `q` selection or `q` preservation:

```text
either q = 1/3 directly,
or p = q plus H1 self-consistency.
```

For:

```text
q = 1/3,
```

the exact values are:

```text
q/2 = 1/6
eta = q/6 = 1/18
eta/2 = q/12 = 1/36.
```

Two-hundred-sixtieth verdict:

```text
Items 1-4 can belong to an interface-local transfer object.
```

But:

```text
item 5 is a collar/self-consistency condition unless the boundary variation
contains an independent q-stationarity equation.
```

So the likely orchestra split is:

```text
phi0 interface action -> eta, H1 coupling, half split, trace role,
collar/source self-consistency -> q=1/3 through p=q.
```

## 276. q stationarity requirement

Implemented in `native_q_stationarity_requirement.py`.

The C1 radial action in `f` is:

```text
S_C1 = (1/4) int r^2 f'^2 dr.
```

Its variation gives the boundary term:

```text
delta S_C1,boundary = Pi_F delta F
Pi_F = (1/2) R^2 f'(R).
```

There is no independent:

```text
delta q
```

boundary term in this first-order variational problem.

Therefore a local boundary functional of the form:

```text
S_b(F,n)
```

can cancel:

```text
Pi_F delta F,
```

but cannot by itself impose stationarity with respect to:

```text
q = -R f'(R)/F.
```

To select `q` locally, one of the following must be true:

```text
1. the boundary functional depends on slope/extrinsic-curvature data,
2. the variational principle is rewritten in phase-space form,
3. q is selected by a collar bulk/self-consistency equation instead.
```

Two-hundred-sixty-first verdict:

```text
Direct q selection is not supplied by the ordinary C1 endpoint variation.
```

The current native route is therefore:

```text
collar self-consistency / no source running,
```

unless:

```text
a genuine slope/joint boundary term is derived.
```

## 277. delta_h integral gate

Implemented in `native_delta_h_integral_gate.py`.

For the radial equation:

```text
f'' + 2 f'/r + 2 s(r) f/r^2 = 0,
```

use:

```text
t = ln r
q(t) = -d ln f/dt.
```

Then the exact q-flow is:

```text
dq/dt = q^2 - q + 2s(t).
```

If `p` is the endpoint exponent and `q_phi0` is the collar slope:

```text
delta_h = q_phi0 - p.
```

Therefore:

```text
delta_h = int_endpoint^phi0 [q^2 - q + 2s(t)] dt.
```

For the constant self-consistent H1 branch:

```text
q = 1/3
s = q(1 - q)/2 = 1/9
dq/dt = 0
delta_h = 0.
```

Two-hundred-sixty-second verdict:

```text
No collar renormalization is an exact integral condition on q-flow.
```

A hidden metric mechanism could enforce it in three ways:

```text
1. make the H1 source constant at s=1/9,
2. allow source running but make the total q-flow integral vanish,
3. impose a boundary condition that fixes q_phi0=p.
```

This gives a precise target for the next scan:

```text
find whether the metric supplies constant source, integral cancellation,
or a q-matching boundary condition.
```

## 278. q-flow enforcement route scan

Implemented in `native_q_flow_enforcement_route_scan.py`.

The exact `delta_h` gate has three possible enforcement routes, plus one
profile-memory branch.

Constant H1 source:

```text
metric object:
    phi-blind ell=1 angular eigenvalue and isotropic H1 shell stress
how it would enforce delta_h=0:
    s(t)=1/9 throughout the active collar makes q=1/3 a fixed solution
status:
    best current route, but source constancy is not derived
next test:
    derive whether the H1 source is a collar density or a phi0-local delta source
```

Integral cancellation:

```text
metric object:
    two-sided phi bridge and possible positive/negative source regions
how it would enforce delta_h=0:
    nonconstant q-flow integrates to zero between endpoint and phi0
status:
    possible but less clean; high risk of disguised fitting
next test:
    look for an exact antisymmetry or conservation law before using it
```

q-matching boundary condition:

```text
metric object:
    joint/slope boundary term or phase-space endpoint condition
how it would enforce delta_h=0:
    variation imposes q_phi0=p directly
status:
    possible only if a genuine slope/extrinsic-curvature boundary term exists
next test:
    derive a UDT-native joint term; do not import GHY/Israel dynamics blindly
```

Bulk DtN memory:

```text
metric object:
    warped collar Cauchy-data map
how it affects delta_h:
    does not enforce delta_h=0; instead keeps profile dependence
status:
    important discriminator, but opposite of simple branch
next test:
    use only if transfer action is bulk propagation rather than interface-local
```

Two-hundred-sixty-third verdict:

```text
The cleanest no-running route is constant H1 source.
```

The other two simple-branch routes are stricter:

```text
integral cancellation requires an exact symmetry/conservation law,
direct q-matching requires a real slope/joint boundary term.
```

So the immediate target becomes:

```text
is the H1 source a constant collar density, or only a localized phi0 shell?
```

## 279. Shell versus collar source split

Implemented in `native_shell_vs_collar_source_split.py`.

Two different source localizations have different mathematical jobs.

Collar density:

```text
s(t) = 1/9 across the active collar.
```

Then:

```text
dq/dt = q^2 - q + 2s
```

has:

```text
q = 1/3
```

as a fixed solution.

This supports:

```text
delta_h = 0
```

and therefore the conditional derivation of:

```text
P_phi0.
```

Localized `phi0` shell:

```text
source concentrated at the interface.
```

This changes:

```text
boundary momentum / jump.
```

It supports:

```text
eta as an interface-local transfer scale.
```

But it does not by itself prove:

```text
q was constant through the collar.
```

Two-hundred-sixty-fourth verdict:

```text
The same metric may supply both instruments, but they are not the same
mathematical object.
```

In orchestra language:

```text
collar density addresses q preservation,
phi0 shell stress addresses interface transfer.
```

This resolves the apparent tension:

```text
P_phi0 derivation wants collar constancy,
gamma transfer wants interface locality.
```

They can coexist if the metric supplies a constant H1 collar source whose
integrated endpoint terminates in a localized `phi0` shell stress.

## 280. Revised orchestra architecture

Implemented in `native_revised_orchestra_architecture.py`.

The current best architecture is layered.

H1 collar source:

```text
role:
    preserve endpoint slope through the collar
exact output:
    delta_h=0 and q=1/3 if s=1/9 is constant
open gate:
    derive source constancy from metric/angular data
```

phi0 shell stress:

```text
role:
    localize the boundary momentum and angular transfer scale
exact output:
    q/2 shell scale and eta=q/6 after H1/S2 projection
open gate:
    derive full S0 value action, not only F-derivative
```

Symmetric interface gluing:

```text
role:
    turn full boundary action into one-sided transfer
exact output:
    A_side=(eta/2)I3 on H1
open gate:
    prove transfer object is composable and side-symmetric
```

H1 boundary-state measure:

```text
role:
    count unlabelled bridge channels
exact output:
    Tr_H1 exp[-(eta/2)I3] = 3 exp(-eta/2)
open gate:
    prove state counting rather than averaging
```

Two-hundred-sixty-fifth verdict:

```text
The current best architecture is not one mechanism.
```

It is a layered metric orchestra:

```text
collar source -> q preservation,
phi0 shell -> eta transfer scale,
symmetric gluing -> eta/2 side action,
H1 state measure -> factor 3 trace.
```

This avoids both failure modes:

```text
1. pretending one object does every job,
2. inventing unrelated mechanisms when the metric already supplies linked roles.
```

## 281. H1 source localization criterion

Implemented in `native_h1_source_localization_criterion.py`.

There are two exact ways an H1 source can enter the radial problem.

Collar density:

```text
f'' + 2f'/r + 2s(r)f/r^2 = 0.
```

This source acts on every linking `S2` through the collar.

Localized shell:

```text
f'' contains Delta f' delta(r - R).
```

This source changes the boundary momentum jump at `phi0`.

The localization criterion is:

```text
If the H1 angular structure is transported as data on each linking S2,
it is a collar-density candidate.
```

But:

```text
If the H1 angular structure exists only as a matching/jump condition at F=1,
it is a shell candidate.
```

Two-hundred-sixty-sixth verdict:

```text
The normalized H1 spectrum is collar-constant, but source localization is
not decided by the spectrum alone.
```

What must be determined is:

```text
does H1 live as transported collar data,
or only as terminal phi0 interface data?
```

## 282. H1 transport versus activation

Implemented in `native_h1_transport_vs_activation.py`.

Two pieces must be separated.

H1 transport:

```text
L1 = (-r^2 Delta_S2)/2 = I3
```

on every linking `S2`.

Status:

```text
metric-derived.
```

Consequence:

```text
the H1 frame is available throughout the collar.
```

H1 activation:

```text
the radial f equation couples to H1 with source s=1/9.
```

Status:

```text
not derived.
```

Consequence:

```text
needed for q=1/3 fixed flow.
```

H1 source constancy:

```text
s(t) is independent of collar position.
```

Status:

```text
conditional.
```

Consequence:

```text
follows if the activation coefficient is built only from normalized H1 geometry.
```

H1 shell transfer:

```text
same H1 frame receives localized phi0 jump/stress.
```

Status:

```text
partly derived.
```

Consequence:

```text
supports eta as interface-local transfer scale.
```

Two-hundred-sixty-seventh verdict:

```text
The metric derives H1 transport, not H1 activation.
```

Therefore the source-constancy gate becomes:

```text
derive that the H1 activation coefficient is built only from normalized,
phi-blind H1 geometry.
```

If that is true:

```text
s(t) = constant.
```

If not:

```text
s(t) may run through amplitude, branch, or boundary-layer data.
```

## 283. Constant source activation requirements

Implemented in `native_constant_source_activation_requirements.py`.

The radial source equation is:

```text
f'' + 2f'/r + 2s f/r^2 = 0.
```

The intrinsic scalar curvature of the linking sphere is:

```text
R2 = 2/r^2.
```

Therefore:

```text
2s f/r^2 = s R2 f.
```

A constant source follows if:

```text
1. the active source is a fixed fraction of R2,
2. the fraction is built from normalized H1/S2 data,
3. no radial amplitude/window multiplies the source.
```

For:

```text
s = 1/9,
```

the source is:

```text
(1/9) R2 f.
```

Two-hundred-sixty-eighth verdict:

```text
Constant s is native if H1 activation is a fixed curvature-share.
```

But:

```text
any radial amplitude, window, or branch-dependent normalization makes s(t)
run and reopens delta_h.
```

So the next exact target is:

```text
derive a fixed H1 curvature-share coupling, not a radial source profile.
```

## 284. one-ninth two-factor curvature share

Implemented in `native_one_ninth_two_factor_curvature_share.py`.

The target source strength is:

```text
s = 1/9,
```

so:

```text
source = (1/9) R2 f.
```

A single S2/H1 isotropic projection gives:

```text
<n_a n_b> = delta_ab/3.
```

That supplies:

```text
1/3,
```

not:

```text
1/9.
```

The non-circular two-factor route is:

```text
source fraction = curvature-share factor x H1 projection factor
                = (1/3) x (1/3)
                = 1/9.
```

Required independence:

```text
the first 1/3 must be a curvature/source share,
the second 1/3 must be an H1/S2 projection share,
and they must not be the same projection counted twice.
```

Two-hundred-sixty-ninth verdict:

```text
s=1/9 is derivable only if the metric supplies two independent one-third
factors.
```

A single isotropic projection is insufficient.

Thus the fixed-curvature-share route needs:

```text
independent curvature-share 1/3
```

plus:

```text
independent H1/S2 projection 1/3.
```

## 285. Self-coupled curvature-share source

Implemented in `native_self_coupled_curvature_share_source.py`.

There is a less circular way to use the curvature-share factor.

At `phi0`:

```text
R3/R2 = q.
```

If H1 activation uses:

```text
curvature-share factor q
```

times:

```text
independent H1/S2 projection 1/3,
```

then the source law is:

```text
s(q) = q/3.
```

Endpoint/collar self-consistency requires:

```text
q(1 - q)/2 = s(q).
```

So:

```text
q(1 - q)/2 = q/3.
```

The solutions are:

```text
q = 0
```

and:

```text
q = 1/3.
```

The nontrivial branch is:

```text
q = 1/3.
```

Then:

```text
s = q/3 = 1/9
eta = q/6 = 1/18.
```

Two-hundred-seventieth verdict:

```text
This route does not assume the curvature share is already one third.
```

It assumes the source law:

```text
s(q) = q/3,
```

then self-consistency selects:

```text
q = 1/3
```

as the nontrivial branch.

The remaining derivation target is now sharper:

```text
derive H1 activation as curvature-share q times independent H1/S2 projection 1/3.
```

## 286. Self-coupled q-flow

Implemented in `native_self_coupled_q_flow.py`.

Start with the exact q-flow:

```text
dq/dt = q^2 - q + 2s(q).
```

For the self-coupled curvature-share source:

```text
s(q) = q/3.
```

Then:

```text
dq/dt = q^2 - q + 2q/3
      = q^2 - q/3
      = q(q - 1/3).
```

The fixed branches are:

```text
q = 0
q = 1/3.
```

On the nontrivial branch:

```text
q = 1/3
s(q) = 1/9
dq/dt = 0
delta_h = 0.
```

Two-hundred-seventy-first verdict:

```text
s(q)=q/3 is not a constant-source assumption off shell.
```

It becomes:

```text
s = 1/9
```

on the selected fixed branch:

```text
q = 1/3.
```

This can derive `P_phi0` if:

```text
the source law s(q)=q/3 is native.
```

## 287. s(q)=q/3 status audit

Implemented in `native_s_q_over_three_status_audit.py`.

The candidate source law:

```text
s(q) = q/3
```

has exact ingredients.

Curvature-share identity:

```text
R3/R2 = q at phi0.
```

Status:

```text
exact metric identity.
```

H1 projection factor:

```text
<n_a n_b> = delta_ab/3.
```

Status:

```text
exact round-S2 average.
```

Source law:

```text
s(q) = q/3.
```

Status:

```text
candidate coupling, not yet variationally derived.
```

Fixed branch:

```text
q = 1/3
s = 1/9.
```

Status:

```text
exact consequence if the source law holds.
```

Two-hundred-seventy-second verdict:

```text
The ingredients of s(q)=q/3 are exact.
```

But:

```text
the multiplication into a source law is the remaining gate.
```

Therefore:

```text
derive s(q)=q/3 from the boundary/collar action before treating P_phi0 as
fully derived.
```

## 288. Updated P_phi0 route after source scan

Implemented in `native_updated_p_phi0_route_after_source_scan.py`.

The source-localization scan updates the best route to `P_phi0`.

```text
H1 transport:
    status: derived
    output: H1 frame exists on every linking S2

curvature-share identity:
    status: derived
    output: R3/R2=q at phi0

H1 projection:
    status: derived
    output: projection factor 1/3

activation law:
    status: open gate
    output: s(q)=q/3

self-coupled q-flow:
    status: conditional theorem
    output: dq/dt=q(q-1/3)

nontrivial fixed branch:
    status: conditional theorem
    output: q=1/3, s=1/9, eta=1/18, delta_h=0
```

Two-hundred-seventy-third verdict:

```text
The route to P_phi0 now hinges on deriving s(q)=q/3.
```

If that activation law is native:

```text
q=1/3 is not postulated.
```

It follows as:

```text
the nontrivial fixed branch of the self-coupled curvature-share q-flow.
```

This is the sharpest current mathematical target:

```text
derive or reject the activation law s(q)=q/3.
```

## 289. Boundary functional q correction

Implemented in `native_boundary_functional_q_correction.py`.

Some earlier notes used the shorthand:

```text
a conjugate boundary functional can set q through dS/df=q/2.
```

The stricter variational reading is:

```text
dS/df cancels the C1 boundary momentum for the q supplied by the
interior/collar solution.
```

It selects `q` only if:

```text
1. S_b contains an independent slope/extrinsic-curvature variable, or
2. varying the full boundary/collar action gives a q stationarity equation.
```

Otherwise:

```text
q is inherited from the collar q-flow/self-consistency problem.
```

Two-hundred-seventy-fourth verdict:

```text
Do not treat dS/df=q/2 as a derivation of q.
```

It is:

```text
a momentum-matching condition
```

unless:

```text
a q-variation is present.
```

This reinforces the current route:

```text
derive q through source law / q-flow,
then use the boundary functional to carry the phi0 momentum and H1 transfer.
```

## 290. Activation law alternative scan

Implemented in `native_activation_law_alternative_scan.py`.

To avoid myopia, scan nearby simple activation laws.

For:

```text
s(q) = c q,
```

self-consistency gives:

```text
q(1 - q)/2 = c q.
```

Thus:

```text
q = 0
```

or:

```text
q = 1 - 2c.
```

Candidate laws:

```text
no projection:
    law: s=q
    nonzero fixed branch: q=-1
    status: rejects finite positive nontrivial branch

single radial-angular plane share:
    law: s=q/2
    nonzero fixed branch: q=0
    status: rejects finite positive nontrivial branch

H1/S2 projection share:
    law: s=q/3
    nonzero fixed branch: q=1/3
    status: finite positive branch

two-plane plus H1 mixed share:
    law: s=q/6
    nonzero fixed branch: q=2/3
    status: non-finite or threshold-risk branch for C1 endpoint

fixed constant source:
    law: s=1/9
    fixed branches: q=1/3 and q=2/3
```

Two-hundred-seventy-fifth verdict:

```text
s=q/3 is special among simple projection laws because it gives q=1/3,
the finite self-similar branch.
```

Other nearby natural-looking coefficients either:

```text
kill the finite positive branch,
```

or:

```text
move it to the non-finite companion branch q=2/3.
```

This does not derive `s=q/3`, but it raises its priority as the only simple
projection law in this family that lands on the finite nontrivial branch.

## 291. Activation coefficient selection logic

Implemented in `native_activation_coefficient_selection_logic.py`.

Compare simple coefficient-selection logics.

Use full curvature share:

```text
coefficient: c=1
metric reason: activate all spatial curvature share without projection
problem: over-activates; no finite positive branch
```

Use one radial-angular plane:

```text
coefficient: c=1/2
metric reason: split q across two radial-angular planes
problem: selects only trivial branch
```

Use H1 isotropic channel share:

```text
coefficient: c=1/3
metric reason: project scalar curvature share into three equivalent H1 channels
problem: best current candidate; needs variational activation proof
```

Use radial plane plus H1 share:

```text
coefficient: c=1/6
metric reason: combine per-plane share with H1 projection
problem: lands on non-finite companion branch
```

Two-hundred-seventy-sixth verdict:

```text
The c=1/3 law has the cleanest metric role:
scalar curvature-share activation distributed over the three transported H1
channels.
```

It remains:

```text
a variational coupling gate.
```

This suggests the source law should be read as:

```text
s(q) = one H1 channel share of the scalar curvature-share q.
```

## 292. Revised architecture with self-coupled source

Implemented in `native_revised_architecture_with_self_coupled_source.py`.

The orchestra architecture can be sharpened again.

Self-coupled H1 collar source:

```text
revised role:
    one H1 channel share of scalar curvature-share q
output:
    s(q)=q/3 -> q-flow dq/dt=q(q-1/3)
remaining gate:
    derive the activation law from boundary/collar variation
```

Finite-action branch filter:

```text
revised role:
    reject trivial or companion non-finite branches
output:
    selects nontrivial finite q=1/3 branch if activation law holds
remaining gate:
    verify no hidden running/window alters the source law
```

phi0 shell transfer:

```text
revised role:
    carry q/2 boundary momentum into H1-projected eta
output:
    eta=q/6=1/18 on q=1/3 branch
remaining gate:
    derive S0 value action
```

H1 state-count transfer:

```text
revised role:
    count unlabelled H1 bridge channels
output:
    gamma=3 exp(-eta/2) if trace role holds
remaining gate:
    derive state-count measure rather than average
```

Two-hundred-seventy-seventh verdict:

```text
The collar layer is now best framed as a self-coupled channel-share law,
not as an assumed constant source.
```

That law is:

```text
s(q)=q/3.
```

If derived, it makes:

```text
q=1/3
```

the nontrivial fixed branch rather than an imposed value.

## 293. Big ponder hyperfocus audit

Implemented in `native_big_ponder_hyperfocus_audit.py`.

Question:

```text
Are we hyperfocused on s(q)=q/3, or is it the promising route?
```

Route audit:

```text
self-coupled H1 activation s(q)=q/3:
    promise:
        uses exact ingredients R3/R2=q and H1 projection 1/3;
        gives q=1/3 as fixed branch
    hyperfocus risk:
        multiplication into a source law is not yet variationally derived
    continue if:
        derive a boundary/collar action term whose variation activates one
        H1 channel share of q
    demote if:
        no action term can couple curvature-share q to H1 activation without
        an arbitrary multiplier

interface-local phi0 shell transfer:
    promise:
        eta carrier is localized and angular-only; matches transfer locality
    hyperfocus risk:
        does not by itself preserve q through the collar
    continue if:
        derive S0 value action on H1 from the shell functional
    demote if:
        shell action only cancels Pi_F and supplies no H1 value action

warped bulk DtN branch:
    promise:
        exact positional-dilation refactor; preserves H1 triplet with Bessel
        dressing
    hyperfocus risk:
        may be a probe-propagation object rather than mass-transfer action
    continue if:
        boundary transfer is shown to arise by eliminating the collar bulk
    demote if:
        transfer is shown to be interface-local and profile-independent

q-matching slope/joint term:
    promise:
        could select p=q directly
    hyperfocus risk:
        high risk of importing GR joint machinery
    continue if:
        derive a UDT-native slope/extrinsic-curvature variation
    demote if:
        only standard Dirichlet GHY cancellation is available

integral cancellation:
    promise:
        would allow source running without changing q_phi0
    hyperfocus risk:
        highest fitting risk unless backed by exact symmetry
    continue if:
        find exact conservation/antisymmetry forcing integral q-flow to vanish
    demote if:
        cancellation is only arranged by chosen source profile
```

Two-hundred-seventy-eighth verdict:

```text
Continue on s(q)=q/3 as the primary route, but only as an activation-law
derivation problem.
```

Do not keep doing q-flow algebra just because it is productive. The next test
must be:

```text
can the boundary/collar action actually produce s(q)=q/3?
```

Keep two branches alive as guards against tunnel vision:

```text
interface shell branch:
    if transfer is local at phi0

warped DtN branch:
    if transfer is bulk-collar propagation
```

Stop condition for the primary route:

```text
if s(q)=q/3 cannot be produced without inserting the multiplier by hand,
demote it back to a conditional postulate.
```

## 294. Activation action requirements

Implemented in `native_activation_action_requirements.py`.

To produce the radial source equation:

```text
f'' + 2f'/r + 2s(q) f/r^2 = 0,
```

an action term must contribute to the Euler-Lagrange equation as:

```text
+ 2s(q) f/r^2.
```

Equivalently, after multiplying by `r^2`, the source contribution is:

```text
2s(q) f.
```

For:

```text
s(q)=q/3,
```

the required contribution is:

```text
(2q/3) f.
```

A boundary-only term:

```text
S_b(F,n)
```

cannot produce this collar bulk source.

It can only change:

```text
endpoint momentum/value conditions.
```

Therefore `s(q)=q/3` requires one of:

```text
1. a collar-local action density proportional to q times H1 share,
2. a phase-space/slope boundary term whose variation is equivalent to such
   a collar source,
3. a derived reduction where eliminating H1 collar data induces the source.
```

Two-hundred-seventy-ninth verdict:

```text
The activation law cannot be derived from the existing endpoint-only H1
boundary skeleton.
```

It needs:

```text
a collar action
```

or:

```text
a slope/joint action.
```

This is the first hard test of the primary route.

## 295. Collar action source test

Implemented in `native_collar_action_source_test.py`.

Use the radial variational form:

```text
S = int [(1/4) r^2 f'^2 - V(f,r)] dr.
```

The Euler-Lagrange equation is:

```text
(1/2 r^2 f')' + dV/df = 0.
```

Equivalently:

```text
f'' + 2f'/r + 2(dV/df)/r^2 = 0.
```

To get:

```text
f'' + 2f'/r + 2s(q) f/r^2 = 0,
```

we need:

```text
dV/df = s(q) f.
```

So:

```text
V = (1/2)s(q)f^2.
```

For:

```text
s(q)=q/3,
```

this would be:

```text
V = (q/6) f^2.
```

Problem:

```text
q = -r f'/f.
```

Therefore:

```text
V = (q/6)f^2
```

is not an ordinary potential:

```text
V(f,r).
```

It is derivative-dependent unless `q` is treated as an independent collar or
phase-space variable.

Two-hundred-eightieth verdict:

```text
A simple local potential can generate a fixed s, but s(q)=q/3 requires
derivative-dependent or phase-space collar structure.
```

This does not kill the route, but it tightens it:

```text
s(q)=q/3 is not produced by an ordinary f-only collar potential.
```

## 296. Derivative-dependent activation test

Implemented in `native_derivative_dependent_activation_test.py`.

The naive derivative-dependent candidate for:

```text
s(q)=q/3
```

would be:

```text
V = (q/6)f^2,
```

with:

```text
q = -r f'/f.
```

Substitute:

```text
V = -(r/6) f f'.
```

But:

```text
r f f' = (r/2)(f^2)'
       = (1/2)(r f^2)' - (1/2)f^2.
```

Therefore:

```text
V = -(1/12)(r f^2)' + (1/12)f^2.
```

Up to a boundary term, this is:

```text
V_eff = (1/12)f^2.
```

Then:

```text
dV_eff/df = f/6.
```

So the source is:

```text
s = 1/6.
```

Two-hundred-eighty-first verdict:

```text
The naive derivative substitution V=(q/6)f^2 does not produce the intended
self-coupled source.
```

Up to a boundary term it becomes:

```text
a fixed s=1/6 potential.
```

That is the wrong activation law and lands on the non-finite companion branch.

Therefore:

```text
s(q)=q/3 requires a more genuine phase-space or constrained-variable action,
not a simple substitution q=-rf'/f inside an ordinary potential.
```

## 297. Constrained q action test

Implemented in `native_constrained_q_action_test.py`.

Try treating `q` as an independent collar variable with constraint:

```text
q + r f'/f = 0.
```

Candidate action structure:

```text
S = int [ (1/4) r^2 f'^2 - (q/6)f^2
          + lambda(q + r f'/f) ] dr.
```

Variations give:

```text
delta lambda:
    q + r f'/f = 0
```

and:

```text
delta q:
    -f^2/6 + lambda = 0
    lambda = f^2/6.
```

The multiplier is fixed algebraically, but this does not by itself select:

```text
q = 1/3.
```

`q` still follows from the coupled `f` equation.

Risk:

```text
The term -(q/6)f^2 was inserted to force s(q)=q/3.
```

Unless that term is derived, the constrained-variable action only repackages
the postulate.

Two-hundred-eighty-second verdict:

```text
Promoting q to an independent variable is mathematically possible, but it
does not derive the activation law.
```

The open native-origin question becomes:

```text
why should the collar action contain q f^2 / 6?
```

## 298. q f^2 / 6 origin scan

Implemented in `native_qf2_over_six_origin_scan.py`.

The activation-law route now requires a native origin for:

```text
q f^2 / 6.
```

Scan of possible origins:

```text
bare C1 radial action:
    native object: (1/4) r^2 f'^2
    can supply: no; supplies kinetic term and endpoint momentum only
    verdict: reject as source of q f^2/6

ordinary f-only potential:
    native object: V(f,r)
    can supply: no for q-dependent source; q contains f'
    verdict: reject for s(q)=q/3

naive derivative substitution:
    native object: V=(q/6)f^2 with q=-rf'/f
    can supply: no; reduces to boundary term plus fixed s=1/6
    verdict: reject

constrained q phase-space action:
    native object: independent q plus constraint q+rf'/f=0
    can supply: only if q f^2/6 term is itself supplied
    verdict: repackages gate, does not derive it

EH/curvature primitive atlas:
    native object: B_EH=-r^2 f' at phi0
    can supply: identifies q boundary jump, not collar q f^2 action
    verdict: useful atlas, not enough

H1 projected boundary action:
    native object: B<n_a n_b>
    can supply: supplies eta projection after scalar budget exists
    verdict: transfer support, not collar activation

unknown collar H1 action:
    native object: transported H1 data on each linking S2
    can supply: possible if variation produces q f^2/6
    verdict: only remaining primary-route source
```

Two-hundred-eighty-third verdict:

```text
Known C1/boundary/curvature pieces do not yet derive q f^2/6.
```

Therefore:

```text
the primary s(q)=q/3 route survives only as an unknown collar H1 action.
```

This is a demotion pressure, not a rejection:

```text
continue only by searching for a genuine collar H1 action;
otherwise demote s(q)=q/3 to a conditional postulate.
```

## 299. Post action-test route status

Implemented in `native_post_action_test_route_status.py`.

The action tests change the route status.

```text
s(q)=q/3 primary route:
    status:
        under demotion pressure
    reason:
        known C1/boundary/curvature pieces do not derive q f^2/6
    next action:
        search only for a genuine collar H1 action; otherwise demote to
        conditional postulate

interface-local transfer theorem:
    status:
        still strong conditional
    reason:
        eta carrier and H1 triplet are interface-local once q is supplied
    next action:
        derive S0 value action and state-count role

warped DtN branch:
    status:
        kept as discriminator
    reason:
        exact if transfer is bulk propagation through collar
    next action:
        do not use unless transfer is shown to be bulk-eliminated

q from direct slope/joint term:
    status:
        open but risky
    reason:
        requires genuine UDT slope variation
    next action:
        only pursue if a native joint term appears
```

Two-hundred-eighty-fourth verdict:

```text
Do not force s(q)=q/3.
```

It remains:

```text
promising but unproved.
```

The next valid step is:

```text
a targeted search for a native collar H1 action.
```

If that search fails:

```text
demote s(q)=q/3 to a conditional postulate and continue with the
interface-local transfer theorem as conditional on q.
```

## 300. phi0 quasilocal slope-density identity

Implemented in `native_phi0_quasilocal_slope_density.py`.

A useful GR-atlas object for the same metric form is the Misner-Sharp
mass function:

```text
m_MS(r) = r(1-f)/2.
```

This is not imported as a UDT mass mechanism.  It is used only as an
exact metric identity for the ansatz.

Its exact derivative is:

```text
m_MS'(r) = (1 - f - r f')/2.
```

The spatial scalar curvature identity is:

```text
R3 = 2(1 - f - r f')/r^2,
```

so:

```text
R3 = 4 m_MS'/r^2.
```

At a phi0 collar:

```text
f(R)=1,
q=-R f'(R)/f(R)=-R f'(R).
```

Therefore:

```text
m_MS(R)=0,
m_MS'(R)=q/2,
R3/R2=q,        R2=2/R^2.
```

This is a sharper version of the positive-background / negative-phi
access idea:

```text
phi0 can hide the quasilocal value channel while exposing the
quasilocal slope-density channel.
```

For q=1/3:

```text
m_MS'(R)=1/6,
R3/R2=1/3,
H1-projected boundary unit=(q/2)/3=1/18.
```

Two-hundred-eighty-fifth verdict:

```text
The same collar q appears as:

    C1 boundary momentum density:      q/2
    Brown-York angular stress unit:    q/2
    Misner-Sharp slope-density:        q/2
    spatial curvature fraction:        q
    H1 projection of q/2:              q/6.
```

This is not yet a derivation of q=1/3.

But it is real progress under the uncover-the-metric frame:

```text
several exact metric instruments are playing the same collar note.
```

## 301. Collar H1 action accept/reject gate

Implemented in `native_collar_h1_action_accept_reject_gate.py`.

Any proposed native collar H1 action must pass all of the following
gates.

```text
collar support:
    requirement:
        the object must live on S2 x I, not only on the phi0 endpoint
    rejects:
        pure boundary counterterms and value-only shell actions

native H1 carrier:
    requirement:
        the H1 triplet must enter through round-S2 geometry,
        transported H1 data, or an exact edge mode
    rejects:
        a hand-added three-state multiplier

q source without substitution trick:
    requirement:
        variation must supply the same effect as dV/df=(q/3)f without
        replacing q by -r f'/f inside an ordinary potential
    rejects:
        the naive q f^2/6 term that collapses to fixed s=1/6

curvature-share origin:
    requirement:
        the q dependence should trace to an exact collar identity such
        as R3/R2=q, m_MS'=q/2, or C1 momentum q/2
    rejects:
        an arbitrary coefficient selected only because it gives q=1/3

no double counting:
    requirement:
        the collar action must reduce consistently to the
        interface-local eta carrier or to the warped DtN branch,
        not both at once
    rejects:
        using interface action and bulk propagation as independent
        factors for the same degree of freedom

exactness:
    requirement:
        all identities used in the closure must be exact in f, q,
        and the angular projector
    rejects:
        linearized or small-q arguments promoted to conclusions
```

Two-hundred-eighty-sixth verdict:

```text
A candidate that fails any one of these gates is not a derivation of
s(q)=q/3.
```

It may remain a conditional postulate, but not a native
metric-uncovered result.

## 302. Collar H1 action candidate scan

Implemented in `native_collar_h1_action_candidate_scan.py`.

Current candidate scan:

```text
C1 radial bulk action:
    native object:
        (1/4) integral r^2 f'^2 dr
    useful piece:
        gives exact boundary momentum Pi_f=(1/2)r^2 f'
    gap:
        no H1 carrier and no q-dependent collar source
    status:
        reject as activation action

phi0 boundary momentum projected into H1:
    native object:
        (-Pi_f/R)/3 = q/6
    useful piece:
        gives eta once q is already present
    gap:
        endpoint projection cannot by itself enforce q through the collar
    status:
        transfer support only

spatial curvature fraction:
    native object:
        R3/R2=q at phi0
    useful piece:
        native source of the q scalar as geometry, not analogy
    gap:
        identity is local at the collar; no variational H1 action yet
    status:
        promising ingredient

Misner-Sharp slope density:
    native object:
        m_MS'=q/2 at phi0 while m_MS=0
    useful piece:
        separates hidden value channel from exposed slope-density channel
    gap:
        atlas identity does not supply the H1 action kernel
    status:
        promising ingredient

Brown-York angular stress:
    native object:
        dimensionless angular stress unit q/2 at f=1
    useful piece:
        matches the angular-only shell signature
    gap:
        GR boundary-stress map is not yet a UDT variational derivation
    status:
        promising atlas, not closure

ell=1 angular identity:
    native object:
        (-r^2 Delta_S2)/2 = I3 on H1
    useful piece:
        supplies the exact triplet arena
    gap:
        does not provide the scalar q budget or collar source
    status:
        necessary but insufficient

auxiliary transported H1 amplitude:
    native object:
        an unknown collar field A_H1(r) with an equation A_H1=q
    useful piece:
        could produce q f^2/6 if A_H1 f^2/6 were native
    gap:
        no such metric-supplied auxiliary action has been uncovered
    status:
        open only as search target
```

Two-hundred-eighty-seventh verdict:

```text
The orchestra is visible:

    C1 momentum,
    curvature fraction,
    quasilocal slope-density,
    Brown-York angular stress,
    and H1 identity

all point at the same collar channel.
```

The missing piece is still:

```text
an exact collar variational object that makes them one action.
```

## 303. Curvature-share action no-go

Implemented in `native_curvature_share_action_no_go.py`.

The tempting native scalar through the collar is:

```text
A[f] = R3/R2 = 1 - f - r f'.
```

If this were the missing object, the most direct scalar action-density
candidate would be:

```text
V_A = A[f] f^2 / 6,
L_A = -V_A.
```

The exact Euler-Lagrange contribution from this `L_A` is:

```text
dL_A/df - d/dr(dL_A/df') = f(f-1)/3.
```

Equivalently:

```text
L_A = -(1-f-r f')f^2/6
    = total derivative + (-f^2/6 + f^3/9).
```

Therefore:

```text
the explicit q-bearing derivative part is absorbed into a boundary term,
and the remaining collar variation is f(f-1)/3, not (q/3)f.
```

At phi0:

```text
f=1,
f(f-1)/3=0.
```

Two-hundred-eighty-eighth verdict:

```text
The raw curvature-share scalar A=R3/R2 is a real metric ingredient,
but placing A f^2/6 into an ordinary scalar collar action does not
derive s(q)=q/3.
```

The missing object must be more than:

```text
a scalar curvature-share coefficient.
```

## 304. Post curvature no-go route update

Implemented in `native_post_curvature_no_go_route_update.py`.

The curvature-share no-go changes the route ranking.

```text
ordinary scalar collar action:
    updated status:
        demote
    reason:
        raw R3/R2 coefficient loses the q source under exact variation
    next test:
        do not pursue unless a new non-scalar variable is found

self-coupled activation s(q)=q/3:
    updated status:
        conditional only
    reason:
        algebraic fixed branch remains exact, but action origin is missing
    next test:
        keep as a minimal postulate candidate, not a derived result

boundary/joint slope channel:
    updated status:
        promote as search target
    reason:
        q survives naturally as C1 momentum jump, angular stress, and
        slope-density
    next test:
        look for a native variational boundary or edge term that fixes q

interface-local H1 transfer:
    updated status:
        promote as best current conditional theorem
    reason:
        once q is supplied, eta=q/6 and gamma=3 exp(-eta/2) follow cleanly
    next test:
        derive the q-setting boundary condition or state q as conditional

warped DtN collar propagation:
    updated status:
        keep as discriminator
    reason:
        it is exact if transfer is bulk-eliminated instead of interface-local
    next test:
        use only after the action chooses a bulk propagation interpretation
```

Two-hundred-eighty-ninth verdict:

```text
The metric orchestra is not pointing to a simple scalar bulk mechanism.
```

It is pointing to:

```text
a collar boundary/joint channel where value, slope, angular stress,
and H1 projection meet.
```

This is the current best non-myopic reading.

## 305. Two-lane decision record

Implemented in `native_two_lane_decision_record.py`.

Decision:

```text
Stop spending primary effort on deriving q=1/3 from the same
already-tested local C1/H1/curvature pieces.
```

This is not a retreat from the metric-uncovering frame.  It is a guard
against circularity.

The work now splits into two lanes.

```text
conditional particle-sector lane:
    status:
        active
    allowed work:
        bank q=1/3 as P_phi0 and derive exact consequences for eta,
        H1 transfer, DtN discriminator, and particle-sector structure
    forbidden work:
        claim q=1/3 is derived by the already-tested C1/H1/curvature
        algebra

foundational q-origin lane:
    status:
        parked but open
    allowed work:
        search for a genuinely new native boundary, joint, edge-mode,
        or covariant phase-space object
    forbidden work:
        continue cycling through ordinary scalar potentials or the same
        q-flow algebra
```

Two-hundred-ninetieth verdict:

```text
P_phi0 is allowed as a minimal explicit postulate/anchor in the
particle-sector lane.
```

Any q-origin derivation must come from:

```text
a new native variational object,
```

not from:

```text
relabeling the existing pattern.
```

## 306. P_phi0 active-lane payload

Implemented in `native_p_phi0_active_lane_payload.py`.

In the active lane, bank:

```text
P_phi0:
    q=1/3.
```

This gives the following payload.

```text
q = 1/3
q/2 = 1/6
eta = 1/18
eta/2 = 1/36
gamma_simple = 3 exp(-1/36) = 2.91781343135...
```

But the statuses are not all the same.

```text
phi0 slope:
    status:
        postulated by P_phi0
    value/rule:
        q=1/3

dimensionless boundary momentum/stress/slope-density unit:
    status:
        exact consequence of metric identities plus P_phi0
    value/rule:
        q/2=1/6

H1/S2 projected eta:
    status:
        exact consequence of round-S2 second moment
    value/rule:
        eta=(q/2)/3=1/18

one-sided action:
    status:
        conditional on symmetric composable boundary gluing
    value/rule:
        eta/2=1/36

simple H1 trace multiplier:
    status:
        conditional on P_transfer/interface-local identity kernel
    value/rule:
        gamma=3 exp(-1/36)

warped DtN multiplier:
    status:
        separate conditional branch if transfer is literal bulk propagation
    value/rule:
        gamma_warped=3 exp(-B/36), with B from exact self-similar DtN

typed depths and branch coefficients:
    status:
        not supplied by P_phi0
    value/rule:
        must be derived or separately postulated before mass predictions
        are claimed
```

Two-hundred-ninety-first verdict:

```text
In the active lane, P_phi0 is enough to derive eta exactly.
```

It is not enough to claim:

```text
gamma,
typed depth,
branch coefficients,
or mass predictions
```

without additional gates.

## 307. Transfer branch selection gate

Implemented in `native_transfer_branch_selection_gate.py`.

After banking `P_phi0`, the next non-circular choice is the transfer
branch.

There are two distinct branches.

```text
interface-local H1 transfer:
    use if:
        the transfer action lives directly on phi0 boundary/edge data
    exact form:
        gamma_simple = 3 exp(-1/36)
    status:
        best current conditional branch; supported by localized q/2
        identities

warped bulk DtN transfer:
    use if:
        the transfer action is obtained by eliminating the negative-phi
        collar bulk
    exact form:
        gamma_warped = 3 exp(-B/36)
    status:
        exact discriminator branch; profile-sensitive through B
```

For the self-similar `P_phi0`, `ell=1` warped collar:

```text
B = I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2)).
```

Equivalently, `B` is the half-integer hyperbolic rational expression
already recorded in the warped DtN section.

Diagnostic numerical values:

```text
B = 0.692726581294...
gamma_simple = 2.91781343135...
gamma_warped = 2.94282464475...
gamma_warped/gamma_simple = 1.00857190289...
```

Two-hundred-ninety-second verdict:

```text
Do not average or combine these branches.
```

The action must decide whether transfer is:

```text
interface-local
```

or:

```text
bulk-DtN.
```

The current evidence leans interface-local because the native `q/2`
objects are localized at `phi0`, but this is a branch-selection argument,
not a final derivation.

## 308. Active-lane work order

Implemented in `native_active_lane_work_order.py`.

The active lane now proceeds in this order.

```text
1. hold P_phi0 fixed
    allowed inputs:
        q=1/3 as an explicit active-lane postulate
    completion test:
        eta=1/18 is used consistently, while q-origin claims stay parked

2. select transfer branch
    allowed inputs:
        interface-local H1 action or warped bulk DtN, not both
    completion test:
        a native action/locality argument decides which gamma is admissible

3. derive or bank P_transfer
    allowed inputs:
        only after branch selection
    completion test:
        the trace/multiplier role of the H1 triplet is stated as derived
        or conditional

4. audit typed depth
    allowed inputs:
        edge graph variables after shared-frame merging
    completion test:
        node counts are fixed without double-counting M1/Hopf or E1
        shape modes

5. audit branch coefficients
    allowed inputs:
        finite-cell normalization, shape measure, compact bundle status
    completion test:
        M1/E1 coefficients are derived or explicitly marked diagnostic

6. use electron anchor only at the end
    allowed inputs:
        one dimensionful scale after dimensionless structure is fixed
    completion test:
        mass comparisons are checks, not inputs to choose gates
```

Two-hundred-ninety-third verdict:

```text
If a step cannot be completed exactly, mark it conditional and move to
consequence mapping.
```

Do not:

```text
backfit it from observed masses.
```

## 309. Interface-local working branch selection

Implemented in `native_interface_local_working_branch_selection.py`.

The active lane selects the interface-local transfer branch as the working
branch.

This selection is based on locality signals, not mass fitting.

```text
C1 momentum jump:
    localization:
        localized at phi0 when the exterior tail is flat
    implication:
        supports an interface-local eta carrier

distributional curvature jump:
    localization:
        delta-supported at the slope discontinuity
    implication:
        supports a joint/interface reading

Brown-York angular stress:
    localization:
        nonzero angular stress at f=1 with zero subtracted value energy
    implication:
        supports angular boundary action rather than bulk propagation

H1 angular identity:
    localization:
        intrinsic to the phi-blind S2 angular sector
    implication:
        supports an interface H1 kernel if the scalar eta is supplied

warped DtN map:
    localization:
        depends on propagation through the negative-phi collar profile
    implication:
        kept as discriminator, not the working branch unless action
        requires bulk elimination
```

Two-hundred-ninety-fourth verdict:

```text
Use interface-local H1 transfer as the active-lane working branch.
```

Guardrail:

```text
This is not a derivation of P_transfer.
```

It only chooses which conditional branch to develop first.  The warped
DtN branch remains exact and available if the action is later shown to
be bulk-eliminated.

## 310. P_transfer active-lane status

Implemented in `native_p_transfer_active_lane_status.py`.

Under banked `P_phi0`:

```text
eta = 1/18,
side action = eta/2 = 1/36,
gamma_simple = 3 exp(-1/36) = 2.91781343135...
```

The active-lane `P_transfer` gates are:

```text
H1 selected transfer space:
    status:
        conditional on ell=0 exclusion / lowest nonconstant bridge
    consequence:
        dim H1=3

scalar side action:
    status:
        conditional on symmetric composable boundary gluing
    consequence:
        A_side scalar=eta/2=1/36

identity kernel on H1:
    status:
        conditional on interface-local scalar-to-angular coupling
    consequence:
        A_side|H1=(1/36) I3

trace interpretation:
    status:
        conditional on unlabelled H1 boundary-state count
    consequence:
        Tr_H1 exp[-(1/36)I3]=3 exp(-1/36)

node multiplication:
    status:
        not supplied by P_transfer alone
    consequence:
        needed before gamma powers or typed-depth ladders are claimed
```

Two-hundred-ninety-fifth verdict:

```text
P_transfer is bankable as the second active-lane postulate.
```

If banked:

```text
gamma=3 exp(-1/36)
```

is exact inside the interface-local branch.

It still does not derive:

```text
typed depth
or branch coefficients.
```

## 311. Typed-depth active-lane gate

Implemented in `native_typed_depth_active_lane_gate.py`.

Typed-depth status:

```text
M1 compact primitive:
    exact geometry:
        CP1/Hopf data pushes into the common H1 frame; primitive
        compact/radial scalar can add one shape node per side
    candidate depth:
        3 shared H1 frame nodes + 1 core shape + 1 phi0 shape = 5
    missing gate:
        prove those five variables are independent transfer factors
        after Hopf-frame merging
    active status:
        candidate P_depth_M1, not derived

E1 ordinary H1:
    exact geometry:
        ordinary H1 after common-amplitude removal has a
        two-dimensional relative-shape plane
    candidate depth:
        3 shared H1 frame nodes + 2 core shapes + 2 phi0 shapes = 7
    missing gate:
        prove the two relative-shape coordinates at each side factor
        as independent transfer nodes
    active status:
        candidate P_depth_E1, not derived
```

Two-hundred-ninety-sixth verdict:

```text
The geometry supports the ingredients of 5 and 7.
```

But:

```text
transfer-node independence is still a graph/action claim.
```

Therefore typed depth remains conditional unless a boundary Hessian or
edge graph derives the factorization.

## 312. Branch-coefficient active-lane gate

Implemented in `native_branch_coefficient_active_lane_gate.py`.

Branch coefficient status:

```text
finite-cell normalization:
    exact status:
        open after Dirac/Form-T removal
    cannot do:
        reuse legacy M1/E1 coefficient ratios as derived
    required next:
        renormalize cells in the post-P_phi0 variables

M1 compact occupation:
    exact status:
        primitive compact bundle remains conditional
    cannot do:
        tune M1 by an occupation weight fitted to masses
    required next:
        derive or explicitly bank compact primitive occupation

E1 relative-shape measure:
    exact status:
        bare relative plane is exactly isotropic
    cannot do:
        extract an E1 boost from measure anisotropy
    required next:
        derive boundary-action weighting if E1 gets a coefficient shift

CP1/Hopf M1 measure:
    exact status:
        Fubini-Study measure pushes to round S2 second moment
    cannot do:
        extract an M1 correction from bare CP1 anisotropy
    required next:
        derive compact-bundle or boundary-action weighting if M1 shifts

electron anchor:
    exact status:
        allowed only after dimensionless coefficients are fixed
    cannot do:
        choose gates by matching electron/muon/tau values
    required next:
        use masses as downstream checks
```

Two-hundred-ninety-seventh verdict:

```text
Branch coefficients are not available yet in the active lane.
```

They are the next real calculation after:

```text
transfer branch
and typed graph status
```

are fixed.

Until then:

```text
mass comparisons remain diagnostic.
```

## 313. Active-lane consequence map

Implemented in `native_active_lane_consequence_map.py`.

The active lane is now tiered by what has actually been licensed.

```text
Tier A: eta foundation
    inputs:
        P_phi0 plus exact H1/S2 projection
    licenses:
        q=1/3, q/2=1/6, eta=1/18
    not licensed:
        gamma, typed depths, branch coefficients, masses

Tier B: interface transfer
    inputs:
        Tier A plus banked P_transfer on the interface-local branch
    licenses:
        gamma=3 exp(-1/36) as an exact conditional trace identity
    not licensed:
        gamma powers, typed-depth ladders, branch coefficients, masses

Tier C: typed graph
    inputs:
        Tier B plus banked or derived P_depth_M1/P_depth_E1
    licenses:
        symbolic ladder powers such as gamma^5 and gamma^7 inside the
        selected graph
    not licensed:
        branch coefficient normalization and dimensional mass predictions

Tier D: coefficient-complete dimensionless sector
    inputs:
        Tier C plus derived M1/E1 finite-cell and measure coefficients
    licenses:
        dimensionless mass ratios inside the chosen active-lane model
    not licensed:
        absolute masses until the electron anchor is applied

Tier E: anchored mass comparison
    inputs:
        Tier D plus electron mass as the single dimensionful anchor
    licenses:
        mass comparisons as downstream checks
    not licensed:
        using observed masses to choose prior gates
```

Two-hundred-ninety-eighth verdict:

```text
The current active lane is solid through Tier A.
```

Tier B is bankable if:

```text
P_transfer is explicitly accepted.
```

Tiers C-E remain consequence-mapping territory until their gates are:

```text
derived
```

or:

```text
intentionally banked.
```

## 314. Tier C symbolic ladder

Implemented in `native_tier_c_symbolic_ladder.py`.

Banked active-lane inputs for Tier C:

```text
P_phi0:
    q=1/3 -> eta=1/18

P_transfer:
    gamma=3 exp(-1/36)

P_depth_M1:
    n_M1=5

P_depth_E1:
    n_E1=7
```

Numerically:

```text
gamma = 2.91781343135...
gamma^5 = 211.488908378...
gamma^7 = 1800.53941904...
gamma^2 = 8.51363522016...
```

Coefficient-free symbolic structure:

```text
M1/electron-anchor ratio = C_M1 gamma^5
E1/electron-anchor ratio = C_E1 gamma^7
E1/M1 ratio = (C_E1/C_M1) gamma^2
```

Two-hundred-ninety-ninth verdict:

```text
Tier C licenses the exponents 5 and 7 inside the banked graph and the
universal gamma powers inside the interface-local branch.
```

Tier C does not license:

```text
the values of C_M1 or C_E1,
identification of M1/E1 with observed particles,
or dimensional masses.
```

## 315. M2 competing-branch gate

Implemented in `native_m2_competing_branch_gate.py`.

If typed depth depends only on dimension `d` through:

```text
n = 3 + 2(d-1),
```

then all `d=3` branches inherit:

```text
n=7.
```

This creates a real branch-selection issue.

```text
M1 compact primitive:
    dimension:
        d=2
    depth:
        n=5
    active role:
        candidate lower-depth compact branch
    issue:
        requires compact primitive occupation if used as anchor branch

M2 compact triplet:
    dimension:
        d=3
    depth:
        n=7
    active role:
        competing d=3 compact branch
    issue:
        shares the same dimension-depth as E1 unless excluded or weighted
        by a native rule

E1 ordinary H1:
    dimension:
        d=3
    depth:
        n=7
    active role:
        candidate d=3 ordinary branch
    issue:
        endpoint resonance and ell=1 support it, but do not by themselves
        eliminate M2
```

Three-hundredth verdict:

```text
The active lane cannot simply choose E1 over M2 by target matching.
```

It needs a native selector, such as:

```text
endpoint resonance,
compact-bundle occupancy,
boundary coefficient suppression,
or an edge-graph rule.
```

## 316. Tier C to Tier D coefficient requirements

Implemented in `native_tier_c_to_d_coefficient_requirements.py`.

Tier D begins only after the coefficient symbols in Tier C are computed
or explicitly banked.

```text
C_M1:
    role:
        dimensionless coefficient multiplying the M1 depth-5 ladder factor
    allowed origin:
        post-Dirac finite-cell normalization, compact occupation, or
        boundary-action weight
    forbidden origin:
        fitted correction chosen after comparing to observed muon mass

C_E1:
    role:
        dimensionless coefficient multiplying the E1 depth-7 ladder factor
    allowed origin:
        endpoint-resonant H1 finite-cell normalization or boundary-action
        weight
    forbidden origin:
        fitted correction chosen after comparing to observed tau mass

C_M2:
    role:
        dimensionless coefficient for the competing compact triplet branch
    allowed origin:
        same compact-bundle sector that defines or suppresses M2
    forbidden origin:
        silent omission
```

Three-hundred-first verdict:

```text
Until these coefficients are computed from the post-P_phi0 boundary/cell
variables or explicitly banked, Tier C remains symbolic.
```

## 317. Active M2 selector status

Implemented in `native_active_m2_selector_status.py`.

The `M2` branch can be demoted conditionally, but not silently.

```text
primitive compact-bundle selector:
    effect on M2:
        demotes M2 because flux n=2 is nonprimitive while M1 has |n|=1
    status:
        conditional on compact U(1) bundle occupancy Pbundle0
    caveat:
        does not derive why a nontrivial compact bundle must be occupied

flux-energy superadditivity:
    effect on M2:
        demotes M2 because radial flux energy scales as n^2, so n=2
        costs more than two primitives
    status:
        native energy-ordering pressure if compact flux is admitted
    caveat:
        does not prove a decay channel or absolute exclusion

ordinary endpoint resonance:
    effect on M2:
        favors E1 over M2 for the d=3 ordinary branch because E1 is
        the p=1/3 endpoint-resonant H1 sector
    status:
        strong active-lane selector inside the ordinary angular sector
    caveat:
        does not by itself compare ordinary E1 to compact M2 unless
        compact sectors are separately classified

silent omission:
    effect on M2:
        would remove M2 by not counting it
    status:
        rejected
    caveat:
        this is target-shaped bookkeeping, not a metric rule
```

Three-hundred-second verdict:

```text
If Pbundle0 is banked, then M1 is the primitive compact branch and M2
is nonprimitive/diagnostic, while E1 is the ordinary endpoint-resonant
d=3 branch.
```

Without `Pbundle0`, the compact branch is not active and `M1` cannot be
used as a compact-bundle anchor without further input.

## 318. Active-lane postulate ledger after Tier C

Implemented in `native_active_lane_postulate_ledger_after_tier_c.py`.

Current active-lane ledger:

```text
P_phi0:
    status:
        banked active-lane postulate
    role:
        sets q=1/3 and therefore eta=1/18 after H1/S2 projection
    risk:
        q-origin remains parked

P_transfer:
    status:
        optional second banked postulate
    role:
        turns eta into gamma=3 exp(-1/36) on the interface-local branch
    risk:
        requires interface-local identity kernel and trace interpretation

P_depth:
    status:
        optional graph postulate, not derived
    role:
        assigns M1 depth 5 and E1 depth 7
    risk:
        requires independent transfer-node factorization

Pbundle0:
    status:
        optional compact-sector postulate
    role:
        admits primitive nontrivial compact U(1) bundle occupancy for M1
        and demotes M2 as nonprimitive
    risk:
        compact occupancy is not forced by the bare metric

P_coeff:
    status:
        not banked
    role:
        would supply C_M1, C_E1, and C_M2
    risk:
        banking it would turn the model into coefficient fitting unless
        derived

electron anchor:
    status:
        allowed only after dimensionless structure is fixed
    role:
        sets the single dimensionful scale
    risk:
        must not be used to select earlier gates
```

Three-hundred-third verdict:

```text
The active lane is mathematically organized, but its predictive strength
depends on how many of P_transfer, P_depth, and Pbundle0 are intentionally
banked rather than derived.
```

## 319. Next coefficient-calculation contract

Implemented in `native_next_coefficient_calculation_contract.py`.

The next real Tier D task is not another ladder fit.  It is a
post-Dirac finite-cell normalization calculation for `M1`, `M2`, and
`E1` under one shared boundary/cell convention.

```text
post-Dirac variables:
    exact input:
        use f, q, eta, H1/S2 projectors, Hopf/CP1 data, and
        relative-shape coordinates only
    output needed:
        a coefficient functional in native variables
    fail condition:
        any dependence on the removed Dirac/Form-T structure

normalization domain:
    exact input:
        finite negative-phi cell with phi0 boundary and endpoint/core side
    output needed:
        well-defined integrals or boundary determinants for M1, M2, and E1
    fail condition:
        undefined cutoff dependence hidden in C_i

branch comparison:
    exact input:
        evaluate M1, M2, and E1 in the same normalization convention
    output needed:
        C_M1, C_M2, C_E1 or a derived suppression of one branch
    fail condition:
        silent omission of M2

no mass input:
    exact input:
        do not use electron/muon/tau masses during coefficient calculation
    output needed:
        dimensionless coefficients before anchoring
    fail condition:
        choosing coefficients by residual errors
```

Three-hundred-fourth verdict:

```text
Tier D begins with a native coefficient functional, not with observed
mass residuals.
```

## 320. Tier D legacy coefficient rejection

Implemented in `native_tier_d_legacy_coefficient_rejection.py`.

The old coefficient inputs are rejected as Tier D inputs.

```text
old finite-cell eigenfrequencies:
    old role:
        supplied provisional M1/M2/E1 coefficient ratios
    rejection reason:
        computed in the pre-active-lane scaffold with legacy eta/profile
        choices
    replacement requirement:
        recompute from post-P_phi0 variables under one shared boundary
        convention

eta=0.03 runs:
    old role:
        exploratory mass-sector diagnostics
    rejection reason:
        active lane uses eta=1/18 exactly after banked P_phi0
    replacement requirement:
        use eta=1/18 or keep the result outside Tier D

softened profile parameters:
    old role:
        regularized singular endpoint for numerical exploration
    rejection reason:
        profile choices are not a native coefficient functional
    replacement requirement:
        derive profile, prove profile-independence, or state profile
        dependence

observed lepton residuals:
    old role:
        identified possible correction directions
    rejection reason:
        mass data cannot choose coefficients in the active lane
    replacement requirement:
        use only after dimensionless coefficients are fixed
```

Three-hundred-fifth verdict:

```text
The old M1/M2/E1 coefficient ratios may remain diagnostics.
```

They are not Tier D inputs in the post-Dirac active lane.

## 321. Tier D functional candidate audit

Implemented in `native_tier_d_functional_candidate_audit.py`.

Current Tier D functional candidates:

```text
boundary Hessian determinant:
    native inputs:
        second variation of the phi0 boundary functional in typed node
        variables
    could output:
        relative weights for M1, M2, and E1 after node merging
    current status:
        best Tier D target, but boundary functional is not yet derived
    risk:
        cannot be invented as a Gaussian measure

finite-cell action norm:
    native inputs:
        C1 radial action plus angular H1/compact-bundle terms after P_phi0
    could output:
        dimensionless branch normalizations if action is finite and shared
    current status:
        open; angular/bundle action still missing
    risk:
        old numerical action scales do not define the coefficient

Dirichlet-to-Neumann determinant:
    native inputs:
        exact collar operator on selected branch data
    could output:
        profile-sensitive determinant weights
    current status:
        available only if transfer branch becomes bulk-DtN
    risk:
        wrong branch for the current interface-local working lane

bare shape-measure volume:
    native inputs:
        CP1/S2 and E1 relative-plane measures
    could output:
        only normalized measure factors after a boundary measure is chosen
    current status:
        insufficient by itself; bare measures are isotropic
    risk:
        volume ratios depend on normalization and can become arbitrary

compact occupation weight:
    native inputs:
        Pbundle0 plus primitive line-bundle occupancy
    could output:
        M1 activation or M2 suppression factor
    current status:
        conditional postulate, not coefficient calculation
    risk:
        can hide fitting if assigned numerically
```

Three-hundred-sixth verdict:

```text
The next promising object is a boundary Hessian or shared finite-cell
action norm in the typed variables.
```

No existing coefficient candidate is currently a derived Tier D
functional.

## 322. Bare measure coefficient no-go

Implemented in `native_bare_measure_coefficient_no_go.py`.

Bare measure facts:

```text
CP1/Hopf M1 measure:
    exact fact:
        Fubini-Study measure on CP1 pushes forward to the round S2 measure
    coefficient consequence:
        no anisotropic M1 correction from bare projective geometry

H1/S2 second moment:
    exact fact:
        <n_a n_b>=delta_ab/3
    coefficient consequence:
        gives eta projection, not a branch coefficient

E1 relative plane:
    exact fact:
        after removing common amplitude, the relative-shape plane is
        isotropic
    coefficient consequence:
        no E1 coefficient boost from bare relative-angle measure

volume normalization:
    exact fact:
        total measure can be normalized to one on each branch space
    coefficient consequence:
        absolute volume ratios are not invariant unless the boundary
        measure specifies them
```

Three-hundred-seventh verdict:

```text
Bare geometry measures support isotropy and projection identities.
```

They do not supply:

```text
C_M1,
C_M2,
or C_E1
```

without a derived boundary action or measure density.

## 323. Tier D working target

Implemented in `native_tier_d_working_target.py`.

Tier D should now target:

```text
1. construct the typed boundary variable vector
    exact requirement:
        include shared H1 frame variables, M1 compact/radial variables,
        M2 compact triplet data, and E1 relative-shape variables

2. write the post-P_phi0 boundary functional
    exact requirement:
        use only eta, H1/S2 projection, Hopf/CP1 map, relative-shape
        coordinates, and compact-bundle labels if Pbundle0 is banked

3. compute the quadratic kernel or Hessian
    exact requirement:
        derive it from the functional; do not assign diagonal weights by hand

4. evaluate M1, M2, and E1 under the same kernel
    exact requirement:
        produce C_M1, C_M2, C_E1 or a derived null/suppression result

5. check invariance
    exact requirement:
        coefficients must be independent of coordinate basis, arbitrary
        measure normalization, and observed masses
```

Three-hundred-eighth verdict:

```text
Tier D should search for the typed boundary functional and its Hessian.
```

If that object cannot be built:

```text
coefficients remain open.
```

## 324. Boundary Hessian constructibility audit

Implemented in `native_boundary_hessian_constructibility_audit.py`.

Known pieces:

```text
value closure a_tail=0:
    current status:
        required but not written as an explicit functional
    Hessian role:
        sets the value side of the boundary problem

momentum condition q/2:
    current status:
        available only through banked P_phi0 in the active lane
    Hessian role:
        sets the first variation at phi0

H1 projection eta=q/6:
    current status:
        derived after P_phi0 from round-S2 second moment
    Hessian role:
        projects scalar first variation into H1

typed node variables:
    current status:
        candidate variables identified for M1, M2, and E1
    Hessian role:
        provide coordinates for a possible Hessian

boundary functional S_phi0[nodes]:
    current status:
        not derived
    Hessian role:
        required before any Hessian exists

second variation / Hessian:
    current status:
        not constructible yet
    Hessian role:
        would define C_M1, C_M2, C_E1 or coupled spectra
```

Three-hundred-ninth verdict:

```text
The active lane has boundary conditions and typed variables.
```

It does not yet have:

```text
S_phi0[nodes].
```

Therefore the coefficient Hessian cannot be claimed or evaluated.

## 325. Tier D block-kernel skeleton

Implemented in `native_tier_d_block_kernel_skeleton.py`.

Symmetry constrains the possible kernel blocks.

```text
shared H1 frame block:
    variables:
        three H1/S2 frame components with unit/projective constraints
    symmetry constraint:
        round-S2 symmetry restricts identity-like pieces to multiples of I3
    unknown:
        whether this block is traced once, three times, or coupled to shapes

M1 compact/radial block:
    variables:
        primitive compact-bundle data plus one residual shape scalar per side
        if Pbundle0 is banked
    symmetry constraint:
        Hopf/CP1 bridge maps orientation into the shared H1 frame
    unknown:
        compact occupation and residual scalar kernel

M2 compact triplet block:
    variables:
        nonprimitive compact n=2 triplet data
    symmetry constraint:
        eligible as d=3 representation but nonprimitive in compact flux
    unknown:
        derived suppression, diagnostic coefficient, or exclusion

E1 relative-shape block:
    variables:
        two-dimensional relative plane per side after removing common amplitude
    symmetry constraint:
        isotropy restricts bare relative metric to multiples of I2
    unknown:
        boundary-action weight and cross-coupling to shared H1 frame

cross-coupling blocks:
    variables:
        couplings among shared frame, compact data, and relative shapes
    symmetry constraint:
        symmetry may force some blocks to vanish, but this must be derived
    unknown:
        whether the kernel factorizes or has a coupled spectrum
```

Three-hundred-tenth verdict:

```text
Symmetry does not set block weights or prove factorization.
```

A block-diagonal kernel would be:

```text
a result,
```

not:

```text
an assumption.
```

## 326. Diagonal weight insertion no-go

Implemented in `native_diagonal_weight_insertion_no_go.py`.

Forbidden insertions:

```text
assign M1 weight by residual:
    inserted object:
        C_M1 chosen to improve anchored mu-like comparison
    why invalid:
        uses observed mass before Tier D is complete

assign E1 weight by residual:
    inserted object:
        C_E1 chosen to improve anchored tau-like comparison
    why invalid:
        turns coefficient calculation into fitting

drop M2 by coefficient zero:
    inserted object:
        C_M2=0 without compact-bundle or boundary-action derivation
    why invalid:
        silent omission of a competing d=3 branch

assume diagonal Hessian:
    inserted object:
        no cross-coupling among H1, compact, and relative-shape variables
    why invalid:
        factorization is exactly what the boundary functional must derive
```

Three-hundred-eleventh verdict:

```text
Any numerical C_i or diagonal block weight inserted before deriving
S_phi0[nodes] is P_coeff.
```

`P_coeff` is not banked in the active lane.

## 327. Lepton-ratio diagnostic lane

Implemented in `native_lepton_ratio_diagnostic_lane.py`.

Lepton ratios can be used only as downstream pressure tests.

With the current symbolic Tier C ladder:

```text
gamma = 2.91781343135...
gamma^5 = 211.488908378...
gamma^7 = 1800.53941904...
```

Observed ratios:

```text
mu/e = 206.768282988...
tau/e = 3477.22828002...
tau/mu = 16.8170293324...
```

Diagnostic pressure values:

```text
mu/e ratio pressure on C_M1:
    diagnostic value:
        0.977679087636...
    allowed use:
        compare against a later derived C_M1
    forbidden use:
        define C_M1 from this value

tau/e ratio pressure on C_E1:
    diagnostic value:
        1.93121474779...
    allowed use:
        compare against a later derived C_E1
    forbidden use:
        define C_E1 from this value

tau/mu pressure on C_E1/C_M1:
    diagnostic value:
        1.97530536575...
    allowed use:
        test a later derived coefficient ratio
    forbidden use:
        choose E1 over M2 or tune branch weights
```

Three-hundred-twelfth verdict:

```text
Lepton ratios are useful as downstream pressure tests.
```

They cannot select:

```text
P_transfer,
P_depth,
Pbundle0,
M2 suppression,
or coefficient values inside Tier D.
```

## 328. Lepton-ratio falsification contract

Implemented in `native_lepton_ratio_falsification_contract.py`.

Rules:

```text
pre-registration:
    use:
        state P_phi0, transfer branch, P_transfer, P_depth, Pbundle0,
        and coefficient functional before comparing ratios
    violation:
        changing any of those after seeing residuals

M2 inclusion:
    use:
        include M2 as active, suppressed, or conditionally demoted before
        ratio comparison
    violation:
        dropping M2 because it worsens the ratio story

coefficient independence:
    use:
        derive C_M1, C_M2, C_E1 without electron/muon/tau data
    violation:
        solving coefficients from observed ratios

anchor order:
    use:
        apply the electron anchor only after dimensionless ratios are fixed
    violation:
        using the electron anchor to choose branch assignments

failure allowed:
    use:
        if derived coefficients miss ratios, record the miss as
        falsification pressure
    violation:
        retuning gates to absorb the miss
```

Three-hundred-thirteenth verdict:

```text
Lepton ratios become powerful only after the model is frozen.
```

Before that, they are:

```text
diagnostics,
```

not:

```text
construction tools.
```

## 329. S_phi0 first-jet reconstruction

Implemented in `native_s_phi0_first_jet_reconstruction.py`.

The active lane can specify the first variation of `S_phi0` at the
boundary point.

Known active-lane scalars:

```text
q = 1/3
q/2 = 1/6
eta = 1/18
```

First-jet pieces:

```text
value closure:
    fixed by:
        finite closed cell requirement
    first-variation content:
        delta S contains multiplier term enforcing a_tail=0

C1 conjugate momentum:
    fixed by:
        banked P_phi0
    first-variation content:
        dS/df at phi0 must cancel Pi_f and carry q/2=1/6

H1 projection:
    fixed by:
        round-S2 second moment
    first-variation content:
        projected first variation is eta=(q/2)/3=1/18

one-sided split:
    fixed by:
        banked P_transfer gluing rule if accepted
    first-variation content:
        each side carries eta/2=1/36
```

Three-hundred-fourteenth verdict:

```text
The active lane can specify the first variation of S_phi0 at the boundary.
```

This is enough to carry:

```text
eta.
```

It is not enough to determine:

```text
coefficient weights.
```

## 330. S_phi0 second-jet gap

Implemented in `native_s_phi0_second_jet_gap.py`.

The second local variation has the formal role:

```text
delta^2 S_phi0 = delta x^a K_ab delta x^b.
```

Missing second-jet pieces:

```text
typed-node Hessian K_ab:
    why needed:
        determines quadratic weights, coupled spectra, and possible
        coefficients
    not fixed by:
        q, eta, H1 projection, or lepton ratios

cross-coupling blocks:
    why needed:
        decide whether H1 frame, M1 compact data, M2 compact data, and
        E1 relative shapes factorize
    not fixed by:
        round-S2 isotropy alone

M2 suppression/null direction:
    why needed:
        decides whether nonprimitive compact triplet is suppressed,
        diagnostic, or active
    not fixed by:
        dimension-depth rule

boundary measure density:
    why needed:
        turns geometric variables into invariant coefficient weights
    not fixed by:
        bare CP1/S2 or relative-plane volume
```

Three-hundred-fifteenth verdict:

```text
The missing coefficient object is the second jet of S_phi0 in typed
boundary variables.
```

First-variation data cannot determine it.

## 331. S_phi0 jet status

Implemented in `native_s_phi0_jet_status.py`.

Current `S_phi0` status:

```text
zeroth/value tier:
    status:
        partly specified as a_tail=0 requirement
    licenses:
        closed-cell boundary value condition
    does not license:
        momentum, eta, coefficients

first-variation tier:
    status:
        specified conditionally by P_phi0 and H1 projection
    licenses:
        q/2 and eta=1/18
    does not license:
        Hessian, coefficients, branch weights

one-sided transfer tier:
    status:
        specified only if P_transfer is banked
    licenses:
        eta/2 and gamma=3 exp(-1/36)
    does not license:
        typed-depth powers or branch coefficients

second-variation tier:
    status:
        missing
    licenses:
        would license C_M1, C_M2, C_E1 or a coupled replacement
    does not license:
        anything until S_phi0[nodes] is derived
```

Three-hundred-sixteenth verdict:

```text
We have enough S_phi0 information for eta and conditional transfer.
```

We do not have enough for:

```text
Tier D coefficients.
```

## 332. Symmetry-allowed second-jet form

Implemented in `native_symmetry_allowed_second_jet_form.py`.

Symmetry narrows the possible Hessian, but does not determine it.

```text
shared H1 frame:
    symmetry-allowed form:
        K_H1 = alpha I_3 on the ell=1 triplet
    free data:
        alpha
    consequence:
        round-S2 symmetry gives identity form, not the weight alpha

E1 relative shape per side:
    symmetry-allowed form:
        K_E1 = beta I_2 on the two-dimensional relative plane
    free data:
        beta, plus possible core-phi0 coupling beta_cross
    consequence:
        relative-plane isotropy gives I_2 form, not the coefficient

M1 compact residual scalar:
    symmetry-allowed form:
        K_M1 is a symmetric 2x2 scalar-side matrix for core/phi0 residuals
    free data:
        three scalar entries before additional gluing constraints
    consequence:
        scalar symmetry does not reduce it to a unique number

M2 compact triplet:
    symmetry-allowed form:
        K_M2 = alpha_2 I_3 if the nonprimitive compact triplet remains active
    free data:
        alpha_2
    consequence:
        same dimension as E1 does not imply same coefficient or status

cross blocks:
    symmetry-allowed form:
        zero only if representation, parity, bundle, or endpoint symmetries
        forbid them
    free data:
        all allowed couplings not killed by exact symmetry
    consequence:
        factorization is a derived property, not a default
```

Three-hundred-seventeenth verdict:

```text
Symmetry narrows the Hessian to block forms and a finite set of
constants/couplings.
```

It does not compute those constants.  Therefore symmetry alone cannot
produce:

```text
C_M1,
C_M2,
or C_E1.
```

## 333. Second-jet free-constants no-go

Implemented in `native_second_jet_free_constants_no_go.py`.

Free constants exposed by the symmetry-reduced second jet:

```text
alpha:
    controls:
        shared H1 frame block weight
    cannot be chosen by:
        choosing it fixes transfer/trace strength beyond eta if not derived

beta:
    controls:
        E1 relative-shape block weight
    cannot be chosen by:
        choosing it can create the needed E1 coefficient pressure by hand

beta_cross:
    controls:
        core-phi0 E1 relative-shape coupling
    cannot be chosen by:
        choosing it decides factorization versus coupled spectrum

M1 scalar-side matrix entries:
    controls:
        primitive compact/radial residual weight
    cannot be chosen by:
        choosing them can tune the M1 coefficient pressure

alpha_2 or null rule:
    controls:
        M2 compact triplet activity or suppression
    cannot be chosen by:
        choosing it silently decides the competing d=3 branch
```

Three-hundred-eighteenth verdict:

```text
A symmetry-allowed Hessian with free constants is not Tier D.
```

Tier D begins only when:

```text
S_phi0[nodes]
```

fixes those constants or derives a parameter-free coupled spectrum.

## 334. Metric-supplied second-jet candidate scan

Implemented in `native_metric_supplied_second_jet_candidate_scan.py`.

Question:

```text
Is the metric already supplying the second jet?
```

Candidate scan:

```text
ell=1 angular Laplacian:
    metric supplies:
        L1=(-R^2 Delta_S2)/2=I3 on H1
    still missing:
        action time/coupling that multiplies L1 by eta/2
    second-jet status:
        supplies identity operator shape, not coefficient weights

heat-kernel semigroup:
    metric supplies:
        exp(-t L1), trace, and exact composition once t is given
    still missing:
        native identification of t with eta/2 and node factorization
    second-jet status:
        supplies transfer mathematics, not S_phi0 Hessian constants

Dirichlet-to-Neumann map:
    metric supplies:
        a canonical way to map boundary values to conjugate momenta
    still missing:
        native phi0 DtN/Calderon map for typed boundary variables
    second-jet status:
        could supply second jet if constructed; not currently available

Hamilton-Jacobi on-shell action:
    metric supplies:
        boundary momenta are first derivatives of on-shell action
    still missing:
        second functional derivative in typed variables
    second-jet status:
        right formal home for Hessian, but not yet computed

standard EH+GHY Dirichlet completion:
    metric supplies:
        metric boundary completion for fixed induced metric
    still missing:
        does not preserve the phi0 slope momentum at f=1
    second-jet status:
        reject as eta/second-jet source in this active lane

corner/joint term:
    metric supplies:
        localized codimension-2 boundary object where radial and S2 data meet
    still missing:
        UDT-specific joint action and its typed second variation
    second-jet status:
        promising location, not yet a computed kernel
```

Three-hundred-nineteenth verdict:

```text
The metric supplies strong operator shapes:
    L1,
    heat semigroup,
    boundary momentum,
    and possible DtN/HJ homes.
```

It has not yet supplied:

```text
the typed second-jet constants or clock.
```

## 335. Metric operator vs clock split

Implemented in `native_metric_operator_vs_clock_split.py`.

The current picture is an operator/clock split.

```text
operator shape:
    metric status:
        metric supplies L1=I3 on ell=1 and I2 on the E1 relative plane
        by symmetry
    active-lane role:
        known

edge scalar:
    metric status:
        banked P_phi0 plus projection supplies eta=1/18
    active-lane role:
        known only because P_phi0 is banked

side clock:
    metric status:
        eta/2 is supplied only if P_transfer gluing is banked
    active-lane role:
        conditional

second-jet weights:
    metric status:
        not supplied by operator symmetry or eta
    active-lane role:
        missing

node factorization:
    metric status:
        not supplied by heat-kernel semigroup alone; needs boundary
        graph/action
    active-lane role:
        missing/conditional P_depth
```

Three-hundred-twentieth verdict:

```text
The metric is supplying the operator arena more strongly than the
coefficient clock.
```

This supports the interface-transfer route, but does not close Tier D.

## 336. Metric already-doing inventory

Implemented in `native_metric_already_doing_inventory.py`.

Inventory of what the metric is already doing:

```text
negative-phi arena:
    exact metric object:
        f=e^{-2phi}>1 for phi<0
    already does:
        creates the finite-action endpoint/collar problem without Dirac/Form-T
    boundary status:
        native background arena

phi-blind angular sector:
    exact metric object:
        g_AB=r^2 omega_AB
    already does:
        preserves the round S2 spectrum and H1 triplet across phi sign
    boundary status:
        native operator arena

C1 boundary momentum:
    exact metric object:
        Pi_f=(1/2)r^2 f'
    already does:
        at phi0 gives -Pi_f/R=q/2, the local edge slope unit
    boundary status:
        first variation fixed once q is banked

interface curvature jump:
    exact metric object:
        flat exterior plus inner f'=-q/R
    already does:
        produces angular-only shell stress and Delta K R=q/2
    boundary status:
        localized phi0/joint object

H1/S2 projection:
    exact metric object:
        <n_a n_b>=delta_ab/3
    already does:
        turns q/2 into eta=q/6
    boundary status:
        projection identity, not a transfer kernel by itself

ell=1 Laplacian identity:
    exact metric object:
        L1=(-R^2 Delta_S2)/2=I3 on H1
    already does:
        supplies the three-channel identity operator shape
    boundary status:
        operator shape supplied

proper radial refactor:
    exact metric object:
        d rho=dr/sqrt(f), r''/r=f'/(2r)
    already does:
        adds the positional-dilation/extrinsic term to the normal operator
    boundary status:
        bulk DtN branch supplied if bulk propagation is chosen

heat semigroup:
    exact metric object:
        exp(-t L1)
    already does:
        supplies trace/composition mathematics once the action time t is given
    boundary status:
        clock t not supplied by semigroup itself

local boundary expansion:
    exact metric object:
        S_b(F,a)=S0[a]+S1[a](F-1)+O((F-1)^2)
    already does:
        separates value/angular action S0 from slope closure S1
    boundary status:
        shows why first variation does not determine coefficients
```

Three-hundred-twenty-first verdict:

```text
The metric is already supplying the arena, slope unit, angular identity,
projection, interface jump, and warped normal operator.
```

The unresolved piece is narrower:

```text
the angular value action / second jet S0[a] or K_ab on typed boundary
variables.
```

## 337. Metric uncovered vs missing split

Implemented in `native_metric_uncovered_vs_missing_split.py`.

Current uncovered/missing split:

```text
eta carrier:
    uncovered:
        q/2 appears as boundary momentum, curvature jump, and angular
        stress; H1 projection gives q/6
    missing:
        q=1/3 remains banked as P_phi0

transfer operator shape:
    uncovered:
        L1=I3 on ell=1 and heat-kernel trace gives 3 exp(-t)
    missing:
        metric has not identified t=eta/2 without P_transfer

bulk propagation alternative:
    uncovered:
        positional dilation gives exact warped DtN operator
    missing:
        action has not selected bulk-DtN over interface-local transfer

typed node arena:
    uncovered:
        H1 frame, Hopf/CP1 bridge, and E1 relative plane are exact
        geometries
    missing:
        node independence and factorization remain P_depth unless derived

coefficient arena:
    uncovered:
        symmetry restricts Hessian blocks to identity/scalar forms
    missing:
        free constants/couplings remain until S_phi0 second jet is derived

M2 handling:
    uncovered:
        metric/topology demotes M2 if Pbundle0 is admitted because n=2
        is nonprimitive
    missing:
        compact bundle occupancy Pbundle0 itself is not forced by the
        bare metric
```

Three-hundred-twenty-second verdict:

```text
This is not an empty fit scaffold.
```

Several load-bearing structures are metric-uncovered.  But the remaining
gaps are real and should stay named rather than filled by coefficient
choices.

## 338. S0 value-action target

Implemented in `native_s0_value_action_target.py`.

The next object to uncover is:

```text
S0[a],
```

the angular/value part of `S_phi0`.

Targets:

```text
interface-local H1 value action:
    required form:
        S0[a]|H1 = (eta/2)<a,L1 a> for one side, with L1=I3
    metric clue:
        ell=1 angular Laplacian supplies L1; interface jump supplies
        eta scale
    open problem:
        derive why the value action uses side time eta/2

two-sided full value action:
    required form:
        S0_full[a]|H1 = eta<a,L1 a>
    metric clue:
        symmetric gluing would split this into eta/2 per side
    open problem:
        derive gluing from the boundary variational principle

bulk-DtN value action:
    required form:
        S0[a]=<a,K_DtN a>/2 with warped K_DtN
    metric clue:
        positional dilation supplies the warped normal operator
    open problem:
        action must choose bulk propagation and its normalization

typed coefficient Hessian:
    required form:
        S0[x]=1/2 x^a K_ab x^b over H1, M1, M2, and E1 variables
    metric clue:
        symmetry constrains K_ab block forms
    open problem:
        derive block weights and cross-couplings from S_phi0, not from fits
```

Three-hundred-twenty-third verdict:

```text
The metric has supplied the natural operators.
```

It has not yet supplied:

```text
the action-time normalization or typed Hessian weights.
```

## 339. S0 orchestra role map

Implemented in `native_s0_orchestra_role_map.py`.

The orchestra metaphor enters here as role composition, not additive
mechanism stacking.

```text
phi0 interface jump:
    role for S0:
        weight source
    contributes:
        q/2 local angular stress scale, projected to eta=q/6
    must not do:
        be counted again as a separate coefficient after eta is formed

ell=1 Laplacian:
    role for S0:
        operator shape
    contributes:
        L1=I3 on H1
    must not do:
        supply the eta clock or branch coefficients by itself

heat semigroup:
    role for S0:
        composition law
    contributes:
        exp(-t L1), trace, and gluing algebra once t is known
    must not do:
        choose t without the boundary action

symmetric gluing:
    role for S0:
        side splitter
    contributes:
        eta -> eta/2 per side if full boundary action composes
        symmetrically
    must not do:
        be assumed if the boundary object is bulk-DtN instead

proper radial/DtN operator:
    role for S0:
        bulk-memory alternative
    contributes:
        warped propagation kernel if transfer is through the collar
    must not do:
        be multiplied together with interface-local transfer for the same
        variable

H1 frame / CP1 bridge / E1 relative plane:
    role for S0:
        typed variable arena
    contributes:
        coordinates for possible S0[x] Hessian blocks
    must not do:
        create independent nodes unless the boundary graph proves
        independence

compact bundle primitivity:
    role for S0:
        branch selector
    contributes:
        conditional M1 activation and M2 demotion if Pbundle0 is banked
    must not do:
        supply a numeric coefficient by occupation fiat
```

Three-hundred-twenty-fourth verdict:

```text
S0 may be a coupled composition of already-uncovered metric instruments.
```

The safe rule is:

```text
role composition,
```

not:

```text
additive mechanism stacking.
```

## 340. S0 orchestra composition tests

Implemented in `native_s0_orchestra_composition_tests.py`.

Candidate compositions:

```text
interface-local scalar-times-L1:
    form:
        S0_side = (eta/2)<a,L1 a>
    status:
        allowed conditional target
    next/test:
        derive side split and scalar-to-L1 coupling

two-sided full scalar-times-L1:
    form:
        S0_full = eta<a,L1 a>
    status:
        allowed conditional target
    next/test:
        derive symmetric gluing to get side action

bulk DtN quadratic form:
    form:
        S0 = (1/2)<a,K_warped a>
    status:
        allowed alternative branch
    next/test:
        use instead of interface-local S0, not in addition

interface-local plus bulk DtN product:
    form:
        S0 = eta L1 plus K_warped for same H1 variable
    status:
        reject by double counting
    next/test:
        only allowed if variables are distinct and boundary graph proves it

bare measure volume coefficient:
    form:
        C_i from CP1/S2 or relative-plane volume
    status:
        reject
    next/test:
        bare measures are isotropic and normalization-dependent

block Hessian with free constants:
    form:
        K = diag(alpha I3, beta I2, ...)
    status:
        not Tier D
    next/test:
        derive constants from S_phi0 or keep as P_coeff
```

Three-hundred-twenty-fifth verdict:

```text
The orchestra can explain how eta, L1, gluing, and DtN alternatives meet.
```

But it also makes double counting easier.  Each instrument must have one
role in one branch unless a boundary graph proves otherwise.

## 341. Orchestra double-counting guard

Implemented in `native_orchestra_double_counting_guard.py`.

Double-counting guard:

```text
eta reuse:
    risk:
        using q/2, Brown-York stress, curvature jump, and eta as
        independent weights
    guardrail:
        treat them as the same edge scalar seen through different metric
        identities

interface plus DtN:
    risk:
        multiplying interface-local gamma by warped gamma for the same H1
        transfer
    guardrail:
        choose one transfer branch unless variables are proven distinct

H1 count versus H1 projection:
    risk:
        using the 1/3 projection and the 3-state trace as the same operation
    guardrail:
        projection makes eta; trace counts states after a transfer kernel
        exists

CP1/Hopf overcount:
    risk:
        counting M1 Hopf orientation as extra nodes in addition to shared
        H1 frame
    guardrail:
        Hopf bridge merges orientation into H1 unless residual variables
        are derived

M2 omission:
    risk:
        removing M2 because E1 is the desired d=3 branch
    guardrail:
        demote M2 only through primitive-bundle/energy/order rules or
        explicit coefficient result

coefficient constants:
    risk:
        turning symmetry-allowed alpha, beta, alpha_2 into fitted weights
    guardrail:
        derive them from S0 or leave Tier D open
```

Three-hundred-twenty-sixth verdict:

```text
The orchestra frame is useful only if it prevents overcounting.
```

Multiple metric identities may be:

```text
the same instrument,
```

not:

```text
separate additive contributions.
```

## 342. S0 full-action gate

Implemented in `native_s0_full_action_gate.py`.

The two ingredients:

```text
eta
```

and:

```text
L1
```

are not the same gate.

```text
edge scalar eta:
    status:
        available after banked P_phi0 plus H1/S2 projection
    supplies:
        eta=1/18
    does not supply:
        an angular operator

normalized ell=1 angular operator:
    status:
        metric-derived
    supplies:
        L1=(-R^2 Delta_S2)/2=I3 on H1
    does not supply:
        the coefficient eta

trace-preserving scalar lift:
    status:
        plausible but still a boundary-measure rule
    supplies:
        one scalar boundary budget distributed over the H1 identity
    does not supply:
        the transfer/gluing interpretation

full value action:
    status:
        not derived
    supplies:
        would be S0_full=eta <a,L1 a>
    does not supply:
        cannot be claimed from eta and L1 separately
```

Three-hundred-twenty-seventh verdict:

```text
The metric supplies eta and L1 as separate objects.
```

The missing `S0_full` gate is:

```text
the native boundary rule that forms the product eta L1 as the angular
value action.
```

## 343. S0 side-split gate

Implemented in `native_s0_side_split_gate.py`.

For the scalar weights:

```text
full scalar weight eta=1/18,
side scalar weight eta/2=1/36.
```

The side split has its own gates.

```text
full boundary action exists:
    status:
        not yet derived
    consequence:
        needed before a side split has anything to split

two-sided composability:
    status:
        conditional boundary-kernel structure
    consequence:
        left side plus right side equals one full shared boundary action

reflection symmetry:
    status:
        natural if the two sides are the same boundary object
    consequence:
        left weight equals right weight

side action:
    status:
        exact after the previous gates
    consequence:
        S0_side=(eta/2)<a,L1 a>
```

Three-hundred-twenty-eighth verdict:

```text
The half-factor is exact only after S0_full exists as a symmetric
composable boundary action.
```

It does not derive:

```text
S0_full.
```

## 344. S0 current composition status

Implemented in `native_s0_current_composition_status.py`.

Current status:

```text
eta:
    current status:
        available in active lane through P_phi0 and H1/S2 projection
    role:
        scalar edge weight

L1=I3:
    current status:
        metric-derived from the ell=1 Laplacian
    role:
        angular identity operator

eta L1:
    current status:
        missing coupling gate
    role:
        full angular value action

(eta/2)L1:
    current status:
        conditional after eta L1 plus symmetric side split
    role:
        one-sided transfer action

Tr exp[-(eta/2)L1]:
    current status:
        exact after one-sided transfer action exists
    role:
        gamma trace

powers of gamma:
    current status:
        conditional on independent typed nodes
    role:
        hierarchy ladder factors
```

Three-hundred-twenty-ninth verdict:

```text
The unresolved point is not the trace, the half split, or L1.
```

It is:

```text
the native coupling eta L1 inside S0_full.
```

## 345. H1 restriction eta-L1 simplification

Implemented in `native_h1_restriction_eta_l1_simplification.py`.

On the restricted `H1` transfer space, several full-S2 operator
distinctions collapse.

```text
isotropic angular surface stress:
    full S2 form:
        eta I on the selected angular boundary data
    H1 restriction:
        eta I3
    implication:
        enough for an H1 value action if H1 is already selected

normalized ell=1 Laplacian:
    full S2 form:
        eta L1, L1=(-R^2 Delta_S2)/2
    H1 restriction:
        eta I3
    implication:
        equivalent to isotropic stress after H1 restriction

rank-one direction stress:
    full S2 form:
        eta n n^T
    H1 restriction:
        eigenvalues depend on the chosen direction
    implication:
        not equivalent to the H1 identity trace unless averaged or traced
        differently

normalized second moment:
    full S2 form:
        eta I3/3 if applied as an operator after eta is already formed
    H1 restriction:
        eta I3/3
    implication:
        wrong if used after eta; the 1/3 projection has already been spent
        forming eta
```

Three-hundred-thirtieth verdict:

```text
If the transfer space is already H1, the metric does not need to derive
a full-S2 eta L1 coupling.
```

It only needs:

```text
an isotropic angular value action with scalar eta on H1.
```

## 346. H1 selection burden shift

Implemented in `native_h1_selection_burden_shift.py`.

The H1 restriction shifts the burden.

```text
full-S2 operator selection:
    before:
        derive why S0_full uses eta L1 rather than eta I, eta nn^T,
        or another operator
    after:
        not needed for the trace if H1 is independently selected
    status:
        burden reduced

H1 transfer-space selection:
    before:
        needed but partly obscured by eta L1 language
    after:
        central gate: why exactly the ell=1 triplet carries the transfer
    status:
        still open/conditional

constant-mode exclusion:
    before:
        one reason to prefer L1 over I on the full S2
    after:
        becomes part of H1 selection rather than part of coefficient coupling
    status:
        supported by exact ell=0 endpoint exclusion

isotropic angular value action:
    before:
        had to be eta L1 on full S2
    after:
        can be eta I3 on H1
    status:
        supported by angular-only shell stress after projection, but
        value-action status still conditional

side split and trace:
    before:
        unchanged
    after:
        still requires composable side kernel and trace interpretation
    status:
        conditional P_transfer
```

Three-hundred-thirty-first verdict:

```text
The coupling problem may reduce to H1 selection plus isotropic angular
value action.
```

This is progress, but it does not derive:

```text
P_transfer
or typed-depth factorization.
```

## 347. S0 revised active gate after H1 restriction

Implemented in `native_s0_revised_active_gate_after_h1_restriction.py`.

Revised active gate:

```text
eta scalar:
    revised status:
        available after banked P_phi0 and H1/S2 projection
    remaining gap:
        P_phi0 remains banked, not derived

H1 transfer space:
    revised status:
        best current selected space: ell=1 is first finite nonconstant
        angular bridge
    remaining gap:
        must show the transfer value action lives exactly on H1

S0_full on H1:
    revised status:
        can be written as eta <a,a>_H1, equivalently eta <a,L1 a>_H1
    remaining gap:
        must derive that the projected angular shell stress is a value
        action, not only first variation

S0_side on H1:
    revised status:
        becomes (eta/2)<a,a>_H1 if symmetric composable gluing is banked
    remaining gap:
        P_transfer gluing remains conditional

gamma trace:
    revised status:
        exact after S0_side exists: Tr_H1 exp[-(eta/2)I3]
    remaining gap:
        trace interpretation remains part of P_transfer

Tier D coefficients:
    revised status:
        unchanged: need typed second jet/coupled Hessian
    remaining gap:
        H1 restriction does not compute M1/M2/E1 coefficient weights
```

Three-hundred-thirty-second verdict:

```text
The active S0 gate is now narrower.
```

Derive:

```text
an isotropic angular value action on the already-selected H1 transfer
space.
```

Full-S2 `eta L1` coupling is sufficient, but may not be necessary.

## 348. Forced H1 operator merge

Implemented in `native_forced_h1_operator_merge.py`.

Once the transfer space is restricted to `H1`, the following become the
same operator:

```text
isotropic H1 value action:
    pre-merge form:
        eta I on selected angular data
    H1 form:
        eta I3
    merge status:
        merge allowed if selected data are H1

normalized ell=1 Laplacian action:
    pre-merge form:
        eta L1, with L1=(-R^2 Delta_S2)/2
    H1 form:
        eta I3
    merge status:
        merge forced after H1 projection

H1 trace action:
    pre-merge form:
        eta times the identity on a three-state transfer space
    H1 form:
        eta I3
    merge status:
        same object after transfer-space selection
```

Three-hundred-thirty-third verdict:

```text
After H1 transfer-space selection, these are not separate mechanisms.
```

They are the same H1 identity value action written in different metric
languages.

## 349. H1 merge boundary conditions

Implemented in `native_h1_merge_boundary_conditions.py`.

The merge is legitimate only under these conditions:

```text
H1 transfer-space selection:
    required status:
        must be derived or explicitly banked
    why needed:
        without H1 restriction, eta I and eta L1 differ on the full S2

ell=0 exclusion:
    required status:
        supported by exact endpoint equation
    why needed:
        prevents the constant mode from carrying the transfer action

isotropic value-action status:
    required status:
        still to derive
    why needed:
        shell stress gives angular scale, but value action is more than
        stress signature

projection not reused:
    required status:
        must be enforced
    why needed:
        the 1/3 has already been spent forming eta; do not apply I3/3 again
```

Three-hundred-thirty-fourth verdict:

```text
The merge is legitimate only after H1 selection.
```

It does not by itself prove:

```text
the value-action status
or transfer trace.
```

## 350. Do-not-merge remaining gates

Implemented in `native_do_not_merge_remaining_gates.py`.

Do not merge the following gates:

```text
P_phi0 / q=1/3:
    why not merged:
        H1 operator equivalence does not select the scalar edge slope q
    status:
        banked

symmetric side split:
    why not merged:
        full H1 value action and one-sided transfer are different
        composition levels
    status:
        conditional P_transfer

trace interpretation:
    why not merged:
        an operator on H1 does not automatically mean the physical
        operation is a trace
    status:
        conditional P_transfer

typed depth:
    why not merged:
        H1 identity action does not prove independent repeated nodes
    status:
        conditional P_depth

M1/M2/E1 coefficients:
    why not merged:
        H1 restriction does not compute the typed second jet
    status:
        open Tier D

bulk DtN branch:
    why not merged:
        interface-local H1 merge and bulk propagation are alternative
        branches for the same variable
    status:
        kept separate
```

Three-hundred-thirty-fifth verdict:

```text
The forced merge is only eta-I3/L1-on-H1.
```

Transfer, depth, coefficients, and q-origin remain separate gates.

## 351. Active chain after H1 merge

Implemented in `native_active_chain_after_h1_merge.py`.

Applying the forced merge gives the revised active chain.

```text
P_phi0 plus H1/S2 projection:
    status:
        banked scalar slope plus exact projection
    output:
        eta=1/18

H1 transfer-space selection:
    status:
        supported by ell=0 exclusion and ell=1 first finite nonconstant
        bridge; still a gate
    output:
        transfer space H1 with dim=3

forced H1 operator merge:
    status:
        exact after H1 selection
    output:
        isotropic stress, eta L1|H1, and eta I3 are one object

H1 full value action:
    status:
        still requires value-action status
    output:
        S0_full|H1 = eta I3

symmetric side split:
    status:
        conditional P_transfer gluing
    output:
        A_side|H1=(eta/2)I3=(1/36)I3

H1 trace:
    status:
        conditional P_transfer trace interpretation
    output:
        gamma=Tr exp[-(1/36)I3]=3 exp(-1/36)
```

Three-hundred-thirty-sixth verdict:

```text
The scalar-to-L1 product gate is replaced by a forced H1 identity merge.
```

The remaining active gate is:

```text
value-action status on H1,
```

followed by optional `P_transfer` gluing and trace.

## 352. P_transfer after H1 merge

Implemented in `native_p_transfer_after_h1_merge.py`.

Revised `P_transfer` status:

```text
H1 identity value action:
    revised status:
        merged object if H1 selected and isotropic value-action status
        is derived/banked
    consequence:
        S0_full|H1=eta I3

side split:
    revised status:
        conditional on symmetric composable boundary action
    consequence:
        A_side|H1=(eta/2)I3

trace operation:
    revised status:
        conditional on unlabelled H1 boundary-state count
    consequence:
        gamma=3 exp(-eta/2)

node product:
    revised status:
        not supplied by P_transfer
    consequence:
        needed before gamma powers are licensed
```

Three-hundred-thirty-seventh verdict:

```text
P_transfer no longer needs a separate full-S2 eta-L1 coupling.
```

It still needs:

```text
value-action status,
side composability,
trace,
and later node-product structure.
```

## 353. Consequence map after H1 merge

Implemented in `native_consequence_map_after_h1_merge.py`.

Updated consequence map:

```text
Tier A: eta foundation:
    licensed:
        eta=1/18 from banked P_phi0 plus exact H1/S2 projection
    not licensed:
        q-origin

Tier A2: H1 identity merge:
    licensed:
        if H1 is selected, eta I3 and eta L1|H1 are the same operator
    not licensed:
        value-action status

Tier B: transfer:
    licensed:
        if value action, side split, and trace are banked,
        gamma=3 exp(-1/36)
    not licensed:
        gamma powers / node product

Tier C: typed graph:
    licensed:
        if P_depth is banked, symbolic gamma^5 and gamma^7 ladders
    not licensed:
        branch coefficients and M2 coefficient/suppression

Tier D: coefficients:
    licensed:
        not licensed by H1 merge
    not licensed:
        S_phi0 typed second jet
```

Three-hundred-thirty-eighth verdict:

```text
The merge upgrades the operator gate, not the postulate ledger.
```

It reduces `P_transfer`'s burden but leaves:

```text
q-origin,
gluing/trace,
typed depth,
and coefficients
```

separate.

## 354. Self-similar C1 value action

Implemented in `native_self_similar_c1_value_action.py`.

For a self-similar finite negative-phi cell:

```text
f(r) = (R/r)^q
f(R) = 1
f' = -q R^q r^(-q-1)
```

The radial C1 action is:

```text
S_C1 = (1/4) integral_0^R r^2 f'^2 dr
     = q^2 R / [4(1-2q)]
```

so the scale-normalized action is:

```text
S_C1/R = q^2/[4(1-2q)].
```

For the banked self-similar branch:

```text
q = 1/3
S_C1/R = 1/12
H1 projection = (S_C1/R)/3 = 1/36
eta = q/6 = 1/18
eta/2 = 1/36
```

Three-hundred-thirty-ninth verdict:

```text
The projected on-shell C1 action value equals eta/2 exactly.
```

This is not a linear approximation. It is the exact C1 action of the
self-similar branch, normalized by `R`, then projected through the same
`H1/S2` factor that supplied the angular isotropic share.

## 355. C1 value-action q condition

Implemented in `native_c1_value_action_q_condition.py`.

Demand that the projected C1 action value equal the side action:

```text
[q^2/(4(1-2q))]/3 = eta/2
```

With:

```text
eta = q/6
```

this becomes:

```text
q^2/[12(1-2q)] = q/12.
```

For the nontrivial branch `q != 0`:

```text
q/(1-2q) = 1
q = 1 - 2q
3q = 1
q = 1/3
```

The branches are therefore:

```text
q=0:
    trivial

q=1/3:
    nontrivial self-similar value-action branch
```

Three-hundred-fortieth verdict:

```text
q=1/3 is not only a banked slope here; it is the nontrivial solution of
projected C1 value action = eta/2.
```

This still does not fully derive `P_phi0`, because the physical rule
selecting this equality must be justified. But it upgrades `q=1/3` from
a loose imposed value to a metric value-action fixed-point candidate.

## 356. Value-action status after C1

Implemented in `native_value_action_status_after_c1.py`.

Updated gate status:

```text
H1 side action value:
    previous status:
        conditional on symmetric gluing after eta
    updated status:
        exactly matched by projected self-similar C1 action at q=1/3
    remaining gap:
        interpret the projected radial action as the H1 boundary value action

q=1/3:
    previous status:
        banked P_phi0
    updated status:
        supported by value-action equality condition
    remaining gap:
        still needs a variational selection argument if promoted from postulate

S0_full on H1:
    previous status:
        missing value-action status
    updated status:
        two projected C1 sides would compose to eta if symmetric full action is required
    remaining gap:
        derive the two-sided composition object

trace gamma:
    previous status:
        conditional P_transfer
    updated status:
        unchanged; exact if side action is traced over H1 states
    remaining gap:
        trace interpretation remains conditional

Tier D coefficients:
    previous status:
        open
    updated status:
        unchanged
    remaining gap:
        need typed second jet beyond the scalar H1 side action
```

Three-hundred-forty-first verdict:

```text
The metric appears to supply the eta/2 side value through its own C1
action, once the self-similar q=1/3 branch and H1 projection are in place.
```

That is a real narrowing of `P_transfer`.

The remaining burden is no longer:

```text
where does eta/2 numerically come from?
```

The remaining burden is sharper:

```text
why is the projected C1 action the transfer boundary value action,
why is the physical operation a trace over H1 states,
and how do node products/depth and Tier D coefficients arise?
```

## 357. C1 value-momentum pair

Implemented in `native_c1_value_momentum_pair.py`.

The C1 functional now supplies a paired object.

For the self-similar finite cell:

```text
f(r) = (R/r)^q
S_C1/R = q^2/[4(1-2q)]
-Pi_f/R = q/2 at phi0
```

At `q=1/3`:

```text
S_C1/R = 1/12
H1 projected action = 1/36
H1 projected momentum = 1/18
eta = q/6 = 1/18
eta/2 = 1/36
```

Exact pair:

```text
projected momentum = eta
projected action   = eta/2
```

Three-hundred-forty-second verdict:

```text
The same C1 metric functional supplies both the eta momentum and the
eta/2 action value on the self-similar H1-projected branch.
```

This fills the numerical value-action hole more strongly than symmetric
gluing alone. The remaining gate is operational:

```text
is this projected C1 action the physical transfer boundary action?
```

## 358. H1 internal trace from gluing

Implemented in `native_h1_internal_trace_gluing.py`.

Let the one-side H1 transfer kernel be:

```text
K_ij = exp(-a) delta_ij
a = eta/2 = 1/36
```

If an external H1 label is fixed:

```text
K_ii = exp(-a)
```

If the H1 label is internal after gluing and unobserved:

```text
sum_i K_ii = Tr_H1 K = 3 exp(-a)
```

This is an index contraction, not an average:

```text
normalized average -> exp(-a)
determinant        -> exp(-3a)
trace              -> 3 exp(-a)
```

Three-hundred-forty-third verdict:

```text
Once the metric gives an identity kernel on H1 and the H1 label is an
internal glued boundary label, the trace is the natural invariant
contraction.
```

The remaining gate is now specific:

```text
prove the particle transfer leaves the H1 label internal/unobserved,
rather than externally fixed or normalized away.
```

## 359. Metric product law from locality

Implemented in `native_metric_product_law_from_locality.py`.

For one independent H1 transfer slot:

```text
K = exp(-a) I3
a = 1/36
Tr K = 3 exp(-a) = gamma
```

For `n` independent local slots:

```text
K_total = K_1 tensor K_2 tensor ... tensor K_n
Tr K_total = product_i Tr K_i
           = gamma^n
```

Numerically:

```text
n=5: gamma^n = 211.488908378
n=7: gamma^n = 1800.53941904
```

Three-hundred-forty-fourth verdict:

```text
The metric/local-action side supplies the product law if the boundary
slots are independent local transfer factors.
```

It does not by itself derive:

```text
M1 depth = 5
E1 depth = 7
```

Those still require a typed boundary graph or Hessian that identifies
the independent slots.

## 360. Metric jigsaw hole scan

Implemented in `native_jigsaw_metric_hole_scan.py`.

Updated hole map:

```text
eta/2 side value:
    metric piece:
        self-similar C1 action value, H1-projected:
        (S_C1/R)/3 = 1/36
    status:
        filled conditionally on q=1/3 self-similar branch
    remaining gap:
        justify the value-action equality as the selected boundary rule

eta momentum:
    metric piece:
        C1 canonical boundary momentum, H1-projected:
        (-Pi_f/R)/3 = 1/18
    status:
        filled under banked P_phi0
    remaining gap:
        derive q=1/3 or keep it banked

trace over H1:
    metric piece:
        identity kernel on the three-dimensional H1 transfer space;
        internal label contraction gives Tr
    status:
        filled if the H1 label is internal/unobserved after gluing
    remaining gap:
        prove the particle transfer is an internal H1 boundary contraction

gamma product powers:
    metric piece:
        local action additivity and tensor-product trace over independent
        transfer slots
    status:
        filled as a product law once independent slots exist
    remaining gap:
        derive the typed slot counts and independence graph

M1/E1 typed depths:
    metric piece:
        common H1 frame plus side shape variables are visible in the
        metric inventory
    status:
        partly outlined, not derived
    remaining gap:
        construct the boundary Hessian/edge graph that selects 5 and 7 factors

Tier D coefficients:
    metric piece:
        metric second jet/Hessian of S_phi0 in typed boundary variables
    status:
        not filled
    remaining gap:
        derive the actual typed second jet rather than inserting coefficients
```

Three-hundred-forty-fifth verdict:

```text
The metric now appears to fill the eta and eta/2 numerical pieces.
It also supplies exact trace/product operations if the boundary labels
are internal and independent.
```

The unresolved pieces have moved to:

```text
q selection,
internal-label status,
typed independence,
and the typed second jet.
```

## 361. q=1/3 convergence pattern

Implemented in `native_q_one_third_convergence_pattern.py`.

At `q=1/3`, several exact metric balances coincide:

```text
profile exponent q                 = 1/3
finite-action remainder 1-2q       = 1/3
unprojected C1 action S_C1/R       = 1/12
unprojected boundary momentum q/2  = 1/6
action / momentum                  = 1/2
```

Equivalent nontrivial conditions:

```text
1 - 2q = q                 -> q=1/3
q^2/[4(1-2q)] = q/4        -> q=1/3
[S_C1/R]/3 = (q/6)/2       -> q=1/3
```

Three-hundred-forty-sixth verdict:

```text
q=1/3 is the point where profile scaling, finite-action scaling,
C1 action value, and projected side-action normalization lock together.
```

This is convergence evidence, not a standalone variational selection
theorem. It says the metric is repeatedly pointing at the same branch
from different native faces.

## 362. Trace/product merge pattern

Implemented in `native_trace_product_merge_pattern.py`.

For one internal H1 boundary label:

```text
K = exp(-a) I3
a = 1/36
Tr K = 3 exp(-a)
```

For two independent internal labels:

```text
K_total = K_1 tensor K_2
Tr K_total = Tr(K_1) Tr(K_2)
             = gamma^2
```

Thus trace and product are not separate mechanisms once independent
local boundary labels are established.

Three-hundred-forty-seventh verdict:

```text
The operation-level jigsaw piece is internal-label contraction.
```

A single internal label gives a trace. Independent local internal labels
give tensor-product traces and therefore gamma powers.

## 363. Depth side-pair pattern

Implemented in `native_depth_side_pair_pattern.py`.

The candidate depth pattern is:

```text
depth = common H1 frame + two boundary sides * side-shape dimension
      = 3 + 2s
```

For the active branches:

```text
M1 compact primitive:
    common H1 frame nodes = 3
    side shape dimension  = 1
    boundary sides        = 2
    depth                 = 5
    status:
        candidate compact residual shape scalar per side

E1 ordinary H1:
    common H1 frame nodes = 3
    side shape dimension  = 2
    boundary sides        = 2
    depth                 = 7
    status:
        candidate relative H1 shape plane per side
```

Three-hundred-forty-eighth verdict:

```text
The 5 and 7 depths have a shared metric form: 3 + 2s.
```

This is stronger than two unrelated counts, but it still depends on
proving that each side-shape coordinate is an independent internal
transfer label.

## 364. C1 radial second-jet piece

Implemented in `native_c1_radial_second_jet_piece.py`.

For:

```text
A(q) = S_C1/R = q^2/[4(1-2q)]
```

the exact derivatives at `q=1/3` are:

```text
A(1/3)            = 1/12
A'(1/3)           = 1
A''(1/3)          = 27/2
H1-projected A''/3 = 9/2
```

Three-hundred-forty-ninth verdict:

```text
The C1 metric supplies an exact scalar radial stiffness at the q=1/3 branch.
```

This is a second-jet piece in the q/radial direction, not the full typed
Hessian for M1/E1 coefficients.

Tier D should therefore not start from free coefficient fitting. It should
first ask whether each typed Hessian block descends from exact C1/HJ
second variations like this radial piece.

## 365. Exact q-variation Taylor expansion

Implemented in `native_c1_q_taylor_variation_exact.py`.

Let:

```text
A(q) = S_C1/R = q^2/[4(1-2q)]
q0 = 1/3
u = q - q0
```

Exact derivatives:

```text
A(q0)   = 1/12
A'(q0)  = 1
A''(q0) = 27/2
```

Taylor expansion through second order:

```text
A(q0+u) = 1/12 + u + (27/4)u^2 + O(u^3)
```

H1-projected Taylor expansion:

```text
A_H1(q0+u) = 1/36 + (1/3)u + (9/4)u^2 + O(u^3)
```

Three-hundred-fiftieth verdict:

```text
q=1/3 is not a stationary point of the bare radial C1 action.
```

Therefore the metric is not saying:

```text
bare C1 minimization selects q=1/3.
```

It is saying:

```text
q=1/3 is the self-similar/action-value balance point.
```

A further constraint or boundary condition is required if `q=1/3` is to
be promoted from balance branch to variationally selected branch.

## 366. Warped DtN Hessian spectrum

Implemented in `native_warped_dtn_hessian_spectrum.py`.

For the self-similar collar `q=1/3`, the finite angular-mode branch has
exact DtN eigenvalues:

```text
D_ell =
    sqrt(ell(ell+1))
    I_{7/2}(6 sqrt(ell(ell+1)))
    / I_{5/2}(6 sqrt(ell(ell+1)))
```

for `ell >= 1`, and:

```text
D_0 = 0.
```

Numerical diagnostics:

```text
ell  degeneracy  role                D_ell
0    1           scalar zero mode    0
1    3           H1 triplet          0.979663326282794223
2    5           higher shape block  1.98578554532783401
3    7           higher shape block  2.98930596601578915
4    9           higher shape block  3.99146105672220567
5    11          higher shape block  4.99290164261621273
```

Three-hundred-fifty-first verdict:

```text
If the phi0 action is the on-shell warped-collar action, the angular
second variation is diagonal in ell,m with eigenvalues D_ell.
```

The `ell=1` block is exactly proportional to `I3` by degeneracy. It is
not equal to the intrinsic boundary `L1=I3` kernel unless the Bessel-ratio
factor is removed by a separate boundary-action rule.

## 367. Metric variation block diagonal pattern

Implemented in `native_metric_variation_block_diagonal.py`.

The metric variation separates into blocks:

```text
radial q / scalar branch:
    metric origin:
        self-similar C1 action A(q)=q^2/[4(1-2q)]
    first variation:
        nonzero at q=1/3: A'(1/3)=1
    second variation:
        A''(1/3)=27/2; H1-projected scalar stiffness 9/2
    consequence:
        q selection needs a constraint/boundary condition, not bare stationarity

ell=0 angular boundary mode:
    metric origin:
        constant S2 mode
    first variation:
        couples to scalar/radial normalization
    second variation:
        DtN eigenvalue D_0=0 for constant finite mode
    consequence:
        not a particle transfer triplet

ell=1 / H1 triplet:
    metric origin:
        round S2 degeneracy plus warped collar DtN
    first variation:
        orthogonal to scalar radial first variation
    second variation:
        D_1 I3 for warped on-shell action,
        or I3 for intrinsic boundary action
    consequence:
        metric supplies the threefold identity block

ell>=2 shape blocks:
    metric origin:
        higher S2 harmonics / relative-shape variables
    first variation:
        orthogonal to ell=0 and ell=1 by S2 harmonic orthogonality
    second variation:
        D_ell I_(2ell+1) inside each irreducible block
    consequence:
        candidate home for typed shape Hessian pieces
```

Three-hundred-fifty-second verdict:

```text
The metric action naturally separates scalar/radial, H1 triplet,
and higher-shape Hessian blocks.
```

Coefficients should be searched as exact block eigenvalues, reductions,
or Schur complements, not inserted.

## 368. H1 relative-plane Hessian

Implemented in `native_h1_relative_plane_hessian.py`.

Start with an H1 identity Hessian:

```text
K_H1 = k I3
```

Choose an orthonormal split:

```text
e0 = common-amplitude direction
e1,e2 = relative-shape plane
```

Because `K_H1` is proportional to `I3`:

```text
O^T K_H1 O = k I3
```

After fixing or removing the common amplitude `e0`:

```text
K_relative = k I2
```

For the intrinsic side-action branch:

```text
k = eta/2 = 1/36
K_relative = (1/36) I2
```

For the warped-DtN branch:

```text
k = fixed normalization * D_1
K_relative = same k on both relative coordinates
```

Three-hundred-fifty-third verdict:

```text
The E1 two-dimensional relative plane does not require a new anisotropic
coefficient if it is the common-amplitude quotient of the H1 identity block.
```

The open question is whether the typed E1 relative plane is exactly this
quotient.

## 369. Variation gap update

Implemented in `native_variation_gap_update.py`.

Updated gaps:

```text
q selection:
    newly calculated:
        bare C1 A'(1/3)=1, so q=1/3 is not bare-action stationary
    still missing:
        the constraint or boundary condition whose stationarity selects
        the self-similar balance

H1 identity Hessian:
    newly calculated:
        ell=1 second variation is an exact identity block by S2 degeneracy
    still missing:
        choice between intrinsic boundary I3 and warped DtN B I3 as the
        physical transfer action

trace/product:
    newly calculated:
        internal-label contraction plus tensor-product locality explains
        trace and powers
    still missing:
        proof that typed particle slots are internal, local, and independent

typed coefficients:
    newly calculated:
        radial second-jet and angular DtN blocks are calculable
        metric-action pieces
    still missing:
        the typed boundary reduction/Schur complement that maps those blocks
        to C_M1 and C_E1
```

Three-hundred-fifty-fourth verdict:

```text
The metric action is producing variation data.
```

The next exact task is not coefficient fitting. It is boundary reduction:

```text
identify which variation block is integrated out,
which is fixed,
which is traced,
and which is left internal.
```

## 370. Variation orchestra pattern

Implemented in `native_variation_orchestra_pattern.py`.

The metric action is producing a small set of reusable voices:

```text
radial scalar:
    metric variation:
        A(q), A'(q), A''(q) from self-similar C1 action
    orchestra role:
        sets value/momentum/stiffness in the scalar q direction
    open gate:
        stationarity constraint selecting q=1/3

H1 identity:
    metric variation:
        ell=1 angular second variation is an identity block
    orchestra role:
        provides the three channel states and their equal action
    open gate:
        intrinsic boundary action versus warped on-shell DtN choice

relative H1 plane:
    metric variation:
        quotient of k I3 by common amplitude leaves k I2
    orchestra role:
        candidate source of the E1 two side-shape coordinates
    open gate:
        prove typed E1 shapes are exactly this quotient

higher angular blocks:
    metric variation:
        ell>=2 DtN blocks are diagonal by S2 irreducibility
    orchestra role:
        possible dormant or correction voices
    open gate:
        show whether particle sector uses or suppresses them

local product:
    metric variation:
        independent local variations produce tensor-product Hessian traces
    orchestra role:
        turns one transfer block into gamma powers
    open gate:
        derive independence of typed boundary slots
```

Three-hundred-fifty-fifth verdict:

```text
The particle sector likely selects and composes native metric-variation
voices rather than requiring unrelated mechanisms.
```

## 371. Current non-repeated state after variation audit

This section consolidates the current frontier so later context resets do
not re-open superseded loops.

The active result is not:

```text
gamma was assumed,
eta/2 was inserted,
and typed depth was fitted.
```

The active result is:

```text
the metric is now supplying exact pieces, while a smaller set of
operation/selection gates remains open.
```

Current filled or narrowed pieces:

```text
eta:
    status:
        supplied by C1 boundary momentum plus H1/S2 projection
    exact value:
        eta = 1/18 under q=1/3

eta/2:
    old status:
        conditional side split / transfer ansatz
    current status:
        exact projected C1 action value on the self-similar q=1/3 branch
    exact value:
        (S_C1/R)/3 = 1/36 = eta/2

H1 identity block:
    old status:
        separate eta-I3 / eta-L1 coupling burden
    current status:
        after H1 selection, isotropic stress, L1|H1, and I3 are the same
        identity block

trace:
    old status:
        abstract transfer postulate
    current status:
        exact invariant contraction if the H1 label is internal after gluing

gamma powers:
    old status:
        repeated ladder ansatz
    current status:
        exact tensor-product trace law if independent local transfer slots exist

typed depths:
    old status:
        separate 5 and 7 counts
    current status:
        shared pattern depth = 3 + 2s, with s=1 for M1 and s=2 for E1
    remaining gate:
        prove side-shape coordinates are independent internal transfer labels

second variation:
    old status:
        missing coefficient object
    current status:
        radial C1 second jet and angular warped-DtN Hessian blocks are
        calculable metric-action pieces
```

Current open gates:

```text
q selection:
    q=1/3 is a self-similar/action-value balance point, not a bare C1
    stationary point. A boundary condition or constraint must select it,
    or it remains banked.

transfer-action branch:
    decide whether the physical transfer action is intrinsic boundary I3
    or on-shell warped DtN D_1 I3.

internal-label status:
    prove that particle transfer leaves H1 labels internal/unobserved so
    the physical contraction is trace, not fixed label, average, or determinant.

typed independence:
    prove M1/E1 side-shape coordinates factor as independent local transfer
    slots.

boundary reduction:
    compute the Schur complement / reduction rule that maps metric Hessian
    blocks to branch coefficients C_M1 and C_E1.
```

Superseded or downgraded loops:

```text
derive eta/2 only from symmetric gluing:
    superseded by projected C1 action value; gluing may still interpret
    composition but no longer supplies the number by itself

derive full-S2 eta L1 coupling:
    superseded after H1 selection by forced H1 identity merge

fit Tier D coefficients from lepton ratios:
    rejected; lepton ratios remain diagnostics only

claim q=1/3 from bare C1 minimization:
    rejected; A'(1/3)=1

collapse intrinsic boundary action and warped DtN:
    rejected unless a boundary-action rule proves the Bessel factor should
    be removed
```

Three-hundred-fifty-sixth verdict:

```text
The work is progressing: the repeated open gates have narrowed into a
boundary-reduction problem.
```

Next best exact task:

```text
construct the boundary reduction map:
    choose/fix/trace/internalize the scalar q block,
    the H1 identity block,
    the relative H1 plane,
    and higher angular blocks,
then compute the resulting Schur complement or block determinant.
```

## 372. Second-variation cross-term audit

Implemented in `native_second_variation_cross_term_audit.py`.

Use the local quadratic form for angular boundary data:

```text
S(q,a) = A(q) + (1/2) D_l(q) sum_m a_m^2 + higher order
```

At the background angular amplitude `a_m=0`:

```text
dS/dq        = A'(q)
dS/da_m      = D_l(q) a_m
d2S/dq da_m  = D_l'(q) a_m = 0
d2S/da_m da_n = D_l(q) delta_mn
```

Exact consequence:

```text
The scalar q block and angular amplitude blocks are Hessian
block-diagonal at zero angular background amplitude.
```

Three-hundred-fifty-seventh verdict:

```text
A q-angular Schur complement cannot generate branch coefficients at
second order unless a nonzero background angular mode, boundary constraint,
or explicit same-representation cross term is derived.
```

This rules out a tempting but unsupported path:

```text
use generic q-angular mixing to tune M1/E1 coefficients.
```

The metric does not give that mixing at the quadratic background level.

## 373. Boundary operation reduction table

Implemented in `native_boundary_operation_reduction_table.py`.

For an identity block `a I_d`, the possible boundary operations are not
interchangeable:

```text
fixed external label:
    operation:
        select one diagonal channel of exp(-a I_d)
    result:
        exp(-a)
    status:
        not gamma; no multiplicity factor

internal unobserved label:
    operation:
        contract the boundary index: Tr exp(-a I_d)
    result:
        d exp(-a)
    status:
        gamma form for d=3 and a=eta/2

normalized average:
    operation:
        (1/d) Tr exp(-a I_d)
    result:
        exp(-a)
    status:
        removes the multiplicity; not gamma

determinant:
    operation:
        det exp(-a I_d)
    result:
        exp(-a d)
    status:
        different exponent; not gamma

Gaussian integration:
    operation:
        integral exp[-(1/2) x^T k I_d x] dx
    result:
        (2 pi/k)^(d/2), up to measure
    status:
        measure-sensitive; dangerous unless metric measure is derived

Schur complement:
    operation:
        integrate/fix a coupled block [[A,C],[C^T,B]]
    result:
        B - C^T A^(-1) C
    status:
        requires an exact cross block C
```

Three-hundred-fifty-eighth verdict:

```text
The metric can supply the block, but the physical boundary operation
decides whether the block contributes a trace, determinant, average,
Gaussian measure, or Schur complement.
```

Therefore `gamma` specifically requires:

```text
internal unobserved H1 label contraction.
```

It is not produced by determinant, average, Gaussian integration, or a fixed
external label.

## 374. Two-side shape Schur pattern

Implemented in `native_two_side_shape_schur_pattern.py`.

Let each side-shape space have dimension `s` and isotropic block `k I_s`.

The exact reduction cases are:

```text
local independent sides:
    cross coupling:
        c = 0
    eigenvalues:
        k, k on each side-shape coordinate
    if one side is eliminated:
        k
    verdict:
        product trace allowed if labels are internal and independent

symmetric same-representation coupling:
    cross coupling:
        c != 0 in [[kI_s,cI_s],[cI_s,kI_s]]
    eigenvalues:
        k+c and k-c, each with degeneracy s
    if one side is eliminated:
        k - c^2/k
    verdict:
        exact reduction formula, but c must come from the metric boundary action

hard side matching:
    cross coupling:
        constraint x_core = x_phi0
    eigenvalues:
        one side-pair variable instead of two independent variables
    if one side is eliminated:
        not a Schur coefficient; it changes depth
    verdict:
        would reduce depth and invalidate gamma^(3+2s)
```

Three-hundred-fifty-ninth verdict:

```text
The depth pattern 3+2s requires the local independent-sides case.
```

Any same-representation cross coupling or hard matching must be derived
before it can modify coefficients or depth.

## 375. Current boundary-reduction map

Implemented in `native_boundary_reduction_current_map.py`.

Boundary reduction is now a finite decision table over metric-supplied blocks:

```text
scalar q block:
    metric supplied:
        A(1/3)=1/12, A'(1/3)=1, A''(1/3)=27/2
    allowed reductions:
        fixed by boundary condition,
        constrained to q=1/3,
        or integrated with a derived measure
    current best status:
        not stationary by bare C1; likely fixed/constrained, not traced

H1 identity block:
    metric supplied:
        I3 with side action eta/2,
        or warped D1 I3 if on-shell collar is used
    allowed reductions:
        internal trace,
        fixed label,
        normalized average,
        determinant,
        or Gaussian integration
    current best status:
        gamma requires internal trace

E1 relative plane:
    metric supplied:
        k I2 if it is the common-amplitude quotient of H1
    allowed reductions:
        two independent side traces,
        side matching,
        or same-representation Schur coupling
    current best status:
        depth=7 requires two independent side planes

M1 compact residual scalar:
    metric supplied:
        one side-shape scalar per side if CP1/Hopf quotient supplies s=1
    allowed reductions:
        two independent side traces,
        side matching,
        or scalar 2x2 Schur reduction
    current best status:
        depth=5 requires two independent side scalars

higher ell blocks:
    metric supplied:
        D_ell I_(2ell+1) from warped DtN for ell>=2
    allowed reductions:
        suppressed,
        fixed,
        integrated,
        or included as correction voices
    current best status:
        not currently part of active ladder unless a selection rule admits them
```

Three-hundred-sixtieth verdict:

```text
The next hidden metric piece to seek is not another number; it is the
boundary condition or measure that chooses the reduction column.
```

## 376. Induced S2 measure H1 trace

Implemented in `native_induced_s2_measure_h1_trace.py`.

On the `phi0` boundary, the induced angular measure is the round `S2` measure:

```text
dmu = dOmega
```

For the `ell` subspace, the projector diagonal obeys the addition theorem:

```text
P_ell(Omega,Omega) = sum_m |Y_ell,m(Omega)|^2
                   = (2 ell + 1)/(4 pi)
```

Therefore:

```text
Tr P_ell = integral_S2 P_ell(Omega,Omega) dOmega
         = 2 ell + 1
```

For `H1 / ell=1`:

```text
Tr P_H1 = 3
side action a = eta/2 = 1/36
Tr_H1 exp(-a I3) = exp(-a) Tr P_H1
                 = 3 exp(-1/36)
```

Three-hundred-sixty-first verdict:

```text
The factor 3 is not an imported state count if the boundary operation is
the induced-measure trace over the H1 projector.
```

It is the round-S2 boundary measure reading the `ell=1` degeneracy.

## 377. Plain-sight internal-boundary trace

Implemented in `native_plain_sight_internal_boundary_trace.py`.

A `phi0` surface can be read in two different ways:

```text
external boundary:
    H1 label is fixed by outside data
    contribution = K_ii = exp(-a)

internal glued interface:
    H1 label lives on the shared phi0 boundary
    outside observer does not fix which H1 basis label crosses the interface
    gluing contracts the shared index
    contribution = sum_i K_ii = Tr_H1 K
```

For:

```text
K = exp(-a) I3
```

the internal interface contraction gives:

```text
Tr_H1 K = 3 exp(-a)
```

Three-hundred-sixty-second verdict:

```text
If phi0 is the bridge between negative-phi matter side and positive-phi
scalar/background side, the H1 label is naturally internal to the bridge.
```

Then trace is the gluing contraction, not an extra mechanism.

## 378. phi0 Calderon plain-sight audit

Implemented in `native_phi0_calderon_plain_sight.py`.

The `phi0` boundary already exposes the ingredients of a Cauchy-data problem:

```text
Dirichlet value:
    metric object:
        f(phi0)=1
    role:
        sets the phi0 interface surface
    status:
        exact by definition of phi0

Neumann momentum:
    metric object:
        -Pi_f/R=q/2
    role:
        sets the C1 boundary momentum jump
    status:
        exact once q is selected/banked

H1 boundary data:
    metric object:
        ell=1 projector on the round S2 boundary
    role:
        finite angular interface label space
    status:
        exact after H1 selection

two-sided extension:
    metric object:
        negative-phi side plus positive/scalar side sharing phi0
    role:
        turns phi0 data into internal Cauchy data
    status:
        supported by bridge geometry; projector not fully constructed
```

Calderon reading:

```text
The missing boundary-reduction rule may be the phi0 Cauchy-data projector:
keep only boundary data that extend to both sides of the interface,
then contract internal H1 labels with the induced S2 measure.
```

Three-hundred-sixty-third verdict:

```text
The metric already exposes the ingredients of the reduction rule:
phi0 value, C1 momentum, H1 projector, and two-sided interface data.
```

What remains is constructing the exact projector, not inventing a force.

## 379. Boundary measure decision update

Implemented in `native_boundary_measure_decision_update.py`.

Updated gate status:

```text
trace operation:
    previous status:
        conditional internal-label rule
    plain-sight piece:
        round-S2 induced measure gives Tr P_H1=3;
        internal phi0 gluing contracts the label
    revised status:
        strongly supported if phi0 is treated as internal two-sided interface

boundary operation choice:
    previous status:
        finite decision table
    plain-sight piece:
        external boundary fixes labels;
        internal boundary traces labels
    revised status:
        reduced to deciding whether phi0 is external or internal for
        particle transfer

H1 state count:
    previous status:
        abstract degeneracy
    plain-sight piece:
        addition theorem integrates projector diagonal to 3
    revised status:
        metric-measure supplied

coefficient reduction:
    previous status:
        open Schur/complement problem
    plain-sight piece:
        Calderon/Cauchy projector is the natural reduction object
    revised status:
        still open; exact projector must be constructed
```

Three-hundred-sixty-fourth verdict:

```text
The trace factor may be hiding in plain sight in the induced S2 measure
plus internal-boundary gluing.
```

The remaining hard object is now sharper:

```text
construct the exact phi0 Cauchy-data / Calderon projector.
```

## 380. phi0 Cauchy projector first form

Implemented in `native_phi0_cauchy_projector_first_form.py`.

Metric boundary data at `phi0`:

```text
value constraint:
    f|phi0 = 1

C1 momentum jump:
    Delta Pi_f/R = q/2

angular boundary space:
    H1 = ell=1(S2)

induced measure:
    round S2 measure
```

For `q=1/3`:

```text
Delta Pi_f/R = 1/6
H1 projection eta = (Delta Pi/R)/3 = 1/18
projected C1 side action = eta/2 = 1/36
```

First-form projector:

```text
P_phi0 = P_value(f=1) * P_jump(Delta Pi=q/2) * P_H1
```

On an H1 identity side action:

```text
P_H1 exp[-(eta/2) I3] P_H1 = exp(-1/36) P_H1

Tr_boundary[...] = exp(-1/36) Tr(P_H1)
                 = 3 exp(-1/36)
```

Three-hundred-sixty-fifth verdict:

```text
The metric-supplied value constraint, momentum jump, H1 projector, and
induced boundary measure compose directly into the gamma kernel if phi0
is treated as an internal two-sided interface.
```

Remaining caveat:

```text
prove this first-form product is the exact Calderon projector for the
UDT phi0 bridge.
```

## 381. Cauchy graph projector idempotence

Implemented in `native_cauchy_graph_projector_idempotence.py`.

For a one-mode boundary graph:

```text
p = lambda u
```

use the Dirichlet-fiber projection from arbitrary Cauchy data `(u,p)` to
admissible data:

```text
P_lambda(u,p) = (u, lambda u)
```

Matrix form:

```text
P = [ 1      0
      lambda 0 ]
```

For:

```text
lambda = 1/36
```

the check is exact:

```text
P^2 = P
```

For H1, `lambda` acts as `lambda I3`, so this graph projector is copied on
each of the three H1 boundary labels.

Three-hundred-sixty-sixth verdict:

```text
A Cauchy projector is the graph of the metric's DtN/action relation.
```

The unresolved issue is which `lambda` is physical:

```text
intrinsic eta/2,
warped DtN dressing,
or a constrained two-sided combination.
```

## 382. Internal gluing symplectic form

Implemented in `native_internal_gluing_symplectic_form.py`.

For a boundary field `u` with conjugate momentum `p`, the C1/HJ boundary
variation has canonical form:

```text
delta S_boundary = integral_boundary p delta u
```

For two regions glued at `phi0`, orientations are opposite. The shared
boundary variation is:

```text
delta S_glued = integral_phi0 (p_minus + p_plus + p_source) delta u
```

Admissible internal gluing imposes:

```text
u_minus = u_plus
p_minus + p_plus + p_source = 0
```

Consequences:

```text
the shared value u is not external data;
the shared label is summed/contracted in the glued amplitude;
for an H1 identity kernel, this contraction is Tr_H1.
```

Three-hundred-sixty-seventh verdict:

```text
Internal trace is the boundary symplectic gluing rule in finite dimensions.
```

It becomes an extra assumption only if `phi0` is treated as an external
observed boundary rather than a shared interface.

## 383. Calderon projector gap status

Implemented in `native_calderon_projector_gap_status.py`.

Current projector ingredients:

```text
boundary value projector:
    supplied by metric:
        phi0 definition f=1
    current status:
        filled

momentum-jump projector:
    supplied by metric:
        C1 boundary momentum Delta Pi/R=q/2
    current status:
        filled after q is selected/banked

H1 angular projector:
    supplied by metric:
        round S2 ell=1 subspace
    current status:
        filled after H1 selection

trace measure:
    supplied by metric:
        induced S2 measure, Tr P_H1=3
    current status:
        filled

internal gluing contraction:
    supplied by metric:
        opposite-orientation boundary symplectic form
    current status:
        filled if phi0 is the two-sided bridge

exact two-sided Calderon projector:
    supplied by metric:
        bulk extension problem on both phi sides
    current status:
        not yet constructed

transfer-action branch:
    supplied by metric:
        intrinsic boundary action or warped on-shell DtN
    current status:
        still a fork
```

Three-hundred-sixty-eighth verdict:

```text
Most projector ingredients are now visible.
```

The remaining nontrivial construction is:

```text
the exact two-sided Calderon projector,
and the choice of intrinsic-boundary versus warped-DtN action inside it.
```

## 384. Interface versus warped double-count test

Implemented in `native_interface_vs_warped_double_count_test.py`.

Test matrix:

```text
data required:
    interface-local:
        uses only phi0 value, C1 momentum jump, H1 projector, induced S2 measure
    warped DtN:
        requires finite extension through the negative-phi collar
    implication:
        interface branch is boundary-local; warped branch is bulk-propagating

eta/2 origin:
    interface-local:
        uses projected finite-cell C1 action value once
    warped DtN:
        risks adding a second on-shell collar propagation factor on top of
        C1 action
    implication:
        warped branch must prove it replaces, not multiplies, the C1 side action

gluing:
    interface-local:
        internal phi0 label is contracted directly by boundary symplectic gluing
    warped DtN:
        gluing is through a bulk DtN extension operator
    implication:
        both are possible, but they describe different operations

profile sensitivity:
    interface-local:
        depends on q and induced boundary geometry at phi0
    warped DtN:
        depends on the full collar profile through Bessel ratio
    implication:
        if particle transfer is interface-local, profile memory is extra data

composition:
    interface-local:
        one-side action eta/2 composes to eta under symmetric gluing
    warped DtN:
        DtN composition uses bulk extension kernels and determinant/normalization data
    implication:
        simple gamma requires interface composition; warped propagation needs
        its own measure
```

Three-hundred-sixty-ninth verdict:

```text
The interface-local branch currently passes the gamma-transfer test with
fewer extra structures.
```

The warped-DtN branch remains valid for bulk collar propagation, but using
it in the transfer kernel must be:

```text
a replacement for the intrinsic side action,
not a multiplier.
```

## 385. Transfer branch decision table

Implemented in `native_transfer_branch_decision_table.py`.

Branch status:

```text
intrinsic interface:
    kernel:
        A_side = (eta/2) I3
    physical reading:
        local phi0 boundary transfer / internal interface label contraction
    accepted when:
        transfer is a boundary event at phi0 using value, momentum jump,
        H1 projector, and induced measure
    rejected when:
        a later derivation proves transfer is full bulk-collar propagation

warped bulk DtN:
    kernel:
        A_side = (eta/2) B I3 or a normalized D1 form
    physical reading:
        on-shell finite-collar propagation of angular boundary data
    accepted when:
        transfer is defined by eliminating the negative-phi collar bulk
    rejected when:
        used in addition to intrinsic interface action for the same H1 crossing

product of both:
    kernel:
        3 exp(-eta/2) times 3 exp(-eta B/2), or equivalent
    physical reading:
        two transfer kernels assigned to one H1 crossing
    accepted when:
        never without a proof of two independent physical events
    rejected when:
        default rejected as double counting
```

Three-hundred-seventieth verdict:

```text
Keep the intrinsic interface branch as the active transfer branch.
```

Keep warped DtN as:

```text
bulk-propagation alternative / correction branch.
```

Do not multiply them for the same H1 transfer event.

## 386. Plain-sight transfer branch update

Implemented in `native_plain_sight_transfer_branch_update.py`.

Updated gates:

```text
transfer action branch:
    previous status:
        intrinsic boundary versus warped DtN unresolved
    updated status:
        intrinsic interface is active branch;
        warped DtN is alternative bulk-propagation branch
    remaining gap:
        prove phi0 transfer is interface-local from the exact Calderon projector

double counting:
    previous status:
        guardrail only
    updated status:
        explicitly rejects multiplying intrinsic transfer by warped DtN
        for same H1 crossing
    remaining gap:
        identify any separate physical event before using both

gamma kernel:
    previous status:
        conditional P_transfer
    updated status:
        metric-composed first form gives gamma under internal phi0
        interface reading
    remaining gap:
        derive q selection and exact projector

warped DtN:
    previous status:
        competing transfer possibility
    updated status:
        retained as collar response / possible correction,
        not active gamma transfer
    remaining gap:
        derive when bulk propagation, rather than interface transfer,
        is the observed operation
```

Three-hundred-seventy-first verdict:

```text
The active lane is now intrinsic phi0 interface transfer.
```

Warped DtN remains real metric mathematics, but it is parked as bulk collar
response unless the exact projector selects bulk propagation as the observed
transfer operation.

## 387. H1 projector admissibility spectrum

Implemented in `native_h1_projector_admissibility_spectrum.py`.

Use the endpoint equation:

```text
p(1-p)/2 = eta ell(ell+1)
eta = 1/18
```

Real endpoint powers require:

```text
1 - 8 eta ell(ell+1) >= 0
ell(ell+1) <= 1/(8 eta) = 9/4
```

Exact spectrum:

```text
ell  lambda  discriminant  roots        finite nontrivial?
0    0       1             0, 1         no
1    2       1/9           1/3, 2/3     yes
2    6       -5/3          none         no
3    12      -13/3         none         no
4    20      -71/9         none         no
5    30      -37/3         none         no
```

Finite C1 endpoint action requires:

```text
p < 1/2
```

so for `ell=1`, the admissible nontrivial root is:

```text
p = 1/3.
```

Three-hundred-seventy-second verdict:

```text
ell=1 gives the only nontrivial finite angular endpoint sector at eta=1/18.
```

Therefore:

```text
P_adm,nontrivial = P_H1.
```

## 388. phi0 projector selection chain

Implemented in `native_phi0_projector_selection_chain.py`.

Selection chain:

```text
phi0 value surface:
    metric input:
        f(phi0)=1
    selection result:
        scalar boundary value is fixed, not a transfer label
    status:
        exact

C1 momentum jump:
    metric input:
        Delta Pi/R=q/2
    selection result:
        sets eta=q/6 after H1/S2 projection
    status:
        exact once q is selected/banked

endpoint admissibility:
    metric input:
        p(1-p)/2=eta ell(ell+1),
        finite C1 requires p<1/2
    selection result:
        at eta=1/18, ell=0 is trivial,
        ell=1 is only nontrivial finite,
        ell>=2 rejected
    status:
        exact after eta

boundary angular projector:
    metric input:
        round S2 harmonic decomposition
    selection result:
        P_adm,nontrivial = P_ell=1 = P_H1
    status:
        derived after previous filters

boundary measure:
    metric input:
        induced round S2 measure
    selection result:
        Tr P_H1=3
    status:
        exact
```

Three-hundred-seventy-third verdict:

```text
Once q/eta is supplied, H1 is not merely the first useful sector.
```

It is the only nontrivial finite angular endpoint sector that survives
the `phi0` boundary/admissibility filters.

## 389. H1 selection gate update

Implemented in `native_h1_selection_gate_update.py`.

Updated gate status:

```text
H1 transfer-space selection:
    previous status:
        strongly supported by ell=0 exclusion and lowest nonconstant sector
    updated status:
        derived conditional on eta=1/18:
        H1 is the only nontrivial finite endpoint sector
    remaining gap:
        derive q=1/3/eta or keep it banked

ell=0:
    previous status:
        background/scalar by interpretation
    updated status:
        exactly trivial finite branch p=0 under endpoint equation
    remaining gap:
        none for nontrivial matter transfer

ell>=2:
    previous status:
        higher shape blocks parked
    updated status:
        no real endpoint powers at eta=1/18
    remaining gap:
        could re-enter only as corrections if eta/rule changes

P_H1 in Cauchy projector:
    previous status:
        first-form projector ingredient after H1 selection
    updated status:
        admissible nontrivial angular projector after endpoint filter
    remaining gap:
        exact full Calderon projector still not constructed
```

Three-hundred-seventy-fourth verdict:

```text
H1 selection is no longer a free transfer-space ansatz once eta=1/18
is accepted.
```

The remaining upstream gate is:

```text
q/eta selection.
```

## 390. q/eta compatibility gate

Implemented in `native_q_eta_compatibility_gate.py`.

Metric inputs:

```text
eta = q/6
```

from C1 boundary momentum plus H1/S2 projection, and

```text
p(1-p)/2 = eta ell(ell+1)
```

for endpoint angular powers. On H1, `ell=1`, so:

```text
p(1-p)/2 = 2 eta = q/3.
```

The H1-only admissibility window as a function of `q` is:

```text
ell=1 real:       1 - (8/3)q >= 0  -> q <= 3/8
ell=2 rejected:   1 - 8q < 0       -> q > 1/8

nontrivial H1-only window:
    1/8 < q <= 3/8
```

So H1 admissibility alone does not select `q=1/3`. It only makes
`q=1/3` legal and excludes higher ordinary angular endpoint sectors.

The sharper result comes from compatibility.

First compatibility:

```text
self-similar endpoint Cauchy datum:
    p = q

H1 endpoint equation:
    q(1-q)/2 = q/3

branches:
    q = 0
    q = 1/3
```

Second compatibility:

```text
H1 projected C1 action:
    A_H1(q) = q^2/[12(1-2q)]

side action:
    eta/2 = q/12

action compatibility:
    q^2/[12(1-2q)] = q/12

branches:
    q = 0
    q = 1/3
```

At the nontrivial branch:

```text
q = 1/3
eta = 1/18
H1 endpoint roots = 1/3, 2/3
finite C1 root = p = 1/3
A_H1(q) = 1/36
eta/2 = 1/36
```

Three-hundred-seventy-fifth verdict:

```text
q=1/3 is the unique nontrivial common branch of:

1. C1 momentum plus H1/S2 projection,
2. H1 endpoint self-similarity p=q,
3. projected C1 side-action compatibility.
```

This is stronger than a fit and stronger than a free postulate. It is a
conditional compatibility theorem.

Remaining caveat:

```text
derive the exact phi0 Cauchy/Calderon projector rule that identifies
endpoint exponent, collar slope, and projected C1 side action as one
self-similar boundary datum.
```

If that projector identification is derived, then `q=1/3`,
`eta=1/18`, and `P_H1` are forced together. Until then, `q=1/3` should
be treated as a tightly constrained metric-native ansatz, not an
unconditional theorem.

## 391. Remaining postulates after q/eta gate

Implemented in `native_remaining_postulates_after_q_eta_gate.py`.

No longer free if the projector-identification condition is accepted:

```text
H1 selection:
    reason:
        only nontrivial finite endpoint sector at eta=1/18

eta=1/18:
    reason:
        eta=q/6 and q=1/3 under the compatibility gate

side value eta/2:
    reason:
        projected C1 action equals eta/2 at q=1/3
```

Still open / banked:

```text
P_projector_identification:
    exact phi0 Calderon projector must identify p, q, and C1 side action
    as one self-similar Cauchy datum

P_internal_trace:
    exact projector must show the H1 label is internal/unobserved
    so the boundary operation is Tr_H1

P_typed_depth:
    independent typed boundary slots must be derived before using
    depth = 3 + 2s

P_branch_coefficients:
    metric Hessian/Schur reductions must produce M1/E1 branch coefficients

electron mass anchor:
    one external dimensionful calibration
```

Three-hundred-seventy-sixth verdict:

```text
The active mathematical postulate is no longer q=1/3 itself.
```

The active upstream assumption is now:

```text
the exact phi0 projector identifies endpoint exponent, collar slope,
and projected C1 side action as one self-similar Cauchy datum.
```

That is a much narrower target than importing a mass mechanism or an
arbitrary coupling.

## 392. Positional-dilation Calderon refactor

Implemented in `native_positional_dilation_calderon_refactor.py`.

Use the GR/PDE Calderon object only as mathematical machinery:

```text
Calderon projector =
    projection onto Cauchy data that are traces of valid bulk solutions.
```

Now refactor the Cauchy data through the UDT positional-dilation metric.
On a spatial slice:

```text
dl^2 = f^-1 dr^2 + r^2 dOmega^2
d/d rho = sqrt(f) d/dr
```

At `phi0`:

```text
f = 1
d/d rho = d/dr
```

The scale-normalized Cauchy eigenvalue is therefore:

```text
kappa[u] = -R (d u/d rho) / u

at phi0:
    kappa[u] = -R u'(R)/u(R)
```

For a homogeneous collar trace:

```text
u = (R/r)^p
kappa[u] = p
```

For the C1 collar field:

```text
q = -R f'(R)/f(R)
f(R) = 1
kappa[f] = q
```

The one-mode Calderon graph projector has the block form:

```text
P_kappa(u,m) = (u, kappa u)

matrix:
    P_kappa = [1 0; kappa 0]

idempotence:
    P_kappa^2 = P_kappa
```

This gives the exact transformed-projector interpretation of the old
`p=q` assumption:

```text
If phi0 is one shared self-similar Cauchy graph, then the angular
endpoint exponent p and the C1 collar slope q are the same graph
eigenvalue.

Therefore:
    p = q
```

Then H1 compatibility gives:

```text
p(1-p)/2 = eta * 2
eta = q/6
p = q

q(1-q)/2 = q/3

branches:
    q = 0
    q = 1/3
```

Nontrivial branch:

```text
q = 1/3
eta = 1/18
side action eta/2 = 1/36
```

Three-hundred-seventy-seventh verdict:

```text
The GR Calderon machinery, after positional-dilation refactor,
does not import mass emergence.
```

It identifies the exact native proof target:

```text
prove that phi0 is a single self-similar Cauchy graph.
```

If true, `p=q` is not an extra postulate. It is the graph identity of the
transformed Calderon projector.

Remaining hard proof:

```text
exclude, or explicitly derive, a non-self-similar phi0 boundary layer
with independent p and q.
```

So the current status is:

```text
q=1/3 is forced by the transformed Calderon graph only if the phi0
projector has one self-similar Cauchy eigenvalue.
```

The next mathematical target is no longer vague. It is the uniqueness of
the `phi0` Cauchy graph under the UDT positional-dilation boundary
operator.

## 393. phi0 Cauchy graph uniqueness gate

Implemented in `native_phi0_cauchy_graph_uniqueness_gate.py`.

The refactored Calderon problem has two exact alternatives.

Alternative A:

```text
single self-similar Cauchy graph
```

Meaning:

```text
angular endpoint eigenvalue p
C1 collar eigenvalue q

are the same graph eigenvalue.
```

Condition:

```text
p = q
```

Then H1 with `eta=q/6` gives:

```text
q(1-q)/2 = q/3

branches:
    q = 0
    q = 1/3
```

The nontrivial result is:

```text
q = 1/3
eta = 1/18
P_adm = P_H1
```

Alternative B:

```text
split boundary-layer graph
```

Meaning:

```text
angular endpoint eigenvalue p
C1 collar eigenvalue q

are independent boundary-layer data.
```

Then the H1 endpoint equation is only:

```text
p(1-p)/2 = q/3
```

and H1-only admissibility gives:

```text
1/8 < q <= 3/8
```

So:

```text
q is not selected by this gate.
```

Three-hundred-seventy-eighth verdict:

```text
The Calderon proof is now a uniqueness problem.
```

What would count as proof:

```text
1. a derived two-sided Calderon projector with one graph eigenvalue;
2. a boundary/joint term whose stationarity enforces p=q; or
3. a no-extra-scale theorem excluding independent boundary-layer data.
```

If one of those is derived from the UDT positional-dilation boundary
operator, then the chain closes:

```text
single graph -> p=q -> q=1/3 -> eta=1/18 -> H1 projector.
```

If not, the result remains:

```text
a strong compatibility theorem plus a narrowed postulate.
```

## 394. delta_h exclusion audit

Implemented in `native_delta_h_exclusion_audit.py`.

Write a general finite-cell collar as:

```text
f(r) = (R/r)^p h(r)
h(R) = 1
```

Then the `phi0` slope is:

```text
q = -d ln f / d ln r |R
  = p - d ln h / d ln r |R
  = p + delta_h
```

Therefore:

```text
p = q
```

if and only if:

```text
delta_h = 0.
```

Important correction:

```text
no-extra-scale alone does not prove delta_h = 0.
```

Counterexample:

```text
h(r) = exp[-a(r/R - 1)]
h(R) = 1
-d ln h / d ln r |R = a
q = p + a
```

This deformation uses only the dimensionless coordinate `r/R` and a
dimensionless amplitude `a`. It introduces no new length scale, but it
breaks `p=q`.

Example:

```text
p = 1/3
a = delta_h = 1/20
q = p + a = 23/60
```

So the proof cannot be:

```text
no new length scale -> p=q.
```

It must instead be:

```text
no independent boundary-layer shape direction h -> delta_h=0 -> p=q.
```

Three-hundred-seventy-ninth verdict:

```text
The Calderon uniqueness proof must remove the independent h direction
from phi0 Cauchy data, or show the native boundary variation kills it.
```

Viable exact routes:

```text
1. derive a one-graph Calderon projector whose Cauchy data contain no
   independent h direction;

2. derive a phi0 joint/boundary stationarity equation setting
   delta_h=0;

3. derive a constant H1 source law through the collar, making the
   finite-action branch globally self-similar.
```

This is a guard against overclaiming. The metric route remains promising,
but the next proof must exclude a shape degree of freedom, not merely an
extra scale.

## 395. delta_h variational status

Implemented in `native_delta_h_variational_status.py`.

The exact C1 radial action is:

```text
S_C1 = (1/4) integral r^2 f'^2 dr
```

Its variation is:

```text
delta S_C1 = bulk + [Pi_f delta f]
Pi_f = (1/2) r^2 f'
```

At `phi0`:

```text
f(R) = 1
```

Using:

```text
f(r) = (R/r)^p h(r)
h(R) = 1
q = p + delta_h
```

a variation of `delta_h` changes the boundary derivative, not the
boundary value:

```text
delta f(R) = 0
delta f'(R) != 0
```

Therefore the ordinary first-order C1 boundary term:

```text
[Pi_f delta f]
```

does not stationarize `delta_h` when `f(R)` is fixed.

So `delta_h=0` cannot be derived from:

```text
1. a plain Dirichlet phi0 value condition;
2. a boundary functional depending only on f(R).
```

It can only be derived by something that restricts Cauchy data, such as:

```text
1. bulk equation plus regularity/global endpoint condition;
2. derivative-dependent boundary/joint term involving f'(R)
   or extrinsic curvature;
3. Calderon projector restricting admissible Cauchy data to one graph;
4. native angular/collar source law that keeps h'(R)=0.
```

Three-hundred-eightieth verdict:

```text
The p=q proof must use a Cauchy-data restriction.
```

The already-known C1 momentum boundary variation supplies the right
linear momentum unit:

```text
-Pi_f/R = q/2
```

but by itself it does not remove an independent boundary-layer derivative
direction. The next serious target is therefore a derivative-sensitive
`phi0` joint/corner term or an exact one-graph Calderon projector.

## 396. Derivative-sensitive joint-term audit

Implemented in `native_derivative_joint_term_audit.py`.

Critical distinction:

```text
seeing the slope is not the same as varying derivative data.
```

Candidate status:

```text
C1 first-order boundary variation:
    sees slope:
        yes, through Pi_f = (1/2)R^2 f'
    varies derivative data:
        no, boundary term is Pi_f delta f
    can enforce delta_h=0:
        no
    status:
        supplies q/2 unit but not p=q

boundary functional B(f):
    sees slope:
        only if slope is inserted as a parameter
    varies derivative data:
        no
    can enforce delta_h=0:
        no
    status:
        can cancel momentum but cannot stationarize h'(R)

standard EH+GHY Dirichlet completion:
    sees slope:
        raw EH sees f', GHY cancels f' in the action value
    varies derivative data:
        no under Dirichlet metric data
    can enforce delta_h=0:
        no
    status:
        rejected as eta/q selector

Brown-York angular stress:
    sees slope:
        yes, angular stress unit is q/2 at f=1
    varies derivative data:
        not by itself; it is a response tensor
    can enforce delta_h=0:
        no
    status:
        good atlas diagnostic, not a UDT stationarity equation

Israel shell jump:
    sees slope:
        yes, trace-reversed angular jump has q/2
    varies derivative data:
        bookkeeping, not an action by itself
    can enforce delta_h=0:
        no
    status:
        exact interface accounting, not selection
```

The needed object has the form:

```text
B_joint = B(F, Q, angular data)

F = f(R)
Q = -R f'(R)/f(R)
```

Required stationarity conditions:

```text
value/momentum closure:
    partial B / partial F |F=1 = Q/2

graph uniqueness:
    partial B / partial Q enforces Q=p
```

Three-hundred-eighty-first verdict:

```text
The GR corpus points at the correct derivative-sensitive kind of object,
but the currently known GR candidates do not close p=q after
positional-dilation refactor.
```

The active target is now sharply one of:

```text
1. derive a UDT-native B(F,Q,H1);
2. derive an exact one-graph Calderon projector;
3. derive a global endpoint/constant-H1-source condition that removes h.
```

## 397. H1 source-law constructibility audit

Implemented in `native_h1_source_law_constructibility.py`.

Exact metric ingredients:

```text
spatial curvature fraction:
    status:
        exact metric geometry
    role:
        R3(phi0)/R2(phi0) = q

H1/S2 projection factor:
    status:
        exact after H1 selection
    role:
        one H1 share gives factor 1/3
```

The desired source law is:

```text
s(q) = q/3
```

If native, the exact q-flow becomes:

```text
dq/dt = q^2 - q + 2q/3
      = q(q - 1/3)
```

Fixed branches:

```text
q = 0
q = 1/3
```

At the nontrivial branch:

```text
q = 1/3
s(q) = 1/9
dq/dt = 0
delta_h = 0
```

Then the constant-H1 source result applies:

```text
finite C1 action keeps the q=1/3 branch
the q=2/3 companion is rejected
p=q=1/3
eta=1/18
```

Three-hundred-eighty-second verdict:

```text
The metric supplies q and the H1 projection factor separately.
```

But:

```text
s(q)=q/3 is derived only if the UDT boundary/collar variational principle
forms their product as the active H1 source.
```

Until that product rule is derived, `s(q)=q/3` is the cleanest narrowed
postulate, not a completed derivation.

This is the orchestra metaphor in precise form:

```text
curvature share q
H1 projection 1/3
finite-action endpoint filtering
C1 q-flow

must act as one coupled metric composition.
```

If they do, `q=1/3` is forced. If they remain separate diagnostics, the
proof is still open.

## 398. phi0 metric identity ponder

Implemented in `native_phi0_metric_identity_ponder.py`.

Stand-back classification:

```text
neutral fixed surface:
    metric statement:
        phi=0 gives f=exp(-2phi)=1
    consequence:
        radial/time dilation is reset to the flat normalization at the interface
    proof status:
        exact

phi-sign bridge:
    metric statement:
        positive and negative phi branches meet at the same f=1 surface
    consequence:
        phi0 is the natural crossing surface between exterior/scalar
        and negative-phi data
    proof status:
        exact as geometry; physical gluing still must be specified

angular invariant carrier:
    metric statement:
        g_AB=r^2 omega_AB is phi-blind and -r^2 Delta_S2 is phi-sign invariant
    consequence:
        angular labels can pass through phi0 without radial-dilation ambiguity
    proof status:
        exact

first-jet detector:
    metric statement:
        at f=1, value data are trivial but f' can remain nonzero
    consequence:
        nontrivial phi0 data live in the Cauchy momentum /
        extrinsic-curvature jump
    proof status:
        exact

internal gluing surface:
    metric statement:
        two-sided negative/positive phi continuation shares the same boundary S2
    consequence:
        if both sides are part of one object, H1 labels are contracted,
        giving a trace
    proof status:
        conditional on treating phi0 as an internal bridge,
        not an external wall

single Cauchy graph:
    metric statement:
        not forced by f=1 alone
    consequence:
        would identify p=q and close q=1/3
    proof status:
        open; requires exclusion of independent boundary-layer h
```

Three-hundred-eighty-third verdict:

```text
The metric presents phi0 as a neutral first-jet bridge.
```

Meaning:

```text
value data are fixed by f=1;
angular data are invariant across phi sign;
nontrivial radial data are carried only by the first jet.
```

Implication:

```text
Do not treat phi0 primarily as a wall that creates q.
```

Treat it as:

```text
a Cauchy-data filter that decides which first jets are admissible
at the neutral bridge.
```

Sharp remaining question:

```text
Does the neutral bridge admit an independent boundary-layer h,
or does first-jet admissibility collapse the data to one graph?
```

This reframes the next step. The target is not another local q
manipulation. The target is the admissible first-jet space of the UDT
neutral bridge.

## 399. First-jet source inventory

Implemented in `native_first_jet_source_inventory.py`.

The exact collar q-flow is:

```text
dq/dt = q^2 - q + 2s(t)
```

and the collar factorization is:

```text
f(r) = (R/r)^p h(r)
q_phi0 = p + delta_h
```

Therefore an independent `h` direction is not free. It is equivalent to
nonzero integrated q-flow:

```text
delta_h = integral [q^2 - q + 2s(t)] dt
```

Source inventory:

```text
no angular source:
    source content:
        s(t)=0
    q behavior:
        q=0 is the regular/nontrivial-free branch
    verdict:
        scalar background, not mass-cell endpoint

constant H1 collar source:
    source content:
        s(t)=1/9
    q behavior:
        q=1/3 fixed branch;
        q=2/3 companion rejected by finite C1 action
    verdict:
        single graph, delta_h=0

self-coupled H1 source:
    source content:
        s(q)=q/3
    q behavior:
        fixed branches q=0 and q=1/3;
        on nontrivial branch s=1/9
    verdict:
        single graph if the product rule is native

running collar source:
    source content:
        s(t) arbitrary or branch-dependent
    q behavior:
        q runs; endpoint exponent p and phi0 slope q can split
    verdict:
        split graph / independent h direction
```

At the nontrivial fixed branch:

```text
q = 1/3
s = q(1-q)/2 = 1/9
eta = q/6 = 1/18
```

Three-hundred-eighty-fourth verdict:

```text
The neutral bridge does not need a rule forbidding arbitrary h.
```

It needs:

```text
a metric source inventory.
```

If the elementary bridge contains only the invariant H1 source and no
running collar source, the first jet collapses to:

```text
q=p=1/3
```

If the metric supplies running source content, then:

```text
p and q may split.
```

This is the best stand-back reframing so far. The next proof target is:

```text
derive the source inventory of the elementary phi0 bridge.
```

That is more native than inventing a wall condition and more precise than
chasing q algebra.

## 400. phi0 asymptotic-infinity reading

Implemented in `native_phi0_asymptotic_infinity_reading.py`.

Correction / refinement:

```text
phi0 means phi=0, equivalently f=e^{-2phi}=1.
```

In an asymptotically flat Schwarzschild-type exterior:

```text
f -> 1
phi = -1/2 ln f -> 0
```

at spatial infinity.

So:

```text
phi0 is infinity/normalization-like, not horizon-like.
```

A Schwarzschild horizon is:

```text
f = 0,
```

not:

```text
f = 1.
```

For the negative-phi / negative-mass type branch:

```text
f = 1 + a/r,  a>0
phi < 0
phi -> 0 as r -> infinity
```

so the negative-phi well also approaches `phi0` as its asymptotic
normalization.

Therefore a finite matter cell with:

```text
f=1 at phi0
```

is best read as:

```text
an internalized asymptotic boundary for the negative-phi cell.
```

Consequences:

```text
value data:
    f=1 is flat/asymptotic normalization

first-jet data:
    f' or q carries tail/ADM-like Cauchy information

flat exterior:
    requires exterior tail cancellation

interior bridge:
    can preserve a nonzero interior first jet as an interface jump

angular boundary:
    S2 measure and normalized angular spectrum survive exactly
```

Three-hundred-eighty-fifth verdict:

```text
phi0 is doing infinity-boundary work inside the finite-cell problem.
```

This explains why the GR/PDE boundary-at-infinity corpus keeps pointing
to useful machinery:

```text
ADM/tail constants,
Brown-York boundary stress,
Calderon/Cauchy projectors,
boundary traces over S2 harmonics.
```

But the UDT-specific rule is sharper:

```text
the internalized infinity must cancel the exterior tail while preserving
the interior first jet.
```

That is likely the missing boundary operation behind:

```text
P_value(f=1)
P_jump(Delta Pi=q/2)
P_H1
```

So the next target becomes:

```text
derive the internalized-asymptotic phi0 gluing rule.
```

This is a better phrase than "wall" or "shell" for the current object.

## 401. Phi-realm ontology bridge

Implemented in `native_phi_realm_ontology_bridge.py`.

Working ontology:

```text
negative phi realm:
    metric role:
        matter-side existence region;
        finite-action negative-phi cells live here
    bridge requirement:
        must remain accessible through phi0 rather than becoming a
        disconnected sheet

positive phi realm:
    metric role:
        scalar/background support on which matter is externally /
        macroscopically accessible
    bridge requirement:
        must receive matter information without importing the negative-phi
        radial scale

phi=0 surface:
    metric role:
        asymptotic-normalization / neutral bridge where f=1
    bridge requirement:
        must cancel exterior tail while preserving admissible interior
        first jet

scale-invariant angular sector:
    metric role:
        common S2 spectrum with normalized operator -r^2 Delta_S2
    bridge requirement:
        carries labels across phi sign and scale changes
```

Exact bridge facts:

```text
g_AB = r^2 omega_AB is phi-blind
-r^2 Delta_S2 has eigenvalues ell(ell+1), independent of r scale
L1 = (-r^2 Delta_S2)/2 equals I3 on ell=1
phi=0 gives f=1, the common normalization surface
```

Three-hundred-eighty-sixth verdict:

```text
Matter belongs to negative phi.
Positive phi is the scalar/macroscopic support realm.
The scale-invariant angular sector is the native bridge that lets
negative-phi matter be present in the macro-accessible realm.
```

Proof implication:

```text
The source inventory of the elementary phi0 bridge should be built from
angular invariants and first-jet matching, not from a radial mechanism
imported from either side alone.
```

This keeps the bridge role metric-native:

```text
negative phi supplies matter-side first-jet data;
positive phi supplies macro/scalar accessibility;
angular invariants supply the cross-realm carrier.
```

## 402. Angular bridge coupling modes

Implemented in `native_angular_bridge_coupling_modes.py`.

The bridge may not be a single simple operation. It may compose several
metric-native roles of the angular sector.

Candidate modes:

```text
binding-to-both-realms:
    metric reading:
        an angular component has support on both phi<0 matter data and
        phi>0 scalar/background data
    would explain:
        why negative-phi matter remains macro-accessible instead of
        becoming a disconnected sheet
    proof test:
        derive a two-sided boundary action whose angular variable is
        shared across the phi=0 bridge
    risk:
        can sound like an imported force unless kept as boundary/gluing support

resonance:
    metric reading:
        the same scale-invariant angular eigenvalue is admissible on both
        sides and at the finite-action endpoint
    would explain:
        why H1/ell=1, p=1/3, and eta=1/18 keep appearing together
    proof test:
        show the angular eigenvalue, endpoint exponent, and first-jet
        slope are one admissible Cauchy graph
    risk:
        resonance language can hide the still-open graph uniqueness proof

interference / cancellation:
    metric reading:
        two-sided bridge data cancel exterior radial tail while preserving
        the interior angular first-jet imprint
    would explain:
        how matter can be present in the macro realm without leaking a
        negative-phi radial tail
    proof test:
        derive a gluing condition where radial tail terms cancel and
        H1-projected first-jet data survive
    risk:
        highest fitting risk unless the cancellation follows from a
        symplectic/gluing identity
```

Exact common substrate:

```text
g_AB = r^2 omega_AB is shared across phi signs
-r^2 Delta_S2 is scale-invariant
phi=0 is the internalized asymptotic normalization surface
first-jet data q/2 can be projected through H1
```

Three-hundred-eighty-seventh verdict:

```text
The likely missing fact is how the already-visible angular bridge data
are used by the phi=0 gluing.
```

The observed metric behavior may be a composition of:

```text
shared support,
endpoint resonance / admissibility,
radial-tail interference or cancellation.
```

Next test:

```text
Search for a two-sided phi=0 gluing identity where the radial tail
cancels but the scale-invariant H1 first-jet imprint survives.
```

This is the current best concrete form of the "glue" idea as a metric
gluing question, without importing Standard Model gluon dynamics.

## 403. Tail-cancel / H1-survive gluing identity

Implemented in `native_tail_cancel_h1_survive_gluing.py`.

Source-free radial C1 identity:

```text
(r^2 f')' = 0
f = A + B/r
Pi_f = (1/2)r^2 f' = -B/2
```

Exterior flatness requires:

```text
B_out = 0
Pi_out = 0
```

so:

```text
exterior radial tail cancels.
```

Interior first jet at `phi=0`:

```text
f(R)=1
q = -R f'_in/f(R)
Pi_in = -qR/2
```

Two-sided gluing with an interface source gives:

```text
Pi_out - Pi_in = Delta Pi
Delta Pi = qR/2
```

Therefore:

```text
the exterior tail can be zero while the interior first jet survives
as a localized interface momentum jump.
```

At the nontrivial H1-compatible branch:

```text
q = 1/3
Delta Pi/R = 1/6
H1 projection eta = (Delta Pi/R)/3 = 1/18
one-side bridge action = eta/2 = 1/36
```

H1 survival condition:

```text
The radial tail is scalar/monopole data and is killed outside.
The surviving imprint is the H1-projected interface jump:

    P_H1(Delta Pi/R) = eta I3
```

Three-hundred-eighty-eighth verdict:

```text
The desired operation is not smooth matching.
```

It is:

```text
internalized-asymptotic gluing:
    value f=1 is shared;
    exterior tail B_out is zero;
    interior first jet q survives as Delta Pi;
    H1 projection carries the macro-accessible imprint.
```

This resolves one piece of the glue puzzle:

```text
radial tail cancellation and angular first-jet survival are compatible.
```

Remaining proof:

```text
derive why the elementary bridge selects q=1/3 / H1 rather than merely
allowing an arbitrary interface jump.
```

## 404. Metric-only bridge imprint audit

Implemented in `native_bridge_imprint_selection_filter.py`.

Metric facts already in hand:

```text
1. exterior scalar/radial tail cancellation is B_out=0;
2. a nonzero interior first jet appears as Delta Pi;
3. normalized angular data are scale-invariant at phi=0.
```

Angular decomposition at `phi=0`:

```text
ell=0:
    scalar/background channel

ell=1:
    first nonconstant angular channel H1

ell>=2:
    higher angular shape channels
```

Observed consequence 1:

```text
The ell=0 radial/scalar tail cannot be the macro-accessible imprint.
It is killed outside by B_out=0.
```

Observed consequence 2, conditional on `eta=1/18`:

```text
ell=0:
    discriminant = 1
    result = trivial finite branch only

ell=1:
    discriminant = 1/9
    result = nontrivial finite branch p=1/3

ell>=2:
    discriminant < 0
    result = no real endpoint powers
```

Therefore:

```text
Once eta=1/18 is supplied, H1 is the only nontrivial finite
scale-invariant angular imprint that can survive the bridge.
```

Three-hundred-eighty-ninth verdict:

```text
The metric kills scalar radial tail outside and preserves the first
nontrivial angular imprint at the bridge.
```

This is not a new mechanism. It is a channel audit from existing metric
facts.

What it proves:

```text
why the surviving imprint is H1, after eta/q is supplied.
```

What it does not prove:

```text
why q=1/3 is selected rather than an arbitrary interface jump.
```

So the remaining upstream selector is still:

```text
the elementary source inventory / q=1/3 rule.
```

## 405. phi=0 projection-intersection audit

Implemented in `native_phi0_projection_intersection_audit.py`.

Metric-given subconditions:

```text
1. Value normalization:
       f(phi=0) = 1

2. Exterior tail kernel:
       source-free exterior f_out = 1 + B_out/r
       flat macro/scalar exterior imposes B_out = 0
       since Pi_out = -B_out/2, this also gives Pi_out = 0

3. Interior first-jet image:
       q = -R f'_in/f(R)
       Pi_in = -qR/2
       Delta Pi = Pi_out - Pi_in = qR/2

4. Scale-invariant angular carrier:
       normalized angular data are decomposed by -R^2 Delta_S2
       H1 is ell=1, the first nonconstant sector
```

Projection-intersection form:

```text
admissible macro-visible imprint
    = ker(B_out)
      intersect image(Delta Pi)
      restricted to scale-invariant angular boundary data
```

If the upstream selector supplies:

```text
q = 1/3
```

then:

```text
Delta Pi/R = 1/6
H1 projection eta = 1/18
side value eta/2 = 1/36
```

Exact without selecting `q`:

```text
tail cancellation forces Pi_out=0;
any nonzero interior q survives only as an interface jump;
angular scale-invariant data are the only non-radial bridge labels.
```

Three-hundred-ninetieth verdict:

```text
The metric is exposing a projection intersection, not a force.
```

The intersection is:

```text
value normalization,
radial-tail kernel,
first-jet image,
angular scale-invariant restriction.
```

Remaining open:

```text
why the elementary bridge source inventory selects q=1/3
instead of an arbitrary Delta Pi/R=q/2.
```

## 406. Projection-intersection q-constraint audit

Implemented in `native_projection_intersection_q_constraint_audit.py`.

The projection intersection imposes:

```text
f = 1
B_out = 0 -> Pi_out = 0
Delta Pi/R = q/2
angular imprint must be scale-invariant
```

By itself, this allows any `q` with a corresponding interface jump:

```text
q = 1/6 -> Delta Pi/R = 1/12
q = 1/4 -> Delta Pi/R = 1/8
q = 1/3 -> Delta Pi/R = 1/6
q = 3/8 -> Delta Pi/R = 3/16
```

If:

```text
eta = q/6
```

and H1-only endpoint admissibility is imposed, then:

```text
ell=2 rejected requires q > 1/8
ell=1 real requires q <= 3/8
```

so:

```text
H1-only window: 1/8 < q <= 3/8
```

Therefore:

```text
projection intersection + H1-only admissibility narrows q to an interval,
not a point.
```

The point:

```text
q = 1/3
```

still requires an additional exact condition:

```text
1. p=q self-similar Cauchy graph;
2. s(q)=q/3 fixed source law; or
3. projected C1 side-action compatibility.
```

Three-hundred-ninety-first verdict:

```text
Tail cancellation and angular imprint survival are selection filters,
but not the q selector.
```

The selector remains:

```text
elementary source inventory / self-similar Cauchy graph condition.
```

## 407. q selector routes after projection

Implemented in `native_q_selector_routes_after_projection.py`.

The projection intersection has narrowed the problem but does not select
`q`. Exact routes that do select `q=1/3`:

```text
self-similar Cauchy graph:
    exact equation:
        p=q and p(1-p)/2=(q/6)*2 -> q=0 or q=1/3
    metric reading:
        phi=0 bridge admits one first-jet graph, not independent
        boundary-layer memory
    status:
        best Calderon/projector route;
        still must exclude running h

self-coupled H1 source inventory:
    exact equation:
        s(q)=q/3 and dq/dt=q^2-q+2s -> dq/dt=q(q-1/3)
    metric reading:
        curvature share q and H1 share 1/3 form the active collar source
    status:
        best source-inventory route;
        product rule not yet derived

projected C1 side-action compatibility:
    exact equation:
        q^2/[12(1-2q)] = q/12 -> q=0 or q=1/3
    metric reading:
        projected radial C1 action value equals the one-side bridge action
    status:
        strong value-action compatibility;
        needs physical rule selecting equality
```

Common nontrivial output:

```text
q = 1/3
Delta Pi/R = q/2 = 1/6
eta = q/6 = 1/18
eta/2 = 1/36
```

Metric-only priority after the bridge reframe:

```text
1. self-similar Cauchy graph / source inventory are primary because
   they speak directly to admissible first-jet data;

2. side-action compatibility is consilience unless the boundary action
   proves that equality is the stationarity condition.
```

Three-hundred-ninety-second verdict:

```text
q=1/3 has three exact metric-native convergence routes.
```

But:

```text
one of their premise rules must still be derived from the phi=0
internalized-asymptotic gluing.
```

## 408. Internalized-asymptotic source split

Implemented in `native_internalized_asymptotic_source_split.py`.

The source inventory must not conflate three distinct metric roles.

```text
interface delta source:
    metric location:
        localized at phi=0 internalized-asymptotic boundary
    exact job:
        sets Pi_out - Pi_in = Delta Pi,
        allowing B_out=0 while q_in survives
    q selection power:
        none by itself; accepts whatever q_in is supplied
    bridge reading:
        tail-cancel / first-jet-transfer object

collar density source:
    metric location:
        distributed through the negative-phi collar linking S2s
    exact job:
        enters dq/dt=q^2-q+2s(t),
        controlling whether q runs
    q selection power:
        can select q=1/3 if s=1/9 or s(q)=q/3 is native
    bridge reading:
        first-jet-admissibility / source-inventory object

angular boundary projector:
    metric location:
        scale-invariant S2 data at phi=0
    exact job:
        removes scalar tail as macro imprint and keeps admissible
        angular imprint
    q selection power:
        selects H1 after eta/q is supplied;
        does not select q alone
    bridge reading:
        macro-accessible angular carrier
```

Three-hundred-ninety-third verdict:

```text
The phi=0 interface source and the collar source are different metric
roles.
```

The first explains:

```text
tail cancellation and first-jet survival.
```

The second is where:

```text
q=1/3 must be selected if it is to be derived from the metric.
```

Next exact question:

```text
Does the scale-invariant angular sector live only at the phi=0
interface, or is it transported through the negative-phi collar
as a constant H1 source?
```

## 409. H1 transport versus collar source

Implemented in `native_h1_transport_vs_collar_source.py`.

Metric-only layers:

```text
kinematic H1 transport:
    exact metric fact:
        each linking S2 has g_AB=r^2 omega_AB and normalized operator
        -r^2 Delta_S2
    consequence:
        ell=1/H1 is identifiable at every radius in the collar
    limitation:
        identifiability is not yet a source term

constant angular eigenvalue:
    exact metric fact:
        -r^2 Delta_S2 Y_lm = ell(ell+1)Y_lm;
        for H1, lambda=2
    consequence:
        the H1 eigenvalue does not run through the collar
    limitation:
        a non-running eigenvalue does not by itself fix source normalization

collar source law:
    exact metric fact:
        radial q-flow would use dq/dt=q^2-q+2s(t)
    consequence:
        if H1 supplies s=1/9, q=1/3 is fixed and delta_h=0
    limitation:
        the map H1 transport -> s=1/9 remains unproved

boundary-only H1 projector:
    exact metric fact:
        at phi=0, H1 is the first nontrivial scale-invariant angular imprint
    consequence:
        explains macro-accessible imprint after eta/q is supplied
    limitation:
        does not control q-running inside the collar
```

Three-hundred-ninety-fourth verdict:

```text
H1 is transported kinematically through the collar because the normalized
angular spectrum is radius/phi invariant.
```

But:

```text
a kinematically transported H1 sector becomes a q-selecting collar source
only if the UDT action couples it into s(t).
```

Next proof target:

```text
derive or reject the map:

    transported H1 angular data -> constant collar source s=1/9
```

## 410. Angular Diophantine survivor audit

Implemented in `native_angular_diophantine_survivor_audit.py`.

The old canonical file contains a Diophantine angular triple, but that
triple was historically entangled with the Form-T/Dirac import. The useful
question is therefore not whether to restore the old mechanism. The useful
question is:

```text
which angular arithmetic survives after the non-native operator layer is
quarantined?
```

Metric-native angular dimensions on the linking two-spheres are:

```text
N_ell = 2ell + 1

ell=0: N=1, scalar/background, Lambda^3 count=0
ell=1: N=3, nonconstant angular, Lambda^3 count=1
ell=2: N=5, nonconstant angular, Lambda^3 count=10
ell=3: N=7, nonconstant angular, Lambda^3 count=35
ell=4: N=9, nonconstant angular, Lambda^3 count=84
```

Immediate survivor facts:

```text
ell=0 has N=1 and is the scalar/radial tail channel.
Tail cancellation kills that as the macro-visible matter imprint.
ell=1 has N=3 and is the first nonconstant angular channel.
N=3 is the first dimension with a unique Lambda^3 object.
N>3 has multiple Lambda^3 objects, not a unique triplet.
```

Legacy Diophantine identity, treated only as an angular-arithmetic atlas:

```text
(2j+1)^2(2ell+1)(2K+1) = C(2ell+2K+1, 2ell+1)
```

With the legacy `2j+1=2` input:

```text
ell=0: K hits=none
ell=1: K hits=3
ell=2: K hits=none
ell=3: K hits=none
ell=4: K hits=none
```

Four-hundredth verdict:

```text
The Form-T-specific parts of the old triple remain quarantined.
```

But:

```text
its angular arithmetic points to the same native S2 fact:
after scalar-tail cancellation, the first nonconstant angular bridge has
dimension N=3, and N=3 is uniquely epsilon-eligible.
```

This pins the angular `3` without importing spinors.

It does not yet prove `q=1/3`. It changes the missing step into a sharper
metric question:

```text
Does the phi=0 bridge use the transported angular dimension by the rule

    p = 1/N

so that N=3 gives p=1/3 and, on the one-graph C1 bridge, q=p=1/3?
```

Equivalent self-similar form:

```text
1 - 2p = p  ->  p = 1/3
```

Next proof target:

```text
derive or reject the metric rule connecting the surviving angular dimension
N=3 to the endpoint/first-jet exponent.
```

## 411. `N=3` to `p=q` bridge gate

Implemented in `native_n3_pq_bridge_gate.py`.

The current bridge should be treated as an orchestra gate, not as a single
invented mechanism.

Metric-visible pieces:

```text
scalar tail cancellation removes ell=0, N=1 as matter imprint
first nonconstant S2 angular carrier is ell=1, N=3
N=3 has Lambda^3 count=1
```

Angular inventory:

```text
ell=0: N=1, scalar tail, Lambda^3 count=0
ell=1: N=3, angular carrier, Lambda^3 count=1
ell=2: N=5, angular carrier, Lambda^3 count=10
ell=3: N=7, angular carrier, Lambda^3 count=35
ell=4: N=9, angular carrier, Lambda^3 count=84
```

Endpoint C1 self-similarity:

```text
finite action remainder exponent = 1 - 2p
self-similar endpoint condition: 1 - 2p = p
p = 1/3
```

Angular-dimension reading:

```text
if endpoint exponent is inverse surviving angular dimension,

    p = 1/N

then with N=3:

    p = 1/3
```

The important point is that this is no longer a lone fit. The two sides have
different metric origins:

```text
N=3:
    from scalar-tail cancellation plus first nonconstant S2 angular survival

p=1/3:
    from exact C1 endpoint/action self-similarity
```

Their agreement is:

```text
p = 1/N = 1/3
```

Now write a finite cell as:

```text
f(r) = (R/r)^p h(r)
h(R) = 1
```

The phi0 collar slope is:

```text
q_phi0 = p - d ln h/d ln r |R
       = p + delta_h
```

Therefore:

```text
q_phi0 = p  iff  delta_h = 0
```

If the one-graph/no-running bridge `delta_h=0` holds:

```text
q = 1/3
Delta Pi/R = q/2 = 1/6
eta = q/6 = 1/18
eta/2 = 1/36
s = q(1-q)/2 = 1/9
```

Four-hundred-first verdict:

```text
N=3 is now pinned by angular survival, not by a Dirac import.
p=1/3 is independently pinned by exact C1 endpoint self-similarity.
Their equality p=1/N is therefore an intersection of metric pieces.
```

The remaining nontrivial gate is:

```text
q_phi0 = p
```

equivalently:

```text
delta_h = 0.
```

If that gate is derived, then:

```text
q=1/3 follows without fitting.
```

Next proof target:

```text
derive or reject whether the phi0 boundary/collar problem forces the
one-graph condition delta_h=0.
```

## 412. General `N` source-filter audit

Implemented in `native_general_N_source_filter.py`.

Test the metric-product source law:

```text
s(q,N) = q/N
```

This is not asserted as derived in this section. It is the exact form obtained
if the active collar source is:

```text
radial curvature share q times angular projection share 1/N.
```

The q-flow is:

```text
dq/dt = q^2 - q + 2s
      = q^2 - q + 2q/N
      = q(q - (1 - 2/N))
```

The nonzero branch is therefore:

```text
q_N = 1 - 2/N = (N-2)/N
```

Now apply this exactly on the S2 angular ladder:

```text
ell=0, N=1:
    q_N=-1
    s=q/N=-1
    C1 action: not finite
    matter-cell status: excluded

ell=1, N=3:
    q_N=1/3
    s=q/N=1/9
    C1 action: finite
    matter-cell status: eligible

ell=2, N=5:
    q_N=3/5
    s=q/N=3/25
    C1 action: not finite
    matter-cell status: excluded

ell=3, N=7:
    q_N=5/7
    s=q/N=5/49
    C1 action: not finite
    matter-cell status: excluded

ell=4, N=9:
    q_N=7/9
    s=q/N=7/81
    C1 action: not finite
    matter-cell status: excluded
```

Four-hundred-second verdict:

```text
If s(q,N)=q/N is derived from the boundary/collar variation,
the metric-product law selects N=3 and q=1/3 together.
```

Then the `3` is not inserted. It is the only S2 angular dimension surviving all
three exact filters:

```text
1. scalar-tail cancellation excludes ell=0/N=1 as matter imprint;
2. S2 angular dimensions are N=2ell+1;
3. finite C1 action requires q_N < 1/2.
```

Since:

```text
q_N = (N-2)/N,
```

the finite-action condition gives:

```text
(N-2)/N < 1/2
```

so:

```text
N < 4.
```

On the non-scalar S2 ladder:

```text
N=3
```

is the only survivor.

This is the current sharpest version of the puzzle:

```text
derive or reject s(q,N)=q/N from the phi0 boundary/collar variation.
```

If accepted, it simultaneously supplies:

```text
N=3
q=1/3
s=1/9
Delta Pi/R=1/6
eta=1/18
eta/2=1/36
```

## 413. Projector-rank activation audit

Implemented in `native_projector_rank_activation_audit.py`.

The previous section makes a hidden assumption explicit.

A trace-normalized angular projector gives:

```text
normalized share = rank(P)/N = m/N
```

If the collar source is radial share times projected angular share:

```text
s(q,N,m) = q m/N
```

Then:

```text
dq/dt = q^2 - q + 2q m/N
      = q(q - (1 - 2m/N))
```

The nonzero branch is:

```text
q_(N,m) = 1 - 2m/N = (N - 2m)/N
```

Odd S2 dimensions with admissible projector ranks:

```text
ell=1, N=3:
    m=1: q=1/3, finite, rank-one law

ell=2, N=5:
    m=1: q=3/5, not finite, rank-one law
    m=2: q=1/5, finite, higher-rank law

ell=3, N=7:
    m=1: q=5/7, not finite, rank-one law
    m=2: q=3/7, finite, higher-rank law
    m=3: q=1/7, finite, higher-rank law

ell=4, N=9:
    m=1: q=7/9, not finite, rank-one law
    m=2: q=5/9, not finite, higher-rank law
    m=3: q=1/3, finite, higher-rank law
    m=4: q=1/9, finite, higher-rank law
```

Four-hundred-third verdict:

```text
s(q,N)=q/N is equivalent to a rank-one angular activation law.
```

It is not merely:

```text
some angular projection exists.
```

Rank-one consequence:

```text
m=1 gives q=(N-2)/N.
finite C1 action then allows only N=3 on the non-scalar S2 ladder.
```

Higher-rank warning:

```text
if m is freely selectable, additional finite branches appear.
```

For example:

```text
N=5, m=2 gives q=1/5.
```

Therefore the missing metric statement is sharper:

```text
the phi0 collar activates a canonical rank-one angular projector.
```

The `N=3` Lambda-three uniqueness is a candidate reason for that rank-one
activation, but arbitrary higher-rank activation must be excluded before this
becomes a proof.

Next exact target:

```text
derive or reject canonical rank-one angular activation from the scale-invariant
phi0/H1 projector.
```

## 414. SO(3) exterior-cube invariant audit

Implemented in `native_so3_exterior_cube_invariant_audit.py`.

For the real S2 harmonic space `H_ell`:

```text
dim H_ell = N = 2ell + 1
dim Lambda^3 H_ell = C(N,3)
```

A canonical scalar three-form appears as a spin-0 summand in:

```text
Lambda^3 H_ell.
```

Exact SO(3) exterior-cube decompositions:

```text
ell=1, N=3:
    Lambda^3 dimension=1
    SO(3) irreps=[0]
    spin-0 invariant count=1

ell=2, N=5:
    Lambda^3 dimension=10
    SO(3) irreps=[1, 3]
    spin-0 invariant count=0

ell=3, N=7:
    Lambda^3 dimension=35
    SO(3) irreps=[0, 2, 3, 4, 6]
    spin-0 invariant count=1

ell=4, N=9:
    Lambda^3 dimension=84
    SO(3) irreps=[1, 3, 3, 4, 5, 6, 7, 9]
    spin-0 invariant count=0

ell=5, N=11:
    Lambda^3 dimension=165
    SO(3) irreps=[0, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9, 10, 12]
    spin-0 invariant count=1
```

Four-hundred-fourth verdict:

```text
ell=1 has Lambda^3 H_1 = spin-0 exactly.
```

Higher odd `ell` spaces can contain a spin-0 summand, but it is embedded in a
larger exterior-cube multiplet. Therefore:

```text
only H1 supplies the scalar three-form without an additional projector choice.
```

This supports canonical rank-one activation for H1 without importing spinors or
a Dirac operator.

It also tightens the exclusion logic:

```text
higher odd ell sectors remain excluded unless a new metric projector is found.
```

Current rank-one source route:

```text
H1 supplies a canonical scalar Lambda^3 object;
rank-one activation gives s(q,N)=q/N;
for H1, N=3, so s(q)=q/3;
self-coupled q-flow then gives q=0 or q=1/3;
nontrivial finite branch gives q=1/3.
```

This is not yet a full variational proof, but the missing piece has narrowed
again:

```text
derive the collar source as trace-normalized action of the canonical H1
Lambda^3 scalar projector on the radial curvature-share q.
```

## 415. H1 area-form projector bridge

Implemented in `native_h1_area_form_projector_bridge.py`.

Use the `ell=1` coordinate harmonics on the unit two-sphere:

```text
n = (sin(theta)cos(phi), sin(theta)sin(phi), cos(theta)).
```

The round metric is recovered directly from the H1 embedding:

```text
d_theta n . d_theta n = 1
d_theta n . d_phi n   = 0
d_phi n . d_phi n     = sin(theta)^2
```

The canonical H1 epsilon identity is:

```text
eps_ijk n_i d_theta n_j d_phi n_k = sin(theta)
```

This is exactly the S2 area density.

So the H1 exterior-cube scalar is not merely a label-space invariant. It pulls
back to the actual angular measure of the collar:

```text
Lambda^3 H1  ->  dOmega_S2.
```

The isotropic H1 second moment is:

```text
<n_i n_j>_S2 = delta_ij / 3.
```

Therefore a scalar boundary/collar quantity `B` acting as `B I_3` on H1 has
per-label share:

```text
B/3.
```

For the collar radial datum:

```text
d ln f = -q d ln r.
```

The canonical transgression candidate is:

```text
d ln f wedge omega_H1 = -q d ln r wedge dOmega.
```

Trace-normalized through H1:

```text
normalized H1 share = q/3.
```

Four-hundred-fifth verdict:

```text
H1 supplies a canonical rank-one scalar angular carrier:

    Lambda^3 H1 -> S2 area form.
```

This justifies the angular `1/3` without choosing a projector by hand.

But there is a no-overclaim line:

```text
d ln f wedge omega_H1 is boundary/transgression-like.
```

By itself it supports:

```text
a Cauchy/interface action
```

more directly than:

```text
an ordinary bulk potential source.
```

This resolves part of the earlier action no-go tension. The failed scalar
potential tests were looking for a bulk `f` potential. The newly uncovered H1
object looks like a natural boundary/Cauchy carrier instead.

Updated proof target:

```text
derive whether the phi0 Calderon/Cauchy boundary action uses this H1
area-form carrier to impose the rank-one source share q/3.
```

## 416. H1 transgression boundary audit

Implemented in `native_h1_transgression_boundary_audit.py`.

Canonical H1 collar form:

```text
Xi_H1 = d ln f wedge omega_H1
```

Since `omega_H1` is the S2 area form and is closed on the collar:

```text
Xi_H1 = d(ln f omega_H1).
```

Therefore on:

```text
I x S2
```

the integral is:

```text
integral Xi_H1 = 4 pi [ln f]_{inner}^{phi0}.
```

At `phi0`:

```text
f(phi0)=1
ln f(phi0)=0
```

Four-hundred-sixth verdict:

```text
the pure H1 transgression is an endpoint/Cauchy object.
```

It does not create:

```text
an ordinary bulk Euler-Lagrange source.
```

It can carry:

```text
boundary Cauchy data and angular normalization.
```

If an independent Cauchy graph supplies:

```text
q = 1/3
```

then:

```text
C1 momentum scale q/2 = 1/6
H1 trace-normalized share q/6 = 1/18
```

But:

```text
the transgression alone does not select q.
```

Proof consequence:

```text
The H1 area-form result should be used to build the phi0 Calderon/Cauchy
boundary projector, not as a standalone bulk source derivation.
```

This resolves the tension with the earlier scalar-action no-go results:

```text
ordinary scalar potential route:
    rejected

H1 area-form/transgression route:
    boundary/Cauchy carrier, still viable
```

Remaining exact gate:

```text
show that the Cauchy projector graph has rank-one H1 scalar boundary data
and fixed slope q=1/3, or keep q=1/3 conditional.
```

## 417. H1 Cauchy graph merge gate

Implemented in `native_h1_cauchy_graph_merge_gate.py`.

Newly derived angular carrier:

```text
Lambda^3 H1 pulls back to the S2 area form.
```

Therefore:

```text
H1 supplies the canonical rank-one angular projector.
```

For H1:

```text
N = 3
lambda = 2
```

The Cauchy graph variable at `phi0` is:

```text
kappa[u] = -R u'(R)/u(R).
```

Use:

```text
p = endpoint/collar graph value for the angular profile
q = C1 collar graph value for f
```

The H1 projected boundary scale is:

```text
eta = (q/2)/N.
```

With `N=3`:

```text
eta = q/6.
```

Angular endpoint compatibility is:

```text
p(1-p)/2 = eta lambda.
```

Substitute:

```text
eta = (q/2)/N
lambda = 2
```

to get:

```text
p(1-p)/2 = q/N.
```

Alternative A:

```text
one self-similar Cauchy graph:
    p = q
```

Then:

```text
q(1-q)/2 = q/N
q = 0 or q = 1 - 2/N.
```

For H1:

```text
N=3
q=1/3
eta=1/18
eta/2=1/36
```

Alternative B:

```text
split boundary-layer graph:
    p and q are independent Cauchy eigenvalues.
```

Then:

```text
p(1-p)/2 = q/N
```

but:

```text
q is not selected without another boundary condition.
```

Four-hundred-seventh verdict:

```text
The H1 area-form result solves the angular-projector side.
```

It does not by itself prove:

```text
p=q.
```

The remaining proof is exactly the Calderon uniqueness problem:

```text
phi0 must admit one self-similar Cauchy graph for elementary mass emergence,
excluding an independent h/boundary-layer mode.
```

This is a stronger position than before. The old open gate contained both:

```text
1. why H1/rank-one/N=3?
2. why p=q?
```

The first is now substantially answered by:

```text
Lambda^3 H1 -> S2 area form.
```

The second remains open and precise.

## 418. Scalar `h`-mode exclusion gate

Implemented in `native_scalar_h_mode_exclusion_gate.py`.

Write the finite-cell interior as:

```text
f(r) = (R/r)^p h(r)
h(R) = 1.
```

Then the `phi0` slope is:

```text
q = -R f'(R)/f(R)
  = p - d ln h / d ln r |R
  = p + delta_h.
```

Exact interpretation:

```text
delta_h is the independent scalar radial boundary-layer Cauchy datum.
```

It is not part of:

```text
the H1 area-form carrier.
```

Elementary H1 bridge reading:

```text
scalar-tail cancellation removes the scalar/radial imprint channel.
Lambda^3 H1 supplies the angular area-form carrier.
```

If the elementary `phi0` projector admits only:

```text
1. value normalization f=1;
2. the canonical H1 area-form carrier;
```

then:

```text
delta_h = 0.
```

Thus:

```text
q = p.
```

With endpoint self-similarity:

```text
p = 1/3.
```

So:

```text
q = p = 1/3
Delta Pi/R = q/2 = 1/6
eta = q/6 = 1/18
eta/2 = 1/36
```

If `delta_h` is allowed:

```text
q = p + delta_h
```

and:

```text
the angular endpoint equation gives only a compatibility range;
q is not selected.
```

Four-hundred-eighth verdict:

```text
p=q is equivalent to excluding the scalar h boundary-layer mode.
```

The H1 area-form result gives a concrete reason to try this:

```text
the elementary bridge has a canonical angular carrier but no canonical
independent scalar h carrier.
```

This is the current best no-new-mechanism route to the one-graph Calderon
condition.

Remaining proof obligation:

```text
show that the phi0 elementary projector really quotients out or forbids
the scalar h boundary-layer mode, rather than merely hiding it from the
macro-visible tail.
```

## 419. `h`-mode source residual audit

Implemented in `native_h_mode_source_residual_audit.py`.

Use:

```text
t = ln r
q = -d ln f/dt.
```

The exact q-flow is:

```text
dq/dt = q^2 - q + 2s(t).
```

Therefore:

```text
s(t) = (q' - q^2 + q)/2.
```

For the self-similar H1 endpoint:

```text
p = 1/3
s0 = p(1-p)/2 = 1/9.
```

Write:

```text
q(t) = p + delta(t).
```

Then the exact source residual is:

```text
Delta s = s - s0
        = [delta' + delta(1-2p) - delta^2]/2.
```

For:

```text
p = 1/3
```

this becomes:

```text
Delta s = [delta' + delta/3 - delta^2]/2.
```

So:

```text
delta = 0  ->  Delta s = 0.
```

But:

```text
nonzero delta is not free.
```

It requires:

```text
1. an additional scalar source residual; or
2. an independent boundary-layer flow compatible with the same source.
```

If the collar source is exactly the canonical H1 area-form source with no
additional scalar source:

```text
s(t) = s0 = 1/9,
```

then:

```text
delta' = delta^2 - delta/3.
```

With endpoint boundary condition:

```text
delta(endpoint) = 0,
```

uniqueness of the first-order q-flow gives:

```text
delta(t) = 0
```

through the elementary collar.

For the old counterexample:

```text
h(r) = exp[-a(r/R - 1)]
a = delta_h = 1/20
```

the exact source residual at `phi0` is:

```text
Delta s(phi0) = 77/2400.
```

Four-hundred-ninth verdict:

```text
allowing h is equivalent to allowing an additional scalar source residual
or an independent boundary-layer flow.
```

Under the current H1 area-form framing:

```text
if the elementary bridge source inventory is exhausted by the canonical H1
area-form carrier, h is excluded and p=q.
```

This does not rely on the older no-extra-scale argument. It uses only:

```text
1. exact q-flow;
2. endpoint self-similar H1 source s0=1/9;
3. absence of an additional scalar source residual.
```

## 420. Post-H1 area-form rebaseline

Implemented in `native_post_h1_rebaseline.py`.

Do not use older audits as premises without re-deriving them under the current
facts.

Current fact set:

```text
1. phi0 value normalization:
   f(phi0)=1

2. exterior scalar-tail cancellation:
   B_out=0
   Pi_out=0

3. interior first-jet datum:
   q=-R f'(R)/f(R)
   Delta Pi/R=q/2

4. H1 area-form identity:
   Lambda^3 H1 pulls back to dOmega_S2
   H1 supplies the canonical rank-one angular carrier

5. H1 trace share:
   N=3
   eta=(q/2)/3=q/6

6. exact q-flow:
   dq/dt=q^2-q+2s(t)

7. h-mode meaning:
   q=p+delta_h
   nonzero delta_h requires a scalar source residual or split graph
```

Conditional elementary closure:

```text
If the elementary bridge has no additional scalar source residual beyond
the canonical H1 area-form carrier, then delta_h=0.
```

Then:

```text
q=p=1/3
s=q(1-q)/2=1/9
Delta Pi/R=1/6
eta=1/18
eta/2=1/36
```

Do not use as premises without re-deriving under current facts:

```text
old no-extra-scale arguments
old Dirac/Form-T spinor imports
old bulk-potential source attempts
old Standard Model analog labels
```

Four-hundred-tenth verdict:

```text
The post-H1 frame is stronger but narrower.
```

Stronger because:

```text
H1 is now tied to the actual S2 area form.
```

Narrower because:

```text
q=1/3 still requires absence of a scalar source residual/split graph.
```

Current live proof obligation:

```text
prove the elementary phi0 bridge source inventory has no scalar residual
beyond the H1 area-form carrier, or keep q=1/3 conditional.
```

## 421. Collar Hodge carrier audit

Implemented in `native_collar_hodge_carrier_audit.py`.

Topological collar:

```text
M = I x S2.
```

De Rham carrier inventory:

```text
H^0(M) = R
H^1(M) = 0
H^2(M) = R [omega_S2]
H^3(M) = 0  for the interval collar with boundary
```

Metric angular carrier:

```text
Lambda^3 H1 pulls back to omega_S2.
```

This is the unique harmonic/cohomological angular two-form carrier.

Radial transgression:

```text
d ln f wedge omega_S2 = d(ln f omega_S2).
```

It is exact on the collar and contributes through boundaries.

Split:

```text
ln f = p ln(R/r) + ln h
h(R)=1.
```

Then:

```text
d ln f wedge omega
  = -p d ln r wedge omega + d ln h wedge omega
  = d[p ln(R/r) omega] + d[ln h omega].
```

At `phi0`:

```text
ln h(R)=0.
```

So the `h` transgression has no `phi0` value contribution. Its effect is:

```text
a derivative/Cauchy residual,
```

not:

```text
a new harmonic angular carrier.
```

Four-hundred-eleventh verdict:

```text
Hodge inventory supports excluding h from the elementary carrier space,
because h is an exact scalar boundary residual.
```

But:

```text
it does not by itself prove the Calderon projector performs that quotient.
```

The remaining proof is now a boundary-domain statement:

```text
Does the elementary phi0 projector keep only value normalization plus the
H1 harmonic area-form carrier, quotienting exact scalar h residuals?
```

If yes:

```text
h is excluded
delta_h=0
q=p=1/3
```

## 422. Elementary `phi0` projector candidate

Implemented in `native_elementary_phi0_projector_candidate.py`.

Use the current post-H1 carrier basis:

```text
e0 = value normalization f(phi0)=1
e1 = self-similar endpoint/Cauchy exponent p
e2 = exact scalar boundary residual delta_h
e3 = H1 harmonic area-form carrier
```

Candidate elementary projector:

```text
keep e0
keep e1
kill e2
keep e3
```

Matrix form:

```text
P = [1, 0, 0, 0;
     0, 1, 0, 0;
     0, 0, 0, 0;
     0, 0, 0, 1]
```

It is idempotent:

```text
P^2 = P.
```

Under this projector:

```text
delta_h=0
q=p
eta=(q/2)/N
N=3 from H1 area-form carrier
```

H1 compatibility on the one graph gives:

```text
q(1-q)/2 = q/N
q=0 or q=1-2/N.
```

For:

```text
N=3
```

the nontrivial branch is:

```text
q=1/3
eta=1/18
eta/2=1/36
```

Four-hundred-twelfth verdict:

```text
This is an exact idempotent candidate for the elementary phi0 projector
after the H1 area-form discovery.
```

It is a proof only if the UDT boundary domain is shown to use this
harmonic-carrier quotient:

```text
keep:
    value normalization,
    self-similar Cauchy exponent,
    H1 harmonic area-form carrier;

kill:
    exact scalar h residual.
```

This is also the cleanest minimal postulate if a final derivation is not yet
available:

```text
P_elem quotients exact scalar boundary residuals and keeps the canonical H1
area-form carrier.
```

It is not a Standard Model import. It is a boundary-domain statement for the
UDT `phi0` projector.

## 423. Relative `h`-residual domain audit

Implemented in `native_relative_h_residual_domain_audit.py`.

Post-H1 carrier split on the collar:

```text
M = I x S2
```

Use:

```text
harmonic angular carrier: omega_H1 = dOmega_S2
scalar boundary residual: y = ln h
```

Boundary normalization at `phi0`:

```text
h(phi0)=1
y(phi0)=0.
```

So `h` has no value trace at `phi0`. It can enter `phi0` Cauchy data only
through:

```text
dy/dn at phi0
```

or equivalently:

```text
delta_h = -d ln h / d ln r |phi0.
```

Exact carrier classification:

```text
omega_H1 is the harmonic angular carrier.
d y wedge omega_H1 = d(y omega_H1) is exact.
```

Because:

```text
y(phi0)=0,
```

its `phi0` value trace vanishes.

Therefore:

```text
nonzero delta_h is a relative exact Cauchy residual.
```

If the elementary bridge source inventory is exhausted by H1:

```text
p=1/3
s0=p(1-p)/2=1/9
q=p+delta
delta' = delta^2 - delta/3.
```

With endpoint/self-similar boundary datum:

```text
delta=0
```

at one end, uniqueness of the first-order flow gives:

```text
delta=0
```

through the elementary collar.

If a relative exact scalar residual is admitted:

```text
delta_h may be nonzero
q=p+delta_h
```

and:

```text
the elementary branch is no longer selected by H1 alone.
```

Four-hundred-thirteenth verdict:

```text
The remaining question is not algebraic.
```

It is the boundary domain of the elementary `phi0` projector:

```text
harmonic angular carrier only:
    h killed
    q=p

harmonic carrier plus relative exact scalar residual:
    h allowed
    q remains conditional
```

Minimal current postulate, if needed:

```text
Elementary mass emergence uses the harmonic H1 carrier domain and quotients
relative exact scalar Cauchy residues.
```

This postulate is small and native:

```text
it selects a boundary domain;
it does not import a Standard Model mechanism;
it does not add a bulk force;
it matches the H1 area-form geometry already uncovered.
```

## 424. Harmonic domain projection audit

Implemented in `native_harmonic_domain_projection_audit.py`.

Hodge-Morrey style carrier split on:

```text
I x S2
```

is:

```text
harmonic carrier: omega_S2
exact residual:   d(y omega_S2)
y = ln h.
```

Boundary values:

```text
y(phi0)=0 because h(phi0)=1.
```

If the endpoint profile normalization absorbs `h` at the inner end, the
elementary residual also has:

```text
y(endpoint)=0.
```

Then:

```text
integral_{I x S2} d(y omega_S2)
  = 4 pi [y]_{endpoint}^{phi0}
  = 0.
```

So a two-boundary relative exact `h` residual carries:

```text
no harmonic/cohomological charge;
no phi0 value trace;
only derivative/Cauchy data.
```

A harmonic representative projector would therefore:

```text
keep omega_S2;
kill d(y omega_S2).
```

If the elementary `phi0` domain is this harmonic representative domain:

```text
delta_h=0
q=p=1/3
eta=q/6=1/18
```

If the domain is larger:

```text
exact relative h residuals are allowed;
q is not fixed by the H1 carrier alone.
```

Four-hundred-fourteenth verdict:

```text
The harmonic-domain projection is a natural current-facts candidate for the
elementary phi0 projector.
```

It is not:

```text
a bulk mechanism,
a Standard Model import,
or a fitted q value.
```

It is a boundary-domain statement:

```text
elementary mass emergence uses the harmonic representative domain rather
than the full relative Cauchy domain.
```

This is currently the cleanest form of the remaining postulate/derivation
target.

## 425. Relative residual spectrum audit

Implemented in `native_relative_residual_spectrum_audit.py`.

Let:

```text
y = ln h
```

be a scalar residual on a finite collar interval.

For the elementary normalization:

```text
y(endpoint)=0
y(phi0)=0.
```

The scalar relative/Dirichlet interval spectrum has modes:

```text
y_n(t) = sin(n pi t/L),  n=1,2,...
```

with eigenvalues:

```text
(n pi/L)^2 > 0.
```

Therefore:

```text
there is no nonzero scalar harmonic residual y with zero endpoint values.
```

By contrast:

```text
omega_H1 = dOmega_S2
```

is the harmonic angular carrier.

Elementary zero-carrier domain:

```text
keeps the harmonic H1 carrier;
kills positive relative scalar residual modes.
```

If elementary mass emergence is the zero/harmonic carrier sector:

```text
y=0
delta_h=0
q=p=1/3.
```

If positive relative scalar modes are admitted:

```text
h is an excitation or boundary-layer dressing;
q is branch/profile dependent.
```

Four-hundred-fifteenth verdict:

```text
h is not part of the elementary harmonic carrier space.
```

It can exist only as:

```text
a larger-domain relative scalar excitation.
```

This supports, but does not independently prove, the elementary `phi0`
projector that kills `h`.

Current interpretation:

```text
q=1/3 belongs to the elementary harmonic-carrier branch.
nonzero delta_h belongs to an enlarged relative-scalar boundary-layer branch.
```

## 426. Current proof stack after H1

Implemented in `native_current_proof_stack_after_h1.py`.

Derived/current facts:

```text
1. phi0 fixes value: f=1
2. exterior scalar tail is killed: B_out=0
3. interior first jet survives as Delta Pi/R=q/2
4. ell=0 is scalar/tail, not the angular matter carrier
5. first nonconstant S2 carrier is H1 with N=3
6. Lambda^3 H1 pulls back to dOmega_S2
7. H1 gives eta=(q/2)/3=q/6
8. exact q-flow is dq/dt=q^2-q+2s(t)
9. h residual means q=p+delta_h
10. nonzero delta_h is a scalar residual/split graph
```

Minimal boundary-domain assumption still open:

```text
elementary phi0 mass emergence uses the harmonic H1 carrier domain
and quotients relative exact scalar h residuals.
```

If that domain statement holds:

```text
delta_h=0
q=p=1/3
s=1/9
Delta Pi/R=1/6
eta=1/18
eta/2=1/36
```

If that domain statement fails:

```text
relative scalar h modes are admitted
q remains branch/profile dependent
q=1/3 is conditional, not derived
```

Four-hundred-sixteenth verdict:

```text
The route is not merely fitting now.
```

The metric has supplied:

```text
a coherent harmonic-carrier branch.
```

The remaining issue is:

```text
the boundary domain of elementary phi0 data.
```

This is the current high-level state:

```text
uncovered:
    H1 is the canonical harmonic angular carrier;
    scalar h is an exact relative residual;
    q=1/3 is the one-graph H1 harmonic branch.

not yet proven:
    elementary mass emergence must use only that harmonic carrier domain.
```

## 427. `eta/2` after harmonic closure

Implemented in `native_eta_half_after_harmonic_closure.py`.

Use only the current post-H1 facts:

```text
harmonic H1 carrier gives N=3;
elementary harmonic-domain closure gives delta_h=0;
endpoint self-similarity gives q=p=1/3.
```

For a self-similar finite cell:

```text
f(r)=(R/r)^q.
```

The radial C1 action is:

```text
S_C1/R = q^2/[4(1-2q)].
```

At:

```text
q=1/3
```

this gives:

```text
S_C1/R = 1/12.
```

Project through the H1 carrier dimension:

```text
N=3.
```

Then:

```text
H1 projected C1 action = (S_C1/R)/N
                        = (1/12)/3
                        = 1/36.
```

The H1 projected momentum unit is:

```text
eta = (q/2)/N
    = (1/6)/3
    = 1/18.
```

So:

```text
eta/2 = 1/36.
```

Exact identity:

```text
H1 projected C1 action = eta/2.
```

Equivalently, before setting `q`, demand:

```text
projected C1 action = eta/2.
```

That is:

```text
[q^2/(4(1-2q))]/N = [(q/2)/N]/2.
```

The `N` cancels:

```text
q^2/[4(1-2q)] = q/4.
```

For the nontrivial branch:

```text
q = 1/3.
```

Four-hundred-seventeenth verdict:

```text
eta/2 is not an extra postulate once the elementary harmonic closure
supplies q=1/3.
```

It is:

```text
the exact H1-projected on-shell C1 action value of the self-similar finite
cell.
```

Symmetric gluing can still explain:

```text
why two sides compose to eta.
```

But it is no longer needed to manufacture:

```text
1/36.
```

Updated postulate ledger:

```text
eta/2 transfer weight:
    no longer independent after q=1/3 harmonic closure;
    derived as projected on-shell C1 action value.
```

## 428. Endpoint self-similarity after H1 domain

Implemented in `native_endpoint_self_similarity_after_h1_domain.py`.

Use current facts:

```text
H1 area-form carrier gives N=3;
H1 eigenvalue lambda=2;
H1 projected boundary scale eta=(q/2)/N;
harmonic-domain projector kills h, so p=q.
```

Endpoint compatibility:

```text
p(1-p)/2 = eta lambda.
```

Substitute:

```text
eta=(q/2)/N
lambda=2.
```

Then:

```text
p(1-p)/2 = q/N.
```

One-graph condition:

```text
p=q.
```

For the nontrivial branch:

```text
p(1-p)/2 = p/N
(1-p)/2 = 1/N
p = 1 - 2/N.
```

With:

```text
N=3
```

this gives:

```text
p=1/3.
```

Consequences:

```text
q=p=1/3
finite-action remainder exponent 1-2p=1/3
endpoint profile exponent p=1/3
endpoint self-similarity 1-2p=p
eta=(q/2)/N=1/18
projected C1 action=1/36
eta/2=1/36
```

Four-hundred-eighteenth verdict:

```text
Endpoint self-similarity is not an independent postulate if the harmonic
H1 domain projector is accepted or derived.
```

It follows from:

```text
H1 endpoint compatibility plus the one-graph condition p=q.
```

If the harmonic-domain projector is not accepted, endpoint self-similarity can
remain a fallback closure principle.

Updated postulate ledger:

```text
endpoint self-similarity:
    no longer independent under harmonic-domain projector;
    becomes an output of the H1 one-graph branch.
```

## 429. `h`-residual energy identity

Implemented in `native_h_residual_energy_identity.py`.

Let:

```text
y = ln h
```

be the scalar relative residual on the collar interval.

Elementary relative boundary values:

```text
y(endpoint)=0
y(phi0)=0.
```

If `y` is source-free/harmonic on the elementary scalar residual sector, then:

```text
y''=0.
```

Energy identity:

```text
integral (y')^2 dt = [y y']_endpoint^phi0 - integral y y'' dt.
```

With:

```text
y=0 at both ends
y''=0
```

this gives:

```text
integral (y')^2 dt = 0.
```

Therefore:

```text
y'=0
y=constant
boundary values force y=0.
```

So:

```text
h=1
delta_h=0.
```

Then on the H1 one-graph branch:

```text
q=p=1/3
eta=1/18
eta/2=1/36.
```

If `y` is nonzero:

```text
it is not a source-free harmonic residual.
```

It must be:

```text
a positive relative scalar excitation
```

or be driven by:

```text
an additional scalar source/boundary-layer condition.
```

Four-hundred-nineteenth verdict:

```text
The elementary projector kills h if the scalar residual sector is
source-free and harmonic/zero-mode.
```

The remaining domain statement is:

```text
whether elementary mass emergence is precisely this source-free harmonic
carrier sector.
```

This is a partial proof of item 1 under a clear domain premise. It does not add
a new mechanism. It says:

```text
nonzero h cannot live in the elementary source-free harmonic sector.
```

## 430. Mixed Hodge domain theorem audit

Implemented in `native_mixed_hodge_domain_theorem_audit.py`.

Collar:

```text
M = I x S2
boundary = S2_endpoint union S2_phi0.
```

Angular H1 carrier:

```text
omega_H1 = dOmega_S2
boundary type: absolute/tangential angular carrier
harmonic representative: nonzero
carrier dimension: one scalar area-form from Lambda^3 H1
```

Scalar `h` residual:

```text
y = ln h
y(endpoint)=0
y(phi0)=0
boundary type: relative scalar residual
```

Relative harmonic zero-form test on the interval:

```text
Delta y = 0
y|boundary = 0.
```

By the maximum principle / energy identity:

```text
y=0.
```

Thus:

```text
absolute harmonic H1 area carrier survives;
relative harmonic scalar h residual vanishes.
```

Domain theorem candidate:

```text
Elementary phi0 data are mixed Hodge representatives:
    absolute harmonic angular carrier;
    no relative scalar residual zero-mode.
```

Consequences:

```text
h=1
delta_h=0
p=q
H1 one-graph branch gives q=1/3.
```

Four-hundred-twentieth verdict:

```text
This is close to a proof of the remaining domain premise if UDT's
elementary phi0 projector is identified with the mixed Hodge harmonic
representative projector on the collar.
```

The only remaining step is deriving that identification from the UDT boundary
variational problem.

Updated minimal premise:

```text
P_domain:
    the elementary phi0 projector is the mixed Hodge harmonic representative
    projector on I x S2.
```

Then:

```text
H1 survives by the absolute harmonic angular area form;
h is killed because relative harmonic zero-forms with zero boundary values
vanish.
```

## 431. Postulate ledger after mixed Hodge

Implemented in `native_postulate_ledger_after_mixed_hodge.py`.

No longer independent:

```text
eta/2:
    derived as H1-projected on-shell C1 action at q=1/3

endpoint self-similarity:
    derived from H1 endpoint compatibility plus p=q

rank-one angular carrier:
    supplied by Lambda^3 H1 -> dOmega_S2

h exclusion within elementary harmonic sector:
    follows from relative harmonic 0-form energy identity
```

Remaining minimal domain premise:

```text
P_domain:
    elementary phi0 mass emergence uses the mixed Hodge harmonic
    representative projector on I x S2.
```

What `P_domain` means:

```text
keep absolute harmonic H1 angular area carrier;
kill relative exact scalar h residuals.
```

If `P_domain` holds:

```text
h=1
delta_h=0
q=p=1/3
s=1/9
Delta Pi/R=1/6
eta=1/18
eta/2=1/36
```

Still outside this pre-spectrum closure:

```text
electron mass scale anchor;
full spectrum/depth/typed coefficient construction.
```

Four-hundred-twenty-first verdict:

```text
The remaining pre-spectrum postulate has been compressed to one
boundary-domain identification, P_domain.
```

Everything else in the elementary branch follows from metric/H1/C1 identities
once `P_domain` is accepted or derived.

## 432. `P_domain` from Dirichlet principle

Implemented in `native_p_domain_dirichlet_principle.py`.

Scalar residual variable:

```text
y = ln h.
```

Elementary relative boundary class:

```text
y(endpoint)=0
y(phi0)=0.
```

Residual scalar energy:

```text
E[y] = integral_I (y')^2 dt.
```

Variation with fixed endpoint values:

```text
delta E = -2 integral_I y'' delta y dt.
```

The boundary term vanishes because:

```text
delta y=0
```

at both ends.

Euler-Lagrange equation:

```text
y''=0.
```

Unique minimizer in the relative class:

```text
y=0
E_min=0.
```

Any nonzero `h` residual has:

```text
E[y] > 0.
```

So it is:

```text
a positive relative scalar excitation,
```

not:

```text
the elementary least-action representative.
```

Angular H1 carrier:

```text
omega_H1=dOmega_S2
```

is a harmonic angular representative, not a relative scalar residual.

Four-hundred-twenty-second verdict:

```text
If elementary phi0 mass emergence is the least-action representative in its
fixed relative scalar boundary class, P_domain follows.
```

That is:

```text
keep H1 harmonic area carrier;
kill h residual.
```

Remaining assumption:

```text
elementary means least-action/harmonic representative, not an excited
relative scalar boundary-layer state.
```

This is smaller than the previous statement of `P_domain`. It is a standard
variational/domain principle applied to the metric's scalar residual sector.

## 433. Elementary branch definition audit

Implemented in `native_elementary_branch_definition_audit.py`.

Pre-spectrum elementary branch means:

```text
no typed excitation/depth structure yet;
no additional scalar source residual;
no positive relative scalar boundary-layer mode;
keep only metric-forced harmonic carrier data.
```

Metric-forced carrier data at `phi0`:

```text
value normalization f=1;
absolute harmonic H1 area carrier;
first jet q through C1 momentum.
```

Excluded from the elementary ground branch:

```text
relative scalar h residual with E[y]>0.
```

Reason:

```text
it is an excitation/dressing of the collar domain.
```

Therefore in the elementary branch:

```text
h=1
delta_h=0
p=q.
```

Then H1 one-graph compatibility gives:

```text
q=p=1/3
s=1/9
eta=1/18
eta/2=1/36.
```

Four-hundred-twenty-third verdict:

```text
P_domain is equivalent to defining the pre-spectrum elementary branch as
the least-action harmonic carrier branch.
```

Nonzero `h` is not forbidden absolutely. It is classified as:

```text
a higher relative scalar boundary-layer excitation
```

outside:

```text
the elementary branch.
```

This avoids overclaiming. The metric is not saying no scalar residual can ever
exist. It is saying the elementary branch is the harmonic/least-action
representative before relative scalar excitations are added.

## 434. Final pre-spectrum postulate status

Implemented in `native_final_prespectrum_postulate_status.py`.

Derived in the current frame:

```text
H1 area-form carrier:
    Lambda^3 H1 -> dOmega_S2

rank-one angular carrier:
    H1, N=3

h exclusion inside elementary branch:
    Dirichlet principle

p=q:
    because delta_h=0 in least-action branch

p=q=1/3:
    H1 one-graph compatibility

eta=1/18:
    H1-projected C1 momentum

eta/2=1/36:
    H1-projected on-shell C1 action

endpoint self-similarity:
    consequence of N=3 one-graph branch
```

Remaining domain statement:

```text
The pre-spectrum elementary branch is the least-action mixed-Hodge harmonic
carrier branch on I x S2.
```

This means:

```text
keep absolute harmonic H1 area carrier;
quotient/omit positive relative scalar h excitations.
```

Not claimed:

```text
h modes cannot exist;
all spectrum/depth coefficients are derived;
the electron mass scale is derived.
```

Elementary branch output:

```text
q=1/3
s=1/9
Delta Pi/R=1/6
eta=1/18
eta/2=1/36
```

Four-hundred-twenty-fourth verdict:

```text
For the pre-spectrum elementary branch, the old q/eta/eta-half postulates
have collapsed into one boundary-domain definition.
```

The next stage is spectrum construction, where positive relative scalar/typed
modes may re-enter as excitations rather than as the elementary ground branch.
