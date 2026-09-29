# Direct mathematical check freeze

Candidate read: INITIAL_CANDIDATE.md SHA256 600c261ec1662d8a8315034ef362f78563e7c8a193a2ca8fecad2d119ea46d52.
Author checks/code/output not yet read. General supplied Lorentz2 coordinate
metric, smooth T,L>0, arbitrary smooth b; both future null orientations.
Independently derive coordinate Christoffels, transform the resulting connection
to the orthonormal frame, compute scalar curvature by contracted coordinate
Riemann tensor, and compute frequency derivative using the affine geodesic
coordinate equation. Compare with candidate Cartan formulas only after these
objects are built. Check diagonal reciprocal specialization and actual flat
control, plus exact Lie brackets used by the smooth-character argument.
Exact symbolic arithmetic, CPU-only, SymPy already installed, one computational
thread, 60s/512MiB via existing run_capture.py; no grids, physical fit or source
admission. Save failures; stop or narrow if limits are exhausted. Mathematical
proofs still own general scope and global/domain assertions. These are controls
for supplied geometries, not selected native UDT physical histories.
