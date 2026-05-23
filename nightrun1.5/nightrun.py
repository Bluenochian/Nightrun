import argparse
import base64
import importlib.util
import json
import os
import random
import re
import shutil
import subprocess
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import requests


API = "http://127.0.0.1:7860"
LORA_SCAN_CACHE = {}
BLOCKED_POSITIVE_PATTERN = re.compile(
    r"\b("
    r"child|children|kid|kids|teen|teenage|teenager|minor|underage|preteen|"
    r"loli|lolita|little girl|young girl|schoolgirl|school boy|schoolboy|"
    r"school uniform|high school|middle school|kindergarten|toddler|infant|baby|"
    r"student|hogwarts student|rape|raped|raping|non[- ]?consensual|forced|forceful|"
    r"unconscious|drugged|hypnosis|hypnotized|mind control|incest|bestiality|zoophilia|"
    r"animal sex|necrophilia|petit|petite|latex"
    r")\b",
    re.IGNORECASE,
)
ANSI_ENABLED = False
COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "orange": "\033[38;5;208m",
    "pink": "\033[38;5;213m",
    "violet": "\033[38;5;141m",
    "teal": "\033[38;5;44m",
    "bold": "\033[1m",
    "dim": "\033[2m",
}
RESET = "\033[0m"
PRINT_LOCK = threading.RLock()
LIVE_STATUS_WIDTH = 0
EMPTY_CLEANUP_SESSION_DECISION = None
PROMPT_RECENT = defaultdict(list)
PROMPT_RECENT_COLORS = []
SPINNER_FRAMES = ["|", "/", "-", "\\"]
CATEGORY_COLOR_CYCLE = [
    "bright_cyan",
    "bright_magenta",
    "bright_yellow",
    "bright_green",
    "orange",
    "teal",
    "violet",
    "pink",
    "bright_blue",
    "green",
]
CATEGORY_COLORS = {
    "concept": "bright_cyan",
    "character": "bright_magenta",
    "creature_or_nonhuman": "violet",
    "hair": "bright_yellow",
    "eyes": "teal",
    "clothing": "orange",
    "pose": "bright_green",
    "body_pose": "green",
    "safe_pose": "bright_blue",
    "glamour_pose": "pink",
    "expression": "yellow",
    "sensual_layer": "pink",
    "body_focus": "orange",
    "stocking_layer": "bright_magenta",
    "environment": "bright_cyan",
    "environment_rich": "cyan",
    "time_and_weather": "bright_blue",
    "lighting": "bright_yellow",
    "camera": "violet",
    "scene_depth": "teal",
    "scene_embellishment": "bright_magenta",
    "magic_element": "violet",
    "aura_style": "bright_magenta",
    "effects": "bright_green",
    "style_layer": "bright_blue",
    "effect_layer": "teal",
    "artist_direction": "yellow",
    "color_grade": "pink",
    "composition": "orange",
    "quality_style": "bright_green",
    "detail": "bright_yellow",
    "genre": "bright_cyan",
    "world_module": "violet",
    "abstract_idea": "bright_magenta",
    "equipment": "orange",
    "module_character_archetypes": "bright_magenta",
    "module_outfits": "orange",
    "module_environments": "bright_cyan",
    "module_props_equipment": "orange",
    "module_factions": "violet",
    "module_technology": "teal",
    "module_magic_system": "violet",
    "module_landscapes": "bright_cyan",
    "module_architecture": "cyan",
    "module_lighting_mood": "bright_yellow",
    "module_color_palettes": "pink",
    "module_cinematic_language": "bright_blue",
    "module_prompt_modifiers": "bright_green",
    "module_ships": "bright_blue",
    "module_droids": "teal",
}
COLOR_FAMILY_PATTERNS = {
    "blue": r"\b(blue|sapphire|azure|navy|cobalt)\b",
    "cyan": r"\b(cyan|teal|turquoise|aqua|electric cyan)\b",
    "red": r"\b(red|crimson|scarlet|ruby|blood)\b",
    "pink": r"\b(pink|rose|magenta)\b",
    "purple": r"\b(purple|violet|lavender|plum)\b",
    "green": r"\b(green|emerald|mint|jade)\b",
    "gold": r"\b(gold|golden|amber|honey)\b",
    "orange": r"\b(orange|ember|copper|bronze)\b",
    "white": r"\b(white|ivory|pearl|opal)\b",
    "black": r"\b(black|obsidian|charcoal|onyx)\b",
    "silver": r"\b(silver|steel|chrome|metallic)\b",
    "brown": r"\b(brown|sepia|tan|sand)\b",
    "rainbow": r"\b(rainbow|iridescent|holographic|multicolor|multicolored|prismatic)\b",
}


def now_stamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def enable_console_color(config):
    global ANSI_ENABLED

    console_cfg = config.get("console", {})
    if not console_cfg.get("color", True) or os.environ.get("NO_COLOR"):
        ANSI_ENABLED = False
        return

    if not sys.stdout.isatty():
        ANSI_ENABLED = False
        return

    if os.name == "nt":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_uint()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass

    ANSI_ENABLED = True


def colorize(text, color=None):
    if ANSI_ENABLED and color in COLORS:
        return f"{COLORS[color]}{text}{RESET}"
    return text


def _clear_live_status_unlocked():
    global LIVE_STATUS_WIDTH

    if LIVE_STATUS_WIDTH:
        sys.stdout.write("\r" + (" " * LIVE_STATUS_WIDTH) + "\r")
        sys.stdout.flush()
        LIVE_STATUS_WIDTH = 0


def clear_live_status():
    with PRINT_LOCK:
        _clear_live_status_unlocked()


def log(message, color=None):
    line = f"{datetime.now().isoformat(timespec='seconds')} {message}"
    with PRINT_LOCK:
        _clear_live_status_unlocked()
        print(colorize(line, color), flush=True)
    if RUN_LOG:
        with RUN_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def console_status(message, color=None):
    line = f"{datetime.now().isoformat(timespec='seconds')} {message}"
    with PRINT_LOCK:
        _clear_live_status_unlocked()
        print(colorize(line, color), flush=True)


def log_rich(segments):
    stamp = datetime.now().isoformat(timespec="seconds")
    plain = stamp + " " + "".join(text for text, _ in segments)
    display = stamp + " " + "".join(colorize(text, color) for text, color in segments)
    with PRINT_LOCK:
        _clear_live_status_unlocked()
        print(display, flush=True)
    if RUN_LOG:
        with RUN_LOG.open("a", encoding="utf-8") as f:
            f.write(plain + "\n")


def console_live_status(message, color=None):
    global LIVE_STATUS_WIDTH

    if not sys.stdout.isatty():
        return

    with PRINT_LOCK:
        text = colorize(message, color)
        padding = max(0, LIVE_STATUS_WIDTH - len(message))
        sys.stdout.write("\r" + text + (" " * padding))
        sys.stdout.flush()
        LIVE_STATUS_WIDTH = max(LIVE_STATUS_WIDTH, len(message))


def format_seconds(value):
    try:
        seconds = max(0, int(float(value)))
    except (TypeError, ValueError):
        return "?"

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h{minutes:02d}m"
    if minutes:
        return f"{minutes}m{seconds:02d}s"
    return f"{seconds}s"


def get_api_progress():
    try:
        response = requests.get(f"{API}/sdapi/v1/progress?skip_current_image=true", timeout=4)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def progress_bar(percent, frame_index, width=20):
    if percent is None:
        marker = frame_index % width
        return "[" + "".join("=" if i == marker else "." for i in range(width)) + "]"

    filled = max(0, min(width, int(round(width * percent / 100))))
    return "[" + ("#" * filled) + ("-" * (width - filled)) + "]"


def progress_worker(label, stop_event, poll_seconds, color, expected_steps=None):
    poll_seconds = max(2.0, float(poll_seconds))
    next_poll = 0
    frame_index = 0
    percent = None
    status = "waiting for Forge progress"
    last_status_line = None

    while not stop_event.is_set():
        polled = False
        if time.time() >= next_poll:
            polled = True
            next_poll = time.time() + poll_seconds
            data = get_api_progress()
            parts = []
            percent = None

            if data:
                state = data.get("state") or {}
                try:
                    percent = max(0, min(100, int(float(data.get("progress", 0)) * 100)))
                except (TypeError, ValueError):
                    percent = None

                step = state.get("sampling_step")
                steps = state.get("sampling_steps")
                try:
                    stale_steps = expected_steps is not None and steps and int(steps) != int(expected_steps)
                except (TypeError, ValueError):
                    stale_steps = False

                if stale_steps:
                    status = f"waiting for current {expected_steps}-step job to lock in"
                    percent = None
                else:
                    if percent is not None:
                        parts.append(f"{percent:3d}%")
                    if step is not None and steps:
                        parts.append(f"step {step}/{steps}")

                    eta = data.get("eta_relative")
                    if eta is not None:
                        parts.append(f"eta {format_seconds(eta)}")

                    job = str(state.get("job") or "").strip()
                    if job:
                        parts.append(job[:80])

                    status = " | ".join(parts) if parts else "Forge accepted job, waiting for sampler"
            else:
                status = "waiting for Forge API progress"

        frame = SPINNER_FRAMES[frame_index % len(SPINNER_FRAMES)]
        line = f"{label} {frame} {progress_bar(percent, frame_index)} {status}"
        if sys.stdout.isatty():
            console_live_status(line, color)
        elif polled and line != last_status_line:
            console_status(f"{label} progress | {status}", color)
            last_status_line = line

        frame_index += 1
        stop_event.wait(1.0)


