# Nightrun — Linux Native

**Separate Linux edition. No new numerical version.**

We already had a Linux launch path, but it was still attached to a combined
Windows/Linux ZIP. This is a proper independent Linux package with the same
modular engine, without the Windows-specific launchers.

## What's included

- A Linux-only `.tar.gz` and `.zip`. No `.bat` or `.ico` files.
- A `nightrun-linux` terminal command for setup, dry runs, validation,
  real batches, stopping, history analysis and metadata upscaling.
- A **no-sudo per-user installer**, KDE/GNOME application-menu entries and PNG
  icons. Works with XDG app/config/state locations and paths containing spaces.
- A dedicated Python venv for the small runtime dependencies, installed
  explicitly during setup instead of silently while rendering.
- Writable user-level batch locks and stop signals. Second launches cannot
  accidentally erase an active batch's stop request.
- The existing three prompt engines, curated franchise catalog, full prompt
  pools, LoRA resolution and Forge API workflow. Nothing stripped out there.

## Install

```bash
tar -xzf nightrun-linux-native.tar.gz
cd nightrun-linux
bash install.sh
nightrun-linux setup --repo "/path/to/Forge"
nightrun-linux validate
nightrun-linux dry-run --count 1
```

A real one-image test is still recommended before an overnight batch.
Linux Forge versions, GPU drivers and extensions differ, and simulated
tests don't make those differences vanish.

Numbered releases [2.3](https://github.com/Bluenochian/Nightrun/releases/tag/v2.3),
[2.2](https://github.com/Bluenochian/Nightrun/releases/tag/v2.2),
[2.0](https://github.com/Bluenochian/Nightrun/releases/tag/release2)
and [1.5](https://github.com/Bluenochian/Nightrun/releases/tag/release)
remain available, unchanged. Linux Native has its own **versionless**
`linux-native` tag.
