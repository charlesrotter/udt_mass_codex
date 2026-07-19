# Infinite-c / UDT Reciprocity adjudication — derivation report

Date: 2026-07-18  
Branch: `codex/infinite-c-reciprocity-adjudication-2026-07-18`  
Required parent: `b3cd93bd92960b89935b9946b88f2e6017195c99`  
Preregistration commit: `de6c264`

## Adjudication

The preregistered outcome is:

```text
LAYERED_COMPATIBILITY_METRIC_NONDISCRIMINATING
```

Both intuitions in the motivating exchange were partly correct, but they apply to different
meanings of “infinite c”:

1. A **literal infinite conversion at the same foundational layer** is incompatible with the
   current Reciprocal-c Identity. `C=infinity` and `1/C=0` are not two coequal finite conversion
   isomorphisms, and their product is not a defined inverse identity. Adopting that ontology would
   require replacing—not deriving—the present foundation.
2. A **regulated/projective infinite-c limit** is compatible with dual Reciprocity. Every finite
   regulator remains an invertible determinant-one reciprocal transformation, while its metric has
   a finite conformal limit. The singular endpoint is not itself a group element.
3. A **finite light cone that looks reciprocal** does not prove the internal Reciprocity Principle.
   A nonreciprocal diagonal calibration gives the same local adapted time/parallel conformal block
   and is related to the reciprocal representative by a common scale. CSN removes that block-level
   metric difference, while only the reciprocal representative preserves the internal `K`-pairing.
4. The first post-preregistration owner clarification supplies two possible **layered** candidates:
   atemporal/global closure (H5A), which is compatible with geometric Reciprocity, and a genuinely
   timed instantaneous substrate (H5B), which is an open replacement causal theory.
5. The second clarification supplies the cleanest metric reading (H6): with finite observational
   anchor `c_0`, the adapted null slope is `c_0 exp(-2phi)`. Its reciprocal endpoints are infinity
   and zero, while local metric proper measurements remain `c_0`.

Therefore the infinite-c idea neither forces abandonment nor independently validates Reciprocity.
The present foundation remains unchanged. The constructed local adapted time/parallel conformal
block cannot adjudicate the internal principle; a native pairing/representation theorem or
full-four-dimensional/global/internal observable is needed.

## T1 — layers, units, and meanings

The following objects must not be conflated:

| Object | Meaning |
|---|---|
| `C` | Counterfactual bare/regulator conversion used only in this audit |
| `c_eff` | Finite null slope in an already chosen time/parallel two-plane |
| `1/c_eff` | Operational slowness in selected units |
| `P^T K P=K` | Internal dual-pairing preservation |
| `[g]_CSN` | Conformal causal geometry after common-scale quotient |
| atemporal/global closure | Candidate underlying relation with no primitive propagation parameter |

The number `186,000` depends on choosing miles and seconds; its inverse is a time per mile, not a
unit-independent physical invariant. UDT could seek an emergent finite universal causal conversion
or dimensionless ratios involving it, but no foundation can be selected by that numerical spelling.

The owner clarification also separates status layers: the existence and measured value of a finite
universal `c_obs` can be an observational anchor, while interpreting `c_obs` and `1/c_obs` as coequal
conversion directions is a foundational geometric statement. Neither is automatically a statement
about a pregeometric substrate.

## T2 — literal infinity is not an invertible reciprocal conversion

For finite positive diagonal

```text
P=diag(u,v),   K=[[0,1],[1,0]],
```

the equation `P^T K P=K` is exactly `uv=1`; both entries are finite and nonzero. The literal pair
`(infinity,0)` is not an element of `GL(2,R)`. The expression `0*infinity` is undefined, not one.

Thus H1 conflicts with the current finite, faithful same-layer Reciprocal-c interpretation. This is
a type/domain incompatibility, not an empirical falsification of the owner-stated principle. A
boundary point, limiting sequence, generalized projective object, or emergent lower layer must be
classified separately.

## T3 — the regulated reciprocal limit exists projectively

Let `C` be finite and let the desired effective null slope be finite positive `c_eff`. Choose

