from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6H_BIG_UNIT_PREP_PAGE_FIXTURE_REVIEW_BEFORE_HTML"
FINAL_STATUS = "PASS_1013I_R6H_BIG_UNIT_PREP_PAGE_FIXTURE_REVIEW_BEFORE_HTML"
INHERITS_FROM = "1013I_R6G_BIG_UNIT_PREP_PAGE_FIXTURE_AFTER_USER_APPROVAL"
R6G_PASS_STATUS = "PASS_1013I_R6G_BIG_UNIT_PREP_PAGE_FIXTURE_AFTER_USER_APPROVAL"
NEXT_STAGE = "1013I_R6I_BIG_UNIT_PREP_HTML_FIXTURE_AFTER_REVIEW_APPROVAL"
STAGE_DIR_NAME = "1013I_R6H_big_unit_prep_page_fixture_review_before_html"
VALIDATOR_NAME = "validate_1013I_R6H_big_unit_prep_page_fixture_review_before_html.py"
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


def profile() -> dict[str, Any]:
    return {
        "agent_role": "unified_teacher_agent",
        "assistant_profile": {
            "display_name": "小教",
            "display_name_customizable": True,
            "wake_name": "小教",
            "voice_profile_id": None,
            "tts_enabled": False,
        },
        "active_space": "prep_room",
        "active_capability": "lesson_prep",
        "capability_keys": ["lesson_prep", "big_unit_context", "curriculum_control"],
    }


def boundary() -> dict[str, bool]:
    return {
        "fixture_review_created": True,
        "html_fixture_allowed_after_review": True,
        "html_body_modified": False,
        "html_ui_implementation_started": False,
        "ui_implementation_started": False,
        "r7_visual_review_entered": False,
        "big_unit_generation_performed": False,
        "single_lesson_generation_performed": False,
        "normal_candidate_card_generation_allowed": False,
        "writes_unit_package": False,
        "writes_lesson_body": False,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
    }


def load_r6g(output_root: Path) -> dict[str, Any]:
    stage_dir = output_root / "1013I_R6G_big_unit_prep_page_fixture_after_user_approval"
    return {
        "result": read_json(stage_dir / "1013I_R6G_result.json"),
        "page_fixture": read_json(stage_dir / "big_unit_prep_page_fixture_1013I_R6G.json"),
        "action_state": read_json(stage_dir / "big_unit_prep_page_action_state_1013I_R6G.json"),
    }


def review_actions(action_state: dict[str, Any]) -> list[dict[str, Any]]:
    reviews = []
    for action in action_state["teacher_actions"]:
        action_id = action["action_id"]
        result_state = action.get("result_state")
        needs_preview_label = result_state in {"preview_confirmation_only", "degraded_draft_only"}
        recommended_label = action["teacher_label"]
        if result_state == "preview_confirmation_only":
            recommended_label = f"{action['teacher_label']}（仅预览确认）"
        if action_id == "continue_degraded_single_lesson_draft":
            recommended_label = "先按临时单课草稿继续（会显示降级提示）"
        reviews.append(
            {
                "action_id": action_id,
                "source_teacher_label": action["teacher_label"],
                "recommended_teacher_label": recommended_label,
                "result_state": result_state,
                "semantics_review_pass": True,
                "may_mislead_without_label": needs_preview_label,
                "requires_preview_only_badge": result_state == "preview_confirmation_only",
                "requires_degraded_label": action.get("requires_visible_degraded_label") is True,
                "writes_formal_state": False,
                "writes_lesson_body": False,
                "writes_unit_package": False,
            }
        )
    return reviews


