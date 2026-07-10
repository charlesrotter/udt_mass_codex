## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE (appearance / null structure) |
| **Source** | External clean derivation (Charles-relayed); upgrades MAP |
| **Build-on grade** | **DERIVED** under WORKING reciprocal diagonal \(A(T,r)\); **LEAD** on wall-loud specialization |
| **Prior** | `simple_metric_timelive_residual_appearance_MAP.md` |
| **Scope** | Metric-led; no mechanisms, dS, free \(D_A\), BAO-fixing |

### Premise ledger

| Item | Tag |
|------|-----|
| Reciprocal diagonal time-live \(A(T,r)\), \(B=1/A\), \(T=ct\) | **WORKING** |
| Static L \(A=1-r/X\) | CANON WR-L |
| Time-live \(A_T\neq 0\) | OPEN regime |
| \(D_A=r\) in spherical areal chart | DERIVED while chart holds |
| Source/worldline model | OPEN |
| Observing or targeting? | DERIVE light-cone structure — not fit data |

**Notation:** \(A_T=\partial_T A\), \(A_r=\partial_r A\), \(H_X=X_T/X\).

---

# Exact time-live light-cone / AP equations

Metric (\(T=ct\)):

\[
ds^2=-A(T,r)\,dT^2+A(T,r)^{-1}dr^2+r^2 d\Omega^2.
\]

---

## 1. Null cone

Radial null: \(0=-A\,dT^2+A^{-1}dr^2\):

\[
\boxed{\frac{dr}{dT}=\pm A.}
\]

Incoming future-directed to the seat:

\[
\boxed{\frac{dr}{dT}=-A.}
\]

Survives static and time-live.

---

## 2. Photon energy not conserved

\[
E=-p_T=A\frac{dT}{d\lambda}.
\]

Geodesic equation ⇒ for radial null:

\[
\boxed{\frac{dE}{dT}=\frac{A_T}{A}E,}
\qquad
\boxed{
E_o=E_e\exp\left[\int_e^o \frac{A_T}{A}\,dT\right].
}
\]

Static L: \(A_T=0\) ⇒ \(E\) conserved.

---

## 3. Exact redshift

Static-seat observer: \(\omega=E/\sqrt{A}\), \(1+z=\omega_e/\omega_o\):

\[
\boxed{
1+z
=
\sqrt{\frac{A_o}{A_e}}
\exp\left[
-\int_e^o \frac{A_T}{A}\,dT
\right]
=
\sqrt{\frac{A_o}{A_e}}
\exp\left[
-\int_e^o \partial_T\ln A\,dT
\right].
}
\]

With \(A=e^{-2\phi}\):

\[
\boxed{
1+z
=
e^{\phi_e-\phi_o}
\exp\left[
2\int_e^o \phi_T\,dT
\right].
}
\]

**Central result.** Static L recovers \(1+z=\sqrt{A_o/A_e}\). Time-live ⇒ path-integrated \(z\).

---

## 4. AP / two-leg equation

Along incoming cone \(dr/dT=-A\):

\[
\boxed{
\frac{d\ln(1+z)}{dr}
=
-\frac{1}{2A}
\left(
A_r+\frac{A_T}{A}
\right).
}
\]

Transverse (while areal spherical chart holds):

\[
\boxed{D_A=r.}
\]

Log-redshift AP leg:

\[
\boxed{
R_{\mathrm{AP}}
\equiv
r\frac{d\ln(1+z)}{dr}
=
-\frac{r}{2A}
\left(
A_r+\frac{A_T}{A}
\right).
}
\]

**Static L** (\(A=1-r/X\), \(A_r=-1/X\), \(A_T=0\)):

\[
R_{\mathrm{AP}}^{L}=\frac{r}{2AX}=\frac{1-A}{2A}.
\]

With \(A=(1+z)^{-2}\):

\[
\boxed{R_{\mathrm{AP}}^{L}=z+\frac{z^2}{2}.}
\]

Recovers recorded static pure-AP relation.

**Time-live** adds exactly one new term:

