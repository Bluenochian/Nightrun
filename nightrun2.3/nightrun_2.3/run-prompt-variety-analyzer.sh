#!/usr/bin/env bash
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)/common.sh"
nr_python
ROOT="${1:-$NR_REPO/test-renders}"
if [[ $# -gt 0 ]]; then shift; fi
cd -- "$NR_REPO"
"$NR_PYTHON" "$NR_DIR/tools/analyze_prompt_history.py" "$ROOT" --report "$NR_DIR/prompt_variety_report.json" "$@"
