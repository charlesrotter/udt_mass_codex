# Preserved reviewer construction failure

source_first_check.* is the initial failed reviewer execution, before seal or
author exposure. It failed the direct full-tensor comparison at6.457 seconds,
exit1, no timeout. The connection and its derivative were assembled inside one
loop, so derivative entries accessed later, still-zero connection entries.

Finite diagnosis: the admitted equations and fixed brackets were unchanged;
there was no numerical approximation, boundary solve or global field inference.
The dependency order is an implementation defect. The only repair separates
the two assembly loops. This is a reviewer pre-seal harness repair, not a
post-review scientific repair of an author candidate. Preserve the initial
streams and exact diff (one added for-loop declaration) alongside the corrected
source and subsequent result. The original program is reconstructible exactly
by removing that declaration at the connection-derivative pass.
