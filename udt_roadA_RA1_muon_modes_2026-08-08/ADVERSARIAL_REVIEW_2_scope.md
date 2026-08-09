# ADVERSARIAL REVIEW 2 — RA1 — falsifier/scope/ledger adjudication

Date 2026-08-08 | reviewer: R2 (Fable, hostile brief: F-MUOFF / F-RETRO / F-TEMPLATE /
F-SHOP-CLASS / F-LAWHUNT / scope+ledger). Independent spot-verification performed by hand;
a fired falsifier was treated as first-class. NOT committed (per dispatch).

## What I verified by hand (not taken on trust)

- **Re-ran `derive_ra1.py` fresh**: 46/46 keys True; KEY/TOTAL lines diff-identical to the
  banked `run_output.txt`.
- **Freeze timeline**: prereg committed at 438ef424 (Sat Aug 8 23:01:13 2026); `git diff
  438ef424 -- PREREGISTRATION.md` is EMPTY (no retro-edit); the three derivation files are
  untracked (uncommitted, per dispatch). F-RETRO's timeline leg is clean.
- **Number scan**: grep for float literals / Planck / 220 / 1056 / 2.4 / acoustic / peak /
  CMB across all three files — only falsifier-language hits. K28's float-atom audit is real
  but narrow (7 audited expressions); the grep closes the file-level gap. No observational
  number anywhere.
- **Load-bearing algebra recomputed by hand**: sigma_eff = (n+min(n,2q))/2 from p=sqrt(AD)
  with A~u^n, D~R_w²u^n+h0²u^{2q} — correct. Wedge sign: e+2 = 2(2−n−q)/(2−n−2q), denom
  = 2(1−sigma)>0 on the LC side, so supercritical ⇔ q>2−n — correct. Critical-line
  coefficient: u^{−nu} = (s h0 nu/2R_w²)^{−2} gives −8ωmR_w²/(h0 nu²)/s² — correct.
  K23: 1/A² − r²/(AD) = h²/(A²D) — correct. WKB memberships (K19a–c): |v|²~s^{β/2}
  integrable (attractive LC); growing branch exp(+c s^{1−β/2}) not L² (repulsive LP) —
  correct. Empty-wedge check for n<2 (interval (2−n,(2−n)/2) empty) — correct; the q<0,
  n<2 corner is genuinely subcritical (their witness (3/2,−1)→sub confirms my algebra).

## Per-falsifier verdicts

**1. F-MUOFF — DOES NOT FIRE.** The metric matrix `g` carries symbolic h from its first
assembly (script line 31); S1–S9 all run with h symbolic and nonzero; `subs(h,0)` appears
only in K7 (h-carrier IDENTIFICATION, after the mu-on system is posed — legitimate D5
support) and the S10/D5 block. The §4(a) center analysis uses h→0 NEAR r=0 only, as the
disclosed SS3-regular profile-class property (P-RA1-8 fork), not a mixing shutoff — variant
(b) keeps h(0)≠0 and is carried. D5 is derived last from the mu-on objects. HOWEVER:
**K29 is structurally THIN** — a presence-of-h atom check would still pass if some
intermediate had been computed at h=0 and patched; it verifies vocabulary, not order. The
actual F-MUOFF discharge rests on reading the script's construction order (which I did, and
it is clean), plus this review. AMENDMENT A3: say so in §8 — "K29 is a necessary structural
witness; the order claim is discharged by script inspection + review, not by the key alone."

