# Derivation notes — the c_eff reciprocal (does it un-blind A*B?)

Mode: OBSERVE. Exact sympy 1.13.1, CPU, float-free. Status: UNBANKED. Extends PREREG_ADDENDUM_ceff_reciprocal.md.
Scripts (uncommitted): `ceff_reciprocal.py`, `f234.py`, `ricci.py`. F-STEER guard: driver WANTS un-blind; algebra decides.

## FACTS (exact, general A(r),B(r))  [metric ds^2=-A c^2 dt^2 + B dr^2 + r^2 dOmega^2]
- `sqrt(-g) = c * sqrt(A*B) * r^2 * |sin theta|`  -> EH volume is depth-blind IFF `A*B = const`.
- coordinate light speed `c_eff^2 = -g_tt/g_xx = c^2 * A/B`.
- **LOAD-BEARING STRUCTURAL FACT:** `c_eff` depends ONLY on the RATIO `A/B`. The volume-blindness is
  governed by the PRODUCT `A*B`. Ratio and product are INDEPENDENT (orthogonal) combinations of A,B.
  => "reciprocity via c_eff" fixes A/B; it NEVER by itself determines A*B. A*B is a FREE residual.
  This single fact drives the whole verdict.

## A*B for each formalization (EXACT)
| # | reading | constraint imposed | A*B | c_eff-consistent? | blind? |
|---|---------|--------------------|-----|-------------------|--------|
| 1 | clock x ruler = 1 (sqrt(A)sqrt(B)=1) | AB=1 | **1 CONST** | yes | **BLIND** (= frozen control) |
| 2 | proper light speed dl/dtau = c_eff | A/B=1 => A=B | A^2 (function) | c_eff=c CONST (degenerate) | c_eff-var KILLED |
| 3 | g_tt*g_xx = -c_eff^2 literal | B=1 forced | A (function) | yes (single-slot) | **UN-BLIND (degenerate ruler)** |
| 4a| A=u, B=1/u (reciprocal split) | AB=1 | **1 CONST** | yes (A/B=u^2) | **BLIND** |
| 4b| A=u^2, B=1/u^2 | AB=1 | 1 CONST | NO (A/B=u^4) | reject (inconsistent) |
| 4c| A=u^2, B=1 (clock carries all depth) | — | **u^2 (function)** | yes | **UN-BLIND** |
| 4d| A=1, B=1/u^2 (ruler carries all depth) | — | **u^-2 (function)** | yes | **UN-BLIND** |

(u := c_eff/c, the depth field.)

## READING OF THE TABLE
- Every reading that keeps genuine RECIPROCITY — depth split reciprocally between clock and ruler
  (F1, F4a) — gives **A*B = 1 (BLIND)**. Same as the frozen constant-c lock; the constant being c_eff
  vs c_E is irrelevant, exactly as the addendum anticipated.
- Every UN-BLIND reading (F3, F4c, F4d) puts the depth in ONE slot only (clock OR ruler). That is a
  SINGLE-SLOT, NON-reciprocal reading — it ABANDONS reciprocity. It is not "the c_eff reciprocal";
  it is "the c_eff single-slot."
- F2 (proper light speed = c_eff): the proper-measured radial light speed is invariantly c (=1) for
  ANY A,B; imposing it equal c_eff forces A=B => c_eff=c constant. Un-blinds volume ONLY by
  trivializing c_eff. Not a genuine c_eff-reciprocal.

## PART B — single-field EH variation on the UN-BLIND readings (does un-blinding rescue a phi-law?)
Metric built from ONE field u(r); S = int R sqrt(-g); exact single-field Euler-Lagrange
E[u] = dL/du - d/dr(dL/du') + d^2/dr^2(dL/du''), L = R * r^2 * sqrt(AB). [ricci.py, EXACT]

- **4c (A=u^2, B=1), AB=u^2 un-blind:** L = -2r^2 u'' - 4r u' = d/dr(-2r^2 u') — a TOTAL DERIVATIVE.
    E[u] == 0 IDENTICALLY (for every u).  => **VACUOUS — a NULL LAGRANGIAN AGAIN**, despite AB non-blind.
    Admits the profile u=1-r/X trivially (admits ALL). Effective source G^t_t == 0 identically
    (B=1 => G^t_t=0 for all A); anisotropic pressure only. Un-blinding the VOLUME did NOT rescue it.

- **4d (A=1, B=1/u^2), AB=u^-2 un-blind:** E[u] = 2(u^2 - 1)/u^2 — NONVACUOUS but PURELY ALGEBRAIC
    (no surviving derivatives). E=0 <=> **u = 1** (c_eff = c_E, FLAT). Does **NOT admit** the profile:
    E[u=1-r/X] = 2r(2X - r)/((r-X)|X-r|) != 0. Effective source on the (forbidden) profile:
    G^t_t = 3/X^2 - 4/(X r) != 0 — intrinsic nonzero stress, but NOT selected (the law forces u=1).

- control (A=u^2, B=u, non-reciprocal, AB=u^3): E = 3(u-1)/sqrt(u) — nonvacuous, again forces u=1.

### PART-B READING
In EVERY un-blind formalization the single-field EH variation FAILS to deliver a phi-law that admits
the varying-c_eff profile c_eff=c_E(1-r/X): it is either VACUOUS (4c: null Lagrangian, admits all /
selects nothing) or NONVACUOUS-BUT-FLAT-FORCING (4d, control: an algebraic law whose only root is
u=1, i.e. c_eff=const). The profile c_eff=c_E(1-r/X) is FORBIDDEN or UNSELECTED in all cases.

## FALSIFIER CHECK
- F-STEER: driver wanted UN-BLIND. Honest algebra: the genuine c_eff-RECIPROCAL (F1/F4a) is BLIND;
  un-blind only via NON-reciprocal single-slot (F3/4c/4d), and even those give no profile-admitting
  law. Refused the steer.
- F-IMPORT: EH used reference-only; g[u] native metric-from-one-field. c set=reference scale only.
- F-SCOPE: static / radial / EH-reference. Held; no native action, no physics, no mass claimed.

## VERDICT (scoped, UNBANKED): STILL-BLIND (with a MIXED tail)
The c_eff reciprocity, formalized AS reciprocity (depth split reciprocally over clock and ruler),
gives A*B = const => volume BLIND — identical to the frozen constant-c lock. UN-BLIND A*B=function is
reachable ONLY by abandoning reciprocity (single-slot depth, F3/4c/4d); and even there the single-field
EH variation never yields a law admitting c_eff=c_E(1-r/X) (4c vacuous null-Lagrangian; 4d/control
force c_eff=const). So no honest c_eff-reciprocal formalization un-blinds into a live phi-law.

**Single load-bearing step:** `c_eff^2 = c^2 * A/B` depends ONLY on the ratio A/B, while volume-
blindness is governed by the INDEPENDENT product A*B; genuine reciprocity pins A*B=1 (blind), so
c_eff-reciprocity leaves the EH volume blind — the free residual A*B, not c_eff, is the un-blinding
knob, and no reciprocal reading touches it.

Nothing banks; re-derivation + exact table; four-check N/A (OBSERVE lead). Fork for Charles.
