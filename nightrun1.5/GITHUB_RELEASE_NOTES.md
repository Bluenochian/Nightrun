# Nightrun for Forge

Portable Forge/Forge-Neo prompt randomizer and metadata replay pipeline.

## What It Is

- Nightrun prompt-pool randomizer for anime/dark fantasy image batches.
- Forge API runner for base images and optional Ultimate SD Upscale passes.
- Metadata-first replay: every image writes prompt/seed/settings JSON.
- Drag-and-drop 2x metadata upscaler that can recreate a missing base image before upscaling.
- First-run setup that detects paths, GPU/VRAM, checkpoint availability, LoRA folders, and writes `config.local.json`.
- First-run setup also creates Desktop shortcuts for the base runner and metadata upscaler on Windows.
- Chained metadata upscales use the latest existing output image by default instead of recreating the original base.

## Why It Exists

Shared Stable Diffusion workflows often fail because:

- hardcoded local paths do not exist on another PC,
- checkpoints or LoRA filenames differ from CivitAI display names,
- workflow graphs depend on missing custom nodes or extensions,
- VRAM assumptions are too high for the target machine,
- metadata cannot be replayed after an image is moved or deleted.

This pack avoids most of that by using Forge's API, plain `.txt` pools, local LoRA scanning, conservative VRAM profiles, and metadata replay.

## First Run

1. Put this folder under `sd-webui-forge-neo/workflows/nightrun1.5`.
2. Run `Run First Setup.bat`.
3. Use the Desktop shortcuts it creates, or check warnings in the console / `setup_report.json`.
4. Run `Run Validation Stress Test.bat`.
5. Run `Run One DRY TEST.bat`.
6. Start `Run Nightrun BASE only.bat` or `Run Nightrun FULL upscale.bat`.
