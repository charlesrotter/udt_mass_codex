"""Replay the preserved probe with bounded Git and a new isolated fixture."""

import pathlib
import sys

review = pathlib.Path(__file__).resolve().parent
source = (review / "probe_candidate.py").read_text()
assert len(sys.argv) == 2, "supply a fresh fixture basename"
assert sys.argv[1].isidentifier(), "plain review-local fixture basename required"
source = source.replace('REVIEW / "probe_fixture_initial"', 'REVIEW / ' + repr(sys.argv[1]))
source = source.replace('["git", "diff"', '["git", "-c", "core.preloadIndex=false", "-c", "index.threads=1", "diff"')
source = source.replace('["git", "show"', '["git", "-c", "pack.threads=1", "-c", "core.packedGitWindowSize=16m", "-c", "core.packedGitLimit=64m", "show"')
exec(compile(source, str(review / "probe_candidate.py"), "exec"))
