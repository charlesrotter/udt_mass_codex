# Reciprocal Metric Null-Line Selector — Audit Report

Date: 2026-07-19
Mode: preregistered, CPU-only, exact symbolic metric audit
Base: `e76d748881e6a091ce367a4c11db640700724bfb`
Preregistration: `9fc890a5074f016917272b1b37b3681cedff2d53`

## Result first

```text
NONTRIVIAL_STATIC_NULL_DPHI_EXCLUDED_WITHIN_POSITIVE_SPATIAL_STATIC_SUBFAMILY;
TIME_LIVE_NULL_DPHI_OPTIONAL_EIKONAL_BRANCH;
ROUND_ANGULAR_WARPED_FAMILY_PETROV_D_OR_O_CONDITIONAL;
RECIPROCAL_ANISOTROPIC_PETROV_I_COUNTERFAMILY_EXISTS;
UNIQUE_REPEATED_PND_UNDERDETERMINED;
GLOBAL_CONFORMAL_NULL_LINE_NOT_DERIVED
```

The reciprocal metric has now eliminated the two most immediate ways it might have selected one
light direction without a new law. A static dilation gradient cannot be a nonzero null direction.
A time-live dilation gradient can be null, but only when it obeys an additional eikonal equation.
The angular sector is decisive rather than decorative: the tested static common round warp supplies
an unordered pair of repeated null directions or none, while an equally reciprocal anisotropic transverse metric
has four simple principal null directions. The present foundation therefore does not choose one.

This is not an unconditional no-go. The counterfamilies satisfy the tested reciprocal kinematics;
they are not certified solutions of a complete UDT action, because that action is still open. A
future native equation could restrict the angular sector to an algebraically special family. No
current equation does so.

## 1. Exact causal type of `d phi`

Use the registered local reciprocal representative, retaining an arbitrary positive angular block:

\[
 ds^2=-c^2e^{-2\phi}dt^2+e^{2\phi}dr^2+q_{AB}dx^A dx^B,
 \qquad q_{AB}>0.
\]

The inverse-metric norm is

\[
 P\equiv g^{-1}(d\phi,d\phi)
 =-\frac{e^{2\phi}}{c^2}\phi_t^2
  +e^{-2\phi}\phi_r^2
 +q^{AB}\phi_A\phi_B .
\]

For `q_AB=[[a,b],[b,d]]` with `a>0` and `Delta=ad-b^2>0`, the angular term is explicitly

\[
 q^{AB}\phi_A\phi_B
 =\frac{\phi_1^2}{a}
 +\frac{(a\phi_2-b\phi_1)^2}{a\Delta}\geq0.
\]

This expression comes from an explicit symbolic inverse of the full four-by-four metric block; it
is not installed as a definitional placeholder.

Under a smooth positive nondegenerate Common-Scale change `g -> Omega^2 g`, `P -> Omega^-2 P`. Its
sign and zero set are therefore conformally well typed within that scope.

### Static branch

For `phi_t=0`,

\[
 P=e^{-2\phi}\phi_r^2+q^{AB}\phi_A\phi_B\geq0.
\]

Because `q_AB` is positive, equality requires `phi_r=phi_A=0`. Then `d phi=0`, which defines no
projective line. Thus every nonzero static dilation gradient is spacelike, including one with
angular dependence. The angular sector strengthens the positive obstruction; it does not cancel it.

At the registered static seal, `phi=0`, `phi_t=0`, and

\[
 P_{\rm seal}=\phi_r^2+q^{AB}\phi_A\phi_B.
\]

The finite-cell canon leaves the normal derivative free. If it is nonzero the gradient is
spacelike; if every derivative vanishes, the gradient disappears. The static seal therefore does
not select a null line. This says nothing about the still-open time-on seal conditions.

### Time-live branch

With no angular gradient, nullness becomes

\[
 \phi_t=\pm c e^{-2\phi}\phi_r.
\]

With angular variation,

\[
 \phi_t^2=c^2e^{-4\phi}\phi_r^2
 +c^2e^{-2\phi}q^{AB}\phi_A\phi_B.
\]

