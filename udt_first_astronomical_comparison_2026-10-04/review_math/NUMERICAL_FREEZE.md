# Independent ACP1 finite-check freeze

Candidate exposure: INITIAL_CANDIDATE.md SHA-256
4f477ceaadf4139045b63d6aa8df35c0f2b75c8482062aa87f2a31fc67f9fac4, after
SOURCE_FIRST seal. Parent implementation and numerical outcomes are unexposed.
Only this reviewer's check_readout.py runs here; no other implementation imports.

Question: do the candidate clock/angle/frame identities survive independent
exact proper-clock, typed screen and source-summary arithmetic controls?
Regime: supplied regular 1+1 Minkowski clock families embedded in 4D; finite
2x2 screen algebra with positive screen metrics; actual CGCG source-summary
units at retained conventional scope. Controls are free-and-explored mathematics,
not a metric ansatz for the galaxy. Frame signs/scales are stated conventions.

Frozen inputs: 8 proper-clock samples r=(1/3,1/2,2/3,1,3/2,2,3,5),
eta'=a=(i+1)/7; source rest-line multipliers (i+2)/3 with derivatives (i-2)/11;
affine family scales (i+2)/5 with derivatives (2-i)/13. Four explicit screen
matrices/GL frame pairs and three observer boosts exp(eta)=(1/2,2,3) are listed
in code. Three marginal summary points are lower/median/upper values for the
CGCG row of MCP_TABLE1_INPUT.tsv, not a joint posterior region. Total 18 finite
cases, below the 100-case ceiling. All quantities come from declared controls
or the pinned source; no observed outcome tunes a control.

Equations checked independently: norm/acceleration constraints; coordinate
arrival t_o=t+x versus endpoint null frequency; optical derivative from
received nu=alpha/Z; affine quotient differentiation; J=-omega_o B_eo with
future-affine reverse block and sky sign; GL screen covector typing/area metric
coefficients; observer aberration derivative; rational chi=(1-Z^2)/(1+Z^2)
versus Decimal tanh form. Wrong-rule substitutions intentionally test an extra
arrival divisor, one-endpoint affine scaling, fixed-frame sign reversal and
determinant-as-map substitution. These are finite separators, not universal
mutation coverage or theorem certification.

All rational checks are exact Fraction equality; Decimal uses 70 digits and
absolute tolerance 1e-65 only for log/exp versus exact rational tanh. No floating
ODE, spatial grid, GPU, fit, timeout or long production. Each process gets a
2 GiB address-space limit and one BLAS/OMP thread. A failure stops this script
without replacing its output; any code repair requires a separate documented
rerun and preservation of the initial script/output. Success supports the finite
identities only; general proof hypotheses and source-systemic-clock realization
still require substantive review.

Exact execution command after freezing code/input hashes:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 udt_first_astronomical_comparison_2026-10-04/review_math/check_readout.py > udt_first_astronomical_comparison_2026-10-04/review_math/check_readout.stdout.json 2> udt_first_astronomical_comparison_2026-10-04/review_math/check_readout.stderr
```
