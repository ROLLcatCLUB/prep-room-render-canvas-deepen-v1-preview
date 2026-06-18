from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "1013I_R6_TEACHER_SELF_PREP_RENDER_SURFACE_ALPHA"
NEXT_STAGE = "1013I_R7_TEACHER_SELF_PREP_RENDER_SURFACE_VISUAL_REVIEW"
DEPRECATED_VISIBLE_NAMES = ["小备", "小评", "小管", "小美"]
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\\s*[:=]\\s*['\\\"][A-Za-z0-9_\\-]{20,}"),
    re.compile(r"(?i)app[_-]?secret\\s*[:=]\\s*['\\\"][A-Za-z0-9_\\-]{20,}"),
    re.compile(r"(?i)tenant[_-]?access[_-]?token\\s*[:=]\\s*['\\\"][A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)bearer\\s+[A-Za-z0-9_.-]{20,}"),
    re.compile(r"(?i)cookie\\s*[:=]\\s*['\\\"][^'\\\"]{20,}"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_output_root(root: Path) -> Path:
    nested_output_root = root / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
    if nested_output_root.exists():
        return nested_output_root
    review_repo_root_marker = root / "1013I_R4_minimal_self_prep_page_fixture"
    if review_repo_root_marker.exists():
        return root
    raise FileNotFoundError(
        "Cannot locate PREP_ROOM_RENDER_CANVAS_DEEPEN_V1 outputs. "
        "Run from xiaobei-core root or from the GitHub review repo root."
    )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_inputs(output_root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    r4_dir = output_root / "1013I_R4_minimal_self_prep_page_fixture"
    r5_dir = output_root / "1013I_R5_teacher_self_prep_alpha_smoke"
    fixture = read_json(r4_dir / "minimal_self_prep_page_fixture_1013I_R4.json")
    actions = read_json(r4_dir / "minimal_self_prep_page_actions_1013I_R4.json")
    r5_result = read_json(r5_dir / "1013I_R5_result.json")
    r5_trace = read_json(r5_dir / "self_prep_alpha_smoke_trace_1013I_R5.json")
    r5_snapshot = read_json(r5_dir / "self_prep_alpha_smoke_state_snapshot_1013I_R5.json")
    return fixture, actions, r5_result, r5_trace, r5_snapshot


def count_actions(actions: dict[str, Any], action_name: str) -> int:
    return sum(1 for action in actions.get("actions", []) if action.get("action") == action_name)


def compact_reasons(card: dict[str, Any]) -> list[str]:
    reasons = []
    for reason in card.get("why_this_suggestion", []):
        label = reason.get("teacher_label", "依据")
        value = reason.get("source_value")
        if isinstance(value, list):
            value = "、".join(str(item) for item in value)
        reasons.append(f"{label}: {value}")
    return reasons[:3]


def action_labels_for_preview_item(actions: dict[str, Any], preview_item_id: str) -> list[dict[str, Any]]:
    results = []
    for action in actions.get("actions", []):
        if action.get("target_preview_item_id") != preview_item_id:
            continue
        results.append(
            {
                "action_id": action["action_id"],
                "action": action["action"],
                "label": action["label"],
                "available": bool(action.get("available", False)),
                "fixture_only": True,
                "provider_called": bool(action.get("provider_called", False)),
                "model_called": bool(action.get("model_called", False)),
                "formal_apply_performed": bool(action.get("formal_apply_performed", False)),
                "lesson_body_modified": bool(action.get("lesson_body_modified", False)),
            }
        )
    return results


def build_render_surface(fixture: dict[str, Any], actions: dict[str, Any], r5_snapshot: dict[str, Any]) -> dict[str, Any]:
    sections = fixture["sections"]
    summary = sections["teacher_input_summary"]
    review_cards = sections["review_cards_section"]["cards"]
    preview_items = sections["preview_diff_section"]["accepted_preview_items"]
    diff_cards = sections["preview_diff_section"]["preview_diff_cards"]
    revision_items = sections["revision_queue_section"]["items"]
    rejected_items = sections["rejected_items_section"]["items"]
    action_policy = actions["action_state_policy"]
    diff_by_review_card = {card["review_card_id"]: card for card in diff_cards}
    return {
        "render_surface_id": "teacher_self_prep_render_surface_alpha_1013I_R6",
        "stage": STAGE_ID,
        "source_page_fixture": "minimal_self_prep_page_fixture_1013I_R4.json",
        "source_alpha_smoke_snapshot": "self_prep_alpha_smoke_state_snapshot_1013I_R5.json",
        "render_surface_alpha_only": True,
        "page_title_section": {
            "current_space_label": "备课室",
            "current_capability_label": "自助备课",
            "assistant_display_name": fixture["assistant_profile"]["display_name"],
            "status_badge": "预览中 / 未正式应用",
            "primary_state": action_policy["current_primary_state"],
        },
        "teacher_input_summary_section": {
            "title": "小教理解的备课需求",
            "intent_summary": f"{summary['grade_level']} {summary['subject']}《{summary['lesson_title']}》，{summary['lesson_count']}课时，{summary['unit_or_textbook_context']}。",
            "subject": summary["subject"],
            "grade_level": summary["grade_level"],
            "lesson_title": summary["lesson_title"],
            "target_output": "生成可审阅的备课预览候选",
            "class_profile_hint": summary["class_profile_hint"],
            "teacher_ideas": summary["teacher_ideas"],
            "existing_materials": summary["existing_materials"],
            "classroom_constraints": summary["classroom_constraints"],
            "information_sufficiency_hint": "信息足够生成预览候选；缺少细化材料时只能继续停留在预览态。",
            "missing_information_hint": "可后续补充班级作品样例、教材页图片、评价标准；本轮不自动追问模型。",
        },
        "review_cards_section": {
            "title": "3 个建议先给老师看",
            "state_hint": "当前主状态已经采纳到预览；再改和暂不采用只作为旁路动作保留。",
            "cards": [
                {
                    "review_card_id": card["review_card_id"],
                    "display_order": card["card_order"],
                    "title": card["card_title"],
                    "target_section": card["target_section"],
                    "assistant_suggestion": card["assistant_suggestion"],
                    "reason_summary": compact_reasons(card),
                    "risk_note": card["risk_note"],
                    "current_status": "accepted_to_preview_only",
                    "status_badge": "已进入预览",
                    "not_current_states": ["revision_requested_simulated", "rejected_for_current_preview_path_simulated"],
                    "state_conflict": False,
                }
                for card in review_cards
            ],
        },
        "preview_diff_section": {
            "title": "当前预览中会出现的调整",
            "state_hint": "仅预览，未写入备课正文。",
            "current_preview_mode": sections["preview_diff_section"]["current_preview_mode"],
            "items": [
                {
                    "preview_item_id": item["preview_item_id"],
                    "review_card_id": item["review_card_id"],
                    "target_section": item["target_section"],
                    "status_badge": diff_by_review_card[item["review_card_id"]]["display_badge"],
                    "preview_text": item["preview_text"],
                    "before_state": diff_by_review_card[item["review_card_id"]]["before_state"],
                    "after_state": diff_by_review_card[item["review_card_id"]]["after_state"],
                    "preview_only_note": "仅预览，未写入备课正文",
                    "can_revert": item["can_revert"],
                    "can_revise": item["can_revise"],
                    "can_formal_apply": item["can_formal_apply"],
                    "lesson_body_modified": False,
                    "formal_apply_performed": False,
                }
                for item in preview_items
            ],
        },
        "action_area": {
            "title": "可操作但不正式写入",
            "actions_by_preview_item": [
                {
                    "preview_item_id": item["preview_item_id"],
                    "target_section": item["target_section"],
                    "actions": action_labels_for_preview_item(actions, item["preview_item_id"]),
                }
                for item in preview_items
            ],
        },
        "revision_queue_section": {
            "title": "再改一版",
            "visual_weight": "secondary",
            "alternate_path": True,
            "state_hint": "这是 smoke 验证过的旁路状态，不是当前主状态。",
            "items": [
                {
                    "revision_item_id": item["revision_item_id"],
                    "review_card_id": item["review_card_id"],
                    "title": item["card_title"],
                    "status": item["revision_status"],
                    "reason": item["revision_reason"],
                    "provider_called": False,
                    "model_called": False,
                }
                for item in revision_items
            ],
        },
        "rejected_items_section": {
            "title": "暂不采用",
            "visual_weight": "secondary",
            "alternate_path": True,
            "state_hint": "这是 smoke 验证过的旁路状态，不是当前主状态。",
            "items": [
                {
                    "rejected_item_id": item["rejected_item_id"],
                    "review_card_id": item["review_card_id"],
                    "title": item["card_title"],
                    "status": item["reject_status"],
                    "can_restore": item["can_restore"],
                    "lesson_body_modified": False,
                    "formal_apply_performed": False,
                }
                for item in rejected_items
            ],
        },
        "boundary_notice_section": {
            "title": "本轮边界",
            "preview_only": True,
            "fixture_only": True,
            "render_surface_alpha_only": True,
            "formal_apply_allowed": False,
            "provider_model_call_allowed": False,
            "provider_called": False,
            "model_called": False,
            "formal_apply_performed": False,
            "lesson_body_modified": False,
            "html_body_modified": False,
            "database_written": False,
            "memory_written": False,
            "feishu_written": False,
            "official_export_created": False,
            "official_archive_created": False,
            "main_project_pushed": False,
        },
        "agent_role": fixture["agent_role"],
        "assistant_profile": fixture["assistant_profile"],
        "active_space": fixture["active_space"],
        "active_capability": fixture["active_capability"],
        "current_primary_state": r5_snapshot["current_primary_state"],
        "revision_and_reject_are_alternate_paths": r5_snapshot["revision_and_reject_are_alternate_paths"],
        "action_state_not_confusing": r5_snapshot["action_state_not_confusing"],
    }


def scan_deprecated(payload: Any) -> list[str]:
    text = json.dumps(payload, ensure_ascii=False)
    return [name for name in DEPRECATED_VISIBLE_NAMES if name in text]


def scan_secrets(payload: Any) -> list[str]:
    text = json.dumps(payload, ensure_ascii=False)
    return [pattern.pattern for pattern in SECRET_PATTERNS if pattern.search(text)]


def build_snapshot(surface: dict[str, Any], actions: dict[str, Any]) -> dict[str, Any]:
    return {
        "snapshot_id": "teacher_self_prep_render_surface_snapshot_1013I_R6",
        "stage": STAGE_ID,
        "render_surface_id": surface["render_surface_id"],
        "page_title_section_present": bool(surface.get("page_title_section")),
        "teacher_input_summary_section_present": bool(surface.get("teacher_input_summary_section")),
        "review_cards_section_present": bool(surface.get("review_cards_section")),
        "review_card_count": len(surface["review_cards_section"]["cards"]),
        "preview_diff_section_present": bool(surface.get("preview_diff_section")),
        "preview_diff_card_count": len(surface["preview_diff_section"]["items"]),
        "revision_queue_section_present": bool(surface.get("revision_queue_section")),
        "revision_queue_count": len(surface["revision_queue_section"]["items"]),
        "rejected_items_section_present": bool(surface.get("rejected_items_section")),
        "rejected_items_count": len(surface["rejected_items_section"]["items"]),
        "action_area_present": bool(surface.get("action_area")),
        "revert_action_count": count_actions(actions, "revert_preview_item"),
        "revise_action_count": count_actions(actions, "revise_preview_item"),
        "reject_action_count": count_actions(actions, "reject_preview_item"),
        "current_primary_state": surface["current_primary_state"],
        "revision_and_reject_are_alternate_paths": surface["revision_and_reject_are_alternate_paths"],
        "action_state_not_confusing": surface["action_state_not_confusing"],
        "review_card_state_conflict_count": sum(1 for card in surface["review_cards_section"]["cards"] if card["state_conflict"]),
        "alternate_paths_visually_secondary": surface["revision_queue_section"]["visual_weight"] == "secondary"
        and surface["rejected_items_section"]["visual_weight"] == "secondary",
        "render_surface_alpha_only": surface["render_surface_alpha_only"],
        "preview_only": surface["boundary_notice_section"]["preview_only"],
        "fixture_only": surface["boundary_notice_section"]["fixture_only"],
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "official_export_created": False,
        "official_archive_created": False,
        "main_project_pushed": False,
        "agent_role": surface["agent_role"],
        "assistant_profile_present": bool(surface["assistant_profile"]),
        "assistant_profile_display_name": surface["assistant_profile"].get("display_name"),
        "active_space": surface["active_space"],
        "active_capability": surface["active_capability"],
        "teacher_visible_deprecated_agent_hits": scan_deprecated(surface),
        "secret_scan_hits": scan_secrets(surface),
    }


def build_result(r5_result: dict[str, Any], r5_trace: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    boundary_false_keys = [
        "provider_called",
        "model_called",
        "formal_apply_performed",
        "lesson_body_modified",
        "html_body_modified",
        "database_written",
        "memory_written",
        "feishu_written",
        "official_export_created",
        "official_archive_created",
        "main_project_pushed",
    ]
    final_pass = (
        r5_result["final_status"] == "PASS_1013I_R5_TEACHER_SELF_PREP_ALPHA_SMOKE"
        and all(step.get("passed") for step in r5_trace["steps"])
        and snapshot["teacher_input_summary_section_present"]
        and snapshot["review_cards_section_present"]
        and snapshot["review_card_count"] == 3
        and snapshot["preview_diff_section_present"]
        and snapshot["preview_diff_card_count"] == 3
        and snapshot["revision_queue_section_present"]
        and snapshot["revision_queue_count"] == 3
        and snapshot["rejected_items_section_present"]
        and snapshot["rejected_items_count"] == 3
        and snapshot["action_area_present"]
        and snapshot["revert_action_count"] == 3
        and snapshot["revise_action_count"] == 3
        and snapshot["reject_action_count"] == 3
        and snapshot["current_primary_state"] == "accepted_to_preview_only"
        and snapshot["revision_and_reject_are_alternate_paths"]
        and snapshot["action_state_not_confusing"]
        and snapshot["review_card_state_conflict_count"] == 0
        and snapshot["alternate_paths_visually_secondary"]
        and snapshot["render_surface_alpha_only"]
        and snapshot["preview_only"]
        and snapshot["fixture_only"]
        and snapshot["agent_role"] == "unified_teacher_agent"
        and snapshot["assistant_profile_present"]
        and snapshot["assistant_profile_display_name"] == "小教"
        and snapshot["active_space"] == "prep_room"
        and snapshot["active_capability"] == "lesson_prep"
        and not snapshot["teacher_visible_deprecated_agent_hits"]
        and not snapshot["secret_scan_hits"]
        and not any(snapshot[key] for key in boundary_false_keys)
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013I_R5_TEACHER_SELF_PREP_ALPHA_SMOKE",
        "final_status": f"PASS_{STAGE_ID}" if final_pass else f"FAIL_{STAGE_ID}",
        "next_stage": NEXT_STAGE,
        **snapshot,
        "formal_apply_allowed": False,
        "provider_model_call_allowed": False,
    }


def build_report(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R6 Teacher Self Prep Render Surface Alpha",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Scope: fixture-only / preview-only render surface alpha.",
            "",
            "## Render Surface",
            "",
            f"- teacher_input_summary_section_present={str(result['teacher_input_summary_section_present']).lower()}",
            f"- review_card_count={result['review_card_count']}",
            f"- preview_diff_card_count={result['preview_diff_card_count']}",
            f"- revision_queue_count={result['revision_queue_count']}",
            f"- rejected_items_count={result['rejected_items_count']}",
            f"- action_area_present={str(result['action_area_present']).lower()}",
            f"- current_primary_state={result['current_primary_state']}",
            f"- action_state_not_confusing={str(result['action_state_not_confusing']).lower()}",
            "",
            "## Teacher-Facing State",
            "",
            "- Current primary state is accepted-to-preview-only.",
            "- Revision and rejected items are visually secondary alternate paths.",
            "- The surface is organized as title, input summary, review cards, preview diffs, actions, alternate paths, and boundary notice.",
            "",
            "## Boundary",
            "",
            f"- render_surface_alpha_only={str(result['render_surface_alpha_only']).lower()}",
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
            f"- official_export_created={str(result['official_export_created']).lower()}",
            f"- official_archive_created={str(result['official_archive_created']).lower()}",
            "",
        ]
    )


def copy_source_delta(root: Path, output_root: Path) -> None:
    source_delta_dir = output_root / "source_delta_1013I_R6" / "scripts"
    source_delta_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "scripts" / Path(__file__).name, source_delta_dir / Path(__file__).name)


def run(root: Path) -> int:
    output_root = resolve_output_root(root)
    out_dir = output_root / "1013I_R6_teacher_self_prep_render_surface_alpha"
    fixture, actions, r5_result, r5_trace, r5_snapshot = load_inputs(output_root)
    surface = build_render_surface(fixture, actions, r5_snapshot)
    snapshot = build_snapshot(surface, actions)
    result = build_result(r5_result, r5_trace, snapshot)

    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "teacher_self_prep_render_surface_alpha_1013I_R6.json", surface)
    write_json(out_dir / "teacher_self_prep_render_surface_snapshot_1013I_R6.json", snapshot)
    write_json(out_dir / "1013I_R6_result.json", result)
    write_text(out_dir / "1013I_R6_report.md", build_report(result))
    copy_source_delta(root, output_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=None)
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else repo_root_from_script()
    return run(root)


if __name__ == "__main__":
    raise SystemExit(main())
