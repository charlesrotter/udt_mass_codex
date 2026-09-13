# NAP1 R1 — trace-response witness precision

The fresh reviewer identified one quantifier ambiguity in INITIAL_CANDIDATE §5:
nonzero c2 with S=0 does not make EVERY G301 representative E nonzero.
The exact expression is E=-3(a+4b)c2 eta. The tracefree representative a+4b=0
has E=0 even for nonzero c2. To witness that DDR permits a nonzero trace response,
choose the allowed comparison representative a=1,b=0 and c2!=0, giving E=-3c2 eta.
This is an algebraic counterexample to replacing DDR by E=0, not a response adoption.

Smallest same-premise repair: qualify that example; no equation or scientific
landing changes. The initial candidate remains byte-preserved. Parent exact code
already tests the specific a=1,b=0,c2=1 witness, independent of this wording repair.
REVIEWED_RESULT and the decision brief use the corrected formulation. Reviewer
repair acceptance is recorded separately; this note does not self-certify it.
