# Audit report — intrinsic defect transport atlas

## Result

The frozen complete-cell metric supplies two sharply different transport stories.

First, the intrinsic defect line is globally simpler than its local pictures suggest. The three
great-circle obstruction set is a two-vertex/six-edge graph whose complement has `H1=Z^5`, but the
line has an explicit global nonzero lift. Its first Stiefel-Whitney class is zero and its projected
metric holonomy is the identity on every loop. Around every regular defect edge the representative
vector still turns once and its ambient derivative has a `1/rho` meridional singularity. That local
turning is real geometry, but it is not nontrivial projective monodromy or a charge.

Second, the Lorentzian plane spanned by the clock and the defect line has a nontrivial metric
connection:

```text
omega_E=(q_T/2)(n3 theta2-n2 theta3),
q_T=2a/(sqrt(u)F).
```

In the distinguished metric-anchored `(T,n)` frame, the connection is nonzero throughout the
continued domain because the parent audit proved that the line is never purely ruler-aligned. A
general `SO(1,1)` frame change would change the connection one-form; its curvature is the invariant
object. That curvature is exactly nonzero at both preregistered rational points for all six full
candidates. The four registered screen/`lambda` configurations have distinct exact sampled
curvature coordinate triples at both points; this is not a global signature. The `a=4,5` controls
scale the `a=1` connection and curvature by exact factors four and five.

## Honest status

This is a bounded, metric-led, stationary/off-shell geometric atlas.

- `DERIVED_EXACT`: graph topology, global lift, trivial `w1`, trivial real-line connection and
  holonomy, pole puncture census, metric-anchored kernel-plane connection formula, and exact twist
  scaling.
- `DERIVED_LOCAL`: regular-edge vector turning and its `1/rho` meridional leading behavior.
- `OBSERVED_EXACT_BOUNDED`: nonzero and distinct kernel-plane curvature triples at two exact points.
- `OPEN`: the global zero set of that curvature, finite path holonomies, pole turning asymptotics,
  full Levi-Civita holonomy, and every physical interpretation or selection.

## What this rules out

The attractive visual winding around the defect graph cannot honestly be promoted into a
nonorientable line, a `Z2` charge, or a Hopf carrier. The global lift explicitly defeats that
interpretation in this family. Likewise, nonzero point curvature cannot be promoted into a known
finite-loop holonomy.

## What it newly exposes

The complete metric nevertheless supplies a genuine differential coupling: the clock/defect plane
connection depends on both the clock twist and the full angular-screen geometry. This is a more
structured geometric object than the defect line alone, and its branch dependence is exact. It is
still not an equation of motion, selector, source, or substrate theorem.

## Controls and limits

The calculation retained all 18 candidates: six full, nine intrinsic-zero, two projector-blocked,
and one degenerate. It retained all six graph edges, six equatorial crossings, and both six-puncture
pole links. It used no GPU, fit, ODE/PDE, relaxation, action, source, carrier, density, or outcome
retuning.

The exact evidence is in `EXACT_DERIVATION.md`, `EDGE_ATLAS.tsv`, `TOPOLOGY_ATLAS.tsv`,
`CONNECTION_POINTS.tsv`, `CANDIDATE_TRANSPORT_ATLAS.tsv`, and `TRANSPORT_RESULT.json`.

## Maximum conclusion

The registered complete-cell metric has a globally orientable intrinsic defect line with trivial
line holonomy but nontrivial local ambient turning, plus a distinct clock/line plane whose
metric-derived connection is nonzero in its distinguished anchored frame and has locally
branch-dependent curvature. Nothing here selects matter, charge, a carrier, a physical background,
or a preferred universe branch.
