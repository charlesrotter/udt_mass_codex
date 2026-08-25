# External `gpt-5.4` fresh adversarial review

Date: 2026-08-25

Disposition: `ACCEPT_WITH_REPAIRS`

## Findings

1. Medium: the registered production derivation was not replayable in the supplied environment
   because `derive_angular_nondiscard.py` required `sympy`, which was absent. A fresh reviewer could
   rerun the independent and hostile-check branches, but not the symbolic production branch from
   source. The mathematical package claim survived because the independent replay succeeded, but
   the live replay story was overstated until the dependency was supplied or removed.

Manifest verification passed. The hashes of `REVIEW_SCOPE.json` and `REVIEW_MANIFEST.tsv` matched
the authorized values, and all 33 manifest payload rows matched their recorded SHA-256 hashes and
byte counts.

Replay results:

- `python3 verify_independent.py` passed with 10,044 exact assertions across 700 arbitrary jet
  cases, 446 nonflat `f=1+C/r` vacuum-family cases, and 267 trace-balanced
  `f=1+a*r^2+b/r` cases;
- `python3 run_catch_proofs.py` passed and caught all eight hostile mutations;
- `python3 verify_package.py` passed after replay artifacts were writable;
- `python3 derive_angular_nondiscard.py` failed immediately on missing `sympy`.

The mathematical findings were favorable within scope. The independent tensor reconstruction
confirmed

```text
G^t_t = G^r_r = (r f' + f - 1)/r^2
G^theta_theta = G^phi_phi = f'/r + f''/2
```

while the isolated two-dimensional clock-radius block is identically Einstein-zero. The flat-screen
corruption is real: with `k=0`, `r^2 G^t_t = r f' + f`, and on every nonzero-`C` member of
`f=1+C/r` it returns `1`, not `0`.

The reviewer independently confirmed

```text
A_parallel+A_perp=E1-E0
A_parallel=(r^2 f''-r f')/2
A_perp=1-f+r f'/2
```

and therefore the sum `(r^2 f''-2f+2)/2 = E1-E0`. On `f=1+C/r`,
`A_parallel=3C/(2r)` and `A_perp=-3C/(2r)`, so both are nonzero for `C!=0` and cancel exactly.

The zero-angular-trace family is complete: solving `r^2 f''-2f+2=0` gives
`f=1+a*r^2+b/r`, and then `E0=E1=3 a r^2`, so trace balance alone does not imply vacuum. The
mass-aspect rewrite is also exact under `mu=r(1-f)/2`:

```text
E0=-2 mu'
E1=-r mu''
A_parallel=-r mu''+3 mu'-3 mu/r
A_perp=-mu'+3 mu/r
A_parallel+A_perp=2 mu'-r mu''
```

The reviewer found no circular reuse inside the bounded replay. The independent branch does not
import production code or read production results and reconstructs Christoffel, Ricci, scalar, and
Einstein tensors from raw metric jets before checking the formulas. It is a targeted verifier, not
a blind rediscovery engine, but it is not circular.

The scope ceiling was accepted: the package consistently keeps the claim bounded to the
static-spherical GR-quiet comparator and explicitly denies a global/source/history/loud-law
promotion.

## Exact repairs

1. Supply `sympy` in the declared replay environment, or replace the registered symbolic
   derivation with a dependency-free replay so `python3 derive_angular_nondiscard.py` is executable
   for fresh reviewers.
2. Until fixed, narrow wording such as “production full-metric symbolic derivation: PASS” to
   “manifested symbolic result verified; live rerun unavailable in this environment.”

## Strongest bounded landing

Within the sealed static-spherical positive-`f` GR-quiet comparison only, G260 establishes that the
angular sector is indispensable to the nontrivial residual and remains individually active on every
nonflat `f=1+C/r` member. The isolated radial two-dimensional block is vacuous, the flat-screen
`k=0` corruption breaks the vacuum family, `A_parallel+A_perp=E1-E0` is correct, and the zero-trace
family is exactly `f=1+a*r^2+b/r`. None of this licenses a derived global Einstein law, a UDT
parent law, a source/history law, or a loud/global extension.
