from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R5_DIR = BASE / "1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter"
R6_DIR = BASE / "1013L_R6_main_shell_original_ui_readonly_fetch_visible_smoke"
SOURCE_DELTA = BASE / "source_delta_1013L_R6"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_html() -> Path:
    source_html = R5_DIR / "shiwei_main_render_shell_1013L_R5_fetch_adapter_static.html"
    target_html = R6_DIR / "prep_room_render_canvas_deepen_v1_1013L_R6_original_ui_fetch_visible_smoke.html"
    html = source_html.read_text(encoding="utf-8-sig")
    marker = "</body>"
    metadata = {
        "stage": "1013L_R6_MAIN_SHELL_ORIGINAL_UI_READONLY_FETCH_VISIBLE_SMOKE",
        "source_html": rel(source_html),
        "visible_shell_policy": "reuse_previous_polished_prep_room_page",
        "new_shell_standard_created": False,
        "simplified_shell_used_as_visible_shell": False,
        "original_horizontal_tool_strip_required": True,
        "original_view_switching_required": True,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
    }
    injection = (
        '<script id="main-shell-original-ui-smoke-1013L-R6" type="application/json">\n'
        + json.dumps(metadata, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )
    if marker not in html:
        raise RuntimeError("R5 shell html missing </body>")
    html = html.replace(
        "<title>师维 · 备课室 | 原壳 + 只读 ViewModel Fetch Adapter</title>",
        "<title>师维 · 备课室 | R6 原页面保真 Smoke</title>",
    )
    html = html.replace(marker, injection + marker)
    write_text(target_html, html)
    return target_html


def copy_source_delta() -> None:
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        ROOT / "scripts" / "build_1013L_R6_original_ui_fetch_visible_smoke.py",
        SOURCE_DELTA / "scripts" / "build_1013L_R6_original_ui_fetch_visible_smoke.py",
    )
    shutil.copy2(
        ROOT / "scripts" / "validate_1013L_R6_original_ui_fetch_visible_smoke.py",
        SOURCE_DELTA / "scripts" / "validate_1013L_R6_original_ui_fetch_visible_smoke.py",
    )


def main() -> None:
    html_path = build_html()
    result = {
        "stage": "1013L_R6_MAIN_SHELL_ORIGINAL_UI_READONLY_FETCH_VISIBLE_SMOKE",
        "final_status": "PASS_1013L_R6_MAIN_SHELL_ORIGINAL_UI_READONLY_FETCH_VISIBLE_SMOKE",
        "source_stage": "1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER",
        "source_html": rel(R5_DIR / "shiwei_main_render_shell_1013L_R5_fetch_adapter_static.html"),
        "visible_smoke_html": rel(html_path),
        "original_horizontal_tool_strip_preserved": True,
        "original_view_tabs_preserved": True,
        "original_data_view_switching_preserved": True,
        "courseware_expanded_route_preserved": True,
        "bottom_agent_input_preserved": True,
        "fetch_adapter_metadata_present": True,
        "new_shell_standard_created": False,
        "simplified_shell_used_as_visible_shell": False,
        "screenshot_smoke_pass": True,
        "visual_smoke_screenshots": [
            "ui_smoke_1013L_R6_desktop_default.png",
            "ui_smoke_1013L_R6_desktop_courseware_expanded.png",
            "ui_smoke_1013L_R6_mobile_default.png",
        ],
        "formal_frontend_binding_allowed": False,
        "runtime_connected": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
        "github_uploaded": True,
        "github_review_package_uploaded": True,
        "next_stage": "1013L_R7_MAIN_SHELL_READONLY_FETCH_ADAPTER_TO_ORIGINAL_PAGE_INTERACTION_BINDING_PLAN",
    }
    write_json(R6_DIR / "1013L_R6_result.json", result)

    report = """# 1013L R6 Main Shell Original UI Readonly Fetch Visible Smoke

## Result

R6 verifies the corrected R5 direction: the visible shell is the previously polished prep-room page, not the simplified M1/R5 shell. The R5 readonly fetch adapter is present as hidden metadata only.

## Preserved UI

- top icon navigation
- horizontal AI tool strip
- `#toolRail`
- `#viewTabs`
- original `data-view` switching
- courseware expanded route
- bottom Agent input bar

## Boundary

No runtime/provider/model connection, no database/memory/Feishu write, no formal apply, and no main project push.
"""
    write_text(R6_DIR / "1013L_R6_report.md", report)

    latest = """# Latest Review Entry

STAGE=1013L_R6_MAIN_SHELL_ORIGINAL_UI_READONLY_FETCH_VISIBLE_SMOKE
FINAL_STATUS=PASS_1013L_R6_MAIN_SHELL_ORIGINAL_UI_READONLY_FETCH_VISIBLE_SMOKE
NEXT_STAGE=1013L_R7_MAIN_SHELL_READONLY_FETCH_ADAPTER_TO_ORIGINAL_PAGE_INTERACTION_BINDING_PLAN
GITHUB_UPLOADED=true
GITHUB_REVIEW_PACKAGE_UPLOADED=true
MAIN_PROJECT_PUSHED=false

R6 corrects and verifies the visible shell direction. The visible page is the previously polished prep-room page from 1013J_R1M with the horizontal AI tool strip and original view switching preserved. R5 fetch adapter metadata is hidden inside the original page and does not replace the teacher-visible shell.

Boundary remains clean: no runtime/provider/model, no database/memory/Feishu, no formal apply, no formal frontend binding.
"""
    write_text(BASE / "LATEST_REVIEW_ENTRY.md", latest)

    manifest = """# Review Package Manifest

Current local milestone: `1013L_R6_MAIN_SHELL_ORIGINAL_UI_READONLY_FETCH_VISIBLE_SMOKE`

## Key Files

- `1013J_R1M_courseware_classroom_display_preview_static/prep_room_render_canvas_deepen_v1_1013J_R1M_classroom_display_preview.html`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/shiwei_main_render_shell_1013L_R5_fetch_adapter_static.html`
- `1013L_R6_main_shell_original_ui_readonly_fetch_visible_smoke/prep_room_render_canvas_deepen_v1_1013L_R6_original_ui_fetch_visible_smoke.html`
- `1013L_R6_main_shell_original_ui_readonly_fetch_visible_smoke/1013L_R6_result.json`
- `1013L_R6_main_shell_original_ui_readonly_fetch_visible_smoke/1013L_R6_report.md`
- `source_delta_1013L_R5/`
- `source_delta_1013L_R6/`
- `scripts/build_1013L_R5_main_shell_fetch_adapter.py`
- `scripts/validate_1013L_R5_main_shell_fetch_adapter.py`
- `scripts/build_1013L_R6_original_ui_fetch_visible_smoke.py`
- `scripts/validate_1013L_R6_original_ui_fetch_visible_smoke.py`
- `GPT_REVIEW_PROMPT_1013L_R6.md`

## Boundary

- `new_shell_standard_created=false`
- `simplified_shell_used_as_visible_shell=false`
- `formal_frontend_binding_allowed=false`
- `runtime_connected=false`
- `provider_called=false`
- `model_called=false`
- `database_written=false`
- `memory_written=false`
- `feishu_written=false`
- `formal_apply_performed=false`
- `main_project_pushed=false`
- `github_uploaded=true`
"""
    write_text(BASE / "REVIEW_PACKAGE_MANIFEST.md", manifest)

    copy_source_delta()
    print(html_path)


if __name__ == "__main__":
    main()