```text
u_R=sqrt(c_eff/C),
v_R=sqrt(C/c_eff),
P_R=diag(u_R,v_R).
```

Then exactly

```text
det(P_R)=1,
P_R^T K P_R=K.
```

The reciprocal metric block is

```text
g_R=diag(-C^2 u_R^2,v_R^2)
   =(C/c_eff) diag(-c_eff^2,1).
```

Therefore its conformal class is the ordinary finite Lorentz block for every finite `C`. As
`C -> infinity`, `u_R -> 0` and `v_R -> infinity`; the unscaled matrix has no finite endpoint. After
projective normalization,

```text
sqrt(c_eff/C) P_R=P_NR -> diag(0,1),
```

a finite rank-one representative exists, but it is singular and lies outside `GL(2)`/`PGL(2)`.
There is no finite **invertible reciprocal** endpoint. Reciprocity holds along the regulated family,
not as an equation on the singular endpoint.

This makes H2 `CONDITIONAL_COMPATIBLE`, not derived or selected. The bare regulator adds no local
observable and no explanation for why `c_eff` has a particular finite value.

## T4 — the divergent constant creates no new residual warping

Write

```text
phi_C(x)=(1/2)log(C/c_star)+psi(x).
```

Then

```text
g_C=(C/c_star)
    diag(-c_star^2 exp(-2psi), exp(2psi)),
c_eff(x)=c_star exp(-2psi(x)),
d phi_C=d psi.
```

The regulator-dependent part is a spacetime-constant common factor when `C` and `c_star` are
constant. It contributes no derivatives and disappears from the local CSN conformal geometry. Any
curvature/warping attributable to this reciprocal block comes from the residual field, its coupling
to the full geometry, and global/boundary structure—not from the magnitude of the divergent
constant itself.

This is exact reparameterization of the finite residual reciprocal metric. It is not yet a new
physical mechanism.

## T5 — nonreciprocal countermodel with the same light cone

Now omit dual Reciprocity and choose

```text
P_NR=diag(c_eff/C,1).
```

It gives

```text
g_NR=diag(-c_eff^2,1),
det(P_NR)=c_eff/C,
P_NR^T K P_NR=(c_eff/C)K.
```

So it does **not** preserve the internal pairing for generic `C`. Nevertheless,

```text
P_R=sqrt(C/c_eff) P_NR.
```

The two calibrations differ only by a finite common factor for every finite regulator and therefore
represent the same local pre-scale CSN geometry in the selected adapted time/parallel block for
every finite regulator. Full four-dimensional conformal equivalence would additionally require the
open transverse completion to co-scale; post-scale matter, boundary, or global closure may also
distinguish representatives. More generally, every positive `diag(u,v)` decomposes as

```text
diag(u,v)=sqrt(uv) [diag(u,v)/sqrt(uv)],
```

and the bracketed representative has determinant one.

This is the load-bearing independence result:

> CSN plus a diagonal causal ratio always permits a determinant-one representative, but it does not
> derive the physical internal statement `P^T K P=K`.

`P_NR` is not an admissible countermodel to the **current full C1 ledger**, because dual Reciprocity
is founding there. It is an admissible logical countermodel to the claim that infinite-c plus CSN
would independently derive that founding principle.

## T6 — literal Galilean-to-Lorentz emergence is a replacement theory

“Infinite causal speed” as physical ontology is not merely a large coefficient in a Lorentz metric.
It normally means no finite Lorentz cone and requires a Galilean/degenerate clock-plus-space
structure or some other pregeometry. No finite invertible anisotropic dilation changes that
structure into a nondegenerate Lorentz conformal metric; the transition is singular.

A coherent H4 theory could still be built, but it needs new content:

- the pregeometric fields and symmetry group;
- a dynamics or phase/closure rule producing a nondegenerate cone;
- universal coupling of every carrier and interaction to that same cone;
- control of preferred-frame and dispersion branches;
- finite-cell/global selection of the residual conversion.

