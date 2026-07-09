## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE / OBSERVE (multi-step) |
| **Frame** | promising candidates L/P; SNe as clue rank |
| **Slice** | selection principles for \(A=1-r/X\); \(F(\phi)\) chart family; composition laws |
| **Observing or targeting?** | DERIVE what selects L; OBSERVE chart family — not χ²-fit free \(F\) |
| **Build-on grade** | **LEAD** (selection for L partial; P_ell still CHOSE) |
| **Re-run** | CAS in session; SNe scores with correct full cov |

### Premise ledger

| Item | Tag |
|------|-----|
| Reciprocal metric + Einstein continuum | E-room |
| \(p_t=-\rho/2\) as selector | **named geometric condition** (not yet “why half”) |
| \(A(0)=1\), \(A(X)=0\) | wall + regular origin (ρ may diverge) |
| Additive \(\phi\) + chart \(y=XF(\phi)\) | family MAP |
| P_ell / J1 | joins CHOSE |

---

# Multi-step: selection structure for L and chart family

---

## STEP 1 — Continuum selector that unique-izes **L**

On the reciprocal metric, Einstein gives \(\rho,p_r,p_t\) from \(A(r)\).

**Condition:** \(p_t = -\frac12\rho\)  
(equivalent: \(G^\theta{}_\theta = \frac12 G^t{}_t\)).

CAS ODE:
\[
r^2 A'' + r A' - A + 1 = 0.
\]

**General solution:**
\[
A(r)=1+\frac{C_1}{r}+C_2 r.
\]

**Boundary / regularity:**

| Condition | Effect |
|-----------|--------|
| No Coulomb pole at origin (\(C_1=0\)) | \(A=1+C_2 r\) |
| Outer wall \(A(X)=0\) | \(C_2=-1/X\) |

\[
\boxed{A=1-\frac{r}{X}}
\]
**unique** under \(\{p_t=-\rho/2,\ C_1=0,\ A(X)=0\}\).

**Check:** on this profile \(\rho=1/(4\pi X r)\), \(p_r=-\rho\), \(p_t=-\rho/2\) — holds.

### Status of this selection

| Piece | Tag |
|-------|-----|
| Uniqueness under those conditions | **DERIVED** |
| Why \(p_t=-\rho/2\)? | **OPEN** — geometric simplicity / “half” ratio; not yet forced by reach |
| Why not \(C_1\neq 0\)? | regularity / finite \(A(0)\) |
| Matches SNe-near **L** | yes (same law) |

**Not** the false dust \(p_r=0\) scar. New, consistent continuum selector.

---

## STEP 2 — Power family reminder

\(A=1-c r^{p}\) \(\Rightarrow\) \(p_t/\rho=-p/2\) (constant in \(r\)).

- Constant anisotropy ratio: any fixed \(p\)  
- Ratio \(=-\frac12\): **\(p=1\)** only  

Same target **L**. “Constant half” is the power-family face of Step 1.

---

## STEP 3 — **L** is also kinematic (composition reopened)

Additive dilation depth \(\phi\) with \(A=e^{-2\phi}\) is common.

**Chart map** \(r/X=F(\phi)\), \(F(0)=0\), \(F\to 1\) as \(\phi\to\infty\):

| Name | \(F(\phi)\) | \(r/X\) | Composition on chart (from \(\phi\) additive) |
|------|------------|---------|-----------------------------------------------|
| **H** | \(\tanh\phi\) | \(\tanh\phi\) | \((x_1+x_2)/(1+x_1 x_2/X^2)\) Lorentz-like |
| **L** | \(1-e^{-2\phi}\) | \(1-A\) | \(r_1\oplus r_2=r_1+r_2-r_1 r_2/X\) |
| other | \(1-e^{-\phi}\), \(\tanh(\phi/2)\), \(\phi/(1+\phi)\), … | … | each induces its own \(\oplus\) |

**L composition** \(r_1\oplus r_2=r_1+r_2-r_1 r_2/X\):

- Associative (CAS)  
- Identity \(0\)  
- Wall \(X\) absorbing: \(r\oplus X=X\)  
- **Not** the same group as hyp fractional-linear  

So **L is not “mere continuum shopping.”**  
It is: **additive \(\phi\) + chart \(r/X=1-e^{-2\phi}\)**  
equivalently **\(r/X=1-A\)**.

H is: **additive \(\phi\) + chart \(x/X=\tanh\phi\)**.

**Unified fork:** which monotone chart \(F(\phi)\) pairs with additive depth and finite wall?

---

## STEP 4 — P_ell status (unchanged honesty)

| Join | Forced by metric? | SNe vs same hyp \(A(x)\) |
|------|-------------------|-------------------------|
| J1 \(r=x\) | **No** (CHOSE) | fail 2.17 |
| P_ell \(x=\ell\) | **No** (CHOSE explore) | better 1.02 |

P_ell remains **motivated rods**, not theorem.  
No new force found this pass — only reaffirmed join ≠ kinematics.

---

## STEP 5 — \(F(\phi)\) family vs SNe (clue, correct full cov)

\(d_L/X=e^{2\phi}F(\phi)\), \(\phi=\ln(1+z)\), 1 offset:

| Chart \(F\) | χ²/dof | Note |
|-------------|--------:|------|
| **L:** \(1-e^{-2\phi}\) | **0.910** | = linear ceiling |
| \(F=\phi/(1+\phi)\) | **0.937** | near; asymptotic wall only |
| \(F=1-e^{-\phi}\) | 1.294 | mid |
| **H:** \(\tanh\phi\) | 2.167 | fail |
| \(\tanh(\phi/2)\) | 2.724 | worse |

**Clue:** among simple \(F(\phi)\) with additive \(\phi\), **L’s chart is best**; another near miss \(\phi/(1+\phi)\); pure tanh (H) loses.

Not a free function fit — discrete named maps.

---

## STEP 6 — Zoom synthesis (where this leaves elegance)

```
additive φ  +  A = e^{-2φ}  +  finite wall
                    │
        choose chart F:  r = X F(φ)
                    │
     ┌──────────────┼──────────────┐
     │              │              │
  F=tanh φ      F=1-e^{-2φ}    F=other
     H              L           …
  Lorentz ⊕     “survival” ⊕
  SNe fail      SNe near
  c-sibling     continuum p_t=-ρ/2 unique
```

| Path | Theory job remaining |
|------|----------------------|
| **L** | Motivate \(p_t=-\rho/2\) *or* chart \(r/X=1-A\) *or* composition \(r_1+r_2-r_1 r_2/X\) as native positional law |
| **H** | Keep as \(c\)-sibling ideal; not current cosmology shape under J1 |
| **P** | Still need reason for P_ell if hyp \(A(x)\) kept |
| **Avoid** | Averaging H and L; free \(F(\phi)\) spline to χ² |

---

## One-line

**L is uniquely selected by \(p_t=-\rho/2\) + regularity + wall, and equivalently by chart \(r/X=1-e^{-2\phi}\) with its own associative composition; H is the tanh chart with Lorentz-like ⊕ — SNe prefer L’s chart; P_ell still unforced join on H’s kinematics.**
