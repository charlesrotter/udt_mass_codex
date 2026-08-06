# Adversarial Review B — OE-MOTION / c_eff / GR-equivalence

Reviewer: blind adversarial agent, 2026-08-05, branch grok. Independent symbolic
recompute from scratch (sympy 1.13.1); imported NO derivation code. Script:
scratchpad/reviewB.py. Target: DERIVATION_NOTES.md claims (i) c_eff-coordinate and
(ii) OE-MOTION (lock content in g_xx/(-g_tt), located in motion, departure NOT claimed).

## Independent recomputation (all confirmed)

- **Coordinate energy** E² = c²e^{-4φ}(P² + c²m²e^{2φ}) — matches note 1.
- **SR-local reduction** E_loc² − [(mc²)² + (p̂c)²] = 0 identically, with E_loc=E/√(−g_tt/c²),
  p̂=P/√g_xx. B=g_xx and φ drop out. Note 2 (OE-SR-LOCAL) is a correct exact identity.
- **c_eff**: radial null gives dx/dt = √(−g_tt/g_xx) = c·e^{-2φ}. Matches note 3.

## 1. Does g_xx/(−g_tt) enter an observable, or is it gauge?

Two-sided answer:
- **In ≥2+1 D with an areal radius** (deflection/Shapiro/orbits — the sector the notes
  invoke): YES, g_xx enters independently. For ds²=−A c²dt²+B dr²+r²dΩ², the radial photon
  coordinate speed is c√(A/B) and the Shapiro integrand is (1/c)√(B/A) dr; the light-bending
  refractive index is n=√(B/A). With B=1 the deflection is HALF (the missing Einstein factor
  of 2 lives in g_rr=B). So g_xx is genuinely observable there. The notes' LOCATION claim —
  "content sits in g_xx/(−g_tt), the motion sector" — is FAIR.
- **In the actual 1+1 metric the notes compute**: g_xx is PURE GAUGE. Setting X=∫√g_xx dx
  gives g_XX≡1; the ratio g_xx/(−g_tt) is not invariant under x→x'(x). There is NO areal
  radius in a 1+1 metric to pin x. So the OE-MOTION content does not exist in the object
  actually solved — it requires the angular/areal structure of a higher-D metric that was
  not part of this derivation. **The location claim borrows structure it did not compute.**
  The notes label it "LOCATION only," a LEAD, and NOT a departure — so this is honest
  under-claiming, but the reader should know the motion content is a POINTER, not a result
  of the 1+1 exercise. → NARROW.

## 2. GR-equivalence kill

**Schwarzschild in standard areal coordinates satisfies the reciprocal lock exactly.**
A=1−r_s/r, B=1/(1−r_s/r) ⟹ A·B=1 ⟹ g_tt·g_rr = −A B c² = −c². The lock g_tt g_xx=−c²
IS the well-known Schwarzschild property −g_tt g_rr=c², holding for the whole
−f dt²+f^{-1}dr²+r²dΩ² family (Schwarzschild, RN, Sch–dS). So:
- The lock is **coordinate-achievable in GR — indeed it is GR vacuum's natural chart.**
  "Located in motion, UNLIKE GR" would be EMPTY as a vacuum statement: GR vacuum already
  sits on the lock. The PREREGISTRATION's banked-footing line calling g_tt g_xx=−c² "the
  UDT departure from GR, where g_tt,g_xx are independent" is **WRONG/overstated** — g_tt and
  g_xx are NOT independent in GR vacuum; A·B=1 is forced there.
- With generic matter, GR gives A·B=1 ⟺ G^t_t=G^r_r ⟺ ρ=−p_r; generic matter breaks it.
  So UDT imposing the lock everywhere differs from GR-with-generic-matter but agrees with
  GR vacuum / ρ=−p_r sources. Whether that is a real departure is **conditional on the
  matter sector — exactly what DERIVATION_NOTES note 4 calls unchecked/OPEN.** The notes'
  refusal to claim a departure is CORRECT and vindicated; the PREREGISTRATION §1 assertion
  of departure is the overreach, and it is not carried into the notes' verdict.

## 3. Audit of (i) c_eff

c_eff=e^{-2φ}c is a radial-null coordinate speed (confirmed). Grep of the probe dir shows
it is flagged F-COORD / "NOT asserted physical" at every occurrence; it is never used as an
input to any invariant or elevated to a measurable. **c_eff discipline HELD; no smuggling.**

## 4. Is "content is in motion" established or just relocation?

It is **relocation of an as-yet-unproven claim**, honestly labeled. The 1+1 derivation
proves only the null (OE-SR-LOCAL). The motion content is asserted by pointing at the
g_xx/(−g_tt) combination that WOULD enter deflection/Shapiro in a higher-D metric not
solved here, and is explicitly NOT claimed to be a GR departure. As a LEAD/pointer that is
legitimate; as an established finding it is not, and the notes do not claim it is.

## Verdict: NARROW (pass on discipline; two corrections owed)

- OE-SR-LOCAL identity: solid, reproduced.
- c_eff-coordinate discipline: HELD.
- OE-MOTION: fair as a LOCATION pointer, but (a) the g_xx content is gauge in the actual
  1+1 metric and imports higher-D structure, and (b) the lock is NOT a GR departure in
  vacuum — Schwarzschild's areal chart satisfies it identically. The DERIVATION_NOTES were
  disciplined (departure NOT claimed, OPEN). The **PREREGISTRATION §1 statement that
  g_tt g_xx=−c² is "the UDT departure from GR, where g_tt,g_xx are independent" is refuted**
  and should be corrected: g_tt,g_xx are locked in GR vacuum too. No physics departure is
  established; none is claimed in the notes.
