from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


COLOR_PATTERNS = {
    "blue": r"\b(blue|sapphire|azure|navy|cobalt)\b",
    "cyan_teal": r"\b(cyan|teal|turquoise|aqua|electric cyan)\b",
    "red": r"\b(red|crimson|scarlet|ruby|blood)\b",
    "pink_magenta": r"\b(pink|rose|magenta)\b",
    "purple_violet": r"\b(purple|violet|lavender|plum)\b",
    "green": r"\b(green|emerald|mint|jade)\b",
    "gold_amber": r"\b(gold|golden|amber|honey)\b",
    "orange_copper": r"\b(orange|ember|copper|bronze)\b",
    "white_ivory": r"\b(white|ivory|pearl|opal)\b",
    "black_obsidian": r"\b(black|obsidian|charcoal|onyx)\b",
    "silver_steel": r"\b(silver|steel|chrome|metallic)\b",
    "rainbow_iridescent": r"\b(rainbow|iridescent|holographic|multicolor|multicolored|prismatic)\b",
}

CONCEPT_PATTERNS = {
    "candle": r"\b(candle|candles|candlelit|candlelight|candelabra|chandelier)\b",
    "cemetery": r"\b(cemetery|graveyard|tomb|mausoleum|coffin|crypt)\b",
    "vampire": r"\b(vampire|vampiric|fangs|blood-drinker)\b",
    "gothic": r"\b(gothic|cathedral|gargoyle|victorian|baroque)\b",
    "moon": r"\b(moon|moonlit|lunar|eclipse)\b",
    "blue_cyan": r"\b(blue|cyan|teal|aqua|turquoise|sapphire|azure|cobalt|navy)\b",
    "witch_magic": r"\b(witch|sorceress|spell|wand|arcane|rune|magic)\b",
    "sci_fi": r"\b(cyber|android|spaceship|starship|laser|hologram|mecha|neon)\b",
    "wasteland": r"\b(wasteland|raider|vault|radiation|scrapyard|ruined diner)\b",
}

WATCH_CATEGORIES = [
    "world_module",
    "module_identity",
    "genre_core",
    "genre_root",
    "genre",
    "concept",
    "character",
    "module_character_archetypes",
    "module_outfits",
    "clothing",
    "glamour_pose",
    "pose",
    "body_pose",
    "camera",
    "module_environments",
    "environment",
    "environment_rich",
    "module_props_equipment",
    "equipment",
    "style_layer",
    "artist_direction",
    "color_grade",
    "module_color_palettes",
]


