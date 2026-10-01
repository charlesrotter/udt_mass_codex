"""Import adapter to fixed TPP1 TT construction; no scientific function is copied."""
import importlib.util
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[1]/'udt_time_live_production_preparation_2026-10-01/initial_family.py'
_spec=importlib.util.spec_from_file_location('tps1_fixed_tpp_initial_family',SOURCE)
_module=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_module)
construct=_module.construct
tt_tensor=_module.tt_tensor
