# Exact derivation — complete observer-network assembly from scratch

Date: 2026-08-11

Mode: metric-led, exact analytic/CPU, all declared channels retained by type

Preregistration commit: `27e01595`

## 1. Result first

The regular UDT instruments do assemble into a coherent network, but coherence is not the same as
flatness. There are two exact realizations:

1. **Common endpoint atlas.** Object states and complete frames generate direct transitions. Every
   triangle descends identically for arbitrary smooth time-live histories.
2. **Path-labelled relation.** Arrows compose and reverse exactly while different routes can carry
   nonzero reciprocal periods, angular holonomy, or complete-matrix holonomy.

Four-observer face returns obey their own exact boundary-of-boundary/Bianchi bookkeeping identity.
This is the discrete `d^2=0` identity, not a new compatibility theorem or physical law. It does not
force any face return to vanish. Requiring every direct comparison to equal every
composite route would impose a genuine flat-descent restriction, but no frozen source owns that
condition universally. The banked R17 path/normal structure explicitly permits holonomy.

Primary landing:

```text
ASSEMBLY_IDENTITIES_ONLY_WITH_ROUTE_DEPENDENCE_OPEN.
```

Secondary conditional result:

```text
ALL_ROUTE_DIRECT_EQUALS_COMPOSITE_IFF_THE_RELEVANT_SCALAR_PERIODS_AND_MATRIX_HOLONOMIES_VANISH;
THIS_IS_A_CONDITIONAL_FLAT_DESCENT_RESTRICTION_NOT_A_CURRENTLY_OWNED_UNIVERSAL_UDT_LAW.
```

## 2. Scalar network: endpoint potentials versus edge data

For four observer objects, let `phi_i` and `kappa_i` be supplied object-state coordinates. On a
matched common family define

```text
delta_ij=phi_j-phi_i,
Delta_kappa_ij=kappa_j-kappa_i.
```

Every triangle closes identically:

```text
delta_ij+delta_jk-delta_ik=0,
Delta_kappa_ij+Delta_kappa_jk-Delta_kappa_ik=0.       (1)
```

Equation (1) holds for arbitrary values and arbitrary smooth time dependence of every object
state. It is descent bookkeeping, not an evolution equation.

Now allow a genuinely edge- or path-labelled antisymmetric depth `e_ij=-e_ji`. Its face period is

```text
omega_ijk=e_ij+e_jk+e_ki.                            (2)
```

Reversal does not force `omega_ijk=0`. On a four-object simplex the four face periods obey

```text
omega_123-omega_023+omega_013-omega_012=0.           (3)
```

Equation (3) is exact for every six edge values: it is `d^2=0`. It correlates the face returns but
does not select the edges or set a face period to zero. On the complete simplex, all face periods
vanish iff the edge depth descends to an object potential. On a path groupoid with nontrivial loops,
closed periods can remain as route data.

The finite `K4` network is a type diagnostic. It does not assert that scalar distances add around
an arbitrary spatial triangle. Scalar addition applies only when the relation family supplies
correctly matched composable depth channels.

## 3. Terminal `c_E` calibration

Write `z_ij=exp(delta_ij)`. The founded reciprocal character and conditional terminal ratio are

```text
D(z)=diag(z^-1,z),
r_ij=c_eff^(pair)(j;i)/c_E=z_ij^-2.                  (4)
```

For carried matched depths,

```text
D(z_jk)D(z_ij)=D(z_ij z_jk),
r_ij r_jk=(z_ij z_jk)^-2.                            (5)
```

Compared with an independently supplied direct edge,

```text
m_ijk=z_ij z_jk/z_ik,
(r_ij r_jk)/r_ik=m_ijk^-2.                           (6)
```

Thus `c_E` exposes the same route mismatch; it does not remove it. If the pair readout descends to
one endpoint scalar, every closed product is one. If it is path/pair calibrated, a nonunit closed
product is calibration holonomy until a physical descent rule says otherwise.

Imposing `c_eff=c_E` independently at every endpoint would set every `z_ij=1` and trivialize the
positional depth. That is not the terminal-calibration rule in the frozen sources. `c_E` fixes the
clock/ruler unit and ordinary reference; the complete relation determines the terminal ratio.

## 4. Angular orchestra and four-observer coherence

Let an oriented angular carry be

```text
U_ij in SO(2),
U_ji=U_ij^-1.
```

The based face holonomy is

```text
H_ijk=U_ki U_jk U_ij.                                (7)
```

