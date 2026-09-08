# SM2 pre-review check repair — original evidence retained

01:50UTC initial captured run exited1 at second_stabilizer_constraint.
Original script check_tensor.py SHA256
652b67bd0b09057e0d9c43269857bd1484d3aced8c5d848547ae9b71ea845620
and author_checks_initial.stdout/.stderr/.json remain unchanged. The failing
assertion compared expanded t*v+t*z with factored t*(v+z) using structural
SymPy equality. The mathematical difference is identically zero; this is a
false negative of the check, not a refuted stabilizer identity.

Grouped same-premise repair before review, in check_tensor_repaired.py:

- compare the stabilizer difference after simplification with zero;
- similarly fix a later expanded-versus-factored transport check (not reached
  in the original failed run; no second observed failure is claimed);
- instantiate the varying-A mutation as actual A(n)=n^2 rather than use a
  formal unknown-function derivative as a nonidentity guard.

Candidate mathematics unchanged. Repaired script SHA256
3c4591000db6a2f673c6328b4778ca940fd9a3e82057c53031e8b3dc4589015d.
Captured run01:51UTC exit0,14/14 exact anchors. stdout SHA256
740d00e11cb8a1eb619227531d2d60ca02f0855be40c78ac8f19a69920b617a3.
Both initial and repaired evidence sent to the fresh reviewer. Conservatively
count this as the step's one grouped repair allowance; direct fresh review
must check the repair as well as the general argument. No second repair
cycle is planned. Neither passing checks nor repair makes the claim accepted.
