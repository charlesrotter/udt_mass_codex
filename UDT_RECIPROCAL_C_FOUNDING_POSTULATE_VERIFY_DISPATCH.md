# Workstation dispatch — cold audit of the Reciprocal-c founding postulate

## Attribution and scope

Charles Rotter proposed on 2026-07-15:

> **$c$ is a reciprocal identity of time and length—not a one-way speed.** The directions
> $L=cT$ and $T=L/c$ are equally fundamental.

The derivation combines this with the previously stated UDT Reciprocity Principle and positional
composition. Independently determine whether that combination genuinely derives the reciprocal
metric or merely conceals it in terminology.

Audit only these new files:

- `UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md`
- `UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md`
- `verify_udt_reciprocal_c_postulate.py`
- `verify_udt_reciprocal_c_postulate_out.txt`

Do not alter `LIVE.md` or `CANON.md`, adopt the postulate, start F/G, or import GR field equations.

## 1. Cold formalization

Before reading the supplied proof in detail, give at least two precise mathematical meanings of
“$c$ is a reciprocal identity.” Test separately:

1. ordinary covariance/intertwining of the isomorphism $c:\mathcal T\to\mathcal L$;
2. a dual/contragredient action on the two conversion directions.

Report whether the first forces equal or inverse scale factors. Do not allow the successful second
meaning to erase the first countercase.

## 2. Reciprocity circularity gate

State the UDT Reciprocity Principle in words without metric coefficients. Then translate it into
an equation. Determine whether

$$
P^T K P=K
$$

is a faithful independent formulation or whether it simply postulates $uv=1$ under another name.
Return both the strongest defense and the strongest objection.

## 3. Metric derivation

Starting from

$$
q=(c\,dt,dr)^T,
\qquad
P(\Delta)=\operatorname{diag}(u(\Delta),v(\Delta)),
$$

audit:

1. the dual-pairing algebra;
2. the continuous composition theorem;
3. reversal;
4. exclusion or survival of the trivial representation;
5. the local quadratic metric readout;
6. every assumption required to obtain
   $ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2$.

Identify explicitly which parts come from Reciprocal-c, Reciprocity, positional relativity,
observation, and inherited local metric structure.

## 4. Consequence audit

Recompute independently:

$$
\det P,
\qquad
\det g_{(t,r)},
\qquad
\sqrt{-g},
$$

$$
S^{-1}dS,
\qquad
\frac12\operatorname{Tr}\!\left[(S^{-1}dS)^2\right],
\qquad
\frac12\operatorname{Tr}(S_A^{-1}S_B).
$$

Determine whether the quadratic tangent inner product is unique up to normalization on the
one-dimensional group. Separate this geometric fact from an action principle.

## 5. Action adversary

Test the family

$$
I_F=\int dV_4\,F(Y),
\qquad
Y=\frac12\operatorname{Tr}(J_\mu J^\mu).
$$

Exhibit at least two symmetry-compatible choices with different nonlinear Euler equations. Then
independently reduce the canonical quadratic choice in the full reciprocal physical metric to the
static radial sector and test it on

$$
A(r)=1-\frac rX.
$$

Audit the reported residual

$$
\left.\mathcal E_A\right|_{\rm WR-L}
=-\frac{r(4X-3r)}{4(X-r)^2}.
$$

Any algebraic error must be corrected before a conclusion is returned.

## 6. $X$ audit

Determine independently whether the local postulates contain or select a length scale. Check

$$
\phi_{\rm WR-L}=-\frac12\ln(1-r/X)
$$

and its $r\to X^-$ limit. Separate:

- infinite group depth;
- coordinate location $X$;
- global boundary datum;
- integration constant;
- fundamental constant.

Do not recommend postulating $X_{\max}$ merely because it is absent locally.

## 7. Required verdict

Return:

1. PASS/FAIL for sections 1–6;
2. corrected algebra for every failure;
3. full hidden-assumption ledger;
4. strongest circularity objection;
5. strongest reason the postulate is genuinely upstream;
6. one metric verdict:
   - **FAILS TO DERIVE UDT METRIC**;
   - **DERIVES ONLY BY RESTATEMENT**;
   - **DERIVES UNDER EXPLICIT INDEPENDENT PREMISES**;
7. one action verdict:
   - **UNIQUE ACTION DERIVED**;
   - **QUADRATIC GEOMETRY ONLY; ACTION OPEN**;
8. one $X$ verdict:
   - **LOCALLY DERIVED**;
   - **GLOBAL/INTEGRATION STATUS OPEN**;
   - **MUST BE POSTULATED**, with proof.

Retain raw scripts and output. Stop after reporting; no canon or frontier rewrite without Charles's
explicit verdict.
