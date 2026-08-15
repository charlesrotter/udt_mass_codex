# Preregistration — uncompressed complete-pair evaluator reconstruction

Date: 2026-08-14  
Mode: `MAP -> OBSERVE -> PONDER -> DERIVE`; metric-led after a pair realization is supplied  
Outcome at registration: **NOT YET EVALUATED**

## 1. Why this reset is required

The currently registered reciprocal/orchestra package begins from the exact reduction

```text
h = B^T eta_2 B + P,
P = C^T q C,
C = S + Z Y^-1,
q = Q^T Q,
```

on an A-calibrated, invertible-`Y` stratum. That reduction is valid for the pair metric, but it
compresses three logically different ingredients before the time-live calculation starts:

1. the complete-coframe screen geometry `Q`;
2. the complete-coframe base-to-screen mixing `S`; and
3. the supplied pair immersion through `Y` and `Z`.

It then studies a chosen trace of `B^-T P B^-1`, and its quiet-middle statement holds `P`, common
scale, and shift fixed. That is a conditional response diagnostic, not a derivation of the complete
observer-pair relation or its regime evolution.

This package therefore restarts one level earlier. It must carry the uncompressed objects to the
terminal reciprocal-`c_E` readout before any quotient or scalar summary is introduced.

## 2. Whole question

Given:

- a supplied smooth Lorentzian four-metric represented locally by the complete coframe
  `E=[[B,0],[Q S,Q]]`;
- a supplied smooth rank-two ordered pair realization with Jacobian `J=[Y;Z]`;
- the observed calibration `c_E` in the A-observer clock/ruler coordinates;

what does the metric derive, exactly and without compression, for

```text
(B,Q,S,Y,Z) -> h=J^T E^T eta_4 E J
             -> (T_pair,L_pair,beta_pair,phi_pair)
             -> c_eff^(pair)/c_E ?
```

The same question is asked for a generic first variation and for a generic live parameter
`lambda`, retaining `dB`, `dQ`, `dS`, `dY`, and `dZ` separately.

The audit must then determine:

1. exactly what information is lost by the reductions `q=Q^TQ`, `C=S+ZY^-1`, and `P=C^TqC`;
2. whether a scalar called `mu` is actually derived and uniquely typed by this complete-pair map;
3. which parts are metric evaluation and which still require a supplied pair realization or a
   supplied history.

## 3. Bounded regime and complete degrees of freedom

Primary derivation:

- arbitrary real invertible `B in GL(2,R)` on the declared time-oriented base chart;
- arbitrary real invertible `Q in GL(2,R)` representing a positive screen metric;
- arbitrary real `S in Mat(2,R)` — all four mixing components live;
- arbitrary real `Y,Z in Mat(2,R)` such that `J=[Y;Z]` has rank two;
- arbitrary independent first variations/time derivatives of all five matrices;
- terminal readout only on the regular calibrated Lorentzian pair stratum
  `h00<0`, `det(h)<0`;
- no invertibility assumption on `Y` in the primary formula.

Secondary quotient analysis:

- `Y` invertible only where the A-calibrated reduction is explicitly invoked;
- screen-frame `O(2)` gauge, pair-coordinate `GL(2)` covariance, and all algebraic fibers of the
  reductions are retained and classified;
- chart boundaries `rank(J)<2`, `det(Y)=0`, `h00=0`, `det(h)=0`, and degenerate screen/base blocks
  are recorded rather than silently discarded.

No physical values, profile, boundary condition, source, carrier, action, bootstrap law, SNe/CMB/BAO
data, `X_max`, GR equation, Lambda-CDM interpretation, or numerical fit enters.

## 4. Required exact derivation

Define

```text
eta_4 = diag(eta_2,I_2),       eta_2=diag(-1,+1),
E     = [[B,0],[Q S,Q]],       J=[Y;Z],
U     = B Y,                   R=S Y+Z,
A     = Q R,                   V=EJ=[U;A].
```

The production derivation must establish or falsify:

1. **Uncompressed pullback**

   ```text
   h = V^T eta_4 V = U^T eta_2 U + A^T A
     = Y^T B^T eta_2 B Y + (S Y+Z)^T Q^T Q (S Y+Z).
   ```

2. **Exact first variation**

   ```text
   delta U = delta B Y + B delta Y,
   delta R = delta S Y + S delta Y + delta Z,
   delta A = delta Q R + Q delta R,
   delta h = 2 sym(U^T eta_2 delta U + A^T delta A),
   ```

   with `sym(M)=(M+M^T)/2`. Every independent variation must be shown explicitly.

3. **Exact time-live evaluator** — the same equations with `delta -> d/dlambda`; no equation of
   motion may be inferred from this chain rule.

4. **Terminal readout** on `h00<0`, `det(h)<0`

   ```text
   T_pair^2    = -h00,
   beta_pair   = h01/h00,
   L_pair^2    = h11-h01^2/h00,
   phi_pair    = (1/4) log[(-det h)/h00^2]
               = (1/2) log(L_pair/T_pair),
   c_eff/c_E   = T_pair/L_pair = exp(-2 phi_pair).
   ```

