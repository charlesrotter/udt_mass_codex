# PASS — fresh adversarial review

Date: 2026-08-17
Mode: fresh read-only bounded review
Repair requests: none

The bounded maximum conclusion is justified; no physical identification is derived.

- \(J_1=\beta T u+Ln\), while \(r=J_1-\beta J_0=Ln\) and \(\xi=\rho n\). These are correctly
  kept distinct.
- For \(\epsilon=\pm1\),
  \[
  \xi=\epsilon r\iff\rho=\epsilon L,
  \quad
  T=L\frac{X_{\max}-\epsilon L}{X_{\max}+\epsilon L},
  \quad
  X_{\max}^{(\epsilon)}=\epsilon L\frac{L+T}{L-T}.
  \]
  Given \(T,L,X_{\max}>0\), both branches require \(0<L<X_{\max}\) and
  \(\epsilon(L-T)>0\). All divisions are controlled by \(L>0\), \(L+T>0\), \(L\ne T\), and
  \(X_{\max}+\epsilon L\ne0\).
- Coordinate equality is correctly a neighborhood-field statement:
  \[
  \xi=\epsilon J_1\iff \rho=\epsilon L,\quad\beta\equiv0.
  \]
  Pointwise \(\beta=0\) is insufficient for derivative/carry claims.
- With \(f=\rho/L\),
  \[
  [u,\xi]=L\,u(f)n+f\kappa u,
  \quad
  \kappa=J_1(\log T)-u(\beta T)
  =\frac{T_\sigma-T\beta_\tau-\beta T_\tau}{T}.
  \]
  Direct coordinate calculation and conversion give the same normalized coefficients, with signs
  and lapse/shift derivatives correct.
- All four counterexamples replay exactly. Equality and carry imply neither direction.
- \(X_{\max}^{(\epsilon)}\) is only a conditional candidate. Constancy across a supplied family is
  necessary, not shown sufficient; universality and numerical value remain open.

Non-blocking verifier caveat: `verify_package.py` reruns package scripts and consumes their generated
booleans, while its preregistration gate checks commit existence. Direct inspection confirmed
commit `09a45aa3` contains only `PREREGISTRATION.md` and `SOURCE_MANIFEST.tsv`; the fresh exact replay
supplies the load-bearing independent check.
