#!/usr/bin/env bash
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)/common.sh"
nr_config
nr_python
META="${1:-}"
if [[ -z "$META" ]]; then
    read -r -p 'Metadata JSON path: ' META
fi
META="${META%\"}"
META="${META#\"}"
[[ -f "$META" ]] || { printf 'Nightrun: metadata file not found: %s\n' "$META" >&2; exit 2; }
if [[ $# -gt 0 ]]; then shift; fi
SCALE="2"
if [[ $# -gt 0 && "$1" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    SCALE="$1"
    shift
fi
cd -- "$NR_REPO"
"$NR_PYTHON" "$NR_DIR/modules/upscale_from_metadata.py" "$META" --config "$NR_CONFIG" --scale "$SCALE" "$@"