class ProgressReporter:
    def __init__(self, config, label, color="blue", expected_steps=None):
        console_cfg = config.get("console", {})
        self.enabled = bool(console_cfg.get("progress", True))
        self.poll_seconds = float(console_cfg.get("progress_poll_seconds", 12))
        self.label = label
        self.color = color
        self.expected_steps = expected_steps
        self.stop_event = threading.Event()
        self.thread = None

    def __enter__(self):
        if self.enabled:
            self.thread = threading.Thread(
                target=progress_worker,
                args=(self.label, self.stop_event, self.poll_seconds, self.color, self.expected_steps),
                daemon=True,
            )
            self.thread.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.thread:
            self.stop_event.set()
            self.thread.join(timeout=2)
            clear_live_status()


def load_json(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def resolve_config_path(workflow_dir, config_arg):
    path = Path(config_arg)
    if path.is_absolute():
        return path
    return workflow_dir / path


def configured_path(value, base):
    if not value:
        return None
    path = Path(os.path.expandvars(str(value))).expanduser()
    if not path.is_absolute():
        path = base / path
    return path


RUN_FOLDER_PREFIXES = ("nightrun-", "overnight-randomizer-")


def is_run_folder(folder):
    return folder.is_dir() and folder.name.startswith(RUN_FOLDER_PREFIXES)


def resolve_repo(workflow_dir, config):
    paths_cfg = config.get("paths", {})
    configured = configured_path(
        paths_cfg.get("repo")
        or os.environ.get("NIGHTRUN_FORGE_REPO")
        or os.environ.get("OVERNIGHT_FORGE_REPO"),
        workflow_dir,
    )
    if configured:
        return configured
    return workflow_dir.parents[1]


def resolve_output_root(repo, config):
    paths_cfg = config.get("paths", {})
    configured = configured_path(
        paths_cfg.get("output_dir")
        or os.environ.get("NIGHTRUN_OUTPUT_DIR")
        or os.environ.get("OVERNIGHT_OUTPUT_DIR"),
        repo,
    )
    if configured:
        return configured
    return repo / "test-renders"


def cleanup_state_path(workflow_dir, config):
    cleanup_cfg = config.get("empty_run_cleanup", {})
    filename = cleanup_cfg.get("remember_file", "cleanup.local.json")
    return workflow_dir / filename


def load_cleanup_preference(workflow_dir, config):
    path = cleanup_state_path(workflow_dir, config)
    if not path.exists():
        return None
    try:
        data = load_json(path)
    except Exception:
        return None
    choice = str(data.get("empty_run_cleanup", "")).strip().lower()
    return choice if choice in {"always", "never"} else None


def save_cleanup_preference(workflow_dir, config, choice):
    path = cleanup_state_path(workflow_dir, config)
    path.write_text(
        json.dumps(
            {
                "empty_run_cleanup": choice,
                "saved_at": datetime.now().isoformat(timespec="seconds"),
            },
            indent=2,
            ensure_ascii=True,
        ),
        encoding="utf-8",
    )


def folder_has_images(folder, extensions):
    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in extensions:
            return True
    return False


def find_empty_run_folders(output_root, config):
    cleanup_cfg = config.get("empty_run_cleanup", {})
    extensions = {
        ext.lower() if str(ext).startswith(".") else "." + str(ext).lower()
        for ext in cleanup_cfg.get("image_extensions", [".png", ".jpg", ".jpeg", ".webp"])
    }
    if not output_root.exists():
        return []

    candidates = []
    root = output_root.resolve()
    for folder in output_root.iterdir():
        if not is_run_folder(folder):
            continue
        try:
            resolved = folder.resolve()
        except OSError:
            continue
        if resolved.parent != root:
            continue
        if not folder_has_images(folder, extensions):
            candidates.append(folder)
    return sorted(candidates, key=lambda path: path.name)


def ask_empty_cleanup_decision(workflow_dir, config, candidates):
    global EMPTY_CLEANUP_SESSION_DECISION

    preference = load_cleanup_preference(workflow_dir, config)
    if preference:
        return preference
    if EMPTY_CLEANUP_SESSION_DECISION:
        return EMPTY_CLEANUP_SESSION_DECISION
    if not sys.stdin.isatty():
        log("Empty run cleanup skipped: no remembered choice and no interactive console.", "dim")
        return "never_session"

    shown = ", ".join(path.name for path in candidates[:5])
    extra = "" if len(candidates) <= 5 else f", +{len(candidates) - 5} more"
    log_rich(
        [
            ("EMPTY RUN CLEANUP ", "bright_yellow"),
            (f"found {len(candidates)} empty Nightrun run folder(s) with no images.", "white"),
        ]
    )
    log_rich([("  Candidates: ", "dim"), (shown + extra, "white")])
    prompt = (
        "Clean these empty Nightrun folders? "
        "[Y] yes / [N] no / [A] yes, don't ask again / [D] no, don't ask again: "
    )
    while True:
        try:
            answer = input(colorize(prompt, "bright_cyan")).strip().lower()
        except EOFError:
            EMPTY_CLEANUP_SESSION_DECISION = "never_session"
            log("Empty run cleanup skipped: console input was not available.", "dim")
            return "never_session"
        if answer in {"y", "yes"}:
            EMPTY_CLEANUP_SESSION_DECISION = "always_session"
            return EMPTY_CLEANUP_SESSION_DECISION
        if answer in {"n", "no"}:
            EMPTY_CLEANUP_SESSION_DECISION = "never_session"
            return EMPTY_CLEANUP_SESSION_DECISION
        if answer in {"a", "always", "yes always"}:
            save_cleanup_preference(workflow_dir, config, "always")
            return "always"
        if answer in {"d", "never", "no always"}:
            save_cleanup_preference(workflow_dir, config, "never")
            return "never"


def cleanup_empty_run_folders(config, workflow_dir, output_root):
    global RUN_LOG

    cleanup_cfg = config.get("empty_run_cleanup", {})
    if not cleanup_cfg.get("enabled", True):
        return []

    candidates = find_empty_run_folders(output_root, config)
    if not candidates:
        return []

    decision = ask_empty_cleanup_decision(workflow_dir, config, candidates)
    if decision not in {"always", "always_session"}:
        log(f"Empty run cleanup skipped for {len(candidates)} folder(s).", "dim")
        return []

    removed = []
    root = output_root.resolve()
    for folder in candidates:
        try:
            resolved = folder.resolve()
            if resolved.parent != root or not is_run_folder(folder):
                continue
            if RUN_LOG and RUN_LOG.parent.resolve() == resolved:
                RUN_LOG = None
            shutil.rmtree(folder)
            removed.append(folder)
        except Exception as exc:
            log(f"Could not remove empty run folder {folder.name}: {exc}", "yellow")
    if removed:
        log(f"Empty run cleanup removed {len(removed)} folder(s) with no images.", "green")
    return removed


def normalize_prompt_fragment(text):
    """Normalize one pool line without changing the source file."""
    line = str(text).replace("，", ",").strip()
    line = re.sub(r"\s+", " ", line)
    line = re.sub(r"\s*,\s*", ", ", line)
    parts = [part.strip(" ,") for part in line.split(",") if part.strip(" ,")]
    return ", ".join(parts)


def dedupe_prompt_fragments(text):
    parts = [part.strip(" ,") for part in normalize_prompt_fragment(text).split(",") if part.strip(" ,")]
    clean = []
    seen = set()
    for part in parts:
        key = part.lower()
        if key in seen:
            continue
        clean.append(part)
        seen.add(key)
    return ", ".join(clean)


def strip_blocked_positive_fragments(text):
    parts = [part.strip(" ,") for part in normalize_prompt_fragment(text).split(",") if part.strip(" ,")]
    return ", ".join(part for part in parts if not BLOCKED_POSITIVE_PATTERN.search(part))


def validate_prompt_text(text, label, strip_blocked=False):
    normalized = dedupe_prompt_fragments(text)
    if strip_blocked:
        normalized = dedupe_prompt_fragments(strip_blocked_positive_fragments(normalized))
    if not normalized:
        raise RuntimeError(f"{label} became empty after prompt formatting.")
    if normalized.startswith(",") or normalized.endswith(","):
        raise RuntimeError(f"{label} has a leading/trailing comma: {normalized}")
    if re.search(r",\s*,", normalized):
        raise RuntimeError(f"{label} has an empty comma slot: {normalized}")
    if re.search(r",\S", normalized):
        raise RuntimeError(f"{label} has a comma without a following space: {normalized}")
    if re.search(r"\b1girl[a-zA-Z]", normalized):
        raise RuntimeError(f"{label} appears to have merged '1girl' into the next tag: {normalized}")
    return normalized


def load_pool(path, required=False, normalize_prompt=True):
    """Load a prompt pool safely.

    Empty lines and # comments are ignored.
    Missing/empty optional pools do not crash the run.
    """
    lines = []
    if not path.exists():
        if required:
            raise RuntimeError(f"Required pool is missing: {path}")
        log(f"Optional pool missing, skipped: {path}")
        return lines

    with path.open("r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if normalize_prompt:
                line = normalize_prompt_fragment(line)
                if not line:
                    continue
            lines.append(line)

    if required and not lines:
        raise RuntimeError(f"Required pool is empty: {path}")
    if not lines:
        log(f"Optional pool empty, skipped: {path}")
    return lines


def load_world_modules_from_catalog(workflow_dir, config):
    system_cfg = config.get("franchise_system", {})
    catalog_name = system_cfg.get("catalog_py", "franchise_catalog.py")
    catalog_path = workflow_dir / catalog_name
    if not catalog_path.exists():
        return []

    try:
        spec = importlib.util.spec_from_file_location("nightrun_franchise_catalog", catalog_path)
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot build import spec")
        catalog = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(catalog)
    except Exception as exc:
        log(f"Franchise catalog skipped {catalog_name}: {exc}", "yellow")
        return []

    if hasattr(catalog, "get_modules"):
        modules = catalog.get_modules()
    elif hasattr(catalog, "MODULE_CATALOG"):
        modules = catalog.MODULE_CATALOG
    else:
        log(f"Franchise catalog has no MODULE_CATALOG: {catalog_name}", "yellow")
        return []

    loaded = []
    for index, module in enumerate(modules):
        if not isinstance(module, dict):
            continue
        item = dict(module)
        item["_path"] = str(catalog_path)
        item["_id"] = str(item.get("id") or f"catalog_{index:04d}")
        loaded.append(item)
    return loaded


def load_world_modules(workflow_dir, config):
    return load_world_modules_from_catalog(workflow_dir, config)


def weighted_choice(items, weight_key="weight"):
    if not items:
        return None
    weights = [max(0.001, float(item.get(weight_key, 1.0))) if isinstance(item, dict) else 1.0 for item in items]
    return random.choices(items, weights=weights, k=1)[0]


def choose_world_module(config, workflow_dir):
    system_cfg = config.get("franchise_system", {})
    if not system_cfg.get("enabled", True):
        return None, False
    if random.random() > float(system_cfg.get("chance", 0.0)):
        return None, False

    modules = load_world_modules(workflow_dir, config)
    if not modules:
        return None, False
    module = weighted_choice(modules)
    fusion = random.random() <= float(system_cfg.get("fusion_mode_chance", 0.0))
    return module, fusion


def module_pick_count(field_cfg):
    if isinstance(field_cfg, dict):
        return int(field_cfg.get("pick", 1))
    return 1


def compose_world_module_prompt(config, module, fusion=False):
    system_cfg = config.get("franchise_system", {})
    fields_cfg = system_cfg.get("fields", {})
    default_fields = [
        "character_archetypes",
        "outfits",
        "environments",
        "props_equipment",
        "architecture",
        "lighting_mood",
        "color_palettes",
        "cinematic_language",
        "prompt_modifiers",
    ]
    fields = fields_cfg or {name: {"pick": 1} for name in default_fields}

    parts = []
    choices = {
        "world_module": [
            str(module.get("label") or module.get("name") or module.get("_id")),
            "fusion mode" if fusion else "coherent mode",
        ]
    }

    for field_name, field_cfg in fields.items():
        pool = module.get(field_name, [])
        if not pool:
            continue
        chance = float(field_cfg.get("chance", 1.0)) if isinstance(field_cfg, dict) else 1.0
        if random.random() > chance:
            continue
        picked = choose_items(pool, module_pick_count(field_cfg), f"module_{field_name}", config)
        picked = [strip_blocked_positive_fragments(item) for item in picked]
        picked = [item for item in picked if item]
        if not picked:
            continue
        choices[f"module_{field_name}"] = picked
        parts.extend(picked)

    return parts, choices


def pool_allowed_with_world_module(pool_cfg, module_active, fusion, config):
    if not module_active:
        return True, 1.0

    name = pool_cfg.get("name", "")
    system_cfg = config.get("franchise_system", {})
    risky = set(
        system_cfg.get(
            "risky_generic_pools_when_active",
            [
                "concept",
                "genre",
                "creature_or_nonhuman",
                "clothing",
                "equipment",
                "environment",
                "environment_rich",
                "magic_element",
                "aura_style",
                "effects",
                "effect_layer",
                "style_layer",
                "artist_direction",
                "color_grade",
            ],
        )
    )
    if name not in risky:
        return True, 1.0
    if not fusion:
        return False, 0.0
    return True, float(system_cfg.get("fusion_risky_pool_chance_multiplier", 0.25))


def api_alive():
    try:
        requests.get(f"{API}/sdapi/v1/progress?skip_current_image=true", timeout=5)
        return True
    except requests.RequestException:
        return False


def ensure_forge(repo):
    if api_alive():
        log("Forge API already running.", "green")
        return

    log("Starting Forge API.", "yellow")
    stdout = repo / "launch-nightrun.log"
    stderr = repo / "launch-nightrun.err.log"
    args = [
        str(repo / "venv" / "Scripts" / "python.exe"),
        "launch.py",
        "--uv",
        "--api",
        "--lowvram",
        "--pin-shared-memory",
        "--reserve-vram",
        "2.5",
        "--tiled-conv2d",
        "64",
        "--cuda-malloc",
        "--expandable-segments",
    ]
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    with stdout.open("w", encoding="utf-8", errors="replace") as out, stderr.open(
        "w", encoding="utf-8", errors="replace"
    ) as err:
        subprocess.Popen(args, cwd=repo, stdout=out, stderr=err, creationflags=creationflags)

    for _ in range(90):
        time.sleep(5)
        if api_alive():
            log("Forge API is ready.", "green")
            return

    raise RuntimeError(f"Forge API did not become ready. Check {stderr}")


def post_api(endpoint, body, timeout, repo, retries=1):
    last_error = None
    for attempt in range(retries + 1):
        try:
            response = requests.post(f"{API}{endpoint}", json=body, timeout=timeout)
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.RequestException as exc:
            last_error = exc
            log(f"API call failed on attempt {attempt + 1}: {exc}", "red")
            if attempt < retries:
                ensure_forge(repo)
                time.sleep(8)
    raise RuntimeError(str(last_error))


def get_gpu_temp():
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
            text=True,
            timeout=8,
        )
        return int(out.strip().splitlines()[0])
    except Exception:
        return None


def get_gpu_stats():
    try:
        out = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=memory.used,memory.total,temperature.gpu,utilization.gpu",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            timeout=8,
        )
        parts = [p.strip() for p in out.strip().split(",")]
        return {
            "memory_used_mb": int(parts[0]),
            "memory_total_mb": int(parts[1]),
            "temp_c": int(parts[2]),
            "util_percent": int(parts[3]),
        }
    except Exception:
        return {}


