from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6N_R2_CENTERED_PAGE_LEFT_ALIGNED_TEXT_PATCH"
FINAL_STATUS = "PASS_1013I_R6N_R2_CENTERED_PAGE_LEFT_ALIGNED_TEXT_PATCH"
INHERITS_FROM = "1013I_R6N_R1_CENTERED_NUMBERED_TEXT_READING_PATCH"
NEXT_STAGE = "USER_REVIEW_BIG_UNIT_TEXT_READING_PAGE"
STAGE_DIR_NAME = "1013I_R6N_R2_centered_page_left_aligned_text_patch"
R6N_R1_DIR_NAME = "1013I_R6N_R1_centered_numbered_text_reading_patch"
HTML_NAME = "prep_room_render_canvas_deepen_v1_R6N_R2_centered_page_left_aligned_text.html"
VALIDATOR_NAME = "validate_1013I_R6N_R2_centered_page_left_aligned_text_patch.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]
RAW_KEYS = ["unit_theme", "big_idea", "student_context", "performance_task", "learning_stages", "formal_apply"]
SECRET_PATTERNS = [re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"), re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}")]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "REVIEW_PACKAGE_MANIFEST.md").exists() and (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "html_modified": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def r6n_r2_css() -> str:
    return """

    /* 1013I_R6N_R2: center the page block, keep text left-aligned */
    .nb-unit-reading-doc {
      max-width: 720px;
      margin-left: auto;
      margin-right: auto;
      text-align: left;
    }

    .nb-unit-reading-head {
      text-align: left;
    }

    .nb-unit-reading-head p {
      margin-left: 0;
      margin-right: 0;
    }

    .nb-unit-reading-section h3,
    .nb-unit-reading-section p {
      text-align: left;
    }

    .nb-reading-actions,
    .nb-reading-material-buttons {
      justify-content: flex-start;
    }
"""


def build_html(output_root: Path) -> str:
    base = output_root / R6N_R1_DIR_NAME / "prep_room_render_canvas_deepen_v1_R6N_R1_centered_numbered_text_reading.html"
    source = base.read_text(encoding="utf-8")
    source = source.replace("师维 · 备课室 | R6N_R1 居中序号文本", "师维 · 备课室 | R6N_R2 居中版心左对齐文本")
    source = source.replace("\n  </style>", r6n_r2_css() + "\n  </style>", 1)
    source = source.replace('data-r6n-r1-centered-numbered-static="true"', 'data-r6n-r1-centered-numbered-static="true" data-r6n-r2-left-aligned-text="true"')
    source = source.replace('data-r6n-r1-centered-numbered-page="true"', 'data-r6n-r1-centered-numbered-page="true" data-r6n-r2-left-aligned-page="true"')
    source = source.replace(
        "<!-- 1013I_R6N_R1: centered numbered text-reading patch; preview only, no runtime/provider/formal apply. -->",
        "<!-- 1013I_R6N_R2: centered page block with left-aligned text; preview only, no runtime/provider/formal apply. -->",
    )
    return source


def extract_function_body(source: str, name: str, next_name: str) -> str:
    start = source.index(f"    function {name}")
    end = source.index(f"    function {next_name}", start)
    return source[start:end]


def find_browser() -> Path | None:
    for path in CHROME_CANDIDATES:
        if path.exists():
            return path
    return None


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8].hex() != "89504e470d0a1a0a":
        raise ValueError(f"Not a PNG: {path}")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def create_screenshots(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    screenshots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": screenshots}
    for viewport in [{"id": "desktop", "width": 1440, "height": 1100}, {"id": "mobile", "width": 390, "height": 1100}]:
        out = stage_dir / f"ui_smoke_screenshot_1013I_R6N_R2_{viewport['id']}.png"
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-cache",
            "--disable-default-apps",
            "--no-first-run",
            f"--window-size={viewport['width']},{viewport['height']}",
            f"--screenshot={out}",
            "file:///" + html_path.as_posix(),
        ]
        run = subprocess.run(cmd, text=True, capture_output=True, timeout=60)
        if run.returncode != 0:
            return {"screenshot_smoke_pass": False, "screenshot_error": run.stderr[-500:], "screenshots": screenshots}
        width, height = png_size(out)
        screenshots.append({"viewport": viewport["id"], "path": out.name, "width": width, "height": height, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": all(item["bytes"] > 10000 for item in screenshots), "screenshot_error": None, "screenshots": screenshots}


def scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() and path.suffix.lower() != ".png" else ""
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path))
                break
    return hits


