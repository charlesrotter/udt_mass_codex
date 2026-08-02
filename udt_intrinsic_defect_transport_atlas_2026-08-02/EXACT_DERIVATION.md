# Exact derivation — intrinsic defect transport atlas

## Scope and authority

This is an exact CPU, stationary, off-shell calculation on the same frozen 18-candidate
`R x S3` ensemble as the parent distribution audit. Full transport is defined only for
`C04,C08,C09,C10,C16,C17`; the nine intrinsic-zero candidates, two projector-blocked candidates,
and one degenerate candidate remain controls. No action, source, carrier, boundary, density,
physical branch, or time evolution is supplied.

Write

```text
W=dPhi_contact wedge dSigma_contact,
N_flat=star(T_flat wedge W),
L_W=span(N).
```

After canceling the common `q3` factor at the generic equator, the raw coefficient vector is

```text
f=(f12,f13,f23),
f12=q0 q1^2+3 q0 q2^2+2 q1 q2 q3,
f13=q0^2 q1+3 q0 q2 q3-2 q1 q2^2,
f23=3 q0^2 q2-q0 q1 q3+2 q1^2 q2.
```

The result is an atlas of four distinct objects: projective line monodromy, local ambient turning,
the projected metric connection of the line, and the projected Lorentzian connection of
`span(T,N)`. They are not interchangeable.

## 1. The complete obstruction graph and its complement

The parent zero-locus proof implies that the maximal continued domain is

```text
M=S3 minus D,
D=C03 union C13 union C23,
C03: q1=q2=0,
C13: q0=q2=0,
C23: q0=q1=0.
```

The generic equator is included in `M`. Each great circle is split by the shared points
`q3=+1` and `q3=-1`, so `D` is a connected graph with two vertices and six edges. Therefore

```text
b1(D)=E-V+1=6-2+1=5.
```

Alexander duality gives

```text
H1(S3 minus D;Z)=H^1(D;Z)=Z^5.
```

Thus the complement has five independent homology loops. This alone does not make the line bundle
nonorientable and does not supply a charge.

## 2. A global lift trivializes the projective line bundle

For every intrinsic nondegenerate candidate, conversion from `f` to the unnormalized orthonormal
components of `N` is a smooth linear map `L_g`. In the registered component convention its
determinant is

```text
det(L_g)=1/(F^2 u)>0,
```

where `u>0` and the screen area `F>0`. The parent exhaustive zero-locus proof says `f` is nonzero
everywhere on `M`. Hence

```text
N_tilde=L_g f
```

is a continuous global nonzero representative on `M`. Normalizing it gives a global lift
`n:M->S2` of the projective map `[N]:M->RP2`. Consequently

```text
w1(L_W)=0 on every one of the five H1 generators,
line monodromy = identity,
every regular projective meridian is trivial in pi1(RP2)=Z2.
```

This conclusion is global. It is not inferred from point samples.

## 3. Local turning at all six regular graph edges

At a symbolic non-pole base point, the transverse leading matrices have determinants

```text
C03:  3 q0^2(q0^2+q3^2) =  3 q0^2 on S3,
C13:  2 q1^2(q1^2+q3^2) =  2 q1^2 on S3,
C23: -6 q2^2(q2^2+q3^2) = -6 q2^2 on S3.
```

They have rank two on both open arcs of each circle. A small oriented transverse vector meridian
therefore has degree magnitude one. With the frozen domain/image orientations the displayed signs
are `+1,+1,-1`; reversing an orientation reverses the relevant sign, so the signs are not canonical.

The normalized vector turns once. Its image line in the local `RP1` turns twice, and the inclusion
into `RP2` sends that even traversal to the trivial `Z2` class. Therefore all of the following are
simultaneously true:

```text
local vector turning: nontrivial, degree magnitude 1;
local RP1 traversal count: 2;
intrinsic RP2 meridian class: 0;
global line w1: 0.
```

Conflating these statements would manufacture a false topological obstruction.

## 4. The two pole links retain all six incident directions

Near either shared pole, with pole sign `s=+1` or `s=-1` and tangent coordinates `(x,y,z)`, the
quadratic leading map is

```text
(2 s y z, 3 s x z, -s x y).
```

It vanishes on the link sphere exactly at

```text
+/-e0, +/-e1, +/-e2.
```

Thus each pole link is an `S2` with six punctures. No puncture is removed or merged. The global lift
already fixes the projective class of every loop in this link complement; the visually complicated
six-ray junction does not override `w1=0`.

## 5. The line connection is trivial while ambient turning is not

For the global unit representative `n`, metric compatibility gives

```text
Pi_L(nabla_X n)=g(n,nabla_X n)n=0.
```

