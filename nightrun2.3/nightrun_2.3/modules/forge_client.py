"""Forge API startup, option setting, txt2img, img2img, and GPU guards."""

from nightrun_runtime import (
    API,
    ProgressReporter,
    api_alive,
    ensure_forge,
    generate_base,
    get_api_progress,
    get_gpu_stats,
    get_gpu_temp,
    post_api,
    progress_bar,
    progress_worker,
    set_options,
    upscale_image,
    wait_for_temperature,
    write_base64_image,
)
