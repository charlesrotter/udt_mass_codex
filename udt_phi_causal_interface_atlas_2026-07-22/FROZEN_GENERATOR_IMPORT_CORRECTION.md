# Frozen-generator import correction

The first post-adversarial verifier run stopped before a verdict because the dynamically loaded
frozen generator defines a dataclass and its module had not been inserted into `sys.modules`.

The correction inserts the exact import specification name and module into `sys.modules` before
executing that already-frozen source. This is standard Python import-loader bookkeeping. It changes
no generator byte, probe point, expected sign, interval certificate, tolerance, or conclusion.
