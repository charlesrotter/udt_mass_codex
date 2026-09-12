"""Hostile checks for G413 correspondence and historical projection boundaries."""
from pathlib import Path
import shutil
import pytest
import ti1_banking_guard as guard

REPO = Path(__file__).resolve().parents[1]


def fixture(root):
    for name in (*guard.TI1_GUARD_FILES, "CURRENT_SCIENTIFIC_PREMISES.tsv"):
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if name == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            target.write_bytes(guard.without_ti2(guard.without_ncb1((REPO / name).read_bytes())))
        else:
            shutil.copy2(REPO / name, target)
    return root


def test_whole_source_and_current_registry_correspondence():
    guard.validate_ti1_banking(REPO)


@pytest.mark.parametrize("field", range(9))
def test_every_g413_field_is_exactly_authenticated(tmp_path, field):
    root = fixture(tmp_path)
    path = root / "CURRENT_SCIENTIFIC_PREMISES.tsv"
    lines = path.read_bytes().splitlines(keepends=True)
    fields = lines[1].rstrip(b"\n").split(b"\t")
    fields[field] += b" UNCONDITIONAL_PHYSICAL_LAW"
    lines[1] = b"\t".join(fields) + b"\n"
    path.write_bytes(b"".join(lines))
    with pytest.raises(SystemExit, match="TI1 (current row missing/duplicate|exact row/scope changed)"):
        guard.validate_ti1_banking(root, authenticate_sources=False)


@pytest.mark.parametrize("mode", ["missing", "duplicate", "reorder", "old_row", "header"])
def test_membership_order_and_original395_are_protected(tmp_path, mode):
    root = fixture(tmp_path)
    path = root / "CURRENT_SCIENTIFIC_PREMISES.tsv"
    lines = path.read_bytes().splitlines(keepends=True)
    if mode == "missing":
        lines.pop(1)
    elif mode == "duplicate":
        lines.insert(1, lines[1])
    elif mode == "reorder":
        lines[1], lines[2] = lines[2], lines[1]
    elif mode == "header":
        lines[0] = lines[0].replace(b"term", b"altered_term")
    else:
        i = next(i for i, line in enumerate(lines) if line.startswith(b"G312\t"))
        lines[i] = lines[i].replace(b"FILTER", b"DERIVED")
    path.write_bytes(b"".join(lines))
    with pytest.raises(SystemExit, match="TI1"):
        guard.validate_ti1_banking(root, authenticate_sources=False)


@pytest.mark.parametrize("name", guard.TI1_GUARD_FILES)
def test_acceptance_record_cannot_append_an_upgrade(tmp_path, name):
    root = fixture(tmp_path)
    path = root / name
    path.write_bytes(path.read_bytes() + b"\nPHYSICALLY_DERIVED\n")
    with pytest.raises(SystemExit, match="TI1 guard file changed"):
        guard.validate_ti1_banking(root, authenticate_sources=False)


@pytest.mark.parametrize("name", ["INITIAL_CANDIDATE.md", "review/REVIEW.md", "review/FINAL_FIDELITY.md"])
def test_original_science_review_and_history_poison_is_detected(monkeypatch, name):
    target = REPO / "udt_two_shape_nonlinear_interaction_2026-09-11" / name
    original = Path.read_bytes
    seen = []
    def read(path):
        raw = original(path)
        if path == target:
            seen.append(path)
            return raw + b"DISCARDED_LIMITS"
        return raw
    monkeypatch.setattr(Path, "read_bytes", read)
    with pytest.raises(SystemExit, match="TI1 original source evidence changed"):
        guard.validate_ti1_banking(REPO)
    assert seen


def test_projection_absence_is_only_for_historical_use_and_preserves_other_bytes():
    raw = (REPO / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()
    old = guard.without_ti1(raw, required=True)
    assert guard.without_ti1(old) == old
    with pytest.raises(SystemExit, match="TI1 current row missing"):
        guard.without_ti1(old, required=True)
    poisoned = raw.replace(b"G312\t", b"G312_CHANGED\t", 1)
    assert b"G312_CHANGED\t" in guard.without_ti1(poisoned)


def test_current_validation_uses_one_registry_snapshot(monkeypatch):
    target = REPO / "CURRENT_SCIENTIFIC_PREMISES.tsv"
    original = Path.read_bytes
    reads = []
    def read(path):
        raw = original(path)
        if path == target:
            reads.append(path)
            if len(reads) > 1:
                return raw.replace(b"G413\t", b"FORGED\t")
        return raw
    monkeypatch.setattr(Path, "read_bytes", read)
    guard.validate_ti1_banking(REPO, authenticate_sources=False)
    assert len(reads) == 1


@pytest.mark.parametrize("name", [
    "validate_conditional_banking", "validate_shared_constraint_banking",
    "validate_persistence_banking", "validate_restrictiveness_banking",
    "validate_source_metric_banking", "validate_reconstruction_banking",
    "validate_coupled_banking", "validate_vacuum_scale_banking",
    "validate_berger_banking", "validate_closed_fibre_banking",
    "validate_neighboring_tidal_banking", "validate_reviewed_backlog_banking",
])
def test_each_standalone_historical_guard_authenticates_before_ignoring_g413(monkeypatch, name):
    import verify_current_scientific_premises as historical
    original = Path.read_bytes
    target = REPO / "CURRENT_SCIENTIFIC_PREMISES.tsv"
    seen = []
    def read(path):
        raw = original(path)
        if path == target:
            seen.append(path)
            lines = raw.splitlines(keepends=True)
            i = next(i for i,line in enumerate(lines) if line.startswith(b"G413\t"))
            lines[i] = lines[i].replace(b"NOT_PHYSICAL_ADOPTION", b"PHYSICAL_LAW_ADOPTED", 1)
            return b"".join(lines)
        return raw
    monkeypatch.setattr(Path, "read_bytes", read)
    with pytest.raises(SystemExit, match="TI1 exact row/scope changed"):
        getattr(historical, name)(REPO, authenticate_sources=False)
    assert len(seen) == 1
