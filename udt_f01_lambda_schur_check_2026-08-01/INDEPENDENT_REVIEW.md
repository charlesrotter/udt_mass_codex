# Independent cold review — F01 lambda/mu Schur check

Date: 2026-08-01  
Reviewer: fresh adversarial Codex subagent `/root/f01_schur_cold_verifier`  
Verdict: **PASS-WITH-CAVEATS**

## Result first

The scientific result survives the cold replay:

```text
SCHUR_SIGN_MIXED_ACROSS_OWNED_BRANCHES
```

Within the conditional local F01 constants-census slice, at `ell=1`, on the unique massive
crease root in `s in (1,3)`, and under the supplied R05/R06 trace fork plus the
germ-Hessian-flat wall witnesses:

- R05 has strictly positive lambda/mu Schur sign for both the right-Dirichlet and free-right
  form domains;
- R06 has an explicit strictly negative joint field-plus-mu witness for both domains; and
- all four joint negative indices are exactly one.

I found no factor-of-two error, sign reversal, boundary-domain substitution, false all-root
argument, or inertia overclaim in that bounded mathematics.

One preregistered procedural gate is unmet: both primary interval certificates report 50- and
60-decimal-digit runs, while `PREREGISTRATION.md` requires primary arithmetic at at least 80
decimal digits. The independent replay used 90/100-digit outward interval arithmetic and confirms
the signs with large margins, so this is not evidence of a changed scientific outcome. It is still
a required contract repair before an unconditional package `PASS`.

## Independent route

The verifier did not import or execute any primary script. It first re-differentiated the frozen
joint density and evaluated the **unreduced** Hessian on independently reconstructed R05 responses
and on the supplied exact-rational R06 witnesses. Only after freezing those outcomes in memory did
it open the primary JSON outputs for regression comparison.

All 12 source-manifest objects at base `53bdc2c` matched their Git blob, byte count, and SHA-256.
The current premise guard also passed:

```text
PASS: 18 premise guards, 9 startup controls, 754 candidate dispositions, corrected DOF semantics
```

### 1. All-root proof and bracket

With `z=s(x+1)`, the weight is

```text
q(z)=1-z+z^2/2,
F(s)=I(2s)/s,
I(U)=integral_0^U log(q(z)) dz.
```

Because `q(z)-1=z(z-2)/2`, `I` decreases on `(0,2)` and increases strictly for `U>2`.
Moreover, `I(2)<0` and

```text
I(6) >= -2 log(2) + 2 log(5) = 2 log(5/2) > 0.
```

Thus there is exactly one root in `s in (1,3)`. Independent outward evaluation gave

```text
F(1.68102) in
[-5.13232447866439018491e-6, -5.13232447866439018490e-6]

F(1.68103) in
[ 9.03495074230082799733e-6,  9.03495074230082799734e-6].
```

The high-precision noncertifying root readout was
`1.6810236226618486823362104283993544366...`.

### 2. Scale and factor-of-two check

Direct second differentiation at generic finite nonzero `a_F=a` and `a_F'=a'` gives

```text
k = a'/a^2,
Q = Q_field + 2(k mu)L + (k mu)^2 C.
```

Hence the scalar Schur complement is multiplied by `k^2>0`; the P1 representative cannot
change its sign. For `a=a'=2`, `k=1/2`, so the representative-mu Schur value is one quarter of
the dimensionless `nu=1` value. This independently catches both the possible missing factor of
two in the cross block and a missing second power of `a_F`.

### 3. R05 elimination and boundary domains

Pointwise angular minimization yields

```text
L0[p] = -(w p')' - s^2 p/w,

ell[p] = integral {
  s^2 p [1 + log(w)(1-1/w)] + log(w) w' p'
} dx,

C = s^2 integral log(w)^2(1-1/w) dx.
```

The response source and exact basis rechecked symbolically:

```text
L0[u] = s^2 [1-(1-log(w))/w],
u_part = 1-log(w),
v1 = w'/w,
v2 = 1-1/w.
```

The independently reconstructed responses are

```text
u_D = 1-log(w) + v1/s + B_D v2,
B_D = -[W(1-log(W))+2s-1]/(W-1),

u_F = 1-log(w) + v1/s - v2/(2s-1),
W=w(1).
```

They obey, respectively,

```text
u_D(-1)=u_D(1)=0,

u_F(-1)=0,
w u_F' + w' u_F + log(w)w' = 0 at x=1.
```

The left-vanishing homogeneous solution is proportional to `v2`; `v2(1)` is nonzero on the
Dirichlet domain, and its homogeneous natural trace is `w'(1)`, also nonzero. Thus neither
response inverts a hidden zero mode.

