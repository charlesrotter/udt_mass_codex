# Pre-freeze reviewer output-serialization failure

The first independent child completed its mathematical assertions but exited1
while JSON-serializing SymPy Zero objects. The traceback and empty stdout remain
source_first.stderr/.stdout with the actual capture record. The exact original
script is preserved here. Fix only: add default=str to json.dumps. No equation,
assertion, domain, resource ceiling or scientific conclusion changed. This is
a reviewer pre-freeze implementation correction, not an author repair cycle.
The corrected run must execute every check again under a fresh output prefix.
