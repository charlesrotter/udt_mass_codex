# Independent checks before parent-candidate exposure

`SOURCE_FIRST.md` was written before the first independent run. Afterwards the
parent communicated a pre-freeze algebraic refinement: use dimensionless ranges
mu=mH in [.005,.01], A=aH in [.05,.1], E in[1,10], principal preparation,
y=1/(HR)<=2e-5, H>0 free, instead of an absolute-scale compact box. It also
communicated proposed continuous equal-width records with width .1, epsilon_Y
.003, absolute angle error5e-8, timestamp error .001T and receiver-length-time
source drift bound q=5e-6. This is exposure to evolving lead details, not to a
parent candidate, code or result. The independent frozen test was not changed.

The shape-only range removes a dimensional parameter prior. Tail membership is
still a supplied conditional premise: an unknown H appears in y and a finite
record has not independently established it. Numerically fixed observation
times1.6 and200 are noncircular even if discovery first described them using a
synthetic H0=.005. H0 must not appear as unknown truth inside the estimator or
in a claim of guaranteed real-world cadence/error. The dimensional error/drift
budgets are metrological assumptions in calibrated receiver units.

## Independent finite incidence witness

The frozen two-point finite-window records passed. The 28 incidence cases
include 24 records and four saved-value precision replays. Original incidence
equations use independently written quadratures and an exact E=1 radius/time
relation, not a parent utility. The short common-time record admits both
factor-two scales: maximal midpoint logZ error0.0020000188877224 and
log-angle error0.0020000303156592, each below0.0025. The long record separates
this particular pair: errors0.2500011336336765 and0.2500018196595889. This is a
nearby independent witness using a declared discrete two-point window measure;
it is not yet a reproduction of the parent's proposed continuous windows.

All four 90-digit replays agree with saved 70-digit results at all65 saved
significant digits. The zero reported discrepancy reflects that serialization,
not a proof of exact arithmetic. Incidence residual tests and tetrad norm
tests passed. Capture records4.720632533s, maxRSS27840KiB, address-space cap
2GiB, no wall/CPU cutoff, returncode0 and empty stderr. Exact commands, versions,
equations, records and capture hashes are retained.

## Tighter continuous-window interval derived independently

Let W(t)=mean_{s in[-w/2,w/2]}Y(t+s), with one identical nonnegative normalized
window at both centers. If |Y'-H|<=rho H+q throughout all swept windows and
the intervening gap, differentiation under the finite integral gives the same
bound for W'. No point derivative is extracted from observed samples.

Let d be the observed increment, deterministic error per mean<=epsilon, nominal
time difference T, and center error<=sigma. For T>2sigma and d+2epsilon>=0,

 H_lo=max(0,[(d-2epsilon)/(T+2sigma)-q]/(1+rho)),
 H_hi=[(d+2epsilon)/(T-2sigma)+q]/(1-rho).

Proof: upper drift bound is positive, so its maximum uses T+2sigma. For the
upper H bound either the lower drift bound is nonnegative and its minimum uses
T-2sigma, or H<q/(1-rho), already below the stated H_hi. Clipping H_lo at0
handles a negative increment lower bound. Strict positivity of H_lo is required
for a finite upper bound on1/H. These formulas need0<=rho<1. Unknown source
normalization cancels; arbitrary unknown source drift does not.

For positive theta with |-(log theta)'-H|<=rho_A H, the arithmetic window mean
M=mean(theta) also satisfies |-(log M)'-H|<=rho_A H: M'/M is a positive
theta-weighted mean of theta'/theta. Consequently absolute deterministic angle
errors epsilon_A can be propagated before taking logarithms. If all a_i-
epsilon_A>0, the true decreasing-angle log ratio lies between

 d_lo=log[(a0-epsilon_A)/(a1+epsilon_A)],
 d_hi=log[(a0+epsilon_A)/(a1-epsilon_A)].

For d_hi>=0, H lies in
[max(0,d_lo/((1+rho_A)(T+2sigma))),
 d_hi/((1-rho_A)(T-2sigma))]. A lower ratio below0 yields only H_lo=0.
This distinguishes mean angle from mean log-angle, incorporates finite
windows, and exposes the absolute resolution requirement as theta decays.

No universal inverse uniqueness follows. Unknown frame motion or centroid
motion can imitate angular drift; receiver energy and source geometric values
remain nuisance parameters within the class; unknown tail membership, image
selection and source persistence remain physical-interface limits. A separating
long record for two histories is not a proof that every distinct H is excluded.
