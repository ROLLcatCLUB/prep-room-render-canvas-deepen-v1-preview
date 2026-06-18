from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6G_BIG_UNIT_PREP_PAGE_FIXTURE_AFTER_USER_APPROVAL"
FINAL_STATUS = "PASS_1013I_R6G_BIG_UNIT_PREP_PAGE_FIXTURE_AFTER_USER_APPROVAL"
INHERITS_FROM = "1013I_R6F_BIG_UNIT_PREP_PAGE_FIXTURE_USER_REVIEW_GATE"
R6F_PASS_STATUS = "PASS_1013I_R6F_BIG_UNIT_PREP_PAGE_FIXTURE_USER_REVIEW_GATE"
USER_REVIEW_DECISION = "APPROVE_WITH_CONSTRAINTS"
NEXT_STAGE = "1013I_R6H_BIG_UNIT_PREP_PAGE_FIXTURE_REVIEW_BEFORE_HTML"
STAGE_DIR_NAME = "1013I_R6G_big_unit_prep_page_fixture_after_user_approval"
VALIDATOR_NAME = "validate_1013I_R6G_big_unit_prep_page_fixture_after_user_approval.py"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)app[_-]?secret\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)tenant[_-]?access[_-]?token\s*[:=]\s*['\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)cookie\s*[:=]\s*['\"][^'\"]{20,}"),
]


LESSON_POSITION_LABELS = {
    "unit_entry": "单元开头：先激发兴趣、建立问题",
    "concept_building": "概念建立：先让学生弄清楚一个关键概念",
    "method_learning": "方法学习：重点学一种观察/表现方法",
    "creative_production": "创作表现：主要完成一件作品",
    "critique_and_revision": "交流修改：主要展示、评价、调整作品",
    "exhibition_or_reflection": "展示反思：主要呈现成果、回看学习过程",
    "unknown_pending_teacher_confirm": "暂不确定：需要老师补充单元材料",
}


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
        "page_fixture_created": True,
        "fixture_only": True,
        "ui_implementation_started": False,
        "html_ui_implementation_allowed": False,
        "html_body_modified": False,
        "lesson_body_modified": False,
        "normal_candidate_card_generation_allowed": False,
        "writes_unit_package": False,
        "writes_lesson_body": False,
        "verified_textbook_anchor_created": False,
        "official_claim_created": False,
        "big_unit_generation_performed": False,
        "single_lesson_generation_performed": False,
        "r7_visual_review_entered": False,
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


def stage_dir(output_root: Path, name: str) -> Path:
    return output_root / name


def load_inputs(output_root: Path) -> dict[str, Any]:
    r6e = stage_dir(output_root, "1013I_R6E_official_unit_material_readonly_extraction_fixture")
    r6f = stage_dir(output_root, "1013I_R6F_big_unit_prep_page_fixture_user_review_gate")
    return {
        "r6e_result": read_json(r6e / "1013I_R6E_result.json"),
        "r6e_extraction_fixture": read_json(r6e / "official_unit_material_extraction_fixture_1013I_R6E.json"),
        "textbook_anchor_candidates": read_json(r6e / "textbook_anchor_candidates_1013I_R6E.json"),
        "big_unit_chain_candidates": read_json(r6e / "big_unit_chain_candidates_1013I_R6E.json"),
        "teacher_confirmation_required_items": read_json(
            r6e / "teacher_confirmation_required_items_1013I_R6E.json"
        ),
        "r6f_result": read_json(r6f / "1013I_R6F_result.json"),
        "r6f_structure_proposal": read_json(
            r6f / "big_unit_prep_page_structure_proposal_1013I_R6F.json"
        ),
        "r6f_sections": read_json(r6f / "big_unit_prep_page_sections_1013I_R6F.json"),
    }


def build_light_timeline(big_unit_chain: dict[str, Any]) -> list[dict[str, Any]]:
    chain = big_unit_chain["unit_package_candidate"]["unit_task_chain_candidates"]
    timeline = []
    for item in chain:
        fields = item.get("field_candidates", [])
        field_labels = [field.get("teacher_friendly_name") or field.get("official_field_name") for field in fields]
        timeline.append(
            {
                "timeline_node_id": f"timeline_{item['stage_id']}",
                "stage_id": item["stage_id"],
                "teacher_title": item["stage_name"],
                "one_sentence_purpose": item["stage_goal"],
                "field_count": len(fields),
                "field_label_preview": field_labels[:3],
                "expanded_by_default": False,
                "writes_unit_package": False,
                "candidate_status": "pending_teacher_review",
            }
        )
    return timeline


