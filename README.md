<p align="center">
  <img width="4270" height="1232" alt="Nightrun banner" src="https://github.com/user-attachments/assets/d85e59d2-9fbf-476f-a000-47259c7703e2" />
</p>

<p align="center">
  <strong>Portable overnight prompt generation for Stable Diffusion Forge and Forge-Neo.</strong><br>
  Prompt pools, metadata replay, LoRA scanning, controlled randomness, upscale automation, thermal pauses, VRAM chill sessions, and long-run safety without hardcoded local chaos.
</p>

<p align="center">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows-5865F2?style=for-the-badge&logo=windows&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Stable Diffusion" src="https://img.shields.io/badge/stable%20diffusion-Forge%20%2F%20Forge--Neo-7B2FF7?style=for-the-badge">
  <img alt="Workflow" src="https://img.shields.io/badge/workflow-overnight%20automation-8A2BE2?style=for-the-badge">
</p>

<p align="center">
  <a href="#-fast-start">Fast start</a> ·
  <a href="#-what-nightrun-actually-does">Features</a> ·
  <a href="#-prompt-pools-the-normal-engine-first">Prompt pools</a> ·
  <a href="#-lora-handling">LoRA handling</a> ·
  <a href="#-franchise--world-modules-the-coherence-layer">World modules</a> ·
  <a href="#-metadata-upscaling">Metadata upscaling</a> ·
  <a href="#-configuration-power">Config</a> ·
  <a href="#-troubleshooting">Troubleshooting</a>
</p>

---

## 🌌 What is Nightrun?

**Nightrun** is a portable local workflow system for Stable Diffusion Forge / Forge-Neo.

It is not just a button that throws prompts at Forge. It is an overnight image machine that builds prompts from editable pools, validates your setup, scans LoRAs, manages long runs, writes replayable metadata, pauses when the GPU gets too hot, schedules chill sessions during huge batches, creates clean stop points, and can upscale from old metadata later.

The whole point is controlled chaos: you get variety, but the run is still structured enough to avoid turning every batch into random visual sludge.

It is built for people who want big batches without babysitting, but also do not want every output to feel like the same prompt wearing a different hat.

---

## ✨ What Nightrun actually does

| System | What it gives you |
| --- | --- |
| 🌙 **Overnight runs** | Generate large Forge batches while you sleep instead of babysitting every render. |
| 🧩 **Editable prompt pools** | Build prompts from plain `.txt` files instead of one giant hardcoded prompt blob. |
| 🎲 **Controlled randomness** | Uses chances, picks, boosts, step ranges, LoRA weights, and module chances so variety is configurable instead of blind. |
| 🧠 **Selection memory** | Penalizes recently used prompt choices and repeated color families during a run, reducing samey batches. |
| 🌈 **Color anti-repetition** | Tracks broad color families such as blue, cyan, red, purple, green, gold, black, silver, and iridescent. |
| 👁️ **Rare heterochromia control** | Keeps heterochromia rare through `selection_memory.heterochromia_chance` instead of letting it dominate eye prompts. |
| 🧬 **Coherent world modules** | Optional franchise/world layer that can keep selected outfits, environments, props, factions, colors, lighting, and cinematic language in the same universe. |
| 🎭 **Fusion mode** | Allows stranger cross-world combinations intentionally while reducing risky generic pool chances. |
| 🎲 **Randomized base steps** | Randomly chooses base steps from `base.steps_min` to `base.steps_max` for speed/quality variety. |
| 🚀 **Low-step auto-upscale** | If a base render lands under the configured step threshold, Nightrun can upscale it automatically so fast runs can still become useful final images. |
| 🔥 **GPU temperature pause** | Uses `nvidia-smi` to pause when the GPU is too hot, then resumes after it cools below the configured temperature. |
| 🧊 **Long-run VRAM chill** | During very large batches, schedules random rest sessions every now and then to let the machine settle. |
| 💤 **Between-image rest** | Adds configurable sleep time between images instead of hammering the system nonstop. |
| 🧪 **Validation mode** | Stress-tests pools, LoRAs, aliases, prompt formatting, missing resources, and generation logic before rendering. |
| 👁️ **Dry-run mode** | Writes prompts and metadata without touching Forge image generation, so you can inspect the run first. |
| 🪄 **Metadata replay** | Recreate, inspect, or upscale later from saved metadata instead of losing the exact prompt/settings chain. |
| 🖼️ **Metadata sidecars** | Every image gets detailed metadata: seed, prompt, negative prompt, choices, LoRAs, GPU stats, status, errors, and upscale reason. |
| 🔁 **Chained upscales** | Upscaler metadata can point to previous upscale outputs, so later upscales can continue from the best available source. |
| 🛠️ **Auto upscale tuning** | Metadata upscaler adjusts tile width, padding, steps, and denoise for target size unless you override them. |
| 🔍 **LoRA scanning** | Scans local LoRA folders, resolves aliases, skips missing LoRAs safely, and avoids crashing the whole run. |
| 🧬 **LoRA synergies** | If a trigger LoRA is selected, matching support LoRAs can be added with controlled chances and weights. |
| 🎚️ **Random LoRA weights** | LoRA weights can be randomized inside safe min/max ranges for less repetitive outputs. |
| 🧱 **LoRA safety limits** | Caps random LoRAs and total LoRAs so the prompt does not become a cursed stack of everything at once. |
| 📊 **Prompt variety analyzer** | Finds repeated colors, repeated modules, repeated categories, world-module usage, and prompt patterns. |
| 🧯 **Clean stop signal** | Stop after the current image instead of killing Forge mid-generation. |
| 🖥️ **First-run setup** | Generates local config, detects VRAM profile, checks checkpoint, counts LoRAs, checks Ultimate SD Upscale, and creates shortcuts. |
| 🧹 **Empty run cleanup** | Can clean empty dry-run or failed-test folders without touching folders that contain images. |
| 🖼️ **Contact sheet** | Creates a simple visual contact sheet when a run produces images. |
| 🧰 **Portable sharing** | Public `config.json` stays shareable while private paths go into `config.local.json`. |