def build_result(html_path: Path, visual_smoke: dict[str, Any]) -> dict[str, Any]:
    html_text = html_path.read_text(encoding="utf-8")
    body = extract_function_body(html_text, "renderBigUnitPrepSurface(view)", "renderBigUnitPrepRightPanel(view)")
    hits = [key for key in RAW_KEYS if key in body]
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "html_fixture_created": html_path.exists(),
        "page_block_centered": "margin-left: auto;" in html_text and "margin-right: auto;" in html_text,
        "text_left_aligned": all(text in html_text for text in [
            ".nb-unit-reading-head {\n      text-align: left;",
            ".nb-unit-reading-section h3,\n    .nb-unit-reading-section p {\n      text-align: left;",
            "justify-content: flex-start;",
        ]),
        "not_all_lines_center_aligned": "data-r6n-r2-left-aligned-page" in html_text,
        "numbered_sections_present": all(f">{i:02d}<" in body for i in range(1, 7)),
        "section_titles_corrected": all(text in body for text in ["单元方向", "学生起点", "表现任务", "学习推进", "课堂支架", "资料补充"]),
        "old_explanation_not_section_title": "<h3>这个单元想带学生走向哪里" not in body and "这个单元想带学生走向哪里：" in body,
        "main_surface_raw_engineering_field_hits": hits,
        "engineering_fields_not_primary_surface": hits == [],
        "left_unit_entry_kept": "data-big-unit-entry" in html_text and "nb-unit-entry-badge" in html_text,
        "single_lesson_entries_kept": "data-node^='nb-lesson'" in html_text,
        "top_level_nav_not_modified": "大单元</a>" not in html_text,
        "preview_only_badges_visible": "教师确认前不写入正式备课本" in html_text,
        "screenshot_smoke_pass": visual_smoke.get("screenshot_smoke_pass") is True,
        "screenshot_count": len(visual_smoke.get("screenshots", [])),
        "secret_scan_hits": [],
        **boundary(),
    }
    required = [
        "html_fixture_created",
        "page_block_centered",
        "text_left_aligned",
        "not_all_lines_center_aligned",
        "numbered_sections_present",
        "section_titles_corrected",
        "old_explanation_not_section_title",
        "engineering_fields_not_primary_surface",
        "left_unit_entry_kept",
        "single_lesson_entries_kept",
        "top_level_nav_not_modified",
        "preview_only_badges_visible",
        "screenshot_smoke_pass",
    ]
    failures = [key for key in required if result.get(key) is not True]
    if hits:
        failures.append("main_surface_raw_engineering_field_hits")
    result["failed_checks"] = failures
    result["final_status"] = FINAL_STATUS if not failures else "FAIL_1013I_R6N_R2_CENTERED_PAGE_LEFT_ALIGNED_TEXT_PATCH"
    return result


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    latest = f"""# Latest Review Entry

```text
REVIEW_STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_RECOMMENDED_STAGE={NEXT_STAGE}
PAGE_BLOCK_CENTERED={str(result["page_block_centered"]).lower()}
TEXT_LEFT_ALIGNED={str(result["text_left_aligned"]).lower()}
NOT_ALL_LINES_CENTER_ALIGNED={str(result["not_all_lines_center_aligned"]).lower()}
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
MAIN_PROJECT_PUSHED=false
```

## Summary

R6N_R2 keeps the reading document as a centered page block, but restores left alignment for the title, paragraphs, section headings, and action rows. It fixes the misunderstanding that every line should be centered.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "README.md", f"""# PREP_ROOM_RENDER_CANVAS_DEEPEN_V1

Current stage: `{STAGE_ID}`

R6N_R2 centers the overall reading page block while keeping all text left-aligned.
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

```text
current_stage={STAGE_ID}
final_status={result["final_status"]}
main_project_pushed=false
```

## Key Files

```text
{STAGE_DIR_NAME}/{HTML_NAME}
{STAGE_DIR_NAME}/1013I_R6N_R2_result.json
{STAGE_DIR_NAME}/1013I_R6N_R2_report.md
scripts/{VALIDATOR_NAME}
source_delta_1013I_R6N_R2/scripts/{VALIDATOR_NAME}
```
""")
    write_text(stage_dir / "1013I_R6N_R2_report.md", f"""# 1013I_R6N_R2 Report

This patch centers the page block, not every line.

- page block centered: `{result["page_block_centered"]}`
- text left aligned: `{result["text_left_aligned"]}`
- not all lines center aligned: `{result["not_all_lines_center_aligned"]}`
- screenshot smoke pass: `{result["screenshot_smoke_pass"]}`

Boundary: no runtime, provider/model, formal apply, database, memory, Feishu, or main-project push.
""")


def validate_result(result: dict[str, Any]) -> None:
    if result.get("failed_checks"):
        raise SystemExit("R6N_R2 validation failed: " + ", ".join(result["failed_checks"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    output_root = resolve_output_root(args.root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, build_html(output_root))
    visual_smoke = create_screenshots(stage_dir, html_path)
    write_json(stage_dir / "visual_smoke_1013I_R6N_R2.json", visual_smoke)
    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path])
    write_json(stage_dir / "1013I_R6N_R2_result.json", result)
    write_json(stage_dir / "centered_page_left_aligned_text_patch_manifest_1013I_R6N_R2.json", {"stage": STAGE_ID, "inherits_from": INHERITS_FROM, "boundary": boundary()})
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013I_R6N_R2" / "scripts"
    source_delta.mkdir(parents=True, exist_ok=True)
    target = source_delta / VALIDATOR_NAME
    if Path(__file__).resolve() != target:
        shutil.copy2(Path(__file__).resolve(), target)
    result = build_result(html_path, visual_smoke)
    result["secret_scan_hits"] = scan_secrets([html_path, output_root / "LATEST_REVIEW_ENTRY.md", output_root / "README.md"])
    write_json(stage_dir / "1013I_R6N_R2_result.json", result)
    write_docs(output_root, stage_dir, result)
    validate_result(result)
    print("ALL_1013I_R6N_R2_CENTERED_PAGE_LEFT_ALIGNED_TEXT_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["final_status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
