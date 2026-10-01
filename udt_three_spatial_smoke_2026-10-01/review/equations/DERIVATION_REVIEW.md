# TDS1 independent equation review — construction stage

Reviewer: `/root/tds_equations`, fresh separate context, inherited parent model.
The parent supplied the intended equation and scope before this review. This is
independent argument and a separately implemented scalar-loop NumPy calculation,
not a different-model review. No producer implementation was available or imported
for the initial checks. Later code/history reviews require their own exact bindings.

Startup attribution: parent reports continuing synchronized `grok` at
`d65a7ea0faa0e38b9b1ad5ed5e3743be5178288d`, normal verifier PASS and prior unchanged-
source full406 SMK1 audit PASS. Reviewer independently checked current HEAD and
status; no tracked edits were present, the TDS1 directory and unrelated preexisting
untracked material were present. Protected payloads were not opened. Read the TDS1
work order, central R9/R10/R11/R12N and current G312 authority. They permit the
conditional Ric=0 comparison; they do not identify the native response with Ricci.

## Reduced equation and exact algebraic boundary

Use signature (-,+,+,+), coordinate derivatives, and
`Gamma^a_mn = g^ab (d_m g_bn + d_n g_bm - d_b g_mn)/2`.
Write `C_m = g_ma g^bc Gamma^a_bc`. For arbitrary smooth metric jets, define

```
E_mn = g^ab d_a d_b g_mn
     + (d_n g^ab)(d_a g_mb) + (d_m g^ab)(d_a g_nb)
     + 2 Gamma^a_bn Gamma^b_am.
```

Direct expansion of the Christoffel definition in the original Ricci tensor gives

```
E_mn = -2 Ric_mn + d_m C_n + d_n C_m - 2 Gamma^a_mn C_a.
```

Thus `E=0` and harmonic constraints `C=0` throughout a smooth slab imply Ric=0.
An arbitrary solution of the reduced wave equation alone need not solve Ric=0.
Initial harmonic constraints and the Einstein initial constraints are both needed
for the continuum propagation argument. Numerical constraint errors are not removed
by that continuum theorem and must be measured directly in the saved histories.

This agrees with the vacuum, zero-source specialization of equation9 in
[Pretorius, gr-qc/0407110v2](https://arxiv.org/pdf/gr-qc/0407110): his source H is
`-C`, so the displayed source terms yield the same sign. His source is used only
as a mathematical method reference, not a UDT premise. The tensor contraction,
mixed time-space terms, and nonlinear inverse derivatives must all remain in the
implementation when general spatial dependence is released.

## Harmonic initial velocities

At the initial slice set alpha=1 and beta=0 as supplied gauge data. With
`K_ij=-L_n gamma_ij/2`, use

```
g_00=-1, g_0i=0, g_ij=gamma_ij,
d_t g_ij=-2 K_ij,
d_t g_00=2 tr_gamma K,
d_t g_0i=gamma_ij gamma^kl (3)Gamma^j_kl.
```

Substitution into `C^0` gives `d_t g_00/2-tr K=0`. Substitution into `C^i`
gives `-gamma^ij d_t g_0j+gamma^kl (3)Gamma^i_kl=0`. These are exactly the
four harmonic conditions at the initial slice. In lapse/shift language,
`d_t alpha=-tr K` and `d_t beta^i=gamma^kl (3)Gamma^i_kl` there. In the conformal
seed gamma=psi^4 delta, the lower time-space velocity simplifies to
`d_t g_0i=-2 d_i log psi`. Neither zero shift velocity nor zero lapse velocity
is generally compatible with harmonic coordinates.

For a flat conformal seed and CMC tau in the Lambda=0 comparison, a TT tensor
`Abar` gives

```
gamma_ij=psi^4 delta_ij,
K_ij=psi^-2 Abar_ij+(tau/3) gamma_ij,
-8 Delta psi-|Abar|^2 psi^-7+(2 tau^2/3) psi^5=0.
```

This is the R11 conformal formula under the stated restricted seed assumptions.
Independent original Hamiltonian/momentum checks remain necessary; solving a
mistyped conformal equation or checking it with the same code is insufficient.
Three wavevectors spanning R^3 remove a common constant translation from a
nondegenerate Fourier seed; merely two non-collinear directions do not. Such a
rank diagnostic does not prove absence of every nonlinear Killing field.

## Independent checks completed

`independent_jets.py` uses explicit scalar loops for Christoffels, their derivatives,
Ricci, the reduced equation and harmonic constraints. It does not import producer
code or Torch. Twelve deterministic random Lorentz metric2-jets check the full
off-constraint identity, so success is not restricted to zero-curvature controls.
Twelve arbitrary positive-definite spatial1-jets and symmetric K tensors check
the harmonic initial velocities. Sign reversal of the lapse velocity is detected.

Two analytic controls are checked from explicit metric jets:

* Harmonic Kasner: `ds^2=-exp(2s)ds^2+sum_i exp(2p_i s)dx_i^2`, with
  `p=(-2,3,6)/7`, sum p=sum p^2=1. Changing the quadratic condition is detected.
* Oblique gauge wave: unit n=k/|k|, k=(1,2,2),
  `g=eta+(F-1)(-dt^2+(n dot dx)^2)`,
  `F=1-.13 sin(k dot x-|k|t)>0`. This rotated finite-amplitude flat metric
  has zero Ricci and harmonic constraints but nonzero coordinate derivatives.
  Its role follows the gauge-wave control in
  [Alcubierre et al., gr-qc/0305023](https://arxiv.org/pdf/gr-qc/0305023).

`INDEPENDENT_JETS_RESULT.json` records exact numerical maxima and source hash.
The maximum random-jet identity error is5.56e-16; original Ricci, reduced equation,
C and dC in the analytic controls are below7e-16. These are floating-point algebra
checks, not formal proof, independent integration, or convergence of saved histories.
Captured execution used0.133s and32472KiB within180s/2GiB, CPU only.

Initial disposition: equation/sign and initial-gauge construction supported under
the explicit conditional comparison premises. Numerical implementation, nontrivial
initial constraints, actual outputs, refinement and production readiness are not
yet reviewed by this construction-stage record.
