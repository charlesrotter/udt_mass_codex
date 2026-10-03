# PSC1 exposed candidate check freeze

Exposure: INITIAL_CANDIDATE, DISCOVERY_SCOPE, REFERENCES, CHECK_PLAN,
CANDIDATE_FREEZE, parent symbolic source/output, original and repaired saved-jet
checker, IMPLEMENTATION_REPAIR, REPAIR_FREEZE and original failure receipt.
No peer review or implementation opened. Same reviewer context as source-first.

Independent route: read only the saved log-p coefficients in EXACT_RESULT.
Construct p(L)=exp(log p) with exact standard-library Fraction series. Use
the actual conformal homogeneous metric g=p(L)^2 diag(-1,1,1,1) and reconstruct
Ricci, metric scalar curvature, Hessian and Box terms. Evaluate full original
00 and spatial components, and recover alpha/beta by solving two spatial
coefficient equations rather than importing parent's inference helper/formula.
Validate original checker failure and repaired coefficient from these residuals.
This is a different code/library path from parent's symbolic check but shares
the admitted metric equation and saved data. No observational independence.

Supported truncation: log-p supplied through L^5, unknown coefficients >=6
set to zero only as a formal representative. Original spatial coefficients
through L^1 and original00 through L^3 are not altered by those omitted terms.
Do not claim an exact finite history or higher residual order from the jets.

Same resource/stops as source-first: existing capture, one BLAS thread,2GiB,
finite CPU, no elapsed/CPU cutoff or GPU. Exact identities only. Preserve first
output and any failure; no shared mutations. Freeze script and inputs before run.
