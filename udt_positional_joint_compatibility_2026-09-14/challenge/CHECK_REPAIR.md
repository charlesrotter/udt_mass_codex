# Source-inventory metadata repair

The early independent source-pin check matched all 19 entries then present in
the parent's SOURCE_PINS.json. Before `check_sources.py` captured its saved
result, the parent expanded that inventory to 34 entries. The saved check
matched all 34 with no mismatches and empty stderr.

The challenger's final packaging check contained the stale assertion
`s['original_pins_checked']==19 and not s['original_pin_mismatches']` and failed
with `AssertionError`, exit 1. The failed assertion concerned inventory count,
not scientific algebra, source drift or a failed source hash. RECORD.json was
repaired to distinguish `early_source_pins_matched=19` from
`saved_source_pins_matched=34`. The final package check reads the actual saved
count rather than imposing the obsolete value. The source assessment and all
scientific formulas remain unchanged.
