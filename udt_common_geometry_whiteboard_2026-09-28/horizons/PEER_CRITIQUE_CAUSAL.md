# Horizons peer critique of the sealed causal lane

Reviewer context: /root/cgw_horizons, after completing/sealing its independent
horizon argument. This is a specialist peer check, **not** the later fresh
adversarial review and not different-model verification. Runtime model/version
is not independently attested. Target causal INITIAL_NOTE SHA256 independently
verified as 04ab83d23ee6f695dc1a6cd80c773163129a45703e0cf29b47a0d78160fcb75b.
The initial horizon note/seal were left unchanged. No sibling files were edited.

Verdict: **no load-bearing algebraic defect found in the specified fixed-base,
positive-domain comparison.** The conformal clock/screen weights, affine
reparameterization, one-cone witness, finite-source proper-clock drift and
two-sided complete-null-line rigidity survive direct checks. Three presentation
and domain clarifications should accompany synthesis; none needs a new physical
premise or replacement equation. The conditional Einstein antecedent must remain
visible, and the witness must not be summarized as all possible clock data.

## What was examined and independently checked

Read the sealed INITIAL_NOTE, CHECK_FREEZE, check_causal.py, run metadata, source
pins and initial seal; then read G374/G375's controlling reviewed scope summaries
and the load-bearing G348 screen-area/observer normalization equations. Current
G312 filter-only authority was already read independently in the horizon lane.
No original historical source packages were fully replayed. The causal author's
tensor utility was inspected for check scope but was not imported or reused.

PEER_CHECK_FREEZE.md and check_causal_peer.py record a separate 12-identity
symbolic calculation with Python 3.10.12/SymPy 1.13.1, no observational data,
no copied tensor engine, exact-zero residuals and empty stderr. The command was

```sh
timeout 600s python3 udt_common_geometry_whiteboard_2026-09-28/horizons/check_causal_peer.py > udt_common_geometry_whiteboard_2026-09-28/horizons/PEER_CHECK_STDOUT.json 2> udt_common_geometry_whiteboard_2026-09-28/horizons/PEER_CHECK_STDERR.txt
```

It exited 0 in under one second under two-thread/2-GiB caps. This is independent
small-algebra implementation and peer rederivation; it is not independent
rederivation of every G374/G348 theorem, a formal proof, or a full global audit.

## 1. Affine and clock/screen normalization: survives

With ghat=u^-2 g and Uhat=uU, the connection difference gives
nabla_hat_k k=-2 k(log u) k for a g-affine null k. Therefore khat=u^2 k is
affine in ghat, and omegahat=u omega. This gives rhat/r=u_e/u_o, while the
quotient-screen area weight at e gives dhat_o=d_o/u_e. Thus

    rhat dhat_o = r d_o/u_o.

The endpoint factors are in the correct places. The product is equal only after
the stated observer calibration u_o=1; it is not constant along a ray or a law
of luminosity transport. Aberration factors under matched endpoint boosts are
identical between the conformal geometries, so they do not defeat the comparison.

For u=a+bs and khat=u^2 k,

    d shat/ds=1/(a+bs)^2,
    shat-shat(0)=s/[a(a+bs)].

At the observation event omegahat_o=a omega_o. If both reference frequencies
are independently normalized to 1, use khat_norm=(u^2/a)k. The corresponding
affine parameter is a times the preceding expression. The causal note's
normalization sentence is correct, including for a!=1; finite versus infinite
extent is unaffected by this positive constant. The b=0 limiting case remains
shat=s/a^2, despite the author's checker declaring b nonzero for its symbolic
Möbius test. The formula itself and direct differentiation include b=0.

## 2. One-cone curvature/clock degeneracy and drift: survives at stated data scope

Write Q=-t^2+|x|^2 and u=1+kappa Q/2. An independent conformal Ricci calculation
uses Hess(u)=kappa eta, Box(u)=4kappa, |du|^2=kappa^2 Q. In four dimensions,

    Ric_hat = 2u^-1 Hess(u)
              +[u^-1 Box(u)-3u^-2|du|^2]eta
            =6kappa u^-2 eta.

