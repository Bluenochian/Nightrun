Nightrun 1.5 for Forge / Forge-Neo
=======================================

Portable prompt-pool batch runner for Stable Diffusion Forge and Forge-Neo.
It builds varied prompts from plain text pools, runs Forge through the API,
writes replayable metadata for every image, and includes a drag-and-drop
metadata upscaler that can recreate missing base images before upscaling.

The project is designed for sharing. The public config stays portable, while
first-run setup writes machine-specific paths and hardware choices into
config.local.json.


For Impatient People
--------------------

1. Run First Setup.bat
2. Run Validation Stress Test.bat
3. Run One DRY TEST.bat
4. Run Nightrun BASE only.bat
5. Use Stop After Current Image.bat when you want it to finish cleanly


What It Does
------------

- Generates large batches of prompts and images from modular .txt pools.
- Runs Forge through the built-in API instead of a locked workflow graph.
- Supports base-only generation, full generation with scheduled upscales, dry
  prompt tests, and validation stress tests.
- Writes a prompt text file, metadata JSON, log, summary, and contact sheet for
  each run.
- Can replay metadata later for 2x, 3x, 4x, or custom-size upscales.
- Can recreate a missing base image from metadata before upscaling it.
- Scans local LoRA folders and skips missing LoRAs instead of crashing.
- Supports LoRA aliases when CivitAI display names do not match local filenames.
- Uses GPU/VRAM setup profiles so the same package can work on different PCs.
- Includes a large franchise-inspired catalog that keeps world details coherent.
- Includes stop-after-current-image control for long Nightrun sessions.
- Includes prompt history analysis to catch repetitive outputs.
- Lets your VRAM/GPU to rest between long sessions, heat-spikes and configurable intervals.

Main Idea
---------

A normal random prompt tool can easily become nonsense because every part is
pulled from unrelated pools. This pipeline tries to avoid that.

When no franchise module is selected, it behaves like a broad art randomizer.
It combines character, clothing, pose, lighting, environment, camera, style,
color, effects, detail, and optional LoRAs.

When a franchise/world module is selected, the runner pulls themed outfits,
environments, props, factions, creatures, architecture, technology, magic,
lighting, palettes, and cinematic language from that same module. Riskier
generic pools are disabled in coherent mode so the result does not mix random
wizard robes, cyberpunk armor, wasteland bunkers, and spaceship interiors unless
fusion mode is intentionally active.


Requirements
------------

- Windows is the main target for the included .bat launchers.
- Stable Diffusion Forge or Forge-Neo.
- Forge API support. The runner starts Forge with --api if it is not already up.
- A checkpoint installed under the Forge models folder.
- Python from the Forge venv is recommended.
- Optional but recommended: Ultimate SD Upscale extension for FULL mode and
  metadata upscaling.
- Optional LoRAs under models/Lora or another folder listed in config.json.

This pack does not download checkpoints, LoRAs, extensions, or models. It only
uses what is already installed locally.


Fast Start
----------

1. Put this folder somewhere inside or near your Forge / Forge-Neo install.
   A common layout is:

     sd-webui-forge-neo/workflows/nightrun1.5

2. Run:

     Run First Setup.bat

   This creates your private config.local.json, which stores your local Forge
   path, output path, VRAM profile, and checkpoint choice.

3. Read the setup warnings, if any.

4. Run:

     Run Validation Stress Test.bat

5. Run:

     Run One DRY TEST.bat

6. Start a real batch with either:

     Run Nightrun BASE only.bat
     Run Nightrun FULL upscale.bat


First-Run Setup
---------------

Run First Setup.bat calls setup_pipeline.py.

It will:

- ask for the Forge / Forge-Neo repo folder,
- ask for the output folder,
- detect GPU vendor and VRAM when possible,
- choose a safe VRAM profile,
- check whether the configured checkpoint exists,
- count local LoRAs,
- check whether Ultimate SD Upscale appears installed,
- write config.local.json,
- write setup_report.json,
- create Desktop shortcuts called Nightrun and Upscaler on Windows.

config.local.json does not exist until you run First Setup -- that is expected.
It is intentionally local. Do not upload it to GitHub or CivitAI.
It contains machine paths and setup results.

