<p align="center">
  <img width="4270" height="1232" alt="Nightrun banner" src="https://github.com/user-attachments/assets/633634ea-5840-4feb-b476-cc98167ab258"/>
</p>

<p align="center">
  <strong>Leave Forge running overnight. You can go do something else.</strong>
</p>

<p align="center">
  <a href="https://github.com/Bluenochian/Nightrun/releases/tag/v2.2"><strong>Download Nightrun 2.2</strong></a> ·
  <a href="#getting-started">Getting started</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="#whats-new-in-22">2.2 fixes</a> ·
  <a href="#versions-and-old-downloads">Old versions</a>
</p>

---

## What is Nightrun?

I made it because I wanted to leave Stable Diffusion Forge running while I was asleep. That sounded great. Staying up to babysit prompts, LoRAs and GPU temperatures? Not so much.

Nightrun builds prompts from editable pools, sends local batches to Forge / Forge-Neo, remembers what it generated, and can replay old metadata for upscaling. It can pause for GPU cooling and stop cleanly between images. Pretty simple idea; the implementation got a bit out of hand, as these things do.

**2.2 is a maintenance release built on the real 2.0 code.** It keeps the three prompt engines, curated franchise catalog and the rebuilt text pools. I didn't rename the old 1.5 runner and pretend it was an update.

## Getting started

**Windows + Forge / Forge-Neo** is the main supported setup for the included `.bat` launchers. You need Python, `requests`, a working local Forge API and your own checkpoint. Pillow is recommended for PNG metadata stamping and contact sheets.