Hence R_hat=24kappa. On t=-s, x=s n, u=1 exactly, du along the null tangent
vanishes, and the normalized ray remains affine. Constant-curvature null
screen tide is zero by contraction with k^2=0 and screen orthogonality.
Accordingly d_o=s and the specified one-cone endpoint clocks/ratios agree.
This does not rely on the reused source tensor utility.

For fixed source x=L n, t_e=t_o-L,

    u_o=1-kappa t_o^2/2,
    u_e=u_o+kappa L t_o,
    r=u_e/u_o, d_o=L/u_e, d/dT_o=u_o d/dt_o.

Direct differentiation gives r'(0)=kappa L and d_o'(0)=-kappa L^2; the product
drift vanishes at zero. The proper-clock conversion is required away from zero.
The inferred R_hat=24r'(0)/d_o(0) is valid only in this family and prescription.
No detector access or general curvature reconstruction follows.

## 3. Actual future return: additional check, no inverse-segment error found

The causal note explicitly avoids equating inverse-segment reciprocity with a
later return, and its example supports that distinction. Consider a prompt
clock-marker relay: central emission at t=0, source reception/re-emission at
t=L,x=L n, central reception at t=2L. For kappa>0 require 2kappa L^2<1 so all
these finite segments stay in the positive domain. The coordinate travel maps
each have derivative 1. Proper-clock factors are therefore

    r_forward=1,
    r_later_return=1/(1-2kappa L^2),
    r_echo=1/(1-2kappa L^2).

The later return is generally not the inverse of the forward factor. The exact
general relay derivative is u_central(t)/u_central(t+2L). This direct event-map
check supports the causal note's wording; it supplies no native physical relay
or population. Future-return comparisons must retain these distinct events.

## 4. Global positivity and completeness: survives, with its full antecedent

On each complete base-null geodesic, the conformal Einstein equation makes
u(s)=a+bs for every s in R. Positivity for every s forces b=0. Since every null
tangent starts such a complete geodesic and null directions span the tangent
space, du=0 everywhere; connectedness then makes u constant. This uses base
null completeness in **both** directions and a positive u on the **whole same
manifold**. It does not require the rescaled metric to be assumed complete.

There is no counterexample from the local polynomial witness: its positive
domain is generally a proper patch, and for nonzero kappa it cannot be a
positive conformal factor on all Minkowski space. Likewise u=1-Ht on t<1/H
is a proper patch. It has infinite past comoving proper lookback but finite
past null affine extent; this is compatible with extension to a larger
geometry and is not an inextendible singularity claim.

The causal note appropriately distinguishes relative clock divergence C from
absolute rhat=C r, which also depends on the base clock ratio. Its rigidity
statement is a restriction on this conditional class, not a UDT impossibility
theorem or a proof of physical X_max. G312 membership remains unclosed.

## Precision repairs recommended for the parent synthesis

| Location / potential defective reading | Reason or counterexample | Strongest survivor and smallest repair |
|---|---|---|
| Opening says “even all clock and screen measurements on one past cone” | The body correctly admits that source acceleration/clock derivatives and transverse transport can differ. Those are also possible clock-related measurements. | Say “the specified null-cone endpoint frequency/ratio, screen-radius and normalized-affine records.” Preserve the body's exclusions. |
| Past-directed s versus positive future frequency | On t=-s,x=s n, d/ds is past directed; -g(U,d/ds) is negative for future U. Ratios are unchanged, but individual positive frequencies need the future tangent. | State that s increases into the past while the future signal tangent is -d/ds, or explicitly use a positive past-ray frequency magnitude. The affine/Möbius results remain unchanged. |
| Neighboring-cone drift could be read uniformly over an unbounded cone | For kappa>0 and any fixed negative t_o, u_e=u_o+kappa L t_o becomes negative for sufficiently large L. There is no common two-sided arrival-time interval for all unbounded L in this chart. | The derivative exists for every fixed finite source, or uniformly for a bounded L family after choosing a common positive neighborhood. This already matches the finite-segment premise; state it in the headline application. |

These are scope/sign-convention clarifications, not objections to equations
(1)–(11) in their intended conventions. No candidate has been promoted, and
the fresh review remains necessary. No extra measurements, fits, field law,
source coupling, preferred center or further research task was introduced.