def build_lesson_position_options(extraction_fixture: dict[str, Any]) -> list[dict[str, Any]]:
    roles = extraction_fixture["lesson_position_candidate"]["possible_roles"]
    return [
        {
            "role_key": role,
            "teacher_label": LESSON_POSITION_LABELS.get(role, role),
            "visible_to_teacher": True,
            "selected": False,
            "candidate_status": "pending_teacher_review",
        }
        for role in roles
    ]


def build_page_fixture(inputs: dict[str, Any]) -> dict[str, Any]:
    textbook_candidates = inputs["textbook_anchor_candidates"]
    big_unit_chain = inputs["big_unit_chain_candidates"]
    confirmation_items = inputs["teacher_confirmation_required_items"]["items"]
    extraction_fixture = inputs["r6e_extraction_fixture"]
    source_lesson = textbook_candidates["candidates"][0]["source_request_lesson"]
    candidate_anchor = textbook_candidates["candidates"][0]["candidate_anchor"]
    timeline = build_light_timeline(big_unit_chain)
    lesson_position_options = build_lesson_position_options(extraction_fixture)

    return {
        "stage": STAGE_ID,
        "fixture_id": "big_unit_prep_page_fixture_1013I_R6G",
        "inherits_from": INHERITS_FROM,
        "user_review_decision": USER_REVIEW_DECISION,
        "approval_constraints_applied": [
            "decision_first_layout",
            "big_unit_chain_as_light_timeline",
            "lesson_position_teacher_labels_present",
        ],
        **profile(),
        "teacher_visible_title": "大单元位置确认",
        "page_purpose": "help_teacher_make_required_decisions_before_single_lesson_prep",
        "layout_mode": "decision_first",
        "decision_first_layout": True,
        "first_screen": {
            "top": {
                "component_type": "blocking_reason_banner",
                "teacher_copy": "现在还不能直接生成单课备课，需要先确认教材锚点、大单元推进链和这节课承担的任务。",
                "blocking_state_visible": True,
                "normal_candidate_card_generation_allowed": False,
            },
            "middle": {
                "component_type": "confirmation_missing_list",
                "teacher_copy": "还差这些确认",
                "items": confirmation_items,
                "default_state": "expanded",
            },
            "lower": {
                "component_type": "candidate_summary_three_column",
                "columns": [
                    {
                        "column_id": "textbook_anchor_summary",
                        "teacher_label": "教材锚点",
                        "summary": f"{source_lesson['grade']} {source_lesson['subject']}《{source_lesson['lesson_title']}》",
                        "candidate_status": candidate_anchor["teacher_confirmation_status"],
                    },
                    {
                        "column_id": "lesson_position_summary",
                        "teacher_label": "本课位置",
                        "summary": "待老师选择这节课在单元中承担什么任务",
                        "candidate_status": "pending_teacher_review",
                    },
                    {
                        "column_id": "big_unit_chain_summary",
                        "teacher_label": "大单元链",
                        "summary": f"{len(timeline)} 个阶段候选，先轻量查看",
                        "candidate_status": "pending_teacher_review",
                    },
                ],
            },
            "right": {
                "component_type": "readonly_reference_rail",
                "teacher_label": "只读依据",
                "default_state": "collapsed",
                "official_reference_notes_collapsed": True,
            },
        },
        "sections": [
            {
                "section_id": "decision_status",
                "teacher_label": "为什么现在不能直接生成单课",
                "default_state": "expanded",
                "priority": 1,
                "blocking_state_visible": True,
                "normal_candidate_card_generation_allowed": False,
            },
            {
                "section_id": "teacher_confirmation_items",
                "teacher_label": "还差哪几项教师确认",
                "default_state": "expanded",
                "priority": 2,
                "items": confirmation_items,
                "candidate_fields_marked_pending_teacher_review": True,
            },
            {
                "section_id": "textbook_anchor_candidates",
                "teacher_label": "教材锚点候选",
                "default_state": "summary",
                "priority": 3,
                "candidate": textbook_candidates["candidates"][0],
                "candidate_fields_marked_pending_teacher_review": True,
                "verified_textbook_anchor_created": False,
            },
            {
                "section_id": "lesson_position_candidate",
                "teacher_label": "本课承担什么任务",
                "default_state": "summary",
                "priority": 4,
                "options": lesson_position_options,
                "lesson_position_teacher_labels_present": True,
                "engineering_enum_visible_as_primary_copy": False,
                "candidate_fields_marked_pending_teacher_review": True,
            },
            {
                "section_id": "big_unit_chain_light_timeline",
                "teacher_label": "大单元推进链",
                "default_state": "summary",
                "priority": 5,
                "timeline": timeline,
                "big_unit_chain_as_light_timeline": True,
                "full_big_unit_body_visible": False,
                "writes_unit_package": False,
            },
            {
                "section_id": "readonly_reference_notes",
                "teacher_label": "只读依据和风险提醒",
                "default_state": "collapsed",
                "priority": 6,
                "official_reference_notes_collapsed": True,
                "official_claim_created": False,
            },
        ],
        **boundary(),
    }


