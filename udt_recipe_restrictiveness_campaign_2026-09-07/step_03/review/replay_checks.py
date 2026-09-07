"""Check actual saved replay outcomes and serial execution intervals."""
import datetime
import json
from pathlib import Path

review=Path(__file__).resolve().parent
step=review.parent
pairs=[('replay_author','serial_author',0,None),
       ('replay_nonharmonic','serial_mutant_harmonicity',1,'original_exact_Ricci'),
       ('replay_fixed_phase','serial_mutant_fixed_phase',1,'fixed_phase_matching_not_automatic')]
out=[]
previous_end=None
for fresh,old,code,guard in pairs:
    record=json.loads((review/(fresh+'.json')).read_text())
    data=json.loads((review/(fresh+'.stdout')).read_text())
    assert record['returncode']==code and not record['timeout']
    assert record['address_space_bytes']==512*1024**2 and record['cpu_seconds']==60
    assert data.get('failed')==guard
    assert data['status']==('PASS' if code==0 else 'FAIL')
    for suffix in ('.stdout','.stderr'):
        assert (review/(fresh+suffix)).read_bytes()==(step/(old+suffix)).read_bytes()
    started=datetime.datetime.fromisoformat(record['started_utc']).timestamp()
    assert previous_end is None or started>previous_end
    previous_end=started+record['duration_seconds']
    out.append({'run':fresh,'exit':code,'failed_guard':guard,'duration_seconds':record['duration_seconds'],
        'maxrss_kib':record['maxrss_kib'],'stdout_stderr':'BYTE_IDENTICAL_TO_FROZEN_SERIAL'})
print(json.dumps({'status':'PASS','strict_serial_capture_intervals':True,'actual_replays':out},indent=2))
