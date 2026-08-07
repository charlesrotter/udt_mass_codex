# ADVERSARIAL REVIEW 1 — independent recompute of every cell + completeness attack

Reviewer: Claude (Fable 5), fresh context | Date: 2026-08-07 | Branch: grok
Protocol: `derive_o2.py` NEVER OPENED. All cells recomputed in fresh sympy/mpmath:
`adversarial_recompute_1.py` (26 symbolic checks, all True, no False entries;
output `run_review1_part1.txt`) + `adversarial_recompute_2.py` (budget-infimum
construction, protective-budget bound, generality probes; `run_review1_part2.txt`).
Ground read at source only: O1 DERIVATION_NOTES (CONSOLIDATED), the c_eff integration
doc, `simple_metric_L_native_optical_derive_results.md`, the 08-05 copresence notes.

## 1. Realization cells — per-cell verdicts

| Cell | Verdict | Independent result |
|---|---|---|
| proper, class (i) | **CONFIRMED** | finite iff n<2; value 2R_w/(sqrt(c_0)(2−n)) exact at general c_0; witnesses 4R_w/(3√c_0), 2R_w/√c_0, n=2 log-divergent — all reproduced |
| proper, class (ii) | **CONFIRMED** | ∫e^{r/2X}dr = ∞ |
| optical, class (i) | **CONFIRMED** | finite iff n<1; value R_w/(c_0(1−n)); n=1 partial = −(R_w/c_0)ln u exact; n=2 power-divergent |
| n=1 log rate | **CONFIRMED** | ℓ_opt = 2R_w·δ exact at c_0=1 (δ = −½ln u); the "/n" in the notes' "2R_w δ/n" is meaningful ONLY at n=1 (for n≠1 ℓ_opt is not ∝ δ) — wording flag, no error |
| optical/travel time, class (ii) | **CONFIRMED** | divergent; T ≡ ℓ_opt/c identically under the lock (c_eff = cA at observer normalization) |
| class (iii) edges | **CONFIRMED** | optical n=1 finite iff p<−1 (value 1/a at p=−(1+a); P=1 edge divergent; witness 1/ln2); proper n=2 finite iff p<−2 (value 2/a) |
| areal | **CONFIRMED** | (i) → R_w finite all n; (ii) divergent |
| redshift z | **CONFIRMED** | divergent both classes. NOTE: 1+z = A^{−1/2} presumes c_0=1; general c_0 gives 1+z = √(c_0/A) — same verdict. See normalization flag below |
| d_L = (1+z)²r | **CONFIRMED** | (i) divergent all n (r→R_w>0, A→0); (ii) divergent |
| d_A both conventions | **CONFIRMED** | adopted d_A=r: R_w finite (i) / divergent (ii). Variant r/(1+z)=r√A → 0 both classes. Etherington + banked d_L=(1+z)²r FORCES d_A=r (variant would give d_L=(1+z)r ≠ banked) — the adjudication is exact and correctly reasoned |
| infall proper time | **CONFIRMED** | re-derived from scratch: conserved e = A dt/dτ ⇒ (dr/dτ)² = c²(e²−A) (symbolic check True); integrand → 1/(ce) finite nonzero at wall; explicit witness n=1, e=1: τ = 2R_w/c; (ii) divergent (dr/dτ → ce over infinite range). Worldline posit IS stated in the notes (tagged). One unstated proviso: reaching the wall needs e² > A along the path — automatic for from-rest infall on these monotone-decreasing profiles; for a non-monotone A choose e² > sup A. Verdict (finite, all n) robust |

**Normalization flag (cosmetic, no verdict changes):** the notes declare observer
normalization φ(0)=0 yet carry c_0 general; A(0)=c_0 forces c_0=1 under that
normalization. c_0 only rescales values; the z/d_L rows implicitly use c_0=1. Suggest
one sentence tying c_0≠1 to a relocated observer or dropped normalization.

## 2. Abstract rows

**(a) depth δ_t:** CONFIRMED — divergent, definitional; O1 cited correctly.
**(b) leg count:** CONFIRMED — O1's amended theorem + the infinite-chain caveat both
quoted faithfully (checked against O1 CONSOLIDATED verbatim content).