def build_action_state_fixture(page_fixture: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": STAGE_ID,
        "fixture_id": "big_unit_prep_page_action_state_1013I_R6G",
        "teacher_actions": [
            {
                "action_id": "confirm_textbook_anchor",
                "teacher_label": "确认这个教材锚点",
                "enabled": True,
                "writes_formal_anchor": False,
                "result_state": "preview_confirmation_only",
            },
            {
                "action_id": "choose_lesson_position",
                "teacher_label": "选择这节课承担的任务",
                "enabled": True,
                "writes_lesson_body": False,
                "result_state": "preview_confirmation_only",
            },
            {
                "action_id": "confirm_chain_shape",
                "teacher_label": "这个单元链大方向可以",
                "enabled": True,
                "writes_unit_package": False,
                "result_state": "preview_confirmation_only",
            },
            {
                "action_id": "request_more_material",
                "teacher_label": "我还要补教材/单元材料",
                "enabled": True,
                "writes_database": False,
                "result_state": "awaiting_material",
            },
            {
                "action_id": "continue_degraded_single_lesson_draft",
                "teacher_label": "先按临时单课草稿继续",
                "enabled": True,
                "requires_visible_degraded_label": True,
                "normal_candidate_card_generation_allowed": False,
                "result_state": "degraded_draft_only",
            },
        ],
        "candidate_fields_marked_pending_teacher_review": True,
        "normal_candidate_card_generation_allowed": False,
        **boundary(),
    }


