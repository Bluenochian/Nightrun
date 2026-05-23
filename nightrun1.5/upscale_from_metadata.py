import argparse
import copy
import json
import re
import struct
from pathlib import Path

import nightrun as machine


def load_json(path):
    with path.open("r", encoding="utf-8-sig", errors="replace") as f:
        return json.load(f)


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def repair_mojibake(text):
    if not text:
        return text
    for encoding in ("cp1252", "latin-1"):
        try:
            repaired = str(text).encode(encoding).decode("utf-8")
        except UnicodeError:
            continue
        if repaired != text:
            return repaired
    return text


def existing_path(raw):
    if not raw:
        return None

    candidates = [str(raw), repair_mojibake(raw)]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return path
    return None


def metadata_stem(meta, meta_path):
    if isinstance(meta.get("index"), int):
        return f"{meta['index']:04d}"
    name = meta_path.stem
    if name.endswith(".metadata"):
        return name[: -len(".metadata")]
    return name[:-9] if name.endswith("_metadata") else name


def source_candidates(meta, meta_path, source_mode):
    stem = metadata_stem(meta, meta_path)
    folder = meta_path.parent
    candidates = []

    # Metadata created by this 2x tool describes output_image. When users chain
    # upscales, that existing output must be the source, not the original base.
    if source_mode in ("auto", "upscale"):
        candidates.append(meta.get("output_image"))

    if source_mode == "auto":
        candidates.append(meta.get("upscale_file"))
        candidates.extend(str(path) for path in sorted(folder.glob(f"{stem}_upscale_*.png"), reverse=True))
        candidates.append(meta.get("source_image"))
        candidates.append(meta.get("base_file"))
        candidates.extend(str(path) for path in sorted(folder.glob(f"{stem}_base_*.png"), reverse=True))

    if source_mode == "base":
        candidates.append(meta.get("base_file"))
        candidates.extend(str(path) for path in sorted(folder.glob(f"{stem}_base_*.png")))

    if source_mode == "upscale":
        candidates.append(meta.get("upscale_file"))
        candidates.extend(str(path) for path in sorted(folder.glob(f"{stem}_upscale_*.png")))

    candidates.extend(str(path) for path in sorted(folder.glob(f"{stem}*.png"), reverse=True))
    return candidates


def resolve_source_image(meta, meta_path, source_mode):
    seen = set()
    for candidate in source_candidates(meta, meta_path, source_mode):
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        path = existing_path(candidate)
        if path:
            return path

    return None


def size_from_text(text):
    if not text:
        return None
    match = re.search(r"(\d{3,5})x(\d{3,5})", str(text))
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def planned_base_size(meta, config):
    for value in (meta.get("base_file"), meta.get("upscale_file")):
        size = size_from_text(value)
        if size:
            return size

    base_cfg = config.get("base", {})
    return int(base_cfg.get("width", 1344)), int(base_cfg.get("height", 768))


def recreated_base_path(meta_path, meta, width, height):
    stem = metadata_stem(meta, meta_path)
    return meta_path.parent / f"{stem}_recreated_base_{width}x{height}_{machine.now_stamp()}.png"


def base_steps_from_metadata(meta, config, args):
    if args.recreate_steps is not None:
        return int(args.recreate_steps)
    if meta.get("base_steps") is not None:
        return int(meta["base_steps"])
    return int(config.get("base", {}).get("steps", 50))


def parse_prompt_file(path):
    if not path.exists():
        return None, None

    text = path.read_text(encoding="utf-8", errors="replace")
    positive = ""
    negative = ""
    section = None

    for raw in text.splitlines():
        line = raw.strip()
        if line.upper() == "POSITIVE:":
            section = "positive"
            continue
        if line.upper() == "NEGATIVE:":
            section = "negative"
            continue
        if not line:
            continue
        if section == "positive":
            positive = f"{positive} {line}".strip()
        elif section == "negative":
            negative = f"{negative} {line}".strip()

    return positive or None, negative or None