**(c) Depth budget inf-over-chains: AMENDED — the infimum is exactly 0. The row's
"F (≤ ~0.85)" materially understates its own finding.** Settled constructively:
1. Pure boost legs are strain-identity arrows (C = I, verified symbolically): they are
   typed-invertible comparison arrows of DEPTH ZERO — the budget does not charge them.
2. The O1 trace law recomputed independently (symbolic + numeric): cosh(2δ_comp) =
   cosh(2(p+q)) + 2sinh²(w)sinh(2p)sinh(2q), det C = 1; unbounded in w at fixed
   p, q > 0 (coefficient sinh(2p)sinh(2q) > 0 strictly).
3. Greedy construction: legs of depth ε/2^k with growing twists. For total budget
   ε = 0.1, 0.01, and 0.001 the chain accumulates to the wall — final λ_t down to
   5.4e−22 at total depth budget 0.000999, EVERY truncation regular and
   timelike-labeled (eigenline η-causality checked each step; isometry legs leave
   truncation strains unchanged, so truncation depths increase monotonically).
4. This works for every ε > 0 ⇒ inf over wall-accumulating chains of Σ|δ_i| = 0.
   Not attained: a zero-budget chain is isometry-only, strain ≡ I, λ_t ≡ 1.
**Honest entry: "0 (infimum, not attained) — the measure is DEGENERATE for the wall:
it assigns the wall zero separation."** Stronger still: at the abstract-groupoid layer
the same construction reaches ANY finite depth target at arbitrarily small budget, so
the pure-depth budget is a degenerate pseudo-metric globally, not merely wall-finite.
The probe's text explicitly declined to claim inf=0 ("not determined here") — honest,
but determinable, and the determination flips the row from "finite separation" to
"zero separation," a materially different (and more striking) statement.

## 3. Completeness attack — findings

**(A) MISSING ABSTRACT MEASURE (material, changes the abstract-sector structure): the
FULL non-compact budget** Σ(|δ_i| + |w_i|) (depth plus non-compact twist rapidity;
twist rapidity is invariant conjugacy data between consecutive legs). PROVABLY
wall-PROTECTIVE: λ_max(C) ≤ σ_max(M)² and ln σ_max is subadditive over products with
σ_max(D_δ) = e^{|δ|}, σ_max(B_w) = e^{|w|}, hence δ_comp ≤ Σ(|δ_i| + |w_i|) exactly
(200 random-chain numeric trials: zero violations). Accumulating to the wall forces
the full budget → ∞: DIVERGENT. With this row the abstract sector reads cleanly:
leg-count protective; full budget protective (the SR-like functional that survives);
pure-depth budget degenerate (0) — O1's budget-breaking is charged ENTIRELY to the
uncharged twist channel. Recommend adding this row.

**(B) Non-radial paths — rows survive AS TRUE DISTANCES (strengthens):** under the
lock + areal anchor, dl ≥ dr/√A pointwise, so the radial path minimizes proper length
(and dl/√A ≥ dr/A minimizes Fermat length): the proper row IS the geodesic distance,
the optical row IS the least optical path. No cheaper non-radial route to the wall.

**(C) Radar distance:** ≡ optical/travel-time equivalence class (round-trip Fermat);
already covered — worth one line in the degeneracy note.

**(D) Parallax distance — candidate missing observable row (non-blocking):** a
standard observable-anchored distance requiring null-congruence/beam data beyond the
areal anchor; not settled here; either an O2-OBSTRUCTED entry or a later computation.
Enumeration gap flagged, structure of the table unchanged.

**(E) MISSING APPROACH CLASS (one cell affected): infinite-radius walls with
sub-exponential decay** — class (ii′): A ~ r^{−α}, α > 0 (not representable in
(i)/(ii)/(iii)). Every class-(ii) column entry generalizes to ANY wall at infinite
chart radius (A ≤ 1 near the wall ⇒ integrands ≥ 1 over infinite range) EXCEPT the
d_A-variant r/(1+z) = r√A = r^{1−α/2}: → ∞ (α<2), FINITE NONZERO (α=2), → 0 (α>2).
So the variant cell's "→ 0" is exponential-specific, and the "near-total degeneracy
in class (ii)" note is a general infinite-radius-wall fact for all rows except the
variant row. One-cell scoping amendment.

