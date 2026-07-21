# P02 law-neutral local-jet atlas — preregistration

Date: 2026-07-21

Base: `0167b90438fbc13679b7a043066ab990ea54aa98`

Authority: Charles explicitly authorized the next registered step after accepting the completed P01
canonical geometry evaluator.

## Frozen question

What are the exact local zero-, first-, and second-jet strata of the complete law-neutral metric
configuration, after coordinate, local-frame, and Common-Scale Neutrality bookkeeping is made
explicit, while retaining the signed local `phi` field and the conditional supplied `2+2` split as
separate structures?

This is P02 `LOCAL_JET_ATLAS` in `CONFIGURATION_SPACE`. It does not impose Reciprocity as an
off-shell metric constraint, apply the finite-cell seal, select a reciprocal plane, choose a
`phi`-metric join, evaluate an action or EOM, rank a branch, solve an ODE/PDE, or compare with GR,
matter, or observations.

## Whole frame and bounded regime

- The regular parent is a four-dimensional Lorentzian metric/coframe local two-jet.
- The zero-jet closure also retains every real symmetric 4x4 inertia class, including degenerate
  and non-Lorentzian type-change loci. P01 rejects those loci as evaluator inputs; P02 records them.
- First- and second-jet differential strata are certified on the regular Lorentzian branch. No
  inverse-dependent quantity is extended canonically across `det(g)=0`.
- `phi` is an independent signed local field for this classification. Its value and covector are
  not identified with distance or with a metric slot.
- The ten-slot `2+2` representation is conditional on a supplied base/screen split. Its type-change
  closure is mapped, but the split is not selected or promoted to global geometry.
- All work is point-local. Continuous tensor components and invariants remain free moduli; the atlas
  classifies the registered exact discriminant/rank/Jordan strata rather than replacing continuous
  space by a numerical grid.

## Redundancy and dimension contract

The atlas will verify the standard local jet count directly rather than assume it:

1. a symmetric metric two-jet has `10 + 40 + 100 = 150` components;
2. an invertible coordinate Jacobian fixes the zero-jet representative to an inertia normal form;
3. 40 second-coordinate-derivative parameters remove the metric first jet in normal coordinates;
4. 80 third-coordinate-derivative parameters remove the noncurvature part of the second jet;
5. the remaining 20 components are the algebraic Riemann tensor; and
6. local positive CSN rescaling changes the ten-component Schouten/Ricci sector through the Hessian
   of `ln Omega` while leaving the ten-component Weyl tensor and its Petrov type invariant.

Local Lorentz changes of coframe are metric gauge. Petrov labels and polynomial invariants are used
instead of treating frame components as distinct branches. The atlas will explicitly retain that a
generic Weyl orbit still has continuous invariant moduli; a discrete Petrov label is not a complete
numerical solution.

## Frozen zero-jet strata and witnesses

### Full metric inertia

Enumerate exactly the 15 triples `(n_negative,n_positive,n_zero)` summing to four. The frozen witness
for each is diagonal with `-1`, then `+1`, then `0` in those multiplicities. `det(g)=0` is the
degeneracy discriminant. Positive CSN rescaling must preserve every triple.

### Conditional split inertia

Enumerate the Cartesian product of the six real symmetric 2x2 inertia triples for `h` and the six
for `q`, giving 36 supplied-split strata. Use the fixed rational mixed matrix

`A = [[1/3,-1/5],[2/7,1/11]]`.

The exact triangular congruence must prove `inertia(g)=inertia(h)+inertia(q)`,
`rank(g)=rank(h)+rank(q)`, and `det(g)=det(h)det(q)` for every stratum. The P01 regular conditional
branch is exactly Lorentzian `h` plus positive-definite `q`. `det(h)=0`, `det(q)=0`, and failure of
the Sylvester conditions `q22>0`, `det(q)>0` remain visible type-change boundaries.

## Frozen first-jet strata and witnesses

All first-jet witnesses use `g=diag(-1,1,1,1)`, supplied `h=diag(-1,1)`, `q=I2`, and `A=0` at the
point.

### Signed `dphi`

Classify the eight exact alignment/causal strata:

1. zero covector;
2. horizontal-only timelike, null, and spacelike;
3. vertical-only spacelike; and
4. mixed horizontal/vertical timelike, null, and spacelike.

Frozen covector witnesses are respectively
`(0,0,0,0)`, `(1,0,0,0)`, `(1,1,0,0)`, `(0,1,0,0)`,
`(0,0,1,0)`, `(2,0,1,0)`, `(1,0,1,0)`, and `(1,0,2,0)`.
The causal discriminant is `g^{-1}(dphi,dphi)=0`, with the zero covector kept separate. Positive CSN
rescaling may change the norm magnitude but not zero/nonzero status or causal sign.

### Screen expansion, shear, and twist

Use horizontal fields `H_i = partial_i - A_i^A partial_A` and define

`F^A_ij = H_i(A^A_j) - H_j(A^A_i)`,

`B_iAB = (1/2)(L_Hi q)_AB`,

`theta_i = tr(q^{-1} B_i)`, and

`sigma_i = B_i - (theta_i/2) q`.