Useful setup commands:

  python setup_pipeline.py --dry-run
  python setup_pipeline.py --non-interactive --repo "D:\sd-webui-forge-neo" --profile auto
  python setup_pipeline.py --profile low_4_6gb
  python setup_pipeline.py --no-shortcuts

Dry-run setup is non-interactive. It prints the setup report but does not write
config.local.json.


Launchers
---------

Run First Setup.bat
  Creates config.local.json, setup_report.json, and optional Desktop shortcuts.

Run Validation Stress Test.bat
  Checks pool files, prompt formatting, LoRA resolution, and sample generation
  without rendering images. Writes validation_report.json in the test run folder.

Run One DRY TEST.bat
  Builds prompt files and metadata only. It does not call Forge image generation.
  Useful for checking whether prompts feel sane before wasting GPU time.

Run Nightrun BASE only.bat
  Generates base images. Low-step auto-upscale can still trigger if enabled in
  config.json.

Run Nightrun FULL upscale.bat
  Generates base images and scheduled upscale passes according to upscale.every_n.

Stop After Current Image.bat
  Creates STOP_AFTER_CURRENT_IMAGE.txt. The runner finishes the current image,
  then stops before starting the next one.

Clear Stop Signal.bat
  Removes STOP_AFTER_CURRENT_IMAGE.txt.

Run 2x Upscale From Metadata.bat
  Drag one or more *_metadata.json files onto it, or run it and paste a metadata
  path. It finds the best source image, or recreates the base image if needed,
  then makes a 2x upscale by default.

Run Prompt Variety Analyzer.bat
  Scans metadata from a render folder, reports repeated categories/colors, and
  writes prompt_variety_report.json.


Run Modes
---------

The main script is nightrun.py.

  python nightrun.py --mode validate --count 100 --config config.local.json
  python nightrun.py --mode dry-run --count 5 --config config.local.json
  python nightrun.py --mode base --config config.local.json
  python nightrun.py --mode full --config config.local.json

Modes:

validate
  Loads pools, scans LoRAs, resolves aliases, samples prompts, checks formatting,
  and fails if required resources are missing.

dry-run
  Writes prompt text and metadata only. No Forge generation call is made.

base
  Generates base images. Scheduled FULL upscales are disabled, but low-step
  auto-upscale can still happen if upscale.auto_when_base_steps_below is set.

full
  Generates base images and scheduled upscales.

Optional arguments:

--count N
  Overrides config count for this run.

--config PATH
  Uses config.local.json or another config file.

--seed N
  Sets the root seed. Image 1 uses seed N+1, image 2 uses N+2, and so on.


Outputs
-------

Each run creates a folder named like:

  nightrun-YYYYMMDD-HHMMSS

Inside it you may see:

- 0001_base_WIDTHxHEIGHT.png
- 0001_upscale_WIDTHxHEIGHT.png
- 0001_prompt.txt
- 0001_metadata.json
- summary.json
- run.log
- contact_sheet.jpg when images exist
- validation_report.json in validation mode

The metadata is intentionally detailed. It includes the seed, prompt, negative
prompt, selected pools, selected LoRAs, LoRA source information, base steps,
image paths, GPU stats when available, status, errors, and upscale reason.


Metadata Upscaling
------------------

The upscaler script is upscale_from_metadata.py.

Basic 2x:

  python upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --scale 2

Use the original base image as the source:

  python upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --source base --scale 2

Use an existing upscale as the source:

  python upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --source upscale --scale 2

Custom target size:

  python upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --width 3072 --height 1728

Dry-run check:

  python upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --scale 3 --dry-run

Source selection modes:

base
  Prefer the original base image.

upscale
  Prefer existing upscale images.

auto
  Prefer the most advanced existing image. It checks output_image from previous
  upscaler metadata first, then upscale_file, then source_image, then base_file,
  then matching PNGs in the folder.

If the source image is missing, the upscaler can recreate the base image from
the metadata prompt, negative prompt, seed, and base size. Disable that with:

  --no-create-if-missing

Upscale tuning is automatic. Larger targets reduce tile width, padding, steps,
and denoise where needed unless you override them with:

  --steps
  --denoise
  --tile-width
  --padding
  --recreate-steps
  --seed
  --output


Config Files
------------

config.json
  Shared defaults. Safe to ship. This is the public base config.

