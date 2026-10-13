# Dispatch A — local shape candidate

Status: current researcher candidate awaiting fresh review. This is pure toy
mathematics; no physical interpretation, adoption, promotion, or publication.

## Mandate and source scope

The active dispatch is `../TASK.md`. The admitted premises are:

- P1: `f: R -> R` is twice continuously differentiable.
- P2: `f(-x) = f(x)` for every real x.
- P3: `f(0) = 0`.
- P4: `f(x) >= 0` for every real x.

Question: what universal restriction on the local shape at zero survives the
failure of exact quadratic selection, and what comparisons does it exclude?
Quantifier: every function satisfying P1–P4; asymptotic regime `x -> 0`.
Frame: premise-led pure mathematics, with no metric or physical choices.
P1–P4 are pinned by the toy dispatch, not inferred from method instructions.
The coefficient and test functions remain free-and-explored. No extra premise
is adopted, including analyticity, positive curvature, or a leading power law.

The supplied prior `../NOTEBOOK.md` is the only inspected mathematical
predecessor. It rejects Q1 (“every admitted f is a positive multiple of x^2”)
using x^4. That rejection is retained. No novelty outside this fixture is claimed.
The local skill, copied AGENTS.md, and operating plan supply methods only.

Parent startup attribution: the parent reports branch `grok`, HEAD
`60c273ef24900535ea2f375a32ec394b8bc633b8`, synchronization completed, tracked
files clean, and 76 unrelated untracked names protected. This child did not
verify those repository facts or repeat startup; the isolated task forbids real
repository checks and inspection. No scientific corpus or sibling case was read.

Workspace: only `case_a/output/` is writable. Inputs remain fixed.
Methods: direct elementary calculus, counterexamples, and at most two small CPU
checks; no external search, agents, GPU, background job, or publication.
Planned check: one Python standard-library exact-integer differentiation check
of the oscillatory boundary example, under a 10-second timeout. No grid, fitted
parameters, tolerance, floating-point inference, or long solve is involved.
Checkpoint: this notebook and saved check artifacts. Stop: a substantive
candidate/negative ready for review, or a genuine blocker. Maximum conclusion:
a consequence of P1–P4 with its limits, awaiting fresh review. The explicit
dispatch excludes nested review agents; self-checking will not be called review.

## Discovery and route decisions

1. Q1 is closed by the saved x^4 counterexample. It does not rule out a useful
   local restriction. Even positive quadratic curvature would not imply exact
   quadratic form: x^2+x^4 is also admitted.
2. Q2, developed here: the normalized ratio f(x)/x^2 must have a finite,
   nonnegative limit. Motivation: retain exactly the second-order information
   supplied by C2 and the minimum at zero. Test: derive an integral identity
   and a remainder bound directly from P1–P4.
3. Q2 survives the exact argument below. The zero-limit case remains open as to
   its finer shape; it is not silently discarded as trivial or forced to be x^4.
4. Challenge tempting strengthenings with explicit admitted functions: an
   arbitrary nonnegative quadratic coefficient, arbitrary real leading powers
   greater than two, a flat function, and a degenerate oscillatory function.
   These are witnesses and counterexamples, not a census of all possibilities.

No failed numerical runs or hidden additional assumptions preceded this
candidate. The mathematical exploration above preceded the candidate freeze.

## Frozen candidate A-C1: nonnegative quadratic contact

For every f satisfying P1–P4, there is a unique finite number
`a = f''(0)/2 >= 0` such that

    f'(0) = 0,
    f(x)  = a*x^2 + o(x^2),
    f'(x) = 2*a*x + o(|x|).

In particular `lim[x -> 0, x != 0] f(x)/x^2 = a`. Define the function-specific
continuity modulus

    omega(r) = sup{|f''(t) - f''(0)| : |t| <= r}.

It is finite for each finite r and tends to zero as r decreases to zero. Exact
bounds, valid for every real x, are

    |f(x) - a*x^2| <= x^2*omega(|x|)/2,
    |f'(x) - 2*a*x| <= |x|*omega(|x|).

Proof. Differentiating the evenness identity at zero gives `-f'(0)=f'(0)`.
For any real x, apply the fundamental theorem of calculus twice to
`g(s)=f(s*x)`, on the fixed interval `0 <= s <= 1`. The hypotheses hold because
f is C2. Using f(0)=f'(0)=0 gives

    f(x)  = x^2 * integral_0^1 (1-s)*f''(s*x) ds,
    f'(x) = x   * integral_0^1 f''(s*x) ds.

Subtract the constant-curvature terms and bound the remaining integrals by
omega(|x|). This proves the bounds and limits for both signs of x. Since
`f(x)/x^2 >= 0` for x != 0, its limit is nonnegative. The limit fixes a uniquely.
This proof uses no fourth derivative or nonzero Taylor coefficient.

Every value a >= 0 is possible: `f(x)=a*x^2` satisfies all four premises.
For a=0, nonzero examples also exist, including x^4. Thus the allowed
second-order data at zero are precisely `(f(0), f'(0), f''(0))=(0,0,2*a)`
with a >= 0. This is a characterization of those data, not of all local germs.

Conditional branch: if the derived value a is positive, continuity of f''
provides a function-dependent delta > 0 with f''(x) > 0 for |x| < delta.
Consequently f is strictly convex there and f(x)>0 for 0<|x|<delta. For every
epsilon>0 a sufficiently small delta also gives

    (a-epsilon)*x^2 <= f(x) <= (a+epsilon)*x^2.

