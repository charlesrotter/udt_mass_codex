# G346 preregistration execution note

Date: 2026-09-04
Preregistration commit: `9a037558`

The first production execution of the frozen formulas passed `11204/11204`. The first
implementation-distinct execution passed `4251/4251`. The first hostile-mutation execution caught
`20/20`. No formula, tolerance, alternative, physical question, or maximum conclusion was changed
after seeing these outcomes.

The result remains locally verified and bounded until fresh sealed external adversarial review.

The first aggregate package replay returned `18/19`. Its only failure asked the preregistration file
to contain the hash of the commit that was created by committing that file. A preregistration file
cannot contain the hash of its own future commit. The integrity check was corrected to require the
hash in the later audit and execution note, while Git proof will authenticate the preregistration
commit in the sealed intake. This packaging-only repair changed no formula, tolerance, alternative,
outcome, or scientific claim.
