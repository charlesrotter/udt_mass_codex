# What the kernel can retain when scalar clock depth is silent — KTI1

Status: VERIFIED-WITH-CAVEATS; CONDITIONAL, UNPROMOTED.
INITIAL_CANDIDATE.md and DATA_FREEZE.md control the exact mathematical scope.

## What we learned

In the twisting example from DCI1, the missing rotation information can survive outside
the scalar clock depth. The current completed pair metric retains a shift: a coefficient
describing how the chosen clock and ruler directions mix. With a supplied common labeling
and calibration of neighboring comparisons, the spatial variation of those shifts reveals
the twist, even though every scalar clock depth remains zero.

The precise extraction for this example is

    b = partial_x beta_y - partial_y beta_x,
    W = b^2/2.

W is the observer family's vorticity norm used in DCI1. These are transverse derivatives
across neighboring queries. Looking farther along one individual stationary pair strip
does not provide them. The common event labels, clock synchronization and ruler calibration
are supplied comparison data; the kernel does not generate or physically realize them.

This makes one previously missing data connection explicit. It does not establish physical
access to the records, reconstruct all curvature, or select a metric, history or physical law.

## The informative limits

| Retained records in the declared example | What follows |
|---|---|
| Scalar null-clock depths on each metric's own branches | All zero; paths and endpoint incidence maps are not asserted identical |
| Coordinate-pair matrices at the central event, including their time derivatives | Agree for zero and nonzero twist |
| Coordinate-pair shifts with matched spatial first derivatives | Determine b and W within this family and calibration |
| Orthogonal-pair matrices and adapted-frame V component arrays throughout the neighborhood | Can all agree while W differs; discarded ambient frame/germ variation matters |
| Full ambient coframe or coordinate germ fields with neighborhood derivatives | Retain the distinction as supplied input geometry, not recovered scalar-output information |

A nonzero shift at one point is not invariant rotation: even flat geometry can have a
nonzero shift after a changed synchronization/query choice. The antisymmetric spatial
variation above removes a common smooth synchronization gradient. The comparison carefully
distinguishes transforming the same germ from choosing a different germ after a coordinate
change. No shift of an original marked query is silently deleted.

Likewise, constant numerical direction components in each metric's own adapted frame do
not mean the ambient tangent fields or their transport agree. G182's common-coframe
condition is essential. The example does not show insufficiency of the complete E,J input.

## What is now open

The relevant next boundary is the ownership and availability of the comparison family:
which jointly marked pair records are supplied or justified, and what can actually be
obtained from them? This result does not choose that family as a physical protocol. It
does not prove that extra physical laws are required to supply the missing information.

The calculation uses G176/G179's completed scalar Phi=-log T and retained shift. The older
arbitrary-calibration scalar remains a control. Existing evaluator equations and source
grades are unchanged; this is an application of their information distinctions to DCI1's
specific geometry. It is not a new theorem of differential geometry or a whole-theory census.

## Evidence and return point

The author run passed 85 exact identity diagnostics and 11 wrong-formula controls. It reuses
existing G179 pullback and NCI1 coordinate-geometry utilities, disclosed as author regression.
An initial control used a matrix with the wrong shape and failed; its source/output were
preserved, the shape was corrected, and the next actual run passed. The mathematical
candidate did not change. The construction partner wrote separate code and passed 55 exact
checks; that is construction evidence, not the later fresh adversarial review.

Fresh separate-context adversarial review accepted the unchanged candidate and the brief's
scope. Before candidate/code exposure, the reviewer independently passed 88 identities and
18 executable mutation rejections, including direct metric vorticity and explicit immersions.
It also replayed the corrected author checks, rejected all 11 wrong formulas through the
actual author identity guard, checked guard failure modes, and reproduced the original
ShapeError from the preserved source. The exact repair changes only the zero-vector shape.
No scientific repair was required. Full evidence, exposure and omissions are in review/REVIEW.md.
Exact runtime model/version is UNATTESTED; fresh context and different implementation do not
establish different models. The original pending-review candidate remains preserved as history.
Full source pins, frozen comparison, outputs, exposure and discovery history are preserved.
No registry/canon/fixed-manuscript change or automatic successor is authorized. Backup
completeness/pre-reboot unsaved state remain UNVERIFIED; ScratchDisk is archive-only.
