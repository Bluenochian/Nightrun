# Nightrun Linux Native — the actual user guide

> The goal is to leave Forge rendering overnight, not spend the entire night trying to make Nightrun work. So here's the setup, what to edit, and what to do when something inevitably acts stupid.

**Contents:** [Install](#1-install-it) · [Connect Forge](#2-tell-it-where-forge-lives) · [First run](#3-the-first-run-dont-skip-this) · [What to edit](#4-what-you-can-actually-edit) · [Custom prompts](#5-edit-prompt-pools-without-losing-them) · [LoRAs](#6-loras-and-world-modules) · [Daily use](#7-running-and-stopping-batches) · [Upscaling](#8-metadata-and-upscaling) · [Problems](#9-when-something-goes-wrong)

## 1. Install it

You need a working **Stable Diffusion Forge / Forge-Neo** installation, its models, Python 3 with the `venv` module, `flock` (util-linux), and a Linux desktop. KDE Plasma is fine. GNOME is fine. You do **not** need Wine or Windows batch files. NVIDIA temperature watching also requires `nvidia-smi`.

Download `nightrun-linux-native.tar.gz` from the [Linux Native release](https://github.com/Bluenochian/Nightrun/releases/tag/linux-native). In the directory where you downloaded it:

```bash
tar -xzf nightrun-linux-native.tar.gz
cd nightrun-linux
bash install.sh
```

That's a **per-user** install, no `sudo`. The installer creates a small private Python environment and installs `requests` and `Pillow` there. It doesn't download Forge, checkpoints, LoRAs, or an entire AI ecosystem because of course it doesn't.

If you manage Python dependencies yourself, `bash install.sh --no-deps` skips the environment installation. You'll need a Python interpreter with the runtime packages available.

Installed locations by default:

| File or setting | Where it goes |
| --- | --- |
| Application code and bundled pools | `~/.local/share/nightrun-linux/` |
| Terminal command | `~/.local/bin/nightrun-linux` |
| Desktop-menu launchers | `~/.local/share/applications/` |
| **Your** local settings | `~/.config/nightrun-linux/config.local.json` |
| Stop file, batch lock and setup report | `~/.local/state/nightrun-linux/` |
| Generated images | Whatever output directory you select |

The first three XDG paths follow `XDG_DATA_HOME`, `XDG_CONFIG_HOME` and `XDG_STATE_HOME` where appropriate. The command lives in `~/.local/bin/`. If typing `nightrun-linux` says *command not found*, run `~/.local/bin/nightrun-linux` instead, or add `~/.local/bin` to your `PATH`.

## 2. Tell it where Forge lives

Open a terminal, then run:

```bash
nightrun-linux setup --repo "/home/you/Stable-Diffusion-Forge"
```

**Replace that path.** It's an example, not a magical default. Choose the folder that contains Forge's `launch.py`, `models/`, and `venv/` (or `.venv/`).

Setup checks your Forge path, GPU/VRAM, installed checkpoints and LoRAs. It'll ask questions unless you use `--non-interactive`. For an unattended setup, supply the details explicitly:

```bash
nightrun-linux setup \
  --repo "/home/you/Forge" \
  --checkpoint "my-installed-checkpoint.safetensors" \
  --output-dir "/home/you/Pictures/Nightrun" \
  --non-interactive
```

Don't copy that checkpoint name verbatim unless you enjoy error messages. Use a real model installed under your Forge `models/Stable-diffusion/` directory.

**Already configured?** Running setup again normally preserves your tuned settings. Use `--reset-local` only if you specifically want to rebuild them from the defaults and GPU profile. Make a copy of your config first. There's no undo button for an overwritten JSON file.

## 3. The first run. Don't skip this.

Run these **in order**, not all at once:

```bash
nightrun-linux validate --count 100
nightrun-linux dry-run --count 5
nightrun-linux base --count 1
```

**Validate** checks configured prompt files, LoRA references and prompt composition. **Dry-run** produces prompts and metadata without asking Forge to generate images. **Base --count 1** is your actual one-image test; that last step *does* need Forge and your GPU.

If those work, start a proper batch:

```bash
nightrun-linux base --count 20
```

You can also run `nightrun-linux full --count 20` when you want scheduled upscaling. **Careful:** base mode can *still* upscale low-step images if the `upscale.auto_when_base_steps_below` threshold is active. If you want absolutely no upscaling, set `upscale.enabled` to `false` in your config.

The KDE/GNOME application menu also has **Nightrun** and **Nightrun Metadata Upscaler**, but the terminal is the easiest place to see errors. A black window quietly disappearing doesn't tell you anything useful.

## 4. What you can actually edit

**This is the important file:**

```bash
nano "$(nightrun-linux config-path)"
```

Or open it in Kate, VS Code, or whichever editor you're using. It's normal JSON, not a mysterious programming language. Make a backup first:

```bash
cp "$(nightrun-linux config-path)" "$(nightrun-linux config-path).backup"
```

After editing, check that you haven't dropped a comma into the void:

```bash
python3 -m json.tool "$(nightrun-linux config-path)" >/dev/null
nightrun-linux validate --count 20
```

**Change the existing values in your file.** The examples below show *parts* of the config, not complete replacement files.

| What you want | What to edit in `config.local.json` | Example |
| --- | --- | --- |
| Default batch size | `count` | `"count": 20` (rather than the shipped 300) |
| Checkpoint | `checkpoint` | `"checkpoint": "my-model.safetensors"` |
| Base resolution | `base.width`, `base.height` | `1024` × `1024` |
| Sampling steps | `base.steps_min`, `base.steps_max` | `25` to `35` |
| Guidance | `base.cfg_scale` | `5.0` |
| Output location | `paths.output_dir` | Absolute path to your render folder |
| Upscale frequency | `upscale.enabled`, `upscale.every_n` | `false` or `2` |
| GPU pause | `temperature.pause_above_c`, `resume_below_c` | `78` / `66` |
| Long breaks | `long_run_chill.enabled` | `true` or `false` |
| Which prompt engine wins more | `prompt_engines.weights` | Classic `3`, others `1` |
| Avoid adult-oriented styling | `prompt_pools` entry named `sensual_layer` | Set its `chance` to `0` |

### A couple of useful examples

**Make Classic show up more often.** Locate the existing `prompt_engines` object, then edit its `weights`:

```json
"weights": {
  "classic": 3,
  "combinator": 1,
  "franchise": 1
}
```

These are *relative weights*, not percentages. A weight of zero disables selection **by weight**, but check the corresponding engine's `enabled` setting too if you want it fully off.

**Stop upscaling altogether.** Find `upscale` and change:

```json
"enabled": false
```

**Change one prompt category's frequency.** In `prompt_pools`, find the item where `name` is `hair`, `clothing`, `environment`, or whatever you're targeting. Edit `chance` (0 = never, 1 = always when eligible) and `pick` (how many fragments to choose). An example entry:

```json
{
  "name": "hair",
  "file": "pools/hair.txt",
  "pick": 1,
  "chance": 0.40
}
```

**Don't paste that as a new top-level object.** Edit the existing entry. Otherwise you've made a lovely piece of invalid JSON.

## 5. Edit prompt pools without losing them

Want to change the words in your images? Look in the installed `pools/` folder. It's plain UTF-8 text. Each nonempty, non-comment line is a candidate prompt fragment.

For example, `pools/concept.txt` might contain lines like:

```text
moonlit gothic library
rain-soaked city at dawn
quiet abandoned observatory
```

Each line is separate. You don't need to cram an entire novel into one line, and you shouldn't put JSON into a `.txt` pool.

**Important:** the installed pools live inside the app directory. Reinstalling/updating the app can replace them. Keep personal changes in your config directory instead:

```bash
mkdir -p "$HOME/.config/nightrun-linux/pools"
cp "$HOME/.local/share/nightrun-linux/pools/concept.txt" \
   "$HOME/.config/nightrun-linux/pools/concept.txt"
nano "$HOME/.config/nightrun-linux/pools/concept.txt"
```

Then change the **existing concept** entry in `prompt_pools` from `"file": "pools/concept.txt"` to the full path of your copy. Example:

```json
"file": "/home/you/.config/nightrun-linux/pools/concept.txt"
```

Replace `/home/you` with your real home directory. **Use an absolute path**, not `~`—the pool loader reads the file path directly.

You can do the same with `genre.txt`, `clothing.txt`, `pose.txt`, `negative_extra.txt` (under `negative_pools`), and other lists. They all follow the same idea.

If Nightrun complains about a missing pool, check the `file` path in your config before blaming the GPU. That's a different problem.

## 6. LoRAs and world modules

Nightrun scans Forge's local `models/Lora` folders, resolves aliases and tries not to guess when two names look too similar.

In `config.local.json`:

- `lora_scan.folders` lists the folders to scan **relative to Forge**.
- `lora_scan.aliases` maps a friendly name to an actual installed file stem.
- `always_loras` holds LoRAs that appear every run.
- `random_loras` holds candidates with their own `chance` and weight ranges.
- `max_total_loras` limits the final stack. Trust me, more LoRAs isn't always better.

For example, if the pool says `PrettyEyes` but your installed file is
`PerfectEyesXL.safetensors`, the alias entry should look like this
**inside the existing** `lora_scan.aliases` object:

```json
"PrettyEyes": "PerfectEyesXL"
```

Don't forget the comma if it's between two existing entries. JSON is extremely committed to its punctuation.

**Franchise / world prompts** are configured through `franchise_system` and `prompt_engines`. The source catalog is bundled under
`modules/franchise_catalog.py`. The safest way to favor one engine is
changing `prompt_engines.weights`; you shouldn't need to edit Python
source just to adjust prompt style.

## 7. Running and stopping batches

```bash
nightrun-linux base --count 10
nightrun-linux full --count 10
nightrun-linux stop
nightrun-linux clear-stop
```

`stop` requests a clean exit **after the current image**, not a mid-render
crash. It also interrupts between-image pauses and thermal waits. A batch
lock stops a second launcher from clearing the first one's stop request.
Use `clear-stop` if you deliberately want to clear a leftover flag.

Generated runs usually contain files such as
`0001_base_...png`, `0001_metadata.json`,
`0001_prompt.txt`, `run.log` and `summary.json`.
The summary tells you whether a batch finished, stopped or failed. Read it
before declaring victory.

## 8. Metadata and upscaling

Want to upscale an existing image? Give Nightrun the metadata JSON saved
alongside it:

```bash
nightrun-linux upscale "/home/you/Pictures/Nightrun/0001_metadata.json" --scale 2
```

Use `--source base` to prefer the original, `--source upscale` for a
previous upscale, or `--no-create-if-missing` to stop Nightrun from
recreating a missing original. Upscaling needs Forge and the relevant
extension/checkpoint; it isn't just a resize command.

To examine past prompt variety:

```bash
nightrun-linux analyze "/home/you/Pictures/Nightrun"
```

## 9. When something goes wrong

| What happened | What to check |
| --- | --- |
| `command not found` | Use `~/.local/bin/nightrun-linux` or add that directory to your PATH. |
| `python3 -m venv` fails | Install your distro's Python venv support, then reinstall. |
| No installed checkpoint | Check Forge's `models/Stable-diffusion/` and rerun setup with `--checkpoint`. |
| `config.local.json` missing | Run `nightrun-linux setup`, not just `base`. |
| JSON parsing error | Run `python3 -m json.tool "$(nightrun-linux config-path)"` and fix the missing quote or comma. |
| Forge doesn't start | Verify its own venv and `launch.py`. Check `launch-nightrun.err.log` in your Forge directory. |
| Missing or skipped LoRA | Check filename, installed folders and aliases. Ambiguous matches are deliberately skipped. |
| Upscale fails | Check Ultimate SD Upscale and try a base-only image first. |
| GPU temperature stays high | Check cooling settings and `nvidia-smi`; AMD/Intel monitoring differs. |
| Second batch refuses to start | Good. The batch lock is protecting your first run. Stop that job before starting another. |

## 10. Uninstalling without losing your work

From the extracted Linux Native package:

```bash
bash uninstall.sh
```

The uninstall script removes the app and desktop entries. **It leaves your
configuration, output images and state alone.** Back up personal pool files
and `config.local.json` whenever you change machines.

If you only remember one thing from this guide: **edit your local config,
keep your custom pools separate, and test one image before running 300.**

There. Your GPU can babysit itself now. Mostly.