config.local.json
  Machine-specific setup output. Not for sharing.

setup_report.json
  Local setup diagnostics. Useful for debugging, not needed in public releases.

cleanup.local.json
  Stores the remembered answer for empty dry-run folder cleanup. Not for sharing.

prompt_variety_report.json
  Local report created by the analyzer. Not for sharing.


Important Config Sections
-------------------------

count
  Default number of images for real runs.

checkpoint
  Forge checkpoint name. The value in config.json is only a placeholder. Run
  First Setup.bat to write the correct checkpoint into config.local.json, or
  edit config.local.json manually.

vae, forge_preset, clip_skip
  Extra Forge options applied through the API when configured.

fixed_prefix and fixed_suffix
  Always included in the positive prompt.

negative_base and negative_pools
  Base negative prompt plus optional negative pool files.

base
  Width, height, sampler, scheduler, CFG, and random step range for base images.
  steps_min and steps_max are used to choose a random base step count per image.

upscale
  Ultimate SD Upscale settings, scheduled upscale behavior, and low-step
  auto-upscale threshold.

temperature
  Optional NVIDIA GPU temperature pause/resume rules using nvidia-smi.

sleep_between_images_seconds
  Rest time between images.

long_run_chill
  Random longer rests during very large batches to give VRAM/GPU time to settle.

console
  Console color and live progress behavior.

empty_run_cleanup
  Optional cleanup for empty run folders created by dry tests or failed tests.

selection_memory
  In-memory anti-repetition system for a single run. It penalizes recently used
  prompt choices and recently dominant color families.

franchise_system
  Enables the coherent world module system and controls how often it triggers.

prompt_pools
  Main positive prompt pool list. Each entry points at a .txt file and can have
  pick, chance, required, and boost_if_any settings.

always_loras
  LoRAs that are attempted every time.

random_loras
  LoRAs with individual chance values.

lora_pools
  LoRA names loaded from pool files with randomized weights.

lora_synergies
  Conditional LoRA support. If a trigger LoRA is selected, extra matching LoRAs
  can be added.

lora_scan
  Local LoRA folder scanning, aliases, missing-LoRA behavior, and cache behavior.

max_random_loras and max_total_loras
  Safety limits for LoRA stacking.

dynamic_prompt
  Experimental alternate theme-family prompt builder. Disabled by default.
  Leave it as-is unless you want to dig into it -- it does nothing while
  enabled is set to false.


Prompt Pools
------------

Pool files are plain UTF-8 .txt files under pools/. Empty lines and lines
starting with # are ignored.

Most pool lines are normal comma-separated prompt fragments. The runner cleans
spacing, removes duplicate comma-separated fragments, strips blocked positive
terms, and validates that commas are formatted correctly.

Default positive pools include concept, genre, abstract idea, character,
creature/nonhuman, hair, eyes, clothing, pose, body pose, safe pose, glamour
pose, expression, sensual layer, body focus, stockings, equipment, environment,
rich environment, time/weather, lighting, camera, scene depth, scene
embellishment, magic element, aura style, effects, style layer, effect layer,
artist direction, color grade, composition, quality style, and detail.

A few pool notes:

- character_loras.txt is legacy compatibility data. The default config uses
  lora_character_concept.txt instead.
- lora_sampler_speed.txt is present but not enabled by default. It can be wired
  into lora_pools if you want LCM/Lightning style speed LoRAs.
- style_loras.txt is also legacy-style data. The active LoRA style pool is
  lora_style.txt.
- negative_extra.txt is appended to negative_base.


LoRA Handling
-------------

The runner scans folders listed in config.json under lora_scan.folders. By
default this is models/Lora under the Forge repo.

Supported file extensions:

- .safetensors
- .pt
- .ckpt

Resolution behavior:

- Exact normalized names match first.
- Aliases are applied when the target file exists locally.
- Soft matching is attempted for ugly filenames and copied CivitAI titles.
- If a LoRA folder exists and a LoRA is missing, the LoRA is skipped and logged.
- If no LoRA folder is found, raw names can be kept so portable tests still work.
- Duplicate LoRAs are removed by resolved file stem.
- max_total_loras trims the final LoRA list.