def wait_for_temperature(config):
    temp_cfg = config.get("temperature", {})
    pause_above = temp_cfg.get("pause_above_c", 78)
    resume_below = temp_cfg.get("resume_below_c", 66)
    check_seconds = temp_cfg.get("check_seconds", 20)

    temp = get_gpu_temp()
    if temp is None or temp < pause_above:
        return

    log(f"GPU is {temp}C, pausing until it cools below {resume_below}C.", "yellow")
    while True:
        time.sleep(check_seconds)
        temp = get_gpu_temp()
        if temp is None or temp <= resume_below:
            log(f"GPU cooldown done. Current temp: {temp}C.", "green")
            return
        log(f"Still cooling: {temp}C.", "yellow")


def write_base64_image(image64, path):
    if image64.startswith("data:image/"):
        image64 = image64.split(",", 1)[1]
    path.write_bytes(base64.b64decode(image64))


def selection_memory_config(config):
    cfg = config.get("selection_memory", {})
    return {
        "enabled": bool(cfg.get("enabled", True)),
        "recent_per_category": int(cfg.get("recent_per_category", 28)),
        "recent_colors": int(cfg.get("recent_colors", 18)),
        "repeat_penalty": float(cfg.get("repeat_penalty", 0.08)),
        "color_repeat_penalty": float(cfg.get("color_repeat_penalty", 0.16)),
        "blue_cyan_extra_penalty": float(cfg.get("blue_cyan_extra_penalty", 0.35)),
        "heterochromia_chance": float(cfg.get("heterochromia_chance", 0.025)),
        "color_categories": set(
            cfg.get(
                "color_categories",
                [
                    "concept",
                    "hair",
                    "eyes",
                    "clothing",
                    "environment",
                    "environment_rich",
                    "lighting",
                    "style_layer",
                    "effect_layer",
                    "effects",
                    "aura_style",
                    "color_grade",
                    "abstract_idea",
                    "genre",
                    "world_module",
                    "module_color_palettes",
                    "module_lighting_mood",
                    "module_cinematic_language",
                ],
            )
        ),
    }


