# F01 lambda/mu Schur exact check — preregistration

Date: 2026-08-01  
Base commit: `53bdc2c`  
Mode: CPU-only; conditional-P4-response-led; exact/validated scalar and index calculation

## Whole question

For every root in the registered interval `s in (1,3)` of

```text
F(s) = integral_-1^1 log(w_s(x)) dx,
w_s(x) = (s^2/2)x^2 + (s^2-s)x + 1+s^2/2-s,
```

what is the sign of the constant-`lambda`/`mu` Schur complement in the joint second variation of
the conditional F01 crease-cell branch, separately for:

1. R05 supplied free `f/h` traces; and
2. R06 supplied odd, zero `f/h` traces?

The registered `v_p` crease trace, the permitted other-end trace alternatives, and their exact
germ-Hessian-flat boundary form must be carried rather than replaced by a convenient Dirichlet box.
If those boundary domains do not determine one Schur problem, the result must branch or stop.

This is a local single-cell index question. It is not the free second-wall-germ question and is not
a native/global stability-hypothesis test.

## Frame and premise ledger before computation

| Item | Status/treatment |
|---|---|
| Founded UDT metric and reciprocal `phi` | `DERIVED`, background only |
| P4 response and quadratic class | `CONDITIONAL` |
| constants census / BASE moduli | `OPEN` census choice, carried conditionally |
| complete metric parent relation | conditional P4 subdomain; not natively selected |
| `ell=1` | `CHOSE`, must travel |
| crease normalization and `s in (1,3)` | registered conditional branch |
| P1 pairings | carry both; `a_F'=2`; do not silently pin a physical `a_F` value |
| free versus supplied-odd `f/h` traces | supplied branch fork; compute separately |
| germ-Hessian-flat wall responses | `CONDITIONAL` witnesses |
| unrestricted second wall germ | `OPEN`, outside this tile and still blocks full certification |
| prior Galerkin index near `s=1.68102` | `CORROBORATION_ONLY`, free-trace branch only |
| time, carrier, bootstrap, action ownership, matter, mass | `OPEN`/outside conclusion |

No GR, quantum, standard particle, Hopfion, observational, or desired-stability template enters the
calculation.

## Prework disclosure and temptation

Before executable work, the primary context noticed the exact substitution

```text
z=s(x+1),
w_s=1-z+z^2/2,
F(s)=s^-1 integral_0^(2s) log(1-z+z^2/2) dz.
```

Because the logarithm is negative for `0<z<2` and positive for `z>2`, its primitive decreases to
`z=2` and then increases. This hand observation suggests root uniqueness once opposite endpoint
signs are certified. It is disclosed here before code and must be independently checked; it is not
accepted merely because it simplifies the problem.

The pre-existing Galerkin lead tempts the outcome that `mu` adds no second negative direction on
R05. No such lead exists for R06. Both positive and negative Schur signs must be treated as
first-class outcomes.

## Required construction

1. Freeze the exact cited sources by path, Git blob, byte count, and SHA-256.
2. Derive the joint quadratic form from the frozen P4 density, retaining symbolic positive scales
   until their sign-independence is proved.
3. Derive the admissible boundary/trace domains from R05/R06 and the wall-gate sources. Do not infer
   them from the old Galerkin basis.
4. Isolate every root of `F` in `(1,3)`, including endpoint/exclusion and uniqueness or multi-root
   proof. Record raw brackets and interval/error bounds.
5. Derive the exact field-relaxed Schur scalar

   ```text
   S_mu = C - B A_field^-1 B*
   ```

   on every owned R05/R06 trace variant. An on-shell-family tangent may be used only after proving it
   solves the same linearized field and boundary problem; otherwise it is merely a control.
6. Certify the sign with interval/error enclosures excluding zero. If the result is exactly zero,
   certify the identity and kernel instead.
7. Independently reconstruct the joint index by a different spectral/index enclosure that does not
   import the primary Schur value or sign.

## Certification contract

- Root coverage is all roots in `(1,3)`, not the known approximate root alone.
- Primary arithmetic uses at least 80 decimal digits plus explicit interval/error bounds; increasing
  precision must nest/enforce the same sign.
- Every quadrature or spectral truncation has an explicit tail/residual bound. A converged decimal is
  corroboration, not certification.
- The independent route must certify the relevant inertia/index on each branch and trace variant.
- Raw stdout/stderr, commands, Python/SymPy/mpmath versions, brackets, enclosures, matrix dimensions,
  residual bounds, and SHA-256 are preserved.
- No tolerance, basis, branch, or boundary may be changed after seeing a sign. Failure to certify is
  a valid outcome.

## Exact outcome classes

Choose one primary class:

- `SCHUR_POSITIVE_ALL_OWNED_BRANCHES__NO_ADDED_NEGATIVE_DIRECTION`;
- `SCHUR_NEGATIVE_ONE_OR_MORE_BRANCHES__ADDED_NEGATIVE_DIRECTION`;
- `SCHUR_ZERO_OR_DEGENERATE_ONE_OR_MORE_BRANCHES`;
- `SCHUR_SIGN_MIXED_ACROSS_OWNED_BRANCHES`;
- `BOUNDARY_DOMAIN_NOT_UNIQUELY_OWNED__BRANCHED_OR_STOPPED`;
- `CERTIFICATION_FAILED__SIGN_OPEN`;
- `SOURCE_CONFLICT_STOP`.

## Falsifiers and fail-closed checks

Reject the package if it:

- omits or duplicates a root;
- substitutes the existing approximate root without an all-root proof;
- uses the old Galerkin sign as primary evidence;
- freezes `mu`, `v_p`, or an angular direction belonging to the named joint space;
- substitutes Dirichlet conditions for a free/seam trace;
- identifies R05 and R06 or transfers evidence between them;
- ignores a boundary Hessian or calls germ-Hessian-flat native;
- uses a decimal sign without a zero-excluding error bound;
- treats an on-shell tangent as the Schur minimizer without checking the linearized boundary problem;
- converts a local conditional index into whole-chain stability, time persistence, native matter,
  bootstrap selection, a basin count, or particle taxonomy.

## Maximum conclusion

At most: the local conditional lambda/mu Schur sign and branch-local joint index for each exact
owned F01 crease-cell trace domain under `ell=1` and germ-Hessian-flat wall witnesses. The free
second-wall-germ curvature, full chain, physical boundary, native variation selection, dynamics,
bootstrap, carrier, matter, mass, and global stability hypothesis remain open.

No GPU work, time-live solve, F02-F07 calculation, physics fitting, canonization, or repository
reorganization is authorized.
