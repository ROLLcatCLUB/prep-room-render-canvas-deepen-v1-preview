from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R0A1_DIR = OUTPUT_ROOT / "1013I_R0A1_request_id_trace_alignment_hotfix"
R2_DIR = OUTPUT_ROOT / "1013I_R2_teacher_review_card_surface_from_seed"
R3_DIR = OUTPUT_ROOT / "1013I_R3_self_prep_preview_chain_from_review_cards"
OUT_DIR = OUTPUT_ROOT / "1013I_R4_minimal_self_prep_page_fixture"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013I_R4" / "scripts"

STAGE_ID = "1013I_R4_MINIMAL_SELF_PREP_PAGE_FIXTURE"
NEXT_STAGE = "1013I_R5_TEACHER_SELF_PREP_ALPHA_SMOKE"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_teacher_input_summary(request: dict[str, Any]) -> dict[str, Any]:
    teacher_input = request["teacher_input"]
    return {
        "section_id": "teacher_input_summary",
        "title": "教师输入摘要",
        "request_id": request["request_id"],
        "original_request_id": request["original_request_id"],
        "grade_level": teacher_input["grade_level"],
        "subject": teacher_input["subject"],
        "lesson_title": teacher_input["lesson_title"],
        "lesson_count": teacher_input["lesson_count"],
        "unit_or_textbook_context": teacher_input["unit_or_textbook_context"],
        "class_profile_hint": teacher_input["class_profile_hint"],
        "teacher_ideas": teacher_input["teacher_ideas"],
        "existing_materials": teacher_input["existing_materials"],
        "classroom_constraints": teacher_input["classroom_constraints"],
        "preferred_depth": teacher_input["preferred_depth"],
        "agent_role": teacher_input["agent_role"],
        "assistant_profile": teacher_input["assistant_profile"],
        "active_space": teacher_input["active_space"],
        "active_capability": teacher_input["active_capability"],
    }


def build_review_cards_section(surface: dict[str, Any]) -> dict[str, Any]:
    return {
        "section_id": "review_cards",
        "title": "候选审阅卡",
        "state_hint": "教师先看建议，再选择采纳到预览、再改一版或暂不采用。",
        "cards": surface["review_cards"],
    }


def build_preview_section(preview_state: dict[str, Any], diff_cards: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "section_id": "preview_diff",
        "title": "当前预览态",
        "state_hint": "当前页面主状态显示为采纳到预览；修改和暂不采用作为可切换路径，不与当前预览态混在一起。",
        "current_preview_mode": "accepted_to_preview_only",
        "accepted_preview_items": preview_state["accepted_preview_items"],
        "preview_diff_cards": diff_cards,
    }


def build_revision_section(preview_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "section_id": "revision_queue",
        "title": "再改一版队列",
        "state_hint": "这些是动作路径验证后的可切换队列，不代表当前预览态同时已退回修改。",
        "items": preview_state["revision_queue"],
        "audit_simulated_path": True,
    }


def build_rejected_section(preview_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "section_id": "rejected_items",
        "title": "暂不采用项",
        "state_hint": "这些是动作路径验证后的可切换队列，不代表当前预览态同时已拒绝。",
        "items": preview_state["rejected_items"],
        "audit_simulated_path": True,
    }


def build_page_actions(preview_state: dict[str, Any]) -> dict[str, Any]:
    actions = []
    for item in preview_state["accepted_preview_items"]:
        actions.append(
            {
                "action_id": f"revert_{item['preview_item_id']}",
                "action": "revert_preview_item",
                "label": "撤回预览",
                "target_preview_item_id": item["preview_item_id"],
                "available": True,
                "formal_apply_performed": False,
                "lesson_body_modified": False,
            }
        )
        actions.append(
            {
                "action_id": f"revise_{item['preview_item_id']}",
                "action": "revise_preview_item",
                "label": "再改一版",
                "target_preview_item_id": item["preview_item_id"],
                "available": True,
                "provider_called": False,
                "model_called": False,
            }
        )
        actions.append(
            {
                "action_id": f"reject_{item['preview_item_id']}",
                "action": "reject_preview_item",
                "label": "暂不采用",
                "target_preview_item_id": item["preview_item_id"],
                "available": True,
                "formal_apply_performed": False,
                "lesson_body_modified": False,
            }
        )
    return {
        "actions_id": "minimal_self_prep_page_actions_1013I_R4",
        "stage": STAGE_ID,
        "action_state_policy": {
            "current_primary_state": "accepted_to_preview_only",
            "revision_and_reject_are_alternate_paths": True,
            "action_state_not_confusing": True,
        },
        "actions": actions,
        "revert_action_present": any(action["action"] == "revert_preview_item" for action in actions),
        "formal_apply_allowed": False,
        "provider_call_allowed": False,
        "model_call_allowed": False,
    }


