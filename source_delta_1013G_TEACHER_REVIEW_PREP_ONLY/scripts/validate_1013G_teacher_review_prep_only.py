from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
PREP_DIR = OUTPUT_ROOT / "1013G_PREP_candidate_review_sandbox"
OUT_DIR = OUTPUT_ROOT / "1013G_teacher_review_prep_only"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013G_TEACHER_REVIEW_PREP_ONLY" / "scripts"

STAGE_ID = "1013G_TEACHER_REVIEW_PREP_ONLY"


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
        "prep_result": read_json(PREP_DIR / "1013G_PREP_result.json"),
        "review_surface": read_json(PREP_DIR / "candidate_review_surface_1013G_PREP.json"),
    }


def build_teacher_review_prep_surface(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    surface = []
    for card in cards:
        surface.append(
            {
                "review_card_id": card["card_id"].replace("1013g_prep", "1013g_teacher_review_prep"),
                "source_card_id": card["card_id"],
                "target_section": card["target"],
                "what_will_change": card["candidate_adjustment"],
                "current_text": card["original_paragraph"],
                "why_suggested": card["why_this_change"],
                "risk_note": card["risk_note"],
                "teacher_action_options": [
                    {
                        "id": "accept_to_preview_only",
                        "label": "采纳到预览",
                        "effect": "create_preview_state_only",
                        "formal_apply_performed": False,
                        "lesson_body_modified": False,
                    },
                    {
                        "id": "reject",
                        "label": "暂不采用",
                        "effect": "mark_candidate_rejected_in_sandbox_only",
                        "formal_apply_performed": False,
                        "lesson_body_modified": False,
                    },
                    {
                        "id": "revise",
                        "label": "再改一版",
                        "effect": "request_revised_candidate_in_sandbox_only",
                        "formal_apply_performed": False,
                        "lesson_body_modified": False,
                    },
                ],
                "default_state": "waiting_teacher_review",
                "accept_to_preview_only": True,
                "formal_apply_allowed": False,
                "entered_formal_1013G": False,
            }
        )
    return surface


def build_result(inputs: dict[str, Any], surface: list[dict[str, Any]]) -> dict[str, Any]:
    prep_result = inputs["prep_result"]
    expected_count = int(prep_result.get("approved_candidates_loaded") or 0)
    teacher_action_options_present = all(
        {option["id"] for option in card["teacher_action_options"]}
        == {"accept_to_preview_only", "reject", "revise"}
        for card in surface
    )
    boundary = {
        "teacher_review_prep_surface_created": bool(surface),
        "candidate_cards_loaded": len(surface),
        "teacher_action_options_present": teacher_action_options_present,
        "accept_to_preview_only": all(card["accept_to_preview_only"] for card in surface),
        "reject_option_present": all(
            any(option["id"] == "reject" for option in card["teacher_action_options"]) for card in surface
        ),
        "revise_option_present": all(
            any(option["id"] == "revise" for option in card["teacher_action_options"]) for card in surface
        ),
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
        boundary["teacher_review_prep_surface_created"]
        and boundary["candidate_cards_loaded"] == expected_count
        and boundary["teacher_action_options_present"]
        and boundary["accept_to_preview_only"]
        and boundary["reject_option_present"]
        and boundary["revise_option_present"]
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
        "inherits_from": "1013G_PREP_CANDIDATE_REVIEW_SANDBOX",
        "final_status": "PASS_1013G_TEACHER_REVIEW_PREP_ONLY" if final_pass else "FAIL_1013G_TEACHER_REVIEW_PREP_ONLY",
        "next_stage": "1013H_SANDBOX_APPLY_TO_PREVIEW_ONLY",
        **boundary,
    }


def build_report(result: dict[str, Any], surface: list[dict[str, Any]]) -> str:
    lines = [
        "# 1013G Teacher Review Prep Only",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- NEXT_STAGE: `{result['next_stage']}`",
        "- Boundary: teacher-review preparation only; no formal 1013G, no formal apply, no lesson body write.",
        "",
        "## Decision",
        "",
        "This stage turns sandbox candidate cards into teacher-review preparation cards. The teacher actions are prepared as options only: accept to preview, reject, or revise. Accept to preview still means sandbox/preview state only.",
        "",
        "## Review Cards",
        "",
    ]
    for card in surface:
        action_ids = ", ".join(option["id"] for option in card["teacher_action_options"])
        lines.extend(
            [
                f"- `{card['review_card_id']}` / {card['target_section']}",
                f"  - current: {card['current_text']}",
                f"  - suggested: {card['what_will_change']}",
                f"  - actions: {action_ids}",
            ]
        )
    lines.extend(
        [
            "",
            "## Required Checks",
            "",
            f"- teacher_review_prep_surface_created={str(result['teacher_review_prep_surface_created']).lower()}",
            f"- candidate_cards_loaded={result['candidate_cards_loaded']}",
            f"- teacher_action_options_present={str(result['teacher_action_options_present']).lower()}",
            f"- accept_to_preview_only={str(result['accept_to_preview_only']).lower()}",
            f"- reject_option_present={str(result['reject_option_present']).lower()}",
            f"- revise_option_present={str(result['revise_option_present']).lower()}",
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
    surface = build_teacher_review_prep_surface(inputs["review_surface"])
    result = build_result(inputs, surface)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "teacher_review_prep_surface_1013G.json", surface)
    write_json(OUT_DIR / "1013G_teacher_review_prep_result.json", result)
    write_text(OUT_DIR / "1013G_teacher_review_prep_report.md", build_report(result, surface))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
