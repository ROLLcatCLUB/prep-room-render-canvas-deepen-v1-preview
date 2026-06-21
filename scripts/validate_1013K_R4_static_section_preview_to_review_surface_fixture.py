from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R4_STATIC_SECTION_PREVIEW_TO_REVIEW_SURFACE_FIXTURE"
FINAL_STATUS = "PASS_1013K_R4_STATIC_SECTION_PREVIEW_TO_REVIEW_SURFACE_FIXTURE"
INHERITS_FROM = "1013K_R3_BIG_UNIT_CANDIDATE_ENVELOPE_TO_STATIC_SECTION_PREVIEW"
NEXT_STAGE = "1013K_M1_CURRICULUM_TO_BIG_UNIT_REVIEW_MILESTONE_PACKAGE"
STAGE_DIR_NAME = "1013K_R4_static_section_preview_to_review_surface_fixture"
VALIDATOR_NAME = "validate_1013K_R4_static_section_preview_to_review_surface_fixture.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_big_unit_review_surface_1013K_R4.py"
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
    from backend.xiaobei_ai.prep_room_big_unit_review_surface_1013K_R4 import (  # noqa: PLC0415
        build_static_section_preview_to_review_surface_fixture,
    )

    return build_static_section_preview_to_review_surface_fixture


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
    write_json(stage_dir / "big_unit_review_surface_fixture_1013K_R4.json", payload["review_surface_fixture"])
    write_json(stage_dir / "big_unit_review_state_1013K_R4.json", payload["review_state"])
    write_json(stage_dir / "big_unit_teacher_review_checklist_1013K_R4.json", payload["teacher_review_checklist"])
    write_json(stage_dir / "big_unit_review_surface_trace_1013K_R4.json", payload["review_surface_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R4"
    backend_src = root / BACKEND_ADAPTER_RELATIVE_PATH
    backend_dst = delta_root / BACKEND_ADAPTER_RELATIVE_PATH
    script_src = root / "scripts" / VALIDATOR_NAME
    script_dst = delta_root / "scripts" / VALIDATOR_NAME
    backend_dst.parent.mkdir(parents=True, exist_ok=True)
    script_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backend_src, backend_dst)
    shutil.copy2(script_src, script_dst)
    return [backend_dst, script_dst]


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    r3_result = read_json(
        output_root / "1013K_R3_big_unit_candidate_envelope_to_static_section_preview" / "1013K_R3_result.json"
    )
    surface = payload["review_surface_fixture"]
    state = payload["review_state"]
    checklist = payload["teacher_review_checklist"]
    trace = payload["review_surface_trace"]
    boundary = payload["boundary"]
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]

    sections = surface.get("sections", [])
    section_states = state.get("section_states", [])
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_milestone": True,
        "milestone_upload_recommended": True,
        "r3_pass": r3_result.get("final_status") == "PASS_1013K_R3_BIG_UNIT_CANDIDATE_ENVELOPE_TO_STATIC_SECTION_PREVIEW",
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "review_surface_fixture_created": (stage_dir / "big_unit_review_surface_fixture_1013K_R4.json").exists(),
        "review_state_created": (stage_dir / "big_unit_review_state_1013K_R4.json").exists(),
        "teacher_review_checklist_created": (stage_dir / "big_unit_teacher_review_checklist_1013K_R4.json").exists(),
        "review_surface_trace_created": (stage_dir / "big_unit_review_surface_trace_1013K_R4.json").exists(),
        "section_count": surface.get("section_count"),
        "review_state_section_count": len(section_states),
        "teacher_checklist_item_count": len(checklist.get("items", [])),
        "all_sections_have_main_reading_content": all(
            bool(section.get("main_reading_content", {}).get("paragraphs")) for section in sections
        ),
        "all_sections_have_collapsed_side_note": all(
            section.get("side_note", {}).get("default_collapsed") is True for section in sections
        ),
        "all_sections_have_three_teacher_actions": all(
            len(section.get("teacher_actions", [])) == 3 for section in sections
        ),
        "all_sections_pending_teacher_review": state.get("all_sections_pending_teacher_review"),
        "any_formal_apply_allowed": state.get("any_formal_apply_allowed"),
        "all_state_can_formal_apply_false": all(
            item.get("can_formal_apply") is False for item in section_states
        ),
        "teacher_confirmation_required": checklist.get("teacher_confirmation_required"),
        "blocking_gate_summary_present": bool(surface.get("blocking_gate_summary")),
        "normal_candidate_generation_allowed": surface.get("blocking_gate_summary", {}).get(
            "normal_candidate_generation_allowed"
        ),
        "trace_event_count": len(trace.get("events", [])),
        "trace_side_effects_performed": trace.get("side_effects_performed"),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary,
    }
    required_true = [
        "github_upload_deferred_until_milestone",
        "milestone_upload_recommended",
        "r3_pass",
        "backend_adapter_created",
        "review_surface_fixture_created",
        "review_state_created",
        "teacher_review_checklist_created",
        "review_surface_trace_created",
        "all_sections_have_main_reading_content",
        "all_sections_have_collapsed_side_note",
        "all_sections_have_three_teacher_actions",
        "all_sections_pending_teacher_review",
        "all_state_can_formal_apply_false",
        "teacher_confirmation_required",
        "blocking_gate_summary_present",
        "review_surface_fixture_only",
        "preview_only",
        "teacher_review_required",
    ]
    required_false = [
        "any_formal_apply_allowed",
        "normal_candidate_generation_allowed",
        "trace_side_effects_performed",
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
    if result["review_state_section_count"] != 10:
        failures.append("review_state_section_count")
    if result["teacher_checklist_item_count"] < 5:
        failures.append("teacher_checklist_item_count")
    if result["trace_event_count"] < 4:
        failures.append("trace_event_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R4 Static Section Preview To Review Surface Fixture Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
GITHUB_UPLOAD_DEFERRED_UNTIL_MILESTONE=true
MILESTONE_UPLOAD_RECOMMENDED=true

## Scope

R4 turns R3 static big-unit sections into a teacher review surface fixture, review state, checklist, and trace. It remains preview-only and does not write a formal unit package or lesson body.

## Key Checks

```text
section_count={result["section_count"]}
review_state_section_count={result["review_state_section_count"]}
teacher_checklist_item_count={result["teacher_checklist_item_count"]}
all_sections_have_main_reading_content={str(result["all_sections_have_main_reading_content"]).lower()}
all_sections_have_three_teacher_actions={str(result["all_sections_have_three_teacher_actions"]).lower()}
all_sections_pending_teacher_review={str(result["all_sections_pending_teacher_review"]).lower()}
any_formal_apply_allowed={str(result["any_formal_apply_allowed"]).lower()}
normal_candidate_generation_allowed={str(result["normal_candidate_generation_allowed"]).lower()}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
database_written={str(result["database_written"]).lower()}
memory_written={str(result["memory_written"]).lower()}
```

## Milestone Note

R4 completes a local backend milestone from curriculum control to teacher review surface fixture. The next step is a milestone package upload rather than another tiny GitHub commit.

## Validator

validator_pass={str(result["validator_pass"]).lower()}
failed_checks={json.dumps(result["failed_checks"], ensure_ascii=False)}
"""


def update_local_review_root(output_root: Path) -> None:
    latest = f"""# Latest Review Entry

STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
NEXT_STAGE={NEXT_STAGE}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_MILESTONE=true
MILESTONE_UPLOAD_RECOMMENDED=true
PROVIDER_MODEL_CALL_ALLOWED=false
FORMAL_APPLY_ALLOWED=false
DATABASE_WRITE_ALLOWED=false
MEMORY_WRITE_ALLOWED=false

1013K_R4 converts R3 static sections into a teacher review surface fixture with preview-only actions. This completes a local backend milestone from curriculum control to teacher review surface; upload should happen as a milestone bundle, not as another tiny package.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/big_unit_review_surface_fixture_1013K_R4.json`
- `{STAGE_DIR_NAME}/big_unit_review_state_1013K_R4.json`
- `{STAGE_DIR_NAME}/big_unit_teacher_review_checklist_1013K_R4.json`
- `{STAGE_DIR_NAME}/big_unit_review_surface_trace_1013K_R4.json`
- `{STAGE_DIR_NAME}/1013K_R4_result.json`
- `{STAGE_DIR_NAME}/1013K_R4_report.md`
- `backend/xiaobei_ai/prep_room_big_unit_review_surface_1013K_R4.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. No provider/model call, no runtime connection, no database/memory/Feishu write, no formal apply, no unit_package or lesson body write.

Milestone upload recommended: `{NEXT_STAGE}`
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


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
        stage_dir / "big_unit_review_surface_fixture_1013K_R4.json",
        stage_dir / "big_unit_review_state_1013K_R4.json",
        stage_dir / "big_unit_teacher_review_checklist_1013K_R4.json",
        stage_dir / "big_unit_review_surface_trace_1013K_R4.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R4_result.json", result)
    write_text(stage_dir / "1013K_R4_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R4_STATIC_SECTION_PREVIEW_TO_REVIEW_SURFACE_FIXTURE_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
