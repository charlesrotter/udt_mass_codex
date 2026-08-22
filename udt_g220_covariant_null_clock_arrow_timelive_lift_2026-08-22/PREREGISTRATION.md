# G220 preregistration — covariant dynamic null clock arrow

Date: 2026-08-22
Status: `PREREGISTERED_NOT_RUN`

## Required derivations

1. For `F(tau_A,tau_B)=sigma(z_A(tau_A),z_B(tau_B))=0`, derive

   ```text
   r_AB=d tau_B/d tau_A
       =-(sigma_a U_A^a)/(sigma_a' U_B^a')
       =(k_A.U_A)/(k_B.U_B)
       =omega_A/omega_B > 0
   delta_AB=-log r_AB.
   ```

   Affine rescaling of `k` must cancel. The denominator must be nonzero.

2. On

   ```text
   h=-N(t)^2(dt+beta(t) dx)^2+A(t)^2 dx^2,
   C_+(t)=A(t)-N(t) beta(t)>0,
   ```

   for fixed-`x` observers separated by coordinate `L>0`, derive

   ```text
   L=integral[t_A,t_B] N(t)/C_+(t) dt,
   d t_B/d t_A=N_A C_+B/(C_+A N_B),
   r_AB=C_+B/C_+A,
   delta_AB=log(C_+A/C_+B).
   ```

3. Pull the target observer clock back using source proper time `y=tau_A`. The completed target clock
   coefficient must be exactly `T_B=d tau_B/dy=r_AB` after source normalization, so the completed
   reciprocal readout equals the null-incidence result.

4. Recover exactly:

   - G219 moving flat: `r_AB=exp(eta)`;
   - primary static reciprocal metric: `r_AB=exp(phi_A-phi_B)` and
     `delta_AB=phi_B-phi_A`;
   - conformal time-live control `N=A=exp(Omega(t)), beta=0`:
     `r_AB=exp(Omega_B-Omega_A)`;
   - affine ruler/shift control `N=1`, `A=a0+a1 t`, `beta=s t`:
     `C_+=a0+(a1-s)t` and the exact incidence map has slope
     `exp((a1-s)L)` on every registered positive branch.

5. Distinguish mathematical inverse from a later left-moving return. The latter depends on
   `C_-=A+N beta` at its own later endpoint events and is not generically the inverse arrow.

## Mutually exclusive primary landings

```text
COVARIANT_NULL_CLOCK_ARROW_DERIVED__TIMELIVE_PAIR_PULLBACK_MATCHES__NULL_REMAINS_QUERY_TYPED
COVARIANT_ARROW_DERIVED__COMPLETED_PULLBACK_REQUIRES_REPAIR
TIMELIVE_CONTROL_BREAKS_G219_FACTORIZATION
NULL_CLOCK_ARROW_LIFT_REFUTED
```

## Falsifiers

- disagreement between world-function and affine-frequency derivations;
- dependence on affine normalization of `k`;
- failure of any mandatory control recovery;
- a target completed clock coefficient different from the proper-clock incidence derivative;
- a purported time-live formula that freezes every varying channel;
- identifying later causal return with inverse;
- selecting null as universal physical protocol from this conditional calculation.

## Certification contract

- exact frozen source hashes;
- exact symbolic production derivation;
- independent standard-library rational replay for local endpoint and pullback identities;
- explicit mutation catches including sign, endpoint order, affine scaling, lapse cancellation,
  completed-clock mismatch, and return/inverse confusion;
- current premise verifier and full repository tests as producer-local evidence;
- fresh zero-context adversarial review before banking.

## Maximum conclusion

At most G220 may derive the null-incidence clock arrow on one supplied regular branch, prove its exact
completed-pullback match, and exhibit a genuine time-live base-metric control. It may not select null
as the UDT positional protocol, derive a physical history, close angular/screen/mixing propagation,
or infer transfer, observation, `X_max`, action, source, matter, bootstrap, mass, or signalling.
