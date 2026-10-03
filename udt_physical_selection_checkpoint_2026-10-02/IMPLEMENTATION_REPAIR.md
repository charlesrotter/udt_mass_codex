# PSC1 exact saved-jet checker repair

The first parent symbolic/original-tensor job passed42 identities. The separate
stdlib saved-jet checker then failed with residual243/50000000 on the cubic
completion. The initial code and failed receipt remain fixed. This is an
implementation coefficient error, not a changed candidate, tolerance or data.

For a=1+c3 t³+c4 t⁴+c5 t⁵+..., direct proper-time geometry gives

    R=36c3 t+72c4 t²+120c5 t³+O(t⁴),
    [t³]F=240alpha c5+15552beta c3 c4.

The spatial equation's linear coefficient is therefore
-1440alpha c5-93312beta c3c4-12c3. The stdlib checker uses half of that coefficient:
-720alpha c5-46656beta c3c4-6c3. Its original hand-transcribed cross coefficient
77760 was wrong. Replace only77760 with46656 in the separately preserved
recompute_saved_jets_repaired.py. No science/check threshold is changed.

The exact initial failure and repaired run have different receipt names. Candidate
review must independently verify this expansion and assess the repair rather than
treat a successful rerun as independent scientific acceptance. The initial proof,
symbolic script, saved coefficients and all prior scope limits are unchanged.
