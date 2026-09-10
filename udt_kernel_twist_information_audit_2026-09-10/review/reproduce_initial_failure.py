#!/usr/bin/env python3
"""Execute preserved initial bytes using their original logical path; never alter files."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]
original=p/'checks/INITIAL_check_candidate.py'
logical=p/'check_candidate.py'
exec(compile(original.read_text(),str(logical),'exec'),{'__file__':str(logical),'__name__':'__main__'})
