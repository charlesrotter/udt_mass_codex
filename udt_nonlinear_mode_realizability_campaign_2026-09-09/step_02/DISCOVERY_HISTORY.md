# NR2 pre-review discovery history

The first full spatial-coordinate check ran successfully before proof freeze;
initial_checks.* is retained with its original 30-predicate output. Its script
then gained four explicit Bianchi contractions before the frozen candidate.
pre_bianchi_check.py is a reconstruction of the old script by removing only the block beginning
`# Contract Bianchi at an arbitrary slice-normal spatial-coordinate anchor.`
and ending immediately before the final print. Its reconstructed status is
explicit: no pre-run hash of that old source was saved, and chronology is not
certified by its later hash. No original output was replaced.
The original check semantics and exact output remain visible, not independently
reviewed at that earlier state. A later frozen-code rerun is separately captured.

Two notation clarifications were made to the proof before freeze, without changing
its argument: `M_epsilon|0=2H, V_epsilon|0=-Hdot` and the analogous s/kappa line
were made explicit as partial epsilon derivatives; the divergence in equation8
was written `div_gamma(D^sharp)` instead of `D^i D_i` with a prose warning that
it was divergence, not a squared norm. These are disclosed pre-freeze edits,
not a correction requested by a reviewer. Initial candidate freeze follows them.
