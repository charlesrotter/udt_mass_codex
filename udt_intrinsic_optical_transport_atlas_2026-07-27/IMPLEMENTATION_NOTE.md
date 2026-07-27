# Implementation note — SciPy underflow control

The first production launch stopped before completing or writing any path outcome because
`numpy.seterr(all="raise")` converted SciPy's harmless `nextafter` underflow probe into an exception.

The implementation was corrected to

```text
over=raise, divide=raise, invalid=raise, under=ignore.
```

No path, metric parameter, equation, tolerance, event, affine length, checkpoint, falsification
gate, or conclusion was changed.  The successful production run began only after this numerical
library compatibility correction.
