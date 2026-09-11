"""Reuse this review's unchanged-code runner for the separately frozen addendum."""
from pathlib import Path
out=Path(__file__).resolve().parent
source=(out/'run_replays.py').read_text()
for old,new in [('REPLAY_PLAN.json','METROLOGY_REPLAY_PLAN.json'),
                ('REPLAY_RESULTS.json','METROLOGY_REPLAY_RESULTS.json'),
                ("'replay_'","'replay_added_'")]:
    expected=2 if old=='REPLAY_PLAN.json' else 1
    assert source.count(old)==expected,(old,source.count(old))
    source=source.replace(old,new)
exec(compile(source,str(out/'run_replays.py'),'exec'),
     {'__name__':'__main__','__file__':str(out/'run_replays.py')})
