# Exact derivation — session skeleton (2026-08-14)

Grade: unbanked. Algebra below is the session derivation, not a blind-verified package.

Areal radius is \(\rho\) here. August’s own letter \(r\) means the **depth ratio** \(e^{\Delta\phi}\). Those must not be confused.

## 1. Lapse backbone (rest, radial, no mixing)

CHOSE presentation:

\[
ds^2=-e^{-2\phi_{\mathrm{rad}}}c_E^2\,dt^2+e^{2\phi_{\mathrm{rad}}}\,d\rho^2+\rho^2 d\Omega^2.
\]

Finite max comparison plus R3-as-boost:

\[
\phi_{\mathrm{rad}}=\mathrm{artanh}\Bigl(\frac{\rho}{X}\Bigr),\qquad
e^{\phi_{\mathrm{rad}}}=\sqrt{\frac{X+\rho}{X-\rho}}.
\]

Rest observers, Killing \(t\), frequency \(\omega=-k\cdot u\):

\[
1+z=e^{\phi_{\mathrm{rad},q}-\phi_{\mathrm{rad},p}}.
\]

From the origin, \(1+z=e^{\phi_{\mathrm{rad}}}=\sqrt{(X+\rho)/(X-\rho)}\) and

\[
\frac{\rho}{X}=\frac{(1+z)^2-1}{(1+z)^2+1}.
\]

Radial pair conversion (no mixing):

\[
\frac{c_{\mathrm{eff}}}{c_E}=e^{-2\phi_{\mathrm{rad}}}=\frac{1}{(1+z)^2}.
\]

Liouville \(I_\nu/\nu^3\) conserved, \(D_A=\rho\):

\[
d_L=\rho\,(1+z)^2.
\]

This backbone is a **reduction**, not the full model.

## 2. Lean \(\mu\) (recorded, then demoted)

If the pair immersion leans into the sphere,

\[
\mu_{\mathrm{lean}}=\rho\,|\partial_t\Omega|,\qquad
\phi_{\mathrm{lean}}=\phi_{\mathrm{rad}}-\frac14\log\bigl(1-\mu_{\mathrm{lean}}^2 e^{2\phi_{\mathrm{rad}}}\bigr).
\]

Steady circling makes \(\mu_{\mathrm{lean}}\) constant (a tilt). Periodic rocking makes \(\phi_{\mathrm{lean}}\) tick. That object is **not** the August \(\mu\). It is kept only as a worldline reduction.

## 3. August \(\mu\) — the comparison arrow

Owned 2026-08-06 (`udt_mixing_channel_lane_2026-08-06/`). One live screen. Comparison \(p\to q\):

\[
A=\begin{pmatrix}
e^{-\Delta\phi}&0&\mu\\
0&e^{\Delta\phi}&0\\
0&0&s
\end{pmatrix},
\qquad
\Delta\phi=\phi_{\mathrm{rad},q}-\phi_{\mathrm{rad},p},
\qquad
s=\frac{R_q}{R_p}.
\]

This session CHOSE \(R=\rho\) (areal). Then \(s=\rho_q/\rho_p\). The origin is illegal for \(s\).

Strain \(C_A=A^\dagger A\), \(\eta=\mathrm{diag}(-1,1,1)\). Radial eigenvalue \(e^{2\Delta\phi}\). Clock–screen block:

\[
\lambda_\pm=\frac{e^{-2\Delta\phi}+s^2-\mu^2\pm\sqrt{\Delta}}{2},
\]

\[
\Delta=\bigl((e^{-\Delta\phi}-s)^2-\mu^2\bigr)\bigl((e^{-\Delta\phi}+s)^2-\mu^2\bigr).
\]

Hyperbolic (real depth) when

\[
|\mu|\le\bigl|e^{-\Delta\phi}-s\bigr|
\quad\text{or}\quad
|\mu|\ge e^{-\Delta\phi}+s.
\]

Elliptic (no real depth) between those bounds.

On the branch that returns \(e^{-2\Delta\phi}\) at \(\mu=0\),

\[
\delta_t=-\frac12\log\lambda_{\mathrm{time}}.
\]

Lock defect (scoped \(s\neq e^{\Delta\phi}\)):