The projected metric connection of this oriented real line is therefore flat in the global unit
frame, and its holonomy is the identity on every loop.

This does not say that `n` is ambiently parallel. Near a regular edge the normalized transverse
linear map changes by one full vector turn around a meridian. The meridional component of
`(I-Pi_L)nabla n` has `1/rho` leading size as the transverse radius `rho` tends to zero; bounded
Levi-Civita terms cannot cancel that leading angular derivative. This is local extrinsic turning,
not intrinsic line holonomy.

## 6. The Lorentzian kernel-plane connection

Let `E_W=span(T,n)`. The global timelike unit vector `T` and global spacelike unit vector `n`
trivialize, orient, and time-orient this plane bundle on `M`.

For the registered coframe

```text
theta0=u^(-1/2)(dt+a sigma3),
theta2=sqrt(F)(r sigma1+b sigma2),
theta3=sqrt(F) r^(-1) sigma2,
d sigma3=-2 sigma1 wedge sigma2,
```

define the positive signed screen-rotation coefficient (for the registered `a>0` candidates)

```text
q_T=2a/(sqrt(u) F),    Q_T=q_T^2.
```

With the parent exterior-system convention,

```text
t0=-2a/(sqrt(u)F)=-q_T.
```

Before applying the kernel relation, the full metric-anchored connection is

```text
omega_E=-n(phi) theta0-(t0/2)(n3 theta2-n2 theta3).
```

The stationary normalized Killing congruence has no spatial expansion or shear, so its spatial
derivative contributes one half of the spatial two-form. On the rank-two locus,
`i_n(dphi wedge dSigma)=0` and independence of `dphi,dSigma` force both `n(phi)=0` and
`n(Sigma)=0`. Therefore the connection in the distinguished metric-anchored frame `(T,n)` reduces
to

```text
omega_E(X)=g(n,nabla_X T),
omega_E=(q_T/2)(n3 theta2-n2 theta3).
```

Its squared one-form norm is

```text
|omega_E|^2=(Q_T/4)(n2^2+n3^2).
```

All six full candidates have `a!=0`, `u,F>0`, and the parent proved that the nonzero line is never
ruler-aligned. Hence `(n2,n3)` never vanish together and `omega_E` is nonzero everywhere on `M` in
this metric-anchored frame. A general `SO(1,1)` gauge change adds an inhomogeneous frame term to the
connection one-form; this zero/nonzero statement is not promoted to an arbitrary-gauge invariant.
The curvature below is gauge invariant. This is metric transport, not a field equation.

Because `SO+(1,1)` is abelian,

```text
Omega_E=d omega_E
```

is its curvature. Exact first-order jet algebra evaluated all three components at both registered
rational points `p1` and `p2` for all six candidates. All 12 certificates are nonzero. At each
point the four registered screen/`lambda` configurations `C04,C08,C09,C10` give four distinct exact
coordinate triples for the curvature two-form. This sampled distinction is not called a global or
coordinate-free signature. Since `C16` and `C17` differ from `C08` only by `a=4` and `a=5`,
respectively,

```text
omega(C16)=4 omega(C08),  Omega(C16)=4 Omega(C08),
omega(C17)=5 omega(C08),  Omega(C17)=5 Omega(C08)
```

exactly. The point certificates establish local nonzero curvature and exact branch dependence;
they do not establish that `Omega_E` is nowhere zero globally.

## 7. Small and finite loop holonomy

Although `n` depends on meridional angle, the coefficients of `omega_E` remain bounded near a
regular defect edge. A radius-`rho` meridian has coordinate length `O(rho)`, so

```text
integral omega_E -> 0
```

and its kernel-plane holonomy approaches the identity as `rho->0`.

Finite-loop holonomy requires the actual path integral of `omega_E` (or an exact equivalent
theorem). Those integrals were not exhaustively evaluated. Nonzero point curvature does not supply
their values. Full four-dimensional Levi-Civita holonomy is a separate tangent-bundle object and
was not computed.

## Maximum conclusion

Within the frozen stationary/off-shell ensemble, the intrinsic defect line is globally orientable
and has trivial projected line holonomy despite nontrivial singular ambient turning. Its associated
clock/line kernel plane has a metric-derived connection one-form that is everywhere nonzero in the
metric-anchored frame, plus exact locally nonzero, branch-dependent curvature certificates. This is
a bounded geometric transport atlas only.

No topological charge, quantization, carrier, Hopf section, particle, force, substrate ontology,
preferred branch, field equation, dynamics, action, source, boundary, density/bootstrap value,
`X_max`, matter, mass, stability, phenomenology, or canonization is derived.