---

## 🚀 Fast start

1. Put the Nightrun folder somewhere inside or near your Forge / Forge-Neo install.

```text
sd-webui-forge-neo/
  workflows/
    nightrun1.5/
```

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

### What the pool categories actually mean

| Area | Real pools involved | Why it matters |
| --- | --- | --- |
| 🧠 **Core idea** | `concept`, `genre`, `abstract_idea` | Gives the image its main concept, genre flavor, and stranger abstract direction. |
| 👤 **Character identity** | `character`, `creature_or_nonhuman`, `expression` | Defines who or what is in the image and how they read emotionally. |
| 💇 **Appearance** | `hair`, `eyes`, `body_focus` | Adds face/body visual anchors without forcing one fixed character design. |
| 👗 **Styling / clothing** | `clothing`, `stocking_layer`, `sensual_layer` | Controls outfit, silhouette, glam layer, and styling intensity. |
| 🧍 **Pose language** | `pose`, `body_pose`, `safe_pose`, `glamour_pose` | Gives the render body language, framing posture, and safer pose variety. |
| 🧰 **Props / equipment** | `equipment` | Adds weapons, tools, objects, accessories, artifacts, or scene interaction when the roll allows it. |
| 🌆 **Scene building** | `environment`, `environment_rich`, `time_and_weather`, `scene_depth`, `scene_embellishment` | Builds the world around the subject instead of leaving the image floating in nowhere. |
| 🎥 **Cinematic layer** | `lighting`, `camera`, `composition`, `color_grade`, `artist_direction` | Controls mood, shot language, polish, framing, and the final visual direction. |
| ✨ **Effects / powers** | `magic_element`, `aura_style`, `effects`, `effect_layer`, `style_layer` | Adds energy, magic, atmosphere, stylization, and extra visual identity. |
| 💎 **Quality / detail** | `quality_style`, `detail` | Adds detail language and quality/style finishing. |

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

That means the pool system is not just “roll dice forever.” It has a memory layer that pushes the run away from repeating itself too aggressively.

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

### Why the LoRA system matters

A normal prompt script usually fails in one of two ways:

1. it crashes because a LoRA name does not match the local file,
2. or it shoves too many LoRAs into the prompt and turns the output into soup.