\[
\boxed{
\Delta R_{\mathrm{AP}}
=
-\frac{r A_T}{2A^2}.
}
\qquad
\boxed{
R_{\mathrm{AP}}
=
R_{\mathrm{AP}}^{\mathrm{static}}
-\frac{r A_T}{2A^2}
\quad\text{(for same instantaneous }A_r\text{).}
}
\]

Static two-leg identity breaks by that pure geometric term — no matter mechanism.

---

## 5. Specialize: time-live L \(A=1-r/X(T)\)

\[
A_r=-\frac1X,\qquad
A_T=\frac{r X_T}{X^2}=(1-A)\frac{X_T}{X}=(1-A)H_X.
\]

Seat \(A_o=1\):

\[
\boxed{
1+z
=
A_e^{-1/2}
\exp\left[
-\int_e^o
\frac{(1-A)H_X}{A}\,dT
\right].
}
\]

AP log-leg:

\[
\boxed{
R_{\mathrm{AP}}
=
\frac{1-A}{2A}
-
\frac{X H_X (1-A)^2}{2A^2}.
}
\]

\(H_X=0\) ⇒ static L recovered.

\[
\boxed{\text{time-live L changes AP by a pure }X_T\text{ term, with no matter mechanism.}}
\]

---

## 6. Wall-as-sky (stronger than MAP)

Near wall \(A\to 0\), time-live L:

\[
\frac{A_T}{A}=\frac{(1-A)H_X}{A}\sim\frac{H_X}{A}.
\]

Null: \(dT\sim -dr/A\). Redshift integral:

\[
\int\frac{A_T}{A}\,dT\sim\int\frac{H_X}{A^2}\,dr.
\]

If \(H_X\neq 0\) at the wall, the wall limit is **singular / horizon-loud**.

\[
\boxed{\text{A moving WR-L wall is horizon-loud in the diagonal time-live sector.}}
\]

To avoid that (metric-led alternatives, not mechanisms):

\[
\boxed{A_T=O(A^{1+\varepsilon})\text{ near the wall}}
\quad\text{or}\quad
\boxed{X_T=0\text{ at the wall}}
\quad\text{or}
\quad
\text{reciprocal diagonal form fails (broader time-live metric).}
\]

---

## 7. Forced vs open

### Forced (WORKING \(A(T,r)\) sector)

| Claim | Status |
|-------|--------|
| \(p_T\) not conserved if \(A_T\neq 0\) | **DERIVED** |
| \(z\) path-integrated | **DERIVED** |
| \(R_{\mathrm{AP}}=-\frac{r}{2A}(A_r+A_T/A)\) | **DERIVED** |
| Static two-leg AP identity breaks | **DERIVED** |
| Moving L wall horizon-loud unless \(A_T\) vanishes fast enough near \(A=0\) | **DERIVED** (under \(A=1-r/X(T)\)) |

### Open

1. Does \(B=1/A\) survive true time-live?  
2. Is \(g_{Tr}\) forced?  
3. Source/observer congruence ⇒ definite \(dz/dT_o\) law?  
4. Angular symmetry break / scatter / caustics?  
5. Is \(X(T)\) allowed, or time-live only local/interior with fixed wall?

---

## 8. Relation to prior MAP

| MAP item | This derive |
|----------|-------------|
| Path-integrated \(1+z\) formula | **Confirmed** (exact under WORKING form) |
| AP vs drift related faces | AP equation now **explicit**; drift law still OPEN (needs congruence) |
| Scatter not forced by \(A(r,t)\) alone | Unchanged |
| Birkhoff | Still GR-form warning only; form remains WORKING |

---

## One-line

**Exact time-live appearance: \(1+z=\sqrt{A_o/A_e}\exp[-\int\partial_T\ln A\,dT]\) and \(R_{\mathrm{AP}}=-\frac{r}{2A}(A_r+A_T/A)\); time-live L adds pure \(H_X\) AP term and a moving wall is horizon-loud unless \(A_T\) dies at the wall.**
