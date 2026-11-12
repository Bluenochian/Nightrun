<p align="center">
  <img width="4270" height="1232" alt="Nightrun banner" src="https://github.com/user-attachments/assets/633634ea-5840-4feb-b476-cc98167ab258"/>
</p>

<p align="center">
  <strong>Overnight prompt batches for Stable Diffusion Forge and Forge-Neo.</strong><br>
  Editable pools, LoRA matching, metadata replay, upscaling, and sensible breaks when the GPU needs one.
</p>

<p align="center">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows-5865F2?style=for-the-badge&logo=windows&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
</p>

<p align="center">
  <a href="#-installation--folder-placement">Installation</a> ·
  <a href="#-fast-start">Fast start</a> ·
  <a href="#-what-nightrun-actually-does">Features</a> ·
  <a href="#-prompt-pools-the-normal-engine-first">Prompt pools</a> ·
  <a href="#-lora-handling">LoRA handling</a> ·
  <a href="#-franchise--world-modules-the-coherence-layer">World modules</a> ·
  <a href="#-metadata-upscaling">Metadata upscaling</a> ·
  <a href="#-configuration-power">Config</a> ·
  <a href="#-troubleshooting">Troubleshooting</a> ·
  <a href="#-versions-in-this-repo">Versions</a>
</p>

---

## 📁 Installation — Folder placement

The Windows launchers expect Nightrun to sit **two folders below your Forge root**. They look for `venv\Scripts\python.exe` relative to that root.

For the source checkout, use:

```text
YourForgeFolder/
  venv/
  workflows/
    nightrun1.5/
      nightrun.py
      config.json
      Run First Setup.bat
      pools/
```

