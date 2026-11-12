#!/usr/bin/env bash
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)/common.sh"
touch -- "$NR_DIR/STOP_AFTER_CURRENT_IMAGE.txt"
echo 'Stop requested. The current image can finish before the batch exits.'