def choice_key(text):
    return re.sub(r"\s+", " ", str(text).strip().lower())


def detect_color_families(text):
    lowered = str(text).lower()
    families = set()
    for family, pattern in COLOR_FAMILY_PATTERNS.items():
        if re.search(pattern, lowered):
            families.add(family)
    return families


def weighted_pick_without_replacement(candidates, weights, count):
    chosen = []
    pool = list(candidates)
    weight_pool = [max(0.001, float(weight)) for weight in weights]
    for _ in range(min(count, len(pool))):
        picked = random.choices(pool, weights=weight_pool, k=1)[0]
        index = pool.index(picked)
        chosen.append(picked)
        del pool[index]
        del weight_pool[index]
    return chosen


def remember_prompt_choices(category, picked, config):
    mem = selection_memory_config(config)
    if not mem["enabled"]:
        return

    recent = PROMPT_RECENT[category]
    for item in picked:
        key = choice_key(item)
        if key:
            recent.append(key)
            del recent[:-mem["recent_per_category"]]
        for family in detect_color_families(item):
            PROMPT_RECENT_COLORS.append(family)
            del PROMPT_RECENT_COLORS[:-mem["recent_colors"]]


def choose_items(pool, count, category=None, config=None):
    if not pool or count <= 0:
        return []

    if not category or not config:
        if count <= 1:
            return [random.choice(pool)]
        return random.sample(pool, min(count, len(pool)))

    mem = selection_memory_config(config)
    if not mem["enabled"]:
        picked = [random.choice(pool)] if count <= 1 else random.sample(pool, min(count, len(pool)))
        return picked

    candidates = list(pool)
    if category == "eyes":
        hetero = [item for item in candidates if "heterochromia" in item.lower()]
        non_hetero = [item for item in candidates if "heterochromia" not in item.lower()]
        if hetero and non_hetero and random.random() > mem["heterochromia_chance"]:
            candidates = non_hetero

    recent = set(PROMPT_RECENT.get(category, []))
    recent_colors = PROMPT_RECENT_COLORS[-mem["recent_colors"] :]
    weights = []
    for item in candidates:
        key = choice_key(item)
        weight = 1.0
        if key in recent:
            weight *= mem["repeat_penalty"]
        if category in mem["color_categories"]:
            families = detect_color_families(item)
            overlap = sum(1 for family in families if family in recent_colors)
            if overlap:
                weight *= mem["color_repeat_penalty"] ** overlap
            if ("blue" in families or "cyan" in families) and sum(1 for family in recent_colors if family in {"blue", "cyan"}) >= 4:
                weight *= mem["blue_cyan_extra_penalty"]
        weights.append(weight)

    picked = weighted_pick_without_replacement(candidates, weights, count)
    remember_prompt_choices(category, picked, config)
    return picked


def weight_value(item):
    lo = float(item.get("min", item.get("weight_min", 1.0)))
    hi = float(item.get("max", item.get("weight_max", lo)))
    return round(random.uniform(lo, hi), 2)


def base_step_range(config):
    base_cfg = config["base"]
    low = int(base_cfg.get("steps_min", base_cfg.get("steps", 30)))
    high = int(base_cfg.get("steps_max", base_cfg.get("steps", low)))
    if low > high:
        low, high = high, low
    return low, high


def choose_base_steps(config):
    low, high = base_step_range(config)
    return random.randint(low, high)


def long_run_chill_config(config, count):
    cfg = dict(config.get("long_run_chill", {}))
    if not cfg.get("enabled", True):
        return None

    only_when_count_over = int(cfg.get("only_when_count_over", 100))
    if count <= only_when_count_over:
        return None

    every_min = int(cfg.get("every_min_generations", 12))
    every_max = int(cfg.get("every_max_generations", 20))
    sleep_min = float(cfg.get("sleep_min_minutes", 5))
    sleep_max = float(cfg.get("sleep_max_minutes", 10))

    if every_min > every_max:
        every_min, every_max = every_max, every_min
    if sleep_min > sleep_max:
        sleep_min, sleep_max = sleep_max, sleep_min

    return {
        "every_min_generations": max(1, every_min),
        "every_max_generations": max(1, every_max),
        "sleep_min_minutes": max(0.1, sleep_min),
        "sleep_max_minutes": max(0.1, sleep_max),
    }


def schedule_next_chill(chill_cfg, completed_count):
    if not chill_cfg:
        return None
    spacing = random.randint(chill_cfg["every_min_generations"], chill_cfg["every_max_generations"])
    return completed_count + spacing


def run_long_chill(chill_cfg, completed_count, next_chill_at, stop_file):
    if not chill_cfg or next_chill_at is None or completed_count < next_chill_at:
        return next_chill_at

    chill_minutes = random.uniform(chill_cfg["sleep_min_minutes"], chill_cfg["sleep_max_minutes"])
    chill_seconds = int(chill_minutes * 60)
    log(
        f"VRAM CHILL ACTIVE after {completed_count} generations: resting {format_seconds(chill_seconds)}.",
        "cyan",
    )

    remaining = chill_seconds
    while remaining > 0:
        if stop_file.exists():
            log("Stop file found during VRAM chill. Ending chill early.", "yellow")
            return None
        nap = min(30, remaining)
        time.sleep(nap)
        remaining -= nap

    next_chill = schedule_next_chill(chill_cfg, completed_count)
    log(f"VRAM chill done. Next chill scheduled after generation {next_chill}.", "green")
    return next_chill


def log_run_rules(mode, config, count):
    low, high = base_step_range(config)
    log(f"BASE STEPS active: random range {low}-{high}.", "cyan")

    up_cfg = config.get("upscale", {})
    if not up_cfg.get("enabled", True):
        log("UPSCALE disabled.", "yellow")
    else:
        every_n = int(up_cfg.get("every_n", 1))
        threshold = up_cfg.get("auto_when_base_steps_below")

        if mode == "full" and every_n > 0:
            log(f"FULL UPSCALE active: every {every_n} image(s) will upscale.", "magenta")

        if threshold is not None:
            log(f"LOW-STEP AUTO UPSCALE active: base steps below {threshold} will upscale.", "magenta")

    chill_cfg = long_run_chill_config(config, count)
    raw_chill_cfg = config.get("long_run_chill", {})
    if chill_cfg:
        log(
            "LONG-RUN VRAM CHILL active: "
            f"{chill_cfg['sleep_min_minutes']:g}-{chill_cfg['sleep_max_minutes']:g} min rest "
            f"every {chill_cfg['every_min_generations']}-{chill_cfg['every_max_generations']} generations.",
            "cyan",
        )
    elif raw_chill_cfg.get("enabled", True):
        threshold_count = int(raw_chill_cfg.get("only_when_count_over", 100))
        log(f"LONG-RUN VRAM CHILL idle: count must be above {threshold_count}.", "dim")


def should_upscale_for_image(mode, config, index, base_steps):
    up_cfg = config.get("upscale", {})
    if not up_cfg.get("enabled", True):
        return False, "upscale disabled"

    every_n = int(up_cfg.get("every_n", 1))
    if mode == "full" and every_n > 0 and index % every_n == 0:
        return True, f"full mode every_n={every_n}"

    threshold = up_cfg.get("auto_when_base_steps_below")
    if threshold is not None and base_steps < int(threshold):
        return True, f"base steps {base_steps} below {threshold}"

    return False, "not scheduled"


def normalize_name(name):
    return re.sub(r"[^a-z0-9]+", "", str(name).lower())


def scan_loras(repo, config):
    scan_cfg = config.get("lora_scan", {})
    if not scan_cfg.get("enabled", True):
        return None, {}

    folders = scan_cfg.get("folders", ["models/Lora"])
    aliases = scan_cfg.get("aliases", {})
    cache_key = (str(repo), tuple(folders), tuple(sorted(aliases.items())))
    if scan_cfg.get("cache", True) and cache_key in LORA_SCAN_CACHE:
        return LORA_SCAN_CACHE[cache_key]

    found = {}
    folders_found = False

    for rel in folders:
        folder = repo / rel
        if not folder.exists():
            continue
        folders_found = True
        for ext in ("*.safetensors", "*.pt", "*.ckpt"):
            for file in folder.rglob(ext):
                stem = file.stem
                found[normalize_name(stem)] = stem

    local_count = len(found)
    for alias, target in aliases.items():
        target_stem = found.get(normalize_name(target))
        if target_stem:
            found[normalize_name(alias)] = target_stem

    if folders_found:
        log(f"LoRA scan found {local_count} local LoRA files.")
    else:
        log("No LoRA folder found from config lora_scan.folders.")

    result = (folders_found, found)
    if scan_cfg.get("cache", True):
        LORA_SCAN_CACHE[cache_key] = result
    return result


