#!/usr/bin/env python3
"""Package the maintained modular Nightrun engine as a Linux-only edition."""
from __future__ import annotations

import argparse
import hashlib
import shutil
import tarfile
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "nightrun2.3" / "nightrun_2.3"
LINUX = ROOT / "linux-native"
FILES = ("nightrun.py", "config.json", "requirements.txt")
DIRECTORIES = ("modules", "pools", "tools")


def replace_exact(path: Path, original: str, replacement: str) -> None:
    content = path.read_text(encoding="utf-8")
    if content.count(original) != 1:
        raise RuntimeError(f"Unexpected source in {path.name}: {original[:60]!r}")
    path.write_text(content.replace(original, replacement), encoding="utf-8")


def create(output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    package = output / "nightrun-linux"
    if package.exists():
        shutil.rmtree(package)
    package.mkdir()
    if not (SOURCE / "modules/nightrun_runtime.py").is_file():
        raise RuntimeError("Missing shared modular Nightrun engine")
    for file in FILES:
        shutil.copy2(SOURCE / file, package / file)
    for directory in DIRECTORIES:
        shutil.copytree(
            SOURCE / directory, package / directory,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
    for file in ("nightrun", "install.sh", "uninstall.sh", "README.md", "RELEASE_NOTES.md"):
        shutil.copy2(LINUX / file, package / file)
        if file.endswith(".sh") or file == "nightrun":
            (package / file).chmod(0o755)

    # Live stop flags and setup reports belong to XDG state, not the code folder.
    replace_exact(
        package / "modules/nightrun_runtime.py",
        'stop_file = workflow_dir / "STOP_AFTER_CURRENT_IMAGE.txt"',
        'stop_file = Path(os.environ.get("NIGHTRUN_STOP_FILE", str(workflow_dir / "STOP_AFTER_CURRENT_IMAGE.txt")))',
    )
    replace_exact(
        package / "modules/setup_pipeline.py",
        'save_json(wf / "setup_report.json", report)',
        'save_json(Path(os.environ.get("NIGHTRUN_SETUP_REPORT", str(wf / "setup_report.json"))), report)',
    )

    icons = package / "assets/icons"
    icons.mkdir(parents=True)
    for old, new in (
        ("nightrun.ico", "nightrun.png"),
        ("nightrun_upscaler.ico", "nightrun-upscaler.png"),
    ):
        with Image.open(SOURCE / "assets/icons" / old) as ico:
            art = ico.convert("RGBA")
            art.thumbnail((256, 256), Image.Resampling.LANCZOS)
            canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
            canvas.alpha_composite(art, ((256 - art.width) // 2, (256 - art.height) // 2))
            canvas.save(icons / new, format="PNG")

    names = [p for p in package.rglob("*") if p.is_file()]
    assert not any(p.suffix.lower() in (".bat", ".ico", ".exe") for p in names)
    assert (package / "modules/franchise_catalog.py").exists()
    assert (package / "modules/nightrun_runtime.py").exists()
    assert (package / "pools/genre.txt").exists()

    zip_path = output / "nightrun-linux-native.zip"
    tar_path = output / "nightrun-linux-native.tar.gz"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in sorted(names):
            archive.write(file, file.relative_to(output))
    with tarfile.open(tar_path, "w:gz") as archive:
        for file in sorted(names):
            archive.add(file, arcname=file.relative_to(output), recursive=False)
    with zipfile.ZipFile(zip_path) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("ZIP integrity verification failed")
    sha_file = output / "SHA256SUMS"
    hashes = {
        name.name: hashlib.sha256(name.read_bytes()).hexdigest()
        for name in (zip_path, tar_path)
    }
    sha_file.write_text("".join(f"{digest}  {name}\n" for name, digest in hashes.items()))
    return {"files": len(names), "zip": zip_path, "tar": tar_path, "hashes": hashes}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist-linux-native")
    args = parser.parse_args()
    result = create(args.output)
    print(f"Linux Native: {result['files']} files (Windows launchers excluded)")
    for filename, digest in result["hashes"].items():
        print(f"{digest}  {filename}")
