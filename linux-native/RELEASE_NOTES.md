# Nightrun — Linux Native

**Native Linux installation for Stable Diffusion Forge / Forge-Neo.**

Install Nightrun directly on your Linux desktop with a per-user installer,
application-menu shortcuts, XDG settings, and the `nightrun-linux` command.
The rendering engine and prompt tools are included.

## What you get

- Linux-only `.tar.gz` and `.zip` with no Windows `.bat` or `.ico` files.
- The maintained modular Classic / Combinator / Franchise engines, their
  prompt pools, LoRAs, Forge generation and metadata replay.
- A per-user installation with **no sudo**, isolated Python dependencies,
  KDE/GNOME menu entries and PNG icons.
- A separate local config, user-level stop signals and a batch lock. A second
  launch won't clear the first run's stop request. Because that would be
  exceptionally stupid.
- A **proper user guide** showing exactly how to install, connect Forge,
  edit `config.local.json`, keep customized prompt pools across upgrades,
  adjust LoRAs and engine weights, and troubleshoot failures.

## Install

```bash
tar -xzf nightrun-linux-native.tar.gz
cd nightrun-linux
bash install.sh
~/.local/bin/nightrun-linux setup --repo "/path/to/Forge"
~/.local/bin/nightrun-linux validate --count 100
~/.local/bin/nightrun-linux dry-run --count 5
~/.local/bin/nightrun-linux base --count 1
```

Yes, the `/path/to/Forge` part is a placeholder. Please replace it.

The **[Linux Native guide](https://github.com/Bluenochian/Nightrun/blob/main/linux-native/GUIDE.md)**
covers what those commands do, what to customize and where the files go.
A copy is included in the download.

Automated Linux tests and dry runs verify the installer and workflow.
Actual GPU rendering depends on your Forge, models, drivers and extensions.
Test one image before your first overnight run.

Windows is still available as [Nightrun 2.2](https://github.com/Bluenochian/Nightrun/releases/tag/v2.2).
The older [2.0](https://github.com/Bluenochian/Nightrun/releases/tag/release2)
and [1.5](https://github.com/Bluenochian/Nightrun/releases/tag/release)
releases remain available separately.
