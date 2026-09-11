"""Update maintained navigation for proposed banking; preserve bounded startup size."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def replace(s,a,b):
    if a not in s:raise SystemExit('Missing navigation anchor: '+a[:100])
    return s.replace(a,b)

for name in ['AGENTS.md','LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md',
             'CURRENT_SCIENTIFIC_PREMISES.md','INDEX.md','MEMORY.md']:
    p=ROOT/name;s=p.read_text().replace('365-row','395-row')
    if name=='LIVE.md':
        a=s.index('Conditional mathematical banking through G382');b=s.index('### Distinctions',a)
        s=s[:a]+'''Banking through G382 is COMPLETE; G383--G412 integration is pending final checks/review.
The exact 395-row `CURRENT_SCIENTIFIC_PREMISES.tsv` owns grades; `INDEX.md` routes the banking draft.
Whole original reviews/limits control, including false passes/repairs, CF2 buffers LOST, not preserved
or recovered, and NT1 lost buffers/unsnapshotted reviewer code. Original365 rows remain unchanged.
G383--G394 cover the original curvature recipe, HB/BI and nonlinear/localized geometry.
G395--G401 cover conditional response, controlled correspondence, limits and realizable response jets.
G402--G405 cover null-clock integrability, curvature information and exact metric/kernel expansion.
G406--G410 cover conditional measurement/design mathematics; G409=CO2 is a design control.
G411=LC2 is one published-summary benchmark; G412=FW2 is one failed finite procedure.
No physical identification, instrument certification or native equation selection follows.
NE1 retains fading-profile/cumulative marked-area-rate/tidal departure in its exact polarized family;
supplied data/marking and conditional equation remain, without genericity or stability.
The fixed through-G352 manuscript remains an earlier edition. Actual banking checks/reviews: INDEX.

'''+s[b:]
    elif name=='HANDOFF.md':
        s=replace(s,'HB2/HB3 and BI2/BI3 remain UNPROMOTED. Fixed manuscript/coverage remains through G352, not the frontier.',
                  'G383--G412 backlog integration awaits final checks/review. Fixed manuscript/coverage stays through G352.')
        a=s.index('NR1--NR2/LG1--LG2/LE1/SE1/NE1:');b=s.index('Optional source branch',a)
        s=s[:a]+'''G383--G394: original recipe, HB/BI, nonlinear/localized geometry; G395--G401: response/correspondence.
G402--G405: null-clock/curvature/kernel expansion; G406--G410: conditional measurement/design math.
G409=CO2 design, G411=LC2 published benchmark, G412=FW2 finite procedure retain distinct categories.
All original365 rows and scientific evidence remain unchanged; banking draft/checks: INDEX.

'''+s[b:]
        s=replace(s,'dated handoff sequence. Capacity UNVERIFIED; old full365 PASS is prior evidence.',
                  'dated handoff sequence. General capacity UNVERIFIED; prior passes are historical evidence.')
    elif name=='CURRENT_RESEARCH_PROGRAM.md':
        s=replace(s,'Full365 PASS; maintenance evidence: INDEX. No scientific promotion.',
                  'G383--G412 banking draft/checks: INDEX; final integration pending.')
        s=replace(s,'HB2/HB3 and BI2/BI3 remain UNPROMOTED; G376 banked only the required BI1 predecessor.',
                  'G384--G387 bank HB2/HB3/BI2/BI3 conditionally; G376 remains BI1.')
        a=s.index('NR1--NR2/LG1--LG2/LE1/SE1/NE1:');b=s.index('Geometric theory/calibration',a)
        s=s[:a]+'''G383--G394: original curvature recipe, HB/BI and nonlinear/localized geometry.
G395--G401: conditional response/correspondence; G402--G405: null-clock/curvature/kernel expansion.
G406--G410: conditional measurement mathematics and G409=CO2 design control.
G411=LC2: published-summary benchmark; G412=FW2: failed finite procedure, not a metric constraint.
Whole original reviews/caveats control; roadmap: `UDT_RESEARCH_ROADMAP.md`.

'''+s[b:]
    elif name=='CURRENT_SCIENTIFIC_PREMISES.md':
        s=replace(s,'Banking through G382 is COMPLETE, VERIFIED-WITH-CAVEATS at reviewed conditional scopes.',
                  'Banking through G382 is COMPLETE; G383--G412 integration awaits final checks/review.')
        s=replace(s,'Full365 PASS after maintenance; no scientific promotion. Maintenance/review closeout: INDEX.',
                  'New prebank365 PASS; expanded banking checks/review: INDEX.')
        s=replace(s,'G376 banked only required BI1; HB2/HB3 and BI2/BI3 remain UNPROMOTED.',
                  'G376 remains BI1; G384--G387 conditionally bank HB2/HB3/BI2/BI3.')
        s=replace(s,'Response-foundations campaign complete: roadmap via INDEX; no scientific promotion. Backup completeness/pre-reboot unsaved state',
                  'G383--G412:27 conditional math results, CO2 design, LC2 benchmark and FW2 finite procedure; exact scopes: INDEX.\nBackup completeness/pre-reboot unsaved state')
        s=replace(s,'Exact grades, original evidence, canon and fixed manuscript are preserved.',
                  'Original365 rows, evidence, canon and fixed manuscript remain unchanged.')
    elif name=='INDEX.md':
        s=replace(s,'Banking through G382 is COMPLETE at reviewed conditional scopes; response-foundations campaign complete.',
                  'G383--G412 banking draft; final integration pending. Earlier banking through G382 COMPLETE.')
        s=replace(s,'Latest: `udt_exact_metric_kernel_expansion_2026-09-10/DECISION_BRIEF.md`; ER1 conditional UNPROMOTED.',
                  'Latest: `udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md`; exact claims/dispositions/checks there.')
        s=s.replace('Latest banking:','Prior banking:').replace('NE1 reviewed UNPROMOTED','G394=NE1 conditional').replace('SE1 reviewed UNPROMOTED','G393=SE1 conditional').replace('LE1 reviewed UNPROMOTED','G392=LE1 conditional').replace('LG1--LG2 UNPROMOTED','G390--G391 conditional').replace('NR1--NR2 UNPROMOTED','G388--G389 conditional').replace('HB2/HB3 unpromoted','G384/G385 conditional').replace('BI2/BI3 unpromoted','G386/G387 conditional')
        s=replace(s,'Full365 PASS; maintenance: `maintenance_guard_sweep_2026-09-10/WORK_RECORD.md`; no scientific promotion.',
                  'Prior maintenance: `maintenance_guard_sweep_2026-09-10/WORK_RECORD.md`; historical full365 PASS.')
    elif name=='MEMORY.md':
        s=replace(s,'HB2/HB3 and BI2/BI3 remain UNPROMOTED; three CD vacuous checks remain EXCLUDED.',
                  'G383--G412 backlog integration awaits final checks/review; three CD vacuous checks remain EXCLUDED.')
        s=replace(s,'NR/LG/LE1/SE1/NE1 are reviewed UNPROMOTED; INDEX owns full scopes/reviews, not stability/content.',
                  '27 conditional mathematical results plus CO2 design, LC2 benchmark and FW2 finite procedure; scopes: INDEX.')
        s=replace(s,'Full365 PASS after maintenance; evidence: INDEX. No new banking.',
                  'Original365 rows/evidence remain unchanged. Banking checks/reviews: INDEX.')
        s=replace(s,'ND1/ND2/QC1/QC2/GL1/GL2/RF1 reviewed UNPROMOTED; campaigns complete; roadmap via INDEX.',
                  'Roadmap closeouts record bank/hold/control dispositions; no automatic successor.')
    if name in ('LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md'):
        s=replace(s,'G381=NT1 and G382=NT2 conditional mathematical banking is COMPLETE at the reviewed scopes.',
                  'G383--G412 conditional mathematical banking and G411=LC2/G412=FW2 acceptance await final integration.\nEarlier G381=NT1/G382=NT2 banking is COMPLETE; scopes/reviews: INDEX.')
    p.write_text(s)

p=ROOT/'UDT_RESEARCH_ROADMAP.md';s=p.read_text()
s=replace(s,'its original baseline was', 'its original baseline was')
s=replace(s,'ER1 expansion and next discussion. No later campaign is automatically authorized.',
          'ER1 expansion and backlog banking. No later discovery campaign is automatically authorized.')
s=replace(s,'what was learned, limitations and the next justified decision. Do not replace it with dated status',
          'what was learned, limitations, next justified decision and each result\'s promotion disposition:\n'
          '**bank at demonstrated scope; hold for a named missing gate; or retain as control/exploration**.\n'
          'Conditional results need not wait for physical identification. Review is distinct from promotion.\n'
          'Do not replace this checkpoint with dated status')
s=replace(s,'| Exact metric/kernel, stages1–2 | ER1 contribution COMPLETE, reviewed VERIFIED-WITH-CAVEATS, UNPROMOTED |',
          '| Exact metric/kernel, stages1–2 | ER1 COMPLETE, reviewed; G405 exact-scope banking integration pending |')
s=replace(s,'its exact execution and final fidelity receipts are in that package. The two-hour authorization\nis spent at closeout; later stages and promotion remain separate decisions. Stop for discussion.',
          'its exact execution and final fidelity receipts are in that package. The two-hour research authorization\n'
          'is spent. Charles separately authorized the reviewed backlog banking:30 entries G383--G412,\n'
          'with source gates passed and final integration pending. `udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md`\n'
          'and `DISPOSITIONS.tsv` in that package own exact scopes, grades, checks and remaining gates.\n'
          'All original science is preserved. Later discovery stages remain separate decisions; stop for discussion.')
# Earlier campaign sections describe their actual historical return state, explicitly superseded here.
s=replace(s,'## Aim and current position',
          'Current acceptance overlay: earlier UNPROMOTED/campaign-only language below records historical\n'
          'returns. The G383--G412 banking packet and maintained checkpoint own their later disposition;\n'
          'original result packages remain unchanged. No physical adoption or canon is included.\n\n## Aim and current position')
p.write_text(s)
print('Updated bounded navigation draft and standing roadmap promotion disposition.')