**(F) Oscillatory profiles:** exist outside (i)-(iii) (e.g. A = u^{3/2}(2+sin(1/u))/3;
numerically: proper converges ≈ 4.93, optical diverges) — the family is not
exhaustive, but such profiles obey the general inclusion chain (sec. 4), so only the
sharp iff-in-n criteria are family-scoped, as the notes already imply. n=0 (no wall)
correctly out of scope; n<0 is the λ_t→∞ end — outside the frozen question (covered
abstractly by O1 reversal; a realization table for that end was not owed).

## 4. The inclusion chain — CONFIRMED and STRENGTHENED to profile-general

For ANY A → 0 profile (any class, oscillatory included): near the wall A < 1, so
1/A > 1/√A > 1 pointwise, giving exactly: optical-finite ⇒ proper-finite ⇒
chart-range-finite ⇒ areal/d_A-finite (and infall-finite given e² > sup A). Never
conversely: witnesses n = 3/2 (proper yes, optical no) and n = 3 (areal yes, proper
no). The notes state this inside the class-(i) grading; it is in fact CLASS-GENERAL —
a free upgrade the consolidation should take.

## 5. The P-opt / knife-edge adjudication (sharp)

dℓ_opt/dφ = 2R_w u^{1−n}/(c_0 n) — constant iff n=1 (value 2R_w/c_0 = κ, so κ = 2X at
c_0=1, matching the banked X = κ/2). Therefore: **within pure class (i) at the
observer normalization, P-opt ⇔ n=1 ⇔ the optical knife-edge — exact.** But over the
declared full family the identification is ONE-WAY: P-opt ⇒ knife-edge, NOT
conversely. Counterexample verified: the class-(iii) member n=1, p≠0 sits at the
knife-edge yet has dℓ_opt/dφ = −2R_w(−ln u)^p ln u/(c_0(p−ln u)) — non-constant, so
it violates P-opt while sharing the n=1 edge. Also P-opt is a GLOBAL exact law
(forces A = 1−r/X everywhere) while knife-edge membership is a near-wall asymptotic
tangency. "P-opt IS the optical knife-edge" is a loose gloss; the exact statement:
P-opt selects the unique pure n=1 member, which sits exactly ON the knife-edge; the
edge itself contains non-P-opt profiles (either side resolvable by log corrections).
The notes' own phrasing ("reproduces the banked L slogan as the n=1 knife-edge") is
compatible but should carry the one-way arrow explicitly.

## 6. Cross-checks (all six re-verified independently)

1. L proper = 2X — CONFIRMED (exact). 2. L optical log-divergent at rate ℓ_opt = 2Xδ
— CONFIRMED (exact partial integral). 3. Exponential proper divergent — CONFIRMED.
4. Quadratic (n=2) proper divergent — CONFIRMED. 5. Banked family A=(1−r/X)^{1/m}
finite iff m>1/2 ⇔ our n=1/m<2 — CONFIRMED (reduce_inequalities: 1/m<2 ⇔ m>1/2 on
m>0). 6. d_L/X = z(z+2) ⇔ d_L=(1+z)²r on L — CONFIRMED symbolically. No disagreement
with any banked cell.

## VERDICT

- Item 1 (realization cells): **CONFIRMED** (every cell; one cosmetic c_0/φ(0)
  normalization flag; one wording flag on "2R_wδ/n"; one infall proviso e² > sup A).
- Item 2 (abstract rows): (a),(b) **CONFIRMED**; (c) **AMENDED — inf = 0 exactly,
  measure degenerate for the wall (and globally, at the abstract layer)**.
- Item 3 (completeness): two real findings — the protective FULL budget row
  (missing measure, material) and class (ii′) power-decay walls (missing class,
  one-cell scoping of the d_A-variant entry). Proper/optical rows proven to be true
  (path-minimizing) distances. Parallax flagged as candidate row, non-blocking.
- Item 4 (inclusion chain): **CONFIRMED + STRENGTHENED** (profile-general, not
  class-(i)-specific).
- Item 5 (cross-checks): **CONFIRMED**, all six.

**OVERALL: O2-TABLE SUSTAINED — AMENDED.** No cell broken; no F/D verdict overturned.
Owed edits before banking: (1) budget row entry → "0 — degenerate (not attained)";
(2) add the protective full-budget row (or record it as a named omission); (3) scope
the d_A-variant class-(ii) cell as exponential-specific (ii′ family); (4) state the
P-opt/knife-edge identification as one-way; (5) the cosmetic c_0 normalization note.
