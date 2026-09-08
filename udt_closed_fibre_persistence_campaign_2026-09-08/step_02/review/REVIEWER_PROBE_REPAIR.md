# Reviewer-only post-exposure harness repair

The initial aggregate post_exposure_check run exited 1 after 28.736358 seconds,
no timeout, maxRSS 73236 KiB. Its original source is preserved as
post_exposure_check_initial_failed.py and its original capture/empty stdout/
traceback remain post_exposure_check.{json,stdout,stderr}.

The finite plan tried to delete the f and f' terms of dRic while retaining
f''. SymPy xreplace recursively replaced f inside the unprotected f'' node,
so it also erased the principal jet. The author suite rejected that broader
mutation. The review aggregate incorrectly asserted a predicted false pass
before emitting its buffered evidence and therefore ended with an assertion.
Its intermediate in-memory outputs were not saved; they are not claimed as
preserved original streams. This evidence-capture limitation stays disclosed.

The corrected mutation explicitly maps f'' to itself before the f/f' deletions,
which protects the higher derivative node from recursive replacement. The
original overbroad mutation is separately re-executed and preserved in the
corrected aggregate, clearly labeled replay. An exception hook now emits any
partial buffered evidence before a future harness failure. Original files and
the sealed source-first work remain unchanged. No author source or scientific
argument is repaired and no author repair/re-review cycle is consumed.