Positive a is a case distinction, not a new universal premise. If a=0, the
universal conclusion is f(x)=o(x^2), with no asserted leading nonzero power.

## Sharpness and adverse examples

1. For every real p>2, `f(x)=|x|^p` is admitted. Away from zero its second
   derivative is `p*(p-1)*|x|^(p-2)`; the first and second derivatives at zero
   are zero and extend continuously. Taking 2<p<4 refutes the proposed
   strengthening “a=0 implies f=O(x^4).” Nonintegral p also defeats an assumed
   integer-power expansion. This family is a witness, not a chosen law.
2. Let f(0)=0 and `f(x)=exp(-1/x^2)` for x != 0. This admitted even function is
   positive away from zero and is o(|x|^p) for every fixed p>0. To check the
   required C2 hypothesis directly, its derivatives away from zero are
   `2*x^(-3)*exp(-1/x^2)` and
   `(4*x^(-6)-6*x^(-4))*exp(-1/x^2)`; both tend to zero at zero. The difference
   quotients at zero do so too. Exponential decay dominates each fixed power,
   as follows directly from the positive exponential series. Thus a nonzero
   leading power is not guaranteed, even for a nonzero function.
3. Let f(0)=0 and `f(x)=x^8*(2+sin(1/x^2))` for x != 0. It is even and
   nonnegative. Its derivatives away from zero are

       f'(x)  = 8*x^7*(2+sin(1/x^2)) - 2*x^5*cos(1/x^2),
       f''(x) = 56*x^6*(2+sin(1/x^2))
                -26*x^4*cos(1/x^2) - 4*x^2*sin(1/x^2).

   The difference quotients give f'(0)=f''(0)=0, and these expressions tend to
   zero, proving C2 at zero. At positive points with `1/x^2=pi/2+2*pi*k`,
   f''(x)=168*x^6-4*x^2<0 for all sufficiently large integers k. At points
   with `1/x^2=3*pi/2+2*pi*k`, f''(x)=56*x^6+4*x^2>0. Both sequences tend
   to zero. Local convexity therefore is not forced in the a=0 case.
   At `1/x^2=2*pi*k`, f'(x)=16*x^7-2*x^5<0 for all sufficiently large k;
   at `1/x^2=(2*k+1)*pi`, f'(x)=16*x^7+2*x^5>0. Thus even monotonic
   increase on a right neighborhood of zero need not hold.

## Comparison use and precise limits

A proposed comparison law whose f(x)/x^2 diverges, lacks a limit, or tends to a
negative constant is excluded by P1–P4. For example, a positive leading cusp
`c*|x|^p` with c>0 and 0<p<2 is impossible. An oscillating coefficient of
x^2 with no limit is also impossible. Each surviving a>=0 remains free, and
the theorem supplies no uniform neighborhood, convergence rate over the class,
growth law, equation, or unique comparison law. It constrains the germ at zero,
not arbitrary shapes away from zero. Evenness is sufficient for f'(0)=0;
nonnegativity and f(0)=0 would also imply this by the elementary minimum test.

## Verification, disposition, and next decision

The proof above is exact mathematical reasoning by this researcher. The saved
`check.py` separately differentiates the oscillatory example using exact integer
coefficient rules and checks the stated derivative coefficients and phase
reductions. It is a same-context algebra regression, not independent review,
not a numerical proof of the universal statement, and not class sampling.
Actual command, versions, outcome, resource use, source hashes, and artifact
hashes are recorded in adjacent output files after execution.

Return point reached: substantive candidate A-C1 and adverse results suitable
for review. The local-shape uncertainty has narrowed from unrestricted law
selection to finite nonnegative quadratic contact, with a sharp distinction
between positive-curvature and degenerate cases. Further searches for a unique
law under the same premises have no support in this result.

Proposed next decision: send A-C1's exact integral argument and its sharpness
examples to a fresh reviewer. The reviewer should challenge both signs of x,
the modulus bound, the nonnegative limit, the positive-curvature branch, and the
C2 status and sign sequences of the degenerate examples. No such review has
occurred here, and no agent was spawned. A successor should name the remaining
comparison question it could resolve. A unique-law conclusion would require
additional justified restrictions because the admitted counterexamples already
rule out uniqueness. This return does not request routine permission or assert
that all informative mathematics is exhausted.

The supplied prior notebook and initial Q1 remain unchanged. No repository
integration, commit, push, physical adoption, or CANON edit was performed.

### Actual execution record

One of the permitted two CPU checks was used. From `case_a/output/`, the exact
command was:

```bash
timeout 10s python3 check.py > check.stdout.json 2> check.stderr.txt
```

It exited 0 with all six exact algebra comparisons passing. The saved stdout
records Python 3.10.12, Linux x86_64, an internal measured duration of about
0.00091 seconds, and peak resident memory of 10,176 KiB. The duration excludes
interpreter startup. Stderr is empty. There were no failed or repeated runs.
No second mathematical CPU check was needed; exact arguments own the claims.
The check does not verify universal quantifiers or replace inspection of limits.

Input bytes were recorded after the research write, using:

```bash
sha256sum ../TASK.md ../NOTEBOOK.md ../AGENTS.md ../UDT_RESEARCH_OPERATING_PLAN.md ../.agents/skills/goal-directed-research/SKILL.md > source_sha256.txt
```

Only the two new authored files `NOTEBOOK.md` and `check.py`, their check outputs,
and provenance manifests were created under output/. These recorded hashes bind
the inspected sources; they are not a before/after proof or a scientific check.
The output manifest binds the final artifacts without including itself.
