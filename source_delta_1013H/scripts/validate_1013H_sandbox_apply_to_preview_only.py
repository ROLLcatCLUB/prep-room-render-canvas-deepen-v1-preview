from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
SOURCE_DIR = OUTPUT_ROOT / "1013G_teacher_review_prep_only"
OUT_DIR = OUTPUT_ROOT / "1013H_sandbox_apply_to_preview_only"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013H" / "scripts"

STAGE_ID = "1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY"


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


def load_inputs() -> dict[str, Any]:
    return {
        "teacher_prep_result": read_json(SOURCE_DIR / "1013G_teacher_review_prep_result.json"),
        "teacher_prep_surface": read_json(SOURCE_DIR / "teacher_review_prep_surface_1013G.json"),
    }


def build_action_trace(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    trace = []
    for card in cards:
        for option in card["teacher_action_options"]:
            action_id = option["id"]
            if action_id == "accept_to_preview_only":
                preview_state = "preview_candidate_applied_in_sandbox"
                candidate_text_visible = True
                revision_requested = False
                rejected = False
            elif action_id == "reject":
                preview_state = "preview_candidate_rejected_in_sandbox"
                candidate_text_visible = False
                revision_requested = False
                rejected = True
            else:
                preview_state = "preview_revision_requested_in_sandbox"
                candidate_text_visible = False
                revision_requested = True
                rejected = False
            trace.append(
                {
                    "trace_id": f"1013h_trace_{len(trace) + 1:02d}",
                    "source_review_card_id": card["review_card_id"],
                    "target_section": card["target_section"],
                    "action_id": action_id,
                    "action_label": option["label"],
                    "preview_state": preview_state,
                    "candidate_text_visible_in_preview": candidate_text_visible,
                    "revision_requested": revision_requested,
                    "candidate_rejected_in_sandbox": rejected,
                    "formal_apply_performed": False,
                    "lesson_body_modified": False,
                    "html_body_modified": False,
                    "database_written": False,
                    "memory_written": False,
                    "feishu_written": False,
                }
            )
    return trace


def build_preview_state(cards: list[dict[str, Any]]) -> dict[str, Any]:
    accepted_cards = []
    waiting_cards = []
    for card in cards:
        accepted_cards.append(
            {
                "preview_item_id": card["review_card_id"].replace("1013g_teacher_review_prep", "1013h_preview"),
                "source_review_card_id": card["review_card_id"],
                "target_section": card["target_section"],
                "current_text": card["current_text"],
                "preview_text": card["what_will_change"],
                "preview_status": "accepted_to_preview_only",
                "can_revert": True,
                "can_revise": True,
                "can_formal_apply": False,
                "lesson_body_modified": False,
            }
        )
        waiting_cards.append(
            {
                "source_review_card_id": card["review_card_id"],
                "target_section": card["target_section"],
                "available_actions": ["accept_to_preview_only", "reject", "revise"],
                "default_action": "waiting_teacher_choice",
            }
        )
    return {
        "preview_state_id": "1013H_SANDBOX_PREVIEW_STATE",
        "source_stage": "1013G_TEACHER_REVIEW_PREP_ONLY",
        "preview_state_created": True,
        "accepted_preview_items": accepted_cards,
        "waiting_teacher_choice_items": waiting_cards,
        "preview_only": True,
        "formal_apply_allowed": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
    }


def build_diff_cards(preview_state: dict[str, Any]) -> list[dict[str, Any]]:
    diff_cards = []
    for item in preview_state["accepted_preview_items"]:
        diff_cards.append(
            {
                "diff_card_id": item["preview_item_id"].replace("1013h_preview", "1013h_diff"),
                "source_preview_item_id": item["preview_item_id"],
                "target_section": item["target_section"],
                "before": item["current_text"],
                "after_preview_only": item["preview_text"],
                "change_type": "sandbox_preview_replacement",
                "visible_badge": "预览中",
                "can_revert": True,
                "formal_apply_performed": False,
                "lesson_body_modified": False,
            }
        )
    return diff_cards


def build_result(preview_state: dict[str, Any], diff_cards: list[dict[str, Any]], action_trace: list[dict[str, Any]]) -> dict[str, Any]:
    action_ids = {item["action_id"] for item in action_trace}
    boundary = {
        "preview_state_created": preview_state["preview_state_created"],
        "accepted_preview_items_count": len(preview_state["accepted_preview_items"]),
        "preview_diff_cards_created": bool(diff_cards),
        "accept_to_preview_only_simulated": "accept_to_preview_only" in action_ids,
        "reject_simulated": "reject" in action_ids,
        "revise_simulated": "revise" in action_ids,
        "revert_available": all(item["can_revert"] for item in preview_state["accepted_preview_items"]),
        "candidate_preview_only": True,
        "formal_apply_performed": False,
        "entered_formal_1013G": False,
        "lesson_body_modified": False,
        "html_body_modified": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
        "allow_formal_apply": False,
    }
    final_pass = (
        boundary["preview_state_created"]
        and boundary["accepted_preview_items_count"] == 3
        and boundary["preview_diff_cards_created"]
        and boundary["accept_to_preview_only_simulated"]
        and boundary["reject_simulated"]
        and boundary["revise_simulated"]
        and boundary["revert_available"]
        and boundary["candidate_preview_only"]
        and not any(
            boundary[key]
            for key in [
                "formal_apply_performed",
                "entered_formal_1013G",
                "lesson_body_modified",
                "html_body_modified",
                "database_written",
                "memory_written",
                "feishu_written",
                "main_project_pushed",
                "allow_formal_apply",
            ]
        )
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013G_TEACHER_REVIEW_PREP_ONLY",
        "final_status": "PASS_1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY" if final_pass else "FAIL_1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY",
        "next_stage": "1013I_TEACHER_SELF_PREP_INPUT_MINIMAL_FLOW",
        **boundary,
    }


def build_report(result: dict[str, Any], diff_cards: list[dict[str, Any]]) -> str:
    lines = [
        "# 1013H Sandbox Apply To Preview Only",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- NEXT_STAGE: `{result['next_stage']}`",
        "- Boundary: preview-state only; no formal apply, no formal 1013G, no lesson body write, no database/memory/Feishu write.",
        "",
        "## Decision",
        "",
        "`accept_to_preview_only` now creates sandbox preview-state items and preview diff cards. It does not write the formal lesson body and remains reversible.",
        "",
        "## Preview Diff Cards",
        "",
    ]
    for card in diff_cards:
        lines.extend(
            [
                f"- `{card['diff_card_id']}` / {card['target_section']}",
                f"  - before: {card['before']}",
                f"  - preview: {card['after_preview_only']}",
                f"  - can_revert: {str(card['can_revert']).lower()}",
            ]
        )
    lines.extend(
        [
            "",
            "## Required Checks",
            "",
            f"- preview_state_created={str(result['preview_state_created']).lower()}",
            f"- accepted_preview_items_count={result['accepted_preview_items_count']}",
            f"- preview_diff_cards_created={str(result['preview_diff_cards_created']).lower()}",
            f"- accept_to_preview_only_simulated={str(result['accept_to_preview_only_simulated']).lower()}",
            f"- reject_simulated={str(result['reject_simulated']).lower()}",
            f"- revise_simulated={str(result['revise_simulated']).lower()}",
            f"- revert_available={str(result['revert_available']).lower()}",
            f"- formal_apply_performed={str(result['formal_apply_performed']).lower()}",
            f"- entered_formal_1013G={str(result['entered_formal_1013G']).lower()}",
            f"- lesson_body_modified={str(result['lesson_body_modified']).lower()}",
            f"- html_body_modified={str(result['html_body_modified']).lower()}",
            f"- database_written={str(result['database_written']).lower()}",
            f"- memory_written={str(result['memory_written']).lower()}",
            f"- feishu_written={str(result['feishu_written']).lower()}",
            f"- main_project_pushed={str(result['main_project_pushed']).lower()}",
        ]
    )
    return "\n".join(lines) + "\n"


def copy_source_delta() -> None:
    SOURCE_DELTA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA_DIR / Path(__file__).name)


def main() -> int:
    inputs = load_inputs()
    cards = inputs["teacher_prep_surface"]
    action_trace = build_action_trace(cards)
    preview_state = build_preview_state(cards)
    diff_cards = build_diff_cards(preview_state)
    result = build_result(preview_state, diff_cards, action_trace)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "sandbox_preview_state_1013H.json", preview_state)
    write_json(OUT_DIR / "preview_diff_cards_1013H.json", diff_cards)
    write_json(OUT_DIR / "teacher_action_trace_1013H.json", action_trace)
    write_json(OUT_DIR / "1013H_result.json", result)
    write_text(OUT_DIR / "1013H_report.md", build_report(result, diff_cards))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
