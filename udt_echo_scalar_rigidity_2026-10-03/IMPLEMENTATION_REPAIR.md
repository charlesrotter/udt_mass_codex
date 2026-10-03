# Exact-expression comparison repair

The initial captured script failed on Python structural equality between
factorized expressions. The finite diagnostic shows `-T²(b−14)/8` and
`T²(14−b)/8` have distinct expression trees but zero exact expanded difference;
the wrong Qsecond=12 retains residual T²/4. The original run/script/freeze stay
unchanged. The repaired check compares exact expanded polynomial differences
with zero at three equivalent symbolic assertions. No equation, control case,
tolerance, numerical algorithm or scientific candidate changes. Its full run
must verify the actual original p/q residual and all original-incidence cases;
the diagnostic alone does not certify them. This is the second parent control
script and the included same-premise implementation repair. The one-case
captured diagnostic belongs to this repair, not an additional search.
