# D1 — two-mode calibration rank needs a nonzero coefficient

Direct whole-candidate review, 2026-09-13. INITIAL_CANDIDATE.md section5 says:
"With known two-mode phases, one linear amplitude direction remains after Q_A is fixed."
The preceding family permits arbitrary fixed known phases. Let
phi_j=pi/2-k_j xi_A (mod pi), j=1,2. Then both source cosines vanish and
Q_A=a_1 cos(theta_1A)+a_2 cos(theta_2A)=0 for ALL a_1,a_2. Consistent ideal
rates fix L but leave TWO amplitude directions, not exactly one.

Survivor: the linear map a -> Q_A has rank one whenever at least one source
cosine is nonzero, and then a one-dimensional nullspace; at both nodes it has
rank zero and a two-dimensional nullspace. For the supplied benchmark phi1=0,
xi_A=.7, k1=.75, cos(.525) is nonzero, so the intended known-phase StageC
slice and all finite records are unaffected. No new physical premise is needed.

Smallest source-preserving repair: keep the frozen candidate and record an
explicit controlling qualification in the reviewed overlay: one amplitude
freedom remains under the nonzero coefficient/rank-one hypothesis; the both-node
case retains two. Unknown phases/extra modes remain outside the one-dimensional
claim. The objection concerns a sentence's general quantifier, not metric
completion, propagation, physical adoption, or the numerical tolerance contract.
