# Formulae and index conventions

This package uses coordinates `x^mu = (x0,x1,y2,y3)`, internal coframe indices `I,J`, base indices
`i,j = 0,1`, and screen indices `A,B = 2,3`. The internal metric is
`eta = diag(-1,+1,+1,+1)`. The coframe matrix has rows `I` and columns `mu`:

The `2+2` interface is conditional on a supplied base/screen split; the evaluator does not select it.

```text
g_mu_nu = eta_IJ e^I_mu e^J_nu.
```

The primary evaluator input is the local metric two-jet
`(g_mu_nu, partial_a g_mu_nu, partial_a partial_b g_mu_nu)`. First jets are symmetric in metric
indices; second jets are symmetric in both metric and derivative index pairs.

## Conditional 2+2 representation

Given—not selected—a base/screen split,

```text
ds^2 = h_ij dx^i dx^j
     + q_AB (dy^A + A^A_i dx^i)(dy^B + A^B_j dx^j).
```

The ten slots are `h00,h01,h11,q22,q23,q33,A2_0,A3_0,A2_1,A3_1`. The coordinate blocks are

```text
G_ij = h_ij + q_AB A^A_i A^B_j,
G_iB = q_AB A^A_i,
G_AB = q_AB.
```

The exact inverse and determinant checks use

```text
G^{-1 ij} = h^{ij},
G^{-1 iB} = -h^{ij} A^B_j,
G^{-1 AB} = q^{AB} + A^A_i h^{ij} A^B_j,
det G = det h det q.
```

This representation is complete component bookkeeping only inside the supplied split branch.

## Connection and curvature

```text
Gamma^rho_mu_nu = 1/2 g^{rho sigma}
  (partial_mu g_sigma_nu + partial_nu g_sigma_mu - partial_sigma g_mu_nu),

R^rho_sigma_mu_nu = partial_mu Gamma^rho_nu_sigma
  - partial_nu Gamma^rho_mu_sigma
  + Gamma^rho_mu_lambda Gamma^lambda_nu_sigma
  - Gamma^rho_nu_lambda Gamma^lambda_mu_sigma,

Ric_sigma_nu = R^rho_sigma_rho_nu,
R = g^{sigma nu} Ric_sigma_nu.
```

No Einstein equation or action is evaluated.

## Cartan reconstruction

For inverse frame `E_J^nu`, the torsion-free spin connection is reconstructed from the tetrad
postulate:

```text
omega^I_Jmu = (Gamma^rho_mu_nu e^I_rho - partial_mu e^I_nu) E_J^nu.
```

The verifier checks

```text
T^I_mu_nu = 2 partial_[mu e^I_nu] + 2 omega^I_J[mu e^J_nu] = 0,

Omega^I_Jmu_nu = 2 partial_[mu omega^I_Jnu]
  + 2 omega^I_K[mu omega^K_Jnu]
  = e^I_rho R^rho_sigma_mu_nu E_J^sigma.
```

These are geometric identities, not field equations.

## Common-Scale Neutrality bookkeeping

For `g' = Omega^2 g`, `sigma_mu = partial_mu ln Omega`:

```text
e' = Omega e,
g' = Omega^2 g,
g'^{-1} = Omega^-2 g^-1,
det g' = Omega^8 det g,
sqrt(|det g'|) = Omega^4 sqrt(|det g|),

Gamma'^rho_mu_nu = Gamma^rho_mu_nu
  + delta^rho_mu sigma_nu + delta^rho_nu sigma_mu
  - g_mu_nu g^{rho lambda} sigma_lambda.
```

The evaluator records these weights without selecting a physical representative.
