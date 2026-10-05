# Independent controls before candidate exposure

SOURCE_FIRST.md and check_independent.py were hashed before execution in
SOURCE_FIRST_MANIFEST.json. The source-first note contains one typographic
`+` before `luminosity`; this has no mathematical meaning and the sealed file
is retained unchanged. Its formulas are this reviewer's pre-exposure derivation.

Exact command:

    python3 udt_optical_jacobi_attachment_2026-10-05/review_fidelity/check_independent.py > udt_optical_jacobi_attachment_2026-10-05/review_fidelity/check.stdout 2> udt_optical_jacobi_attachment_2026-10-05/review_fidelity/check.stderr

Exit 0; stderr empty. All 16 frozen cases completed inside the internal 2GiB
address-space limit and single-thread BLAS settings, CPU only, without timeout.
No failure, repair, rerun or omitted named case occurred. Exact runtime/library
versions and all named values are saved in INDEPENDENT_RESULT.json; stdout is
preserved. The checks are ordinary numerical evidence, not interval certification.

The 12 direct second-order Jacobi integrations agree with the independently
constructed ray-variation factors to maximum scaled error
9.798434810934587e-11, below the frozen 2e-8 threshold. The largest discrepancy
is the most nearly tangential case. Non-tangential nine-case maximum is
4.3109820432723695e-12. This corroborates the component formulas, including sign;
it does not independently rederive curvature from a full Christoffel tensor.

Three deliberate controls disprove an unqualified outgoing-regularity-implies-
no-caustic assertion. For m=1,a=3.001,H=.01,R=1000 and
b/[a/sqrt(f(a))]=.99,.9999,.999999, all source bounds are strict but P/pi is
1.145484731005425, 1.8864120128015345 and 2.5246548039803898. Because P(r)
increases continuously from zero, these paths cross at least one, one and two
out-of-plane conjugate points respectively. No claim of stable orbit, population
typicality or a global ray classification is made. These are valid conditional
geometric controls; no observation is being fit.

Four high-precision actual orbiting-source incidences obey the frozen original
incidence residual threshold 1e-35 and source regularity. For R=10^3,10^4,10^5,
10^6 the pole-product relative discrepancy from (a+E/H)/sqrt(h) decreases as
.1392404, .0132226, .001311818, .0001310745. The finite errors are retained, not
called exact agreement. The numerical tail agrees with the independently
derived asymptotic scaling; it is not a proof of a limit. At R=10^6,
b=.00344391120335 and D_A=99.98720131594, with endpoint 1/H=100. Thus the check
uses nonradial finite rays on one actual rotating source history.

Interpretive constraints: J maps sky variations to source rest-screen lengths;
its inverse maps source lengths to sky only where nonsingular. Quotient screen
isometry implements the circular emitter rest screen without a spurious endpoint
Lorentz factor. This geometric screen and linearization are supplied readouts;
no material ruler, disk dynamics, finite emitter or brightness law has been
derived. Shared Python/scipy/mpmath libraries, supplied metric/premises and
inherited model identity limit independence even though this implementation and
context are distinct. Parent results/code have still not been read when writing
this report.
