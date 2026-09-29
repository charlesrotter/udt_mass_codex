# Source corrections found during reconstruction

## C1 — G310 boosted reciprocal shape tangent

Source: udt_g310_differential_dual_reciprocity_tracefree_ownership_2026-08-31/EXACT_DERIVATION.md,
section3, covector-basis boosted half-tangent formula. Source bytes are preserved.
For C²−S²=1, u'=Ce0+Sei, n'=Se0+Cei and a odot b=a tensor b+b tensor a,
expansion gives

    H(u',n')/2 − (C²+S²)H(e0,ei)/2 = +2CS(e0-flat odot ei-flat).

The source displays -2CS on that covector-basis right side. Its coordinate0i
entries are negative because e0-flat=(-1,0,0,0); this does not reverse the
coefficient multiplying the covector basis itself. The spatial formula fixes
the same unnormalized odot convention, so changing that convention cannot repair
just the boosted line.

The separate mathematical reviewer independently computed the tensor span and
annihilator from lowered vectors: rank9, annihilator span(g). The sign-corrected
nonzero directions give exactly the same span. Thus the formula needs correction;
the trace-free/trace-line conclusion survives the reconstructed proof. This is
not a blanket reproof of G310 or its descendants, nor a scientific grade change.

Impact: central R9 is corrected; R10 uses only the surviving annihilator, and
R11/R12 inherit the conditional Einstein branch with full current G312 limits.
Original response/source/branch records retain their grades and ownership. The
central dependency graph records the correction so later changes flag both
positive implications and negative restrictions. No original code or evidence
is rewritten to manufacture a historical pass.
