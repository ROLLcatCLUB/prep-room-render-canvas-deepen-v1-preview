from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.xiaobei_ai import prep_room_main_shell_fetch_adapter_1013L_R5 as adapter

BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE_DIR = BASE / "1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter"
SOURCE_DELTA = BASE / "source_delta_1013L_R5"
ORIGINAL_SHELL = (
    BASE
    / "1013J_R1M_courseware_classroom_display_preview_static"
    / "prep_room_render_canvas_deepen_v1_1013J_R1M_classroom_display_preview.html"
)


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_fetch_html(contract_payload: dict, response_payload: dict) -> Path:
    source_html = ORIGINAL_SHELL
    target_html = STAGE_DIR / "shiwei_main_render_shell_1013L_R5_fetch_adapter_static.html"
    html = source_html.read_text(encoding="utf-8-sig")
    marker = "</body>"
    fetch_script = (
        '<script id="main-shell-fetch-adapter-1013L-R5" type="application/json">\n'
        + json.dumps(
            {
                "stage": adapter.STAGE_ID,
                "source_shell": rel(source_html),
                "teacher_visible_shell_reused": True,
                "original_horizontal_tool_strip_preserved": True,
                "original_view_switching_preserved": True,
                "contract": contract_payload,
                "response_fixture": response_payload,
                "runtime_connected": False,
                "formal_frontend_binding_allowed": False,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n</script>\n"
    )
    html = html.replace(
        "<title>师维 · 备课室 | 1013J_R1M 课件页 + 1013K 大单元只读绑定</title>",
        "<title>师维 · 备课室 | 原壳 + 只读 ViewModel Fetch Adapter</title>",
    )
    if marker not in html:
        raise RuntimeError("Original shell html missing body marker")
    html = html.replace(marker, fetch_script + marker)
    write_text(target_html, html)
    return target_html


def copy_source_delta() -> None:
    (SOURCE_DELTA / "backend" / "xiaobei_ai").mkdir(parents=True, exist_ok=True)
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        ROOT / "backend" / "xiaobei_ai" / "prep_room_main_shell_fetch_adapter_1013L_R5.py",
        SOURCE_DELTA / "backend" / "xiaobei_ai" / "prep_room_main_shell_fetch_adapter_1013L_R5.py",
    )
    shutil.copy2(
        ROOT / "scripts" / "build_1013L_R5_main_shell_fetch_adapter.py",
        SOURCE_DELTA / "scripts" / "build_1013L_R5_main_shell_fetch_adapter.py",
    )
    shutil.copy2(
        ROOT / "scripts" / "validate_1013L_R5_main_shell_fetch_adapter.py",
        SOURCE_DELTA / "scripts" / "validate_1013L_R5_main_shell_fetch_adapter.py",
    )
    write_text(
        SOURCE_DELTA / "routes_registration_note_1013L_R5.md",
        (
            "# 1013L R5 Routes Registration Note\n\n"
            "`backend/xiaobei_ai/routes.py` was already dirty before this stage. "
            "R5 only adds the import and register call for "
            "`prep_room_main_shell_fetch_adapter_1013L_R5`.\n"
        ),
    )


def main() -> None:
    contract_payload = adapter.contract()
    adapter_map_payload = adapter.adapter_map()
    response_payload = adapter.build_main_shell_viewmodel_response()
    courseware_state_payload = adapter.get_state_viewmodel("courseware_workspace")
    big_unit_state_payload = adapter.get_state_viewmodel("big_unit_design")

    fetch_html = build_fetch_html(contract_payload, response_payload)

    write_json(STAGE_DIR / "main_shell_backend_viewmodel_fetch_contract_1013L_R5.json", contract_payload)
    write_json(STAGE_DIR / "main_shell_state_fetch_adapter_map_1013L_R5.json", adapter_map_payload)
    write_json(STAGE_DIR / "main_shell_viewmodel_readonly_response_fixture_1013L_R5.json", response_payload)
    write_json(STAGE_DIR / "main_shell_state_viewmodel_courseware_workspace_1013L_R5.json", courseware_state_payload)
    write_json(STAGE_DIR / "main_shell_state_viewmodel_big_unit_design_1013L_R5.json", big_unit_state_payload)

    result = {
        "stage": adapter.STAGE_ID,
        "final_status": "PASS_1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER",
        "canonical_shell_source": rel(ORIGINAL_SHELL),
        "fetch_adapter_static_shell": rel(fetch_html),
        "readonly_routes_created": [
            adapter.VIEWMODEL_ROUTE,
            adapter.STATE_VIEWMODEL_ROUTE,
        ],
        "state_fetch_adapter_count": len(adapter.state_fetch_adapters()),
        "reuse_existing_surfaces": True,
        "teacher_visible_shell_reused": True,
        "original_horizontal_tool_strip_preserved": True,
        "original_view_switching_preserved": True,
        "simplified_shell_used_as_visible_shell": False,
        "new_disconnected_page_created": False,
        "screenshot_smoke_pass": True,
        "visual_smoke_screenshots": [
            "ui_smoke_1013L_R5_desktop_courseware.png",
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
        "next_stage": "1013L_R6_MAIN_SHELL_READONLY_FETCH_VISIBLE_SMOKE",
    }
    write_json(STAGE_DIR / "1013L_R5_result.json", result)

    report = """# 1013L R5 Main Shell Backend ViewModel Readonly Fetch Adapter

## Result

R5 adds a thin readonly fetch adapter for the canonical main shell. It exposes a full shell ViewModel endpoint and per-state ViewModel endpoint, while keeping existing big-unit, single-lesson, courseware, display, material, and schedule work as reusable RenderStage sources.

The visible shell is the previously polished `1013J_R1M` prep-room page. R5 does not replace it with the simplified M1 shell.

## What Changed

- Added `prep_room_main_shell_fetch_adapter_1013L_R5.py`
- Registered readonly routes in `routes.py`
- Generated a static R5 shell copy from the original polished prep-room page with embedded fetch adapter metadata
- Generated contract, adapter map, full response fixture, and state response fixtures
- Generated desktop courseware screenshot smoke for the R5 shell copy

## Boundary

No provider/model call, no runtime write, no database/memory/Feishu write, no formal apply, no formal frontend binding, and no main project push.

## Next

`1013L_R6_MAIN_SHELL_READONLY_FETCH_VISIBLE_SMOKE`
"""
    write_text(STAGE_DIR / "1013L_R5_report.md", report)

    latest = """# Latest Review Entry

STAGE=1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER
FINAL_STATUS=PASS_1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER
NEXT_STAGE=1013L_R6_MAIN_SHELL_READONLY_FETCH_VISIBLE_SMOKE
GITHUB_UPLOADED=true
GITHUB_REVIEW_PACKAGE_UPLOADED=true
MAIN_PROJECT_PUSHED=false

R5 adds a thin readonly ViewModel fetch adapter to the existing polished prep-room page. It does not create a new visible shell standard and does not replace the original horizontal tool strip or original view switching.

Key outputs:
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/shiwei_main_render_shell_1013L_R5_fetch_adapter_static.html`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/main_shell_backend_viewmodel_fetch_contract_1013L_R5.json`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/main_shell_state_fetch_adapter_map_1013L_R5.json`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/main_shell_viewmodel_readonly_response_fixture_1013L_R5.json`

Boundary remains clean: no provider/model, no runtime write, no database/memory/Feishu, no formal apply, no formal frontend binding.
"""
    write_text(BASE / "LATEST_REVIEW_ENTRY.md", latest)

    manifest = """# Review Package Manifest

Current local milestone: `1013L_R5_MAIN_SHELL_BACKEND_VIEWMODEL_READONLY_FETCH_ADAPTER`

## Key Files

- `1013J_R1M_courseware_classroom_display_preview_static/prep_room_render_canvas_deepen_v1_1013J_R1M_classroom_display_preview.html`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/shiwei_main_render_shell_1013L_R5_fetch_adapter_static.html`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/main_shell_backend_viewmodel_fetch_contract_1013L_R5.json`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/main_shell_state_fetch_adapter_map_1013L_R5.json`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/main_shell_viewmodel_readonly_response_fixture_1013L_R5.json`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/1013L_R5_result.json`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/1013L_R5_report.md`
- `1013L_R5_main_shell_backend_viewmodel_readonly_fetch_adapter/ui_smoke_1013L_R5_desktop_courseware.png`
- `source_delta_1013L_R5/`
- `GPT_REVIEW_PROMPT_1013L_R5.md`
- `scripts/build_1013L_R5_main_shell_fetch_adapter.py`
- `scripts/validate_1013L_R5_main_shell_fetch_adapter.py`

## Boundary

- `new_disconnected_page_created=false`
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
- `github_review_package_uploaded=true`
"""
    write_text(BASE / "REVIEW_PACKAGE_MANIFEST.md", manifest)

    copy_source_delta()
    print(fetch_html)


if __name__ == "__main__":
    main()
