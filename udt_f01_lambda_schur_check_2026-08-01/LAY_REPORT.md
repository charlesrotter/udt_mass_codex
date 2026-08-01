# F01 result in lay language

We inspected one conditional “building block” that had looked partly promising for stability.

Imagine checking whether a tabletop tips when every allowed leg can move. Earlier work had checked
most of the legs but left one global adjustment knob fixed. Under one edge rule the tabletop already
tilted. Under another edge rule it looked level.

This audit allowed the missing knob to move. The result is:

- in the first edge rule, the knob does not make the existing tilt worse;
- in the second edge rule, the knob recreates one tilt that the edge pin had hidden.

So both versions of this local conditional block still have one unstable direction. They get it in
different ways, which proves that the edge rule and the global adjustment cannot be audited
separately.

This is useful progress, but it is not a verdict against UDT matter or the stability hypothesis. The
tested block depends on a conditional response law, chosen normalization, supplied edge rules, and a
flat wall-response witness. The physical wall completion, complete chain, time evolution, native
action, carrier, and global bootstrap remain open.

The elegance note remains a hypothesis about a larger self-consistent structure. This calculation
does not confirm it; it prevents one incomplete local slice from being mistaken for that structure.
