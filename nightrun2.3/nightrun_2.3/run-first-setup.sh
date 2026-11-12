#!/usr/bin/env bash
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)/common.sh"
nr_python
cd -- "$NR_DIR"
printf 'Nightrun setup — configure paths, checkpoint and GPU settings.\n'
"$NR_PYTHON" "$NR_DIR/modules/setup_pipeline.py" "$@"
echo 'Next: run-validation-stress-test.sh, then run-one-dry-test.sh.'
