#!/usr/bin/env bash
# Per-user Linux install; never needs sudo.
set -Eeuo pipefail
[[ "$(id -u)" -ne 0 ]] || { echo "Install as your desktop user, not root." >&2; exit 2; }
SRC="$(cd -- "$(dirname -- "$0")" && pwd -P)"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
BIN="$HOME/.local/bin"
APP="$DATA/nightrun-linux"
MENU="$DATA/applications"
ICON_DIR="$DATA/icons/hicolor/256x256/apps"
NO_DEPS=false
if [[ "${1:-}" == --no-deps ]]; then NO_DEPS=true; shift; fi
[[ $# -eq 0 ]] || { echo "Usage: bash install.sh [--no-deps]" >&2; exit 2; }
[[ -f "$SRC/nightrun.py" && -d "$SRC/modules" && -f "$SRC/nightrun" ]] || {
  echo "Run install.sh from the extracted Linux Native archive." >&2; exit 2;
}
for p in "$APP" "$BIN" "$MENU" "$ICON_DIR"; do
  [[ ! -L "$p" ]] || { echo "Refusing symlinked install directory: $p" >&2; exit 2; }
  mkdir -p -- "$p"
done
for folder in modules pools tools assets; do
  mkdir -p -- "$APP/$folder"
  cp -a -- "$SRC/$folder/." "$APP/$folder/"
done
for file in nightrun nightrun.py config.json requirements.txt README.md GUIDE.md; do
  cp -f -- "$SRC/$file" "$APP/$file"
done
chmod 755 "$APP/nightrun"
if [[ "$NO_DEPS" == false ]]; then
  command -v python3 >/dev/null 2>&1 || { echo "Python 3 missing." >&2; exit 2; }
  python3 -m venv "$APP/.venv" || {
    echo "Python venv unavailable; install python3-venv, or retry with --no-deps." >&2; exit 2;
  }
  echo "Installing the small Python dependencies into Nightrun's private venv..."
  "$APP/.venv/bin/python" -m pip install --disable-pip-version-check -r "$APP/requirements.txt"
fi
LINK="$BIN/nightrun-linux"
if [[ -e "$LINK" && ! -L "$LINK" ]]; then
  echo "Won't replace your existing file at $LINK; remove/rename it first." >&2
  exit 2
fi
ln -sfn -- "$APP/nightrun" "$LINK"
for name in nightrun nightrun-upscaler; do
  cp -f -- "$APP/assets/icons/$name.png" "$ICON_DIR/io.bluenochian.$name.png"
done

# .desktop Exec is *not* a shell. Double quote and escape the complete path.
escape_exec() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//\$/\\\$}"
  value="${value//\`/\\\`}"
  printf '"%s"' "$value"
}
EXEC="$(escape_exec "$LINK")"
cat >"$MENU/io.bluenochian.Nightrun.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Nightrun
Comment=Local Forge batch generation
Exec=$EXEC base
Icon=io.bluenochian.nightrun
Terminal=true
Categories=Graphics;Utility;
StartupNotify=false
EOF
cat >"$MENU/io.bluenochian.NightrunUpscaler.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Nightrun Metadata Upscaler
Comment=Replay and upscale saved images
Exec=$EXEC upscale
Icon=io.bluenochian.nightrun-upscaler
Terminal=true
Categories=Graphics;Utility;
StartupNotify=false
EOF
chmod 644 "$MENU"/io.bluenochian.Nightrun*.desktop
command -v update-desktop-database >/dev/null && update-desktop-database "$MENU" >/dev/null 2>&1 || true
echo "Installed Nightrun Linux Native at: $APP"
echo "Launcher: $LINK"
echo "First run: $LINK setup --repo '/path/to/Forge'"
echo "Your local settings will be kept in ${XDG_CONFIG_HOME:-$HOME/.config}/nightrun-linux/"