def build_page_fixture(
    request: dict[str, Any],
    surface: dict[str, Any],
    preview_state: dict[str, Any],
    diff_cards: list[dict[str, Any]],
    actions: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    sections = {
        "sections_id": "minimal_self_prep_page_sections_1013I_R4",
        "stage": STAGE_ID,
        "teacher_input_summary": build_teacher_input_summary(request),
        "review_cards_section": build_review_cards_section(surface),
        "preview_diff_section": build_preview_section(preview_state, diff_cards),
        "revision_queue_section": build_revision_section(preview_state),
        "rejected_items_section": build_rejected_section(preview_state),
    }
    fixture = {
        "page_fixture_id": "minimal_self_prep_page_fixture_1013I_R4",
        "stage": STAGE_ID,
        "source_request_file": "teacher_self_prep_request_1013I_R0A1.json",
        "source_review_card_surface": "teacher_review_card_surface_1013I_R2.json",
        "source_preview_chain_state": "self_prep_preview_chain_state_1013I_R3.json",
        "source_request_id": request["request_id"],
        "lesson_context": preview_state["lesson_context"],
        "agent_role": preview_state["agent_role"],
        "assistant_profile": preview_state["assistant_profile"],
        "active_space": preview_state["active_space"],
        "active_capability": preview_state["active_capability"],
        "page_mode": "fixture_only",
        "teacher_alpha_readiness": "internal_click_flow_after_R4",
        "sections": sections,
        "actions": actions,
        "boundary_flags": {
            "preview_only": True,
            "fixture_only": True,
            "provider_called": False,
            "model_called": False,
            "formal_apply_performed": False,
            "lesson_body_modified": False,
            "html_body_modified": False,
            "database_written": False,
            "memory_written": False,
            "feishu_written": False,
        },
    }
    return fixture, sections


def scan_deprecated(payload: Any) -> list[str]:
    text = json.dumps(payload, ensure_ascii=False)
    return [name for name in DEPRECATED_VISIBLE_NAMES if name in text]


def has_legacy_agent_field(payload: Any) -> bool:
    if isinstance(payload, dict):
        return "agent" in payload or any(has_legacy_agent_field(value) for value in payload.values())
    if isinstance(payload, list):
        return any(has_legacy_agent_field(item) for item in payload)
    return False


def build_result(fixture: dict[str, Any], sections: dict[str, Any], actions: dict[str, Any]) -> dict[str, Any]:
    hits = sorted(set(scan_deprecated(fixture) + scan_deprecated(sections) + scan_deprecated(actions)))
    legacy_agent = has_legacy_agent_field(fixture) or has_legacy_agent_field(sections) or has_legacy_agent_field(actions)
    boundary = {
        "minimal_page_fixture_created": True,
        "teacher_input_summary_present": bool(sections["teacher_input_summary"]),
        "review_cards_section_present": bool(sections["review_cards_section"]["cards"]),
        "preview_diff_section_present": bool(sections["preview_diff_section"]["preview_diff_cards"]),
        "revision_queue_section_present": bool(sections["revision_queue_section"]["items"]),
        "rejected_items_section_present": bool(sections["rejected_items_section"]["items"]),
        "revert_action_present": actions["revert_action_present"],
        "action_state_not_confusing": actions["action_state_policy"]["action_state_not_confusing"],
        "current_primary_state": actions["action_state_policy"]["current_primary_state"],
        "revision_and_reject_are_alternate_paths": actions["action_state_policy"]["revision_and_reject_are_alternate_paths"],
        "review_card_count": len(sections["review_cards_section"]["cards"]),
        "preview_diff_card_count": len(sections["preview_diff_section"]["preview_diff_cards"]),
        "revision_queue_count": len(sections["revision_queue_section"]["items"]),
        "rejected_items_count": len(sections["rejected_items_section"]["items"]),
        "agent_role": fixture["agent_role"],
        "assistant_profile_present": bool(fixture["assistant_profile"]),
        "active_space": fixture["active_space"],
        "active_capability": fixture["active_capability"],
        "teacher_visible_deprecated_agent_hits": hits,
        "legacy_agent_field_present": legacy_agent,
        "preview_only": True,
        "fixture_only": True,
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
    }
    final_pass = (
        boundary["minimal_page_fixture_created"]
        and boundary["teacher_input_summary_present"]
        and boundary["review_cards_section_present"]
        and boundary["preview_diff_section_present"]
        and boundary["revision_queue_section_present"]
        and boundary["rejected_items_section_present"]
        and boundary["revert_action_present"]
        and boundary["action_state_not_confusing"]
        and boundary["current_primary_state"] == "accepted_to_preview_only"
        and boundary["revision_and_reject_are_alternate_paths"]
        and boundary["review_card_count"] == 3
        and boundary["preview_diff_card_count"] == 3
        and boundary["revision_queue_count"] == 3
        and boundary["rejected_items_count"] == 3
        and boundary["agent_role"] == "unified_teacher_agent"
        and boundary["assistant_profile_present"]
        and boundary["active_space"] == "prep_room"
        and boundary["active_capability"] == "lesson_prep"
        and not boundary["teacher_visible_deprecated_agent_hits"]
        and not boundary["legacy_agent_field_present"]
        and boundary["preview_only"]
        and boundary["fixture_only"]
        and not any(
            boundary[key]
            for key in [
                "provider_called",
                "model_called",
                "formal_apply_performed",
                "lesson_body_modified",
                "html_body_modified",
                "database_written",
                "memory_written",
                "feishu_written",
                "main_project_pushed",
            ]
        )
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013I_R3_SELF_PREP_PREVIEW_CHAIN_FROM_REVIEW_CARDS",
        "final_status": "PASS_1013I_R4_MINIMAL_SELF_PREP_PAGE_FIXTURE" if final_pass else "FAIL_1013I_R4_MINIMAL_SELF_PREP_PAGE_FIXTURE",
        "next_stage": NEXT_STAGE,
        **boundary,
    }


def build_report(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R4 Minimal Self Prep Page Fixture",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Boundary: page fixture only; no provider/model, no formal apply, no lesson body/html write.",
            "",
            "## Page Sections",
            "",
            f"- teacher_input_summary_present={str(result['teacher_input_summary_present']).lower()}",
            f"- review_cards_section_present={str(result['review_cards_section_present']).lower()}",
            f"- preview_diff_section_present={str(result['preview_diff_section_present']).lower()}",
            f"- revision_queue_section_present={str(result['revision_queue_section_present']).lower()}",
            f"- rejected_items_section_present={str(result['rejected_items_section_present']).lower()}",
            f"- revert_action_present={str(result['revert_action_present']).lower()}",
            "",
            "## State Clarity",
            "",
            f"- current_primary_state={result['current_primary_state']}",
            f"- revision_and_reject_are_alternate_paths={str(result['revision_and_reject_are_alternate_paths']).lower()}",
            f"- action_state_not_confusing={str(result['action_state_not_confusing']).lower()}",
            "",
            "## Boundary Flags",
            "",
            f"- preview_only={str(result['preview_only']).lower()}",
            f"- fixture_only={str(result['fixture_only']).lower()}",
            f"- provider_called={str(result['provider_called']).lower()}",
            f"- model_called={str(result['model_called']).lower()}",
            f"- formal_apply_performed={str(result['formal_apply_performed']).lower()}",
            f"- lesson_body_modified={str(result['lesson_body_modified']).lower()}",
            f"- html_body_modified={str(result['html_body_modified']).lower()}",
            f"- database_written={str(result['database_written']).lower()}",
            f"- memory_written={str(result['memory_written']).lower()}",
            f"- feishu_written={str(result['feishu_written']).lower()}",
            "",
        ]
    )


def copy_source_delta() -> None:
    SOURCE_DELTA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA_DIR / Path(__file__).name)


def main() -> int:
    request = read_json(R0A1_DIR / "teacher_self_prep_request_1013I_R0A1.json")
    surface = read_json(R2_DIR / "teacher_review_card_surface_1013I_R2.json")
    preview_state = read_json(R3_DIR / "self_prep_preview_chain_state_1013I_R3.json")
    diff_cards = read_json(R3_DIR / "self_prep_preview_diff_cards_1013I_R3.json")
    actions = build_page_actions(preview_state)
    fixture, sections = build_page_fixture(request, surface, preview_state, diff_cards, actions)
    result = build_result(fixture, sections, actions)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "minimal_self_prep_page_fixture_1013I_R4.json", fixture)
    write_json(OUT_DIR / "minimal_self_prep_page_sections_1013I_R4.json", sections)
    write_json(OUT_DIR / "minimal_self_prep_page_actions_1013I_R4.json", actions)
    write_json(OUT_DIR / "1013I_R4_result.json", result)
    write_text(OUT_DIR / "1013I_R4_report.md", build_report(result))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
