# First twist-gate correction

The first invocation of `derive_product_twist.py` stopped before writing an outcome because two
implementation checks incorrectly treated legitimate solution-space structure as an algebra failure.

First, `K=0` does not uniquely mean the Cartesian representative `F=1`; it also permits local polar
or linear `F` charts. The parent flat-tile comparison is therefore recovered under the exact
registered Cartesian control `K=0, F=1`, not under `K=0` alone.

Second, constant Gaussian curvature does not select a preferred transverse vector or one-form. The
coordinate twist

```text
d psi + epsilon*u(r) d theta
```

retains the directional screen connection through `F_prime/F`. Requiring the twist density to
depend only on scalar `K` would silently impose the very angular section the audit is testing. Under
the binding solution-space protocol, that dependence must be characterized rather than filtered.

The implementation was corrected before banking to:

- test parent recovery only at the registered `F=1` Cartesian control; and
- record surviving angular-connection dependence as an outcome classification, not a failed check.

No metric, profile, curvature identity, tolerance, boundary, or frozen outcome wording changed. The
failed pre-bank invocation supplies no scientific result.