Alias example in config.json:

  "aliases": {
    "DarkerThanBlackIllustrious": "DarkerThanDarkIllustriousV1"
  }

This means a pool/config entry using DarkerThanBlackIllustrious can resolve to
the installed DarkerThanDarkIllustriousV1 file.


Franchise / World Catalog
-------------------------

franchise_catalog.py provides world-coherent prompt modules.

Current catalog size:

- 428 source worlds/franchises
- 1,202 generated module variants

When a module is active, it can inject:

- character_archetypes
- outfits
- environments
- props_equipment
- factions
- creatures
- architecture
- technology
- magic_system
- landscapes
- ships
- droids
- lighting_mood
- color_palettes
- cinematic_language
- prompt_modifiers

Coherent mode:
  Risky generic pools are disabled so the selected world stays visually coherent.

Fusion mode:
  Risky generic pools are allowed at a reduced chance multiplier, letting weird
  cross-world combinations happen intentionally.

Catalog module types:

Rich SPECS
  Hand-authored detailed modules for worlds where extra coherence matters.

compact_spec modules
  Medium-detail modules generated from roles, outfits, environments, props, and
  faction lists.

Wide rows
  Long-tail modules built from an id, source name, six signature terms, and a
  flavor string.

Lens variants:

Each wide row is expanded through three lenses:

core
  Lead identity, signature outfit, primary location, signature prop.

factions
  Faction agent, faction uniform, conflict zone, faction artifact.

landmarks
  Landmark setpiece lead, setpiece outfit, landmark scene, setpiece object.

That is how the catalog expands to 1,202 variants without hand-writing every
variant as a full dict.


Adding New Franchise Modules
----------------------------

Fast method: add a pipe-delimited row to BULK_FRANCHISE_ROWS_TEXT in
franchise_catalog.py.

Format:

  module_id|Source Name|term1;term2;term3;term4;term5;term6|flavor string

Example:

  severance|Severance|Lumon;MDR office;severed floor;waffle party;Eagan shrine;Perpetuity Wing|corporate liminal psychological sci-fi

Six signature terms are required.

The flavor string helps keyword detection. Words like sci-fi, cyber, space,
robot, military, and hacker can add technology fields. Words like fantasy,
magic, gothic, vampire, myth, and occult can add magic_system fields.

Python tuple method: add to WIDE_FRANCHISE_ROWS.

  ("module_id", "Source Name", ["term1", "term2", "term3", "term4", "term5", "term6"], "flavor string"),

Full-control method: add a hand-authored dict in SPECS.

Duplicate module IDs are blocked by validation in the catalog builder. Keep IDs
unique across SPECS, compact specs, wide rows, and bulk rows.


VRAM Profiles
-------------

Setup chooses a profile from detected VRAM, or you can force one.

unknown_safe
  Conservative fallback when GPU/VRAM cannot be detected.

low_4_6gb
  Safer for 4 to 6 GB GPUs and laptops.

balanced_6_8gb
  Moderate settings.

quality_8_12gb
  Higher base resolution and upscale settings.

high_12gb_plus
  Larger base output and more LoRA headroom.

Force a profile:

  python setup_pipeline.py --profile low_4_6gb


Prompt Variety Analyzer
-----------------------

The analyzer reads *_metadata.json files and looks for repetition.

Run from the .bat:

  Run Prompt Variety Analyzer.bat

Manual:

  python tools/analyze_prompt_history.py "D:\renders" --top 12 --report prompt_variety_report.json

It reports:

- metadata file count,
- top repeated categories,
- color distribution,
- world module usage,
- exact prompt repeats,
- warning when blue/cyan or a category dominates too much.


Empty Run Cleanup
-----------------

Dry runs and failed tests can create folders with no images. Cleanup is narrow
on purpose.

It only considers direct child folders named:

  nightrun-*

inside the configured output folder. Legacy `overnight-randomizer-*` empty folders are also recognized for cleanup after upgrading, and only removes folders with no .png,
.jpg, .jpeg, or .webp files.

The first time it finds empty run folders, it asks:

- yes
- no
- yes, don't ask again
- no, don't ask again

The remembered answer is stored in cleanup.local.json.


Common Problems
---------------

Checkpoint not found
  Run setup again and select an installed checkpoint, or edit config.local.json.