def resolve_lora_name(raw_name, folders_found, lora_index, config):
    """Return a real local LoRA stem if possible. Otherwise maybe skip.

    This prevents bad prompts from throwing missing-LoRA errors when the script can see the local LoRA folder.
    """
    raw_name = str(raw_name).strip()
    if not raw_name:
        return None

    # If the pool line already contains a full <lora:name:weight> tag, extract the name only.
    match = re.search(r"<lora:([^:>]+):", raw_name, re.IGNORECASE)
    if match:
        raw_name = match.group(1).strip()

    key = normalize_name(raw_name)
    if lora_index is None:
        return raw_name

    if key in lora_index:
        return lora_index[key]

    # Soft match both directions for ugly filenames / copied CivitAI titles.
    for k, stem in lora_index.items():
        if key and (key in k or k in key):
            return stem

    scan_cfg = config.get("lora_scan", {})
    if folders_found and scan_cfg.get("skip_missing_when_folder_found", True):
        log(f"LoRA not found locally, skipped: {raw_name}")
        return None

    if (not folders_found) and scan_cfg.get("fallback_to_raw_names_when_no_lora_folder", True):
        return raw_name

    return None


def lora_tag(raw_name, weight, folders_found, lora_index, config):
    name = resolve_lora_name(raw_name, folders_found, lora_index, config)
    if not name:
        return None
    return f"<lora:{name}:{weight}>"


def lora_key_from_tag(tag):
    match = re.match(r"<lora:([^:>]+):", tag, re.IGNORECASE)
    return normalize_name(match.group(1) if match else tag)


def lora_reference_key(raw_name, lora_index):
    key = normalize_name(raw_name)
    if lora_index and key in lora_index:
        return normalize_name(lora_index[key])
    return key


def make_lora_tags(config, workflow_dir, repo):
    tags = []
    selected = []
    lora_sources = []

    folders_found, lora_index = scan_loras(repo, config)

    for item in config.get("always_loras", []):
        tag = lora_tag(item["name"], weight_value(item), folders_found, lora_index, config)
        if tag:
            tags.append(tag)
            lora_sources.append({"source": "always_loras", "name": item["name"], "tag": tag})

    for item in config.get("random_loras", []):
        if random.random() <= float(item.get("chance", 1.0)):
            selected.append(item)

    random.shuffle(selected)
    max_random = int(config.get("max_random_loras", 4))
    for item in selected[:max_random]:
        tag = lora_tag(item["name"], weight_value(item), folders_found, lora_index, config)
        if tag:
            tags.append(tag)
            lora_sources.append({"source": "random_loras", "name": item["name"], "tag": tag})

    for group in config.get("lora_pools", []):
        if random.random() > float(group.get("chance", 1.0)):
            continue
        pool_path = workflow_dir / group["file"]
        pool = load_pool(pool_path, required=False, normalize_prompt=False)
        if not pool:
            continue

        pick_min = int(group.get("pick_min", 0))
        pick_max = int(group.get("pick_max", 1))
        pick_count = random.randint(pick_min, max(pick_min, pick_max))
        for raw_name in choose_items(pool, pick_count):
            weight = round(random.uniform(float(group.get("weight_min", 0.45)), float(group.get("weight_max", 0.85))), 2)
            tag = lora_tag(raw_name, weight, folders_found, lora_index, config)
            if tag:
                tags.append(tag)
                lora_sources.append({"source": group.get("name", "lora_pool"), "name": raw_name, "tag": tag})

    for synergy in config.get("lora_synergies", []):
        selected_keys = {lora_key_from_tag(tag) for tag in tags}
        trigger_keys = {lora_reference_key(name, lora_index) for name in synergy.get("when_any", [])}
        if trigger_keys and not selected_keys.intersection(trigger_keys):
            continue
        if random.random() > float(synergy.get("chance", 1.0)):
            continue

        candidates = []
        for candidate in synergy.get("candidates", []):
            item = candidate if isinstance(candidate, dict) else {"name": candidate}
            candidate_key = lora_reference_key(item["name"], lora_index)
            if candidate_key not in selected_keys:
                candidates.append(item)
        if not candidates:
            continue

        pick_min = int(synergy.get("pick_min", 1))
        pick_max = int(synergy.get("pick_max", 1))
        pick_count = random.randint(pick_min, max(pick_min, pick_max))
        for item in choose_items(candidates, pick_count):
            weighted_item = dict(item)
            weighted_item.setdefault("min", synergy.get("weight_min", 0.2))
            weighted_item.setdefault("max", synergy.get("weight_max", 0.6))
            tag = lora_tag(item["name"], weight_value(weighted_item), folders_found, lora_index, config)
            if tag:
                tags.append(tag)
                lora_sources.append({"source": synergy.get("name", "lora_synergy"), "name": item["name"], "tag": tag})

    # De-duplicate by LoRA file stem while preserving order.
    clean = []
    clean_sources = []
    seen = set()
    for tag, source in zip(tags, lora_sources):
        key = lora_key_from_tag(tag)
        if key not in seen:
            clean.append(tag)
            clean_sources.append(source)
            seen.add(key)

    max_total = int(config.get("max_total_loras", 0))
    if max_total > 0:
        clean = clean[:max_total]
        clean_sources = clean_sources[:max_total]

    return clean, clean_sources


THEME_FAMILIES = {
    "gothic_vampire": {
        "roles": ["gothic vampire queen", "black rose duchess", "red moon countess", "silver fang noblewoman", "candlelit manor vampire"],
        "outfits": ["black lace gown", "satin corset dress", "velvet high-slit dress", "off-shoulder gothic dress", "black dress with lace gloves"],
        "settings": ["moonlit cemetery", "stained glass chapel", "velvet vampire lounge", "gothic castle balcony", "dark manor bedroom"],
        "lights": ["red moon rim light", "warm candle glow", "deep crimson ambient light", "moonbeam spotlight"],
        "effects": ["black rose petals", "thin shadow wisps", "silver fog", "candle smoke curls", "blood-red crystal glow"],
    },
    "witch_arcane": {
        "roles": ["witch librarian", "arcane alchemist", "occult professor", "tarot oracle", "moonlit spellcaster"],
        "outfits": ["layered witch dress", "black satin corset dress", "dark academic dress", "silk robe over dark dress", "ribbon-laced bodice dress"],
        "settings": ["grand magical library", "candlelit potion shop", "ritual circle chamber", "gilded library balcony", "crystal greenhouse"],
        "lights": ["warm candle glow", "violet arcane glow", "gold chandelier light", "magic circle underlight"],
        "effects": ["floating books", "arcane runes", "violet arcane sparks", "golden magic particles", "floating perfume mist"],
    },
    "cyber_holographic": {
        "roles": ["cyber vampire idol", "holographic idol mage", "star halo android", "neon shrine guardian", "electric storm idol"],
        "outfits": ["holographic bodysuit", "iridescent stage bodysuit", "holographic jacket and black dress", "form-fitting bodysuit", "chrome vampire dress"],
        "settings": ["rainy neon alley", "holographic concert stage", "blue neon nightclub", "cyberpunk hotel suite", "neon station platform"],
        "lights": ["cyan neon backlight", "pink holographic sparkle light", "neon sign edge light", "cool blue hair rim light"],
        "effects": ["cyan holographic fragments", "neon outline accents", "holographic fragments", "wet pavement glow", "iridescent highlights"],
    },
    "angelic_knight": {
        "roles": ["celestial angel warrior", "fallen angel aristocrat", "glass-winged angel", "winged valkyrie", "obsidian angel knight"],
        "outfits": ["white gold armor dress", "black feather cloak", "silver armor corset dress", "blue flame knight armor", "white satin ceremonial gown"],
        "settings": ["winter chapel", "floating sky cathedral", "ruined chapel", "storm-lit armor hall", "glass observatory"],
        "lights": ["gold halo backlight", "blue flame rim light", "silver moonlight", "storm flash backlight"],
        "effects": ["black feather particles", "halo backlight", "blue flame accents", "glowing crown shards", "silver moon dust"],
    },
    "ice_winter": {
        "roles": ["ice palace sorceress", "winter chapel queen", "blue-eyed snow knight", "frostfire armor heroine", "enchanted winter dancer"],
        "outfits": ["white fur-trimmed gown", "silver ceremonial dress", "fur-lined winter dress", "white lace corset dress", "blue flame knight armor"],
        "settings": ["crystal palace corridor", "winter palace bedroom", "frozen mountain pass", "winter chapel", "ice palace corridor"],
        "lights": ["cold blue shadows", "silver moonlight", "cool blue hair rim light", "crystal caustic reflections"],
        "effects": ["drifting snow", "sparkling snow dust", "blue crystal glow", "misty breath in cold air", "snow particles"],
    },
    "dark_boudoir": {
        "roles": ["black veil temptress", "midnight lounge singer", "satin glove vampire", "black pearl countess", "moonlit blood mage"],
        "outfits": ["lace lingerie-inspired gown", "silk slip dress with lace trim", "sheer black overdress", "black satin corset dress", "velvet high-slit dress"],
        "settings": ["luxury vampire boudoir", "satin-curtained manor room", "dark gothic bedroom", "ornate mirror dressing hall", "candlelit bath chamber"],
        "lights": ["soft bedside lamp light", "warm skin highlights", "red window backlight", "candle cluster glow"],
        "effects": ["lace shadow pattern", "mirror reflections", "satin fabric sheen", "floating perfume mist", "wet skin highlights"],
    },
    "dragon_ocean": {
        "roles": ["dragon priestess", "ocean dragon oracle", "cyber dragon princess", "serpent shrine priestess", "gothic mermaid oracle"],
        "outfits": ["scale-trim priestess dress", "iridescent jacket", "silver ceremonial dress", "transparent sleeve gothic gown", "crystal-trim gown"],
        "settings": ["ancient water temple", "dragon shrine waterfall", "bioluminescent forest pool", "moon pool ritual room", "royal bathhouse ruins"],
        "lights": ["teal bioluminescent light", "water reflection uplight", "crystal caustic reflections", "silver moonlight"],
        "effects": ["teal bioluminescent glow", "blue crystal glow", "transparent glass reflections", "water droplets on glass", "small star particles"],
    },
    "warrior_commander": {
        "roles": ["space knight commander", "black armor princess", "storm capital commander", "royal assassin", "sword saint"],
        "outfits": ["gothic power armor", "black leather corset armor", "red lacquer armor", "black gold armor dress", "silver armor corset dress"],
        "settings": ["ruined capital balcony", "cathedral hangar", "floating battlefield ruins", "storm-lit armor hall", "marble temple courtyard"],
        "lights": ["storm lightning highlights", "blue flame rim light", "high contrast spotlight", "red moon rim light"],
        "effects": ["blue electric arcs", "thin lightning threads", "red crystal glow", "embers in the air", "glowing runes"],
    },
}


