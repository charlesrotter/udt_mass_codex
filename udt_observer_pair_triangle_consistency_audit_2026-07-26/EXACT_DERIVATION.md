# Exact derivation

## 1. Fixed-observer finite directional maps

Let `P_u` project onto the supplied observer line, `P_space=I-P_u`, and
`P_n` project onto a supplied unit spatial direction. With
`q=exp(delta)>0`, exponentiating the prior complete generator gives

```text
E_lambda(n;q)
 = q^-1 P_u + q P_n + q^lambda(P_space-P_n)
 = q^-1 P_u + q^lambda P_space + (q-q^lambda)P_n.
```

For a second direction `m` and factor `r`, exact multiplication gives

```text
[E_lambda(n;q),E_lambda(m;r)]
 = (q-q^lambda)(r-r^lambda)[P_n,P_m].
```

The complete zero set in the registered strata is therefore:

- `lambda=1`;
- either depth is zero (`q=1` or `r=1`);
- or the two rank-one projectors commute, which includes parallel and
  orthogonal directions.

For generic nonorthogonal directions and nonzero depths, universal
path-independent comparison in one common frame forces `q^lambda=q` for
every positive `q`, hence `lambda=1`. This is a conditional theorem because
the common flat endpoint-only comparison premise is not founded UDT data.

## 2. A typed endpoint groupoid does not select lambda

Supply one complete coframe `F_A` at each endpoint and define

```text
D_lambda(delta)=diag(exp(-delta),exp(delta),
                     exp(lambda delta),exp(lambda delta)),
T_AB=F_B D_lambda(phi_B-phi_A) F_A^-1.
```

Then

```text
T_BC T_AB
 = F_C D_lambda(phi_C-phi_B) F_B^-1
       F_B D_lambda(phi_B-phi_A) F_A^-1
 = F_C D_lambda(phi_C-phi_A) F_A^-1
 = T_AC
```

for every real `lambda`. Reversal is also exact. Triangle consistency of a
properly typed endpoint groupoid therefore does not select the screen
response. It assumes exactly the endpoint section that current UDT has not
derived.

## 3. Pair-dependent frames expose the missing transition

If the frame at an observer depends on which other observer is being
compared, use

```text
T_AB=F_(B|A) D_AB F_(A|B)^-1,
T_BC=F_(C|B) D_BC F_(B|C)^-1.
```

The product contains

```text
M_B=F_(B|C)^-1 F_(B|A).
```

Unlike endpoint frames cannot be cancelled. `lambda=1` makes the dilation
operator spatially isotropic and therefore insensitive to a pure spatial
rotation of its direction frame, but it does not make `M_B` equal to the
identity or derive how it is transported.

## 4. Changing the observer remains nonabelian

At `lambda=1`, for a supplied observer line `u`,

```text
E_1(u;q)=q^-1 P_u+q(I-P_u).
```

For two noncollinear timelike observer lines,

```text
[E_1(u;q),E_1(v;r)]
 = (q^-1-q)(r^-1-r)[P_u,P_v],
```

which is generically nonzero. Thus the exceptional fixed-observer value does
not turn the complete arbitrary-observer structure into one abelian scalar
law. This agrees with the previously derived nonabelian Lorentz-frame
composition and its angular rotation closure.

## 5. Holonomy and global scope

A nonidentity common-frame loop is an obstruction to the explicitly chosen
flat/path-independent route. It is not a theorem of inconsistency for a
curved or path-transported geometry. Interpreting it as holonomy requires a
connection, path family, and complete branch. The metric supplies a
Levi-Civita connection after a complete metric is given; current sources do
not turn that fact into a noncircular selector of the missing coframe lift or
global finite-cell realization.