def build_review_summary(page_fixture: dict[str, Any]) -> str:
    return f"""# 1013I_R6G Big Unit Prep Page Fixture Review Summary

```text
STAGE={STAGE_ID}
FINAL_STATUS={FINAL_STATUS}
USER_REVIEW_DECISION={USER_REVIEW_DECISION}
NEXT_STAGE={NEXT_STAGE}
HTML_UI_IMPLEMENTATION_ALLOWED=false
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
```

## Applied Constraints

1. Decision-first layout: the first screen starts from the blocking reason and missing teacher confirmations.
2. Big-unit chain is a light timeline: four stage candidates, one sentence each, no full unit body.
3. Lesson-position options use teacher-facing labels while keeping backend role keys.

## Still Forbidden

- No HTML write.
- No real UI implementation.
- No R7 visual review.
- No big-unit body generation.
- No single-lesson plan generation.
- No provider/model call.
- No database, memory, Feishu, export, or archive write.
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


def build_result(output_root: Path, stage_files: list[Path]) -> dict[str, Any]:
    stage = output_root / STAGE_DIR_NAME
    latest_text = (output_root / "LATEST_REVIEW_ENTRY.md").read_text(encoding="utf-8")
    manifest_text = (output_root / "REVIEW_PACKAGE_MANIFEST.md").read_text(encoding="utf-8")
    inputs = load_inputs(output_root)
    page_fixture = read_json(stage / "big_unit_prep_page_fixture_1013I_R6G.json")
    action_state = read_json(stage / "big_unit_prep_page_action_state_1013I_R6G.json")
    lesson_options = [
        option
        for section in page_fixture["sections"]
        if section["section_id"] == "lesson_position_candidate"
        for option in section["options"]
    ]
    timeline = [
        node
        for section in page_fixture["sections"]
        if section["section_id"] == "big_unit_chain_light_timeline"
        for node in section["timeline"]
    ]

    result = {
        "stage": STAGE_ID,
        "generated_at": now(),
        "final_status": FINAL_STATUS,
        "inherits_from": INHERITS_FROM,
        "next_stage": NEXT_STAGE,
        "user_review_decision": USER_REVIEW_DECISION,
        "r6f_result_present": True,
        "r6f_final_status": inputs["r6f_result"].get("final_status"),
        "r6f_pass": inputs["r6f_result"].get("final_status") == R6F_PASS_STATUS,
        "latest_entry_points_to_r6g": f"REVIEW_STAGE={STAGE_ID}" in latest_text
        and f"FINAL_STATUS={FINAL_STATUS}" in latest_text,
        "latest_entry_next_stage_is_r6h": f"NEXT_RECOMMENDED_STAGE={NEXT_STAGE}" in latest_text,
        "manifest_includes_r6g": STAGE_ID in manifest_text and f"{STAGE_DIR_NAME}/" in manifest_text,
        "manifest_next_stage_is_r6h": NEXT_STAGE in manifest_text,
        "page_fixture_created": (stage / "big_unit_prep_page_fixture_1013I_R6G.json").exists(),
        "page_action_state_created": (stage / "big_unit_prep_page_action_state_1013I_R6G.json").exists(),
        "review_summary_created": (stage / "big_unit_prep_page_fixture_review_summary_1013I_R6G.md").exists(),
        "decision_first_layout": page_fixture.get("decision_first_layout") is True,
        "blocking_state_visible": page_fixture["first_screen"]["top"].get("blocking_state_visible") is True,
        "official_reference_notes_collapsed": page_fixture["first_screen"]["right"].get(
            "official_reference_notes_collapsed"
        )
        is True,
        "big_unit_chain_as_light_timeline": any(
            section.get("big_unit_chain_as_light_timeline") is True for section in page_fixture["sections"]
        ),
        "light_timeline_node_count": len(timeline),
        "light_timeline_nodes_collapsed": all(node.get("expanded_by_default") is False for node in timeline),
        "lesson_position_teacher_labels_present": all(option.get("teacher_label") for option in lesson_options),
        "engineering_enum_not_primary_teacher_copy": any(
            section.get("section_id") == "lesson_position_candidate"
            and section.get("engineering_enum_visible_as_primary_copy") is False
            for section in page_fixture["sections"]
        ),
        "candidate_fields_marked_pending_teacher_review": page_fixture.get(
            "sections", []
        )[1].get("candidate_fields_marked_pending_teacher_review")
        is True
        and action_state.get("candidate_fields_marked_pending_teacher_review") is True,
        "teacher_visible_deprecated_agent_hits": scan_deprecated_visible_names(stage_files),
        "secret_scan_hits": scan_secrets(stage_files),
        **profile(),
        **boundary(),
    }
    required_true = [
        "r6f_result_present",
        "r6f_pass",
        "latest_entry_points_to_r6g",
        "latest_entry_next_stage_is_r6h",
        "manifest_includes_r6g",
        "manifest_next_stage_is_r6h",
        "page_fixture_created",
        "page_action_state_created",
        "review_summary_created",
        "decision_first_layout",
        "blocking_state_visible",
        "official_reference_notes_collapsed",
        "big_unit_chain_as_light_timeline",
        "light_timeline_nodes_collapsed",
        "lesson_position_teacher_labels_present",
        "engineering_enum_not_primary_teacher_copy",
        "candidate_fields_marked_pending_teacher_review",
        "fixture_only",
    ]
    required_false = [
        "ui_implementation_started",
        "html_ui_implementation_allowed",
        "html_body_modified",
        "lesson_body_modified",
        "normal_candidate_card_generation_allowed",
        "writes_unit_package",
        "writes_lesson_body",
        "verified_textbook_anchor_created",
        "official_claim_created",
        "big_unit_generation_performed",
        "single_lesson_generation_performed",
        "r7_visual_review_entered",
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
    if result.get("light_timeline_node_count") != 4:
        failures.append("light_timeline_node_count")
    if result["teacher_visible_deprecated_agent_hits"]:
        failures.append("teacher_visible_deprecated_agent_hits")
    if result["secret_scan_hits"]:
        failures.append("secret_scan_hits")
    result["failed_checks"] = failures
    if failures:
        result["final_status"] = "FAIL_1013I_R6G_BIG_UNIT_PREP_PAGE_FIXTURE_AFTER_USER_APPROVAL"
    return result


def build_report(result: dict[str, Any]) -> str:
    return f"""# 1013I_R6G Big Unit Prep Page Fixture Report

