"""Compatibility layer for older scripts that imported nightrun_engine.

New code should import from prompt_engine, lora_resolver, forge_client,
runner, or validation directly.
"""

import nightrun_runtime as _runtime

from forge_client import *  # noqa: F401,F403
from lora_resolver import *  # noqa: F401,F403
from prompt_engine import *  # noqa: F401,F403
from runner import *  # noqa: F401,F403
from validation import *  # noqa: F401,F403
from nightrun_runtime import (
    ANSI_ENABLED,
    CATEGORY_COLORS,
    CATEGORY_COLOR_CYCLE,
    COLORS,
    EMPTY_CLEANUP_SESSION_DECISION,
    LIVE_STATUS_WIDTH,
    PRINT_LOCK,
    RESET,
    RUN_LOG,
    SPINNER_FRAMES,
    WORLD_MODULE_CACHE,
    category_color,
    clear_live_status,
    colorize,
    compact_choice_value,
    configured_path,
    console_live_status,
    console_status,
    enable_console_color,
    format_seconds,
    load_cleanup_preference,
    load_json,
    load_world_modules,
    load_world_modules_from_catalog,
    log,
    log_prompt_map,
    log_rich,
    module_filter_signature,
    module_pick_count,
    module_search_text,
    module_source_keys,
    now_stamp,
    pattern_matches_any,
    resolve_config_path,
    resolve_output_root,
    resolve_repo,
    world_module_allowed_by_config,
)


def set_run_log(path):
    _runtime.RUN_LOG = path
    globals()["RUN_LOG"] = path