HAIR_TAGS = [
    "white long flowing hair, cyan rim light",
    "black hair with red tips, silky strands",
    "silver hair with blunt bangs, moonlit shine",
    "blue-black messy bob, soft flyaway strands",
    "holographic twin tails, iridescent highlights",
    "platinum blonde wavy hair, gold ornaments",
    "wine red long hair, black ribbon accessory",
    "pearl white braided crown, rose hair ornament",
]

EYE_TAGS = [
    "red eyes, sharp vampire stare",
    "ice blue eyes, bright catchlights",
    "gold eyes, half-lidded gaze",
    "cyan glowing eyes, neon ring pupils",
    "violet eyes, glossy highlights",
    "holographic eyes, star-like pupils",
    "emerald eyes, predatory gaze",
]

GLAMOUR_POSES = [
    "seated pose, legs crossed, one hand on thigh",
    "reclining pose, bare shoulders visible, relaxed gaze",
    "leaning forward pose, cleavage emphasis, direct eye contact",
    "over-the-shoulder pose, high slit showing thigh",
    "standing contrapposto pose, hips emphasized, confident posture",
    "hand-near-lips pose, glossy lips visible, teasing smile",
    "sitting on bed pose, dress pooling around hips, candlelit mood",
    "kneeling pose, thighhighs visible, readable hands",
    "mirror glamour pose, choker and collarbone focus",
    "throne pose, dominant posture, garter straps visible",
]

STOCKING_TAGS = [
    "black thighhigh stockings, lace top visible",
    "sheer black stockings, garter straps visible",
    "white thighhigh stockings, soft skin contrast",
    "fishnet stockings, gothic fashion detail",
    "back-seam stockings, high heels visible",
    "stockings with rose embroidery, thigh focus",
    "transparent dark pantyhose, polished anime rendering",
    "ribbon-tied thighhighs, luxury boudoir mood",
    "stockings under high slit dress, elegant exposed leg",
    "garter belt and stockings, tasteful glamour",
]

BODY_FOCUS_TAGS = [
    "collarbone focus, choker shadow on neck",
    "cleavage focus, tasteful framing",
    "waist curve focus, corset lace tension",
    "hip curve focus, satin fold detail",
    "thigh focus, stocking texture visible",
    "bare shoulder focus, silk fabric sliding off shoulder",
    "glossy lips detail, fangs visible",
    "lace glove detail, hand framing face",
]

SCENE_DEPTH_TAGS = [
    "wet floor reflections, cinematic depth",
    "foreground candles, warm glow",
    "moonlight through tall windows, silver fog",
    "ornate mirror reflections, elegant framing",
    "black rose petals in foreground",
    "stained glass color spill, detailed background",
    "lace curtains, soft shadows",
    "floating particles, clean subject separation",
    "gold filigree details, premium splash art staging",
    "shallow reflective water, clear face focus",
]

STYLE_TAGS = [
    "dark fantasy anime style, premium key visual",
    "gothic luxury aesthetic, polished anime rendering",
    "romantic dark fantasy, beautiful horror not grotesque",
    "high-end game character art, clean readable silhouette",
    "cinematic anime portrait, sharp eye detail",
    "holographic cyber fantasy, controlled glow",
    "luxury fashion illustration, detailed fabric",
]


def pick_one(items):
    return random.choice(items)


def maybe_add(parts, choices, name, items, chance):
    if random.random() <= chance:
        picked = pick_one(items)
        parts.append(picked)
        choices[name] = [picked]


def compose_dynamic_prompt(config, workflow_dir, repo):
    dynamic_cfg = config.get("dynamic_prompt", {})
    family_name = random.choice(dynamic_cfg.get("families", list(THEME_FAMILIES)))
    family = THEME_FAMILIES.get(family_name, THEME_FAMILIES["gothic_vampire"])
    choices = {"theme_family": [family_name]}
    prompt_parts = [strip_blocked_positive_fragments(config["fixed_prefix"])]

    core = [
        pick_one(family["roles"]),
        pick_one(family["outfits"]),
        pick_one(family["settings"]),
        pick_one(family["lights"]),
        pick_one(family["effects"]),
    ]
    prompt_parts.extend(strip_blocked_positive_fragments(item) for item in core)
    choices["dynamic_core"] = core

    maybe_add(prompt_parts, choices, "hair", HAIR_TAGS, dynamic_cfg.get("hair_chance", 0.75))
    maybe_add(prompt_parts, choices, "eyes", EYE_TAGS, dynamic_cfg.get("eyes_chance", 0.65))
    maybe_add(prompt_parts, choices, "glamour_pose", GLAMOUR_POSES, dynamic_cfg.get("glamour_pose_chance", 0.65))
    maybe_add(prompt_parts, choices, "stocking_layer", STOCKING_TAGS, dynamic_cfg.get("stocking_chance", 0.7))
    maybe_add(prompt_parts, choices, "body_focus", BODY_FOCUS_TAGS, dynamic_cfg.get("body_focus_chance", 0.5))
    maybe_add(prompt_parts, choices, "scene_depth", SCENE_DEPTH_TAGS, dynamic_cfg.get("scene_depth_chance", 0.8))
    maybe_add(prompt_parts, choices, "style_layer", STYLE_TAGS, dynamic_cfg.get("style_chance", 0.65))

    prompt_parts.append(strip_blocked_positive_fragments(config["fixed_suffix"]))
    lora_tags, lora_sources = make_lora_tags(config, workflow_dir, repo)
    prompt_parts.extend(lora_tags)
    prompt = validate_prompt_text(
        ", ".join(part.strip() for part in prompt_parts if part and part.strip()),
        "positive prompt",
        strip_blocked=True,
    )

    negative_parts = [config.get("negative_base", "")]
    for neg_cfg in config.get("negative_pools", []):
        neg_pool = load_pool(workflow_dir / neg_cfg["file"], required=False)
        negative_parts.extend(neg_pool)
    negative = validate_prompt_text(", ".join(part.strip() for part in negative_parts if part and part.strip()), "negative prompt")

    return prompt, negative, choices, lora_tags, lora_sources


