# Observer-centered Xmax/frame correction

Date: 2026-07-23

Preregistration commit: `2ffafce`

Parent preserved unchanged:
`udt_wrl_xmax_lightcone_frame_audit_2026-07-23/`

Compute: CPU-only exact algebra

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

Charles's correction changes the physical interpretation materially.

The WR-L metric still derives a sharp asymptotic limit in an
observer-centered clock/ruler chart:

```text
A=1-r/X=exp(-2 phi),
clock ratio=sqrt(A)=exp(-phi) -> 0,
optical depth=-X log(A)=2X phi -> infinity.
```

But the parent package's “static observer,” “moving observer,” and
“crossing observer” language was not licensed. In the controlling UDT
framing, `r` is a nonnegative separation/depth assigned by an
observer-centered chart. It is not signed absolute position relative to a
preferred cosmic center.

The regular ingoing extension remains exact mathematics. It proves that
the WR-L tensor can be continued as a Lorentzian manifold. It does not
prove that a physical UDT observer crosses `Xmax`.

There is also a new exact obstruction:

```text
R = 6/(X r),
K = 8/(X^2 r^2).
```

These scalars vary injectively with `r`. If two centered charts were
ordinary overlapping charts of the same tensor geometry, scalar
invariance would require

```text
R(r_O)=R(r_P)  =>  r_O=r_P
```

throughout their overlap. A nontrivial change of center is therefore not
a coordinate relabelling of this fixed WR-L tensor.

This does **not** refute no preferred frame. It says the WR-L object
cannot simultaneously be:

1. one ordinary center-based tensor geometry, and
2. the identically recentered chart of every inertial observer.

To realize the owner premise, it must instead be observer-indexed and
relational, or be a bounded sector of a different complete metric. The
required observer composition law is still open.

## What `Xmax` now means in the corrected calculation

Inside the centered observational chart, `A>0` gives

```text
g_tt < 0  (the t channel is the clock channel),
g_rr > 0  (the r channel is the ruler channel).
```

At `A=0` that polarization degenerates. For `A<0`,

```text
g_tt > 0,
g_rr < 0.
```

The same `t` clock and `r` ruler have exchanged causal roles. Therefore
the metric does not admit a continuation through `X` that preserves the
same observer-centered clock/ruler interpretation.

This is the correct metric-level limiting result:

> `X` is uncrossable **within the same centered clock/ruler
> polarization**.

That is stronger than saying a coordinate slope goes to zero and weaker
than deriving a complete global hard edge. The regular ingoing tensor
extension shows that manifold geometry exists beyond the chart; UDT has
not selected whether that extension is another cell, a seam, a quotient,
an inadmissible continuation, or no physical domain at all.

## Why the parent crossing argument was invalid

The parent introduced

```text
v=c_E t+r_star,
ds2_rad=-A dv2+2 dv dr.
```

The determinant is exactly `-1` at `A=0`, and mathematical causal curves
cross the surface. All that algebra survives.

What does not survive is the noun “observer.” A curve in one manifold
chart does not supply:

- a second equivalent observer-centered chart;
- the relation between the two centers;
- the transformation of the full angular sector;
- a pairwise or three-observer composition law; or
- a rule preserving common `Xmax`.

The parent therefore proved manifold extendibility, not physical
observer crossability.

## No preferred frame and the fixed WR-L center

The exact curvature result is load-bearing. Since both `R` and `K`
identify the positive radius, every isometry of the fixed WR-L tensor
preserves its radial level sets. Rotations and time translations may
remain, but a transformation that carries the center to a genuinely
different observer does not.

Consequently, using one fixed WR-L center as the universal physical
center would create precisely the preferred frame Charles excludes.

The allowed conclusions are:

- `DERIVED`: a standard-chart recentering of the fixed WR-L tensor is
  impossible;
- `OWNER_LOCKED`: macroscopic inertial observers remain equivalent;
- `OPEN`: the observer-indexed relational composition or complete metric
  that reconciles those statements.

The result must not be inflated into a no-go theorem for every relational
metric. It is a no-go only for treating this particular nonhomogeneous
WR-L tensor as one normally overlapping, freely recenterable spacetime
chart.

## Inertial and accelerated frames

The connected local coframe group remains exact:

```text
theta0' = cosh(eta) theta0+sinh(eta) theta1,
theta1' = sinh(eta) theta0+cosh(eta) theta1.
```

It preserves the metric and rescales the two null forms reciprocally.
For constant `eta`, this is the local inertial frame equivalence visible
directly in the metric.

For smooth `eta(t,r)`,

```text
omega' = omega-d eta,
d omega' = d omega.
```

Thus a varying or accelerated **coframe presentation** changes connection
components but does not create invariant curvature or change the
invariant cone.

This sharpens Charles's acceleration statement:

- uniform relative motion cannot physically warp the cone;
- acceleration can tilt the cone's coordinate presentation and add
  connection terms;
- a physical acceleration-induced change in the metric would require a
  further UDT response law, which has not been derived;
- no GR gravity–acceleration equivalence is imported.

## Angular correction

The old constant shift `phi -> phi-beta` still fails the complete WR-L
angular block: at the exact witness used in the parent, the radial-time
ratio is `2` while the angular ratio is `4/9`.

The interpretation changes. This is not an obstruction to the
no-preferred-frame principle. It proves only that shifting depth while
holding one center and its angles fixed is not the required recentering
map. A true observer transformation must act on the full relational
radial-angular data.

## Mass precision

The conditional observational readout

```text
e^phi=1/sqrt(A)
```

diverges at the asymptote. Native invariant matter mass does not yet
follow. Without the complete matter functional and source, the divergence
cannot be used as an independently derived dynamical barrier.

The clock/ruler polarization result already makes `X` the limit of the
same observer-centered chart. Native mass closure remains a separate open
problem.

## Four evidence gates

1. **Preregistered:** yes, commit `2ffafce` before recomputation.
2. **Full or bounded:** bounded exactly to the recorded WR-L tensor,
   centered polarization, local coframes, and standard chart overlap.
3. **Independent:** required before banking; the production result is not
   the final verifier.
4. **Premises audited:** yes. Observer ontology, `r`, `c_E`, `Xmax`,
   angular block, mass, acceleration response, and global completion are
   explicit.

## Maximum conclusion

> The WR-L algebra derives a centered relational clock/ruler asymptote at
> `A=0` and no admissible continuation preserving those same channel
> roles. The regular ingoing extension proves manifold extendibility, not
> a physical observer crossing. Distinct observer centers cannot be
> standard overlapping charts of the same nonhomogeneous WR-L tensor.
> Local inertial coframe equivalence is derived, while global observer
> recentering, common physical `Xmax`, and a physical acceleration-response
> law remain open.

No canonization, navigation edit, GPU work, action, carrier, source, mass
closure, or repository reorganization is performed.
