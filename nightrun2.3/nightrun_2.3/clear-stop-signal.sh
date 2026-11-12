#!/usr/bin/env bash
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)/common.sh"
if [[ -f "$NR_DIR/STOP_AFTER_CURRENT_IMAGE.txt" ]]; then
    rm -- "$NR_DIR/STOP_AFTER_CURRENT_IMAGE.txt"
    echo 'Stop signal cleared.'
else
    echo 'No stop signal to clear.'
fi