def compose_prompt(config, workflow_dir, repo):
    if config.get("dynamic_prompt", {}).get("enabled", False):
        return compose_dynamic_prompt(config, workflow_dir, repo)

    choices = {}
    prompt_parts = [strip_blocked_positive_fragments(config["fixed_prefix"])]
    world_module, fusion = choose_world_module(config, workflow_dir)
    if world_module:
        module_parts, module_choices = compose_world_module_prompt(config, world_module, fusion=fusion)
        prompt_parts.extend(module_parts)
        choices.update(module_choices)

    for pool_cfg in config.get("prompt_pools", []):
        allowed, chance_multiplier = pool_allowed_with_world_module(pool_cfg, bool(world_module), fusion, config)
        if not allowed:
            continue
        chance = float(pool_cfg.get("chance", 1.0))
        chance *= chance_multiplier
        for boost in pool_cfg.get("boost_if_any", []):
            names = set(boost.get("choices", []))
            if names and any(name in choices for name in names):
                chance = max(chance, float(boost.get("chance", chance)) * chance_multiplier)
        if random.random() > chance:
            continue

        pool_path = workflow_dir / pool_cfg["file"]
        pool = load_pool(pool_path, required=bool(pool_cfg.get("required", False)))
        picked = [
            strip_blocked_positive_fragments(item)
            for item in choose_items(pool, int(pool_cfg.get("pick", 1)), pool_cfg["name"], config)
        ]
        picked = [item for item in picked if item]
        if not picked:
            continue
        choices[pool_cfg["name"]] = picked
        prompt_parts.extend(picked)

    prompt_parts.append(strip_blocked_positive_fragments(config["fixed_suffix"]))

    lora_tags, lora_sources = make_lora_tags(config, workflow_dir, repo)
    prompt_parts.extend(lora_tags)

    prompt = validate_prompt_text(
        ", ".join(part.strip() for part in prompt_parts if part and part.strip()),
        "positive prompt",
        strip_blocked=True,
    )

    negative_parts = [normalize_prompt_fragment(config.get("negative_base", ""))]
    for neg_cfg in config.get("negative_pools", []):
        neg_pool = load_pool(workflow_dir / neg_cfg["file"], required=False)
        negative_parts.extend(neg_pool)
    negative = validate_prompt_text(", ".join(part.strip() for part in negative_parts if part and part.strip()), "negative prompt")

    return prompt, negative, choices, lora_tags, lora_sources


def category_color(name, index):
    return CATEGORY_COLORS.get(name, CATEGORY_COLOR_CYCLE[index % len(CATEGORY_COLOR_CYCLE)])


def compact_choice_value(values, limit=180):
    text = " | ".join(str(value) for value in values)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip(" ,;") + "..."


def log_prompt_map(stem, choices):
    if not choices:
        return

    log_rich(
        [
            (f"[{stem}] Prompt map ", "bold"),
            (f"{len(choices)} active categories", "bright_cyan"),
            ("  full prompt saved beside image", "dim"),
        ]
    )
    for index, (name, values) in enumerate(choices.items()):
        color = category_color(name, index)
        label = name.replace("_", " ")
        log_rich(
            [
                (f"[{stem}]   ", "dim"),
                (f"{label:<22}", color),
                (" -> ", "dim"),
                (compact_choice_value(values), "white"),
            ]
        )


def set_options(config, repo):
    body = {
        "sd_model_checkpoint": config["checkpoint"],
        "sd_vae": config.get("vae", "Automatic"),
        "forge_preset": config.get("forge_preset", "xl"),
        "CLIP_stop_at_last_layers": config.get("clip_skip", 2),
    }
    post_api("/sdapi/v1/options", body, timeout=300, repo=repo, retries=1)


def generate_base(config, prompt, negative, seed, steps, out_path, repo, phase_label=None):
    base_cfg = config["base"]
    body = {
        "prompt": prompt,
        "negative_prompt": negative,
        "width": base_cfg["width"],
        "height": base_cfg["height"],
        "steps": steps,
        "cfg_scale": base_cfg["cfg_scale"],
        "sampler_name": base_cfg["sampler_name"],
        "scheduler": base_cfg["scheduler"],
        "seed": seed,
        "batch_size": 1,
        "n_iter": 1,
        "restore_faces": False,
        "tiling": False,
        "enable_hr": False,
        "send_images": True,
        "save_images": False,
        "override_settings": {
            "sd_model_checkpoint": config["checkpoint"],
            "CLIP_stop_at_last_layers": config.get("clip_skip", 2),
        },
        "override_settings_restore_afterwards": False,
    }
    start = time.time()
    with ProgressReporter(config, phase_label or "Base", color="blue", expected_steps=steps):
        result = post_api("/sdapi/v1/txt2img", body, timeout=5400, repo=repo, retries=1)
    write_base64_image(result["images"][0], out_path)
    return round(time.time() - start, 1)


def upscale_image(config, prompt, negative, seed, source_path, out_path, repo, phase_label=None):
    up_cfg = config["upscale"]
    img64 = base64.b64encode(source_path.read_bytes()).decode("ascii")
    script_args = [
        "",
        up_cfg["tile_width"],
        up_cfg["tile_height"],
        up_cfg["mask_blur"],
        up_cfg["padding"],
        64,
        0.10,
        32,
        up_cfg["upscaler_index"],
        True,
        up_cfg["redraw_mode"],
        False,
        8,
        0,
        1,
        up_cfg["width"],
        up_cfg["height"],
        up_cfg.get("scale", 2.25),
    ]
    body = {
        "init_images": [img64],
        "prompt": prompt,
        "negative_prompt": negative,
        "width": up_cfg["width"],
        "height": up_cfg["height"],
        "resize_mode": 0,
        "denoising_strength": up_cfg["denoising_strength"],
        "steps": up_cfg["steps"],
        "cfg_scale": up_cfg["cfg_scale"],
        "sampler_name": up_cfg["sampler_name"],
        "scheduler": up_cfg["scheduler"],
        "seed": seed,
        "batch_size": 1,
        "n_iter": 1,
        "restore_faces": False,
        "include_init_images": False,
        "send_images": True,
        "save_images": False,
        "script_name": "ultimate sd upscale",
        "script_args": script_args,
        "override_settings": {
            "sd_model_checkpoint": config["checkpoint"],
            "CLIP_stop_at_last_layers": config.get("clip_skip", 2),
        },
        "override_settings_restore_afterwards": False,
    }
    start = time.time()
    with ProgressReporter(config, phase_label or "Upscale", color="magenta", expected_steps=up_cfg["steps"]):
        result = post_api("/sdapi/v1/img2img", body, timeout=10800, repo=repo, retries=1)
    write_base64_image(result["images"][0], out_path)
    return round(time.time() - start, 1)


