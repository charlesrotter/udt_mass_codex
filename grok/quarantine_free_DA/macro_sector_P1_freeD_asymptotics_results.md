# P1 free-\(D\), \(W=1\) vacuum — asymptotics (elegant macro test)

**Date:** 2026-07-08 · **Mode: OBSERVE.**  
**Equations:**
\[
(Z D^2\phi')'=4 e^{-2\phi}(D')^2, \qquad
(e^{-2\phi} D')'=-(Z/4)D(\phi')^2
\]
**Frame / MAP:** `UDT_ELEGANT_FRAME.md`, `macro_sector_MAP.md`  
**Script / data:** `macro_sector_P1_freeD_asymptotics.py`, `*_data.json`  
**Status:** PROVISIONAL. Completes free-\(D\) uncompensated vacuum row.

---

## Analytic structure (no new terms)

| Flux | Definition | Monotonicity |
|------|------------|--------------|
| \(G=D^2\phi'\) | φ-gradient charge | \(G'\ge 0\) (nondecreasing) |
| \(F=e^{-2\phi}D'\) | weighted expansion | \(F'\le 0\) (nonincreasing) |

- Outward **redshift** needs \(\phi'>0\) ⇒ \(G>0\) (for \(D>0\)).  
- Even \(G(0)=0\) can grow if \(D'\neq 0\) (angular sector sources φ).  
- **Hard barrier with \(\phi\to+\infty\) as \(r\to\infty\):** usually **fails** proper-distance finiteness (\(e^\phi\) grows).  
- **Hard barrier with finite \(r_*\):** possible when **\(D\to 0\)** (geometry ends) while φ has risen.

---

## Classes observed

### Class E — Expanding (\(D'>0\), \(G\ge 0\))

Typical: \(D\) grows, \(\phi\) rises then slows, run reaches large \(r_{\max}\).

| Test | Result |
|------|--------|
| Redshift out | **YES** (φ increases) |
| Hard barrier | **FAIL** — \(\ell=\int e^\phi dr\) **grows with** \(r_{\max}\) (e.g. expand \(u_0=0.1,v_0=0.5\): \(\ell(10)\sim32\), \(\ell(80)\sim506\)) |
| Preferred center | open exterior less “bag-like,” still observer chart |

**Macro elegant:** incomplete (open infinity, finite-ish depth growth not impassable).

### Class P — Pinch (\(D\to 0\) at finite \(r\))

Triggered by throat \(D'=0,\phi'>0\) or contracting \(D'<0\) with \(\phi'>0\).

| Feature | Observation |
|---------|-------------|
| \(r_{\mathrm{end}}\) | finite (e.g. throat \(u_0=0.1\): \(r\sim 9.8\)) |
| \(\phi_{\mathrm{end}}\) | clusters \(\sim 3.35\) (Z=1 samples) |
| \(\ell\) to end | **finite** (e.g. \(\sim 15.6\) for that throat) |
| null integral | finite |
| Redshift out | **YES** |

| Elegant test | Result |
|--------------|--------|
| Redshift out + finite reach | **PASS** as local chart phenomenon |
| No preferred-center **cosmos** | **FAIL** if sold as *the* universe (special place where spheres shut) |
| Same structure about every observer | **not shown** — would need relational embedding, not this IVP alone |

**This is the only pure-vacuum class on the native skeleton that jointly gives “redder outward” and “can’t go past (finite proper reach).”**  
It does **not** yet deliver the elegant **relational / no preferred center** cosmos.

### Class S — Soft (\(\phi\) decreasing, \(D\) plateau) — prior explore

Finite proper reach possible; **blueshift** out → **FAIL** look-out. Not re-run.

---

## Matter note (same action, no new operator)

Dilated continuum already in the action form adds sources to both EL equations; it **loads \(G\)** and reshapes \(F\).  
It does **not** by itself replace the vacuum exterior laws under \(W=1\): after matter, the same **E vs P** dynamics resume.  
Matter can move a seed from E→P or change \(\ell\), but **does not invent** a new asymptotic type beyond expand / pinch / soft.  
**Not** a sky fit; not a mechanism hunt — just completeness of the skeleton.

---

## Full vacuum scoreboard (updated)

| Package | Redshift out | Hard barrier | Relational cosmos | Verdict |
|---------|--------------|--------------|-------------------|---------|
| P0/P2 compensated open | no / weak | no | scale-free issues | FAIL |
| P3 \(D=r\) | yes | no (finite \(\phi_\infty\)) | singular origin | FAIL |
| P1 Class E expand | yes | no | open chart | FAIL full |
| P1 Class P pinch | yes | **yes** (finite \(\ell\)) | preferred pinch | **local pass only** |
| P1 Class S soft | no | yes | — | FAIL look-out |

**Honest bottom line:**  
Inside the **written native vacuum action**, the only barrier+redshift-out object is the **pinch end of free-\(D\) uncompensated geometry**. That is real metric content. Elevating it to “the UDT universe edge for every observer” would **smuggle a preferred center** unless a **relational multi-observer construction** is derived later — not assumed.

---

## What we will not do next

- Invent an edge term  
- Fit SNe / answer Big Bang  
- Declare pinch = CMB  

---

## Next (metric-led, ordered)

1. **PONDER (Charles):** Is the macro edge allowed to be **relational reuse of a local pinch law**, or must large-reach be **non-singular \(D>0\)** with convergent integrals? That choice is physics framing, not a new field.  
2. **If non-singular edge required:** vacuum packages **do not provide it** on this scoreboard → only remaining skeleton piece is **\(L_m\) asymptotics** / free \(D\) with matter, still characterizing, or a **gauge/relational reformulation** (not a new coupling).  
3. **If pinch-as-edge is acceptable as observer-chart phenomenon:** next is **frame-relation**: can every observer see an analogous “end” without one absolute origin? (hard; pure geometry/kinematics of charts.)

---

## Plain summary

With free sphere size and angular sourcing of dilation, looking out you either **wander forever** while depth grows then softens (no hard wall), or **hit a geometric shutoff** where sphere size pinches and proper distance ends — redder out, finite reach, but it looks like a **special bag**, not a centerless cosmos by itself.  

Vacuum UDT operators **do** contain a barrier+redshift object; they **do not** yet hand the full elegant macro without further **relational** work or **same-action** matter — still no invented mechanisms.
