Nightrun 2.2 — Forge / Forge-Neo
================================

I made Nightrun because leaving Forge running all night sounded great until
I realised that meant babysitting prompts, LoRAs and GPU temperatures too.
This runs local image batches while you're doing literally anything else.

It builds prompts from editable text pools, talks to Forge's local API, saves
metadata, and can upscale old images later. Version 2.2 is mostly a cleanup
and reliability update to the actual 2.0 engine. The big 2.0 pool rebuild,
three prompt engines and franchise catalog are still here.

For the people who just want to use the damn thing
--------------------------------------------------

Place the *nightrun_2.2* folder two levels below the Forge root:

  YourForgeFolder/
    venv/
    workflows/
      nightrun_2.2/
        nightrun.py
        config.json
        modules/
        pools/
        Run First Setup.bat

If you already have a 2.0 folder, keep it until 2.2 is working. You don't
need to overwrite your previous setup.

Run these Windows launchers in order:

  1. Run First Setup.bat
  2. Run Validation Stress Test.bat
  3. Run One DRY TEST.bat
  4. Run Nightrun BASE only.bat (or FULL upscale if you need it)
  5. Stop After Current Image.bat when you want a clean stop

The launchers assume Forge has venv/Scripts/python.exe. First Setup can fall
back to system Python, but the rendering launchers expect the Forge venv.
Dont skip the dry test on a fresh setup. A two-minute check beats an empty
overnight folder.

What you need
-------------

- Windows for the provided .bat files; the Python code can be run directly.
- Stable Diffusion Forge / Forge-Neo with a working local API.
- Python 3.10+ with requests installed.
- Pillow for the PNG metadata stamp and image contact sheets. The runner can
  still save raw PNGs if Pillow is missing; it won't secretly pip-install it.
- A local checkpoint. LoRAs and Ultimate SD Upscale are optional, depending
  on your chosen generation mode.
- Enough GPU memory for the resolution and model you're asking Forge to run.

Nightrun does not download checkpoints, LoRAs, or image models for you.

Modes and commands
------------------

From the nightrun_2.2 folder:

  python nightrun.py --mode validate --count 100 --config config.local.json
  python nightrun.py --mode dry-run --count 5 --config config.local.json
  python nightrun.py --mode base --count 20 --config config.local.json
  python nightrun.py --mode full --count 20 --config config.local.json

validate  Checks pools, local LoRA resolution and prompt construction;
          creates validation_report.json without rendering.
dry-run   Writes sample prompts and metadata. Doesn't call the Forge
          image-generation endpoint.
base      Generates base images; optional low-step auto-upscale can still run
          if the config enables it.
full      Base renders plus scheduled or conditional upscale passes.

--count must be positive. --seed sets the root seed; image N uses seed+N.
If you want a different config, pass its path with --config.

A brief map of the files
------------------------

  config.json                Public defaults
  config.local.json          Your local paths, checkpoint, GPU settings
  nightrun.py                Entry point; modules/ contains the working code
  modules/setup_pipeline.py  First-run detection and configuration
  modules/nightrun_runtime.py  Main Forge/prompt/batch implementation
  modules/upscale_from_metadata.py  Metadata replay/upscaling
  pools/*.txt                Editable prompt fragments
  STOP_AFTER_CURRENT_IMAGE.txt  Created by the Stop launcher

Keep config.local.json off GitHub; it contains your actual filesystem paths.
The main config is shareable and shouldnt have your machine-specific settings.

Prompts, LoRAs and worlds
------------------------

Classic samples the normal pools. Combinator takes those choices and mixes
in controlled transformations. Franchise mode picks one of the curated world
modules so outfits, scenery, people and props belong together. You can tune
their routing weights using prompt_engines in config.json.

The editable pools live in pools/*.txt. One line is one possible fragment;
blank lines and lines beginning with # are ignored. Pick counts, chances,
curated weighting and selection memory are configurable. Selection memory
only lasts for the current run and discourages repeated choices.

LoRA names come from installed folders and aliases. Exact matches win.
Unclear partial matches are skipped instead of grabbing a random similarly
named file. If a LoRA gets skipped, check lora_scan.aliases or the actual
filename first. The LoRA cap still applies to the final tag list.

World modules are in modules/franchise_catalog.py. The 2.0 catalog and the
three prompt engines are kept in 2.2; this update did not throw away your
creative options. Edit the catalog only if you want to make your own worlds.

The sensual_layer pool can include adult-oriented styling and is enabled in
the shipped config. For an SFW-only run, set that pool's chance to 0 in your
local config. It is separate from the normal character and world systems.

Outputs and replay
------------------

Runs use folders named like nightrun-YYYYMMDD-HHMMSS. Depending on the mode:

  0001_base_WIDTHxHEIGHT.png
  0001_upscale_WIDTHxHEIGHT.png
  0001_prompt.txt
  0001_metadata.json
  summary.json
  run.log
  contact_sheet.jpg
  validation_report.json

Metadata records prompts, seeds, chosen layers, LoRAs, filenames and status.
If something fails, summary.json now says FAILED or PARTIAL rather than
claiming the entire batch was fine. A clean stop is marked STOPPED.

For an old render, drag its *_metadata.json onto
"Run 2x Upscale From Metadata.bat", or run:

  python modules/upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --scale 2

Use --source base to prefer the original base file, --source upscale to
prefer a previous upscale, or auto (the default) for the most advanced
available image. When the base image is missing, the upscaler can recreate
it from metadata first. Add --no-create-if-missing to prevent that.

The upscaler also supports --width, --height, --steps, --denoise, --tile-width,
--padding, --seed and --dry-run. Start with 2x before asking for enormous
outputs. VRAM still has a say in this.

Cooling, stopping and cleaning
------------------------------

Temperature pauses use NVIDIA's nvidia-smi. If the GPU exceeds the configured
threshold, Nightrun waits until it cools. The stop file now interrupts those
waits and between-image breaks, too. It wont forcibly interrupt an image
currently being generated, though.

Long-run VRAM chill and between-image rests are configurable. 2.2 no longer
sleeps after the *last* image. Not much point in making you wait for nothing.

Empty run cleanup only considers recognised run folders; read its prompts
carefully. If you want to keep dry-run reports, disable cleanup or use
--cleanup-empty never. Keeping your own image backups is a good idea.

If something goes weird
-----------------------

- "Cannot find the path": your folder isn't two levels below Forge's root.
- Missing checkpoint: rerun setup or select an installed checkpoint.
- Missing LoRA: fix the filename/alias. An ambiguous guess is now skipped.
- Forge API not responding: start Forge with --api and confirm port 7860.
  A 400 request error points to bad settings, not a reason to restart Forge.
- FULL upscale fails: confirm Ultimate SD Upscale is installed and enabled.
- GPU not detected: setup may pick a conservative profile; NVIDIA thermal
  monitoring needs nvidia-smi.
- Failed render: inspect run.log and summary.json before restarting a batch.
- Old metadata image missing: use the metadata upscaler and let it recreate
  the original, unless --no-create-if-missing was set.

The separate 3.0 dashboard in the repository is still a prototype with
simulated generation. Use THIS runner when you want real images.

And that's it. It was meant to save time, not become a second full-time job.

Copyright and assets
--------------------

Models, checkpoints and LoRAs belong to their respective authors and are not
bundled here. Make sure you're allowed to use whichever files you install.
Nightrun is provided as-is; some Forge versions and extensions will behave
differently. Report what actually broke (with private paths redacted).