def make_contact_sheet(image_paths, out_path):
    try:
        from PIL import Image, ImageDraw
    except Exception:
        return

    if not image_paths:
        return

    thumbs = []
    for path in image_paths:
        img = Image.open(path).convert("RGB")
        img.thumbnail((384, 216), Image.Resampling.LANCZOS)
        thumbs.append((path.name, img.copy()))

    cols = 3
    rows = (len(thumbs) + cols - 1) // cols
    pad = 14
    label_h = 34
    sheet = Image.new(
        "RGB",
        (cols * 384 + (cols + 1) * pad, rows * (216 + label_h) + (rows + 1) * pad),
        (22, 22, 22),
    )
    draw = ImageDraw.Draw(sheet)
    for i, (label, img) in enumerate(thumbs):
        x = pad + (i % cols) * (384 + pad)
        y = pad + (i // cols) * (216 + label_h + pad)
        draw.text((x, y), label[:42], fill=(235, 235, 235))
        sheet.paste(img, (x, y + label_h))

    sheet.save(out_path)


def write_metadata(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def iter_lora_config_names(config, workflow_dir):
    for item in config.get("always_loras", []):
        yield "always_loras", item["name"]
    for item in config.get("random_loras", []):
        yield "random_loras", item["name"]
    for group in config.get("lora_pools", []):
        pool = load_pool(workflow_dir / group["file"], required=False, normalize_prompt=False)
        for raw_name in pool:
            yield group.get("name", "lora_pool"), raw_name
    for synergy in config.get("lora_synergies", []):
        for raw_name in synergy.get("when_any", []):
            yield f"{synergy.get('name', 'lora_synergy')}:trigger", raw_name
        for candidate in synergy.get("candidates", []):
            item = candidate if isinstance(candidate, dict) else {"name": candidate}
            yield synergy.get("name", "lora_synergy"), item["name"]


def validate_workflow(config, workflow_dir, repo, out_dir, count):
    pool_refs = []
    for section in ("prompt_pools", "negative_pools", "lora_pools"):
        for item in config.get(section, []):
            if "file" in item:
                pool_refs.append((section, item["file"]))

    missing_pools = []
    empty_pools = []
    for section, rel in pool_refs:
        path = workflow_dir / rel
        if not path.exists():
            missing_pools.append({"section": section, "file": rel})
            continue
        if not load_pool(path, required=False, normalize_prompt=(section != "lora_pools")):
            empty_pools.append({"section": section, "file": rel})

    folders_found, lora_index = scan_loras(repo, config)
    missing_loras = []
    resolved_loras = []
    for source, raw_name in iter_lora_config_names(config, workflow_dir):
        resolved = resolve_lora_name(raw_name, folders_found, lora_index, config)
        if resolved:
            resolved_loras.append({"source": source, "name": raw_name, "resolved": resolved})
        else:
            missing_loras.append({"source": source, "name": raw_name})

    samples = []
    max_prompt_chars = 0
    max_lora_count = 0
    for _ in range(max(1, count)):
        prompt, negative, choices, loras, lora_sources = compose_prompt(config, workflow_dir, repo)
        max_prompt_chars = max(max_prompt_chars, len(prompt))
        max_lora_count = max(max_lora_count, len(loras))
        samples.append(
            {
                "prompt_chars": len(prompt),
                "negative_chars": len(negative),
                "lora_count": len(loras),
                "loras": loras,
                "lora_sources": lora_sources,
                "choices": choices,
                "prompt": prompt,
            }
        )

    report = {
        "status": "ok" if not missing_pools and not missing_loras else "needs_attention",
        "sample_count": len(samples),
        "missing_pools": missing_pools,
        "empty_pools": empty_pools,
        "missing_loras": missing_loras,
        "resolved_lora_count": len(resolved_loras),
        "max_prompt_chars": max_prompt_chars,
        "max_lora_count": max_lora_count,
        "samples": samples[:10],
    }
    write_metadata(out_dir / "validation_report.json", report)
    log(
        "VALIDATION "
        f"status={report['status']} samples={len(samples)} "
        f"missing_pools={len(missing_pools)} missing_loras={len(missing_loras)} "
        f"max_prompt_chars={max_prompt_chars} max_loras={max_lora_count}"
    )
    if missing_pools or missing_loras:
        raise RuntimeError(f"Validation found {len(missing_pools)} missing pools and {len(missing_loras)} missing LoRAs.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["base", "full", "dry-run", "validate"], default="full")
    parser.add_argument("--count", type=int, default=None)
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    workflow_dir = Path(__file__).resolve().parent
    config = load_json(resolve_config_path(workflow_dir, args.config))
    repo = resolve_repo(workflow_dir, config)
    enable_console_color(config)
    count = args.count or int(config.get("count", 1))
    seed_root = args.seed if args.seed is not None else random.randint(1, 2_147_483_000)

    global RUN_LOG
    output_root = resolve_output_root(repo, config)
    cleanup_empty_run_folders(config, workflow_dir, output_root)
    out_dir = output_root / f"nightrun-{now_stamp()}"
    out_dir.mkdir(parents=True, exist_ok=True)
    RUN_LOG = out_dir / "run.log"
    stop_file = workflow_dir / "STOP_AFTER_CURRENT_IMAGE.txt"

    log_rich(
        [
            ("NIGHTRUN ", "bold"),
            (f"mode={args.mode} ", "bright_cyan"),
            (f"count={count} ", "white"),
            (f"seed_root={seed_root}", "dim"),
        ]
    )
    log(f"OUTPUT {out_dir}", "cyan")
    log_run_rules(args.mode, config, count)

    if args.mode == "validate":
        validate_workflow(config, workflow_dir, repo, out_dir, count)
        cleanup_empty_run_folders(config, workflow_dir, output_root)
        return

    if args.mode != "dry-run":
        ensure_forge(repo)
        set_options(config, repo)

    results = []
    final_images = []
    chill_cfg = long_run_chill_config(config, count)
    next_chill_at = schedule_next_chill(chill_cfg, 0)
    if next_chill_at is not None:
        log(f"First VRAM chill scheduled after generation {next_chill_at}.", "cyan")

    for index in range(1, count + 1):
        if stop_file.exists():
            log("Stop file found before next image. Ending batch.", "yellow")
            break

        prompt, negative, choices, loras, lora_sources = compose_prompt(config, workflow_dir, repo)
        base_steps = choose_base_steps(config)
        seed = seed_root + index
        stem = f"{index:04d}"
        base_cfg = config["base"]
        up_cfg = config["upscale"]
        base_path = out_dir / f"{stem}_base_{base_cfg['width']}x{base_cfg['height']}.png"
        up_path = out_dir / f"{stem}_upscale_{up_cfg['width']}x{up_cfg['height']}.png"
        prompt_path = out_dir / f"{stem}_prompt.txt"
        meta_path = out_dir / f"{stem}_metadata.json"

        prompt_path.write_text(
            "POSITIVE:\n" + prompt + "\n\nNEGATIVE:\n" + negative + "\n",
            encoding="utf-8",
        )

        meta = {
            "index": index,
            "seed": seed,
            "choices": choices,
            "loras": loras,
            "lora_sources": lora_sources,
            "base_steps": base_steps,
            "prompt": prompt,
            "negative_prompt": negative,
            "base_file": str(base_path),
            "upscale_file": None,
            "status": "planned",
            "gpu_before": get_gpu_stats(),
        }

        log_rich(
            [
                (f"[{stem}] ", "dim"),
                ("Nightrun image ", "bold"),
                (f"{index}/{count} ", "bright_cyan"),
                (f"seed={seed} ", "white"),
                (f"steps={base_steps} ", "bright_yellow"),
                (f"pools={len(choices)} ", "bright_green"),
                (f"loras={len(loras)}", "bright_magenta"),
            ]
        )
        log_prompt_map(stem, choices)
        if args.mode == "dry-run":
            meta["status"] = "dry-run"
            write_metadata(meta_path, meta)
            results.append(meta)
            log(f"[{stem}] Dry-run metadata written.", "green")
            continue

        try:
            wait_for_temperature(config)
            log(f"[{stem}] Base generation starting with {base_steps} steps.", "yellow")
            base_seconds = generate_base(
                config,
                prompt,
                negative,
                seed,
                base_steps,
                base_path,
                repo,
                phase_label=f"[{stem}] Base {index}/{count}",
            )
            meta["base_seconds"] = base_seconds
            meta["status"] = "base-ok"
            final_images.append(base_path)
            log(f"[{stem}] Base done in {base_seconds}s -> {base_path.name}", "green")

            should_upscale, upscale_reason = should_upscale_for_image(args.mode, config, index, base_steps)
            if should_upscale:
                wait_for_temperature(config)
                upscale_color = "magenta" if "below" in upscale_reason else "yellow"
                log(f"[{stem}] UPSCALE ACTIVE: {upscale_reason}.", upscale_color)
                log(f"[{stem}] Upscale starting.", upscale_color)
                upscale_seconds = upscale_image(
                    config,
                    prompt,
                    negative,
                    seed,
                    base_path,
                    up_path,
                    repo,
                    phase_label=f"[{stem}] Upscale {index}/{count}",
                )
                meta["upscale_seconds"] = upscale_seconds
                meta["upscale_reason"] = upscale_reason
                meta["upscale_file"] = str(up_path)
                meta["status"] = "upscale-ok"
                final_images[-1] = up_path
                log(f"[{stem}] Upscale done in {upscale_seconds}s -> {up_path.name}", "green")
            else:
                meta["upscale_reason"] = upscale_reason

        except Exception as exc:
            meta["status"] = "failed"
            meta["error"] = str(exc)
            log(f"[{stem}] FAILED {exc}", "red")

        meta["gpu_after"] = get_gpu_stats()
        write_metadata(meta_path, meta)
        results.append(meta)

        if stop_file.exists():
            log("Stop file found after current image. Ending batch.", "yellow")
            break

        if index < count:
            next_chill_at = run_long_chill(chill_cfg, len(results), next_chill_at, stop_file)
            if stop_file.exists():
                log("Stop file found after VRAM chill. Ending batch.", "yellow")
                break

        sleep_seconds = int(config.get("sleep_between_images_seconds", 0))
        if sleep_seconds > 0:
            log(f"[{stem}] Sleeping {sleep_seconds}s before next image.", "dim")
            time.sleep(sleep_seconds)

    summary = {
        "status": "OK",
        "mode": args.mode,
        "count_requested": count,
        "count_completed": len(results),
        "output_dir": str(out_dir),
        "seed_root": seed_root,
        "results": results,
    }
    write_metadata(out_dir / "summary.json", summary)
    make_contact_sheet(final_images, out_dir / "contact_sheet.jpg")
    removed_empty = cleanup_empty_run_folders(config, workflow_dir, output_root)
    current_removed = any(path.resolve() == out_dir.resolve() for path in removed_empty)
    log("FINISH Nightrun", "green")
    print("")
    if current_removed:
        print("Done. Current output folder had no images, so cleanup removed it:")
        print(out_dir)
    else:
        print("Done. Output folder:")
        print(out_dir)


RUN_LOG = None


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Interrupted by user.")
        sys.exit(130)