5. **Exact live terminal derivative**

   ```text
   dot phi_pair
     = (1/4) tr(h^-1 dot h) - (1/2) dot h00/h00,
   d(c_eff/c_E)/dlambda
     = -2 dot phi_pair (c_eff/c_E).
   ```

6. **Sensitivity census** — construct exact regular witnesses showing whether each of
   `B,Q,S,Y,Z` can independently change `phi_pair` while the other four are held fixed. A zero
   derivative at one symmetric point does not prove a channel is absent; both generic and
   symmetry-protected points must be tested.

7. **Compression/fiber theorem** on invertible `Y`

   ```text
   W=Z Y^-1,  C=S+W,  q=Q^TQ,  P=C^TqC,
   Y^-T h Y^-1 = B^T eta_2 B + P.
   ```

   The audit must exhibit exact distinct inputs with identical `P` for at least:

   - `S -> S+D`, `W -> W-D`;
   - screen left-frame rotations `Q -> OQ`;
   - distinct `C` representatives with identical `C^TqC` where allowed;
   - identical zero-order `P` but different uncompressed first derivatives.

8. **`mu` type audit**

   - modern complete-coframe mixing is the four-component matrix `S`;
   - the July conditional object `mu_old=B_old^2/(A_old^2 b_old^2)` belongs to a different
     mixed-base ansatz and is not to be identified with `S`, `C`, `P`, an eigenvalue, determinant,
     or trace without an exact derivation;
   - if no scalar invariant is uniquely selected by the complete-pair evaluator, the result must say
     `NO_SCALAR_MU_OWNED` rather than choosing one.

## 5. Premise classification

- `c_E`: `OBSERVED`; calibration of pair clock/ruler coordinates.
- reciprocal exponential character on a supplied depth: `DERIVED`.
- complete coframe chart: `CONDITIONAL`; a regular local chart on the complete metric arena.
- complete metric history `B(lambda),Q(lambda),S(lambda)`: `SUPPLIED/CONDITIONAL`.
- pair realization `Y(lambda),Z(lambda)`: `SUPPLIED/CONDITIONAL`.
- pullback, terminal decomposition, and their variations: candidates for `DERIVED` conditional
  evaluation identities.
- physical pair assignment, history, regime score, scalar `mu`, action, source, carrier, bootstrap,
  and global completion: `OPEN` or inactive.

## 6. Falsification and certification contract

The primary algebra is falsified if:

- direct `J^T E^T eta_4 E J` disagrees with the uncompressed formula;
- the direct variation disagrees with the registered variation formula;
- finite-difference live checks disagree after tolerance is tightened through a preregistered step
  sequence;
- terminal reconstruction fails on any regular witness;
- a claimed active channel cannot change the terminal output on any regular generic witness;
- a claimed compression fiber does not preserve the stated compressed object;
- the analysis identifies the old scalar `mu` with modern mixing without a type-correct map;
- any result claims that the chain rule supplies physical evolution or that the metric alone selects
  `Y,Z`.

Certification requires:

1. exact symbolic production checks;
2. an independent component/Fraction or high-precision implementation not importing production
   functions;
3. hostile catch proofs mutating one sign or omitting each of `dQ`, `dS`, `dY`, and `dZ`;
4. a complete premise audit;
5. a fresh read-only adversarial review before a load-bearing verdict is promoted.

## 7. Preregistered primary landings

Return exactly one:

1. `FULL_UNCOMPRESSED_TERMINAL_EVALUATOR_DERIVED__NO_SCALAR_MU_OWNED__PHYSICAL_PAIR_AND_HISTORY_OPEN`
2. `FULL_UNCOMPRESSED_TERMINAL_EVALUATOR_DERIVED__CURRENT_MU_EMBEDS_AS_A_UNIQUE_DERIVED_INVARIANT`
3. `CHANNEL_RESOLUTION_REQUIRES_EXTRA_SPLIT_OR_QUERY_DATA`
4. `ALGEBRA_OR_TYPE_FAILURE`

Landing 1 is a successful reconstruction, not a negative failure: it means the complete metric and
the supplied pair realization produce one exact reciprocal-`c_E` readout with every orchestra
channel retained, while neither a scalar mixing knob nor a physical trajectory has been invented.

## 8. Maximum allowed conclusion

At most:

> For a supplied regular complete metric and supplied regular ordered pair realization, the complete
> coframe determines an exact, uncompressed pair metric and terminal `phi_pair`/`c_eff` readout. Its
> exact variation retains reciprocal/base, screen, four-component mixing, embedding, shift, and
> query motion separately. Any Gram compression is an output quotient with explicitly classified
> fibers. This is a conditional evaluator; it does not construct the physical pair realization,
> select a metric history, derive a regime score, or justify a scalar `mu` unless a separate exact
> uniqueness proof succeeds.