None is supplied by the current foundation or by the algebraic limit. H4 remains
`OPEN_REPLACEMENT_THEORY`.

## Post-preregistration H5A/H5B — observational geometry over a deeper layer

After preregistration, the owner disclosed a roughly 35-year-old historical picture: distant
emission was imagined as
an instantaneous or globally related underlying state change, while the observer's finite light
travel time was a consequence of observational spacetime geometry. This is
`HISTORICAL_OWNER_INTUITION / QUESTION_ONLY` under the provenance firewall: electrons, energy
levels, instantaneous transitions, a native carrier, and a time-live matter action are not derived
UDT objects. The exact input and its timing are
preserved in `POST_PREREG_OWNER_CLARIFICATION.md` rather than silently folded into the preregistration.

This is more coherent than H1 if the layers are kept distinct:

```text
underlying atemporal/global closure
        -> bootstrap/realization map (OPEN)
finite observational Lorentz geometry with c_obs
        -> null paths and observer travel times
```

If the underlying layer has no primitive geometric time or distance, “infinite speed” is not yet a
well-typed speed. It is better provisionally described as absence of a propagation parameter,
atemporal closure, or global constraint. Assigning it a Galilean speed would require an additional
substrate clock, distance, and preferred simultaneity structure.

The observer's travel time can then be geometric:

```text
T_obs[gamma] = integral_gamma s_g d ell,
s_g = 1/c_obs
```

in a static optical shorthand, or more generally by the null relations of the emergent metric. This
does not require literal curvature to be large everywhere: a finite baseline Lorentz geometry
already has nonzero travel time, while curvature/inhomogeneous dilation changes paths, redshifts,
and delays. If UDT intends *all* baseline slowness to be “warp,” the finite cell/bootstrap must derive
that ever-present baseline geometric calibration.

Most importantly, an underlying instantaneous/global relation must not become an observable
superluminal signalling channel. A local electron state transition, an atemporal global solution
constraint, and the observer's accessible signal are three different statements. Universal cone
coupling is necessary but not sufficient: the theory must also cover controllable interventions and
information transfer through the underlying relation.

Two hypotheses must remain separate:

- `H5A_ATEMPORAL_GLOBAL_CLOSURE` has no primitive substrate time/distance. It is
  `CONCEPTUALLY_COMPATIBLE_NOT_DERIVED`; Reciprocity can remain foundational for the emergent
  geometric conversion pair without being derived by H5A.
- `H5B_TIMED_INSTANTANEOUS_SUBSTRATE` has a real substrate clock, distance, and instantaneous
  propagation. It requires simultaneity or equivalent preferred causal structure and belongs with
  H4 as an `OPEN_REPLACEMENT_THEORY`.

Silently translating H5B into H5A would be invalid. Either is a possible future owner choice, but
only H5A avoids adding a replacement causal structure now.

## Post-preregistration H6 — reciprocal causal endpoint flow as a metric property

The owner then clarified that the infinite/zero behavior should be a direct property of the metric
at asymptotic reciprocal depth. The exact statement and its post-preregistration timing are retained
in `POST_PREREG_METRIC_ENDPOINT_CLARIFICATION.md`.

In the conditional adapted reciprocal block with finite observational anchor `c_0`,

```text
g_phi=diag(-c_0^2 exp(-2phi), exp(2phi)).
```

The radial coordinate null slope follows directly from `ds^2=0`:

```text
c_coord(phi)=sqrt(-g_tt/g_parallel)=c_0 exp(-2phi).
```

It obeys the exact reciprocal relation

```text
c_coord(phi)c_coord(-phi)=c_0^2,
```

and endpoint limits

```text
phi -> -infinity: c_coord -> infinity,
phi = 0:           c_coord = c_0,
phi -> +infinity: c_coord -> 0.
```

This is the cleanest current interpretation of the historical idea: infinite and zero are
reciprocal asymptotic causal-slope boundaries, while finite observational `c_0` is their self-dual
geometric anchor. No literal infinite coefficient is inserted into the metric, and Reciprocity is
used rather than abandoned.

The infinity and zero are not automatically local measurements. Static observers using the same
metric have

