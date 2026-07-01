"""Interaction matrix for the current native mass-emergence orchestra."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    name: str
    role: str
    affects_m1: str
    affects_e1: str
    current_status: str


INSTRUMENTS = [
    Instrument(
        "negative-phi finite cell",
        "creates endpoint/boundary problem",
        "provides finite-action endpoint stage",
        "provides finite-action endpoint stage",
        "native metric behavior",
    ),
    Instrument(
        "ordinary S2 angular frame",
        "metric-derived identity transport",
        "not enough for compact bundle alone",
        "directly supports E1 frame transport",
        "derived for ordinary sectors",
    ),
    Instrument(
        "compact U(1) bundle",
        "primitive nontrivial anchor sector",
        "selects M1 if Pbundle0 admitted",
        "not used for E1",
        "minimal postulate Pbundle0",
    ),
    Instrument(
        "endpoint admissibility",
        "sector selection through p(lambda)",
        "allows M1 finite endpoint",
        "selects E1 via p=1/N",
        "partly derived, eta still postulated",
    ),
    Instrument(
        "boundary closure entropy",
        "large hierarchy scale",
        "depth 5 if epsilon-mediated independent constraints",
        "depth 7 if epsilon-mediated independent constraints",
        "leading hierarchy candidate",
    ),
    Instrument(
        "constraint correlations",
        "branch damping",
        "can lower M1/mu-like branch",
        "would lower E1/tau-like branch, undesirable",
        "possible M1 residual instrument only",
    ),
    Instrument(
        "angular determinant/RG",
        "small log correction candidate",
        "scheme-dependent; not assigned",
        "possible positive E1 correction if derived",
        "open; high overfit risk",
    ),
    Instrument(
        "electron anchor",
        "sets absolute scale",
        "anchors M1 ground branch",
        "sets E1 masses by ratios",
        "accepted input F",
    ),
]


def main() -> None:
    print("Native orchestra interaction matrix")
    print()
    for item in INSTRUMENTS:
        print(item.name)
        print(f"  role: {item.role}")
        print(f"  M1/electron-mu branch: {item.affects_m1}")
        print(f"  E1/tau branch: {item.affects_e1}")
        print(f"  status: {item.current_status}")
        print()
    print("verdict:")
    print("  M1 and E1 are not the same instrument played louder")
    print("  selection, scale, damping, and residual correction are distributed across different native pieces")


if __name__ == "__main__":
    main()
