# G141 preregistration — endpoint triangular transition and ordered inverse

Date: 2026-08-17

## Whole bounded question

Determine whether the signed ordered depth and its inverse are already derived, on a supplied
regular compatible endpoint-pair family, by comparing the unique positive triangular clock/ruler
coframes of the endpoint pair metrics rather than by asking one unoriented pair pullback to supply a
sign.

For each endpoint state `i`, let its complete pair metric be formed after all angular, screen, and
mixing channels have entered. On the regular calibrated stratum write uniquely

\[
h_i=R_i^T\eta_2R_i,
\qquad
R_i=\begin{pmatrix}T_i&T_i\beta_i\\0&L_i\end{pmatrix},
\qquad T_i,L_i>0.
\]

Test the relative transition

\[
C_{BA}=R_BR_A^{-1}\in B^+(2)
\]

and the positive-upper-triangular grading character

\[
\delta(C)=\frac12\log\frac{C_{11}}{C_{00}}.
\]

## Frame and premise ledger

- Method: metric-led exact finite algebra; no fit, selector, dynamics, or preferred congruence.
- `DERIVED`: complete pair pullback; unique positive triangular decomposition on the regular
  calibrated Lorentzian stratum; founded reciprocal character on supplied ordered depth; G138
  endpoint-difference algebra; G139 endpoint/transport typing; G140 terminal-sign correction.
- `CHOSE`: one rational constant complete coframe and three rational rank-two endpoint query
  differentials as a nondegenerate all-instruments control.
- `SUPPLIED/CONDITIONAL`: the three endpoint states belong to one compatible calibrated relation
  family so their triangular coframes have matching clock/ruler channel types.
- `OPEN/OMITTED`: universal physical family/query selection; singular/null strata; time-live and
  global completion; `X_max` value and proper length; observations, light/EM, action, source,
  bootstrap, matter, mass, and dynamics.

## Preregistered exact theorem tests

For arbitrary positive triangular endpoint coframes, test exactly:

1. `C_CB C_BA=C_CA`, `C_AB=C_BA^-1`, and identity at coincidence.
2. `delta(C_BA)=Phi_B-Phi_A`, where `Phi_i=(1/2)log(L_i/T_i)`.
3. `delta(C_CB C_BA)=delta(C_CB)+delta(C_BA)` and reversal changes sign.
4. The common-scale character
   `kappa(C_BA)=(1/2)log[(C_BA)00(C_BA)11]=kappa_B-kappa_A` composes separately.
5. The transition shift may be nonzero but cannot alter either diagonal character.
6. The relative pair metric `h_BA=C_BA^T eta_2 C_BA` has terminal readout
   `phi_pair(h_BA)=delta(C_BA)`. Thus the banked A-calibrated terminal formula is the metric readout
   of the relative transition, not of an unoriented affine-strip reversal.
7. `q_BA=exp(-2 delta)=q_B/q_A`, reversal is reciprocal, and the G137 bounded position obeys its
   Mobius composition law without a preferred root.
8. The pure reciprocal matrix `D(d)=diag(exp(-d),exp(d))` is retained and maps to `d`.

## Preregistered all-instruments witness

Use the fixed rational complete coframe

```text
B=[[2,1/5],[0,3/2]]
Q=[[4/3,1/7],[0,5/4]]
S=[[1/10,-1/12],[1/15,1/9]]
E=[[B,0],[Q S,Q]]
```

and three endpoint query differentials `J_i=[Y_i;Z_i]`:

```text
Y_A=[[1,0],[0,1]]                 Z_A=[[1/20,-1/25],[1/30,1/18]]
Y_B=[[1,1/20],[-1/30,1]]          Z_B=[[-1/24,1/28],[1/32,-1/21]]
Y_C=[[1,-1/25],[1/40,1]]          Z_C=[[1/27,1/31],[-1/29,1/26]]
```

Preregister that production must first verify, rather than assume, Lorentz signature of `g=E^T eta
E`, rank two of every `J_i`, regular Lorentzian `h_i=J_i^TgJ_i`, nonzero screen/mixing contribution,
and at least one nonzero relative shift. Failure of any gate invalidates the witness but not the
abstract theorem.

## Certification and falsification contract

Production uses exact SymPy algebra and frozen source hashes. An independent implementation must
reconstruct the numeric matrices and identities without importing the production functions. A
fresh adversary must attack multiplication order, triangular decomposition, endpoint calibration,
the full-`GL` commutator objection, and any promotion from a supplied compatible family to a
universal family selector.

Falsify or narrow the proposed join if the transition fails exact composition/inversion, its
grading differs from endpoint potential difference, the relative terminal formula disagrees, or
the all-instruments witness is nonregular.

Maximum possible conclusion:

```text
REGULAR_ENDPOINT_PAIR_METRICS_DERIVE_POSITIVE_TRIANGULAR_COFRAMES__
RELATIVE_TRANSITIONS_COMPOSE_AND_REVERSE_EXACTLY__
RECIPROCAL_GRADING_EQUALS_ENDPOINT_PHI_DIFFERENCE_AND_RELATIVE_TERMINAL_READOUT__
ORDER_SUPPLIES_SIGN_WITHOUT_A_PREFERRED_ROOT__
COMPLETE_ORCHESTRA_REMAINS_UPSTREAM__
PHYSICAL_COMPATIBLE_FAMILY_HISTORY_XMAX_AND_GLOBAL_COMPLETION_OPEN
```
