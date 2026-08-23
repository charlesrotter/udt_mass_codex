# G231 exact derivation — Cartan regional realization bridge

Date: 2026-08-23

## 1. Bounded question

G227, G228, and G230 establish the exterior-closure stages through
`(R, nabla R, nabla^2 R)` at one supplied event; G229 supplies their metric-jet bridge through
fourth order. G231 asks what data type can replace the pointwise tower by one metric on an actual
local neighborhood.

The answer must distinguish:

1. curvature components written in an unspecified moving frame;
2. curvature components evaluated in an already supplied orthonormal coframe; and
3. curvature components accompanied by a lawful rule for all horizontal derivatives and vertical
   Lorentz-frame changes.

Only item 3 is a genuine Cartan realization input. Item 1 is incomplete. Item 2 already presupposes
the metric whose realization was supposedly being sought.

## 2. The ten-dimensional frame-bundle coframe

Let `(M,g)` be a local time-oriented Lorentz four-manifold and let `P -> M` be its local
orthonormal-frame bundle. On `P`, the four solder forms `theta^a` and six independent
metric-compatible connection forms satisfying
`omega_ab=eta_ac omega^c_b=-omega_ba` together form a coframe. They satisfy

```text
d theta^a = -omega^a_b wedge theta^b,
d omega^a_b = -omega^a_c wedge omega^c_b
              +(1/2) R^a_bcd theta^c wedge theta^d.
```

The first equation is zero torsion. The second defines the curvature components relative to the
moving orthonormal frame. Neither equation assigns numerical values to `R`.

## 3. First exterior closure: algebraic Bianchi

Apply `d` to the torsion equation. In covariant form,

```text
0 = D^2 theta^a = Omega^a_b wedge theta^b,
Omega^a_b=(1/2)R^a_bcd theta^c wedge theta^d.
```

Therefore

```text
R^a_[bcd] = 0.
```

Before this closure, a metric-compatible curvature two-form has

```text
dim(Lambda^2 V* tensor so(1,3)) = 6*6 = 36.
```

The exact exterior map `Omega^a_b -> Omega^a_b wedge theta^b` has rank 16. Its kernel therefore
has dimension 20, exactly the algebraic Riemann-curvature module in four dimensions.

This is the G227 same-event module, now obtained as `d^2 theta=0` rather than introduced as a
standalone tensor space.

## 4. Second exterior closure: differential Bianchi

Apply `d` to the connection equation. In covariant form,

```text
D Omega^a_b = 0,
```

or, in components,

```text
R^a_b[cd;e] = 0.
```

A first derivative of algebraic curvature initially has `4*20=80` components. The exact
differential-Bianchi symbol has rank 20 and leaves a 60-dimensional kernel. This is precisely the
G228 first-variation module.

## 5. Curvature-component carry is part of the input type

With all curvature indices lowered and with `nabla e_a=omega^p_a e_p`, component differentiation
is

```text
d R_abcd
 = R_abcd;e theta^e
   +omega^p_a R_pbcd
   +omega^p_b R_apcd
   +omega^p_c R_abpd
   +omega^p_d R_abcp.
```

This formula exposes two distinct kinds of carry:

- `R_abcd;e` supplies horizontal change from event to neighboring event;
- the four `omega` terms supply the vertical Lorentz action when the orthonormal frame changes at
  the same event. This action is canonical once `R` is typed as an `SO(1,3)` tensor; it is not a
  second freely chosen derivative law.

A table of bare moving-frame values `R_abcd(x)` is incomplete unless its principal moving frame,
canonical Lorentz action, and horizontal derivative law have been declared. Consequently, an
untyped bare `R` table is not a closed Cartan input.

## 6. Third closure: the nonlinear Ricci commutator

Use the frozen convention

```text
[nabla_f,nabla_e] = nabla_f nabla_e - nabla_e nabla_f.
```

For an all-lower curvature tensor,

```text
[nabla_f,nabla_e] R_abcd
 = -R^p_afe R_pbcd
   -R^p_bfe R_apcd
   -R^p_cfe R_abpd
   -R^p_dfe R_abcp.
```

Thus the antisymmetric part of `nabla^2 R` is not freely specifiable; it is an affine translation
fixed quadratically by `R`. The differentiated differential-Bianchi symbol has rank 80. The
commutator symbol has rank 120. Their combined rank in the 320-dimensional ordered second-
derivative arena is 194, leaving a 126-dimensional compatible affine target.

