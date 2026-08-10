# Exact derivation — non-isometric calibration-magnitude ownership

Date: 2026-08-10

Current grade: **VERIFIED-WITH-CAVEATS; CORRECTED EXTERNAL REVIEW ACCEPTED**

Primary preregistered landing:

```text
BRANCH_CONDITIONAL_MAGNITUDE_OWNER_ONLY__NO_UNIVERSAL_OWNER
```

## 1. Result first

The frozen 24-identity by five-family census has no `OWNER_DERIVED` row for a complete physical
reciprocal comparison. It does contain exactly two branch-conditional owners of a narrower object:

- R17/W01 owns the endpoint Killing-norm magnitude `delta_K` and separately owns an intrinsic
  reciprocal grading, but does not select the non-isometric lift that joins them as the physical
  comparison law;
- R18/W02 owns the unique-Killing endpoint clock magnitude `delta_K`, but has no intrinsic ruler
  scale and therefore cannot determine the complete terminal reciprocal imbalance.

All metric-owned path transports are isometric or projector-only. A supplied pair-surface Jacobian
can generate a nonzero complete magnitude, but no current branch owns the physical query/surface.
No current native dynamical or bootstrap return supplies the missing completion.

The result therefore separates **magnitude existence** from **reciprocal completion and physical
application**. It does not derive the physical law.

## 2. Ownership type

An endpoint clock calibration magnitude is generated when a branch itself supplies one common
unnormalized timelike state `K` whose norm can vary. Write

```text
N(p)=sqrt[-g(K,K)]_p,
chi_K(p,q)=N(p)/N(q),
delta_K(p,q)=log chi_K(p,q).
```

For three endpoints,

```text
chi_K(p,q) chi_K(q,r)=chi_K(p,r),
delta_K(p,q)+delta_K(q,r)=delta_K(p,r).
```

A constant rescaling `K -> aK` cancels from `chi_K`, so this is not normalization by presentation.
It is a genuine endpoint magnitude on branches where the metric owns the unique line/state.

This remains weaker than ownership of the complete physical reciprocal magnitude. That stronger
object must also own a ruler/grading, the non-isometric action of `delta_K`, the pair relation or
surface, intermediate carry, and terminal compatibility.

## 3. R17 — owned magnitude, unselected reciprocal lift

Frozen R17 evidence supplies:

```text
N=c_E exp(-phi),
delta_K(p,q)=log[N(p)/N(q)],
X_lambda=-P_u+P_n+lambda H,
U_gamma = Levi-Civita path transport.
```

The conditional assembly

```text
A_gamma=U_gamma exp[delta_K X_lambda]
```

is exact on matched path-carried states. Its reciprocal density equals `delta_K`, and the full
isometric factor preserves angular mixing and holonomy. However, external review of G42 already
established that the branch owns the ingredients separately but does not select their semidirect
assembly as the physical comparison law.

The exact witness makes the distinction sharp. On a normalized clock/ruler flag,

```text
U only:                  (rho_1,rho_2,Q)=(1,1,1),
D(log 2):                (rho_1,rho_2,Q)=(1/4,1,16),
U D(log 2):              (rho_1,rho_2,Q)=(1/4,1,16).
```

The metric-owned `U` transports but generates no magnitude. The branch-owned `delta_K` supplies a
magnitude. Choosing to exponentiate it through `X_lambda` is the remaining selector. R17 is thus
`OWNER_CONDITIONAL_BRANCH_ONLY`, never a complete physical owner.

Its additional open joints are the carried-to-intrinsic endpoint reset, physical path/query, and
global pair-surface realization.

## 4. R18 — owned clock magnitude, missing ruler completion

R18 owns one global nonvanishing unique timelike Killing calibration state. Its endpoint ratio is
exact, non-isometric when the lapse varies, and compositional. The branch has no same-branch
intrinsic ruler scale.

The missing information is not cosmetic. Fix the same clock density `T=1/2` and compare

```text
h_1=diag(-1/4,4),
h_2=diag(-1/4,1).
```

Both have the same clock factor, but the terminal determinant arguments are

```text
[-det(h_1)]/h_00^2=16,
[-det(h_2)]/h_00^2=4.
```

Therefore

```text
phi_pair(h_1)=log 2,
phi_pair(h_2)=(1/2)log 2.
```

