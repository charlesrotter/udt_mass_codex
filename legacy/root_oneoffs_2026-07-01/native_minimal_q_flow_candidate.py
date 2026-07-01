from dataclasses import dataclass


@dataclass(frozen=True)
class FlowPoint:
    q: float
    beta: float
    beta_prime: float


def beta(q: float, source_s: float) -> float:
    # Minimal autonomous flow whose fixed points reproduce
    # q(1-q)/2 = s. Sign/orientation is conventional until derived.
    return q * q - q + 2.0 * source_s


def beta_prime(q: float) -> float:
    return 2.0 * q - 1.0


def roots(source_s: float) -> tuple[float, float] | None:
    disc = 1.0 - 8.0 * source_s
    if disc < 0.0:
        return None
    root = disc**0.5
    return ((1.0 - root) / 2.0, (1.0 + root) / 2.0)


def main() -> None:
    print("Minimal q-flow candidate")
    print("=" * 24)
    print("Use a minimal autonomous beta function consistent with")
    print("the endpoint fixed-point relation:")
    print("  q(1-q)/2 = s")
    print()
    print("Candidate:")
    print("  dq/dtau = beta(q) = q^2 - q + 2s")
    print("where tau orientation must be derived from the full action.")
    print()

    for source_s in [0.0, 1.0 / 9.0, 1.0 / 8.0, 0.14]:
        print(f"s={source_s:.12g}")
        r = roots(source_s)
        if r is None:
            print("  no real fixed points")
            continue
        for q in r:
            bp = beta_prime(q)
            if bp < 0:
                stability_forward = "attractive for forward tau"
            elif bp > 0:
                stability_forward = "repulsive for forward tau"
            else:
                stability_forward = "marginal"
            print(f"  fixed q={q:.12g}")
            print(f"    beta={beta(q, source_s):+.3e}")
            print(f"    beta'={bp:+.12g}")
            print(f"    nominal stability={stability_forward}")

    print("\nFor s=1/9:")
    print("  fixed points are q=1/3 and q=2/3.")
    print("  q=1/3 is attractive or repulsive depending on radial-flow orientation.")
    print()
    print("Audit verdict:")
    print("  - The angular-source fixed-point relation naturally contains q=1/3.")
    print("  - Stability and collar inheritance cannot be decided without the")
    print("    correctly oriented q-flow from the full boundary action.")
    print("  - This is a promising nonlinear target, not a completed derivation.")


if __name__ == "__main__":
    main()
