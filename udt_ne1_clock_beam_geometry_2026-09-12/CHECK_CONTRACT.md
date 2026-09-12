# NCB1 check freeze

Before new computation/reviewer scientific disclosure. Scope: INITIAL_CANDIDATE
equations (1)–(14); claims at infinity require analytic review, not sampling.

Author symbolic route: original four-metric Christoffels and required Riemann
contractions with arbitrary a(t,xi), log b_y(t,xi), log b_z(t,xi); both signs;
null/affine ray, parallel screen, two individual tides and mixed entry.
Independently differentiate the quadrature map, vertex slope, affine scaling
and background primitive. Check trace-free tide using NE1 null constraint.
Structural zeros and normalization arithmetic are coverage/regression, not
independent theorem counts. Use SymPy exact identities, not numeric tolerance.

Author finite route: scipy Bessel/quadrature plus solve_ivp DOP853 direct
curvature Jacobi ODE and null lambda-constraint integral. Samples use
epsilon in {0,1/6,-1/6,1/2}, t_e in {1,2}, xi_e in {0,0.7}, both signs,
lengths in {0.2,2}; selected long-reception illustrations at t_o=10,100,1000
for epsilon=1/6, t_e=1, xi_e=0, s=+1. No fit, data tuning or interval
certification. Finite-leg ODE relative/absolute tolerances 2e-11/2e-12;
accept mixed scaled error <=2e-8 against quadrature. Repeat hardest selected
case at 2e-12/2e-13 to disclose sensitivity. Quadrature epsabs/epsrel 2e-11,
limit500; all warnings/failures retained. Long values are illustrations;
do not evaluate overflowing exponentials or claim numerical asymptotics.

Fixed-path phase formula diagnostic: epsilon=1/6,d=1,xi_e=0.7,both signs,
t_e in {100,200,400,800}; report errors versus (13), no assertion from a
finite sequence of an asymptotic proof. Check positivity from exact finite
integrals; late fixed-path analytic bounds receive substantive review.

Mutations: execute altered-source or altered-validator-input variants that
drop source endpoint b_i(e) normalization, invert the clock ratio, or suppress
lambda in the metric ray while retaining the original connection. The SAME
load-bearing baseline assertions must reject; save actual nonzero defects
and exits. A mere text-token presence check is not a catch proof.

Source-first reviewer chooses an independent argument/check implementation
without seeing these new formulas or results; direct stage will assess all
load-bearing steps, source ownership, branch/marking/limit hypotheses and
false-pass risks. Record checks not repeated and unavailable independence.

CPU only; caps and capture utility are WORK_ORDER.md. No thresholds or samples
may be changed after outcomes without a preserved finite diagnostic and
explicit same-premise repair record. Initial files remain byte-preserved.
