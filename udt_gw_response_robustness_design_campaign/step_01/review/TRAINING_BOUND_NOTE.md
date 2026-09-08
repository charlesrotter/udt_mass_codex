# Source-first refinement: training bound and nonvacuity

2026-09-08 00:36 UTC, before parent target exposure. This supplements the
unchanged source-first seal and independent source notes. The parent received
this mathematical requirement by message before producing its pinned target.

Let T:Y->Y_T be a fixed bounded training/readout map and N:Y->Z a fixed
bounded null. Assume NA0=0, ||T A0 h||>=gamma_T||h||,
||T E||<=epsilon_T<gamma_T, ||T e||<=eta_T, and ||N E||<=beta.
Under y=(A0+E)h+e, triangle inequality yields
 (gamma_T-epsilon_T)||h|| <= ||T y||+eta_T.
Therefore
 ||N y|| <= beta (||T y||+eta_T)/(gamma_T-epsilon_T)+eta_N
when also ||N e||<=eta_N.
T can be an explicitly selected training-detector readout or the orthogonal
nominal signal projection, provided the full-domain inequalities are proved.
No statistical independence between Ty and Ny follows, even when they are
orthogonal in a chosen inner product.

The earlier whole-y bound remains valid but may be vacuous. For ||N||<=1,
beta/(gamma-epsilon)>=1 and nonnegative noise allowances imply
 beta(||y||+eta)/(gamma-epsilon)+eta_N >= ||y|| >= ||Ny||.
Such a sufficient inequality cannot reject any y. Failure to reject with it
does not prove physical compatibility; a sharper bound may exist.

Nonvacuity of the training form is conditional too. If T and N together
admit y with Ty=0 and arbitrarily large Ny, its RHS is a finite constant
when eta_T,eta_N,beta,gamma_T-epsilon_T are fixed. Such y eventually violates
the bound. This supplies mathematical informative capacity in that direction,
not population power, noise validity, achievable instrument sensitivity or a
claim that a physical discrepancy realizes that direction.

For any target effect one still needs the physically relevant norms,
actual numerical uncertainty/amplitude controls, and error model coverage.
An arbitrary scenario coefficient is not an empirical certificate.

