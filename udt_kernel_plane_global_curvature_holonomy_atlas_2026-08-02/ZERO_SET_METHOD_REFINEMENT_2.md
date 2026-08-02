# Exact zero-set method refinement 2 — contact stratum and defined-domain saturation

Date: 2026-08-02  
Original preregistration: `c06eb8a6`  
First method refinement: `bf500492`

## Trigger before zero-set outcome

The intrinsic route proved chart equivalence and produced the exact `C04` curvature numerator
triple. A direct five-variable Gröbner calculation exceeded five minutes without returning a
basis. No numerical root reconnaissance, exact root, zero locus, or absence result had been
computed.

During algebraic factor inspection, the exact necessary contact obstruction was found:

```text
eta wedge d eta
 = 2(q0^2 q1^2-3 q0^2 q2^2-2 q1^2 q2^2)
   (q0^2+q1^2+q2^2+q3^2) volume.
```

This identity is itself an intermediate exact result, not a zero-set verdict. On the unit sphere,
every regular curvature zero must lie on

```text
A=q0^2 q1^2-3 q0^2 q2^2-2 q1^2 q2^2=0.
```

The implication follows from `eta wedge Omega=eta wedge d eta/sqrt(P)` and does not assume a
candidate answer.

## Frozen exact refinement

For each owner:

1. preserve the raw intrinsic polynomial triple;
2. also compute its exact remainder modulo the sphere equation, eliminating only powers `q0^2`
   through `q0^2=1-q1^2-q2^2-q3^2`;
3. prove raw-minus-remainder belongs to the sphere ideal;
4. add the necessary equation `A=0` only on the domain where the registered connection exists;
5. saturate by the product of the defect measure and the exact numerator and denominator of
   `P=uS`.

The last saturation is not a physical exclusion. On the real registered domain, `P>0` and its
profile denominator is positive, so it is exactly the defined domain of `omega`. It prevents
irrelevant complex `P=0` components from obstructing a certificate about real regular points.

The direct defect-only ideal remains preserved as provenance. A unit ideal in the refined
defined-domain saturation certifies no complex zeros where the connection is defined. A non-unit
ideal still requires exact real classification; numerical reconnaissance cannot close it.

Candidate universe, profile data, defect set, loop universe, and maximum conclusion remain
unchanged.