The [2.0 release ZIP](https://github.com/Bluenochian/Nightrun/releases/tag/release2) uses its own `nightrun_2.0` folder. Follow the instructions **inside that download** if you're using it. Don't mix paths from the two packages.

If `workflows/` doesn't exist, create it. The important part is the two-level depth, not the spelling of `workflows`.

---
## 🌌 What is Nightrun?

I wanted to leave Forge rendering overnight without sitting there choosing every prompt or checking whether the GPU was cooking itself. That's pretty much where Nightrun came from.

It builds prompts from editable text pools, talks to the local Forge / Forge-Neo API, runs batches, saves settings alongside the images, and gives the PC a rest when it's needed. There's a separate metadata upscaler for revisiting old renders.

It's configurable because I don't want everyone stuck with my preferred prompts, LoRAs, or hardware settings. Change the pools, run a small dry test, and make it yours.

---
## ✨ What Nightrun actually does

| Part | What happens |
| --- | --- |
| **Batch runner** | Runs base or full image batches using Forge's local API. |
| **Prompt pools** | Assembles prompts from editable UTF-8 text lists, with weights and chances in the config. |
| **World modules** | Optionally keeps an entire prompt within one franchise or setting instead of mixing everything. |
| **LoRA resolution** | Scans local LoRAs, matches aliases and filenames, and respects stack limits. |
| **Metadata** | Saves the prompt, seed, choices, settings and paths so you can trace a result later. |
| **Upscaling** | Can upscale from saved metadata, including recreating a missing base image. |
| **Cooling and stopping** | Supports temperature pauses, scheduled breaks, and stop-after-current-image. |
| **Validation** | Can inspect generated prompts and local resources before spending GPU time. |
| **Portable config** | Public defaults stay in `config.json`; machine-specific settings go into `config.local.json`. |

The Windows launchers are included. You can also run the Python scripts directly if you prefer.

---
## 🚀 Fast start

1. Place the Nightrun folder at the correct depth inside your Forge / Forge-Neo install — see [Installation](#-installation--folder-placement) above.

2. Run first setup:

```powershell
Run First Setup.bat
```

3. Validate before wasting GPU time:

```powershell
Run Validation Stress Test.bat
```

4. Preview one prompt without rendering:

```powershell
Run One DRY TEST.bat
```

5. Start a real run:

```powershell
Run Nightrun BASE only.bat
```

or:

```powershell
Run Nightrun FULL upscale.bat
```

6. When you want it to stop cleanly:

```powershell
Stop After Current Image.bat
```

---

## 🧩 Prompt pools: the normal engine first

This is the normal Nightrun engine.

These pools are the main editable prompt system. They live in `pools/`, they are plain UTF-8 `.txt` files, and each line can become part of a generated prompt.

Empty lines and lines starting with `#` are ignored.

The important thing: **these pools are the everyday editing surface**. If someone wants to change the personality of Nightrun, this is where they start.

World/franchise modules are an extra coherence layer explained later, not the first thing users need to understand.

### How a normal prompt is assembled

Nightrun builds the positive prompt from multiple layers:

| Order | Layer | What it does |
| --- | --- | --- |
| 1 | `fixed_prefix` | Always-on quality / style / baseline tags. |
| 2 | Optional world module | Only appears if the franchise/world system rolls active. Explained later. |
| 3 | `prompt_pools` | The normal editable `.txt` pool system listed below. |
| 4 | `fixed_suffix` | Always-on final prompt additions. |
| 5 | LoRA tags | Always LoRAs, random LoRAs, LoRA pools, and synergy LoRAs after resolution. |
| 6 | Formatter / validator | Normalizes comma spacing, strips blocked positive terms, removes duplicate comma fragments, and rejects broken prompt layouts. |

The negative prompt is built separately from `negative_base` plus every loaded negative pool.

### Actual shipped prompt pools

These are the real normal pools currently wired in `config.json`:

| Pool name | File | Pick | Chance / behavior |
| --- | --- | ---: | --- |
| `concept` | `pools/concept.txt` | 1 | always |
| `genre` | `pools/genre.txt` | 1 | 50% |
| `abstract_idea` | `pools/abstract_idea.txt` | 1 | 20% |
| `character` | `pools/character.txt` | 1 | 90% |
| `creature_or_nonhuman` | `pools/creature_and_nonhuman.txt` | 1 | 18% |
| `hair` | `pools/hair.txt` | 1 | 80% |
| `eyes` | `pools/eyes.txt` | 1 | 70% |
| `clothing` | `pools/clothing.txt` | 1 | 75% |
| `pose` | `pools/pose.txt` | 1 | 75% |
| `body_pose` | `pools/body_pose.txt` | 1 | 55% |
| `safe_pose` | `pools/safe_pose.txt` | 1 | 50% |
| `glamour_pose` | `pools/glamour_pose.txt` | 1 | 50% |
| `expression` | `pools/expression.txt` | 1 | 65% |
| `sensual_layer` | `pools/sensual_layer.txt` | 1 | 45% |
| `body_focus` | `pools/body_focus.txt` | 1 | 38% |
| `stocking_layer` | `pools/stocking_layer.txt` | 1 | 62% |
| `equipment` | `pools/equipment.txt` | 1 | 20%<br>boosts to 46% if `genre`, `environment`, or `magic_element` appeared |
| `environment` | `pools/environment.txt` | 1 | 78% |
| `environment_rich` | `pools/environment_rich.txt` | 1 | 52% |
| `time_and_weather` | `pools/time_and_weather.txt` | 1 | 45% |
| `lighting` | `pools/lighting.txt` | 1 | 80% |
| `camera` | `pools/camera.txt` | 1 | 55% |
| `scene_depth` | `pools/scene_depth.txt` | 2 | 70% |
| `scene_embellishment` | `pools/scene_embellishment.txt` | 1 | 55% |
| `magic_element` | `pools/magic_element.txt` | 1 | 58% |
| `aura_style` | `pools/aura_style.txt` | 1 | 48% |
| `effects` | `pools/effects.txt` | 1 | 58% |
| `style_layer` | `pools/style_layer.txt` | 1 | 72% |
| `effect_layer` | `pools/effect_layer.txt` | 1 | 58% |
| `artist_direction` | `pools/artist_direction.txt` | 1 | 45% |
| `color_grade` | `pools/color_grade.txt` | 1 | 48% |
| `composition` | `pools/composition.txt` | 1 | 70% |
| `quality_style` | `pools/quality_style.txt` | 1 | 52% |
| `detail` | `pools/detail.txt` | 1 | 52% |

### Boosted pools

Some pools are not just flat chances. For example, `equipment` normally has its own chance, but it can boost higher if earlier choices like genre, environment, or magic appeared.

That means props and objects show up more often when the scene actually has a reason for them, instead of appearing at random with no context.

### Selection memory

Configured in `selection_memory`:

```json
{
  "enabled": true,
  "recent_per_category": 28,
  "recent_colors": 18,
  "repeat_penalty": 0.08,
  "color_repeat_penalty": 0.16,
  "blue_cyan_extra_penalty": 0.35,
  "heterochromia_chance": 0.025
}
```

This is one of the reasons long batches do not feel as repetitive.

Nightrun remembers recent picks per category, remembers recent broad color families, penalizes repeated choices, adds extra penalty to blue/cyan repetition, and keeps heterochromia rare.

That means the pool system is not just "roll dice forever." It has a memory layer that pushes the run away from repeating itself too aggressively.

---

## 🧬 LoRA handling

Nightrun does not blindly throw LoRAs into the prompt and hope.

It scans, resolves, aliases, soft-matches, limits, deduplicates, and skips safely when needed.

| System | What it does |
| --- | --- |
| 🔍 **Folder scan** | Scans configured LoRA folders under the Forge repo. |
| 🧾 **Alias map** | Lets CivitAI display names resolve to real local filenames. |
| 🧠 **Soft matching** | Helps with ugly filenames, spaces, hyphens, underscores, and copied titles. |
| 🚫 **Missing skip** | If LoRA folders exist and a LoRA is missing, it is skipped and logged instead of crashing the run. |
| 🎚️ **Weight ranges** | LoRAs can roll randomized weights from configured min/max ranges. |
| 🧬 **Synergies** | Trigger LoRAs can pull matching support LoRAs. |
| 🧱 **Stack limits** | `max_random_loras` and `max_total_loras` prevent insane LoRA pileups. |
| 🧹 **Deduping** | Duplicate LoRAs are removed by resolved file stem. |

### LoRA pool files

| LoRA pool | File | Chance | Pick range | Weight range |
| --- | --- | ---: | ---: | ---: |
| `style_lora_from_pool` | `pools/lora_style.txt` | 55% | 0 to 1 | 0.18 to 0.5 |
| `detail_lora_from_pool` | `pools/lora_detail.txt` | 35% | 0 to 1 | 0.12 to 0.38 |
| `aura_effect_lora_from_pool` | `pools/lora_aura_effect.txt` | 35% | 0 to 1 | 0.1 to 0.36 |
| `character_concept_lora_from_pool` | `pools/lora_character_concept.txt` | 18% | 0 to 1 | 0.28 to 0.58 |
| `hsr_lora_from_pool` | `pools/hsr_character_loras.txt` | 8% | 0 to 1 | 0.28 to 0.55 |

Example alias:

```json
"aliases": {
  "DarkerThanBlackIllustrious": "DarkerThanDarkIllustriousV1"
}
```

So a pool can use a readable/display name while the actual local filename says something uglier.

## 🧠 Franchise / world modules: the coherence layer

Now the module system makes sense.

The normal pools above are the main engine. The franchise/world system is an optional layer on top of that.

When it activates, Nightrun selects one world module from `franchise_catalog.py` and pulls pieces from that same source family so the image can stay visually coherent.

Configured in `franchise_system`:

```json
{
  "enabled": true,
  "chance": 0.32,
  "fusion_mode_chance": 0.12,
  "fusion_risky_pool_chance_multiplier": 0.25,
  "catalog_py": "franchise_catalog.py"
}
```

### Real module fields

These are the actual module fields wired in the config, not a vague fake list:

| Module field | Pick | Chance |
| --- | ---: | ---: |
| `character_archetypes` | 1 | always |
| `outfits` | 1 | always |
| `environments` | 1 | always |
| `props_equipment` | 1 | 75% |
| `factions` | 1 | 35% |
| `technology` | 1 | 35% |
| `magic_system` | 1 | 35% |
| `landscapes` | 1 | 45% |
| `architecture` | 1 | 75% |
| `creatures` | 1 | 28% |
| `ships` | 1 | 24% |
| `droids` | 1 | 22% |
| `lighting_mood` | 1 | always |
| `color_palettes` | 1 | always |
| `cinematic_language` | 1 | always |
| `prompt_modifiers` | 1 | 70% |

### How world modules interact with normal pools

When a world module is active, it is not supposed to flatten the entire prompt system.

It adds a coherent themed layer, then Nightrun continues through the normal prompt pools with extra rules.

In **coherent mode**, risky generic pools can be blocked so they do not fight the selected world.

Risky generic pools currently include:

```text
concept, genre, creature_or_nonhuman, clothing, equipment, environment, environment_rich, magic_element, aura_style, effects, effect_layer, style_layer, artist_direction, color_grade
```

That means the generic pools most likely to contradict the selected world can stay out of the way.

In **fusion mode**, those same risky pools are allowed, but their chances are multiplied by `fusion_risky_pool_chance_multiplier`.

That means weird combinations can still happen, but intentionally and less aggressively.

### Catalog scale

The included catalog builds **hundreds of source worlds/franchises** into **1,202 usable module variants**.

It supports multiple module styles:

| Type | Meaning |
| --- | --- |
| 💎 **Rich specs** | Hand-authored detailed modules for worlds where extra coherence matters. |
| 🧱 **Compact specs** | Medium-detail modules generated from roles, outfits, environments, props, and factions. |
| 🌊 **Wide rows** | Long-tail source rows expanded through reusable lenses. |

Wide rows can expand through lenses like:

| Lens | Focus |
| --- | --- |
| `core` | lead identity, signature outfit, primary location, signature prop |
| `factions` | faction agent, faction uniform, conflict zone, faction artifact |
| `landmarks` | setpiece lead, setpiece outfit, landmark scene, setpiece object |

---

## 🎲 Controlled randomness and quality logic

Nightrun is random, but not stupid-random.

### Random base steps

Configured in:

```json
{
  "width": 1344,
  "height": 768,
  "steps": 65,
  "steps_min": 30,
  "steps_max": 65,
  "cfg_scale": 5.09,
  "sampler_name": "Euler a",
  "scheduler": "Automatic"
}
```

Each image can get a random base step count inside the configured range.

This gives speed/quality variety without editing the config every time.

### Low-step auto-upscale

Configured in:

```json
{
  "auto_when_base_steps_below": 43,
  "steps": 35,
  "width": 3072,
  "height": 1728
}
```

If the base render used fewer steps than the threshold, Nightrun can trigger upscale automatically.

The idea is simple: low-step base generations save time, but the upscale can still turn them into useful final images.

So a faster hybrid run does not automatically mean "throwaway preview." It can still produce final-looking images through the upscale path.

## 🔥 Thermal and long-run protection

Nightrun includes multiple "do not cook my PC all night" systems.

### GPU temperature pause

Configured in:

```json
{
  "pause_above_c": 78,
  "resume_below_c": 66,
  "check_seconds": 20
}
```

If the GPU reaches the pause temperature, Nightrun waits.

It checks again every configured number of seconds and resumes when the GPU cools below the resume temperature.

This is NVIDIA-focused because it uses `nvidia-smi`.

### Long-run VRAM chill

Configured in:

```json
{
  "enabled": true,
  "only_when_count_over": 100,
  "every_min_generations": 12,
  "every_max_generations": 20,
  "sleep_min_minutes": 5,
  "sleep_max_minutes": 10
}
```

For big batches, Nightrun schedules random chill sessions every so many generations.

That means it can pause for a few minutes during a long run instead of hammering GPU and VRAM nonstop.

### Between-image sleep

Configured in:

```json
"sleep_between_images_seconds": 15
```

A small rest between images keeps the workflow less brutal on the machine.

This matters because overnight generation is not just about output count. It is also about not treating your PC like disposable hardware.

---

## 🧭 Included launchers

| Launcher | What it does |
| --- | --- |
| 🖥️ `Run First Setup.bat` | Creates `config.local.json`, writes setup diagnostics, and creates desktop shortcuts. |
| 🧪 `Run Validation Stress Test.bat` | Tests pools, LoRA resolution, aliases, prompt formatting, and sample generation logic without rendering. |
| 👁️ `Run One DRY TEST.bat` | Writes prompt and metadata only. No Forge image call. |
| 🌙 `Run Nightrun BASE only.bat` | Generates base images. Low-step auto-upscale can still trigger if enabled. |
| 🚀 `Run Nightrun FULL upscale.bat` | Generates base images and scheduled upscale passes according to `upscale.every_n`. |
| 🪄 `Run 2x Upscale From Metadata.bat` | Drag one or more `*_metadata.json` files onto it for metadata-based upscaling. |
| 📊 `Run Prompt Variety Analyzer.bat` | Reads old metadata and reports repeated colors, modules, and patterns. |
| 🧯 `Stop After Current Image.bat` | Creates the clean stop signal. |
| 🧹 `Clear Stop Signal.bat` | Removes the stop signal. |

---

## 🧪 Run modes

The main script is:

```powershell
py nightrun.py --mode validate --count 100 --config config.local.json
py nightrun.py --mode dry-run --count 5 --config config.local.json
py nightrun.py --mode base --config config.local.json
py nightrun.py --mode full --config config.local.json
```

| Mode | What happens |
| --- | --- |
| 🧪 `validate` | Loads pools, scans LoRAs, resolves aliases, samples prompts, checks formatting, and fails if required resources are missing. |
| 👁️ `dry-run` | Writes prompt text and metadata only. No Forge generation call. |
| 🌙 `base` | Generates base images. Scheduled full upscales are disabled, but low-step auto-upscale can still happen. |
| 🚀 `full` | Generates base images and scheduled upscales. |

Optional arguments:

```powershell
py nightrun.py --mode full --count 300 --config config.local.json --seed 12345
```

| Argument | Meaning |
| --- | --- |
| `--count N` | Override the configured image count for this run. |
| `--config PATH` | Use `config.local.json` or another config file. |
| `--seed N` | Set the root seed. Image 1 uses `N+1`, image 2 uses `N+2`, and so on. |

---

## 🪄 Metadata upscaling

The upscaler script is:

```powershell
py upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --scale 2
```

Use the original base image as source:

```powershell
py upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --source base --scale 2
```

Use an existing upscale as source:

```powershell
py upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --source upscale --scale 2
```

Custom target size:

```powershell
py upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --width 3072 --height 1728
```

Dry-run check:

```powershell
py upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --scale 3 --dry-run
```

Disable missing-base recreation:

```powershell
py upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --scale 2 --no-create-if-missing
```

### Source selection modes

| Source | Behavior |
| --- | --- |
| `auto` | Prefer the most advanced available image. Checks previous upscaler metadata first, then upscale file, then source image, then base file, then matching PNGs. |
| `base` | Prefer the original base image. |
| `upscale` | Prefer an existing upscale image. |

If the source image is missing, the upscaler can recreate the base from metadata first, then upscale it.

The upscaler also writes a new `.metadata.json` beside the new image, which makes later chained upscales cleaner.

---

## 📦 Outputs

Each run creates a folder named like:

```text
nightrun-YYYYMMDD-HHMMSS
```

Inside it you may see:

```text
0001_base_WIDTHxHEIGHT.png
0001_upscale_WIDTHxHEIGHT.png
0001_prompt.txt
0001_metadata.json
summary.json
run.log
contact_sheet.jpg
validation_report.json
```

Metadata can include:

| Field | Meaning |
| --- | --- |
| `seed` | Reproducible seed for that image. |
| `prompt` | Full positive prompt. |
| `negative_prompt` | Full negative prompt. |
| `choices` | Which pools/modules were selected. |
| `loras` | Final LoRA tags. |
| `lora_sources` | Where each LoRA came from. |
| `base_steps` | Randomized base step count used for that image. |
| `gpu_before` / `gpu_after` | GPU stats when available. |
| `status` | Planned, dry-run, base-ok, upscale-ok, failed. |
| `upscale_reason` | Why upscale did or did not happen. |
| `error` | Error text when a generation fails. |

---

## 🖥️ First-run setup

`Run First Setup.bat` calls `setup_pipeline.py`.

It will:

- ask for the Forge / Forge-Neo repo folder,
- ask for the output folder,
- detect GPU vendor and VRAM when possible,
- choose a safe VRAM profile,
- check whether the configured checkpoint exists,
- count local LoRAs,
- check whether Ultimate SD Upscale appears installed,
- write `config.local.json`,
- write `setup_report.json`,
- create Desktop shortcuts called **Nightrun** and **Upscaler** on Windows.

Manual setup commands:

```powershell
py setup_pipeline.py --dry-run
py setup_pipeline.py --non-interactive --repo "D:\sd-webui-forge-neo" --profile auto
py setup_pipeline.py --profile low_4_6gb
py setup_pipeline.py --no-shortcuts
```

---

## ⚙️ Configuration power

Nightrun is built to be tuned.

| Config section | What it controls |
| --- | --- |
| `count` | Default number of images. |
| `checkpoint` | Forge checkpoint name. |
| `vae`, `forge_preset`, `clip_skip` | Forge options applied through the API. |
| `fixed_prefix`, `fixed_suffix` | Always-on positive prompt pieces. |
| `negative_base`, `negative_pools` | Negative prompt system. |
| `base` | Base width, height, sampler, scheduler, CFG, and step range. |
| `upscale` | Ultimate SD Upscale settings, scheduled upscales, and low-step auto-upscale. |
| `temperature` | GPU pause/resume temperature rules. |
| `sleep_between_images_seconds` | Rest time between images. |
| `long_run_chill` | Random longer rest sessions for huge batches. |
| `console` | Console color and live progress behavior. |
| `empty_run_cleanup` | Empty folder cleanup behavior. |
| `selection_memory` | Anti-repetition and color-family memory. |
| `franchise_system` | Coherent world module chance, module fields, risky pool behavior, and fusion behavior. |
| `prompt_pools` | Main positive prompt pools, chances, picks, and boosts. |
| `always_loras` | LoRAs attempted every time. |
| `random_loras` | LoRAs with individual chance values. |
| `lora_pools` | LoRAs loaded from pool files with randomized weights. |
| `lora_synergies` | Conditional support LoRAs. |
| `lora_scan` | Folders, aliases, missing behavior, and local resolution. |
| `max_random_loras`, `max_total_loras` | LoRA stack safety limits. |
| `dynamic_prompt` | Experimental alternate theme-family prompt builder, disabled by default. |

---

## 📊 Prompt variety analyzer

Run:

```powershell
Run Prompt Variety Analyzer.bat
```

Manual:

```powershell
py tools/analyze_prompt_history.py "D:\renders" --top 12 --report prompt_variety_report.json
```

It reports:

- metadata file count,
- top repeated categories,
- color distribution,
- world module usage,
- exact prompt repeats,
- warnings when one color/category dominates too hard.

---

## 🧹 Empty run cleanup

Dry-runs and failed tests can create empty folders.

Nightrun can clean those, but narrowly:

- only direct child folders named `nightrun-*`,
- legacy empty `overnight-randomizer-*` folders are recognized after upgrading,
- folders with `.png`, `.jpg`, `.jpeg`, or `.webp` are not removed.

The remembered cleanup answer is stored in:

```text
cleanup.local.json
```

Do not publish that file.

---

## 🧰 Config files

| File | Purpose |
| --- | --- |
| `config.json` | Public shared defaults. Safe to ship. |
| `config.local.json` | Machine-specific paths and setup choices. Do not publish. |
| `setup_report.json` | Local setup diagnostics. Useful for debugging. |
| `cleanup.local.json` | Local empty-folder cleanup preference. |
| `prompt_variety_report.json` | Local analyzer output. |

---

## 🧯 Troubleshooting

| Problem | Fix |
| --- | --- |
| **"System cannot find the path" on launch** | The folder is not placed correctly. See [Installation](#-installation--folder-placement) at the top of this page. |
| **Checkpoint not found** | Run setup again and select an installed checkpoint, or edit `config.local.json`. |
| **LoRA skipped** | Local filename probably differs from pool/config name. Add an alias or rename the pool entry. |
| **FULL upscale fails** | Install/enable Ultimate SD Upscale in Forge, restart Forge, then try again. |
| **Window closes instantly** | Run from the included `.bat` files so the window pauses and shows the error. |
| **No GPU detected** | Setup uses `unknown_safe`. CPU-only generation will be extremely slow. |
| **AMD or Intel GPU detected** | Setup can size the config from detected VRAM, but Forge support depends on your backend. |
| **Progress looks wrong for a moment** | Forge can briefly return stale progress. Nightrun ignores stale states that do not match expected steps. |
| **Metadata upscaler cannot find source image** | Keep metadata beside the image. If the image is gone, it can recreate the base unless `--no-create-if-missing` is used. |
| **Unicode / weird paths** | Setup writes JSON with ASCII escapes to survive older Windows consoles and editors better. |

---

## 🧠 Under the hood

A few things worth knowing if you're debugging a run:

- Nightrun talks to the local Forge API at `127.0.0.1:7860`. If Forge isn't running, the batch runner can start it with `launch.py --api`.
- `config.local.json` holds your machine's paths and setup choices; don't commit it.
- Selection memory lives in the running process; it isn't a database of old prompt history.
- Validation keeps the report readable by saving only a sample of the prompts it checked.
- A stop signal is checked between images and during long cooling pauses. It won't cut a render in half.
- Temperature monitoring uses `nvidia-smi`; don't assume identical behavior on AMD or a setup without NVIDIA tools.
- The metadata upscaler can read PNG dimensions without Pillow and tries to repair some Windows path-encoding problems.
- `tools/rebuild_prompt_pools.py` is a developer utility, not something you need to run during normal setup.

---
## 🆕 Versions in this repo

The checked-in Windows batch runner lives in `nightrun1.5/`. There is also a [Nightrun 2.0 download](https://github.com/Bluenochian/Nightrun/releases/tag/release2), which is packaged separately. The instructions above describe the files **actually present in this source checkout**, not a promise that every release ZIP has the same structure.

At the repository root you'll see `nightrun_web.py` and `templates/index.html`: an early **3.0 dashboard prototype**. Its generation loop currently **simulates prompts and progress**, rather than starting real image batches. It's there to experiment with the interface. For actual overnight generation, use the batch runner.

I'd rather be upfront about the difference than have somebody leave the dashboard open all night expecting 300 finished renders.

---
## 📝 License and usage

Nightrun runs against models, checkpoints, LoRAs and extensions you install yourself. It doesn't ship or download those assets. Franchise names are labels for organizing prompt ideas, not packaged franchise content.

Check the licenses of whatever models and extensions you use. The code is provided as-is, without a promise that your setup or GPU will behave exactly like mine.

---

<p align="center">
  <strong>🌙 Let the PC do the babysitting.</strong>
</p>