#!/usr/bin/env bash
# Shared setup for Linux launchers. Keep this boring; it gets called at 2 AM.
set -Eeuo pipefail
export PYTHONUNBUFFERED=1 PYTHONIOENCODING=utf-8
NR_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
NR_DEFAULT_REPO="$(cd -- "$NR_DIR/../.." && pwd -P)"
NR_REPO="${NIGHTRUN_FORGE_REPO:-$NR_DEFAULT_REPO}"

nr_config() {
    NR_CONFIG="$NR_DIR/config.json"
    [[ -f "$NR_DIR/config.local.json" ]] && NR_CONFIG="$NR_DIR/config.local.json"
    if [[ ! -f "$NR_CONFIG" ]]; then
        printf 'Nightrun: config missing: %s\n' "$NR_CONFIG" >&2
        exit 2
    fi
}
nr_python() {
    if [[ -n "${NIGHTRUN_PYTHON:-}" ]]; then
        [[ -x "$NIGHTRUN_PYTHON" ]] || { echo "Nightrun: NIGHTRUN_PYTHON is not executable: $NIGHTRUN_PYTHON" >&2; exit 2; }
        NR_PYTHON="$NIGHTRUN_PYTHON"
    elif [[ -x "$NR_REPO/venv/bin/python" ]]; then
        NR_PYTHON="$NR_REPO/venv/bin/python"
    elif [[ -x "$NR_REPO/.venv/bin/python" ]]; then
        NR_PYTHON="$NR_REPO/.venv/bin/python"
    elif command -v python3 >/dev/null 2>&1; then
        NR_PYTHON="$(command -v python3)"
        printf 'Nightrun: Forge venv not found; using %s for the runner.\n' "$NR_PYTHON" >&2
    elif command -v python >/dev/null 2>&1; then
        NR_PYTHON="$(command -v python)"
        printf 'Nightrun: Forge venv not found; using %s for the runner.\n' "$NR_PYTHON" >&2
    else
        echo 'Nightrun: Python not found. Install Python 3 and requests.' >&2
        exit 2
    fi
}
nr_lock_runner() {
    command -v flock >/dev/null 2>&1 || { echo 'Nightrun: util-linux flock is required on Linux.' >&2; exit 2; }
    exec {NR_LOCK_FD}>"$NR_DIR/.nightrun.lock"
    if ! flock -n "$NR_LOCK_FD"; then
        echo 'Nightrun: another batch is running. Stop that one before launching a second.' >&2
        exit 3
    fi
}
nr_run() {
    nr_python
    cd -- "$NR_REPO"
    "$NR_PYTHON" "$@"
}
