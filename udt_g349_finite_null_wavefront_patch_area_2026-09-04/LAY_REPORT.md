# G349 lay report — from one infinitesimal ray to a finite patch

Date: 2026-09-04
Grade: `EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_R1_R4_REPAIRS`

## What we learned

G348 showed that the metric gives an exact tiny-area response for one narrow bundle of nearby null
paths. G349 shows how those tiny pieces combine across a whole supplied patch of directions.

The metric remains well behaved even when that patch folds over itself or passes through a caustic.
At a caustic, the local cross-sectional area can momentarily shrink to zero. The spacetime and the
complete ray evolution do not thereby become singular.

The external reviewer caught an important distinction. A direction-dependent endpoint cut can
make the map have two independent coordinate directions even when only one direction survives
across the physical transverse screen. The second coordinate direction can run along the null ray
itself and adds no physical cross-sectional area. The repaired result therefore counts transverse
screen directions, not ordinary coordinate rank. This preserves the area theorem and includes the
previously missed zero-area null sheet.

There are two honest finite areas:

1. **Sheet area:** count every arriving ray sheet. If two different starting directions land on the
   same region, count that region twice.
2. **Union area:** count the geometric region only once, however many sheets cover it.

The local metric formula integrates directly to sheet area. Union area additionally requires the
full global map so we can identify which directions reach the same endpoint. That is geometry, not
a new light or transfer law.

## What this does not yet provide

This does not say how much energy or brightness travels on a sheet, which paths are physically
populated, how a detector responds, or which area should be called an observational distance. It
also does not choose a metric history, physical scale, or `X_max`.

The independent repair-only reviewer rebuilt the tricky zero-area null-sheet example from scratch,
replayed every registered check, and accepted the repair without another defect.

So the advance is real but bounded: the metric now owns a finite, caustic-aware geometric area for
a supplied ray patch. The next layer will have to decide what physical information, if any, is
carried over that geometry.
