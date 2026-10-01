# TPP1 source-first mathematical assessment

Reviewer `/root/tpp_math` is an actual separate context, with the parent model
inherited. This is not a different-model or blind review. Parent startup and
the unchanged launch full406/central checks are attributed to the parent; I
independently checked `grok` HEAD `90d9bc49e2fed787d9068b0a50e13a62ac58021b`
and tracked-clean status. The 52 unrelated names were not opened. This reviewer
owns only `review/math/`; CPU checks are capped at180s/4GiB each.

I read the work order, central R12T, current G312 filter-only authority, TDS1's
equations and prior independent metric-only Ricci and original ADM-constraint
review implementations. Those existing implementations will be reused with
explicit attribution rather than represented as new independent derivations.
The prior implementations share Fourier collocation with the producer; they
do not call its evolution code. Current review concerns conditional numerical
methods and cannot identify Ricci with the native UDT response.

## Principal coordinate-frequency bound

For a spacelike slice, write the metric as

    ds² = -alpha² dt² + gamma_ij(dx^i + beta^i dt)(dx^j + beta^j dt).

The frozen-coefficient principal wave operator has frequencies

    omega = -beta·k +/- alpha sqrt(k_i gamma^ij k_j)

for exp(i(k·x-omega t)). Therefore, with |k_i| <= Kmax,

    |omega| <= Kmax |beta|_1 + alpha sqrt(lambda_max(gamma^-1)) |k|_2
            <= Kmax (|beta|_1 + alpha sqrt(3 lambda_max(gamma^-1))).

Take the maximum over sampled spatial points. For a cubic even N grid and
period L, Kmax=pi N/L safely includes the Nyquist second derivative even if
the real first-derivative convention removes its first derivative. Cubical
Fourier support, positive gamma and lapse, finite inverse, and the actual
evolved shift are needed. An anisotropic grid requires the appropriate
per-direction bounds, not an unqualified substitution of one smaller N.

This bounds local frozen-coefficient principal frequencies. It does not bound
the full variable-coefficient discretized operator, coefficient-derivative
terms, pseudospectral aliasing, nonlinear growth or nonnormal transient
amplification. RK4's imaginary-axis interval alone is not nonlinear stability.
A small CFL factor is an engineering control requiring original-equation
checks, refinement and a qualified finite history. If the controller evaluates
only the current metric, its bound predicts the next step; it does not promise
the bound remains satisfied at internal stages or the endpoint. Stage checks
and step rejection can strengthen that narrower engineering control.

## General transverse-traceless modes

For any nonzero integer n, choose orthonormal transverse vectors p,q with
p·n=q·n=0. Then

    Tplus = p tensor p - q tensor q,
    Tcross = p tensor q + q tensor p

are symmetric, trace-free, and satisfy n^i T_ij=0. A finite sum of their
constant linear combinations times cos(2pi n·x/L + phase), plus any constant
trace-free symmetric tensor, is analytically TT for the flat conformal metric.
The allowed n must fit the supplied grid; sampling a wave above Nyquist can
alias its direction and invalidate the discrete divergence. Strictly below
Nyquist avoids the ambiguous real Nyquist mode. A deterministic transverse
basis is a construction choice, not a physical polarization selection law.

For constant tau the existing positive conformal solve remains the supplied
vacuum-constraint construction. Its scalar residual does not replace checking
the original Hamiltonian and momentum constraints from saved gamma,K.
Generalized modes may require higher mesh resolution: no tolerance increase or
seed removal should manufacture a pass. Three linearly independent active
wavevectors can support loss of constant translation symmetry; this does not
exclude arbitrary nonlinear Killing fields.

## Planned scoped numerical checks

Check analytic TT contraction and independently differentiated saved seeds;
original saved gamma,K constraints and harmonic compatibility; rejected
nonfinite/degenerate bounds; direct principal-frequency comparison on finite
Fourier modes, including a deliberate omitted-shift false-pass fixture.
Reuse the prior original metric-only Ricci checker on uniformly spaced saved
windows, all eligible times and grid points up to32³ within the CPU cap.
Compare matched states and readouts under spatial and time refinement. Larger
load-only meshes must remain distinguished from scientifically checked meshes.
The two omitted slices at either end of each five-point Ricci window and gaps
between windows remain explicitly untested by that diagnostic.

This source-first note precedes TPP1 producer code and numerical outcomes.
Substantive results and exact source bindings will be recorded separately.

## Initial reviewer controls

`check_principal_bound.py` passed24 seeded positive-metric trials over729
Fourier vectors each, ten independently SVD-constructed TT polarizations,
four invalid-hypothesis catches and an omitted-shift counterexample. These
are controls supporting the stated algebra, not producer validation.
The first capture invocation requested the work-order4GiB allowance; the
unchanged capture utility rejected it because that utility caps memory at2GiB
(`assert 1<=seconds<=900 and 1<=mib<=2048`, before running the checker).
The repeated command used180s/2048MiB and passed in0.052s,33152KiB peak RSS.
Its captured stdout, stderr and receipt are saved as `principal_bound.*`.
