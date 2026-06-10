import cmath
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class HopfSample:
    theta: float
    phi: float
    phase: float


def spinor(theta: float, phi: float) -> tuple[complex, complex]:
    # A normalized two-section coordinate for CP1 -> S2.
    return (
        math.cos(theta / 2.0) * cmath.exp(-0.5j * phi),
        math.sin(theta / 2.0) * cmath.exp(0.5j * phi),
    )


def apply_phase(z: tuple[complex, complex], phase: float) -> tuple[complex, complex]:
    u = cmath.exp(1j * phase)
    return (u * z[0], u * z[1])


def hopf_vector(z: tuple[complex, complex]) -> tuple[float, float, float]:
    a, b = z
    x = 2.0 * (a.conjugate() * b).real
    y = 2.0 * (a.conjugate() * b).imag
    z_axis = abs(a) ** 2 - abs(b) ** 2
    return (x, y, z_axis)


def norm2(v: tuple[float, float, float]) -> float:
    return sum(component * component for component in v)


def expected_s2(theta: float, phi: float) -> tuple[float, float, float]:
    return (
        math.sin(theta) * math.cos(phi),
        math.sin(theta) * math.sin(phi),
        math.cos(theta),
    )


def max_abs_diff(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return max(abs(x - y) for x, y in zip(a, b))


def main() -> None:
    print("M1 Hopf-to-H1 bridge audit")
    print("=" * 29)
    print("Primitive compact U(1) doublet data:")
    print("  z = (z1, z2) in C2")
    print("  normalize z†z=1")
    print("  quotient common compact phase z ~ exp(i alpha) z")
    print("  projective space CP1 is S2")
    print()
    print("Phase-invariant bilinears:")
    print("  X = 2 Re(z1* z2)")
    print("  Y = 2 Im(z1* z2)")
    print("  Z = |z1|^2 - |z2|^2")
    print("These satisfy X^2+Y^2+Z^2=1 for normalized z.")
    print()

    samples = [
        HopfSample(theta=0.3, phi=0.7, phase=1.2),
        HopfSample(theta=1.1, phi=2.4, phase=-0.9),
        HopfSample(theta=2.2, phi=-1.7, phase=0.4),
    ]
    for sample in samples:
        base = spinor(sample.theta, sample.phi)
        phased = apply_phase(base, sample.phase)
        v_base = hopf_vector(base)
        v_phased = hopf_vector(phased)
        v_expected = expected_s2(sample.theta, sample.phi)
        print(f"theta={sample.theta:.3f}, phi={sample.phi:.3f}, phase={sample.phase:.3f}")
        print(f"  Hopf vector={tuple(round(x, 9) for x in v_base)}")
        print(f"  norm^2={norm2(v_base):.12g}")
        print(f"  phase-invariance error={max_abs_diff(v_base, v_phased):.3g}")
        print(f"  S2 coordinate error={max_abs_diff(v_base, v_expected):.3g}")

    print("\nBridge verdict:")
    print("  - The primitive compact doublet has a native projective map CP1 -> S2.")
    print("  - The three invariant bilinears are exactly S2 coordinate-vector data,")
    print("    i.e. the ell=1/H1 angular frame.")
    print("  - This gives a metric/topology bridge from M1 compact data to the")
    print("    common phi=0 H1 frame without importing Dirac Form T.")
    print("  - Remaining condition: the boundary action must use these projective")
    print("    bilinears as its shape-closure variables.")


if __name__ == "__main__":
    main()
