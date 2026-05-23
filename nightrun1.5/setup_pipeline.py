import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


PROFILE_PRESETS = {
    "unknown_safe": {
        "base": {"width": 896, "height": 512, "steps": 35, "steps_min": 24, "steps_max": 35},
        "upscale": {"width": 1792, "height": 1024, "steps": 16, "denoising_strength": 0.2, "tile_width": 320, "padding": 96, "auto_when_base_steps_below": 30},
        "max_random_loras": 1,
        "max_total_loras": 4,
        "sleep_between_images_seconds": 25,
    },
    "low_4_6gb": {
        "base": {"width": 1024, "height": 576, "steps": 45, "steps_min": 28, "steps_max": 45},
        "upscale": {"width": 2048, "height": 1152, "steps": 20, "denoising_strength": 0.22, "tile_width": 384, "padding": 128, "auto_when_base_steps_below": 34},
        "max_random_loras": 2,
        "max_total_loras": 5,
        "sleep_between_images_seconds": 20,
    },
    "balanced_6_8gb": {
        "base": {"width": 1152, "height": 648, "steps": 55, "steps_min": 30, "steps_max": 55},
        "upscale": {"width": 2304, "height": 1296, "steps": 26, "denoising_strength": 0.24, "tile_width": 512, "padding": 144, "auto_when_base_steps_below": 36},
        "max_random_loras": 3,
        "max_total_loras": 7,
        "sleep_between_images_seconds": 15,
    },
    "quality_8_12gb": {
        "base": {"width": 1344, "height": 768, "steps": 65, "steps_min": 30, "steps_max": 65},
        "upscale": {"width": 2688, "height": 1536, "steps": 32, "denoising_strength": 0.26, "tile_width": 512, "padding": 160, "auto_when_base_steps_below": 40},
        "max_random_loras": 3,
        "max_total_loras": 7,
        "sleep_between_images_seconds": 15,
    },
    "high_12gb_plus": {
        "base": {"width": 1536, "height": 864, "steps": 65, "steps_min": 35, "steps_max": 65},
        "upscale": {"width": 3072, "height": 1728, "steps": 35, "denoising_strength": 0.28, "tile_width": 640, "padding": 192, "auto_when_base_steps_below": 42},
        "max_random_loras": 4,
        "max_total_loras": 8,
        "sleep_between_images_seconds": 10,
    },
}


def load_json(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_json(path, data):
    # ASCII JSON keeps non-English paths as \u escapes, which survives old
    # Windows consoles, Git viewers, and non-UTF editors much better.
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True), encoding="utf-8")


def stable_path_text(path):
    return os.fsdecode(os.fsencode(Path(path)))


def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip().strip('"')
    return value or default


def ui(title, color="36"):
    if os.name == "nt":
        return
    print(f"\033[{color}m{title}\033[0m")


def line(char="-", width=56):
    print(char * width)


def step(message):
    print(f"> {message}")


def workflow_dir():
    return Path(__file__).resolve().parent


def detect_repo(start):
    for path in [start, *start.parents]:
        if (path / "launch.py").exists() and (path / "models").exists():
            return path
    if len(start.parents) >= 2:
        return start.parents[1]
    return start