One owned clock magnitude does not determine the reciprocal clock/ruler imbalance. R18 is also
`OWNER_CONDITIONAL_BRANCH_ONLY`, with an intrinsic ruler or equivalent reciprocal-area condition
still missing.

## 5. Pair-surface Jacobian family

A lawful supplied pair Jacobian can generate a complete non-isometric magnitude. The retained mixed
witness gives

```text
(rho_1,rho_2,Q)=(3/16,3/4,64/3),
delta_RF=(1/4)log(64/3).
```

This is a structural existence witness. The pair-map atlas proves that the metric fills in a local
orthogonal exponential tube only after a full query supplies worldline, event pairing, ruler
direction/evolution, and a regular branch. Pair surfaces also lack a canonical middle composition
unless calibration state is carried.

Consequently every typed branch row in this family is
`BLOCKED_MISSING_PHYSICAL_QUERY`, not `OWNER_DERIVED`.

## 6. Path and global-completion family

R17, R19, and R23 own metric-compatible path transport; R24 owns set-equivariant projector
transport. These objects retain genuine path labels, mixing, and holonomy and compose in their
proper types. They do not change clock/ruler density:

```text
P_gamma^T g_q P_gamma=g_p
  => (rho_1,rho_2,Q)=(1,1,1).
```

R18's global completion supplies the endpoint clock state already classified in the preceding
family, not an additional path-generated reciprocal magnitude. Thus the five surviving typed
path/global rows are `TRANSPORT_OR_READOUT_ONLY`.

Conditional geodesic, Jacobi, seam, lift, and presentation families do not improve this ruling:
they either require an unowned query/state or fail the required compositional type. Nonidentity
holonomy is retained and never collapsed into endpoint exactness.

## 7. Native dynamics/bootstrap family

No frozen current premise supplies a native action, response law, bootstrap return, or calibration
state that generates the missing magnitude. All 24 cells are therefore
`BLOCKED_MISSING_DYNAMIC_LAW`.

This is not evidence against bootstrap. It records that bootstrap is a candidate upstream owner,
not an already derived kinematic input. No integral, weighting, action, or desired filter is added.

## 8. Complete 120-cell census

The atlas contains exactly one row for each of 24 identities and five fixed families:

| Disposition | Count |
|---|---:|
| `AGGREGATE_MEMBER_DEPENDENT` | 3 |
| `BLOCKED_MISSING_DYNAMIC_LAW` | 24 |
| `BLOCKED_MISSING_PHYSICAL_QUERY` | 14 |
| `BLOCKED_NONUNIQUE_INTRINSIC_CLOCK` | 1 |
| `INSUFFICIENT_TYPED_EVIDENCE` | 42 |
| `NO_OWNED_NONZERO_CLOCK_SCALE` | 4 |
| `OWNER_CONDITIONAL_BRANCH_ONLY` | 2 |
| `SUPPORTED_NO_COMPLETE_PHYSICAL_OWNER` | 24 |
| `TRANSPORT_OR_READOUT_ONLY` | 6 |

The 24 null-hypothesis rows say that no identity presently owns the **complete physical**
non-isometric magnitude. They do not erase R17/R18's narrower clock-magnitude ownership and do not
predict what unrealized taxonomy branches will do when actual metrics exist.

## 9. What this narrows

The open joint is not uniform:

- **R17:** derive or reject the selector that solders an already-owned endpoint magnitude to an
  already-owned reciprocal grading as the physical comparison, while retaining path holonomy and
  the complete pair surface;
- **R18:** derive an intrinsic ruler/reciprocal completion or prove none exists on the branch;
- **other branches:** first obtain the missing typed query, nonzero calibration state, or native
  dynamical owner.

The next strongest bounded question, if external review accepts this classification, is R17's
**magnitude-to-grading selection joint**: whether the two founding postulates require the owned
`delta_K` to act through the owned reciprocal grading, or whether both zero and nonzero lifts remain
compatible.

## 10. Maximum conclusion

This is complete only for the frozen 24 identities, five families, and their declared regular
strata. It does not select a universe branch, `delta_RF`, R17, a pair surface, universal `c_eff`, an
action, source, carrier, matter, mass, bootstrap value, `X_max`, CMB spectrum, or signalling law.
