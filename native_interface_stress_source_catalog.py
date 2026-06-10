from dataclasses import dataclass


@dataclass(frozen=True)
class StressCandidate:
    name: str
    mixed_pattern: tuple[str, str, str]
    native_status: str
    match_quality: str
    caution: str


CANDIDATES = [
    StressCandidate(
        name="required phi0 jump bracket",
        mixed_pattern=("0", "-q/2", "-q/2"),
        native_status="metric-derived from nonzero inner q and flat exterior",
        match_quality="target signature",
        caution="overall Israel sign convention omitted; zero t-component is robust in this setup",
    ),
    StressCandidate(
        name="ordinary surface tension/domain wall",
        mixed_pattern=("nonzero", "nonzero", "nonzero"),
        native_status="generic shell matter, not specifically metric-derived",
        match_quality="poor: usually includes energy density/time component",
        caution="would be an imported wall unless derived as a UDT boundary term",
    ),
    StressCandidate(
        name="static angular gradient field on shell",
        mixed_pattern=("energy", "anisotropic angular", "anisotropic angular"),
        native_status="angular variables are native; stress form depends on action",
        match_quality="partial: angular support, but generally has energy density and anisotropy",
        caution="needs averaging/subtraction to match isotropic no-time target",
    ),
    StressCandidate(
        name="round-S2 curvature/boundary functional",
        mixed_pattern=("0 or topological", "isotropic angular", "isotropic angular"),
        native_status="plausible metric boundary term on the interface",
        match_quality="best structural match",
        caution="must be derived from the variational principle, not appended",
    ),
    StressCandidate(
        name="trace-subtracted H1 boundary kernel",
        mixed_pattern=("0", "isotropic angular", "isotropic angular"),
        native_status="compatible with earlier trace-preserving H1 projection",
        match_quality="good if kernel is a constraint stress, not material energy",
        caution="must show why energy-density part is constrained/subtracted",
    ),
    StressCandidate(
        name="radial Coulomb/Maxwell tail",
        mixed_pattern=("radial/electric energy", "radial pressure", "angular pressure"),
        native_status="abelian force is metric-native, but radial flux is singular",
        match_quality="poor for phi0 angular shell target",
        caution="not the carrier of this interface signature",
    ),
]


def main() -> None:
    print("Interface stress-source catalog")
    print("=" * 31)
    print("Target from metric jump, in shell directions (t, theta, phi):")
    print("  [K^a_b] - delta^a_b[K] = (0, -q/2, -q/2)")
    print()
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  pattern:       {candidate.mixed_pattern}")
        print(f"  native status: {candidate.native_status}")
        print(f"  match quality: {candidate.match_quality}")
        print(f"  caution:       {candidate.caution}")
        print()

    print("Catalog verdict:")
    print("  - The phi0 layer looks more like a metric boundary/corner constraint")
    print("    or trace-subtracted angular interface kernel than ordinary shell matter.")
    print("  - A naive angular field or surface tension would usually add a time/energy")
    print("    component that the target signature does not show.")
    print("  - The next derivation should come from the boundary variational principle,")
    print("    not from adding a material wall force.")


if __name__ == "__main__":
    main()