def prompt_from_metadata(meta, meta_path):
    prompt = meta.get("prompt")
    negative = meta.get("negative_prompt")
    if prompt and negative:
        return prompt, negative

    stem = metadata_stem(meta, meta_path)
    file_prompt, file_negative = parse_prompt_file(meta_path.parent / f"{stem}_prompt.txt")
    prompt = prompt or file_prompt
    negative = negative or file_negative

    if not prompt or not negative:
        raise RuntimeError(f"Metadata/prompt file did not contain both positive and negative prompts: {meta_path}")
    return prompt, negative


def image_size(path):
    try:
        from PIL import Image

        with Image.open(path) as img:
            return img.size
    except Exception:
        pass

    with path.open("rb") as f:
        header = f.read(24)
    if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 24:
        return struct.unpack(">II", header[16:24])

    raise RuntimeError(f"Could not read image size: {path}")


def output_path_for(meta_path, source_path, width, height, scale):
    stem = metadata_stem(load_json(meta_path), meta_path)
    stamp = machine.now_stamp()
    scale_label = f"{scale:g}x".replace(".", "p")
    return source_path.parent / f"{stem}_{scale_label}_upscale_{width}x{height}_{stamp}.png"


def clamp(value, low, high):
    return max(low, min(high, value))


def tune_upscale_for_target(up_cfg, src_w, src_h, target_w, target_h, scale, args):
    """Tune tiled upscale defaults for larger targets without hiding overrides."""
    pixels = target_w * target_h

    if args.tile_width is not None:
        tile_width = args.tile_width
    elif pixels >= 24_000_000:
        tile_width = 320
    elif pixels >= 14_000_000:
        tile_width = 384
    else:
        tile_width = int(up_cfg.get("tile_width", 512))

    if args.padding is not None:
        padding = args.padding
    else:
        padding = int(up_cfg.get("padding", 128))
        if scale >= 4 or pixels >= 24_000_000:
            padding = min(padding, 112)
        elif scale >= 3 or pixels >= 14_000_000:
            padding = min(padding, 128)

    if args.steps is not None:
        steps = args.steps
    else:
        steps = int(up_cfg.get("steps", 24))
        if scale >= 4:
            steps = min(steps, 24)
        elif scale >= 3:
            steps = min(steps, 28)

    if args.denoise is not None:
        denoise = args.denoise
    else:
        denoise = float(up_cfg.get("denoising_strength", 0.24))
        if scale >= 4:
            denoise = min(denoise, 0.22)
        elif scale >= 3:
            denoise = min(denoise, 0.24)

    up_cfg["tile_width"] = int(clamp(tile_width, 256, 768))
    up_cfg["padding"] = int(clamp(padding, 64, 192))
    up_cfg["steps"] = int(clamp(steps, 8, 45))
    up_cfg["denoising_strength"] = round(clamp(denoise, 0.05, 0.45), 3)

    return {
        "source_size": [src_w, src_h],
        "target_size": [target_w, target_h],
        "target_megapixels": round(pixels / 1_000_000, 2),
        "tile_width": up_cfg["tile_width"],
        "padding": up_cfg["padding"],
        "steps": up_cfg["steps"],
        "denoising_strength": up_cfg["denoising_strength"],
    }


