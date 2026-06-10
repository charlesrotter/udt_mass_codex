from dataclasses import dataclass


@dataclass(frozen=True)
class TestResult:
    test: str
    interface_local: str
    warped_dtn: str
    implication: str


TESTS = [
    TestResult(
        "data required",
        "uses only phi0 value, C1 momentum jump, H1 projector, induced S2 measure",
        "requires finite extension through the negative-phi collar",
        "interface branch is boundary-local; warped branch is bulk-propagating",
    ),
    TestResult(
        "eta/2 origin",
        "uses projected finite-cell C1 action value once",
        "risks adding a second on-shell collar propagation factor on top of C1 action",
        "warped branch must prove it replaces, not multiplies, the C1 side action",
    ),
    TestResult(
        "gluing",
        "internal phi0 label is contracted directly by boundary symplectic gluing",
        "gluing is through a bulk DtN extension operator",
        "both are possible, but they describe different operations",
    ),
    TestResult(
        "profile sensitivity",
        "depends on q and induced boundary geometry at phi0",
        "depends on the full collar profile through Bessel ratio",
        "if particle transfer is interface-local, profile memory is extra data",
    ),
    TestResult(
        "composition",
        "one-side action eta/2 composes to eta under symmetric gluing",
        "DtN composition uses bulk extension kernels and determinant/normalization data",
        "simple gamma requires interface composition; warped propagation needs its own measure",
    ),
]


def main() -> None:
    print("interface vs warped double-count test")
    print("=" * 40)
    for result in TESTS:
        print(result.test)
        print(f"  interface-local: {result.interface_local}")
        print(f"  warped DtN:      {result.warped_dtn}")
        print(f"  implication:     {result.implication}")
        print()

    print("Test verdict:")
    print("  The interface-local branch currently passes the gamma-transfer test")
    print("  with fewer extra structures. The warped-DtN branch remains valid for")
    print("  bulk collar propagation, but using it in the transfer kernel must be")
    print("  a replacement for the intrinsic side action, not a multiplier.")


if __name__ == "__main__":
    main()
