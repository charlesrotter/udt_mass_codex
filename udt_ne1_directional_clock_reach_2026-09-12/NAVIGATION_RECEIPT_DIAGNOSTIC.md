# Preserved receipt-assembly diagnostic

At21:19:59UTC the first parent navigation receipt assembly ended with actual
AssertionError at line6 before writing the receipt. The failing expression
was `assert sorted(changed)==allowed`, where changed was the subset of
SOURCE_PINS.json whose current hashes differ. The allowed five pointer paths
were CURRENT_RESEARCH_PROGRAM, HANDOFF, INDEX, LIVE and UDT_RESEARCH_ROADMAP.
The tracked diff matched those five exactly, so its preceding assertion passed.

SOURCE_PINS has23 entries and does not include INDEX.md. Its actually changed
subset contains four paths, not five. No unexpected source or registry change
occurred. The failed command made no mutations and wrote no partial receipt.
This was a bookkeeping defect in the new receipt, not a failed scientific,
full398 or navigation execution; those actual captures remain intact.

Smallest repair: authenticate all23 pins against their baseline Git blobs;
expect exactly the four pinned current-pointer changes and19 unchanged pins;
independently authenticate INDEX's old/current bytes using its baseline blob;
retain the exact five-path tracked-diff scope. The repaired receipt records
both the initial passing navigation run and the later editorial-navigation
run. No test assertion, scientific claim, source pin or tolerance is relaxed.
