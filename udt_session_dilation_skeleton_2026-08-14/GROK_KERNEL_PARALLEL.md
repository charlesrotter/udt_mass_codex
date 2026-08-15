# Parallel work brief — `grok2` skeleton and `grok` kernel

Date: 2026-08-15  
From: `grok2` @ this commit  
Compared against: `origin/grok` @ `fbc1c9e0`  
Grade: unbanked comparison. Not a merge. Not a verdict on either lane.

This file is for the other workstation. Please **incorporate as suggestions**, not as a
replacement of the banked evaluator.

## Verdict

**Parallel, not in contradiction.**

| lane | job | grade |
|---|---|---|
| `grok` | complete-pair **evaluator** | banked `VERIFIED-WITH-CAVEATS` |
| `grok2` | candidate **history / observational pair** | unbanked session skeleton |

Do not pick a winner. Do not smash the layers.

## What `grok` owns (do not rewrite)

Package: `udt_uncompressed_pair_kernel_reconstruction_2026-08-14/`

```text
h = Y^T B^T eta_2 B Y + (S Y + Z)^T Q^T Q (S Y + Z)
phi_pair = (1/4) log[(-det h)/h00^2]
c_eff / c_E = exp(-2 phi_pair)
```

Landing: `FULL_UNCOMPRESSED_TERMINAL_EVALUATOR_DERIVED` / `NO_SCALAR_MU_OWNED` /
`PHYSICAL_PAIR_AND_HISTORY_OPEN`.

August crosswalk: `udt_august6_mu_complete_kernel_crosswalk_2026-08-15/`

```text
M_pq = Q_q (S_q - S_p) B_p^{-1}
mu_lock = -[M_pq]_(screen, clock)
```

August \(\mu\) is one entry of a \(2\times 2\) hallway matrix on a one-screen slice. It is
not \(\phi_{\mathrm{pair}}\). The \(S/Z\) fiber can change ambient mixing and leave \(h\)
fixed. Four mixing components exist; the old scalar cannot uniquely extend.

## What `grok2` offers (candidate input, not a rival formula)

Package: `udt_session_dilation_skeleton_2026-08-14/`

1. **Lapse chart (proposed history, not selected by the evaluator)**
   \[
   \phi_{\mathrm{rad}}=\mathrm{artanh}(\rho/X).
   \]
   Rest-observer spectroscopic \(1+z=e^{\Delta\phi_{\mathrm{rad}}}\).
   \(d_L=\rho(1+z)^2\) under Liouville and \(D_A=\rho\).

2. **Observed nearby slope, not a derived \(X\)**
   Five Hubble-flow megamaser disks (Pesce et al. 2020 Table 1; Keplerian
   \(D_A\), not \(\Lambda\)CDM \(D(z)\); CMB-frame optical \(z=v/c\); NGC 4258
   excluded a priori): \(X\sim 4\times 10^3\,\mathrm{Mpc}\) to about ten percent.
   They sit at \(\rho/X\sim 0.01\)–\(0.03\) and do not test the \(\tanh\) bend.

3. **Observational pair for sky patterns**
   Earth–sky. Local physics unchanged. Two distant galaxies comparing with each
   other is not the BAO/SNe viewing geometry.

4. **Type fork, keep open**
   Spectroscopic \(1+z=e^{\Delta\phi}\) from static \(g\) versus heard
   \(\delta_t(\Delta\phi,s,\mu)\) from the comparison arrow. Do not identify
   them with \(\phi_{\mathrm{pair}}\) or with \(\mu_{\mathrm{lock}}\).

5. **Scoped empty, not a no-go**
   Uniform \(k\) on a redshift shell \(\Rightarrow\) no preferred angle.
   Direction-dependent or time-live Earth-sky structure remains open.

6. **3 K screen (POSIT)**
   If the 2.725 K bath is starlight at \(T_\star\), the screen sits against
   \(X\). \(T_\star\) is interpretation-conditional.

## How to incorporate (do this)

1. Keep the banked evaluator as the machine. Feed `grok2` objects as a
   **supplied** \((E,J)\) or as a declared one-screen slice of \(M_{pq}\).
   Do not append a scalar \(\mu\) to the terminal \(\phi_{\mathrm{pair}}\) formula.

2. If you need the August \(3\times 3\) \(A(\Delta\phi,s,\mu)\) from this
   skeleton, realize it **only** through the already-banked slice
   \(B_p=I\), \(Q_p=1\), \(S_p=0\), \(B_q=\mathrm{diag}(a,r)\), \(Q_q=s\),
   \(S_q=(-\mu/s,0)\). That is the crosswalk, not a second kernel.

3. If you write a history, treat \(\phi_{\mathrm{rad}}=\mathrm{artanh}(\rho/X)\)
   as a candidate for the reciprocal block / lapse, tagged
   `DERIVED-this-session / not selected`. The megamaser number is
   `OBSERVED` slope only.

4. For any sky-pattern query (BAO, CMB angular, SNe as seen from Earth),
   the observer is Earth. Do not use galaxy–galaxy pairs as the measurement
   pair. Local \(k\) on Earth labs stays \(\approx 0\).

5. Do not read G97 (`chi2=16255/1366` on one G79 control) as a rejection of
   this \(\tanh\) chart. That tile is a different geometry/query. Likewise do
   not read this skeleton as a rejection of G97.

6. Do not pick \(k\) or \(\omega\) to manufacture BAO. Do not import an
   acoustic length.

7. If you want a first join, the smallest lawful one is: encode the rest
   radial \(\tanh\) chart as one supplied \((B,Q,S,Y,Z)\) with \(S=0\),
   \(Z=0\), \(Q\) the areal screen, and report \(\phi_{\mathrm{pair}}\) versus
   \(\phi_{\mathrm{rad}}\). That checks whether the dashboard recovers the
   lapse when mixing is off. Only then turn mixing on as the August slice.

## What not to do

- Do not merge `grok2` into `grok` as a kernel replacement.
- Do not replace \(M_{pq}\) by our one-screen \(A\).
- Do not call lean \(\mu_{\mathrm{lean}}=\rho|\partial_t\Omega|\) the August object.
- Do not treat the megamaser \(X\) as derived from the metric.
- Do not bank a BAO detection or a BAO no-go from this brief.

## Suggested next sentence on `grok`

“The uncompressed evaluator remains the machine. `grok2` supplies one unbanked
candidate history (Earth–sky, \(\tanh\) lapse, observed nearby \(X\)) to be
encoded as a supplied pair, not as a second \(\mu\).”
