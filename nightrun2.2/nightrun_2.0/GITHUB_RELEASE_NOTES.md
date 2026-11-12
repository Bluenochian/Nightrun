# Nightrun 2.2 — fewer surprises after midnight

A proper maintenance update to **Nightrun 2.0**, not a repackaged 1.5 build.

You can still leave Forge to do its thing overnight. I'd just rather it didn't
lie about failed renders or waste your time trying to restart Forge over a bad
request. So I fixed those parts.

## Fixed

- **Forge health checks:** HTTP errors (including 404/500) no longer count as a healthy API.
- **Bad requests:** an HTTP 400-series error from Forge now fails with a useful message instead of pointlessly retrying and trying to restart it.
- **LoRA name matching:** exact and alias matches still work; fuzzy matches must have a single unambiguous candidate. An uncertain guess gets skipped instead of loading the wrong model.
- **Batch counts:** `--count 0` and negative image counts now fail early, rather than silently using the default or producing an empty "successful" batch.
- **Honest summaries:** `summary.json` now distinguishes `OK`, `PARTIAL`, `FAILED` and `STOPPED` and records attempted, completed and failed counts.
- **Cooling and stopping:** Stop After Current Image interrupts GPU cooldowns and between-image sleeps. The runner doesn't take an extra break after the last image.
- **Pillow dependency:** no more surprise `pip install` during import. If Pillow isn't installed, raw PNGs still save; install Pillow for metadata stamping and contact sheets.
- **Prompt filter:** repaired a missing `|` in a regex that had accidentally glued the blocked tokens into one impossible word.

## Kept from 2.0

All three prompt engines (Classic / Combinator / Franchise), the rebuilt pool
lists, the curated world modules, metadata replay, standalone upscaling and
existing Windows launchers are still included.

## One thing before you unzip

**Don't overwrite your working install on the first attempt.** Extract
`nightrun_2.2/` beside your older Nightrun folder, keep your
`config.local.json`, run First Setup, Validation and a Dry Test, then try a
small real batch.

The ZIP contains the actual runner and pool files. It does **not** include
checkpoints, model files, LoRAs, Forge, or Ultimate SD Upscale.

Windows is the main launcher target; the Python logic also has offline
regression checks on Python 3.10, 3.12 and 3.13. Those tests do **not** replace
a full overnight run against your particular Forge build and GPU.

[Source and setup](https://github.com/Bluenochian/Nightrun/tree/main/nightrun2.2) ·
[2.0 release — still available](https://github.com/Bluenochian/Nightrun/releases/tag/release2) ·
[1.5 release — also still available](https://github.com/Bluenochian/Nightrun/releases/tag/release)

Now go render something. Your PC can do the babysitting.
