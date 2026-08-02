# Fresh zero-context cold review return

Date: 2026-08-02  
Reviewer: `/root/cartan_contact_cold_review`  
Repository mode: read-only  
Reviewed HEAD: `5a8ad6f4ef493043bda1bb1804ae558714cec8bd`

## Verdict

`PASS_AFTER_REQUIRED_CORRECTIONS`.

The central split-relative identity survives, but the curvature census and two presentation claims
require correction before the package is used as a base.

## Contract rulings

| ID | ruling | exact return |
|---|---|---|
| R01 | PASS | review manifest 20/20, parent source manifest 29/29, and parent package manifest 43/43 match path, Git blob, byte count, and SHA-256 |
| R02 | PASS | `t1=kappa exp(phi)/D`, `v=log|t1|=B+phi-sigma`, so `dv=dphi-dsigma` and `-dphi wedge dv=dphi wedge dsigma` |
| R03 | PASS | `lambda_phi_v=(v dphi-phi dv)/2=lambda_phi_sigma+d(B phi/2)` |
| R04 | PASS | for `Theta'=O Theta`, `t1'=det(O)t1`; local `SO(2)` invariance and reflection-safe `|t1|` follow |
| R05 | PASS | `det(P)` and `t1` flip together under reflection; absolute logs survive every nondegenerate orientation stratum |
| R06 | CORRECT | `m'=m`, `C'=O C O^-1`, `L1'=(E1 O)O^-1+O L1 O^-1`; `mC` transforms homogeneously, but extracting it from total `A1=L1+mC` requires the supplied Maurer-Cartan decomposition |
| R07 | PASS | formal affine quotient rank one; universally exact kernel dimension five |
| R08 | PASS | formal and fixed pullback ranks are separated; collapse concerns the differential/curl, not general primitive cohomology |
| R09 | PASS | `phi=x1`, `sigma=x2`, `P=exp(x2/2)I` is a smooth invertible complete-`S3` witness with nonzero tangent wedge |
| R10 | NARROW | no actual joined-Cartan family omitted from the frozen authorities; scope must say “within the frozen 29-source authority set” |
| R11 | PASS | fresh Koszul reconstruction gives zero torsion, metric compatibility, `d^2=0`, and six nonzero lower curvature-pair blocks |
| R12 | CORRECT | parent zero-`p/sigma` bilinear wording is false: 12 rows contain some mixed `p_u s_v` monomial; only the narrowly tested leg-aligned projection is zero |
| R13 | PASS | a connection coefficient is not a tensor; tensorial curvature/difference/projector routes remain open |
| R14 | CORRECT | “production” overstates the result; `t1` provides an algebraic first-Cartan encoding/reconstruction, not a new constraint, field, response, or law |
| R15 | PASS | no action, density, carrier, source, mass, matter, bootstrap, or physical branch is promoted |

## Exact mixed-curvature correction

In a reverse-closure independent Koszul normal form, the rows containing at least one mixed
`p_u s_v` monomial are

```text
Omega02[02], Omega02[03], Omega03[02], Omega03[03],
Omega12[12], Omega12[13], Omega12[23],
Omega13[12], Omega13[13], Omega13[23],
Omega23[12], Omega23[13].
```

Both closure pivots give zero for the narrowly tested leg-aligned pair, but raw monomial attribution
is closure-normal-form dependent. No tensorial mixed-curvature no-go follows.

## Required corrections

1. Use `v=log(|t1|/T0)` with arbitrary positive `T0` unless coefficients are explicitly
   dimensionless. Then `B=log(|kappa|/(D0 T0))`; differential results are unchanged.
2. Replace the imprecise `m`-mixing description by the exact transformation law above.
3. Replace “zero phi/sigma bilinear rows” by the exact six-block / twelve-mixed-row / zero
   leg-aligned statement.
4. Add corrected machine fields and a complete mixed-monomial table; do not treat the parent
   header-only alternating table as a full census.
5. Replace “produces” with “encodes/reconstructs from the registered first-Cartan contact
   coefficient.”
6. Add catches for full mixed scanning, opposite closure pivots, exact `m/L1` gauge law, and frozen
   source-relative branch scope.

Repository remained unchanged and clean.

