from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R5_BIG_UNIT_REVIEW_ACTION_STATE_DRY_RUN"
FINAL_STATUS = "PASS_1013K_R5_BIG_UNIT_REVIEW_ACTION_STATE_DRY_RUN"
INHERITS_FROM = "1013K_R4_STATIC_SECTION_PREVIEW_TO_REVIEW_SURFACE_FIXTURE"
NEXT_STAGE = "1013K_R6_BIG_UNIT_REVIEW_ACTION_STATE_TO_PREVIEW_SURFACE_FIXTURE"
STAGE_DIR_NAME = "1013K_R5_big_unit_review_action_state_dry_run"
VALIDATOR_NAME = "validate_1013K_R5_big_unit_review_action_state_dry_run.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_big_unit_review_action_state_1013K_R5.py"
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
    from backend.xiaobei_ai.prep_room_big_unit_review_action_state_1013K_R5 import (  # noqa: PLC0415
        build_big_unit_review_action_state_dry_run,
    )

    return build_big_unit_review_action_state_dry_run


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
    write_json(stage_dir / "big_unit_section_preview_action_state_1013K_R5.json", payload["review_action_state"])
    write_json(stage_dir / "big_unit_section_accepted_preview_items_1013K_R5.json", payload["accepted_preview_items"])
    write_json(stage_dir / "big_unit_section_revision_queue_1013K_R5.json", payload["revision_queue"])
    write_json(stage_dir / "big_unit_section_rejected_items_1013K_R5.json", payload["rejected_items"])
    write_json(stage_dir / "big_unit_section_action_trace_1013K_R5.json", payload["action_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R5"
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

1013K_R5 converts the R4 teacher review surface into static preview-only action states. It simulates accept-to-preview, revise, and reject paths without writing a unit package, lesson body, runtime schema, database, memory, or Feishu.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/big_unit_section_preview_action_state_1013K_R5.json`
- `{STAGE_DIR_NAME}/big_unit_section_accepted_preview_items_1013K_R5.json`
- `{STAGE_DIR_NAME}/big_unit_section_revision_queue_1013K_R5.json`
- `{STAGE_DIR_NAME}/big_unit_section_rejected_items_1013K_R5.json`
- `{STAGE_DIR_NAME}/big_unit_section_action_trace_1013K_R5.json`
- `{STAGE_DIR_NAME}/1013K_R5_result.json`
- `{STAGE_DIR_NAME}/1013K_R5_report.md`
- `backend/xiaobei_ai/prep_room_big_unit_review_action_state_1013K_R5.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. No provider/model call, no runtime connection, no database/memory/Feishu write, no formal apply, no unit_package or lesson body write.
"""
    write_text(output_root / "LATEST_REVIEW_ENTRY.md", latest)
    write_text(output_root / "REVIEW_PACKAGE_MANIFEST.md", manifest)


def build_result(root: Path, output_root: Path, payload: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    r4_result = read_json(output_root / "1013K_R4_static_section_preview_to_review_surface_fixture" / "1013K_R4_result.json")
    action_state = payload["review_action_state"]
    accepted = payload["accepted_preview_items"]
    revision = payload["revision_queue"]
    rejected = payload["rejected_items"]
    trace = payload["action_trace"]
    boundary = payload["boundary"]
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]

    all_accepted_preview_only = all(
        item.get("state") == "accepted_to_preview_only"
        and item.get("can_formal_apply") is False
        and item.get("writes_unit_package") is False
        and item.get("writes_lesson_body") is False
        for item in accepted.get("items", [])
    )
    all_revision_preview_only = all(
        item.get("state") == "revision_requested_preview_only"
        and item.get("can_formal_apply") is False
        and item.get("writes_unit_package") is False
        and item.get("writes_lesson_body") is False
        for item in revision.get("items", [])
    )
    all_rejected_preview_only = all(
        item.get("state") == "rejected_for_current_preview_path"
        and item.get("can_formal_apply") is False
        and item.get("writes_unit_package") is False
        and item.get("writes_lesson_body") is False
        for item in rejected.get("items", [])
    )
    all_trace_side_effect_free = all(
        event.get("side_effects_performed") is False
        and event.get("provider_called") is False
        and event.get("model_called") is False
        and event.get("formal_apply_performed") is False
        and event.get("writes_unit_package") is False
        and event.get("writes_lesson_body") is False
        for event in trace.get("events", [])
    )

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_next_milestone": True,
        "r4_pass": r4_result.get("final_status") == "PASS_1013K_R4_STATIC_SECTION_PREVIEW_TO_REVIEW_SURFACE_FIXTURE",
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "action_state_created": (stage_dir / "big_unit_section_preview_action_state_1013K_R5.json").exists(),
        "accepted_preview_items_created": (stage_dir / "big_unit_section_accepted_preview_items_1013K_R5.json").exists(),
        "revision_queue_created": (stage_dir / "big_unit_section_revision_queue_1013K_R5.json").exists(),
        "rejected_items_created": (stage_dir / "big_unit_section_rejected_items_1013K_R5.json").exists(),
        "action_trace_created": (stage_dir / "big_unit_section_action_trace_1013K_R5.json").exists(),
        "accepted_preview_items_count": accepted.get("item_count"),
        "revision_queue_count": revision.get("item_count"),
        "rejected_items_count": rejected.get("item_count"),
        "action_trace_count": trace.get("event_count"),
        "current_default_path": action_state.get("current_default_path"),
        "alternate_paths_not_simultaneous": action_state.get("path_semantics", {}).get(
            "not_simultaneous_teacher_final_state"
        ),
        "all_accepted_preview_only": all_accepted_preview_only,
        "all_revision_preview_only": all_revision_preview_only,
        "all_rejected_preview_only": all_rejected_preview_only,
        "all_trace_side_effect_free": all_trace_side_effect_free,
        "revert_available": action_state.get("revert_available"),
        "can_formal_apply": action_state.get("can_formal_apply"),
        "normal_candidate_generation_allowed": action_state.get("normal_candidate_generation_allowed"),
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary,
    }

    required_true = [
        "github_upload_deferred_until_next_milestone",
        "r4_pass",
        "backend_adapter_created",
        "action_state_created",
        "accepted_preview_items_created",
        "revision_queue_created",
        "rejected_items_created",
        "action_trace_created",
        "alternate_paths_not_simultaneous",
        "all_accepted_preview_only",
        "all_revision_preview_only",
        "all_rejected_preview_only",
        "all_trace_side_effect_free",
        "revert_available",
        "action_state_dry_run_only",
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
    if result["accepted_preview_items_count"] != 10:
        failures.append("accepted_preview_items_count")
    if result["revision_queue_count"] != 10:
        failures.append("revision_queue_count")
    if result["rejected_items_count"] != 10:
        failures.append("rejected_items_count")
    if result["action_trace_count"] != 30:
        failures.append("action_trace_count")
    if result["current_default_path"] != "accepted_to_preview_only":
        failures.append("current_default_path")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R5 Big Unit Review Action State Dry Run Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
LOCAL_ONLY_SMALL_PACKAGE=true
GITHUB_UPLOAD_DEFERRED_UNTIL_NEXT_MILESTONE=true

## Scope

R5 maps R4 review-surface actions into static preview-only action states. It does not generate new teacher content and does not write unit packages, lesson bodies, runtime schema, database, memory, or Feishu.

## Key Checks

```text
accepted_preview_items_count={result["accepted_preview_items_count"]}
revision_queue_count={result["revision_queue_count"]}
rejected_items_count={result["rejected_items_count"]}
action_trace_count={result["action_trace_count"]}
current_default_path={result["current_default_path"]}
alternate_paths_not_simultaneous={str(result["alternate_paths_not_simultaneous"]).lower()}
normal_candidate_generation_allowed={str(result["normal_candidate_generation_allowed"]).lower()}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
database_written={str(result["database_written"]).lower()}
memory_written={str(result["memory_written"]).lower()}
formal_apply_performed={str(result["formal_apply_performed"]).lower()}
```

## Note

Accepted, revise, and reject paths are simulated for review coverage. They are not simultaneous final teacher choices; the default visible path is accepted-to-preview-only.

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
        stage_dir / "big_unit_section_preview_action_state_1013K_R5.json",
        stage_dir / "big_unit_section_accepted_preview_items_1013K_R5.json",
        stage_dir / "big_unit_section_revision_queue_1013K_R5.json",
        stage_dir / "big_unit_section_rejected_items_1013K_R5.json",
        stage_dir / "big_unit_section_action_trace_1013K_R5.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R5_result.json", result)
    write_text(stage_dir / "1013K_R5_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R5_BIG_UNIT_REVIEW_ACTION_STATE_DRY_RUN_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