def load_json(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def find_metadata(root):
    root = Path(root)
    if root.is_file() and root.name.endswith("_metadata.json"):
        return [root]
    return sorted(root.rglob("*_metadata.json"))


def flatten_choice(value):
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value:
        return [str(value)]
    return []


def category_choices(choices, category):
    values = flatten_choice(choices.get(category))
    if category == "world_module":
        values = [value for value in values if value not in {"coherent mode", "fusion mode"}]
    return values


def colors_in_text(text):
    lowered = text.lower()
    return [name for name, pattern in COLOR_PATTERNS.items() if re.search(pattern, lowered)]


def concepts_in_text(text):
    lowered = text.lower()
    return [name for name, pattern in CONCEPT_PATTERNS.items() if re.search(pattern, lowered)]


def ratio(count, total):
    return round(count / total, 3) if total else 0


def top_items(counter, limit):
    return [{"item": item, "count": count} for item, count in counter.most_common(limit)]


def analyze(root, top_n=12):
    files = find_metadata(root)
    category_counts = {name: Counter() for name in WATCH_CATEGORIES}
    color_counts = Counter()
    concept_counts = Counter()
    exact_prompt_counts = Counter()
    module_runs = Counter()
    tag_counts = []
    repeated_tag_prompts = 0
    samples = []

    for path in files:
        try:
            meta = load_json(path)
        except Exception:
            continue

        prompt = str(meta.get("prompt") or "")
        if prompt:
            exact_prompt_counts[prompt] += 1
            tags = [part.strip().lower() for part in prompt.split(",") if part.strip()]
            tag_counts.append(len(tags))
            if len(tags) != len(set(tags)):
                repeated_tag_prompts += 1
            for color in colors_in_text(prompt):
                color_counts[color] += 1
            for concept in concepts_in_text(prompt):
                concept_counts[concept] += 1

        choices = meta.get("choices") or {}
        for category in WATCH_CATEGORIES:
            for item in category_choices(choices, category):
                category_counts[category][item] += 1
                if category == "world_module":
                    module_runs[item] += 1

        samples.append(
            {
                "file": str(path),
                "status": meta.get("status"),
                "world_module": category_choices(choices, "world_module"),
                "color_grade": flatten_choice(choices.get("color_grade") or choices.get("module_color_palettes")),
                "pose": flatten_choice(choices.get("glamour_pose") or choices.get("pose") or choices.get("body_pose")),
                "camera": flatten_choice(choices.get("camera")),
                "environment": flatten_choice(choices.get("module_environments") or choices.get("environment")),
            }
        )

    total = len(samples)
    repeated_categories = {}
    for category, counter in category_counts.items():
        if not counter:
            continue
        most_common = counter.most_common(1)[0]
        repeated_categories[category] = {
            "unique": len(counter),
            "top_ratio": ratio(most_common[1], total),
            "top": top_items(counter, top_n),
        }

    warnings = []
    blue_cyan = color_counts["blue"] + color_counts["cyan_teal"]
    if total and blue_cyan / total > 0.45:
        warnings.append(f"Blue/cyan appears in {round(blue_cyan / total * 100, 1)}% of prompts.")
    if total and concept_counts["candle"] / total > 0.18:
        warnings.append(f"Candle/candlelight appears in {round(concept_counts['candle'] / total * 100, 1)}% of prompts.")
    for concept, count in concept_counts.most_common():
        if total >= 10 and count / total >= 0.35:
            warnings.append(f"Concept family '{concept}' may be dominating: {round(count / total * 100, 1)}%.")
    for category, data in repeated_categories.items():
        if data["top_ratio"] >= 0.22 and total >= 10:
            warnings.append(f"{category} may be repetitive: top item ratio {data['top_ratio']}.")
    repeated_prompts = sum(1 for _, count in exact_prompt_counts.items() if count > 1)
    if repeated_prompts:
        warnings.append(f"{repeated_prompts} exact prompt text(s) repeated.")
    if total and repeated_tag_prompts:
        warnings.append(f"{repeated_tag_prompts} prompt(s) contain repeated comma tags.")
    if tag_counts and max(tag_counts) > 80:
        warnings.append(f"Longest prompt has {max(tag_counts)} comma tags; local SD may behave cleaner below 80.")

    return {
        "root": str(root),
        "metadata_files": total,
        "warnings": warnings,
        "color_distribution": {
            color: {"count": count, "ratio": ratio(count, total)}
            for color, count in color_counts.most_common()
        },
        "concept_family_distribution": {
            concept: {"count": count, "ratio": ratio(count, total)}
            for concept, count in concept_counts.most_common()
        },
        "world_modules": top_items(module_runs, top_n),
        "tag_count": {
            "average": round(sum(tag_counts) / len(tag_counts), 1) if tag_counts else 0,
            "max": max(tag_counts) if tag_counts else 0,
            "prompts_with_repeated_tags": repeated_tag_prompts,
        },
        "repeated_categories": repeated_categories,
        "exact_prompt_repeats": top_items(Counter({k[:220]: v for k, v in exact_prompt_counts.items() if v > 1}), top_n),
        "samples": samples[: min(20, len(samples))],
    }


def print_summary(report):
    print("")
    print("Prompt Variety Analyzer")
    print("-----------------------")
    print(f"Metadata files: {report['metadata_files']}")
    if report["warnings"]:
        print("")
        print("Warnings")
        for warning in report["warnings"]:
            print(f"- {warning}")
    else:
        print("No major repetition warnings.")
    print("")
    print("Top colors")
    for color, data in list(report["color_distribution"].items())[:10]:
        print(f"- {color}: {data['count']} ({data['ratio']})")
    print("")
    print("Top concept families")
    for concept, data in list(report["concept_family_distribution"].items())[:10]:
        print(f"- {concept}: {data['count']} ({data['ratio']})")
    print("")
    print("Tag count")
    tags = report.get("tag_count", {})
    print(f"- average: {tags.get('average', 0)}")
    print(f"- max: {tags.get('max', 0)}")
    print(f"- prompts with repeated tags: {tags.get('prompts_with_repeated_tags', 0)}")
    print("")
    print("Top repeated categories")
    for category, data in report["repeated_categories"].items():
        top = data["top"][0] if data["top"] else None
        if top:
            print(f"- {category}: {top['count']}x {top['item']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="Output folder or test-renders root to scan.")
    parser.add_argument("--top", type=int, default=12)
    parser.add_argument("--report", default=None, help="Optional JSON report path.")
    args = parser.parse_args()

    report = analyze(Path(args.root), top_n=args.top)
    print_summary(report)
    if args.report:
        path = Path(args.report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print("")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