\[
\lambda_{\mathrm{time}}\,e^{2\Delta\phi}=1
\quad\Leftrightarrow\quad
\mu=0.
\]

On \(s=e^{\Delta\phi}\), \(\mu\) is gauge under the same \(O(1,1+1)\) endpoint group. Nearby pairs on this \(\tanh\) chart hit that locus near \(\rho/X\approx 0.618\). Typical pairs do not.

Small mixing, \(a=e^{-\Delta\phi}\):

\[
\lambda_{\mathrm{time}}=a^2\Bigl(1-\frac{\mu^2}{a^2-s^2}\Bigr)+O(\mu^4).
\]

## 4. Cocycle

Constant \(\mu\) does not compose. Group law

\[
A(a_1,s_1,m_1)A(a_2,s_2,m_2)=A(a_1 a_2,\,s_1 s_2,\,a_1 m_2+m_1 s_2)
\]

forces

\[
\mu(p,q)=e^{-\Delta\phi}\,k(q)-s\,k(p).
\]

No \(k\) is selected. Closure does not quantize \(\mu\) and does not pin \(\phi_{\mathrm{rad}}\) (COUPLING-INERT, 2026-08-06).

If \(k=k(t)\) and each slice still obeys the coboundary, \(\delta_t\) can tick. The period is whatever \(k\) does.

## 5. Earth–sky pair (BAO viewing geometry)

UDT does not change local physics. BAO is what Earth sees.

The measurement pair is Earth \(p\) and a source \(q(\hat n)\) on our sky, not two distant galaxies comparing with each other.

Local Earth labs: \(s\approx 1\), \(e^{\Delta\phi}\approx 1\), same \(k\) \(\Rightarrow\) \(\mu\approx 0\).

Cosmological arrow:

\[
\mu(\hat n)=e^{-\Delta\phi}\,k\bigl(q(\hat n)\bigr)-s\,k_{\mathrm{Earth}}.
\]

A uniform \(k\) on a redshift shell gives a uniform heard-depth shift, not a preferred angle. A preferred angle requires direction dependence or time-live angular structure **as seen from Earth**. That is not derived. The frozen-shell case is a scoped empty, not a model no-go.

Fork, kept open: spectroscopic \(1+z=e^{\Delta\phi}\) from static \(g\) versus heard \(\delta_t(\Delta\phi,s,\mu)\). They differ when \(\mu\neq 0\).

## 6. 3 K screen (POSIT)

If the 2.725 K bath is starlight from a thermal screen at \(T_\star\),

\[
1+z=\frac{T_\star}{T_{\mathrm{CMB}}},\qquad
\frac{\rho}{X}=\frac{\alpha^2-1}{\alpha^2+1},\qquad\alpha=\frac{T_\star}{T_{\mathrm{CMB}}}.
\]

Then \(\rho_{\mathrm{CMB}}/X=1-2/(\alpha^2+1)\). Areal adjacency to the bound. \(T_\star\) is interpretation-conditional, not derived. Volume-filling stars do not automatically make a single Planck sky.

## 7. Nearby geometric slope (OBSERVED, not derived)

Pesce et al. 2020 Table 1 megamaser angular-diameter distances (Keplerian disks, not \(\Lambda\)CDM \(D(z)\)). CMB-frame optical \(z=v/c\). Exclude NGC 4258 a priori (peculiar/recession \(\sim 37\%\)). Law: \(X=\rho\bigl((1+z)^2+1\bigr)/\bigl((1+z)^2-1\bigr)\). Peculiar floor \(250\,\mathrm{km\,s^{-1}}\) as uncertainty only.

Five Hubble-flow objects give \(X\sim 4\times 10^3\,\mathrm{Mpc}\) to about ten percent. They sit at \(\rho/X\sim 0.01\)–\(0.03\) and do not test the \(\tanh\) bend. Degenerate with no \(M_B\) because these distances are geometric.

## 8. Still missing

- second \(S^2\) screen
- regular \(s\) at the origin
- which \(k\) exists
- time-live \(g\), not only time-live \(k\)
- identification of spectroscopic \(z\) with \(\delta_t\) or \(\Delta\phi\)
- a derivation of \(X\)
- a derived sky angle