G231 reproduces the complete G230 count:

```text
320 - 194 = 126.
```

The constant-curvature control passes algebraic Bianchi and closes with zero first/second
horizontal derivatives, zero curvature action on itself, and zero vertical Lorentz action. The
explicit non-space-form symmetric-bivector witness `R_(01)(02)=R_(02)(01)=1` passes algebraic
Bianchi but has nonzero quadratic commutator. It therefore proves that deleting the nonlinear term
changes the regional closure problem.

## 7. Recursive prolonged system

Write `R^(k)=nabla^k R`. At every order the realization data must contain:

```text
d R^(k) = horizontal R^(k+1) terms
          + vertical Lorentz action on R^(k),
```

subject to:

- algebraic symmetries inherited from curvature;
- differentiated Bianchi identities;
- Ricci commutators that exchange adjacent covariant-derivative slots;
- compatibility among all consequences obtained by further differentiation.

These equations constrain the allowed score. They do not select the values of any `R^(k)`.

## 8. The input trilemma

### Bare moving-frame curvature

```text
input = {R}
status = INCOMPLETE
```

There is no typed principal moving frame and no owned horizontal derivative law. The vertical
action would be canonical after `R` is declared an `SO(1,3)` tensor, but an untyped table does not
yet own that equivariant action. Writing arbitrary component functions without these data does not
define a frame-independent exterior system.

### Curvature relative to a supplied coframe

```text
input = {theta, omega, R}
status = EVALUATIVE_ALREADY_HAS_METRIC
```

The solder form reconstructs `g=eta_ab theta^a theta^b`, while the torsion-free connection is its
Levi-Civita connection. This is a lawful evaluator, but it cannot be advertised as deriving that
same metric from curvature.

### Curvature plus classifying derivative data

```text
input = {R typed as an SO(1,3) tensor, horizontal derivative law,
         principal SO(1,3) action, smooth anchor and structure functions,
         regularity, full G-structure-algebroid identities and equivariance}
status = TYPED_CARTAN_REALIZATION_PROBLEM
```

For a finite-dimensional classifying manifold, smooth anchor/structure functions, regularity, and
the full `SO(1,3)`-equivariant `G`-structure-algebroid identities and action conditions, standard
Cartan-realization theory supplies a conditional local `G`-realization. The standard construction
permits an effective orbifold quotient under a locally free action; an ordinary Lorentz manifold
requires a free principal action/trivial isotropy.

When the data require an infinite PDE prolongation, the available theorem gives an analytic local
**coframe** realization of a formally integrable relative algebroid. Principal-`SO(1,3)`
equivariance and descent to a Lorentz metric are not supplied by that theorem and remain open.

## 9. Theorem boundary

The following statements are deliberately separate.

| Statement | G231 status |
|---|---|
| The closure stages G227, G228, and G230 are reproduced; G229 is their metric-jet bridge | `DERIVED_EXACT` |
| Bare moving-frame `R` is a complete regional input | `REFUTED_BY_TYPE_AND_EXTERIOR_CLOSURE` |
| Fully regular finite `SO(1,3)` `G`-structure-algebroid data have local `G`-realizations | `STANDARD_CONDITIONAL_LOCAL_THEOREM` |
| Analytic formally integrable relative-algebroid data have local coframe realizations | `STANDARD_CONDITIONAL_ANALYTIC_COFRAME_THEOREM` |
| Infinite-route principal-`SO(1,3)` descent to a Lorentz metric | `OPEN` |
| Arbitrary smooth infinite curvature prescription has a local realization | `NOT_CLAIMED` |
| A local realization extends globally | `NOT_CLAIMED` |
| The identities generate curvature values or a UDT physical history | `NOT_DERIVED` |

The finite-dimensional `G`-structure-algebroid route is standard for regular finite-type geometric
structures. The analytic formally-integrable route is a distinct coframe/PDE theorem and must not
be silently upgraded to a principal Lorentz bundle, generic smooth realization, or global
existence.

## 10. Exact result

```text
CARTAN_REGIONAL_BRIDGE__BARE_R_NOT_CLOSED__CLASSIFYING_DERIVATIVE_DATA_REQUIRED
```

G231 identifies the correct local integration architecture. The apparent chain of one-more-jet
questions is the beginning of one exterior differential system. That is a real simplification.
The remaining open object is correspondingly sharper: UDT still needs the metric-native values or
classifying derivative law that the Cartan machine is to integrate. G231 does not invent that law.
