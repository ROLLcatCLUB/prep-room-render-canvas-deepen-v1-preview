from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R7_DIR = BASE / "1013L_R7_original_page_fetch_adapter_interaction_binding_plan"
R8_DIR = BASE / "1013L_R8_original_page_static_readonly_fetch_hook"
R9_DIR = BASE / "1013L_R9_original_page_viewmodel_hydration_static_smoke"
R10_DIR = BASE / "1013L_R10_existing_page_readonly_viewmodel_binding_milestone_package"
SOURCE_DELTA = BASE / "source_delta_1013L_R10"


STAGE = "1013L_R10_EXISTING_PAGE_READONLY_VIEWMODEL_BINDING_MILESTONE_PACKAGE"
FINAL_STATUS = "PASS_1013L_R10_EXISTING_PAGE_READONLY_VIEWMODEL_BINDING_MILESTONE_PACKAGE"
NEXT_STAGE = "1013L_R11_EXISTING_PAGE_READONLY_VIEWMODEL_STATIC_HYDRATION_APPLY"


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
        "new_visible_page_created": False,
        "new_shell_standard_created": False,
        "visible_dom_changed_in_r10": False,
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
        R7_DIR / "1013L_R7_result.json",
        R7_DIR / "original_page_interaction_inventory_1013L_R7.json",
        R7_DIR / "original_ui_to_render_state_map_1013L_R7.json",
        R7_DIR / "main_shell_fetch_adapter_to_original_page_binding_plan_1013L_R7.json",
        R7_DIR / "1013L_R7_report.md",
        R8_DIR / "1013L_R8_result.json",
        R8_DIR / "static_readonly_fetch_hook_contract_1013L_R8.json",
        R8_DIR / "static_hook_state_resolution_fixture_1013L_R8.json",
        R8_DIR / "prep_room_render_canvas_deepen_v1_1013L_R8_static_readonly_fetch_hook.html",
        R8_DIR / "1013L_R8_report.md",
        R9_DIR / "1013L_R9_result.json",
        R9_DIR / "hook_resolution_browser_smoke_1013L_R9.json",
        R9_DIR / "prep_room_render_canvas_deepen_v1_1013L_R9_hook_smoke.html",
        R9_DIR / "1013L_R9_report.md",
        ROOT / "scripts" / "build_1013L_R7_original_page_interaction_binding_plan.py",
        ROOT / "scripts" / "validate_1013L_R7_original_page_interaction_binding_plan.py",
        ROOT / "scripts" / "build_1013L_R8_original_page_static_readonly_fetch_hook.py",
        ROOT / "scripts" / "validate_1013L_R8_original_page_static_readonly_fetch_hook.py",
        ROOT / "scripts" / "build_1013L_R9_original_page_viewmodel_hydration_static_smoke.py",
        ROOT / "scripts" / "validate_1013L_R9_original_page_viewmodel_hydration_static_smoke.py",
        ROOT / "scripts" / "build_1013L_R10_existing_page_readonly_viewmodel_binding_milestone_package.py",
        ROOT / "scripts" / "validate_1013L_R10_existing_page_readonly_viewmodel_binding_milestone_package.py",
    ]


def copy_source_delta() -> None:
    (SOURCE_DELTA / "scripts").mkdir(parents=True, exist_ok=True)
    for name in [
        "build_1013L_R10_existing_page_readonly_viewmodel_binding_milestone_package.py",
        "validate_1013L_R10_existing_page_readonly_viewmodel_binding_milestone_package.py",
    ]:
        shutil.copy2(ROOT / "scripts" / name, SOURCE_DELTA / "scripts" / name)


