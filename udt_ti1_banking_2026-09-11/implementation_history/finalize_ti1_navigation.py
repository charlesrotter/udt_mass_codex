from pathlib import Path
old='G383--G412 exact-scope banking is COMPLETE; G413=TI1 acceptance/integration underway; authorized evolution scope: INDEX.'
new='G383--G412 exact-scope banking is COMPLETE; G413=TI1 is conditionally banked; authorized evolution scope: INDEX.'
for name in ['LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md']:
 p=Path(name);s=p.read_text();assert old in s,name;p.write_text(s.replace(old,new))
for name in ['LIVE.md','CURRENT_SCIENTIFIC_PREMISES.md']:
 p=Path(name);s=p.read_text().replace('Exact-scope banking through G412 is COMPLETE','Exact-scope banking through G413 is COMPLETE');p.write_text(s)
p=Path('CURRENT_SCIENTIFIC_PREMISES.md');s=p.read_text().replace('Original365 rows, evidence, canon','Original395 rows, evidence, canon').replace('New prebank365 and full395 PASS; banking checks/review: INDEX.','New prebank395 and full396 PASS; banking checks/review: INDEX.');p.write_text(s)
p=Path('INDEX.md');s=p.read_text().replace('G383--G412 exact-scope banking COMPLETE; actual full395 PASS; scopes/reviews below.','G383--G412 exact-scope banking COMPLETE; G413 banked; full396 PASS; scopes/reviews below.').replace('Latest: `udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md`','Backlog: `udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md`');p.write_text(s)
p=Path('MEMORY.md');s=p.read_text().replace('Original365 rows/evidence remain unchanged. Banking checks/reviews: INDEX.','G413=TI1 conditional; original395 rows/evidence unchanged; checks/reviews: INDEX.');p.write_text(s)
p=Path('UDT_RESEARCH_ROADMAP.md');s=p.read_text().replace('Updated: 2026-09-10.','Updated: 2026-09-11.',1).replace('The campaigns described below are COMPLETE; their authorizations are spent, not live dispatches.','Earlier campaigns below are COMPLETE; the current bounded TI2 dispatch is identified at the maintained checkpoint.').replace('ER1 expansion and backlog banking. No later discovery campaign is automatically authorized.','ER1 expansion, backlog/G413 banking and the bounded TI2 evolution study. No successor is automatic.').replace('returns. The G383--G412 banking packet and maintained checkpoint own their later disposition;','returns. The G383--G412 and G413 banking packets and maintained checkpoint own later dispositions;')
s=s.replace('TI1 reviewed conditional two-shape comparison; UNPROMOTED','G413=TI1 conditionally banked at full reviewed scope').replace('TI1 proves datum-dependent local retention of nonzero curvature; broader study not dispatched','TI1 local retention banked; bounded TI2 initial-evolution comparison authorized')
old='''All original science is preserved. Charles then authorized TI1's bounded construction/check/review
cycle; it returned the reviewed conditional result without scientific repair. Its three-hour work
order closes at this return, with no automatic successor. TI1 disposition: HOLD for Charles's
separate exact-scope promotion authorization; controls remain controls. This is a named ownership
gate, not a requirement to identify physics before banking valid conditional mathematics.
`udt_two_shape_nonlinear_interaction_2026-09-11/DECISION_BRIEF.md` and `SESSION_RECORD.md`
own the lay return, actual checks, context/exposure record and preservation. Stop for discussion.'''
new='''All original science is preserved. Charles separately authorized exact-scope TI1 promotion:
G413 accepts both reviewed survivors, including full analytic-development/second-record-jet limits,
without scientific repair or equation adoption. `udt_ti1_banking_2026-09-11/BANKING_RECORD.md`
and its CLOSEOUT.md own the current acceptance, original395/whole-source preservation, fresh
integration review, repaired historical-projection guard and actual full396/check results.
The original TI1 UNPROMOTED headers remain historical. Controls remain controls.

Charles also authorized the bounded TI2 evolution comparison, including checks, fresh separate-context
review and bounded same-premise repair. `udt_ti1_banking_2026-09-11/WORK_ORDER.md` owns the scope;
`udt_two_shape_evolution_2026-09-11/FRAME_AND_DISCOVERY.md` freezes the comparison before output.
Combined banking/research hard return2026-09-11 16:00:50UTC, CPU only. Question: initial geometric
rate beyond its matched small-amplitude reference, with phase/completion controls and lawful retained
records. Return a reviewed conditional candidate, cancellation/freedom or precise obstacle; TI2
promotion is not authorized. No new physical premise or automatic successor. Stop for lay discussion
at this return. Backup completeness/pre-reboot unsaved state remain UNVERIFIED.'''
assert old in s;s=s.replace(old,new);p.write_text(s)
