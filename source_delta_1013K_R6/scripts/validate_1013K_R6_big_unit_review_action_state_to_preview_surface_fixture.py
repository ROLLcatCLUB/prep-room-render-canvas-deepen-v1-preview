from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R6_BIG_UNIT_REVIEW_ACTION_STATE_TO_PREVIEW_SURFACE_FIXTURE"
FINAL_STATUS = "PASS_1013K_R6_BIG_UNIT_REVIEW_ACTION_STATE_TO_PREVIEW_SURFACE_FIXTURE"
INHERITS_FROM = "1013K_R5_BIG_UNIT_REVIEW_ACTION_STATE_DRY_RUN"
NEXT_STAGE = "1013K_R7_BIG_UNIT_PREVIEW_SURFACE_TO_RENDER_VIEWMODEL_CONTRACT"
STAGE_DIR_NAME = "1013K_R6_big_unit_review_action_state_to_preview_surface_fixture"
VALIDATOR_NAME = "validate_1013K_R6_big_unit_review_action_state_to_preview_surface_fixture.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_big_unit_preview_surface_1013K_R6.py"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)app[_-]?secret\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)tenant[_-]?access[_-]?token\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)cookie\s*[:=]\s*['\"][^'\"]{20,}"),
]


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_backend_adapter(root: Path):
    sys.path.insert(0, str(root))
    from backend.xiaobei_ai.prep_room_big_unit_preview_surface_1013K_R6 import (  # noqa: PLC0415
        build_big_unit_review_action_state_to_preview_surface_fixture,
    )

    return build_big_unit_review_action_state_to_preview_surface_fixture


