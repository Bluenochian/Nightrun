#!/usr/bin/env bash
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)/common.sh"
nr_config
printf 'Nightrun: validate | config: %s\n' "$NR_CONFIG"
nr_run "$NR_DIR/nightrun.py" --mode validate --count 100 --config "$NR_CONFIG" "$@"