Nightrun tries to avoid both.

It can scan local folders, resolve names, use aliases, skip missing files safely, randomize weights inside safe ranges, add support LoRAs only when trigger LoRAs appear, and cap the total LoRA count.

That means the LoRA layer stays powerful without becoming a slot machine strapped to a grenade.

---

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

### What those module fields actually do

| Module field | What it contributes |
| --- | --- |
| 👤 `character_archetypes` | The kind of subject the world wants: warrior, princess, rogue, agent, noble, pilot, commander, android, survivor, monster hunter, magical student, and so on. |
| 👗 `outfits` | Clothing that belongs to that world instead of generic random clothing fighting the theme. |
| 🏛️ `environments` | Places, interiors, exteriors, battlefields, cities, temples, stations, ruins, schools, forests, castles, ships, streets, and setpieces that fit the chosen source. |
| 🧰 `props_equipment` | Weapons, artifacts, devices, relics, tools, accessories, books, blades, staffs, terminals, guns, masks, or other story objects. |
| 🏴 `factions` | Groups, houses, orders, clans, empires, guilds, armies, corporations, rebels, cults, schools, or organizations tied to the world. |
| ⚙️ `technology` | Sci-fi devices, advanced gear, machinery, terminals, cybernetics, ships, robots, holograms, weapons, or tech language where that world needs it. |
| ✨ `magic_system` | Spell systems, supernatural logic, divine powers, curses, occult forces, elemental systems, rituals, or other non-tech power structures. |
| 🌄 `landscapes` | Wider scenic identity: wastelands, snowy kingdoms, neon cities, fantasy valleys, cursed lands, alien horizons, gothic skylines, and more. |
| 🏗️ `architecture` | Building language and structural identity: castles, temples, ruins, towers, city blocks, halls, megastructures, bunkers, stations, shrines. |
| 🐉 `creatures` | Beasts, monsters, summons, aliens, demons, animals, constructs, fantasy creatures, and nonhuman world flavor. |
| 🚀 `ships` | Spacecraft, airships, boats, warships, transports, starfighters, or other vehicle/setpiece elements when the world supports them. |
| 🤖 `droids` | Robots, androids, drones, automatons, mechs, synthetic companions, or machine-life elements when relevant. |
| 💡 `lighting_mood` | The lighting attitude of the world: moonlit, neon, divine, dusty, cinematic, gothic, magical, oppressive, heroic, eerie, etc. |
| 🌈 `color_palettes` | Palette direction that belongs to the world instead of accidental color mud. |
| 🎥 `cinematic_language` | Shot language, mood language, framing style, genre feel, and how the world wants to be visually presented. |
| 📝 `prompt_modifiers` | Extra tags that make the selected module feel stronger, more specific, and less generic. |

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

### Why this layer exists

Without the world module layer, a random prompt system can accidentally mix things like:

- fantasy robes,
- cyberpunk armor,
- spaceship corridors,
- cursed forest lighting,
- random weapons,
- unrelated color palettes,
- and a totally unrelated cinematic direction.

Sometimes that can be fun.

Most of the time, it is just incoherent.

The franchise/world module system exists so the run can still be surprising while keeping the selected idea internally consistent.

Normal pools give broad variety.

World modules give coherence.

Fusion mode gives controlled madness.

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

So a faster hybrid run does not automatically mean “throwaway preview.” It can still produce final-looking images through the upscale path.

### Weighted chances everywhere

Nightrun exposes chances and weights across the workflow:

- prompt pool chances,
- prompt pool pick counts,
- `boost_if_any` logic,
- world module chance,
- fusion mode chance,
- risky pool multiplier,
- random LoRA chances,
- LoRA pool pick min/max,
- LoRA weight min/max,
- LoRA synergy chance,
- max random LoRAs,
- max total LoRAs,
- selection memory penalties,
- color repetition penalties,
- long-run chill timing.

That is why it feels like a system instead of a tiny script.

You are not stuck with one behavior. You can tune the machine until it behaves like your machine.

---

## 🔥 Thermal and long-run protection

