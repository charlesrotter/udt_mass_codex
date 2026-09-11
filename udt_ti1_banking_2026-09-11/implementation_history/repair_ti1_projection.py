from pathlib import Path
p=Path('verify_current_scientific_premises.py');t=p.read_text()
old='    raw = (root / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()\n    ddr = '
new='    raw = (root / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()\n    without_ti1(raw)  # Authenticate present G413 on this snapshot; retain every byte.\n    ddr = '
assert t.count(old)==1;t=t.replace(old,new)
old='            if source_key == "CURRENT_SCIENTIFIC_PREMISES.tsv":\n                lines = payload.splitlines(keepends=True)'
new='            if source_key == "CURRENT_SCIENTIFIC_PREMISES.tsv":\n                without_ti1(payload)  # Validate before the explicit removal loop.\n                lines = payload.splitlines(keepends=True)'
assert t.count(old)==1;t=t.replace(old,new)
old='registry_lines = (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes().splitlines(keepends=True)'
new='registry_lines = without_ti1((ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()).splitlines(keepends=True)'
assert t.count(old)==4;t=t.replace(old,new);p.write_text(t)