LoRA skipped
  The local filename probably differs from the pool/config name. Add an alias or
  rename the pool entry.

FULL upscale fails
  Install/enable Ultimate SD Upscale in Forge, restart Forge, then try again.

Window closes instantly
  Run from the included .bat files so the window pauses and shows the error.

No GPU detected
  Setup uses unknown_safe. Generation may still work if Forge supports the local
  backend, but CPU-only generation will be extremely slow.

AMD or Intel GPU detected
  Setup can size the config from detected VRAM, but actual Forge support depends
  on that system's backend.

Progress looks wrong for a moment
  Forge can briefly return stale progress. The runner ignores stale states that
  do not match the expected step count.

Metadata upscaler cannot find source image
  Keep the metadata beside the image when possible. If the image is gone, the
  upscaler can recreate the base unless --no-create-if-missing is used.

Unicode / weird path text
  The setup file writes config JSON with ASCII escapes to survive older Windows
  consoles and editors better. Runtime reading uses UTF-8 tolerant loading.


Nerd Corner: Extra Details Most Users Can Ignore
------------------------------------------------

Config and API

- The main config resolver prefers config.local.json when launchers select it,
  but config.json remains the safe shared fallback.
- Paths in config can be relative to the Forge repo or absolute.
- The runner starts Forge with launch.py --api when the API is not already alive.
- API calls are sent to http://127.0.0.1:7860/sdapi/v1/ by default.
- Forge options are applied through /sdapi/v1/options before generation.
- Base generation uses txt2img with override_settings for checkpoint, VAE,
  forge_preset, and CLIP skip where configured.
- Upscaling uses img2img with the Ultimate SD Upscale script args expected by
  Forge installations that expose that extension through the API.

Prompt Building

- The positive prompt formatter normalizes comma spacing, removes duplicate
  comma-separated fragments, strips blocked positive terms, and rejects broken
  comma layouts.
- The negative prompt is built from negative_base plus every loaded negative
  pool line.
- selection_memory is runtime-only. It does not write a memory database. It just
  penalizes recently picked items during the current process.
- Color anti-repetition detects broad families like blue, cyan/teal, red,
  purple, green, gold, black, silver, and iridescent.
- Heterochromia in the eyes pool is intentionally rare through
  selection_memory.heterochromia_chance.
- boost_if_any can raise a pool chance when earlier categories were selected.
- With a world module active, risky generic pools are blocked in coherent mode.
  In fusion mode they are multiplied by fusion_risky_pool_chance_multiplier.

LoRA Handling

- LoRA scanning caches results per repo, folder list, and alias map for the
  current Python process.
- LoRA names are normalized by removing non-alphanumeric characters and using
  lowercase, which helps with spaces, underscores, hyphens, and CivitAI titles.
- The final LoRA list is de-duplicated after always_loras, random_loras,
  lora_pools, and lora_synergies are combined.

Run Behavior

- Validation writes only the first 10 sampled prompts into validation_report.json
  to keep the file readable.
- summary.json stores all per-image result metadata collected during the run.
- Contact sheets are created only when images exist.
- STOP_AFTER_CURRENT_IMAGE.txt is checked before a new image, after an image,
  and during long-run chill sleeps.
- Long-run chill only activates when count is above long_run_chill.only_when_count_over.
- Temperature waiting is NVIDIA-focused because it uses nvidia-smi.

Setup and Compatibility

- setup_pipeline.py checks NVIDIA first, then Windows video controller data,
  then rocm-smi on Linux when available.
- setup_pipeline.py writes JSON with ensure_ascii=True on purpose for stronger
  Windows console/editor compatibility.
- upscale_from_metadata.py repairs common mojibake path text before deciding an
  image is missing.
- The metadata upscaler writes a sidecar .metadata.json next to the new upscale.
  Chained upscales use that output_image first in auto mode.
- If Pillow is available, image size is read with Pillow. If not, PNG dimensions
  are read directly from the PNG header.
- tools/rebuild_prompt_pools.py is a developer helper for rebuilding the shipped
  pool files. Normal users do not need it.


License / Usage Note
--------------------

Use this with models, LoRAs, and extensions you are allowed to use. Franchise
module names are inspiration labels for prompt organization; they do not include
model files, LoRA files, checkpoints, or copyrighted assets.