Nightrun includes multiple “do not cook my PC all night” systems.

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
| **Checkpoint not found** | Run setup again and select an installed checkpoint, or edit `config.local.json`. |
| **LoRA skipped** | Local filename probably differs from pool/config name. Add an alias or rename the pool entry. |
| **FULL upscale fails** | Install/enable Ultimate SD Upscale in Forge, restart Forge, then try again. |
| **Window closes instantly** | Run from the included `.bat` files so the window pauses and shows the error. |
| **No GPU detected** | Setup uses `unknown_safe`. CPU-only generation will be extremely slow. |
| **AMD or Intel GPU detected** | Setup can size the config from detected VRAM, but Forge support depends on your backend. |
| **Progress looks wrong for a moment** | Forge can briefly return stale progress. Nightrun ignores stale states that do not match expected steps. |
| **Metadata upscaler cannot find source image** | Keep metadata beside the image. If the image is gone, it can recreate the base unless `--no-create-if-missing` is used. |
| **Unicode / weird paths** | Setup writes JSON with ASCII escapes to survive older Windows consoles and editors better. |

## 🧠 Nerd corner

Most users can ignore this section. It is here for people who want to know what is happening under the hood.

### Config and API

- the main config resolver prefers `config.local.json` when launchers select it
- `config.json` remains the safe shared fallback
- paths in config can be relative to the Forge repo or absolute
- Nightrun starts Forge with `launch.py --api` when the API is not already alive
- API calls go to `http://127.0.0.1:7860/sdapi/v1/` by default
- Forge options are applied through `/sdapi/v1/options` before generation
- base generation uses `txt2img` with override settings for checkpoint, VAE, Forge preset, and CLIP skip where configured
- upscaling uses `img2img` with the Ultimate SD Upscale script args expected by Forge installations that expose the extension through the API

### Prompt building

- positive prompt formatting normalizes comma spacing
- duplicate comma-separated fragments are removed
- blocked positive terms are stripped
- broken comma layouts are rejected
- negative prompt is built from `negative_base` plus every loaded negative pool line
- `selection_memory` is runtime-only and does not write a memory database
- color anti-repetition detects broad families like blue, cyan/teal, red, purple, green, gold, black, silver, and iridescent
- heterochromia in the eyes pool is intentionally rare through `selection_memory.heterochromia_chance`
- `boost_if_any` can raise a pool chance when earlier categories were selected
- with a world module active, risky generic pools are blocked in coherent mode
- in fusion mode, risky generic pools are multiplied by `fusion_risky_pool_chance_multiplier`

### LoRA handling

- LoRA scanning caches results per repo, folder list, and alias map for the current Python process
- LoRA names are normalized by removing non-alphanumeric characters and using lowercase
- final LoRA list is de-duplicated after `always_loras`, `random_loras`, `lora_pools`, and `lora_synergies` are combined

### Run behavior

- validation writes only the first 10 sampled prompts into `validation_report.json`
- `summary.json` stores all per-image result metadata collected during the run
- contact sheets are created only when images exist
- `STOP_AFTER_CURRENT_IMAGE.txt` is checked before a new image, after an image, and during long-run chill sleeps
- long-run chill only activates when count is above `long_run_chill.only_when_count_over`
- temperature waiting is NVIDIA-focused because it uses `nvidia-smi`

### Setup and compatibility

- `setup_pipeline.py` checks NVIDIA first, then Windows video controller data, then `rocm-smi` on Linux when available
- setup writes JSON with `ensure_ascii=True` for stronger Windows console and editor compatibility
- `upscale_from_metadata.py` repairs common mojibake path text before deciding an image is missing
- the metadata upscaler writes a sidecar `.metadata.json` next to the new upscale
- chained upscales use that `output_image` first in auto mode
- if Pillow is available, image size is read with Pillow
- if Pillow is not available, PNG dimensions are read directly from the PNG header
- `tools/rebuild_prompt_pools.py` is a developer helper for rebuilding shipped pool files

---

## 📝 License / usage note

Use this with models, LoRAs, and extensions you are allowed to use.

Franchise module names are inspiration labels for prompt organization. Nightrun does not include model files, LoRA files, checkpoints, or copyrighted assets.

---

<p align="center">
  <strong>🌙 The run continues where the hand lets go.</strong>
</p>
