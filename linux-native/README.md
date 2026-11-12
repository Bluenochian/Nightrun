# Nightrun — Linux Native

This is the **separate Linux edition**, not a new Nightrun version number.
It runs the same maintained modular image-generation engine as the existing
2.3 build, but the package is Linux-only: no Windows batch launchers, no
Windows icon files, and no need to put it inside Forge's workflow directory.

I wanted a Linux release that acts like a Linux program rather than a Windows
ZIP wearing a shell script. So this one has XDG-aware user installation,
application menu entries, PNG icons, and one terminal command.

## Installation

Download **nightrun-linux-native.tar.gz** from the
[Linux Native release](https://github.com/Bluenochian/Nightrun/releases/tag/linux-native):

```bash
tar -xzf nightrun-linux-native.tar.gz
cd nightrun-linux
bash install.sh
```

The installer runs as **your desktop user**, without sudo. It creates a private
Python virtual environment and openly installs `requests` and `Pillow`.
You'll need Python 3 with `venv`, util-linux `flock`, and an internet
connection for first-time Python dependency installation. If dependencies are
already provided by the Python interpreter you want to use, run
`bash install.sh --no-deps` instead.

To connect your Forge installation:

```bash
~/.local/bin/nightrun-linux setup --repo "$HOME/Stable-Diffusion-Forge"
```

Or run `nightrun-linux setup` and enter the folder when prompted.
First setup detects your GPU, checkpoint and output paths. Your settings
live **outside the app folder** and remain intact when you reinstall.

Then try these in order:

```bash
nightrun-linux validate --count 100
nightrun-linux dry-run --count 5
nightrun-linux base --count 20
nightrun-linux full --count 20
nightrun-linux stop
```

`base` and `full` send real image-generation jobs to Forge's local API;
`validate` and `dry-run` don't. The application menu includes
**Nightrun** (base mode) and **Nightrun Metadata Upscaler**.

For an old render, use:

```bash
nightrun-linux upscale "/path to/0001_metadata.json" --scale 2
```

If Forge isn't already running, the app tries its own `launch.py --api`
using the **Forge virtual environment**, not an unrelated Python installation.
The Forge models, extensions and VRAM requirements remain yours to manage.

## Native Linux paths

| Item | Default |
| --- | --- |
| Installed app + isolated venv | `~/.local/share/nightrun-linux/` |
| Command | `~/.local/bin/nightrun-linux` |
| App menu entries | `~/.local/share/applications/` |
| Local configuration | `~/.config/nightrun-linux/config.local.json` |
| Stop signal, lock, setup report | `~/.local/state/nightrun-linux/` |
| Outputs and run logs | Your chosen Forge output directory |

Application, config and state respect `XDG_DATA_HOME`,
`XDG_CONFIG_HOME`, and `XDG_STATE_HOME`. Add
`$HOME/.local/bin` to your PATH if you want to use the command by
its short name from a terminal.

No root permissions or system-wide background services are required.

## Upgrades and uninstall

Run `bash install.sh` again from a newer Linux Native archive.
Your local configuration, output folder and previous renders are separate
from the installed code, so they aren't overwritten.

Uninstall with `bash uninstall.sh` from the archive. Personal config,
state and generated images are preserved. You can clean those manually if
you really want them gone.

## Compatibility and limits

This edition is **native Linux packaging**, not a new rendering engine.
NVIDIA temperature monitoring still depends on `nvidia-smi`; it won't
automatically work with every AMD/Intel driver and Forge backend.

CI covers the Linux package, command-line setup, dry-run behavior, and
installation paths. No automated check can guarantee a real GPU render will
work on every Linux distro. Try one image before leaving it unattended.

The existing [numbered Nightrun releases](https://github.com/Bluenochian/Nightrun/releases)
are preserved. This Linux edition uses the versionless `linux-native`
release tag instead of inventing a 2.4.
