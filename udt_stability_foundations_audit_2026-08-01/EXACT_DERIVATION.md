# Exact derivation — stability foundations

This record derives type-level necessities and algebraic nonuniqueness controls. It does not derive
a new UDT equation.

## 1. Three non-equivalent questions

Let `K` be the currently admitted metric/coframe configuration set.

**Geometric persistence** asks whether a curve `gamma(s)` remains in an admissible realized set.
Without a native law selecting `gamma`, this is a kinematic path property. The existence of some
admissible curve is not a physical stability theorem.

**Energetic or spectral stability** requires more data. For an energy/action `E`, background `u`,
allowed tangent space `V_u`, boundary domain, and pairing, the tested object is the restricted
second variation

```
H_u(v,w) = d^2 E[u](v,w),       v,w in V_u.
```

Changing `E`, `V_u`, the gauge quotient, boundary data, or pairing can change the verdict. The P4
and particle results are exact instances of this conditional construction.

**Bootstrap self-consistency** requires a coupled global/local object. Write `B` for the global
background, `A(B)` for the local admissibility/equation data it selects, `u` for a local solution,
and `R(u)` for the recomputed global response. The closure schema is

```
u in Sol(A(B)),                 B = R(u).
```

This notation is type-correct but does not define `A`, `Sol`, or `R`.

## 2. Fixed-realization gate

The formal P4 modules provide scoped inclusions into a common response alphabet. They are not
themselves sets of realized configurations. Let `r_static`, `r_time`, and `r_angular` denote the
corresponding restrictions of a candidate whole configuration `u`, and let `M_alpha` denote the
registered module condition in each sector. A realized coexistence claim would require a nonempty
set

```
R = {u in U :
       r_static(u)  in M_static,
       r_time(u)    in M_time,
       r_angular(u) in M_angular,
       live_time(u) != 0,
       live_angular(u) != 0,
       E_native[u] = 0,
       B_native[u] = 0,
       u uses one compatible premise stack}.
```

Here `E_native` denotes a complete whole-system equation or equivalent response operation and
`B_native` a differentiable finite-cell boundary completion.

The two nonzero conditions apply whenever **time-live/angular-live coexistence** is claimed. They
exclude the purely static shared mode, which is an exact compatibility control but cannot witness
nonzero live coexistence. Structurally, `R` is a compatible pullback/fiber product over the same
whole configuration, equation, boundary, and premise stack—not a literal intersection of module
images.
The notation does not presume an action. The cold P4 review proves formal module recovery only and
explicitly leaves one fixed realized on-shell solution open. Therefore nonemptiness of `R` is open.

This quantifier distinction is load-bearing:

```
for every formal module member, an embedding formula exists
```

does not imply

```
there exists one physical u satisfying every module and one whole-system problem.
```

## 3. Dynamics is not contained in kinematics

Use the same scalar configuration line, the same state `q=0`, and `V=q^2/2`. Three supplied flows
give

```
q_dot = -q   => dV/dt = -q^2   (asymptotically stable),
q_dot = +q   => dV/dt = +q^2   (unstable),
q_dot =  0   => dV/dt =  0     (neutral).
```

The configuration geometry and equilibrium are identical. Only the response law differs. Thus a
formal time-dependent configuration space cannot determine physical stability without a native
flow, response law, or equivalent certificate.

## 4. A metric configuration does not fix a Hessian sign

On the same scalar configuration line and background `q=0`, take

```
E_plus  =  q^2/2,      d^2 E_plus/dq^2  = +1,
E_minus = -q^2/2,      d^2 E_minus/dq^2 = -1.
```

The opposite exact Hessians demonstrate why a supplied functional is load-bearing. This does not
say that either functional is admissible UDT physics.

## 5. A fixed-point schema does not fix the map

On the same global state line, three maps give

```
F_contract(B)=B/2:  fixed point B=0, derivative 1/2;
F_expand(B)=2B:     fixed point B=0, derivative 2;
F_shift(B)=B+1:     no fixed point.
```

Therefore writing `B=F(B)` neither proves existence nor stability. UDT needs the two physical arrows
and their domains before a bootstrap stability question is determined.

The already derived conditional quotient identity

```
rho = M/V,
delta rho = (delta M - rho delta V)/V
```

does not close the loop because a same-solution native mass `M`, boundary charge, and response map
remain open.

## 6. Minimal missing structure

The smallest honest result is a pair of joins:

1. `J_realize = (u, E_native, B_native, P_compatible)` making the formal sectors one nonempty
   realized finite-cell problem.
2. `J_persist = (response/certificate, perturbation domain, gauge/reading, pairing, boundary)`
   making persistence testable about that solution.

A complete bootstrap may couple them by deriving `A` and `R`. A complete action with its variation
domain and boundary completion may also implement them. The audit derives neither route and does not
rank them by familiarity.

“Minimal” is used only in this typed sense. `J_realize` supplies the object being tested and
`J_persist` supplies the rule or certificate under which persistence has meaning. One future native
operation may implement both, and alternative equivalent mathematical packages are not excluded.

## 7. Mechanical record

`derive_stability_foundations.py` uses exact SymPy algebra for the countermodels, validates the 94
frozen source identities, checks load-bearing source tokens, emits all TSV ledgers and
`DERIVATION_RESULT.json`, and exercises seven mutation catches. The deterministic output is preserved
in `DERIVATION_STDOUT.txt`.
