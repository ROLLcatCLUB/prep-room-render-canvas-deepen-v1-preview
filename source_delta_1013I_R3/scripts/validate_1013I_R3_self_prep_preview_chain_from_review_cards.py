from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
SOURCE_DIR = OUTPUT_ROOT / "1013I_R2_teacher_review_card_surface_from_seed"
OUT_DIR = OUTPUT_ROOT / "1013I_R3_self_prep_preview_chain_from_review_cards"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013I_R3" / "scripts"

STAGE_ID = "1013I_R3_SELF_PREP_PREVIEW_CHAIN_FROM_REVIEW_CARDS"
NEXT_STAGE = "1013I_R4_MINIMAL_SELF_PREP_PAGE_FIXTURE"
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


def build_preview_state(surface: dict[str, Any]) -> dict[str, Any]:
    accepted_items = []
    revision_queue = []
    rejected_items = []
    for card in surface["review_cards"]:
        base = {
            "review_card_id": card["review_card_id"],
            "source_seed_id": card["source_seed_id"],
            "source_request_id": card["source_request_id"],
            "target_section": card["target_section"],
            "card_title": card["card_title"],
            "assistant_suggestion": card["assistant_suggestion"],
            "risk_note": card["risk_note"],
            "agent_role": card["agent_role"],
            "assistant_profile": card["assistant_profile"],
            "active_space": card["active_space"],
            "active_capability": card["active_capability"],
        }
        accepted_items.append(
            {
                **base,
                "preview_item_id": f"preview_item_{card['source_seed_id']}",
                "preview_status": "accepted_to_preview_only",
                "preview_text": card["assistant_suggestion"],
                "can_revert": True,
                "can_revise": True,
                "can_formal_apply": False,
                "lesson_body_modified": False,
                "formal_apply_performed": False,
            }
        )
        revision_queue.append(
            {
                **base,
                "revision_item_id": f"revision_item_{card['source_seed_id']}",
                "revision_status": "revision_requested_simulated",
                "revision_reason": "Teacher may request a clearer or lighter version before preview.",
                "provider_called": False,
                "model_called": False,
                "lesson_body_modified": False,
            }
        )
        rejected_items.append(
            {
                **base,
                "rejected_item_id": f"rejected_item_{card['source_seed_id']}",
                "reject_status": "rejected_for_current_preview_path_simulated",
                "can_restore": True,
                "lesson_body_modified": False,
                "formal_apply_performed": False,
            }
        )
    return {
        "preview_chain_state_id": "self_prep_preview_chain_state_1013I_R3",
        "stage": STAGE_ID,
        "source_review_card_surface": "teacher_review_card_surface_1013I_R2.json",
        "source_surface_id": surface["surface_id"],
        "source_request_id": surface["source_request_id"],
        "lesson_context": surface["lesson_context"],
        "agent_role": surface["agent_role"],
        "assistant_profile": surface["assistant_profile"],
        "active_space": surface["active_space"],
        "active_capability": surface["active_capability"],
        "preview_only": True,
        "accepted_preview_items": accepted_items,
        "revision_queue": revision_queue,
        "rejected_items": rejected_items,
        "revert_available": True,
        "formal_apply_allowed": False,
        "lesson_body_write_allowed": False,
    }


def build_diff_cards(preview_state: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "diff_card_id": f"preview_diff_{item['source_seed_id']}",
            "review_card_id": item["review_card_id"],
            "target_section": item["target_section"],
            "before_state": "teacher_review_card_pending",
            "after_state": "preview_only_candidate_visible",
            "after_preview_text": item["preview_text"],
            "display_badge": "预览中",
            "can_revert": True,
            "formal_apply_performed": False,
            "lesson_body_modified": False,
        }
        for item in preview_state["accepted_preview_items"]
    ]


def build_action_trace(surface: dict[str, Any]) -> list[dict[str, Any]]:
    trace = []
    for card in surface["review_cards"]:
        for action in ["accept_to_preview", "revise_seed", "reject_seed"]:
            trace.append(
                {
                    "trace_id": f"trace_{action}_{card['source_seed_id']}",
                    "stage": STAGE_ID,
                    "review_card_id": card["review_card_id"],
                    "source_seed_id": card["source_seed_id"],
                    "action": action,
                    "simulated": True,
                    "result_state": {
                        "accept_to_preview": "accepted_to_preview_only",
                        "revise_seed": "revision_requested_simulated",
                        "reject_seed": "rejected_for_current_preview_path_simulated",
                    }[action],
                    "provider_called": False,
                    "model_called": False,
                    "formal_apply_performed": False,
                    "lesson_body_modified": False,
                    "html_body_modified": False,
                    "database_written": False,
                    "memory_written": False,
                    "feishu_written": False,
                }
            )
    return trace


def build_bridge(preview_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "bridge_id": "self_prep_preview_chain_to_minimal_page_fixture_bridge_1013I_R3",
        "stage": STAGE_ID,
        "source_preview_chain_state_id": preview_state["preview_chain_state_id"],
        "next_stage": NEXT_STAGE,
        "page_fixture_ready": True,
        "required_page_fixture_parts": [
            "teacher input summary",
            "review cards",
            "preview diff cards",
            "revision queue",
            "rejected items",
            "revert action",
        ],
        "formal_apply_allowed": False,
        "provider_call_allowed": False,
        "model_call_allowed": False,
    }


def scan_deprecated(payload: Any) -> list[str]:
    text = json.dumps(payload, ensure_ascii=False)
    return [name for name in DEPRECATED_VISIBLE_NAMES if name in text]


def has_legacy_agent_field(payload: Any) -> bool:
    if isinstance(payload, dict):
        return "agent" in payload or any(has_legacy_agent_field(value) for value in payload.values())
    if isinstance(payload, list):
        return any(has_legacy_agent_field(item) for item in payload)
    return False


