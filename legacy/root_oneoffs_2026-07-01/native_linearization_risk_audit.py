from dataclasses import dataclass


@dataclass(frozen=True)
class Approximation:
    name: str
    current_linear_form: str
    nonlinear_native_version: str
    risk: str
    next_test: str


APPROXIMATIONS = [
    Approximation(
        name="endpoint power law",
        current_linear_form="f ~ r^-p near the endpoint",
        nonlinear_native_version="solve the full nonlinear f equation with angular/interface boundary data",
        risk="power-law asymptotics may miss finite-cell nonlinear matching constants",
        next_test="compare exact numerical finite-cell solutions to asymptotic p=1/3 scaling",
    ),
    Approximation(
        name="interface scalar jump",
        current_linear_form="B = Delta K R = p/2",
        nonlinear_native_version="use full extrinsic curvature of matched finite cell, not only local power slope",
        risk="finite-radius matching can alter the effective boundary scalar",
        next_test="compute K for full profile f(r), not only f=(R/r)^p",
    ),
    Approximation(
        name="S2 isotropic projection",
        current_linear_form="<n_a n_b> = delta_ab/3",
        nonlinear_native_version="integrate the actual boundary distribution of n_a induced by the cell",
        risk="boundary distribution may be anisotropic even though the metric measure is isotropic",
        next_test="derive or solve for the n_a distribution before averaging",
    ),
    Approximation(
        name="rank-one closure projectors",
        current_linear_form="independent P_i=|i><i| traces",
        nonlinear_native_version="full coupled boundary kernel on products of H1/projective variables",
        risk="independent traces may become correlated by nonlinear constraints",
        next_test="construct the full small-kernel and check whether it factorizes",
    ),
    Approximation(
        name="Hopf bridge",
        current_linear_form="CP1=S2 maps compact doublet to H1 direction",
        nonlinear_native_version="boundary action in phase-invariant bilinears z†sigma_a z with normalization constraints",
        risk="the measure/Jacobian on CP1 may contribute nontrivial weights",
        next_test="include Fubini-Study measure and compare with round S2 measure",
    ),
    Approximation(
        name="symmetric transfer",
        current_linear_form="one side carries eta/2",
        nonlinear_native_version="compose exact boundary kernels and inspect the gluing measure",
        risk="gluing may introduce determinant/Jacobian factors beyond exp(-eta/2)",
        next_test="derive transfer composition including boundary measure normalization",
    ),
    Approximation(
        name="branch coefficients",
        current_linear_form="finite-cell coefficient ratios reused from current ladder",
        nonlinear_native_version="derive coefficients from the same nonlinear boundary graph",
        risk="few-percent residuals may live in nonlinear coefficient normalization",
        next_test="stop treating residuals until coefficients are recomputed in the typed graph",
    ),
]


def main() -> None:
    print("Linearization/approximation risk audit")
    print("=" * 39)
    print("Current results may be a correct skeleton but still miss nonlinear")
    print("metric behavior. Do not patch residuals before testing these.")
    print()
    for item in APPROXIMATIONS:
        print(item.name)
        print(f"  current form:   {item.current_linear_form}")
        print(f"  nonlinear form: {item.nonlinear_native_version}")
        print(f"  risk:           {item.risk}")
        print(f"  next test:      {item.next_test}")
    print()
    print("Audit verdict:")
    print("  The few-percent mass residuals should not yet be interpreted as")
    print("  missing physical mechanisms. They may be artifacts of linearized")
    print("  boundary kernels, asymptotic endpoint forms, or simplified measures.")


if __name__ == "__main__":
    main()