```text
d tau=exp(-phi)dt,
d ell=exp(phi)dr,
```

so for every finite `phi` a radial null ray satisfies exactly `d ell/d tau=c_0`. Thus H6 can preserve
Einsteinian local light speed while its adapted coordinate cone opens and closes. Endpoint
orthonormal frames degenerate. If locally measured light speed itself is intended to diverge or
vanish, H6 does not implement that; a different matter-clock coupling, multiple cone, or altered
local causal structure would be required. `c_coord` is not a diffeomorphism scalar; it presupposes
the conditional time/parallel lines and chart. The full four-dimensional cone and matter clock/ruler
coupling remain open.

At finite `phi` the block is Lorentzian and nondegenerate with determinant `-c_0^2`. The unscaled
metric has no finite matrix limit at either endpoint: one component diverges while the other
vanishes. After singular conformal/projective normalizations, exact rank-one representatives are

```text
exp(2phi)g_phi -> diag(-c_0^2,0)  as phi -> -infinity,
exp(-2phi)g_phi -> diag(0,1)      as phi -> +infinity.
```

These are comparable respectively to open-cone (Galilean-like) and closed-cone (Carrollian-like)
contractions. The normalizing factors themselves tend to zero, so these are boundary/projective
limits rather than finite CSN transformations. The symmetry labels are not adopted UDT foundations.

Finally, the current foundation supplies no map from physical distance to `phi`. The proposed

```text
distance -> 0  corresponds to phi -> -infinity,
CMB            corresponds to phi -> +infinity
```

is therefore `OPEN`. “Distance” must distinguish coordinate radius, metric proper distance, event
separation, and resolution/positional scale. Ordinary local separation tending to zero does not
imply `phi -> -infinity`; in an areal-center reading, regularity and the transverse geometry may
actively challenge `exp(2phi)->0`.

The existing conditional WR-L profile supplies a direct comparison:

```text
phi(r)=-(1/2)log(1-r/X),
c_coord(r)=c_0(1-r/X).
```

It gives `c_coord(0)=c_0`, not infinity, and tends to zero at its wall. Since that profile is not
uniquely selected, this does not refute H6; it proves that a fast short-separation endpoint needs a
different/running depth map rather than following automatically from the current branch.

The observational CMB is initially a comparison/readout surface on an observer's past-null
geometry, not automatically a spatial wall or finite-cell boundary. It cannot be silently identified
with the canonical mirror seal: the synchronized static-sector seal parity currently states
`phi=0` there. A native time-live topology/profile must distinguish center, CMB surface, wall, and
mirror seal before the endpoint picture becomes physical rather than kinematic.

## T7 — no revised Lorentz algebra for constant effective c

For

```text
g_eff=diag(-c_eff^2,1),
gamma=(1-w^2/c_eff^2)^(-1/2),
Lambda=[[gamma,-gamma w/c_eff^2],[-gamma w,gamma]],
```

for real `|w|<c_eff`, exact algebra gives `Lambda^T g_eff Lambda=g_eff`. This is the ordinary
`O(1,1)` time/parallel boost block with the effective finite causal conversion, not a completed
`O(1,3)` geometry. A large or divergent constant calibration does not by itself deform the boost
algebra.

If `psi(x)` varies, there is generally no single global Lorentz transformation; the effective
metric has local Lorentz frames and may be curved. That is geometry from the residual field/full
metric, not a new boost algebra proved by infinite `C`.

## T8 — neither principle derives the other

The exact models close both directions:

- Infinite-c plus CSN fixes at most the effective ratio/projective cone. `P_NR` proves it does not
  derive the internal `K`-pairing.
- Dual Reciprocity fixes `uv=1` but leaves `C`, `c_eff`, the residual field, and any regulator
  interpretation free. It does not select `C -> infinity` or the observed conversion.

Thus the two ideas are logically independent until a deeper UDT statement relates positional
action, internal pairing, spacetime realization, and global closure.

## T9 — the prior realization gap remains

