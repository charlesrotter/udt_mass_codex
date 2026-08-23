# G233 replay-interface preregistration

Date: 2026-08-23

The production and independent scripts currently write their registered JSON outputs beside the
scripts. Before assembling the review package, add only:

- `--no-write`, which prints the same JSON without persistent output;
- `--output PATH`, which changes only the destination when writing is enabled.

No equation, test value, expected result, check, or landing may change. The interface repair passes
only if no-write stdout parses to byte-equivalent JSON content with the already registered outputs.
