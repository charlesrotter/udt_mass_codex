# G85 exact derivation — mixed time-live completion archetypes

## 1. Result first

The G84 mixed-branch obstruction is not a generic obstruction to a smooth complete metric. It is
an obstruction to retaining too few complete-metric channels at the candidate seam.

For every one of the `196` nonzero-mixing AM controls:

- retaining only the stationary mixing, or making only that mixing time-dependent, remains
  degenerate at the equatorial axial fixed set;
- a smooth nonvanishing clock-radial shift gives a regular Lorentzian metric on the declared
  `R x S^3` candidate while preserving the exact G75 north cell;
- a smooth negative clock-norm lift also gives a regular Lorentzian metric but removes the
  stationary lapse-zero asymptote; and
- tapering the angular mixing at least as fast as the lapse gives a smooth uniformly null seam,
  with a local zero-shift bifurcate realization or a global shift-supported realization.

These are mutually distinct kinematic completions. The current metric identities select none of
them. The exact landing is

```text
COMPLETE_METRIC_CHANNELS_ADMIT_MULTIPLE_KINEMATIC_COMPLETION_CLASSES
__NO_NATIVE_HISTORY_SELECTED.
```

## 2. General seam algebra

On the G84 minimal doubled spatial candidate, consider the complete-metric slice

```text
ds^2/R^2 = u dτ^2 +2b dτdχ +4dχ^2
           +D dθ^2+C dψ^2+2H dτdψ,
D=4sin(χ)^2,
C=D sin(θ)^2,
H=h sin(θ)^2.
```

The frozen stationary continuation is `u=-cos(chi)^2`, `b=0`, and
`h=4sin(chi)^2 q(4sin(chi)^2)`. The spatial `chi,theta,psi` block is positive away from ordinary
polar-coordinate fixed sets. Direct expansion gives

```text
det(g/R^2) = D[(4u-b^2)C-4H^2],                    (1)

S_time = u-b^2/4-H^2/C.                            (2)
```

At either axial fixed point, the axial one-form vanishes. The invariant clock-radial block is

```text
G_H = [[u_H,b_H],[b_H,4]],
det G_H = 4u_H-b_H^2.                              (3)
```

Since the radial direction is positive, the local regular-Lorentz condition is

```text
4u_H-b_H^2 < 0.                                    (4)
```

Equation (4) is pointwise. Time derivatives of `h` cannot change it. This is why turning on time
without turning on another metric channel does not repair G84.

## 3. Causal type of the candidate seam

The induced metric on `chi=pi/2` has determinant

```text
det(g_seam/R^2) = D(u_H C-H^2).                     (5)
```

For the lapse-zero classes `u_H=0`:

- if `h_H!=0`, equation (5) is negative off axis, so the seam is timelike there; at the axial
  fixed set `H=0`, it becomes null;
- if `h_H=0`, the induced metric is degenerate at every angular point, so a regular ambient
  completion has a uniformly null seam.

Thus nonzero angular mixing and a uniform horizon-like seam are incompatible within this declared
metric block at `u_H=0`. A radial shift repairs the ambient metric but does not change the induced
seam metric, so it does not make the nonzero-mixing seam uniformly null.

If `u_H<0`, equation (5) is negative everywhere after regular angular coordinates are used. The
seam is timelike, and the stationary lapse-zero asymptote has been removed.

## 4. Constructive time-live global witnesses

Let `chi_0=pi/6`, the exact edge of the inherited G75 north cell, and choose
`chi_1` with `chi_0<chi_1<pi/2`. A `C-infinity` gate can be made from

```text
eta(y)=0                    for y<=0,
eta(y)=exp(-1/y)            for y>0,
S(y)=eta(y)/(eta(y)+eta(1-y)),
W(chi)=S((chi-chi_0)/(chi_1-chi_0))
       S(((pi-chi)-chi_0)/(chi_1-chi_0)).           (6)
```

Then `W=0` on the registered north cell and near the south pole, while `W=1` in a band containing
the equator. The numerical verifier uses the corresponding `C2` quintic gate; equation (6) proves
that no finite differentiability compromise is needed for existence.

### 4.1 Clock-radial shift family

For arbitrary `B>0`, `|epsilon|<1`, and real `omega`, set

```text
b(τ,chi)=B W(chi)[1+epsilon sin(omega τ)],
u=-cos(chi)^2.                                      (7)
```

At the seam, `b_H` never vanishes and equation (4) is strictly negative. Away from the seam,
`u<0` already gives the correct signature. Near the poles `W=0`; the mixing one-form is smooth
because

```text
h sin(theta)^2 dψ=q(r^2)(X dY-Y dX),                (8)
```

with `r=2sin(chi)`. Equations (6)--(8) therefore define a smooth, time-live Lorentz metric on the
declared `R x S^3` candidate for every frozen polynomial `q`. It equals the G75 control exactly on
its authoritative cell.

The condition `b_H(t)!=0` is load-bearing. If it crosses zero while `u_H=0`, the axial degeneracy
returns at that time.

### 4.2 Clock-norm lift family

For arbitrary `L>0`, `|epsilon|<1`, and real `omega`, set

```text
u=-cos(chi)^2-L W(chi)[1+epsilon sin(omega τ)],
b=0.                                                (9)
```

Now `u_H<0`, so equations (2)--(5) give a smooth Lorentz metric and a timelike seam. This family
also preserves the inherited north cell. It does not preserve the candidate lapse-zero asymptote;
that is a classification, not a defect.

### 4.3 Mixing-taper families

Because continuation beyond `chi_0` is free, define a smooth continuation equal to the frozen
mixing on the inherited cell and satisfying

```text
h=A h_tilde,   A=cos(chi)^2                         (10)
```

near the seam. A stronger explicit witness sets `h=0` on an equatorial band by using (6).

For the zero-shift bifurcate chart, use the G84 coordinates

```text
U=2cos(chi)e^(-τ/2),
V=2cos(chi)e^(+τ/2),
A=UV/4,
dτ=dV/V-dU/U.
```

Then

```text
h dτ=(h_tilde/4)(U dV-V dU),                        (11)
```

which is smooth. Equation (10), not merely `h_H=0`, is the sufficient zero-shift rate condition.
Alternatively, combine the taper with (7); the ambient metric is globally regular in the
`R x S^3` chart and equation (5) gives a uniformly null seam.

## 5. Full frozen census

The production and independent implementations parse the original rational polynomials rather
than trusting the G84 count. They reproduce:

```text
196 mixed profiles,
104 q(4)>0,
 92 q(4)<0.
```

Their inherited behavior classes are `24` center-off, `20` endpoint-tapered, `36` sign-changing,
`112` persistent-sign, and `4` zero-at-both-original-boundaries. Each appears under all five
archetypes, giving exactly `980` unique rows.

The completion result is independent of the sign and magnitude of `q(4)` because the mixing enters
the Schur complement as a negative square. This is an algebraic classification, not evidence that
all profiles are physically equivalent.

## 6. What this does and does not close

G85 closes the narrow question left by G84: nonzero mixing is not globally dead. It can coexist
with a smooth complete metric once other complete-coframe channels are allowed. It also sharpens
the candidate asymptote question: keeping nonzero seam mixing prevents `chi=pi/2` from being one
uniform null observer wall in this class.

But the locally jet-open complete coframe admits all these histories. Maurer--Cartan compatibility
does not choose among them, and no native evolution/global-selection law is supplied. Therefore
G85 derives neither the physical continuation nor physical `X_max`.

No profile, topology, `R`, endpoint, CMB source or observable, action, matter law, bootstrap
closure, boundary functional, or signalling interpretation is selected.
