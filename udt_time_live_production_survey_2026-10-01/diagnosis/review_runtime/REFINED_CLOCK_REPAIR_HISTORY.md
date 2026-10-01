# Reviewed-field input join repair

The mathematical source reviewer found that the first refined-clock adapter
authenticated a field-review report and an assembly separately without joining
the exact reviewed late history to the exact clock input. A mutually edited
history and assembly could therefore evade that incomplete relationship even
though the field-review bytes themselves stayed fixed.

The original source, freeze, dispatch and author-side controls are retained under
`initial_refined_clock/`; no refined clock query ran with that edition. The bounded
repair requires canonical `review_math/REPAIR_MATH.json` covering exactly 26 hashed
case reports, with original-equation PASS. Every new history and assembly must
match its reviewed window-2 binding. Each of the 13 original anchors is likewise
joined to its hashed original case report. Original and repaired refinement grades
remain separate; this change adds no query, threshold, equation, or physical premise.

New negative controls must exhibit the formerly missing relationship: a history
and assembly changed together while the reviewed field report stays fixed must
be rejected. Source review and operation checks will bind the repaired edition
before execution. The initial controls remain truthful about their narrower
coverage and do not count as having tested this new relation.