These are eikonal equations, not identities implied by `g_tt g_rr/c^2=-1`. An exact nontrivial
local radial solution is

\[
 \phi(t,r)=\frac12\log\!\left(\frac{A+2ck t}{B-2kr}\right),
\]

where numerator and denominator are positive. The same reciprocal form also admits timelike and
spacelike first jets. Hence null `d phi` is a real candidate branch, but Reciprocity does not select
that branch, its sign, boundary data, or global continuation.

## 2. What the checked round angular family actually selects

The runnable constructor covers the conditional static reciprocal round-sphere family

\[
 ds^2=-e^{-2p(r)}dt^2+e^{2p(r)}dr^2
 +R(r)^2(d\theta^2+\sin^2\!\theta\,d\varphi^2).
\]

At an arbitrary regular radial point, denote the local two-jets by
`p0,p1,p2,R0,R1,R2`, with `R0>0`. Exact Newman-Penrose contraction gives

\[
 \Psi_0=\Psi_1=\Psi_3=\Psi_4=0,
\]

\[
 \Psi_2=-\frac{e^{-2p_0}}{6R_0^2}
 \left(2R_0^2p_1^2-R_0^2p_2+2R_0R_1p_1-R_0R_2+R_1^2-e^{2p_0}\right),
\]

up to the conventional overall Riemann/NP sign. Because the two-jets are arbitrary, this zero
pattern covers the whole regular static family rather than one numerical witness.

Therefore:

- `mathcal W != 0`: Petrov D, with two distinct double base-null directions;
- `mathcal W = 0`: Petrov O, with vanishing Weyl tensor and no Weyl-selected direction.

The missing high-degree terms in the projective PND polynomial encode the second double root at
infinity; `6 Psi2 z^2` must not be misread as one unique ray. Type II, III, or N cannot occur inside
this nondegenerate common-warp family. At a D-to-O locus the displayed radial pair may remain as a
coordinate splitting, but Weyl curvature stops selecting it.

This checked theorem is `CONDITIONAL`: staticity and the round common warp are pinned by habit. It is
not the unrestricted time-live angular sector allowed by the frozen UDT ledger. A fresh analytic
review derived the familiar broader 2+2 warped D/O reduction, but the banked runnable claim here is
deliberately limited to the static reciprocal family displayed above.

## 3. Exact anisotropic reciprocal counterfamily

On a finite local radial interval, set `c=1` by the constant time-unit convention and take

\[
 \phi=r,\qquad
 ds^2=-e^{-2r}dt^2+e^{2r}dr^2+e^{4r}dx^2+e^{6r}dy^2.
\]

The metric is nondegenerate and has positive transverse block. It exactly preserves the reciprocal
temporal/radial product. At `r=0`, `phi=0` with free nonzero normal derivative, consistent with the
limited static-seal datum. It is a local kinematic family; no claim of global fold completion is
made.

Exact Christoffel-Riemann-Ricci-Weyl contraction gives, at `r=0`,

\[
 \Psi_0=\Psi_4=-\frac54,\qquad
 \Psi_1=\Psi_3=0,\qquad
 \Psi_2=-\frac{13}{12}.
\]

The PND polynomial is

\[
 Q(z)=-\frac14(z^2+5)(5z^2+1),
\]

with four simple roots `z=+-i sqrt(5), +-i/sqrt(5)`. Its quartic discriminant is `32400`. The
independent speciality invariant test gives

\[
 I=\frac{61}{12},\qquad J=-\frac{91}{216},\qquad
 I^3-27J^2=\frac{2025}{16}\ne0.
\]

Thus this metric is exactly Petrov I, not II, III, D, N, or O. A fresh adversarial review reported a
separate orthonormal-frame reproduction; the checked-in independent verifier separately recomputes
the coordinate curvature, NP scalars, PND polynomial, and discriminant without importing the
constructor.

The transverse metric is the point of the counterexample. The reciprocal identity controls the
clock/parallel pair but imposes no equality on the two transverse warp rates. Therefore it cannot,
by itself, enforce the algebraic speciality needed for one repeated PND.