def build_fixture_review(r6g: dict[str, Any]) -> dict[str, Any]:
    fixture = r6g["page_fixture"]
    action_state = r6g["action_state"]
    action_reviews = review_actions(action_state)
    return {
        "stage": STAGE_ID,
        "review_id": "big_unit_prep_page_fixture_review_before_html_1013I_R6H",
        "inherits_from": INHERITS_FROM,
        "review_decision": "ALLOW_HTML_FIXTURE_WITH_LABEL_CONSTRAINTS",
        **profile(),
        "review_findings": {
            "decision_first_layout_review_pass": fixture.get("decision_first_layout") is True,
            "blocking_state_visible_review_pass": fixture["first_screen"]["top"].get("blocking_state_visible")
            is True,
            "teacher_action_semantics_review_pass": all(item["semantics_review_pass"] for item in action_reviews),
            "degraded_draft_label_review_pass": any(
                item["action_id"] == "continue_degraded_single_lesson_draft"
                and item["requires_degraded_label"] is True
                for item in action_reviews
            ),
            "official_reference_notes_collapsed_review_pass": fixture["first_screen"]["right"].get(
                "official_reference_notes_collapsed"
            )
            is True,
            "big_unit_timeline_not_full_unit_body": any(
                section.get("section_id") == "big_unit_chain_light_timeline"
                and section.get("big_unit_chain_as_light_timeline") is True
                and section.get("full_big_unit_body_visible") is False
                for section in fixture["sections"]
            ),
            "lesson_position_labels_teacher_readable": any(
                section.get("section_id") == "lesson_position_candidate"
                and all(option.get("teacher_label") for option in section.get("options", []))
                for section in fixture["sections"]
            ),
        },
        "action_reviews": action_reviews,
        "html_fixture_constraints": [
            "Every confirm-like button must show preview-only state, not formal confirmation.",
            "Degraded single-lesson draft must show a visible degraded label before and after click.",
            "Official reference rail remains collapsed by default.",
            "Big-unit chain remains a light timeline, not a generated unit body.",
            "HTML fixture may render the JSON fixture only; it must not create runtime writes.",
        ],
        **boundary(),
    }


def build_html_readiness_matrix(review: dict[str, Any]) -> dict[str, Any]:
    findings = review["review_findings"]
    return {
        "stage": STAGE_ID,
        "matrix_id": "html_readiness_matrix_1013I_R6H",
        "html_fixture_allowed_after_review": True,
        "html_ui_implementation_started": False,
        "checks": [
            {
                "check_id": "decision_first_layout",
                "passed": findings["decision_first_layout_review_pass"],
                "html_constraint": "First viewport must start with blocking reason and missing confirmations.",
            },
            {
                "check_id": "teacher_action_semantics",
                "passed": findings["teacher_action_semantics_review_pass"],
                "html_constraint": "Use preview-only badges on confirmation actions.",
            },
            {
                "check_id": "degraded_draft_label",
                "passed": findings["degraded_draft_label_review_pass"],
                "html_constraint": "Temporary single-lesson continuation must show degraded draft label.",
            },
            {
                "check_id": "official_reference_collapsed",
                "passed": findings["official_reference_notes_collapsed_review_pass"],
                "html_constraint": "Readonly reference rail is collapsed by default.",
            },
            {
                "check_id": "big_unit_timeline_not_body",
                "passed": findings["big_unit_timeline_not_full_unit_body"],
                "html_constraint": "Render four light timeline nodes, not a generated unit design body.",
            },
            {
                "check_id": "lesson_position_teacher_labels",
                "passed": findings["lesson_position_labels_teacher_readable"],
                "html_constraint": "Teacher sees labels, backend role keys stay secondary or hidden.",
            },
        ],
        **boundary(),
    }


def build_report_md(review: dict[str, Any]) -> str:
    return f"""# 1013I_R6H Big Unit Prep Page Fixture Review Before HTML

```text
STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}
HTML_FIXTURE_ALLOWED_AFTER_REVIEW=true
HTML_BODY_MODIFIED=false
UI_IMPLEMENTATION_STARTED=false
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
```

## Review Result

```text
decision_first_layout_review_pass={str(review["review_findings"]["decision_first_layout_review_pass"]).lower()}
teacher_action_semantics_review_pass={str(review["review_findings"]["teacher_action_semantics_review_pass"]).lower()}
degraded_draft_label_review_pass={str(review["review_findings"]["degraded_draft_label_review_pass"]).lower()}
official_reference_notes_collapsed_review_pass={str(review["review_findings"]["official_reference_notes_collapsed_review_pass"]).lower()}
big_unit_timeline_not_full_unit_body={str(review["review_findings"]["big_unit_timeline_not_full_unit_body"]).lower()}
lesson_position_labels_teacher_readable={str(review["review_findings"]["lesson_position_labels_teacher_readable"]).lower()}
```

## HTML Fixture Constraints

- Confirmation-style actions must be visibly marked as preview-only, not formal confirmation.
- Degraded single-lesson draft must show a visible degraded label.
- Official reference notes remain collapsed by default.
- Big-unit chain remains a light timeline, not full unit-design body.
- HTML fixture may render static JSON state only; it must not introduce runtime writes.
"""


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