def detect_gpu():
    gpus = []

    # NVIDIA path: most reliable when available.
    try:
        out = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            timeout=10,
        )
    except Exception:
        out = ""

    for line in out.strip().splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 2:
            continue
        try:
            vram_mb = int(parts[1])
        except Exception:
            vram_mb = None
        gpus.append(
            {
                "vendor": "nvidia",
                "name": parts[0],
                "vram_mb": vram_mb,
                "driver": parts[2] if len(parts) > 2 else None,
                "source": "nvidia-smi",
            }
        )

    # Windows fallback: works for NVIDIA/AMD/Intel but AdapterRAM is often missing
    # or capped, so treat it as a hint rather than gospel.
    if not gpus and os.name == "nt":
        ps = (
            "Get-CimInstance Win32_VideoController | "
            "Select-Object Name,AdapterRAM,DriverVersion | ConvertTo-Json -Compress"
        )
        try:
            raw = subprocess.check_output(["powershell", "-NoProfile", "-Command", ps], text=True, timeout=12)
            data = json.loads(raw) if raw.strip() else []
            if isinstance(data, dict):
                data = [data]
            for item in data:
                name = str(item.get("Name") or "Unknown GPU")
                adapter_ram = item.get("AdapterRAM")
                try:
                    vram_mb = int(adapter_ram) // (1024 * 1024) if adapter_ram else None
                except Exception:
                    vram_mb = None
                vendor = "unknown"
                lower_name = name.lower()
                if "nvidia" in lower_name or "geforce" in lower_name or "rtx" in lower_name or "gtx" in lower_name:
                    vendor = "nvidia"
                elif "amd" in lower_name or "radeon" in lower_name:
                    vendor = "amd"
                elif "intel" in lower_name or "arc" in lower_name or "iris" in lower_name:
                    vendor = "intel"
                gpus.append(
                    {
                        "vendor": vendor,
                        "name": name,
                        "vram_mb": vram_mb,
                        "driver": item.get("DriverVersion"),
                        "source": "Win32_VideoController",
                    }
                )
        except Exception:
            pass

    # Linux AMD fallback when rocm-smi exists.
    if not gpus:
        rocm_smi = shutil.which("rocm-smi")
        if rocm_smi:
            try:
                raw = subprocess.check_output([rocm_smi, "--showproductname", "--showmeminfo", "vram"], text=True, timeout=12)
                name = None
                vram_mb = None
                for line in raw.splitlines():
                    lower = line.lower()
                    if "card series" in lower or "product name" in lower:
                        name = line.split(":", 1)[-1].strip()
                    if "total memory" in lower and "vram" in lower:
                        numbers = [token for token in line.replace(":", " ").split() if token.isdigit()]
                        if numbers:
                            vram_mb = int(numbers[-1]) // (1024 * 1024)
                gpus.append({"vendor": "amd", "name": name or "AMD GPU", "vram_mb": vram_mb, "driver": None, "source": "rocm-smi"})
            except Exception:
                pass

    best = None
    if gpus:
        best = sorted(gpus, key=lambda item: item.get("vram_mb") or 0, reverse=True)[0]

    return {
        "available": bool(gpus),
        "name": best.get("name") if best else None,
        "vendor": best.get("vendor") if best else None,
        "vram_mb": best.get("vram_mb") if best else None,
        "driver": best.get("driver") if best else None,
        "source": best.get("source") if best else None,
        "all": gpus,
    }


def choose_profile(vram_mb, requested):
    if requested and requested != "auto":
        return requested
    if not vram_mb:
        return "unknown_safe"
    if vram_mb <= 6144:
        return "low_4_6gb"
    if vram_mb <= 8192:
        return "balanced_6_8gb"
    if vram_mb <= 12288:
        return "quality_8_12gb"
    return "high_12gb_plus"


def find_checkpoints(repo):
    folders = [
        repo / "models" / "Stable-diffusion",
        repo / "models" / "stable-diffusion",
        repo / "models" / "checkpoints",
    ]
    files = []
    for folder in folders:
        if not folder.exists():
            continue
        for ext in ("*.safetensors", "*.ckpt", "*.pt"):
            files.extend(sorted(folder.glob(ext)))
    return files


def checkpoint_exists(repo, checkpoint):
    if not checkpoint:
        return False
    name = Path(str(checkpoint)).name
    for file in find_checkpoints(repo):
        if file.name == name or file.stem == name:
            return True
    return False


def choose_checkpoint(config, repo, requested, interactive):
    if requested:
        return requested
    current = config.get("checkpoint")
    if checkpoint_exists(repo, current):
        return current

    checkpoints = find_checkpoints(repo)
    if not checkpoints:
        return current

    print("")
    print("Checkpoint in config was not found locally.")
    for index, file in enumerate(checkpoints[:20], start=1):
        print(f"  {index}. {file.name}")

    if interactive:
        raw = ask("Checkpoint number to use", "1")
        try:
            choice = max(1, min(len(checkpoints), int(raw)))
        except ValueError:
            choice = 1
        return checkpoints[choice - 1].name

    return checkpoints[0].name


def count_loras(repo, config):
    scan_cfg = config.get("lora_scan", {})
    total = 0
    folders_found = []
    for rel in scan_cfg.get("folders", ["models/Lora"]):
        folder = repo / rel
        if not folder.exists():
            continue
        folders_found.append(rel)
        for ext in ("*.safetensors", "*.pt", "*.ckpt"):
            total += len(list(folder.rglob(ext)))
    return total, folders_found


def inspect_repo(repo):
    checks = {
        "launch_py": (repo / "launch.py").exists(),
        "models_dir": (repo / "models").exists(),
        "venv_python": (repo / "venv" / "Scripts" / "python.exe").exists(),
        "ultimate_sd_upscale": False,
        "api_related_files": [],
    }

    extension_root = repo / "extensions"
    if extension_root.exists():
        for folder in extension_root.iterdir():
            lower = folder.name.lower()
            if "ultimate" in lower and "upscale" in lower:
                checks["ultimate_sd_upscale"] = True

    for pattern in ("*api*.py", "*api*.bat", "*api*.ps1"):
        checks["api_related_files"].extend(str(path.relative_to(repo)) for path in repo.glob(pattern))

    return checks


