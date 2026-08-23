# G230 exact derivation — first nonlinear neighboring-tile obstruction

Date: 2026-08-23
Status: `DERIVED_CONDITIONAL__ONE_SUPPLIED_EVENT__FIXED_TANGENT_FRAME`

## 1. Question and exact ceiling

G229 realizes every supplied compatible `(R,nabla R)` by a Lorentz metric 3-jet. G230 asks whether
those lower-order identities are enough when neighboring first-order tiles are compared around an
infinitesimal two-direction square.

Fix a locally inertial frame at one event:

\[
g_{ab}(0)=\eta_{ab},\qquad g_{ab,c}(0)=0,
\qquad \eta=\operatorname{diag}(-1,1,1,1).
\]

Let

\[
L_{ab,cdef}=g_{ab,cdef}(0),
\qquad
E_{feabcd}=(\nabla_f\nabla_eR)_{abcd}(0).
\]

The complete source and preconstraint target dimensions are

\[
\dim L=10\binom{7}{4}=350,
\qquad
\dim E=16\cdot20=320.
\]

This remains a point-jet theorem. It does not prescribe a curvature field over a region or generate
its values.

## 2. Linear highest-derivative map

Differentiating the G229 curvature convention twice, the part linear in the new fourth metric
derivative is

\[
\boxed{
(C_4L)_{feabcd}
=\frac12\left(
L_{ad,bcef}+L_{bc,adef}-L_{bd,acef}-L_{ac,bdef}
\right).
}
\]

The ordered derivative pair `(f,e)` is retained. Although `C4(L)` is symmetric in that pair, the
complete covariant second derivative is not: its antisymmetric part comes from the lower metric
jet.

Exact rational elimination gives

\[
\operatorname{rank}C_4=126,
\qquad
\dim\ker C_4=350-126=224.
\]

## 3. Intrinsic second-order compatibility

Differentiating the G228 differential Bianchi identity gives

\[
E_{f,eab,cd}+E_{f,abe,cd}+E_{f,bea,cd}=0.
\]

In the reduced 320-slot algebraic-curvature representation these rows have rank 80.

The derivative pair also obeys the Ricci commutator. With the frozen G229 sign convention,

\[
\boxed{
E_{feabcd}-E_{efabcd}
=-R^p{}_{afe}R_{pbcd}
-R^p{}_{bfe}R_{apcd}
-R^p{}_{cfe}R_{abpd}
-R^p{}_{dfe}R_{abcp}.
}
\]

Its homogeneous left-hand matrix has rank 120. Together with differentiated Bianchi, the complete
homogeneous constraint system has rank

\[
\boxed{194},
\]

so its kernel has dimension

\[
320-194=126.
\]

Direct exact multiplication proves

\[
\ker(\text{homogeneous intrinsic constraints})=\operatorname{im}C_4.
\]

Thus no additional linear fourth-order obstruction remains.

## 4. The nonlinear affine offset

Let `H` be the G229 normal metric 2-jet determined by `R`. At the locally inertial event define

\[
A^p{}_{bc|e}=\partial_e\Gamma^p{}_{bc}.
\]

The complete metric readout is affine in `L`:

\[
\boxed{E=C_4(L)+Q(H).}
\]

`Q(H)` contains both:

1. the second derivative of the quadratic Christoffel-product part of the lowered curvature;
2. the covariantization terms `-(partial_f Gamma) R` acting on all four curvature indices.

The production verifier evaluates all 20 diagonal and all 190 cross polarization cases in the
20 curvature coordinates. Because both the affine residual and the commutator right-hand side are
homogeneous quadratic polynomials, those 210 exact cases compare every quadratic coefficient.
Every differentiated-Bianchi and commutator residual is zero.

The smallest nonzero witness is curvature coordinate 1, equivalently the symmetric bivector entry
`Q[(01),(02)]=1`. It gives two nonzero commutator components; the first is exactly `-1`. Setting
`E=0` therefore passes the G227 algebraic curvature gate and the G228 gate with `D=0`, but fails the
G230 overlap condition.

Hence

\[
\boxed{
\text{G227/G228 lower-order compatibility is not sufficient for the next overlap square.}
}
\]

The new term is not an added mechanism or coefficient. It is the metric's own curvature acting on
curvature under Levi-Civita derivative commutation.

## 5. Coordinate kernel and normal slice

An identity-linear fifth-order coordinate change

\[
x^a=y^a+\frac1{120}C^a{}_{bcdef}y^by^cy^dy^ey^f
\]

has `4*56=224` coefficients and changes only the fourth metric jet at this order:

\[
\Delta L_{ij,cdef}=C_{jicdef}+C_{ijcdef}.
\]

Its image has rank 224 and lies in `ker C4`. Therefore

\[
\boxed{\ker C_4=\operatorname{im}G_4.}
\]

The complete fourth-order radial normal-coordinate conditions are

\[
L_{i(j,klmn)}=0.
\]

They have rank 224, leaving a 126-dimensional normal slice. The stacked normal-plus-curvature map
has rank 350, and the normal conditions restricted to the gauge image have rank 224. Thus the
normal slice maps isomorphically onto the compatible 126-dimensional affine translation space and
fixes the fifth-order coordinate gauge uniquely once the tangent frame and lower normal jets are
fixed.

## 6. Independent representation

The independent implementation does not import production or SymPy. It retains all 21 symmetric
bivector slots rather than eliminating algebraic Bianchi. It imposes 16 algebraic-Bianchi rows
explicitly and finds, over each of two finite fields,

| Map | Rank |
|---|---:|
| full 21-slot `C4` | 126 |
| algebraic Bianchi | 16 |
| differentiated Bianchi | 96 |
| derivative commutator | 126 |
| all full-target constraints | 210 |
| quintic gauge | 224 |
| normal rows | 224 |
| stacked normal plus `C4` | 350 |

The modular lower bounds meet the exact upper bounds supplied by kernel inclusion and dimension,
so the rational ranks are certified. A separate exact `Fraction` witness independently verifies
the nonlinear sign and shows why both connection-product and covariantization pieces are needed.

## 7. Landing and boundary

The preregistered landing is

```text
FIRST_NONLINEAR_OVERLAP_OBSTRUCTION__FULL_LOCAL_4JET_REALIZATION
```

Every supplied `(R,nabla R,nabla^2 R)` obeying algebraic curvature symmetry, differentiated
Bianchi, and the nonlinear Ricci commutator has a metric fourth-jet representative at the event.
The statement does not prove that arbitrary pointwise assignments over a finite neighborhood form
one smooth metric, prove convergence of an infinite formal jet, calculate any curvature value,
select observers or transport, derive dynamics, or choose a physical/global history.
