# G226 preregistration — composable null-chain conformal-symplectic assembly

Date: 2026-08-22

Question type: `METRIC_LED`.

## Frozen alternatives

- `A_PRODUCT_ONLY`
- `B_CONFORMAL_SYMPLECTIC_INTERLOCK`
- `C_GAUGE_DEPENDENT_ASSEMBLY`
- `D_NO_CAUSTIC_SAFE_ASSEMBLY`

No alternative may be added after outcome inspection.

## Frozen candidate construction

For a rank-two positive screen `S` and an oriented null vertical line `V`, use the intrinsic
first-jet phase

```text
P(V,S) = S direct_sum Hom(V,S).
```

For a vertical-line isomorphism `s:V_in -> V_out` and screen isometry
`C:S_in -> S_out`, freeze the natural vertex lift

```text
L(C,s):(x,p) -> (C x, C p s^-1).
```

In G224 clock-normalized generators, `s(N_in)=N_out`, so its matrix is
`diag(C,C)`.

For one affine edge with full G188 transfer `M_K`, endpoint frequencies
`omega_A=-g(U_A,K_A)` and `omega_B=-g(U_B,K_B)`, freeze

```text
R_i = diag(I_2, omega_i I_2)
M_e = R_B^-1 M_K R_A
r_e = omega_A/omega_B
q_e = r_e^-1.
```

The proposed exact joint law is

```text
M_e^T Omega M_e = r_e Omega
M_chain = M_BC diag(C_B,C_B) M_AB
r_chain = r_BC r_AB
M_chain^T Omega M_chain = r_chain Omega.
```

No fitted scalar, half-angle, transfer coefficient, `X_max`, profile, or direct-edge equality may
be inserted. The positive normalization `r_chain^-1/2 M_chain` may be used only as an algebraic
symplectic representative, not as a new physical law.

## Required exact checks

1. The first-order Jacobi generator for self-adjoint tide is Hamiltonian.
2. Every affine-edge fundamental transfer is symplectic and invertible.
3. Endpoint clock normalization gives conformal multiplier `r`, not `q`.
4. The G224 vertical coefficient remains `q=r^-1`.
5. The natural vertex lift is `diag(C,C)` in frequency-one generators and is symplectic.
6. The two-edge product has multiplier `r_BC r_AB`.
7. Passive endpoint and independent incoming/outgoing middle `O(2)` basis changes cancel exactly.
8. Constant positive affine-generator rescalings change only coordinate representatives and leave
   the abstract edge map invariant.
9. A singular Jacobi position block is retained while the full phase transfer stays invertible.
10. No inverse of the position block appears anywhere in composition.
11. With identity edge phases, the G225 octant triple embeds its nontrivial screen holonomy as
    `diag(H,H)` in the phase channel.
12. Great-circle G225 controls retain identity direction-space defect.
13. With nontrivial edge phases, vertex rotations and curvature phases are kept in ordered matrix
    composition and are not assumed to commute or scalarize.
14. Scalar multiplier and screen gauge covariance survive a three-edge chain.
15. An independently supplied direct relation is not constrained to equal the composite.

## Certification contract

- Production: exact SymPy algebra with named symbolic and rational controls.
- Independent replay: standard-library exact `Fraction` arithmetic on at least 20,000 seeded
  rational symplectic two-edge chains, independently generated from symmetric free/lens factors
  and rational orthogonal vertex/gauge factors.
- Hostile catches must reject at least: `q` substituted for `r`, omission of derivative rotation at
  the vertex, use of a Jacobi position-block inverse, uncancelled middle gauge, scalarized G225
  holonomy, and forced direct-equals-composite.
- Frozen source hashes and aggregate no-write package replay are required before banking.

## Falsification

Alternative B fails if the clock-normalized edge map does not have multiplier `r`, if the vertex
lift is not gauge-natural, if the two-edge multiplier does not compose, or if the full transfer
ceases to be invertible merely because its position block is singular. A flat endpoint-cocycle
claim is forbidden if the embedded G225 octant holonomy remains nonidentity.

## Maximum conclusion

At most G226 may derive a conformal-symplectic, path-labelled full screen-phase evaluator on one
supplied composable null chain and identify its multiplier with the already derived proper-clock
ratio. It may classify caustics and residual matrix holonomy. It cannot select the null protocol,
promote the G225 pointwise map to physical transport, force an independent direct relation,
populate observers or branches, select a metric history, or derive `X_max`, transfer,
observations, action, source, matter, bootstrap, mass, or signalling.
