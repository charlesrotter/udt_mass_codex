# ADVERSARIAL REVIEW 1 — full independent recompute + completeness attack (O3)

Date 2026-08-07 | branch grok | reviewer: R1 (hostile; independent recompute).
Method: `review1_recompute.py` written FRESH (exact sympy, float-free; 108 checks ->
`review1_output.txt`, all True except one deliberately-paired adjudication key). `derive_o3.py`
was NOT opened until my own recompute had run; it was then diffed key-by-key. Nothing committed.

## 1. D1 — the selection map, cell by cell (independent re-derivation)

Every D1 cell reproduced. Agreements (my keys in `review1_output.txt`, R1_*):

- **S1 proper:** (i) finite iff n<2, value 2R_w/(sqrt(c0)(2-n)); n=2 log-divergent; n>2
  power-divergent [R1_S1_i_*]. (ii) divergent; (ii') divergent all alpha (integrand >=1,
  ->oo, infinite range); (iii) n=2 edge finite iff p<-2 (p=-2 divergent); ESS divergent
  (e^{1/(2s)} >= 1/(2s), harmonic). ALL AGREE.
- **S2 optical == c*travel (lock; O2-verified identity carried, not re-derived):** (i) finite
  iff n<1, value R_w/(c0(1-n)); n=1 exactly log-divergent with exact partial -R_w ln u /c0 and
  rate ell = 2R_w*delta/n at c0=1 (my rate check DERIVES delta from A symbolically — see §4 on
  the vacuity of their rate key); (ii)/(ii') divergent; (iii) n=1 edge finite iff p<-1; ESS
  divergent. ALL AGREE.
- **S3 areal:** wall at R_w for (i)/(iii)/ESS, at infinity for (ii)/(ii'). AGREE (definitional).
- **S4 r*sqrt(A):** (i) ->0, interior max at u=n/(n+2) exactly [R1_S4_i_interior_max_*];
  (ii) ->0, max at r=2X; (ii') three regimes CONFIRMED: alpha=1 witness divergent-monotone,
  **alpha=2: v = rX/(X+r), derivative X^2/(X+r)^2 > 0 (monotone), wall value X** — the surprise
  cell is REAL; alpha=3 witness ->0; critical point at r=2X/(alpha-2) for alpha>2; (iii)
  witnesses ->0; ESS ->0. AGREE — with one scope caveat on (iii), §3-A2.
- **S5 d_L = r/A:** the identity ln d_L = 2*delta + ln r is exact (algebraic); divergent in
  every class and member checked. AGREE — one gloss mis-scoped, §3-A4.
- **S6 z/depth:** divergent in every class, definitional. AGREE.
- **S7 infall (proviso eps^2 > sup A):** exact witness c*tau = 2R_w(sqrt(1+h^2)-h) at n=1,
  c0=1, eps^2=1+h^2 REPRODUCED; class-(i) integrand bounded (sup 1/h at r=0, wall limit
  1/sqrt(c0+h^2)) over finite range => finite ALL n; (ii)/(ii') integrand >= 1/eps over
  infinite range => divergent; ESS wall limit 1/eps, sup A = e^{-1/R_w} < 1 => finite.
  AGREE — except the (iii) sub-cell needs a scope amendment (§3-A2: for p>0 the proviso is
  UNSATISFIABLE from r=0, machine-checked A -> oo at the observer end).
- **S8/S9a/S9b:** cited from O2/O1 consolidated, class-independent; citation use verified
  against the O2 CONSOLIDATED text (inf = 0 depth-only; full budget divergent-protective;
  finite-chain non-attainment). Correctly carried, not re-derived — legal.

Role split (§2 of the notes): the distance-role/rapidity-role assignment follows from the
cells and is reproduced. S5's "distance name, rapidity role" is right (depth-carrier identity
exact). No branch is mis-classed.

## 2. D2 — approach profiles: every exponent/coefficient reproduced

- **kappa table CONFIRMED, and the exactness claim is TRUE:** the residual
  delta - kappa*ln(1/sigma) is EXACTLY u-independent for S1/S2/S3 (symbolic d/du = 0, my
  independent parametrization) — kappa_areal = n/2 (const (n/2)lnR_w - (1/2)ln c0 exact),
  kappa_proper = n/(2-n), kappa_optical = n/(2(1-n)). S7: sigma7/u -> R_w/(c*eps), so
  kappa = n/2 asymptotically with shift (n/2)ln(R_w/(c*eps)) — their notes/table write
  R_w/eps (c=1 implicit) and drop the -(1/2)ln c0 of the constant: cosmetic, flag §3-A6.
- **General-m relation CONFIRMED:** kappa = n/(2(1-nm)) with exact u-free residual;
  1/kappa = 2/n - 2m linear in m slope -2; reciprocal spacing areal->proper->optical
  exactly 1, n-free. [R1_D2_general_m_*]
- **Class-(iii) interior log-log corrections CONFIRMED and STRENGTHENED:** I derived the
  coefficient for GENERAL m: integrand A^{-m} ~ u^{-nm} t^{mp}, sigma ~ u^b t^{mp}/b
  (b = 1-nm), inversion gives ln-ln coefficient (p/2)(nm+b)/b = p/(2b) = (kappa/n)p —
  reproducing areal p/2, proper p/(2-n), optical p/(2(1-n)) in one identity
  [R1_D2_loglog_coeff_general_m_eq_p_over_2b]. Their L'Hopital reduction 1/(q - p/(2t)) -> 1/q
  reproduced exactly. Their per-measure coefficients are RIGHT.
- **DISAGREEMENT (the one numeric dispute): the inversion-witness constant.** Notes §4b claim
  "witness inversion limit (n=1, p=2): the residual converges (= ln 4)". My recompute: with the
  member's ACTUAL exact remaining length sigma1 = 2 e^{-t/2}(t+2) (antiderivative verified by
  differentiation), the residual delta - 1*ln(1/sigma1) - 2*lnln(1/sigma1) -> **ln 8, not ln 4**
  [R1_D2_iii_S1_inversion_residual_converges, R1_ADJ_actual_sigma_residual_eq_log8]. Their
  machine key computes the residual against the LEADING FORM L(t) = t/2 - ln t (a stand-in for
  ln(1/sigma), dropping the factor-2 and the (t+2)-vs-t shift), which does give ln 4
  [R1_ADJ_their_leading_form_residual_eq_log4]; the difference is exactly ln 2
  [R1_ADJ_difference_is_log2]. The load-bearing content (residual CONVERGES; kappa=1; ln-ln
  coefficient 2) is TRUE either way; the stated VALUE ln 4 is wrong for the member itself.
  AMENDMENT A1 owed (not a kill; constants at this witness are not load-bearing, but the notes
  print one and it is the wrong one under the natural reading).
- **Edge members CONFIRMED exactly:** proper n=2, p<-2: ell = t^{(p+2)/2}-class, delta ~ t,
  delta ∝ (1/ell)^{2/|p+2|}; witnesses p=-4 (delta*ell -> 1 at units 1; exponent 1) and p=-3
  (delta*ell^2 -> 4; exponent 2) reproduced with exact partial integrals. Optical n=1, p<-1:
  delta ∝ (1/sigma)^{1/|p+1|}; p=-2 witness delta*sigma -> 1/2 reproduced. Class change
  (log -> power-law depth) CONFIRMED.
- **ESS CONFIRMED:** delta = 1/(2 sigma3) EXACT on the areal branch (no log regime);
  S7 same class via integrand limit. AGREE.
- **S4 alpha=2 exact profile CONFIRMED:** sigma4 = X^2/(X+r) and (1+z)*sigma4 = X for ALL r;
  delta = ln(1/sigma4) + ln X, kappa = 1 globally exact. AGREE.

## 3. D3 + completeness attack: results and AMENDMENTS OWED

D3 reproduced: joint witness n=1/2 (proper 4R_w/(3sqrt(c0))-class value, optical exact);
S4-genuine atom excluded by each of S1/S2/S3/S7 (integrand-unbounded / chart-radius-oo /
nonzero-integrand-limit keys all reproduced); kappa sweeps (0,oo) in every surviving window;
the lattice chain S2 => S1 => S3==S7 verified in-family (window inclusions + edge members:
{n=1,p<-1} lands inside the S1/S3/S7 survivors; {n=2,p<-2} inside S3/S7); S3==S7
verdict-degeneracy holds across (i)/(ii)/(ii')/(iii)/ESS; R-2 ("never softer than log")
verified in-family — (iii) interior members stay leading-log (witness limit delta/ln(1/sigma3)
-> n/2 at p=-2), edge/ESS members escape UPWARD only; R-3 reproduced. R-1's qualified form
(break on S4) is honest and correct.

**AMENDMENTS (none breaks a cell; all are scope/tagging/constant repairs):**

- **A1 (constant, wrong as printed): the inversion-witness "= ln 4".** Against the member's
  actual sigma1 the constant is **ln 8**; ln 4 is the residual against the leading-form
  stand-in L(t) = t/2 - ln t. Fix: either print ln 8, or scope the sentence "residual taken
  w.r.t. the leading form of ln(1/sigma)". Machine-adjudicated (§2). Class content unaffected.
- **A2 (quantifier/scope, the real find): ALL class-(iii) cells are WALL-LOCAL.** The frozen
  (iii) profile A = c0 u^n(-ln u)^{-p} is SINGULAR at the observer end r=0: A(0)=oo for p>0,
  A(0)=0 for p<0 (so phi(0)=0 normalization cannot hold), and for the SURVIVING edge-rescued
  members the separation integrals diverge at the OBSERVER end (optical p<-1: 1/A ~ (1-u)^p
  non-integrable at u->1 [R1_ATTACK_S2_iii_edge_observer_end_divergent_pm2]; proper p<-4-class
  same [R1_ATTACK_S1_iii_edge_observer_end_divergent_pm4]). O2 computed these integrals on
  (log2, oo) — i.e. from r = R_w/2 — so the verdicts were always wall-local; O3's D1 table does
  not carry that tag. Consequences needing the tag: (a) S1/S2 (iii)-edge cells mean "finite
  separation-to-wall from any interior point r0>0" (with interior regularized), NOT "from the
  observer"; (b) **S7 x (iii) "F [bounded integrand, finite range]" is FALSE from r=0 for p>0**
  (A unbounded => proviso eps^2 > sup A unsatisfiable; machine-checked
  [R1_ATTACK_S7_iii_p_pos_A_unbounded_at_observer]) — the cell is comment-only in derive_o3.py
  (no key) and must be restated wall-local; (c) S4 x (iii) "->0 NON-MONOTONE / wall at zero
  separation equal to the observer's own value" fails at literal reading for p>2 (v -> +oo at
  the observer end [R1_ATTACK_S4_iii_observer_end_divergent_p3]); the honest degenerate content
  is "S4-value -> 0 at the wall (wall-locally monotone)". One tag on the (iii) row fixes all.
- **A3 (tagging honesty on the machine record): "94 machine-check keys, all True" overcounts
  the CHECKED content.** Hardcoded-True bookkeeping keys (cannot fail): S3_ii_wall_at_infinite_r,
  S3_iiprime_wall_at_infinite_r, S3_iii_wall_at_finite_Rw, ESS_S3_wall_at_finite_Rw,
  D3_S4gen_excluded_S3_chart_radius_oo. Vacuous-as-checks (algebra that cannot fail, content
  living elsewhere): S2_i_n1_rate_ell_eq_2Rw_delta (checks R_w*t - 2R_w*(t/2) = 0, i.e. t = t —
  delta = t/2 was substituted by hand; my recompute derives delta from A and confirms the rate,
  so the CLAIM is true but their KEY could never have caught it false);
  S7_comparison_integrand_ge_1_over_eps (checks a - (a - b) = b, not the inequality);
  S5_lndL_identity (definitional algebra — intrinsically so, acceptable);
  D2_general_m_reciprocal_kappa_linear + both spacing keys (arithmetic of already-derived
  kappas). Also comment-only cells with NO key: S7 x (iii); S2 x ESS ("same comparison").
  None of this hides a wrong cell (my independent keys cover every one of them and they pass) —
  but the notes' "94 keys" line should say ~10 are bookkeeping/identities and 2 cells are
  keyless, per verifier-honesty norms.
- **A4 (gloss scope): §2's "near the wall d_L = R_w e^{2delta}(1+o(1))"** holds only for
  finite-chart-radius classes ((i)/(iii)/ESS); in (ii)/(ii') d_L = r*e^{2delta} with r -> oo
  [R1_ATTACK_S5_ii_dL_eq_r_times_e2delta_not_Rw]. Divergence verdict unaffected; scope the gloss.
- **A5 (completeness/neutrality on the headline surprise): the S4-genuine alpha=2 atom is
  itself a KNIFE-EDGE and should carry the same "not class-stable" tag n=1 carries.** Tested
  (the natural log-corrected neighbors A = (1+r/X)^{-2} ln(e+r/X)^{nu}): nu>0 => v -> oo
  (monotone divergent, posit fails); nu<0 => v -> 0 (degenerate)
  [R1_ATTACK_S4_iiprime_logcorr_*]. So genuineness is destroyed either way by log corrections —
  exactly the fragility for which O2's license demoted n=1's edge status. The atom SURVIVES as
  an in-family fact (no addition proposed; F-SHOP-CLASS respected — this is a tag, not a new
  member), but headline SURPRISE (1) must not be read as class-stable. Bonus: this defuses the
  completeness pressure the new knife-edge would otherwise create (the resolution is "no new
  genuine members nearby", machine-checked at witnesses).
- **A6 (cosmetic): S7 constants drop c and -(1/2)ln c0** (script sets c=1 silently; table says
  R_w/eps). State the units convention where the S7 const/shift is printed.

**Strengthening found (report, no change owed):** R-1's exclusion of (ii)/(ii') on S1/S2/S7 is
actually PROFILE-GENERAL, not merely family-internal: any A -> 0 wall at infinite chart radius
has integrand >= 1 (S1, S2) or >= 1/eps-limited-below (S7) eventually, over an infinite range —
so "infinite-radius wall excluded" on those branches holds for EVERY A->0 profile, matching the
O2 inclusion hierarchy's profile-generality. (S3 is definitional.) The notes may cite this or
leave scoped; either is honest.

## 4. False-generality / quantifier hunt — outcomes

- "Exact, not asymptotic, for S1/S2/S3" — TRUE (verified symbolically); S7 correctly asymptotic.
- "All n, all p, essential included" (S3/S7 minimal demand) — TRUE with A2's wall-local tag on
  (iii) and the S7 proviso noted (already stated for S7; (iii) sub-case was the gap).
- "Never softer than logarithmic" (R-2) — holds for every member x surviving branch in the
  frozen family (leading kappa > 0 everywhere; corrections only harden). No counterexample found.
- S2 == travel-time equivalence — carried on O2's verified lock identity; stays one class here.
- Areal-anchor chart tag — carried in §3's branch definitions; D2's S3 row does not repeat it
  (minor; R2's beat, no cell effect).
- eps^2 > sup A proviso — correctly stated and satisfiable for (i)/(ESS)/(iii,p<0); the p>0
  failure is A2(b).

## 5. VERDICT

**SUSTAINED-AMENDED.** Every D1/D2/D3 cell verdict, every exponent kappa(n, measure), the
general-m law 1/kappa = 2/n - 2m, the reciprocal spacing 1, the lattice chain + isolated atom,
and all four headline surprises are independently reproduced (108 checks, own scripts, probe
code unopened until after). NO KILL. Amendments owed before consolidation: **A1** (ln 4 -> ln 8
or re-scope the residual definition), **A2** (wall-local tag on every class-(iii) cell; restate
S7 x (iii); soften S4 x (iii) "non-monotone" wording), **A3** (bookkeeping-key honesty on the
"94 keys" line; key or tag the two keyless cells), **A4** (scope the d_L gloss), **A5**
(knife-edge/not-class-stable tag on the S4 alpha=2 atom, same standard as n=1's license),
**A6** (units note). Machine record: `review1_recompute.py` -> `review1_output.txt` (108 True;
1 intentional False adjudication twin R1_D2_iii_S1_inversion_const_eq_log4, whose True twin is
the ln 8 key).

— R1, 2026-08-07. Not committed; nothing banks without R2 + Charles.
