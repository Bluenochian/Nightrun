# Nightrun 1.5 Release Notes

Portable Forge / Forge-Neo prompt generation, metadata replay, and upscale pipeline.

## Release Highlights

- Project renamed and surfaced as `Nightrun`.
- Main CLI entrypoint is now `nightrun.py`.
- Internal engine module is now `nightrun_engine.py`.
- Output folders now use the `nightrun-YYYYMMDD-HHMMSS` prefix.
- Desktop shortcuts use the new bundled `nightrun.ico` and `nightrun_upscaler.ico`.
- Old replaced launchers and old Forge icon files were removed from the package.
- Legacy empty-folder cleanup still recognizes old `overnight-randomizer-*` output folders so upgraded users can clean failed/dry runs safely.

## Generator Changes

- Added a one-file `franchise_catalog.py` system instead of folder-based modules.
- Added config controls for enabling/disabling franchise modules by module ID, source name, or label pattern.
- Added chances for core franchise fields so users can tune how much each module controls.
- Added `genre_core.txt` and `genre_root.txt` with short classic genres and named subgenres.
- Added `exclusive_group` support so related pools, like genre pools, do not stack into noisy genre soup.
- Added prompt concept memory to reduce repeated themes across a run.
- Added stronger candle/candlelight repeat penalties.
- Added stronger blue/cyan repetition pressure and low heterochromia chance.
- Added final `prompt_cleanup` guardrails for repeated comma tags, recurring concept-family caps, and compact SD-style prompt length limits.
- Added prompt map logging with colored categories.
- Added `nightrun-*` run folder naming through config.

## Setup / Portability

- First setup now preserves existing tuned `config.local.json` generation settings by default.
- Added `--reset-local` for intentionally rebuilding local settings from a VRAM profile.
- Added a stronger `tuned_6gb` VRAM profile for 6 GB GPUs.
- 4-5 GB systems remain on the safer low profile.
- Setup creates the `Nightrun` and `Upscaler` desktop shortcuts on Windows.
- Paths are written as portable UTF-safe JSON text to avoid non-English path corruption.

## Upscaler

- Metadata upscaler keeps using an existing upscale as the source when chaining.
- Missing base images can still be recreated from metadata when needed.
- Scale factors such as 2x, 3x, 4x, or custom dimensions are supported.

## Prompt Quality / Debugging

- Rebuilt and purged shipped prompt pools for local Stable Diffusion style prompting: shorter comma tags, fewer bloated lines, and less overpopulation for its own sake.
- Added hand-curated front entries for major pools: concepts, characters, outfits, environments, poses, expressions, lighting, camera, styles, effects, composition, equipment, and palettes.
- Reworked concept and character pools back to direct SD-readable archetypes/descriptors instead of poetic title mashups.
- Clarified pool ownership: `fixed_prefix` owns subject identity, concept owns role/archetype, character owns expression/posture, clothing owns outfit, and environment owns scene.
- Added redundant subject-term stripping so pool lines do not repeat `woman`, `girl`, `female`, or `lady` after the fixed prefix already established the subject.
- Added a configurable curated-top weighting system so hand-picked pool entries appear more often without disabling the full pool.
- Rebalanced recurring motif families so candles, vampire/gothic themes, blue/cyan palettes, rose/moon details, and similar strong motifs appear less often.
- Added hundreds of short genre/subgenre roots, including punk derivatives, weird fiction, new weird, cli-fi, wuxia, xianxia, LitRPG, progression fantasy, ecological horror, analog horror, liminal horror, vaporwave, mecha, kaiju, and more.
- Prompt variety analyzer now reports repeated concept families, including candles, gothic, vampire, blue/cyan, sci-fi, and wasteland motifs.
- Analyzer still reports repeated colors, poses, cameras, outfits, environments, styles, modules, exact prompt repeats, and repeated comma tags.
- Validation stress test checks pool files, prompt formatting, LoRA resolution, and generated prompt samples without rendering images.

## First Run

1. Put this folder under `sd-webui-forge-neo/workflows/nightrun1.5`.
2. Run `Run First Setup.bat`.
3. Run `Run Validation Stress Test.bat`.
4. Run `Run One DRY TEST.bat`.
5. Start `Run Nightrun BASE only.bat` or `Run Nightrun FULL upscale.bat`.

Do not upload `config.local.json`, render outputs, or personal model files.
