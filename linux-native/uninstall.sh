#!/usr/bin/env bash
# Keep personal settings and renders unless explicitly removed by the user.
set -Eeuo pipefail
[[ "$(id -u)" -ne 0 ]] || { echo "Uninstall as your desktop user, not root." >&2; exit 2; }
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
APP="$DATA/nightrun-linux"
LINK="$HOME/.local/bin/nightrun-linux"
if [[ -L "$LINK" && "$(readlink -- "$LINK")" == "$APP/nightrun" ]]; then
  rm -- "$LINK"
fi
rm -f -- "$DATA/applications/io.bluenochian.Nightrun.desktop"
rm -f -- "$DATA/applications/io.bluenochian.NightrunUpscaler.desktop"
rm -f -- "$DATA/icons/hicolor/256x256/apps/io.bluenochian.nightrun.png"
rm -f -- "$DATA/icons/hicolor/256x256/apps/io.bluenochian.nightrun-upscaler.png"
if [[ -f "$APP/nightrun" && -d "$APP/modules" && "$APP" == */nightrun-linux ]]; then
  rm -rf -- "$APP"
fi
echo "Removed the Linux Native application."
echo "Your config (${XDG_CONFIG_HOME:-$HOME/.config}/nightrun-linux), logs, and Forge renders were left alone."
