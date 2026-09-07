# TM1 independent source-first check plan

Reviewer context: /root/tidal_tm1_review, fresh separate context. Model UNKNOWN;
different-model, human-specialist and formal verification UNTESTED. Author TM1
candidate/proof/code/output/verdict not seen. Baseline 508eb238d1321a3bdce9a45eb47a97b63fb1b541.

Question: for fixed sensor positions in a rotating frame, what compensation
acceleration gradient corresponds to negative freely falling relative acceleration?
What scalar signal is indistinguishable from unconstrained sensor offsets?

Scope: local first-order spatial response and exact rotating-frame kinematics.
Use a second-order rotation jet to obtain inertial acceleration independently
of a prewritten gradient inversion formula. T is an arbitrary symmetric
negative-relative-acceleration matrix. This is a conditional engineering map,
not a device law derived from UDT. No zero-trace target or external gravity
model is supplied. Constant time-domain offset projection is a synthetic
operator only, not a claim about every actual GOCE processing implementation.

Choices: curvature sign/metric convention pinned by cited G358 source; sensor
orientation, positive baseline and compensation-force sign explicitly supplied;
symbolic variables free-and-explored. Neglect of finite baseline, residual proof
mass motion, electrostatic nonlinearity, self gravity, timing and metrology error
is a declared ideal restriction. Those errors remain eligibility obligations.

Checks: derive force difference from rotation jet and linear gravity, verify
symmetry/antisymmetry and trace, introduce opposite-sign/factor-two defects,
and prove scalar/bias alias and constant annihilation by centering. All are
exact symbolic/synthetic checks, not observations or numerical certification.

Resources: unchanged shared run_capture.py; one CPU child, 512 MiB address
space, 60 seconds CPU and wall; no GPU. Outputs only in this review directory.
Stop on failure and retain all streams. Maximum conclusion is the stated
conditional map and its exact synthetic identifiability limitations.
