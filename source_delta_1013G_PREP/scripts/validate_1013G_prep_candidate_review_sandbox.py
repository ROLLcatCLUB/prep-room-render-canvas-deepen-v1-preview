from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
GATE_DIR = OUTPUT_ROOT / "1013F_R2D2_review_gate_before_1013G"
R2D2_DIR = OUTPUT_ROOT / "1013F_R2D2_case_reference_structure_assimilation"
HTML_PATH = OUTPUT_ROOT / "prep_room_render_canvas_deepen_v1.html"
OUT_DIR = OUTPUT_ROOT / "1013G_PREP_candidate_review_sandbox"
SOURCE_DELTA_DIR = OUTPUT_ROOT / "source_delta_1013G_PREP" / "scripts"

STAGE_ID = "1013G_PREP_CANDIDATE_REVIEW_SANDBOX"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_inputs() -> dict[str, Any]:
    return {
        "approved": read_json(GATE_DIR / "approved_candidate_moves.json"),
        "rejected": read_json(GATE_DIR / "rejected_candidate_moves.json"),
        "gate_result": read_json(GATE_DIR / "R2D2_review_gate_result.json"),
        "r2d2_patches": read_json(R2D2_DIR / "assimilation_candidate_patch_1013F_R2D2.json"),
        "moves": read_json(R2D2_DIR / "teaching_moves_extraction_1013F_R2D2.json"),
        "html": read_text(HTML_PATH),
    }


def extract_current_baseline(html: str, target: str) -> str:
    target_to_step = {
        "教学过程 · 探究": "explore",
        "教学过程 · 表现": "make",
        "教学过程 · 交流展示": "share",
    }
    step_id = target_to_step.get(target)
    if not step_id:
        return ""
    pattern = rf'id:\s*"{step_id}"[\s\S]*?summary:\s*"([^"]+)"'
    match = re.search(pattern, html)
    return match.group(1) if match else ""


