# G161 repair record

Date: 2026-08-18

## R1 — quotient side and domain

The preliminary audit summary incorrectly wrote `GL+(2)/SO+(1,1)`. The exact proof has a left
action, so the text now states the properly typed quotient

\[
SO^+(h)\backslash\mathcal D_h,
\qquad
\mathcal D_h=\{M\in GL^+(2):Me_0\text{ future timelike}\}.
\]

After a target orthonormal pair frame chooses `h=eta`, this becomes
`SO+(1,1)\D_eta`.

## R2 — independent section coverage

The original independent loop generated `M=boost x B+(2)`. It remains a useful exact live-jet
regression, but it built section existence into the witness.

The repaired verifier adds 700 raw integer matrices generated directly in matrix coordinates and
accepted only when:

- the clock column is future timelike;
- its Lorentz norm has an exact rational square root;
- `det M>0`.

The unique positive section is then reconstructed from those raw matrices with exact `Fraction`
arithmetic.

Fresh repair-only follow-up verdict: `FOLLOWUP_PASS`.
