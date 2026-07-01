from dataclasses import dataclass


@dataclass(frozen=True)
class SourceRole:
    name: str
    metric_location: str
    exact_job: str
    q_selection_power: str
    bridge_reading: str


ROLES = [
    SourceRole(
        name="interface delta source",
        metric_location="localized at phi=0 internalized-asymptotic boundary",
        exact_job="sets Pi_out-Pi_in=Delta Pi, allowing B_out=0 while q_in survives",
        q_selection_power="none by itself; accepts whatever q_in is supplied",
        bridge_reading="tail-cancel / first-jet-transfer object",
    ),
    SourceRole(
        name="collar density source",
        metric_location="distributed through the negative-phi collar linking S2s",
        exact_job="enters dq/dt=q^2-q+2s(t), controlling whether q runs",
        q_selection_power="can select q=1/3 if s=1/9 or s(q)=q/3 is native",
        bridge_reading="first-jet-admissibility / source-inventory object",
    ),
    SourceRole(
        name="angular boundary projector",
        metric_location="scale-invariant S2 data at phi=0",
        exact_job="removes scalar tail as macro imprint and keeps admissible angular imprint",
        q_selection_power="selects H1 after eta/q is supplied; does not select q alone",
        bridge_reading="macro-accessible angular carrier",
    ),
]


def main() -> None:
    print("internalized-asymptotic source split")
    print("=" * 40)
    for role in ROLES:
        print(role.name)
        print(f"  metric location:    {role.metric_location}")
        print(f"  exact job:          {role.exact_job}")
        print(f"  q selection power:  {role.q_selection_power}")
        print(f"  bridge reading:     {role.bridge_reading}")
        print()

    print("Source-inventory verdict:")
    print("  The phi=0 interface source and the collar source are different")
    print("  metric roles. The first explains how tail cancellation and first-jet")
    print("  survival coexist. The second is where q=1/3 must be selected if it")
    print("  is to be derived from the metric.")
    print()
    print("Next exact question:")
    print("  Does the scale-invariant angular sector live only at the phi=0")
    print("  interface, or is it transported through the negative-phi collar")
    print("  as a constant H1 source?")


if __name__ == "__main__":
    main()
