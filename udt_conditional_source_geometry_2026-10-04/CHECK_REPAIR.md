# CGE1 original-equation diagnostic and checker repair

The frozen initial checker failed its first spectral-drift comparison. Original
source INITIAL_CHECK.py, construction capture and a separately frozen diagnostic
run are preserved. Both returned exit1; no output is counted as a pass. The
first actual-arrival frequency error was 1.8787061e-11, while the drift discrepancy
was 0.0034964460, far above the unchanged 1e-7 criterion.

For arrival map A(tau_e)=tau_o, Z=A'. The optical slope (c_E=1) is dZ/dtau_o
=A''/A', not A''/(A')². The initial test had the latter denominator. Candidate
equation (6) and its ACP1-derived slope statement already use the correct chain
rule. Repair changes only that denominator in the test. Equations, candidate,
inputs, numerical precision, step sizes and tolerances are unchanged. This is
a meaningful caught checker error, not evidence against the candidate geometry
or an excuse to weaken the gate. Reviewers receive the failure and repair.

REPAIRED_CHECK_FREEZE.json is written before the repaired execution. The capture
utility retains exact commands, resource limits, stdout/stderr and return code.
