# F02 stationary simultaneous realization — exact derivation

Date: 2026-08-01  
Contract: `PREREGISTRATION.md` committed at `5e0c437` before this calculation  
Primary: `derive_f02_simultaneous.py` (exact SymPy, CPU only)

## 1. Inherited conditional object

The fields-census P1-4D landing has `a_F=2 lambda`. Its nonzero branch is

```text
p = 0
lambda = 0                 (forced by the p row when E0 != 0)
f = f0 + a x
h = h0 + b x
E0 = (g_f a^2 + 2 g_x a b + g_h b^2)/2 .
```

The affine solve requires `g_p != 0` and `Delta_G=g_f g_h-g_x^2 != 0`. Its full
conditionality also includes supplied wall data leaving at least one slope free and the complete
locked lambda row. These are the corrected conditions in
`udt_p4_gradient_seat_2026-07-29/EXACT_DERIVATION.md:176-230`.

We test the registered jet-quadratic member

```text
S = exp(2 lambda p) [ L_tilde(p',f',h') + (c_m/2)(lambda')^2 ] .
```

This does not add a new response to the bank: it is the exact member already tested in the F02
stability slice. It remains a `CONDITIONAL` P4 response, not a selected UDT law.

## 2. Exact background equations

The primary script independently forms all four Euler operators for `p,lambda,f,h`. On the full
affine landing, including the jet term, every residual vanishes. The jet contribution to the
lambda row contains at least one lambda jet and therefore vanishes at `lambda'=lambda''=0`; this is
the inherited lock-reduction theorem instantiated rather than cited alone.

The exact constructive member is

```text
ell=1
g_p=g_f=g_h=c_m=1
g_x=0
p=0
lambda=0
f=x/2
h=0 .
```

It has `Delta_G=1` and `E0=1/8`. All background rows vanish exactly.

## 3. Completion branch

The period census distinguishes acyclic from cyclic completions. An open/acyclic chain has no
non-torsion cycle and leaves the F02 landing untouched; a one-cell cyclic completion forces the
affine slopes to zero. This is explicit in
`udt_p4_period_gate_2026-07-30/EXACT_DERIVATION.md:42-47,209-214`.

For the witness, `f(1)-f(-1)=1`, so it is explicitly incompatible with one-cell periodic
identification and explicitly assigned only to the supplied open/acyclic branch. The calculation
does not turn that branch into a derived physical boundary or a complete universe. In particular,
the background has `p=0` throughout; its canon/physical-completion admissibility remains `OPEN`.

The fold-realization premise `R-A` is not assumed. If it were supplied, its definite wall parities
would set both affine slopes to zero and collapse `E0`, as shown in
`udt_p4_angular_completion_2026-07-30/AUDIT_REPORT.md:50-56,80-92`.

## 4. Joint sector Hessian

Vary all four fields jointly about the background. The exact second-variation density is

```text
g_p (v_p')^2 + c_m (v_lambda')^2
+ g_f (v_f')^2 + 2 g_x v_f' v_h' + g_h (v_h')^2
+ 4 E0 v_lambda v_p .
```

For each Dirichlet mode `k_n=n*pi/(2 ell)`, the only indefinite candidate is the `p/lambda` block

```text
[[g_p k_n^2, 2 E0],
 [2 E0,       c_m k_n^2]]
```

with determinant `g_p c_m k_n^4-4E0^2`. Consequently all registered modes are nonnegative exactly
when

```text
64 E0^2 ell^4 <= g_p c_m pi^4 .
```

For the witness the left side is `1` and the right side is `pi^4`, so the inequality is strict.
This reconstructs the banked dichotomy in
`udt_p4_stability_slice_2026-07-30/EXACT_DERIVATION.md:113-131` on the same background rather than
merely comparing two separate reports.

## 5. Candidate readings and exact scope

At `ell=1,E0=1/8`, the inherited labels give

```text
M_GEN = M_DENS_coordinate = M_DENS_proper = 1/4
M_WALL = 0 .
```

The dissent is preserved. None is promoted to physical mass.

The result is exactly

```text
CONDITIONAL_NONPERIODIC_F02_DIRICHLET_HESSIAN_SECTOR_POSITIVITY_WITNESS_EXISTS
```

It proves that the local background field equations, a supplied nonperiodic open/acyclic posture,
and the registered Dirichlet Hessian sector are not mutually inconsistent. The label is narrowed
per external cold review: it does not claim a completed stationary solution or a global/physical
realization. It also does not select `c_m`, the response law, the posture, a physical boundary,
time evolution, the complete Hessian, bootstrap membership, physical mass, or a species.