def build_result(
    preview_state: dict[str, Any],
    diff_cards: list[dict[str, Any]],
    action_trace: list[dict[str, Any]],
    bridge: dict[str, Any],
) -> dict[str, Any]:
    hits = sorted(
        set(
            scan_deprecated(preview_state)
            + scan_deprecated(diff_cards)
            + scan_deprecated(action_trace)
            + scan_deprecated(bridge)
        )
    )
    legacy_agent = (
        has_legacy_agent_field(preview_state)
        or has_legacy_agent_field(diff_cards)
        or has_legacy_agent_field(action_trace)
        or has_legacy_agent_field(bridge)
    )
    boundary = {
        "preview_chain_state_created": True,
        "source_review_card_surface": preview_state["source_review_card_surface"],
        "review_cards_loaded": len(preview_state["accepted_preview_items"]),
        "accepted_preview_items_count": len(preview_state["accepted_preview_items"]),
        "revision_queue_count": len(preview_state["revision_queue"]),
        "rejected_items_count": len(preview_state["rejected_items"]),
        "preview_diff_cards_created": bool(diff_cards),
        "preview_diff_card_count": len(diff_cards),
        "action_trace_created": bool(action_trace),
        "action_trace_count": len(action_trace),
        "accept_to_preview_simulated": any(item["action"] == "accept_to_preview" for item in action_trace),
        "revise_seed_simulated": any(item["action"] == "revise_seed" for item in action_trace),
        "reject_seed_simulated": any(item["action"] == "reject_seed" for item in action_trace),
        "revert_available": preview_state["revert_available"],
        "bridge_to_minimal_page_fixture_created": bool(bridge),
        "agent_role": preview_state["agent_role"],
        "assistant_profile_present": bool(preview_state["assistant_profile"]),
        "active_space": preview_state["active_space"],
        "active_capability": preview_state["active_capability"],
        "teacher_visible_deprecated_agent_hits": hits,
        "legacy_agent_field_present": legacy_agent,
        "preview_only": True,
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
        boundary["preview_chain_state_created"]
        and boundary["source_review_card_surface"] == "teacher_review_card_surface_1013I_R2.json"
        and boundary["review_cards_loaded"] == 3
        and boundary["accepted_preview_items_count"] == 3
        and boundary["revision_queue_count"] == 3
        and boundary["rejected_items_count"] == 3
        and boundary["preview_diff_cards_created"]
        and boundary["preview_diff_card_count"] == 3
        and boundary["action_trace_created"]
        and boundary["action_trace_count"] == 9
        and boundary["accept_to_preview_simulated"]
        and boundary["revise_seed_simulated"]
        and boundary["reject_seed_simulated"]
        and boundary["revert_available"]
        and boundary["bridge_to_minimal_page_fixture_created"]
        and boundary["agent_role"] == "unified_teacher_agent"
        and boundary["assistant_profile_present"]
        and boundary["active_space"] == "prep_room"
        and boundary["active_capability"] == "lesson_prep"
        and not boundary["teacher_visible_deprecated_agent_hits"]
        and not boundary["legacy_agent_field_present"]
        and boundary["preview_only"]
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
        "inherits_from": "1013I_R2_TEACHER_REVIEW_CARD_SURFACE_FROM_SEED",
        "final_status": "PASS_1013I_R3_SELF_PREP_PREVIEW_CHAIN_FROM_REVIEW_CARDS" if final_pass else "FAIL_1013I_R3_SELF_PREP_PREVIEW_CHAIN_FROM_REVIEW_CARDS",
        "next_stage": NEXT_STAGE,
        **boundary,
    }


def build_report(result: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R3 Self Prep Preview Chain From Review Cards",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Boundary: preview-chain simulation only; no formal apply, no lesson body/html write, no provider/model call.",
            "",
            "## Preview Chain",
            "",
            f"- preview_chain_state_created={str(result['preview_chain_state_created']).lower()}",
            f"- review_cards_loaded={result['review_cards_loaded']}",
            f"- accepted_preview_items_count={result['accepted_preview_items_count']}",
            f"- revision_queue_count={result['revision_queue_count']}",
            f"- rejected_items_count={result['rejected_items_count']}",
            f"- action_trace_count={result['action_trace_count']}",
            f"- revert_available={str(result['revert_available']).lower()}",
            "",
            "## Simulated Actions",
            "",
            f"- accept_to_preview_simulated={str(result['accept_to_preview_simulated']).lower()}",
            f"- revise_seed_simulated={str(result['revise_seed_simulated']).lower()}",
            f"- reject_seed_simulated={str(result['reject_seed_simulated']).lower()}",
            "",
            "## Boundary Flags",
            "",
            f"- preview_only={str(result['preview_only']).lower()}",
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
    surface = read_json(SOURCE_DIR / "teacher_review_card_surface_1013I_R2.json")
    preview_state = build_preview_state(surface)
    diff_cards = build_diff_cards(preview_state)
    action_trace = build_action_trace(surface)
    bridge = build_bridge(preview_state)
    result = build_result(preview_state, diff_cards, action_trace, bridge)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "self_prep_preview_chain_state_1013I_R3.json", preview_state)
    write_json(OUT_DIR / "self_prep_preview_diff_cards_1013I_R3.json", diff_cards)
    write_json(OUT_DIR / "self_prep_review_card_action_trace_1013I_R3.json", action_trace)
    write_json(OUT_DIR / "self_prep_preview_chain_to_minimal_page_fixture_bridge_1013I_R3.json", bridge)
    write_json(OUT_DIR / "1013I_R3_result.json", result)
    write_text(OUT_DIR / "1013I_R3_report.md", build_report(result))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
