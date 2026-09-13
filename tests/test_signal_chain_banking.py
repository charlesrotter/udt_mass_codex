"""Hostile new-bank boundaries; reused historical validators must fail on poison."""
from pathlib import Path
import shutil
import pytest
import signal_chain_banking_guard as guard
import verify_current_scientific_premises as historical
REPO=Path(__file__).resolve().parents[1]

def fixture(root):
    for name in (*guard.SIGNAL_CHAIN_GUARD_FILES,'CURRENT_SCIENTIFIC_PREMISES.tsv'):
        target=root/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(REPO/name,target)
    return root

def test_whole_source_and_current_correspondence():
    guard.validate_signal_chain_banking(REPO)

@pytest.mark.parametrize('ident',guard.SIGNAL_CHAIN_BANKING_IDS)
@pytest.mark.parametrize('field',range(9))
def test_every_added_field_authenticated(tmp_path,ident,field):
    root=fixture(tmp_path);p=root/'CURRENT_SCIENTIFIC_PREMISES.tsv'
    lines=p.read_bytes().splitlines(keepends=True)
    i=next(i for i,r in enumerate(lines) if r.startswith((ident+'\t').encode()))
    fields=lines[i].rstrip(b'\n').split(b'\t');fields[field]+=b' PHYSICAL_LAW_ADOPTED'
    lines[i]=b'\t'.join(fields)+b'\n';p.write_bytes(b''.join(lines))
    with pytest.raises(SystemExit,match='SIGNAL'):
        guard.validate_signal_chain_banking(root,authenticate_sources=False)

@pytest.mark.parametrize('mode',['absent','partial','duplicate','replace_id','reorder','header','old_row'])
def test_membership_and_original_bytes(tmp_path,mode):
    root=fixture(tmp_path);p=root/'CURRENT_SCIENTIFIC_PREMISES.tsv';lines=p.read_bytes().splitlines(keepends=True)
    if mode=='absent': lines=[r for r in lines if not r.startswith(guard.SIGNAL_CHAIN_PREFIXES)]
    elif mode=='partial': lines.pop(1)
    elif mode=='duplicate': lines.insert(1,lines[1])
    elif mode=='replace_id': lines[1]=lines[2]
    elif mode=='reorder': lines[1],lines[2]=lines[2],lines[1]
    elif mode=='header': lines[0]=lines[0].replace(b'term',b'wrong_term')
    else:
        i=next(i for i,r in enumerate(lines) if r.startswith(b'G312\t'));lines[i]+=b'POISON\n'
    p.write_bytes(b''.join(lines))
    with pytest.raises(SystemExit,match='SIGNAL'):
        guard.validate_signal_chain_banking(root,authenticate_sources=False)

@pytest.mark.parametrize('name',guard.SIGNAL_CHAIN_GUARD_FILES)
def test_immutable_acceptance_poison(tmp_path,name):
    root=fixture(tmp_path);p=root/name;p.write_bytes(p.read_bytes()+b'\nUPGRADE')
    with pytest.raises(SystemExit,match='SIGNAL guard file changed'):
        guard.validate_signal_chain_banking(root,authenticate_sources=False)

@pytest.mark.parametrize('name',[
'udt_ne1_tilted_beam_geometry_2026-09-12/INITIAL_CANDIDATE.md',
'udt_redshift_distance_readiness_2026-09-12/SOURCE_PRESERVING_CLARIFICATION.md',
'udt_conditional_signal_sequence_2026-09-12/step_03/REPAIR_CONTRACT.md',
'udt_conditional_signal_sequence_2026-09-12/review_evolving/DIRECT_REVIEW.md'])
def test_source_history_poison(monkeypatch,name):
    original=Path.read_bytes;seen=[]
    def read(path):
        raw=original(path)
        if path==REPO/name: seen.append(path);return raw+b'FORGED'
        return raw
    monkeypatch.setattr(Path,'read_bytes',read)
    with pytest.raises(SystemExit,match='SIGNAL original source evidence changed'):
        guard.validate_signal_chain_banking(REPO)
    assert seen

VALIDATORS=['validate_signal_chain_banking','validate_ncb1_banking','validate_ti2_banking','validate_ti1_banking','validate_reviewed_backlog_banking','validate_conditional_banking','validate_shared_constraint_banking','validate_persistence_banking','validate_restrictiveness_banking','validate_source_metric_banking','validate_reconstruction_banking','validate_coupled_banking','validate_vacuum_scale_banking','validate_berger_banking','validate_closed_fibre_banking','validate_neighboring_tidal_banking']
@pytest.mark.parametrize('name',VALIDATORS)
def test_every_historical_guard_rejects_first_snapshot_poison(monkeypatch,name):
    original=Path.read_bytes;seen=[]
    def read(path):
        raw=original(path)
        if path==REPO/'CURRENT_SCIENTIFIC_PREMISES.tsv':
            seen.append(path)
            return raw.replace(b'G421\trepeated_',b'G421\tFALSE_') if len(seen)==1 else raw
        return raw
    monkeypatch.setattr(Path,'read_bytes',read)
    with pytest.raises(SystemExit,match='SIGNAL exact row/scope changed'):
        getattr(historical,name)(REPO,authenticate_sources=False)
    assert len(seen)==1

@pytest.mark.parametrize('name',VALIDATORS)
def test_one_registry_snapshot_no_substitute(monkeypatch,name):
    original=Path.read_bytes;seen=[]
    def read(path):
        raw=original(path)
        if path==REPO/'CURRENT_SCIENTIFIC_PREMISES.tsv':
            seen.append(path)
            if len(seen)>1: return raw.replace(b'G416\t',b'FORGED\t')
        return raw
    monkeypatch.setattr(Path,'read_bytes',read)
    getattr(historical,name)(REPO,authenticate_sources=False)
    assert len(seen)==1

def test_historical_absence_preserves_other_bytes_but_current_requires_all():
    raw=(REPO/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
    old=guard.without_signal_chain(raw,required=True)
    assert guard.without_signal_chain(old)==old
    with pytest.raises(SystemExit,match='SIGNAL current rows missing'):
        guard.without_signal_chain(old,required=True)
    poisoned=raw.replace(b'G312\t',b'G312_CHANGED\t')
    assert b'G312_CHANGED\t' in guard.without_signal_chain(poisoned)
