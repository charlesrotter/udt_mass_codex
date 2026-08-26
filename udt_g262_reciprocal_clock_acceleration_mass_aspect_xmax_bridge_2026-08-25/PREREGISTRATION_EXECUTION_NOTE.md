# G262 preregistration execution note

Date: 2026-08-25
Status: pre-execution type repair; no algebraic outcome inspected

## R0 — clock and energy arrows

PREREGISTRATION test 7 used the phrase “under the same orientation.” That phrase is too loose.
Freeze the endpoint roles as observer `o` and source `s`:

\[
\delta_{os}=\phi_s-\phi_o,
\qquad
q_{os}=\frac{d\tau_s}{d\tau_o}=e^{-\delta_{os}},
\]

while G95 defines the transported carried-energy ratio as

\[
\epsilon_{so}=\frac{E_o}{E_s}=e^{-\delta_{os}}.
\]

Therefore `q_os=epsilon_so` numerically, but the typed arrows are opposite: the clock derivative
maps observer proper time to source proper time, whereas the energy ratio describes a carrier sent
from source to observer. Reversal and composition must preserve those types rather than using one
ambiguous `AB` label.

No candidate landing, profile control, ownership rule, or certification ceiling changes.
