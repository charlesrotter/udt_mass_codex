#!/usr/bin/env python3
"""Record R3 worker/checkpoint health without restarting or interpreting results."""

from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import subprocess


UNIT = "udt-r3-covariance-20260813.service"
CHECKPOINTS = Path("/tmp/udt_boss_r3_checkpoints_union")
LOG = CHECKPOINTS / "R3_MONITOR.jsonl"


def command(*args):
    return subprocess.run(args, text=True, capture_output=True, check=False)


def main() -> int:
    CHECKPOINTS.mkdir(parents=True, exist_ok=True)
    show = command(
        "systemctl", "--user", "show", UNIT,
        "--property=LoadState,ActiveState,SubState,Result,MainPID,ExecMainCode,ExecMainStatus,MemoryCurrent,CPUUsageNSec",
        "--no-pager",
    )
    props = {}
    for line in show.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            props[key] = value
    checkpoints = sorted(CHECKPOINTS.glob("R3_*.npz"))
    runlog = CHECKPOINTS / "R3_RUN.log"
    service_log = CHECKPOINTS / "R3_SERVICE.log"
    record = {
        "timestamp": dt.datetime.now().astimezone().isoformat(),
        "unit": UNIT,
        "checkpoint_count": len(checkpoints),
        "latest_checkpoint": checkpoints[-1].name if checkpoints else None,
        "latest_checkpoint_mtime": (
            dt.datetime.fromtimestamp(checkpoints[-1].stat().st_mtime).astimezone().isoformat()
            if checkpoints else None
        ),
        "run_log_mtime": (
            dt.datetime.fromtimestamp(runlog.stat().st_mtime).astimezone().isoformat()
            if runlog.exists() else None
        ),
        "service_log_mtime": (
            dt.datetime.fromtimestamp(service_log.stat().st_mtime).astimezone().isoformat()
            if service_log.exists() else None
        ),
        "unit_properties": props,
        "systemctl_returncode": show.returncode,
        "partial_temp_files": sorted(path.name for path in CHECKPOINTS.glob("*.tmp")),
    }
    completed = len(checkpoints) == 194 and (CHECKPOINTS / "R3_RUN.log").exists()
    active = props.get("ActiveState") == "active" and props.get("SubState") == "running"
    if completed:
        record["health"] = "COMPLETE_OR_ASSEMBLY_PENDING"
    elif active:
        record["health"] = "ACTIVE_INCOMPLETE"
    else:
        record["health"] = "ALERT_INACTIVE_INCOMPLETE"
    with LOG.open("a") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    print(json.dumps(record, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
