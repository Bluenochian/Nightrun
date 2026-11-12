#!/usr/bin/env bash
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)/common.sh"
nr_config
nr_lock_runner
rm -f -- "$NR_DIR/STOP_AFTER_CURRENT_IMAGE.txt"
printf 'Nightrun: base | config: %s\n' "$NR_CONFIG"
nr_run "$NR_DIR/nightrun.py" --mode base  --config "$NR_CONFIG" "$@"