def build_review_surface(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    html = inputs["html"]
    patch_by_id = {item["patch_id"]: item for item in inputs["r2d2_patches"]}
    move_by_id = {item["move_id"]: item for item in inputs["moves"]}
    cards = []
    for approved in inputs["approved"]:
        patch = patch_by_id[approved["patch_id"]]
        source_moves = [move_by_id[move_id] for move_id in patch.get("source_move_ids", []) if move_id in move_by_id]
        cards.append(
            {
                "card_id": f"1013g_prep_card_{len(cards) + 1:02d}",
                "source_patch_id": patch["patch_id"],
                "target": patch["target"],
                "status": "sandbox_preview_only",
                "original_paragraph": extract_current_baseline(html, patch["target"]),
                "candidate_adjustment": patch["candidate_text"],
                "why_this_change": patch["why"],
                "risk_note": patch["risk"],
                "source_move_ids": patch["source_move_ids"],
                "source_move_types": [move.get("move_type") for move in source_moves],
                "teacher_action_placeholder": {
                    "can_preview": True,
                    "action_options": ["accept_to_preview_only", "reject", "revise"],
                    "can_accept_now": False,
                    "can_apply_now": False,
                    "required_next_stage": "1013G_TEACHER_REVIEW_PREP_ONLY",
                },
                "boundary_flags": {
                    "candidate_preview_only": True,
                    "lesson_body_modified": False,
                    "html_body_modified": False,
                    "teacher_review_required": True,
                    "formal_apply_performed": False,
                    "entered_1013G": False,
                },
            }
        )
    return cards


def build_result(inputs: dict[str, Any], review_surface: list[dict[str, Any]]) -> dict[str, Any]:
    gate_result = inputs["gate_result"]
    approved_count = int(gate_result.get("approved_candidate_count") or 0)
    boundary = {
        "sandbox_preview_created": bool(review_surface),
        "approved_candidates_loaded": len(review_surface),
        "candidate_preview_only": all(card["boundary_flags"]["candidate_preview_only"] for card in review_surface),
        "lesson_body_modified": False,
        "html_body_modified": False,
        "teacher_review_required": all(card["boundary_flags"]["teacher_review_required"] for card in review_surface),
        "formal_apply_performed": False,
        "entered_1013G": False,
        "database_written": False,
        "memory_written": False,
        "feishu_written": False,
        "main_project_pushed": False,
        "allow_formal_apply": False,
        "allow_enter_1013G_now": False,
    }
    final_pass = (
        boundary["sandbox_preview_created"]
        and boundary["approved_candidates_loaded"] == approved_count
        and boundary["candidate_preview_only"]
        and boundary["teacher_review_required"]
        and not any(
            boundary[key]
            for key in [
                "lesson_body_modified",
                "html_body_modified",
                "formal_apply_performed",
                "entered_1013G",
                "database_written",
                "memory_written",
                "feishu_written",
                "main_project_pushed",
                "allow_formal_apply",
                "allow_enter_1013G_now",
            ]
        )
    )
    return {
        "stage": STAGE_ID,
        "generated_at": now(),
        "inherits_from": "1013F_R2D2_REVIEW_GATE_BEFORE_1013G",
        "final_status": "PASS_1013G_PREP_CANDIDATE_REVIEW_SANDBOX" if final_pass else "FAIL_1013G_PREP_CANDIDATE_REVIEW_SANDBOX",
        "next_stage": "1013G_TEACHER_REVIEW_PREP_ONLY",
        "review_surface_card_count": len(review_surface),
        **boundary,
    }


def build_report(result: dict[str, Any], review_surface: list[dict[str, Any]]) -> str:
    lines = [
        "# 1013G PREP Candidate Review Sandbox",
        "",
        f"- FINAL_STATUS: `{result['final_status']}`",
        f"- NEXT_STAGE: `{result['next_stage']}`",
        "- Boundary: sandbox preview only; no formal 1013G, no apply, no HTML body modification, no database/memory/Feishu write.",
        "",
        "## Decision",
        "",
        "The approved R2D2 candidates were loaded into a teacher-review sandbox data surface. This stage previews candidate cards only. It does not confirm, apply, merge, or write lesson text.",
        "",
        "## Preview Cards",
        "",
    ]
    for card in review_surface:
        lines.extend(
            [
                f"- `{card['card_id']}` / {card['target']}",
                f"  - 原段落: {card['original_paragraph']}",
                f"  - 候选调整: {card['candidate_adjustment']}",
                f"  - 风险提示: {card['risk_note']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Required Checks",
            "",
            f"- sandbox_preview_created={str(result['sandbox_preview_created']).lower()}",
            f"- approved_candidates_loaded={result['approved_candidates_loaded']}",
            f"- candidate_preview_only={str(result['candidate_preview_only']).lower()}",
            f"- lesson_body_modified={str(result['lesson_body_modified']).lower()}",
            f"- html_body_modified={str(result['html_body_modified']).lower()}",
            f"- teacher_review_required={str(result['teacher_review_required']).lower()}",
            f"- formal_apply_performed={str(result['formal_apply_performed']).lower()}",
            f"- entered_1013G={str(result['entered_1013G']).lower()}",
            f"- database_written={str(result['database_written']).lower()}",
            f"- memory_written={str(result['memory_written']).lower()}",
            f"- feishu_written={str(result['feishu_written']).lower()}",
            f"- main_project_pushed={str(result['main_project_pushed']).lower()}",
            "",
            "## Boundary",
            "",
            "- Teacher action controls remain placeholders.",
            "- Accept/apply buttons are not enabled in this data surface.",
            "- A later decision stage must decide whether any candidate can enter real 1013G work.",
        ]
    )
    return "\n".join(lines) + "\n"


def copy_source_delta() -> None:
    SOURCE_DELTA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__), SOURCE_DELTA_DIR / Path(__file__).name)


def main() -> int:
    inputs = load_inputs()
    review_surface = build_review_surface(inputs)
    result = build_result(inputs, review_surface)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "candidate_review_surface_1013G_PREP.json", review_surface)
    write_json(OUT_DIR / "1013G_PREP_result.json", result)
    write_text(OUT_DIR / "1013G_PREP_report.md", build_report(result, review_surface))
    copy_source_delta()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["final_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