## 4. The still-live algebraically special route

Petrov II, III, and N do have one locally distinguished highest-multiplicity projective null line:
a double, triple, or quadruple PND respectively. The exact root multiplicities were checked. But
three additional gates remain:

1. a native equation must force one of those strata rather than D, O, I, or type-changing mixtures;
2. the chosen line must continue smoothly through zeros and type transitions;
3. its propagation and physical soldering must be derived.

A principal null direction is not automatically geodesic from Petrov algebra alone. No Einstein
condition, GR field equation, or Goldberg-Sachs theorem was imported. The prior transport audit
showed that conformal geometry propagates any chosen null ray projectively; it does not choose the
initial ray.

## 5. Bootstrap and finite-cell audit

The current bootstrap principle says that admissible laws and matter must be realized together in a
globally self-consistent solution. It does not yet supply an action, admissibility functional,
boundary variation, or branch-ranking equation. The finite mirrored-cell canon supplies topology
and the limited static `phi` parity/seal datum, but it does not choose a Petrov class or eikonal
branch. Neither text can currently discard the Petrov-I counterfamily or select the time-live null
gradient without adding the missing operator.

Consequently the finite-cell cap gate was not activated. No period, charge, carrier, mass, or action
conclusion follows from this audit.

## 6. Premise audit

| Input | Status in this audit |
|---|---|
| Positional dilation, Reciprocal-c, dual Reciprocity, CSN | `FOUNDING` |
| Exponential reciprocal representative | `DERIVED / CONDITIONAL` |
| 4D conformal-Lorentzian and Petrov readout | `INHERITED / CONDITIONAL` |
| Positive angular metric `q_AB` | `free-and-explored` within the block representative |
| Staticity | `CHOSE / CONDITIONAL SUBFAMILY` |
| Time-live eikonal condition | `free branch`, not an equation of motion |
| Round common warp | `pinned-by-HABIT / CONDITIONAL` |
| Anisotropic rates `(1,2,3)` | `CHOSE / COUNTERFAMILY` |
| Petrov class | `OBSERVED` exact curvature readout per family |
| Static seal value/parity | `CANONIZED / LIMITED SCOPE` |
| Action, source, boundary variation, bootstrap operator | `OPEN` |
| Carrier, physical section, periods, caps | `OPEN / EXCLUDED` |

The chosen counterfamily parameters demonstrate existence, not a preferred universe. The spherical
and anisotropic families do not exhaust all angular geometries. The 32 controller checks are
mechanical identities and fail-closed classification gates, not 32 independent physical facts.

## 7. Four evidence gates

1. **Preregistered:** yes, before curvature algebra, commit `9fc890a`.
2. **Full or bounded scope:** bounded and explicit. The static norm conclusion is complete within the
   positive-spatial block; the Petrov census covers the static reciprocal round common-warp theorem plus one exact
   anisotropic counterfamily, not every metric or on-shell solution.
3. **Independent verification:** yes. Fresh read-only adversaries independently derived the general
   `d phi` census, a broader warped D/O reduction, and the anisotropic Petrov-I invariants. The
   checked-in package verifier separately reconstructs the causal norm, eikonal solution, static
   spherical D witness, anisotropic coordinate curvature, and PND algebra, plus mutation catches.
4. **Every premise audited:** yes, in the table above and `STATUS_LEDGER.tsv`.

The result is therefore banked as `VERIFIED-WITH-CAVEATS`: strong kinematic underdetermination, not a
complete-dynamics no-go.

## 8. What this changes

The next missing object is more precise. It is not merely “some angular math.” UDT needs a native,
conformally admissible equation that correlates the reciprocal `phi` sector with the angular Weyl
structure strongly enough to choose an on-shell algebraic class or eikonal branch. If such an
equation forces II, III, or N and survives the global gates, a unique null line could emerge. If it
instead permits the exact I/D/O alternatives retained here, this route cannot close the carrier
bridge.

No further derivation, action construction, time-live solve, carrier adoption, GPU work,
canonization, repository reorganization, or startup-control edit was performed.