Download [Nightrun 2.2](https://github.com/Bluenochian/Nightrun/releases/tag/v2.2), extract it and put the folder **two levels below your Forge root**:

```text
YourForgeFolder/
├── venv/
└── workflows/
    └── nightrun_2.2/
        ├── nightrun.py
        ├── config.json
        ├── modules/
        ├── pools/
        └── Run First Setup.bat
```

The launchers expect that layout. They go two folders up to find `venv\Scripts\python.exe`. If you already have 1.5 or 2.0 installed, **keep that folder** until 2.2 is working. Dont overwrite your only good config while testing an update.

Run these in order:

1. **Run First Setup.bat** — detect your Forge folder, GPU/VRAM profile, checkpoint and output path; write `config.local.json`.
2. **Run Validation Stress Test.bat** — check pools and LoRAs without generating images.
3. **Run One DRY TEST.bat** — write sample prompts/metadata before spending GPU time.
4. **Run Nightrun BASE only.bat** or **Run Nightrun FULL upscale.bat** — start a real batch.
5. **Stop After Current Image.bat** — stop safely rather than killing Forge mid-render.

The [short 2.2 guide](nightrun2.2/nightrun_2.0/README.txt) has all command-line options and the metadata-upscaling walkthrough.

## How it works

| Part | What's going on |
| --- | --- |
| **Classic** | Builds prompts from the normal editable text pools. |
| **Combinator** | Adds controlled variations without throwing every random idea into one image. |
| **Franchise** | Picks a curated world module, keeping its outfits, scenery and props together. |
| **LoRA matching** | Scans local folders, resolves names and aliases, and respects stack limits. |
| **Selection memory** | Reduces repetition within a run; doesn't create a permanent history database. |
| **Batch runner** | Sends `txt2img` and optional `img2img` jobs to the local Forge API. |
| **Metadata replay** | Keeps seeds, prompts and choices so you can upscale or reconstruct later. |
| **Cooldowns** | Waits when the GPU is hot (NVIDIA `nvidia-smi`); checks for stop signals between work. |

The `pools/` files are plain text. Edit the categories you care about and leave the rest alone. The `config.json` in the release is a shared starting point; **your** folders and model choices belong in `config.local.json`. Don't commit that file.

LoRAs and checkpoints are not included. If a LoRA gets skipped, check the local filename or alias rather than assuming Nightrun found the right one. Some names are just too similar, and guessing wrong is worse than skipping.

## Run modes

From inside `nightrun_2.2/`:

```powershell
python nightrun.py --mode validate --count 100 --config config.local.json
python nightrun.py --mode dry-run --count 5 --config config.local.json
python nightrun.py --mode base --count 20 --config config.local.json
python nightrun.py --mode full --count 20 --config config.local.json
```

The main outputs are numbered base/upscale PNGs, a prompt text file and metadata for each attempt, plus a batch `summary.json` and `run.log`. A failed image isn't magically a successful run because the script reached the end.

To upscale an old image from metadata, drag its `*_metadata.json` onto **Run 2x Upscale From Metadata.bat**, or use:

```powershell
python modules/upscale_from_metadata.py "D:\renders\0001_metadata.json" --config config.local.json --scale 2
```

The upscaler can recreate a missing base image from saved metadata. Use `--no-create-if-missing` when you only want to use files that already exist.

## What's new in 2.2

Mostly fixes. I know, glamorous.

- **Honest Forge health checks.** A 404/500 is not a healthy API; 400-series generation errors are reported without pointless restart attempts.
- **LoRA matches are less reckless.** Ambiguous fuzzy matches get skipped rather than selecting an unrelated model.
- **No fake success counts.** Zero/negative batch counts are rejected; `summary.json` distinguishes failed, partial, stopped and completed runs.
- **Stopping means stopping.** Stop After Current Image now interrupts thermal pauses and between-image sleeps, and there is no unnecessary sleep after the final image.
- **No silent pip installs.** Pillow isn't installed behind your back at import time. Without it, raw PNG saving still works but the extra image metadata/contact sheet may be unavailable.
- **Fixed a busted prompt-filter regex.** Some strings had been concatenated instead of alternated. Yeah, that's not what I intended.
- **Offline regression checks.** Python 3.10, 3.12 and 3.13 tests cover the main failure paths. A real Forge/Windows run still needs to be tested on your own setup.

The original 2.0 prompt pools and franchise catalog are kept as they were. I wasn't about to gut the creative bits for a maintenance update.

## If something's wrong

| Problem | First thing to check |
| --- | --- |
| Launcher can't find a path | Nightrun must sit two levels below the Forge root with `venv/` in that root. |
| Checkpoint missing | Run First Setup again or edit `config.local.json`. |
| LoRA skipped | Check filenames and `lora_scan.aliases`; ambiguous partial names are deliberately skipped. |
| Forge won't respond | Make sure Forge is running with its API on `127.0.0.1:7860`. |
| FULL upscale fails | Enable Ultimate SD Upscale in Forge and test one image first. |
| CUDA / VRAM errors | Lower resolution, LoRA count or batch settings; don't ignore the GPU profile. |
| Image disappeared or failed | Look in `run.log`, `summary.json` and the per-image metadata. |

Nightrun doesn't hide browsing history or upload images to a hosted service; this is a **local** Forge automation tool. You are responsible for the checkpoints, LoRAs and outputs you use. The sensual-layer pool can include adult-oriented entries and is configurable; set its chance to `0` for SFW-only runs.

## Versions and old downloads

| Version | Where | Notes |
| --- | --- | --- |
| **2.2 — current** | [Download v2.2](https://github.com/Bluenochian/Nightrun/releases/tag/v2.2) | Bug fixes on the modular 2.0 engine |
| **2.0** | [Previous release](https://github.com/Bluenochian/Nightrun/releases/tag/release2) | Original modular engine, three prompt builders and rebuilt pools |
| **1.5** | [Original release](https://github.com/Bluenochian/Nightrun/releases/tag/release) | Earlier monolithic runner, still here |
| **3.0 dashboard prototype** | [nightrun_web.py](nightrun_web.py) | UI experiment; its generation loop **simulates** progress, not real render jobs |

The 2.2 source is in [`nightrun2.2/`](nightrun2.2/), imported from the actual 2.0 release and patched. The older `nightrun1.5/` folder stays in this repository for anyone still using it.

Don't mistake the dashboard prototype for a real batch runner. Seriously. Use Nightrun 2.2 for overnight rendering.

---

<p align="center"><strong>🌙 Your PC can do the babysitting.</strong></p>
