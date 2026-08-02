# Fresh cold review return

Grade: **PASS — no load-bearing correction required.**

The reviewer worked read-only in a fresh context, did not import or execute the production script,
and used an independent exact implementation in temporary storage. It reproduced:

```text
X1=(-q1,q0,q3,-q2),
X2=(-q2,-q3,q0,q1),
X3=(-q3,q2,-q1,q0),

W proportional to -24 q3(f12,f13,f23),
f12=q0 q1^2+3 q0 q2^2+2 q1 q2 q3,
f13=q0^2 q1+3 q0 q2 q3-2 q1 q2^2,
f23=3 q0^2 q2-q0 q1 q3+2 q1^2 q2.
```

The exact exhaustive zero locus was independently recovered as

```text
Z(W)={q3=0} union C03 union C13 union C23.
```

The independent support proof used coefficient points `(1,1),(2,3),(4,7),(8,9)`: the first three
are collinear, while every triple containing the fourth is noncollinear.

The nonzero ruler-aligned locus was again empty. The reviewer used a separate reduction in which
the nontrivial case becomes a sum of nonnegative terms, forcing the remaining ratios to zero and
hence forcing `f12=0`. It independently supplied different exact witnesses:

```text
screen-contained: q=(1,1,1,-2)/sqrt(7),
generic-mixed:    q=(1,1,1, 1)/2.
```

It reproduced the Hodge/kernel convention

```text
W=A theta1^theta2+B theta1^theta3+C theta2^theta3,
N_flat=C theta1-B theta2+A theta3,
ker(W)=span(T,N) with dimension 2 when W!=0,
ker(W)=full tangent space with dimension 4 when W=0.
```

The projective line was independently shown to extend across `q3=0` except at
`+/-e0,+/-e1,+/-e2`, and to fail path-independently at every point of the three great circles. The
reviewer recomputed rank-two transverse maps away from `+/-e3`; at the shared poles it found three
distinct limiting directions `[0:0:-1]`, `[0:3:0]`, and `[2:0:0]`.

Finally, it reproduced exactly two components of `S3\Z(W)`: each open `q3` hemisphere is an `R3`
with its three coordinate axes removed, which remains connected, while the removed equator
separates the two hemispheres.

The `6/9/2/1` candidate census, source-manifest SHA-256
`48dcc11e79a0395e920c159a88346656011d8784118f11620f6996db040be122`, and current-premise verifier
also reproduced. The reviewer made no repository edits.
