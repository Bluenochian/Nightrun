# Nightrun for Windows — setup, use, and what to mess with

If you want to leave Forge rendering while you sleep, you're in the right place. If you want to spend six hours looking for `python.exe`, hopefully this prevents that.

**Windows release:** [Nightrun 2.2](https://github.com/Bluenochian/Nightrun/releases/tag/v2.2). **Linux users:** grab [Linux Native](https://github.com/Bluenochian/Nightrun/releases/tag/linux-native) instead.

## 1. Put it in the right folder

You need **Stable Diffusion Forge / Forge-Neo** working first, with a model installed and its Python environment set up.

Extract the `nightrun_2_2.zip` into a folder **two levels below** Forge's root, for example:

```text
C:\AI\Forge\
├── venv\
│   └── Scripts\python.exe
└── workflows\
    └── nightrun_2.2\
        ├── nightrun.py
        ├── config.json
        ├── modules\
        ├── pools\
        └── Run First Setup.bat
```

The exact `workflows` folder name isn't important; the **two-level depth** is. The batch launchers look for Forge's venv by going up two directories. Put it somewhere else and, well, guess what breaks.

## 2. First setup

Double-click **Run First Setup.bat**. It detects your Forge path, VRAM, models, and extensions, then writes `config.local.json`. That's your personal settings file; `config.json` is the shared default.

Then run:

1. **Run Validation Stress Test.bat** — checks prompt pools, LoRAs, and settings without image generation.
2. **Run One DRY TEST.bat** — creates sample prompts and metadata without rendering.
3. **Run Nightrun BASE only.bat** — generates base images.
4. **Run Nightrun FULL upscale.bat** — generates images with scheduled upscaling when enabled.
5. **Stop After Current Image.bat** — asks the current batch to stop cleanly, rather than killing it mid-image.

Keep the window open the first time so you can read warnings. A shiny one-click launcher isn't much use if it hides the error.

## 3. What to edit (and what to leave alone)

Open `config.local.json` in Notepad, VS Code, or another text editor. **Back it up** before major edits. It's JSON, which means quotes, braces and commas actually matter.

| Want to change | Edit this field | Notes |
| --- | --- | --- |
| Number of images | `count` | Default can be large; start with 5 or 10. |
| Model checkpoint | `checkpoint` | Use the real installed filename. |
| Resolution | `base.width`, `base.height` | Bigger means more VRAM. Shocking. |
| Base sampling steps | `base.steps_min`, `base.steps_max` | Reasonable range first, then experiment. |
| Completely disable upscale | `upscale.enabled` | Set to `false`. |
| Upscale every N images | `upscale.every_n` | Used in full mode. |
| When to cool GPU | `temperature.pause_above_c` | Monitor via `nvidia-smi` on NVIDIA. |
| Classic/Combinator/Franchise frequency | `prompt_engines.weights` | Relative weights, not percentages. |
| LoRAs you always want | `always_loras` | Check filenames and VRAM usage. |
| Extra random LoRAs | `random_loras` | Entries have `chance` and weight ranges. |
| Adult-oriented prompt styling | `prompt_pools` → `sensual_layer` | Set `chance` to `0` for SFW-only runs. |

The easiest change for your first night: edit `"count": 300` to `"count": 10` in `config.local.json`. Don't start by rewriting the entire generator. It's not a rite of passage.

### Custom prompt lists

The `pools/` folder contains plain `.txt` files for categories such as `concept`, `genre`, `hair`, `clothing`, and `pose`. A nonempty line is a possible prompt fragment:

```text
gothic moonlit greenhouse
cold rain on old stone
soft amber window light
```

Blank lines and lines starting with `#` are ignored. Add or remove entries, then run validation. Make a separate copy of any pool you customize so replacing the app folder later won't wipe your work.

Want a pool more or less often? In `config.local.json`, find its entry inside `prompt_pools` and change `chance` (0 to 1), or `pick` (number of fragments). Don't turn the entire config into a new JSON object just because a tutorial showed a small example.

### LoRAs

`lora_scan.folders` lists Forge directories to scan. The `aliases` dictionary connects pool names to installed filename stems. A name that matches multiple LoRAs may be skipped deliberately. That's better than loading the wrong one and wondering why everything looks cursed.

Use `max_total_loras` to limit your stack. Some models won't like certain LoRAs even if the filenames look fine; they're not magic compatibility stickers.

## 4. Running batches and reading the output

Use **BASE** first. If that works, try **FULL** with a small batch. Base mode can still trigger conditional upscale when the configured low-step threshold is active; set `upscale.enabled` to `false` if you want *zero* upscaling.

Your run folder will contain numbered PNGs, prompt text, `*_metadata.json`, a `summary.json`, and `run.log`. The summary now distinguishes success, failure, partial completion, and stopping. Read that before deciding everything worked.

To upscale an old result, drag its `*_metadata.json` onto **Run 2x Upscale From Metadata.bat**. You can also use the Python script directly for custom scale/size settings.

The **Stop After Current Image** script won't interrupt a running image in the middle, but it will stop the next image from starting and can interrupt cooling/sleep breaks. That's on purpose.

## 5. Common problems

| Problem | Check first |
| --- | --- |
| `venv\Scripts\python.exe` not found | Make sure Nightrun is exactly two folders below Forge. |
| No checkpoint found | Verify the model is under Forge's `models/Stable-diffusion` folder. |
| Missing LoRAs | Check real filenames, aliases and scan folders. |
| Forge API unavailable | Start Forge with its API enabled, normally port 7860. |
| FULL upscale error | Ensure the matching upscale extension is installed and enabled. |
| Out-of-memory or overheating | Lower image size, reduce LoRAs, adjust cooling/batch settings. |
| Prompt output looks nonsensical | Revisit pool entries and engine weights. More random isn't always better. |

Keep your config, custom prompt lists and image metadata backed up. The old numbered releases are available if you prefer a previous build.

**And please run one dry test before leaving the computer unattended.** Your GPU has enough work without troubleshooting your commas too.
