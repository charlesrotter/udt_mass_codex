# Exact derivation and scope

## 1. Geometry that survives

On the bounded historical control

```text
g=diag(-exp(-2 phi),exp(2 phi),r^2,r^2 sin(theta)^2),
```

with `c=1` during the algebra, the determinant is

```text
det(g)=-r^4 sin(theta)^2.
```

Therefore the reciprocal temporal/radial factors cancel from the volume
density. For any independent static spherical scalar `f`,

```text
Box_g f
 =r^-2 d_r[r^2 exp(-2 phi) f']
 =exp(-2 phi)[f''+2f'/r-2 phi' f'].
```

This is an exact operator identity on the stated metric. It is not a field
equation.

Setting the argument equal algebraically to the metric profile gives

```text
Box_g phi
 =exp(-2 phi)[phi''+2phi'/r-2(phi')^2].
```

A direct four-dimensional Christoffel/Ricci reconstruction independently
returns

```text
G^theta_theta
 =exp(-2 phi)[2(phi')^2-phi''-2phi'/r],
```

and hence

```text
Box_g phi=-G^theta_theta.
```

This is also an exact identity of the restricted metric family. Equating
either side to a physical source would be an additional law.

## 2. The variation-domain fork

The historical source writes the quadratic scalar density

```text
L=1/2 sqrt(-g)[g^rr (d phi)^2+mu^2 phi^2-2S phi].
```

There are two inequivalent problems.

### Independent probe on a fixed metric

Let the varied scalar be `psi` and the fixed background profile be `b`.
Varying

```text
L_probe
 =r^2/2 [exp(-2b)(psi')^2+mu^2 psi^2-2S psi]
```

gives

```text
r^-2 d_r[r^2 exp(-2b) psi']-mu^2 psi=-S.
```

This is the historical screened equation, correctly scoped as a probe-field
equation.

### The same phi determines and varies the metric

If the varied object is the same `phi` inside `g[phi]`, then

```text
L_self
 =r^2/2 [exp(-2phi)(phi')^2+mu^2 phi^2-2S phi]
```

gives instead

```text
exp(-2phi)[phi''+2phi'/r-(phi')^2]-mu^2 phi=-S.
```

The exact difference is

```text
self_lhs-probe_lhs=exp(-2phi)(phi')^2.
```

Thus the historical equation cannot be used as the self-gravitating law for
the metric-determining `phi` without choosing the fixed-background variation
domain.

## 3. Conditional linear control

After the additional approximation `exp(-2phi) -> 1` and the branch choice
`S=0`, the equation becomes

```text
phi''+2phi'/r-mu^2 phi=0.
```

The regular centered solution

```text
phi=C sinh(mu r)/(mu r)
```

is exact for that conditional linear problem. It is not a universal UDT
profile. The approximation, screening scale, source choice, center, static
character, and round angular sector all remain premises.

## 4. Exact WR-L countercontrol

For conditional WR-L,

```text
phi_WRL=-1/2 log(1-r/X),
exp(-2phi_WRL)=1-r/X.
```

Direct substitution gives

```text
Box_g phi_WRL=1/(Xr),
```

and therefore

```text
(Box_g-mu^2)phi_WRL
 =1/(Xr)+(mu^2/2)log(1-r/X).
```

This cannot vanish on `0<r<X` for any finite constant `mu`: it diverges
positively toward the centered end and negatively toward the WR-L wall when
`mu` is nonzero; for `mu=0` it remains `1/(Xr)`. The historical screened
vacuum equation therefore does not select WR-L. An explicit source would be
required, and the old document does not derive one.

## 5. Relation to the current bilocal gate

The old equation acts on a scalar in one centered static chart. It contains
no:

- observer-indexed event pairing;
- neutral self-comparison rule;
- recentering transition/cocycle;
- non-collinear angular direction data;
- screen Jacobi/area transport;
- cut-locus path family;
- complete finite-cell descent.

It consequently cannot supply the current missing longitudinal-transverse
bilocal correspondence. Its exact scalar identities remain useful as static
regression controls once a complete branch and variation domain are supplied.

