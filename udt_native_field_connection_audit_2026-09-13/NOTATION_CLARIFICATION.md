# NFCA1 frozen parameter-notation correction

The fresh direct reviewer identified one documentary type error in the frozen
CANDIDATE_FREEZE parameters string: `J=(du+3dv/2,dx)` denotes covectors.
The correct supplied pair germ has TANGENT columns
`J=(partial_u+(3/2)partial_v,partial_x)`, represented by the4x2 matrix in
INITIAL_AUDIT and both actual implementations. Those sources were already
correct; no metric, germ, equation, code, parameter or scientific claim changes.

Keep CANDIDATE_FREEZE unchanged as the historical frozen record; this note
controls only that mistyped shorthand. The two-form notation du wedge dx
elsewhere correctly denotes covectors and is unaffected. This correction was
made after review identified the error, not disguised as original wording.