**2. F-RETRO — DOES NOT FIRE (incl. the subtle direction).** No observational numbers
(verified above). The h-class h0(1−r/R_w)^q was frozen in the prereg BEFORE derivation
(438ef424) — it cannot have been chosen post-hoc to make the wedge appear. Region
boundaries (sigma_eff=1; q=2−n; q=(2−n)/2) are DERIVED from machine-checked exponents, not
asserted. Witness rationals cover every named region incl. LP ones — coverage, not
curation. Exhaustiveness of the scan: I checked the omitted corners by hand — BUT found a
genuine (measure-zero) GAP, AMENDMENT A1: **the line {n=2, q<0} appears in NO region**
(R4/R5/R6 require n>2; R3 requires q=0; R2' requires q>0 there). By the derived criteria it
is LC (sigma=1+q<1; e=−1>−2 subcritical). Likewise the boundary rays q=(2−n)/2 with n≥2
(q≤0) are unclassified. Note the direction: the omitted line is LADDER-CAPABLE, so the
omission UNDER-reports discrete territory — anti-curation, honest error. Add both lines.

**3. F-TEMPLATE — DOES NOT FIRE, one wording duty.** No make-the-peaks framing; no CMB
drift (grep-clean; RA2 stays gated); the landing is the prereg's expected MIXED outcome
with LP/continuum territory given full table rows and the §9 summary naming it plainly.
The chiral-wedge finding is stated as endpoint character with the pencil caveat stamped.
BUT the two bolded flagship lines — "quantized INTRINSICALLY (no boundary datum)" (§9,
also §7 "quantizes BY ITSELF") and "the mixing never destroys a discrete region — it opens
new ones" (§6, which I verified is TRUE within the map: n<1 stays LC for every q) — are
EXCERPT HAZARDS: quoted alone they shed the wedge/counter-rotating/probe-choice/slice
scope. AMENDMENT A2 (exact wording): wherever "intrinsically quantized / no boundary
datum / quantizes by itself" is bolded, append inline: "(counter-rotating channel of the
deep-mixing wedge n>2, 2−n<q<(2−n)/2 ONLY — divergent h at the wall; scalar-probe W1,
equatorial slice, fixed-(m,omega) pencil scope)". The §6 headline gets "(within the frozen
power-law class, equatorial W1 scope)".

**4. F-SHOP-CLASS — DOES NOT FIRE.** The class used exactly as frozen; q→0 and q<0 edges
CARRIED (R3; R4/R5/R6 — the q<0 edge is where the richest structure lives, not dropped).
One addition = the center-completion fork, cause stated (D2 SS3 banked center-regularity),
D3-untouched — compliant with the prereg's "additions need stated completeness cause". The
equatorial-slice restriction is a disclosed DECLARED slice (P-RA1-2) with the wall-
classification insensitivity argued (bounded-factor squeeze) and the slice-sensitive part
(center indices) named — a scope restriction, not a curation: the dragging term driving the
wedge is present in any through-the-equator realization.

**5. F-LAWHUNT — DOES NOT FIRE.** W1 tagged THEORY(metric-native probe) in the prereg,
P-RA1-3, the scope banner, and §8; "not 'the' dynamics" repeated; W3 untouched. The
spinning-string/NUT center fork (§4b) is disclosed as a pathology needing "a posited axis
datum" — named, NOT supplied: no mechanism invented.

**6. Ledger honesty — HONEST, two nicks.** P-RA1-1..10 complete: SS9 travels (P-RA1-9 +
banner), equatorial slice (P-RA1-2), time-harmonic/real-omega with QNM out-of-scope named
(P-RA1-4), scalar-probe choice (P-RA1-3), weight choice made canonical by the K9 isometry
(P-RA1-6), pencil caveat (P-RA1-7). The 4 disclosed restatements are genuine decidability
issues (I inspected each: K5 wrong comparison multiplier, K18a/c sign-declaration for
powsimp, K24 root ordering) — none changes a claim. Nicks: AMENDMENT A4 — the directory
name `RA1_muon_modes` reads as the PARTICLE muon; it means mu-ON — one disambiguating line
in the notes header (do not rename; paths are referenced). AMENDMENT A5 — R6's
unbounded-below hazard (c_crit ≪ −1/4 co-rotating: LC but fall-to-center, extension-
dependent) is cautioned in R5 but not restated on the R6 row — add the caution there.

## VERDICT: **AMENDED**

No falsifier fires. Five amendments owed before banking, none load-bearing on the landed
RA1-MIXED outcome: A1 (add the omitted LC line {n=2,q<0} + the q=(2−n)/2, n≥2 boundary
rays to the map — the omission was anti-ladder, honest), A2 (inline scope wording on the
two flagship excerpt-hazard lines, exact text above), A3 (state K29's thinness in §8),
A4 (mu-on vs muon disambiguation), A5 (R6 unbounded-below caution). With A1–A5 applied the
package is falsifier-clean at the Verified-LEAD ceiling (external replication bar travels).

— R2 adversarial reviewer, 2026-08-08.
