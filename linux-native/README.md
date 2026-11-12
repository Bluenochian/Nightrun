# Nightrun — Linux Native

**Linux-first installation for Stable Diffusion Forge / Forge-Neo.**

The same modular prompt engines, worlds, pools and upscaling workflow, now
packaged like a Linux desktop app. No Windows launchers, no placing it two
folders below Forge, and no `sudo` required.

## Start here

**[Read the complete Linux Native user guide](GUIDE.md)** — installation, connecting Forge,
the first render, what to edit, custom prompt pools, LoRAs, engines, upscaling,
stopping batches and troubleshooting.

Already know what you're doing? Download the
[Linux Native release](https://github.com/Bluenochian/Nightrun/releases/tag/linux-native):

```bash
tar -xzf nightrun-linux-native.tar.gz
cd nightrun-linux
bash install.sh

~/.local/bin/nightrun-linux setup --repo "/path/to/Forge"
~/.local/bin/nightrun-linux validate --count 100
~/.local/bin/nightrun-linux dry-run --count 5
~/.local/bin/nightrun-linux base --count 1
```

Replace `/path/to/Forge` with your actual installation. The setup script
checks Forge's path, GPU profile and checkpoints. No magical path detection can
fix a folder that isn't your Forge directory.

## What gets installed

| Item | Default location |
| --- | --- |
| App and private Python environment | `~/.local/share/nightrun-linux/` |
| Command | `~/.local/bin/nightrun-linux` |
| Desktop entries | `~/.local/share/applications/` |
| Your configuration | `~/.config/nightrun-linux/config.local.json` |
| Stop file, batch lock and setup report | `~/.local/state/nightrun-linux/` |
| Renders and logs | The Forge output folder you choose |

These use XDG config/data/state locations where appropriate. You'll need Python
3 and its `venv` module, util-linux `flock`, and your own working
Forge / Forge-Neo installation. The installer creates a private venv and
explicitly installs the few Python packages it needs.

**Edit `config.local.json`, not the bundled `config.json`.**
Keep custom prompt pools in your XDG config folder so a future reinstall
doesn't cheerfully replace them. The [editing section](GUIDE.md#4-what-you-can-actually-edit)
explains the actual keys. The [pool section](GUIDE.md#5-edit-prompt-pools-without-losing-them)
shows where to put your own text.

## Commands

```text
nightrun-linux setup       Connect local Forge and choose model/output paths
nightrun-linux validate    Check the config, pools and LoRAs
nightrun-linux dry-run     Generate prompts without GPU rendering
nightrun-linux base        Render base images
nightrun-linux full        Render with scheduled upscaling
nightrun-linux upscale     Replay/upscale an image from metadata JSON
nightrun-linux analyze     Inspect prompt variety across old runs
nightrun-linux stop        Stop after the current image
nightrun-linux clear-stop  Clear a leftover stop signal
nightrun-linux config-path Print the config file location
```

Add `--count 5` to override the configured batch size. Try
`base --count 1` before your first overnight run. Your GPU isn't a
beta tester with infinite patience.

## Updating and uninstalling

Install a newer Linux Native package with `bash install.sh`.
The config and output folders stay separate from application code. To remove
the program, run `bash uninstall.sh` from the extracted package;
personal configs, state and renders stay put.

Linux Forge/GPU compatibility depends on the installed drivers, models and
extensions. The automated checks use offline tests; please verify a real
one-image render on your own machine before leaving an overnight batch.

[Full guide](GUIDE.md) · [Linux Native release notes](RELEASE_NOTES.md) ·
[Windows 2.2](https://github.com/Bluenochian/Nightrun/releases/tag/v2.2)