An effective cone slope presupposes a time/parallel two-plane and does not select its ordered lines.
Neither H1-H6 supplies the native projectors/realization rule identified by the previous
selector. A native spacetime action of the positional representation could potentially provide both
line eigendata and pairing meaning, but it remains the next conceptual hypothesis—not a result here.

## T10 — adjudication and recommendation

| Hypothesis | Ruling | Meaning |
|---|---|---|
| H0 finite reciprocal effective | `CONSISTENT_CURRENT_FOUNDATION` | Retain unless separately revised |
| H1 literal infinity at same layer | `INCOMPATIBLE_IN_CLASS` | Would replace current Reciprocal-c |
| H2 regulated/projective infinity | `CONDITIONAL_COMPATIBLE` | Adapted-block reinterpretation; rank-one endpoint is outside GL(2)/PGL(2) |
| H3 CSN apparent reciprocity | `BLOCK_EQUIVALENT; INTERNAL_PAIRING_NOT_DERIVED` | Proves local time/parallel metric non-discrimination only |
| H4 Galilean-to-Lorentz emergence | `OPEN_REPLACEMENT_THEORY` | Requires a new complete emergence mechanism |
| H5A atemporal global closure | `CONCEPTUALLY_COMPATIBLE_NOT_DERIVED` | Lets Reciprocity govern emergent geometry; owes bootstrap and intervention-level no-signalling |
| H5B timed instantaneous substrate | `OPEN_REPLACEMENT_THEORY` | Adds preferred causal/simultaneity structure |
| H6 reciprocal causal endpoint flow | `CONDITIONALLY_COHERENT_METRIC_BLOCK_INTERPRETATION` | Makes infinity/zero reciprocal metric-slope endpoints around finite self-dual c_0 |

The evidence does not warrant abandoning Reciprocity. It also does not warrant promoting literal
infinite `C`. The regulated version is presently a redundant projective parametrization of the same
local adapted block. The historically intended layered version is better stated as an atemporal
foundation plus observational geometry; it is compatible with geometric Reciprocity but requires a
new bootstrap/realization and no-signalling theorem. The metric-endpoint refinement H6 is the most
economical version of the infinite/zero intuition because it follows directly from the reciprocal
block and retains finite local `c_0`; its distance and CMB mappings remain open.

The strongest next discriminator is conceptual and native:

```text
Does positional dilation/bootstrap carry a physical internal-to-observational-geometric pairing
action beyond the determinant-one representative that CSN makes available automatically?
```

If yes, Reciprocity has independent geometric content and may also help realize the ordered
spacetime lines while the underlying closure remains atemporal. If no, its visible metric signature
is redundant with CSN and its foundational status would require an explicit owner reconsideration.
Either decision must precede additional action searches.

All accepted downstream statuses remain unchanged: Reciprocal-c and dual Reciprocity remain
`FOUNDING`; the reciprocal exponential comparison remains `DERIVED / CONDITIONAL` from those
premises plus composition, regularity, and conventions; `C^2`/Bach remains unique-conditional; EH
conditional; line realization, variation bridge, complete action, carrier/source, finite boundary
charge, unconditional mass, and shared-static source route open.

## Bounded completeness map

| Criterion | Covered | Still open |
|---|---|---|
| Algebra | Finite reciprocal family, rank-one projective limit, H6 endpoint reciprocity, CSN countermodel | Generalized invertible endpoint structure |
| Causality | Adapted null slope, local proper c_0, and O(1;1) Lorentz invariance | Emergent universal coupling/full 4D cone/no-signalling theorem |
| Fields | Regulator and residual separated | Native field ontology and line realization |
| Global | Required discriminator identified | Finite-cell/bootstrap selection and distance/CMB/seal map |
| Action/equations | None promoted | Complete dynamics and variation domain |
| Boundary/topology | Held fixed | Complete finite-cell construction |
| Observation | Unit dependence separated | Dimensionless discriminators and bounds |

The result is CPU-only, action-free, carrier-free, and non-canonizing. It changes no current
foundation, frozen package, research artifact, registry, navigation control, or `grok`.
