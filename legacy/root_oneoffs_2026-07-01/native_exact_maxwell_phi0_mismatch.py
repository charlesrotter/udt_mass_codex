from dataclasses import dataclass


@dataclass(frozen=True)
class Sector:
    name: str
    exact_metric_fact: str
    can_supply_delta_pi: str
    stress_signature: str
    verdict: str


SECTORS = [
    Sector(
        name="static radial Maxwell/Coulomb",
        exact_metric_fact="sqrt(-g) g^rr g^tt is phi-independent, giving flat Coulomb equation",
        can_supply_delta_pi="not as a localized phi0 shell unless a surface charge layer is added",
        stress_signature="bulk radial electric/magnetic stress, not angular-only trace-reversed shell",
        verdict="real metric-given force, wrong carrier for eta-producing phi0 jump",
    ),
    Sector(
        name="surface charge sheet at phi0",
        exact_metric_fact="would create Maxwell field discontinuity by Gauss law",
        can_supply_delta_pi="only if coupled to f boundary momentum by an additional rule",
        stress_signature="electromagnetic surface source, not derived from C1 alone",
        verdict="would be an added charged shell, not currently native",
    ),
    Sector(
        name="H1 angular/interface boundary",
        exact_metric_fact="round S2 projection and C1 boundary momentum share the phi0 collar",
        can_supply_delta_pi="target: must carry C1 momentum jump q/2",
        stress_signature="angular/interface trace-reversed signature",
        verdict="still the correct target, not replaced by Maxwell",
    ),
]


def main() -> None:
    print("Exact Maxwell / phi0 mismatch audit")
    print("=" * 38)
    print("Purpose: prevent the real abelian force from being mistaken for")
    print("the eta-producing phi0 boundary mechanism.")
    print()
    for sector in SECTORS:
        print(sector.name)
        print(f"  exact metric fact: {sector.exact_metric_fact}")
        print(f"  can supply DeltaPi: {sector.can_supply_delta_pi}")
        print(f"  stress signature:   {sector.stress_signature}")
        print(f"  verdict:            {sector.verdict}")
        print()

    print("No-invention verdict:")
    print("  Maxwell/Coulomb remains a real metric-given sector, but it does not")
    print("  automatically supply the C1 phi0 momentum jump. Treat it as a possible")
    print("  later orchestra instrument, not the derived boundary mechanism.")


if __name__ == "__main__":
    main()