The exact rational rotation witnesses have `H_012 != I`, yet composition and reversal remain
lawful. Because `SO(2)` is abelian, the four faces obey

```text
H_123 H_023^-1 H_013 H_012^-1=I.                    (8)
```

Equation (8) is the discrete abelian angular Bianchi identity. It is exact bookkeeping, not a new
compatibility theorem, and it is compatible with every face being nontrivial. For a **chosen smooth
local angular connection on a contractible neighborhood**, identity holonomy around every
sufficiently small based contractible loop is equivalent to zero connection curvature there. That
conditional continuum lemma cannot become a current metric restriction before the physical
comparison connection/arrow is owned. Current ownership instead retains path-labelled angular
holonomy; it does not demand universal flatness.

The same distinction persists for complete nonabelian arrows, with the usual basepoint transports
and conjugations included in the nonabelian Bianchi relation.

## 5. Complete coframe assembly with time and mixing live

Let `E_i(t)` be arbitrary regular complete coframes, including base, angular, and lower mixing
blocks. The endpoint presentation transition

```text
G_ij(t)=E_j(t) E_i(t)^-1                              (9)
```

obeys

```text
G_jk G_ij=G_ik,
G_ji=G_ij^-1                                         (10)
```

and the time derivative of (10) vanishes identically. The exact controller uses four fully
nonconstant lower-block matrices with every declared block active. No frequency or derivative is
selected.

This is an assembled machine, but `G_ij` is an endpoint frame transition. It is not automatically
the physical non-isometric observer-pair relation. A path connection instead produces lawful
holonomy. A supplied physical arrow can also compose, but its metric/query owner remains open.
Conflating these three arrow types either creates a false zero or invents a selector.

## 6. Pair metric, shift, and mixing remain present

On each supplied regular pair cell,

```text
h=-T^2(dy0+beta dy1)^2+L^2(dy1)^2,
kappa=log sqrt(TL),
phi=(1/2)log(L/T).
```

The exact full two-column witness

```text
V0=(1/2,0,1/4,0),
V1=(0,2,1/3,0)
```

gives

```text
h=[[-3/16,1/12],[1/12,37/9]],
beta=-4/9,
L^2=112/27.
```

Thus the scalar, shift, and screen/mixing data are not zeroed in the network audit. `beta` remains
an object/query state and must match through an intermediate object; it is not silently converted
into a third additive scalar. Complete mixing enters the pair metric and full arrow before any
reciprocal projection.

## 7. Causal typing

Every supplied regular pair immersion preserves its induced tangent causal type automatically.
Composition of correctly typed local causal isomorphisms remains lawful. Neither fact implies
global ambient-order reflection, causal convexity, chronology, global hyperbolicity, or selection
of a physical all-observer family.

Those global properties could restrict assembled branches once the pair immersions and completion
are owned. The fifteen frozen sources leave that construction and requirement open. A finite graph
cannot manufacture the missing ambient ownership.

## 8. Ownership classification

The joint structures are not merely loose parts:

- founded reciprocal character: exact on supplied matched depths;
- common-scale and reciprocal endpoint characters: exact on a supplied common family;
- shift: retained endpoint/query state;
- angular carry: exact path-groupoid arrow with holonomy;
- complete frame transitions: exact flat endpoint atlas;
- terminal `c_E`: exact calibrated ratio readout on supplied pair cells;
- local causal typing: automatic on supplied immersions;
- four-observer face relation: exact Bianchi identity.

None of these currently owns all-route flatness, a unique physical calibrated pair/query relation
family, global causal faithfulness, or a nonidentity metric-history equation. The correct next
joint is therefore narrower than an arbitrary search for `R(j^k g;G_global)=0`, but it has two
inseparable parts:

> Which physical calibrated relation family is owned, and within that family does positional
> comparison become endpoint-descended, path-labelled, or a quotient of path data—branch by
> branch and regime by regime?

Relation-family ownership comes first logically; route policy cannot type arrows that have not yet
been physically selected. Together they determine whether the conditional flatness equation is
physical, gauge, or false. Neither is supplied here.

## 9. Scope

The audit covers the complete three- and four-object finite network, object-exact and path-labelled
relation homes, arbitrary smooth regular endpoint coframes, terminal reciprocal calibration,
angular holonomy, and local causal typing. It excludes singular strata and does not classify every
global topology or observer protocol.

No action, source, carrier, matter, mass, bootstrap rule, `X_max` value, CMB spectrum, material
signal law, or dynamics is derived.
