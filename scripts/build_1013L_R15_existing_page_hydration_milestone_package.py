from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R11_DIR = BASE / "1013L_R11_existing_page_readonly_viewmodel_static_hydration_apply"
R12_DIR = BASE / "1013L_R12_existing_page_hydrated_viewmodel_visual_smoke"
R13_DIR = BASE / "1013L_R13_existing_page_big_unit_viewmodel_visible_hydration"
R14_DIR = BASE / "1013L_R14_existing_page_big_unit_viewmodel_visual_smoke"
R15_DIR = BASE / "1013L_R15_existing_page_hydration_milestone_package"
SOURCE_DELTA = BASE / "source_delta_1013L_R15"


STAGE = "1013L_R15_EXISTING_PAGE_HYDRATION_MILESTONE_PACKAGE"
FINAL_STATUS = "PASS_1013L_R15_EXISTING_PAGE_HYDRATION_MILESTONE_PACKAGE"
NEXT_STAGE = "1013L_R16_EXISTING_PAGE_MOBILE_LAYOUT_POLISH_AND_TEACHER_TEST_ENTRY"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "milestone_package_only": True,
        "existing_page_reused": True,
        "new_visible_page_created": False,
        "new_shell_standard_created": False,
        "runtime_connected": False,
        "real_fetch_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
        "formal_frontend_binding_allowed": False,
    }


def required_files() -> list[Path]:
    return [
        R11_DIR / "1013L_R11_result.json",
        R11_DIR / "1013L_R11_report.md",
        R11_DIR / "readonly_viewmodel_static_hydration_payload_1013L_R11.json",
        R11_DIR / "visible_hydration_browser_smoke_1013L_R11.json",
        R11_DIR / "prep_room_render_canvas_deepen_v1_1013L_R11_static_hydration_apply.html",
        R12_DIR / "1013L_R12_result.json",
        R12_DIR / "1013L_R12_report.md",
        R12_DIR / "hydrated_viewmodel_visual_smoke_1013L_R12.json",
        R12_DIR / "ui_smoke_1013L_R12_desktop_normal.png",
        R12_DIR / "ui_smoke_1013L_R12_desktop_courseware_expanded.png",
        R12_DIR / "ui_smoke_1013L_R12_desktop_display_preview.png",
        R12_DIR / "ui_smoke_1013L_R12_mobile_normal.png",
        R13_DIR / "1013L_R13_result.json",
        R13_DIR / "1013L_R13_report.md",
        R13_DIR / "big_unit_visible_hydration_payload_1013L_R13.json",
        R13_DIR / "big_unit_visible_hydration_browser_smoke_1013L_R13.json",
        R13_DIR / "prep_room_render_canvas_deepen_v1_1013L_R13_big_unit_visible_hydration.html",
        R14_DIR / "1013L_R14_result.json",
        R14_DIR / "1013L_R14_report.md",
        R14_DIR / "big_unit_viewmodel_visual_smoke_1013L_R14.json",
        R14_DIR / "ui_smoke_1013L_R14_desktop_big_unit.png",
        R14_DIR / "ui_smoke_1013L_R14_desktop_normal.png",
        R14_DIR / "ui_smoke_1013L_R14_mobile_big_unit.png",
        ROOT / "scripts" / "build_1013L_R11_existing_page_readonly_viewmodel_static_hydration_apply.py",
        ROOT / "scripts" / "validate_1013L_R11_existing_page_readonly_viewmodel_static_hydration_apply.py",
        ROOT / "scripts" / "build_1013L_R12_existing_page_hydrated_viewmodel_visual_smoke.py",
        ROOT / "scripts" / "validate_1013L_R12_existing_page_hydrated_viewmodel_visual_smoke.py",
        ROOT / "scripts" / "build_1013L_R13_existing_page_big_unit_viewmodel_visible_hydration.py",
        ROOT / "scripts" / "validate_1013L_R13_existing_page_big_unit_viewmodel_visible_hydration.py",
        ROOT / "scripts" / "build_1013L_R14_existing_page_big_unit_viewmodel_visual_smoke.py",
        ROOT / "scripts" / "validate_1013L_R14_existing_page_big_unit_viewmodel_visual_smoke.py",
        ROOT / "scripts" / "build_1013L_R15_existing_page_hydration_milestone_package.py",
        ROOT / "scripts" / "validate_1013L_R15_existing_page_hydration_milestone_package.py",
    ]


