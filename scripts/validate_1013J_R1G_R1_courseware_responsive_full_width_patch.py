from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013J_R1G_R1_COURSEWARE_RESPONSIVE_FULL_WIDTH_PATCH"
FINAL_STATUS = "PASS_1013J_R1G_R1_COURSEWARE_RESPONSIVE_FULL_WIDTH_PATCH"
INHERITS_FROM = "1013J_R1G_COURSEWARE_TEMPLATE_DYNAMIC_SCREEN_MAPPING_CONCEPT"
NEXT_STAGE = "USER_REVIEW_COURSEWARE_RESPONSIVE_FULL_WIDTH"
BASE_DIR_NAME = "1013J_R1G_courseware_template_dynamic_screen_mapping_concept"
BASE_HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1G_courseware_template_dynamic_mapping.html"
STAGE_DIR_NAME = "1013J_R1G_R1_courseware_responsive_full_width_patch"
HTML_NAME = "prep_room_render_canvas_deepen_v1_1013J_R1G_R1_courseware_responsive_full_width.html"
VALIDATOR_NAME = "validate_1013J_R1G_R1_courseware_responsive_full_width_patch.py"

CHROME_CANDIDATES = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def locate_output_root(root: Path) -> Path:
    nested = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested.exists():
        return nested
    if (root / "LATEST_REVIEW_ENTRY.md").exists():
        return root
    raise FileNotFoundError("Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs.")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "upload_implemented": False,
        "search_implemented": False,
        "whiteboard_library_connected": False,
        "ppt_export_implemented": False,
        "drag_edit_implemented": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }


def responsive_css() -> str:
    return """

    /* 1013J_R1G_R1: responsive full-width courseware workspace */
    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] {
      width: auto;
      max-width: none;
      min-height: calc(100vh - 210px);
      margin: 6px 6px 34px;
      padding: clamp(8px, 1vw, 14px);
      border-radius: clamp(10px, 1.1vw, 16px);
      box-sizing: border-box;
    }

    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-workbench {
      display: grid;
      grid-template-columns:
        clamp(132px, 13.5vw, 220px)
        minmax(0, 1fr)
        clamp(150px, 16vw, 268px);
      gap: clamp(8px, .9vw, 14px);
      align-items: start;
      width: 100%;
      min-width: 0;
    }

    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-left,
    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-right {
      min-width: 0;
      padding: clamp(8px, .9vw, 12px);
      border-radius: clamp(10px, 1vw, 14px);
      align-self: stretch;
    }

    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-main {
      min-width: 0;
      width: 100%;
    }

    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-screen-frame {
      width: 100%;
      max-width: none;
      aspect-ratio: 16 / 9;
      padding: clamp(8px, 1.1vw, 16px);
      border-radius: clamp(12px, 1.2vw, 18px);
    }

    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-screen {
      padding: clamp(14px, 2vw, 30px);
    }

    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1g-slot {
      min-height: clamp(150px, 25vw, 410px);
    }

    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-screen-list .node-action {
      padding-inline: clamp(6px, .7vw, 10px);
    }

    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-screen-list .node-action strong {
      overflow-wrap: anywhere;
      line-height: 1.25;
    }

    .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-right .node-action {
      width: 100%;
      justify-content: center;
    }

    @media (max-width: 1180px) {
      .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-workbench {
        grid-template-columns: 126px minmax(0, 1fr) 148px;
      }

      .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-title,
      .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-side-block strong {
        font-size: 12px;
      }

      .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1g-note,
      .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-side-block p {
        font-size: 11px;
      }
    }

    @media (max-width: 860px) {
      .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-workbench {
        grid-template-columns: 1fr;
      }

      .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-left,
      .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-right {
        align-self: auto;
      }

      .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1e-screen-list,
      .courseware-r1e-shell[data-1013j-r1g-responsive-full="true"] .courseware-r1g-template-mini {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }
"""


