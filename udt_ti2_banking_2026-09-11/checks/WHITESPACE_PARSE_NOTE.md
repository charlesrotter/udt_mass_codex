# Metadata parser correction

The first parent staging-whitespace parser mistook the printed offending source line
+tests/test_startup_surface.py:1202: for another warning filename, and failed its
allowed-artifact assertion before writing a result JSON. The actual raw stdout/stderr
were already preserved. The corrected parser matches warning paths against actual
staged names and identifies two raw evidence files; the apparent +tests path is printed
context, not a staged path. The unchanged command reproduced byte-identical warnings.
The scoped source formatting check passed. No source or raw evidence was reformatted.
This is parent-owned late publication metadata, not a new scientific or fidelity claim.