Classify the exact product of expansion-covector rank `0/1`, shear-map rank `0/1/2`, and twist-map
rank `0/1`, giving 12 first-jet split strata. At `q=I2,A=0`, use `theta=(0,0)` or `(1,0)`; use the
trace-free basis `diag(1,-1)` and `[[0,1],[1,0]]` for shear rank; and use
`F_01=(0,0)` or `(1,0)` for twist. These factors are constructed from independent first-jet
channels, so the exact 12-fold product must be realized without numerical search.

Under `g -> Omega^2 g`, `A` and `F` are unchanged,
`q^{-1}sigma` is unchanged, and
`theta_i -> theta_i + 2 H_i(ln Omega)`. Expansion is therefore representative-dependent and may be
shifted arbitrarily at one point; its zero/sign is not a pre-scale branch selector. This distinction
must be tested, not merely stated.

## Frozen second-jet strata and witnesses

Second-jet witnesses use Riemann normal coordinates at the point: `g=diag(-1,1,1,1)` and `dg=0`.
Every desired algebraic curvature tensor is converted to a symmetric metric second jet through the
normal-coordinate quadratic formula and independently reconstructed by P01.

### Curvature and Ricci ranks

- Curvature-operator rank: all seven ranks `0..6`, using diagonal sectional-curvature entries on the
  ordered bivector basis `(01,02,03,23,31,12)`.
- Ricci-endomorphism rank: all five ranks `0..4`, using fixed diagonal mixed-Ricci witnesses and the
  exact four-dimensional Weyl-free curvature decomposition.

Every rank is certified by exact minors/rational row reduction. No small singular value or floating
cluster may define a stratum.

### Weyl/Petrov algebraic type

Classify all six four-dimensional Lorentzian Weyl types with exact complex symmetric trace-free
three-by-three self-dual operators `Q=E+iB`:

- `I`: `diag(1,2,-3)`;
- `D`: `diag(1,1,-2)`;
- `II`: `[[2,i,0],[i,0,0],[0,0,-2]]`;
- `III`: `[[0,1,i],[1,0,0],[i,0,0]]`;
- `N`: `[[1,i,0],[i,-1,0],[0,0,0]]`; and
- `O`: zero.

Reconstruct a real Weyl tensor from `E=Re(Q)` and `B=Im(Q)`, prove all algebraic curvature
identities and zero Ricci, convert it to a metric second jet, and recover the same type independently.
Use exact invariants `I=(1/2)tr(Q^2)`, `J=-(1/6)tr(Q^3)`, specialty discriminant
`Delta=I^3-27J^2`, nilpotency indices, and the minimal polynomial to distinguish the types. Petrov
type and Weyl zero/nonzero status are pre-scale invariants. Ricci rank, scalar curvature, and full
Riemann rank remain representative-dependent under local CSN.

## Coverage and product logic

The atlas must distinguish:

- complete discrete coverage of the registered inertia, causal/alignment, rank, integrability, and
  Petrov strata;
- exact symbolic continuous moduli retained inside each stratum; and
- combinations that are undefined at a degenerate metric or unavailable without a supplied split.

On the regular Lorentzian supplied-split branch, zero-, first-, and second-jet channels are freely
specifiable independently before an EOM. Exact constructions must prove that registered factor
strata can be combined; no Monte Carlo frequency may stand in for existence or completeness.

## Independent verification and catches

The main atlas may reuse P01 only as the frozen geometry evaluator. A separate verifier must rebuild
the load-bearing inertia, split congruence, `dphi`, Frobenius/deformation, normal-coordinate
curvature, rank, Schouten/CSN, and Petrov calculations with independent exact formulas.

Exercised fail-closed mutations must reject at least:

1. a missing or duplicate 4D inertia class;
2. a missing or duplicate supplied-split class;
3. an incorrect inertia or determinant factorization;
4. omitted `dphi=0`, null, vertical, or mixed strata;
5. treating null and zero `dphi` as the same;
6. a missing expansion/shear/twist rank combination;
7. declaring expansion CSN-invariant;
8. declaring twist or shear rank representative-dependent at a point;
9. calling nonzero twist integrable;
10. a divided-away zero-rank curvature or Ricci branch;
11. a missing Petrov type;
12. a wrong Petrov invariant, nilpotency index, or D/II distinction;
13. treating Ricci rank or scalar curvature as pre-scale invariant;
14. accepting a floating-only witness;
15. promoting a supplied split, `phi` join, action, EOM, or physical branch;
16. calling a local jet a global solution or physical evolution; and
17. launching P03.

## Compute and stop contract

CPU only; SymPy exact rational/complex algebra first, with float64 P01 replay used only as a regression
anchor. Runtime is bounded to ten minutes and memory to 4 GiB. No parameter sweep, ODE, PDE, GPU,
carrier computation, empirical comparison, or long solve is permitted.

Stop if any registered stratum lacks an exact witness, a rank depends on tolerance, the normal-jet
reconstruction fails, a type-change locus is divided away, or the independent implementation
disagrees.

## Maximum conclusion

`LOCAL_KINEMATIC_SOLUTION_SPACE_CHARACTERIZED_WITHOUT_DYNAMICS`

This ceiling means the registered local jet strata and their continuous moduli are characterized as
configuration geometry. It does not make any stratum on shell, physical, stable, global, or favored;
it does not derive a native action, source, matter carrier, boundary completion, or bootstrap law.