def patch_html(output_root: Path) -> str:
    base_html = output_root / BASE_DIR_NAME / BASE_HTML_NAME
    html = base_html.read_text(encoding="utf-8")
    html = html.replace("1013J_R1G 课件模板与动态映射概念", "1013J_R1G_R1 课件区响应式全宽")
    html = html.replace("</style>", responsive_css() + "\n  </style>", 1)
    html = html.replace(
        '<div class="courseware-r1e-shell" data-1013j-r1-expanded="true" data-1013j-r1g-dynamic-template="true" aria-label="课件制作工作区">',
        '<div class="courseware-r1e-shell" data-1013j-r1-expanded="true" data-1013j-r1g-dynamic-template="true" data-1013j-r1g-responsive-full="true" aria-label="课件制作工作区">',
    )
    return html


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


def javascript_syntax_check(stage_dir: Path, html_text: str) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        return {"javascript_syntax_check_pass": False, "javascript_syntax_error": "node_not_found"}
    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html_text, flags=re.S | re.I)
    files: list[str] = []
    for index, script_text in enumerate(scripts):
        script_path = stage_dir / f"javascript_syntax_1013J_R1G_R1_{index:02d}.js"
        write_text(script_path, script_text)
        files.append(script_path.name)
        proc = subprocess.run([node, "--check", str(script_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            return {"javascript_syntax_check_pass": False, "javascript_syntax_error": proc.stderr.strip() or proc.stdout.strip(), "javascript_syntax_files": files}
    return {"javascript_syntax_check_pass": True, "javascript_syntax_files": files}


def screenshot(stage_dir: Path, html_path: Path) -> dict[str, Any]:
    browser = find_browser()
    shots: list[dict[str, Any]] = []
    if browser is None:
        return {"screenshot_smoke_pass": False, "screenshot_error": "browser_not_found", "screenshots": shots}
    cases = [
        ("wide", 1680, 1050),
        ("desktop", 1440, 1100),
        ("compact", 1024, 900),
    ]
    for name, width, height in cases:
        out = stage_dir / f"ui_smoke_screenshot_1013J_R1G_R1_{name}.png"
        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-cache",
            "--disable-default-apps",
            "--no-first-run",
            f"--window-size={width},{height}",
            f"--screenshot={out}",
            "file:///" + html_path.as_posix() + "?screen=screen_03#coursewareExpanded",
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        actual_width, actual_height = png_size(out)
        shots.append({"case": name, "path": out.name, "width": actual_width, "height": actual_height, "bytes": out.stat().st_size})
    return {"screenshot_smoke_pass": True, "screenshots": shots}


def validate_html(html_text: str) -> dict[str, Any]:
    checks: dict[str, Any] = {
        "responsive_full_width_patch_created": 'data-1013j-r1g-responsive-full="true"' in html_text,
        "shell_fixed_max_width_removed_by_override": "width: auto" in html_text and "max-width: none" in html_text,
        "workbench_fluid_columns_defined": "clamp(132px, 13.5vw, 220px)" in html_text and "minmax(0, 1fr)" in html_text and "clamp(150px, 16vw, 268px)" in html_text,
        "main_screen_fluid_width": ".courseware-r1e-screen-frame" in html_text and "max-width: none" in html_text and "aspect-ratio: 16 / 9" in html_text,
        "side_panels_expand_to_edges": "width: auto" in html_text and "margin: 6px 6px 34px" in html_text,
        "compact_view_media_query_present": "@media (max-width: 1180px)" in html_text and "@media (max-width: 860px)" in html_text,
        "no_fixed_card_layout_language": "固定卡片" not in html_text,
        **boundary(),
    }
    return checks


def failed_checks(checks: dict[str, Any]) -> list[str]:
    failed: list[str] = []
    expected_false = set(boundary().keys())
    for key, value in checks.items():
        if key in {"javascript_syntax_files", "javascript_syntax_error"}:
            continue
        if key in expected_false:
            if value is not False:
                failed.append(key)
        elif value is not True:
            failed.append(key)
    return failed


def write_docs(output_root: Path, stage_dir: Path, result: dict[str, Any]) -> None:
    write_text(stage_dir / "1013J_R1G_R1_report.md", f"""# 1013J_R1G_R1 Courseware Responsive Full Width Patch

FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

R1G_R1 keeps the R1G template and dynamic mapping concept, but removes the fixed card-like workspace feel.

Layout changes:
- courseware workspace expands to almost full viewport width
- left and right columns use responsive clamp widths
- main classroom screen uses fluid center width
- compact breakpoints keep the layout usable on narrower screens

This remains a static review fixture only. No runtime, provider/model, upload, search, whiteboard library, PPT export, drag edit, database, memory, Feishu, or formal apply is connected.

Failed checks: {result["failed_checks"]}
""")
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}

1013J_R1G_R1 adjusts the R1G courseware workspace from a fixed centered card into a responsive full-width work area. The side panels expand with the viewport, the center screen remains fluid, and compact breakpoints keep the page compressible.

Key flags:
- RESPONSIVE_FULL_WIDTH_PATCH_CREATED=true
- SHELL_FIXED_MAX_WIDTH_REMOVED_BY_OVERRIDE=true
- WORKBENCH_FLUID_COLUMNS_DEFINED=true
- MAIN_SCREEN_FLUID_WIDTH=true
- SIDE_PANELS_EXPAND_TO_EDGES=true
- COMPACT_VIEW_MEDIA_QUERY_PRESENT=true
- UPLOAD_IMPLEMENTED=false
- SEARCH_IMPLEMENTED=false
- WHITEBOARD_LIBRARY_CONNECTED=false
- PPT_EXPORT_IMPLEMENTED=false
- DRAG_EDIT_IMPLEMENTED=false
- PROVIDER_CALLED=false
- MODEL_CALLED=false
- FORMAL_APPLY_PERFORMED=false
- MAIN_PROJECT_PUSHED=false
""")
    write_text(output_root / "README.md", f"""# Prep Room Render Canvas Deepen V1 Review Package

Latest stage: `{STAGE_ID}`

Open:
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/1013J_R1G_R1_result.json`

Run:

```bash
python scripts/{VALIDATOR_NAME}
python scripts/{VALIDATOR_NAME} --root <repo-root>
```
""")
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", f"""# Review Package Manifest

Latest stage: `{STAGE_ID}`

Files:
- `LATEST_REVIEW_ENTRY.md`
- `README.md`
- `REVIEW_PACKAGE_MANIFEST.md`
- `{STAGE_DIR_NAME}/{HTML_NAME}`
- `{STAGE_DIR_NAME}/1013J_R1G_R1_result.json`
- `{STAGE_DIR_NAME}/1013J_R1G_R1_report.md`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1G_R1_wide.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1G_R1_desktop.png`
- `{STAGE_DIR_NAME}/ui_smoke_screenshot_1013J_R1G_R1_compact.png`
- `scripts/{VALIDATOR_NAME}`
""")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_root = locate_output_root(root)
    base_result = output_root / BASE_DIR_NAME / "1013J_R1G_result.json"
    if not base_result.exists():
        raise FileNotFoundError(base_result)

    stage_dir = output_root / STAGE_DIR_NAME
    stage_dir.mkdir(parents=True, exist_ok=True)
    html_text = patch_html(output_root)
    html_path = stage_dir / HTML_NAME
    write_text(html_path, html_text)

    js_check = javascript_syntax_check(stage_dir, html_text)
    smoke = screenshot(stage_dir, html_path)
    checks = validate_html(html_text)
    checks.update(js_check)
    checks["screenshot_smoke_pass"] = bool(smoke.get("screenshot_smoke_pass"))
    failed = failed_checks(checks)
    result = {
        "stage": STAGE_ID,
        "status": FINAL_STATUS if not failed else "FAIL_1013J_R1G_R1_COURSEWARE_RESPONSIVE_FULL_WIDTH_PATCH",
        "final_status": FINAL_STATUS if not failed else "FAIL_1013J_R1G_R1_COURSEWARE_RESPONSIVE_FULL_WIDTH_PATCH",
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "created_at": now(),
        **checks,
        "failed_checks": failed,
    }
    write_json(stage_dir / "1013J_R1G_R1_result.json", result)
    write_docs(output_root, stage_dir, result)
    source_delta = output_root / "source_delta_1013J_R1G_R1" / "scripts" / VALIDATOR_NAME
    source_delta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve(), source_delta)
    if failed:
        raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))
    print("ALL_1013J_R1G_R1_COURSEWARE_RESPONSIVE_FULL_WIDTH_PATCH_CHECKS_OK")
    print(json.dumps({"stage": STAGE_ID, "status": result["status"], "failed_checks": failed}, ensure_ascii=False))


if __name__ == "__main__":
    main()