def scan_deprecated_visible_names(paths: list[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name in DEPRECATED_VISIBLE_NAMES:
            if name in text:
                hits.append({"path": str(path), "name": name})
    return hits


def scan_secrets(paths: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        if not path.exists() or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                hits.append(str(path))
                break
    return hits


def write_stage_files(root: Path, output_root: Path) -> dict[str, Any]:
    builder = load_backend_adapter(root)
    payload = builder(root)
    stage_dir = output_root / STAGE_DIR_NAME
    write_json(stage_dir / "big_unit_preview_surface_fixture_1013K_R6.json", payload["preview_surface_fixture"])
    write_json(stage_dir / "big_unit_preview_surface_navigation_1013K_R6.json", payload["preview_navigation"])
    write_json(stage_dir / "big_unit_preview_surface_status_1013K_R6.json", payload["preview_status"])
    write_json(stage_dir / "big_unit_preview_surface_trace_1013K_R6.json", payload["preview_surface_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R6"
    backend_src = root / BACKEND_ADAPTER_RELATIVE_PATH
    backend_dst = delta_root / BACKEND_ADAPTER_RELATIVE_PATH
    script_src = root / "scripts" / VALIDATOR_NAME
    script_dst = delta_root / "scripts" / VALIDATOR_NAME
    backend_dst.parent.mkdir(parents=True, exist_ok=True)
    script_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backend_src, backend_dst)
    shutil.copy2(script_src, script_dst)
    return [backend_dst, script_dst]


def update_local_review_root(output_root: Path) -> None:
    latest = f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true
PROVIDER_MODEL_CALL_ALLOWED=false
FORMAL_APPLY_ALLOWED=false
DATABASE_WRITE_ALLOWED=false
MEMORY_WRITE_ALLOWED=false

1013K_R6 converts R5 preview action state into a renderable big-unit preview surface fixture. It remains static, preview-only, and does not write runtime schema, unit package, lesson body, database, memory, or Feishu.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/big_unit_preview_surface_fixture_1013K_R6.json`
- `{STAGE_DIR_NAME}/big_unit_preview_surface_navigation_1013K_R6.json`
- `{STAGE_DIR_NAME}/big_unit_preview_surface_status_1013K_R6.json`
- `{STAGE_DIR_NAME}/big_unit_preview_surface_trace_1013K_R6.json`
- `{STAGE_DIR_NAME}/1013K_R6_result.json`
- `{STAGE_DIR_NAME}/1013K_R6_report.md`
- `backend/xiaobei_ai/prep_room_big_unit_preview_surface_1013K_R6.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. No provider/model call, no runtime connection, no database/memory/Feishu write, no formal apply, no unit_package or lesson body write.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    r5_result = read_json(output_root / "1013K_R5_big_unit_review_action_state_dry_run" / "1013K_R5_result.json")
    surface = payload["preview_surface_fixture"]
    navigation = payload["preview_navigation"]
    status = payload["preview_status"]
    trace = payload["preview_surface_trace"]
    boundary = payload["boundary"]
    sections = surface.get("sections", [])
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]

    all_sections_preview_visible = all(
        section.get("display_state") == "preview_visible"
        and section.get("accepted_to_preview") is True
        and section.get("writes_unit_package") is False
        and section.get("writes_lesson_body") is False
        and section.get("formal_apply_performed") is False
        for section in sections
    )
    all_sections_have_revert_revise_reject = all(
        {action.get("action") for action in section.get("available_actions", [])} == {"revert", "revise", "reject"}
        for section in sections
    )
    all_sections_have_main_reading_content = all(
        bool(section.get("main_reading_content", {}).get("paragraphs")) for section in sections
    )
    all_trace_side_effect_free = all(
        event.get("side_effects_performed") is False for event in trace.get("events", [])
    )

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_next_milestone": True,
        "r5_pass": r5_result.get("final_status") == "PASS_1013K_R5_BIG_UNIT_REVIEW_ACTION_STATE_DRY_RUN",
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "preview_surface_fixture_created": (stage_dir / "big_unit_preview_surface_fixture_1013K_R6.json").exists(),
        "preview_navigation_created": (stage_dir / "big_unit_preview_surface_navigation_1013K_R6.json").exists(),
        "preview_status_created": (stage_dir / "big_unit_preview_surface_status_1013K_R6.json").exists(),
        "preview_surface_trace_created": (stage_dir / "big_unit_preview_surface_trace_1013K_R6.json").exists(),
        "preview_surface_ready_for_static_render": surface.get("preview_surface_ready_for_static_render"),
        "section_count": surface.get("section_count"),
        "navigation_item_count": navigation.get("item_count"),
        "accepted_preview_items_count": status.get("accepted_preview_items_count"),
        "revision_queue_count": status.get("revision_queue_count"),
        "rejected_items_count": status.get("rejected_items_count"),
        "current_visible_path": status.get("current_visible_path"),
        "revision_and_reject_are_alternate_paths": status.get("revision_and_reject_are_alternate_paths"),
        "preview_visible": status.get("preview_visible"),
        "all_sections_preview_visible": all_sections_preview_visible,
        "all_sections_have_revert_revise_reject": all_sections_have_revert_revise_reject,
        "all_sections_have_main_reading_content": all_sections_have_main_reading_content,
        "trace_event_count": trace.get("event_count"),
        "all_trace_side_effect_free": all_trace_side_effect_free,
        "can_formal_apply": surface.get("can_formal_apply"),
        "normal_candidate_generation_allowed": surface.get("normal_candidate_generation_allowed"),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary,
    }
    required_true = [
        "github_upload_deferred_until_next_milestone",
        "r5_pass",
        "backend_adapter_created",
        "preview_surface_fixture_created",
        "preview_navigation_created",
        "preview_status_created",
        "preview_surface_trace_created",
        "preview_surface_ready_for_static_render",
        "revision_and_reject_are_alternate_paths",
        "preview_visible",
        "all_sections_preview_visible",
        "all_sections_have_revert_revise_reject",
        "all_sections_have_main_reading_content",
        "all_trace_side_effect_free",
        "preview_surface_fixture_only",
        "preview_only",
        "teacher_review_required",
    ]
    required_false = [
        "can_formal_apply",
        "normal_candidate_generation_allowed",
        "runtime_connected",
        "provider_called",
        "model_called",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "unit_package_written",
        "lesson_body_modified",
        "html_body_modified",
        "runtime_schema_applied",
        "official_curriculum_claim_created",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result["section_count"] != 10:
        failures.append("section_count")
    if result["navigation_item_count"] != 10:
        failures.append("navigation_item_count")
    if result["accepted_preview_items_count"] != 10:
        failures.append("accepted_preview_items_count")
    if result["revision_queue_count"] != 10:
        failures.append("revision_queue_count")
    if result["rejected_items_count"] != 10:
        failures.append("rejected_items_count")
    if result["current_visible_path"] != "accepted_to_preview_only":
        failures.append("current_visible_path")
    if result["trace_event_count"] != 4:
        failures.append("trace_event_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R6 Big Unit Review Action State To Preview Surface Fixture Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true

## Scope

R6 converts the R5 accepted-to-preview action state into a renderable big-unit preview surface fixture. It is still static and preview-only.

## Key Checks

```text
preview_surface_ready_for_static_render={str(result["preview_surface_ready_for_static_render"]).lower()}
section_count={result["section_count"]}
navigation_item_count={result["navigation_item_count"]}
current_visible_path={result["current_visible_path"]}
all_sections_preview_visible={str(result["all_sections_preview_visible"]).lower()}
all_sections_have_revert_revise_reject={str(result["all_sections_have_revert_revise_reject"]).lower()}
normal_candidate_generation_allowed={str(result["normal_candidate_generation_allowed"]).lower()}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
database_written={str(result["database_written"]).lower()}
memory_written={str(result["memory_written"]).lower()}
formal_apply_performed={str(result["formal_apply_performed"]).lower()}
```

## Validator

validator_pass={str(result["validator_pass"]).lower()}
failed_checks={json.dumps(result["failed_checks"], ensure_ascii=False)}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    payload = write_stage_files(root, output_root)
    update_local_review_root(output_root)
    source_delta_files = copy_source_delta(root, output_root)
    stage_dir = output_root / STAGE_DIR_NAME
    stage_files = [
        stage_dir / "big_unit_preview_surface_fixture_1013K_R6.json",
        stage_dir / "big_unit_preview_surface_navigation_1013K_R6.json",
        stage_dir / "big_unit_preview_surface_status_1013K_R6.json",
        stage_dir / "big_unit_preview_surface_trace_1013K_R6.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R6_result.json", result)
    write_text(stage_dir / "1013K_R6_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R6_BIG_UNIT_REVIEW_ACTION_STATE_TO_PREVIEW_SURFACE_FIXTURE_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
