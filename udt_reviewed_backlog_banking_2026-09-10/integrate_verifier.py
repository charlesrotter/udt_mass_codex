"""Apply the narrow additive-bank adapter to the frozen baseline verifier once."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
p=ROOT/'verify_current_scientific_premises.py'
s=p.read_text()
if 'REVIEWED_BACKLOG_BANKING_IDS =' in s:
    raise SystemExit('Adapter already installed; inspect changes instead of reapplying.')
ledger=json.loads((HERE/'BANKED_CLAIMS.json').read_text())
ids=tuple(x['premise_id'] for x in ledger['claims'])
count=365+len(ids)
pins={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest()
      for x in [HERE/'BANKED_ROWS.tsv',HERE/'BANKED_CLAIMS.json',HERE/'BANKING_RECORD.md',
                HERE/'SOURCE_EVIDENCE_SHA256SUMS',HERE/'DISPOSITIONS.tsv']}
constants='''
# Exact owner-authorized backlog additions. Original365 rows are preserved verbatim.
REVIEWED_BACKLOG_BANKING_IDS = %r
REVIEWED_BACKLOG_PREFIXES = tuple(f"{item}\\t".encode() for item in REVIEWED_BACKLOG_BANKING_IDS)
REVIEWED_BACKLOG_BASELINE = "f5faabb43a582fec9a71c1d4a3b065efffae25bd"
REVIEWED_BACKLOG_BASE_SHA256 = %r
REVIEWED_BACKLOG_BANKING_SOURCE = "udt_reviewed_backlog_banking_2026-09-10/BANKING_RECORD.md"
REVIEWED_BACKLOG_PINS = %r
REVIEWED_BACKLOG_GUARD_FILES = tuple(REVIEWED_BACKLOG_PINS)
CURRENT_REGISTRY_ROW_COUNT = %d

''' % (ids,ledger['baseline_registry_sha256'],pins,count)
s=s.replace('PREMISE_REGISTRY_CONTROLS = (',constants+'PREMISE_REGISTRY_CONTROLS = (',1)
s=s.replace('dict.fromkeys(NEIGHBORING_TIDAL_BANKING_IDS +',
            'dict.fromkeys(REVIEWED_BACKLOG_BANKING_IDS + NEIGHBORING_TIDAL_BANKING_IDS +',1)
# Existing historical validators still authenticate their complete old-row projections.
s=s.replace(' + NEIGHBORING_TIDAL_BANKING_IDS',' + NEIGHBORING_TIDAL_BANKING_IDS + REVIEWED_BACKLOG_BANKING_IDS')
# The previous replacement also touches the explicit replay prefix just added; de-duplicate it.
s=s.replace('REVIEWED_BACKLOG_BANKING_IDS + NEIGHBORING_TIDAL_BANKING_IDS + REVIEWED_BACKLOG_BANKING_IDS +',
            'REVIEWED_BACKLOG_BANKING_IDS + NEIGHBORING_TIDAL_BANKING_IDS +')
s=s.replace('not in NEIGHBORING_TIDAL_BANKING_IDS]',
            'not in NEIGHBORING_TIDAL_BANKING_IDS + REVIEWED_BACKLOG_BANKING_IDS]')
a=s.index('def validate_neighboring_tidal_banking(');b=s.index('def validate_startup_surface(',a)
old=s[a:b]
old=old.replace('for item in NEIGHBORING_TIDAL_BANKING_IDS)',
                'for item in NEIGHBORING_TIDAL_BANKING_IDS + REVIEWED_BACKLOG_BANKING_IDS)',1)
old=old.replace('rows = read_tsv(root / "CURRENT_SCIENTIFIC_PREMISES.tsv")',
                'rows = [row for row in read_tsv(root / "CURRENT_SCIENTIFIC_PREMISES.tsv")\n'
                '            if row["premise_id"] not in REVIEWED_BACKLOG_BANKING_IDS]',1)
s=s[:a]+old+s[b:]
s=s.replace('line.startswith((b"G382\\t",',
            'line.startswith(REVIEWED_BACKLOG_PREFIXES + (b"G382\\t",')
validator='''def validate_reviewed_backlog_banking(root: Path, *, authenticate_sources: bool = True) -> None:
    """Authenticate exact accepted claims, categories, dependencies and immutable evidence.

    This is source/registry correspondence, not a scientific proof or new review.
    Whole pinned rows reject appended contradictions as well as missing scope.
    """
    payloads = {}
    for relative, expected in REVIEWED_BACKLOG_PINS.items():
        target = root / relative
        require(target.is_file(), f"backlog guard file missing: {relative}")
        payload = target.read_bytes()
        require(hashlib.sha256(payload).hexdigest() == expected,
                f"backlog guard file changed: {relative}")
        payloads[relative] = payload
    package = Path(REVIEWED_BACKLOG_BANKING_SOURCE).parent
    claims = json.loads(payloads[str(package / "BANKED_CLAIMS.json")])["claims"]
    expected_rows = payloads[str(package / "BANKED_ROWS.tsv")].splitlines(keepends=True)
    raw = (root / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()
    lines = raw.splitlines(keepends=True)
    require(lines[:1] == expected_rows[:1], "backlog registry header changed")
    added = [line for line in lines if line.startswith(REVIEWED_BACKLOG_PREFIXES)]
    require(added == expected_rows[1:], "backlog exact rows/scope/order changed")
    require(lines[1:1+len(added)] == added, "backlog rows must precede original rows")
    original = b"".join(line for line in lines if not line.startswith(REVIEWED_BACKLOG_PREFIXES))
    require(hashlib.sha256(original).hexdigest() == REVIEWED_BACKLOG_BASE_SHA256,
            "backlog changed an original365 registry byte")
    rows = read_tsv(root / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    by_id = {row["premise_id"]:row for row in rows}
    require(len(rows) == len(by_id) == CURRENT_REGISTRY_ROW_COUNT,
            "backlog registry count/uniqueness changed")
    require(tuple(c["premise_id"] for c in claims) == REVIEWED_BACKLOG_BANKING_IDS,
            "backlog claim membership changed")
    accepted = set(by_id) - set(REVIEWED_BACKLOG_BANKING_IDS)
    for claim in claims:
        require(set(claim["required_registry_ids"]) <= accepted,
                f"backlog dependency order/closure changed: {claim['premise_id']}")
        row = by_id[claim["premise_id"]]
        require(row["current_status"] == claim["grade"] and row["epistemic_label"] == "MIXED",
                f"backlog evidence category changed: {claim['premise_id']}")
        require(row["controlling_source"] == REVIEWED_BACKLOG_BANKING_SOURCE,
                "backlog controlling source changed")
        accepted.add(claim["premise_id"])
    if not authenticate_sources:
        return
    entries = [line.split(maxsplit=1) for line in
               payloads[str(package / "SOURCE_EVIDENCE_SHA256SUMS")].decode().splitlines()]
    require(len(entries) == len({name for _,name in entries}), "backlog duplicate evidence path")
    for expected, relative in entries:
        path = Path(relative)
        require(not path.is_absolute() and ".." not in path.parts
                and re.fullmatch(r"[0-9a-f]{64}",expected) is not None,
                "backlog unsafe evidence path")
        target = root / path
        require(target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == expected,
                f"backlog original source evidence changed: {relative}")
    frozen = subprocess.run(["git", "show", f"{REVIEWED_BACKLOG_BASELINE}:CURRENT_SCIENTIFIC_PREMISES.tsv"],
                            cwd=ROOT, capture_output=True, timeout=15, check=False)
    require(frozen.returncode == 0 and frozen.stdout == original,
            "backlog does not reproduce authorized baseline registry")


'''
s=s.replace('def validate_startup_surface(',validator+'def validate_startup_surface(',1)
s=s.replace('validate_neighboring_tidal_banking(root, authenticate_sources=False)',
            'validate_neighboring_tidal_banking(root, authenticate_sources=False)\n'
            '    validate_reviewed_backlog_banking(root, authenticate_sources=False)',1)
s=s.replace('    validate_neighboring_tidal_banking(ROOT)\n',
            '    validate_neighboring_tidal_banking(ROOT)\n    validate_reviewed_backlog_banking(ROOT)\n',1)
s=s.replace('len(registry_rows) == 365','len(registry_rows) == CURRENT_REGISTRY_ROW_COUNT')
s=s.replace('len({row["premise_id"] for row in registry_rows}) == 365',
            'len({row["premise_id"] for row in registry_rows}) == CURRENT_REGISTRY_ROW_COUNT')
a=s.index('def main()');s=s[:a]+s[a:].replace('len(rows) == 365','len(rows) == CURRENT_REGISTRY_ROW_COUNT',1).replace('len(by_id) == 365','len(by_id) == CURRENT_REGISTRY_ROW_COUNT',1)
s=s.replace('exactly 365 rows',f'exactly {count} rows').replace('365-row',f'{count}-row')
for anchor,stop in [('    live_next =','    handoff_next_parts'),('    handoff_next =','    # Completed ranges')]:
    a=s.index(anchor);b=s.index(stop,a);block=s[a:b]
    block=block.replace('"G381=NT1", "G382=NT2"','"G383--G412", "G411=LC2", "G412=FW2"')
    s=s[:a]+block+s[b:]
s=s.replace('realizations, free profiles and preserved false-pass/LOST-source caveats; no physical identification"',
            'realizations, free profiles and preserved false-pass/LOST-source caveats; no physical identification; "\n'
            '        "PASS: G383--G412 reviewed backlog:27 conditional mathematical results, one design control, "\n'
            '        "one published-summary benchmark and one finite procedure result; all original365 rows "\n'
            '        "and frozen source evidence preserved; no physical adoption or canon"')
p.write_text(s)
print('Installed narrow additive verifier adapter:',count,'rows;',len(ids),'new entries.')