def upscale_one(meta_path, base_config, workflow_dir, repo, args):
    meta_path = Path(meta_path)
    meta = load_json(meta_path)
    config = copy.deepcopy(base_config)
    prompt, negative = prompt_from_metadata(meta, meta_path)
    seed = int(meta.get("seed", args.seed if args.seed is not None else 1))

    source_path = resolve_source_image(meta, meta_path, args.source)
    source_created = False
    source_seconds = None

    if source_path:
        src_w, src_h = image_size(source_path)
    else:
        if not args.create_if_missing:
            stem = metadata_stem(meta, meta_path)
            raise RuntimeError(f"No source image found for {stem}, and --no-create-if-missing was used.")

        src_w, src_h = planned_base_size(meta, config)
        source_path = recreated_base_path(meta_path, meta, src_w, src_h)
        recreate_steps = base_steps_from_metadata(meta, config, args)

        base_cfg = config.setdefault("base", {})
        base_cfg["width"] = src_w
        base_cfg["height"] = src_h

        machine.log("SOURCE image missing: recreating base image from metadata first.", "yellow")
        machine.log(f"RECREATE BASE target {source_path} ({src_w}x{src_h}, steps={recreate_steps})", "yellow")

        if not args.dry_run:
            source_seconds = machine.generate_base(
                config,
                prompt,
                negative,
                seed,
                recreate_steps,
                source_path,
                repo,
                phase_label=f"recreate base {metadata_stem(meta, meta_path)}",
            )
            source_created = True
            machine.log(f"RECREATE BASE done in {source_seconds}s -> {source_path}", "green")

    target_w = args.width or int(round(src_w * args.scale))
    target_h = args.height or int(round(src_h * args.scale))
    out_path = Path(args.output) if args.output else output_path_for(meta_path, source_path, target_w, target_h, args.scale)

    up_cfg = config.setdefault("upscale", {})
    up_cfg["enabled"] = True
    up_cfg["width"] = target_w
    up_cfg["height"] = target_h
    up_cfg["scale"] = args.scale
    tune_report = tune_upscale_for_target(up_cfg, src_w, src_h, target_w, target_h, args.scale, args)

    machine.log(f"METADATA {meta_path}", "cyan")
    machine.log(f"SOURCE {source_path} ({src_w}x{src_h})", "yellow" if source_created else "cyan")
    machine.log(f"TARGET {out_path} ({target_w}x{target_h}, scale={args.scale:g})", "magenta")
    machine.log(
        "UPSCALE TUNING "
        f"tile={tune_report['tile_width']} padding={tune_report['padding']} "
        f"steps={tune_report['steps']} denoise={tune_report['denoising_strength']} "
        f"target={tune_report['target_megapixels']}MP",
        "magenta",
    )

    if args.dry_run:
        if not source_path.exists():
            machine.log("DRY RUN: would recreate missing base image, then upscale it.", "yellow")
        else:
            machine.log("DRY RUN: no upscale sent to Forge.", "yellow")
        return out_path

    seconds = machine.upscale_image(
        config,
        prompt,
        negative,
        seed,
        source_path,
        out_path,
        repo,
        phase_label=f"2x upscale {metadata_stem(meta, meta_path)}",
    )

    save_json(
        out_path.with_suffix(".metadata.json"),
        {
            "source_metadata": str(meta_path),
            "source_image": str(source_path),
            "source_created": source_created,
            "source_seconds": source_seconds,
            "output_image": str(out_path),
            "source_size": [src_w, src_h],
            "target_size": [target_w, target_h],
            "scale": args.scale,
            "tuning": tune_report,
            "seed": seed,
            "seconds": seconds,
            "prompt": prompt,
            "negative_prompt": negative,
        },
    )
    machine.log(f"DONE in {seconds}s -> {out_path}", "green")
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metadata", nargs="+", help="One or more *_metadata.json files.")
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--source", choices=["base", "upscale", "auto"], default="auto")
    parser.add_argument("--scale", type=float, default=2.0)
    parser.add_argument("--width", type=int, default=None)
    parser.add_argument("--height", type=int, default=None)
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--denoise", type=float, default=None)
    parser.add_argument("--tile-width", type=int, default=None)
    parser.add_argument("--padding", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--recreate-steps", type=int, default=None)
    parser.add_argument("--no-create-if-missing", dest="create_if_missing", action="store_false")
    parser.add_argument("--dry-run", action="store_true")
    parser.set_defaults(create_if_missing=True)
    args = parser.parse_args()

    workflow_dir = Path(__file__).resolve().parent
    config = load_json(machine.resolve_config_path(workflow_dir, args.config))
    repo = machine.resolve_repo(workflow_dir, config)
    machine.enable_console_color(config)

    first_meta = Path(args.metadata[0])
    log_dir = first_meta.parent if first_meta.parent.exists() else machine.resolve_output_root(repo, config)
    machine.RUN_LOG = log_dir / f"metadata-2x-upscale-{machine.now_stamp()}.log"

    machine.log(f"START metadata 2x upscale count={len(args.metadata)}", "bold")
    if not args.dry_run:
        machine.ensure_forge(repo)
        machine.set_options(config, repo)

    for meta_path in args.metadata:
        upscale_one(meta_path, config, workflow_dir, repo, args)

    machine.log("FINISH metadata 2x upscale", "green")


if __name__ == "__main__":
    main()
