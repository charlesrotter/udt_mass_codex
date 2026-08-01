# F02 global-completion external-review correction layer

Date: 2026-08-01  
Parent package: `udt_f02_global_completion_admissibility_2026-08-01/`  
Parent package commit: `bafc5d7`  
Parent manifest SHA-256: `d15feffade73d8a90dc0e5e99523be6bdb7811a02643a13ef7898e9a63445832`

## Status

The authorized read-only gpt-5.4 review returned `PASS-WITH-REQUIRED-REPAIRS`. It found one
source-freezing/citation defect and no mathematical refutation. This append-only layer repairs the
defect without changing any byte of the frozen parent package.

The maximum conclusion remains:

```text
OPEN_INCOMPLETE_REGISTERED_CLOSURE_DATA
```

## Exact repair

The parent package uses regular-cap evenness in transverse geodesic distance to exclude a nonzero
affine F02 slope in rows G06/G07. It correctly states that the F02 coordinate `x` has unit spatial
weight on the tested branch, but its frozen `SOURCE_INVENTORY.tsv` omitted the registered metric
source that proves this normalization.

The missing source is now frozen in `SOURCE_ADDITION.tsv`. It gives the registered toric chart

```text
q_B = exp(2 lambda phi) (dx^2 + bh(x) dy^2),
```

and identifies `f` as the connection moment and `bh` as the horizontal-norm field. The already
frozen F02 local report gives `p=lambda=h=0, f=x/2`, while the already frozen gradient-seat source
identifies the varying fields as `(phi,f,bh)`. On the F02 landing `p=phi=0` and `lambda=0`, hence

```text
q_B(dx,dx)=exp(2 lambda phi)=1.
```

Therefore `x` is transverse proper distance up to orientation and an additive constant on this
branch. At a regular cap, `dx/d rho=+1` or `-1`; the frozen cap series gives
`df/d rho -> 0` and `dbh/d rho -> 0`, so `df/dx -> 0` and `dbh/dx -> 0`. Because the F02 profiles are
affine, either zero cap derivative kills the corresponding slope globally. D06/D07 and G06/G07
therefore retain their original scope and result.

This repair does not select a cap, fold, boundary, action, response law, carrier, source, or physical
completion. It only closes the cited normalization premise for the parent package's conditional cap
obstruction.

## Four gates after review

1. Preregistered: yes—the parent package preregistered the cold adversarial audit and its exact
   review questions before transmission.
2. Full or bounded: bounded to the nine registered completion rows and the conditional affine F02
   landing; no exhaustive theorem over unregistered completions.
3. Independent: gpt-5.4 read-only adversarial review passed the equations and source semantics after
   requiring this source-freezing repair.
4. Premises: the repair source is frozen exactly; all parent premise stamps and open scopes remain
   unchanged.
