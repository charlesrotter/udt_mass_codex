# Exact derivation — carried/intrinsic middle-morphism ownership

Date: 2026-08-10

Current grade: **VERIFIED-WITH-CAVEATS**

Sharpened post-review landing:

```text
GAUGE_GROUPOID_ALREADY_SUFFICIENT_FOR_PROJECTOR_ALIGNMENT__CALIBRATION_DESCENT_OPEN
```

The preregistered landing `RELATIVE_ORBIT_DERIVED__REPRESENTATIVE_OPEN` remains a valid lower
bound. Fresh manifest-confined external review showed that it understates the strongest owned
object: the full path-labelled `SO(2)` alignment bitorsor already composes exactly by balanced
composition. A single screen-phase representative remains unselected and is not required for that
projector-level composition.

## 1. Result first

On every retained regular C01--C06 stratum, a carried reciprocal grading and the grading rebuilt
from the endpoint metric have the same causal spectral type. They can therefore be aligned by a
proper orthochronous Lorentz map. The alignment is not unique.

When the full metric-owned projector triple is retained,

```text
(P_u,P_n,H),
```

all alignment maps form a continuous `SO(2)` torsor: after one alignment is chosen, an arbitrary
rotation of the two-dimensional screen gives another exact alignment while changing none of the
owned clock/ruler/screen projectors. The branch therefore owns the two reductions, the full
path-labelled alignment bitorsor, and its balanced representative-free composition. It does not
select one middle-morphism representative.

This is narrower and more constructive than “`M_B` is missing.” Existence is not missing on the
regular same-`lambda` strata. What remains missing is not projector-level composition. It is a
proof that the terminal reciprocal scalar and calibration-density data descend through this
bitorsor, or else a lawful physical pair atlas containing the additional non-screen data they
require.

## 2. Correct objects

At an endpoint `q`, let

```text
R_int(q)=(P_u^int,P_n^int,H^int)
```

be the reduction reconstructed from the complete metric: the unique timelike Killing line, its
twist-selected spacelike ruler line, and their orthogonal screen. For a supplied path
`gamma:p->q`, let

```text
R_car(gamma,q)=U_gamma R_int(p) U_gamma^-1
```

be the corresponding Levi-Civita-carried reduction. Its grading is

```text
X_car=-P_u^car+P_n^car+lambda H^car,
```

whereas the locally rebuilt grading is

```text
X_int=-P_u^int+P_n^int+lambda H^int.
```

The prior full-holonomy audit proves `X_car != X_int` generically. They are not two names for one
endpoint tensor. They are two reductions in the same Lorentz tangent space.

The present audit first uses the minimal isometric alignment arena

```text
G=SO^+(T_qM,g_q).
```

Allowing general-linear maps would enlarge, not remove, the nonuniqueness. Calibration density and
non-isometric pair-surface realization are deliberately not smuggled into this grading-alignment
question.

## 3. Existence and torsor theorem

For fixed `lambda`, both reductions have:

- one timelike clock line;
- one spacelike ruler line;
- one positive two-dimensional screen;
- the same time/orientation component after those components are supplied.

The proper orthochronous Lorentz group acts transitively on such regular ordered decompositions.
Hence the alignment set

```text
M_gamma(q)={M in G: M R_car M^-1=R_int}
```

is nonempty.

If `M_0` is one solution and

```text
H_int={h in G: h R_int h^-1=R_int},
```

then every `h M_0` is also a solution. Conversely, if `M_1` is another solution, then
`M_1 M_0^-1` lies in `H_int`. Therefore

```text
M_gamma(q)=H_int M_0=M_0 H_car.
```

This is a bitorsor, not a singleton.

For the complete projector triple, the connected stabilizer is exactly the rotation group of the
positive screen:

```text
H_int ~= SO(2).
```

The metric and its orientation give the screen metric and its quarter-turn complex structure, but
not a preferred nonzero screen axis or phase. `SO(2)` preserves all of this data.

## 4. Exact finite witness

In an adapted frame put

```text
eta=diag(-1,1,1,1),
X_lambda=diag(-1,1,lambda,lambda).
```

Use the rational boost

```text
B_01=[[5/4,3/4,0,0],
      [3/4,5/4,0,0],
      [0,0,1,0],
      [0,0,0,1]]
```

and the exact screen quarter-turn

```text
R_23=[[1,0,0,0],
      [0,1,0,0],
      [0,0,0,-1],
      [0,0,1,0]].
```

Both preserve `eta`, have determinant one, and preserve time orientation. Define

```text
X_car=B_01 X_lambda B_01^-1,
M_0=B_01^-1,
M_1=R_23 B_01^-1.
```

For every retained `lambda` value,

```text
M_0 X_car M_0^-1=X_lambda,
M_1 X_car M_1^-1=X_lambda,
M_0 != M_1.
```

The same two maps align `P_u`, `P_n`, and `H` exactly. Thus nonuniqueness survives after the full
metric-owned clock/ruler/screen decomposition is retained; it is not an artifact of using the
grading alone.

## 5. Stabilizer census across all six strata

The exact Lorentz-algebra commutator census gives:

| lambda | stabilizer of `X_lambda` | stabilizer of `(P_u,P_n,H)` |
|---:|---:|---:|
| -2 | 1 | 1 |
| -1 | 3 | 1 |
| 0 | 1 | 1 |
| 1/2 | 1 | 1 |
| 1 | 3 | 1 |
| 2 | 1 | 1 |

Dimensions are Lie-algebra dimensions. At generic `lambda`, the grading stabilizer is screen
`so(2)`. At `lambda=+1`, grading alone merges ruler and screen into a spatial `so(3)` eigenspace.
At `lambda=-1`, grading alone merges clock and screen into an `so(1,2)` eigenspace. Retaining the
separately metric-owned clock and twist-ruler projectors reduces both exceptional cases back to
the same one-dimensional screen stabilizer.

