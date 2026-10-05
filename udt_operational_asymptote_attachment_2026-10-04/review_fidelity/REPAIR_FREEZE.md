# Bounded numerical-domain repair, before rerun

The initial implementation stopped honestly at case13: the a=10,H=.01,E=1,
b_*=2 family at R=60 did not bracket an incidence root within the frozen
strict source interval. The twelve a=8 cases completed, with all79 performed
checks passing; overall run FAILED because of the uncompleted case. Initial
code, code seal, stdout/stderr and JSON are retained in initial_attempt/.

The solver-first protocol was read on this mismatch. Diagnosis: this is a
finite branch-coverage failure of the selected early reception, not failure
of the late-limit implicit-function argument. CPR1 explicitly supplies a
local late branch, not all early receptions or phases. The sign and original
incidence equations are unchanged. The receiver and ray-domain positivity
remain required. No failed branch is turned into a whole-theory nonexistence
claim or patched with a new observer/phase.

Bounded repair: retain the first family radii60,600,6000,60000, but check the
second family at600,6000,60000. Keep its fixed histories, all equations,
tolerances, precisions and stops unchanged. The first early second-family
reception remains unverified and is explicitly omitted. The new run uses
56 cases; combined with13 attempted initial cases, total69 remains below100.
No additional family or physical mechanism is introduced. Save a new code
seal before rerunning, and report initial failure beside the repaired result.