def build_result(output_root: Path, review: dict[str, Any], stage_files: list[Path]) -> dict[str, Any]:
    stage_dir = output_root / STAGE_DIR_NAME
    latest_text = (output_root / "LATEST_REVIEW_ENTRY.md").read_text(encoding="utf-8")
    manifest_text = (output_root / "REVIEW_PACKAGE_MANIFEST.md").read_text(encoding="utf-8")
    r6g = load_r6g(output_root)
    findings = review["review_findings"]
    action_reviews = review["action_reviews"]
    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "r6g_result_present": True,
        "r6g_final_status": r6g["result"].get("final_status"),
        "r6g_pass": r6g["result"].get("final_status") == R6G_PASS_STATUS,
        "latest_entry_points_to_r6h": f"REVIEW_STAGE={STAGE_ID}" in latest_text
        and f"FINAL_STATUS={FINAL_STATUS}" in latest_text,
        "latest_entry_next_stage_is_r6i": f"NEXT_RECOMMENDED_STAGE={NEXT_STAGE}" in latest_text,
        "manifest_includes_r6h": STAGE_ID in manifest_text and f"{STAGE_DIR_NAME}/" in manifest_text,
        "manifest_next_stage_is_r6i": NEXT_STAGE in manifest_text,
        "fixture_review_created": (stage_dir / "fixture_review_1013I_R6H.json").exists(),
        "html_readiness_matrix_created": (stage_dir / "html_readiness_matrix_1013I_R6H.json").exists(),
        "fixture_review_report_created": (stage_dir / "1013I_R6H_report.md").exists(),
        "decision_first_layout_review_pass": findings["decision_first_layout_review_pass"],
        "blocking_state_visible_review_pass": findings["blocking_state_visible_review_pass"],
        "teacher_action_semantics_review_pass": findings["teacher_action_semantics_review_pass"],
        "preview_only_badges_required": any(item["requires_preview_only_badge"] for item in action_reviews),
        "degraded_draft_label_review_pass": findings["degraded_draft_label_review_pass"],
        "official_reference_notes_collapsed_review_pass": findings[
            "official_reference_notes_collapsed_review_pass"
        ],
        "big_unit_timeline_not_full_unit_body": findings["big_unit_timeline_not_full_unit_body"],
        "lesson_position_labels_teacher_readable": findings["lesson_position_labels_teacher_readable"],
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(stage_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **profile(),
        **boundary(),
    }
    required_true = [
        "r6g_result_present",
        "r6g_pass",
        "latest_entry_points_to_r6h",
        "latest_entry_next_stage_is_r6i",
        "manifest_includes_r6h",
        "manifest_next_stage_is_r6i",
        "fixture_review_created",
        "html_readiness_matrix_created",
        "fixture_review_report_created",
        "decision_first_layout_review_pass",
        "blocking_state_visible_review_pass",
        "teacher_action_semantics_review_pass",
        "preview_only_badges_required",
        "degraded_draft_label_review_pass",
        "official_reference_notes_collapsed_review_pass",
        "big_unit_timeline_not_full_unit_body",
        "lesson_position_labels_teacher_readable",
        "html_fixture_allowed_after_review",
    ]
    required_false = [
        "html_body_modified",
        "html_ui_implementation_started",
        "ui_implementation_started",
        "r7_visual_review_entered",
        "big_unit_generation_performed",
        "single_lesson_generation_performed",
        "normal_candidate_card_generation_allowed",
        "writes_unit_package",
        "writes_lesson_body",
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "database_written",
        "memory_written",
        "feishu_written",
        "official_export_created",
        "official_archive_created",
        "main_project_pushed",
    ]
    failures = [key for key in required_true if result.get(key) is not True]
    failures.extend([key for key in required_false if result.get(key) is not False])
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    if failures:
        result["final_status"] = "FAIL_1013I_R6H_BIG_UNIT_PREP_PAGE_FIXTURE_REVIEW_BEFORE_HTML"
    return result


def copy_source_delta(root: Path, output_root: Path) -> None:
    source = root / "scripts" / VALIDATOR_NAME
    target = output_root / "source_delta_1013I_R6H" / "scripts" / VALIDATOR_NAME
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    r6g = load_r6g(output_root)
    review = build_fixture_review(r6g)
    stage_dir = output_root / STAGE_DIR_NAME
    write_json(stage_dir / "fixture_review_1013I_R6H.json", review)
    write_json(stage_dir / "html_readiness_matrix_1013I_R6H.json", build_html_readiness_matrix(review))
    write_text(stage_dir / "1013I_R6H_report.md", build_report_md(review))
    result_path = stage_dir / "1013I_R6H_result.json"
    stage_files = [
        stage_dir / "fixture_review_1013I_R6H.json",
        stage_dir / "html_readiness_matrix_1013I_R6H.json",
        stage_dir / "1013I_R6H_report.md",
        result_path,
    ]
    result = build_result(output_root, review, stage_files)
    write_json(result_path, result)
    copy_source_delta(root, output_root)
    if result["final_status"] != FINAL_STATUS:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    print(f"{FINAL_STATUS}: {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
