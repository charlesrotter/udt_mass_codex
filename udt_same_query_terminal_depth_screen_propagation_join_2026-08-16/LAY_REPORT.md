# Lay report — the screen and the depth now use the same tape

This closes one more loose connection, conditionally but exactly.

G108 showed that the changing angular-screen area is calculated by the evolving geometry, but its
formula still used a supplied reciprocal-depth coordinate. The terminal pair metric was already
calculating that coordinate. On one continuous, consistently calibrated observer-pair tape, the
depth between two positions is simply the change in the tape's own reciprocal reading:

```text
pair depth = later phi_pair - earlier phi_pair.
```

So the screen-volume rate and the reciprocal depth no longer come from separate knobs. The same
complete pair relation supplies both.

The condition matters. If we splice together two independently calibrated tapes, we must carry the
calibration change at the splice. If `phi_pair` temporarily stops changing, it still labels the
endpoints but cannot serve as the local distance-like parameter at that point. And none of this
chooses which complete history or observer query Nature realizes.

In the orchestra metaphor: the conductor's distance marker and the screen instrument are now read
from the same score. We still have not derived which score the universe selects.
