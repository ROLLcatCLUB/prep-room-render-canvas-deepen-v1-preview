from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
SOURCE_DIR = OUTPUT_ROOT / "1013I_R1_candidate_card_seed_from_self_prep_request"
OUT_DIR = OUTPUT_ROOT / "1013I_R2_teacher_review_card_surface_from_seed"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013I_R2" / "scripts"

STAGE_ID = "1013I_R2_TEACHER_REVIEW_CARD_SURFACE_FROM_SEED"
NEXT_STAGE = "1013I_R3_SELF_PREP_PREVIEW_CHAIN_FROM_REVIEW_CARDS"
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


def readable_basis(seed_basis: list[dict[str, Any]]) -> list[dict[str, Any]]:
    labels = {
        "lesson_title": "课题",
        "class_profile_hint": "班级情况",
        "teacher_ideas": "老师想法",
        "existing_materials": "已有材料",
        "resource_preferences": "资源偏好",
        "classroom_constraints": "课堂限制",
        "preferred_depth": "备课深度",
        "active_capability": "当前能力",
    }
    return [
        {
            "source_field": item["field"],
            "teacher_label": labels.get(item["field"], item["field"]),
            "source_value": item["value"],
        }
        for item in seed_basis
    ]


def build_review_cards(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    cards = []
    for index, seed in enumerate(bundle["candidate_cards"], start=1):
        cards.append(
            {
                "review_card_id": f"review_card_{index:02d}_{seed['seed_id']}",
                "source_seed_id": seed["seed_id"],
                "source_request_id": seed["source_request_id"],
                "source_request_file": seed["source_request_file"],
                "card_order": index,
                "card_type": seed["card_type"].replace("_seed", "_review_card"),
                "target_section": seed["target_section"],
                "card_title": seed["seed_title"],
                "teacher_prompt": seed["teacher_visible_prompt"],
                "assistant_display_name": seed["assistant_profile"]["display_name"],
                "assistant_suggestion": seed["draft_seed"],
                "why_this_suggestion": readable_basis(seed["seed_basis"]),
                "risk_note": seed["risk_note"],
                "teacher_action_options": [
                    {
                        "action": "accept_to_preview",
                        "label": "采纳到预览",
                        "effect": "send_to_next_preview_chain_only",
                        "formal_apply_performed": False,
                        "lesson_body_modified": False,
                    },
                    {
                        "action": "revise_seed",
                        "label": "再改一版",
                        "effect": "return_to_seed_revision_queue",
                        "formal_apply_performed": False,
                        "lesson_body_modified": False,
                    },
                    {
                        "action": "reject_seed",
                        "label": "暂不采用",
                        "effect": "mark_card_rejected_for_this_preview",
                        "formal_apply_performed": False,
                        "lesson_body_modified": False,
                    },
                ],
                "review_state": {
                    "status": "pending_teacher_review",
                    "accepted_to_preview": False,
                    "rejected": False,
                    "revision_requested": False,
                    "teacher_review_required": True,
                },
                "boundary_flags": {
                    "review_surface_only": True,
                    "provider_called": False,
                    "model_called": False,
                    "formal_apply_performed": False,
                    "lesson_body_modified": False,
                    "html_body_modified": False,
                    "database_written": False,
                    "memory_written": False,
                    "feishu_written": False,
                },
                "agent_role": seed["agent_role"],
                "assistant_profile": seed["assistant_profile"],
                "active_space": seed["active_space"],
                "active_capability": seed["active_capability"],
            }
        )
    return cards


def build_surface(bundle: dict[str, Any], cards: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "surface_id": "teacher_review_card_surface_1013I_R2",
        "stage": STAGE_ID,
        "source_bundle_id": bundle["bundle_id"],
        "source_request_file": bundle["source_request_file"],
        "source_request_id": bundle["source_request_id"],
        "original_request_id": bundle["original_request_id"],
        "request_id_trace_aligned": bundle["request_id_trace_aligned"],
        "lesson_context": bundle["lesson_context"],
        "agent_role": bundle["agent_role"],
        "assistant_profile": bundle["assistant_profile"],
        "active_space": bundle["active_space"],
        "active_capability": bundle["active_capability"],
        "review_cards": cards,
        "review_card_count": len(cards),
        "surface_state": "pending_teacher_review",
        "teacher_review_required": True,
        "preview_apply_allowed_next_stage_only": True,
        "formal_apply_allowed": False,
    }


def build_actions(cards: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "actions_id": "review_card_actions_1013I_R2",
        "stage": STAGE_ID,
        "available_actions": ["accept_to_preview", "revise_seed", "reject_seed"],
        "action_semantics": {
            "accept_to_preview": {
                "label": "采纳到预览",
                "allowed_now": False,
                "next_stage": NEXT_STAGE,
                "description": "R2 only exposes the action; R3 may simulate preview-chain state.",
            },
            "revise_seed": {
                "label": "再改一版",
                "allowed_now": True,
                "description": "Mark the card for seed revision without model/provider call.",
            },
            "reject_seed": {
                "label": "暂不采用",
                "allowed_now": True,
                "description": "Mark the card rejected for the current preview path.",
            },
        },
        "card_action_bindings": [
            {
                "review_card_id": card["review_card_id"],
                "source_seed_id": card["source_seed_id"],
                "actions": [action["action"] for action in card["teacher_action_options"]],
            }
            for card in cards
        ],
        "formal_apply_allowed": False,
        "lesson_body_write_allowed": False,
    }


def build_trace(bundle: dict[str, Any], cards: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "trace_id": "teacher_review_card_surface_trace_1013I_R2",
        "stage": STAGE_ID,
        "source_bundle_id": bundle["bundle_id"],
        "source_request_id": bundle["source_request_id"],
        "review_card_count": len(cards),
        "seed_to_card_mapping": [
            {"seed_id": card["source_seed_id"], "review_card_id": card["review_card_id"]}
            for card in cards
        ],
        "provider_called": False,
        "model_called": False,
        "formal_apply_performed": False,
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


def build_result(surface: dict[str, Any], actions: dict[str, Any], trace: dict[str, Any]) -> dict[str, Any]:
    hits = sorted(set(scan_deprecated(surface) + scan_deprecated(actions) + scan_deprecated(trace)))
    legacy_agent = has_legacy_agent_field(surface) or has_legacy_agent_field(actions) or has_legacy_agent_field(trace)
    boundary = {
        "teacher_review_card_surface_created": True,
        "review_card_actions_created": True,
        "review_card_trace_created": True,
        "review_card_count": surface["review_card_count"],
        "source_bundle_id": surface["source_bundle_id"],
        "source_request_file": surface["source_request_file"],
        "source_request_id": surface["source_request_id"],
        "request_id_trace_aligned": surface["request_id_trace_aligned"],
        "agent_role": surface["agent_role"],
        "assistant_profile_present": bool(surface["assistant_profile"]),
        "active_space": surface["active_space"],
        "active_capability": surface["active_capability"],
        "teacher_action_options_present": True,
        "accept_to_preview_option_present": True,
        "revise_option_present": True,
        "reject_option_present": True,
        "accept_to_preview_executed": False,
        "teacher_visible_deprecated_agent_hits": hits,
        "legacy_agent_field_present": legacy_agent,
        "review_surface_only": True,
        "teacher_review_required": True,
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
        boundary["teacher_review_card_surface_created"]
        and boundary["review_card_actions_created"]
        and boundary["review_card_trace_created"]
        and boundary["review_card_count"] == 3
        and boundary["source_request_file"] == "teacher_self_prep_request_1013I_R0A1.json"
        and boundary["source_request_id"] == "teacher_self_prep_request_1013I_R0A"
        and boundary["request_id_trace_aligned"]
        and boundary["agent_role"] == "unified_teacher_agent"
        and boundary["assistant_profile_present"]
        and boundary["active_space"] == "prep_room"
        and boundary["active_capability"] == "lesson_prep"
        and boundary["teacher_action_options_present"]
        and boundary["accept_to_preview_option_present"]
        and boundary["revise_option_present"]
        and boundary["reject_option_present"]
        and not boundary["accept_to_preview_executed"]
        and not boundary["teacher_visible_deprecated_agent_hits"]
        and not boundary["legacy_agent_field_present"]
        and boundary["review_surface_only"]
        and boundary["teacher_review_required"]
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
        "inherits_from": "1013I_R1_CANDIDATE_CARD_SEED_FROM_SELF_PREP_REQUEST",
        "final_status": "PASS_1013I_R2_TEACHER_REVIEW_CARD_SURFACE_FROM_SEED" if final_pass else "FAIL_1013I_R2_TEACHER_REVIEW_CARD_SURFACE_FROM_SEED",
        "next_stage": NEXT_STAGE,
        **boundary,
    }


def build_report(result: dict[str, Any], surface: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 1013I R2 Teacher Review Card Surface From Seed",
            "",
            f"- FINAL_STATUS: `{result['final_status']}`",
            f"- NEXT_STAGE: `{result['next_stage']}`",
            "- Boundary: teacher review surface only; action execution and preview-chain state are deferred to R3.",
            "",
            "## Cards",
            "",
            f"- review_card_count={result['review_card_count']}",
            f"- review_card_ids={', '.join(card['review_card_id'] for card in surface['review_cards'])}",
            "",
            "## Required UI Data",
            "",
            "- Each card includes title, source teacher input, assistant suggestion, why-this-suggestion, risk note, and teacher action options.",
            f"- accept_to_preview_option_present={str(result['accept_to_preview_option_present']).lower()}",
            f"- revise_option_present={str(result['revise_option_present']).lower()}",
            f"- reject_option_present={str(result['reject_option_present']).lower()}",
            "",
            "## Boundary Flags",
            "",
            f"- accept_to_preview_executed={str(result['accept_to_preview_executed']).lower()}",
            f"- review_surface_only={str(result['review_surface_only']).lower()}",
            f"- teacher_review_required={str(result['teacher_review_required']).lower()}",
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
    bundle = read_json(SOURCE_DIR / "candidate_card_seed_bundle_1013I_R1.json")
    cards = build_review_cards(bundle)
    surface = build_surface(bundle, cards)
    actions = build_actions(cards)
    trace = build_trace(bundle, cards)
    result = build_result(surface, actions, trace)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "teacher_review_card_surface_1013I_R2.json", surface)
    write_json(OUT_DIR / "review_card_actions_1013I_R2.json", actions)
    write_json(OUT_DIR / "teacher_review_card_surface_trace_1013I_R2.json", trace)
    write_json(OUT_DIR / "1013I_R2_result.json", result)
    write_text(OUT_DIR / "1013I_R2_report.md", build_report(result, surface))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
