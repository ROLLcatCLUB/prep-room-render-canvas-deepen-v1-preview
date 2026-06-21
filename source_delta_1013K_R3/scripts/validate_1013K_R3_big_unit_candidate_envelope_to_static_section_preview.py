from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013K_R3_BIG_UNIT_CANDIDATE_ENVELOPE_TO_STATIC_SECTION_PREVIEW"
FINAL_STATUS = "PASS_1013K_R3_BIG_UNIT_CANDIDATE_ENVELOPE_TO_STATIC_SECTION_PREVIEW"
INHERITS_FROM = "1013K_R2_CURRICULUM_PROFILE_TO_BIG_UNIT_CANDIDATE_ENVELOPE"
NEXT_STAGE = "1013K_R4_STATIC_SECTION_PREVIEW_TO_REVIEW_SURFACE_FIXTURE"
STAGE_DIR_NAME = "1013K_R3_big_unit_candidate_envelope_to_static_section_preview"
VALIDATOR_NAME = "validate_1013K_R3_big_unit_candidate_envelope_to_static_section_preview.py"
BACKEND_ADAPTER_RELATIVE_PATH = "backend/xiaobei_ai/prep_room_big_unit_static_section_preview_1013K_R3.py"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
TEACHER_TEXT_BANNED_TERMS = [
    "schema",
    "provider",
    "model",
    "database",
    "memory",
    "feishu",
    "unit_package",
    "lesson_body",
    "formal_apply",
    "runtime",
]
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
    from backend.xiaobei_ai.prep_room_big_unit_static_section_preview_1013K_R3 import (  # noqa: PLC0415
        build_big_unit_candidate_envelope_to_static_section_preview,
    )

    return build_big_unit_candidate_envelope_to_static_section_preview


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