The free-right boundary contribution was not lost. Before integration by parts, the raw field
density contains `2w'pp'+s^2p^2`; after reduction it differs by
`d(w'p^2)/dx`. Evaluating the raw Hessian directly therefore retains the free-right boundary term.

Coarse independent 90/100-digit outward range enclosures over the entire root bracket were:

| R05 domain | dimensionless `nu` Schur enclosure | representative `mu` enclosure |
|---|---:|---:|
| right Dirichlet | `[6.9966, 9.7104]` | `[1.7491, 2.4276]` |
| right free | `[6.8981, 9.1913]` | `[1.7245, 2.2979]` |

These intentionally coarse enclosures exclude zero by wide margins and overlap the tighter
primary certificates.

### 4. R06 admissibility and negative witnesses

For each supplied witness,

```text
p(x)=P_factor(x) sum_(k=0)^3 p_k x^k,
f_variation(x)=(1-x^2) sum_(k=0)^3 f_k x^k,
mu=1.
```

`P_factor=1-x^2` gives both-end Dirichlet `p`; `P_factor=1+x` gives the crease-Dirichlet/free-right
domain. Exact rational endpoint evaluation gives

```text
p_FREE(1) = -250315829/500000000 != 0,
f_variation(-1)=f_variation(1)=0.
```

Thus the free witness genuinely exercises the larger free-right form domain rather than silently
substituting Dirichlet. A generic free-right trial function is not required to satisfy the Euler
Robin condition; that condition belongs to a stationary response/eigenfunction, not to every
member of the quadratic-form domain.

The verifier evaluated the full representative raw Hessian

```text
w(p'^2+f'^2) + 2p(w'p'+s f') + s^2p^2
+ s^2p(1+log w) + log(w)(w'p'+s f')
+ s^2 log(w)^2/4.
```

Its whole-bracket outward enclosures were

| R06 domain | full joint-Q enclosure |
|---|---:|
| right Dirichlet | `[-0.7358, -0.5744]` |
| right free | `[-1.4832, -1.3218]` |

Both are strictly negative and overlap the primary certificates.

### 5. Inertia

- R05: the frozen parent source owns field index one. The independently positive one-coordinate
  Schur complement leaves the joint negative index equal to one by Sylvester inertia, modulo the
  derivative-invisible angular shift kernel which has zero cross coupling.
- R06: the frozen parent source owns a nonnegative/positive field core. A negative witness gives
  joint index at least one. Because the field core is codimension one in the joint space, any
  negative subspace has dimension at most one. The joint index is therefore exactly one.

No conclusion here counts unrestricted second-wall-germ curvature or a full chain/time problem.

## Mutation and false-pass audit

The independent artifact records 14 mutation/catch-proof rows covering: lost root coverage; wrong
`z=s(x+1)` upper limit; wrong scale power; missing cross factor two; source-sign flip; Dirichlet/free
response substitution; dropped free boundary term; Dirichlet substitution for the R06 free witness;
primitive-versus-derivative confusion; frozen `mu`; dropped positive diagonal; both possible inertia
miscounts; and scope promotion. Three are direct in-memory mutated-data checks and the remainder are
exact algebraic rejection proofs tied to symbolic identities. They are not claimed as 14 independent
numerical reruns.

## Required repair

Before changing this disposition to `PASS`:

1. Raise both primary certificate runs from 50/60 interval decimal digits to at least the
   preregistered floor, preferably 80/100 or stronger.
2. Require the higher-precision intervals to nest inside the lower-precision intervals and exclude
   zero on all four branches.
3. Regenerate `FREE_SCHUR_CERTIFICATE.json` and `NEGATIVE_WITNESS_CERTIFICATE.json`.
4. Update the 50/60-digit numerical-method sentence in `EXACT_DERIVATION.md`.
5. Rerun `verify_f01_package.py` and this independent verifier.

No algebraic or scientific repair is otherwise required by this review.

## Four gates and ceiling

1. **Preregistered:** yes, but the primary `>=80`-digit execution clause is not yet met.
2. **Full or bounded:** complete for the four named local F01 form domains and every root in
   `s in (1,3)`; not a full F01 wall/chain/time problem.
3. **Independent:** yes for source freeze, algebra, signs, admissibility, and inertia; primary-output
   comparison occurred only afterward.
4. **Premises:** passed the current premise guard; constants census, conditional P4 response,
   `ell=1`, supplied trace fork, and germ-flat witness status all travel.

Maximum conclusion: **conditional local F01 lambda/mu Schur sign and joint index only.** The free
second wall germ, full chain, physical boundary, native variation/action/carrier/source/matter/mass,
time persistence, bootstrap membership, and global stability hypothesis remain open.

Environment-only caveat: this subagent could not fetch/pull because its sandbox exposed `.git` as
read-only. It verified checked-out HEAD `af71724` and all frozen source objects; the parent context
will independently confirm origin synchronization before banking.