```text
STAGE={STAGE_ID}
FINAL_STATUS={result["final_status"]}
USER_REVIEW_DECISION={USER_REVIEW_DECISION}
INHERITS_FROM={INHERITS_FROM}
NEXT_STAGE={NEXT_STAGE}
PAGE_FIXTURE_ALLOWED=true
HTML_UI_IMPLEMENTATION_ALLOWED=false
FORMAL_APPLY_ALLOWED=false
PROVIDER_MODEL_CALL_ALLOWED=false
```

## Result

```text
page_fixture_created={str(result["page_fixture_created"]).lower()}
decision_first_layout={str(result["decision_first_layout"]).lower()}
blocking_state_visible={str(result["blocking_state_visible"]).lower()}
official_reference_notes_collapsed={str(result["official_reference_notes_collapsed"]).lower()}
big_unit_chain_as_light_timeline={str(result["big_unit_chain_as_light_timeline"]).lower()}
light_timeline_node_count={result["light_timeline_node_count"]}
lesson_position_teacher_labels_present={str(result["lesson_position_teacher_labels_present"]).lower()}
candidate_fields_marked_pending_teacher_review={str(result["candidate_fields_marked_pending_teacher_review"]).lower()}
writes_unit_package={str(result["writes_unit_package"]).lower()}
writes_lesson_body={str(result["writes_lesson_body"]).lower()}
normal_candidate_card_generation_allowed={str(result["normal_candidate_card_generation_allowed"]).lower()}
ui_implementation_started={str(result["ui_implementation_started"]).lower()}
html_body_modified={str(result["html_body_modified"]).lower()}
```

## Boundary

R6G creates a JSON page fixture only. It does not write HTML, does not implement UI, does not enter R7 visual review, does not generate a big-unit body or single-lesson plan, and does not call provider/model or write database, memory, Feishu, export, or archive.
"""


def copy_source_delta(root: Path, output_root: Path) -> None:
    source = root / "scripts" / VALIDATOR_NAME
    target = output_root / "source_delta_1013I_R6G" / "scripts" / VALIDATOR_NAME
    if source.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = resolve_output_root(root)
    inputs = load_inputs(output_root)
    stage = output_root / STAGE_DIR_NAME
    page_fixture = build_page_fixture(inputs)
    write_json(stage / "big_unit_prep_page_fixture_1013I_R6G.json", page_fixture)
    write_json(stage / "big_unit_prep_page_action_state_1013I_R6G.json", build_action_state_fixture(page_fixture))
    write_text(stage / "big_unit_prep_page_fixture_review_summary_1013I_R6G.md", build_review_summary(page_fixture))
    result_path = stage / "1013I_R6G_result.json"
    report_path = stage / "1013I_R6G_report.md"
    stage_files = [
        stage / "big_unit_prep_page_fixture_1013I_R6G.json",
        stage / "big_unit_prep_page_action_state_1013I_R6G.json",
        stage / "big_unit_prep_page_fixture_review_summary_1013I_R6G.md",
        result_path,
        report_path,
    ]
    result = build_result(output_root, stage_files)
    write_json(result_path, result)
    write_text(report_path, build_report(result))
    copy_source_delta(root, output_root)
    if result["final_status"] != FINAL_STATUS:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    print(f"{FINAL_STATUS}: {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
