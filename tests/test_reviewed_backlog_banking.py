"""Adversarial acceptance/preservation guards for exact backlog banking."""
from pathlib import Path
import shutil
import pytest
import verify_current_scientific_premises as guard

REPO=Path(__file__).resolve().parents[1]

def copy_guard(tmp_path):
    for name in (*guard.REVIEWED_BACKLOG_GUARD_FILES,'CURRENT_SCIENTIFIC_PREMISES.tsv'):
        dest=tmp_path/name;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(REPO/name,dest)
    return tmp_path

def change_field(root,pid,field,value):
    p=root/'CURRENT_SCIENTIFIC_PREMISES.tsv';lines=p.read_text().splitlines(keepends=True)
    index=lines[0].rstrip('\n').split('\t').index(field)
    matches=[i for i,line in enumerate(lines) if line.startswith(pid+'\t')]
    assert len(matches)==1
    i=matches[0];row=lines[i].rstrip('\n').split('\t');row[index]=value
    lines[i]='\t'.join(row)+'\n';p.write_text(''.join(lines))

def test_backlog_exact_source_preservation():
    guard.validate_reviewed_backlog_banking(REPO)

@pytest.mark.parametrize('pid',guard.REVIEWED_BACKLOG_BANKING_IDS)
@pytest.mark.parametrize('field,value',[
    ('current_status','PHYSICAL_LAW_DERIVED'),
    ('active_use','UNRESTRICTED_GLOBAL_NATIVE_UDT_THEOREM'),
    ('open_scope','NO_REMAINING_CONDITIONS'),
    ('controlling_source','CANON.md'),
])
def test_every_added_row_rejects_grade_scope_or_source_corruption(tmp_path,pid,field,value):
    root=copy_guard(tmp_path);change_field(root,pid,field,value)
    with pytest.raises(SystemExit,match='backlog exact rows/scope/order changed'):
        guard.validate_reviewed_backlog_banking(root,authenticate_sources=False)

@pytest.mark.parametrize('pid',['G176','G312','G353','G382'])
def test_original_registry_bytes_remain_protected(tmp_path,pid):
    root=copy_guard(tmp_path);change_field(root,pid,'open_scope','DISCARDED_ORIGINAL_LIMITS')
    with pytest.raises(SystemExit,match='backlog changed an original365 registry byte'):
        guard.validate_reviewed_backlog_banking(root,authenticate_sources=False)

@pytest.mark.parametrize('mode',['missing','duplicate','reverse','historical_first'])
def test_added_membership_and_order(tmp_path,mode):
    root=copy_guard(tmp_path);p=root/'CURRENT_SCIENTIFIC_PREMISES.tsv';lines=p.read_bytes().splitlines(keepends=True)
    n=len(guard.REVIEWED_BACKLOG_BANKING_IDS)
    # Target the historical G383 block explicitly after authenticated G413.
    start=next(i for i,line in enumerate(lines) if line.startswith(b'G383\t'))
    if mode=='missing':lines.pop(start)
    elif mode=='duplicate':lines.insert(start,lines[start])
    elif mode=='reverse':lines[start:start+n]=reversed(lines[start:start+n])
    else:lines=lines[:start]+lines[start+n:]+lines[start:start+n]
    p.write_bytes(b''.join(lines))
    with pytest.raises(SystemExit,match='backlog (exact rows/scope/order changed|rows must precede original rows)'):
        guard.validate_reviewed_backlog_banking(root,authenticate_sources=False)

@pytest.mark.parametrize('relative',guard.REVIEWED_BACKLOG_GUARD_FILES)
def test_pinned_claim_record_and_history_reject_appended_contradiction(tmp_path,relative):
    root=copy_guard(tmp_path);p=root/relative
    p.write_bytes(p.read_bytes()+b'\nAPPENDED: ALL CONDITIONS ARE NOW PHYSICALLY DERIVED\n')
    with pytest.raises(SystemExit,match='backlog guard file changed'):
        guard.validate_reviewed_backlog_banking(root,authenticate_sources=False)

@pytest.mark.parametrize('relative',[
    'udt_exact_metric_kernel_expansion_2026-09-10/INITIAL_CANDIDATE.md',
    'udt_directional_clock_curvature_whiteboard_2026-09-10/checks/AUTHOR_01_EXCLUSION.json',
    'udt_gw170817_fixed_window_test_campaign_2026-09-07/step_02/evaluation_R1_run.stdout',
])
def test_original_source_or_exclusion_corruption_is_caught(monkeypatch,relative):
    target=REPO/relative;read=Path.read_bytes;seen=[]
    def poisoned(path):
        data=read(path)
        if path==target:
            seen.append(path);return data+b'CORRUPT'
        return data
    monkeypatch.setattr(Path,'read_bytes',poisoned)
    with pytest.raises(SystemExit,match='backlog original source evidence changed'):
        guard.validate_reviewed_backlog_banking(REPO)
    assert seen