Therefore no retained regular stratum provides a unique projector alignment.

## 6. What is frame-independent

Choose adapted frames `E_int` and `E_car` for the two reductions and form

```text
R=E_int^-1 E_car.
```

Changing the adapted frames by stabilizer elements gives

```text
R -> h_int^-1 R h_car.
```

The representative changes, but its double-coset class

```text
[R] in H_int\G/H_car
```

does not. Equivalently, the endpoint metric owns the ordered pair of projector triples directly.
This path-labelled relative orbit is a frame-independent shadow of the stronger owned object: the
whole alignment bitorsor.

The phrase “double coset” must not be misread as a new scalar or group law. `SO(2)` is not normal in
`SO^+(1,3)`: conjugating a screen rotation by a clock/screen boost takes it outside the screen
stabilizer. Consequently the naive double-coset space does not inherit the group multiplication
needed for middle-arrow composition.

A correctly typed gauge groupoid/bitorsor category composes without selecting a screen phase. The
exact balanced-composition witness is derived in the next subsection. Descent of the terminal
reciprocal readout and calibration density remains the next question.

### 6.1 Exact balanced composition

Let three reductions be represented by adapted Lorentz frames `g_1,g_2,g_3`, and let
`H_i=g_i SO(2) g_i^-1` be their screen stabilizers. An alignment from reduction 1 to 2 has the form

```text
m_12 = g_2 h_a g_1^-1,
```

and an alignment from reduction 2 to 3 has the form

```text
m_23 = g_3 h_b g_2^-1.
```

Changing the middle representative by `h_2 in H_2` must act on both legs:

```text
m_23 -> m_23 h_2,
m_12 -> h_2^-1 m_12.
```

The product is then exactly invariant:

```text
(m_23 h_2)(h_2^-1 m_12)=m_23 m_12.
```

The production SymPy derivation and an independent rational `Fraction` implementation verify this
with `g_1=I`, rational boosts `g_2=B_01`, `g_3=B_02`, and exact screen rotations. The product maps
every projector in reduction 1 to its counterpart in reduction 3. Changing only one leg fails, as
required by the new catch-proof. Thus ordinary multiplication of double-coset classes remains
ill-defined, but balanced composition of the alignment bitorsors is exact and representative-free.

## 7. Why the complete coframe does not silently fix the phase

The displayed branch coframe contains named `sigma_1,sigma_2` representatives, so one can write

```text
M=E_int E_car^-1.
```

That is a valid conditional representative. It is not metric-owned merely because it is easy to
write. Orientation-preserving screen rotations change the two named screen axes while leaving the
metric, intrinsic clock, twist-ruler, screen projector, and grading fixed.

More abstractly, a Lorentz-natural adapted-frame choice would require an equivariant section of

```text
G -> G/SO(2).
```

No strictly left-equivariant section exists because the base flag has a nontrivial `SO(2)`
stabilizer. A universal continuous section is also globally obstructed: restricting to the maximal
compact subgroup gives the nontrivial bundle `SO(3)->S^2`, whose section would provide a nowhere-zero
tangent vector field on `S^2`. Local gauges and branch presentations exist; the metric does not
thereby select one as physical.

Likewise, “shortest,” “minimum boost,” polar, or Frobenius representatives require an additional
objective, Euclideanization, ordering convention, or connection on the flag space. They may be
useful controls, but none is among the frozen UDT premises.

## 8. Holonomy keeps the relation path-labelled

The frozen branch evidence is not a diagonal toy:

- 18/18 local rows have nonzero clock/ruler `nabla X`;
- 36/36 loops return nonidentity Lorentz holonomy;
- 36/36 loops fail ordinary endpoint grading closure;
- 36/36 loop integrations retain exact path composition within tolerance.

Thus the carried reduction depends on the supplied path. A different path changes the relative
orbit unless the intervening holonomy lies in the intrinsic stabilizer. The sampled full-holonomy
branches do not satisfy that reduction. Path labels cannot be erased.

## 9. Consequence for the R17 conditional assembly

The previous conditional formula

```text
A_gamma=U_gamma exp(delta_K X_p)
```

still composes exactly on matched carried objects. This audit neither selects nor refutes that
assembly. It refines its endpoint seam:

- an isometric projector alignment to the locally rebuilt reduction always exists on the retained
  regular same-`lambda` strata;
- the alignment representative is an `SO(2)` family, not a metric-selected map;
- calibration density, pair-surface integrability, and the physical relation functor are not fixed
  by projector alignment.

The projector-level middle bridge is therefore no longer missing: its correct object is the whole
alignment bitorsor rather than one chosen matrix. It remains possible that every lawful reciprocal
scalar readout is invariant across this bitorsor. If so, selecting a screen phase is unnecessary
for the scalar sector. That scalar/calibration-density descent statement has not yet been proved.

## 10. Scoped landing

The preregistered primary landing remains the valid lower bound

```text
RELATIVE_ORBIT_DERIVED__REPRESENTATIVE_OPEN.
```

Fresh external adjudication sharpens it to

```text
GAUGE_GROUPOID_ALREADY_SUFFICIENT_FOR_PROJECTOR_ALIGNMENT__CALIBRATION_DESCENT_OPEN.
```

This is a bounded kinematic result for C01--C06 on regular supplied paths. It is not a complete
observer-pair law, scalar cocycle, universal `c_eff`, dynamics, source, matter, mass, bootstrap,
boundary, `X_max`, CMB, or signalling result.