def warn_about_environment(repo, gpu, repo_checks, checkpoint_found, lora_count):
    warnings = []
    if not repo_checks["launch_py"]:
        warnings.append("Forge launch.py was not found. Point setup at the Forge/Forge-Neo root folder.")
    if not repo_checks["models_dir"]:
        warnings.append("models folder was not found under the repo.")
    if not repo_checks["venv_python"]:
        warnings.append("repo\\venv\\Scripts\\python.exe was not found. The .bat launchers expect a Forge venv.")
    if not checkpoint_found:
        warnings.append("Configured checkpoint was not found locally. Generation will fail until the checkpoint name matches an installed model.")
    if lora_count == 0:
        warnings.append("No local LoRA files were found. The workflow will skip LoRAs until models/Lora is populated.")
    if not repo_checks["ultimate_sd_upscale"]:
        warnings.append("Ultimate SD Upscale extension was not detected. FULL upscale and metadata upscale need that script.")
    if not gpu.get("available"):
        warnings.append("No GPU was detected. Setup used the unknown_safe profile; CPU-only generation will be extremely slow.")
    if gpu.get("vendor") in ("amd", "intel"):
        warnings.append(f"{gpu.get('vendor').upper()} GPU detected. Forge support depends on that system's backend; setup used VRAM only for sizing.")
    return warnings


def apply_profile(config, profile_name):
    preset = PROFILE_PRESETS[profile_name]
    result = copy.deepcopy(config)

    result.setdefault("base", {}).update(preset["base"])
    result.setdefault("upscale", {}).update(preset["upscale"])
    result["max_random_loras"] = preset["max_random_loras"]
    result["max_total_loras"] = preset["max_total_loras"]
    result["sleep_between_images_seconds"] = preset["sleep_between_images_seconds"]
    return result


def detect_python(repo):
    venv_python = repo / "venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    return shutil.which("python") or shutil.which("py") or "python"


def powershell_single(value):
    return "'" + str(value).replace("'", "''") + "'"


def desktop_dir():
    if os.name == "nt":
        try:
            raw = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command", "[Environment]::GetFolderPath('Desktop')"],
                text=True,
                timeout=10,
            ).strip()
            if raw:
                return Path(raw)
        except Exception:
            pass
    return Path.home() / "Desktop"


def create_windows_shortcut(name, target, icon=None, working_dir=None):
    if os.name != "nt":
        return {"name": name, "created": False, "reason": "shortcuts are only created automatically on Windows"}

    icon_path = Path(icon) if icon else None

    script = [
        "$shell = New-Object -ComObject WScript.Shell",
        "$desktop = [Environment]::GetFolderPath('Desktop')",
        f"$shortcutPath = Join-Path $desktop {powershell_single(name + '.lnk')}",
        "$shortcut = $shell.CreateShortcut($shortcutPath)",
        f"$shortcut.TargetPath = {powershell_single(target)}",
        f"$shortcut.WorkingDirectory = {powershell_single(working_dir or Path(target).parent)}",
    ]
    if icon_path and icon_path.exists():
        script.append(f"$shortcut.IconLocation = {powershell_single(str(icon_path))}")
    script.extend(
        [
            "$shortcut.Save()",
            "Write-Output $shortcutPath",
        ]
    )

    try:
        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "; ".join(script)],
            text=True,
            stderr=subprocess.STDOUT,
            timeout=20,
            encoding="utf-8",
        )
        shortcut_path = output.strip().splitlines()[-1] if output.strip() else str(desktop_dir() / f"{name}.lnk")
        return {"name": name, "created": True, "path": shortcut_path, "icon": stable_path_text(icon_path) if icon_path and icon_path.exists() else None}
    except subprocess.CalledProcessError as exc:
        return {"name": name, "created": False, "reason": exc.output.strip()}
    except Exception as exc:
        return {"name": name, "created": False, "reason": str(exc)}


def remove_legacy_shortcut(name):
    if os.name != "nt":
        return
    script = [
        "$desktop = [Environment]::GetFolderPath('Desktop')",
        f"$shortcutPath = Join-Path $desktop {powershell_single(name + '.lnk')}",
        "if (Test-Path -LiteralPath $shortcutPath) { Remove-Item -LiteralPath $shortcutPath -Force }",
    ]
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "; ".join(script)],
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20,
            check=False,
        )
    except Exception:
        pass