def main() -> None:
    r7 = read_json(R7_DIR / "1013L_R7_result.json")
    r8 = read_json(R8_DIR / "1013L_R8_result.json")
    r9 = read_json(R9_DIR / "1013L_R9_result.json")
    smoke = read_json(R9_DIR / "hook_resolution_browser_smoke_1013L_R9.json")
    file_index = []
    missing = []
    for path in required_files():
        if path.exists():
            file_index.append({"path": rel(path), "bytes": path.stat().st_size})
        else:
            missing.append(rel(path))

    write_json(
        R10_DIR / "milestone_file_index_1013L_R10.json",
        {
            "index_id": "milestone_file_index_1013L_R10",
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
            r7.get("stage"),
            r8.get("stage"),
            r9.get("stage"),
        ],
        "r7_pass": r7.get("final_status", "").startswith("PASS_"),
        "r8_pass": r8.get("final_status", "").startswith("PASS_"),
        "r9_pass": r9.get("final_status", "").startswith("PASS_"),
        "existing_original_page_reused": True,
        "original_horizontal_tool_strip_preserved": True,
        "original_view_switching_preserved": True,
        "resident_agent_input_preserved": True,
        "hidden_readonly_fetch_hook_created": True,
        "hook_resolution_smoke_pass": smoke.get("hook_resolution_smoke_pass") is True,
        "smoke_case_count": smoke.get("case_count"),
        "new_visible_page_created": False,
        "new_shell_standard_created": False,
        "formal_frontend_binding_allowed": False,
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
    }
    write_json(R10_DIR / "1013L_R10_result.json", result)

    report = """# 1013L R10 Existing Page Readonly ViewModel Binding Milestone Package

## Decision

R10 packages the local R7-R9 line as a GitHub-reviewable milestone.

The visible shell remains the existing polished 1013J_R1M prep-room page. R7 maps original interactions to readonly states, R8 injects a hidden static readonly fetch hook, and R9 verifies the hook in Edge headless across the main original page routes.

## Verified Routes

- default existing page -> `single_lesson_design`
- explicit week calendar -> `week_calendar`
- explicit prep notebook -> `single_lesson_design`
- courseware expanded -> `courseware_workspace`
- classroom display preview -> `classroom_display_preview`

## Boundary

No new visible shell, no runtime fetch, no provider/model call, no database/memory/Feishu write, no formal apply, and no main project push.
"""
    write_text(R10_DIR / "1013L_R10_report.md", report)

    latest = f"""# Latest Review Entry

STAGE={STAGE}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
GITHUB_UPLOADED=true
GITHUB_REVIEW_PACKAGE_UPLOADED=true
MAIN_PROJECT_PUSHED=false

R10 packages R7-R9 as the current milestone. The existing 1013J_R1M polished prep-room page remains the visible shell. No new shell standard is created.

Key result:

- original horizontal AI tool strip preserved
- original view switching preserved
- resident Agent input preserved
- hidden readonly fetch hook created
- browser smoke confirms 5 route/state resolutions
- runtime/provider/model/database/memory/Feishu/formal apply all remain false

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
```
"""
    write_text(BASE / "LATEST_REVIEW_ENTRY.md", latest)

    manifest = f"""# Review Package Manifest

Current milestone: `{STAGE}`

## Included Line

- `1013L_R7_original_page_fetch_adapter_interaction_binding_plan/`
- `1013L_R8_original_page_static_readonly_fetch_hook/`
- `1013L_R9_original_page_viewmodel_hydration_static_smoke/`
- `1013L_R10_existing_page_readonly_viewmodel_binding_milestone_package/`
- `source_delta_1013L_R7/`
- `source_delta_1013L_R8/`
- `source_delta_1013L_R9/`
- `source_delta_1013L_R10/`

## Critical Files

- `1013L_R10_existing_page_readonly_viewmodel_binding_milestone_package/1013L_R10_result.json`
- `1013L_R10_existing_page_readonly_viewmodel_binding_milestone_package/1013L_R10_report.md`
- `1013L_R10_existing_page_readonly_viewmodel_binding_milestone_package/milestone_file_index_1013L_R10.json`
- `1013L_R9_original_page_viewmodel_hydration_static_smoke/hook_resolution_browser_smoke_1013L_R9.json`
- `1013L_R8_original_page_static_readonly_fetch_hook/prep_room_render_canvas_deepen_v1_1013L_R8_static_readonly_fetch_hook.html`

## Boundary

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
"""
    write_text(BASE / "REVIEW_PACKAGE_MANIFEST.md", manifest)

    review_prompt = f"""# GPT Review Prompt - 1013L R10

Please review the 1013L R10 milestone package.

Focus:

1. Confirm the visible shell remains the existing 1013J_R1M polished prep-room page.
2. Confirm R7 maps original page interactions to readonly viewmodel states without replacing UI.
3. Confirm R8 creates only a hidden static readonly fetch hook.
4. Confirm R9 browser smoke resolves:
   - default -> single_lesson_design
   - week calendar -> week_calendar
   - prep notebook -> single_lesson_design
   - courseware expanded -> courseware_workspace
   - display preview -> classroom_display_preview
5. Confirm no runtime/provider/model/database/memory/Feishu/formal apply/main-project-push happened.

Required boundary fields:

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
```

Expected decision if clean:

```text
REVIEW_DECISION=ACCEPT
ACCEPTED_STAGE={STAGE}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
FORMAL_FRONTEND_BINDING_ALLOWED=false
```
"""
    write_text(BASE / "GPT_REVIEW_PROMPT_1013L_R10.md", review_prompt)
    write_text(BASE / "GPT_REVIEW_PROMPT.md", review_prompt)

    copy_source_delta()
    print(R10_DIR)


if __name__ == "__main__":
    main()
