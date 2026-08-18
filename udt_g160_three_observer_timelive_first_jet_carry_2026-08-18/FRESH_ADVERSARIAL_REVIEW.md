# G160 fresh adversarial review

Date: 2026-08-18
Reviewer mode: fresh zero-context, read-only, no research continuation

## Initial verdict

Verdict: `REPAIR_REQUIRED`

The core tensor, connection, order, determinant, positive-triangular, total-rate, and scalar-versus-
matrix calculations passed. Two statements exceeded the evidence:

1. carry closure is sufficient but not necessary for equality of carried `(h,dot h)`, because
   finite Lorentz stabilizers and infinitesimal metric-skew rates are invisible to the pair first jet;
2. the unrestricted `GL+(2)` witness disproves a universal carry-only `phi,beta` law on that whole
   class, but does not prove that positive `B+(2)` is necessary for every exact subfamily.

The reviewer also required the independent implementation to cover the finite-defect rate, general
`phi,beta` rates, live gauge invariance of joined `(C,Gamma)`, and total-rate composition.

## Exact hostile witnesses

For `h=diag(-1,1)`, the nonidentity Lorentz matrix

\[
L=\begin{pmatrix}5/3&4/3\\4/3&5/3\end{pmatrix}
\]

satisfies `L^T h L=h`; a direct carry `L` and staged carry `I` therefore return the same stationary
pair first jet despite finite nonclosure. At identity carry,

\[
K=\begin{pmatrix}0&1\\1&0\end{pmatrix}
\]

is nonzero but obeys `K^T h+hK=0`, so equality of first jets also misses rate nonclosure.

The orientation-preserving sign reversal `-I` lies outside positive `B+(2)` but leaves every pair
metric and its terminal coefficients unchanged. Positive `B+(2)` is therefore a sufficient treated
class, not a necessity theorem.

## Final repair disposition

Verdict: `PASS`

The production derivation now includes both stabilizer witnesses, distinguishes source-gauge
covariance from joined-total-rate gauge invariance, and calls positive `B+(2)` sufficient rather
than necessary. The independent Fraction/dual-number implementation now covers all four previously
missing loads over 500 exact trials apiece. Mutation guards catch both overclaims. Physical carry,
query, history, `lambda`, and completion remain open.