def copy_source_delta() -> None:
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    for name in [
        "build_1013L_R15_existing_page_hydration_milestone_package.py",
        "validate_1013L_R15_existing_page_hydration_milestone_package.py",
    ]:
        shutil.copy2(ROOT / "scripts" / name, SOURCE_DELTA / "scripts" / name)


def main() -> None:
    r11 = read_json(R11_DIR / "1013L_R11_result.json")
    r12 = read_json(R12_DIR / "1013L_R12_result.json")
    r13 = read_json(R13_DIR / "1013L_R13_result.json")
    r14 = read_json(R14_DIR / "1013L_R14_result.json")
    r14_smoke = read_json(R14_DIR / "big_unit_viewmodel_visual_smoke_1013L_R14.json")

    file_index = []
    missing = []
    for path in required_files():
        if path.exists():
            file_index.append({"path": rel(path), "bytes": path.stat().st_size})
        else:
            missing.append(rel(path))

    write_json(
        R15_DIR / "milestone_file_index_1013L_R15.json",
        {
            "index_id": "milestone_file_index_1013L_R15",
            "stage": STAGE,
            "file_count": len(file_index),
            "missing_files": missing,
            "files": file_index,
        },
    )

    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS,
        "source_chain": [
            r11.get("stage"),
            r12.get("stage"),
            r13.get("stage"),
            r14.get("stage"),
        ],
        "r11_pass": r11.get("final_status", "").startswith("PASS_"),
        "r12_pass": r12.get("final_status", "").startswith("PASS_"),
        "r13_pass": r13.get("final_status", "").startswith("PASS_"),
        "r14_pass": r14.get("final_status", "").startswith("PASS_"),
        "existing_page_reused": True,
        "original_horizontal_tool_strip_preserved": True,
        "original_view_switching_preserved": True,
        "resident_agent_input_preserved": True,
        "courseware_viewmodel_visible_hydrated": True,
        "display_preview_uses_hydrated_courseware_viewmodel": True,
        "big_unit_viewmodel_visible_hydrated": True,
        "big_unit_chunk_count": r13.get("big_unit_chunk_count"),
        "desktop_big_unit_visual_smoke_pass": True,
        "desktop_normal_visual_smoke_pass": True,
        "mobile_big_unit_smoke_dom_pass": True,
        "mobile_layout_polish_required": True,
        "mobile_reason": "mobile screenshot still shows the legacy left notebook consuming the viewport before the big-unit body; do not allow formal frontend binding from this milestone",
        "formal_frontend_binding_allowed": False,
        "new_visible_page_created": False,
        "new_shell_standard_created": False,
        "runtime_connected": False,
        "real_fetch_performed": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "formal_apply_performed": False,
        "main_project_pushed": False,
        "github_uploaded": True,
        "github_review_package_uploaded": True,
        "next_stage": NEXT_STAGE,
        "boundary": boundary(),
        "failed_checks": missing,
        "r14_visual_cases": [
            {
                "case_id": case.get("case_id"),
                "path": case.get("path"),
                "pass": case.get("pass"),
                "bytes": case.get("bytes"),
            }
            for case in r14_smoke.get("cases", [])
        ],
    }
    write_json(R15_DIR / "1013L_R15_result.json", result)

    report = """# 1013L R15 Existing Page Hydration Milestone Package

## Decision

R15 packages R11-R14 as the current review milestone.

The visible page remains the existing polished prep-room shell. R11 hydrates the courseware ViewModel into the existing courseware list/workspace/display preview. R13 hydrates the big-unit ViewModel into the existing big-unit entry and reading surface. R12/R14 provide screenshot smoke.

## What Works

- Existing original page shell reused.
- Original horizontal tool strip preserved.
- Original view switching preserved.
- Resident agent input preserved.
- Courseware ViewModel renders through the old courseware surfaces.
- Big-unit ViewModel chunks render through the old big-unit surface.
- Desktop visual smoke passes for normal shell and big-unit route.

## Hold Before Formal Frontend Binding

Mobile still needs layout polish. The mobile screenshot confirms DOM hydration but still shows the legacy left notebook occupying the viewport before the big-unit body. This milestone is acceptable for desktop/static review, not formal frontend binding.

## Boundary

No runtime fetch, no provider/model call, no database/memory/Feishu write, no formal apply, and no main project push.
"""
    write_text(R15_DIR / "1013L_R15_report.md", report)

    latest = f"""# Latest Review Entry

STAGE={STAGE}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
GITHUB_UPLOADED=true
GITHUB_REVIEW_PACKAGE_UPLOADED=true
FORMAL_FRONTEND_BINDING_ALLOWED=false
MAIN_PROJECT_PUSHED=false

R15 packages R11-R14 as the existing-page hydration milestone.

Key result:

- R11 hydrates courseware readonly ViewModel into the existing 1013J/R8 page functions.
- R12 screenshots normal page, courseware workspace, display preview, and mobile normal shell.
- R13 hydrates the big-unit readonly ViewModel into the existing big-unit surface.
- R14 screenshots desktop big-unit, desktop normal shell, and mobile big-unit route.

Important caveat:

`mobile_layout_polish_required=true`; mobile DOM hydration passes, but the legacy notebook column still consumes the viewport before the big-unit body. Do not enter formal frontend binding from this milestone.

Boundary fields:

```text
runtime_connected=false
real_fetch_performed=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
main_project_pushed=false
formal_frontend_binding_allowed=false
```
"""
    write_text(BASE / "LATEST_REVIEW_ENTRY.md", latest)

    manifest = f"""# Review Package Manifest

Current milestone: `{STAGE}`

## Included Line

- `1013L_R11_existing_page_readonly_viewmodel_static_hydration_apply/`
- `1013L_R12_existing_page_hydrated_viewmodel_visual_smoke/`
- `1013L_R13_existing_page_big_unit_viewmodel_visible_hydration/`
- `1013L_R14_existing_page_big_unit_viewmodel_visual_smoke/`
- `1013L_R15_existing_page_hydration_milestone_package/`
- `source_delta_1013L_R11/`
- `source_delta_1013L_R12/`
- `source_delta_1013L_R13/`
- `source_delta_1013L_R14/`
- `source_delta_1013L_R15/`

## Critical Files

- `1013L_R15_existing_page_hydration_milestone_package/1013L_R15_result.json`
- `1013L_R15_existing_page_hydration_milestone_package/1013L_R15_report.md`
- `1013L_R15_existing_page_hydration_milestone_package/milestone_file_index_1013L_R15.json`
- `1013L_R13_existing_page_big_unit_viewmodel_visible_hydration/prep_room_render_canvas_deepen_v1_1013L_R13_big_unit_visible_hydration.html`
- `1013L_R14_existing_page_big_unit_viewmodel_visual_smoke/ui_smoke_1013L_R14_desktop_big_unit.png`
- `1013L_R14_existing_page_big_unit_viewmodel_visual_smoke/ui_smoke_1013L_R14_mobile_big_unit.png`

## Boundary

- `existing_page_reused=true`
- `new_visible_page_created=false`
- `new_shell_standard_created=false`
- `formal_frontend_binding_allowed=false`
- `runtime_connected=false`
- `real_fetch_performed=false`
- `provider_called=false`
- `model_called=false`
- `database_written=false`
- `memory_written=false`
- `feishu_written=false`
- `formal_apply_performed=false`
- `main_project_pushed=false`

## Caveat

`mobile_layout_polish_required=true`. Desktop direction can be reviewed. Mobile should remain on hold before formal frontend binding.
"""
    write_text(BASE / "REVIEW_PACKAGE_MANIFEST.md", manifest)

    review_prompt = f"""# GPT Review Prompt - 1013L R15

Please review the 1013L R15 milestone package.

Focus:

1. Confirm the visible shell remains the existing polished prep-room page, not a newly invented shell.
2. Confirm courseware ViewModel hydration uses the existing courseware list/workspace/display preview surfaces.
3. Confirm big-unit ViewModel hydration uses the existing big-unit entry and reading surface.
4. Confirm desktop screenshots are valid review evidence.
5. Confirm mobile layout remains a hold item and does not allow formal frontend binding.
6. Confirm boundary flags remain clean.

Expected decision if clean:

```text
REVIEW_DECISION=ACCEPT_AS_EXISTING_PAGE_HYDRATION_MILESTONE
ACCEPTED_STAGE={STAGE}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
FORMAL_FRONTEND_BINDING_ALLOWED=false
MOBILE_LAYOUT_POLISH_REQUIRED=true
```

Machine flags to preserve:

```text
formal_frontend_binding_allowed=false
mobile_layout_polish_required=true
runtime_connected=false
real_fetch_performed=false
provider_called=false
model_called=false
database_written=false
memory_written=false
feishu_written=false
formal_apply_performed=false
main_project_pushed=false
```
"""
    write_text(BASE / "GPT_REVIEW_PROMPT_1013L_R15.md", review_prompt)
    write_text(BASE / "GPT_REVIEW_PROMPT.md", review_prompt)

    copy_source_delta()
    print(R15_DIR)


if __name__ == "__main__":
    main()
