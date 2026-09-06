"""Deliberately defective scratch child for a capture-runner semantics probe."""
import sys
if '--mutation' not in sys.argv:
    raise AssertionError('INTENTIONAL_BASELINE_FAILURE_FOR_CAPTURE_ONLY_PROBE')
print('INTENTIONAL_UNCAUGHT_MUTANT_FOR_CAPTURE_ONLY_PROBE')