def teacher_text_has_banned_terms(preview_bundle: dict[str, Any]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for section in preview_bundle.get("sections", []):
        text = "\n".join(section.get("body_paragraphs", [])) + "\n" + section.get("summary", "")
        lower = text.lower()
        for term in TEACHER_TEXT_BANNED_TERMS:
            if term in lower:
                hits.append({"section_preview_id": section["section_preview_id"], "term": term})
    return hits


def write_stage_files(root: Path, output_root: Path) -> dict[str, Any]:
    builder = load_backend_adapter(root)
    payload = builder(root)
    stage_dir = output_root / STAGE_DIR_NAME
    write_json(
        stage_dir / "big_unit_static_section_preview_bundle_1013K_R3.json",
        payload["static_section_preview_bundle"],
    )
    write_json(stage_dir / "big_unit_static_preview_review_actions_1013K_R3.json", payload["preview_review_actions"])
    write_json(stage_dir / "big_unit_static_preview_trace_1013K_R3.json", payload["static_preview_trace"])
    return payload


def copy_source_delta(root: Path, output_root: Path) -> list[Path]:
    delta_root = output_root / "source_delta_1013K_R3"
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
    r2_result = read_json(
        output_root / "1013K_R2_curriculum_profile_to_big_unit_candidate_envelope" / "1013K_R2_result.json"
    )
    preview_bundle = payload["static_section_preview_bundle"]
    actions = payload["preview_review_actions"]
    trace = payload["static_preview_trace"]
    boundary = payload["boundary"]
    teacher_visible_scan_files = [path for path in stage_files if "source_delta" not in path.as_posix()]
    sections = preview_bundle.get("sections", [])
    action_groups = actions.get("actions", [])
    teacher_text_hits = teacher_text_has_banned_terms(preview_bundle)

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "github_upload_deferred_until_milestone": True,
        "r2_pass": r2_result.get("final_status") == "PASS_1013K_R2_CURRICULUM_PROFILE_TO_BIG_UNIT_CANDIDATE_ENVELOPE",
        "backend_adapter_created": (root / BACKEND_ADAPTER_RELATIVE_PATH).exists(),
        "static_section_preview_bundle_created": (
            stage_dir / "big_unit_static_section_preview_bundle_1013K_R3.json"
        ).exists(),
        "preview_review_actions_created": (
            stage_dir / "big_unit_static_preview_review_actions_1013K_R3.json"
        ).exists(),
        "static_preview_trace_created": (stage_dir / "big_unit_static_preview_trace_1013K_R3.json").exists(),
        "section_count": preview_bundle.get("section_count"),
        "all_sections_static_preview_text_created": all(
            section.get("static_preview_fixture_text_created") is True for section in sections
        ),
        "all_sections_teacher_review_required": all(section.get("teacher_review_required") is True for section in sections),
        "all_sections_degraded_preview_label_required": all(
            section.get("degraded_preview_label_required") is True for section in sections
        ),
        "all_sections_model_text_not_generated": all(
            section.get("model_candidate_text_generated") is False for section in sections
        ),
        "all_sections_write_nothing": all(
            section.get("writes_unit_package") is False and section.get("writes_lesson_body") is False
            for section in sections
        ),
        "main_reading_surface_ready": preview_bundle.get("main_reading_surface_ready"),
        "action_group_count": actions.get("section_action_count"),
        "preview_only_actions": actions.get("preview_only_actions"),
        "all_action_groups_have_three_actions": all(len(group.get("actions", [])) == 3 for group in action_groups),
        "trace_event_count": len(trace.get("events", [])),
        "trace_side_effects_performed": trace.get("side_effects_performed"),
        "trace_model_candidate_text_generated": trace.get("model_candidate_text_generated"),
        "teacher_text_banned_term_hits": teacher_text_hits,
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(teacher_visible_scan_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **boundary,
    }
    required_true = [
        "github_upload_deferred_until_milestone",
        "r2_pass",
        "backend_adapter_created",
        "static_section_preview_bundle_created",
        "preview_review_actions_created",
        "static_preview_trace_created",
        "all_sections_static_preview_text_created",
        "all_sections_teacher_review_required",
        "all_sections_degraded_preview_label_required",
        "all_sections_model_text_not_generated",
        "all_sections_write_nothing",
        "main_reading_surface_ready",
        "preview_only_actions",
        "all_action_groups_have_three_actions",
        "static_preview_fixture_only",
        "degraded_preview_only",
        "teacher_review_required",
    ]
    required_false = [
        "trace_side_effects_performed",
        "trace_model_candidate_text_generated",
        "runtime_connected",
        "provider_called",
        "model_called",
        "model_candidate_text_generated",
        "unit_package_written",
        "lesson_body_modified",
        "html_body_modified",
        "database_written",
        "memory_written",
        "feishu_written",
        "formal_apply_performed",
        "runtime_schema_applied",
        "official_curriculum_claim_created",
        "full_standard_text_dumped_to_prompt",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result["section_count"] != 10:
        failures.append("section_count")
    if result["action_group_count"] != 10:
        failures.append("action_group_count")
    if result["trace_event_count"] < 3:
        failures.append("trace_event_count")
    if result["teacher_text_banned_term_hits"]:
        failures.append("teacher_text_banned_term_hits")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    result["validator_pass"] = not failures
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013K_R3 Big Unit Candidate Envelope To Static Section Preview Report

STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={result["next_stage"]}
GITHUB_UPLOAD_DEFERRED_UNTIL_MILESTONE=true

## Scope

R3 turns R2 big-unit candidate envelopes into teacher-readable static section preview fixtures. This is deterministic fixture text for review, not model output and not a formal unit package.

## Key Checks

```text
section_count={result["section_count"]}
main_reading_surface_ready={str(result["main_reading_surface_ready"]).lower()}
all_sections_teacher_review_required={str(result["all_sections_teacher_review_required"]).lower()}
all_sections_degraded_preview_label_required={str(result["all_sections_degraded_preview_label_required"]).lower()}
all_sections_model_text_not_generated={str(result["all_sections_model_text_not_generated"]).lower()}
preview_only_actions={str(result["preview_only_actions"]).lower()}
provider_called={str(result["provider_called"]).lower()}
model_called={str(result["model_called"]).lower()}
unit_package_written={str(result["unit_package_written"]).lower()}
lesson_body_modified={str(result["lesson_body_modified"]).lower()}
database_written={str(result["database_written"]).lower()}
memory_written={str(result["memory_written"]).lower()}
```

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
PROVIDER_MODEL_CALL_ALLOWED=false
FORMAL_APPLY_ALLOWED=false
DATABASE_WRITE_ALLOWED=false
MEMORY_WRITE_ALLOWED=false

1013K_R3 converts R2 candidate envelopes into teacher-readable static section preview fixtures. It is local-only and deterministic; no provider/model call and no formal unit_package or lesson body write.
"""
    manifest = f"""# Review Package Manifest

Latest local stage: `{STAGE_ID}`

Includes:

- `{STAGE_DIR_NAME}/big_unit_static_section_preview_bundle_1013K_R3.json`
- `{STAGE_DIR_NAME}/big_unit_static_preview_review_actions_1013K_R3.json`
- `{STAGE_DIR_NAME}/big_unit_static_preview_trace_1013K_R3.json`
- `{STAGE_DIR_NAME}/1013K_R3_result.json`
- `{STAGE_DIR_NAME}/1013K_R3_report.md`
- `backend/xiaobei_ai/prep_room_big_unit_static_section_preview_1013K_R3.py`
- `scripts/{VALIDATOR_NAME}`

Boundary: local-only small package. No GitHub upload until milestone; no provider/model call, no runtime connection, no database/memory/Feishu write, no formal apply, no unit_package or lesson body write.

Next stage: `{NEXT_STAGE}`
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
        stage_dir / "big_unit_static_section_preview_bundle_1013K_R3.json",
        stage_dir / "big_unit_static_preview_review_actions_1013K_R3.json",
        stage_dir / "big_unit_static_preview_trace_1013K_R3.json",
        *source_delta_files,
        output_root / "LATEST_REVIEW_ENTRY.md",
        output_root / "REVIEW_PACKAGE_MANIFEST.md",
    ]
    result = build_result(root, output_root, payload, stage_files)
    write_json(stage_dir / "1013K_R3_result.json", result)
    write_text(stage_dir / "1013K_R3_report.md", build_report(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["validator_pass"]:
        print("ALL_1013K_R3_BIG_UNIT_CANDIDATE_ENVELOPE_TO_STATIC_SECTION_PREVIEW_CHECKS_OK")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
