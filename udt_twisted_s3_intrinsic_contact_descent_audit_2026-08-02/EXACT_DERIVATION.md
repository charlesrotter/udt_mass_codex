# Exact derivation — branch-intrinsic contact descent

## 1. Frozen witness and derived reduction

The audit stays inside the three previously verified off-shell metrics

```text
theta0=u^(-1/2)(dt+sigma3),
theta1=u^(+1/2)sigma3,
theta2=u^(lambda/2)sigma1,
theta3=u^(lambda/2)sigma2,
g=-theta0^2+theta1^2+theta2^2+theta3^2,
lambda=-1,0,+1,
4<=u<=11,
d sigma3=kappa sigma1 wedge sigma2,  kappa=-2.
```

The parent all-gate audit proves that the full continuous Killing algebra is one-dimensional. Its
unique line is timelike, and the nonzero Killing twist gives a global spacelike ruler line. For any
local unit representatives, the two lines are represented in the displayed coframe by

```text
T=plus_or_minus E0,       S=plus_or_minus E1.
```

No displayed coframe slot is being promoted merely by its label: the independent Killing and twist
certificates identify these lines first. Hence

```text
Pi_pair=-T tensor T_flat+S tensor S_flat,
H=identity-Pi_pair
```

are sign-independent metric tensors on this witness. `H` is the orthogonal screen projector.

## 2. Tensorial contact objects

The old full-screen calculation used the coefficients of `dtheta0` and `dtheta1` on an oriented
screen. To remove orientation and frame choices, define instead

```text
F_T_ab=H_a^c H_b^d (d T_flat)_cd,
F_S_ab=H_a^c H_b^d (d S_flat)_cd,
Q_T=(1/2) F_T_ab F_T^ab,
Q_S=(1/2) F_S_ab F_S^ab,
Q=Q_S-Q_T.
```

`T` or `S` sign reversal changes the corresponding two-form sign but not its squared norm. A
screen-orientation reversal changes the signed area coefficients but not these contractions. A
constant rescaling of the unnormalized Killing generator disappears when `T` is normalized. Since
the projectors and exterior derivatives transform tensorially, all three contractions are invariant
under arbitrary passive frame changes—including frames mixing the derived pair and screen.

This differs from taking the `23` slots of an arbitrarily transformed coframe. The exact rational
Lorentz control in `derive_intrinsic_descent.py` gives

```text
Q_naive=(9/16)(q_S^2-q_T^2),
Q_tensor=q_S^2-q_T^2.
```

The naive slot route is therefore rejected, exactly as required by the parent full-frame no-descent
result. The new descent works because the metric-derived projectors are reconstructed first.

## 3. Exact witness formulas

Since `T_flat=-theta0` and `S_flat=theta1`, the first structure equations give

```text
F_T=-t0 theta2 wedge theta3,
F_S=+t1 theta2 wedge theta3,
t0=kappa u^(-1/2-lambda),
t1=kappa u^(+1/2-lambda).
```

Therefore

```text
Q_T=kappa^2 u^(-1-2 lambda),
Q_S=kappa^2 u^(+1-2 lambda),
Q=kappa^2 u^(-1-2 lambda)(u^2-1).                 (1)
```

These are genuine metric scalars on the explicit witness. The signed pair `(q_T,q_S)` remains a
section of the sign/orientation local system, not two canonically signed numerical scalars.

With `kappa^2=4` and `4<=u<=11`, the exact ranges are

| `lambda` | monotonicity | exact `Q_min` | exact `Q_max` |
|---:|---|---:|---:|
| -1 | increasing | `240` | `5280` |
| 0 | increasing | `15` | `480/11` |
| +1 | decreasing | `480/1331` | `15/16` |

Thus all three metrics occupy only the strict `Q>0` stratum. There is no null or negative contact
point on the frozen witness. This does not remove those strata from other profiles, twist values,
screens, or branches.

## 4. Differential reconstruction

Both squared amplitudes are nonzero. On the frozen `a=R=1` witness their dimensionless ratio first
gives an **absolute** metric scalar:

```text
Phi_contact=(1/4)log(Q_S/Q_T)=(1/4)log(u^2)=phi.          (2)
```

No Killing rescaling, sign, orientation, or dimensional reference enters this ratio. This absolute
identification is bounded to the frozen unit witness. In the general unfrozen constant-parameter
family the same construction gives

```text
Phi_contact=phi+(1/2)log(R/a),
```

so it does not establish a universal founded zero independently of the branch normalization.

Direct differentiation gives

```text
dphi=(1/4)d log(Q_S/Q_T),
dsigma=-(1/4)d log(Q_S Q_T)=2 lambda dphi,
sigma=log(|D|/D0)=lambda log u.
```

Thus `phi` itself and the screen-area differential become intrinsic on the frozen witness. The
product `Q_S Q_T` is dimensionful, so absolute `sigma` still needs an area reference; only
`dsigma` is reference free.

For

```text
z=(1/2)log(Q/T0^2),
```

the absolute scalar depends on the positive dimensional reference `T0`, while

```text
dz=[(u^2+1)/(u^2-1)-2 lambda] dphi
```

is reference independent and metric intrinsic. In particular,

```text
dphi wedge dz=0,
dphi wedge dsigma=0.                                (3)
```

The old alternating contact class therefore **collapses identically on this witness**. The metric
projector resolves the descent problem, but this one-depth screen profile contains no independent
depth–area modulation. Equation (3) must not be described as nontrivial production.

## 5. Object-by-object boundary

The derived projector also promotes complete contractions of the Riemann tensor with `Pi_pair` and
`H` from supplied-split quantities to metric scalars on this witness. This is a class-level
naturality statement; the audit does not compute or select a preferred curvature contraction.

The metric supplies the screen plane and its unoriented area density, not two individual screen
axes. Signed contact components, screen axes, displayed area/shear/rotation/anholonomy slots, and
Levi-Civita connection coefficients remain frame or orientation dependent. An absolute contact log
or alternating primitive retains reference freedom. Parallel transport and holonomy require a path
or loop. No carrier section or global physical law follows from the local bundle reduction.

## 6. Controls and exact scope

- Constant depth: the parent curvature-invariant certificate is zero, so the intrinsic pair is not
  retroactively promoted.
- Twist free: the unique clock certificate may survive, but the ruler line and pair projector do
  not.
- Slice null: the prior ineligible control remains ineligible and is not crossed.
- General `GL(2,R)` screen: not present in this witness and not claimed.

The exact result is branch-intrinsic and off shell. It does not select the profile, `lambda`, twist,
stationarity, `S3`, an equation, action, source, boundary, density/bootstrap return, carrier,
`X_max`, matter, mass, stability, or phenomenology.
