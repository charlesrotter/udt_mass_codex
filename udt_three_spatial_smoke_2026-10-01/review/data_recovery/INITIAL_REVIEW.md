# TDS1 recovered initial-data review

Reviewer: actual fresh separate context `/root/tds_data_recovery`, inherited model;
not different-model or blind review. Parent startup/synchronization and unchanged
SMK1 audit evidence are attributed to `/root`; this reviewer independently read
HEAD `d65a7ea0faa0e38b9b1ad5ed5e3743be5178288d`, `grok` status, TDS1 work order,
the original producer and interrupted reviewer checkers/receipts, central R11,
and current G312 authority. Old `review/data/` files were left unchanged. Parent
provided the old N8 numerical values before this recomputation. The entire result
is source-exposed numerical review, not blind confirmation or acceptance.

The physical scope remains a supplied periodic, CMC/conformally-flat initial
family in the **conditional Ric=0, Lambda=0 comparison branch**. Current G312
does not identify that branch as UDT's native response equation. The CMC,
conformal-flatness, topology, lapse/shift, phases, amplitudes, and coordinate
scales are supplied. The work order states these limits and does not authorize
multi-hour production or claim general solution-space coverage.

## Formula review

The constant and three mode matrices used for the conformal seed have zero
Euclidean trace. For a mode depending only on coordinate j, its j-th matrix row
vanishes, so its Euclidean divergence is zero. The seed is therefore exactly TT
as an analytic periodic field. With gamma=psi^4 delta and
K=psi^-2 seed+(tau/3)gamma, the scalar constraint reduces to the stated
-8 Delta psi-|seed|^2 psi^-7+(2/3)tau^2 psi^5=0. This establishes the construction's
algebraic provenance, not the validity of a saved discrete solution by itself.

At the initial lapse1/shift0 slice, K=-v_ij/2. Direct contraction of the
four-metric first derivatives gives H_0=-v_00/2+tr(K) and
H_i=-v_0i-2 partial_i log(psi). Thus the producer choices v_00=2tau and
v_0i=-2 partial_i log(psi) have the correct signs. At finite collocation
resolution the product/chain rule is not exact; direct contraction from saved
g,v is therefore checked separately rather than assumed zero.

## Saved-field recomputation

`initial_review.stdout` contains full results, source hashes, catches, versions,
and checker self-controls. Its associated receipt captures command, duration,
resource limits, and stdout/stderr. The original connection-based Hamiltonian
and momentum checker was reused unchanged from the interrupted reviewer, with
formula inspection in this recovered context; it imports no producer code.
This is a new actual recomputation, not a claim of a second new implementation.

| Mesh | max Hamiltonian | max momentum | max initial harmonic contraction |
|---|---:|---:|---:|
| 8^3 | 1.2033528873e-6 | 2.1815755598e-7 | 4.4166003062e-8 |
| 12^3 | 2.7368729505e-10 | 1.1401930457e-10 | 1.5231424114e-11 |
| 16^3 | 2.1849189125e-13 | 4.2784352450e-14 | 4.1355536617e-15 |

All are below the existing 2e-5 initial smoke threshold and decrease strongly
under refinement. The residual of the producer's conformal equation is not
substituted for these original metric/connection residuals.

An additional independently coded density-divergence expression for momentum,
gamma^-1/2 partial_j(gamma^1/2 K^j_i)-K^jk partial_i gamma_jk/2-partial_i tr(K),
has max residuals 2.21e-8, 3.40e-12, 2.53e-15. Its disagreement with the direct
connection expression decreases from 2.40e-7 to 4.21e-14. The two expressions
are analytically identical but their finite collocation products differ; this
is discretization evidence, not two independent discretizations.

The seed trace/divergence, metric symmetry/positive spatial eigenvalues,
four-metric Lorentz signature, g_ij=gamma, and v_ij=-2K were checked. Deliberately
changing v_00 by .02 produces a harmonic violation greater than .009. The reused
checker independently recovers analytic conformal curvature and isotropic-K
momentum controls and detects a bad K. These are meaningful checker controls,
not a proof of all errors being detected.

The derivative Gram matrix has three positive eigenvalues near
4.98855e-5, 1.33193e-4, 1.99559e-4 on every mesh. This excludes a nonzero constant
coordinate translation preserving this saved (gamma,K) datum. It does **not**
exclude arbitrary Killing fields, identify physical inhomogeneity uniquely,
or imply genericity. One amplitude1 family has been checked at this point.

## Decision and remaining scope

**PASS for the saved initial data and declared finite-resolution scope.** No
initial-data sign, constraint, or rank defect was found. This result is not a
continuum constraint certificate, independent long-time evolution check,
null/readout validation, or production readiness. Evolution outputs, original
four-dimensional Ricci/constraint residuals, refinements, actual changed-state
restart/stop tests, and measured workload remain to be reviewed separately.
