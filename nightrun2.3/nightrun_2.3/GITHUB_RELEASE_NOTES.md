# Nightrun 2.3 — Linux joins the party

Claude started the Linux port with matching shell scripts, and I kept going.
The early version worked for straightforward paths, but KDE shortcuts,
odd install locations and Forge's launch environment needed more attention.

This version contains the **actual modular 2.0/2.2 engine**, not a dressed-up
copy of 1.5. All three prompt engines, rebuilt pools, curated world modules,
LoRA matching and metadata upscaling are kept.

## What's new

- Nine Linux shell launchers. All nine Windows `.bat` launchers are preserved.
- Linux can create KDE/GNOME desktop shortcuts with properly quoted paths
  (including directories containing spaces) and converted PNG icons.
- Forge startup selects the actual Forge virtualenv and uses `launch.py --api`
  on Linux without forcing the old Windows CUDA flags.
- If Forge exits during startup, Nightrun stops trying and points to the logs.
- The new Linux scripts share one small helper, support Python/repo overrides,
  and prevent two concurrent batches from clobbering each other's stop signal.
- The 2.2 error handling, safe batch status and stop-aware cooldown fixes
  remain in place.

## Before installing

Extract `nightrun_2.3` under `YourForgeFolder/workflows/`, with your Forge
`venv/` two levels above. Linux needs Bash, util-linux `flock`, Python 3.10+
and `requests`. Pillow is recommended for the image extras and desktop icon
conversion. Keep your old installation until you've confirmed 2.3 works.

Try `run-first-setup.sh`, `run-validation-stress-test.sh`, then
`run-one-dry-test.sh` before running a real batch. The Windows setup
instructions and launchers have not been removed.

**Testing boundaries:** Linux unit tests and a one-image dry-run smoke test
passed. CI also checks Python syntax and regression behavior. A full Linux
Forge+GPU run, different driver backends and actual graphical desktop
interactions are **not yet verified**.

Earlier downloads stay available: [2.2](https://github.com/Bluenochian/Nightrun/releases/tag/v2.2),
[2.0](https://github.com/Bluenochian/Nightrun/releases/tag/release2), and
[1.5](https://github.com/Bluenochian/Nightrun/releases/tag/release).

If it fails on your distro, send the error and a redacted log. I'd rather fix
the actual problem than pretend all Linux installs are identical.