def create_desktop_shortcuts(wf):
    icon_dir = wf / "assets" / "icons"
    shortcuts = [
        {
            "name": "Nightrun",
            "target": wf / "Run Nightrun BASE only.bat",
            "icon": icon_dir / "nightrun.ico",
        },
        {
            "name": "Upscaler",
            "target": wf / "Run 2x Upscale From Metadata.bat",
            "icon": icon_dir / "nightrun_upscaler.ico",
        },
    ]
    results = []
    remove_legacy_shortcut("Overnight of the base model")
    remove_legacy_shortcut("Overnight Randomizer")
    remove_legacy_shortcut("Run Overnight BASE only")
    for item in shortcuts:
        results.append(
            create_windows_shortcut(
                item["name"],
                item["target"],
                icon=item["icon"],
                working_dir=wf,
            )
        )
    return results


def setup(args):
    wf = workflow_dir()
    base_config_path = wf / args.base_config
    config = load_json(base_config_path)

    print("")
    ui("Nightrun Setup", "36")
    line("=")
    step("Detecting Forge folder, GPU, VRAM, models, and extensions.")

    repo_default = detect_repo(wf)
    interactive = not args.non_interactive

    repo = Path(args.repo).expanduser() if args.repo else repo_default
    if interactive:
        repo = Path(ask("Forge/Forge-Neo repo folder", str(repo))).expanduser()
    repo = repo.resolve()

    output_default = repo / "test-renders"
    output_dir = Path(args.output_dir).expanduser() if args.output_dir else output_default
    if interactive:
        output_dir = Path(ask("Output folder", str(output_dir))).expanduser()
    output_dir = output_dir.resolve()

    step("Scanning GPU and VRAM.")
    gpu = detect_gpu()
    profile = choose_profile(gpu.get("vram_mb"), args.profile)
    step(f"Selected profile: {profile}")
    local_config = apply_profile(config, profile)
    step("Checking checkpoint and LoRA folders.")
    local_config["checkpoint"] = choose_checkpoint(local_config, repo, args.checkpoint, interactive)
    if args.count is not None:
        local_config["count"] = args.count

    local_config["paths"] = {
        "repo": stable_path_text(repo),
        "workflow_dir": stable_path_text(wf),
        "output_dir": stable_path_text(output_dir),
    }
    local_config["setup"] = {
        "configured_at": datetime.now().isoformat(timespec="seconds"),
        "profile": profile,
        "gpu": gpu,
        "python": detect_python(repo),
        "base_config": stable_path_text(base_config_path),
    }

    lora_count, lora_folders = count_loras(repo, local_config)
    repo_checks = inspect_repo(repo)
    checkpoint_found = checkpoint_exists(repo, local_config.get("checkpoint"))
    warnings = warn_about_environment(repo, gpu, repo_checks, checkpoint_found, lora_count)
    report = {
        "repo": stable_path_text(repo),
        "workflow_dir": stable_path_text(wf),
        "output_dir": stable_path_text(output_dir),
        "profile": profile,
        "gpu": gpu,
        "checkpoint": local_config.get("checkpoint"),
        "checkpoint_found": checkpoint_found,
        "lora_count": lora_count,
        "lora_folders_found": lora_folders,
        "repo_checks": repo_checks,
        "warnings": warnings,
        "config_written": stable_path_text(wf / args.output_config),
    }

    print("")
    print("Setup summary")
    line("-")
    for key, value in report.items():
        print(f"{key}: {value}")
    if warnings:
        print("")
        print("Warnings")
        print("--------")
        for warning in warnings:
            print(f"- {warning}")

    if args.dry_run:
        print("")
        print("Dry run only. No config.local.json written.")
        return report

    output_dir.mkdir(parents=True, exist_ok=True)
    save_json(wf / args.output_config, local_config)

    shortcut_results = []
    if not args.no_shortcuts:
        shortcut_results = create_desktop_shortcuts(wf)
        report["shortcuts"] = shortcut_results

    save_json(wf / "setup_report.json", report)

    print("")
    print(f"Wrote {wf / args.output_config}")
    if shortcut_results:
        print("")
        print("Desktop shortcuts")
        print("-----------------")
        for result in shortcut_results:
            if result.get("created"):
                print(f"Created: {result.get('name')} -> {result.get('path')}")
            else:
                print(f"Skipped/failed: {result.get('name')} ({result.get('reason')})")
    print("Run the validation or dry-test .bat next.")
    return report


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stdin.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--profile", choices=["auto", *PROFILE_PRESETS.keys()], default="auto")
    parser.add_argument("--checkpoint", default=None)
    parser.add_argument("--count", type=int, default=None)
    parser.add_argument("--base-config", default="config.json")
    parser.add_argument("--output-config", default="config.local.json")
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--no-shortcuts", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    setup(args)


if __name__ == "__main__":
    main()
